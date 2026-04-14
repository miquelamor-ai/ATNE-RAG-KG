/* ATNE — Lògica frontend */

// ── Definició de característiques (data-driven) ────────────────────────────

const CHARACTERISTICS = {
    nouvingut: {
        label: "Nouvingut",
        subtipus: "contextual",
        subvars: [
            { id: "L1", label: "Llengua materna (L1)", type: "text", placeholder: "Ex: àrab, urdú, xinès..." },
            { id: "familia_linguistica", label: "Família lingüística", type: "select",
              options: ["romanica", "germanica", "eslava", "araboberber", "sinotibetana", "altra"] },
            { id: "alfabet_llati", label: "Alfabet llatí", type: "select", options: ["true", "false"],
              labels: ["Sí", "No"] },
            { id: "escolaritzacio_previa", label: "Escolarització prèvia", type: "select",
              options: ["si", "parcial", "no"] },
            { id: "mecr", label: "Nivell català (MECR)", type: "select",
              options: ["pre-A1", "A1", "A2", "B1", "B2"] },
            { id: "calp", label: "Llengua acadèmica (CALP)", type: "select",
              options: ["inicial", "emergent", "consolidat"] },
        ]
    },
    tea: {
        label: "TEA",
        subtipus: "constitutiva",
        subvars: [
            { id: "nivell_suport", label: "Nivell suport (DSM-5)", type: "select",
              options: ["1", "2", "3"] },
            { id: "comunicacio_oral", label: "Comunicació oral", type: "select",
              options: ["fluida", "limitada", "no_verbal"] },
        ]
    },
    tdah: {
        label: "TDAH",
        subtipus: "constitutiva",
        subvars: [
            { id: "presentacio", label: "Presentació (DSM-5)", type: "select",
              options: ["inatent", "hiperactiu", "combinat"] },
            { id: "grau", label: "Grau de suport", type: "select",
              options: ["lleu", "moderat", "sever"] },
            { id: "baixa_memoria_treball", label: "Baixa memòria de treball", type: "select",
              options: ["false", "true"], labels: ["No", "Sí"] },
            { id: "fatiga_cognitiva", label: "Fatiga cognitiva", type: "select",
              options: ["false", "true"], labels: ["No", "Sí"] },
        ]
    },
    dislexia: {
        label: "Dislèxia",
        subtipus: "constitutiva",
        subvars: [
            { id: "tipus_dislexia", label: "Tipus (ruta afectada)", type: "select",
              options: ["fonologica", "superficial", "mixta"] },
            { id: "grau", label: "Grau de severitat", type: "select",
              options: ["lleu", "moderat", "sever"] },
            { id: "tipografia_adaptada", label: "Tipografia adaptada", type: "select",
              options: ["false", "true"], labels: ["No", "Sí"] },
            { id: "columnes_estretes", label: "Columnes estretes (màx. 44 car.)", type: "select",
              options: ["false", "true"], labels: ["No", "Sí"] },
        ]
    },
    altes_capacitats: {
        label: "Altes capacitats",
        subtipus: "constitutiva",
        subvars: [
            { id: "tipus_capacitat", label: "Tipus", type: "select",
              options: ["global", "talent_especific"] },
        ]
    },
    di: {
        label: "Discapacitat intel·lectual",
        subtipus: "constitutiva",
        subvars: [
            { id: "grau", label: "Grau", type: "select", options: ["lleu", "moderat", "sever"] },
        ]
    },
    tdl: {
        label: "TDL (Trastorn del Llenguatge)",
        subtipus: "constitutiva",
        subvars: [
            { id: "modalitat", label: "Modalitat afectada", type: "select",
              options: ["comprensiu", "expressiu", "mixt"] },
            { id: "morfosintaxi", label: "Morfosintaxi afectada", type: "select",
              options: ["false", "true"], labels: ["No", "Sí"] },
            { id: "semantica", label: "Semàntica/lèxic afectat", type: "select",
              options: ["false", "true"], labels: ["No", "Sí"] },
            { id: "pragmatica", label: "Pragmàtica afectada", type: "select",
              options: ["false", "true"], labels: ["No", "Sí"] },
            { id: "discurs_narrativa", label: "Discurs/narrativa afectat", type: "select",
              options: ["false", "true"], labels: ["No", "Sí"] },
            { id: "comprensio_lectora", label: "Comprensió lectora afectada", type: "select",
              options: ["false", "true"], labels: ["No", "Sí"] },
            { id: "grau", label: "Grau de severitat", type: "select",
              options: ["lleu", "moderat", "sever"] },
            { id: "bilingue", label: "Context bilingüe/plurilingüe", type: "select",
              options: ["false", "true"], labels: ["No", "Sí"] },
        ]
    },
    tdc: {
        label: "TDC / Dispraxia",
        subtipus: "constitutiva",
        subvars: [
            { id: "grau", label: "Grau de severitat", type: "select",
              options: ["lleu", "moderat", "sever"] },
            { id: "motricitat_fina", label: "Motricitat fina afectada", type: "select",
              options: ["false", "true"], labels: ["No", "Sí"] },
            { id: "motricitat_grossa", label: "Motricitat grossa afectada", type: "select",
              options: ["false", "true"], labels: ["No", "Sí"] },
            { id: "acces_teclat", label: "Accés teclat com a alternativa", type: "select",
              options: ["true", "false"], labels: ["Sí", "No"] },
        ]
    },
    disc_visual: {
        label: "Discapacitat visual",
        subtipus: "constitutiva",
        subvars: [
            { id: "grau", label: "Grau", type: "select",
              options: ["baixa_visio_moderada", "baixa_visio_greu", "ceguesa"],
              labels: ["Baixa visió moderada", "Baixa visió greu", "Ceguesa"] },
        ]
    },
    disc_auditiva: {
        label: "Discapacitat auditiva",
        subtipus: "constitutiva",
        subvars: [
            { id: "comunicacio", label: "Comunicació", type: "select",
              options: ["oral", "LSC", "bimodal"] },
            { id: "implant_coclear", label: "Implant coclear", type: "select",
              options: ["false", "true"], labels: ["No", "Sí"] },
        ]
    },
    disc_motora: {
        label: "Discapacitat motora",
        subtipus: "constitutiva",
        subvars: [
            { id: "acces_teclat", label: "Accés teclat/pantalla", type: "select",
              options: ["true", "false"], labels: ["Sí", "No"] },
        ]
    },
    vulnerabilitat: {
        label: "Vulnerabilitat socioeducativa",
        subtipus: "contextual",
        subvars: [
            { id: "sensibilitat_tematica", label: "Sensibilitat temàtica (trauma)", type: "select",
              options: ["false", "true"], labels: ["No", "Sí — evitar temes sensibles"] },
        ]
    },
    trastorn_emocional: {
        label: "Trastorn emocional / conducta",
        subtipus: "contextual",
        subvars: [
            { id: "sensibilitat_tematica", label: "Sensibilitat temàtica (trauma)", type: "select",
              options: ["false", "true"], labels: ["No", "Sí — evitar temes sensibles"] },
        ]
    },
};

// ── Opcions dinàmiques per etapa ──────────────────────────────────────────

const CURSOS_PER_ETAPA = {
    infantil: [
        { value: "P3", label: "P3" },
        { value: "P4", label: "P4" },
        { value: "P5", label: "P5" },
    ],
    primaria: [
        { value: "1r", label: "1r" },
        { value: "2n", label: "2n" },
        { value: "3r", label: "3r" },
        { value: "4t", label: "4t" },
        { value: "5e", label: "5è" },
        { value: "6e", label: "6è" },
    ],
    ESO: [
        { value: "1r", label: "1r" },
        { value: "2n", label: "2n" },
        { value: "3r", label: "3r" },
        { value: "4t", label: "4t" },
    ],
    batxillerat: [
        { value: "1r", label: "1r" },
        { value: "2n", label: "2n" },
    ],
    FP: [
        { value: "1r_CFGB", label: "1r Grau Bàsic (CFGB)" },
        { value: "2n_CFGB", label: "2n Grau Bàsic (CFGB)" },
        { value: "1r_CGM", label: "1r Grau Mitjà (CFGM)" },
        { value: "2n_CGM", label: "2n Grau Mitjà (CFGM)" },
        { value: "1r_CGS", label: "1r Grau Superior (CFGS)" },
        { value: "2n_CGS", label: "2n Grau Superior (CFGS)" },
    ],
};

// Nomenclatura oficial: Decret 21/2023 (Infantil), Decret 175/2022 (Primària+ESO),
// Decret 171/2022 (Batxillerat). FP: famílies professionals + transversals.
const AMBITS_PER_ETAPA = {
    // Decret 21/2023 — 4 eixos de desenvolupament i aprenentatge
    infantil: [
        { value: "creixement_autonomia", label: "Un infant que creix amb autonomia i confiança" },
        { value: "comunicacio_llenguatges", label: "Un infant que es comunica amb diferents llenguatges" },
        { value: "descoberta_entorn", label: "Un infant que descobreix l'entorn amb curiositat" },
        { value: "diversitat_mon", label: "Un infant que forma part de la diversitat del món" },
    ],
    // Decret 175/2022, Annex 2 — Àrees d'educació primària
    primaria: [
        { value: "llengua_literatura_cat", label: "Llengua Catalana i Literatura" },
        { value: "llengua_literatura_cas", label: "Llengua Castellana i Literatura" },
        { value: "llengua_estrangera", label: "Llengua Estrangera" },
        { value: "matematiques", label: "Matemàtiques" },
        { value: "coneixement_medi", label: "Coneixement del Medi Natural, Social i Cultural" },
        { value: "educacio_artistica", label: "Educació Artística" },
        { value: "educacio_fisica", label: "Educació Física" },
        { value: "educacio_valors", label: "Educació en Valors Cívics i Ètics" },
        { value: "religio", label: "Religió" },
        { value: "tutoria", label: "Tutoria" },
        { value: "aula_acollida", label: "Aula d'acollida" },
        { value: "siei", label: "SIEI (Suport Intensiu per a l'Escolarització Inclusiva)" },
    ],
    // Decret 175/2022, Annex 3 — Matèries d'ESO
    ESO: [
        { value: "llengua_literatura_cat", label: "Llengua Catalana i Literatura" },
        { value: "llengua_literatura_cas", label: "Llengua Castellana i Literatura" },
        { value: "llengua_estrangera", label: "Llengua Estrangera" },
        { value: "matematiques", label: "Matemàtiques" },
        { value: "biologia_geologia", label: "Biologia i Geologia" },
        { value: "fisica_quimica", label: "Física i Química" },
        { value: "ciencies_socials", label: "Ciències Socials: Geografia i Història" },
        { value: "tecnologia_digitalitzacio", label: "Tecnologia i Digitalització" },
        { value: "digitalitzacio", label: "Digitalització" },
        { value: "educacio_plastica", label: "Educació Plàstica, Visual i Audiovisual" },
        { value: "musica", label: "Música" },
        { value: "educacio_fisica", label: "Educació Física" },
        { value: "educacio_valors", label: "Educació en Valors Cívics i Ètics" },
        { value: "filosofia", label: "Filosofia" },
        { value: "economia", label: "Economia Bàsica" },
        { value: "emprenedoria", label: "Emprenedoria" },
        { value: "cultura_classica", label: "Cultura Clàssica" },
        { value: "llati", label: "Llatí: Llengua i Cultura" },
        { value: "arts_esceniques", label: "Arts Escèniques i Dansa" },
        { value: "fopp", label: "Formació i Orientació Personal i Professional" },
        { value: "robotica", label: "Robòtica i Programació" },
        { value: "segona_llengua", label: "Segona Llengua Estrangera" },
        { value: "tutoria", label: "Tutoria" },
        { value: "aula_acollida", label: "Aula d'acollida" },
        { value: "siei", label: "SIEI (Suport Intensiu per a l'Escolarització Inclusiva)" },
    ],
    // Decret 171/2022 — Modalitats + matèries comunes de batxillerat
    batxillerat: [
        { value: "mod_ciencies_tecnologia", label: "Modalitat: Ciències i Tecnologia" },
        { value: "mod_humanitats_socials", label: "Modalitat: Humanitats i Ciències Socials" },
        { value: "mod_arts", label: "Modalitat: Arts" },
        { value: "mod_general", label: "Modalitat: General" },
        { value: "llengua_literatura_cat", label: "Llengua Catalana i Literatura (comuna)" },
        { value: "llengua_literatura_cas", label: "Llengua Castellana i Literatura (comuna)" },
        { value: "llengua_estrangera", label: "Llengua Estrangera (comuna)" },
        { value: "filosofia", label: "Filosofia (comuna)" },
        { value: "historia", label: "Història (comuna)" },
        { value: "educacio_fisica", label: "Educació Física (comuna)" },
        { value: "tutoria", label: "Tutoria" },
    ],
    FP: [
        { value: "admin_gestio", label: "Administració i gestió" },
        { value: "comerc_marketing", label: "Comerç i màrqueting" },
        { value: "electricitat_electronica", label: "Electricitat i electrònica" },
        { value: "fabricacio_mecanica", label: "Fabricació mecànica" },
        { value: "hoteleria_turisme", label: "Hoteleria i turisme" },
        { value: "imatge_personal", label: "Imatge personal" },
        { value: "imatge_so", label: "Imatge i so" },
        { value: "industria_alimentaria", label: "Indústria alimentària" },
        { value: "informatica_comunicacions", label: "Informàtica i comunicacions" },
        { value: "installacio_manteniment", label: "Instal·lació i manteniment" },
        { value: "sanitat", label: "Sanitat" },
        { value: "serveis_socioculturals", label: "Serveis socioculturals i a la comunitat" },
        { value: "transport_vehicles", label: "Transport i manteniment de vehicles" },
        { value: "activitats_fisiques", label: "Activitats físiques i esportives" },
        { value: "arts_grafiques", label: "Arts gràfiques" },
        { value: "quimica", label: "Química" },
        { value: "edificacio_obra_civil", label: "Edificació i obra civil" },
        { value: "energia_aigua", label: "Energia i aigua" },
        { value: "fusta_moble", label: "Fusta, moble i suro" },
        { value: "maritimopesquera", label: "Marítimopesquera" },
        { value: "textil_confeccio", label: "Tèxtil, confecció i pell" },
        { value: "agraria", label: "Agrària" },
        { value: "seguretat_medi_ambient", label: "Seguretat i medi ambient" },
        { value: "vidre_ceramica", label: "Vidre i ceràmica" },
        { value: "arts_artesanies", label: "Arts i artesanies" },
        // Mòduls transversals (comuns a tots els cicles)
        { value: "fol", label: "Formació i Orientació Laboral (FOL)" },
        { value: "eie", label: "Empresa i Iniciativa Emprenedora (EIE)" },
        { value: "angles_tecnic", label: "Anglès tècnic" },
        { value: "tutoria", label: "Tutoria" },
    ],
};

