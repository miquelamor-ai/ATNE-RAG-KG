/**
 * tests/test_diagram_layout.js — guard determinista del LAYOUT del mapa conceptual
 * (bloc B / correccions del bloc A del renderitzador de diagrames).
 *
 * Carrega ui/atne/js/diagram-editor-core.js (ATNE_EDIT_CORE) + ui/atne/js/
 * mermaid-converter.js sobre un DOM stub mínim, renderitza mostres de markdown amb
 * el pipeline REAL (renderMermaidBlock) i inspecciona el SVG resultant. Verifica:
 *
 *   1. Cadena de 4+ nivells -> nº de nodes amb data-line == nº d'ítems del markdown
 *      (A1: el layout recursiu no descarta nodes profunds en silenci).
 *   2. Concepte amb 2 proposicions -> les dues queden EN PARAL·LEL (mateixa y, x
 *      diferent) (A2: fork horitzontal, no cadena vertical falsa).
 *   3. Mapa de 3 nivells -> geometria byte-a-byte estable (snapshot anti-regressió).
 *   4. Bloc "Enllaços creuats" -> splitCross el separa i parseTree de l'arbre
 *      l'ignora; el render hi posa una etiqueta clicable (data-cross-idx).
 *
 * Cap dependència; corre a node net (job `core` del CI, sense submodule: només
 * llegeix fitxers del repo).  ÚS: node tests/test_diagram_layout.js
 */
'use strict';
const fs = require('fs');
const path = require('path');

// ── DOM stub mínim però suficient per a renderMermaidBlock (SVG + zoom + edit) ──
function FakeEl(tag) {
  this.tagName = tag; this.attrs = {}; this.children = []; this.style = {};
  this.dataset = {}; this._text = ''; this._classes = new Set();
  var self = this;
  this.classList = {
    add: function (c) { self._classes.add(c); },
    remove: function (c) { self._classes.delete(c); },
    contains: function (c) { return self._classes.has(c); },
    toggle: function (c, on) { if (on === undefined) on = !self._classes.has(c); on ? self._classes.add(c) : self._classes.delete(c); },
  };
}
FakeEl.prototype.setAttribute = function (k, v) { this.attrs[k] = String(v); };
FakeEl.prototype.getAttribute = function (k) { return (k in this.attrs) ? this.attrs[k] : null; };
FakeEl.prototype.hasAttribute = function (k) { return k in this.attrs; };
FakeEl.prototype.removeAttribute = function (k) { delete this.attrs[k]; };
FakeEl.prototype.appendChild = function (c) { if (c) this.children.push(c); return c; };
FakeEl.prototype.insertBefore = function (c) { if (c) this.children.unshift(c); return c; };
FakeEl.prototype.removeChild = function (c) { var i = this.children.indexOf(c); if (i >= 0) this.children.splice(i, 1); return c; };
FakeEl.prototype.replaceChild = function (n, o) { var i = this.children.indexOf(o); if (i >= 0) this.children[i] = n; return o; };
FakeEl.prototype.addEventListener = function () {};
FakeEl.prototype.removeEventListener = function () {};
FakeEl.prototype.cloneNode = function () { return new FakeEl(this.tagName); };
FakeEl.prototype.getBoundingClientRect = function () { return { left: 0, top: 0, right: 0, bottom: 0, width: 0, height: 0 }; };
Object.defineProperty(FakeEl.prototype, 'textContent', {
  get: function () { return this._text; },
  set: function (v) { this._text = v; this.children = []; },
});
Object.defineProperty(FakeEl.prototype, 'innerHTML', {
  get: function () { return ''; },
  set: function (v) { if (v === '') this.children = []; },   // noop creatiu (no parsegem HTML)
});
Object.defineProperty(FakeEl.prototype, 'className', {
  get: function () { return this.attrs.class || ''; },
  set: function (v) { this.attrs.class = String(v); },
});
function _hasClass(el, cls) {
  return ((el.attrs && el.attrs.class) || '').split(/\s+/).indexOf(cls) >= 0 || (el._classes && el._classes.has(cls));
}
function _classFromSel(sel) { var m = sel.match(/\.([\w-]+)/); return m ? m[1] : null; }
FakeEl.prototype.querySelector = function (sel) {
  // Els selectors de wrapper han de cercar de debò (han de tornar null si absents).
  if (/wrapper/.test(sel)) {
    var cls = _classFromSel(sel), found = null;
    (function walk(el) {
      for (var i = 0; i < el.children.length && !found; i++) {
        if (_hasClass(el.children[i], cls)) found = el.children[i];
        else walk(el.children[i]);
      }
    })(this);
    return found;
  }
  // Per a la resta (slider/pct del zoom, etc.) tornem un stub no-null perquè el
  // codi encadenat (addEventListener) no peti. El test no els inspecciona.
  return new FakeEl('stub');
};
FakeEl.prototype.querySelectorAll = function () { return []; };

