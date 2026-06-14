/**
 * tests/test_mindmap_layout.js — guard determinista del LAYOUT del MAPA MENTAL
 * (buildMindMap del renderitzador de diagrames).
 *
 * Renderitza un mapa mental amb etiquetes LLARGUES (el cas real "Revolució
 * Industrial") amb el pipeline real (renderMermaidBlock) sobre un DOM stub i
 * verifica les correccions de llegibilitat (14/06):
 *
 *   1. Tots els nodes es dibuixen (data-nid) — cap descartat.
 *   2. Les FULLES amb etiqueta llarga s'AJUSTEN (wrap → multi-línia). Abans
 *      sortien en una sola línia llarga i es trepitjaven.
 *   3. Cap solapament VERTICAL entre nodes de la MATEIXA columna (l'alçada real
 *      per nombre de línies alimenta el layout → germanes amb prou separació).
 *
 * Cap dependència; corre a node net (job `core` del CI; només llegeix fitxers
 * del repo).  ÚS: node tests/test_mindmap_layout.js
 */
'use strict';
const fs = require('fs');
const path = require('path');

// ── DOM stub mínim (mateix patró que test_diagram_layout.js) ──
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
  set: function (v) { if (v === '') this.children = []; },
});
Object.defineProperty(FakeEl.prototype, 'className', {
  get: function () { return this.attrs.class || ''; },
  set: function (v) { this.attrs.class = String(v); },
});
FakeEl.prototype.querySelector = function (sel) { if (/wrapper/.test(sel)) return null; return new FakeEl('stub'); };
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
if (!M || !M.renderMermaidBlock) { console.error('ERROR: ATNE_MERMAID absent'); process.exit(2); }

let fails = 0;
function check(name, cond, detail) {
  if (cond) console.log('  OK   ' + name);
  else { console.log('  FAIL ' + name + (detail ? ' — ' + detail : '')); fails++; }
}
function descendants(el, acc) { acc = acc || []; el.children.forEach(function (c) { acc.push(c); descendants(c, acc); }); return acc; }

// Mapa mental real (cas "Revolució Industrial") amb fulles LLARGUES (preguntes).
const MD = [
  '- **Revolució Industrial**',
  '  - Factors tècnics',
  '    - Màquina de vapor',
  '    - Innovació tecnològica',
  '  - Recursos naturals',
  '    - Carbó i ferro',
  '    - Abundància a Anglaterra',
  '  - Transformacions socials',
  '    - Creixement urbà',
  '    - Aparició de noves classes socials',
  '  - Impacte ambiental',
  '    - Consum de combustibles fòssils',
  "    - Inici de l'Antropocè",
  '  - Preguntes obertes',
  '    - Com serien les ciutats sense la Revolució Industrial?',
  '    - Quins altres factors podrien haver impulsat una revolució similar?',
].join('\n');

var cont = new FakeEl('div');
cont.dataset.md = MD;
M.renderMermaidBlock(cont, MD, 'mapa_mental');

// Recull els grups de node (data-nid) i, per cada un, les seves línies de text.
var groups = descendants(cont).filter(function (e) { return e.tagName === 'g' && ('data-nid' in e.attrs); });
function nodeInfo(g) {
  var texts = descendants(g).filter(function (e) { return e.tagName === 'text'; });
  var ys = texts.map(function (t) { return +t.attrs.y; });
  var xs = texts.map(function (t) { return +t.attrs.x; });
  return { lbl: g.attrs['data-lbl'] || '', nLines: texts.length,
           x: xs.length ? xs[0] : 0, top: Math.min.apply(null, ys), bottom: Math.max.apply(null, ys) };
}
var infos = groups.map(nodeInfo);

// (1) Tots els nodes dibuixats (16 = arrel + 5 branques + 10 fulles).
check('mapa mental: tots els nodes dibuixats', groups.length === 16, 'grups=' + groups.length);

// (2) Les fulles amb pregunta llarga s'AJUSTEN (wrap → > 1 línia).
var longLeaf = infos.find(function (n) { return /Com serien les ciutats/.test(n.lbl); });
check('fulla llarga fa wrap (> 1 línia)', !!longLeaf && longLeaf.nLines > 1,
  longLeaf ? ('nLines=' + longLeaf.nLines) : 'fulla no trobada');

// (3) Cap solapament VERTICAL entre nodes de la MATEIXA columna (mateix x ±2 px).
//     Marge de mitja línia (8 px) al voltant del rang de text de cada node.
var PAD = 8, overlap = null;
for (var i = 0; i < infos.length && !overlap; i++) {
  for (var j = i + 1; j < infos.length; j++) {
    var a = infos[i], b = infos[j];
    if (Math.abs(a.x - b.x) > 2) continue;                 // columnes diferents → ok
    var aTop = a.top - PAD, aBot = a.bottom + PAD, bTop = b.top - PAD, bBot = b.bottom + PAD;
    if (aTop < bBot && bTop < aBot) {                       // rangs verticals que es creuen
      overlap = a.lbl + ' ↔ ' + b.lbl + ' (x=' + a.x + ')'; break;
    }
  }
}
check('cap solapament vertical entre nodes de la mateixa columna', !overlap, overlap || '');

console.log(fails === 0 ? '\nTOTS OK' : `\n${fails} FALLADES`);
process.exit(fails === 0 ? 0 : 1);
