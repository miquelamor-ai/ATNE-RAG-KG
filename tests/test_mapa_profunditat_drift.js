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
const SRC_ESQUEMA = path.join(ROOT, 'corpus', 'external', 'corpusFJE', 'skills',
  'mediacio', 'generate-esquema-visual', 'rubrica.json');
const SRC_MAPA_MENTAL = path.join(ROOT, 'corpus', 'external', 'corpusFJE', 'skills',
  'mediacio', 'generate-mapa-mental', 'rubrica.json');
const DATA = path.join(ROOT, 'ui', 'atne', 'js', 'diagram-mecr-depth.data.js');

const { extractAll, extractEsquema, extractMapaMental } = require('../scripts/build_mapa_profunditat_data.js');

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

['levels', 'branques_max', 'subelements_max', 'densitat_max', 'cross_max'].forEach((mapName) => {
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

// ── ESQUEMA VISUAL: mateix guard sobre la clau `esquema` del derivat ──
// (canon propi, estructura de passos diferent: profunditat + densitat). Si el
// submodule es bumpeja i canvia un límit sense regenerar, aquest test ho atrapa.
if (!fs.existsSync(SRC_ESQUEMA)) {
  console.error('ERROR: canon esquema absent (' + path.relative(ROOT, SRC_ESQUEMA) + ') — cal el submodule corpusFJE.');
  process.exit(2);
}
const rubricaE = JSON.parse(fs.readFileSync(SRC_ESQUEMA, 'utf8'));
const freshE = extractEsquema(rubricaE);
check('derivat conté la clau «esquema»', !!committed.esquema,
  'committed.esquema = ' + JSON.stringify(committed.esquema));
if (committed.esquema) {
  ['levels', 'densitat_max'].forEach((mapName) => {
    const a = JSON.stringify(committed.esquema[mapName]);
    const b = JSON.stringify(freshE[mapName]);
    check('cap drift esquema «' + mapName + '» .data.js ↔ canon', a === b,
      '\n      committed: ' + a + '\n      canon:     ' + b +
      '\n      → regenera amb: node scripts/build_mapa_profunditat_data.js');
  });
}
// Sanity pedagògic esquema: profunditat i densitat creixen amb el MECR.
check('esquema gradació profunditat A2 ≤ B1 ≤ C1+',
  freshE.levels.A2 <= freshE.levels.B1 && freshE.levels.B1 <= freshE.levels['C1+'],
  JSON.stringify(freshE.levels));
check('esquema gradació densitat A2 < B1 < B2',
  freshE.densitat_max.A2 < freshE.densitat_max.B1 && freshE.densitat_max.B1 < freshE.densitat_max.B2,
  JSON.stringify(freshE.densitat_max));

// ── MAPA MENTAL: guard sobre la clau `mapa_mental` (canon propi: profunditat +
// branques + densitat; sense subelements, com l'esquema) ──
if (!fs.existsSync(SRC_MAPA_MENTAL)) {
  console.error('ERROR: canon mapa mental absent (' + path.relative(ROOT, SRC_MAPA_MENTAL) + ') — cal el submodule corpusFJE.');
  process.exit(2);
}
const rubricaM = JSON.parse(fs.readFileSync(SRC_MAPA_MENTAL, 'utf8'));
const freshM = extractMapaMental(rubricaM);
check('derivat conté la clau «mapa_mental»', !!committed.mapa_mental,
  'committed.mapa_mental = ' + JSON.stringify(committed.mapa_mental));
if (committed.mapa_mental) {
  ['levels', 'branques_max', 'densitat_max'].forEach((mapName) => {
    const a = JSON.stringify(committed.mapa_mental[mapName]);
    const b = JSON.stringify(freshM[mapName]);
    check('cap drift mapa_mental «' + mapName + '» .data.js ↔ canon', a === b,
      '\n      committed: ' + a + '\n      canon:     ' + b +
      '\n      → regenera amb: node scripts/build_mapa_profunditat_data.js');
  });
}
// Sanity pedagògic mapa mental: branques i densitat creixen amb el MECR.
check('mapa_mental gradació branques A2 ≤ B1 ≤ B2',
  freshM.branques_max.A2 <= freshM.branques_max.B1 && freshM.branques_max.B1 <= freshM.branques_max.B2,
  JSON.stringify(freshM.branques_max));
check('mapa_mental gradació densitat A2 < B1 < B2',
  freshM.densitat_max.A2 < freshM.densitat_max.B1 && freshM.densitat_max.B1 < freshM.densitat_max.B2,
  JSON.stringify(freshM.densitat_max));

console.log(fails === 0 ? '\nTOTS OK' : `\n${fails} FALLADES`);
process.exit(fails === 0 ? 0 : 1);
