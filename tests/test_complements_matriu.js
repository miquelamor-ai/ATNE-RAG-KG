/**
 * tests/test_complements_matriu.js — test Node determinista de la matriu
 * d'auto-suggestió de complements al Pas 2 (ui/atne/js/complements-matriu.js).
 *
 * Des de R0 (2026-06-01) la matriu és CANON: complements-matriu.js consumeix
 * matriu_cobertura.json del submodule corpusFJE via complements-matriu.data.js
 * (derivat incrustat, generat per scripts/build_matriu_data.js). Aquest test cobreix:
 *   - GUARD anti-drift: .data.js ↔ matriu_cobertura.json del submodule (deep-equal).
 *   - Lleis R1/R2/R3 + fallback R4/A5 (cas titella i companyia).
 *   - GOLDEN SNAPSHOT: 711 combinacions byte-a-byte (contracte de no-regressió).
 *
 * Execució:
 *   node tests/test_complements_matriu.js
 *
 * ⚠️ DESPRÉS DE BUMPEJAR EL SUBMODULE corpusFJE, regenera el derivat i verifica:
 *   node scripts/build_matriu_data.js && node tests/test_complements_matriu.js
 * Si el test surt KO amb "DRIFT", és que falta el primer pas (regenerar el .data.js).
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

// ─────────────────────────────────────────────────────────────────────────
// GUARD D'EQUIVALÈNCIA DERIVAT ↔ CANON (matís demanat per mineriaRAG, R0).
//
// complements-matriu.data.js és un DERIVAT de matriu_cobertura.json del submodule
// (generat per scripts/build_matriu_data.js). Aquest test FALLA si algú bumpeja
// el submodule sense regenerar el .data.js → detecta drift silenciós, que és
// exactament el que la canonització R0 vol eliminar. El golden snapshot detecta
// canvis de COMPORTAMENT; aquest detecta FRESCOR del derivat respecte al canon.
// ─────────────────────────────────────────────────────────────────────────
console.log('=== GUARD equivalència .data.js ↔ matriu_cobertura.json (canon submodule) ===');
(function checkEmbeddedFreshness() {
  let embedded, canon;
  try {
    embedded = require('../ui/atne/js/complements-matriu.data.js');
    canon = require('../corpus/external/corpusFJE/.tooling/matriu_cobertura.json');
  } catch (e) {
    nFail++;
    failures.push('No s\'ha pogut carregar .data.js o el canon del submodule: ' + e.message);
    console.log('  ✗ càrrega fallida: ' + e.message);
    return;
  }
  // Comparació canònica: mateixa serialització de claus ordenades (deep-equal robust).
  function canonicalize(o) {
    if (Array.isArray(o)) return o.map(canonicalize);
    if (o && typeof o === 'object') {
      return Object.keys(o).sort().reduce(function (acc, k) { acc[k] = canonicalize(o[k]); return acc; }, {});
    }
    return o;
  }
  const a = JSON.stringify(canonicalize(embedded));
  const b = JSON.stringify(canonicalize(canon));
  if (a === b) {
    nPass++;
    console.log('  ✓ .data.js coincideix amb el canon del submodule (version ' + canon.version + ')');
  } else {
    nFail++;
    failures.push(
      'DRIFT: complements-matriu.data.js NO coincideix amb matriu_cobertura.json del submodule.\n' +
      '    → Regenera amb:  node scripts/build_matriu_data.js\n' +
      '    (probablement s\'ha bumpejat el submodule sense regenerar el derivat).'
    );
    console.log('  ✗ DRIFT detectat — regenera amb: node scripts/build_matriu_data.js');
  }
})();

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

// ─────────────────────────────────────────────────────────────────────────
// GOLDEN SNAPSHOT — contracte anti-regressió per al refactor R0 (matriu canon).
//
// tests/golden/matriu_complements_snapshot.json captura la sortida actual de
// defaultComplementsForProfile per a 711 combinacions (13 condicions × 9 MECR ×
// 5 cursos + fallbacks NONE/NOUV_L1 + 4 parelles). Quan mineriaRAG publiqui
// matriu_cobertura.json i fem R0 (consum del JSON canon), aquest bloc ha de
// seguir verd SENSE tocar el snapshot: garanteix que el refactor reprodueix el
// comportament byte-a-byte. Si el snapshot mai necessita actualització
// intencionada, regenera'l amb el mateix algoritme i revisa el diff.
// ─────────────────────────────────────────────────────────────────────────
console.log('\n=== GOLDEN SNAPSHOT (711 combinacions · contracte R0) ===');
(function checkSnapshot() {
  let snap;
  try {
    snap = require('./golden/matriu_complements_snapshot.json');
  } catch (e) {
    console.log('  ⚠️  snapshot no trobat — saltant (genera amb el workflow R0)');
    return;
  }
  const mecrs = ['pre-A1', 'A1', 'A2', 'B1', 'B2', 'C1', 'C2', '', undefined];
  const cursos = ['1r Primària', '2n Primària', '3r Primària', '3r ESO', ''];
  const conds = Object.keys(M.MATRIU_CONDICIONS);
  let mismatches = 0, checked = 0;
  function cmp(key, actual) {
    checked++;
    const exp = JSON.stringify(snap[key]);
    const act = JSON.stringify(actual);
    if (exp !== act) {
      mismatches++;
      if (mismatches <= 10) {
        console.log(`  ✗ ${key}\n    snapshot: ${exp}\n    actual:   ${act}`);
      }
    }
  }
  conds.forEach(function (c) {
    mecrs.forEach(function (me) {
      cursos.forEach(function (cu) {
        cmp(c + '|' + (me === undefined ? 'undef' : me) + '|' + cu,
            M.defaultComplementsForProfile({ cat: c, curs: cu }, me));
      });
    });
  });
  mecrs.forEach(function (me) {
    cursos.forEach(function (cu) {
      cmp('NONE|' + (me === undefined ? 'undef' : me) + '|' + cu,
          M.defaultComplementsForProfile({ curs: cu }, me));
      cmp('NOUV_L1|' + (me === undefined ? 'undef' : me) + '|' + cu,
          M.defaultComplementsForProfile({ curs: cu, conditions: [{ key: 'nouvingut', l1: 'arab' }] }, me));
    });
  });
  [['disl', 'cat'], ['disl', 'tdl'], ['tea', 'ac'], ['tdah', 'disl']].forEach(function (pair) {
    mecrs.forEach(function (me) {
      cmp(pair.join('+') + '|' + (me === undefined ? 'undef' : me) + '|',
          M.defaultComplementsForProfile({ chips: pair.map(function (x) { return { cat: x }; }) }, me));
    });
  });
  if (mismatches === 0) {
    nPass++;
    console.log(`  ✓ ${checked} combinacions coincideixen amb el snapshot`);
  } else {
    nFail++;
    failures.push(`GOLDEN SNAPSHOT: ${mismatches}/${checked} desviacions del comportament canon R0`);
    console.log(`  ✗ ${mismatches}/${checked} desviacions (només 10 primeres mostrades)`);
  }
})();

console.log('\n' + '='.repeat(60));
console.log(`RESULTAT: ${nPass} OK · ${nFail} KO`);
console.log('='.repeat(60));
if (nFail > 0) {
  console.log('\nFALLADES:\n' + failures.join('\n'));
  process.exit(1);
}