const COMPLEMENTS = {
    glossari: "Glossari de termes clau",
    negretes: "Paraules clau en negreta",
    definicions_integrades: "Definicions integrades al text",
    traduccio_l1: "Traducció L1 dels termes clau",
    pictogrames: "Pictogrames / icones de suport",
    esquema_visual: "Esquema / resum visual",
    bastides: "Bastides (scaffolding guiat)",
    mapa_conceptual: "Mapa conceptual",
    preguntes_comprensio: "Preguntes de comprensió lectora",
    activitats_aprofundiment: "Activitats d'aprofundiment",
    mapa_mental: "Mapa mental",
    argumentacio_pedagogica: "Argumentació pedagògica",
};

// Agrupació epistemològica dels complements ("ajuts") per a la UI del Pas 3.
// Taxonomia unificada amb Saber-ne+ (Bloc 1 §5): Lèxics / Visuals / Estructurals
// / Síntesi / Comprensió / Ampliació, més "Docent" per a la transparència
// pedagògica (no és un ajut per a l'alumne).
//
// NOTA IMPORTANT: aquestes categories són d'AJUTS QUE S'AFEGEIXEN al text
// adaptat. NO són les categories de les instruccions d'adaptació (aquelles
// són les macrodirectives al backend: LÈXIC, SINTAXI, ESTRUCTURA, GESTIÓ,
// PROTECCIÓ, que descriuen com l'LLM transforma el text). Les categories
// d'AQUÍ són "què s'afegeix AL COSTAT del text", no "què fa l'LLM AL text".
//
// Referència taxonomia: Saber-ne+ §5 + projectes.xtec.cat/tilc
const COMPLEMENT_GROUPS = {
    "Ajuts lèxics": {
        cat: "lexic",
        icon: "list",
        desc: "Paraules i significat",
        items: [
            { key: "negretes", label: "Paraules clau destacades en negreta al text" },
            { key: "definicions_integrades", label: "Definicions curtes entre parèntesis al flux del text" },
            { key: "glossari", label: "Glossari al final amb termes i definicions simples" },
            { key: "traduccio_l1", label: "Traducció a la llengua materna (per a nouvinguts)" },
        ],
    },
    "Ajuts visuals": {
        cat: "visual",
        icon: "image",
        desc: "Suport icònic i multimodal",
        items: [
            { key: "pictogrames", label: "Pictogrames o icones al costat dels conceptes clau" },
        ],
    },
    "Ajuts estructurals": {
        cat: "estructura",
        icon: "schema",
        desc: "Organització visible del contingut",
        items: [
            { key: "esquema_visual", label: "Esquema o diagrama de l'estructura del text" },
        ],
    },
    "Ajuts de síntesi": {
        cat: "sintesi",
        icon: "hub",
        desc: "Xarxes de conceptes i relacions",
        items: [
            { key: "mapa_conceptual", label: "Mapa conceptual — nodes + relacions (ESO endavant)" },
            { key: "mapa_mental", label: "Mapa mental — esquema radial creatiu" },
        ],
    },
    "Ajuts de comprensió": {
        cat: "comprensio",
        icon: "quiz",
        desc: "Verificació i suports (ZDP, Vygotsky)",
        items: [
            { key: "preguntes_comprensio", label: "Preguntes graduades (MALL/TILC: 3 moments × 3 nivells)" },
            { key: "bastides", label: "Bastides: suports progressius (connectors, frases model, banc paraules)" },
        ],
    },
    "Ajuts d'ampliació": {
        cat: "ampliacio",
        icon: "rocket_launch",
        desc: "Repte cognitiu i anar més enllà",
        items: [
            { key: "activitats_aprofundiment", label: "Activitats d'aprofundiment: connexions, recerca, debat" },
        ],
    },
    "Transparència docent": {
        cat: "docent",
        icon: "psychology",
        desc: "Per al docent, no per a l'alumne",
        items: [
            { key: "argumentacio_pedagogica", label: "Justificació pedagògica de les decisions d'adaptació" },
        ],
    },
};


// ── Estat de l'aplicació ───────────────────────────────────────────────────

const state = {
    step: 1,
    adaptedText: "",
    originalText: "",
    historyId: null,       // ID de l'entrada a Supabase history
    feedbackRating: null,  // 1=dolenta, 2=regular, 3=bona
};

let _historyLoaded = false; // cache flag historial


// ── Inicialització ─────────────────────────────────────────────────────────

document.addEventListener("DOMContentLoaded", () => {
    renderCharGrid();
    renderComplementGrid();
    renderObservableBehaviors();
    renderAjutsList();
    loadContextFromStorage();
    updateEtapaSelects(); // Sincronitzar cursos/àmbits amb l'etapa carregada
    loadProfileList();
    checkHealth();
    bindEvents();
    updateMecrPreview();
    updateStickyBar();
    updateAsideProgress();
});


// ── Via observable: estat i renderitzat ────────────────────────────────────

// Via actualment activa: 'observable' (default) o 'diagnostic'
let currentVia = "observable";

// Set d'ajuts marcats manualment pel docent (per distingir dels automàtics)
const manualAjuts = new Set();
// Set d'ajuts marcats manualment com a exclosos (per si el docent desmarca un automàtic)
const suppressedAjuts = new Set();

function renderObservableBehaviors() {
    const container = document.getElementById("observable-behaviors");
    if (!container || !window.ObservableMapping) return;

    const items = Object.entries(window.ObservableMapping.BEHAVIORS);
    container.innerHTML = items.map(([bid, beh]) => `
        <label class="behavior-item">
            <input type="checkbox" data-behavior="${bid}">
            <span>${beh.label}</span>
        </label>
    `).join("");

    container.querySelectorAll('input[type="checkbox"][data-behavior]').forEach(cb => {
        cb.addEventListener("change", () => {
            syncAjutsFromBehaviors();
            updateMecrPreview();
        });
    });
}

function renderAjutsList() {
    const container = document.getElementById("ajuts-list");
    if (!container || !window.ObservableMapping) return;

    const ajuts = window.ObservableMapping.AJUTS;
    const grups = window.ObservableMapping.AJUT_GRUPS;

    // Agrupar per grup
    const perGrup = {};
    for (const [aid, ajut] of Object.entries(ajuts)) {
        if (!perGrup[ajut.grup]) perGrup[ajut.grup] = [];
        perGrup[ajut.grup].push({ id: aid, label: ajut.label });
    }

    let html = "";
    for (const [grupKey, grupLabel] of Object.entries(grups)) {
        const items = perGrup[grupKey] || [];
        if (!items.length) continue;
        html += `<div class="ajut-grup">
            <div class="ajut-grup-label">${grupLabel}</div>
            ${items.map(it => `
                <label class="ajut-item">
                    <input type="checkbox" data-ajut="${it.id}">
                    <span>${it.label}</span>
                </label>
            `).join("")}
        </div>`;
    }
    container.innerHTML = html;

    // Marcar manualment quan el docent toca
    container.querySelectorAll('input[type="checkbox"][data-ajut]').forEach(cb => {
        cb.addEventListener("change", () => {
            const aid = cb.dataset.ajut;
            if (cb.checked) {
                manualAjuts.add(aid);
                suppressedAjuts.delete(aid);
            } else {
                manualAjuts.delete(aid);
                // Si la conducta que l'havia activat encara està marcada,
                // registrem que el docent el vol explícitament fora.
                if (isAjutAutoActive(aid)) suppressedAjuts.add(aid);
            }
        });
    });
}

function isAjutAutoActive(ajutId) {
    // Retorna true si alguna conducta marcada l'activa automàticament
    const active = getActiveBehaviorIds();
    const { ajutsAutomatics } = window.ObservableMapping.behaviorsToProfile(active);
    return ajutsAutomatics.has(ajutId);
}

function getActiveBehaviorIds() {
    return Array.from(
        document.querySelectorAll('#observable-behaviors input[type="checkbox"]:checked')
    ).map(cb => cb.dataset.behavior);
}

function syncAjutsFromBehaviors() {
    // Quan es marca/desmarca una conducta, ajustem els ajuts:
    //  - automàtics: segueixen el que digui el mapping
    //  - manuals: no els tocaems
    //  - suprimits manualment: queden fora tot i que siguin auto
    const active = getActiveBehaviorIds();
    const { ajutsAutomatics } = window.ObservableMapping.behaviorsToProfile(active);

    document.querySelectorAll('#ajuts-list input[type="checkbox"][data-ajut]').forEach(cb => {
        const aid = cb.dataset.ajut;
        const isAuto = ajutsAutomatics.has(aid);
        const isManual = manualAjuts.has(aid);
        const isSuppressed = suppressedAjuts.has(aid);

        cb.checked = (isAuto && !isSuppressed) || isManual;
    });
}

function getSelectedAjutIds() {
    return Array.from(
        document.querySelectorAll('#ajuts-list input[type="checkbox"][data-ajut]:checked')
    ).map(cb => cb.dataset.ajut);
}

function getDesfase() {
    const r = document.querySelector('input[name="desfase"]:checked');
    return r ? parseInt(r.value, 10) : 0;
}

function updateMecrPreview() {
    if (!window.ObservableMapping) return;
    const etapa = document.getElementById("ctx-etapa").value;
    const curs = document.getElementById("ctx-curs").value;
    const desfase = getDesfase();
    const mecr = window.ObservableMapping.computeMecr(etapa, curs, desfase);
    const ref = window.ObservableMapping.getMecrReferencia(etapa, curs);

    // Alumne individual
    const preview = document.getElementById("mecr-preview-value");
    if (preview) {
        preview.textContent = desfase === 0
            ? `${mecr} (nivell del curs)`
            : `${mecr} (desplaçat des de ${ref})`;
    }

    // Grup: 3 nivells
    const low = document.getElementById("grup-mecr-low");
    const mid = document.getElementById("grup-mecr-mid");
    const high = document.getElementById("grup-mecr-high");
    if (low && mid && high) {
        low.textContent = window.ObservableMapping.computeMecr(etapa, curs, -1);
        mid.textContent = ref;
        high.textContent = window.ObservableMapping.computeMecr(etapa, curs, 1);
    }
}

function setVia(via) {
    currentVia = via;
    // La via diagnòstic ara és un <details>, s'obre/tanca sola.
    // La via observable sempre visible — el diagnostic és un desplegable secundari.
    // currentVia es determina per si hi ha conductes marcades o si el details diagnostic està obert.
}

function updateCurrentVia() {
    const diagPanel = document.getElementById("via-diagnostic-panel");
    const hasBehaviors = getActiveBehaviorIds().length > 0;
    const diagOpen = diagPanel && diagPanel.open;
    // Si té conductes marcades O el diagnòstic està tancat, usem observable.
    // Si el diagnòstic està obert i no hi ha conductes, usem diagnostic.
    currentVia = (diagOpen && !hasBehaviors) ? "diagnostic" : "observable";
}


// ── Actualitzar selects dinàmics per etapa ─────────────────────────────────

function updateEtapaSelects() {
    const etapa = document.getElementById("ctx-etapa").value;

    // Actualitzar cursos
    const cursSelect = document.getElementById("ctx-curs");
    const cursActual = cursSelect.value;
    const cursos = CURSOS_PER_ETAPA[etapa] || [];
    cursSelect.innerHTML = cursos.map(c =>
        `<option value="${c.value}">${c.label}</option>`
    ).join("");
    // Intentar mantenir el curs seleccionat si existeix a la nova etapa
    if (cursos.some(c => c.value === cursActual)) {
        cursSelect.value = cursActual;
    }

    // Actualitzar àmbits
    const ambitSelect = document.getElementById("ctx-ambit");
    const ambitActual = ambitSelect.value;
    const ambits = AMBITS_PER_ETAPA[etapa] || [];
    ambitSelect.innerHTML = ambits.map(a =>
        `<option value="${a.value}">${a.label}</option>`
    ).join("");
    if (ambits.some(a => a.value === ambitActual)) {
        ambitSelect.value = ambitActual;
    }

    // Canviar etiquetes segons etapa
    const ambitLabel = document.querySelector('label[for="ctx-ambit"]');
    if (ambitLabel) {
        ambitLabel.textContent = etapa === "FP" ? "Família professional" : "Àmbit";
    }
    const materiaLabel = document.getElementById("ctx-materia-label");
    if (materiaLabel) {
        materiaLabel.textContent = etapa === "FP" ? "Mòdul / UF" : "Tema";
    }
    const materiaInput = document.getElementById("ctx-materia");
    if (materiaInput) {
        materiaInput.placeholder = etapa === "FP"
            ? "Ex: FOL, Sistemes informàtics..."
            : "Ex: La fotosíntesi, La Revolució Francesa...";
    }
}

