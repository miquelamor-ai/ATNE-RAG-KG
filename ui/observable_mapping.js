/* ATNE — Mapping de la via observable
 *
 * Tradueix les 6 conductes observables a:
 *   (a) característiques del perfil (format compatible amb collectProfile / instruction_filter)
 *   (b) ajuts pedagògics visibles a la dreta de la doble columna
 *
 * La via observable NO és un pipeline alternatiu: genera el mateix dict de
 * caracteristiques que la via diagnòstic, de manera que tot el motor
 * d'adaptació (instruction_filter, build_system_prompt) segueix igual.
 *
 * Doble ús:
 *  - Docent no expert: marca conductes a l'esquerra; els ajuts de la dreta
 *    s'autoactiven automàticament (informatiu, transparent).
 *  - Docent expert (DOP/tutor): pot marcar ajuts directament a la dreta
 *    sense passar per les conductes (via experta emergent).
 */

// ── Les 6 conductes observables ────────────────────────────────────────────
// Cada conducta defineix:
//   - label: text que veu el docent
//   - chars: característiques a activar al profile (amb sub-variables)
//   - ajuts: IDs dels ajuts que s'activen automàticament a la dreta
//
// Fusió: si dues conductes activen la mateixa característica amb sub-variables
// diferents (ex: 1 i 5 toquen tots dos 'tdah'), les sub-variables s'uneixen
// (OR lògic per booleans, última guanya per categories).

const OBSERVABLE_BEHAVIORS = {
    b1_atencio: {
        label: "Li costa mantenir l'atenció en textos llargs i sovint no els acaba",
        chars: {
            tdah: {
                actiu: true,
                presentacio: "inatent",
                grau: "moderat",
                baixa_memoria_treball: true,
            },
        },
        ajuts: ["fragmentar", "paragrafs_curts"],
    },

    b2_descodificacio: {
        label: "Llegeix paraula a paraula, sense fluïdesa, o fa errors freqüents en llegir",
        chars: {
            dislexia: {
                actiu: true,
                tipus_dislexia: "fonologica",
                grau: "moderat",
                tipografia_adaptada: true,
            },
        },
        ajuts: ["una_idea_frase", "vocabulari_frequent", "tipografia_adaptada"],
    },

    b3_oral_vs_escrit: {
        label: "Entén millor quan se li explica oralment que quan llegeix sol/a",
        chars: {
            tdl: {
                actiu: true,
                modalitat: "comprensiu",
                comprensio_lectora: true,
                grau: "moderat",
            },
        },
        ajuts: ["connectors_explicits", "una_idea_frase"],
    },

    b4_vocabulari: {
        label: "Té un vocabulari més reduït del que necessita per al curs",
        chars: {
            tdl: {
                actiu: true,
                semantica: true,
                grau: "moderat",
            },
        },
        ajuts: ["vocabulari_frequent", "glossari_integrat", "definicions_linia"],
    },

    b5_instruccions: {
        label: "Necessita repetir o fraccionar les instruccions per poder seguir-les",
        chars: {
            tdah: {
                actiu: true,
                presentacio: "inatent",
                baixa_memoria_treball: true,
            },
        },
        ajuts: ["instruccions_numerades", "una_idea_frase"],
    },

    b6_comprensio_global: {
        label: "Capta la idea general però li costa retenir els detalls concrets",
        chars: {
            tdl: {
                actiu: true,
                comprensio_lectora: true,
                modalitat: "comprensiu",
                grau: "lleu",
            },
        },
        ajuts: ["destacats_visuals", "una_idea_frase"],
    },
};


// ── Catàleg d'ajuts pedagògics (columna dreta) ─────────────────────────────
// Agrupats per categoria. Cada ajut té un ID i un label visible.
// També mapeja a una clau de 'complements' del backend (o null si ja s'activa
// via les sub-variables del perfil).

const AJUT_CATALOG = {
    // Estructura
    fragmentar: {
        label: "Fragmentar el text en segments curts",
        grup: "estructura",
        complement: null, // ja s'activa via C-01/C-04 quan hi ha el perfil
    },
    paragrafs_curts: {
        label: "Paràgrafs curts",
        grup: "estructura",
        complement: null,
    },
    una_idea_frase: {
        label: "Una idea per frase",
        grup: "estructura",
        complement: null,
    },

    // Llengua
    vocabulari_frequent: {
        label: "Vocabulari freqüent i proper",
        grup: "llengua",
        complement: null,
    },
    glossari_integrat: {
        label: "Glossari integrat al text",
        grup: "llengua",
        complement: "glossari",
    },
    definicions_linia: {
        label: "Definicions en línia",
        grup: "llengua",
        complement: "definicions",
    },
    connectors_explicits: {
        label: "Connectors explícits (perquè, després, per tant...)",
        grup: "llengua",
        complement: null,
    },

    // Accessibilitat visual
    destacats_visuals: {
        label: "Destacats visuals dels conceptes clau",
        grup: "accessibilitat",
        complement: null,
    },
    tipografia_adaptada: {
        label: "Tipografia adaptada (dislèxia)",
        grup: "accessibilitat",
        complement: null,
    },

    // Suport cognitiu
    instruccions_numerades: {
        label: "Instruccions numerades pas a pas",
        grup: "cognitiu",
        complement: null,
    },
};

