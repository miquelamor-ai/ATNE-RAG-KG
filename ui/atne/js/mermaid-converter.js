/**
 * ATNE · diagram-renderer.js v6 — SVG pur, zero dependències externes
 *
 * mapa_conceptual → Novak: nodes+proposicions, layout top-down, gradient+ombra
 * mapa_mental     → Buzan: branques en cinta degradada (tapered ribbon), layout proporcional
 * esquema_visual  → Jerarquia LR, roundrects, codificació de profunditat
 */
(function () {
  'use strict';

  var NS = 'http://www.w3.org/2000/svg';

  // ─────────────────────────────────────────────────────────────────────────────
  // SVG UTILITIES
  // ─────────────────────────────────────────────────────────────────────────────

  function el(tag, attrs, children) {
    var e = document.createElementNS(NS, tag);
    if (attrs) Object.keys(attrs).forEach(function (k) { e.setAttribute(k, attrs[k]); });
    if (children) children.forEach(function (c) { if (c) e.appendChild(c); });
    return e;
  }

  function txt(s, attrs) {
    var t = el('text', attrs);
    t.textContent = s;
    return t;
  }

  // Amplada estimada del text sense canvas
  function tw(label, fs) { return label.length * (fs || 12) * 0.57; }

  // Divideix text en línies
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

  // Bloc de text SVG multi-línia centrat
  function mtext(lines, cx, cy, fs, attrs) {
    var g = el('g');
    var lh = (fs || 12) * 1.4, dy = -(lines.length - 1) * lh / 2;
    lines.forEach(function (l) {
      var t = txt(l, Object.assign({ x: cx, y: cy + dy, 'font-size': fs || 12,
        'text-anchor': 'middle', 'dominant-baseline': 'central' }, attrs || {}));
      g.appendChild(t);
      dy += lh;
    });
    return g;
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // PARSING COMÚ
  // ─────────────────────────────────────────────────────────────────────────────

  function indentLv(line) {
    var m = line.match(/^(\s*)/);
    return m ? Math.floor(m[1].replace(/\t/g, '  ').length / 2) : 0;
  }

  function rawLbl(line) { return line.replace(/^\s*-\s+/, '').replace(/\*\*/g, '').trim(); }
  function isBold(line) { return /^\s*-\s+\*\*.+\*\*$/.test(line); }

  function cleanMd(md) {
    return md.split('\n').filter(function (l) {
      var t = l.trim();
      return t && !t.startsWith('#') && !t.startsWith('```') && !t.startsWith('>');
    }).join('\n');
  }

  // Retorna arbre genèric { label, bold, children[] }
  function parseTree(md) {
    var lines = cleanMd(md).split('\n');
    if (!lines.length) return null;
    var lvs = lines.map(indentLv);
    var min = Math.min.apply(null, lvs);
    var root = null, stack = [];
    for (var i = 0; i < lines.length; i++) {
      var lv = lvs[i] - min, lbl = rawLbl(lines[i]);
      if (!lbl) continue;
      var node = { label: lbl, bold: isBold(lines[i]), children: [] };
      if (!root) { root = node; stack = [{ lv: 0, node: node }]; continue; }
      while (stack.length > 1 && stack[stack.length - 1].lv >= lv) stack.pop();
      stack[stack.length - 1].node.children.push(node);
      stack.push({ lv: lv, node: node });
    }
    return root;
  }

  // Aplana l'arbre del mapa conceptual: negretes → proposicions (etiquetes d'aresta)
  function treeToGraph(root) {
    var nodes = [], edges = [], cnt = 0;
    function visit(node, parentId, prop) {
      if (!node) return;
      if (node.bold) {
        node.children.forEach(function (c) { visit(c, parentId, node.label); });
      } else {
        var id = 'c' + cnt++;
        nodes.push({ id: id, label: node.label, root: parentId === null });
        if (parentId !== null) edges.push({ s: parentId, t: id, lbl: prop || '' });
        var curProp = '';
        node.children.forEach(function (c) {
          if (c.bold) { curProp = c.label; c.children.forEach(function (gc) { visit(gc, id, curProp); }); }
          else { visit(c, id, curProp); }
        });
      }
    }
    visit(root, null, '');
    return { nodes: nodes, edges: edges };
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // MAPA CONCEPTUAL — Novak, layout top-down
  // ─────────────────────────────────────────────────────────────────────────────

  var CM = { RX: 68, RY: 24, NW: 122, NH: 38, NR: 9, HG: 26, VG: 84, M: 36, PFS: 10 };

  function buildConceptMap(md) {
    var g = treeToGraph(parseTree(cleanMd(md)));
    if (!g.nodes.length) return null;

    var byId = {}, kids = {};
    g.nodes.forEach(function (n) { byId[n.id] = n; kids[n.id] = []; });
    g.edges.forEach(function (e) { if (kids[e.s]) kids[e.s].push(e.t); });

    // Amplada del subàrbre
    function sw(id) {
      var cs = kids[id] || [];
      if (!cs.length) return CM.NW + CM.HG;
      return Math.max(CM.NW + CM.HG, cs.reduce(function (s, k) { return s + sw(k); }, 0));
    }

    // Assigna posicions
    function place(id, sx, y) {
      var n = byId[id], s = sw(id);
      n.x = sx + s / 2; n.y = y;
      var cx = sx;
      (kids[id] || []).forEach(function (k) { var ks = sw(k); place(k, cx, y + CM.NH + CM.VG); cx += ks; });
    }
    place(g.nodes[0].id, 0, 0);

    // Bounding box
    var xs = g.nodes.map(function (n) { return n.x; });
    var ys = g.nodes.map(function (n) { return n.y; });
    var x0 = Math.min.apply(null, xs) - CM.RX - CM.M;
    var y0 = Math.min.apply(null, ys) - CM.RY - CM.M;
    var x1 = Math.max.apply(null, xs) + CM.RX + CM.M;
    var y1 = Math.max.apply(null, ys) + CM.NH + CM.M;

    var uid = 'cm' + (Math.random() * 1e9 | 0);
    var svg = el('svg', {
      viewBox: [x0, y0, x1 - x0, y1 - y0].join(' '), xmlns: NS,
      width: '100%', style: 'max-height:540px;display:block',
      'font-family': 'Georgia,"Times New Roman",serif',
    });

    // ── Defs: gradient, ombra, fletxa ────────────────────────────────────────
    var defs = el('defs');
    // Gradient radial per a l'arrel
    defs.appendChild(el('radialGradient', { id: uid + '-rg', cx: '38%', cy: '32%', r: '65%' }, [
      el('stop', { offset: '0%', 'stop-color': '#ddd6fe' }),
      el('stop', { offset: '100%', 'stop-color': '#7c3aed' }),
    ]));
    // Drop shadow
    defs.appendChild(el('filter', { id: uid + '-sh', x: '-25%', y: '-25%', width: '150%', height: '150%' }, [
      el('feDropShadow', { dx: 0, dy: 2, stdDeviation: 3, 'flood-opacity': 0.13 }),
    ]));
    // Gradient per als nodes concepte (profunditat → lleuger tint)
    defs.appendChild(el('linearGradient', { id: uid + '-ng', x1: 0, y1: 0, x2: 0, y2: 1 }, [
      el('stop', { offset: '0%', 'stop-color': '#ffffff' }),
      el('stop', { offset: '100%', 'stop-color': '#f1f5f9' }),
    ]));
    // Marcador de fletxa (purple discret)
    defs.appendChild(el('marker', {
      id: uid + '-arr', viewBox: '0 0 12 12', refX: 11, refY: 6,
      markerWidth: 6, markerHeight: 6, orient: 'auto',
    }, [el('path', { d: 'M0,2 L12,6 L0,10 L3,6 Z', fill: '#7c3aed', 'fill-opacity': 0.8 })]));
    svg.appendChild(defs);

    // ── Arestes ───────────────────────────────────────────────────────────────
    var gE = el('g');
    g.edges.forEach(function (e) {
      var sn = byId[e.s], tn = byId[e.t];
      if (!sn || !tn) return;
      var sx = sn.x, sy = sn.y + (sn.root ? CM.RY : CM.NH / 2);
      var tx = tn.x, ty = tn.y - CM.NH / 2;
      var my = (sy + ty) / 2;
      // Bezier suau vertical
      var d = 'M ' + sx + ' ' + sy + ' C ' + sx + ' ' + my + ' ' + tx + ' ' + my + ' ' + tx + ' ' + ty;
      gE.appendChild(el('path', {
        d: d, stroke: '#a78bfa', 'stroke-width': 1.5, fill: 'none',
        'stroke-opacity': 0.7, 'marker-end': 'url(#' + uid + '-arr)',
      }));
      // Etiqueta de la proposició al punt mig de la corba
      if (e.lbl) {
        var lx = (sx + tx) / 2, ly = (sy + ty) / 2 - 5;
        var lw = tw(e.lbl, CM.PFS) + 10;
        gE.appendChild(el('rect', { x: lx - lw / 2, y: ly - CM.PFS - 2, width: lw, height: CM.PFS + 6,
          fill: '#fff', rx: 3, 'fill-opacity': 0.9 }));
        gE.appendChild(txt(e.lbl, { x: lx, y: ly - 2, 'font-size': CM.PFS, 'font-style': 'italic',
          'text-anchor': 'middle', 'dominant-baseline': 'central', fill: '#5b21b6',
          'font-family': 'system-ui,sans-serif' }));
      }
    });
    svg.appendChild(gE);

    // ── Nodes ─────────────────────────────────────────────────────────────────
    var gN = el('g', { filter: 'url(#' + uid + '-sh)' });
    g.nodes.forEach(function (n) {
      var g2 = el('g');
      if (n.root) {
        g2.appendChild(el('ellipse', { cx: n.x, cy: n.y, rx: CM.RX, ry: CM.RY,
          fill: 'url(#' + uid + '-rg)', stroke: '#6d28d9', 'stroke-width': 2 }));
        var rl = wrap(n.label, CM.RX * 1.7, 13);
        g2.appendChild(mtext(rl, n.x, n.y, 13, { fill: '#fff', 'font-weight': 'bold' }));
      } else {
        var nw = Math.max(CM.NW, tw(n.label, 12) + 30);
        g2.appendChild(el('rect', { x: n.x - nw / 2, y: n.y - CM.NH / 2, width: nw, height: CM.NH,
          rx: CM.NR, fill: 'url(#' + uid + '-ng)', stroke: '#94a3b8', 'stroke-width': 1 }));
        var nl = wrap(n.label, nw - 22, 12);
        g2.appendChild(mtext(nl, n.x, n.y, 12, { fill: '#1e293b' }));
      }
      gN.appendChild(g2);
    });
    svg.appendChild(gN);
    return svg;
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // MAPA MENTAL — Buzan, layout lateral proporcional, branques en cinta degradada
  // ─────────────────────────────────────────────────────────────────────────────

  var MM = {
    RW: 128, RH: 42, RR: 12,        // root
    L1H: 32, LNH: 24,               // alçada nodes fills
    XS: 180,                         // pas horitzontal per nivell
    VG: 18,                          // espai vertical entre germans
    M: 44,                           // marge SVG
    W0: 9, W1: 4, W2: 2,            // amplada cinta (root/L1/L2+)
    PALETTE: [
      '#4f46e5','#0891b2','#059669','#d97706',
      '#7c3aed','#be185d','#0f766e','#b45309',
    ],
  };

  // Cinta degradada (tapered ribbon) entre dos punts
  function ribbon(sx, sy, tx, ty, w1, w2, color) {
    var cpx = (tx - sx) * 0.52;
    var cp1x = sx + cpx, cp2x = tx - cpx;
    // Corba superior (de source top a target top)
    // Corba inferior (de target bottom a source bottom)
    var d = [
      'M', sx, sy - w1 / 2,
      'C', cp1x, sy - w1 / 2, cp2x, ty - w2 / 2, tx, ty - w2 / 2,
      'L', tx, ty + w2 / 2,
      'C', cp2x, ty + w2 / 2, cp1x, sy + w1 / 2, sx, sy + w1 / 2,
      'Z',
    ].join(' ');
    return el('path', { d: d, fill: color });
  }

  function buildMindMap(md) {
    var tree = parseTree(cleanMd(md));
    if (!tree) return null;

    var palette = MM.PALETTE;

    // Alçada del subàrbre proporcional als fills (recursiu)
    function sh(node, depth) {
      var base = (depth <= 1 ? MM.L1H : MM.LNH) + MM.VG;
      if (!node.children || !node.children.length) return base;
      var tot = node.children.reduce(function (s, c) { return s + sh(c, depth + 1); }, 0);
      return Math.max(base, tot);
    }

    // Assigna posicions: root (0,0), branques als costats
    tree.x = 0; tree.y = 0; tree.depth = 0;
    var kids   = tree.children || [];
    var nRight = Math.ceil(kids.length / 2);

    function placeGroup(group, dir, depth) {
      if (!group.children || !group.children.length) return;
      var bx   = group.x + dir * MM.XS;
      var totH = group.children.reduce(function (s, c) { return s + sh(c, depth); }, 0) - MM.VG;
      var cy   = group.y - totH / 2;
      group.children.forEach(function (child) {
        var csh = sh(child, depth);
        child.x = bx; child.y = cy + csh / 2 - MM.VG / 2; child.depth = depth;
        placeGroup(child, dir, depth + 1);
        cy += csh;
      });
    }

    // Fals node grup per a cada costat
    placeGroup({ x: 0, y: 0, children: kids.slice(0, nRight) },  1, 1);
    placeGroup({ x: 0, y: 0, children: kids.slice(nRight) },    -1, 1);

    // Assigna colors i els propaga
    kids.forEach(function (k, i) { k.color = palette[i % palette.length]; });
    function propagate(n) { (n.children || []).forEach(function (c) { c.color = c.color || n.color; propagate(c); }); }
    kids.forEach(propagate);

    // Bounding box
    function allNodes(n) { return [n].concat((n.children || []).reduce(function (a, c) { return a.concat(allNodes(c)); }, [])); }
    var all = allNodes(tree);
    var xs  = all.map(function (n) { return n.x; });
    var ys  = all.map(function (n) { return n.y; });
    var maxTW = 160; // reserva text
    var x0 = Math.min.apply(null, xs) - maxTW / 2 - MM.M;
    var y0 = Math.min.apply(null, ys) - MM.L1H - MM.M;
    var x1 = Math.max.apply(null, xs) + maxTW / 2 + MM.M;
    var y1 = Math.max.apply(null, ys) + MM.L1H + MM.M;
    var vW = x1 - x0, vH = y1 - y0;

    var uid = 'mm' + (Math.random() * 1e9 | 0);
    var svg = el('svg', {
      viewBox: [x0, y0, vW, vH].join(' '), xmlns: NS,
      width: '100%', style: 'max-height:520px;display:block',
      'font-family': 'system-ui,-apple-system,sans-serif',
    });

    // Defs: gradient root, ombra
    var defs = el('defs');
    defs.appendChild(el('filter', { id: uid + '-sh', x: '-20%', y: '-20%', width: '140%', height: '140%' }, [
      el('feDropShadow', { dx: 0, dy: 3, stdDeviation: 4, 'flood-opacity': 0.18 }),
    ]));
    defs.appendChild(el('linearGradient', { id: uid + '-rg', x1: '0%', y1: '0%', x2: '0%', y2: '100%' }, [
      el('stop', { offset: '0%', 'stop-color': '#334155' }),
      el('stop', { offset: '100%', 'stop-color': '#0f172a' }),
    ]));
    svg.appendChild(defs);

    var gRibbons = el('g'); // Cintas sota els nodes
    var gNodes   = el('g');

    function draw(node) {
      // Dibuixa la cinta des del pare fins a aquest node
      if (node.depth > 0 && node.parent !== undefined) {
        // La cinta es dibuixa a drawChildren
      }

      // Dibuixa el node
      var g = el('g');
      if (node.depth === 0) {
        // Arrel: gradient fosc + ombra
        g.setAttribute('filter', 'url(#' + uid + '-sh)');
        g.appendChild(el('rect', { x: node.x - MM.RW / 2, y: node.y - MM.RH / 2,
          width: MM.RW, height: MM.RH, rx: MM.RR, fill: 'url(#' + uid + '-rg)' }));
        g.appendChild(txt(node.label, { x: node.x, y: node.y, 'font-size': 14, 'font-weight': '700',
          'text-anchor': 'middle', 'dominant-baseline': 'central', fill: '#fff',
          'letter-spacing': '0.3px' }));
      } else {
        var color = node.color || '#64748b';
        var fs    = node.depth === 1 ? 13 : 11;
        var nh    = node.depth === 1 ? MM.L1H : MM.LNH;
        var ntw   = Math.max(60, tw(node.label, fs)) + 18;
        if (node.depth === 1) {
          // L1: pill colorit
          g.appendChild(el('rect', { x: node.x - ntw / 2, y: node.y - nh / 2, width: ntw, height: nh,
            rx: nh / 2, fill: color + '18', stroke: color, 'stroke-width': 2 }));
          g.appendChild(txt(node.label, { x: node.x, y: node.y, 'font-size': fs, 'font-weight': '600',
            'text-anchor': 'middle', 'dominant-baseline': 'central', fill: color }));
        } else {
          // L2+: text pur amb línia colored sota
          var labelW = tw(node.label, fs) + 4;
          g.appendChild(el('line', { x1: node.x - labelW / 2, y1: node.y + nh / 2 - 2,
            x2: node.x + labelW / 2, y2: node.y + nh / 2 - 2,
            stroke: color, 'stroke-width': 1.5, 'stroke-opacity': 0.6 }));
          g.appendChild(txt(node.label, { x: node.x, y: node.y, 'font-size': fs,
            'text-anchor': 'middle', 'dominant-baseline': 'central', fill: '#334155' }));
        }
      }
      gNodes.appendChild(g);

      // Dibuixa cintas + nodes dels fills
      (node.children || []).forEach(function (child) {
        child.parent = node;
        var color   = child.color || '#94a3b8';
        var isRight = child.x > node.x;
        var dirX    = isRight ? 1 : -1;

        // Punt de connexió al pare
        var pw, ph;
        if (node.depth === 0) { pw = MM.RW; ph = MM.RH; }
        else { pw = Math.max(60, tw(node.label, node.depth === 1 ? 13 : 11)) + 18; ph = node.depth === 1 ? MM.L1H : MM.LNH; }

        var sx = node.x + dirX * pw / 2, sy = node.y;

        // Punt de connexió al fill
        var cw = Math.max(60, tw(child.label, child.depth === 1 ? 13 : 11)) + 18;
        var tx = child.x - dirX * cw / 2, ty = child.y;

        // Amplada de cinta
        var w1 = node.depth === 0 ? MM.W0 : child.depth === 1 ? MM.W1 : MM.W2;
        var w2 = child.depth === 1 ? MM.W1 : MM.W2;

        gRibbons.appendChild(ribbon(sx, sy, tx, ty, w1, w2, color));
        draw(child);
      });
    }

    draw(tree);
    svg.appendChild(gRibbons);
    svg.appendChild(gNodes);
    return svg;
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // ESQUEMA VISUAL — jerarquia LR, codificació de profunditat
  // ─────────────────────────────────────────────────────────────────────────────

  var SC = { RW: 130, RH: 38, NW: 110, NH: 32, NR: 8, HG: 56, VG: 14, M: 22 };

  // Colors per profunditat: root=purple, depth1=slate, depth2+=zinc
  var SC_FILLS   = ['#ede9fe', '#f1f5f9', '#f9fafb'];
  var SC_STROKES = ['#6d28d9', '#64748b', '#9ca3af'];
  var SC_TEXTS   = ['#3b0764', '#1e293b', '#374151'];

  function buildSchema(md) {
    var tree = parseTree(cleanMd(md));
    if (!tree) return null;

    function shH(node) {
      if (!node.children || !node.children.length) return SC.NH + SC.VG;
      return node.children.reduce(function (s, c) { return s + shH(c); }, 0);
    }

    function place(node, x, sy, depth) {
      var h = shH(node);
      node.x = x; node.y = sy + h / 2 - SC.VG / 2; node.depth = depth;
      var cy = sy, nw = depth === 0 ? SC.RW : SC.NW, nh = depth === 0 ? SC.RH : SC.NH;
      (node.children || []).forEach(function (c) {
        var ch = shH(c); place(c, x + nw + SC.HG, cy, depth + 1); cy += ch;
      });
    }
    place(tree, 0, 0, 0);

    function allNodes(n) { return [n].concat((n.children || []).reduce(function (a, c) { return a.concat(allNodes(c)); }, [])); }
    var all = allNodes(tree);
    var ys  = all.map(function (n) { return n.y; });
    var x0  = -SC.M, y0 = Math.min.apply(null, ys) - SC.RH - SC.M;
    var x1  = Math.max.apply(null, all.map(function (n) { return n.x + SC.RW; })) + SC.M;
    var y1  = Math.max.apply(null, ys) + SC.RH + SC.M;

    var uid = 'sc' + (Math.random() * 1e9 | 0);
    var svg = el('svg', { viewBox: [x0, y0, x1 - x0, y1 - y0].join(' '), xmlns: NS,
      width: '100%', style: 'max-height:480px;display:block',
      'font-family': 'system-ui,sans-serif' });

    var defs = el('defs');
    defs.appendChild(el('filter', { id: uid + '-sh', x: '-20%', y: '-20%', width: '140%', height: '140%' }, [
      el('feDropShadow', { dx: 0, dy: 1, stdDeviation: 2, 'flood-opacity': 0.1 }),
    ]));
    defs.appendChild(el('marker', { id: uid + '-a', viewBox: '0 0 10 10', refX: 9, refY: 5,
      markerWidth: 5, markerHeight: 5, orient: 'auto' },
      [el('path', { d: 'M0,2 L10,5 L0,8 L2.5,5 Z', fill: '#94a3b8' })]));
    svg.appendChild(defs);

    var gL = el('g'), gN = el('g', { filter: 'url(#' + uid + '-sh)' });

    all.forEach(function (n) {
      var d  = Math.min(n.depth, SC_FILLS.length - 1);
      var nw = n.depth === 0 ? SC.RW : SC.NW, nh = n.depth === 0 ? SC.RH : SC.NH;
      // Arestes als fills
      (n.children || []).forEach(function (c) {
        var cnw = c.depth === 0 ? SC.RW : SC.NW;
        var sx = n.x + nw, sy = n.y, tx = c.x, ty = c.y;
        var mx = (sx + tx) / 2;
        gL.appendChild(el('path', { d: 'M ' + sx + ' ' + sy + ' C ' + mx + ' ' + sy + ' ' + mx + ' ' + ty + ' ' + tx + ' ' + ty,
          stroke: '#cbd5e1', 'stroke-width': 1.5, fill: 'none', 'marker-end': 'url(#' + uid + '-a)' }));
      });
      // Node
      gN.appendChild(el('rect', { x: n.x, y: n.y - nh / 2, width: nw, height: nh, rx: SC.NR,
        fill: SC_FILLS[d], stroke: SC_STROKES[d], 'stroke-width': n.depth === 0 ? 2 : 1 }));
      var ls = wrap(n.label, nw - 16, 12);
      gN.appendChild(mtext(ls, n.x + nw / 2, n.y, 12, { fill: SC_TEXTS[d], 'font-weight': n.depth === 0 ? '700' : '400' }));
    });

    svg.appendChild(gL);
    svg.appendChild(gN);
    return svg;
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // CONTROLS UI
  // ─────────────────────────────────────────────────────────────────────────────

  function buildZoom(svgEl) {
    var row = document.createElement('div');
    row.className = 'mermaid-zoom-row';
    row.innerHTML = '<label class="mermaid-zoom-label">Mida <input type="range" ' +
      'class="mermaid-zoom-slider" min="30" max="180" value="100">' +
      '<span class="mermaid-zoom-pct">100%</span></label>';
    var sl = row.querySelector('.mermaid-zoom-slider');
    var sp = row.querySelector('.mermaid-zoom-pct');
    sl.addEventListener('input', function () {
      var pct = +sl.value, scale = pct / 100;
      sp.textContent = pct + '%';
      svgEl.style.transform = 'scale(' + scale + ')';
      svgEl.style.transformOrigin = 'top left';
    });
    return row;
  }

  function buildEdit(mdRaw, cont, type) {
    var d = document.createElement('details');
    d.className = 'mermaid-edit-details';
    var s = document.createElement('summary');
    s.className = 'mermaid-edit-toggle';
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

    var svgEl = null;
    try {
      var md = mdRaw.split('\n').filter(function (l) {
        return !l.match(/^##\s+/) && !l.match(/^```/) && !l.match(/^>/);
      }).join('\n').trim();

      if (compType === 'mapa_conceptual')                          svgEl = buildConceptMap(md);
      else if (compType === 'mapa_mental' || compType === 'mapa_mental_fallback') svgEl = buildMindMap(md);
      else if (compType === 'esquema_visual')                      svgEl = buildSchema(md);
    } catch (e) { console.warn('[ATNE diagram]', compType, e); }

    if (svgEl) {
      inner.appendChild(svgEl);
      outer.appendChild(buildZoom(svgEl));
    } else {
      inner.innerHTML = '<p style="color:#94a3b8;font-size:12px;padding:14px">No s\'ha pogut generar el diagrama. Edita el font per corregir-ho.</p>';
    }
    outer.appendChild(buildEdit(mdRaw, cont, compType));
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // API PÚBLICA (compatible amb pas3.html)
  // ─────────────────────────────────────────────────────────────────────────────

  window.ATNE_MERMAID = {
    renderMermaidBlock:          renderMermaidBlock,
    renderAllMermaidComplements: function () {},
  };

})();