// ── Health check ───────────────────────────────────────────────────────────

async function checkHealth() {
    try {
        const resp = await fetch("/api/health");
        const data = await resp.json();
        document.getElementById("dot-supabase").className =
            "health-dot " + (data.supabase ? "ok" : "err");
        document.getElementById("dot-gemini").className =
            "health-dot " + (data.gemini ? "ok" : "err");
    } catch {
        document.getElementById("dot-supabase").className = "health-dot err";
        document.getElementById("dot-gemini").className = "health-dot err";
    }
}


// ── Navegació per passos ───────────────────────────────────────────────────

function goToStep(n) {
    state.step = n;
    document.querySelectorAll(".step-tab").forEach(tab => {
        tab.classList.toggle("active", parseInt(tab.dataset.step) === n);
    });
    // Aside steps (Stitch shell v2)
    document.querySelectorAll(".aside-step").forEach(step => {
        step.classList.toggle("active", parseInt(step.dataset.step) === n);
    });
    document.querySelectorAll(".step-panel").forEach(panel => {
        panel.classList.toggle("active", panel.id === `step-${n}`);
    });
    if (n === 3) requestProposal();
    if (n === 2) updateContextPill();
    updateStickyBar();
    updateAsideProgress();
}

function updateAsideProgress() {
    const n = state.step;
    const fill = document.getElementById("aside-progress-fill");
    const text = document.getElementById("aside-progress-text");
    if (fill) fill.style.width = `${n * 25}%`;
    if (text) {
        const labels = {
            1: "Pas 1 de 4: Context i Perfil",
            2: "Pas 2 de 4: Entrada de Text",
            3: "Pas 3 de 4: Adaptació",
            4: "Pas 4 de 4: Resultats",
        };
        text.textContent = labels[n] || "";
    }
}

function goToPrevStep() {
    if (state.step > 1) goToStep(state.step - 1);
}

function goToNextStep() {
    if (state.step === 4) {
        // Al pas 4, "Continuar" = "Nova adaptació" (torna al pas 1)
        goToStep(1);
    } else if (state.step === 3) {
        // Al pas 3, "Continuar" = "Adaptar"
        runAdaptation();
    } else if (state.step < 4) {
        goToStep(state.step + 1);
    }
}

function updateStickyBar() {
    const n = state.step;
    const label = document.getElementById("sticky-step-label");
    const fill = document.getElementById("sticky-progress-fill");
    const btnBack = document.getElementById("btn-back");
    const btnNext = document.getElementById("btn-next");

    if (label) {
        label.textContent = `Pas ${n} de 4`;
        label.removeAttribute("hidden");
        label.dataset.progress = String(n);
    }
    if (fill) fill.style.width = `${n * 25}%`;
    if (btnBack) btnBack.style.visibility = n === 1 ? "hidden" : "visible";

    if (btnNext) {
        // Preservar estructura: span.btn-label + icon
        const labelSpan = btnNext.querySelector(".btn-label");
        const icon = btnNext.querySelector(".material-symbols-outlined");
        let text = "Continuar";
        let cls = "sticky-bar-v2-btn";
        if (n === 3) {
            text = "Adaptar";
            cls = "sticky-bar-v2-btn sticky-bar-v2-btn-ok";
        } else if (n === 4) {
            text = "Nova adaptació";
        }
        if (labelSpan) labelSpan.textContent = text;
        btnNext.className = cls;
        // Assegurar que l'icona no s'ha perdut
        if (!icon && labelSpan) {
            const newIcon = document.createElement("span");
            newIcon.className = "material-symbols-outlined";
            newIcon.textContent = "arrow_forward";
            btnNext.appendChild(newIcon);
        }
    }
}


// ── Renderitzar grid de característiques ───────────────────────────────────

function renderCharGrid() {
    const grid = document.getElementById("char-grid");
    grid.innerHTML = "";

    for (const [key, char] of Object.entries(CHARACTERISTICS)) {
        const div = document.createElement("div");
        div.className = "char-item";
        div.dataset.key = key;

        let subvarsHTML = "";
        if (char.subvars.length > 0) {
            const rows = char.subvars.map(sv => {
                if (sv.type === "select") {
                    const opts = sv.options.map((o, i) => {
                        const label = sv.labels ? sv.labels[i] : o;
                        return `<option value="${o}">${label}</option>`;
                    }).join("");
                    return `<div class="subvar-row">
                        <label>${sv.label}</label>
                        <select data-char="${key}" data-var="${sv.id}">${opts}</select>
                    </div>`;
                } else {
                    return `<div class="subvar-row">
                        <label>${sv.label}</label>
                        <input type="text" data-char="${key}" data-var="${sv.id}"
                               placeholder="${sv.placeholder || ''}">
                    </div>`;
                }
            }).join("");
            subvarsHTML = `<div class="char-subvars">${rows}</div>`;
        }

        div.innerHTML = `
            <label>
                <input type="checkbox" data-char="${key}">
                ${char.label}
            </label>
            ${subvarsHTML}
        `;

        const cb = div.querySelector('input[type="checkbox"]');
        cb.addEventListener("change", () => {
            div.classList.toggle("checked", cb.checked);
            check2eAlert();
        });

        grid.appendChild(div);
    }
}


// ── Detecció doble excepcionalitat (2e) ──────────────────────────────────────

function check2eAlert() {
    const acChecked = document.querySelector('input[type="checkbox"][data-char="altes_capacitats"]')?.checked;
    const otherChars = Object.keys(CHARACTERISTICS).filter(k => k !== 'altes_capacitats');
    const otherActive = otherChars.some(k =>
        document.querySelector(`input[type="checkbox"][data-char="${k}"]`)?.checked
    );

    let alertDiv = document.getElementById("alert-2e");
    if (acChecked && otherActive) {
        if (!alertDiv) {
            alertDiv = document.createElement("div");
            alertDiv.id = "alert-2e";
            alertDiv.className = "alert-2e";
            alertDiv.innerHTML = `
                <strong>Perfil 2e detectat — Doble excepcionalitat</strong>
                <p>Has seleccionat altes capacitats combinada amb una altra condició.
                Això és el que es coneix com a <strong>doble excepcionalitat (2e)</strong>:
                un perfil propi on el potencial i les dificultats s'emmascaren mútuament.
                L'alumne pot semblar "normal" quan internament lluita amb reptes i avorriment alhora.</p>
                <p>L'adaptació mantindrà el <strong>repte cognitiu alt</strong> però amb el
                <strong>format adaptat</strong> a la condició associada.</p>
            `;
            document.getElementById("char-grid").after(alertDiv);
        }
    } else if (alertDiv) {
        alertDiv.remove();
    }
}


// ── Renderitzar grid de complements ────────────────────────────────────────

function renderComplementGrid() {
    const grid = document.getElementById("complement-grid");
    if (!grid) return;
    grid.innerHTML = "";

    for (const [groupLabel, group] of Object.entries(COMPLEMENT_GROUPS)) {
        const groupDiv = document.createElement("div");
        groupDiv.className = "complement-group";
        groupDiv.dataset.cat = group.cat;
        groupDiv.innerHTML = `
            <div class="complement-group-header">
                <span class="complement-group-icon material-symbols-outlined">${group.icon}</span>
                <div class="complement-group-meta">
                    <div class="complement-group-label">${groupLabel}</div>
                    <div class="complement-group-desc">${group.desc}</div>
                </div>
            </div>
        `;

        const list = document.createElement("div");
        list.className = "complement-group-list";

        for (const item of group.items) {
            list.innerHTML += `
                <label class="complement-item" id="comp-${item.key}">
                    <input type="checkbox" data-comp="${item.key}">
                    <span class="complement-text">${item.label}</span>
                    <span class="complement-auto-badge">Automàtic</span>
                </label>
            `;
        }

        groupDiv.appendChild(list);
        grid.appendChild(groupDiv);
    }

    // Listener: quan el docent toca un checkbox, treu el badge "Automàtic"
    grid.querySelectorAll('input[data-comp]').forEach(cb => {
        cb.addEventListener('change', () => {
            cb.closest('.complement-item').classList.remove('auto');
        });
    });
}


// ── Recollir perfil del formulari ──────────────────────────────────────────

function collectProfile() {
    // Via observable: construir caracteristiques a partir de les conductes
    if (currentVia === "observable") {
        const behaviorIds = getActiveBehaviorIds();
        const { caracteristiques: fromBehaviors } =
            window.ObservableMapping.behaviorsToProfile(behaviorIds);

        // Inicialitzem totes les claus conegudes amb actiu=false (per compat amb server)
        const caracteristiques = {};
        for (const key of Object.keys(CHARACTERISTICS)) {
            caracteristiques[key] = { actiu: false };
        }
        // Copiem les activades per les conductes
        for (const [key, data] of Object.entries(fromBehaviors)) {
            caracteristiques[key] = data;
        }

        return {
            nom: document.getElementById("profile-nom").value || "Sense nom",
            caracteristiques,
            canal_preferent: document.getElementById("profile-canal").value,
            observacions: document.getElementById("profile-obs").value,
            _via: "observable",
            _behaviors: behaviorIds,
            _ajuts: getSelectedAjutIds(),
            _desfase: getDesfase(),
        };
    }

    // Via diagnòstic (original)
    const caracteristiques = {};
    for (const key of Object.keys(CHARACTERISTICS)) {
        const cb = document.querySelector(`input[type="checkbox"][data-char="${key}"]`);
        if (!cb) { caracteristiques[key] = { actiu: false }; continue; }
        const entry = { actiu: cb.checked };
        if (cb.checked) {
            document.querySelectorAll(`[data-char="${key}"][data-var]`).forEach(el => {
                let val = el.value;
                if (val === "true") val = true;
                else if (val === "false") val = false;
                entry[el.dataset.var] = val;
            });
        }
        caracteristiques[key] = entry;
    }
    return {
        nom: document.getElementById("profile-nom").value || "Sense nom",
        caracteristiques,
        canal_preferent: document.getElementById("profile-canal").value,
        observacions: document.getElementById("profile-obs").value,
        _via: "diagnostic",
    };
}


// ── Recollir context docent ────────────────────────────────────────────────

function collectContext() {
    const aulaRadio = document.querySelector('input[name="ctx-aula"]:checked');
    const aulaHidden = document.querySelector('input[name="ctx-aula"][type="hidden"]');
    return {
        etapa: document.getElementById("ctx-etapa").value,
        curs: document.getElementById("ctx-curs").value,
        ambit: document.getElementById("ctx-ambit").value,
        materia: document.getElementById("ctx-materia").value,
        tipus_aula: aulaRadio ? aulaRadio.value : (aulaHidden ? aulaHidden.value : "ordinaria"),
    };
}


// ── Persistir context a localStorage ───────────────────────────────────────

function saveContextToStorage() {
    localStorage.setItem("atne_context", JSON.stringify(collectContext()));
}

function loadContextFromStorage() {
    try {
        const ctx = JSON.parse(localStorage.getItem("atne_context"));
        if (!ctx) return;
        if (ctx.etapa) {
            document.getElementById("ctx-etapa").value = ctx.etapa;
            updateEtapaSelects(); // Regenerar opcions abans de posar curs/àmbit
        }
        if (ctx.curs) document.getElementById("ctx-curs").value = ctx.curs;
        if (ctx.ambit) document.getElementById("ctx-ambit").value = ctx.ambit;
        if (ctx.materia) document.getElementById("ctx-materia").value = ctx.materia;
        if (ctx.tipus_aula) {
            const radio = document.querySelector(`input[name="ctx-aula"][value="${ctx.tipus_aula}"]`);
            if (radio) radio.checked = true;
        }
    } catch { /* ignore */ }
}


// ── Perfils: desar / carregar / llistar (localStorage + servidor) ─────────

function getLocalProfiles() {
    try {
        return JSON.parse(localStorage.getItem("atne_profiles")) || {};
    } catch { return {}; }
}

function saveLocalProfiles(profiles) {
    localStorage.setItem("atne_profiles", JSON.stringify(profiles));
}

async function loadProfileList() {
    const sel = document.getElementById("profile-selector");
    sel.innerHTML = '<option value="_new">— Nou perfil —</option>';

    // Carregar des de localStorage (font principal)
    const local = getLocalProfiles();
    for (const [key, p] of Object.entries(local)) {
        sel.innerHTML += `<option value="${key}">${p.nom}</option>`;
    }

    // Intentar sincronitzar des del servidor (per si hi ha perfils antics)
    try {
        const resp = await fetch("/api/profiles");
        const serverProfiles = await resp.json();
        for (const p of serverProfiles) {
            if (!local[p.fitxer]) {
                // Carregar perfil complet del servidor i guardar a localStorage
                const detailResp = await fetch(`/api/profiles/${p.fitxer}`);
                const detail = await detailResp.json();
                local[p.fitxer] = detail;
                sel.innerHTML += `<option value="${p.fitxer}">${p.nom}</option>`;
            }
        }
        saveLocalProfiles(local);
    } catch { /* servidor no disponible, localStorage és suficient */ }
}

async function saveProfile() {
    const profile = collectProfile();
    const key = profile.nom.toLowerCase().replace(/[^a-z0-9àáèéíïòóúüç]+/g, "_").replace(/_+/g, "_").slice(0, 30);

    // Desar a localStorage (font principal)
    const local = getLocalProfiles();
    local[key] = profile;
    saveLocalProfiles(local);

    // Intentar desar també al servidor (backup)
    try {
        await fetch("/api/profiles", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(profile),
        });
    } catch { /* no passa res, ja tenim localStorage */ }

    await loadProfileList();
    // Seleccionar el perfil acabat de desar
    document.getElementById("profile-selector").value = key;
    alert(`Perfil "${profile.nom}" desat correctament.`);
}

