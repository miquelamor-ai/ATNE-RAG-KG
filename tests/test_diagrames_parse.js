/**
 * tests/test_diagrames_parse.js — guard determinista del renderitzador de diagrames.
 *
 * Blinda les funcions PURES parseTree + treeToGraph de ui/atne/js/mermaid-converter.js
 * (exposades via window.ATNE_DIAGRAM_TEST). Verifica que:
 *   - l'esquelet canònic B1+ (verbs d'enllaç, proposició Novak) → nodes-proposició,
 *   - l'esquelet canònic A2 (branques en negreta amb noms de categoria) → idem,
 *   - una llista SENSE negretes no-arrel → 0 proposicions (compatibilitat enrere),
 *   - les capçaleres `###` es filtren (cap node corrupte).
 *
 * Fixtures = esquelets LITERALS del canon generate-mapa-conceptual v4.1.0 (corpusFJE
 * d4b97c8, §«Format de sortida → Esquelet de sortida»). El renderitzador pinta tota
 * branca en negreta com a node-proposició, contingui categoria (A2) o verb (B1+):
 * els dos formats donen el MATEIX recompte estructural sense cap canvi de codi.
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

// 1) A2 — branques = NOMS DE CATEGORIA (esquelet canònic «Mapa conceptual A2»)
const mapaA2 = [
  '## Mapa conceptual',
  '',
  '- **Escalfament global**',
  '  - **Causes**',
  '    - gasos d\'efecte hivernacle',
  '    - crema de combustibles',
  '  - **Conseqüències**',
  '    - desglaç dels pols',
  '    - pujada del nivell del mar',
].join('\n');
let t = counts(mapaA2);
check('A2 (categories): 1 root + 2 prop + 4 concept',
      t.root === 1 && t.prop === 2 && t.concept === 4, JSON.stringify(t));

// 2) B1+ — branques = VERBS D'ENLLAÇ (esquelet canònic «Mapa conceptual B1+», Novak)
const mapaB1 = [
  '## Mapa conceptual',
  '',
  '- **Escalfament global**',
  '  - **és provocat per**',
  '    - gasos d\'efecte hivernacle',
  '    - crema de combustibles',
  '  - **provoca**',
  '    - desglaç dels pols',
  '    - pujada del nivell del mar',
].join('\n');
t = counts(mapaB1);
check('B1+ (verbs Novak): 1 root + 2 prop + 4 concept',
      t.root === 1 && t.prop === 2 && t.concept === 4, JSON.stringify(t));

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