global.window = {};
global.localStorage = { getItem: function () { return null; } };
global.document = {
  createElement: function (t) { return new FakeEl(t); },
  createElementNS: function (ns, t) { return new FakeEl(t); },
  getElementById: function () { return null; },
  addEventListener: function () {},
};
global.MouseEvent = function () {};
global.MutationObserver = function () { this.observe = function () {}; this.disconnect = function () {}; };

const ROOT = path.join(__dirname, '..');
eval(fs.readFileSync(path.join(ROOT, 'ui', 'atne', 'js', 'diagram-editor-core.js'), 'utf8'));
eval(fs.readFileSync(path.join(ROOT, 'ui', 'atne', 'js', 'mermaid-converter.js'), 'utf8'));

const M = global.window.ATNE_MERMAID;
const C = global.window.ATNE_EDIT_CORE;
const T = global.window.ATNE_DIAGRAM_TEST;
if (!M || !M.renderMermaidBlock || !C || !T) {
  console.error('ERROR: API absent (ATNE_MERMAID / ATNE_EDIT_CORE / ATNE_DIAGRAM_TEST)');
  process.exit(2);
}

// ── Utilitats d'inspecció del SVG renderitzat ──
function render(md) {
  var cont = new FakeEl('div');
  cont.dataset.md = md;
  M.renderMermaidBlock(cont, md, 'mapa_conceptual');
  return cont;
}
function descendants(el, acc) {
  acc = acc || [];
  el.children.forEach(function (c) { acc.push(c); descendants(c, acc); });
  return acc;
}
function nodeGroups(cont) {     // grups de NODE (data-nid present), exclou enllaços creuats
  return descendants(cont).filter(function (e) { return e.tagName === 'g' && ('data-nid' in e.attrs); });
}
function crossGroups(cont) {
  return descendants(cont).filter(function (e) { return e.tagName === 'g' && ('data-cross-idx' in e.attrs); });
}
// Centre (cx,cy) d'un grup de node: del rect (concepte/arrel) o del primer text (proposició)
function center(g) {
  var ds = descendants(g);
  var rect = ds.find(function (e) { return e.tagName === 'rect'; });
  if (rect) return { cx: +rect.attrs.x + (+rect.attrs.width) / 2, cy: +rect.attrs.y + (+rect.attrs.height) / 2 };
  var t = ds.find(function (e) { return e.tagName === 'text'; });
  if (t) return { cx: +t.attrs.x, cy: +t.attrs.y };
  return null;
}

let fails = 0;
function check(name, cond, detail) {
  if (cond) { console.log('  OK   ' + name); }
  else { console.log('  FAIL ' + name + (detail ? ' — ' + detail : '')); fails++; }
}
function countItems(md) { return md.split('\n').filter(function (l) { return /^\s*-\s+/.test(l); }).length; }