async function loadProfile() {
    const sel = document.getElementById("profile-selector");
    if (sel.value === "_new") {
        resetProfileForm();
        return;
    }

    // Carregar des de localStorage
    const local = getLocalProfiles();
    const profile = local[sel.value];
    if (profile) {
        applyProfileToForm(profile);
        return;
    }

    // Fallback: servidor
    try {
        const resp = await fetch(`/api/profiles/${sel.value}`);
        const serverProfile = await resp.json();
        applyProfileToForm(serverProfile);
        // Guardar a localStorage per futures vegades
        local[sel.value] = serverProfile;
        saveLocalProfiles(local);
    } catch (e) {
        alert("Error carregant el perfil: " + e.message);
    }
}

function resetProfileForm() {
    document.getElementById("profile-nom").value = "";
    document.getElementById("profile-obs").value = "";
    document.querySelectorAll('.char-item').forEach(item => {
        item.classList.remove("checked");
        item.querySelector('input[type="checkbox"]').checked = false;
    });
}

function applyProfileToForm(profile) {
    document.getElementById("profile-nom").value = profile.nom || "";
    document.getElementById("profile-obs").value = profile.observacions || "";
    document.getElementById("profile-canal").value = profile.canal_preferent || "mixte";
    const chars = profile.caracteristiques || {};
    for (const [key, val] of Object.entries(chars)) {
        const cb = document.querySelector(`input[type="checkbox"][data-char="${key}"]`);
        if (!cb) continue;
        cb.checked = val.actiu;
        cb.closest(".char-item").classList.toggle("checked", val.actiu);
        if (val.actiu) {
            for (const [svKey, svVal] of Object.entries(val)) {
                if (svKey === "actiu") continue;
                const el = document.querySelector(`[data-char="${key}"][data-var="${svKey}"]`);
                if (el) el.value = String(svVal);
            }
        }
    }
}


// ── Proposta d'adaptació ───────────────────────────────────────────────────

async function requestProposal() {
    const profile = collectProfile();
    const context = collectContext();
    try {
        const resp = await fetch("/api/propose", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ caracteristiques: profile.caracteristiques, context }),
        });
        const proposal = await resp.json();
        applyProposal(proposal, profile);
    } catch (e) {
        console.error("Error obtenint proposta:", e);
    }
}

function applyProposal(proposal, profile) {
    document.getElementById("param-dua").value = proposal.dua || "Core";
    document.getElementById("param-lf").value = proposal.lf || 2;
    document.getElementById("param-mecr").value = proposal.mecr_sortida || "B2";

    // Activar/desactivar complements
    const comps = proposal.complements || {};
    for (const [key, active] of Object.entries(comps)) {
        const cb = document.querySelector(`input[data-comp="${key}"]`);
        if (cb) {
            cb.checked = active;
            const item = cb.closest(".complement-item");
            item.classList.toggle("auto", active);
        }
    }

    // Mostrar base de la proposta
    const chars = profile.caracteristiques || {};
    const actives = Object.entries(chars)
        .filter(([_, v]) => v.actiu)
        .map(([k]) => CHARACTERISTICS[k]?.label || k);
    document.getElementById("proposal-basis").textContent =
        actives.length > 0 ? `Basat en: ${actives.join(" + ")}` : "Perfil genèric";

    // Bloc 2e a la proposta
    show2eProposalBlock(chars);
}

function show2eProposalBlock(chars) {
    let block = document.getElementById("proposal-2e");
    const acActive = chars.altes_capacitats?.actiu;
    const otherChars = Object.keys(CHARACTERISTICS).filter(k => k !== 'altes_capacitats');
    const otherActives = otherChars.filter(k => chars[k]?.actiu);

    if (acActive && otherActives.length > 0) {
        const comboLabels = otherActives.map(k => CHARACTERISTICS[k]?.label || k);
        const comboDesc = {
            dislexia: "contingut complex però format visual/oral accessible. El rendiment pot ser irregular: brillant en unes matèries i molt per sota en d'altres.",
            tea: "repte cognitiu dins estructura predictible i literal. L'hiperfocus en àrees d'interès pot ser motor d'aprenentatge.",
            nouvingut: "contingut ric amb llengua simplificada i glossari complet. El potencial cognitiu pot quedar ocult per la barrera lingüística.",
            tdah: "repte intel·lectual amb tasques curtes i variades. Alta creativitat combinada amb inatenció i baixa tolerància a la frustració.",
        };
        const descriptions = otherActives.map(k => comboDesc[k] || "adaptar format mantenint repte.").join(" ");

        if (!block) {
            block = document.createElement("div");
            block.id = "proposal-2e";
            block.className = "proposal-card proposal-2e";
            const proposalCards = document.querySelectorAll(".proposal-card");
            proposalCards[proposalCards.length - 1].after(block);
        }
        block.innerHTML = `
            <h3>Perfil detectat: Doble excepcionalitat (2e)</h3>
            <p><strong>AC + ${comboLabels.join(" + ")}</strong>: ${descriptions}</p>
            <p class="info-2e">El potencial i les dificultats es poden emmascarar mútuament:
            l'alumne pot semblar "normal" quan internament el seu perfil requereix atenció específica.
            L'adaptació manté el repte cognitiu alt amb format adaptat.</p>
        `;
        block.style.display = "block";
    } else if (block) {
        block.style.display = "none";
    }
}


// ── Recollir paràmetres del pas 3 ──────────────────────────────────────────

function collectParams() {
    const complements = {};
    document.querySelectorAll("input[data-comp]").forEach(cb => {
        complements[cb.dataset.comp] = cb.checked;
    });
    // Gènere textual (pas 2) — si no seleccionat, buit (auto-detecció al backend)
    const genereEl = document.getElementById("input-genere-textual");
    const genere = genereEl ? genereEl.value : "";

    let mecr = document.getElementById("param-mecr").value;

    // Via observable: el MECR es calcula des del Bloc A (etapa+curs+desfase)
    // i els ajuts marcats afegeixen complements del backend.
    if (currentVia === "observable" && window.ObservableMapping) {
        const etapa = document.getElementById("ctx-etapa").value;
        const curs = document.getElementById("ctx-curs").value;
        const desfase = getDesfase();
        mecr = window.ObservableMapping.computeMecr(etapa, curs, desfase);

        const ajutIds = getSelectedAjutIds();
        const fromAjuts = window.ObservableMapping.ajutsToComplements(ajutIds);
        for (const [k, v] of Object.entries(fromAjuts)) {
            complements[k] = v;
        }
    }

    return {
        dua: document.getElementById("param-dua").value,
        lf: parseInt(document.getElementById("param-lf").value),
        mecr_sortida: mecr,
        genere_discursiu: genere,
        complements,
        auditor: getAuditorEnabled(),
    };
}


// ── Adaptació (SSE) ───────────────────────────────────────────────────────

async function runAdaptation() {
    const text = document.getElementById("input-text").value;
    if (!text.trim()) {
        alert("Cal introduir un text a adaptar.");
        return;
    }

    const profile = collectProfile();
    const context = collectContext();
    const params = collectParams();

    state.originalText = text;

    // Mostrar progress
    state._doneHandled = false;
    const progressArea = document.getElementById("progress-area");
    const progressSteps = document.getElementById("progress-steps");
    progressArea.classList.add("active");
    progressSteps.innerHTML = "";

    const btn = document.getElementById("btn-next") || document.getElementById("btn-adapt");
    if (btn) { btn.disabled = true; btn.textContent = "Adaptant..."; }

    try {
        const modelSel = document.getElementById("model-selector");
        const model = modelSel ? modelSel.value : "mistral";
        const verifyToggle = document.getElementById("verify-toggle");
        const verify_retry = verifyToggle ? verifyToggle.checked : true;

        // Mode d'adaptació: alumne (1 versió) o grup (3 versions)
        const mode = getAdaptMode();
        const levels = mode === "grup"
            ? ["accessible", "estandard", "exigent"]
            : ["single"];

        state.adaptMode = mode;
        state.versions = {}; // { accessible: "...", estandard: "...", exigent: "..." }
        state.doneLevels = new Set();

        const paramsWithVerify = { ...params, verify_retry, levels };
        const resp = await fetch("/api/adapt", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text, profile, context, params: paramsWithVerify, model }),
        });

        const reader = resp.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;
            buffer += decoder.decode(value, { stream: true });

            const lines = buffer.split("\n");
            buffer = lines.pop(); // últim fragment incomplet

            for (const line of lines) {
                if (!line.startsWith("data: ")) continue;
                try {
                    const ev = JSON.parse(line.slice(6));
                    handleSSEEvent(ev, progressSteps);
                } catch { /* ignore parse errors */ }
            }
        }
    } catch (e) {
        progressSteps.innerHTML += `<div class="progress-step" style="color:var(--err);">Error: ${e.message}</div>`;
    }

    if (btn) { btn.disabled = false; btn.textContent = "Adaptar"; }
}

function handleSSEEvent(ev, container) {
    const level = ev.level || "";
    const levelTag = level ? ` [${versionLabel(level)}]` : "";

    if (ev.type === "step") {
        // Marcar anteriors com done (només els del mateix level o sense level)
        container.querySelectorAll(`.progress-step.active[data-level="${level}"]`).forEach(el => {
            el.classList.remove("active");
            el.classList.add("done");
            el.querySelector(".spinner")?.remove();
        });
        const div = document.createElement("div");
        div.className = "progress-step active";
        div.dataset.level = level;
        div.innerHTML = `<div class="spinner"></div>${ev.msg}${levelTag}`;
        container.appendChild(div);
    } else if (ev.type === "result") {
        // Acumulem per versió. Si no hi ha level, és una versió única.
        if (state.adaptMode === "grup" && level) {
            state.versions[level] = ev.adapted;
            // En mode grup guardem el quality report per nivell
            state.qualityReports = state.qualityReports || {};
            if (ev.quality_report) state.qualityReports[level] = ev.quality_report;
        } else {
            state.adaptedText = ev.adapted;
            state.lastQualityReport = ev.quality_report || null;
        }
    } else if (ev.type === "done_level") {
        // Un nivell individual ha acabat. En mode grup, això pot dispar el
        // renderitzat parcial (per mostrar una pestanya mentre les altres
        // encara generen). Per simplicitat, esperem el 'done' global.
        state.doneLevels.add(level);
        container.querySelectorAll(`.progress-step.active[data-level="${level}"]`).forEach(el => {
            el.classList.remove("active");
            el.classList.add("done");
            el.querySelector(".spinner")?.remove();
        });
    } else if (ev.type === "done") {
        if (state._doneHandled) return; // evitar duplicats
        state._doneHandled = true;
        container.querySelectorAll(".progress-step.active").forEach(el => {
            el.classList.remove("active");
            el.classList.add("done");
            el.querySelector(".spinner")?.remove();
        });
        container.innerHTML += `<div class="progress-step done">Adaptació completada!</div>`;
        showResult();
    }
}

function versionLabel(level) {
    return ({
        accessible: "Més accessible",
        estandard: "Estàndard",
        exigent: "Més exigent",
    })[level] || level;
}

function bindVersionTabs() {
    document.querySelectorAll("#version-tabs .version-tab").forEach(tab => {
        // Elimina listeners previs clonant
        const nw = tab.cloneNode(true);
        tab.parentNode.replaceChild(nw, tab);
    });
    document.querySelectorAll("#version-tabs .version-tab").forEach(tab => {
        tab.addEventListener("click", () => switchVersion(tab.dataset.version));
    });
}

function switchVersion(level) {
    if (!state.versions || !state.versions[level]) return;
    state.currentVersion = level;
    state.adaptedText = state.versions[level];

    // Reparsejar seccions del text d'aquesta versió
    const sections = parseAdaptedSections(state.adaptedText);
    document.getElementById("result-adapted").innerHTML = formatMarkdown(sections.main || state.adaptedText);

    // Actualitzar complements (cada versió pot tenir-ne de propis)
    const compDiv = document.getElementById("result-complements");
    compDiv.innerHTML = "";
    for (const [title, content] of Object.entries(sections.complements)) {
        const icon = getCompIcon(title);
        const isAudit = title.toLowerCase().includes("auditoria") || title.toLowerCase().includes("argumentació");
        const openAttr = isAudit ? "" : "open";
        compDiv.innerHTML += `
            <details class="complement-card" ${openAttr}>
                <summary class="complement-header">
                    <span class="complement-icon">${icon}</span>
                    <span class="complement-title">${title}</span>
                </summary>
                <div class="complement-body">${formatMarkdown(content)}</div>
            </details>
        `;
    }

    updateVersionTabsUI();

    // Actualitzar Quality Report per al nivell actiu
    const qr = state.qualityReports && state.qualityReports[level];
    if (qr) {
        renderQualityReport("quality-report-p4", "quality-body-p4", "quality-badge-p4", qr);
    }
}

function updateVersionTabsUI() {
    document.querySelectorAll("#version-tabs .version-tab").forEach(tab => {
        const isActive = tab.dataset.version === state.currentVersion;
        const hasContent = state.versions && state.versions[tab.dataset.version];
        tab.classList.toggle("version-active", isActive);
        tab.style.borderBottomColor = isActive ? "#0369a1" : "transparent";
        tab.style.color = isActive ? "#0369a1" : (hasContent ? "#374151" : "#94a3b8");
        tab.disabled = !hasContent;
    });
    const label = document.getElementById("version-label");
    if (label) label.textContent = state.currentVersion ? `— ${versionLabel(state.currentVersion)}` : "";
}


