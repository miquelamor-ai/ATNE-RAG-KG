/**
 * diagram-mecr-depth.data.js — AUTO-GENERAT. NO EDITAR A MÀ.
 *
 * Derivat de: corpus/external/corpusFJE/skills/mediacio/generate-mapa-conceptual/
 * rubrica.json (font 4.1.1-canonic). Modulació de l'editor Novak per
 * MECR: profunditat (levels) + amplada (branques_max, subelements_max) + densitat
 * total (densitat_max). Tot extret del canon.
 * Regenera amb:  node scripts/build_mapa_profunditat_data.js  (post-bump submodule).
 *
 * Consumidor: ui/atne/js/diagram-editor-ui.js (bloc B4). Aquest fitxer NOMÉS exposa
 * els números del canon. Guard de drift: tests/test_mapa_profunditat_drift.js.
 */
(function (root) {
  'use strict';
  var ATNE_MAPA_PROFUNDITAT = {
  "_meta": {
    "source": "skills/mediacio/generate-mapa-conceptual/rubrica.json",
    "font_canonic": "skills/mediacio/generate-mapa-conceptual/M3_instrument-generar-mapa-conceptual.md",
    "font_version": "4.1.1-canonic",
    "rubrica_version": "1.0.1",
    "extret_de": {
      "levels": "pas_5_estructura_markdown.descriptor (regex `N nivell`)",
      "branques_max": "pas_3_relacio_de_branca.countable.max",
      "subelements_max": "pas_4_detalls_de_les.descriptor (regex `N-M sub-element` / \"Cap\")",
      "densitat_max": "heuristiques_docent H6.descripcio (regex `MECR ≤ N`)"
    },
    "nota": "Limits tal qual del canon. El consumidor nomes tracta null com a sense limit."
  },
  "levels": {
    "pre-A1": null,
    "A1": 1,
    "A2": 2,
    "B1": 3,
    "B2": 4,
    "C1+": null
  },
  "branques_max": {
    "pre-A1": null,
    "A1": 3,
    "A2": 4,
    "B1": 5,
    "B2": 6,
    "C1+": 6
  },
  "subelements_max": {
    "pre-A1": 0,
    "A1": 0,
    "A2": 3,
    "B1": 4,
    "B2": null,
    "C1+": null
  },
  "densitat_max": {
    "pre-A1": 3,
    "A1": 5,
    "A2": 8,
    "B1": 12,
    "B2": 15,
    "C1+": 15
  }
};
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = ATNE_MAPA_PROFUNDITAT;
  } else {
    root.ATNE_MAPA_PROFUNDITAT = ATNE_MAPA_PROFUNDITAT;
  }
})(typeof window !== 'undefined' ? window : globalThis);

