/**
 * ATNE · diagram-renderer.js v7 — SVG pur + edició gràfica in-place
 *
 * Clic en qualsevol node → popup d'edició → re-render automàtic
 * Cap dependència externa. Funciona offline.
 *
 * mapa_conceptual → Novak, TD, gradient+ombra, proposicions a les arestes
 * mapa_mental     → Buzan, lateral, branques en cinta degradada (tapered ribbon)
 * esquema_visual  → Jerarquia LR, codificació de profunditat
 */
(function () {
  'use strict';

  var NS = 'http://www.w3.org/2000/svg';

  // Llegeix la font seleccionada a ATNE (localStorage + window.ATNE_FONTS)
  function pageFont() {
    try {
      var key = localStorage.getItem('atne.font_key');
      if (key && window.ATNE_FONTS && window.ATNE_FONTS[key]) {
        return window.ATNE_FONTS[key].css;
      }
    } catch (e) {}
    return 'system-ui,-apple-system,sans-serif';
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // SVG UTILITIES
  // ─────────────────────────────────────────────────────────────────────────────

  function el(tag, attrs, children) {
    var e = document.createElementNS(NS, tag);
    if (attrs) Object.keys(attrs).forEach(function (k) { e.setAttribute(k, attrs[k]); });
    if (children) children.forEach(function (c) { if (c) e.appendChild(c); });
    return e;
  }

  function txt(s, attrs) { var t = el('text', attrs); t.textContent = s; return t; }

  function tw(label, fs) { return label.length * (fs || 12) * 0.57; }

  function wrap(label, maxPx, fs) {
    var cw = (fs || 12) * 0.57, max = Math.max(7, Math.floor(maxPx / cw));
    if (label.length <= max) return [label];
    var words = label.split(' '), lines = [], cur = '';
    words.forEach(function (w) {
      var test = cur ? cur + ' ' + w : w;
      if (test.length <= max) { cur = test; } else { if (cur) lines.push(cur); cur = w; }
    });
    if (cur) lines.push(cur);
    return lines.length ? lines : [label.slice(0, max) + '…'];
  }

  function mtext(lines, cx, cy, fs, attrs) {
    var g = el('g'), lh = (fs || 12) * 1.4, dy = -(lines.length - 1) * lh / 2;
    lines.forEach(function (l) {
      var t = txt(l, Object.assign({ x: cx, y: cy + dy, 'font-size': fs || 12,
        'text-anchor': 'middle', 'dominant-baseline': 'central' }, attrs || {}));
      g.appendChild(t); dy += lh;
    });
    return g;
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // PARSING — guarda lineIdx per a l'edició
  // ─────────────────────────────────────────────────────────────────────────────

  function indentLv(line) {
    var m = line.match(/^(\s*)/);
    return m ? Math.floor(m[1].replace(/\t/g, '  ').length / 2) : 0;
  }
  function rawLbl(line) { return line.replace(/^\s*-\s+/, '').replace(/\*\*/g, '').trim(); }
  function isBoldLn(line) { return /^\s*-\s+\*\*.+\*\*$/.test(line); }

  // parseTree: cada node inclou lineIdx (índex a la línia original del md filtrat)
  function parseTree(md) {
    var rawLines = md.split('\n');
    var lines = [], lineMap = [];  // línies filtrades + índex original
    rawLines.forEach(function (l, i) {
      var t = l.trim();
      if (t && !t.startsWith('#') && !t.startsWith('```') && !t.startsWith('>')) {
        lines.push(l); lineMap.push(i);
      }
    });
    if (!lines.length) return null;
    var lvs = lines.map(indentLv), min = Math.min.apply(null, lvs);
    var cnt = 0, root = null, stack = [];
    for (var i = 0; i < lines.length; i++) {
      var lv = lvs[i] - min, lbl = rawLbl(lines[i]);
      if (!lbl) continue;
      var node = { nid: cnt++, label: lbl, bold: isBoldLn(lines[i]),
                   lineIdx: lineMap[i], children: [] };
      if (!root) { root = node; stack = [{ lv: 0, node: node }]; continue; }
      while (stack.length > 1 && stack[stack.length - 1].lv >= lv) stack.pop();
      stack[stack.length - 1].node.children.push(node);
      stack.push({ lv: lv, node: node });
    }
    return root;
  }

  // Aplana l'arbre en nodes + edges
  // Nodes bold (no arrel) → nodes proposició (isProp=true), sense caixa, text cursiu
  // L'arrel sempre és node concepte, fins i tot si és bold al markdown
  function treeToGraph(root) {
    var nodes = [], edges = [], cnt = 0;
    function visit(node, parentId) {
      if (!node) return;
      var isRoot = (parentId === null);
      if (node.bold && !isRoot) {
        var pid = 'p' + cnt++;
        nodes.push({ id: pid, label: node.label, isProp: true, lineIdx: node.lineIdx });
        edges.push({ s: parentId, t: pid });
        node.children.forEach(function (c) { visit(c, pid); });
      } else {
        var id = 'c' + cnt++;
        nodes.push({ id: id, label: node.label, root: isRoot, lineIdx: node.lineIdx });
        if (!isRoot) edges.push({ s: parentId, t: id });
        node.children.forEach(function (c) { visit(c, id); });
      }
    }
    visit(root, null);
    return { nodes: nodes, edges: edges };
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // EDICIÓ GRÀFICA
  // ─────────────────────────────────────────────────────────────────────────────

  // Actualitza el label d'una línia del markdown conservant la sintaxi (guió, negreta)
  function updateLine(md, lineIdx, newLabel) {
    var lines = md.split('\n');
    if (lineIdx < 0 || lineIdx >= lines.length) return md;
    var line = lines[lineIdx];
    var boldM  = line.match(/^(\s*-\s+)\*\*(.+)\*\*\s*$/);
    var plainM = line.match(/^(\s*-\s+)(.+)$/);
    if (boldM)  lines[lineIdx] = boldM[1]  + '**' + newLabel + '**';
    else if (plainM) lines[lineIdx] = plainM[1] + newLabel;
    return lines.join('\n');
  }

  // Popup d'edició flotant — sempre dins del viewport
  function showEditPopup(nodeGroupEl, currentLabel, onSave) {
    var old = document.getElementById('atne-node-popup');
    if (old) old.remove();

    var bbox = nodeGroupEl.getBoundingClientRect();
    var popW = 248, popH = 48;
    var ww = window.innerWidth, wh = window.innerHeight;
    var left = bbox.left + bbox.width / 2 - popW / 2;
    var top  = bbox.top - popH - 8;
    if (top < 8) top = bbox.bottom + 6;
    left = Math.max(4, Math.min(left, ww - popW - 4));
    top  = Math.max(4, Math.min(top,  wh - popH - 4));

    var pop = document.createElement('div');
    pop.id = 'atne-node-popup';
    pop.style.cssText =
      'position:fixed;left:' + left + 'px;top:' + top + 'px;z-index:9999;' +
      'background:#fff;border:2px solid #6d28d9;border-radius:10px;' +
      'padding:8px 10px;box-shadow:0 8px 32px rgba(109,40,217,.18);' +
      'display:flex;gap:7px;align-items:center;font-family:system-ui,sans-serif';

    var inp = document.createElement('input');
    inp.type = 'text'; inp.value = currentLabel;
    inp.style.cssText =
      'border:1.5px solid #ddd6fe;border-radius:6px;padding:5px 8px;' +
      'font-size:12.5px;width:190px;outline:none;color:#1e293b;font-family:inherit;' +
      'transition:border-color .15s';
    inp.addEventListener('focus',  function () { inp.style.borderColor = '#6d28d9'; });
    inp.addEventListener('blur',   function () { inp.style.borderColor = '#ddd6fe'; });

    var btn = document.createElement('button');
    btn.textContent = '✓';
    btn.style.cssText =
      'background:#6d28d9;color:#fff;border:none;border-radius:6px;' +
      'padding:5px 10px;cursor:pointer;font-size:13px;font-weight:700;' +
      'transition:opacity .15s';
    btn.addEventListener('mouseover', function () { btn.style.opacity = '.8'; });
    btn.addEventListener('mouseout',  function () { btn.style.opacity = '1'; });

    pop.appendChild(inp);
    pop.appendChild(btn);
    document.body.appendChild(pop);
    inp.focus(); inp.setSelectionRange(0, inp.value.length);

    function save() {
      var val = inp.value.trim(); pop.remove();
      if (val && val !== currentLabel) onSave(val);
    }
    function cancel() { pop.remove(); }

    btn.addEventListener('click', save);
    inp.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { e.preventDefault(); save(); }
      if (e.key === 'Escape') cancel();
      e.stopPropagation();
    });
    // Clic fora → cancel
    setTimeout(function () {
      function handler(e) {
        if (!pop.contains(e.target)) { cancel(); document.removeEventListener('mousedown', handler, true); }
      }
      document.addEventListener('mousedown', handler, true);
    }, 60);
  }

  // Afegeix escoltador de clic als nodes editable d'un SVG
  function addEditListeners(svgEl, filteredMd, cont, compType) {
    svgEl.addEventListener('click', function (e) {
      // Puja des de l'element clicat fins trobar data-nid
      var target = e.target;
      while (target && target !== svgEl) {
        if (target.hasAttribute && target.hasAttribute('data-nid')) break;
        target = target.parentElement;
      }
      if (!target || !target.hasAttribute('data-nid')) return;

      var lineIdx  = parseInt(target.getAttribute('data-line'), 10);
      var label    = target.getAttribute('data-lbl');

      showEditPopup(target, label, function (newLabel) {
        var newMd = updateLine(filteredMd, lineIdx, newLabel);
        cont.dataset.md = newMd;
        cont.classList.remove('mermaid-active');
        cont.innerHTML = '';
        renderMermaidBlock(cont, newMd, compType);
      });
    });
  }

  // Grup SVG per a un node editable
  function nodeGroup(node) {
    return el('g', {
      'data-nid': node.nid !== undefined ? node.nid : '',
      'data-line': node.lineIdx !== undefined ? node.lineIdx : -1,
      'data-lbl': node.label,
      style: 'cursor:pointer',
    });
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // MAPA CONCEPTUAL — Novak, top-down
  // ─────────────────────────────────────────────────────────────────────────────

  // Mapa conceptual — constants
  var CM = {
    RW: 148, RH: 40, RR: 10,   // root: amplada, alçada, radi cantonades
    NW: 108, NH: 34, NR: 7,    // nodes concepte
    PH: 15,                     // alçada zona text proposició
    HG: 32,                     // gap horitzontal entre columnes
    VG: 38,                     // gap vertical arrel → proposicions
    PG: 12,                     // gap proposició → primer fill
    LG: 8,                      // gap entre fills verticals
    M:  28,                     // marge exterior
    PFS: 11,                    // font-size proposicions
  };

  function buildConceptMap(md) {
    var g = treeToGraph(parseTree(md));
    if (!g.nodes.length) return null;

    var byId = {}, kids = {};
    g.nodes.forEach(function (n) { byId[n.id] = n; kids[n.id] = []; });
    g.edges.forEach(function (e) { if (kids[e.s]) kids[e.s].push(e.t); });

    // ── Layout: arrel al centre, proposicions en columnes, fills apilats verticalment ──
    var rootId  = g.nodes[0].id;
    var propIds = kids[rootId] || [];
    var nCols   = Math.max(1, propIds.length);
    var colW    = Math.max(CM.NW, CM.RW / nCols + CM.HG) + CM.HG;
    var totalW  = nCols * colW;

    byId[rootId].x = totalW / 2;
    byId[rootId].y = 0;

    propIds.forEach(function (pid, i) {
      var prop = byId[pid];
      prop.x   = i * colW + colW / 2;
      prop.y   = CM.RH / 2 + CM.VG + CM.PH / 2;

      // Acumulador vertical: tots els fills i néts van en la mateixa columna
      var cy = prop.y + CM.PH / 2 + CM.PG;
      (kids[pid] || []).forEach(function (lid) {
        byId[lid].x = prop.x;
        byId[lid].y = cy + CM.NH / 2;
        cy += CM.NH;
        // Néts (3r nivell) → directament a sota del pare, mateixa columna
        (kids[lid] || []).forEach(function (slid) {
          cy += CM.LG;
          byId[slid].x = prop.x;
          byId[slid].y = cy + CM.NH / 2;
          cy += CM.NH;
        });
        cy += CM.LG;
      });
    });

    // Centra l'arrel sobre totes les proposicions (independentment del nombre)
    if (propIds.length) {
      var propXs = propIds.map(function (pid) { return byId[pid].x; });
      byId[rootId].x = (Math.min.apply(null, propXs) + Math.max.apply(null, propXs)) / 2;
    }

    // ── ViewBox ──
    var all = g.nodes.filter(function (n) { return n.x !== undefined; });
    var xs  = all.map(function (n) { return n.x; });
    var ys  = all.map(function (n) { return n.y; });
    var x0  = Math.min.apply(null, xs) - CM.NW / 2 - CM.M;
    var y0  = Math.min.apply(null, ys) - CM.RH / 2 - CM.M;
    var x1  = Math.max.apply(null, xs) + CM.NW / 2 + CM.M;
    var y1  = Math.max.apply(null, ys) + CM.NH / 2 + CM.M;

    var uid = 'cm' + (Math.random() * 1e9 | 0);
    var svg = el('svg', { viewBox: [x0, y0, x1 - x0, y1 - y0].join(' '), xmlns: NS,
      width: '100%', style: 'max-height:580px;display:block',
      'font-family': pageFont() });

    var defs = el('defs');
    // Ombra subtil per als nodes
    defs.appendChild(el('filter', { id: uid + '-sh', x: '-20%', y: '-20%', width: '140%', height: '140%' }, [
      el('feDropShadow', { dx: 0, dy: 1, stdDeviation: 2.5, 'flood-opacity': 0.10 }),
    ]));
    // Fletxa de punta neta
    defs.appendChild(el('marker', { id: uid + '-arr', viewBox: '0 0 10 10', refX: 9, refY: 5,
      markerWidth: 5, markerHeight: 5, orient: 'auto-start-reverse' },
      [el('path', { d: 'M0,1 L9,5 L0,9 L2.5,5 Z', fill: '#818cf8' })]));
    svg.appendChild(defs);

    // ── Arestes ──
    var gE = el('g');
    g.edges.forEach(function (e) {
      var sn = byId[e.s], tn = byId[e.t];
      if (!sn || tn.x === undefined) return;

      var isRootEdge = sn.root;
      var sx = sn.x, sy = sn.y + (isRootEdge ? CM.RH / 2 : CM.PH / 2 + 2);
      var tx = tn.x, ty = tn.isProp ? tn.y - CM.PH / 2 - 2 : tn.y - CM.NH / 2;

      var d;
      if (Math.abs(sx - tx) < 2) {
        // Mateixa columna: línia recta vertical
        d = 'M ' + sx + ' ' + sy + ' L ' + tx + ' ' + ty;
      } else {
        // Columna diferent: bezier suau
        var my = sy + (ty - sy) * 0.55;
        d = 'M ' + sx + ' ' + sy + ' C ' + sx + ' ' + my + ' ' + tx + ' ' + my + ' ' + tx + ' ' + ty;
      }
      gE.appendChild(el('path', { d: d, stroke: '#a5b4fc', 'stroke-width': 1.5,
        fill: 'none', 'marker-end': 'url(#' + uid + '-arr)' }));
    });
    svg.appendChild(gE);

    // ── Nodes ──
    var gN = el('g');
    g.nodes.forEach(function (n) {
      if (n.x === undefined) return;
      var grp = nodeGroup(n);
      var title = document.createElementNS(NS, 'title');
      title.textContent = 'Clic per editar'; grp.appendChild(title);

      if (n.isProp) {
        // Proposició: text cursiu centrat, sense caixa
        var lines = wrap(n.label, colW - 16, CM.PFS);
        grp.appendChild(mtext(lines, n.x, n.y, CM.PFS, {
          fill: '#4338ca', 'font-style': 'italic', 'font-weight': '600' }));
        // subratllat proporcional
        var uw = Math.min(tw(n.label, CM.PFS), colW - 20) * 0.85;
        grp.appendChild(el('line', {
          x1: n.x - uw / 2, y1: n.y + CM.PFS * 0.9,
          x2: n.x + uw / 2, y2: n.y + CM.PFS * 0.9,
          stroke: '#818cf8', 'stroke-width': 1, 'stroke-opacity': 0.5 }));

      } else if (n.root) {
        // Arrel: rectangle arrodonit fosc, text blanc
        grp.setAttribute('filter', 'url(#' + uid + '-sh)');
        grp.appendChild(el('rect', {
          x: n.x - CM.RW / 2, y: n.y - CM.RH / 2,
          width: CM.RW, height: CM.RH, rx: CM.RR,
          fill: '#312e81', stroke: '#6366f1', 'stroke-width': 1.5 }));
        grp.appendChild(mtext(wrap(n.label, CM.RW - 24, 13), n.x, n.y, 13,
          { fill: '#fff', 'font-weight': '700', 'letter-spacing': '0.3px' }));

      } else {
        // Concepte fill: rectangle clar
        grp.setAttribute('filter', 'url(#' + uid + '-sh)');
        var nw = Math.max(CM.NW, tw(n.label, 12) + 28);
        grp.appendChild(el('rect', {
          x: n.x - nw / 2, y: n.y - CM.NH / 2,
          width: nw, height: CM.NH, rx: CM.NR,
          fill: '#f5f3ff', stroke: '#a5b4fc', 'stroke-width': 1 }));
        grp.appendChild(mtext(wrap(n.label, nw - 18, 12), n.x, n.y, 12,
          { fill: '#1e1b4b' }));
      }
      gN.appendChild(grp);
    });
    svg.appendChild(gN);
    return svg;
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // MAPA MENTAL — Buzan, lateral, tapered ribbon
  // ─────────────────────────────────────────────────────────────────────────────

  var MM = {
    RW: 128, RH: 42, RR: 12, L1H: 32, LNH: 24,
    XS: 180, VG: 18, M: 44, W0: 9, W1: 4, W2: 2,
    PALETTE: ['#4f46e5','#0891b2','#059669','#d97706',
              '#7c3aed','#be185d','#0f766e','#b45309'],
  };

  function ribbon(sx, sy, tx, ty, w1, w2, color) {
    var cpx = (tx - sx) * 0.52, cp1x = sx + cpx, cp2x = tx - cpx;
    var d = ['M', sx, sy - w1 / 2,
      'C', cp1x, sy - w1 / 2, cp2x, ty - w2 / 2, tx, ty - w2 / 2,
      'L', tx, ty + w2 / 2,
      'C', cp2x, ty + w2 / 2, cp1x, sy + w1 / 2, sx, sy + w1 / 2, 'Z'].join(' ');
    return el('path', { d: d, fill: color });
  }

  function buildMindMap(md) {
    var tree = parseTree(md);
    if (!tree) return null;

    function sh(node, d) {
      var base = (d <= 1 ? MM.L1H : MM.LNH) + MM.VG;
      if (!node.children || !node.children.length) return base;
      return Math.max(base, node.children.reduce(function (s, c) { return s + sh(c, d + 1); }, 0));
    }

    tree.x = 0; tree.y = 0; tree.depth = 0;
    var kids   = tree.children || [];
    var nRight = Math.ceil(kids.length / 2);

    function placeGroup(group, dir, depth) {
      if (!group.children || !group.children.length) return;
      var bx = group.x + dir * MM.XS;
      var totH = group.children.reduce(function (s, c) { return s + sh(c, depth); }, 0) - MM.VG;
      var cy = group.y - totH / 2;
      group.children.forEach(function (child) {
        var csh = sh(child, depth);
        child.x = bx; child.y = cy + csh / 2 - MM.VG / 2; child.depth = depth;
        placeGroup(child, dir, depth + 1); cy += csh;
      });
    }
    placeGroup({ x: 0, y: 0, children: kids.slice(0, nRight) },  1, 1);
    placeGroup({ x: 0, y: 0, children: kids.slice(nRight) },    -1, 1);

    kids.forEach(function (k, i) { k.color = MM.PALETTE[i % MM.PALETTE.length]; });
    function propagate(n) { (n.children || []).forEach(function (c) { c.color = c.color || n.color; propagate(c); }); }
    kids.forEach(propagate);

    function allNodes(n) { return [n].concat((n.children || []).reduce(function (a, c) { return a.concat(allNodes(c)); }, [])); }
    var all = allNodes(tree);
    var xs = all.map(function (n) { return n.x; }), ys = all.map(function (n) { return n.y; });
    var x0 = Math.min.apply(null, xs) - 160 - MM.M, y0 = Math.min.apply(null, ys) - MM.L1H - MM.M;
    var x1 = Math.max.apply(null, xs) + 160 + MM.M, y1 = Math.max.apply(null, ys) + MM.L1H + MM.M;

    var uid = 'mm' + (Math.random() * 1e9 | 0);
    var svg = el('svg', { viewBox: [x0, y0, x1 - x0, y1 - y0].join(' '), xmlns: NS,
      width: '100%', style: 'max-height:520px;display:block',
      'font-family': pageFont() });

    var defs = el('defs');
    defs.appendChild(el('filter', { id: uid + '-sh', x: '-20%', y: '-20%', width: '140%', height: '140%' }, [
      el('feDropShadow', { dx: 0, dy: 3, stdDeviation: 4, 'flood-opacity': 0.18 }) ]));
    defs.appendChild(el('linearGradient', { id: uid + '-rg', x1: '0%', y1: '0%', x2: '0%', y2: '100%' }, [
      el('stop', { offset: '0%', 'stop-color': '#334155' }),
      el('stop', { offset: '100%', 'stop-color': '#0f172a' }) ]));
    svg.appendChild(defs);

    var gR = el('g'), gN = el('g');

    function drawNode(node) {
      var grp = nodeGroup(node);
      var title = document.createElementNS(NS, 'title');
      title.textContent = 'Clic per editar'; grp.appendChild(title);

      if (node.depth === 0) {
        grp.setAttribute('filter', 'url(#' + uid + '-sh)');
        grp.appendChild(el('rect', { x: node.x - MM.RW / 2, y: node.y - MM.RH / 2,
          width: MM.RW, height: MM.RH, rx: MM.RR, fill: 'url(#' + uid + '-rg)' }));
        grp.appendChild(txt(node.label, { x: node.x, y: node.y, 'font-size': 14, 'font-weight': '700',
          'text-anchor': 'middle', 'dominant-baseline': 'central', fill: '#fff', 'letter-spacing': '0.3px' }));
      } else {
        var color = node.color || '#64748b';
        var fs = node.depth === 1 ? 13 : 11;
        var nh = node.depth === 1 ? MM.L1H : MM.LNH;
        var ntw = Math.max(60, tw(node.label, fs)) + 18;
        if (node.depth === 1) {
          grp.appendChild(el('rect', { x: node.x - ntw / 2, y: node.y - nh / 2, width: ntw, height: nh,
            rx: nh / 2, fill: color + '18', stroke: color, 'stroke-width': 2 }));
          grp.appendChild(txt(node.label, { x: node.x, y: node.y, 'font-size': fs, 'font-weight': '600',
            'text-anchor': 'middle', 'dominant-baseline': 'central', fill: color }));
        } else {
          var lw2 = tw(node.label, fs) + 4;
          grp.appendChild(el('line', { x1: node.x - lw2 / 2, y1: node.y + nh / 2 - 2,
            x2: node.x + lw2 / 2, y2: node.y + nh / 2 - 2, stroke: color, 'stroke-width': 1.5, 'stroke-opacity': 0.6 }));
          grp.appendChild(txt(node.label, { x: node.x, y: node.y, 'font-size': fs,
            'text-anchor': 'middle', 'dominant-baseline': 'central', fill: '#334155' }));
        }
      }
      gN.appendChild(grp);

      (node.children || []).forEach(function (child) {
        child.parent = node;
        var color = child.color || '#94a3b8';
        var dirX  = child.x > node.x ? 1 : -1;
        var pw = node.depth === 0 ? MM.RW : Math.max(60, tw(node.label, node.depth === 1 ? 13 : 11)) + 18;
        var cw2 = Math.max(60, tw(child.label, child.depth === 1 ? 13 : 11)) + 18;
        var sx = node.x + dirX * pw / 2, sy = node.y;
        var tx = child.x - dirX * cw2 / 2, ty = child.y;
        var w1 = node.depth === 0 ? MM.W0 : child.depth === 1 ? MM.W1 : MM.W2;
        var w2 = child.depth === 1 ? MM.W1 : MM.W2;
        gR.appendChild(ribbon(sx, sy, tx, ty, w1, w2, color));
        drawNode(child);
      });
    }

    drawNode(tree);
    svg.appendChild(gR); svg.appendChild(gN);
    return svg;
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // ESQUEMA VISUAL — jerarquia LR, codificació de profunditat
  // ─────────────────────────────────────────────────────────────────────────────

  var SC = { RW: 130, RH: 38, NW: 110, NH: 32, NR: 8, HG: 56, VG: 14, M: 22 };
  var SC_F = ['#ede9fe', '#f1f5f9', '#f9fafb'];
  var SC_S = ['#6d28d9', '#64748b', '#9ca3af'];
  var SC_T = ['#3b0764', '#1e293b', '#374151'];

  function buildSchema(md) {
    var tree = parseTree(md);
    if (!tree) return null;

    function shH(node) {
      if (!node.children || !node.children.length) return SC.NH + SC.VG;
      return node.children.reduce(function (s, c) { return s + shH(c); }, 0);
    }
    function place(node, x, sy, depth) {
      var h = shH(node); node.x = x; node.y = sy + h / 2 - SC.VG / 2; node.depth = depth;
      var nw = depth === 0 ? SC.RW : SC.NW, cy = sy;
      (node.children || []).forEach(function (c) { var ch = shH(c); place(c, x + nw + SC.HG, cy, depth + 1); cy += ch; });
    }
    place(tree, 0, 0, 0);

    function allNodes(n) { return [n].concat((n.children || []).reduce(function (a, c) { return a.concat(allNodes(c)); }, [])); }
    var all = allNodes(tree);
    var ys = all.map(function (n) { return n.y; });
    var x0 = -SC.M, y0 = Math.min.apply(null, ys) - SC.RH - SC.M;
    var x1 = Math.max.apply(null, all.map(function (n) { return n.x + SC.RW; })) + SC.M;
    var y1 = Math.max.apply(null, ys) + SC.RH + SC.M;

    var uid = 'sc' + (Math.random() * 1e9 | 0);
    var svg = el('svg', { viewBox: [x0, y0, x1 - x0, y1 - y0].join(' '), xmlns: NS,
      width: '100%', style: 'max-height:480px;display:block', 'font-family': pageFont() });

    var defs = el('defs');
    defs.appendChild(el('filter', { id: uid + '-sh', x: '-20%', y: '-20%', width: '140%', height: '140%' }, [
      el('feDropShadow', { dx: 0, dy: 1, stdDeviation: 2, 'flood-opacity': 0.1 }) ]));
    defs.appendChild(el('marker', { id: uid + '-a', viewBox: '0 0 10 10', refX: 9, refY: 5,
      markerWidth: 5, markerHeight: 5, orient: 'auto' },
      [el('path', { d: 'M0,2 L10,5 L0,8 L2.5,5 Z', fill: '#94a3b8' })]));
    svg.appendChild(defs);

    var gL = el('g'), gN = el('g', { filter: 'url(#' + uid + '-sh)' });
    all.forEach(function (n) {
      var d = Math.min(n.depth, SC_F.length - 1);
      var nw = n.depth === 0 ? SC.RW : SC.NW, nh = n.depth === 0 ? SC.RH : SC.NH;
      (n.children || []).forEach(function (c) {
        var sx = n.x + nw, sy = n.y, tx = c.x, ty = c.y, mx = (sx + tx) / 2;
        gL.appendChild(el('path', { d: 'M ' + sx + ' ' + sy + ' C ' + mx + ' ' + sy + ' ' + mx + ' ' + ty + ' ' + tx + ' ' + ty,
          stroke: '#cbd5e1', 'stroke-width': 1.5, fill: 'none', 'marker-end': 'url(#' + uid + '-a)' }));
      });
      var grp = nodeGroup(n);
      var title = document.createElementNS(NS, 'title');
      title.textContent = 'Clic per editar'; grp.appendChild(title);
      grp.appendChild(el('rect', { x: n.x, y: n.y - nh / 2, width: nw, height: nh, rx: SC.NR,
        fill: SC_F[d], stroke: SC_S[d], 'stroke-width': n.depth === 0 ? 2 : 1 }));
      grp.appendChild(mtext(wrap(n.label, nw - 16, 12), n.x + nw / 2, n.y, 12,
        { fill: SC_T[d], 'font-weight': n.depth === 0 ? '700' : '400' }));
      gN.appendChild(grp);
    });
    svg.appendChild(gL); svg.appendChild(gN);
    return svg;
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // CONTROLS UI
  // ─────────────────────────────────────────────────────────────────────────────

  function buildZoom(svgEl) {
    var row = document.createElement('div');
    row.className = 'mermaid-zoom-row';
    row.innerHTML = '<label class="mermaid-zoom-label">Mida <input type="range" ' +
      'class="mermaid-zoom-slider" min="40" max="200" value="100">' +
      '<span class="mermaid-zoom-pct">100%</span></label>';
    var sl = row.querySelector('.mermaid-zoom-slider'), sp = row.querySelector('.mermaid-zoom-pct');
    var wrapper = svgEl.closest('.mermaid-wrapper') || svgEl.parentElement;
    sl.addEventListener('input', function () {
      var pct = +sl.value;
      sp.textContent = pct + '%';
      // Escalat per amplada: el SVG creix i el wrapper fa scroll si cal
      svgEl.style.width  = pct + '%';
      svgEl.style.height = 'auto';
      wrapper.style.maxHeight = pct > 100 ? '640px' : '';
      wrapper.style.overflowX = pct > 100 ? 'auto' : '';
      wrapper.style.overflowY = pct > 100 ? 'auto' : '';
    });
    return row;
  }

  function buildEdit(mdRaw, cont, type) {
    var d = document.createElement('details'); d.className = 'mermaid-edit-details';
    var s = document.createElement('summary'); s.className = 'mermaid-edit-toggle';
    s.innerHTML = '<svg viewBox="0 0 16 16" width="11" fill="currentColor"><path d="M11.013 1.427a1.75 1.75 0 0 1 2.474 0l1.086 1.086a1.75 1.75 0 0 1 0 2.474l-8.61 8.61c-.21.21-.47.364-.756.445l-3.251.93a.75.75 0 0 1-.927-.928l.929-3.25c.081-.286.235-.547.445-.758l8.61-8.61zm1.414 1.06a.25.25 0 0 0-.354 0l-8.61 8.61a.25.25 0 0 0-.064.108l-.681 2.382 2.382-.68a.25.25 0 0 0 .108-.065l8.61-8.61a.25.25 0 0 0 0-.353z"/></svg> Editar font del diagrama';
    var ta = document.createElement('textarea');
    ta.className = 'mermaid-edit-textarea'; ta.value = mdRaw; ta.rows = 9; ta.spellcheck = false;
    var btn = document.createElement('button');
    btn.type = 'button'; btn.className = 'mermaid-rerender-btn'; btn.textContent = 'Refés el diagrama';
    btn.addEventListener('click', function () {
      var newMd = ta.value.trim(); if (!newMd) return;
      cont.dataset.md = newMd; cont.classList.remove('mermaid-active'); cont.innerHTML = '';
      renderMermaidBlock(cont, newMd, type);
    });
    d.appendChild(s); d.appendChild(ta); d.appendChild(btn);
    return d;
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // RENDER PRINCIPAL
  // ─────────────────────────────────────────────────────────────────────────────

  function renderMermaidBlock(cont, mdRaw, compType) {
    if (cont.querySelector('.diagram-wrapper')) return;
    if (cont.classList.contains('schema')) cont.classList.add('mermaid-active');

    var outer = document.createElement('div');
    outer.className = 'mermaid-wrapper diagram-wrapper';
    var inner = document.createElement('div');
    inner.className = 'diagram-inner';
    outer.appendChild(inner);
    cont.innerHTML = ''; cont.appendChild(outer);

    // Filtra capçaleres Markdown (## Mapa conceptual, etc.)
    var filteredMd = mdRaw.split('\n').filter(function (l) {
      return !l.match(/^##\s+/) && !l.match(/^```/) && !l.match(/^>/);
    }).join('\n').trim();

    var svgEl = null;
    try {
      if (compType === 'mapa_conceptual')                                       svgEl = buildConceptMap(filteredMd);
      else if (compType === 'mapa_mental' || compType === 'mapa_mental_fallback') svgEl = buildMindMap(filteredMd);
      else if (compType === 'esquema_visual')                                    svgEl = buildSchema(filteredMd);
    } catch (e) { console.warn('[ATNE diagram]', compType, e); }

    if (svgEl) {
      inner.appendChild(svgEl);
      addEditListeners(svgEl, filteredMd, cont, compType);
      outer.appendChild(buildZoom(svgEl));
    } else {
      inner.innerHTML = '<p style="color:#94a3b8;font-size:12px;padding:14px">No s\'ha pogut generar el diagrama.</p>';
    }
    outer.appendChild(buildEdit(filteredMd, cont, compType));
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // API PÚBLICA
  // ─────────────────────────────────────────────────────────────────────────────

  window.ATNE_MERMAID = {
    renderMermaidBlock:          renderMermaidBlock,
    renderAllMermaidComplements: function () {},
  };

})();
