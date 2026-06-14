/* ═══ ATNE · diagram-editor-ui.js — Subsistema d'edició de diagrames (bloc B3+B4) ═══
 *
 * Capa d'UI sobre el renderitzador (mermaid-converter.js) i el nucli pur
 * (diagram-editor-core.js). Serveix els TRES tipus de diagrama d'ATNE, segons el
 * `type` passat a attach() (mapa_conceptual | mapa_mental | esquema_visual):
 *
 *   · MAPA CONCEPTUAL (Novak) — joc complet: afegir conceptes/proposicions, ×,
 *     enllaços creuats amb ↝ (mode connexió de dos clics) i edició d'aquests.
 *   · MAPA MENTAL i ESQUEMA VISUAL — arbres jeràrquics PURS: joc reduït de
 *     + branca (fill) / + germà / ×. SENSE proposicions ni enllaços creuats.
 *
 * Comú a tots: edició de label pel popup del renderitzador, desfés/refés
 * (Ctrl+Z / Ctrl+Y), barra de control injectada i mini-toolbar sobre l'editor
 * de font (sagnat / negreta / cursiva). La modulació per MECR (profunditat,
 * amplada, densitat) ve del canon de cada tipus (veure capsObj).
 *
 * Tota mutació passa per la FONT ÚNICA (el markdown a `cont.dataset.md`); el
 * render es recalcula després. Adaptat del prototip validat (v0.2), SENSE el
 * codi d'arrencada del banc de proves (#seed/#diagram/#src): en producció el
 * contenidor real i el MECR del perfil arriben per `attach()`.
 *
 * Carrega DESPRÉS de mermaid-converter.js (usa window.ATNE_MERMAID) i, si hi és,
 * consumeix window.ATNE_MAPA_PROFUNDITAT (límit de profunditat per MECR, canon).
 *
 * BACKLOG CONEGUT (decidit amb Miquel 13/06 — diferit, no bloquejant):
 *   1. renameInCross NO s'enganxa: si es reanomena un node pel popup d'edició del
 *      renderitzador, els enllaços creuats que el referencien queden trencats
 *      (el label vell ja no existeix). El nucli té renameInCross() a punt.
 *   2. Les edicions de LABEL pel popup del renderitzador NO entren al desfés (el
 *      renderitzador re-renderitza pel seu compte). Les operacions estructurals
 *      (+/×/↝) i l'editor de font SÍ que hi entren.
 */
