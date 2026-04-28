/**
 * ATNE · Model canònic de perfils — font única de veritat
 *
 * Aquest mòdul és el centre del sistema de perfils. Tot allò que produeix o
 * consumeix un perfil (Flash, Taller pas1/pas2/pas3, persistència, payload
 * cap al backend, render de targetes) hi passa pel mig.
 *
 * Capes:
 *   FORM (Flash | Taller persona | Taller grup)
 *     ↓ (adapter)
 *   PERFIL CANÒNIC  ←  font única
 *     ↓ (mappers)
 *   PERSISTÈNCIA · CARD · PAYLOAD BACKEND
 *
 * Decisions clau:
 *   1. Claus de condicions canòniques: noms llargs (tdah, dislexia, nouvingut,
 *      altes_capacitats, tea, di, tdl, discapacitat_auditiva,
 *      discapacitat_visual, discalculia, vulnerabilitat).
 *   2. Subvariables sempre niades dins de cada condició.
 *   3. alfabet_llati i toggles boolean tenen 3 estats: true | false | null
 *      (null = "desconegut" — el backend NO ha d'assumir true per defecte).
 *   4. MECR final = derivació explícita (curs + condicions + override manual).
 *   5. behaviors i aids del perfil es mostren a la targeta. Si l'usuari no
 *      n'ha declarat cap, els derivem automàticament des de les condicions.
 */
