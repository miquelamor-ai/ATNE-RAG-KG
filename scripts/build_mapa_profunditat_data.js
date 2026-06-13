/**
 * build_mapa_profunditat_data.js — genera ui/atne/js/diagram-mecr-depth.data.js
 * des del canon rubrica.json de generate-mapa-conceptual (submodule corpusFJE).
 *
 * Bloc B4 de l'editor de diagrames: el botó "+ proposició" de l'editor Novak
 * gradua la profunditat per MECR. El LÍMIT ve del canon, NO es hardcoda al codi.
 *
 * Font canònica de la profunditat: rubrica.json → levels[*].passos →
 * `pas_5_estructura_markdown` → descriptor (p. ex. "2 nivells de sangria").
 * N'extraiem el primer enter seguit de "nivell". Si el descriptor no parla de
 * nivells (pre-A1 = llista plana; C1+ = mapa de contrast en columnes) → null.
 *
 * El consumidor (diagram-editor-ui.js) aplica el límit TAL QUAL del canon
 * (A2=2, B1=3, B2=4); només tracta `null` com a "sense límit" (nivells no
 * comptables: pre-A1 esquema pla, C1+ contrast). Cap regla pedagògica al codi.
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
const OUT = path.join(ROOT, 'ui', 'atne', 'js', 'diagram-mecr-depth.data.js');

// Extreu, per a cada nivell MECR, els nivells de sangria que el canon declara al
// pas estructura_markdown. Funció PURA i compartida amb el guard de drift.
function extractDepths(rubrica) {
  const levels = {};
  const lv = rubrica.levels || {};
  Object.keys(lv).forEach((key) => {
    const passos = lv[key].passos || [];
    const pas = passos.find((p) => /estructura_markdown/.test(p.pas_id || ''));
    let n = null;
    if (pas && typeof pas.descriptor === 'string') {
      const m = pas.descriptor.match(/(\d+)\s*nivell/i);
      if (m) n = parseInt(m[1], 10);
    }
    levels[key] = n;   // enter (nivells de sangria del canon) o null (sense jerarquia comptable)
  });
  return levels;
}

module.exports = { extractDepths };

// Quan s'executa directament: regenera el fitxer derivat.
if (require.main === module) {
  const rubrica = JSON.parse(fs.readFileSync(SRC, 'utf8'));
  const meta = rubrica._meta || {};
  const out = {
    _meta: {
      source: 'skills/mediacio/generate-mapa-conceptual/rubrica.json',
      font_canonic: meta.font_canonic || null,
      font_version: meta.font_version || null,
      rubrica_version: meta.version || null,
      extret_de: 'levels[*].passos.pas_5_estructura_markdown.descriptor (regex `N nivell`)',
      nota: 'Limit tal qual del canon. El consumidor nomes tracta null com a sense limit (pre-A1/C1+).',
    },
    levels: extractDepths(rubrica),
  };

  const banner =
`/**
 * diagram-mecr-depth.data.js — AUTO-GENERAT. NO EDITAR A MÀ.
 *
 * Derivat de: corpus/external/corpusFJE/skills/mediacio/generate-mapa-conceptual/
 * rubrica.json (font ${meta.font_version || '?'}). Profunditat (nivells de sangria)
 * per MECR, extreta del pas estructura_markdown del canon.
 * Regenera amb:  node scripts/build_mapa_profunditat_data.js  (post-bump submodule).
 *
 * Consumidor: ui/atne/js/diagram-editor-ui.js (bloc B4 — gate "+ proposició").
 * Aquest fitxer NOMÉS exposa els números del canon; la política (B2+ lliure) viu
 * al consumidor. Guard de drift: tests/test_mapa_profunditat_drift.js.
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
  console.log('✓ generat', path.relative(ROOT, OUT),
    '— levels:', JSON.stringify(out.levels));
}