// ── Mostrar resultat ───────────────────────────────────────────────────────

// Icones per cada tipus de complement
const COMP_ICONS = {
    "glossari": "📘",
    "esquema visual": "🧩",
    "esquema": "🧩",
    "mapa conceptual": "🧠",
    "preguntes de comprensió": "❓",
    "preguntes": "❓",
    "activitats d'aprofundiment": "🚀",
    "activitats": "🚀",
    "bastides": "🪜",
    "bastides (scaffolding)": "🪜",
    "mapa mental": "💡",
    "argumentació pedagògica": "📊",
    "argumentacio pedagogica": "📊",
    "notes d'auditoria": "📝",
    "notes": "📝",
    "negretes": "✏️",
    "definicions integrades": "📎",
    "traducció l1": "🌍",
    "pictogrames": "🖼️",
};

function getCompIcon(title) {
    const lower = title.toLowerCase();
    for (const [key, icon] of Object.entries(COMP_ICONS)) {
        if (lower.includes(key)) return icon;
    }
    return "📄";
}

function showResult() {
    document.getElementById("result-original").textContent = state.originalText;

    // Mode grup: inicialitzar pestanyes i seleccionar la primera versió disponible
    const versionTabs = document.getElementById("version-tabs");
    if (state.adaptMode === "grup" && state.versions && Object.keys(state.versions).length) {
        versionTabs.style.display = "flex";
        bindVersionTabs();
        // Triar la versió estàndard com a defecte (si hi és)
        const defaultVersion = state.versions.estandard ? "estandard"
            : (state.versions.accessible ? "accessible" : "exigent");
        state.currentVersion = defaultVersion;
        state.adaptedText = state.versions[defaultVersion];
        updateVersionTabsUI();
    } else {
        versionTabs.style.display = "none";
    }

    // Parsejar seccions del text adaptat
    const sections = parseAdaptedSections(state.adaptedText);
    document.getElementById("result-adapted").innerHTML = formatMarkdown(sections.main || state.adaptedText);

    // Renderitzar complements amb acordions i icones
    const compDiv = document.getElementById("result-complements");
    compDiv.innerHTML = "";

    for (const [title, content] of Object.entries(sections.complements)) {
        const icon = getCompIcon(title);
        const isAudit = title.toLowerCase().includes("auditoria") || title.toLowerCase().includes("argumentació");
        const openAttr = isAudit ? "" : "open";

        compDiv.innerHTML += `
            <details class="complement-card" ${openAttr}>
                <summary class="complement-header">
                    <span class="complement-icon">${icon}</span>
                    <span class="complement-title">${title}</span>
                </summary>
                <div class="complement-body">${formatMarkdown(content)}</div>
            </details>
        `;
    }

    // Stats de paraules separades
    const origWords = state.originalText.trim().split(/\s+/).length;
    const mainWords = (sections.main || "").trim().split(/\s+/).length;
    const compWords = Object.values(sections.complements).reduce((sum, c) => sum + c.trim().split(/\s+/).length, 0);
    const totalWords = mainWords + compWords;
    const statsDiv = document.getElementById("result-word-stats");
    if (statsDiv) {
        statsDiv.innerHTML = `
            <span><strong>Original:</strong> ${origWords} par</span>
            <span style="color:#6b7280">|</span>
            <span><strong>Text adaptat:</strong> ${mainWords} par</span>
            <span style="color:#6b7280">|</span>
            <span><strong>Complements:</strong> ${compWords} par</span>
            <span style="color:#6b7280">|</span>
            <span><strong>Total:</strong> ${totalWords} par</span>
            <span style="color:#6b7280">|</span>
            <span style="color:${mainWords <= origWords ? '#059669' : '#d97706'}">${mainWords <= origWords ? '↓' : '↑'} ${Math.abs(Math.round((mainWords/origWords-1)*100))}% vs original</span>
        `;
    }

    // Quality Report al Pas 4 (si disponible)
    const qualityReport = state.adaptMode === "grup" && state.currentVersion && state.qualityReports
        ? state.qualityReports[state.currentVersion]
        : state.lastQualityReport;
    if (qualityReport) {
        renderQualityReport("quality-report-p4", "quality-body-p4", "quality-badge-p4", qualityReport);
    } else {
        document.getElementById("quality-report-p4")?.setAttribute("hidden", "hidden");
    }

    // Resetar feedback
    state.feedbackRating = null;
    state.historyId = null;
    document.querySelectorAll(".feedback-btn").forEach(b => b.classList.remove("selected"));
    document.getElementById("feedback-comment-area").style.display = "none";
    document.getElementById("feedback-thanks").style.display = "none";
    document.getElementById("feedback-comment").value = "";

    // Desar a historial (sense rating encara)
    saveToHistory();

    // Anar al pas 4
    goToStep(4);
}

// ── Historial i feedback ─────────────────────────────────────────────────

async function saveToHistory() {
    const profile = collectProfile();
    const context = collectContext();
    const params = collectParams();
    try {
        const resp = await fetch("/api/history", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                profile_name: profile.nom,
                profile: profile,
                context: context,
                params: params,
                original: state.originalText,
                adapted: state.adaptedText,
            }),
        });
        const data = await resp.json();
        if (data.ok && data.id) {
            state.historyId = data.id;
            // Invalidar cache d'historial perquè la propera vegada es refresqui
            _historyLoaded = false;
        }
    } catch { /* no bloquejant */ }
}

function rateFeedback(rating) {
    state.feedbackRating = rating;
    // Marcar botó seleccionat
    document.querySelectorAll(".feedback-btn").forEach(b => {
        b.classList.toggle("selected", parseInt(b.dataset.rating) === rating);
    });
    // Mostrar camp de comentari (especialment si dolenta/regular)
    document.getElementById("feedback-comment-area").style.display = "flex";
    // Enviar rating immediatament
    sendFeedback(rating);
}

async function sendFeedback(rating, comment) {
    if (!state.historyId) return;
    const body = { rating };
    if (comment) body.comment = comment;
    try {
        await fetch(`/api/history/${state.historyId}`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body),
        });
    } catch { /* no bloquejant */ }
}

async function submitFeedback() {
    const comment = document.getElementById("feedback-comment").value.trim();
    if (comment) {
        await sendFeedback(state.feedbackRating, comment);
    }
    document.getElementById("feedback-comment-area").style.display = "none";
    document.getElementById("feedback-thanks").style.display = "block";
}

function parseAdaptedSections(text) {
    const result = { main: "", complements: {} };
    const parts = text.split(/^## /m);

    if (parts.length <= 1) {
        result.main = text;
        return result;
    }

    // El primer part pot ser buit o preàmbul
    for (const part of parts) {
        if (!part.trim()) continue;
        const nlIdx = part.indexOf("\n");
        const title = nlIdx > -1 ? part.slice(0, nlIdx).trim() : part.trim();
        const body = nlIdx > -1 ? part.slice(nlIdx + 1).trim() : "";

        if (title.toLowerCase().includes("text adaptat")) {
            result.main = body;
        } else if (title.toLowerCase().includes("auditoria")) {
            result.complements["Notes d'auditoria"] = body;
        } else {
            result.complements[title] = body;
        }
    }

    if (!result.main) result.main = text;
    return result;
}

function formatMarkdown(text) {
    if (!text) return "";
    const lines = text.split("\n");
    const html = [];
    let inTable = false;
    let inCodeBlock = false;
    let codeLines = [];
    let inList = false;

    for (let i = 0; i < lines.length; i++) {
        let line = lines[i];

        // Bloc de codi / esquema (```)
        if (line.trim().startsWith("```")) {
            if (inCodeBlock) {
                html.push('<pre class="schema-box">' + codeLines.join("\n") + '</pre>');
                codeLines = [];
                inCodeBlock = false;
            } else {
                if (inList) { html.push("</ul>"); inList = false; }
                inCodeBlock = true;
            }
            continue;
        }
        if (inCodeBlock) {
            codeLines.push(escapeHtml(line));
            continue;
        }

        // Taules markdown
        if (line.trim().startsWith("|")) {
            if (inList) { html.push("</ul>"); inList = false; }
            if (!inTable) {
                inTable = true;
                html.push('<div class="table-wrapper"><table class="md-table">');
                // Primera fila = header
                const cells = parseTableRow(line);
                html.push("<thead><tr>" + cells.map(c => `<th>${inlineMarkdown(c)}</th>`).join("") + "</tr></thead><tbody>");
                // Saltar la línia separadora (|---|---|)
                if (i + 1 < lines.length && /^\|[\s\-:|]+\|?$/.test(lines[i + 1].trim())) i++;
                continue;
            }
            const cells = parseTableRow(line);
            html.push("<tr>" + cells.map(c => `<td>${inlineMarkdown(c)}</td>`).join("") + "</tr>");
            continue;
        }
        if (inTable) {
            html.push("</tbody></table></div>");
            inTable = false;
        }

        // Headings (### dins de seccions)
        if (line.startsWith("### ")) {
            if (inList) { html.push("</ul>"); inList = false; }
            html.push(`<h4 class="section-subtitle">${inlineMarkdown(line.slice(4))}</h4>`);
            continue;
        }

        // Llistes (*, -, numerades)
        const bulletMatch = line.match(/^(\s*)[*\-]\s+(.+)/);
        const numMatch = line.match(/^(\s*)\d+\.\s+(.+)/);
        if (bulletMatch || numMatch) {
            if (!inList) { html.push('<ul class="md-list">'); inList = true; }
            const content = bulletMatch ? bulletMatch[2] : numMatch[2];
            html.push(`<li>${inlineMarkdown(content)}</li>`);
            continue;
        }
        if (inList && line.trim() === "") {
            html.push("</ul>");
            inList = false;
        }

        // Línia buida
        if (line.trim() === "") {
            html.push('<div class="spacer"></div>');
            continue;
        }

        // Paràgraf normal
        html.push(`<p>${inlineMarkdown(line)}</p>`);
    }

    if (inTable) html.push("</tbody></table></div>");
    if (inList) html.push("</ul>");
    if (inCodeBlock) html.push('<pre class="schema-box">' + codeLines.join("\n") + '</pre>');

    return html.join("\n");
}

function inlineMarkdown(text) {
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/`(.*?)`/g, '<code>$1</code>')
        .replace(/_(.*?)_/g, '<em>$1</em>');
}

function escapeHtml(text) {
    return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function parseTableRow(line) {
    return line.split("|").filter((_, i, arr) => i > 0 && i < arr.length - 1).map(c => c.trim());
}


// ── Exportació ─────────────────────────────────────────────────────────────

async function exportDoc(format) {
    const profile = collectProfile();
    // Enviar el text complet (adaptat + complements) per a l'exportació
    // state.adaptedText conté tot el markdown original de Gemini
    try {
        const resp = await fetch("/api/export", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                format,
                adapted: state.adaptedText,
                original: state.originalText,
                profile_name: profile.nom,
            }),
        });
        if (!resp.ok) {
            alert("Error exportant.");
            return;
        }
        const blob = await resp.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = resp.headers.get("content-disposition")?.split("filename=")[1]?.replace(/"/g, "")
            || `adaptacio.${format}`;
        a.click();
        URL.revokeObjectURL(url);
    } catch (e) {
        alert("Error exportant: " + e.message);
    }
}


// ── Upload de fitxer (PDF/DOCX/MD/TXT) ─────────────────────────────────────

async function handleFileUpload(ev) {
    const input = ev.target;
    const file = input.files && input.files[0];
    if (!file) return;

    const status = document.getElementById("upload-status");
    const textarea = document.getElementById("input-text");

    status.textContent = `Llegint "${file.name}"…`;
    status.style.color = "#0369a1";

    try {
        const formData = new FormData();
        formData.append("file", file);

        const resp = await fetch("/api/extract-text", {
            method: "POST",
            body: formData,
        });
        const data = await resp.json();

        if (!resp.ok) {
            status.textContent = `Error: ${data.error || resp.statusText}`;
            status.style.color = "#b91c1c";
            input.value = ""; // permet reintentar amb el mateix fitxer
            return;
        }

        editorPushUndo();
        textarea.value = data.text;
        updateWordCount();
        status.textContent = `${file.name} — ${data.paraules} paraules extretes (${data.format_detectat.toUpperCase()})`;
        status.style.color = "#15803d";
        // Auto-switch a mode "write" després de pujar
        if (typeof switchMode === "function") switchMode("write");
    } catch (e) {
        status.textContent = `Error de xarxa: ${e.message}`;
        status.style.color = "#b91c1c";
    } finally {
        input.value = "";
    }
}


// ── Generació de text base (layout permanent) ─────────────────────────────

// Estat per a "Desfer regeneració" — guarda l'últim text abans de regenerar
let _lastTextBeforeGeneration = null;

function updateGenerateButtonLabel() {
    const textarea = document.getElementById("input-text");
    const label = document.getElementById("btn-generate-label");
    if (!textarea || !label) return;
    label.textContent = textarea.value.trim() ? "Regenerar text" : "Generar text";
}

