/**
 * tests/test_mapa_profunditat_drift.js — guard de drift del derivat de modulació
 * per MECR de l'editor de diagrames (bloc B4): profunditat + amplada + densitat.
 *
 * Verifica que ui/atne/js/diagram-mecr-depth.data.js segueix sent el derivat FIDEL
 * del canon rubrica.json (generate-mapa-conceptual). Si algú bumpeja el submodule
 * corpusFJE i canvia un límit SENSE regenerar el .data.js, aquest test falla amb
 * DRIFT i recorda el flux de regeneració.
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

const { extractAll } = require('../scripts/build_mapa_profunditat_data.js');

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
const fresh = extractAll(rubrica);

['levels', 'branques_max', 'subelements_max', 'densitat_max'].forEach((mapName) => {
  const a = JSON.stringify(committed[mapName]);
  const b = JSON.stringify(fresh[mapName]);
  check('cap drift «' + mapName + '» .data.js ↔ canon', a === b,
    '\n      committed: ' + a + '\n      canon:     ' + b +
    '\n      → regenera amb: node scripts/build_mapa_profunditat_data.js');
});

// Sanity pedagògic: la gradació creix amb el MECR (profunditat i amplada).
check('gradació profunditat A2 < B1', fresh.levels.A2 < fresh.levels.B1,
  'A2=' + fresh.levels.A2 + ' B1=' + fresh.levels.B1);
check('gradació branques A2 ≤ B1 ≤ B2',
  fresh.branques_max.A2 <= fresh.branques_max.B1 && fresh.branques_max.B1 <= fresh.branques_max.B2,
  JSON.stringify(fresh.branques_max));

console.log(fails === 0 ? '\nTOTS OK' : `\n${fails} FALLADES`);
process.exit(fails === 0 ? 0 : 1);
