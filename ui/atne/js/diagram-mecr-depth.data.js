/**
 * diagram-mecr-depth.data.js — AUTO-GENERAT. NO EDITAR A MÀ.
 *
 * Derivat de: corpus/external/corpusFJE/skills/mediacio/generate-mapa-conceptual/
 * rubrica.json (font 4.2.0-canonic). Modulació de l'editor Novak per
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
    "font_version": "4.2.0-canonic",
    "rubrica_version": "1.0.1",
    "extret_de": {
      "levels": "pas_5_estructura_markdown.descriptor (regex `N nivell`)",
      "branques_max": "pas_3_relacio_de_branca.countable.max",
      "subelements_max": "pas_4_detalls_de_les.descriptor (regex `N-M sub-element` / \"Cap\")",
      "densitat_max": "heuristiques_docent H6.descripcio (regex `MECR ≤ N`)",
      "cross_max": "pas_6_nombre_recomanat.countable.max (enllacos creuats; avis no bloqueig)"
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
  },
  "cross_max": {
    "pre-A1": 0,
    "A1": 0,
    "A2": 0,
    "B1": 1,
    "B2": 2,
    "C1+": 3
  },
  "esquema": {
    "_meta": {
      "source": "skills/mediacio/generate-esquema-visual/rubrica.json",
      "font_canonic": "skills/mediacio/generate-esquema-visual/M3_instrument-generar-esquema-visual.md",
      "font_version": "1.0.0-canonic",
      "rubrica_version": "1.0.1",
      "extret_de": {
        "levels": "pas_2_profunditat_de_l.descriptor (regex `N nivell` / `N-M nivells`)",
        "densitat_max": "pas_2_total_nodes.countable.max"
      },
      "nota": "Esquema: nomes profunditat + densitat (no branques/subelements). null = sense limit."
    },
    "levels": {
      "pre-A1": 1,
      "A1": 2,
      "A2": 2,
      "B1": 3,
      "B2": 3,
      "C1+": 4
    },
    "densitat_max": {
      "pre-A1": 3,
      "A1": 4,
      "A2": 6,
      "B1": 8,
      "B2": 12,
      "C1+": 15
    }
  },
  "mapa_mental": {
    "_meta": {
      "source": "skills/mediacio/generate-mapa-mental/rubrica.json",
      "font_canonic": "skills/mediacio/generate-mapa-mental/M3_instrument-generar-mapa-mental.md",
      "font_version": "1.1.0-canonic",
      "rubrica_version": "1.0.1",
      "extret_de": {
        "levels": "pas_3_nivells_d_expansio.descriptor (regex `N nivell` / `N-M nivells`)",
        "branques_max": "pas_2_nombre_de_branques.countable.max",
        "densitat_max": "heuristiques_docent H5.descripcio (regex `MECR ≤ N`)"
      },
      "nota": "Mapa mental: profunditat + branques + densitat (no subelements). null = sense limit."
    },
    "levels": {
      "pre-A1": 1,
      "A1": 1,
      "A2": 2,
      "B1": 2,
      "B2": 3,
      "C1+": 3
    },
    "branques_max": {
      "pre-A1": 2,
      "A1": 3,
      "A2": 4,
      "B1": 5,
      "B2": 7,
      "C1+": 8
    },
    "densitat_max": {
      "pre-A1": 4,
      "A1": 6,
      "A2": 10,
      "B1": 15,
      "B2": 20,
      "C1+": 24
    }
  }
};
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = ATNE_MAPA_PROFUNDITAT;
  } else {
    root.ATNE_MAPA_PROFUNDITAT = ATNE_MAPA_PROFUNDITAT;
  }
})(typeof window !== 'undefined' ? window : globalThis);