const AJUT_GRUPS = {
    estructura: "Estructura",
    llengua: "Llengua",
    accessibilitat: "Accessibilitat visual",
    cognitiu: "Suport cognitiu",
};


// ── Taula etapa+curs → MECR de referència ─────────────────────────────────
// Quan el docent diu "al nivell del curs" (Bloc A = 0), aquest és el MECR.
// Els desplaçaments (+2/+1/0/-1/-2) pugen o baixen d'un nivell per pas.

const MECR_SCALE = ["pre-A1", "A1", "A2", "B1", "B2"];

const MECR_PER_ETAPA_CURS = {
    infantil: { P3: "pre-A1", P4: "pre-A1", P5: "pre-A1" },
    primaria: {
        "1r": "pre-A1", "2n": "pre-A1",
        "3r": "A1", "4t": "A1",
        "5e": "A2", "6e": "A2",
    },
    ESO: {
        "1r": "A2", "2n": "A2",
        "3r": "B1", "4t": "B1",
    },
    batxillerat: { "1r": "B2", "2n": "B2" },
    FP: {
        "1r_CFGB": "A2", "2n_CFGB": "A2",
        "1r_CGM": "B1", "2n_CGM": "B1",
        "1r_CGS": "B2", "2n_CGS": "B2",
    },
};

function getMecrReferencia(etapa, curs) {
    const byEtapa = MECR_PER_ETAPA_CURS[etapa] || {};
    return byEtapa[curs] || "B1"; // fallback raonable
}

function applyDesfase(mecrRef, desfase) {
    // desfase: enter -2..+2
    const idx = MECR_SCALE.indexOf(mecrRef);
    if (idx === -1) return mecrRef;
    const newIdx = Math.max(0, Math.min(MECR_SCALE.length - 1, idx + desfase));
    return MECR_SCALE[newIdx];
}


// ── Fusió de característiques quan hi ha múltiples conductes ──────────────
// Si dues conductes activen 'tdah' amb sub-vars diferents, les unim.

function mergeChars(acc, add) {
    for (const [charKey, newData] of Object.entries(add)) {
        if (!acc[charKey]) {
            acc[charKey] = { ...newData };
            continue;
        }
        const existing = acc[charKey];
        for (const [subKey, subVal] of Object.entries(newData)) {
            if (subKey === "actiu") {
                existing.actiu = existing.actiu || subVal;
            } else if (typeof subVal === "boolean") {
                // OR lògic: si un diu true, queda true
                existing[subKey] = existing[subKey] === true || subVal === true;
            } else if (typeof subVal === "string") {
                // Escales ordinals (grau lleu<moderat<sever): ens quedem amb la més intensa
                if (subKey === "grau") {
                    const order = { lleu: 1, moderat: 2, sever: 3 };
                    const curr = order[existing[subKey]] || 0;
                    const next = order[subVal] || 0;
                    if (next > curr) existing[subKey] = subVal;
                } else if (!existing[subKey]) {
                    // Si no estava definit, posem-lo; si ja hi és, respectem (primer guanya)
                    existing[subKey] = subVal;
                }
            } else {
                if (existing[subKey] === undefined) existing[subKey] = subVal;
            }
        }
    }
    return acc;
}

// ── API pública del mòdul ──────────────────────────────────────────────────
// Exposat a window per ser accessible des d'app.js sense bundler.

window.ObservableMapping = {
    BEHAVIORS: OBSERVABLE_BEHAVIORS,
    AJUTS: AJUT_CATALOG,
    AJUT_GRUPS: AJUT_GRUPS,
    MECR_SCALE: MECR_SCALE,

    /** Calcula el MECR de sortida a partir del context + desplaçament del Bloc A */
    computeMecr(etapa, curs, desfase) {
        const ref = getMecrReferencia(etapa, curs);
        return applyDesfase(ref, desfase);
    },

    getMecrReferencia: getMecrReferencia,

    /**
     * Donat un array d'IDs de conductes marcades, retorna:
     *  - caracteristiques: dict compatible amb collectProfile()
     *  - ajutsAutomatics: set d'IDs d'ajuts que s'han activat automàticament
     */
    behaviorsToProfile(behaviorIds) {
        let chars = {};
        const ajuts = new Set();

        for (const bid of behaviorIds) {
            const beh = OBSERVABLE_BEHAVIORS[bid];
            if (!beh) continue;
            chars = mergeChars(chars, beh.chars);
            for (const aid of beh.ajuts) ajuts.add(aid);
        }

        return { caracteristiques: chars, ajutsAutomatics: ajuts };
    },

    /**
     * Donat un set d'IDs d'ajuts marcats (manualment o automàticament),
     * retorna el dict de complements per al payload de /api/adapt.
     */
    ajutsToComplements(ajutIds) {
        const complements = {};
        for (const aid of ajutIds) {
            const ajut = AJUT_CATALOG[aid];
            if (ajut && ajut.complement) {
                complements[ajut.complement] = true;
            }
        }
        return complements;
    },
};
