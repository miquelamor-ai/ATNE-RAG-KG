/**
 * tests/test_editor_md_alignment.js — guard de regressió del bug 15/06:
 * +/×/germana operaven sobre la branca equivocada a pas3.
 *
 * Causa: el renderitzador calcula `data-line` sobre el markdown FILTRAT (sense la
 * capçalera `## Mapa conceptual`), però l'editor operava sobre `dataset.md`, que a
 * pas3 conserva la capçalera (+ línia en blanc) = 2 línies de més → cada mutació
 * per índex quedava desplaçada 2 línies. (↝ no es veia afectat: opera per etiqueta.)
 *
 * Fix: `md()` de l'editor SEMPRE filtra (filterMd). Aquest test verifica que, fins
 * i tot amb la capçalera present a la font, la font OPERATIVA de l'editor
 * (window.ATNE_DIAGRAM_EDITOR._filterMd) queda alineada amb els `data-line` del
 * SVG — i que SENSE filtrar quedaria desplaçada (documenta el bug).
 *
 * Cap dependència; corre a node net (job `core` del CI).
 *   ÚS: node tests/test_editor_md_alignment.js
 */
'use strict';
const fs = require('fs');
const path = require('path');

// ── DOM stub mínim (suficient per a renderMermaidBlock + càrrega de l'editor) ──
function FakeEl(tag) {
  this.tagName = tag; this.attrs = {}; this.children = []; this.style = {};
  this.dataset = {}; this._text = ''; this._classes = new Set();
  var self = this;
  this.classList = {
    add: function (c) { self._classes.add(c); }, remove: function (c) { self._classes.delete(c); },
    contains: function (c) { return self._classes.has(c); }, toggle: function () {} };
}
FakeEl.prototype.setAttribute = function (k, v) { this.attrs[k] = String(v); };
FakeEl.prototype.getAttribute = function (k) { return (k in this.attrs) ? this.attrs[k] : null; };
FakeEl.prototype.hasAttribute = function (k) { return k in this.attrs; };
FakeEl.prototype.appendChild = function (c) { if (c) this.children.push(c); return c; };
FakeEl.prototype.insertBefore = function (c) { if (c) this.children.unshift(c); return c; };
FakeEl.prototype.removeChild = function (c) { var i = this.children.indexOf(c); if (i >= 0) this.children.splice(i, 1); return c; };
FakeEl.prototype.replaceChild = function (n, o) { var i = this.children.indexOf(o); if (i >= 0) this.children[i] = n; return o; };
FakeEl.prototype.addEventListener = function () {};
FakeEl.prototype.cloneNode = function () { return new FakeEl(this.tagName); };
FakeEl.prototype.getBoundingClientRect = function () { return { left: 0, top: 0, right: 0, bottom: 0, width: 0, height: 0 }; };
Object.defineProperty(FakeEl.prototype, 'textContent', { get: function () { return this._text; }, set: function (v) { this._text = v; this.children = []; } });
Object.defineProperty(FakeEl.prototype, 'innerHTML', { get: function () { return ''; }, set: function (v) { if (v === '') this.children = []; } });
Object.defineProperty(FakeEl.prototype, 'className', { get: function () { return this.attrs.class || ''; }, set: function (v) { this.attrs.class = String(v); } });
function _hasClass(el, cls) { return ((el.attrs && el.attrs.class) || '').split(/\s+/).indexOf(cls) >= 0 || (el._classes && el._classes.has(cls)); }
FakeEl.prototype.querySelector = function (sel) {
  if (/wrapper/.test(sel)) {
    var cls = (sel.match(/\.([\w-]+)/) || [])[1], found = null;
    (function walk(el) { for (var i = 0; i < el.children.length && !found; i++) { if (_hasClass(el.children[i], cls)) found = el.children[i]; else walk(el.children[i]); } })(this);
    return found;
  }
  return new FakeEl('stub');
};
FakeEl.prototype.querySelectorAll = function () { return []; };

global.window = {};
global.localStorage = { getItem: function () { return null; } };
global.document = {
  createElement: function (t) { return new FakeEl(t); },
  createElementNS: function (ns, t) { return new FakeEl(t); },
  getElementById: function () { return null; }, addEventListener: function () {},
};
global.MouseEvent = function () {};
global.MutationObserver = function () { this.observe = function () {}; this.disconnect = function () {}; };

