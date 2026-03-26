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
    tdah: { label: "TDAH", subtipus: "constitutiva", subvars: [] },
    dislexia: { label: "Dislèxia", subtipus: "constitutiva", subvars: [] },
    altes_capacitats: {
        label: "Altes capacitats",
        subtipus: "constitutiva",
        subvars: [
            { id: "tipus_capacitat", label: "Tipus", type: "select",
              options: ["global", "talent_especific"] },
            { id: "doble_excepcionalitat", label: "Doble excepcionalitat", type: "select",
              options: ["false", "true"], labels: ["No", "Sí"] },
        ]
    },
    di: {
        label: "Discapacitat intel·lectual",
        subtipus: "constitutiva",
        subvars: [
            { id: "grau", label: "Grau", type: "select", options: ["lleu", "moderat", "sever"] },
        ]
    },
    tdl: { label: "TDL (Trastorn del Llenguatge)", subtipus: "constitutiva", subvars: [] },
    disc_visual: {
        label: "Discapacitat visual",
        subtipus: "constitutiva",
        subvars: [
            { id: "grau", label: "Grau", type: "select", options: ["baixa_visio", "ceguesa"] },
        ]
    },
    disc_auditiva: {
        label: "Discapacitat auditiva",
        subtipus: "constitutiva",
        subvars: [
            { id: "comunicacio", label: "Comunicació", type: "select",
              options: ["oral", "LSC", "mixta"] },
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
        { value: "1r_CGM", label: "1r CGM" },
        { value: "2n_CGM", label: "2n CGM" },
        { value: "1r_CGS", label: "1r CGS" },
        { value: "2n_CGS", label: "2n CGS" },
    ],
};

