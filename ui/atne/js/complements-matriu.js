/**
 * complements-matriu.js — consumidor del canon matriu_cobertura.json
 *
 * Decideix quins complements pre-marcar al Pas 2 segons:
 *   - les condicions del perfil (matriu base condició → complements)
 *   - el nivell MECR demanat (lleis R1/R2/R3 + fallback R4/A5)
 *
 * ════════════════════════════════════════════════════════════════════════════
 * R0 (2026-06-01): la matriu i les seves lleis són CANON. Viuen a
 * corpus/external/corpusFJE/M2_instruments-mediacio-pedagogica.md i es deriven a
 * `.tooling/matriu_cobertura.json` (senyal mineriaRAG, corpusFJE 2109c91). ATNE
 * NO manté la matriu hardcoded: la llegeix del JSON via complements-matriu.data.js
 * (incrustat build-time, generat per scripts/build_matriu_data.js).
 *
 * Única excepció pactada que resta al codi: la DETECCIÓ de "nouvingut amb L1
 * declarada" (per disparar A5) depèn de l'estructura del perfil al frontend
 * (chip cat / conditions / subvariables / p.l1) → és implementació, no pedagogia.
 * L'EFECTE d'A5 (result) sí ve del canon (rules.A5_nouvingut_l1.result).
 *
 * Tota la resta de defaultComplementsForProfile és 100% derivable del JSON segons
 * el camp `algoritme` del canon.
 *
 * Es carrega des de pas2.html (via <script src>, DESPRÉS de complements-matriu.data.js)
 * i des de tests Node (via require). L'export és dual.
 * ════════════════════════════════════════════════════════════════════════════
 */