async function generateDraftText() {
    const tema = document.getElementById("gen-tema").value.trim() ||
                 document.getElementById("ctx-materia").value.trim();
    const status = document.getElementById("gen-status");
    const btn = document.getElementById("btn-generate-text");

    if (!tema) {
        status.textContent = "Has d'indicar el tema (al Pas 1 o al camp Tema d'aquí).";
        status.style.display = "block";
        status.style.color = "#b91c1c";
        return;
    }

    // Guardar text actual per a "Desfer regeneració"
    const textarea = document.getElementById("input-text");
    if (textarea && textarea.value.trim()) {
        _lastTextBeforeGeneration = textarea.value;
    }

    const payload = {
        tema,
        genere: document.getElementById("gen-genere").value,
        tipologia: document.getElementById("gen-tipologia").value,
        to: document.getElementById("gen-to").value,
        extensio: document.getElementById("gen-extensio").value,
        notes: document.getElementById("gen-notes").value.trim(),
        context: collectContext(),
        model: getSelectedGenModel(),
        auditor: getAuditorEnabled(),
    };

    btn.disabled = true;
    btn.classList.add("is-loading");
    const oldHTML = btn.innerHTML;
    btn.innerHTML = '<span class="material-symbols-outlined">autorenew</span> <span>Generant...</span>';
    status.style.display = "block";
    status.style.color = "var(--on-surface-variant)";
    status.textContent = "Generant amb Gemma 4... pot trigar 15-30 segons.";

    try {
        const resp = await fetch("/api/generate-text", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });
        const data = await resp.json();

        if (!resp.ok) {
            status.textContent = `Error: ${data.error || resp.statusText}`;
            status.style.color = "#b91c1c";
            return;
        }

        if (textarea) {
            editorPushUndo();
            textarea.value = data.text;
        }
        updateWordCount();
        updateGenerateButtonLabel();

        // Quality Report (si disponible)
        if (data.quality_report) {
            renderQualityReport("quality-report-p2", "quality-body-p2", "quality-badge-p2", data.quality_report);
        }

        status.textContent = `Text generat (${data.paraules} paraules${data.model ? " · " + data.model : ""}). Modifica paràmetres i regenera, refina'l, o continua.`;
        status.style.color = "#15803d";

        // Auto-switch a mode "write" perquè es vegi el text generat
        if (typeof switchMode === "function") setTimeout(() => switchMode("write"), 500);

        // Mostrar botó de "Desfer regeneració" si teníem text previ
        const btnUndo = document.getElementById("btn-undo-generate");
        if (btnUndo && _lastTextBeforeGeneration) btnUndo.style.display = "flex";
    } catch (e) {
        status.textContent = `Error de xarxa: ${e.message}`;
        status.style.color = "#b91c1c";
    } finally {
        btn.disabled = false;
        btn.classList.remove("is-loading");
        btn.innerHTML = oldHTML;
        updateGenerateButtonLabel();
    }
}

function undoLastGeneration() {
    if (!_lastTextBeforeGeneration) return;
    const textarea = document.getElementById("input-text");
    if (textarea) textarea.value = _lastTextBeforeGeneration;
    _lastTextBeforeGeneration = null;
    const btnUndo = document.getElementById("btn-undo-generate");
    if (btnUndo) btnUndo.style.display = "none";
    const status = document.getElementById("gen-status");
    if (status) {
        status.textContent = "Regeneració desfeta. El text anterior s'ha restaurat.";
        status.style.color = "var(--on-surface-variant)";
    }
    updateWordCount();
    updateGenerateButtonLabel();
}


// ── Refinament de text (ajusts sense regenerar) ───────────────────────────

const REFINE_LABELS = {
    catala: "Corregint català",
    simplificar: "Simplificant",
    ampliar: "Ampliant",
    escurcar: "Escurçant",
    to_mes_proper: "Aplicant to més proper",
    to_mes_formal: "Aplicant to més formal",
};

async function refineText(preset, customInstruction, triggerBtn, targetId, statusId) {
    // Per defecte, treballa amb el textarea del Pas 2
    targetId = targetId || "input-text";
    statusId = statusId || "refine-status";

    const target = document.getElementById(targetId);
    const status = document.getElementById(statusId);
    if (!target) return;

    // Detectar si és textarea o contenteditable
    const isContentEditable = target.isContentEditable;
    const getCurrentText = () => isContentEditable ? target.innerText : target.value;
    const setNewText = (txt) => {
        if (isContentEditable) target.innerText = txt;
        else target.value = txt;
    };

    const currentText = getCurrentText();
    if (!currentText || !currentText.trim()) {
        if (status) {
            status.textContent = "Primer escriu o genera un text per refinar-lo.";
            status.style.display = "block";
            status.style.color = "#b91c1c";
        }
        return;
    }

    const paraulesIn = currentText.trim().split(/\s+/).length;
    const label = preset ? (REFINE_LABELS[preset] || "Refinant") : "Aplicant instrucció";

    // Estat visual: només toquem els chips del mateix step que el botó activat
    const parentStep = triggerBtn?.closest(".step-panel") || document;
    const allChips = parentStep.querySelectorAll(".refine-chip, .refine-chip-p4");
    allChips.forEach(c => {
        if (c === triggerBtn) {
            c.setAttribute("aria-busy", "true");
            c.classList.add("is-loading");
        } else {
            c.setAttribute("disabled", "disabled");
        }
    });

    if (status) {
        status.style.display = "block";
        status.style.color = "var(--primary)";
        status.innerHTML = `<strong>${label}…</strong> (${paraulesIn} paraules · pot trigar 10-20 s)`;
    }

    const payload = { text: currentText };
    if (preset) payload.preset = preset;
    if (customInstruction) payload.instruccio = customInstruction;

    try {
        const resp = await fetch("/api/refine-text", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });
        const data = await resp.json();

        if (!resp.ok) {
            if (status) {
                status.textContent = `Error: ${data.error || resp.statusText}`;
                status.style.color = "#b91c1c";
            }
            return;
        }

        // Push undo abans de substituir (només per al textarea del Pas 2)
        if (!isContentEditable && targetId === "input-text") editorPushUndo();
        setNewText(data.text);
        if (!isContentEditable) updateWordCount();
        if (status) {
            // Si és LanguageTool (preset català) → mostrar n canvis
            if (data.mode === "languagetool") {
                const n = data.n_canvis || 0;
                if (n === 0) {
                    status.innerHTML = `<strong>Català ✓</strong> No s'han trobat errors (LanguageTool)`;
                } else {
                    status.innerHTML = `<strong>Català ✓</strong> ${n} correcció${n === 1 ? "" : "s"} aplicada${n === 1 ? "" : "s"} (LanguageTool)`;
                }
            } else {
                const delta = data.paraules - paraulesIn;
                const arrow = delta > 0 ? "↑" : delta < 0 ? "↓" : "=";
                const sign = delta > 0 ? "+" : "";
                status.innerHTML = `<strong>${label} ✓</strong> (${paraulesIn} → ${data.paraules} paraules ${arrow} ${sign}${delta})`;
            }
            status.style.color = "#15803d";
            status.style.display = "block";
            // Auto-hide després de 5s
            setTimeout(() => {
                if (status) status.style.display = "none";
            }, 5000);
        }
    } catch (e) {
        if (status) {
            status.textContent = `Error de xarxa: ${e.message}`;
            status.style.color = "#b91c1c";
        }
    } finally {
        // Restaurar tots els chips
        allChips.forEach(c => {
            c.removeAttribute("aria-busy");
            c.removeAttribute("disabled");
            c.classList.remove("is-loading");
        });
        // Re-aplicar toggleRefinePanel només si estem al Pas 2 (textarea)
        if (!isContentEditable) toggleRefinePanel();
    }
}

// ── Mode switcher multimode (Escriure / Pujar / Generar) ──────────────────
function switchMode(mode) {
    document.querySelectorAll(".mode-tab").forEach(tab => {
        tab.classList.toggle("active", tab.dataset.mode === mode);
    });
    document.querySelectorAll(".mode-content").forEach(content => {
        const on = content.dataset.modeContent === mode;
        if (on) content.removeAttribute("hidden");
        else content.setAttribute("hidden", "hidden");
    });
    // El textarea és sempre visible sota (shared-textarea)
}

// ── Desar esborrany (localStorage) ────────────────────────────────────────
function saveDraft() {
    const textarea = document.getElementById("input-text");
    if (!textarea || !textarea.value.trim()) {
        alert("No hi ha text per desar.");
        return;
    }
    const draft = {
        text: textarea.value,
        timestamp: new Date().toISOString(),
        materia: document.getElementById("ctx-materia")?.value || "",
        etapa: document.getElementById("ctx-etapa")?.value || "",
    };
    const drafts = JSON.parse(localStorage.getItem("atne_drafts") || "[]");
    drafts.unshift(draft);
    localStorage.setItem("atne_drafts", JSON.stringify(drafts.slice(0, 20)));

    const btn = document.getElementById("btn-save-draft");
    if (btn) {
        const prevHTML = btn.innerHTML;
        btn.classList.add("is-saved");
        btn.innerHTML = '<span class="material-symbols-outlined">check</span>Desat';
        setTimeout(() => {
            btn.classList.remove("is-saved");
            btn.innerHTML = prevHTML;
        }, 2000);
    }
}

// ── Botons editor: format markdown (negreta/cursiva/vinyeta) ──────────────

function editorApplyFormat(format) {
    const ta = document.getElementById("input-text");
    if (!ta) return;
    ta.focus();

    const start = ta.selectionStart;
    const end = ta.selectionEnd;
    const selected = ta.value.substring(start, end);
    const before = ta.value.substring(0, start);
    const after = ta.value.substring(end);

    let wrapped = "";
    if (format === "bold") {
        wrapped = selected ? `**${selected}**` : "**text en negreta**";
    } else if (format === "italic") {
        wrapped = selected ? `*${selected}*` : "*text en cursiva*";
    } else if (format === "bullet") {
        if (selected) {
            wrapped = selected.split("\n").map(l => l.trim() ? `- ${l}` : l).join("\n");
        } else {
            wrapped = "- ";
        }
    }

    // Guardar snapshot pel nostre undo stack
    editorPushUndo();

    // Inserir mantenint l'historial undo/redo
    if (document.execCommand) {
        ta.setRangeText(wrapped, start, end, "end");
    } else {
        ta.value = before + wrapped + after;
        ta.selectionStart = ta.selectionEnd = start + wrapped.length;
    }
    updateWordCount();
}

// ── Selector de model (només per generació de textos, Pas 2) ─────────────
const GEN_MODEL_STORAGE_KEY = "atne_gen_model";
const GEN_MODEL_DEFAULT = "gemma4";

function getSelectedGenModel() {
    try {
        return localStorage.getItem(GEN_MODEL_STORAGE_KEY) || GEN_MODEL_DEFAULT;
    } catch (e) {
        return GEN_MODEL_DEFAULT;
    }
}

function setSelectedGenModel(model) {
    try {
        localStorage.setItem(GEN_MODEL_STORAGE_KEY, model);
    } catch (e) { /* noop */ }
    document.querySelectorAll(".gen-model-chip").forEach(chip => {
        chip.classList.toggle("selected", chip.dataset.model === model);
    });
}

function initGenModelSelector() {
    const saved = getSelectedGenModel();
    setSelectedGenModel(saved);
    document.querySelectorAll(".gen-model-chip").forEach(chip => {
        chip.addEventListener("click", () => {
            setSelectedGenModel(chip.dataset.model);
        });
    });
}

// ── Toggle auditor LLM experimental (Pas 2, opt-in) ───────────────────────
const AUDITOR_STORAGE_KEY = "atne_auditor_enabled";

function getAuditorEnabled() {
    try {
        return localStorage.getItem(AUDITOR_STORAGE_KEY) === "true";
    } catch (e) {
        return false;
    }
}

function setAuditorEnabled(enabled) {
    try {
        localStorage.setItem(AUDITOR_STORAGE_KEY, enabled ? "true" : "false");
    } catch (e) { /* noop */ }
    const cb = document.getElementById("gen-auditor-enabled");
    if (cb) cb.checked = enabled;
}

function initAuditorToggle() {
    const saved = getAuditorEnabled();
    setAuditorEnabled(saved);
    const cb = document.getElementById("gen-auditor-enabled");
    if (cb) {
        cb.addEventListener("change", () => setAuditorEnabled(cb.checked));
    }
}

// ── Quality Report (Pas 2 generació + Pas 4 adaptació) ───────────────────

