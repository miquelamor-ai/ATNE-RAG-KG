/**
 * ATNE · mermaid-converter.js v4
 *
 * Converteix markdown jeràrquic a sintaxi Mermaid per als complements visuals:
 *   - esquema_visual  → flowchart LR (seqüència/procés)
 *   - mapa_conceptual → flowchart TD (Novak: conceptes + proposicions a les arestes)
 *   - mapa_mental     → mindmap (Buzan: radial, branques en colors vívids)
 *
 * El SKILL de mapa_conceptual genera branques en **negreta** que representen
 * categories semàntiques. El conversor les tracta com a PROPOSICIONS (etiquetes
 * a les arestes de Mermaid), no com a nodes. Resultat: mapa Novak correcte
 * sense modificar el backend.
 */
(function () {
  'use strict';

  // ── Utilitats internes ──────────────────────────────────────────────────

  function escapeMermaidLabel(text) {
    return text
      .replace(/\(/g, '（').replace(/\)/g, '）')
      .replace(/\[/g, '［').replace(/\]/g, '］')
      .replace(/"/g, "'")
      .replace(/:/g, ' —')
      .replace(/\{/g, '｛').replace(/\}/g, '｝')
      .replace(/\|/g, '/')
      .replace(/ /g, ' ')
      .trim();
  }

  function indentLevel(line) {
    const match = line.match(/^(\s*)/);
    if (!match) return 0;
    const ws = match[1];
    const tabs = (ws.match(/\t/g) || []).length;
    const spaces = (ws.match(/ /g) || []).length;
    return tabs > 0 ? tabs : Math.floor(spaces / 2);
  }

  function extractText(line) {
    return line
      .replace(/^\s*-\s+/, '')
      .replace(/\*\*([^*]+)\*\*/g, '$1')
      .replace(/^#+\s+/, '')
      .trim();
  }

  function filterLines(mdText) {
    return mdText.split('\n').filter(function (l) {
      const t = l.trim();
      return t.length > 0 && !t.startsWith('#') && !t.startsWith('```') && !t.startsWith('>');
    });
  }

  // ── Mapa mental — Mermaid mindmap (Buzan, radial) ───────────────────────

  function markdownToMindmap(mdText) {
    const lines = filterLines(mdText);
    if (lines.length === 0) return null;
    const levels = lines.map(l => indentLevel(l));
    const minLevel = Math.min.apply(null, levels);
    const rootCount = lines.filter(l => indentLevel(l) - minLevel === 0).length;
    const needsRoot = rootCount > 1;

    const out = ['mindmap'];
    let rootEmitted = false;
    const shift = needsRoot ? 1 : 0;
    if (needsRoot) { out.push('  root((Mapa))'); rootEmitted = true; }

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      const level = indentLevel(line) - minLevel + shift;
      const text = extractText(line.trim());
      const label = escapeMermaidLabel(text.length > 50 ? text.slice(0, 48) + '…' : text);
      if (!label) continue;
      if (!rootEmitted) {
        out.push('  root((' + label + '))');
        rootEmitted = true;
      } else {
        out.push('  '.repeat(level + 1) + label);
      }
    }
    return rootEmitted ? out.join('\n') : null;
  }

  // ── Esquema visual — flowchart LR (seqüència/procés) ───────────────────

  function markdownToFlowchart(mdText, direction) {
    direction = direction || 'LR';
    const lines = filterLines(mdText);
    if (lines.length === 0) return null;
    const levels = lines.map(l => indentLevel(l));
    const minLevel = Math.min.apply(null, levels);
    const out = ['flowchart ' + direction];
    let nodeId = 0;
    const stack = [];

    for (let i = 0; i < lines.length; i++) {
      const level = levels[i] - minLevel;
      const text = escapeMermaidLabel(extractText(lines[i].trim()));
      if (!text) continue;
      const id = 'n' + nodeId++;
      const label = text.length > 40 ? text.slice(0, 38) + '…' : text;
      while (stack.length > 0 && stack[stack.length - 1].level >= level) stack.pop();
      if (stack.length === 0) {
        out.push('  ' + id + '["' + label + '"]');
      } else {
        out.push('  ' + id + '("' + label + '")');
        out.push('  ' + stack[stack.length - 1].id + ' --> ' + id);
      }
      stack.push({ level, id });
    }
    return nodeId > 0 ? out.join('\n') : null;
  }

  // ── Mapa conceptual — flowchart TD (Novak: conceptes + proposicions) ────
  //
  // El SKILL genera **branques en negreta** com a categories semàntiques.
  // L'algoritme les tracta com a PROPOSICIONS (etiqueta de l'aresta),
  // no com a nodes visuals. Els ítems en text normal són els CONCEPTES (nodes).
  //
  // Format suportat (SKILL actual — negreta com a proposició):
  //   - **TRANSPORTS**               ← concepte arrel
  //     - **Tipus**                  ← proposició (no genera node)
  //       - Terrestres               ← concepte → TRANSPORTS --"Tipus"--> Terrestres
  //       - Aeris                    ← concepte → TRANSPORTS --"Tipus"--> Aeris
  //     - **Funcionament**           ← nova proposició per les branques següents
  //       - Motors                   ← TRANSPORTS --"Funcionament"--> Motors
  //
  // Format opcional (futur SKILL — proposició explícita amb []):
  //   - [es classifica en] Terrestres
  //

  function markdownToConceptMap(mdText) {
    const lines = filterLines(mdText);
    if (lines.length === 0) return null;
    const levels = lines.map(l => indentLevel(l));
    const minLevel = Math.min.apply(null, levels);

    // Parseja cada línia
    const parsed = [];
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      const trimmed = line.trim().replace(/^-\s+/, '');
      const level = levels[i] - minLevel;
      // Format [proposició] Concepte (futur)
      const inlineMatch = trimmed.match(/^\[([^\]]+)\]\s+(.+)$/);
      // Format **Text** (branca-proposició actual del SKILL)
      const boldMatch = !inlineMatch && trimmed.match(/^\*\*(.+)\*\*$/);

      let text, isBold = false, inlineProp = null;
      if (inlineMatch) {
        inlineProp = inlineMatch[1].trim();
        text = escapeMermaidLabel(inlineMatch[2].replace(/\*\*/g, '').trim());
      } else if (boldMatch) {
        text = boldMatch[1].trim();
        isBold = true;
      } else {
        text = escapeMermaidLabel(extractText(trimmed));
      }
      parsed.push({ level, text, isBold, inlineProp });
    }

    if (parsed.length === 0) return null;

    const out = ['flowchart TD'];
    let nodeId = 0;
    const conceptStack = [];   // { level, id } — nodes concepte visibles
    const propAtLevel = {};    // nivel → proposició en curs

    for (let i = 0; i < parsed.length; i++) {
      const { level, text, isBold, inlineProp } = parsed[i];
      const label = text.length > 40 ? text.slice(0, 38) + '…' : text;
      const escaped = escapeMermaidLabel(label);

      if (i === 0) {
        // Sempre el primer ítem és el concepte arrel (oval)
        const id = 'c' + nodeId++;
        out.push('  ' + id + '([' + escaped + '])');
        conceptStack.push({ level, id });

      } else if (isBold) {
        // Branca en negreta = PROPOSICIÓ (no genera node visual)
        propAtLevel[level] = text.length > 35 ? text.slice(0, 33) + '…' : text;
        // Neteja proposicions de nivells més profunds
        Object.keys(propAtLevel).forEach(function (l) {
          if (parseInt(l) > level) delete propAtLevel[l];
        });

      } else {
        // Concepte fill → rectangle arrodonit + aresta amb proposició
        const id = 'c' + nodeId++;
        out.push('  ' + id + '("' + escaped + '")');

        // Troba el node-pare concepte més proper (nivell inferior)
        while (conceptStack.length > 1 && conceptStack[conceptStack.length - 1].level >= level) {
          conceptStack.pop();
        }

        if (conceptStack.length > 0) {
          const parent = conceptStack[conceptStack.length - 1];
          // Determina la proposició: inline > negreta intermèdia > genèric
          let prop = inlineProp;
          if (!prop) {
            for (let l = level - 1; l > parent.level; l--) {
              if (propAtLevel[l]) { prop = propAtLevel[l]; break; }
            }
          }
          if (!prop) prop = 'inclou';
          out.push('  ' + parent.id + ' -->|"' + escapeMermaidLabel(prop) + '"| ' + id);
        }
        conceptStack.push({ level, id });
      }
    }

    return nodeId > 0 ? out.join('\n') : null;
  }

  // ── Dispatcher ──────────────────────────────────────────────────────────

  function convertMarkdownToMermaid(mdText, type) {
    if (!mdText || typeof mdText !== 'string') return null;
    const body = mdText
      .split('\n')
      .filter(function (l) { return !l.match(/^##\s+/) && !l.match(/^```/) && !l.match(/^>/); })
      .join('\n')
      .trim();
    if (!body) return null;
    try {
      if (type === 'mapa_mental' || type === 'mapa_mental_fallback') return markdownToMindmap(body);
      if (type === 'mapa_conceptual') return markdownToConceptMap(body);
      if (type === 'esquema_visual')  return markdownToFlowchart(body, 'LR');
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
            primaryColor: '#f0ece4',
            primaryTextColor: '#1a1714',
            primaryBorderColor: '#c9c3b8',
            lineColor: '#6b6560',
            secondaryColor: '#faf8f4',
            tertiaryColor: '#ffffff',
            fontFamily: 'var(--ui, system-ui)',
            fontSize: '14px',
            // Colors vívids per a cada branca del mapa mental (cScale0-9)
            cScale0: '#4f46e5', cScale1: '#0891b2', cScale2: '#059669',
            cScale3: '#d97706', cScale4: '#7c3aed', cScale5: '#be185d',
            cScale6: '#0f766e', cScale7: '#b45309', cScale8: '#1e40af',
            cScale9: '#047857',
          },
          mindmap: { padding: 20, curve: 'linear' },
          flowchart: { curve: 'basis', padding: 16 },
        });
      } catch (e) { console.warn('[ATNE Mermaid] initialize error:', e); }
      mermaidLoaded = true;
      mermaidLoading = false;
      mermaidCallbacks.forEach(function (fn) { try { fn(); } catch (_) {} });
      mermaidCallbacks.length = 0;
    };
    script.onerror = function () {
      mermaidLoading = false;
      console.warn('[ATNE Mermaid] No s\'ha pogut carregar Mermaid.js des del CDN.');
      mermaidCallbacks.length = 0;
    };
    document.head.appendChild(script);
  }

  // ── Panell d'edició (textarea + botó re-render) ──────────────────────────

  function buildEditPanel(mdRaw, cont, compType) {
    const details = document.createElement('details');
    details.className = 'mermaid-edit-details';
    const summary = document.createElement('summary');
    summary.className = 'mermaid-edit-toggle';
    summary.textContent = '✏️ Editar font del diagrama';
    const textarea = document.createElement('textarea');
    textarea.className = 'mermaid-edit-textarea';
    textarea.value = mdRaw;
    textarea.rows = 8;
    textarea.spellcheck = false;
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'mermaid-rerender-btn';
    btn.textContent = 'Refés el mapa';
    btn.addEventListener('click', function () {
      const newMd = textarea.value.trim();
      if (!newMd) return;
      cont.dataset.md = newMd;
      cont.classList.remove('mermaid-active');
      cont.innerHTML = '';
      renderMermaidBlock(cont, newMd, compType);
    });
    details.appendChild(summary);
    details.appendChild(textarea);
    details.appendChild(btn);
    return details;
  }

  // ── Renderitzat principal ────────────────────────────────────────────────

  function renderMermaidBlock(cont, mdRaw, compType) {
    const mermaidSyntax = convertMarkdownToMermaid(mdRaw, compType);
    if (!mermaidSyntax) {
      console.warn('[ATNE Mermaid] conversió→null per', compType, '— len=' + (mdRaw || '').length);
      return;
    }
    console.log('[ATNE Mermaid] conversió OK per', compType, '— syntax len=', mermaidSyntax.length);

    const wrapper = document.createElement('div');
    wrapper.className = 'mermaid-wrapper';

    // Slider de mida (zoom per escala CSS)
    const zoomRow = document.createElement('div');
    zoomRow.className = 'mermaid-zoom-row';
    zoomRow.innerHTML =
      '<label class="mermaid-zoom-label">Mida ' +
      '<input type="range" class="mermaid-zoom-slider" min="20" max="150" value="100" ' +
      'aria-label="Mida del diagrama"> ' +
      '<span class="mermaid-zoom-pct">100%</span></label>';

    const mermaidDiv = document.createElement('div');
    mermaidDiv.className = 'mermaid-diagram';
    mermaidDiv.setAttribute('data-mermaid-syntax', mermaidSyntax);
    mermaidDiv.textContent = mermaidSyntax;

    const editPanel = buildEditPanel(mdRaw, cont, compType);

    wrapper.appendChild(zoomRow);
    wrapper.appendChild(mermaidDiv);
    wrapper.appendChild(editPanel);

    cont.innerHTML = '';
    if (cont.classList.contains('schema')) cont.classList.add('mermaid-active');
    cont.appendChild(wrapper);

    // Connecta slider → transform CSS sobre el SVG
    const slider = zoomRow.querySelector('.mermaid-zoom-slider');
    const pctLabel = zoomRow.querySelector('.mermaid-zoom-pct');
    slider.addEventListener('input', function () {
      const pct = parseInt(slider.value);
      const svg = mermaidDiv.querySelector('svg');
      pctLabel.textContent = pct + '%';
      if (svg) {
        const scale = pct / 100;
        svg.style.transform = 'scale(' + scale + ')';
        svg.style.transformOrigin = 'top left';
        // Ajusta alçada del wrapper per evitar espai buit sota el SVG reescalat
        const naturalH = parseFloat(svg.getAttribute('height') || svg.getBoundingClientRect().height);
        mermaidDiv.style.height = (naturalH * scale) + 'px';
      }
    });

    const showFallback = function (reason) {
      console.warn('[ATNE Mermaid] fallback:', reason);
      editPanel.open = true;
      mermaidDiv.style.display = 'none';
      zoomRow.style.display = 'none';
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
          }).catch(function (e) { showFallback(e && e.message || 'Promise'); });
        }
      } catch (e) { showFallback(e && e.message || 'excepció'); }
    });
  }

  // ── renderAllMermaidComplements (API de compatibilitat, no es crida) ──────

  function renderAllMermaidComplements() {
    const targets = [
      { sel: '#view-mapa-conc .generic-md', type: 'mapa_conceptual' },
      { sel: '#view-mapa-ment .generic-md', type: 'mapa_mental' },
      { sel: '#view-esquema .schema',       type: 'esquema_visual' },
    ];
    targets.forEach(function (t) {
      const cont = document.querySelector(t.sel);
      if (!cont) return;
      const mdRaw = cont.dataset.md;
      if (!mdRaw || !mdRaw.trim()) return;
      renderMermaidBlock(cont, mdRaw, t.type);
    });
  }

  // ── Exposició global ─────────────────────────────────────────────────────

  window.ATNE_MERMAID = {
    convertMarkdownToMermaid,
    renderAllMermaidComplements,
    renderMermaidBlock,
    _markdownToMindmap: markdownToMindmap,
    _markdownToFlowchart: markdownToFlowchart,
    _markdownToConceptMap: markdownToConceptMap,
    _loadMermaid: loadMermaid,
  };

}());
