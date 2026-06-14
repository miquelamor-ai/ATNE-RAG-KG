/**
 * build_mapa_profunditat_data.js — genera ui/atne/js/diagram-mecr-depth.data.js
 * des del canon rubrica.json de generate-mapa-conceptual (submodule corpusFJE).
 *
 * Bloc B4 de l'editor de diagrames: la modulació per MECR de l'editor Novak (límit
 * de profunditat I d'amplada del mapa) ve del canon, NO es hardcoda al codi.
 *
 * Quatre senyals, tots extrets del canon rubrica.json (font única):
 *   · levels          (profunditat): pas_5_estructura_markdown → "N nivells de sangria".
 *   · branques_max    (amplada):     pas_3_relacio_de_branca.countable.max (branques).
 *   · subelements_max (amplada):     pas_4_detalls_de_les → "N-M sub-elements" / "Cap".
 *   · densitat_max    (nodes totals): heuristiques_docent H6 → "MECR ≤ N nodes".
 * Quan el canon no en declara cap valor comptable per a un nivell → null.
 *
 * El consumidor (diagram-editor-ui.js) aplica els límits TAL QUAL del canon i
 * només tracta `null` com a "sense límit". Cap regla pedagògica al codi: si es
 * vol canviar un límit, es canvia al canon (mineriaRAG) i ATNE el consumeix.
 *
 * Sortida DETERMINISTA (provinença des del _meta del canon, sense data del
 * sistema) perquè el guard de drift sigui estable.
 *
 * ┌─────────────────────────────────────────────────────────────────────────┐
 * │ FLUX després de bumpejar el submodule corpusFJE:                         │
 * │   node scripts/build_mapa_profunditat_data.js \                          │
 * │     && node tests/test_mapa_profunditat_drift.js                         │
 * │ El 1r regenera el derivat; el 2n verifica que no hi ha drift amb el canon.│
 * └─────────────────────────────────────────────────────────────────────────┘
 */
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SRC = path.join(ROOT, 'corpus', 'external', 'corpusFJE', 'skills',
  'mediacio', 'generate-mapa-conceptual', 'rubrica.json');
// Esquema visual: canon PROPI amb estructura de passos DIFERENT del mapa
// conceptual (profunditat a pas_2_profunditat_de_l, densitat a pas_2_total_nodes;
// no té relacio_de_branca/detalls_de_les). Derivat sota la clau `esquema`.
const SRC_ESQUEMA = path.join(ROOT, 'corpus', 'external', 'corpusFJE', 'skills',
  'mediacio', 'generate-esquema-visual', 'rubrica.json');
// Mapa mental: canon propi (canonitzat per mineriaRAG, font ≥ 1.1.0). Estructura
// pròpia: profunditat a pas_3_nivells_d_expansio, branques a pas_2_nombre_de_branques,
// densitat (nodes totals) a la heurística H5. Derivat sota la clau `mapa_mental`.
const SRC_MAPA_MENTAL = path.join(ROOT, 'corpus', 'external', 'corpusFJE', 'skills',
  'mediacio', 'generate-mapa-mental', 'rubrica.json');
const OUT = path.join(ROOT, 'ui', 'atne', 'js', 'diagram-mecr-depth.data.js');

// ── Helpers ──
function mapLevels(rubrica, fn) {
  const out = {}, lv = rubrica.levels || {};
  Object.keys(lv).forEach((key) => { out[key] = fn(lv[key].passos || [], key); });
  return out;
}
function emptyLevels(rubrica) {
  const out = {}; Object.keys(rubrica.levels || {}).forEach((k) => { out[k] = null; }); return out;
}
function findPas(passos, idFrag) { return passos.find((p) => new RegExp(idFrag).test(p.pas_id || '')); }

// ── Extractors PURS del canon (compartits amb el guard de drift) ──

// Profunditat: nivells de sangria (pas_5_estructura_markdown → "N nivells").
function extractDepths(rubrica) {
  return mapLevels(rubrica, (passos) => {
    const pas = findPas(passos, 'estructura_markdown');
    if (pas && typeof pas.descriptor === 'string') {
      const m = pas.descriptor.match(/(\d+)\s*nivell/i);
      if (m) return parseInt(m[1], 10);
    }
    return null;
  });
}

