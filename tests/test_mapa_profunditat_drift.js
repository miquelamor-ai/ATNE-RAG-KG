/**
 * tests/test_mapa_profunditat_drift.js — guard de drift del derivat de profunditat
 * per MECR (bloc B4 de l'editor de diagrames).
 *
 * Verifica que ui/atne/js/diagram-mecr-depth.data.js segueix sent el derivat FIDEL
 * del canon rubrica.json (generate-mapa-conceptual). Si algú bumpeja el submodule
 * corpusFJE i canvia la profunditat per nivell SENSE regenerar el .data.js, aquest
 * test falla amb DRIFT i recorda el flux de regeneració.
 *
 * Necessita el submodule corpusFJE (canon) → corre al job `canon-guards` del CI.
 * Cap dependència; corre a node net.
 *   ÚS: node tests/test_mapa_profunditat_drift.js   (exit != 0 si hi ha drift)
 */
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SRC = path.join(ROOT, 'corpus', 'external', 'corpusFJE', 'skills',
  'mediacio', 'generate-mapa-conceptual', 'rubrica.json');
const DATA = path.join(ROOT, 'ui', 'atne', 'js', 'diagram-mecr-depth.data.js');

const { extractDepths } = require('../scripts/build_mapa_profunditat_data.js');

let fails = 0;
function check(name, cond, detail) {
  if (cond) { console.log('  OK   ' + name); }
  else { console.log('  FAIL ' + name + (detail ? ' — ' + detail : '')); fails++; }
}

if (!fs.existsSync(SRC)) {
  console.error('ERROR: canon absent (' + path.relative(ROOT, SRC) + ') — cal el submodule corpusFJE.');
  process.exit(2);
}
const rubrica = JSON.parse(fs.readFileSync(SRC, 'utf8'));
const committed = require(DATA);   // el .data.js fa module.exports = ATNE_MAPA_PROFUNDITAT
const fresh = extractDepths(rubrica);

check('el .data.js exposa levels', committed && committed.levels && typeof committed.levels === 'object',
  JSON.stringify(committed && committed.levels));

const a = JSON.stringify(committed.levels);
const b = JSON.stringify(fresh);
check('cap drift profunditat .data.js ↔ canon rubrica.json', a === b,
  '\n      committed: ' + a + '\n      canon:     ' + b +
  '\n      → regenera amb: node scripts/build_mapa_profunditat_data.js');

// Sanity pedagògic: el canon ha de graduar A2 < B1 (la profunditat creix amb el MECR).
check('gradació A2 < B1 al canon', fresh['A2'] != null && fresh['B1'] != null && fresh['A2'] < fresh['B1'],
  'A2=' + fresh['A2'] + ' B1=' + fresh['B1']);

console.log(fails === 0 ? '\nTOTS OK' : `\n${fails} FALLADES`);
process.exit(fails === 0 ? 0 : 1);