(function () {
  'use strict';

  // ── Taula curs → MECR (Decret 175/2022 + 171/2022 + 21/2023) ──────────────
  const COURSE_TO_MECR = {
    'I3': 'pre-A1', 'I4': 'pre-A1', 'I5': 'pre-A1',
    '1r Primària': 'A1', '2n Primària': 'A1',
    '3r Primària': 'A1', '4t Primària': 'A2',
    '5è Primària': 'A2', '6è Primària': 'B1',
    'Primer cicle Primària': 'A1',
    'Segon cicle Primària': 'A1',
    'Tercer cicle Primària': 'A2',
    '1r ESO': 'B1', '2n ESO': 'B1', '3r ESO': 'B2', '4t ESO': 'B2',
    'Primer cicle ESO': 'B1', 'Segon cicle ESO': 'B2',
    '1r Batxillerat': 'B2', '2n Batxillerat': 'C1',
    'Grau Bàsic': 'A2', 'Grau Mitjà': 'B1', 'Grau Superior': 'B2',
    '1r FP Grau Bàsic': 'A2', '2n FP Grau Bàsic': 'A2',
    '1r FP Grau Mitjà': 'B1', '2n FP Grau Mitjà': 'B1',
    '1r FP Grau Superior': 'B2', '2n FP Grau Superior': 'B2',
  };
  const MECR_LADDER = ['pre-A1', 'A1', 'A2', 'B1', 'B2', 'C1', 'C2'];

  // ── Curs UI → curs API per a Flash backend ────────────────────────────────
  const CURS_TO_API = {
    'I3': 'primaria_12', 'I4': 'primaria_12', 'I5': 'primaria_12',
    '1r Primària': 'primaria_12', '2n Primària': 'primaria_12',
    '3r Primària': 'primaria_34', '4t Primària': 'primaria_34',
    '5è Primària': 'primaria_56', '6è Primària': 'primaria_56',
    '1r ESO': 'eso_12', '2n ESO': 'eso_12',
    '3r ESO': 'eso_34', '4t ESO': 'eso_34',
    '1r Batxillerat': 'batxillerat', '2n Batxillerat': 'batxillerat',
    '1r FP Grau Bàsic': 'batxillerat', '2n FP Grau Bàsic': 'batxillerat',
    '1r FP Grau Mitjà': 'batxillerat', '2n FP Grau Mitjà': 'batxillerat',
    '1r FP Grau Superior': 'batxillerat', '2n FP Grau Superior': 'batxillerat',
  };

  // ── Metadata de llengües (família + alfabet) per derivar alfabet_llati ────
  // Reduïda al mínim útil. Si la L1 no és aquí, alfabet_llati queda null.
  const L1_META = {
    'Àrab': { family: 'semítica', alphabet: 'àrab', llati: false, romance: false },
    'Amazic': { family: 'amaziga', alphabet: 'tifinag/llatí', llati: true, romance: false },
    'Albanès': { family: 'albanesa', alphabet: 'llatí', llati: true, romance: false },
    'Alemany': { family: 'germànica', alphabet: 'llatí', llati: true, romance: false },
    'Anglès': { family: 'germànica', alphabet: 'llatí', llati: true, romance: false },
    'Bengalí': { family: 'indoirania', alphabet: 'bengalí', llati: false, romance: false },
    'Birmà': { family: 'sinotibetana', alphabet: 'birmà', llati: false, romance: false },
    'Búlgar': { family: 'eslava', alphabet: 'ciríl·lic', llati: false, romance: false },
    'Coreà': { family: 'coreana', alphabet: 'hangul', llati: false, romance: false },
    'Croat': { family: 'eslava', alphabet: 'llatí', llati: true, romance: false },
    'Diola': { family: 'níger-congolesa', alphabet: 'llatí', llati: true, romance: false },
    'Espanyol': { family: 'romance', alphabet: 'llatí', llati: true, romance: true },
    'Èuscar': { family: 'aïllada', alphabet: 'llatí', llati: true, romance: false },
    'Francès': { family: 'romance', alphabet: 'llatí', llati: true, romance: true },
    'Fula (Peul)': { family: 'níger-congolesa', alphabet: 'llatí', llati: true, romance: false },
    'Gallec': { family: 'romance', alphabet: 'llatí', llati: true, romance: true },
    'Grec': { family: 'hel·lènica', alphabet: 'grec', llati: false, romance: false },
    'Guaraní': { family: 'tupí', alphabet: 'llatí', llati: true, romance: false },
    'Gujarati': { family: 'indoirania', alphabet: 'gujarati', llati: false, romance: false },
    'Hausa': { family: 'afroasiàtica', alphabet: 'llatí/àrab', llati: null, romance: false },
    'Hebreu': { family: 'semítica', alphabet: 'hebreu', llati: false, romance: false },
    'Hindi': { family: 'indoirania', alphabet: 'devanagari', llati: false, romance: false },
    'Hongarès': { family: 'uràlica', alphabet: 'llatí', llati: true, romance: false },
    'Igbo': { family: 'níger-congolesa', alphabet: 'llatí', llati: true, romance: false },
    'Indonesi': { family: 'austronèsia', alphabet: 'llatí', llati: true, romance: false },
    'Italià': { family: 'romance', alphabet: 'llatí', llati: true, romance: true },
    'Iorubà': { family: 'níger-congolesa', alphabet: 'llatí', llati: true, romance: false },
    'Japonès': { family: 'japònica', alphabet: 'kanji/kana', llati: false, romance: false },
    'Kazakh': { family: 'túrquica', alphabet: 'ciríl·lic/llatí', llati: null, romance: false },
    'Khmer': { family: 'austroasiàtica', alphabet: 'khmer', llati: false, romance: false },
    'Kurd': { family: 'indoirania', alphabet: 'llatí/àrab', llati: null, romance: false },
    'Lingala': { family: 'níger-congolesa', alphabet: 'llatí', llati: true, romance: false },
    'Malai': { family: 'austronèsia', alphabet: 'llatí', llati: true, romance: false },
    'Malgaix': { family: 'austronèsia', alphabet: 'llatí', llati: true, romance: false },
    'Mandinka': { family: 'níger-congolesa', alphabet: 'llatí', llati: true, romance: false },
    'Marathi': { family: 'indoirania', alphabet: 'devanagari', llati: false, romance: false },
    'Neerlandès': { family: 'germànica', alphabet: 'llatí', llati: true, romance: false },
    'Nepalí': { family: 'indoirania', alphabet: 'devanagari', llati: false, romance: false },
    'Panjabi': { family: 'indoirania', alphabet: 'gurmukhi/shahmukhi', llati: false, romance: false },
    'Pastu': { family: 'indoirania', alphabet: 'àrab', llati: false, romance: false },
    'Persa (farsi / dari)': { family: 'indoirania', alphabet: 'àrab', llati: false, romance: false },
    'Polonès': { family: 'eslava', alphabet: 'llatí', llati: true, romance: false },
    'Portuguès': { family: 'romance', alphabet: 'llatí', llati: true, romance: true },
    'Quítxua': { family: 'quítxua', alphabet: 'llatí', llati: true, romance: false },
    'Romanes': { family: 'indoirania', alphabet: 'llatí', llati: true, romance: false },
    'Romanès': { family: 'romance', alphabet: 'llatí', llati: true, romance: true },
    'Rus': { family: 'eslava', alphabet: 'ciríl·lic', llati: false, romance: false },
    'Serbi': { family: 'eslava', alphabet: 'ciríl·lic/llatí', llati: null, romance: false },
    'Singalès': { family: 'indoirania', alphabet: 'singalès', llati: false, romance: false },
    'Soninke': { family: 'níger-congolesa', alphabet: 'llatí', llati: true, romance: false },
    'Suahili': { family: 'níger-congolesa', alphabet: 'llatí', llati: true, romance: false },
    'Tagalog': { family: 'austronèsia', alphabet: 'llatí', llati: true, romance: false },
    'Tailandès': { family: 'tai-kadai', alphabet: 'tailandès', llati: false, romance: false },
    'Tamazight': { family: 'amaziga', alphabet: 'tifinag/llatí', llati: true, romance: false },
    'Tàmil': { family: 'dravídica', alphabet: 'tàmil', llati: false, romance: false },
    'Telugu': { family: 'dravídica', alphabet: 'telugu', llati: false, romance: false },
    'Tigrinya': { family: 'semítica', alphabet: 'ge\'ez', llati: false, romance: false },
    'Turc': { family: 'túrquica', alphabet: 'llatí', llati: true, romance: false },
    'Ucraïnès': { family: 'eslava', alphabet: 'ciríl·lic', llati: false, romance: false },
    'Urdú': { family: 'indoirania', alphabet: 'àrab (nasta\'liq)', llati: false, romance: false },
    'Uzbek': { family: 'túrquica', alphabet: 'llatí/ciríl·lic', llati: null, romance: false },
    'Vietnamita': { family: 'austroasiàtica', alphabet: 'llatí', llati: true, romance: false },
    'Wolof': { family: 'níger-congolesa', alphabet: 'llatí', llati: true, romance: false },
    'Xinès mandarí': { family: 'sinotibetana', alphabet: 'xinès', llati: false, romance: false },
    'Xinès cantonès': { family: 'sinotibetana', alphabet: 'xinès', llati: false, romance: false },
  };

  // ── Catàleg canònic de condicions (claus llargues) ────────────────────────
  const CONDITION_KEYS = [
    'tdah', 'dislexia', 'nouvingut', 'altes_capacitats', 'tea',
    'di', 'tdl', 'discapacitat_auditiva', 'discapacitat_visual',
    'discalculia', 'vulnerabilitat',
  ];

  // ── Via observable: mapatge conducta → condició implícita ────────────────
  // Permet que un docent SENSE diagnòstic activi les mateixes instruccions
  // marcant les conductes que observa. Una conducta amb mapping clar activa
  // la condició corresponent amb flag `via:'observable'`. Si la condició ja
  // està declarada via diagnòstic, la declarada guanya (no es duplica).
  //
  // Mapeig conservador: només conductes amb significació pedagògica clara.
  // Conductes ambigües (fatiga, conceptes abstractes, bloqueig) NO infereixen
  // — només alimenten observacions descriptives.
  const BEHAVIOR_TO_CONDITION = {
    dist: { key: 'tdah' },           // "Es distreu amb textos llargs"
    imp:  { key: 'tdah' },           // "Respon abans de llegir la consigna"
    dec:  { key: 'dislexia' },       // "Confon paraules o salta línies"
    l2:   { key: 'nouvingut' },      // "Dificultats amb la llengua vehicular"
    fast: { key: 'altes_capacitats' },// "Acaba molt ràpid i es desmotiva"
    // Sense mapping (massa ambigues): fat, abs, neg
  };

  // ── Mapping legacy → canònic ──────────────────────────────────────────────
  const LEGACY_KEY = {
    disl: 'dislexia', l2: 'nouvingut', cat: 'nouvingut',
    ac: 'altes_capacitats', au: 'discapacitat_auditiva', vi: 'discapacitat_visual',
  };

  const CONDITION_LABEL = {
    tdah: 'TDAH', dislexia: 'Dislèxia', nouvingut: 'Català L2',
    altes_capacitats: 'Altes capacitats', tea: 'TEA', di: 'DI',
    tdl: 'TDL', discapacitat_auditiva: 'Disc. auditiva',
    discapacitat_visual: 'Disc. visual', discalculia: 'Discalcúlia',
    vulnerabilitat: 'Vulnerabilitat',
  };

  // Color "cat" del perfil (per a la card) segons primera condició.
  const CONDITION_TO_CAT = {
    tdah: 'tdah', dislexia: 'disl', nouvingut: 'cat', altes_capacitats: 'ac',
    tea: 'tea', di: 'tdah', tdl: 'tdah', discapacitat_auditiva: 'tdah',
    discapacitat_visual: 'tdah', discalculia: 'tdah', vulnerabilitat: 'tdah',
  };

  // ── Util ──────────────────────────────────────────────────────────────────
  function normalizeKey(k) {
    if (!k) return null;
    const lower = String(k).toLowerCase().trim();
    return LEGACY_KEY[lower] || lower;
  }

  function isCanonicalKey(k) {
    return CONDITION_KEYS.indexOf(k) >= 0;
  }

  // Converteix mesos_range → mesos numèric (mediana del rang).
  function mesosRangeToNum(range) {
    const M = {
      'Menys de 6 mesos': 3,
      '6-12 mesos': 9,
      '1-2 anys': 18,
      'Més de 2 anys': 30,
    };
    return M[range] !== undefined ? M[range] : null;
  }

  // Índex case-insensitive de L1_META per resoldre 'àrab', 'arab', 'Àrab' uniformement.
  const L1_META_INDEX = (function () {
    const idx = {};
    Object.keys(L1_META).forEach(k => {
      idx[k.toLowerCase()] = k;
      // Versió sense accents per ajudar amb 'arab', 'frances', etc.
      const noAcc = k.toLowerCase()
        .replace(/[àáâä]/g, 'a').replace(/[èéêë]/g, 'e')
        .replace(/[ìíîï]/g, 'i').replace(/[òóôö]/g, 'o')
        .replace(/[ùúûü]/g, 'u').replace(/[ç]/g, 'c');
      if (!idx[noAcc]) idx[noAcc] = k;
    });
    return idx;
  })();

  function _lookupL1Meta(l1Raw) {
    if (!l1Raw) return { canonical: null, meta: null };
    const lower = String(l1Raw).toLowerCase().trim();
    const canonical = L1_META_INDEX[lower] || null;
    return { canonical, meta: canonical ? L1_META[canonical] : null };
  }

  // Enriqueix una condició nouvingut amb metadata de la L1.
  function enrichNouvingut(cond) {
    if (cond.l1) {
      const { canonical, meta } = _lookupL1Meta(cond.l1);
      if (meta) {
        // Normalitza l1 a la forma canònica del catàleg ('Àrab' en lloc de 'àrab')
        if (canonical) cond.l1 = canonical;
        if (cond.l1_family === undefined) cond.l1_family = meta.family;
        if (cond.l1_alphabet === undefined) cond.l1_alphabet = meta.alphabet;
        // Si l'usuari NO ha declarat alfabet_llati, l'inferim de la L1
        if (cond.alfabet_llati === undefined || cond.alfabet_llati === null) {
          cond.alfabet_llati = meta.llati;
        }
        if (cond.l1_romanic === undefined) cond.l1_romanic = meta.romance;
      }
    }
    if (cond.mesos_range && (cond.mesos_num === undefined || cond.mesos_num === null)) {
      cond.mesos_num = mesosRangeToNum(cond.mesos_range);
    }
    return cond;
  }

  // ── Factory: construir un perfil canònic des de zero ──────────────────────
  function createProfile(opts) {
    const o = opts || {};
    const conditions = (o.conditions || []).map(c => {
      const key = normalizeKey(c.key);
      if (!isCanonicalKey(key)) return null;
      const enriched = Object.assign({}, c, { key });
      if (key === 'nouvingut') enrichNouvingut(enriched);
      return enriched;
    }).filter(Boolean);

    return {
      id: o.id || ('p_' + Date.now().toString(36)),
      source: o.source || 'unknown', // 'taller-person' | 'taller-group' | 'flash' | 'demo'
      type: o.type || 'person',       // 'person' | 'group'
      name: o.name || '',
      course: o.course || '',          // text amb lletra ("2n ESO B")
      course_base: o.course_base || '', // canonical key per a COURSE_TO_MECR
      multi_courses: o.multi_courses || [],
      avatar: o.avatar || (o.name ? o.name[0].toUpperCase() : '?'),
      conditions,
      behaviors: (o.behaviors || []).filter(Boolean),
      aids: (o.aids || []).filter(Boolean),
      mecr_override: o.mecr_override || null,
      group_composition: o.group_composition || [],
      custom: !!o.custom,
      demo: !!o.demo,
      notes: o.notes || '',
      created_at: o.created_at || new Date().toISOString(),
    };
  }

  // ── Derivació de MECR ─────────────────────────────────────────────────────
  // Regles documentades:
  //   1) MECR base = COURSE_TO_MECR[course_base]; si multi-curs, agafa el més baix.
  //   2) AACC: +1 nivell (clamped a C2).
  //   3) Nouvingut: imposa MECR explícit segons mesos i alfabet.
  //      - Menys de 6 mesos: pre-A1 (si alfabet_llati=false), si no A1.
  //      - 6-12 mesos: A1.
  //      - 1-2 anys: A2.
  //      - Més de 2 anys: manté la base.
  //      - L1 romànica: +1 sobre el resultat de Nouvingut (transferència positiva).
  //      Si Nouvingut + AACC: el de Nouvingut guanya (no té sentit pujar a un alumne
  //      arribat fa 2 mesos només per AACC, AACC s'aplica via instruccions de profunditat).
  //   4) mecr_override: si existeix i és vàlid, guanya sempre.
  //
  // Retorna { mecr, auto, reason }
  function deriveMECR(profile) {
    const courses = (profile.multi_courses && profile.multi_courses.length)
      ? profile.multi_courses
      : (profile.course_base ? [profile.course_base] : []);

    let baseIdx = -1;
    for (const c of courses) {
      const m = COURSE_TO_MECR[c];
      if (!m) continue;
      const idx = MECR_LADDER.indexOf(m);
      if (idx < 0) continue;
      if (baseIdx < 0 || idx < baseIdx) baseIdx = idx;
    }
    if (baseIdx < 0) baseIdx = MECR_LADDER.indexOf('B1');

    let idx = baseIdx;
    let reason = 'curs';

    const conds = profile.conditions || [];
    const nouv = conds.find(c => c.key === 'nouvingut');
    const hasAACC = conds.some(c => c.key === 'altes_capacitats');

    if (nouv) {
      let nouvIdx = baseIdx;
      const mr = nouv.mesos_range;
      if (mr === 'Menys de 6 mesos') {
        nouvIdx = MECR_LADDER.indexOf(nouv.alfabet_llati === false ? 'pre-A1' : 'A1');
      } else if (mr === '6-12 mesos') {
        nouvIdx = MECR_LADDER.indexOf('A1');
      } else if (mr === '1-2 anys') {
        nouvIdx = MECR_LADDER.indexOf('A2');
      } else if (mr === 'Més de 2 anys') {
        nouvIdx = baseIdx;
      } else {
        nouvIdx = MECR_LADDER.indexOf('A1');
      }
      if (nouv.l1_romanic === true) nouvIdx = Math.min(nouvIdx + 1, MECR_LADDER.length - 1);
      if (nouvIdx < idx) {
        idx = nouvIdx;
        reason = 'nouvingut';
      }
    } else if (hasAACC) {
      idx = Math.min(idx + 1, MECR_LADDER.length - 1);
      reason = 'aacc+1';
    }

    const auto = MECR_LADDER[idx];

    if (profile.mecr_override && MECR_LADDER.indexOf(profile.mecr_override) >= 0) {
      return { mecr: profile.mecr_override, auto, reason: 'override' };
    }
    return { mecr: auto, auto, reason };
  }

  // ── Derivació visual: chips, behaviors, aids per a la card ────────────────
  function deriveCardView(profile) {
    const { mecr } = deriveMECR(profile);
    const chips = [];
    const conds = profile.conditions || [];

    for (const c of conds) {
      const baseLabel = CONDITION_LABEL[c.key] || c.key;
      // Sufix "(observat)" per a condicions activades via la "via observable".
      // Així el docent veu d'on ve la senyal: declarada (diagnòstic) o inferida (conducta).
      const label = c.via === 'observable' ? `${baseLabel} (observat)` : baseLabel;
      const cat = CONDITION_TO_CAT[c.key] || 'tdah';
      chips.push({ label, cat, observable: c.via === 'observable' });
    }
    const mecrIdx = MECR_LADDER.indexOf(mecr);
    const mecrName = ['Pre-inicial', 'Inicial', 'Bàsic', 'Intermedi', 'Avançat', 'Competent', 'Domini'][mecrIdx] || '';
    chips.push({ label: `${mecr}${mecrName ? ' · ' + mecrName : ''}`, cat: 'lv' });

    // Color "cat" del perfil
    let cat = 'generic';
    if (profile.type === 'group') {
      cat = 'group';
      const firstCond = conds[0];
      if (firstCond) {
        const fc = CONDITION_TO_CAT[firstCond.key];
        if (fc === 'cat') cat = 'group-cat';
        else if (fc === 'ac') cat = 'group-ac';
      }
    } else if (conds[0]) {
      cat = CONDITION_TO_CAT[conds[0].key] || 'generic';
    }

    // Derivació de behaviors si l'usuari no n'ha posat
    let behaviors = (profile.behaviors || []).slice();
    let aids = (profile.aids || []).slice();
    const derived = deriveBehaviorsAndAids(profile);
    if (behaviors.length === 0) behaviors = derived.behaviors;
    if (aids.length === 0) aids = derived.aids;

    return { chips, cat, mecr, behaviors, aids, avatar: profile.avatar };
  }

  // Genera behaviors/aids automàtics a partir de les condicions i subvariables.
  // S'usa quan l'usuari no ha marcat conductes/ajuts manualment.
  function deriveBehaviorsAndAids(profile) {
    const beh = [];
    const aids = [];
    const conds = profile.conditions || [];

    for (const c of conds) {
      if (c.key === 'nouvingut') {
        const head = [c.l1, c.pais].filter(Boolean).join(' · ');
        if (head) beh.push('Origen: ' + head);
        if (c.mesos_range) beh.push('Temps a Catalunya: ' + String(c.mesos_range).toLowerCase());
        if (c.alfabet_llati === false) {
          beh.push('Alfabet d\'origen no llatí');
          aids.push('Transliteració fonètica al glossari');
        }
        if (c.alfabetitzacio_l1 === false) beh.push('Sense alfabetització en L1');
        if (c.escolaritzacio === 'interrompuda') beh.push('Escolarització prèvia interrompuda');
        if (c.l1) aids.push('Glossari amb traducció a ' + String(c.l1).toLowerCase());
        else aids.push('Glossari amb traducció a la L1');
        aids.push('Pictogrames i suport visual');
        aids.push('Frases SVO curtes');
        aids.push('Vocabulari freqüent');
      } else if (c.key === 'tdah') {
        if (c.grau === 'sever') beh.push('TDAH sever — fatiga ràpida');
        else beh.push('Dificultats atencionals');
        aids.push('Fragmentar el text');
        aids.push('Una idea per frase');
        aids.push('Instruccions numerades');
        if (c.baixa_memoria_treball) aids.push('Repetició de la idea clau a cada bloc');
      } else if (c.key === 'dislexia') {
        if (c.tipus === 'fonologica' || c.tipus === 'mixta') beh.push('Dislèxia fonològica');
        else beh.push('Dificultats de descodificació lectora');
        aids.push('Tipografia accessible');
        aids.push('Interlineat ampli');
        aids.push('Marcar paraules clau');
      } else if (c.key === 'tea') {
        beh.push('Necessita estructura predictible');
        aids.push('Evitar ambigüitats i metàfores');
        aids.push('Seqüències pas a pas');
        if (c.suport_nivell >= 2) aids.push('Anticipació de canvis explícita');
      } else if (c.key === 'altes_capacitats') {
        beh.push('Busca repte i profunditat');
        aids.push('Aprofundiment conceptual');
        aids.push('Connexions interdisciplinars');
        aids.push('Preguntes obertes');
      } else if (c.key === 'di') {
        beh.push('Dificultats d\'aprenentatge generals');
        aids.push('Vocabulari freqüent');
        aids.push('Una idea per frase');
        aids.push('Suport visual');
      } else if (c.key === 'tdl') {
        beh.push('Trastorn del desenvolupament del llenguatge');
        aids.push('Glossari de termes');
        aids.push('Frases curtes');
      } else if (c.key === 'discapacitat_auditiva') {
        beh.push('Discapacitat auditiva');
        if (c.comunicacio === 'LSC') aids.push('Simplificació intensiva (L2)');
        aids.push('Suport visual');
      } else if (c.key === 'discapacitat_visual') {
        beh.push('Discapacitat visual');
        aids.push('Tipografia accessible');
        if (c.grau === 'ceguesa') aids.push('Versió en àudio o braille');
      } else if (c.key === 'discalculia') {
        beh.push('Dificultats amb el càlcul');
        aids.push('Substituir nombres abstractes per representacions concretes');
      } else if (c.key === 'vulnerabilitat') {
        beh.push('Context de vulnerabilitat');
        aids.push('Vocabulari freqüent');
        aids.push('Suport visual');
      }
    }

    // Dedup
    return {
      behaviors: Array.from(new Set(beh)),
      aids: Array.from(new Set(aids)),
    };
  }

  // ── Mapper canònic → payload backend (`/api/adapt`) ───────────────────────
  // Aquesta és la ÚNICA via per generar el dict `caracteristiques` que el
  // filtre d'instruccions del backend espera.
  function toBackendProfile(profile) {
    const caracteristiques = {};
    CONDITION_KEYS.forEach(k => { caracteristiques[k] = { actiu: false }; });

    for (const c of profile.conditions || []) {
      if (!isCanonicalKey(c.key)) continue;
      const out = { actiu: true };

      if (c.key === 'nouvingut') {
        if (c.l1) out.l1 = c.l1;
        if (c.pais) out.pais = c.pais;
        if (c.mesos_num != null) out.mesos_catalunya = c.mesos_num;
        if (c.mesos_range) out.mesos_catalunya_range = c.mesos_range;
        if (c.alfabet_llati !== undefined && c.alfabet_llati !== null) out.alfabet_llati = c.alfabet_llati;
        if (c.alfabetitzacio_l1 !== undefined && c.alfabetitzacio_l1 !== null) out.alfabetitzacio_l1 = c.alfabetitzacio_l1;
        if (c.escolaritzacio) out.escolaritzacio = c.escolaritzacio;
        if (c.l1_romanic === true) out.familia_linguistica = 'romanica';
        else if (c.l1_family) out.familia_linguistica = c.l1_family;
      } else if (c.key === 'dislexia') {
        if (c.tipus) out.tipus_dislexia = c.tipus;
        if (c.grau) out.grau = c.grau;
      } else if (c.key === 'tdah') {
        if (c.grau) out.grau = c.grau;
        if (c.subtipus) out.subtipus = c.subtipus;
        if (c.baixa_memoria_treball !== undefined && c.baixa_memoria_treball !== null) out.baixa_memoria_treball = c.baixa_memoria_treball;
        if (c.fatiga_cognitiva !== undefined && c.fatiga_cognitiva !== null) out.fatiga_cognitiva = c.fatiga_cognitiva;
      } else if (c.key === 'tea') {
        if (c.suport_nivell) out.suport_nivell = c.suport_nivell;
        if (c.sensibilitat_sensorial !== undefined) out.sensibilitat_sensorial = c.sensibilitat_sensorial;
      } else if (c.key === 'di') {
        if (c.grau) out.grau = c.grau;
      } else if (c.key === 'tdl') {
        if (c.modalitat) out.modalitat = c.modalitat;
        if (c.semantica !== undefined) out.semantica = c.semantica;
        if (c.morfosintaxi !== undefined) out.morfosintaxi = c.morfosintaxi;
        if (c.pragmatica !== undefined) out.pragmatica = c.pragmatica;
      } else if (c.key === 'discapacitat_auditiva') {
        if (c.grau) out.grau = c.grau;
        if (c.comunicacio) out.comunicacio = c.comunicacio;
        if (c.implant_coclear !== undefined) out.implant_coclear = c.implant_coclear;
      } else if (c.key === 'discapacitat_visual') {
        if (c.grau) out.grau = c.grau;
        if (c.usa_braille !== undefined) out.usa_braille = c.usa_braille;
      } else if (c.key === 'altes_capacitats') {
        if (c.tipus) out.tipus = c.tipus;
      }

      caracteristiques[c.key] = out;
    }

    return {
      nom: profile.name,
      caracteristiques,
      canal_preferent: 'text',
      observacions: (profile.behaviors || []).join(' · '),
      _via: 'canonical',
      group: profile.type === 'group',
      profile_id: profile.id,
      profile_source: profile.source,
    };
  }

  // ── Adapter: Flash form → canonical ───────────────────────────────────────
  // formData: { cursUI, tipus, caracteristica, l1, complements }
  function fromFlashForm(formData) {
    const conds = [];
    const tipus = formData.tipus === 'grup' ? 'group' : 'person';

    if (tipus === 'person' && formData.caracteristica) {
      const k = normalizeKey(formData.caracteristica);
      if (isCanonicalKey(k)) {
        const c = { key: k };
        if (k === 'nouvingut' && formData.l1) c.l1 = formData.l1;
        conds.push(c);
      }
    } else if (tipus === 'group' && formData.caracteristica) {
      // Flash grup: 'suport' → vulnerabilitat, 'repte' → altes_capacitats
      if (formData.caracteristica === 'suport') conds.push({ key: 'vulnerabilitat' });
      else if (formData.caracteristica === 'repte') conds.push({ key: 'altes_capacitats' });
    }

    const cursUI = formData.cursUI || formData.curs || '';
    return createProfile({
      source: 'flash',
      type: tipus,
      name: tipus === 'group' ? `Grup ${cursUI}` : `Alumne/a ${cursUI}`,
      course: cursUI,
      course_base: cursUI,
      avatar: tipus === 'group' ? 'G' : 'A',
      conditions: conds,
    });
  }

  // ── Adapter: Taller form (subvariables planes) → canonical ────────────────
  // pas1 capta:
  //   - conditions: ['nouvingut','dislexia']  (declarades via diagnòstic)
  //   - subvariables: { nouvingut: {l1,...} }
  //   - behaviors_observed: ['dist','l2',...]  (data-beh dels checkboxes)
  // Les behaviors_observed es processen DESPRÉS perquè una condició declarada
  // via diagnòstic guanya sobre la mateixa observada (no es duplica).
  function fromTallerForm(formData) {
    const conds = [];
    const sv = formData.subvariables || {};
    const declaredKeys = new Set();
    for (const rawKey of (formData.conditions || [])) {
      const k = normalizeKey(rawKey);
      if (!isCanonicalKey(k)) continue;
      declaredKeys.add(k);
      const cond = { key: k, via: 'declared' };
      const data = sv[k] || sv[rawKey] || {};

      if (k === 'nouvingut') {
        if (data.l1) cond.l1 = data.l1;
        if (data.pais) cond.pais = data.pais;
        if (data.mesos_range) cond.mesos_range = data.mesos_range;
        if (data.alfabet_llati !== undefined) cond.alfabet_llati = data.alfabet_llati;
        if (data.alfabetitzacio_l1 !== undefined) cond.alfabetitzacio_l1 = data.alfabetitzacio_l1;
        if (data.escolaritzacio) cond.escolaritzacio = data.escolaritzacio;
      } else if (Array.isArray(data.tags)) {
        const tags = data.tags.map(t => String(t).toLowerCase());
        cond.tags = data.tags;
        if (k === 'tdah') {
          if (tags.some(t => t.includes('sever'))) cond.grau = 'sever';
          cond.subtipus = data.tags[0] || '';
        } else if (k === 'dislexia') {
          if (tags.some(t => t.includes('fono'))) cond.tipus = 'fonologica';
          else if (tags.some(t => t.includes('mixta'))) cond.tipus = 'mixta';
          else if (tags.some(t => t.includes('superf'))) cond.tipus = 'superficial';
        } else if (k === 'tea') {
          if (tags.some(t => t.includes('nivell 3'))) cond.suport_nivell = 3;
          else if (tags.some(t => t.includes('nivell 2'))) cond.suport_nivell = 2;
          else if (tags.some(t => t.includes('nivell 1'))) cond.suport_nivell = 1;
          if (tags.some(t => t.includes('sensibilitat'))) cond.sensibilitat_sensorial = true;
        } else if (k === 'di') {
          if (tags.some(t => t.includes('signi'))) cond.grau = 'sever';
          else if (tags.some(t => t.includes('moder'))) cond.grau = 'moderat';
          else if (tags.some(t => t.includes('lleu'))) cond.grau = 'lleu';
        } else if (k === 'altes_capacitats') {
          cond.tipus = data.tags[0] || '';
        } else if (k === 'discapacitat_auditiva') {
          if (tags.some(t => t.includes('lsc'))) cond.comunicacio = 'LSC';
          if (tags.some(t => t.includes('sever'))) cond.grau = 'sever';
          else if (tags.some(t => t.includes('moder'))) cond.grau = 'moderat';
          else if (tags.some(t => t.includes('lleu'))) cond.grau = 'lleu';
        } else if (k === 'discapacitat_visual') {
          if (tags.some(t => t.includes('ceguesa'))) cond.grau = 'ceguesa';
          else if (tags.some(t => t.includes('baixa'))) cond.grau = 'baixa_visio';
          if (tags.some(t => t.includes('braille'))) cond.usa_braille = true;
        } else if (k === 'tdl') {
          if (tags.some(t => t.includes('recept'))) cond.modalitat = 'comprensiu';
          if (tags.some(t => t.includes('sem'))) cond.semantica = true;
          if (tags.some(t => t.includes('morf'))) cond.morfosintaxi = true;
          if (tags.some(t => t.includes('prag'))) cond.pragmatica = true;
        }
      }
      conds.push(cond);
    }

    // Via observable: les conductes marcades pel docent activen condicions
    // implícites quan no estan ja declarades via diagnòstic. Permet adaptar
    // sense necessitat d'informe clínic.
    const observed = formData.behaviors_observed || [];
    for (const behKey of observed) {
      const map = BEHAVIOR_TO_CONDITION[behKey];
      if (!map) continue;
      if (declaredKeys.has(map.key)) continue; // declarada guanya
      // Evita duplicar si ja l'ha posat una altra conducta
      if (conds.find(c => c.key === map.key && c.via === 'observable')) continue;
      conds.push({ key: map.key, via: 'observable', from_behavior: behKey });
    }

    return createProfile({
      source: formData.type === 'group' ? 'taller-group' : 'taller-person',
      type: formData.type === 'group' ? 'group' : 'person',
      name: formData.name,
      course: formData.course,
      course_base: formData.course_base || formData.course,
      multi_courses: formData.multi_courses || [],
      avatar: formData.avatar,
      conditions: conds,
      behaviors: formData.behaviors,
      aids: formData.aids,
      mecr_override: formData.mecr_override,
      group_composition: formData.group_composition,
      custom: true,
    });
  }

  // ── Normalitza un perfil legacy (qualsevol forma) cap al canònic ──────────
  // Tracta perfils antics desats al localStorage o al codi (demos).
  function normalizeLegacy(p) {
    if (!p || typeof p !== 'object') return null;
    // Si ja sembla canònic (té conditions [] amb objectes {key,...})
    const looksCanonical = Array.isArray(p.conditions)
      && p.conditions.length > 0
      && typeof p.conditions[0] === 'object'
      && p.conditions[0] !== null
      && typeof p.conditions[0].key === 'string';
    if (looksCanonical) {
      // Re-enriqueix nouvingut per si la metadata L1 ha canviat
      const conds = p.conditions.map(c => {
        const out = Object.assign({}, c);
        if (out.key === 'nouvingut') enrichNouvingut(out);
        return out;
      });
      return Object.assign({}, p, { conditions: conds });
    }

    // Forma legacy: conditions = ['nouvingut'] (strings) + subvariables niades
    if (Array.isArray(p.conditions) && p.conditions.length > 0 && typeof p.conditions[0] === 'string') {
      return fromTallerForm({
        type: p.type,
        name: p.name,
        course: p.course,
        course_base: p.course_base || p.course,
        multi_courses: p.multi_courses,
        avatar: p.avatar,
        conditions: p.conditions,
        subvariables: p.subvariables || {},
        behaviors: p.behaviors,
        aids: p.aids,
        mecr_override: p.mecr_override,
        group_composition: p.group_composition,
      });
    }

    // Demo legacy: cat/chips/behaviors/aids però sense conditions estructurades.
    // Inferim condicions de cat (i chips si grup).
    const inferred = [];
    const catToKey = {
      tdah: 'tdah', disl: 'dislexia', cat: 'nouvingut', ac: 'altes_capacitats',
      tea: 'tea',
    };
    if (p.type === 'group' && Array.isArray(p.chips)) {
      for (const ch of p.chips) {
        const k = catToKey[ch && ch.cat];
        if (k && !inferred.find(c => c.key === k)) inferred.push({ key: k });
      }
    } else {
      const k = catToKey[p.cat];
      if (k) {
        const c = { key: k };
        if (k === 'nouvingut') {
          if (p.l1) c.l1 = p.l1;
          if (p.mesos_catalunya != null) c.mesos_num = p.mesos_catalunya;
        }
        inferred.push(c);
      }
    }
    // Si tenim subvariables planes a l'arrel del demo, fusionar-les
    const sv = p.subvariables || {};
    for (const cond of inferred) {
      if (sv[cond.key]) {
        Object.assign(cond, sv[cond.key]);
        if (cond.key === 'nouvingut') enrichNouvingut(cond);
      } else if (cond.key === 'nouvingut') {
        enrichNouvingut(cond);
      }
    }

    return createProfile({
      id: p.id,
      source: p.demo ? 'demo' : (p.source || 'unknown'),
      type: p.type,
      name: p.name,
      course: p.course,
      course_base: p.course_base || p.course,
      avatar: p.avatar,
      conditions: inferred,
      behaviors: p.behaviors,
      aids: p.aids,
      custom: !!p.custom,
      demo: !!p.demo,
    });
  }

  // ── Magatzem unificat: clau compartida entre Flash i Taller ───────────────
  // Tota la sessió ATNE té un únic perfil actiu. Aquesta clau el conté en
  // forma canònica perquè qualsevol pàgina (Flash, pas1, pas2, pas3) pugui
  // llegir-lo i continuar el flux sense perdre detall.
  const STORAGE_KEY_ACTIVE = 'atne.profile_active';

  function saveActiveProfile(profile) {
    if (!profile) return;
    try {
      const canonical = profile && profile.conditions && Array.isArray(profile.conditions) && profile.conditions[0]?.key
        ? profile
        : normalizeLegacy(profile);
      if (canonical) localStorage.setItem(STORAGE_KEY_ACTIVE, JSON.stringify(canonical));
    } catch (e) { /* ignore */ }
  }

  function loadActiveProfile() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY_ACTIVE);
      if (!raw) return null;
      const p = JSON.parse(raw);
      // Re-normalitza per si la metadata del catàleg L1_META ha evolucionat
      return normalizeLegacy(p);
    } catch (e) { return null; }
  }

  function clearActiveProfile() {
    try { localStorage.removeItem(STORAGE_KEY_ACTIVE); } catch (e) {}
  }

  // ── API pública ───────────────────────────────────────────────────────────
  // Exposat com a `ATNE_PROFILE_MODEL` per evitar col·lisions amb codi antic
  // que feia servir `window.ATNE_PROFILE` per altres usos.
  window.ATNE_PROFILE_MODEL = {
    // Constants
    CONDITION_KEYS,
    CONDITION_LABEL,
    COURSE_TO_MECR,
    MECR_LADDER,
    CURS_TO_API,
    L1_META,

    // Util
    normalizeKey,
    isCanonicalKey,
    mesosRangeToNum,

    // Factory
    create: createProfile,

    // Adapters
    fromFlashForm,
    fromTallerForm,
    normalizeLegacy,

    // Derivacions
    deriveMECR,
    deriveCardView,
    deriveBehaviorsAndAids,

    // Mappers
    toBackendProfile,

    // Magatzem unificat
    STORAGE_KEY_ACTIVE,
    saveActiveProfile,
    loadActiveProfile,
    clearActiveProfile,
  };
})();