function renderQualityReport(reportId, bodyId, badgeId, report) {
    const card = document.getElementById(reportId);
    const body = document.getElementById(bodyId);
    const badge = document.getElementById(badgeId);
    if (!card || !body || !badge || !report) return;

    // Decidir l'estat global: ok / warn / err
    const nCorr = report.n_correccions || 0;
    const sospitoses = report.paraules_sospitoses || [];
    const avisos = report.avisos_estil || [];
    const llegibilitat = report.llegibilitat || {};
    const llegOk = llegibilitat.ok !== false;
    const caractersExotics = report.caracters_exotics || [];

    let globalStatus = "ok";
    if (!report.lt_disponible) {
        globalStatus = "warn"; // no hem pogut verificar
    } else if (sospitoses.length > 5 || !llegOk) {
        globalStatus = "warn";
    }
    if (sospitoses.length > 15) {
        globalStatus = "err";
    }
    // Els caràcters exòtics sempre pugen el badge a atenció
    if (caractersExotics.length > 0) {
        globalStatus = "err";
    }

    // Badge
    badge.classList.remove("q-ok", "q-warn", "q-err");
    if (globalStatus === "ok") {
        badge.classList.add("q-ok");
        badge.textContent = "OK";
    } else if (globalStatus === "warn") {
        badge.classList.add("q-warn");
        badge.textContent = "Revisa";
    } else {
        badge.classList.add("q-err");
        badge.textContent = "Atenció";
    }

    // Construir contingut
    const rows = [];

    // 0. Caràcters exòtics (prioritat màxima — LLM glitches tipus '홈olatge')
    if (caractersExotics.length > 0) {
        const chips = caractersExotics.slice(0, 10).map(e => {
            const tooltip = `${e.codepoint} · ${e.script} · ${e.ocurrencies} ocurrència${e.ocurrencies === 1 ? "" : "s"}\nContext: ${e.context}`;
            return `<span class="exotic-char-chip" title="${escapeHtml(tooltip)}">${escapeHtml(e.caracter)} <small>${escapeHtml(e.script)}</small></span>`;
        }).join("");
        rows.push(`
            <div class="quality-row q-err">
                <span class="material-symbols-outlined q-icon">error</span>
                <div class="q-content">
                    <p class="q-title">⚠ Caràcters exòtics detectats (${caractersExotics.length})</p>
                    <p class="q-detail">S'han detectat caràcters fora de l'alfabet llatí/català. Probablement són errors de generació de l'LLM (tokenització incorrecta). <strong>Revisa el text manualment</strong> i substitueix-los.</p>
                    <div class="q-words">${chips}</div>
                </div>
            </div>
        `);
    }

    // 1. LanguageTool
    if (!report.lt_disponible) {
        rows.push(`
            <div class="quality-row q-warn">
                <span class="material-symbols-outlined q-icon">cloud_off</span>
                <div class="q-content">
                    <p class="q-title">LanguageTool no disponible</p>
                    <p class="q-detail">No s'ha pogut verificar automàticament. Revisa el text amb més atenció.</p>
                </div>
            </div>
        `);
    } else if (nCorr === 0) {
        rows.push(`
            <div class="quality-row q-ok">
                <span class="material-symbols-outlined q-icon">check_circle</span>
                <div class="q-content">
                    <p class="q-title">LanguageTool: sense errors detectats</p>
                    <p class="q-detail">Cap error ortogràfic o gramàtic obvi al text.</p>
                </div>
            </div>
        `);
    } else {
        const correccionsItems = (report.correccions || []).slice(0, 10).map(c =>
            `<li><code>${escapeHtml(c.original)}</code> → <code>${escapeHtml(c.corregit)}</code> <em>(${escapeHtml(c.missatge || "")})</em></li>`
        ).join("");
        rows.push(`
            <div class="quality-row q-ok">
                <span class="material-symbols-outlined q-icon">auto_fix_high</span>
                <div class="q-content">
                    <p class="q-title">LanguageTool: ${nCorr} correccio${nCorr === 1 ? "" : "ns"} aplicada${nCorr === 1 ? "" : "s"}</p>
                    <p class="q-detail">Errors ortogràfics/gramàtics detectats i corregits automàticament.</p>
                    <details>
                        <summary>Veure correccions (${Math.min(10, nCorr)} de ${nCorr})</summary>
                        <ul class="quality-corrections-list">${correccionsItems}</ul>
                    </details>
                </div>
            </div>
        `);
    }

    // 2. Paraules sospitoses
    if (sospitoses.length > 0) {
        const chips = sospitoses.slice(0, 20).map(p => {
            const sug = (p.suggeriments || []).filter(s => s).slice(0, 3).join(", ");
            const tooltip = sug ? `Suggeriments: ${sug}` : (p.missatge || "Paraula no trobada al diccionari");
            return `<span class="quality-word-chip" title="${escapeHtml(tooltip)}">${escapeHtml(p.paraula)}</span>`;
        }).join("");
        const status = sospitoses.length > 15 ? "q-err" : "q-warn";
        rows.push(`
            <div class="quality-row ${status}">
                <span class="material-symbols-outlined q-icon">dictionary</span>
                <div class="q-content">
                    <p class="q-title">Paraules no trobades al diccionari (${sospitoses.length})</p>
                    <p class="q-detail">Poden ser noms propis, tecnicismes o paraules inventades per l'IA. Revisa manualment:</p>
                    <div class="q-words">${chips}</div>
                </div>
            </div>
        `);
    }

    // 3. Llegibilitat
    const llegClass = llegOk ? "q-ok" : "q-warn";
    const llegIcon = llegOk ? "speed" : "warning";
    const target = llegibilitat.target_mecr || "";
    const wps = llegibilitat.wps || 0;
    const longPct = llegibilitat.long_pct || 0;
    rows.push(`
        <div class="quality-row ${llegClass}">
            <span class="material-symbols-outlined q-icon">${llegIcon}</span>
            <div class="q-content">
                <p class="q-title">Llegibilitat${target ? " (objectiu " + target + ")" : ""}</p>
                <p class="q-detail">${escapeHtml(llegibilitat.missatge || "")}</p>
                <p class="q-detail" style="margin-top:0.25rem">
                    ${wps} paraules/frase · ${longPct}% paraules llargues · ${llegibilitat.n_words || 0} paraules totals
                </p>
            </div>
        </div>
    `);

    // 4. Avisos d'estil (opcional, només si n'hi ha)
    if (avisos.length > 0) {
        rows.push(`
            <div class="quality-row q-warn">
                <span class="material-symbols-outlined q-icon">edit_note</span>
                <div class="q-content">
                    <p class="q-title">${avisos.length} avisos d'estil</p>
                    <p class="q-detail">Consells de redacció (redundàncies, tipografia, estil). No són errors greus.</p>
                </div>
            </div>
        `);
    }

    // 5. Auditor LLM (Layer 3) — warnings qualitatius no detectables per LT
    const avisosAuditor = report.avisos_auditor || [];
    const auditorDisponible = report.auditor_disponible === true;
    const auditorModel = report.auditor_model || "LLM";

    if (auditorDisponible && avisosAuditor.length === 0) {
        rows.push(`
            <div class="quality-row q-ok">
                <span class="material-symbols-outlined q-icon">psychology</span>
                <div class="q-content">
                    <p class="q-title">Auditor pedagògic (${escapeHtml(auditorModel)}): sense avisos</p>
                    <p class="q-detail">L'inspector LLM no ha detectat problemes qualitatius.</p>
                </div>
            </div>
        `);
    } else if (avisosAuditor.length > 0) {
        const tipusIcones = {
            confusa: "help",
            salt: "alt_route",
            vocabulari: "translate",
            repeticio: "repeat",
            connector: "link",
            calc: "g_translate",
        };
        const avisosItems = avisosAuditor.slice(0, 8).map(a => {
            const icon = tipusIcones[a.tipus] || "flag";
            return `
                <li class="auditor-item">
                    <span class="material-symbols-outlined auditor-item-icon">${icon}</span>
                    <div class="auditor-item-body">
                        <span class="auditor-item-tipus">${escapeHtml(a.tipus || "avís")}</span>
                        <em class="auditor-item-fragment">"${escapeHtml(a.fragment || "")}"</em>
                        <span class="auditor-item-motiu">${escapeHtml(a.motiu || "")}</span>
                    </div>
                </li>
            `;
        }).join("");
        const status = avisosAuditor.length > 4 ? "q-warn" : "q-ok";
        rows.push(`
            <div class="quality-row ${status}">
                <span class="material-symbols-outlined q-icon">psychology</span>
                <div class="q-content">
                    <p class="q-title">Auditor pedagògic (${escapeHtml(auditorModel)}): ${avisosAuditor.length} avís${avisosAuditor.length === 1 ? "" : "os"}</p>
                    <p class="q-detail">Revisió qualitativa LLM per detectar problemes que LanguageTool no veu (confusió, salts lògics, vocabulari…).</p>
                    <ul class="auditor-list">${avisosItems}</ul>
                </div>
            </div>
        `);
    } else if (!auditorDisponible && report.auditor_model) {
        rows.push(`
            <div class="quality-row q-warn">
                <span class="material-symbols-outlined q-icon">psychology_off</span>
                <div class="q-content">
                    <p class="q-title">Auditor LLM no disponible</p>
                    <p class="q-detail">No s'ha pogut fer la revisió pedagògica (clau API no configurada o error).</p>
                </div>
            </div>
        `);
    }

    body.innerHTML = rows.join("");
    card.removeAttribute("hidden");
}

