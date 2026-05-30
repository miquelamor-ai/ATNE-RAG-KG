/**
 * tests/test_complements_matriu.js — test Node determinista de la matriu
 * d'auto-suggestió de complements al Pas 2 (ui/atne/js/complements-matriu.js).
 *
 * Validem la modulació MECR/low afegida 2026-05-30 (cas titella):
 *   R1: pictogrames per a perfils visuals a nivell baix.
 *   R2: mapa_conceptual i mapa_mental fora a nivell baix.
 *   R3: glossari fora per dislèxia (sense nouvingut ni TDL) a nivell baix.
 *
 * Cap regressió de la matriu base per a perfils estàndards (B1+, AACC).
 *
 * Execució:
 *   node tests/test_complements_matriu.js
 */
const M = require('../ui/atne/js/complements-matriu.js');

let nPass = 0, nFail = 0;
const failures = [];

function eq(actual, expected, label) {
  const a = JSON.stringify((actual || []).slice().sort());
  const e = JSON.stringify((expected || []).slice().sort());
  if (a === e) {
    nPass++;
    console.log(`  ✓ ${label}`);
  } else {
    nFail++;
    failures.push(`${label}\n    expected: ${e}\n    actual:   ${a}`);
    console.log(`  ✗ ${label}\n    expected: ${e}\n    actual:   ${a}`);
  }
}

function profile(cat) {
  // Perfil mínim amb una sola condició via .cat (forma legacy suportada per has()).
  return { cat: cat, chips: [] };
}

console.log('=== Cas titella (1r primària · dislèxia · A1) — la raó del fix ===');
eq(
  M.defaultComplementsForProfile(profile('disl'), 'A1'),
  ['bastides', 'esquema_visual', 'pictogrames'],
  'disl @ A1 → pictogrames+bastides+esquema (sense glossari textual)'
);

console.log('\n=== Regressió: matriu base estàndard (B1+/AC) ===');
eq(
  M.defaultComplementsForProfile(profile('disl'), 'B1'),
  ['bastides', 'esquema_visual', 'glossari'],
  'disl @ B1 → matriu base intacta (glossari + esquema + bastides)'
);
eq(
  M.defaultComplementsForProfile(profile('tdah'), 'B1'),
  ['glossari', 'esquema_visual', 'preguntes_comprensio'],
  'tdah @ B1 → matriu base'
);
eq(
  M.defaultComplementsForProfile(profile('ac'), 'B2'),
  ['activitats_aprofundiment', 'mapa_mental', 'rubriques'],
  'ac @ B2 → matriu base (enriquiment, no simplificar)'
);

console.log('\n=== R1: pictogrames afegits a perfils visuals @ low ===');
eq(
  M.defaultComplementsForProfile(profile('tdl'), 'A1'),
  ['bastides', 'esquema_visual', 'glossari', 'pictogrames'],
  'tdl @ A1 → afegim pictogrames (glossari es queda — TDL té gap lèxic)'
);
eq(
  M.defaultComplementsForProfile(profile('cat'), 'pre-A1'),
  ['bastides', 'glossari', 'pictogrames'],
  'cat (nouvingut) @ pre-A1 → glossari bilingüe + pictogrames (com matriu base)'
);
eq(
  M.defaultComplementsForProfile(profile('di'), 'A1'),
  ['bastides', 'esquema_visual', 'pictogrames'],
  'di @ A1 → matriu base ja inclou pictogrames; sense glossari (no rebla R3)'
);

console.log('\n=== R2: mapes abstractes fora a low ===');
// Forcem un perfil ac (que té mapa_mental a la matriu) i li donem MECR low artificial
// per verificar que mapa_mental es treu (cas teòric — un ac amb A1 seria estrany,
// però la regla ha d'aplicar).
eq(
  M.defaultComplementsForProfile(profile('ac'), 'A1'),
  ['activitats_aprofundiment', 'rubriques'],
  'ac @ A1 (hipotètic) → mapa_mental fora per low; activitats+rúbriques queden'
);

console.log('\n=== R3: dislèxia (sense nouvingut/TDL) trau glossari a low ===');
eq(
  M.defaultComplementsForProfile(profile('disl'), 'pre-A1'),
  ['bastides', 'esquema_visual', 'pictogrames'],
  'disl @ pre-A1 → sense glossari, amb pictogrames'
);
// Perfil amb disl + cat (nouvingut): glossari es manté (R3 no aplica).
eq(
  M.defaultComplementsForProfile({ cat: 'disl', chips: [{ cat: 'cat' }] }, 'A1'),
  ['bastides', 'esquema_visual', 'glossari', 'pictogrames'],
  'disl + cat @ A1 → glossari es queda (bilingüe per L2)'
);
// disl + tdl: glossari es manté també.
eq(
  M.defaultComplementsForProfile({ cat: 'disl', chips: [{ cat: 'tdl' }] }, 'A1'),
  ['bastides', 'esquema_visual', 'glossari', 'pictogrames'],
  'disl + tdl @ A1 → glossari es queda (TDL té gap lèxic)'
);

console.log('\n=== Banda mid/high: no modulació ===');
eq(
  M.defaultComplementsForProfile(profile('disl'), 'A2'),
  ['bastides', 'esquema_visual', 'glossari'],
  'disl @ A2 → matriu base (no afecten regles low)'
);
eq(
  M.defaultComplementsForProfile(profile('disl'), 'B2'),
  ['bastides', 'esquema_visual', 'glossari'],
  'disl @ B2 → matriu base'
);

console.log('\n=== mecrBand sanity ===');
const cases = [
  ['pre-A1', 'low'], ['PRE-A1', 'low'], ['A1', 'low'],
  ['A2', 'mid'], ['B1', 'mid'],
  ['B2', 'high'], ['C1', 'high'], ['C2', 'high'],
  ['', 'high'], [null, 'high'], [undefined, 'high'],
];
cases.forEach(([input, expected]) => {
  const actual = M.mecrBand(input);
  const label = `mecrBand(${JSON.stringify(input)}) === '${expected}'`;
  if (actual === expected) { nPass++; console.log(`  ✓ ${label}`); }
  else { nFail++; failures.push(`${label} got ${actual}`); console.log(`  ✗ ${label} got ${actual}`); }
});

console.log('\n' + '='.repeat(60));
console.log(`RESULTAT: ${nPass} OK · ${nFail} KO`);
console.log('='.repeat(60));
if (nFail > 0) {
  console.log('\nFALLADES:\n' + failures.join('\n'));
  process.exit(1);
}
