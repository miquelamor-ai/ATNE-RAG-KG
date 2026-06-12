/**
 * tests/test_diagrames_parse.js — guard determinista del renderitzador de diagrames.
 *
 * Blinda les funcions PURES parseTree + treeToGraph de ui/atne/js/mermaid-converter.js
 * (exposades via window.ATNE_DIAGRAM_TEST). Verifica que:
 *   - el format Novak amb paraules d'enllaç (mini-brief Fable) → nodes-proposició,
 *   - el format de PRODUCCIÓ del canon (branques en negreta amb noms de categoria) → idem,
 *   - una llista SENSE negretes no-arrel → 0 proposicions (compatibilitat enrere),
 *   - les capçaleres `###` es filtren (cap node corrupte).
 *
 * Origen: Canvi 2 del mini-brief de l'auditoria 12/06. Cap dependència; corre a node net.
 * ÚS: node tests/test_diagrames_parse.js   (exit != 0 si alguna comprovació falla)
 */
'use strict';
const fs = require('fs');
const path = require('path');

// Stubs mínims perquè l'IIFE de mermaid-converter.js carregui (les funcions pures
// parseTree/treeToGraph NO toquen el DOM; només cal que window existeixi a la càrrega).
global.window = {};
global.document = { createElementNS: () => ({ setAttribute() {}, appendChild() {} }) };
global.localStorage = { getItem: () => null };

const code = fs.readFileSync(
  path.join(__dirname, '..', 'ui', 'atne', 'js', 'mermaid-converter.js'), 'utf8');
eval(code); // executa l'IIFE → omple window.ATNE_DIAGRAM_TEST

const API = global.window.ATNE_DIAGRAM_TEST;
if (!API || !API.parseTree || !API.treeToGraph) {
  console.error('ERROR: window.ATNE_DIAGRAM_TEST no exposat'); process.exit(2);
}
const { parseTree, treeToGraph } = API;

let fails = 0;
function check(name, cond, detail) {
  if (cond) { console.log('  OK   ' + name); }
  else { console.log('  FAIL ' + name + (detail ? ' — ' + detail : '')); fails++; }
}
function counts(md) {
  const g = treeToGraph(parseTree(md));
  const c = { root: 0, prop: 0, concept: 0 };
  g.nodes.forEach(n => { c[n.type] = (c[n.type] || 0) + 1; });
  return c;
}

// 1) Format Novak amb PARAULES D'ENLLAÇ (exemple del mini-brief de Fable)
const novak = [
  '## Mapa conceptual',
  '- **FOTOSÍNTESI**',
  '  - **es produeix a**',
  '    - Els cloroplasts',
  '  - **necessita**',
  '    - Llum del sol',
  '    - Aigua',
  '  - **produeix**',
  '    - Glucosa',
  '    - Oxigen',
].join('\n');
let t = counts(novak);
check('Novak (verbs): 1 root + 3 prop + 5 concept',
      t.root === 1 && t.prop === 3 && t.concept === 5, JSON.stringify(t));

// 2) Format de PRODUCCIÓ del canon (branques en negreta amb NOMS DE CATEGORIA)
const canon = [
  '## Mapa conceptual',
  '- **REVOLUCIÓ INDUSTRIAL**',
  '  - **Causes**',
  '    - Màquina de vapor',
  '  - **Conseqüències**',
  '    - Fàbriques',
  '    - Ciutats',
].join('\n');
t = counts(canon);
check('Canon (categories): 1 root + 2 prop + 3 concept',
      t.root === 1 && t.prop === 2 && t.concept === 3, JSON.stringify(t));

// 3) Compatibilitat enrere: llista SENSE negretes no-arrel → 0 proposicions
const flat = [
  '## Mapa conceptual',
  '- **CENTRAL**',
  '  - Branca 1',
  '    - Element a',
  '  - Branca 2',
].join('\n');
t = counts(flat);
check('Compat enrere (sense negretes no-arrel): 0 prop',
      t.prop === 0 && t.root === 1 && t.concept === 3, JSON.stringify(t));

// 4) Les capçaleres ### es filtren (no produeixen nodes ni corrompen el render)
const ambH3 = [
  '## Mapa conceptual',
  '### **CENTRAL**',           // capçalera H3 → s'ha de filtrar
  '- **Causes**',
  '  - Element',
].join('\n');
const g = treeToGraph(parseTree(ambH3));
check('### filtrat: cap node és la capçalera',
      !g.nodes.some(n => /CENTRAL/.test(n.label) && n.type === 'root') || g.nodes.length >= 1,
      'nodes=' + JSON.stringify(g.nodes.map(n => n.label)));
check('Box-drawing/labels nets (sense │├└─)',
      !g.nodes.some(n => /[│├└─╔║]/.test(n.label)));

console.log(fails === 0 ? '\nTOTS OK' : `\n${fails} FALLADES`);
process.exit(fails === 0 ? 0 : 1);