// ─────────────────────────────────────────────────────────────────────────────
// 1) Cadena de 4+ nivells: cap node descartat (A1)
// ─────────────────────────────────────────────────────────────────────────────
const deepChain = [
  '- **Arrel**',
  '  - **provoca**',
  '    - Concepte A',
  '      - **porta a**',
  '        - Concepte B',
  '          - **deriva en**',
  '            - Concepte C',
].join('\n');
(function () {
  var cont = render(deepChain);
  var groups = nodeGroups(cont);
  var withLine = groups.filter(function (g) { return g.attrs['data-line'] !== '-1'; });
  check('cadena 4+ nivells: tots els nodes dibuixats (cap descartat)',
    groups.length === countItems(deepChain) && withLine.length === countItems(deepChain),
    'grups=' + groups.length + ' ítems=' + countItems(deepChain));
})();

// ─────────────────────────────────────────────────────────────────────────────
// 2) + 3) Mapa A2 de 3 nivells: fork de proposicions germanes + snapshot estable
// ─────────────────────────────────────────────────────────────────────────────
const mapaA2 = [
  '- **Escalfament global**',
  '  - **Causes**',
  '    - gasos',
  '    - crema',
  '  - **Conseqüències**',
  '    - desglaç',
  '    - pujada',
].join('\n');
(function () {
  var cont = render(mapaA2);
  var groups = nodeGroups(cont);
  // Mapa per data-line → centre
  var byLine = {};
  groups.forEach(function (g) { byLine[g.attrs['data-line']] = center(g); });

  // (2) Les dues proposicions (línies 1 i 4) en PARAL·LEL: mateixa y, x diferent.
  var p1 = byLine['1'], p2 = byLine['4'];
  check('A2 fork: 2 proposicions germanes mateixa y',
    p1 && p2 && Math.abs(p1.cy - p2.cy) < 0.5, p1 && p2 ? ('y1=' + p1.cy + ' y2=' + p2.cy) : 'props no trobades');
  check('A2 fork: 2 proposicions germanes x diferent',
    p1 && p2 && Math.abs(p1.cx - p2.cx) > 1, p1 && p2 ? ('x1=' + p1.cx + ' x2=' + p2.cx) : 'props no trobades');

  // (3) Snapshot byte-a-byte de la geometria (tots els centres, arrodonits).
  var snap = Object.keys(byLine).sort(function (a, b) { return +a - +b; })
    .map(function (k) { var c = byLine[k]; return k + ':' + Math.round(c.cx) + ',' + Math.round(c.cy); })
    .join('|');
  // Snapshot amb LG=20 (gap vertical entre germans, ampliat el 13/06 per donar aire).
  const EXPECTED = '0:164,0|1:82,75|2:82,132|3:82,188|4:246,75|5:246,132|6:246,188';
  check('A2 snapshot: geometria estable (anti-regressió)', snap === EXPECTED,
    '\n      actual:   ' + snap + '\n      esperat:  ' + EXPECTED);
})();

// ─────────────────────────────────────────────────────────────────────────────
// 4) Bloc "Enllaços creuats": splitCross separa, parseTree ignora, render etiqueta
// ─────────────────────────────────────────────────────────────────────────────
const ambCross = [
  '- **A**',
  '  - **rel**',
  '    - B',
  '  - **rel2**',
  '    - D',
  '',
  '- Enllaços creuats:',
  '  - B -> D : depèn de',
].join('\n');
(function () {
  var s = C.splitCross(ambCross);
  check('splitCross: separa 1 enllaç creuat', s.cross.length === 1,
    'cross=' + JSON.stringify(s.cross.map(function (c) { return c.from + '->' + c.to; })));
  check('splitCross: l\'arbre no conté el bloc d\'enllaços creuats',
    !/Enlla[çc]os creuats/.test(s.tree), s.tree);
  var tree = T.treeToGraph(T.parseTree(s.tree));
  check('parseTree ignora el bloc: 5 nodes d\'arbre (A,rel,B,rel2,D)', tree.nodes.length === 5,
    'nodes=' + tree.nodes.length);
  var cont = render(ambCross);
  check('render: el node-count del SVG NO inclou l\'enllaç creuat',
    nodeGroups(cont).length === 5, 'grups=' + nodeGroups(cont).length);
  check('render: l\'enllaç creuat té etiqueta clicable (data-cross-idx)',
    crossGroups(cont).length === 1, 'cross-grups=' + crossGroups(cont).length);
})();