// Amplada — branques principals (pas_3_relacio_de_branca.countable.max).
function extractBranques(rubrica) {
  return mapLevels(rubrica, (passos) => {
    const pas = findPas(passos, 'relacio_de_branca');
    if (pas && pas.countable && typeof pas.countable.max === 'number') return pas.countable.max;
    return null;
  });
}

// Amplada — sub-elements per branca (pas_4_detalls_de_les, descriptor en prosa).
function extractSubelements(rubrica) {
  return mapLevels(rubrica, (passos) => {
    const pas = findPas(passos, 'detalls_de_les');
    if (!pas || typeof pas.descriptor !== 'string') return null;
    if (/cap sub-?element/i.test(pas.descriptor)) return 0;
    const m = pas.descriptor.match(/(\d+)\s*[-–]\s*(\d+)\s*sub-?element/i);
    if (m) return parseInt(m[2], 10);
    const m1 = pas.descriptor.match(/(\d+)\s*sub-?element/i);
    if (m1) return parseInt(m1[1], 10);
    return null;
  });
}

// Densitat — nodes totals per MECR, des d'una heurística docent en prosa amb "≤".
// Per defecte H6 (mapa conceptual); el mapa mental usa H5 (mateix patró "MECR ≤ N").
function extractDensitat(rubrica, hid) {
  hid = hid || 'H6';
  const out = emptyLevels(rubrica);
  const h = (rubrica.heuristiques_docent || []).find((x) => x.id === hid);
  if (!h || typeof h.descripcio !== 'string') return out;
  const re = /([A-Za-z0-9+]+(?:-[A-Za-z0-9+]+)*)\s*≤\s*(\d+)/g;
  let m;
  while ((m = re.exec(h.descripcio))) {
    const n = parseInt(m[2], 10);
    expandLevelToken(m[1]).forEach((key) => { if (key in out) out[key] = n; });
  }
  return out;
}
// "pre-A1" → ["pre-A1"]; "B2-C1" → ["B2","C1+"]; "C1"/"C2" → "C1+".
function expandLevelToken(tok) {
  tok = tok.trim();
  if (/^pre-?A1$/i.test(tok)) return ['pre-A1'];
  return tok.split('-').map((p) => { p = p.trim(); return /^C[12]\+?$/i.test(p) ? 'C1+' : p; });
}

// Enllaços creuats — nombre recomanat per MECR (pas_6_nombre_recomanat.countable.max).
// Pas ADDITIU al canon del mapa conceptual (pas_id 1-5 intactes). Avís, no bloqueig.
function extractCrossMax(rubrica) {
  return mapLevels(rubrica, (passos) => {
    const pas = findPas(passos, 'nombre_recomanat');
    if (pas && pas.countable && typeof pas.countable.max === 'number') return pas.countable.max;
    return null;
  });
}

function extractAll(rubrica) {
  return {
    levels: extractDepths(rubrica),
    branques_max: extractBranques(rubrica),
    subelements_max: extractSubelements(rubrica),
    densitat_max: extractDensitat(rubrica),
    cross_max: extractCrossMax(rubrica),
  };
}

// ── Extractors PURS del canon ESQUEMA VISUAL (estructura de passos diferent) ──
// L'esquema NO té relacio_de_branca/detalls_de_les: l'amplada queda implícita en
// el total de nodes. Dos senyals graduats per MECR:
//   · levels       (profunditat): pas_2_profunditat_de_l, descriptor en prosa
//                  ("1 nivell", "2-3 nivells"…) → màxim del rang.
//   · densitat_max (nodes totals): pas_2_total_nodes.countable.max.

// Profunditat de l'arbre (pas_2_profunditat_de_l, prosa "N nivell(s)" / "N-M nivells").
function extractEsquemaDepths(rubrica) {
  return mapLevels(rubrica, (passos) => {
    const pas = findPas(passos, 'profunditat_de_l');
    if (!pas || typeof pas.descriptor !== 'string') return null;
    const range = pas.descriptor.match(/(\d+)\s*[-–]\s*(\d+)\s*nivell/i);
    if (range) return parseInt(range[2], 10);           // rang "N-M" → màxim
    const single = pas.descriptor.match(/(\d+)\s*nivell/i);
    if (single) return parseInt(single[1], 10);
    return null;
  });
}

