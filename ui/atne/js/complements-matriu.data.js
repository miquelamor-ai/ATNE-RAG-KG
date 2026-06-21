/**
 * complements-matriu.data.js — AUTO-GENERAT. NO EDITAR A MÀ.
 *
 * Derivat de: corpus/external/corpusFJE/.tooling/matriu_cobertura.json
 * (canon M2_instruments-mediacio-pedagogica.md, build build_matriu_cobertura.py@v1.0-2026-06-01).
 * Regenera amb:  node scripts/build_matriu_data.js  (després de bumpejar el submodule).
 *
 * El consumidor és complements-matriu.js. Aquest fitxer NOMÉS exposa les dades
 * canon; tota la lògica (algoritme R1..A5) viu al consumidor.
 */
(function (root) {
  'use strict';
  var MATRIU_COBERTURA = {
  "version": "1.0",
  "_meta": {
    "source": "M2_instruments-mediacio-pedagogica.md#matriu-de-cobertura-perfil--complement",
    "generat_at": "2026-06-21",
    "build_tag": "build_matriu_cobertura.py@v1.0-2026-06-01",
    "validacio_pedagogica": "NotebookLM MALL FJE 2026-05-27 (Opció D)"
  },
  "complement_keys": [
    "glossari",
    "esquema_visual",
    "bastides",
    "mapa_conceptual",
    "preguntes_comprensio",
    "activitats_aprofundiment",
    "pictogrames",
    "mapa_mental",
    "plantilles_genere",
    "resum_graduat",
    "cartes_conversacionals",
    "rubriques"
  ],
  "base": {
    "tea": [
      "esquema_visual",
      "bastides",
      "pictogrames"
    ],
    "tdah": [
      "glossari",
      "esquema_visual",
      "preguntes_comprensio"
    ],
    "disl": [
      "glossari",
      "esquema_visual",
      "bastides"
    ],
    "di": [
      "esquema_visual",
      "bastides",
      "pictogrames"
    ],
    "tdl": [
      "glossari",
      "esquema_visual",
      "bastides"
    ],
    "ac": [
      "activitats_aprofundiment",
      "mapa_mental",
      "rubriques"
    ],
    "aud": [
      "glossari",
      "preguntes_comprensio",
      "pictogrames"
    ],
    "vis": [
      "glossari",
      "preguntes_comprensio"
    ],
    "tdc": [
      "glossari",
      "preguntes_comprensio"
    ],
    "cat": [
      "glossari",
      "bastides",
      "pictogrames"
    ],
    "vuln": [
      "glossari",
      "esquema_visual",
      "preguntes_comprensio"
    ],
    "emo": [
      "glossari",
      "preguntes_comprensio"
    ],
    "discalculia": [
      "glossari",
      "esquema_visual",
      "bastides"
    ]
  },
  "visual_need_conditions": [
    "disl",
    "di",
    "tdl",
    "cat",
    "tea",
    "vis",
    "discalculia"
  ],
  "primaria_inicial_cursos": [
    "1r Primària",
    "2n Primària"
  ],
  "rules": {
    "mecr_bands": {
      "low": [
        "pre-A1",
        "A1"
      ],
      "mid": [
        "A2",
        "B1"
      ],
      "high": [
        "B2",
        "C1",
        "C2"
      ]
    },
    "R1_add_pictos": {
      "when_band": "low",
      "if_any": "visual_need_conditions",
      "add": [
        "pictogrames"
      ]
    },
    "R2_drop_maps": {
      "when_band": "low",
      "drop": [
        "mapa_conceptual",
        "mapa_mental"
      ]
    },
    "R3_drop_glossari_disl": {
      "when_band": "low",
      "if": "disl",
      "unless": [
        "cat",
        "tdl"
      ],
      "drop": [
        "glossari"
      ]
    },
    "fallback": {
      "default": [
        "glossari",
        "preguntes_comprensio"
      ]
    },
    "R4_primaria_inicial": {
      "when_band": "low",
      "no_conditions": true,
      "cursos": "primaria_inicial_cursos",
      "only": [
        "preguntes_comprensio"
      ]
    },
    "A5_nouvingut_l1": {
      "overrides": "R4",
      "when": "nouvingut_amb_l1",
      "detection": "runtime (excepció pactada — viu al codi consumidor)",
      "result": [
        "glossari",
        "preguntes_comprensio"
      ]
    }
  },
  "algoritme": "1) Banda MECR via mecr_bands (high = fallback per a buit/desconegut). 2) Base = unió OR de rules.base per cada condició present al perfil. 3) Si banda=low I hi ha alguna condició reconeguda: aplica R1 (afegeix pictos si visual_need), R2 (treu mapes), R3 (treu glossari si disl pur). 4) Si NO hi ha cap condició reconeguda: parteix de fallback.default; si banda=low I curs ∈ primaria_inicial_cursos aplica R4 (només preguntes_comprensio), EXCEPTE si nouvingut amb L1 declarada → A5 (glossari + preguntes_comprensio). R1–R3 i R4/A5 són mútuament exclusius. Ordre de sortida = complement_keys."
};
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = MATRIU_COBERTURA;
  } else {
    root.MATRIU_COBERTURA = MATRIU_COBERTURA;
  }
})(typeof window !== 'undefined' ? window : globalThis);