// ─────────────────────────────────────────────────────────────────────────────
// 5) + 6) Enllaços creuats per CANAL LLIURE (decisió 14/06): la corba (2 cúbics)
//    surt pel passadís i va per sota/sobre de l'abast → NO entra DINS de cap
//    concepte. Ni la corba ni l'etiqueta (col·locació intel·ligent) el trepitgen.
// ─────────────────────────────────────────────────────────────────────────────
function nodeRects(cont) {
  return nodeGroups(cont).map(function (g) {
    var r = descendants(g).find(function (e) { return e.tagName === 'rect'; });
    return r ? { x: +r.attrs.x, y: +r.attrs.y, w: +r.attrs.width, h: +r.attrs.height } : null;
  }).filter(Boolean);
}
function crossCurve(cont) {   // la corba de l'enllaç (traç '4 3'), no el leader ('2 2')
  return descendants(cont).find(function (e) {
    return e.tagName === 'path' && /4 3/.test(e.attrs['stroke-dasharray'] || '');
  });
}
function cubicAt(p0, p1, p2, p3, t) {
  var u = 1 - t;
  return {
    x: u * u * u * p0.x + 3 * u * u * t * p1.x + 3 * u * t * t * p2.x + t * t * t * p3.x,
    y: u * u * u * p0.y + 3 * u * u * t * p1.y + 3 * u * t * t * p2.y + t * t * t * p3.y,
  };
}
function crossSamples(cont) {
  var p = crossCurve(cont); if (!p) return [];
  var nums = (p.attrs.d || '').match(/-?[\d.]+/g) || [], pts = [];
  for (var i = 0; i + 1 < nums.length; i += 2) pts.push({ x: +nums[i], y: +nums[i + 1] });
  var s = [];   // pts = [P0, c1,c2,P1, c3,c4,P2] → dos cúbics
  function smp(a, b, c, d) { for (var t = 0; t <= 1.0001; t += 0.04) s.push(cubicAt(a, b, c, d, t)); }
  if (pts.length >= 4) smp(pts[0], pts[1], pts[2], pts[3]);
  if (pts.length >= 7) smp(pts[3], pts[4], pts[5], pts[6]);
  return s;
}
function pointInRect(p, r, inset) {
  return p.x > r.x + inset && p.x < r.x + r.w - inset && p.y > r.y + inset && p.y < r.y + r.h - inset;
}
function crossHitsNode(cont) {
  var rects = nodeRects(cont), s = crossSamples(cont);
  for (var i = 0; i < s.length; i++)
    for (var j = 0; j < rects.length; j++)
      if (pointInRect(s[i], rects[j], 2)) return true;
  return false;
}
function labelBox(cont) {
  var cg = crossGroups(cont)[0]; if (!cg) return null;
  var r = descendants(cg).find(function (e) { return e.tagName === 'rect'; });
  return r ? { x: +r.attrs.x, y: +r.attrs.y, w: +r.attrs.width, h: +r.attrs.height } : null;
}
function rectsOverlap(a, b, inset) {
  return a.x < b.x + b.w - inset && a.x + a.w > b.x + inset &&
         a.y < b.y + b.h - inset && a.y + a.h > b.y + inset;
}
// L'etiqueta d'un enllaç pot SEURE entre els seus dos conceptes (origen/destí) i
// tocar-los; el que NO pot és trepitjar un concepte ALIÈ. `endpoints` = labels de
// l'origen i el destí d'aquest enllaç, que s'exclouen de la comprovació.
function labelHitsNode(cont, endpoints) {
  var lr = labelBox(cont); if (!lr) return false;
  endpoints = endpoints || [];
  return nodeGroups(cont).filter(function (g) { return endpoints.indexOf(g.attrs['data-lbl']) < 0; })
    .map(function (g) { var r = descendants(g).find(function (e) { return e.tagName === 'rect'; });
      return r ? { x: +r.attrs.x, y: +r.attrs.y, w: +r.attrs.width, h: +r.attrs.height } : null; })
    .filter(Boolean)
    .some(function (n) { return rectsOverlap(lr, n, 2); });
}
// (5) Enllaç horitzontal amb germans apilats dins l'abast (etiqueta llarga).
(function () {
  var cont = render([
    '- **R**', '  - **a**', '    - X1', '    - X2', '  - **b**', '    - Y1', '    - Y2',
    '', '- Enllaços creuats:', '  - X1 -> Y1 : cau des dels núvols',
  ].join('\n'));
  check('enllaç creuat (mateixa fila): corba NI etiqueta trepitgen cap concepte aliè',
    !crossHitsNode(cont) && !labelHitsNode(cont, ['X1', 'Y1']),
    'corba=' + crossHitsNode(cont) + ' etiqueta=' + labelHitsNode(cont, ['X1', 'Y1']));
})();
// (6) Enllaç entre files diferents (columnes de profunditat desigual).
(function () {
  var cont = render([
    '- **R**', '  - **a**', '    - X1', '    - X2', '    - X3', '  - **b**', '    - Y1',
    '', '- Enllaços creuats:', '  - X3 -> Y1 : prové de',
  ].join('\n'));
  check('enllaç creuat (files diferents): corba NI etiqueta trepitgen cap concepte aliè',
    !crossHitsNode(cont) && !labelHitsNode(cont, ['X3', 'Y1']),
    'corba=' + crossHitsNode(cont) + ' etiqueta=' + labelHitsNode(cont, ['X3', 'Y1']));
})();

