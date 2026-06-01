/**
 * build_matriu_data.js — genera ui/atne/js/complements-matriu.data.js des del
 * canon matriu_cobertura.json del submodule corpusFJE.
 *
 * Per què incrustat (build-time) i no fetch: complements-matriu.js s'usa
 * SÍNCRONAMENT al browser (defaultComplementsForProfile es crida en 6 punts de
 * pas2.html sense await). Un fetch asíncron introduiria risc de timing. Incrustar
 * el JSON dins un .data.js carregat via <script src> abans del mòdul garanteix
 * que les dades hi són sempre, sense lògica de càrrega.
 *
 * Font única preservada: el .data.js és DERIVAT del canon (no s'edita a mà). Quan
 * mineriaRAG actualitzi el M2/JSON i fem bump del submodule, cal RE-EXECUTAR
 * aquest script:  node scripts/build_matriu_data.js
 *
 * El propi complements-matriu.js verifica la coherència en càrrega (version) i el
 * test test_complements_matriu.js valida byte-a-byte contra el golden snapshot.
 */
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SRC = path.join(ROOT, 'corpus', 'external', 'corpusFJE', '.tooling', 'matriu_cobertura.json');
const OUT = path.join(ROOT, 'ui', 'atne', 'js', 'complements-matriu.data.js');

const raw = fs.readFileSync(SRC, 'utf8');
const data = JSON.parse(raw); // valida que és JSON correcte

const banner =
`/**
 * complements-matriu.data.js — AUTO-GENERAT. NO EDITAR A MÀ.
 *
 * Derivat de: corpus/external/corpusFJE/.tooling/matriu_cobertura.json
 * (canon M2_instruments-mediacio-pedagogica.md, build ${data._meta ? data._meta.build_tag : '?'}).
 * Regenera amb:  node scripts/build_matriu_data.js  (després de bumpejar el submodule).
 *
 * El consumidor és complements-matriu.js. Aquest fitxer NOMÉS exposa les dades
 * canon; tota la lògica (algoritme R1..A5) viu al consumidor.
 */
(function (root) {
  'use strict';
  var MATRIU_COBERTURA = `;

const body = JSON.stringify(data, null, 2);

const footer = `;
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = MATRIU_COBERTURA;
  } else {
    root.MATRIU_COBERTURA = MATRIU_COBERTURA;
  }
})(typeof window !== 'undefined' ? window : globalThis);
`;

fs.writeFileSync(OUT, banner + body + footer + '\n', 'utf8');
console.log('✓ generat', path.relative(ROOT, OUT), '(version ' + data.version + ')');
