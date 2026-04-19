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
  // el backend (instruction_catalog.py → PROFILE_INSTRUCTION_MAP + camps "profiles"
  // de les instruccions PERFIL). Les claus HAN de coincidir exactament amb les
  // que usa el filtre: minúscules i noms canònics (no sigles majúscules).
  const CAT_TO_CHAR = {
    tdah: 'tdah',
    disl: 'dislexia',
    cat:  'nouvingut',
    ac:   'altes_capacitats'
  };
  const ALL_CHAR_KEYS = [
    'tdah', 'dislexia', 'nouvingut', 'altes_capacitats',
    'tea', 'di', 'discapacitat_auditiva', 'discapacitat_visual'
  ];

  // Timeout per defecte de les crides SSE (3 min). Si el backend no respon
  // en aquest temps, es cancel·la la petició per no deixar el loader penjat.
  const SSE_TIMEOUT_MS = 180000;

  // Combina un AbortSignal de l'usuari amb un timeout. Usa AbortSignal.any
  // si està disponible (Chrome 116+/FF 124+), si no, fa fallback manual.
  function combineSignals(userSignal, timeoutMs) {
    const timeoutSignal = (typeof AbortSignal !== 'undefined' && AbortSignal.timeout)
      ? AbortSignal.timeout(timeoutMs)
      : null;
    if (!userSignal && timeoutSignal) return timeoutSignal;
    if (userSignal && !timeoutSignal) return userSignal;
    if (!userSignal && !timeoutSignal) return undefined;
    if (AbortSignal.any) return AbortSignal.any([userSignal, timeoutSignal]);
    // Fallback: controller que es cancel·la quan qualsevol dels dos ho fa
    const ctrl = new AbortController();
    const abort = () => ctrl.abort();
    if (userSignal.aborted || timeoutSignal.aborted) ctrl.abort();
    else {
      userSignal.addEventListener('abort', abort, { once: true });
      timeoutSignal.addEventListener('abort', abort, { once: true });
    }
    return ctrl.signal;
  }

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
      caracteristiques['tdah'] = { actiu: true };
      caracteristiques['dislexia'] = { actiu: true };
    }
    // Perfils de grup: el 'cat' del perfil és 'group|group-ac|group-cat' i no casa
    // amb CAT_TO_CHAR. Cal recórrer els chips i activar cada característica trobada.
    const isGroup = p.type === 'group' || (p.cat && p.cat.indexOf('group') === 0);
    if (isGroup && Array.isArray(p.chips)) {
      for (const chip of p.chips) {
        const c = CAT_TO_CHAR[chip && chip.cat];
        if (c) caracteristiques[c] = { actiu: true };
      }
    }
    return {
      nom: p.name,
      caracteristiques,
      canal_preferent: 'text',
      observacions: (p.behaviors || []).join(' · '),
      _via: 'diagnostic',
      // Flag informatiu (el backend l'ignora, útil per debugging al dashboard /admin)
      group: !!isGroup
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
   * @param {AbortSignal} [args.signal]  Opcional. Si es dispara, es cancel·la la SSE.
   *   Internament es combina amb un timeout de 180s per evitar loaders penjats.
   * @returns {Promise<{versions: Object, done: boolean}>}
   */
  async function adaptText({ text, profile, context, params = {}, onStep, onResult, onError, signal }) {
    if (!text || !text.trim()) throw new Error('Text buit');

    const backendProfile = buildBackendProfile(profile);
    const backendContext = buildBackendContext(context);
    const backendParams = {
      mecr_sortida: params.mecr_sortida || 'B1',
      levels: params.levels || ['single'],
      ...params
    };

    const combinedSignal = combineSignals(signal, SSE_TIMEOUT_MS);
    const resp = await fetch('/api/adapt', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text,
        profile: backendProfile,
        context: backendContext,
        params: backendParams
        // 'model' omès → backend aplica rotació configurada a /admin
      }),
      signal: combinedSignal
    });

    if (!resp.ok) {
      // Mirem de llegir el cos JSON per obtenir el missatge real del backend
      // (mateix patró que refineText/generateText/extractFile).
      let errMsg = 'HTTP ' + resp.status;
      try { const e = await resp.json(); if (e && e.error) errMsg = e.error; } catch {}
      const err = new Error(errMsg);
      if (onError) onError(err);
      throw err;
    }

    const reader = resp.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    const versions = {};

    try {
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
    } catch (e) {
      // Si la cancel·lació arriba enmig (fetch/read llança AbortError) la
      // propaguem; si ja teníem 'done', el break superior ens hauria tret.
      if (e && (e.name === 'AbortError' || e.name === 'TimeoutError')) {
        if (onError) onError(e);
        throw e;
      }
      throw e;
    }
    return { versions, done: false };
  }

  // ──────────────────────────────────────────────────────
  // Conversió HTML ↔ Markdown per preservar format als refinaments
  // (negretes, cursives, títols, llistes). Les marques de diff
  // (.ins / .sub) es perden en refinar — comportament esperat: un
  // refine és un retoc, no un re-adapt.
  // ──────────────────────────────────────────────────────
  function htmlToMarkdown(html) {
    if (!html) return '';
    let md = html;
    md = md.replace(/<h1[^>]*>([\s\S]*?)<\/h1>/gi, '\n# $1\n');
    md = md.replace(/<h2[^>]*>([\s\S]*?)<\/h2>/gi, '\n## $1\n');
    md = md.replace(/<h3[^>]*>([\s\S]*?)<\/h3>/gi, '\n### $1\n');
    md = md.replace(/<strong[^>]*>([\s\S]*?)<\/strong>/gi, '**$1**');
    md = md.replace(/<b[^>]*>([\s\S]*?)<\/b>/gi, '**$1**');
    md = md.replace(/<em[^>]*>([\s\S]*?)<\/em>/gi, '_$1_');
    md = md.replace(/<i[^>]*>([\s\S]*?)<\/i>/gi, '_$1_');
    // <u> no té equivalent a CommonMark pur: fem servir __text__ (CommonMark
    // extended / GFM). Els exportadors PDF/DOCX del backend ho tornaran a negreta
    // subratllada o a negreta simple segons pipeline; no perdem el contingut.
    md = md.replace(/<u[^>]*>([\s\S]*?)<\/u>/gi, '__$1__');
    // Taules: conversió simple a format pipe. Només gestiona <tr>/<td>/<th>
    // directes; taules amb colspan/rowspan o <thead>/<tbody> niats no es
    // representen correctament — s'hi perd l'estructura però el text es manté.
    md = md.replace(/<table[^>]*>([\s\S]*?)<\/table>/gi, (m, content) => {
      const rows = [];
      const rowRe = /<tr[^>]*>([\s\S]*?)<\/tr>/gi;
      let rm;
      while ((rm = rowRe.exec(content)) !== null) {
        const cellRe = /<(?:th|td)[^>]*>([\s\S]*?)<\/(?:th|td)>/gi;
        const cells = [];
        let cm;
        while ((cm = cellRe.exec(rm[1])) !== null) {
          // Netegem tags interiors per no trencar la pipe
          cells.push(cm[1].replace(/<\/?[a-z][^>]*>/gi, '').replace(/\|/g, '\\|').trim());
        }
        if (cells.length) rows.push('| ' + cells.join(' | ') + ' |');
      }
      if (!rows.length) return '\n';
      // Separador de capçalera (Markdown pipe): si hi ha ≥1 fila, la 1a es tracta com header
      const sep = '| ' + rows[0].split('|').slice(1, -1).map(() => '---').join(' | ') + ' |';
      return '\n' + rows[0] + '\n' + sep + '\n' + rows.slice(1).join('\n') + '\n';
    });
    md = md.replace(/<ul[^>]*>([\s\S]*?)<\/ul>/gi, (m, c) => '\n' + c.replace(/<li[^>]*>([\s\S]*?)<\/li>/gi, '- $1\n') + '\n');
    // NOTA: llistes niades no es recursionen — el niat queda com a llista plana.
    // Per a l'MVP del pilot és acceptable; millora pendent.
    md = md.replace(/<ol[^>]*>([\s\S]*?)<\/ol>/gi, (m, c) => {
      let n = 0;
      return '\n' + c.replace(/<li[^>]*>([\s\S]*?)<\/li>/gi, (_, x) => { n++; return n + '. ' + x + '\n'; }) + '\n';
    });
    md = md.replace(/<p[^>]*>([\s\S]*?)<\/p>/gi, '$1\n\n');
    // <div> com a paràgraf (dues newlines per separar)
    md = md.replace(/<div[^>]*>([\s\S]*?)<\/div>/gi, '$1\n\n');
    md = md.replace(/<br\s*\/?>/gi, '\n');
    // Spans (ins/sub, marques de diff i altres): mantenim el contingut pla
    md = md.replace(/<span[^>]*>([\s\S]*?)<\/span>/gi, '$1');
    // Treure qualsevol tag restant
    md = md.replace(/<\/?[a-z][^>]*>/gi, '');
    md = md.replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'");
    md = md.replace(/\n{3,}/g, '\n\n');
    return md.trim();
  }

  function markdownToHtml(md) {
    if (!md) return '';
    const lines = md.split('\n');
    const out = [];
    let inList = false;
    let listTag = 'ul';
    const inline = s => s
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      .replace(/(^|[\s(])_([^_]+)_/g, '$1<em>$2</em>');
    for (let line of lines) {
      line = line.trim();
      const h1 = line.match(/^#\s+(.+)$/);
      const h2 = line.match(/^##\s+(.+)$/);
      const h3 = line.match(/^###\s+(.+)$/);
      if (h1) { if (inList) { out.push('</' + listTag + '>'); inList = false; } out.push('<h1>' + inline(h1[1]) + '</h1>'); continue; }
      if (h2) { if (inList) { out.push('</' + listTag + '>'); inList = false; } out.push('<h2>' + inline(h2[1]) + '</h2>'); continue; }
      if (h3) { if (inList) { out.push('</' + listTag + '>'); inList = false; } out.push('<h3>' + inline(h3[1]) + '</h3>'); continue; }
      const liUl = line.match(/^-\s+(.+)$/);
      const liOl = line.match(/^(\d+)\.\s+(.+)$/);
      if (liUl) {
        if (!inList || listTag === 'ol') { if (inList) out.push('</' + listTag + '>'); out.push('<ul>'); listTag = 'ul'; inList = true; }
        out.push('<li>' + inline(liUl[1]) + '</li>');
        continue;
      }
      if (liOl) {
        if (!inList || listTag === 'ul') { if (inList) out.push('</' + listTag + '>'); out.push('<ol>'); listTag = 'ol'; inList = true; }
        out.push('<li>' + inline(liOl[2]) + '</li>');
        continue;
      }
      if (inList) { out.push('</' + listTag + '>'); inList = false; }
      if (!line) continue;
      out.push('<p>' + inline(line) + '</p>');
    }
    if (inList) out.push('</' + listTag + '>');
    return out.join('\n');
  }

  // Instrucció sistemàtica que s'afegeix a tots els refinaments per preservar format
  const PRESERVE_FORMAT_INSTRUCTION =
    'IMPORTANT — conserva les marques de format del text original: ' +
    'negretes amb **...**, títols amb # o ##, cursives amb _..._, llistes amb - o 1. 2.. ' +
    'Mantén els termes tècnics en **negreta**, les definicions entre parèntesis, ' +
    'i les traduccions [entre claudators] si n\'hi ha. No eliminis aquestes marques.';

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
    // Afegim sempre la instrucció de preservar format (a més de la del docent),
    // excepte per al preset 'catala' que és LanguageTool determinista (no passa pel LLM)
    if (preset !== 'catala') {
      const combined = instruccio
        ? instruccio + ' ' + PRESERVE_FORMAT_INSTRUCTION
        : PRESERVE_FORMAT_INSTRUCTION;
      body.instruccio = combined;
    } else if (instruccio) {
      body.instruccio = instruccio;
    }
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
   * Variant streaming de generateText (SSE).
   *
   * @param {Object} args  Mateixos camps que generateText + callbacks:
   * @param {Function} [args.onStart]  ({model, target_words}) => void
   * @param {Function} [args.onChunk]  ({text, acumulat}) => void   (el text és el delta)
   * @param {Function} [args.onDone]   ({text, paraules, duration_ms, model}) => void
   * @param {Function} [args.onError]  (err) => void
   * @param {AbortSignal} [args.signal]  Opcional. Si es dispara, es cancel·la la SSE.
   *   Internament es combina amb un timeout de 180s.
   * @returns {Promise<{text: string, paraules: number, model: string}>}  Resultat final.
   */
  async function generateTextStream({ tema, genere, tipologia, to, extensio, notes, context, onStart, onChunk, onDone, onError, signal }) {
    if (!tema || !tema.trim()) throw new Error('Cal un tema per generar el text');
    const body = { tema, genere, tipologia, to, extensio };
    if (notes) body.notes = notes;
    if (context) body.context = context;
    const combinedSignal = combineSignals(signal, SSE_TIMEOUT_MS);
    const resp = await fetch('/api/generate-text-stream', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
      signal: combinedSignal
    });
    if (!resp.ok) {
      // Patró coherent amb la resta: intentem llegir .error del JSON
      let errMsg = 'HTTP ' + resp.status;
      try { const e = await resp.json(); if (e && e.error) errMsg = e.error; } catch {}
      const err = new Error(errMsg);
      if (onError) onError(err);
      throw err;
    }
    const reader = resp.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    let acumulat = '';
    let final = null;
    try {
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
          if (ev.type === 'start' && onStart) {
            onStart(ev);
          } else if (ev.type === 'chunk') {
            acumulat += (ev.text || '');
            if (onChunk) onChunk({ text: ev.text || '', acumulat });
          } else if (ev.type === 'done') {
            final = ev;
            if (onDone) onDone(ev);
          } else if (ev.type === 'error') {
            const err = new Error(ev.message || 'Error stream');
            if (onError) onError(err);
            throw err;
          }
        }
      }
    } catch (e) {
      if (e && (e.name === 'AbortError' || e.name === 'TimeoutError')) {
        if (onError) onError(e);
        throw e;
      }
      throw e;
    }
    return final || { text: acumulat, paraules: 0, model: '' };
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

  // ──────────────────────────────────────────────────────
  // Esborranys desats al servidor (taula `drafts` de Supabase)
  //
  // Permet desar el text del Pas 2 abans d'adaptar-lo, de manera que no
  // es perdi si el docent tanca el navegador o canvia de dispositiu. El
  // docent s'identifica amb un UUID anònim (`atne.docent_id`) persistit
  // al localStorage — no és auth real, però evita barrejar drafts entre
  // dispositius i dóna una primera capa d'aïllament fins que tinguem IAP.
  // ──────────────────────────────────────────────────────

  /**
   * Retorna l'identificador anònim del docent (per desar/recuperar drafts).
   * El genera la primera vegada i el persisteix a localStorage.
   */
  function getDocentId() {
    let id = localStorage.getItem('atne.docent_id');
    if (!id) {
      id = 'doc_' + (crypto.randomUUID
        ? crypto.randomUUID()
        : Math.random().toString(36).slice(2) + Date.now());
      localStorage.setItem('atne.docent_id', id);
    }
    return id;
  }

  /**
   * Crida POST /api/drafts — desa un esborrany (crea o actualitza).
   * Si es passa `id`, fa UPDATE; altrament INSERT.
   *
   * @param {Object} args  { id?, profile_id?, title?, text, materia?, nivell? }
   * @returns {Promise<{ok: boolean, id: number, updated_at: string}>}
   */
  async function saveDraft({ id, profile_id, title, text, materia, nivell } = {}) {
    if (!text || !text.trim()) throw new Error('Text buit');
    const body = {
      docent_id: getDocentId(),
      text,
      profile_id: profile_id || null,
      title: title || null,
      materia: materia || null,
      nivell: nivell || null
    };
    if (id) body.id = id;
    const resp = await fetch('/api/drafts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    });
    if (!resp.ok) {
      let errMsg = 'HTTP ' + resp.status;
      try { const e = await resp.json(); if (e && e.error) errMsg = e.error; } catch {}
      throw new Error(errMsg);
    }
    return resp.json();
  }

  /**
   * Crida GET /api/drafts — llista els esborranys del docent actual.
   *
   * @param {number} [limit=20]
   * @returns {Promise<{ok: boolean, items: Array<{id, profile_id, title,
   *   text_preview, materia, nivell, created_at, updated_at}>}>}
   */
  async function listDrafts(limit = 20) {
    const qs = 'docent_id=' + encodeURIComponent(getDocentId())
             + '&limit=' + encodeURIComponent(limit);
    const resp = await fetch('/api/drafts?' + qs);
    if (!resp.ok) {
      let errMsg = 'HTTP ' + resp.status;
      try { const e = await resp.json(); if (e && e.error) errMsg = e.error; } catch {}
      throw new Error(errMsg);
    }
    return resp.json();
  }

  /**
   * Crida GET /api/drafts/{id} — recupera un draft complet.
   *
   * @param {number} id
   * @returns {Promise<{ok: boolean, item: {id, profile_id, title, text,
   *   materia, nivell, created_at, updated_at}}>}
   */
  async function getDraft(id) {
    if (!id) throw new Error('Cal id');
    const qs = 'docent_id=' + encodeURIComponent(getDocentId());
    const resp = await fetch('/api/drafts/' + encodeURIComponent(id) + '?' + qs);
    if (!resp.ok) {
      let errMsg = 'HTTP ' + resp.status;
      try { const e = await resp.json(); if (e && e.error) errMsg = e.error; } catch {}
      throw new Error(errMsg);
    }
    return resp.json();
  }

  /**
   * Crida DELETE /api/drafts/{id} — esborra un draft.
   *
   * @param {number} id
   * @returns {Promise<{ok: boolean}>}
   */
  async function deleteDraft(id) {
    if (!id) throw new Error('Cal id');
    const qs = 'docent_id=' + encodeURIComponent(getDocentId());
    const resp = await fetch('/api/drafts/' + encodeURIComponent(id) + '?' + qs, {
      method: 'DELETE'
    });
    if (!resp.ok) {
      let errMsg = 'HTTP ' + resp.status;
      try { const e = await resp.json(); if (e && e.error) errMsg = e.error; } catch {}
      throw new Error(errMsg);
    }
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
  async function exportDoc({ format, adapted, profile_name = 'adaptacio' }) {
    if (!adapted || !adapted.trim()) throw new Error('No hi ha text per exportar');
    if (!['pdf', 'docx', 'txt'].includes(format)) throw new Error('Format no suportat: ' + format);
    const resp = await fetch('/api/export', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ format, adapted, profile_name })
    });
    if (!resp.ok) {
      let errMsg = 'HTTP ' + resp.status;
      try { const e = await resp.json(); if (e.error) errMsg = e.error; } catch {}
      throw new Error(errMsg);
    }
    // El backend retorna el fitxer com a attachment; llegim el blob i disparem descàrrega.
    // target=_blank evita que el navegador substitueixi la pàgina actual si ignora download
    // (passa amb alguns Chrome/Edge quan el MIME és application/pdf i hi ha visor natiu).
    const blob = await resp.blob();
    const cd = resp.headers.get('Content-Disposition') || '';
    const match = cd.match(/filename="?([^"]+)"?/);
    const fname = match ? match[1] : 'ATNE_' + format + '.' + format;
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = fname;
    a.target = '_blank'; a.rel = 'noopener';
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 4000);
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

  /**
   * Parseja el text retornat per /api/adapt per separar-lo en seccions
   * (## Text adaptat, ## Glossari, ## Esquema visual, ## Preguntes, ...).
   *
   * Retorna un objecte amb:
   *   main: string — contingut de "## Text adaptat" (o el text sencer si no hi
   *                  ha encapçalaments).
   *   complements: { glossari, esquema_visual, mapa_conceptual, preguntes_comprensio, ... }
   *                els valors són strings markdown de cada secció.
   */
  function parseAdaptedSections(text) {
    const result = { main: '', complements: {} };
    if (!text) return result;
    // Tolerant a «##Preguntes» sense espai (alguns LLMs l'ometen) i a cometes
    // típiques («##'Preguntes'» o «## "Preguntes"»). La normalització també
    // es fa al backend (clean_gemini_output), aquí fem defensa en profunditat.
    // IMPORTANT: el negative lookahead «(?!#)» és obligatori perquè si no,
    // les línies «### Abans de llegir» (sub-seccions dins de Preguntes) també
    // es tractarien com a separador i trencarien la secció.
    const parts = text.split(/^##(?!#)\s*["'`«»“”‘’]*/m);
    if (parts.length <= 1) { result.main = text; return result; }
    // Map de títols del backend → key interna. Les claus del map estan
    // normalitzades (sense accents, lowercase, sense parèntesis) perquè 'norm()'
    // les retorna en aquesta forma — així afegir variants és senzill.
    const TITLE_MAP = {
      'text adaptat': '_main',
      'glossari': 'glossari',
      'esquema visual': 'esquema_visual',
      'esquema': 'esquema_visual',
      'mapa conceptual': 'mapa_conceptual',
      'mapa mental': 'mapa_mental',
      'preguntes de comprensio': 'preguntes_comprensio',
      'preguntes': 'preguntes_comprensio',
      'bastides': 'bastides',
      'bastides scaffolding': 'bastides',
      'scaffolding': 'bastides',
      'activitats daprofundiment': 'activitats_aprofundiment',
      'activitats aprofundiment': 'activitats_aprofundiment',
      'pictogrames': 'pictogrames',
      'traduccio l1': 'traduccio_l1',
      'auditoria': 'auditoria',
      'notes dauditoria': 'auditoria',
      'argumentacio': 'argumentacio',
      'argumentacio pedagogica': 'argumentacio'
    };
    // norm: sense accents, lowercase, sense puntuació ni parèntesis → clau canònica
    const stripAccents = s => s.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    const norm = s => stripAccents(s).toLowerCase().trim()
      .replace(/[()\[\]{}]/g, ' ')
      .replace(/[^\w\s]/g, '')
      .replace(/\s+/g, ' ')
      .trim();
    for (const part of parts) {
      if (!part.trim()) continue;
      const nlIdx = part.indexOf('\n');
      const title = nlIdx > -1 ? part.slice(0, nlIdx).trim() : part.trim();
      const body = nlIdx > -1 ? part.slice(nlIdx + 1).trim() : '';
      // Detecció robusta del títol: primer match literal; si no, cerca per
      // paraula clau (tolerant a variants com "Preguntes de comprensió lectora",
      // "1. Preguntes", "Comprensió lectora", etc.). Fallback: clau generada.
      const titleNorm = norm(title);
      let key = TITLE_MAP[titleNorm];
      if (!key) {
        if (/\btext adapt/.test(titleNorm)) key = '_main';
        else if (/\bpregunt|\bcomprensi/.test(titleNorm)) key = 'preguntes_comprensio';
        else if (/\bglossari|\blexic|\bvocabulari/.test(titleNorm)) key = 'glossari';
        else if (/mapa conceptual/.test(titleNorm)) key = 'mapa_conceptual';
        else if (/mapa mental/.test(titleNorm)) key = 'mapa_mental';
        else if (/\besquema|diagrama/.test(titleNorm)) key = 'esquema_visual';
        else if (/bastid|scaffolding/.test(titleNorm)) key = 'bastides';
        else if (/aprofundiment|enriquiment/.test(titleNorm)) key = 'activitats_aprofundiment';
        else if (/argumentaci/.test(titleNorm)) key = 'argumentacio';
        else if (/auditoria/.test(titleNorm)) key = 'auditoria';
        else if (/pictogram/.test(titleNorm)) key = 'pictogrames';
        else if (/traducci/.test(titleNorm)) key = 'traduccio_l1';
        else key = titleNorm.replace(/\s+/g, '_');
      }
      if (key === '_main') result.main = body;
      else result.complements[key] = body;
    }
    if (!result.main) result.main = text;
    return result;
  }

  window.ATNE_LLM = {
    adaptText,
    refineText,
    generateText,
    generateTextStream,
    extractFile,
    listHistory,
    exportDoc,
    buildBackendProfile,
    buildBackendContext,
    htmlToMarkdown,
    markdownToHtml,
    parseAdaptedSections,
    // Drafts (esborranys al servidor)
    getDocentId,
    saveDraft,
    listDrafts,
    getDraft,
    deleteDraft
  };
})();