const AMBITS_PER_ETAPA = {
    infantil: [
        { value: "descoberta_entorn", label: "Descoberta de l'entorn" },
        { value: "comunicacio_llenguatges", label: "Comunicació i llenguatges" },
        { value: "creixement_personal", label: "Creixement personal" },
    ],
    primaria: [
        { value: "cientific", label: "Científic" },
        { value: "humanistic", label: "Humanístic" },
        { value: "linguistic", label: "Lingüístic" },
        { value: "artistic", label: "Artístic" },
    ],
    ESO: [
        { value: "cientific", label: "Científic" },
        { value: "humanistic", label: "Humanístic" },
        { value: "linguistic", label: "Lingüístic" },
        { value: "artistic", label: "Artístic" },
    ],
    batxillerat: [
        { value: "cientific", label: "Científic" },
        { value: "humanistic", label: "Humanístic" },
        { value: "linguistic", label: "Lingüístic" },
        { value: "artistic", label: "Artístic" },
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


// ── Estat de l'aplicació ───────────────────────────────────────────────────

const state = {
    step: 1,
    adaptedText: "",
    originalText: "",
    historyId: null,       // ID de l'entrada a Supabase history
    feedbackRating: null,  // 1=dolenta, 2=regular, 3=bona
};


// ── Inicialització ─────────────────────────────────────────────────────────

document.addEventListener("DOMContentLoaded", () => {
    renderCharGrid();
    renderComplementGrid();
    loadContextFromStorage();
    updateEtapaSelects(); // Sincronitzar cursos/àmbits amb l'etapa carregada
    loadProfileList();
    checkHealth();
    bindEvents();
});


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

    // Canviar etiqueta: "Àmbit" per la majoria, "Família professional" per FP
    const ambitLabel = document.querySelector('label[for="ctx-ambit"]');
    if (ambitLabel) {
        ambitLabel.textContent = etapa === "FP" ? "Família professional" : "Àmbit";
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
    document.querySelectorAll(".step-panel").forEach(panel => {
        panel.classList.toggle("active", panel.id === `step-${n}`);
    });
    if (n === 3) requestProposal();
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

        const badge = char.subtipus === "contextual"
            ? ' <span style="font-size:11px;color:var(--warn);">(contextual)</span>'
            : "";

        div.innerHTML = `
            <label>
                <input type="checkbox" data-char="${key}">
                ${char.label}${badge}
            </label>
            ${subvarsHTML}
        `;

        // Toggle checked class
        const cb = div.querySelector('input[type="checkbox"]');
        cb.addEventListener("change", () => {
            div.classList.toggle("checked", cb.checked);
        });

        grid.appendChild(div);
    }
}


// ── Renderitzar grid de complements ────────────────────────────────────────

function renderComplementGrid() {
    const grid = document.getElementById("complement-grid");
    grid.innerHTML = "";
    for (const [key, label] of Object.entries(COMPLEMENTS)) {
        grid.innerHTML += `
            <label class="complement-item" id="comp-${key}">
                <input type="checkbox" data-comp="${key}"> ${label}
            </label>
        `;
    }
}


// ── Recollir perfil del formulari ──────────────────────────────────────────

function collectProfile() {
    const caracteristiques = {};
    for (const key of Object.keys(CHARACTERISTICS)) {
        const cb = document.querySelector(`input[type="checkbox"][data-char="${key}"]`);
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
    };
}


// ── Recollir context docent ────────────────────────────────────────────────

function collectContext() {
    return {
        etapa: document.getElementById("ctx-etapa").value,
        curs: document.getElementById("ctx-curs").value,
        ambit: document.getElementById("ctx-ambit").value,
        materia: document.getElementById("ctx-materia").value,
        tipus_aula: document.querySelector('input[name="ctx-aula"]:checked')?.value || "ordinaria",
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
    const actives = Object.entries(profile.caracteristiques || {})
        .filter(([_, v]) => v.actiu)
        .map(([k]) => CHARACTERISTICS[k]?.label || k);
    document.getElementById("proposal-basis").textContent =
        actives.length > 0 ? `Basat en: ${actives.join(" + ")}` : "Perfil genèric";
}


// ── Recollir paràmetres del pas 3 ──────────────────────────────────────────

function collectParams() {
    const complements = {};
    document.querySelectorAll("input[data-comp]").forEach(cb => {
        complements[cb.dataset.comp] = cb.checked;
    });
    return {
        dua: document.getElementById("param-dua").value,
        lf: parseInt(document.getElementById("param-lf").value),
        mecr_sortida: document.getElementById("param-mecr").value,
        complements,
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
    const progressArea = document.getElementById("progress-area");
    const progressSteps = document.getElementById("progress-steps");
    progressArea.classList.add("active");
    progressSteps.innerHTML = "";

    const btn = document.getElementById("btn-adapt");
    btn.disabled = true;
    btn.textContent = "Adaptant...";

    try {
        const resp = await fetch("/api/adapt", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text, profile, context, params }),
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

    btn.disabled = false;
    btn.textContent = "ADAPTAR";
}

function handleSSEEvent(ev, container) {
    if (ev.type === "step") {
        // Marcar anteriors com done
        container.querySelectorAll(".progress-step.active").forEach(el => {
            el.classList.remove("active");
            el.classList.add("done");
            el.querySelector(".spinner")?.remove();
        });
        container.innerHTML += `
            <div class="progress-step active">
                <div class="spinner"></div>
                ${ev.msg}
            </div>
        `;
    } else if (ev.type === "result") {
        state.adaptedText = ev.adapted;
    } else if (ev.type === "done") {
        container.querySelectorAll(".progress-step.active").forEach(el => {
            el.classList.remove("active");
            el.classList.add("done");
            el.querySelector(".spinner")?.remove();
        });
        container.innerHTML += `<div class="progress-step done">Adaptació completada!</div>`;
        showResult();
    }
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


// ── Comptador de paraules ──────────────────────────────────────────────────

function updateWordCount() {
    const text = document.getElementById("input-text").value;
    const words = text.trim() ? text.trim().split(/\s+/).length : 0;
    document.getElementById("word-count").textContent = `${words} paraules`;
}


// ── Bind events ────────────────────────────────────────────────────────────

function bindEvents() {
    // Navegació per tabs
    document.querySelectorAll(".step-tab").forEach(tab => {
        tab.addEventListener("click", () => goToStep(parseInt(tab.dataset.step)));
    });

    // Botons de pas
    document.getElementById("btn-next-2").addEventListener("click", () => goToStep(2));
    document.getElementById("btn-next-3").addEventListener("click", () => goToStep(3));

    // Perfils
    document.getElementById("btn-save-profile").addEventListener("click", saveProfile);
    document.getElementById("btn-load-profile").addEventListener("click", loadProfile);

    // Adaptació
    document.getElementById("btn-adapt").addEventListener("click", runAdaptation);

    // Word count
    document.getElementById("input-text").addEventListener("input", updateWordCount);

    // Actualitzar selects dinàmics quan canvia l'etapa
    document.getElementById("ctx-etapa").addEventListener("change", () => {
        updateEtapaSelects();
        saveContextToStorage();
    });

    // Persistir context en canviar
    ["ctx-curs", "ctx-ambit", "ctx-materia"].forEach(id => {
        document.getElementById(id).addEventListener("change", saveContextToStorage);
    });
    document.querySelectorAll('input[name="ctx-aula"]').forEach(r => {
        r.addEventListener("change", saveContextToStorage);
    });
}
