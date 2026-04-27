/*
 * ATNE — Catàleg de tipografies i auto-switch per perfil
 *
 * Carregar DESPRÉS de auth.js. Exposa:
 *   window.ATNE_FONTS        — catàleg complet
 *   window.atneSetFont(key)  — aplica la font al text adaptat
 *   window.atneAutoFont(profile) — calcula i aplica la font recomanada
 */
(function () {
  'use strict';

  // ── Catàleg ──────────────────────────────────────────────────────────────
  //
  // Cada entrada documenta la tipografia des del punt de vista pedagògic.
  // Camps:
  //   label      — nom comercial per mostrar al selector
  //   css        — valor complet per a font-family
  //   desc       — descripció breu per al selector (docent)
  //   detail     — característiques tècniques i pedagògiques
  //   badge      — etiqueta curta (o null)
  //   conditions — condicions del perfil que activen l'auto-switch
  //   priority   — prioritat si hi ha múltiples condicions (menor = prioritat)

  window.ATNE_FONTS = {

    inter: {
      label: 'Inter',
      css: "'Inter', sans-serif",
      desc: 'Predeterminada · Ús general · Alta llegibilitat',
      detail: [
        'Dissenyada per Rasmus Andersson (2016) específicament per a pantalles.',
        'x-height elevada i apertures obertes → molt llegible a mides petites.',
        'Cobertura: llatí, llatí estès, grec, ciríl·lic.',
        'Bones per a textos acadèmics estàndard (ESO, Batxillerat, FP general).',
        'Variable: pes 100–900.',
      ],
      badge: null,
      conditions: [],   // default — no activa auto-switch
      priority: 99,
    },

    lexend: {
      label: 'Lexend',
      css: "'Lexend', sans-serif",
      desc: 'Dislèxia · TDAH · TDL · Nouvinguts',
      detail: [
        'Dissenyada per Thomas Jockin (Google, 2018) aplicant el Lubalin Spaceband Principle.',
        'Basada en recerca de la Dra. Bonnie Shaver-Troup: l\'espaiat entre lletres redueix l\'esforç visual.',
        'Redueix la confusió entre caràcters similars (b/d, p/q) gràcies a formes més diferenciades.',
        'Ideal per a lectors amb dislèxia, TDAH, TDL i alumnes que aprenen català com a L2.',
        'Cobertura: llatí, llatí estès, vietnamita.',
        'Variable: pes 100–900.',
      ],
      badge: 'dislèxia · TDAH',
      conditions: ['disl', 'tdah', 'tdl', 'cat', 'nouvingut'],
      priority: 2,
    },

    atkinson: {
      label: 'Atkinson Hyperlegible Next',
      css: "'Atkinson Hyperlegible Next', 'Atkinson Hyperlegible', sans-serif",
      desc: 'Baixa visió · TEA · Discriminació màxima de caràcters',
      detail: [
        'Creada pel Braille Institute of America (2019, Next 2024) per a persones amb baixa visió.',
        'Cada caràcter té una forma única i diferenciada: b/d/p/q, 0/O, 1/l/I/j mai es confonen.',
        'Terminacions (ascendents/descendents) exagerats per millorar la discriminació.',
        'Recomanada per al TEA per reduir ambigüitat visual i per a qualsevol DUA-Accés.',
        'Cobertura: llatí, llatí estès.',
        'Pesos: 200, 300, 400, 700.',
      ],
      badge: 'visió · TEA',
      conditions: ['tea', 'bv', 'da', 'da-sig'],
      priority: 1,
    },

    fraunces: {
      label: 'Fraunces',
      css: "'Fraunces', serif",
      desc: 'Títols · Altes capacitats · Textos literaris',
      detail: [
        'Dissenyada per Undercase Type (2020). Serif variable amb eix òptic (9–144pt).',
        'Als cossos de text (9–14pt) és conservadora i llegible; a cossos grans és expressiva.',
        'L\'eix "Wonky" permet formes alternatives per a un estil més literari o creatiu.',
        'Adequada per a textos literaris, poesia, narrativa i producció per a altes capacitats.',
        'Cobertura: llatí, llatí estès.',
        'Variable: pes 100–900, òptic 9–144.',
      ],
      badge: 'literari',
      conditions: ['ac'],
      priority: 3,
    },

    jetbrains: {
      label: 'JetBrains Mono',
      css: "'JetBrains Mono', monospace",
      desc: 'Monospace · Textos tècnics · Codi · FP',
      detail: [
        'Dissenyada per JetBrains (2019) per a programadors.',
        'Amplada augmentada i formes de lletres distintes per a entorns de codi.',
        'Lligadures tipogràfiques (!=, ->, >=) per a textos tècnics.',
        'Indicada per a textos de FP (programació, electrònica, sistemes), ciències computacionals.',
        'Cobertura: llatí, llatí estès, ciríl·lic.',
        'Variable: pes 100–800.',
      ],
      badge: 'tècnic',
      conditions: [],
      priority: 99,
    },

    noto_math: {
      label: 'Noto Sans Math',
      css: "'Noto Sans Math', 'Inter', sans-serif",
      desc: 'Matemàtiques · Física · Química · Símbols',
      detail: [
        'Dissenyada per Google com a part de la família Noto (missió: "cap tofu" = cap caràcter invàlid).',
        'Cobreix el bloc matemàtic de l\'Unicode: ∑ ∫ √ ∂ ≤ ≥ ≠ ∞ π Δ ∇ ⊕ ⊗ ...',
        'Harmonitza visualment amb Inter (mateixa mètrica vertical).',
        'Recomanada per a textos de matemàtiques, física, química i qualsevol matèria STEM.',
        'S\'aplica com a complement (els caràcters llatins segueixen en Inter).',
      ],
      badge: 'STEM',
      conditions: [],  // s'activa per matèria, no per condició de perfil
      priority: 99,
    },

  };

  // ── Selector d'àmbit ─────────────────────────────────────────────────────
  // La font s'aplica a l'element .adapted-output (o l'id passat).
  var TARGET_SELECTOR = '.adapted-output, .result-content, #adapted-text, .adapt-result';

  window.atneSetFont = function (key) {
    var font = window.ATNE_FONTS[key];
    if (!font) return;
    try { localStorage.setItem('atne.font_key', key); } catch (e) {}
    document.querySelectorAll(TARGET_SELECTOR).forEach(function (el) {
      el.style.fontFamily = font.css;
    });
    // Actualitza el selector si existeix
    var sel = document.getElementById('atne-font-sel');
    if (sel) sel.value = key;
  };

  // ── Auto-switch per perfil ────────────────────────────────────────────────
  window.atneAutoFont = function (profile) {
    if (!profile) return;
    var conditions = [];
    // Recull totes les condicions actives del perfil
    if (profile.cat)       conditions.push(profile.cat);
    if (profile.conditions) conditions = conditions.concat(profile.conditions);
    if (profile.chips)     profile.chips.forEach(function(c){ if(c.cat) conditions.push(c.cat); });

    var best = null;
    conditions.forEach(function (cond) {
      Object.entries(window.ATNE_FONTS).forEach(function (kv) {
        var key = kv[0], meta = kv[1];
        if (meta.conditions.includes(cond)) {
          if (!best || meta.priority < window.ATNE_FONTS[best].priority) {
            best = key;
          }
        }
      });
    });

    // Si hi ha una font desada manualment pel docent, la respectem
    var saved = null;
    try { saved = localStorage.getItem('atne.font_key'); } catch(e) {}
    var finalKey = saved || best || 'inter';
    window.atneSetFont(finalKey);
    return finalKey;
  };

  // ── Construeix el selector HTML ───────────────────────────────────────────
  window.atneBuildFontSelector = function (containerId) {
    var container = document.getElementById(containerId);
    if (!container) return;

    var saved = 'inter';
    try { saved = localStorage.getItem('atne.font_key') || 'inter'; } catch(e) {}

    var sel = document.createElement('select');
    sel.id = 'atne-font-sel';
    sel.title = 'Tipografia del text adaptat';
    sel.style.cssText = 'font-size:12px;padding:3px 6px;border:1px solid var(--paper-line,#e4e0da);border-radius:6px;background:#fff;color:var(--ink-700,#374151);cursor:pointer;font-family:inherit';

    Object.entries(window.ATNE_FONTS).forEach(function (kv) {
      var key = kv[0], meta = kv[1];
      var opt = document.createElement('option');
      opt.value = key;
      opt.textContent = meta.label + (meta.badge ? ' · ' + meta.badge : '');
      if (key === saved) opt.selected = true;
      sel.appendChild(opt);
    });

    sel.addEventListener('change', function () {
      localStorage.setItem('atne.font_key', sel.value);
      window.atneSetFont(sel.value);
    });

    // Label
    var label = document.createElement('label');
    label.style.cssText = 'display:flex;align-items:center;gap:6px;font-size:11px;color:var(--ink-500,#6b7280);font-family:var(--mono,monospace)';
    label.innerHTML = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 7V4h16v3M9 20h6M12 4v16"/></svg>Tipus';
    label.appendChild(sel);
    container.appendChild(label);

    // Aplica la font guardada
    window.atneSetFont(saved);
  };

})();
