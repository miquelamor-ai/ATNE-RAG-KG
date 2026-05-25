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
      .replace(/:/g, ' —')    // Mermaid mindmap interpreta ':' com a separador → substituïm per '—'
      .replace(/\{/g, '｛')
      .replace(/\}/g, '｝')
      .replace(/\|/g, '/')    // pipe trenca taules Mermaid
      .replace(/[ ]/g, ' ') // nbsp → espai normal
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

    // Detecta si el LLM ha generat múltiples ítems de nivell 0 (arrels múltiples).
    // Mermaid mindmap requereix exactament UNA arrel. Si n'hi ha més d'una,
    // afegim una arrel implícita "Mapa" i desplacem tots els nodes un nivell.
    const rootCount = lines.filter(l => indentLevel(l) - minLevel === 0).length;
    const needsImplicitRoot = rootCount > 1;

    // Construeix les línies Mermaid
    const mermaidLines = ['mindmap'];
    let rootEmitted = false;
    // Si cal arrel implícita, l'afegim ara i tractem TOTS els ítems com a fills.
    const levelShift = needsImplicitRoot ? 1 : 0;
    if (needsImplicitRoot) {
      mermaidLines.push('  root((Mapa))');
      rootEmitted = true;
    }

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      const trimmed = line.trim();
      // Saltar línies que no siguin items de llista ni text simple
      if (!trimmed) continue;

      const level = indentLevel(line) - minLevel + levelShift;
      const text = escapeMermaidLabel(extractText(trimmed));
      if (!text) continue;

      // Sagnia de 2 espais per nivell (Mermaid mindmap requereix consistència)
      const indent = '  '.repeat(level + 1); // +1 perquè el root és el nivell 0

      // Limita labels llargs per evitar desbordament del node Mermaid
      const labelMindmap = text.length > 50 ? text.slice(0, 48) + '…' : text;
      if (!rootEmitted) {
        // Primer node: root amb doble parèntesi (node rodó destacat)
        mermaidLines.push('  root((' + labelMindmap + '))');
        rootEmitted = true;
      } else {
        mermaidLines.push(indent + labelMindmap);
      }
    }

    if (!rootEmitted) return null;
    return mermaidLines.join('\n');
  }

  // ── Conversió markdown → Mermaid flowchart LR (esquema visual) ────────

  /**
   * Converteix un bloc de text markdown jeràrquic a un diagrama Mermaid
   * de tipus "flowchart" (LR horitzontal per a esquemes; TD vertical per a mapes conceptuals).
   *
   * Cada item de primer nivell es converteix en un node principal;
   * els subnivells en nodes fills connectats amb fletxes.
   *
   * @param {string} mdText       Text markdown (sense la capçalera)
   * @param {string} [direction]  'LR' (per defecte) o 'TD' per a mapa conceptual
   * @returns {string|null}       Sintaxi Mermaid o null si no és parseable
   */
  function markdownToFlowchart(mdText, direction) {
    direction = direction || 'LR';
    const rawLines = mdText.split('\n');
    const lines = rawLines.filter(l => {
      const trimmed = l.trim();
      return trimmed.length > 0 && !trimmed.startsWith('#');
    });

    if (lines.length === 0) return null;

    const levels = lines.map(l => indentLevel(l));
    const minLevel = Math.min(...levels);

    const mermaidLines = ['flowchart ' + direction];
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

  // ── Mapa conceptual Novak (flowchart TD amb proposicions) ─────────────

  /**
   * Converteix markdown jeràrquic a un mapa conceptual estil Novak:
   * nodes (conceptes) connectats per arestes etiquetades (proposicions).
   *
   * Suporta proposicions embegudes al format: "- [proposició] Concepte"
   * Si no hi ha proposició explícita, usa "inclou" com a genèric.
   *
   * Exemple d'entrada:
   *   - Transports
   *     - [es classifiquen en] Tipus
   *       - [inclou] Terrestres
   *       - [inclou] Aeris
   *     - [necessiten] Motors
   *       - [transformen] Energia
   */
  function markdownToConceptMap(mdText) {
    const rawLines = mdText.split('\n');
    const lines = rawLines.filter(l => {
      const t = l.trim();
      return t.length > 0 && !t.startsWith('#') && !t.startsWith('```');
    });
    if (lines.length === 0) return null;

    const levels = lines.map(l => indentLevel(l));
    const minLevel = Math.min(...levels);

    const mermaidLines = ['flowchart TD'];
    let nodeId = 0;
    const parentStack = [];

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      const trimmed = line.trim();
      if (!trimmed) continue;

      const level = indentLevel(line) - minLevel;

      // Suporta proposicions embegudes: "- [proposició] Text del concepte"
      const propMatch = trimmed.match(/^-\s+\[([^\]]+)\]\s+(.+)$/);
      const rawText = propMatch ? propMatch[2] : extractText(trimmed);
      const prop = propMatch ? propMatch[1].trim() : 'inclou';
      const text = escapeMermaidLabel(rawText);
      if (!text) continue;

      const id = 'c' + (nodeId++);
      const label = text.length > 38 ? text.slice(0, 36) + '…' : text;

      while (parentStack.length > 0 && parentStack[parentStack.length - 1].level >= level) {
        parentStack.pop();
      }

      if (parentStack.length === 0) {
        // Concepte arrel: node ovalat per distingir-lo
        mermaidLines.push('  ' + id + '([' + label + '])');
      } else {
        const parent = parentStack[parentStack.length - 1];
        // Concepte fill: rectangle arrodonit
        mermaidLines.push('  ' + id + '("' + label + '")');
        // Aresta amb proposició etiquetada
        mermaidLines.push('  ' + parent.id + ' -->|"' + escapeMermaidLabel(prop) + '"| ' + id);
      }
      parentStack.push({ level, id });
    }

    if (nodeId === 0) return null;
    return mermaidLines.join('\n');
  }

  // ── API pública ─────────────────────────────────────────────────────────

  /**
   * Funció principal de conversió per a Mermaid.
   * Nota: mapa_mental usa markmap (no Mermaid) → retorna null.
   */
  function convertMarkdownToMermaid(mdText, type) {
    if (!mdText || typeof mdText !== 'string') return null;
    const body = mdText
      .split('\n')
      .filter(l => !l.match(/^##\s+/) && !l.match(/^```/))
      .join('\n')
      .trim();

    if (!body) return null;

    try {
      if (type === 'mapa_conceptual') {
        return markdownToConceptMap(body);
      } else if (type === 'esquema_visual') {
        return markdownToFlowchart(body, 'LR');
      }
      // mapa_mental → renderMarkmapBlock (no Mermaid)
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

  // ── Càrrega lazy de markmap.js (mapa mental) ────────────────────────────

  let markmapLoaded = false;
  let markmapLoading = false;
  const markmapCallbacks = [];

  function loadMarkmap(cb) {
    if (markmapLoaded && window.markmap && window.markmap.Transformer && window.markmap.Markmap) {
      cb(); return;
    }
    markmapCallbacks.push(cb);
    if (markmapLoading) return;
    markmapLoading = true;

    function _loadScript(url, onLoad, onErr) {
      var s = document.createElement('script');
      s.src = url;
      s.onload = onLoad;
      s.onerror = onErr;
      document.head.appendChild(s);
    }

    var LIB = 'https://cdn.jsdelivr.net/npm/markmap-lib@0.15.4/dist/browser/index.min.js';
    var VIEW = 'https://cdn.jsdelivr.net/npm/markmap-view@0.15.4/dist/browser/index.min.js';

    _loadScript(LIB, function () {
      _loadScript(VIEW, function () {
        markmapLoaded = true;
        markmapLoading = false;
        markmapCallbacks.forEach(function (fn) { try { fn(); } catch (_) {} });
        markmapCallbacks.length = 0;
      }, function () {
        markmapLoading = false;
        console.warn('[ATNE Markmap] No s\'ha pogut carregar markmap-view');
        markmapCallbacks.length = 0;
      });
    }, function () {
      markmapLoading = false;
      console.warn('[ATNE Markmap] No s\'ha pogut carregar markmap-lib');
      markmapCallbacks.length = 0;
    });
  }

  /**
   * Converteix la llista markdown (guions) a format de capçaleres per a markmap.
   * - Concepte           → # Concepte
   *   - Subconcept       → ## Subconcept
   */
  function markdownListToMarkmapMd(mdText) {
    const lines = mdText.split('\n').filter(function (l) {
      var t = l.trim();
      return t.length > 0 && !t.startsWith('#') && !t.startsWith('```');
    });
    if (lines.length === 0) return null;
    var levels = lines.map(function (l) { return indentLevel(l); });
    var minLevel = Math.min.apply(null, levels);
    var result = [];
    for (var i = 0; i < lines.length; i++) {
      var level = indentLevel(lines[i]) - minLevel + 1;
      var text = extractText(lines[i].trim());
      if (text) result.push('#'.repeat(Math.min(level, 6)) + ' ' + text);
    }
    return result.join('\n');
  }

  /**
   * Construeix el panell d'edició (textarea + botó) comú als dos renders.
   * @param {string}      mdRaw     Markdown font original
   * @param {HTMLElement} cont      Contenidor pare
   * @param {string}      compType  Clau del complement
   * @param {Function}    reRenderFn  Funció a cridar en re-renderitzar
   */
  function buildEditPanel(mdRaw, cont, compType, reRenderFn) {
    var details = document.createElement('details');
    details.className = 'mermaid-edit-details';
    var summary = document.createElement('summary');
    summary.className = 'mermaid-edit-toggle';
    summary.textContent = '✏️ Editar font del diagrama';
    var textarea = document.createElement('textarea');
    textarea.className = 'mermaid-edit-textarea';
    textarea.value = mdRaw;
    textarea.rows = 8;
    textarea.spellcheck = false;
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'mermaid-rerender-btn';
    btn.textContent = 'Refés el mapa';
    btn.addEventListener('click', function () {
      var newMd = textarea.value.trim();
      if (!newMd) return;
      cont.dataset.md = newMd;
      cont.classList.remove('mermaid-active');
      cont.innerHTML = '';
      reRenderFn(cont, newMd, compType);
    });
    details.appendChild(summary);
    details.appendChild(textarea);
    details.appendChild(btn);
    return details;
  }

  /**
   * Renderitza un mapa mental (Buzan) usant markmap.js.
   * Fallback a Mermaid mindmap si markmap no carrega.
   */
  function renderMarkmapBlock(cont, mdRaw, compType) {
    var markmapMd = markdownListToMarkmapMd(mdRaw);
    if (!markmapMd) { return; }

    var wrapper = document.createElement('div');
    wrapper.className = 'mermaid-wrapper';

    var svgEl = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svgEl.style.cssText = 'width:100%;min-height:420px;display:block';

    var editPanel = buildEditPanel(mdRaw, cont, compType, renderMermaidBlock);

    wrapper.appendChild(svgEl);
    wrapper.appendChild(editPanel);

    cont.innerHTML = '';
    cont.appendChild(wrapper);

    loadMarkmap(function () {
      try {
        var mm = window.markmap;
        if (!mm || !mm.Transformer || !mm.Markmap) throw new Error('API no disponible');
        var transformer = new mm.Transformer();
        var transformed = transformer.transform(markmapMd);
        mm.Markmap.create(svgEl, {
          autoFit: true,
          duration: 300,
          maxWidth: 300,
          zoom: true,
          pan: true,
        }, transformed.root);
      } catch (e) {
        console.warn('[ATNE Markmap] error, fallback a Mermaid:', e);
        // Fallback: mermaid mindmap
        var mermaidSyntax = markdownToMindmap(markmapMd.replace(/^#+\s*/gm, '- '));
        if (mermaidSyntax) {
          cont.innerHTML = '';
          renderMermaidBlock(cont, mdRaw, 'mapa_mental_fallback');
        }
      }
    });
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
    // Mapa mental → markmap.js (millor estètica que Mermaid mindmap)
    if (compType === 'mapa_mental') {
      renderMarkmapBlock(cont, mdRaw, compType);
      return;
    }

    const mermaidSyntax = convertMarkdownToMermaid(mdRaw, compType);
    if (!mermaidSyntax) {
      console.warn('[ATNE Mermaid] conversió→null per', compType,
        '— len=' + (mdRaw||'').length);
      return;
    }
    console.log('[ATNE Mermaid] conversió OK per', compType, '— syntax len=', mermaidSyntax.length);

    const wrapper = document.createElement('div');
    wrapper.className = 'mermaid-wrapper';

    const mermaidDiv = document.createElement('div');
    mermaidDiv.className = 'mermaid-diagram';
    mermaidDiv.setAttribute('data-mermaid-syntax', mermaidSyntax);
    mermaidDiv.textContent = mermaidSyntax;

    const editPanel = buildEditPanel(mdRaw, cont, compType, renderMermaidBlock);

    wrapper.appendChild(mermaidDiv);
    wrapper.appendChild(editPanel);

    cont.innerHTML = '';
    if (cont.classList.contains('schema')) {
      cont.classList.add('mermaid-active');
    }
    cont.appendChild(wrapper);

    const showFallback = function (reason) {
      console.warn('[ATNE Mermaid] fallback:', reason);
      editPanel.open = true;
      mermaidDiv.style.display = 'none';
    };
    loadMermaid(function () {
      try {
        const result = window.mermaid.run({ nodes: [mermaidDiv] });
        if (result && typeof result.then === 'function') {
          result.then(function () {
            const svg = mermaidDiv.querySelector('svg');
            const txt = svg ? svg.textContent || '' : '';
            if (/syntax error|parse error/i.test(txt) ||
                (svg && svg.querySelector('[class*="error"]'))) {
              showFallback('SVG d\'error detectat');
            }
          }).catch(function (e) {
            showFallback(e && e.message ? e.message : 'Promise rebutjada');
          });
        }
      } catch (e) {
        showFallback(e && e.message ? e.message : 'excepció síncrona');
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
    console.log('[ATNE Mermaid] renderAllMermaidComplements() cridat');
    const targets = [
      { sel: '#view-mapa-conc .generic-md',  type: 'mapa_conceptual' },
      { sel: '#view-mapa-ment .generic-md',  type: 'mapa_mental' },
      { sel: '#view-esquema .schema',        type: 'esquema_visual' },
    ];
    targets.forEach(function (t) {
      const cont = document.querySelector(t.sel);
      if (!cont) {
        console.log('[ATNE Mermaid] element no trobat:', t.sel);
        return;
      }
      const mdRaw = cont.dataset.md;
      if (!mdRaw || !mdRaw.trim()) {
        console.log('[ATNE Mermaid] dataset.md buit per', t.type);
        return;
      }
      console.log('[ATNE Mermaid] processant', t.type, '— md len=', mdRaw.length);
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