(function (root) {
  'use strict';

  // ───── Canon: dades del matriu_cobertura.json (via .data.js incrustat) ─────
  var CANON;
  if (typeof module !== 'undefined' && module.exports) {
    CANON = require('./complements-matriu.data.js');
  } else {
    CANON = root.MATRIU_COBERTURA;
  }
  if (!CANON || !CANON.base || !CANON.rules) {
    throw new Error('[complements-matriu] canon matriu_cobertura no carregat. ' +
      'Falta complements-matriu.data.js (genera amb node scripts/build_matriu_data.js).');
  }

  var RULES = CANON.rules;
  // API pública retro-compatible: MATRIU_KEYS = complement_keys del canon.
  var MATRIU_KEYS = CANON.complement_keys;
  var VISUAL_NEED_CONDITIONS = CANON.visual_need_conditions;
  var PRIMARIA_INICIAL_CURSOS = CANON.primaria_inicial_cursos;

  // MATRIU_CONDICIONS: es reconstrueix com a 12-booleans per condició a partir de
  // CANON.base (llista de claus) per preservar el contracte de l'API pública que
  // pas2.html i altres consumidors esperen (array de booleans en l'ordre MATRIU_KEYS).
  var MATRIU_CONDICIONS = {};
  Object.keys(CANON.base).forEach(function (cond) {
    var set = {};
    CANON.base[cond].forEach(function (k) { set[k] = true; });
    MATRIU_CONDICIONS[cond] = MATRIU_KEYS.map(function (k) { return !!set[k]; });
  });

  /**
   * Normalitza un MECR a la banda segons rules.mecr_bands.
   * 'high' és el fallback per a entrades buides/desconegudes (no apliquem regles
   * de baix si no sabem el nivell). Coherent amb el camp `algoritme` del canon.
   */
  function mecrBand(mecr) {
    var m = String(mecr || '').toUpperCase().replace('Ç', 'C').trim();
    var bands = RULES.mecr_bands;
    // Comparació case-insensitive contra els valors del canon (pre-A1, A1...).
    function inBand(name) {
      return (bands[name] || []).some(function (v) {
        return String(v).toUpperCase().replace('Ç', 'C').trim() === m;
      });
    }
    if (inBand('low')) return 'low';
    if (inBand('mid')) return 'mid';
    return 'high';
  }

  /**
   * Detecció EXCEPCIÓ PACTADA (no canon): "nouvingut amb L1 declarada", per
   * disparar A5. Depèn de l'estructura del perfil al frontend. L'efecte (result)
   * ve del canon (rules.A5_nouvingut_l1.result).
   */
  function nouvingutAmbL1(p) {
    if (!p) return false;
    function hasChip(c) {
      var cat = p.cat || '';
      var chips = (p.chips || []).map(function (x) { return (x && x.cat) || ''; });
      return cat === c || chips.indexOf(c) !== -1 || cat === ('group-' + c);
    }
    var conds = Array.isArray(p.conditions) ? p.conditions : [];
    var nouCond = conds.find ? conds.find(function (c) { return c && c.key === 'nouvingut'; }) : null;
    var sv = p.subvariables || {};
    var nouSv = sv.nouvingut || sv.l2 || {};
    var isL2 = !!nouCond || hasChip('cat');
    var l1 = (nouCond && nouCond.l1) || nouSv.l1 || p.l1 || '';
    return isL2 && !!l1;
  }

  /**
   * Retorna la llista de complement-IDs auto-suggerits per a (perfil, MECR),
   * aplicant el canon matriu_cobertura.json segons el camp `algoritme`:
   *   1) Banda MECR (high = fallback per a buit/desconegut).
   *   2) Base = unió OR de CANON.base per cada condició present.
   *   3) Si banda=low I hi ha condició: R1 (afegir pictos si visual_need),
   *      R2 (treure mapes), R3 (treure glossari si disl pur).
   *   4) Si NO hi ha condició: fallback.default; si banda=low I curs ∈
   *      primaria_inicial_cursos → R4 (només preguntes), EXCEPTE nouvingut+L1 → A5.
   * Ordre de sortida = complement_keys.
   */
  function defaultComplementsForProfile(p, mecr) {
    var cat = (p && p.cat) || '';
    var chips = (p && p.chips) ? p.chips.map(function (c) { return (c && c.cat) || ''; }).filter(Boolean) : [];
    function has(c) { return cat === c || chips.indexOf(c) !== -1 || cat === ('group-' + c); }

    // 1) + 2) Base: unió OR de les files del canon per cada condició present.
    var active = {};
    MATRIU_KEYS.forEach(function (k) { active[k] = false; });
    var anyKnown = false;
    Object.keys(CANON.base).forEach(function (cond) {
      if (has(cond)) {
        anyKnown = true;
        CANON.base[cond].forEach(function (k) { active[k] = true; });
      }
    });

    var band = mecrBand(mecr);

    if (!anyKnown) {
      // 4) Fallback sense condicions reconegudes.
      var fb = RULES.fallback.default;
      var r4 = RULES.R4_primaria_inicial;
      if (band === (r4.when_band || 'low')) {
        var cursR4 = (p && (p.curs || p.cursUI)) || '';
        var cursList = PRIMARIA_INICIAL_CURSOS; // r4.cursos apunta a primaria_inicial_cursos
        if (cursList.indexOf(cursR4) !== -1) {
          // A5: excepció a R4 si nouvingut amb L1 declarada (detecció runtime,
          // efecte del canon).
          if (nouvingutAmbL1(p)) return RULES.A5_nouvingut_l1.result.slice();
          return r4.only.slice();
        }
      }
      return fb.slice();
    }

    // 3) Modulació per a banda 'low' quan hi ha condicions reconegudes.
    if (band === 'low') {
      // R1: afegir pictogrames si alguna condició de visual_need.
      var r1 = RULES.R1_add_pictos;
      if (band === (r1.when_band || 'low') && VISUAL_NEED_CONDITIONS.some(has)) {
        r1.add.forEach(function (k) { active[k] = true; });
      }
      // R2: treure mapes fora de rang.
      RULES.R2_drop_maps.drop.forEach(function (k) { active[k] = false; });
      // R3: dislèxia pura (sense cat ni tdl) → treure glossari.
      var r3 = RULES.R3_drop_glossari_disl;
      var unless = r3.unless || [];
      if (has(r3.if) && !unless.some(has)) {
        r3.drop.forEach(function (k) { active[k] = false; });
      }
    }

    return MATRIU_KEYS.filter(function (k) { return active[k]; });
  }

  var api = {
    MATRIU_CONDICIONS: MATRIU_CONDICIONS,
    MATRIU_KEYS: MATRIU_KEYS,
    VISUAL_NEED_CONDITIONS: VISUAL_NEED_CONDITIONS,
    mecrBand: mecrBand,
    defaultComplementsForProfile: defaultComplementsForProfile,
    _canonVersion: CANON.version,
  };

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
  } else {
    root.ComplementsMatriu = api;
  }
})(typeof window !== 'undefined' ? window : globalThis);
