/**
 * complements-matriu.js — matriu canònica FJE + modulació per MECR
 *
 * Decideix quins complements pre-marcar al Pas 2 segons:
 *   - les condicions del perfil (matriu condició → complements)
 *   - el nivell MECR demanat (modulació de l'auto-suggestió)
 *
 * Font canon de la matriu: ui/saber-ne.html §7 (Complements per condició),
 * validada amb NotebookLM 2026-05-27 (Opció D).
 *
 * La modulació MECR s'afegeix 2026-05-30 com a resposta a casos reals
 * detectats per docents (cas titella: dislèxia A1 + 1r primària rebia
 * glossari textual i sense pictogrames, ambdós inadequats a aquell nivell).
 *
 * Es carrega tant des de pas2.html (via <script src>) com des de tests
 * Node (via require/import); l'export es fa de manera dual.
 */
(function (root) {
  'use strict';

  // ───── Matriu base: condició → 12 booleans (un per complement) ─────
  //
  // MATRIU §7 v2 (2026-05-27) — refeta segons validació pedagògica NotebookLM
  // (Opció D: bastides i preguntes_comprensio mai activades alhora als defaults).
  // Principis aplicats:
  //   - BASTIDES als perfils d'aprenentatge inicial (estratègia lectora)
  //   - PREGUNTES als perfils amb autonomia lectora (contingut del text)
  //   - Mai BASTIDES + PREGUNTES alhora (eviten redundància plànol crític)
  //   - Visual exclusiu per MECR: esquema (A1/A2) · mapa mental (B1) · mapa conceptual (B2+)
  //   - AC: sense esquema, sense pictogrames (expertise reversal — infantilitza)
  //   - "Menys és més" (MALL): defaults reduïts (mitjana 3 vs 5 abans)
  var MATRIU_CONDICIONS = {
    //            [gloss, esq,   bast,  mapa_c, preg,  aprof, picto, mapa_m, plant, resum, cartes, rubr]
    tea:         [false, true,  true,  false, false, false, true,  false, false, false, false, false],
    tdah:        [true,  true,  false, false, true,  false, false, false, false, false, false, false],
    disl:        [true,  true,  true,  false, false, false, false, false, false, false, false, false],
    di:          [false, true,  true,  false, false, false, true,  false, false, false, false, false],
    tdl:         [true,  true,  true,  false, false, false, false, false, false, false, false, false],
    ac:          [false, false, false, false, false, true,  false, true,  false, false, false, true ],
    aud:         [true,  false, false, false, true,  false, true,  false, false, false, false, false],
    vis:         [true,  false, false, false, true,  false, false, false, false, false, false, false],
    tdc:         [true,  false, false, false, true,  false, false, false, false, false, false, false],
    cat:         [true,  false, true,  false, false, false, true,  false, false, false, false, false], // nouvingut (català L2)
    vuln:        [true,  true,  false, false, true,  false, false, false, false, false, false, false],
    emo:         [true,  false, false, false, true,  false, false, false, false, false, false, false],
    discalculia: [true,  true,  true,  false, false, false, false, false, false, false, false, false],
  };

  var MATRIU_KEYS = [
    'glossari', 'esquema_visual', 'bastides', 'mapa_conceptual',
    'preguntes_comprensio', 'activitats_aprofundiment', 'pictogrames',
    'mapa_mental', 'plantilles_genere', 'resum_graduat', 'cartes_conversacionals',
    'rubriques',
  ];

  // Condicions que necessiten suport visual prioritari a nivell baix.
  // No inclou TDAH/AC/vuln/emo perquè la seva necessitat no és lèxico-visual.
  var VISUAL_NEED_CONDITIONS = ['disl', 'di', 'tdl', 'cat', 'tea', 'vis', 'discalculia'];

  /**
   * Normalitza un MECR a la banda: 'low' (pre-A1/A1), 'mid' (A2/B1), 'high' (B2+).
   * Banda 'high' també és el fallback per a entrades buides/desconegudes
   * — no apliquem regles de baix si no sabem el nivell.
   */
  function mecrBand(mecr) {
    var m = String(mecr || '').toUpperCase().replace('Ç', 'C').trim();
    if (m === 'PRE-A1' || m === 'A1') return 'low';
    if (m === 'A2' || m === 'B1')     return 'mid';
    return 'high';
  }

  /**
   * Retorna la llista de complement-IDs auto-suggerits per a (perfil, MECR).
   *
   * Algoritme:
   *   1) Base: unió OR de les files de la matriu per a cada condició present.
   *   2) Modulació MECR (només banda 'low'):
   *      - R1: si perfil té necessitat visual → AFEGIM pictogrames.
   *      - R2: trèiem mapa_conceptual i mapa_mental (fora de rang segons
   *            SKILL canon: A2+ i B1+ respectivament).
   *      - R3: dislèxia SENSE nouvingut ni TDL → trèiem glossari textual
   *            (afegeix càrrega lectora; pictogrames substitueix-ho amb R1).
   *            Nouvinguts mantenen glossari (bilingüe és central per L2);
   *            TDL manté glossari (gap lèxic és el seu nucli).
   *   3) Sense condicions reconegudes: fallback bàsic ['glossari','preguntes_comprensio'].
   */
  function defaultComplementsForProfile(p, mecr) {
    var cat = (p && p.cat) || '';
    var chips = (p && p.chips) ? p.chips.map(function (c) { return (c && c.cat) || ''; }).filter(Boolean) : [];
    function has(c) { return cat === c || chips.indexOf(c) !== -1 || cat === ('group-' + c); }

    // 1) Base
    var active = new Array(MATRIU_KEYS.length);
    for (var i = 0; i < active.length; i++) active[i] = false;
    var anyKnown = false;
    Object.keys(MATRIU_CONDICIONS).forEach(function (cond) {
      if (has(cond)) {
        anyKnown = true;
        MATRIU_CONDICIONS[cond].forEach(function (v, i) { if (v) active[i] = true; });
      }
    });
    if (!anyKnown) return ['glossari', 'preguntes_comprensio'];

    // 2) Modulació MECR
    var band = mecrBand(mecr);
    var idx = function (id) { return MATRIU_KEYS.indexOf(id); };
    if (band === 'low') {
      var hasVisualNeed = VISUAL_NEED_CONDITIONS.some(has);
      // R1
      if (hasVisualNeed) {
        var iPic = idx('pictogrames');
        if (iPic >= 0) active[iPic] = true;
      }
      // R2
      [idx('mapa_conceptual'), idx('mapa_mental')].forEach(function (i) {
        if (i >= 0) active[i] = false;
      });
      // R3
      if (has('disl') && !has('cat') && !has('tdl')) {
        var iGl = idx('glossari');
        if (iGl >= 0) active[iGl] = false;
      }
    }

    return MATRIU_KEYS.filter(function (_v, i) { return active[i]; });
  }

  var api = {
    MATRIU_CONDICIONS: MATRIU_CONDICIONS,
    MATRIU_KEYS: MATRIU_KEYS,
    VISUAL_NEED_CONDITIONS: VISUAL_NEED_CONDITIONS,
    mecrBand: mecrBand,
    defaultComplementsForProfile: defaultComplementsForProfile,
  };

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
  } else {
    root.ComplementsMatriu = api;
  }
})(typeof window !== 'undefined' ? window : globalThis);
