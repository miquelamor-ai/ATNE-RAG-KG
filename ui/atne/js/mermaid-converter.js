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

  function tw(label, fs) { return label.length * (fs || 12) * 0.62; }

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

  // treeToGraph — nodes bold (no arrel) = nodes proposició VISIBLES (oval italic)
  // UNA proposició per branca, fills concepte penjen d'ella
  function treeToGraph(root) {
    var nodes = [], edges = [], cnt = 0;
    function visit(node, parentId) {
      var isRoot = parentId === null;
      var id = 'c' + cnt++;
      var type = isRoot ? 'root' : (node.bold ? 'prop' : 'concept');
      nodes.push({ id: id, label: node.label, type: type, lineIdx: node.lineIdx });
      if (!isRoot) edges.push({ s: parentId, t: id });
      node.children.forEach(function (c) { visit(c, id); });
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
    RW: 148, RH: 40, RR: 10,   // root
    NW: 120, NH: 36, NR: 8,    // concepte
    PH: 22,                     // proposició (alçada base)
    HG: 44,                     // gap horitzontal → colW = 164
    VG1: 44, VG2: 28, LG: 20,   // LG = gap vertical entre germans (10→20: més aire, feedback 13/06)
    M: 32, PFS: 11,
  };

  function buildConceptMap(md) {
    // Enllaços creuats (graf Novak): separem el bloc del final; l'arbre es
    // parseja net i les arestes transversals es dibuixen a sobre.
    var _cx = (window.ATNE_EDIT_CORE && window.ATNE_EDIT_CORE.splitCross)
      ? window.ATNE_EDIT_CORE.splitCross(md) : { tree: md, cross: [] };
    var g = treeToGraph(parseTree(_cx.tree));
    if (!g.nodes.length) return null;
    var crossLinks = _cx.cross || [];

    var byId = {}, childMap = {};
    g.nodes.forEach(function (n) {
      byId[n.id] = n; childMap[n.id] = [];
      if (n.type === 'prop') {
        var pls = wrap(n.label, CM.NW - 20, CM.PFS);
        n.pLines = pls; n.ph = Math.max(CM.PH, pls.length * 14 + 8);
      } else {
        n.lines = wrap(n.label, CM.NW - 18, 12);
        n.nh    = Math.max(CM.NH, n.lines.length * 16 + 10);
      }
    });
    g.edges.forEach(function (e) { if (childMap[e.s]) childMap[e.s].push(e.t); });

    var rootId = g.nodes[0].id;
    var l1Ids  = childMap[rootId] || [];
    var colW   = CM.NW + CM.HG;  // 164

    // Layout RECURSIU amb FORK HORITZONTAL (fix prototip 2026-06-12):
    // suporta profunditat arbitrària (v0.3) i amplada arbitrària (v0.5).
    // Regles de col·locació (preserven l'estètica original):
    //  - prop -> conceptes: PILA VERTICAL (com sempre)
    //  - concepte/arrel -> 1 fill: cadena vertical
    //  - concepte/arrel -> 2+ fills: FORK HORITZONTAL, proposicions germanes
    //    EN PARAL·LEL amb el pare centrat a sobre (mapa Novak de debò)
    function nodeH(nid) { var n = byId[nid]; return n.type === 'prop' ? n.ph : n.nh; }
    function subW(nid) {
      var n = byId[nid], kids = childMap[nid] || [];
      if (!kids.length) return CM.NW;
      var ws = kids.map(subW);
      if (n.type !== 'prop' && kids.length >= 2) {
        return ws.reduce(function (a, b) { return a + b; }, 0) + CM.HG * (kids.length - 1);
      }
      return Math.max(CM.NW, Math.max.apply(null, ws));
    }
    function subH(nid) {
      var n = byId[nid], h = nodeH(nid), kids = childMap[nid] || [];
      if (!kids.length) return h;
      if (n.type !== 'prop' && kids.length >= 2) {
        return h + CM.VG2 + Math.max.apply(null, kids.map(subH));
      }
      var kH = kids.reduce(function (s, sid) { return s + CM.LG + subH(sid); }, -CM.LG);
      return h + CM.VG2 + kH;
    }
    function colH(nid) { return subH(nid); }
    function placeColumn(nid, cx, topY) {
      var n = byId[nid], h = nodeH(nid), kids = childMap[nid] || [];
      n.x = cx; n.y = topY + h / 2;
      if (!kids.length) return;
      if (n.type !== 'prop' && kids.length >= 2) {
        var x = cx - subW(nid) / 2;
        kids.forEach(function (sid) {
          var w = subW(sid);
          placeColumn(sid, x + w / 2, topY + h + CM.VG2);
          x += w + CM.HG;
        });
      } else {
        var cy = topY + h + CM.VG2;
        kids.forEach(function (sid) { placeColumn(sid, cx, cy); cy += subH(sid) + CM.LG; });
      }
    }

    var startY = CM.RH / 2 + CM.VG1;
    // Amplada variable per columna (HG/2 de marge a cada banda): amb mapes
    // sense forks, els centres queden EXACTAMENT on eren (82, 246, ...).
    var offX = 0;
    l1Ids.forEach(function (nid) {
      var w = subW(nid);
      placeColumn(nid, offX + CM.HG / 2 + w / 2, startY);
      offX += CM.HG + w;
    });
    byId[rootId].y = 0;
    if (l1Ids.length) {
      var xs1 = l1Ids.map(function (id) { return byId[id].x; });
      byId[rootId].x = (Math.min.apply(null, xs1) + Math.max.apply(null, xs1)) / 2;
    } else { byId[rootId].x = colW / 2; }

    var all = g.nodes;
    var xs  = all.map(function (n) { return n.x || 0; });
    var ys  = all.map(function (n) { return n.y || 0; });
    var allH = all.map(function (n) { return n.nh || n.ph || CM.NH; });
    var x0  = Math.min.apply(null, xs) - CM.NW / 2 - CM.M;
    var y0  = Math.min.apply(null, ys) - CM.RH / 2 - CM.M;
    var x1  = Math.max.apply(null, xs) + CM.NW / 2 + CM.M;
    var y1  = Math.max.apply(null, ys) + Math.max.apply(null, allH) / 2 + CM.M;
    var y1b = y1;
    // ── Enrutament dels enllaços creuats (graf Novak) — BUS ORTOGONAL ──
    // La corba surt pel COSTAT del node cap al passadís entre columnes (sempre
    // buit), baixa fins a un BUS horitzontal per sota dels nodes que el tram
    // sobrevola, i puja cap al destí. Així la línia NO travessa MAI cap caixa de
    // concepte, ni en files iguals ni diferents (fix feedback 14/06). El router
    // és compartit pel pre-pass (viewBox) i el draw-pass perquè siguin coherents.
    function crossHalfW(n) { return n.type === 'prop' ? 34 : CM.NW / 2; }
    function crossHalfH(n) { return (n.type === 'prop' ? n.ph : n.nh) / 2; }
    // Mitja amplada d'empremta d'un node (per a la cerca de bandes netes).
    function crossFW(n) { return n.type === 'root' ? CM.RW / 2 : (n.type === 'prop' ? (n.label.length * CM.PFS * 0.6 + 10) / 2 : CM.NW / 2); }
    var mapTop = Infinity, mapBot = -Infinity;
    g.nodes.forEach(function (m) {
      if (m.x === undefined) return;
      mapTop = Math.min(mapTop, m.y - crossHalfH(m));
      mapBot = Math.max(mapBot, m.y + crossHalfH(m));
    });
    if (mapBot === -Infinity) { mapBot = 0; mapTop = 0; }
    function crossRoute(sn, tn, lane, labelW) {
      // Enrutament dels enllaços creuats. PRIORITAT (decisió Miquel 15/06): una corba
      // DIRECTA entre els dos conceptes (estil CmapTools) — curta i sense detour —
      // sempre que NO trepitgi cap altre node. Si la directa xocaria (conceptes amb
      // nodes pel mig), es cau al BUS NET MÉS PROPER (passadís lateral + banda lliure),
      // que garanteix que la línia no travessa cap caixa. Corbes suaus.
      var sxC = sn.x, syC = sn.y, txC = tn.x, tyC = tn.y;
      var dirS = (txC >= sxC) ? 1 : -1, dirT = (sxC > txC) ? 1 : -1;
      var gutS = sxC + dirS * (crossHalfW(sn) + CM.HG / 2);
      var gutT = txC + dirT * (crossHalfW(tn) + CM.HG / 2);
      var edgeSx = sxC + dirS * crossHalfW(sn), edgeTx = txC + dirT * crossHalfW(tn);
      var gutMid = (gutS + gutT) / 2;
      var halfStrip = Math.max(Math.abs(gutT - gutS) / 2, (labelW || 0) / 2) + 6;
      // Mostreja una cadena de cúbics (P = [[x,y]...] de 4/7/... punts) i comprova que
      // cap punt cau dins d'un node. Exclou origen i destí (la corba hi toca pels extrems).
      function clearChain(P) {
        function cub(a, b, c, e, t) { var u = 1 - t; return [u*u*u*a[0] + 3*u*u*t*b[0] + 3*u*t*t*c[0] + t*t*t*e[0], u*u*u*a[1] + 3*u*u*t*b[1] + 3*u*t*t*c[1] + t*t*t*e[1]]; }
        var segs = (P.length - 1) / 3;
        for (var seg = 0; seg < segs; seg++) {
          var a = P[seg*3], b = P[seg*3+1], c = P[seg*3+2], e = P[seg*3+3];
          for (var t = 0; t <= 1.0001; t += 0.04) {
            var pt = cub(a, b, c, e, t);
            for (var i = 0; i < g.nodes.length; i++) {
              var m = g.nodes[i]; if (m.x === undefined || m === sn || m === tn) continue;
              var fw = crossFW(m), fh = crossHalfH(m);
              if (pt[0] > m.x - fw - 2 && pt[0] < m.x + fw + 2 && pt[1] > m.y - fh - 2 && pt[1] < m.y + fh + 2) return false;
            }
          }
        }
        return true;
      }
      // ── 1) CORBA DIRECTA entre origen i destí (sense detour a cap bus) ──
      var ddx = edgeTx - edgeSx, cp1x = edgeSx + ddx * 0.5, cp2x = edgeTx - ddx * 0.5;
      var directOk = clearChain([[edgeSx, syC], [cp1x, syC], [cp2x, tyC], [edgeTx, tyC]]);
      if (directOk && Math.abs(syC - tyC) < 24) {
        // 1a) MATEIX NIVELL (branques del costat): arc CÒNCAU cap a una banda lliure,
        //     amb la proposició a l'ÀPEX (sobre la línia, SENSE cap línia secundària).
        var y0 = (syC + tyC) / 2, midX = (edgeSx + edgeTx) / 2;
        var ax1 = edgeSx + ddx * 0.25, ax2 = edgeTx - ddx * 0.25, lw = Math.max(labelW || 0, 22), BOW = 32;
        var arc = function (dir) {
          var apexY = y0 + dir * BOW, h = dir * BOW * 1.34;
          if (!clearChain([[edgeSx, syC], [ax1, y0 + h], [ax2, y0 + h], [edgeTx, tyC]])) return null;
          for (var i = 0; i < g.nodes.length; i++) {   // l'àpex (etiqueta) lliure de nodes
            var m = g.nodes[i]; if (m.x === undefined) continue;
            if (Math.abs(midX - m.x) < crossFW(m) + lw / 2 && Math.abs(apexY - m.y) < crossHalfH(m) + 11) return null;
          }
          return { d: 'M ' + edgeSx + ' ' + syC + ' C ' + ax1 + ' ' + (y0 + h) + ' ' + ax2 + ' ' + (y0 + h) + ' ' + edgeTx + ' ' + tyC, apexY: apexY };
        };
        var a = arc(-1) || arc(1);   // prova amunt; si no, avall
        if (a) return { d: a.d, lx: midX, ly: a.apexY,
                        minX: Math.min(edgeSx, edgeTx), maxX: Math.max(edgeSx, edgeTx),
                        minY: Math.min(syC, tyC, a.apexY), maxY: Math.max(syC, tyC, a.apexY) };
      }
      // NIVELLS DIFERENTS (diagonal) o sense lloc per a l'arc → BUS net més proper (avall).
      // ── 2) FALLBACK: BUS NET MÉS PROPER (passadís lateral + banda horitzontal lliure) ──
      // Una banda a alçada y és lliure si cap node intercepta l'strip [gutMid±halfStrip].
      function clearBand(y) {
        var lo = gutMid - halfStrip, hi = gutMid + halfStrip;
        for (var i = 0; i < g.nodes.length; i++) {
          var m = g.nodes[i]; if (m.x === undefined) continue;
          var fw = crossFW(m);
          if (hi < m.x - fw || lo > m.x + fw) continue;
          if (y > m.y - crossHalfH(m) - 11 && y < m.y + crossHalfH(m) + 11) return false;
        }
        return true;
      }
      function pathFor(by) {
        return 'M ' + edgeSx + ' ' + syC +
               ' C ' + gutS + ' ' + syC + ' ' + gutS + ' ' + by + ' ' + gutMid + ' ' + by +
               ' C ' + gutT + ' ' + by + ' ' + gutT + ' ' + tyC + ' ' + edgeTx + ' ' + tyC;
      }
      function busClear(by) { return clearChain([[edgeSx, syC], [gutS, syC], [gutS, by], [gutMid, by], [gutT, by], [gutT, tyC], [edgeTx, tyC]]); }
      var base = (syC + tyC) / 2;
      // Fallback exterior (costat més proper) si no es troba cap banda interior neta.
      var busY = (base <= (mapTop + mapBot) / 2) ? (mapTop - 22 - lane * 22) : (mapBot + 22 + lane * 22);
      // BUS NET MÉS PROPER, SENSE biaix avall: a cada distància provem amunt I avall i,
      // si totes dues són netes, triem la de MENYS recorregut vertical (detour mínim).
      for (var off = 0; off <= 900; off += 7) {
        var dOk = clearBand(base + off) && busClear(base + off);
        var uOk = off > 0 && clearBand(base - off) && busClear(base - off);
        if (dOk || uOk) {
          if (dOk && uOk) {
            var costD = Math.abs(base + off - syC) + Math.abs(base + off - tyC);
            var costU = Math.abs(base - off - syC) + Math.abs(base - off - tyC);
            busY = (costU < costD) ? (base - off) : (base + off);
          } else { busY = dOk ? (base + off) : (base - off); }
          break;
        }
      }
      // Etiqueta ancorada AL BUS, prop del concepte d'ORIGEN (no al mig del tram).
      var lblx = gutS + (gutT - gutS) * 0.32;
      var d = pathFor(busY);
      return { d: d, lx: lblx, ly: busY,
               minX: Math.min(edgeSx, gutS, gutT, edgeTx), maxX: Math.max(edgeSx, gutS, gutT, edgeTx),
               minY: Math.min(syC, tyC, busY), maxY: Math.max(syC, tyC, busY) };
    }
    // crossRender: calculat UN COP aquí (corba + col·locació d'etiqueta) i reusat
    // al draw-pass, perquè el viewBox pugui encabir la posició FINAL de l'etiqueta.
    var crossRender = [];
    if (crossLinks.length) {
      var byLx = {};
      g.nodes.forEach(function (n) { if (byLx[n.label] === undefined) byLx[n.label] = n; });
      // Empremtes dels nodes = obstacles per a la col·locació d'etiquetes.
      var footprint = function (n) {
        if (n.type === 'root') return { x: n.x - CM.RW / 2, y: n.y - CM.RH / 2, w: CM.RW, h: CM.RH };
        if (n.type === 'prop') { var pw = n.label.length * CM.PFS * 0.6 + 10; return { x: n.x - pw / 2, y: n.y - n.ph / 2, w: pw, h: n.ph }; }
        return { x: n.x - CM.NW / 2, y: n.y - n.nh / 2, w: CM.NW, h: n.nh };
      };
      var ov = function (a, b) { return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y; };
      var obstacles = g.nodes.filter(function (n) { return n.x !== undefined; }).map(footprint);
      // Cerca voraç: provem el punt mig i, si xoca, ens allunyem en cercles fins
      // trobar un buit (ni sobre un concepte ni sobre una altra etiqueta ja posada).
      var STEPS = [0, 16, 26, 36, 48, 62, 78, 96, 116, 138];
      var DIRS = [[0, 1], [0, -1], [1, 0.5], [-1, 0.5], [1, -0.5], [-1, -0.5], [0.6, 1], [-0.6, 1]];
      crossLinks.forEach(function (cl, ci) {
        var sn = byLx[cl.from], tn = byLx[cl.to];
        if (!sn || !tn || sn.x === undefined || tn.x === undefined) return;
        var r = crossRoute(sn, tn, ci, cl.link ? cl.link.length * 6.2 + 12 : 0);
        x0 = Math.min(x0, r.minX - CM.M); x1 = Math.max(x1, r.maxX + CM.M);
        y0 = Math.min(y0, r.minY - 10); y1b = Math.max(y1b, r.maxY + 10);
        var lbl = null;
        if (cl.link) {
          var w = cl.link.length * 6.2 + 12, h = 18, bx = r.lx, by = r.ly, placed = false;
          for (var si = 0; si < STEPS.length && !placed; si++) {
            var cands = si === 0 ? [[0, 0]] : DIRS;
            for (var di = 0; di < cands.length; di++) {
              var cxC = r.lx + cands[di][0] * STEPS[si], cyC = r.ly + cands[di][1] * STEPS[si];
              var box = { x: cxC - w / 2, y: cyC - h / 2, w: w, h: h };
              var clash = false;
              for (var oi = 0; oi < obstacles.length; oi++) { if (ov(box, obstacles[oi])) { clash = true; break; } }
              if (!clash) { bx = cxC; by = cyC; placed = true; break; }
            }
          }
          obstacles.push({ x: bx - w / 2, y: by - h / 2, w: w, h: h });
          x0 = Math.min(x0, bx - w / 2 - 4); x1 = Math.max(x1, bx + w / 2 + 4);
          y0 = Math.min(y0, by - h / 2 - 4); y1b = Math.max(y1b, by + h / 2 + 4);
          lbl = { x: bx, y: by, w: w, mx: r.lx, my: r.ly };
        }
        crossRender.push({ d: r.d, ci: ci, link: cl.link, label: lbl });
      });
    }

    y1 = Math.max(y1, y1b);
    var uid = 'cm' + (Math.random() * 1e9 | 0);
    var svg = el('svg', { viewBox: [x0, y0, x1 - x0, y1 - y0].join(' '), xmlns: NS,
      'font-family': pageFont() });

    var defs = el('defs');
    defs.appendChild(el('filter', { id: uid + '-sh', x: '-20%', y: '-20%', width: '140%', height: '140%' }, [
      el('feDropShadow', { dx: 0, dy: 1, stdDeviation: 2.5, 'flood-opacity': 0.11 })]));
    defs.appendChild(el('marker', { id: uid + '-arr', viewBox: '0 0 8 8', refX: 7, refY: 4,
      markerWidth: 8, markerHeight: 8, orient: 'auto' },
      [el('path', { d: 'M0,1 L7,4 L0,7 L2,4 Z', fill: '#6366f1' })]));
    svg.appendChild(defs);

    // Mapa de pares (per al routing d'arestes amb bypass)
    var parentOf = {};
    g.edges.forEach(function (e) { parentOf[e.t] = e.s; });

    var gE = el('g');
    g.edges.forEach(function (e) {
      var sn = byId[e.s], tn = byId[e.t]; if (!sn || !tn) return;
      var sy2 = sn.type === 'root' ? sn.y + CM.RH / 2 :
                sn.type === 'prop' ? sn.y + sn.ph / 2 : sn.y + sn.nh / 2;
      var ty2 = tn.type === 'prop' ? tn.y - tn.ph / 2 - 3 : tn.y - tn.nh / 2 - 3;
      var sx2 = sn.x, tx2 = tn.x, d;
      if (Math.abs(sx2 - tx2) < 3) {
        // Routing amb bypass (fix 2026-06-12): si entre origen i destí (mateixa
        // columna) hi ha algun node que NO és germà del destí, una línia recta
        // travessaria un subarbre aliè i llegiria com una cadena FALSA
        // (p.ex. concepte -> 2a proposició saltant el subarbre de la 1a).
        // Les pluges normals (prop -> conceptes apilats, tots germans) queden
        // rectes com sempre: geometria intacta per als mapes existents.
        var needsBypass = g.nodes.some(function (m) {
          if (m.id === e.s || m.id === e.t || m.x === undefined) return false;
          if (Math.abs(m.x - sx2) >= 3) return false;
          var top = m.y - (m.nh || m.ph || 0) / 2, bot = m.y + (m.nh || m.ph || 0) / 2;
          if (bot <= sy2 || top >= ty2) return false;       // fora del tram
          return parentOf[m.id] !== parentOf[e.t];          // no és germà del destí
        });
        if (needsBypass) {
          var off = sx2 + CM.NW / 2 + 20;
          var k = (ty2 - sy2);
          d = 'M ' + sx2 + ' ' + sy2 +
              ' C ' + off + ' ' + (sy2 + k * 0.22) + ' ' + off + ' ' + (sy2 + k * 0.78) +
              ' ' + tx2 + ' ' + ty2;
        } else {
          d = 'M ' + sx2 + ' ' + sy2 + ' L ' + tx2 + ' ' + ty2;
        }
      } else {
        var cp = sy2 + (ty2 - sy2) * 0.6;
        d = 'M ' + sx2 + ' ' + sy2 + ' C ' + sx2 + ' ' + cp + ' ' + tx2 + ' ' + cp + ' ' + tx2 + ' ' + ty2;
      }
      gE.appendChild(el('path', { d: d, stroke: '#a5b4fc', 'stroke-width': 1.5,
        fill: 'none', 'marker-end': 'url(#' + uid + '-arr)' }));
    });
    svg.appendChild(gE);

    // ── Enllaços creuats: es CALCULEN aquí però es dibuixen DESPRÉS dels nodes
    //    (fix v0.8: abans es pintaven sota gN i els rectangles dels conceptes
    //    + ombres tapaven la corba i, sobretot, l'etiqueta de la relació). ──
    var gX = null;
    if (crossRender.length) {
      // Paleta d'estils per als enllaços creuats: cada enllaç (per índex it.ci) en
      // rep un de propi, perquè quan n'hi ha més d'un es distingeixin (i cada nou que
      // l'usuari crea es diferenciï dels anteriors). Doble codi DUA: color + tipus de
      // discontinuïtat alhora (qui no distingeix colors ho capta pel traç, i a l'inrevés).
      // L'etiqueta hereta el color del seu enllaç per poder aparellar-los.
      // Índex 0 = l'estil històric (taronja · "4 3"), per no trencar res que ja anava bé.
      // NB: s'eviten blau/lila/indigo a propòsit — són els colors per defecte dels
      // conceptes i de les connexions d'arbre, i un creuat blavós es confondria amb
      // un enllaç jeràrquic. Doble codi DUA: color + tipus de discontinuïtat.
      var CROSS_STYLES = [
        { line: '#fb923c', arrow: '#ea580c', dash: '4 3',     bg: '#fff7ed', txt: '#c2410c' }, // taronja · guions
        { line: '#10b981', arrow: '#059669', dash: '1 5',     bg: '#ecfdf5', txt: '#047857' }, // verd · punts
        { line: '#ec4899', arrow: '#be185d', dash: '10 5',    bg: '#fdf2f8', txt: '#be185d' }, // rosa · guions llargs
        { line: '#f87171', arrow: '#dc2626', dash: '7 3 2 3', bg: '#fef2f2', txt: '#b91c1c' }, // vermell · guió-punt
        { line: '#eab308', arrow: '#a16207', dash: '2 3',     bg: '#fefce8', txt: '#854d0e' }, // ambre · punts fins
      ];
      // Un marker de fletxa per estil (amb el seu color).
      CROSS_STYLES.forEach(function (st, k) {
        defs.appendChild(el('marker', { id: uid + '-xarr' + k, viewBox: '0 0 8 8', refX: 7, refY: 4,
          markerWidth: 8, markerHeight: 8, orient: 'auto' },
          [el('path', { d: 'M0,1 L7,4 L0,7 L2,4 Z', fill: st.arrow })]));
      });
      gX = el('g');
      crossRender.forEach(function (it) {
        var st = CROSS_STYLES[it.ci % CROSS_STYLES.length];
        // Traç fi i discret (decisió Miquel 14/06): l'enllaç creuat és una anotació
        // secundària, no ha de dominar el mapa.
        gX.appendChild(el('path', { d: it.d, stroke: st.line, 'stroke-width': 1.2,
          'stroke-dasharray': st.dash, fill: 'none', 'marker-end': 'url(#' + uid + '-xarr' + (it.ci % CROSS_STYLES.length) + ')' }));
        if (it.label) {
          var L = it.label, w = L.w;
          // Grup clicable: data-cross-idx identifica l'enllaç per a editar/eliminar
          var lg = el('g', { 'data-cross-idx': it.ci, style: 'cursor:pointer' });
          var tt = document.createElementNS(NS, 'title');
          tt.textContent = 'Clica per editar o eliminar la connexió';
          lg.appendChild(tt);
          // Si l'etiqueta s'ha desplaçat al buit més proper, una línia fina la lliga
          // amb el seu enllaç (estratègia de col·locació intel·ligent, decisió 14/06).
          if (Math.abs(L.x - L.mx) > 2 || Math.abs(L.y - L.my) > 2) {
            lg.appendChild(el('line', { x1: L.mx, y1: L.my, x2: L.x, y2: L.y,
              stroke: st.line, 'stroke-width': 1, 'stroke-dasharray': '2 2' }));
          }
          lg.appendChild(el('rect', { x: L.x - w / 2, y: L.y - 9, width: w, height: 18, rx: 5,
            fill: st.bg, stroke: st.line, 'stroke-width': 1 }));
          lg.appendChild(txt(it.link, { x: L.x, y: L.y + 4, 'text-anchor': 'middle',
            'font-size': 10.5, 'font-style': 'italic', fill: st.txt, 'font-weight': '600' }));
          gX.appendChild(lg);
        }
      });
    }

    var gN = el('g');
    g.nodes.forEach(function (n) {
      if (n.x === undefined) return;
      var grp = nodeGroup(n);
      var ttl = document.createElementNS(NS, 'title');
      ttl.textContent = 'Clic per editar'; grp.appendChild(ttl);

      if (n.type === 'root') {
        grp.setAttribute('filter', 'url(#' + uid + '-sh)');
        grp.appendChild(el('rect', { x: n.x - CM.RW / 2, y: n.y - CM.RH / 2,
          width: CM.RW, height: CM.RH, rx: CM.RR, fill: '#312e81', stroke: '#6366f1', 'stroke-width': 1.5 }));
        grp.appendChild(mtext(wrap(n.label, CM.RW - 24, 13), n.x, n.y, 13,
          { fill: '#fff', 'font-weight': '700' }));

      } else if (n.type === 'prop') {
        // Text italic sobre la línia, sense oval ni quadre.
        // Halo blanc (stroke blanc primer, fill blau sobre) emmascara la línia.
        grp.appendChild(mtext(n.pLines, n.x, n.y, CM.PFS,
          { 'font-style': 'italic', fill: '#4338ca',
            stroke: '#ffffff', 'stroke-width': '5',
            'stroke-linejoin': 'round', 'paint-order': 'stroke' }));

      } else {
        // Concepte
        grp.setAttribute('filter', 'url(#' + uid + '-sh)');
        var hasChildren = childMap[n.id] && childMap[n.id].length;
        grp.appendChild(el('rect', { x: n.x - CM.NW / 2, y: n.y - n.nh / 2,
          width: CM.NW, height: n.nh, rx: CM.NR,
          fill: hasChildren ? '#eef2ff' : '#f8f7ff',
          stroke: hasChildren ? '#818cf8' : '#c4b5fd', 'stroke-width': 1 }));
        grp.appendChild(mtext(n.lines, n.x, n.y, 12, { fill: '#1e1b4b' }));
      }
      gN.appendChild(grp);
    });
    svg.appendChild(gN);
    if (gX) svg.appendChild(gX);   // arestes creuades + etiquetes SEMPRE a sobre
    return svg;
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // MAPA MENTAL — Buzan, lateral, tapered ribbon
  // ─────────────────────────────────────────────────────────────────────────────

  var MM = {
    RW: 128, RH: 42, RR: 12, L1H: 32, LNH: 24,
    XS: 200, VG: 18, M: 44, W0: 9, W1: 4, W2: 2,
    LW1: 150, LW2: 148, WMAX: 168,   // amplades màx de wrap (L1 / fulla) i cap de caixa
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

    // ── Pas 1: MESURA cada node (text amb wrap + dimensions reals) per profunditat.
    // CLAU: les FULLES (depth>=2) també s'ajusten (wrap). Abans sortien en una sola
    // línia llarga → es trepitjaven horitzontalment i no es llegien. L'alçada real
    // (segons el nombre de línies) alimenta sh() perquè reservi prou espai vertical.
    function maxLineW(lines, fs) {
      return lines.reduce(function (m, l) { return Math.max(m, tw(l, fs)); }, 0);
    }
    function measure(node, depth) {
      node.depth = depth;
      if (depth === 0) {
        node._lines = wrap(node.label, MM.RW - 16, 12);
        node._w = MM.RW; node._h = Math.max(MM.RH, node._lines.length * 16 + 10);
      } else if (depth === 1) {
        node._lines = wrap(node.label, MM.LW1, 13);
        node._w = Math.min(Math.max(64, maxLineW(node._lines, 13)) + 20, MM.WMAX);
        node._h = Math.max(MM.L1H, node._lines.length * Math.ceil(13 * 1.4) + 8);
      } else {
        node._lines = wrap(node.label, MM.LW2, 11);
        node._w = Math.min(Math.max(56, maxLineW(node._lines, 11)) + 10, MM.WMAX);
        node._h = Math.max(MM.LNH, node._lines.length * Math.ceil(11 * 1.45) + 6);
      }
      (node.children || []).forEach(function (c) { measure(c, depth + 1); });
    }
    measure(tree, 0);

    // ── Pas 2: alçada del subarbre, usant l'alçada REAL de cada node (no fixa) ──
    function sh(node) {
      var base = node._h + MM.VG;
      if (!node.children || !node.children.length) return base;
      return Math.max(base, node.children.reduce(function (s, c) { return s + sh(c); }, 0));
    }

    tree.x = 0; tree.y = 0;
    var kids   = tree.children || [];
    var nRight = Math.ceil(kids.length / 2);

    function placeGroup(group, dir) {
      if (!group.children || !group.children.length) return;
      var bx = group.x + dir * MM.XS;
      var totH = group.children.reduce(function (s, c) { return s + sh(c); }, 0) - MM.VG;
      var cy = group.y - totH / 2;
      group.children.forEach(function (child) {
        var csh = sh(child);
        child.x = bx; child.y = cy + csh / 2 - MM.VG / 2;
        placeGroup(child, dir); cy += csh;
      });
    }
    placeGroup({ x: 0, y: 0, children: kids.slice(0, nRight) },  1);
    placeGroup({ x: 0, y: 0, children: kids.slice(nRight) },    -1);

    kids.forEach(function (k, i) { k.color = MM.PALETTE[i % MM.PALETTE.length]; });
    function propagate(n) { (n.children || []).forEach(function (c) { c.color = c.color || n.color; propagate(c); }); }
    kids.forEach(propagate);

    function allNodes(n) { return [n].concat((n.children || []).reduce(function (a, c) { return a.concat(allNodes(c)); }, [])); }
    var all = allNodes(tree);
    // ViewBox a partir de les CAIXES reals (x±w/2, y±h/2), no de marges fixos.
    var x0 = Math.min.apply(null, all.map(function (n) { return n.x - n._w / 2; })) - MM.M;
    var x1 = Math.max.apply(null, all.map(function (n) { return n.x + n._w / 2; })) + MM.M;
    var y0 = Math.min.apply(null, all.map(function (n) { return n.y - n._h / 2; })) - MM.M;
    var y1 = Math.max.apply(null, all.map(function (n) { return n.y + n._h / 2; })) + MM.M;

    var uid = 'mm' + (Math.random() * 1e9 | 0);
    var svg = el('svg', { viewBox: [x0, y0, x1 - x0, y1 - y0].join(' '), xmlns: NS,
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
        grp.appendChild(el('rect', { x: node.x - node._w / 2, y: node.y - node._h / 2,
          width: node._w, height: node._h, rx: MM.RR, fill: 'url(#' + uid + '-rg)' }));
        grp.appendChild(mtext(node._lines, node.x, node.y, 12,
          { fill: '#fff', 'font-weight': '700', 'letter-spacing': '0.3px' }));
      } else if (node.depth === 1) {
        var color = node.color || '#64748b';
        grp.appendChild(el('rect', { x: node.x - node._w / 2, y: node.y - node._h / 2,
          width: node._w, height: node._h, rx: node._h / 2,
          fill: color + '18', stroke: color, 'stroke-width': 2 }));
        grp.appendChild(mtext(node._lines, node.x, node.y, 13,
          { fill: color, 'font-weight': '600' }));
      } else {
        // Fulla: text AJUSTAT (multi-línia) + subratllat sota el bloc (la cinta hi
        // arriba pel costat). Amplada del subratllat = amplada de la caixa de text.
        var color2 = node.color || '#64748b';
        grp.appendChild(el('line', { x1: node.x - node._w / 2, y1: node.y + node._h / 2 - 1,
          x2: node.x + node._w / 2, y2: node.y + node._h / 2 - 1,
          stroke: color2, 'stroke-width': 1.5, 'stroke-opacity': 0.6 }));
        grp.appendChild(mtext(node._lines, node.x, node.y - 1, 11, { fill: '#334155' }));
      }
      gN.appendChild(grp);

      (node.children || []).forEach(function (child) {
        child.parent = node;
        var color = child.color || '#94a3b8';
        var dirX  = child.x > node.x ? 1 : -1;
        var sx = node.x + dirX * node._w / 2, sy = node.y;
        // A les fulles la cinta arriba al subratllat (vora inferior); a L1, al centre.
        var tx = child.x - dirX * child._w / 2;
        var ty = child.depth >= 2 ? child.y + child._h / 2 - 1 : child.y;
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

    function nodeNW(depth) { return depth === 0 ? SC.RW : SC.NW; }
    function nodeNH(node, depth) {
      var ls = wrap(node.label, nodeNW(depth) - 16, 12);
      return Math.max(depth === 0 ? SC.RH : SC.NH, ls.length * 16 + 8);
    }
    function shH(node, depth) {
      var nh = nodeNH(node, depth);
      if (!node.children || !node.children.length) return nh + SC.VG;
      return node.children.reduce(function (s, c) { return s + shH(c, depth + 1); }, 0);
    }
    function place(node, x, sy, depth) {
      var h = shH(node, depth);
      node.x = x; node.y = sy + h / 2 - SC.VG / 2; node.depth = depth;
      node.nw = nodeNW(depth); node.nh = nodeNH(node, depth);
      var cy = sy;
      (node.children || []).forEach(function (c) {
        var ch = shH(c, depth + 1);
        place(c, x + node.nw + SC.HG, cy, depth + 1); cy += ch;
      });
    }
    place(tree, 0, 0, 0);

    function allNodes(n) { return [n].concat((n.children || []).reduce(function (a, c) { return a.concat(allNodes(c)); }, [])); }
    var all = allNodes(tree);
    var ys  = all.map(function (n) { return n.y; });
    var nhs = all.map(function (n) { return n.nh; });
    var x0  = -SC.M;
    var y0  = Math.min.apply(null, ys) - Math.max.apply(null, nhs) / 2 - SC.M;
    var x1  = Math.max.apply(null, all.map(function (n) { return n.x + n.nw; })) + SC.M;
    var y1  = Math.max.apply(null, ys) + Math.max.apply(null, nhs) / 2 + SC.M;

    var uid = 'sc' + (Math.random() * 1e9 | 0);
    var svg = el('svg', { viewBox: [x0, y0, x1 - x0, y1 - y0].join(' '), xmlns: NS,
      'font-family': pageFont() });

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
      var nw = n.nw, nh = n.nh;
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

  // Calcula width/height inicials per a un SVG donat el seu viewBox i una
  // alçada màxima de partida. Emmagatzema les dimensions naturals a data-nat-*.
  function svgInitSize(svgEl, maxH) {
    var vb = (svgEl.getAttribute('viewBox') || '').split(/\s+/).map(Number);
    var natW = vb[2] || 600, natH = vb[3] || 400;
    var scale = Math.min(1.0, (maxH || 440) / natH);
    svgEl.setAttribute('data-nat-w', natW);
    svgEl.setAttribute('data-nat-h', natH);
    svgEl.setAttribute('width',  Math.round(natW * scale));
    svgEl.setAttribute('height', Math.round(natH * scale));
    svgEl.style.display = 'block';
    svgEl.style.maxWidth = '100%';
    return Math.round(scale * 100);  // % inicial per al slider
  }

  function buildZoom(svgEl) {
    var initPct = svgInitSize(svgEl, 440);
    var row = document.createElement('div');
    row.className = 'mermaid-zoom-row';
    row.innerHTML = '<label class="mermaid-zoom-label">Mida <input type="range" ' +
      'class="mermaid-zoom-slider" min="20" max="200" value="' + initPct + '">' +
      '<span class="mermaid-zoom-pct">' + initPct + '%</span></label>';
    var sl = row.querySelector('.mermaid-zoom-slider'), sp = row.querySelector('.mermaid-zoom-pct');
    sl.addEventListener('input', function () {
      var pct = +sl.value;
      sp.textContent = pct + '%';
      var natW = parseFloat(svgEl.getAttribute('data-nat-w')) || 600;
      var natH = parseFloat(svgEl.getAttribute('data-nat-h')) || 400;
      svgEl.setAttribute('width',  Math.round(natW * pct / 100));
      svgEl.setAttribute('height', Math.round(natH * pct / 100));
    });
    return row;
  }

  function buildEdit(mdRaw, cont, type) {
    var d = document.createElement('details'); d.className = 'mermaid-edit-details';
    var s = document.createElement('summary'); s.className = 'mermaid-edit-toggle';
    s.innerHTML = '<svg viewBox="0 0 16 16" width="11" fill="currentColor"><path d="M11.013 1.427a1.75 1.75 0 0 1 2.474 0l1.086 1.086a1.75 1.75 0 0 1 0 2.474l-8.61 8.61c-.21.21-.47.364-.756.445l-3.251.93a.75.75 0 0 1-.927-.928l.929-3.25c.081-.286.235-.547.445-.758l8.61-8.61zm1.414 1.06a.25.25 0 0 0-.354 0l-8.61 8.61a.25.25 0 0 0-.064.108l-.681 2.382 2.382-.68a.25.25 0 0 0 .108-.065l8.61-8.61a.25.25 0 0 0 0-.353z"/></svg> Editar font del diagrama';
    var ta = document.createElement('textarea');
    ta.className = 'mermaid-edit-textarea'; ta.value = mdRaw; ta.rows = 9; ta.spellcheck = false;
    // Fix 2026-06-02: el textarea de 9 files (~110px) era massa baix per a
    // mapes/esquemes complexos (contingut de 300px+) → calia scroll dins una
    // caixa petita i "no es veia el text sencer". L'autoajustem al contingut,
    // amb un mínim raonable i un sostre del 70% de la finestra (perquè no
    // ocupi tota la pantalla i el botó "Refés" quedi sempre accessible).
    function autosize() {
      ta.style.height = 'auto';
      var maxH = Math.round(window.innerHeight * 0.7);
      var minH = 130;
      ta.style.height = Math.min(Math.max(ta.scrollHeight + 4, minH), maxH) + 'px';
    }
    ta.addEventListener('input', autosize);
    var btn = document.createElement('button');
    btn.type = 'button'; btn.className = 'mermaid-rerender-btn'; btn.textContent = 'Refés el diagrama';
    btn.addEventListener('click', function () {
      var newMd = ta.value.trim(); if (!newMd) return;
      cont.dataset.md = newMd; cont.classList.remove('mermaid-active'); cont.innerHTML = '';
      renderMermaidBlock(cont, newMd, type);
    });
    d.appendChild(s); d.appendChild(ta); d.appendChild(btn);
    // Quan s'obre el details, ajusta l'alçada al contingut i desplaça'l a la vista.
    d.addEventListener('toggle', function () {
      if (d.open) setTimeout(function () { autosize(); ta.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); }, 60);
    });
    return d;
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // RENDER PRINCIPAL
  // ─────────────────────────────────────────────────────────────────────────────

  function renderMermaidBlock(cont, mdRaw, compType) {
    if (cont.querySelector('.diagram-wrapper')) return;
    if (cont.classList.contains('schema')) cont.classList.add('mermaid-active');
    cont.dataset.compType = compType;

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
    // Re-renderitza tots els diagrames ja existents (e.g., quan canvia la font)
    reRenderAll: function () {
      document.querySelectorAll('[data-comp-type][data-md]').forEach(function (cont) {
        var md   = cont.dataset.md;
        var type = cont.dataset.compType;
        if (!md || !type) return;
        cont.classList.remove('mermaid-active');
        cont.innerHTML = '';
        renderMermaidBlock(cont, md, type);
      });
    },
  };

  // Exposició per a tests deterministes (parseTree/treeToGraph són funcions PURES,
  // no toquen el DOM). Innocu en producció. Veure tests/test_diagrames_parse.js.
  window.ATNE_DIAGRAM_TEST = { parseTree: parseTree, treeToGraph: treeToGraph };

})();
