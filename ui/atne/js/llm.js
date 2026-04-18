/**
 * ATNE · mòdul de comunicació amb el backend LLM
 *
 * Exposa window.ATNE_LLM amb funcions per adaptar, refinar, generar, extreure.
 * El backend aplica rotació silenciosa de models configurada a /admin
 * (Gemma 3 27B + GPT-4o + GPT-4.1-mini per a adapt/generate/complements;
 * Gemma 3 27B fix per a refine; GPT-4o-mini fix per a auditor).
 *
 * Format dels events SSE de /api/adapt (veure server.py:4071):
 *   { type: "step", step: "...", msg: "Missatge", level: "..." }
 *   { type: "result", adapted: "Text adaptat...", quality_report: {...}, level: "..." }
 *   { type: "done_level", level: "..." }
 *   { type: "done", total_levels: N }
 */
(function () {
  'use strict';

  // Mapeig del nostre model simplificat (pas1 PROFILES) al format que espera
  // el backend (server.py → run_adaptation → build_system_prompt).
  // Les claus de 'caracteristiques' han de coincidir amb les del catàleg;
  // usem les 4 principals que ja fem servir al front (tdah/disl/cat/ac).
  const CAT_TO_CHAR = {
    tdah: 'TDAH',
    disl: 'DISLEXIA',
    cat:  'CAT_L2',
    ac:   'AACC'
  };
  const ALL_CHAR_KEYS = ['TDAH', 'DISLEXIA', 'CAT_L2', 'AACC', 'TEA', 'DI', 'AUD', 'VIS'];

  /**
   * Converteix el profile simple del nostre front al format dict que espera
   * el backend a /api/adapt.
   * @param {Object} p  Perfil de window.ATNE_PROFILES (marc/mireia/...).
   * @returns {Object}  Dict amb {nom, caracteristiques, canal_preferent, ...}
   */
  function buildBackendProfile(p) {
    const caracteristiques = {};
    // Totes les característiques inicialitzades a actiu=false (requisit backend)
    ALL_CHAR_KEYS.forEach(k => { caracteristiques[k] = { actiu: false }; });
    // Activem la característica principal del perfil
    const mainChar = CAT_TO_CHAR[p.cat];
    if (mainChar) caracteristiques[mainChar] = { actiu: true };
    // Cas especial Anna: TDAH + Dislèxia. Detectem-ho per l'id.
    if (p.id === 'anna') {
      caracteristiques['TDAH'] = { actiu: true };
      caracteristiques['DISLEXIA'] = { actiu: true };
    }
    return {
      nom: p.name,
      caracteristiques,
      canal_preferent: 'text',
      observacions: (p.behaviors || []).join(' · '),
      _via: 'diagnostic'
    };
  }

  /**
   * Construeix el dict 'context' que acompanya el profile.
   * @param {Object} opts  { materia, nivell_curs, titol }
   */
  function buildBackendContext(opts) {
    return {
      materia: opts.materia || 'Història',
      nivell_curs: opts.nivell_curs || 'ESO',
      titol: opts.titol || ''
    };
  }

  /**
   * Crida /api/adapt amb streaming SSE i invoca callbacks durant la generació.
   *
   * @param {Object} args
   * @param {string} args.text  Text original a adaptar.
   * @param {Object} args.profile  Perfil del nostre model (window.ATNE_PROFILES[id]).
   * @param {Object} args.context  { materia, nivell_curs, titol }
   * @param {Object} [args.params]  { mecr_sortida: "B1", levels: ["single"], ... }
   * @param {Function} [args.onStep]  (ev) => void  Callback per events de progrés.
   * @param {Function} [args.onResult]  (ev) => void  Callback quan arriba una versió.
   * @param {Function} [args.onError]  (err) => void
   * @returns {Promise<{versions: Object, done: boolean}>}
   */
  async function adaptText({ text, profile, context, params = {}, onStep, onResult, onError }) {
    if (!text || !text.trim()) throw new Error('Text buit');

    const backendProfile = buildBackendProfile(profile);
    const backendContext = buildBackendContext(context);
    const backendParams = {
      mecr_sortida: params.mecr_sortida || 'B1',
      levels: params.levels || ['single'],
      ...params
    };

    const resp = await fetch('/api/adapt', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text,
        profile: backendProfile,
        context: backendContext,
        params: backendParams
        // 'model' omès → backend aplica rotació configurada a /admin
      })
    });

    if (!resp.ok) {
      const err = new Error('HTTP ' + resp.status);
      if (onError) onError(err);
      throw err;
    }

    const reader = resp.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    const versions = {};

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop();
      for (const line of lines) {
        if (!line.startsWith('data: ')) continue;
        let ev;
        try { ev = JSON.parse(line.slice(6)); } catch { continue; }

        if (ev.type === 'step' && onStep) {
          onStep(ev);
        } else if (ev.type === 'result') {
          const lvl = ev.level || 'single';
          versions[lvl] = {
            adapted: ev.adapted,
            quality_report: ev.quality_report || null,
            model_used: ev.model_used || null
          };
          if (onResult) onResult(ev);
        } else if (ev.type === 'done_level' && onStep) {
          onStep(ev);
        } else if (ev.type === 'done') {
          return { versions, done: true };
        }
      }
    }
    return { versions, done: false };
  }

  /**
   * Crida /api/refine-text (síncron, sense SSE) — modifica un text existent.
   *
   * El backend accepta un 'preset' de la llista fixa (catala | simplificar |
   * ampliar | escurcar) i/o una 'instruccio' lliure. Si s'envien tots dos,
   * el preset s'aplica primer i la instruccio s'hi afegeix.
   *
   * 'catala' aplica LanguageTool (determinista, no LLM); la resta passen
   * pel LLM fix configurat a /admin (actualment Gemma 3 27B).
   *
   * @param {Object} args
   * @param {string} args.text  Text a refinar.
   * @param {string} [args.preset]  'catala' | 'simplificar' | 'ampliar' | 'escurcar'
   * @param {string} [args.instruccio]  Instrucció lliure del docent.
   * @returns {Promise<{text: string, paraules: number, ...}>}
   */
  async function refineText({ text, preset, instruccio, onError }) {
    if (!text || !text.trim()) throw new Error('Text buit');
    const body = { text };
    if (preset) body.preset = preset;
    if (instruccio) body.instruccio = instruccio;
    const resp = await fetch('/api/refine-text', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    });
    if (!resp.ok) {
      let errMsg = 'HTTP ' + resp.status;
      try { const e = await resp.json(); if (e.error) errMsg = e.error; } catch {}
      const err = new Error(errMsg);
      if (onError) onError(err);
      throw err;
    }
    return resp.json();
  }

  /**
   * Crida /api/generate-text — genera un text base segons context.
   *
   * Payload backend: { tema, genere, tipologia, to, extensio, notes?, context? }.
   * El backend delega al mòdul generador_lliure.py i aplica la rotació de
   * models configurada a /admin (Gemma 3 27B + GPT-4o + GPT-4.1-mini).
   *
   * @returns {Promise<{text: string, ...}>}
   */
  async function generateText({ tema, genere, tipologia, to, extensio, notes, context }) {
    if (!tema || !tema.trim()) throw new Error('Cal un tema per generar el text');
    const body = { tema, genere, tipologia, to, extensio };
    if (notes) body.notes = notes;
    if (context) body.context = context;
    const resp = await fetch('/api/generate-text', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    });
    if (!resp.ok) {
      let errMsg = 'HTTP ' + resp.status;
      try { const e = await resp.json(); if (e.error) errMsg = e.error; } catch {}
      throw new Error(errMsg);
    }
    return resp.json();
  }

  /**
   * Crida /api/extract-text — pujada d'un fitxer (PDF/DOCX/MD/TXT, màx 5 MB)
   * i retorna el text pla extret.
   *
   * @param {File} file  Objecte File del <input type="file">
   * @returns {Promise<{text: string, paraules?: number, ...}>}
   */
  async function extractFile(file) {
    if (!file) throw new Error('Cap fitxer');
    const form = new FormData();
    form.append('file', file);
    const resp = await fetch('/api/extract-text', { method: 'POST', body: form });
    if (!resp.ok) {
      let errMsg = 'HTTP ' + resp.status;
      try { const e = await resp.json(); if (e.error) errMsg = e.error; } catch {}
      throw new Error(errMsg);
    }
    return resp.json();
  }

  /**
   * Crida /api/history — llista les últimes adaptacions desades.
   *
   * @param {number} [limit=30]
   * @returns {Promise<{ok: boolean, items: Array<{id, created_at, profile_name,
   *   original_text, adapted_text, ...}>}>}
   */
  async function listHistory(limit = 30) {
    const resp = await fetch('/api/history?limit=' + encodeURIComponent(limit));
    if (!resp.ok) throw new Error('HTTP ' + resp.status);
    return resp.json();
  }

  /**
   * Crida /api/export — genera un fitxer del text adaptat i el descarrega.
   *
   * Formats suportats al backend: 'pdf', 'docx', 'txt'. Google Docs i imatge
   * no estan implementats (el backend retornarà error).
   *
   * @param {Object} args
   * @param {string} args.format  'pdf' | 'docx' | 'txt'
   * @param {string} args.adapted  HTML o text pla del document adaptat.
   * @param {string} [args.original]  Text original (opcional, per adjuntar).
   * @param {string} [args.profile_name]  Nom del perfil (per al nom del fitxer).
   * @returns {Promise<void>}  Dispara la descàrrega al navegador.
   */
  async function exportDoc({ format, adapted, original = '', profile_name = 'adaptacio' }) {
    if (!adapted || !adapted.trim()) throw new Error('No hi ha text per exportar');
    if (!['pdf', 'docx', 'txt'].includes(format)) throw new Error('Format no suportat: ' + format);
    const resp = await fetch('/api/export', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ format, adapted, original, profile_name })
    });
    if (!resp.ok) {
      let errMsg = 'HTTP ' + resp.status;
      try { const e = await resp.json(); if (e.error) errMsg = e.error; } catch {}
      throw new Error(errMsg);
    }
    // El backend retorna el fitxer com a attachment; llegim el blob i disparem descàrrega
    const blob = await resp.blob();
    const cd = resp.headers.get('Content-Disposition') || '';
    const match = cd.match(/filename="?([^"]+)"?/);
    const fname = match ? match[1] : 'ATNE_' + format + '.' + format;
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = fname;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  }

  // ──────────────────────────────────────────────────────
  // Toast compartit — notificacions no bloquejants
  // ──────────────────────────────────────────────────────
  let toastEl = null;
  function ensureToastEl() {
    if (toastEl) return toastEl;
    toastEl = document.createElement('div');
    toastEl.id = 'atne-toast';
    toastEl.style.cssText = [
      'position:fixed', 'bottom:24px', 'left:50%', 'transform:translateX(-50%)',
      'background:var(--ink-900)', 'color:#fff', 'padding:10px 18px',
      'border-radius:var(--r-md)', 'box-shadow:var(--sh-lg)', 'font-size:13px',
      'font-family:var(--ui)', 'font-weight:500', 'z-index:9999',
      'opacity:0', 'pointer-events:none', 'transition:opacity .2s',
      'max-width:calc(100vw - 32px)', 'text-align:center'
    ].join(';');
    document.body.appendChild(toastEl);
    return toastEl;
  }
  function atneToast(msg, type = 'info') {
    const el = ensureToastEl();
    el.textContent = msg;
    if (type === 'error') el.style.background = 'var(--danger)';
    else if (type === 'success') el.style.background = 'var(--ok)';
    else el.style.background = 'var(--ink-900)';
    el.style.opacity = '1';
    clearTimeout(el._t);
    el._t = setTimeout(() => { el.style.opacity = '0'; }, 3500);
  }
  window.atneToast = atneToast;

  window.ATNE_LLM = {
    adaptText,
    refineText,
    generateText,
    extractFile,
    listHistory,
    exportDoc,
    buildBackendProfile,
    buildBackendContext
  };
})();
