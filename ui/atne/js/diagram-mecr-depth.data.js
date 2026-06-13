/**
 * diagram-mecr-depth.data.js — AUTO-GENERAT. NO EDITAR A MÀ.
 *
 * Derivat de: corpus/external/corpusFJE/skills/mediacio/generate-mapa-conceptual/
 * rubrica.json (font 4.1.1-canonic). Profunditat (nivells de sangria)
 * per MECR, extreta del pas estructura_markdown del canon.
 * Regenera amb:  node scripts/build_mapa_profunditat_data.js  (post-bump submodule).
 *
 * Consumidor: ui/atne/js/diagram-editor-ui.js (bloc B4 — gate "+ proposició").
 * Aquest fitxer NOMÉS exposa els números del canon; la política (B2+ lliure) viu
 * al consumidor. Guard de drift: tests/test_mapa_profunditat_drift.js.
 */
(function (root) {
  'use strict';
  var ATNE_MAPA_PROFUNDITAT = {
  "_meta": {
    "source": "skills/mediacio/generate-mapa-conceptual/rubrica.json",
    "font_canonic": "skills/mediacio/generate-mapa-conceptual/M3_instrument-generar-mapa-conceptual.md",
    "font_version": "4.1.1-canonic",
    "rubrica_version": "1.0.1",
    "extret_de": "levels[*].passos.pas_5_estructura_markdown.descriptor (regex `N nivell`)",
    "nota": "Numeros del canon. La politica B2+ lliure (>=4 o null) viu al consumidor."
  },
  "levels": {
    "pre-A1": null,
    "A1": 1,
    "A2": 2,
    "B1": 3,
    "B2": 4,
    "C1+": null
  }
};
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = ATNE_MAPA_PROFUNDITAT;
  } else {
    root.ATNE_MAPA_PROFUNDITAT = ATNE_MAPA_PROFUNDITAT;
  }
})(typeof window !== 'undefined' ? window : globalThis);