// (7) Col·locació intel·ligent: si el punt mig de l'enllaç cau sobre un concepte,
//     l'etiqueta s'ha de DESPLAÇAR al buit (no quedar damunt del concepte).
(function () {
  var cont = render([
    '- **R**', '  - **a**', '    - X1', '  - **b**', '    - Y1', '  - **c**', '    - Z1',
    '', '- Enllaços creuats:', '  - X1 -> Z1 : passa per',   // punt mig ≈ sobre Y1
  ].join('\n'));
  var lb = labelBox(cont);
  function nrects(c) {
    return nodeGroups(c).map(function (g) {
      var r = descendants(g).find(function (e) { return e.tagName === 'rect'; });
      return r ? { x: +r.attrs.x, y: +r.attrs.y, w: +r.attrs.width, h: +r.attrs.height } : null;
    }).filter(Boolean);
  }
  function ov(a, b) { return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y; }
  var hits = !!lb && nrects(cont).some(function (n) { return ov(lb, n); });
  check('col·locació intel·ligent: l\'etiqueta es mou del concepte al buit',
    !!lb && !hits, 'label=' + !!lb + ' solapa_concepte=' + hits);
})();

// (8) Estils DIFERENTS per enllaç creuat (decisió Miquel 15/06): si n'hi ha 2 o 3,
//     cada un ha de tenir un traç/color propi (paleta cíclica per índex), per no
//     confondre'ls. Doble codi (color + discontinuïtat). L'1r conserva l'estil històric.
(function () {
  var cont = render([
    '- **R**', '  - **a**', '    - X1', '  - **b**', '    - Y1', '  - **c**', '    - Z1',
    '', '- Enllaços creuats:',
    '  - X1 -> Y1 : rel1', '  - Y1 -> Z1 : rel2', '  - X1 -> Z1 : rel3',
  ].join('\n'));
  var curves = descendants(cont).filter(function (e) {
    return e.tagName === 'path' && /xarr/.test(e.attrs['marker-end'] || '');
  });
  var dashes = curves.map(function (p) { return p.attrs['stroke-dasharray']; });
  check('3 enllaços creuats → 3 corbes dibuixades', curves.length === 3, 'corbes=' + curves.length);
  check('cada enllaç creuat amb traç DIFERENT (no es confonen)', new Set(dashes).size === 3,
    'dashes=' + JSON.stringify(dashes));
})();

console.log(fails === 0 ? '\nTOTS OK' : `\n${fails} FALLADES`);
process.exit(fails === 0 ? 0 : 1);