// Densitat — nombre total de nodes (pas_2_total_nodes.countable.max).
function extractEsquemaDensitat(rubrica) {
  return mapLevels(rubrica, (passos) => {
    const pas = findPas(passos, 'total_nodes');
    if (pas && pas.countable && typeof pas.countable.max === 'number') return pas.countable.max;
    return null;
  });
}

function extractEsquema(rubrica) {
  return {
    levels: extractEsquemaDepths(rubrica),
    densitat_max: extractEsquemaDensitat(rubrica),
  };
}

// ── Extractors PURS del canon MAPA MENTAL (Buzan; estructura de passos pròpia) ──
// Tres senyals graduats per MECR:
//   · levels       (profunditat): pas_3_nivells_d_expansio, prosa "N nivell(s)".
//   · branques_max (amplada):     pas_2_nombre_de_branques.countable.max.
//   · densitat_max (nodes totals): heurística H5 (mateix patró "MECR ≤ N" que H6).
// (No té subelements_max comptable, com l'esquema.)
function extractMmDepths(rubrica) {
  return mapLevels(rubrica, (passos) => {
    const pas = findPas(passos, 'nivells_d_expansio');
    if (!pas || typeof pas.descriptor !== 'string') return null;
    const range = pas.descriptor.match(/(\d+)\s*[-–]\s*(\d+)\s*nivell/i);
    if (range) return parseInt(range[2], 10);           // rang "N-M" → màxim
    const single = pas.descriptor.match(/(\d+)\s*nivell/i);
    if (single) return parseInt(single[1], 10);
    return null;
  });
}
function extractMmBranques(rubrica) {
  return mapLevels(rubrica, (passos) => {
    const pas = findPas(passos, 'nombre_de_branques');
    if (pas && pas.countable && typeof pas.countable.max === 'number') return pas.countable.max;
    return null;
  });
}
function extractMapaMental(rubrica) {
  return {
    levels: extractMmDepths(rubrica),
    branques_max: extractMmBranques(rubrica),
    densitat_max: extractDensitat(rubrica, 'H5'),
  };
}

module.exports = { extractDepths, extractBranques, extractSubelements, extractDensitat, extractCrossMax,
  extractAll, extractEsquemaDepths, extractEsquemaDensitat, extractEsquema,
  extractMmDepths, extractMmBranques, extractMapaMental };