(function () {
  'use strict';
  var C = window.ATNE_EDIT_CORE;
  if (!C) { console.warn('[ATNE editor] ATNE_EDIT_CORE absent — carrega diagram-editor-core.js abans.'); return; }

  var state = {
    mecr: 'B1', undo: [], redo: [], lastLine: null, lastLabel: '',
    cont: null, type: 'mapa_conceptual', connecting: null, attached: false,
  };
  var ui = { undoBtn: null, redoBtn: null, badge: null };
  var observer = null;

  // ── Profunditat per MECR (B4): consumida del canon, NO hardcoded ──
  // window.ATNE_MAPA_PROFUNDITAT.levels = { "A2":2, "B1":3, "B2":4, "C1+":null, ... }
  // (nivells de sangria del rubrica.json, pas_5). EL CANON MANA: el límit és el
  // número del canon tal qual (A2=2, B1=3, B2=4). L'única lògica del consumidor és
  // tractar `null` com a "sense límit" — i null vol dir que el canon NO declara
  // nivells comptables (pre-A1 = esquema pla; C1+ = mapa de contrast en columnes).
  // Cap regla pedagògica al codi: si algun dia es vol B2 lliure, es canvia al canon.
  function normMecr(m) {
    m = (m || '').trim();
    if (/^C[12]/i.test(m)) return 'C1+';
    return m;
  }
  // Font de límits SEGONS EL TIPUS de diagrama (cada tipus té el seu canon):
  //   · mapa_conceptual → arrel de ATNE_MAPA_PROFUNDITAT (levels/branques/subel/densitat).
  //   · esquema_visual  → ATNE_MAPA_PROFUNDITAT.esquema (només levels + densitat;
  //                       el canon de l'esquema no té branques/subelements).
  //   · mapa_mental     → sense canon (rubrica.json inexistent) → null = sense límit,
  //                       fins que mineriaRAG el canonitzi (handoff pendent).
  function capsObj() {
    var data = window.ATNE_MAPA_PROFUNDITAT;
    if (!data) return null;
    if (state.type === 'esquema_visual') return data.esquema || null;
    if (state.type === 'mapa_mental') return data.mapa_mental || null;
    return data;                                       // mapa_conceptual (arrel)
  }
  function depthCap() {
    var c = capsObj();
    if (!c || !c.levels) return Infinity;              // sense canon per al tipus → sense límit
    var n = c.levels[normMecr(state.mecr)];
    if (n == null) return Infinity;                    // sense nivells comptables al canon
    return n;                                          // el canon mana: A2=2, B1=3, B2=4
  }
  // Nivell de sangria (indentOf/2) de la línia lineIdx del markdown vigent.
  function levelOf(lineIdx) {
    var line = (md().split('\n')[lineIdx]) || '';
    return Math.floor(C.indentOf(line) / 2);
  }
  // Una "+ proposició" crea una paraula d'enllaç (prop) com a fill de lineIdx,
  // és a dir a nivell levelOf(lineIdx)+1. Bloquegem si supera el límit del canon.
  // Gatejant pel nivell de la PROPOSICIÓ (no del concepte) B1 esdevé més profund
  // que A2 malgrat la paritat de Novak (prop+concepte = 2 nivells de sangria).
  function deepBlocked(lineIdx) {
    var cap = depthCap();
    if (cap === Infinity) return false;
    return (levelOf(lineIdx) + 1) > cap;
  }

  // ── Modulació d'AMPLADA i DENSITAT per MECR (B4) — també del canon ──
  // branques_max (pas_3), subelements_max (pas_4), densitat_max (H6). null → lliure.
  function capFromMap(mapName) {
    var c = capsObj();
    if (!c || !c[mapName]) return Infinity;            // clau absent per al tipus → sense límit
    var n = c[mapName][normMecr(state.mecr)];
    return (n == null) ? Infinity : n;
  }
  function branchMax() { return capFromMap('branques_max'); }
  function subelMax() { return capFromMap('subelements_max'); }
  function densitatMax() { return capFromMap('densitat_max'); }

  function mdLines() { return md().split('\n'); }
  function isItemLn(l) { return /^\s*-\s+/.test(l); }
  // Índex de la línia pare (primera anterior amb menys sagnia). -1 = arrel.
  function parentOf(lineIdx) {
    var ls = mdLines(), lvl = C.indentOf(ls[lineIdx] || '');
    for (var p = lineIdx - 1; p >= 0; p--) {
      if (isItemLn(ls[p]) && C.indentOf(ls[p]) < lvl) return p;
    }
    return -1;
  }
  // Compta els fills DIRECTES (sagnia pare+2) del tipus indicat (prop|concept).
  function childrenOfKind(parentLineIdx, kind) {
    var ls = mdLines();
    var pIndent = parentLineIdx < 0 ? -2 : C.indentOf(ls[parentLineIdx] || '');
    var end = parentLineIdx < 0 ? ls.length - 1 : C.subtreeEnd(md(), parentLineIdx);
    var target = pIndent + 2, count = 0;
    for (var i = parentLineIdx + 1; i <= end; i++) {
      if (!isItemLn(ls[i]) || C.indentOf(ls[i]) !== target) continue;
      if (C.classify(md(), i) === kind) count++;
    }
    return count;
  }
  // Bloqueig per AMPLADA: afegir una branca (prop) sota parentLineIdx o un
  // sub-element (concept) sota una proposició, si ja s'ha arribat al màxim del canon.
  function branchFull(parentLineIdx) {
    var max = branchMax();
    return max !== Infinity && childrenOfKind(parentLineIdx, 'prop') >= max;
  }
  function subelFull(parentPropLineIdx) {
    var max = subelMax();
    return max !== Infinity && childrenOfKind(parentPropLineIdx, 'concept') >= max;
  }
  // Nombre de nodes de l'ARBRE (exclou el bloc d'enllaços creuats) per a la densitat.
  function treeNodeCount() {
    var s = C.splitCross(md());
    return s.tree.split('\n').filter(isItemLn).length;
  }
  // Motius de bloqueig (string per al tooltip) o null si l'operació és permesa.
  function depthReason(anchorLi) {
    if (anchorLi == null || !deepBlocked(anchorLi)) return null;
    var cap = depthCap();
    return 'profunditat màx ' + (cap === Infinity ? '∞' : cap) + ' nivells';
  }
  function branchReason(parentLi) {
    return branchFull(parentLi) ? ('màx ' + branchMax() + ' branques') : null;
  }
  function subelReason(parentPropLi) {
    return subelFull(parentPropLi) ? ('màx ' + subelMax() + ' sub-elements') : null;
  }

  // ── Estat de la font única ──
  function md() { return (state.cont && state.cont.dataset.md) || ''; }

  // Mateix filtre que el renderitzador (renderMermaidBlock): treu capçaleres
  // ## / blocs ``` / cites >. Normalitzem dataset.md a aquesta forma a attach()
  // perquè els data-line del SVG (calculats sobre el md filtrat) quadrin amb els
  // índexs de línia que fan servir les mutacions del nucli. El renderitzador ja
  // desa la forma filtrada després de qualsevol edició de label, així que és
  // coherent amb el seu comportament.
  function filterMd(raw) {
    return (raw || '').split('\n').filter(function (l) {
      return !l.match(/^##\s+/) && !l.match(/^```/) && !l.match(/^>/);
    }).join('\n').trim();
  }

  function isContVisible() {
    return !!(state.cont && state.cont.offsetParent !== null);
  }

  // ── Render + decoració (barra de control + toolbar de font) ──
  function rerender() {
    if (!state.cont || !window.ATNE_MERMAID) return;
    state.cont.classList.remove('mermaid-active');
    state.cont.innerHTML = '';
    window.ATNE_MERMAID.renderMermaidBlock(state.cont, md(), state.type);
    decorate();          // l'observer també hi arriba; ho fem síncron pel render immediat
    updateBadge();
    refreshBtns();
  }

  function setMd(newMd, opts) {
    if (!state.cont) return;
    state.undo.push(md());
    if (state.undo.length > 80) state.undo.shift();
    state.redo = [];                       // una acció nova invalida el refés
    state.cont.dataset.md = newMd;
    rerender();
    if (opts && opts.openLine != null) setTimeout(function () { openPopupFor(opts.openLine); }, 90);
  }
  function undo() {
    if (!state.undo.length) return;
    state.redo.push(md());
    state.cont.dataset.md = state.undo.pop();
    rerender();
  }
  function redo() {
    if (!state.redo.length) return;
    state.undo.push(md());
    state.cont.dataset.md = state.redo.pop();
    rerender();
  }
  function openPopupFor(lineIdx) {
    if (!state.cont) return;
    var g = state.cont.querySelector('g[data-line="' + lineIdx + '"]');
    if (g) g.dispatchEvent(new MouseEvent('click', { bubbles: true }));
  }

  function refreshBtns() {
    [[ui.undoBtn, state.undo.length], [ui.redoBtn, state.redo.length]].forEach(function (p) {
      var b = p[0]; if (!b) return;
      var empty = !p[1];
      b.disabled = empty;
      b.style.opacity = empty ? '.4' : '1';
      b.style.cursor = empty ? 'default' : 'pointer';
    });
  }
  function crossCount() { return (C.splitCross(md()).cross || []).length; }
  function updateBadge() {
    if (!ui.badge) return;
    var n = treeNodeCount();
    var cap = depthCap();
    var capTxt = (cap === Infinity) ? 'profunditat lliure' : ('fins a ' + cap + ' nivells');
    var dmax = densitatMax();
    var nx = crossCount();
    // Enllaços creuats: el principi Novak (i CmapTools) en demana POCS. Llindar tou
    // (≤ CROSS_REC); avís, no bloqueig. NOTA: aquesta xifra hauria de venir del canon
    // (handoff a mineriaRAG, pendent) — de moment és un valor de plataforma documentat.
    var CROSS_REC = 3;
    var dOver = (dmax !== Infinity && n > dmax);
    var xOver = nx > CROSS_REC;
    var crossTxt = nx ? (' · ' + nx + ' connexi' + (nx === 1 ? 'ó' : 'ons') + (xOver ? ' (massa?)' : '')) : '';
    ui.badge.textContent = n + ' nodes' + (dOver ? ' (≤ ' + dmax + ')' : '') +
      ' · ' + normMecr(state.mecr) + ' · ' + capTxt + crossTxt;
    var warn = dOver || xOver;
    ui.badge.style.color = warn ? '#dc2626' : '#6d28d9';
    ui.badge.style.fontWeight = warn ? '700' : '600';
  }

  // Injecta la barra de control + la mini-toolbar de font dins del wrapper del
  // diagrama. Idempotent (no re-injecta si ja hi és). Es torna a cridar després
  // de cada render via MutationObserver, perquè el renderitzador refà el wrapper.
  function decorate() {
    if (!state.cont) return;
    var wrap = state.cont.querySelector('.mermaid-wrapper');
    if (!wrap || wrap.querySelector('.atne-ed-bar')) return;
    if (observer) observer.disconnect();   // evita re-entrada per les nostres pròpies mutacions

    var bar = document.createElement('div');
    bar.className = 'atne-ed-bar';
    bar.style.cssText = 'display:flex;gap:7px;align-items:center;flex-wrap:wrap;' +
      'margin:0 0 8px;padding:6px 9px;background:#f5f3ff;border:1px solid #ede9fe;' +
      'border-radius:8px;font-family:system-ui,sans-serif';

    ui.undoBtn = mkCtrl('↶ Desfés', 'Desfés (Ctrl+Z)', undo);
    ui.redoBtn = mkCtrl('↷ Refés', 'Refés (Ctrl+Y)', redo);
    var hint = document.createElement('span');
    hint.textContent = (state.type === 'mapa_conceptual')
      ? 'Clica un node per editar-lo, afegir-hi o connectar-lo'
      : 'Clica un node per editar-lo o afegir-hi branques';
    hint.style.cssText = 'font-size:11.5px;color:#7c3aed';
    ui.badge = document.createElement('span');
    ui.badge.className = 'atne-ed-badge';
    ui.badge.style.cssText = 'margin-left:auto;font-size:11.5px;color:#6d28d9;font-weight:600';

    bar.appendChild(ui.undoBtn);
    bar.appendChild(ui.redoBtn);
    bar.appendChild(hint);
    bar.appendChild(ui.badge);
    wrap.insertBefore(bar, wrap.firstChild);

    enhanceSourceEditor(wrap);
    refreshBtns(); updateBadge();

    if (observer) observer.observe(state.cont, { childList: true, subtree: true });
  }

  function mkCtrl(label, title, fn) {
    var b = document.createElement('button');
    b.type = 'button'; b.textContent = label; b.title = title;
    b.className = 'atne-ed-ctrl';
    b.style.cssText = 'border:1px solid #ddd6fe;background:#fff;color:#6d28d9;' +
      'border-radius:6px;padding:3px 9px;font-size:12px;font-family:system-ui,sans-serif';
    b.addEventListener('click', function (e) { e.preventDefault(); fn(); });
    return b;
  }

  // ── Botons contextuals injectats al popup d'edició de node existent ──
  document.addEventListener('click', function (e) {
    if (!state.cont) return;
    var t = e.target;
    while (t && t.nodeType === 1 && !(t.hasAttribute && t.hasAttribute('data-nid'))) t = t.parentElement;
    if (!t || t.nodeType !== 1 || !t.hasAttribute('data-nid')) return;
    if (!state.cont.contains(t)) return;   // només el nostre diagrama (mapa conceptual)
    state.lastLine = parseInt(t.getAttribute('data-line'), 10);
    state.lastLabel = t.getAttribute('data-lbl') || '';
    setTimeout(injectButtons, 70);
  }, true);

  function mkBtn(label, title, cls, fn) {
    var b = document.createElement('button');
    b.type = 'button'; b.textContent = label; b.title = title;
    b.className = 'popup-ext-btn' + (cls ? ' ' + cls : '');
    b.style.cssText = 'border:1px solid #ddd6fe;background:#faf5ff;color:#6d28d9;' +
      'border-radius:6px;padding:4px 8px;font-size:12px;cursor:pointer;' +
      'font-family:system-ui,sans-serif;white-space:nowrap';
    if (cls === 'del') b.style.cssText += 'border-color:#fecaca;background:#fef2f2;color:#dc2626;';
    if (cls === 'cross') b.style.cssText += 'border-color:#fed7aa;background:#fff7ed;color:#c2410c;';
    b.addEventListener('click', function (ev) { ev.stopPropagation(); fn(); });
    return b;
  }
  // Botó gatejat per la modulació del canon (B4): si una operació supera un límit
  // (profunditat o amplada) es mostra inactiu amb l'explicació, en lloc d'amagar-lo.
  function gatedBtn(label, title, reason, fn) {
    if (reason) {
      var b = mkBtn(label, 'Límit del canon per a ' + normMecr(state.mecr) + ': ' + reason +
        '. Puja el MECR o canvia el límit al canon.', '', function () {});
      b.disabled = true; b.style.opacity = '.4'; b.style.cursor = 'not-allowed';
      return b;
    }
    return mkBtn(label, title, '', fn);
  }
  function closePopup() { var p = document.getElementById('atne-node-popup'); if (p) p.remove(); }
  function addPropAndConcept(li) {
    var r1 = C.addChild(md(), li, 'enllaç', true);
    var r2 = C.addChild(r1.md, r1.newLineIdx, 'Nou concepte');
    closePopup(); state.lastLine = null;
    setMd(r2.md, { openLine: r1.newLineIdx });
  }

  function injectButtons() {
    var pop = document.getElementById('atne-node-popup');
    if (!pop || pop.querySelector('.popup-ext-btn') || state.lastLine == null) return;
    var li = state.lastLine, kind = C.classify(md(), li);
    var bar = document.createElement('div');
    bar.style.cssText = 'display:flex;gap:5px;margin-left:6px;padding-left:8px;' +
      'border-left:1px solid #e9d5ff;flex-wrap:wrap;align-items:center';

    // ── Mapa mental / esquema visual: arbre jeràrquic PUR. Sense proposicions ni
    //    enllaços creuats — només + branca (fill) / + germà / ×. La profunditat es
    //    gateja des del canon del tipus (esquema sí; mapa mental sense límit fins
    //    que mineriaRAG el canonitzi). La densitat és avís tou al badge.
    if (state.type !== 'mapa_conceptual') {
      bar.appendChild(gatedBtn('+ branca', 'Afegir una branca filla',
        depthReason(li),
        function () {
          var r = C.addChild(md(), li, 'Nova branca');
          closePopup(); state.lastLine = null;
          setMd(r.md, { openLine: r.newLineIdx });
        }));
      if (kind !== 'root') {
        // Germà: mateix nivell (no afegeix profunditat). A l'arrel no s'ofereix
        // (un segon node a sangria 0 trencaria l'arbre d'arrel única).
        bar.appendChild(mkBtn('+ germà', 'Afegir una branca germana', '', function () {
          var r = C.addSibling(md(), li, 'Nova branca');
          closePopup(); state.lastLine = null;
          setMd(r.md, { openLine: r.newLineIdx });
        }));
        bar.appendChild(mkBtn('×', 'Eliminar', 'del', function () {
          var nd = C.descendantCount(md(), li);
          if (nd > 0 && !confirm('Aquest node té ' + nd + ' descendent(s). Eliminar tota la branca?')) return;
          var r = C.deleteSubtree(md(), li);
          closePopup(); state.lastLine = null;
          setMd(r.md);
        }));
      }
      pop.appendChild(bar);
      return;
    }

    if (kind === 'root') {
      // Nova branca sota l'arrel: gate per profunditat (nova prop) + amplada (branques de l'arrel).
      bar.appendChild(gatedBtn('+ proposició', 'Nova branca: paraula d’enllaç + concepte',
        depthReason(li) || branchReason(li),
        function () { addPropAndConcept(li); }));
    } else if (kind === 'prop') {
      // Sub-element sota la proposició: gate per amplada (sub-elements d'aquesta prop).
      bar.appendChild(gatedBtn('+ concepte', 'Afegir un concepte sota aquesta proposició',
        subelReason(li),
        function () {
          var r = C.addChild(md(), li, 'Nou concepte');
          closePopup(); state.lastLine = null;
          setMd(r.md, { openLine: r.newLineIdx });
        }));
      // Proposició germana: mateix nivell (sense gate de profunditat) → amplada del pare.
      bar.appendChild(gatedBtn('+ proposició', 'Proposició germana',
        branchReason(parentOf(li)),
        function () {
          var r = C.addSibling(md(), li, 'enllaç');
          closePopup(); state.lastLine = null;
          setMd(r.md, { openLine: r.newLineIdx });
        }));
    } else if (kind === 'concept') {
      // Concepte germà: mateix nivell → amplada del pare (sub-elements de la prop pare).
      bar.appendChild(gatedBtn('+ germà', 'Concepte germà',
        subelReason(parentOf(li)),
        function () {
          var r = C.addSibling(md(), li, 'Nou concepte');
          closePopup(); state.lastLine = null;
          setMd(r.md, { openLine: r.newLineIdx });
        }));
      // La cadena Novak continua en profunditat: concepte -> enllaç -> concepte.
      // Gate per profunditat (nova prop) + amplada (relacions d'aquest concepte).
      bar.appendChild(gatedBtn('+ proposició', 'Aprofundir: paraula d’enllaç + concepte sota aquest',
        depthReason(li) || branchReason(li),
        function () { addPropAndConcept(li); }));
    }
    if (kind !== 'root') {
      bar.appendChild(mkBtn('×', 'Eliminar', 'del', function () {
        var nd = C.descendantCount(md(), li);
        if (nd > 0 && !confirm('Aquest node té ' + nd + ' descendent(s). Eliminar tota la branca?')) return;
        var r = C.deleteSubtree(md(), li);
        closePopup(); state.lastLine = null;
        setMd(r.md);
      }));
    }
    // Connectar amb un altre concepte (enllaç creuat Novak). Usem data-lbl (fiable).
    var nodeLabel = state.lastLabel || '';
    bar.appendChild(mkBtn('↝ connectar', 'Enllaç creuat cap a un altre concepte', 'cross', function () {
      startConnect(nodeLabel);
      closePopup(); state.lastLine = null;
    }));
    pop.appendChild(bar);
  }

  // ── Mode connexió (enllaços creuats) ──
  function startConnect(fromLabel) {
    if (!state.cont) return;
    var banner = document.createElement('div');
    banner.id = 'connect-banner';
    banner.style.cssText = 'position:fixed;top:10px;left:50%;transform:translateX(-50%);z-index:10000;' +
      'background:#ea580c;color:#fff;padding:8px 16px;border-radius:99px;font-size:13px;' +
      'box-shadow:0 6px 24px rgba(234,88,12,.35);font-family:system-ui,sans-serif;cursor:pointer';
    banner.textContent = 'Connectant des de «' + fromLabel + '» — clica el concepte de destí (Esc o clic aquí per cancel·lar)';
    banner.addEventListener('click', cancelConnect);
    document.body.appendChild(banner);
    state.connecting = fromLabel;
    state.cont.querySelectorAll('g[data-nid]').forEach(function (g) {
      g.style.outline = '2px dashed #fdba74'; g.style.outlineOffset = '2px';
    });
    document.addEventListener('keydown', escConnect, true);
  }
  function escConnect(e) { if (e.key === 'Escape') cancelConnect(); }
  function cancelConnect() {
    state.connecting = null;
    var b = document.getElementById('connect-banner'); if (b) b.remove();
    if (state.cont) state.cont.querySelectorAll('g[data-nid]').forEach(function (g) { g.style.outline = ''; });
    document.removeEventListener('keydown', escConnect, true);
  }
  // Captura el clic de destí en mode connexió (fase de captura, abans del popup)
  document.addEventListener('click', function (e) {
    if (state.type !== 'mapa_conceptual') return;   // enllaços creuats = només Novak
    if (!state.connecting || !state.cont) return;
    var t = e.target;
    while (t && t.nodeType === 1 && !(t.hasAttribute && t.hasAttribute('data-nid'))) t = t.parentElement;
    if (!t || t.nodeType !== 1 || !t.hasAttribute('data-nid') || !state.cont.contains(t)) return;
    e.stopPropagation(); e.preventDefault();
    var toLbl = t.getAttribute('data-lbl') || '';
    var from = state.connecting;
    cancelConnect();
    if (!toLbl) return;
    if (toLbl === from) { alert('No pots connectar un concepte amb ell mateix.'); return; }
    var link = window.prompt('Com es relacionen «' + from + '» → «' + toLbl +
      '»?\nEscriu la paraula d’enllaç (p. ex. «és imprescindible per a», «provoca»):', '');
    if (link && link.trim()) setMd(C.addCross(md(), from, toLbl, link.trim()));
  }, true);

  // ── Clic sobre etiqueta d'enllaç creuat -> editar paraula o eliminar ──
  document.addEventListener('click', function (e) {
    if (state.type !== 'mapa_conceptual') return;   // enllaços creuats = només Novak
    if (state.connecting || !state.cont) return;
    var t = e.target;
    while (t && t.nodeType === 1 && !(t.hasAttribute && t.hasAttribute('data-cross-idx'))) t = t.parentElement;
    if (!t || t.nodeType !== 1 || !t.hasAttribute('data-cross-idx') || !state.cont.contains(t)) return;
    e.stopPropagation();
    var idx = parseInt(t.getAttribute('data-cross-idx'), 10);
    var cross = C.splitCross(md()).cross[idx];
    if (!cross) return;
    showCrossPopup(t, cross, idx);
  }, true);

  function showCrossPopup(anchorEl, cross, idx) {
    var old = document.getElementById('atne-cross-popup'); if (old) old.remove();
    var bbox = anchorEl.getBoundingClientRect();
    var pop = document.createElement('div');
    pop.id = 'atne-cross-popup';
    pop.style.cssText =
      'position:fixed;z-index:9999;background:#fff;border:2px solid #ea580c;border-radius:10px;' +
      'padding:8px 10px;box-shadow:0 8px 32px rgba(234,88,12,.2);display:flex;gap:7px;align-items:center;' +
      'font-family:system-ui,sans-serif;font-size:12.5px';
    var ww = window.innerWidth;
    var left = Math.max(4, Math.min(bbox.left + bbox.width / 2 - 150, ww - 304));
    var top = bbox.top - 52; if (top < 8) top = bbox.bottom + 6;
    pop.style.left = left + 'px'; pop.style.top = top + 'px';

    var lblTxt = document.createElement('span');
    lblTxt.textContent = cross.from + ' → ' + cross.to;
    lblTxt.style.cssText = 'color:#94a3b8;font-size:11px;max-width:120px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap';

    var inp = document.createElement('input');
    inp.type = 'text'; inp.value = cross.link;
    inp.style.cssText = 'border:1.5px solid #fed7aa;border-radius:6px;padding:5px 8px;font-size:12.5px;width:140px;outline:none;color:#1e293b';
    inp.addEventListener('keydown', function (ev) {
      if (ev.key === 'Enter') save();
      if (ev.key === 'Escape') pop.remove();
    });
    function save() {
      var v = inp.value.trim(); pop.remove();
      if (v && v !== cross.link) setMd(C.updateCrossLink(md(), idx, v));
    }
    var btnSave = document.createElement('button');
    btnSave.textContent = 'Desa'; btnSave.type = 'button';
    btnSave.style.cssText = 'border:none;background:#ea580c;color:#fff;border-radius:6px;padding:5px 10px;font-size:12px;cursor:pointer';
    btnSave.onclick = save;

    var btnDel = document.createElement('button');
    btnDel.textContent = '×'; btnDel.type = 'button'; btnDel.title = 'Eliminar la connexió';
    btnDel.style.cssText = 'border:1px solid #fecaca;background:#fef2f2;color:#dc2626;border-radius:6px;padding:5px 9px;font-size:13px;cursor:pointer;font-weight:700';
    btnDel.onclick = function () { pop.remove(); setMd(C.removeCross(md(), idx)); };

    pop.appendChild(lblTxt); pop.appendChild(inp); pop.appendChild(btnSave); pop.appendChild(btnDel);
    document.body.appendChild(pop);
    inp.focus(); inp.select();
    setTimeout(function () {
      function close(ev) { if (!pop.contains(ev.target)) { pop.remove(); document.removeEventListener('mousedown', close, true); } }
      document.addEventListener('mousedown', close, true);
    }, 60);
  }

  // ── Mini-toolbar sobre l'editor de font del renderitzador ──
  // El renderitzador (buildEdit) ja crea un <details> amb .mermaid-edit-textarea i
  // un botó "Refés". Hi enganxem una toolbar (sagnat / negreta / cursiva / nova
  // línia) i encaminem el "commit" pel nostre setMd perquè entri al desfés. NO fem
  // re-render a cada tecla: el textarea viu DINS del wrapper que el render refà, i
  // un re-render per pulsació robaria el focus. El diagrama s'actualitza en sortir
  // del textarea (blur) o amb "Refés".
  function enhanceSourceEditor(wrap) {
    var ta = wrap.querySelector('.mermaid-edit-textarea');
    if (!ta || ta.dataset.atneEnhanced) return;
    ta.dataset.atneEnhanced = '1';
    ta.value = md();   // assegura que reflecteix la font vigent
    // Una mica més ample i alt de sortida (es demanava al feedback 13/06).
    ta.style.width = '100%';
    ta.style.minHeight = '170px';
    ta.style.minWidth = '440px';

    var details = ta.closest('details') || wrap;
    var tb = document.createElement('div');
    tb.className = 'atne-src-toolbar';
    tb.style.cssText = 'display:flex;gap:5px;margin:6px 0 4px;flex-wrap:wrap';
    tb.appendChild(mkTb('→ Sagnat', 'Sagna la selecció (Tab)', function () { doShift(ta, 1); }));
    tb.appendChild(mkTb('← Treu sagnat', 'Treu sagnat (Maj+Tab)', function () { doShift(ta, -1); }));
    tb.appendChild(mkTb('Negreta', 'Negreta (Ctrl+B)', function () { doWrap(ta, '**'); }));
    tb.appendChild(mkTb('Cursiva', 'Cursiva (Ctrl+I)', function () { doWrap(ta, '*'); }));
    ta.parentNode.insertBefore(tb, ta);

    ta.addEventListener('keydown', function (e) {
      if (e.key === 'Tab') { e.preventDefault(); doShift(ta, e.shiftKey ? -1 : 1); }
      else if ((e.ctrlKey || e.metaKey) && !e.shiftKey && e.key.toLowerCase() === 'b') { e.preventDefault(); doWrap(ta, '**'); }
      else if ((e.ctrlKey || e.metaKey) && !e.shiftKey && e.key.toLowerCase() === 'i') { e.preventDefault(); doWrap(ta, '*'); }
    });
    // Commit del text editat → font única + desfés, en perdre el focus.
    ta.addEventListener('blur', function () {
      var v = filterMd(ta.value);
      if (v && v !== md()) setMd(v);
    });
    // Substitueix el botó "Refés" del renderitzador perquè el commit passi pel
    // nostre desfés (un clon perd el listener original del renderitzador).
    var btn = wrap.querySelector('.mermaid-rerender-btn');
    if (btn) {
      var clone = btn.cloneNode(true);
      btn.parentNode.replaceChild(clone, btn);
      clone.addEventListener('mousedown', function (e) { e.preventDefault(); });   // no robis el focus
      clone.addEventListener('click', function () {
        var v = filterMd(ta.value);
        if (v && v !== md()) setMd(v);
      });
    }
  }
  function mkTb(label, title, fn) {
    var b = document.createElement('button');
    b.type = 'button'; b.textContent = label; b.title = title;
    b.style.cssText = 'border:1px solid #ddd6fe;background:#fff;color:#6d28d9;border-radius:6px;' +
      'padding:3px 8px;font-size:11.5px;cursor:pointer;font-family:system-ui,sans-serif';
    // CLAU: preventDefault al mousedown perquè el botó NO robi el focus al textarea.
    // Sense això, el textarea fa blur → commit → re-render → "surts de l'editor".
    b.addEventListener('mousedown', function (e) { e.preventDefault(); });
    b.addEventListener('click', function (e) { e.preventDefault(); fn(); });
    return b;
  }
  function doShift(ta, dir) {
    var v = C.shiftLines(ta.value, ta.selectionStart, ta.selectionEnd, dir);
    var d = dir > 0 ? 2 : -2;
    setTaValue(ta, v, Math.max(0, ta.selectionStart + d), Math.max(0, ta.selectionEnd + d));
  }
  function doWrap(ta, mk) {
    var r = C.wrapSelection(ta.value, ta.selectionStart, ta.selectionEnd, mk);
    setTaValue(ta, r.text, r.selStart, r.selEnd);
  }
  // Edita NOMÉS el textarea (sense re-render → conserva el focus). El commit a la
  // font única es fa al blur / "Refés", capturant tota la sessió com un sol desfés.
  function setTaValue(ta, text, selStart, selEnd) {
    ta.value = text;
    if (selStart != null) ta.setSelectionRange(selStart, selEnd != null ? selEnd : selStart);
    ta.focus();
  }

  // ── Desfés / refés per teclat (només quan el diagrama és visible) ──
  document.addEventListener('keydown', function (e) {
    if (!state.attached || !isContVisible()) return;
    var k = e.key.toLowerCase();
    if ((e.ctrlKey || e.metaKey) && k === 'z' && !e.shiftKey) { e.preventDefault(); undo(); }
    else if ((e.ctrlKey || e.metaKey) && (k === 'y' || (k === 'z' && e.shiftKey))) { e.preventDefault(); redo(); }
  });

  // ── API pública: bootstrap de producció (substitueix el DOMContentLoaded del
  //    banc de proves). La pàgina del Pas 3 crida attach() en mostrar el mapa. ──
  function attach(cont, opts) {
    if (!cont) return;
    opts = opts || {};
    if (opts.mecr) state.mecr = opts.mecr;
    // El tipus de diagrama (mapa_conceptual | mapa_mental | esquema_visual) governa
    // el joc de botons, els listeners de connexió i la font de límits del canon.
    if (opts.type) state.type = opts.type;
    if (state.attached && state.cont === cont) { decorate(); updateBadge(); return; }
    // Normalitza la font al md filtrat → els data-line del render quadren amb els
    // índexs de línia de les mutacions del nucli (sense re-renderitzar).
    cont.dataset.md = filterMd(cont.dataset.md);
    state.cont = cont;
    state.attached = true;
    state.undo = []; state.redo = [];
    if (observer) observer.disconnect();
    observer = new MutationObserver(function () { decorate(); });
    observer.observe(cont, { childList: true, subtree: true });
    decorate(); updateBadge();
  }

  window.ATNE_DIAGRAM_EDITOR = { attach: attach };
})();
