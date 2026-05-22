/**
 * ATNE · mermaid-converter.js
 *
 * Converteix markdown jeràrquic (sagnies amb guions) a sintaxi Mermaid
 * i orquestra la càrrega lazy de Mermaid.js + el renderitzat dels blocs
 * "## Mapa conceptual" i "## Esquema visual".
 *
 * NO modifica el prompt del LLM. És integració purament frontend.
 * Fallback garantit: si Mermaid falla, el text markdown original es mostra.
 */
(function () {
  'use strict';

  // ── Utilitats internes ──────────────────────────────────────────────────

  /**
   * Escapa caràcters que Mermaid interpreta malament dins dels labels de node.
   * Mermaid mindmap permet qualsevol text a les línies (no fa falta escapar
   * el que no és sintaxi Mermaid), però evitem parèntesis dobles i corxets.
   */
  function escapeMermaidLabel(text) {
    return text
      .replace(/\(/g, '（')   // parèntesi llatí → CJK parèntesi (segur per Mermaid)
      .replace(/\)/g, '）')
      .replace(/\[/g, '［')
      .replace(/\]/g, '］')
      .replace(/"/g, "'")     // Mermaid node labels entre cometes: evitem cometes dobles
      .trim();
  }

  /**
   * Determina el nivell de sagnia (nombre d'espais / 2, o nombre de tabuladors).
   * La sagnia mínima trobada al document es normalitza a nivell 0.
   */
  function indentLevel(line) {
    const match = line.match(/^(\s*)/);
    if (!match) return 0;
    const ws = match[1];
    const tabs = (ws.match(/\t/g) || []).length;
    const spaces = (ws.match(/ /g) || []).length;
    return tabs > 0 ? tabs : Math.floor(spaces / 2);
  }

  /**
   * Extreu el text net d'una línia markdown de llista.
   * Elimina el guió inicial i els marcadors de negreta.
   */
  function extractText(line) {
    return line
      .replace(/^\s*-\s+/, '')         // guió de llista
      .replace(/\*\*([^*]+)\*\*/g, '$1') // negreta
      .replace(/^#+\s+/, '')            // capçaleres residuals
      .trim();
  }

  // ── Conversió markdown → Mermaid mindmap (mapa conceptual) ────────────

  /**
   * Converteix un bloc de text markdown jeràrquic (sagnies/guions) a un
   * diagrama Mermaid de tipus "mindmap".
   *
   * Exemple d'entrada:
   *   - Sistema solar
   *     - Estrella central: Sol
   *     - 8 planetes
   *       - Interiors: Mercuri, Venus, Terra, Mart
   *
   * Exemple de sortida:
   *   mindmap
   *     root((Sistema solar))
   *       Estrella central: Sol
   *       8 planetes
   *         Interiors: Mercuri, Venus, Terra, Mart
   *
   * @param {string} mdText  Text markdown (sense la capçalera ## Mapa conceptual)
   * @returns {string|null}  Sintaxi Mermaid o null si no és parseable
   */
  function markdownToMindmap(mdText) {
    const rawLines = mdText.split('\n');
    // Filtra línies buides i capçaleres
    const lines = rawLines.filter(l => {
      const trimmed = l.trim();
      return trimmed.length > 0 && !trimmed.startsWith('#');
    });

    if (lines.length === 0) return null;

    // Detecta el nivell base mínim per normalitzar
    const levels = lines.map(l => indentLevel(l));
    const minLevel = Math.min(...levels);

    // Construeix les línies Mermaid
    const mermaidLines = ['mindmap'];
    let rootEmitted = false;

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      const trimmed = line.trim();
      // Saltar línies que no siguin items de llista ni text simple
      if (!trimmed) continue;

      const level = indentLevel(line) - minLevel;
      const text = escapeMermaidLabel(extractText(trimmed));
      if (!text) continue;

      // Sagnia de 2 espais per nivell (Mermaid mindmap requereix consistència)
      const indent = '  '.repeat(level + 1); // +1 perquè el root és el nivell 0

      if (!rootEmitted) {
        // Primer node: root amb doble parèntesi (node rodó destacat)
        mermaidLines.push('  root((' + text + '))');
        rootEmitted = true;
      } else {
        mermaidLines.push(indent + text);
      }
    }

    if (!rootEmitted) return null;
    return mermaidLines.join('\n');
  }

  // ── Conversió markdown → Mermaid flowchart LR (esquema visual) ────────

  /**
   * Converteix un bloc de text markdown jeràrquic a un diagrama Mermaid
   * de tipus "flowchart LR" (horitzontal, adequat per a seqüències/processos).
   *
   * Cada item de primer nivell es converteix en un node principal;
   * els subnivells en nodes fills connectats amb fletxes.
   *
   * @param {string} mdText  Text markdown (sense la capçalera)
   * @returns {string|null}  Sintaxi Mermaid o null si no és parseable
   */
  function markdownToFlowchart(mdText) {
    const rawLines = mdText.split('\n');
    const lines = rawLines.filter(l => {
      const trimmed = l.trim();
      return trimmed.length > 0 && !trimmed.startsWith('#');
    });

    if (lines.length === 0) return null;

    const levels = lines.map(l => indentLevel(l));
    const minLevel = Math.min(...levels);

    const mermaidLines = ['flowchart LR'];
    let nodeId = 0;
    // Pila per mantenir el pare de cada nivell: { level, id }
    const parentStack = [];
    let lastId = null;

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      const trimmed = line.trim();
      if (!trimmed) continue;

      const level = indentLevel(line) - minLevel;
      const text = escapeMermaidLabel(extractText(trimmed));
      if (!text) continue;

      const id = 'n' + (nodeId++);
      // Limita el text del node a 40 chars per llegibilitat visual
      const label = text.length > 40 ? text.slice(0, 38) + '…' : text;

      // Trobem el pare adequat per a aquest nivell
      // Buidem la pila fins que el pare tingui nivell < actual
      while (parentStack.length > 0 && parentStack[parentStack.length - 1].level >= level) {
        parentStack.pop();
      }

      if (parentStack.length === 0) {
        // Node arrel: rectangle
        mermaidLines.push('  ' + id + '["' + label + '"]');
      } else {
        const parentId = parentStack[parentStack.length - 1].id;
        // Node fill: rectangle arrodonit + connexió al pare
        mermaidLines.push('  ' + id + '("' + label + '")');
        mermaidLines.push('  ' + parentId + ' --> ' + id);
      }

      parentStack.push({ level, id });
      lastId = id;
    }

    if (nodeId === 0) return null;
    return mermaidLines.join('\n');
  }

  // ── API pública ─────────────────────────────────────────────────────────

  /**
   * Funció principal de conversió.
   *
   * @param {string} mdText  Text markdown (pot incloure la capçalera ## o no)
   * @param {'mapa_conceptual'|'esquema_visual'} type  Tipus de diagrama
   * @returns {string|null}  Sintaxi Mermaid o null si el fallback és necessari
   */
  function convertMarkdownToMermaid(mdText, type) {
    if (!mdText || typeof mdText !== 'string') return null;
    // Elimina les capçaleres ## per processar només el contingut
    const body = mdText
      .split('\n')
      .filter(l => !l.match(/^##\s+/))
      .join('\n')
      .trim();

    if (!body) return null;

    try {
      if (type === 'mapa_conceptual' || type === 'mapa_mental') {
        return markdownToMindmap(body);
      } else if (type === 'esquema_visual') {
        return markdownToFlowchart(body);
      }
      return null;
    } catch (e) {
      console.warn('[ATNE Mermaid] Error de conversió:', e);
      return null;
    }
  }

  // ── Càrrega lazy de Mermaid.js ──────────────────────────────────────────

  let mermaidLoaded = false;
  let mermaidLoading = false;
  const mermaidCallbacks = [];

  function loadMermaid(cb) {
    if (mermaidLoaded && window.mermaid) { cb(); return; }
    mermaidCallbacks.push(cb);
    if (mermaidLoading) return;
    mermaidLoading = true;

    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js';
    script.onload = function () {
      try {
        window.mermaid.initialize({
          startOnLoad: false,
          theme: 'base',
          themeVariables: {
            primaryColor: '#f0ece4',        // --cream-2 aprox.
            primaryTextColor: '#1a1714',    // --ink-900
            primaryBorderColor: '#c9c3b8',  // --paper-line
            lineColor: '#6b6560',           // --ink-500
            secondaryColor: '#faf8f4',      // --cream-1
            tertiaryColor: '#ffffff',
            fontFamily: 'var(--ui, system-ui)',
            fontSize: '14px',
          },
          mindmap: { padding: 16, curve: 'linear' },
          flowchart: { curve: 'basis', padding: 16 },
        });
      } catch (e) {
        console.warn('[ATNE Mermaid] initialize error:', e);
      }
      mermaidLoaded = true;
      mermaidLoading = false;
      mermaidCallbacks.forEach(fn => { try { fn(); } catch (_) {} });
      mermaidCallbacks.length = 0;
    };
    script.onerror = function () {
      mermaidLoading = false;
      console.warn('[ATNE Mermaid] No s\'ha pogut carregar Mermaid.js des del CDN.');
      // No executem els callbacks: el fallback (text) ja és visible.
      mermaidCallbacks.length = 0;
    };
    document.head.appendChild(script);
  }

  // ── Renderitzat d'un element .mermaid-block ──────────────────────────────

  /**
   * Donada una referència a un contenidor (`.generic-md` o `.schema`),
   * si conté text de tipus mapa_conceptual/esquema_visual/mapa_mental,
   * substitueix el contingut per un bloc Mermaid renderitzat i guarda
   * el text original en un <details> de fallback/còpia.
   *
   * @param {HTMLElement} cont   El contenidor on ja hi ha el text md2html
   * @param {string} mdRaw      El text markdown original
   * @param {string} compType   La clau del complement (ex. 'mapa_conceptual')
   */
  function renderMermaidBlock(cont, mdRaw, compType) {
    const mermaidSyntax = convertMarkdownToMermaid(mdRaw, compType);
    if (!mermaidSyntax) return; // fallback: deixa el text com estava

    // Construeix el DOM: wrapper + bloc mermaid + details fallback
    const wrapper = document.createElement('div');
    wrapper.className = 'mermaid-wrapper';

    const mermaidDiv = document.createElement('div');
    mermaidDiv.className = 'mermaid-diagram';
    mermaidDiv.setAttribute('data-mermaid-syntax', mermaidSyntax);
    // El text que Mermaid.js renderitza ha d'estar al innerHTML
    mermaidDiv.textContent = mermaidSyntax;

    // Botó toggle text/diagrama
    const toggleBtn = document.createElement('button');
    toggleBtn.type = 'button';
    toggleBtn.className = 'mermaid-toggle-btn';
    toggleBtn.textContent = 'Veure com a text';
    toggleBtn.setAttribute('aria-pressed', 'false');

    // Details de fallback (text original)
    const details = document.createElement('details');
    details.className = 'mermaid-fallback-details';
    const summary = document.createElement('summary');
    summary.textContent = 'Text pla (còpia per a PDF)';
    const pre = document.createElement('pre');
    pre.className = 'mermaid-fallback-pre';
    pre.textContent = mdRaw;
    details.appendChild(summary);
    details.appendChild(pre);

    // Toggle handler
    toggleBtn.addEventListener('click', function () {
      const showText = toggleBtn.getAttribute('aria-pressed') === 'false';
      toggleBtn.setAttribute('aria-pressed', showText ? 'true' : 'false');
      toggleBtn.textContent = showText ? 'Veure com a diagrama' : 'Veure com a text';
      mermaidDiv.style.display = showText ? 'none' : '';
      details.open = showText;
    });

    wrapper.appendChild(toggleBtn);
    wrapper.appendChild(mermaidDiv);
    wrapper.appendChild(details);

    // Substitueix el contingut del contenidor
    cont.innerHTML = '';
    cont.appendChild(wrapper);

    // Demana Mermaid i renderitza
    loadMermaid(function () {
      try {
        // mermaid.run() accepta un selector o una llista de nodes
        window.mermaid.run({ nodes: [mermaidDiv] });
      } catch (e) {
        console.warn('[ATNE Mermaid] run() error:', e);
        // Fallback: mostra el text pla obrint el details
        details.open = true;
        mermaidDiv.style.display = 'none';
      }
    });
  }

  // ── Punt d'entrada: renderitza tots els complements visuals ──────────────

  /**
   * Crida aquesta funció des de pas3.html després d'omplir els complements
   * mapa_conceptual, mapa_mental i esquema_visual.
   *
   * Recorre els contenidors coneguts i aplica renderMermaidBlock si escau.
   */
  function renderAllMermaidComplements() {
    const targets = [
      { sel: '#view-mapa-conc .generic-md',  type: 'mapa_conceptual' },
      { sel: '#view-mapa-ment .generic-md',  type: 'mapa_mental' },
      { sel: '#view-esquema .schema',        type: 'esquema_visual' },
    ];
    targets.forEach(function (t) {
      const cont = document.querySelector(t.sel);
      if (!cont) return;
      const mdRaw = cont.dataset.md;
      if (!mdRaw || !mdRaw.trim()) return;
      renderMermaidBlock(cont, mdRaw, t.type);
    });
  }

  // ── Exposició global ────────────────────────────────────────────────────

  window.ATNE_MERMAID = {
    convertMarkdownToMermaid,
    renderAllMermaidComplements,
    renderMermaidBlock,
    // Exposem les funcions de baix nivell per als tests manuals
    _markdownToMindmap: markdownToMindmap,
    _markdownToFlowchart: markdownToFlowchart,
    _loadMermaid: loadMermaid,
  };

}());