const ROOT = path.join(__dirname, '..');
eval(fs.readFileSync(path.join(ROOT, 'ui', 'atne', 'js', 'diagram-editor-core.js'), 'utf8'));
eval(fs.readFileSync(path.join(ROOT, 'ui', 'atne', 'js', 'mermaid-converter.js'), 'utf8'));
eval(fs.readFileSync(path.join(ROOT, 'ui', 'atne', 'js', 'diagram-editor-ui.js'), 'utf8'));

const M = global.window.ATNE_MERMAID;
const ED = global.window.ATNE_DIAGRAM_EDITOR;
if (!M || !ED || typeof ED._filterMd !== 'function') {
  console.error('ERROR: API absent (ATNE_MERMAID / ATNE_DIAGRAM_EDITOR._filterMd)'); process.exit(2);
}

let fails = 0;
function check(name, cond, detail) {
  if (cond) console.log('  OK   ' + name);
  else { console.log('  FAIL ' + name + (detail ? ' — ' + detail : '')); fails++; }
}
function descendants(el, acc) { acc = acc || []; el.children.forEach(function (c) { acc.push(c); descendants(c, acc); }); return acc; }
function rawLbl(l) { return (l || '').replace(/^\s*-\s+/, '').replace(/\*\*/g, '').trim(); }

// Markdown REAL de pas3: amb la capçalera `## Mapa conceptual` + línia en blanc,
// i un bloc d'enllaços creuats al final (com el genera l'LLM segons el canon).
const withHeader = [
  '## Mapa conceptual', '',
  '- **Cicle de l’aigua**',
  '  - **s’evapora per**',
  '    - la calor del sol',
  '    - la temperatura',
  '  - **es condensa en**',
  '    - núvols',
  '    - boira',
  '  - **precipita com**',
  '    - pluja',
  '    - neu',
  '', '- Enllaços creuats:',
  '  - pluja -> núvols : cau des dels',
].join('\n');

// Renderitza amb la font AMB capçalera (com fa el render a pas3) i recull data-line.
var cont = new FakeEl('div');
cont.dataset.md = withHeader;
M.renderMermaidBlock(cont, withHeader, 'mapa_conceptual');
var groups = descendants(cont).filter(function (e) { return e.tagName === 'g' && ('data-nid' in e.attrs); });

// Font OPERATIVA de l'editor (després del fix): filtrada.
var editorMd = ED._filterMd(withHeader).split('\n');
// Font crua (el bug): sense filtrar.
var rawMd = withHeader.split('\n');

var alignedFiltered = 0, misalignedRaw = 0;
groups.forEach(function (g) {
  var dl = +g.attrs['data-line'], lbl = g.attrs['data-lbl'];
  if (rawLbl(editorMd[dl]) === lbl) alignedFiltered++;
  if (rawLbl(rawMd[dl]) !== lbl) misalignedRaw++;
});

check('amb capçalera, la font operativa (filterMd) queda ALINEADA amb data-line',
  alignedFiltered === groups.length, alignedFiltered + '/' + groups.length + ' nodes alineats');

// Sanity invers: documenta el bug — sense filtrar, els índexs estarien desplaçats.
check('sense filtrar, els índexs estarien DESPLAÇATS (reprodueix el bug)',
  misalignedRaw > 0, misalignedRaw + ' nodes desplaçats amb la font crua');

// Cas concret del Bug 1: "es condensa en" no ha d'apuntar a una branca veïna.
var ec = groups.find(function (g) { return g.attrs['data-lbl'] === 'es condensa en'; });
if (ec) {
  var dl = +ec.attrs['data-line'];
  check('Bug 1: clicar "es condensa en" → la font operativa hi apunta (no a un veí)',
    rawLbl(editorMd[dl]) === 'es condensa en',
    'editorMd[' + dl + ']="' + rawLbl(editorMd[dl]) + '" vs rawMd[' + dl + ']="' + rawLbl(rawMd[dl]) + '"');
}

console.log(fails === 0 ? '\nTOTS OK' : `\n${fails} FALLADES`);
process.exit(fails === 0 ? 0 : 1);