// Quan s'executa directament: regenera el fitxer derivat.
if (require.main === module) {
  const rubrica = JSON.parse(fs.readFileSync(SRC, 'utf8'));
  const meta = rubrica._meta || {};
  const out = Object.assign({
    _meta: {
      source: 'skills/mediacio/generate-mapa-conceptual/rubrica.json',
      font_canonic: meta.font_canonic || null,
      font_version: meta.font_version || null,
      rubrica_version: meta.version || null,
      extret_de: {
        levels: 'pas_5_estructura_markdown.descriptor (regex `N nivell`)',
        branques_max: 'pas_3_relacio_de_branca.countable.max',
        subelements_max: 'pas_4_detalls_de_les.descriptor (regex `N-M sub-element` / "Cap")',
        densitat_max: 'heuristiques_docent H6.descripcio (regex `MECR ≤ N`)',
        cross_max: 'pas_6_nombre_recomanat.countable.max (enllacos creuats; avis no bloqueig)',
      },
      nota: 'Limits tal qual del canon. El consumidor nomes tracta null com a sense limit.',
    },
  }, extractAll(rubrica));

  // ── Esquema visual: derivat del seu canon propi, sota la clau `esquema` ──
  // (mapa_mental NO té rubrica.json → cap clau; el consumidor el tracta sense
  //  límit fins que mineriaRAG el canonitzi. Veure docs/handoff_mineriaRAG_*.)
  if (fs.existsSync(SRC_ESQUEMA)) {
    const rubE = JSON.parse(fs.readFileSync(SRC_ESQUEMA, 'utf8'));
    const metaE = rubE._meta || {};
    out.esquema = Object.assign({
      _meta: {
        source: 'skills/mediacio/generate-esquema-visual/rubrica.json',
        font_canonic: metaE.font_canonic || null,
        font_version: metaE.font_version || null,
        rubrica_version: metaE.version || null,
        extret_de: {
          levels: 'pas_2_profunditat_de_l.descriptor (regex `N nivell` / `N-M nivells`)',
          densitat_max: 'pas_2_total_nodes.countable.max',
        },
        nota: 'Esquema: nomes profunditat + densitat (no branques/subelements). null = sense limit.',
      },
    }, extractEsquema(rubE));
  } else {
    console.warn('  ⚠ canon esquema absent (' + path.relative(ROOT, SRC_ESQUEMA) + ') — clau `esquema` omesa.');
  }

  // ── Mapa mental: derivat del seu canon propi, sota la clau `mapa_mental` ──
  if (fs.existsSync(SRC_MAPA_MENTAL)) {
    const rubM = JSON.parse(fs.readFileSync(SRC_MAPA_MENTAL, 'utf8'));
    const metaM = rubM._meta || {};
    out.mapa_mental = Object.assign({
      _meta: {
        source: 'skills/mediacio/generate-mapa-mental/rubrica.json',
        font_canonic: metaM.font_canonic || null,
        font_version: metaM.font_version || null,
        rubrica_version: metaM.version || null,
        extret_de: {
          levels: 'pas_3_nivells_d_expansio.descriptor (regex `N nivell` / `N-M nivells`)',
          branques_max: 'pas_2_nombre_de_branques.countable.max',
          densitat_max: 'heuristiques_docent H5.descripcio (regex `MECR ≤ N`)',
        },
        nota: 'Mapa mental: profunditat + branques + densitat (no subelements). null = sense limit.',
      },
    }, extractMapaMental(rubM));
  } else {
    console.warn('  ⚠ canon mapa mental absent (' + path.relative(ROOT, SRC_MAPA_MENTAL) + ') — clau `mapa_mental` omesa.');
  }

  const banner =
`/**
 * diagram-mecr-depth.data.js — AUTO-GENERAT. NO EDITAR A MÀ.
 *
 * Derivat de: corpus/external/corpusFJE/skills/mediacio/generate-mapa-conceptual/
 * rubrica.json (font ${meta.font_version || '?'}). Modulació de l'editor Novak per
 * MECR: profunditat (levels) + amplada (branques_max, subelements_max) + densitat
 * total (densitat_max). Tot extret del canon.
 * Regenera amb:  node scripts/build_mapa_profunditat_data.js  (post-bump submodule).
 *
 * Consumidor: ui/atne/js/diagram-editor-ui.js (bloc B4). Aquest fitxer NOMÉS exposa
 * els números del canon. Guard de drift: tests/test_mapa_profunditat_drift.js.
 */
(function (root) {
  'use strict';
  var ATNE_MAPA_PROFUNDITAT = `;

  const body = JSON.stringify(out, null, 2);

  const footer = `;
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = ATNE_MAPA_PROFUNDITAT;
  } else {
    root.ATNE_MAPA_PROFUNDITAT = ATNE_MAPA_PROFUNDITAT;
  }
})(typeof window !== 'undefined' ? window : globalThis);
`;

  fs.writeFileSync(OUT, banner + body + footer + '\n', 'utf8');
  console.log('✓ generat', path.relative(ROOT, OUT));
  console.log('  [mapa conceptual]');
  console.log('  levels:        ', JSON.stringify(out.levels));
  console.log('  branques_max:  ', JSON.stringify(out.branques_max));
  console.log('  subelements_max:', JSON.stringify(out.subelements_max));
  console.log('  densitat_max:  ', JSON.stringify(out.densitat_max));
  console.log('  cross_max:     ', JSON.stringify(out.cross_max));
  if (out.esquema) {
    console.log('  [esquema visual]');
    console.log('  levels:        ', JSON.stringify(out.esquema.levels));
    console.log('  densitat_max:  ', JSON.stringify(out.esquema.densitat_max));
  }
  if (out.mapa_mental) {
    console.log('  [mapa mental]');
    console.log('  levels:        ', JSON.stringify(out.mapa_mental.levels));
    console.log('  branques_max:  ', JSON.stringify(out.mapa_mental.branques_max));
    console.log('  densitat_max:  ', JSON.stringify(out.mapa_mental.densitat_max));
  }
}