function escapeHtml(str) {
    if (str == null) return "";
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// ── Historial d'undo/redo manual per al textarea (Pas 2) ──────────────────
// document.execCommand("undo") no captura canvis programàtics (textarea.value=...)
// per això mantenim el nostre propi stack.
const _editorUndoStack = [];
const _editorRedoStack = [];
const EDITOR_UNDO_MAX = 40;

function editorPushUndo() {
    const ta = document.getElementById("input-text");
    if (!ta) return;
    const last = _editorUndoStack[_editorUndoStack.length - 1];
    if (last === ta.value) return; // no push si és idèntic
    _editorUndoStack.push(ta.value);
    if (_editorUndoStack.length > EDITOR_UNDO_MAX) _editorUndoStack.shift();
    _editorRedoStack.length = 0; // nova acció invalida el redo
}

function editorUndo() {
    const ta = document.getElementById("input-text");
    if (!ta) return;
    ta.focus();
    // Primer intenta l'historial del navegador (canvis manuals de tecla)
    try {
        const ok = document.execCommand("undo");
        if (ok) {
            updateWordCount();
            return;
        }
    } catch (e) { /* noop */ }
    // Si no, utilitza el nostre stack manual
    if (_editorUndoStack.length === 0) return;
    _editorRedoStack.push(ta.value);
    ta.value = _editorUndoStack.pop();
    updateWordCount();
}

function editorRedo() {
    const ta = document.getElementById("input-text");
    if (!ta) return;
    ta.focus();
    try {
        const ok = document.execCommand("redo");
        if (ok) {
            updateWordCount();
            return;
        }
    } catch (e) { /* noop */ }
    if (_editorRedoStack.length === 0) return;
    _editorUndoStack.push(ta.value);
    ta.value = _editorRedoStack.pop();
    updateWordCount();
}

// ── Pill de context (mostra etapa+curs+matèria+perfil al Pas 2) ───────────

function updateContextPill() {
    const pill = document.getElementById("context-pill-text");
    if (!pill) return;

    const etapa = document.getElementById("ctx-etapa")?.value;
    const curs = document.getElementById("ctx-curs")?.value;
    const ambit = document.getElementById("ctx-ambit")?.value;
    const materia = document.getElementById("ctx-materia")?.value.trim();

    const parts = [];
    if (etapa && curs) parts.push(`${curs} ${etapa.toUpperCase()}`);
    else if (etapa) parts.push(etapa.toUpperCase());

    if (materia) parts.push(materia);
    else if (ambit) parts.push(ambit);

    // Resum del perfil de l'alumne
    const mode = document.querySelector('input[name="adapt-mode"]:checked')?.value || "alumne";
    if (mode === "grup") {
        parts.push("Grup d'aula (3 versions)");
    } else {
        const behaviorIds = typeof getActiveBehaviorIds === "function" ? getActiveBehaviorIds() : [];
        if (behaviorIds.length > 0) {
            parts.push(`Alumne · ${behaviorIds.length} ${behaviorIds.length === 1 ? 'observació' : 'observacions'}`);
        } else {
            // Mirar si hi ha característiques NESE actives
            const charsActive = document.querySelectorAll('input[type="checkbox"][data-char]:checked');
            if (charsActive.length > 0) {
                parts.push(`Alumne · ${charsActive.length} ${charsActive.length === 1 ? 'condició' : 'condicions'}`);
            } else {
                parts.push("Alumne genèric");
            }
        }
    }

    pill.textContent = parts.length > 0
        ? parts.join(" · ")
        : "Configura el Pas 1 per veure el context";
}


// ── Botons editor: copiar/enganxar/netejar ────────────────────────────────

async function editorCopyAll() {
    const textarea = document.getElementById("input-text");
    if (!textarea || !textarea.value) return;
    try {
        await navigator.clipboard.writeText(textarea.value);
        const status = document.getElementById("upload-status");
        if (status) {
            const old = status.textContent;
            status.textContent = "Text copiat al porta-retalls ✓";
            status.style.color = "#15803d";
            setTimeout(() => { status.textContent = old; status.style.color = ""; }, 2000);
        }
    } catch {
        textarea.select();
        document.execCommand("copy");
    }
}

async function editorPaste() {
    const textarea = document.getElementById("input-text");
    if (!textarea) return;
    try {
        const text = await navigator.clipboard.readText();
        editorPushUndo();
        textarea.value = text;
        updateWordCount();
        toggleRefinePanel();
    } catch (e) {
        alert("No s'ha pogut llegir el porta-retalls. Enganxa manualment amb Ctrl+V al textarea.");
    }
}

function editorClearAll() {
    const textarea = document.getElementById("input-text");
    if (!textarea) return;
    if (textarea.value && !confirm("Segur que vols esborrar tot el text?")) return;
    editorPushUndo();
    textarea.value = "";
    updateWordCount();
    toggleRefinePanel();
}

// ── Generator v3: sync botons clicables amb selects ocults ────────────────
function initGeneratorButtons() {
    document.querySelectorAll(".generator-card-v3 [data-target]").forEach(container => {
        const targetId = container.dataset.target;
        const select = document.getElementById(targetId);
        if (!select) return;

        // Marca inicial (coincidint amb valor del select)
        const currentVal = select.value;
        container.querySelectorAll(".gen-option").forEach(btn => {
            btn.classList.toggle("selected", btn.dataset.value === currentVal);
        });

        // Click: actualitza selected + valor del select
        container.querySelectorAll(".gen-option").forEach(btn => {
            btn.addEventListener("click", () => {
                container.querySelectorAll(".gen-option").forEach(b => b.classList.remove("selected"));
                btn.classList.add("selected");
                select.value = btn.dataset.value;
                select.dispatchEvent(new Event("change"));
            });
        });
    });
}

function toggleRefinePanel() {
    // Panell ara sempre visible; només togglegem estat "actiu" i el hint (només Pas 2)
    const textarea = document.getElementById("input-text");
    if (!textarea) return;
    const hasText = !!textarea.value.trim();
    // Desactivar chips del Pas 2 si no hi ha text
    document.querySelectorAll("#step-2 .refine-chip, #btn-refine-custom, #refine-instruction").forEach(el => {
        if (hasText) el.removeAttribute("disabled");
        else el.setAttribute("disabled", "disabled");
    });
    const hint = document.getElementById("refine-hint");
    if (hint) hint.style.display = hasText ? "none" : "block";
}


// ── Comptador de paraules ──────────────────────────────────────────────────

function updateWordCount() {
    const text = document.getElementById("input-text").value;
    const words = text.trim() ? text.trim().split(/\s+/).length : 0;
    const wc = document.getElementById("word-count");
    if (wc) wc.textContent = `${words} paraules`;
    toggleRefinePanel();
    updateGenerateButtonLabel();
}


// ── Bind events ────────────────────────────────────────────────────────────

function bindEvents() {
    // Navegació per tabs
    document.querySelectorAll(".step-tab").forEach(tab => {
        tab.addEventListener("click", () => goToStep(parseInt(tab.dataset.step)));
    });
    // Aside nav steps (Stitch shell v2)
    document.querySelectorAll(".aside-step").forEach(step => {
        step.addEventListener("click", () => goToStep(parseInt(step.dataset.step)));
    });

    // Sticky bar navigation
    const btnNext = document.getElementById("btn-next");
    if (btnNext) btnNext.addEventListener("click", goToNextStep);
    const btnBack = document.getElementById("btn-back");
    if (btnBack) btnBack.addEventListener("click", goToPrevStep);

    // Perfils
    document.getElementById("btn-save-profile").addEventListener("click", saveProfile);
    document.getElementById("btn-load-profile").addEventListener("click", loadProfile);
    loadHistoryIfNeeded(); // pre-carregar historial en obrir l'app

    // Adaptació (ara gestionada per sticky bar btn-next al pas 3)

    // Word count
    document.getElementById("input-text").addEventListener("input", updateWordCount);

    // Upload de fitxer
    const fileInput = document.getElementById("file-input");
    if (fileInput) fileInput.addEventListener("change", handleFileUpload);

    // Botó generar/regenerar text
    const btnGen = document.getElementById("btn-generate-text");
    if (btnGen) btnGen.addEventListener("click", generateDraftText);
    const btnUndoGen = document.getElementById("btn-undo-generate");
    if (btnUndoGen) btnUndoGen.addEventListener("click", undoLastGeneration);

    // Pre-omplir camp tema del generador des del context (Pas 1)
    const ctxMateria = document.getElementById("ctx-materia");
    if (ctxMateria) {
        ctxMateria.addEventListener("input", () => {
            const genTema = document.getElementById("gen-tema");
            if (genTema && !genTema.value) genTema.value = ctxMateria.value;
        });
    }

    // Botons editor: format markdown (negreta/cursiva/vinyeta)
    document.querySelectorAll("[data-format]").forEach(btn => {
        btn.addEventListener("click", () => editorApplyFormat(btn.dataset.format));
    });

    // Botons editor: undo/redo
    const btnUndo = document.getElementById("btn-editor-undo");
    if (btnUndo) btnUndo.addEventListener("click", editorUndo);
    const btnRedo = document.getElementById("btn-editor-redo");
    if (btnRedo) btnRedo.addEventListener("click", editorRedo);

    // Botons editor (copiar/enganxar/netejar)
    const btnCopy = document.getElementById("btn-editor-copy");
    if (btnCopy) btnCopy.addEventListener("click", editorCopyAll);
    const btnPaste = document.getElementById("btn-editor-paste");
    if (btnPaste) btnPaste.addEventListener("click", editorPaste);
    const btnCopyAll = document.getElementById("btn-editor-copy-all");
    if (btnCopyAll) btnCopyAll.addEventListener("click", editorCopyAll);
    const btnClear = document.getElementById("btn-editor-clear");
    if (btnClear) btnClear.addEventListener("click", editorClearAll);

    // Botons refinador Pas 2 (chips compactes) — targeten input-text
    document.querySelectorAll("#step-2 .refine-chip, #step-2 .refine-preset").forEach(btn => {
        btn.addEventListener("click", () => refineText(btn.dataset.preset, null, btn, "input-text", "refine-status"));
    });

    // Botons refinador Pas 4 (chips al text adaptat) — targeten result-adapted
    document.querySelectorAll("#step-4 .refine-chip-p4").forEach(btn => {
        btn.addEventListener("click", () => refineText(btn.dataset.preset, null, btn, "result-adapted", "refine-status-p4"));
    });

    // Instrucció pròpia refine Pas 4
    const btnRefineCustomP4 = document.getElementById("btn-refine-custom-p4");
    if (btnRefineCustomP4) {
        btnRefineCustomP4.addEventListener("click", () => {
            const instr = document.getElementById("refine-instruction-p4")?.value.trim();
            if (instr) refineText(null, instr, btnRefineCustomP4, "result-adapted", "refine-status-p4");
        });
    }

    // Generator v3: botons clicables sync amb selects ocults
    initGeneratorButtons();

    // Selector de model de generació (Pas 2)
    initGenModelSelector();

    // Toggle auditoria LLM experimental (Pas 2)
    initAuditorToggle();

    // Mode tabs (multimode Pas 2)
    document.querySelectorAll(".mode-tab").forEach(tab => {
        tab.addEventListener("click", () => switchMode(tab.dataset.mode));
    });

    // Desar esborrany
    const btnSave = document.getElementById("btn-save-draft");
    if (btnSave) btnSave.addEventListener("click", saveDraft);

    // Drag & drop al dropzone
    const dropzone = document.getElementById("dropzone");
    if (dropzone) {
        dropzone.addEventListener("dragover", e => {
            e.preventDefault();
            dropzone.classList.add("drag-over");
        });
        dropzone.addEventListener("dragleave", () => dropzone.classList.remove("drag-over"));
        dropzone.addEventListener("drop", e => {
            e.preventDefault();
            dropzone.classList.remove("drag-over");
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                const fileInput = document.getElementById("file-input");
                fileInput.files = files;
                fileInput.dispatchEvent(new Event("change"));
            }
        });
    }
    const btnRefineCustom = document.getElementById("btn-refine-custom");
    if (btnRefineCustom) {
        btnRefineCustom.addEventListener("click", () => {
            const instr = document.getElementById("refine-instruction").value.trim();
            if (instr) refineText(null, instr);
        });
    }

    // Carregar historial quan s'arriba al pas 2
    document.querySelectorAll('.step-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            if (tab.dataset.step === '2') loadHistoryIfNeeded();
        });
    });

    // Actualitzar selects dinàmics quan canvia l'etapa
    document.getElementById("ctx-etapa").addEventListener("change", () => {
        updateEtapaSelects();
        saveContextToStorage();
        updateMecrPreview();
    });

    // Persistir context en canviar
    ["ctx-curs", "ctx-ambit", "ctx-materia"].forEach(id => {
        document.getElementById(id).addEventListener("change", () => {
            saveContextToStorage();
            if (id === "ctx-curs") updateMecrPreview();
        });
    });
    // ctx-aula ara és un hidden input, no cal listener

    // Via diagnòstic (details toggle)
    const diagPanel = document.getElementById("via-diagnostic-panel");
    if (diagPanel) diagPanel.addEventListener("toggle", updateCurrentVia);

    // Desplaçament del Bloc A
    document.querySelectorAll('input[name="desfase"]').forEach(r => {
        r.addEventListener("change", updateMecrPreview);
    });

    // Mode alumne/grup: actualitza etiqueta del Bloc A
    document.querySelectorAll('input[name="adapt-mode"]').forEach(r => {
        r.addEventListener("change", updateBlocALabel);
    });
}

function updateBlocALabel() {
    const mode = document.querySelector('input[name="adapt-mode"]:checked')?.value || "alumne";
    const label = document.getElementById("bloc-a-label");
    if (label) {
        label.textContent = mode === "grup"
            ? "El grup globalment llegeix i comprèn..."
            : "Aquest alumne llegeix i comprèn...";
    }
    // Mostrar/amagar zones segons mode
    const alumneZones = document.querySelectorAll(".bloc-a, .bloc-b-grid, .via-diagnostic-toggle");
    const grupZone = document.getElementById("grup-config");

    if (mode === "grup") {
        alumneZones.forEach(el => el.style.display = "none");
        if (grupZone) grupZone.style.display = "block";
    } else {
        alumneZones.forEach(el => el.style.display = "");
        if (grupZone) grupZone.style.display = "none";
    }
}

function getAdaptMode() {
    return document.querySelector('input[name="adapt-mode"]:checked')?.value || "alumne";
}

// ── Historial de textos anteriors ──────────────────────────────────────────

async function loadHistoryIfNeeded() {
    if (_historyLoaded) return;
    _historyLoaded = true;
    await refreshHistory();
}

async function refreshHistory() {
    const list = document.getElementById("history-list");
    if (!list) return;

    list.innerHTML = '<div class="history-loading">Carregant historial…</div>';

    try {
        const resp = await fetch("/api/history");
        const data = await resp.json();

        if (!data.ok || !data.items || data.items.length === 0) {
            list.innerHTML = '<div class="history-empty">Encara no hi ha adaptacions guardades.</div>';
            return;
        }

        list.innerHTML = data.items.map((item, i) => {
            const date = new Date(item.created_at).toLocaleString("ca-ES", {
                day: "2-digit", month: "2-digit", year: "2-digit",
                hour: "2-digit", minute: "2-digit"
            });
            const preview = (item.original_text || "").slice(0, 200).replace(/</g, "&lt;").replace(/>/g, "&gt;");
            const profileName = item.profile_name || "Sense nom";
            const hasProfile = item.profile_json && Object.keys(item.profile_json).length > 0;

            return `<div class="history-item">
                <div class="history-item-meta">
                    <span class="history-item-badge">${profileName}</span>
                    <span>${date}</span>
                </div>
                <div class="history-item-preview">${preview}…</div>
                <div class="history-item-actions">
                    <button class="btn btn-secondary" onclick="loadHistoryText(${i})">Carrega text</button>
                    ${hasProfile ? `<button class="btn btn-secondary" onclick="loadHistoryFull(${i})">Carrega text + perfil</button>` : ""}
                </div>
            </div>`;
        }).join("");

        list.dataset.items = JSON.stringify(data.items);

    } catch (e) {
        list.innerHTML = `<div class="history-empty">Error carregant historial: ${e.message}</div>`;
    }
}

function toggleHistory() {
    const list = document.getElementById("history-list");
    const btn = document.getElementById("history-toggle");
    const open = list.style.display !== "none";
    list.style.display = open ? "none" : "block";
    btn.textContent = (open ? "▾" : "▴") + " Textos anteriors";
    if (!open) loadHistoryIfNeeded();
}

function loadHistoryText(index) {
    const list = document.getElementById("history-list");
    const items = JSON.parse(list.dataset.items || "[]");
    const item = items[index];
    if (!item) return;

    document.getElementById("input-text").value = item.original_text || "";
    updateWordCount();

    list.style.display = "none";
    document.getElementById("history-toggle").textContent = "▾ Textos anteriors";
}

function loadHistoryFull(index) {
    const list = document.getElementById("history-list");
    const items = JSON.parse(list.dataset.items || "[]");
    const item = items[index];
    if (!item) return;

    // Carregar text
    document.getElementById("input-text").value = item.original_text || "";
    updateWordCount();

    // Restaurar característiques del perfil
    if (item.profile_json) {
        const chars = item.profile_json.caracteristiques || {};

        // Nom i camps generals
        const nomEl = document.getElementById("profile-nom");
        if (nomEl) nomEl.value = item.profile_json.nom || "";
        const canalEl = document.getElementById("profile-canal");
        if (canalEl && item.profile_json.canal_preferent) canalEl.value = item.profile_json.canal_preferent;
        const obsEl = document.getElementById("profile-obs");
        if (obsEl) obsEl.value = item.profile_json.observacions || "";

        // Característiques: marcar checkboxes i subvariables
        Object.keys(chars).forEach(charId => {
            const entry = chars[charId];
            const cb = document.querySelector(`input[type="checkbox"][data-char="${charId}"]`);
            if (!cb) return;
            cb.checked = !!entry.actiu;
            // Disparar change perquè la UI mostri/oculti subvars
            cb.dispatchEvent(new Event("change", { bubbles: true }));
            // Restaurar subvariables
            if (entry.actiu) {
                Object.keys(entry).forEach(varKey => {
                    if (varKey === "actiu") return;
                    const el = document.querySelector(`[data-char="${charId}"][data-var="${varKey}"]`);
                    if (el) el.value = entry[varKey];
                });
            }
        });
        check2eAlert();
    }

    // Restaurar context
    if (item.context_json) {
        const ctx = item.context_json;
        ["etapa","curs","ambit","materia"].forEach(key => {
            const el = document.getElementById("ctx-" + key);
            if (el && ctx[key] !== undefined) el.value = ctx[key];
        });
        if (ctx.aula) {
            const r = document.querySelector(`input[name="ctx-aula"][value="${ctx.aula}"]`);
            if (r) r.checked = true;
        }
        updateEtapaSelects();
    }

    list.style.display = "none";
    document.getElementById("history-toggle").textContent = "▾ Textos anteriors";
    goToStep(1);

    setTimeout(() => {
        const notice = document.createElement("div");
        notice.style.cssText = "background:#eff6ff;border:1px solid #bfdbfe;color:#1d4ed8;padding:10px 14px;border-radius:8px;font-size:13px;margin-bottom:12px;";
        notice.textContent = "Perfil i text carregats. Modifica el que necessitis i continua al pas 2.";
        const step1 = document.getElementById("step-1");
        step1.insertBefore(notice, step1.firstChild);
        setTimeout(() => notice.remove(), 6000);
    }, 100);
}
