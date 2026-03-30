"""
instruction_catalog.py — Catàleg de instruccions LLM amb regles d'activació i macrodirectives.

Font: docs/decisions/arquitectura_prompt_v2.md + mapa_variables_instruccions.md

Arquitectura:
  Cada instrucció pertany a una MACRODIRECTIVA (camp "macro").
  El filtre agrupa instruccions actives per macro i genera blocs temàtics
  per al prompt, sense IDs visibles per l'LLM.

Activació (84 instruccions efectives):
  SEMPRE     → tota adaptació (12 instruccions nucli)
  NIVELL     → segons MECR de sortida (31 instruccions)
  PERFIL     → segons perfil alumne + sub-variables (38 instruccions)
  COMPLEMENT → segons complements activats (3 instruccions)

Macrodirectives:
  LEXIC, SINTAXI, ESTRUCTURA, COHESIO, COGNITIU, QUALITAT,
  MULTIMODAL, AVALUACIO, PERSONALITZACIO, PERFIL_*
"""

# ═══════════════════════════════════════════════════════════════════════════════
# MACRODIRECTIVES: composició i ordre de presentació al prompt
# ═══════════════════════════════════════════════════════════════════════════════

MACRODIRECTIVES = {
    "LEXIC": {
        "label": "LÈXIC",
        "ordre": 1,
        "instruccions_possibles": [
            "A-01", "A-02", "A-03", "A-04", "A-05", "A-06",
            "A-15", "A-16", "A-17", "A-18", "A-19",
            "A-20", "A-21", "A-22", "A-23",
        ],
    },
    "SINTAXI": {
        "label": "SINTAXI",
        "ordre": 2,
        "instruccions_possibles": [
            "A-07", "A-08", "A-09", "A-10", "A-11",
            "A-12", "A-13", "A-24", "A-25", "A-26",
        ],
    },
    "ESTRUCTURA": {
        "label": "ESTRUCTURA",
        "ordre": 3,
        "instruccions_possibles": [
            "B-01", "B-02", "B-03", "B-04", "B-05", "B-06",
            "B-07", "B-08", "B-09", "B-10", "B-11", "B-13", "B-14",
        ],
    },
    "COGNITIU": {
        "label": "SUPORT COGNITIU",
        "ordre": 4,
        "instruccions_possibles": [
            "C-01", "C-02", "C-03", "C-04", "C-04b", "C-05", "C-06", "C-08",
            "A-27",
        ],
    },
    "QUALITAT": {
        "label": "RIGOR CURRICULAR",
        "ordre": 5,
        "instruccions_possibles": [
            "E-01", "E-02", "E-05", "E-06", "E-07", "E-08",
            "E-09", "E-10", "E-11", "E-12",
        ],
    },
    "MULTIMODAL": {
        "label": "MULTIMODALITAT",
        "ordre": 6,
        "instruccions_possibles": [
            "D-01", "D-02", "D-03", "D-06", "D-06b", "H-21",
        ],
    },
    "AVALUACIO": {
        "label": "AVALUACIÓ I COMPRENSIÓ",
        "ordre": 7,
        "instruccions_possibles": [
            "F-06", "F-09", "F-10",
        ],
    },
    "PERSONALITZACIO": {
        "label": "PERSONALITZACIÓ LINGÜÍSTICA",
        "ordre": 8,
        "instruccions_possibles": [
            "G-01", "G-02", "G-03", "G-05", "G-06", "G-07",
        ],
    },
    "PERFIL": {
        "label": "ADAPTACIONS PER PERFIL",
        "ordre": 9,
        "instruccions_possibles": [
            "H-01", "H-02", "H-03",
            "H-04", "H-04b", "H-05", "H-06",
            "H-07", "H-08", "H-22",
            "H-09", "H-10", "H-11",
            "H-12", "H-14",
            "H-15",
            "H-16", "H-17", "H-23", "H-24", "H-25", "H-26",
            "H-19", "H-20", "H-20b", "H-21",
        ],
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# CATÀLEG: cada instrucció amb ID, text, activació, macro i condicions
# ═══════════════════════════════════════════════════════════════════════════════

CATALOG = {
    # ─── A. ADAPTACIÓ LINGÜÍSTICA ─────────────────────────────────────────────

    "A-01": {
        "text": "Usa vocabulari freqüent. Substitueix termes poc habituals per equivalents d'alta freqüència lèxica.",
        "activation": "SEMPRE",
        "macro": "LEXIC",
        "suppress_if": ["altes_capacitats"],
        "suppress_if_profile": ["dislexia"],  # H-08 ja cobreix això
    },
    "A-02": {
        "text": "Termes tècnics en **negreta** amb definició entre parèntesis la primera vegada.",
        "activation": "SEMPRE",
        "macro": "LEXIC",
    },
    "A-03": {
        "text": "Repetició lèxica coherent: un terme = un concepte. NO variïs per elegància (no sinònims).",
        "activation": "SEMPRE",
        "macro": "LEXIC",
        "suppress_if": ["altes_capacitats"],
        "suppress_if_profile": ["dislexia"],  # H-08 ja cobreix això
    },
    "A-04": {
        "text": "Referents pronominals explícits: si ambigu, repeteix el nom complet.",
        "activation": "SEMPRE",
        "macro": "LEXIC",
    },
    "A-05": {
        "text": "Elimina expressions idiomàtiques, metàfores i sentit figurat. Tot literal.",
        "activation": "SEMPRE",
        "macro": "LEXIC",
        "suppress_if": ["altes_capacitats"],
        "suppress_if_profile": ["tea"],  # H-02 (zero implicitura) és superconjunt
    },
    "A-06": {
        "text": "Elimina polisèmia: cada paraula en un sol sentit. Si cal, substitueix.",
        "activation": "NIVELL",
        "macro": "LEXIC",
        "mecr_levels": ["pre-A1", "A1", "A2", "B1"],
    },
    "A-07": {
        "text": "Una idea per frase. Divideix frases llargues en unitats simples.",
        "activation": "SEMPRE",
        "macro": "SINTAXI",
        "suppress_if": ["altes_capacitats"],
    },
    "A-08": {
        "text": "Veu activa obligatòria. Transforma passives en actives.",
        "activation": "NIVELL",
        "macro": "SINTAXI",
        "mecr_levels": ["pre-A1", "A1", "A2", "B1"],
    },
    "A-09": {
        "text": "Subjecte explícit a cada frase. No l'elideixis.",
        "activation": "NIVELL",
        "macro": "SINTAXI",
        "mecr_levels": ["pre-A1", "A1", "A2", "B1"],
    },
    "A-10": {
        "text": "Ordre canònic: Subjecte + Verb + Complement. Evita inversions.",
        "activation": "NIVELL",
        "macro": "SINTAXI",
        "mecr_levels": ["pre-A1", "A1", "A2", "B1"],
    },
    "A-11": {
        "text": "Puntuació simplificada: punts i dos punts. Evita punt i coma, parèntesis llargs, guions.",
        "activation": "NIVELL",
        "macro": "SINTAXI",
        "mecr_levels": ["pre-A1", "A1", "A2", "B1"],
    },
    "A-12": {
        "text": "Limita la longitud de frase al màxim del nivell MECR de sortida.",
        "activation": "NIVELL",
        "macro": "SINTAXI",
        "mecr_detail": {
            "pre-A1": "Màxim 3-5 paraules per frase.",
            "A1": "Màxim 5-8 paraules per frase.",
            "A2": "Màxim 8-12 paraules per frase.",
            "B1": "Màxim 12-18 paraules per frase.",
            "B2": "Màxim 25 paraules per frase.",
        },
    },
    "A-13": {
        "text": "Redueix subordinades.",
        "activation": "NIVELL",
        "macro": "SINTAXI",
        "mecr_detail": {
            "pre-A1": "ZERO subordinades. Només frases simples SVO.",
            "A1": "ZERO subordinades. Només coordinades simples (i, però).",
            "A2": "Coordinades simples (i, però, perquè). NO subordinades complexes.",
            "B1": "Es permeten subordinades simples (que, quan, si).",
            "B2": "Estructures complexes permeses.",
        },
    },
    "A-14": {
        "text": "Connectors explícits entre frases: per tant, a més, en canvi, primer, després.",
        "activation": "SEMPRE",
        "macro": "LEXIC",
    },
    "A-15": {
        "text": "Scaffolding decreixent (Vygotsky): 1a aparició = terme + definició completa; 2a = terme + definició breu; 3a en endavant = terme sol.",
        "activation": "SEMPRE",
        "macro": "LEXIC",
    },
    "A-16": {
        "text": "Desnominalitza: noms abstractes → verbs. Exemple: 'l'evaporació' → 'quan s'evapora'.",
        "activation": "SEMPRE",
        "macro": "LEXIC",
        "suppress_if": ["altes_capacitats"],
    },
    "A-17": {
        "text": "Evita negacions múltiples. Reformula en positiu.",
        "activation": "NIVELL",
        "macro": "LEXIC",
        "mecr_levels": ["pre-A1", "A1", "A2", "B1"],
    },
    "A-18": {
        "text": "Dates en format complet (12 de març de 2026, no 12/03/26). Xifres amb context.",
        "activation": "SEMPRE",
        "macro": "LEXIC",
    },
    "A-19": {
        "text": "Sigles i abreviatures: escriu la forma completa la primera vegada. Ex: ONU (Organització de les Nacions Unides).",
        "activation": "SEMPRE",
        "macro": "LEXIC",
    },
    "A-20": {
        "text": "Controla la densitat lèxica: redueix la proporció de paraules de contingut per frase.",
        "activation": "NIVELL",
        "macro": "LEXIC",
        "mecr_levels": ["pre-A1", "A1", "A2"],
        "suppress_if_profile": ["tdl"],  # H-16 ja cobreix això
    },
    "A-21": {
        "text": "Descompón paraules compostes llargues: divideix o reformula en paraules simples.",
        "activation": "PERFIL",
        "macro": "LEXIC",
        "profiles": ["dislexia", "nouvingut"],
    },
    "A-22": {
        "text": "Concreta quantificadors abstractes: 'molts' → 'més de 50', 'de vegades' → '2-3 cops per setmana'.",
        "activation": "NIVELL",
        "macro": "LEXIC",
        "mecr_levels": ["pre-A1", "A1", "A2"],
    },
    "A-23": {
        "text": "Evita cultismes i llatinismes. Substitueix per equivalents patrimonials.",
        "activation": "NIVELL",
        "macro": "LEXIC",
        "mecr_levels": ["pre-A1", "A1", "A2"],
    },
    "A-24": {
        "text": "Present d'indicatiu preferent. Evita subjuntiu, condicional i temps composts.",
        "activation": "NIVELL",
        "macro": "SINTAXI",
        "mecr_levels": ["pre-A1", "A1", "A2"],
    },
    "A-25": {
        "text": "Formes verbals simples. Evita perífrasis verbals i construccions complexes.",
        "activation": "NIVELL",
        "macro": "SINTAXI",
        "mecr_levels": ["pre-A1", "A1", "A2"],
    },
    "A-26": {
        "text": "Evita incisos parentètics llargs. Si la definició allarga la frase, posa-la en frase independent.",
        "activation": "NIVELL",
        "macro": "SINTAXI",
        "mecr_levels": ["pre-A1", "A1", "A2", "B1"],
    },
    # ─── NOVA: retall per fatiga ──────────────────────────────────────────────
    "A-27": {
        "text": "Retalla el text al 60-70% de l'extensió original, prioritzant el nucli curricular. Elimina exemples secundaris i detalls no essencials.",
        "activation": "PERFIL",
        "macro": "COGNITIU",
        "profiles": ["tdah", "di"],
        "subvar_conditions": {"fatiga_o_sever": True},  # tdah.fatiga_cognitiva O tdah.grau=sever O di.grau=sever
    },

    # ─── B. ESTRUCTURA I ORGANITZACIÓ ─────────────────────────────────────────

    "B-01": {
        "text": "Paràgrafs curts: 3-5 frases màxim. Un tema per paràgraf.",
        "activation": "SEMPRE",
        "macro": "ESTRUCTURA",
    },
    "B-02": {
        "text": "Blocs temàtics amb títol descriptiu. Format pregunta quan sigui possible.",
        "activation": "SEMPRE",
        "macro": "ESTRUCTURA",
    },
    "B-03": {
        "text": "Frase tòpic al principi de cada paràgraf: anticipa el contingut.",
        "activation": "SEMPRE",
        "macro": "ESTRUCTURA",
    },
    "B-04": {
        "text": "Llistes en lloc d'enumeracions dins del text.",
        "activation": "NIVELL",
        "macro": "ESTRUCTURA",
        "mecr_levels": ["pre-A1", "A1", "A2", "B1"],
    },
    "B-05": {
        "text": "Estructura deductiva: general → particular. Primer la idea, després els detalls.",
        "activation": "NIVELL",
        "macro": "ESTRUCTURA",
        "mecr_levels": ["pre-A1", "A1", "A2", "B1"],
    },
    "B-06": {
        "text": "Ordre cronològic per a processos i seqüències.",
        "activation": "NIVELL",
        "macro": "ESTRUCTURA",
        "mecr_levels": ["pre-A1", "A1", "A2", "B1"],
    },
    "B-07": {
        "text": "Resum anticipatiu (advance organizer): comença cada secció amb una frase que anticipa el contingut.",
        "activation": "NIVELL",
        "macro": "ESTRUCTURA",
        "mecr_levels": ["pre-A1", "A1", "A2"],
    },
    "B-08": {
        "text": "Resum final recapitulatiu: tanca cada secció llarga amb un resum de les idees principals.",
        "activation": "NIVELL",
        "macro": "ESTRUCTURA",
        "mecr_levels": ["pre-A1", "A1", "A2", "B1"],
    },
    "B-09": {
        "text": "Numera els passos i seqüències. Cada pas en línia separada.",
        "activation": "NIVELL",
        "macro": "ESTRUCTURA",
        "mecr_levels": ["pre-A1", "A1", "A2", "B1"],
    },
    "B-10": {
        "text": "Transicions entre seccions: 'Ja hem vist X. Ara veurem Y.'",
        "activation": "SEMPRE",
        "macro": "ESTRUCTURA",
    },
    "B-11": {
        "text": "Salt de línia entre idees. Cada idea en paràgraf o línia independent.",
        "activation": "NIVELL",
        "macro": "ESTRUCTURA",
        "mecr_levels": ["pre-A1", "A1", "A2"],
    },
    "B-13": {
        "text": "Indicadors de progrés: [Secció X de Y] al principi de cada bloc.",
        "activation": "PERFIL",
        "macro": "ESTRUCTURA",
        "profiles": ["tdah"],
    },
    "B-14": {
        "text": "Taules per informació comparativa. Usa markdown: | Col1 | Col2 |",
        "activation": "NIVELL",
        "macro": "ESTRUCTURA",
        "mecr_levels": ["pre-A1", "A1", "A2", "B1"],
    },

    # ─── C. SUPORT COGNITIU ───────────────────────────────────────────────────

    "C-01": {
        "text": "Limita conceptes nous per paràgraf.",
        "activation": "NIVELL",
        "macro": "COGNITIU",
        "mecr_detail": {
            "pre-A1": "Màxim 1 concepte nou per paràgraf.",
            "A1": "Màxim 1-2 conceptes nous per paràgraf.",
            "A2": "Màxim 2 conceptes nous per paràgraf.",
            "B1": "Màxim 3 conceptes nous per paràgraf.",
            "B2": "Densitat conceptual estàndard.",
        },
        # baixa_memoria_treball intensifica: 1-2 → 1, 2 → 1-2, etc.
    },
    "C-02": {
        "text": "Reforç immediat de cada concepte nou: exemple concret, suport visual o connexió amb el quotidià.",
        "activation": "NIVELL",
        "macro": "COGNITIU",
        "mecr_levels": ["pre-A1", "A1", "A2", "B1"],
    },
    "C-03": {
        "text": "Eliminació de redundància decorativa (principi de coherència, Mayer): cada element ha de tenir funció pedagògica clara.",
        "activation": "SEMPRE",
        "macro": "QUALITAT",
    },
    "C-04": {
        "text": "Chunking: agrupa informació en blocs de 3-5 elements (límit memòria de treball).",
        "activation": "SEMPRE",
        "macro": "COGNITIU",
    },
    "C-04b": {
        "text": "Memòria de treball baixa: redueix blocs a 2-3 elements (no 3-5). Repeteix informació clau a cada bloc. Afegeix resums parcials cada 2-3 paràgrafs.",
        "activation": "PERFIL",
        "macro": "COGNITIU",
        "profiles": ["tdah"],
        "subvar_conditions": {"baixa_memoria_treball": True},
    },
    "C-05": {
        "text": "Glossari previ (pre-training, Sweller): comença amb '## Paraules clau' amb els termes essencials.",
        "activation": "NIVELL",
        "macro": "COGNITIU",
        "mecr_levels": ["pre-A1", "A1", "A2"],
    },
    "C-06": {
        "text": "Analogies amb experiències quotidianes: cada concepte abstracte amb un exemple del dia a dia.",
        "activation": "NIVELL",
        "macro": "COGNITIU",
        "mecr_levels": ["pre-A1", "A1", "A2", "B1"],
    },
    "C-08": {
        "text": "Anticipació de vocabulari: els termes clau apareixen primer al glossari, després al text.",
        "activation": "NIVELL",
        "macro": "COGNITIU",
        "mecr_levels": ["pre-A1", "A1", "A2"],
    },

    # ─── D. MULTIMODALITAT (només les que executa l'LLM) ─────────────────────

    "D-01": {
        "text": "Emojis/icones de suport al costat dels conceptes clau (☀️ llum, 💧 aigua, 🌱 planta).",
        "activation": "COMPLEMENT",
        "macro": "MULTIMODAL",
        "complement": "pictogrames",
    },
    "D-02": {
        "text": "Esquema de procés en format text (fletxes, símbols) per mostrar relacions causa-efecte.",
        "activation": "COMPLEMENT",
        "macro": "MULTIMODAL",
        "complement": "esquema_visual",
    },
    "D-03": {
        "text": "Mapa conceptual jeràrquic en format text (arbre amb branques).",
        "activation": "COMPLEMENT",
        "macro": "MULTIMODAL",
        "complement": "mapa_conceptual",
    },
    "D-06": {
        "text": "Prepara el text per a lectura en veu alta: frases amb ritme natural, pauses clares (punts).",
        "activation": "PERFIL",
        "macro": "MULTIMODAL",
        "profiles": ["discapacitat_intellectual", "di", "discapacitat_visual", "disc_visual"],
    },
    "D-06b": {
        "text": "Dislèxia moderada/severa: prepara el text per a lectura en veu alta com a canal principal d'accés. Frases curtes amb ritme natural, pauses clares, evita encavalcaments fonètics.",
        "activation": "PERFIL",
        "macro": "MULTIMODAL",
        "profiles": ["dislexia"],
        "subvar_conditions": {"dislexia_moderat_sever": True},
    },

    # ─── E. CONTINGUT CURRICULAR ──────────────────────────────────────────────
    # NOTA: E-04 eliminat (duplicat de G-01). E-08 fusionat amb G-05.

    "E-01": {
        "text": "Nucli terminològic intocable: MAI substitueixis un terme tècnic curricular per un de col·loquial.",
        "activation": "SEMPRE",
        "macro": "QUALITAT",
    },
    "E-02": {
        "text": "Gradua la definició tècnica segons MECR.",
        "activation": "NIVELL",
        "macro": "QUALITAT",
        "mecr_detail": {
            "pre-A1": "Definició en 3-4 paraules molt bàsiques.",
            "A1": "Definició en 5-8 paraules senzilles.",
            "A2": "Definició breu amb un exemple.",
            "B1": "Definició estàndard amb context.",
            "B2": "Definició acadèmica completa.",
        },
    },
    "E-05": {
        "text": "Mantén l'exactitud científica: les simplificacions lingüístiques NO poden introduir errors conceptuals.",
        "activation": "SEMPRE",
        "macro": "QUALITAT",
    },
    "E-06": {
        "text": "Simplifica processos mantenint la causalitat: la cadena causa→efecte ha de ser completa.",
        "activation": "SEMPRE",
        "macro": "QUALITAT",
    },
    "E-07": {
        "text": "Un exemple concret per cada concepte abstracte.",
        "activation": "NIVELL",
        "macro": "QUALITAT",
        "mecr_levels": ["pre-A1", "A1", "A2", "B1"],
    },
    # E-08 fusionat amb G-05 → queda E-08 com a instrucció única
    "E-08": {
        "text": "Referents culturalment diversos: substitueix referents locals per universals o explica'ls breument. Evita supòsits culturals implícits.",
        "activation": "PERFIL",
        "macro": "QUALITAT",
        "profiles": ["nouvingut", "vulnerabilitat"],
    },
    "E-09": {
        "text": "Evita supòsits culturals implícits: no pressuposar coneixement de festes, tradicions, geografia local.",
        "activation": "PERFIL",
        "macro": "QUALITAT",
        "profiles": ["nouvingut"],
    },
    "E-10": {
        "text": "Sensibilitat a temes traumàtics: evita o contextualitza temes de violència, guerra, separació, mort.",
        "activation": "PERFIL",
        "macro": "QUALITAT",
        "profiles": ["trastorn_emocional", "vulnerabilitat"],
        "subvar_conditions": {"sensibilitat_tematica": True},
    },
    "E-11": {
        "text": "Pistes etimològiques translingües: aprofita arrels llatines/gregues compartides entre català i L1.",
        "activation": "PERFIL",
        "macro": "QUALITAT",
        "profiles": ["nouvingut"],
        "subvar_conditions": {"L1_romanica": True},
    },
    "E-12": {
        "text": "Contra-exemples per delimitar conceptes: 'Això SÍ és X, però això NO és X perquè...'",
        "activation": "NIVELL",
        "macro": "QUALITAT",
        "mecr_levels": ["B1", "B2"],
    },

    # ─── F. AVALUACIÓ I COMPRENSIÓ ────────────────────────────────────────────
    # NOTA: F-10 absorbeix H-13 (eren duplicats)

    "F-06": {
        "text": "Preguntes de comprensió intercalades dins del text: cada 2-3 paràgrafs, una pregunta ràpida.",
        "activation": "PERFIL",
        "macro": "AVALUACIO",
        "profiles": ["tdah"],
    },
    "F-09": {
        "text": "Preguntes de pensament crític: per què? i si...? quines alternatives? quines limitacions?",
        "activation": "PERFIL",
        "macro": "AVALUACIO",
        "profiles": ["altes_capacitats"],
    },
    "F-10": {
        "text": "Connexions interdisciplinars: relaciona el contingut amb altres matèries i àmbits de coneixement.",
        "activation": "PERFIL",
        "macro": "AVALUACIO",
        "profiles": ["altes_capacitats"],
    },

    # ─── G. PERSONALITZACIÓ LINGÜÍSTICA ───────────────────────────────────────
    # NOTA: G-05 eliminat (fusionat amb E-08)

    "G-01": {
        "text": "Glossari bilingüe complet: cada terme tècnic amb traducció a L1 (en alfabet original si escau).\nEXEMPLE OBLIGATORI de format glossari bilingüe:\n| Terme | Traducció L1 | Explicació |\n| **Fotosíntesi** | تمثيل ضوئي (àrab) / 光合作用 (xinès) | les plantes fan menjar amb llum |\nSi la L1 no és llatina, escriu els termes en l'alfabet original.",
        "activation": "PERFIL",
        "macro": "PERSONALITZACIO",
        "profiles": ["nouvingut"],
    },
    "G-02": {
        "text": "Traducció parcial de consignes bàsiques a L1: 'Llegeix' / اقرأ, 'Respon' / أجب, etc.",
        "activation": "PERFIL",
        "macro": "PERSONALITZACIO",
        "profiles": ["nouvingut"],
        "subvar_conditions": {"mecr_low": True},
    },
    "G-03": {
        "text": "Transliteració fonètica OBLIGATÒRIA al glossari: cada terme català ha d'aparèixer escrit en l'alfabet de L1 al costat.\nEXEMPLE: fotosíntesi → فوتوسينتيسي (àrab) / 福托辛特西 (xinès)",
        "activation": "PERFIL",
        "macro": "PERSONALITZACIO",
        "profiles": ["nouvingut"],
        "subvar_conditions": {"alfabet_llati": False},
    },
    "G-06": {
        "text": "Ajusta el to segons MECR.",
        "activation": "NIVELL",
        "macro": "PERSONALITZACIO",
        "mecr_detail": {
            "pre-A1": "To molt conversacional i directe ('Mira! Les plantes...').",
            "A1": "To conversacional i proper ('Ara aprendràs...').",
            "A2": "To conversacional-proper ('En aquesta secció veurem...').",
            "B1": "To proper i acadèmic bàsic.",
            "B2": "To acadèmic complet.",
        },
    },

    "G-07": {
        "text": "Nouvingut sense CALP: estructura discursiva molt explícita. Marca clarament què és una definició, què és un exemple, què és una conclusió. Usa frase tòpic a cada paràgraf.",
        "activation": "PERFIL",
        "macro": "PERSONALITZACIO",
        "profiles": ["nouvingut"],
        "subvar_conditions": {"calp_inicial": True},
    },

    # ─── H. ADAPTACIONS ESPECÍFIQUES PER PERFIL ──────────────────────────────
    # NOTA: H-13 eliminat (duplicat de F-10). H-14b fusionat amb H-14.

    "H-01": {
        "text": "TEA: estructura predictible i fixa — sempre: títol → definició → exemple → activitat.",
        "activation": "PERFIL",
        "macro": "PERFIL",
        "profiles": ["tea"],
    },
    "H-02": {
        "text": "TEA: zero implicitura — tota metàfora, ironia o sentit figurat → literal explícit.",
        "activation": "PERFIL",
        "macro": "PERFIL",
        "profiles": ["tea"],
    },
    "H-03": {
        "text": "TEA: anticipació de canvis — avisa sempre: 'Ara canviem de tema.', 'A continuació veurem...'",
        "activation": "PERFIL",
        "macro": "PERFIL",
        "profiles": ["tea"],
    },
    "H-04": {
        "text": "Micro-blocs de 3-5 frases amb objectiu explícit per bloc ('En aquest bloc aprendràs...').",
        "activation": "PERFIL",
        "macro": "PERFIL",
        "profiles": ["tdah", "trastorn_emocional"],
    },
    "H-04b": {
        "text": "TDAH sever: micro-blocs de 2-3 frases (no 3-5). Objectiu molt curt i concret per bloc.",
        "activation": "PERFIL",
        "macro": "PERFIL",
        "profiles": ["tdah"],
        "subvar_conditions": {"tdah_sever": True},
    },
    "H-05": {
        "text": "TDAH: retroalimentació visual de progrés — barres, percentatges, indicadors visuals.",
        "activation": "PERFIL",
        "macro": "PERFIL",
        "profiles": ["tdah"],
    },
    "H-06": {
        "text": "TDAH: variació dins el text — alterna lectura, esquema, pregunta per mantenir l'atenció.",
        "activation": "PERFIL",
        "macro": "PERFIL",
        "profiles": ["tdah"],
    },
    "H-07": {
        "text": "Dislèxia (Dehaene/Wolf): evita paraules compostes llargues. Divideix o reformula.",
        "activation": "PERFIL",
        "macro": "PERFIL",
        "profiles": ["dislexia"],
    },
    "H-08": {
        "text": "Dislèxia: paraules d'alta freqüència. Repeteix termes clau en lloc d'usar sinònims.",
        "activation": "PERFIL",
        "macro": "PERFIL",
        "profiles": ["dislexia"],
    },
    "H-09": {
        "text": "Discapacitat intel·lectual: UN sol concepte nou per bloc. No barrejar idees.",
        "activation": "PERFIL",
        "macro": "PERFIL",
        "profiles": ["discapacitat_intellectual", "di"],
    },
    "H-10": {
        "text": "Discapacitat intel·lectual: concreció radical — cada concepte abstracte amb exemple tangible i quotidià.",
        "activation": "PERFIL",
        "macro": "PERFIL",
        "profiles": ["discapacitat_intellectual", "di"],
    },
    "H-11": {
        "text": "Discapacitat intel·lectual: repetició sistemàtica en formats diversos (text, esquema, exemple).",
        "activation": "PERFIL",
        "macro": "PERFIL",
        "profiles": ["discapacitat_intellectual", "di"],
    },
    "H-12": {
        "text": "Altes capacitats: profundització conceptual — excepcions, fronteres del coneixement, debats oberts.",
        "activation": "PERFIL",
        "macro": "PERFIL",
        "profiles": ["altes_capacitats"],
    },
    # H-14: fusió de H-14 + H-14b
    "H-14": {
        "text": "Altes capacitats: PROHIBIT SIMPLIFICAR. Mantén la complexitat lingüística i conceptual original o augmenta-la. NO facis servir vocabulari freqüent, NO eliminis subordinades, NO escurcis frases, NO desnominalitzis, NO eliminis sentit figurat. Les regles universals de simplificació NO s'apliquen a aquest perfil.",
        "activation": "PERFIL",
        "macro": "PERFIL",
        "profiles": ["altes_capacitats"],
    },
    "H-15": {
        "text": "Doble excepcionalitat (2e): EQUILIBRI — mantén repte cognitiu ALT amb suports d'accessibilitat. Adapta FORMAT (visual, segmentat) però NO el CONTINGUT intel·lectual.",
        "activation": "PERFIL",
        "macro": "PERFIL",
        "profiles": ["2e"],
    },
    "H-16": {
        "text": "TDL: reducció màxima de densitat lèxica. Cada frase amb el mínim de paraules de contingut.",
        "activation": "PERFIL",
        "macro": "PERFIL",
        "profiles": ["tdl"],
    },
    "H-17": {
        "text": "TDL: modelatge d'ús en context — cada terme tècnic apareix en 2-3 contextos diferents.",
        "activation": "PERFIL",
        "macro": "PERFIL",
        "profiles": ["tdl"],
    },
    "H-23": {
        "text": "TDL receptiu: simplificació lingüística reforçada en TOT el text. L'alumne té dificultat per comprendre, no només per produir.",
        "activation": "PERFIL",
        "macro": "PERFIL",
        "profiles": ["tdl"],
        "subvar_conditions": {"tdl_receptiu": True},
    },
    "H-24": {
        "text": "TDL amb semàntica afectada: redueix vocabulari al mínim funcional. Cada paraula de contingut ha de ser d'alta freqüència o estar definida.",
        "activation": "PERFIL",
        "macro": "PERFIL",
        "profiles": ["tdl"],
        "subvar_conditions": {"tdl_semantica": True},
    },
    "H-25": {
        "text": "TDL amb morfosintaxi afectada: estructura SVO estricta. Evita passives, subordinades, relatius i ordre no canònic.",
        "activation": "PERFIL",
        "macro": "PERFIL",
        "profiles": ["tdl"],
        "subvar_conditions": {"tdl_morfosintaxi": True},
    },
    "H-26": {
        "text": "TDL amb pragmàtica afectada: fes explícita tota intenció comunicativa. No pressuposar que l'alumne infereix el propòsit del text.",
        "activation": "PERFIL",
        "macro": "PERFIL",
        "profiles": ["tdl"],
        "subvar_conditions": {"tdl_pragmatica": True},
    },
    "H-19": {
        "text": "Discapacitat visual: estructura semàntica amb encapçalaments (H1-H3) per lector de pantalla. NO dependre de colors o posicions.",
        "activation": "PERFIL",
        "macro": "PERFIL",
        "profiles": ["discapacitat_visual", "disc_visual"],
    },
    "H-20": {
        "text": "Discapacitat auditiva: simplificació com L2 en sordesa prelocutiva signant.",
        "activation": "PERFIL",
        "macro": "PERFIL",
        "profiles": ["discapacitat_auditiva", "disc_auditiva"],
    },
    "H-20b": {
        "text": "Disc. auditiva LSC: el català escrit és una L2. Simplificació sintàctica reforçada, suport visual per tot contingut, glossari amb suport visual.",
        "activation": "PERFIL",
        "macro": "PERFIL",
        "profiles": ["disc_auditiva", "discapacitat_auditiva"],
        "subvar_conditions": {"comunicacio_lsc": True},
    },

    # ─── NOVES INSTRUCCIONS ───────────────────────────────────────────────────

    "H-21": {
        "text": "Discapacitat visual (ceguesa): descriu textualment qualsevol element visual del text original (taules, gràfics, esquemes) de forma seqüencial i completa.",
        "activation": "PERFIL",
        "macro": "PERFIL",
        "profiles": ["discapacitat_visual", "disc_visual"],
        "subvar_conditions": {"grau_ceguesa": True},
    },
    "H-22": {
        "text": "Dislèxia fonològica: evita encadenar prefixos i sufixos en una mateixa paraula. Reformula: 'descontextualitzar' → 'treure del context'.",
        "activation": "PERFIL",
        "macro": "PERFIL",
        "profiles": ["dislexia"],
        "subvar_conditions": {"tipus_fonologica": True},
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# MAPA PERFIL → INSTRUCCIONS PRIORITZADES
# ═══════════════════════════════════════════════════════════════════════════════

PROFILE_INSTRUCTION_MAP = {
    "nouvingut": {
        "1_lexica": ["A-01", "A-02", "A-04", "A-05", "A-06", "A-20", "A-21"],
        "2_cultural": ["E-08", "E-09", "E-10", "G-01"],
        "3_sintactica": ["A-07", "A-09", "A-12", "A-13", "A-24", "A-25"],
        "4_estructura": ["B-01", "B-02", "B-07", "C-05", "C-08"],
    },
    "tea": {
        "1_inferencia": ["H-01", "H-02", "A-05", "A-06"],
        "2_estructura": ["H-03", "B-02", "B-06", "B-09"],
        "3_lexica": ["A-03", "A-04"],
        "4_discursiva": ["B-03", "B-10"],
    },
    "tdah": {
        "1_atencio": ["H-04", "B-13", "H-06"],
        "2_memoria": ["C-04", "C-01", "B-01"],
        "3_motivacio": ["H-05", "F-06"],
    },
    "dislexia": {
        "1_decodificacio": ["H-07", "H-08", "A-21"],
        "2_compensacio": ["D-06", "A-03"],
    },
    "tdl": {
        "1_lexica": ["H-16", "A-01", "A-02", "A-20"],
        "2_sintactica": ["H-17", "A-07", "A-13", "A-26"],
        "3_memoria": ["C-04", "C-05"],
    },
    "discapacitat_intellectual": {
        "1_discursiva": ["H-09", "H-10", "H-11"],
        "2_inferencia": ["C-01", "C-06"],
        "3_lexica": ["A-01", "A-12", "A-22"],
        "4_visual": ["D-01"],
    },
    "discapacitat_visual": {
        "1_percepcio": ["H-19"],
        "2_estructura": ["B-02", "B-14"],
    },
    "discapacitat_auditiva": {
        "1_lexica": ["H-20", "A-01", "A-07", "A-12", "A-13"],
        "2_visual": ["D-01", "D-02"],
    },
    "altes_capacitats": {
        "1_motivacio": ["H-12", "H-14"],
        "2_repte": ["F-09", "F-10"],
    },
    "2e": {
        "1_equilibri": ["H-15"],
    },
    "vulnerabilitat": {
        "1_motivacio": ["E-10", "A-01"],
        "2_cultural": ["E-08", "E-09"],
        "3_estructura": ["B-01", "B-02", "C-06"],
    },
    "trastorn_emocional": {
        "1_emocional": ["E-10"],
        "2_atencio": ["H-04", "B-01"],
        "3_seguretat": ["B-07"],
    },
    "tdc": {
        "1_estructura": ["B-02", "B-09", "H-19"],
        "2_compensacio": ["B-04", "B-14"],
    },
    "disc_motora": {
        "1_estructura": ["B-02", "H-19"],
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# Llengües romàniques (per activar E-11 pistes etimològiques)
# ═══════════════════════════════════════════════════════════════════════════════

LLENGUES_ROMANIQUES = {
    "castellà", "espanyol", "castellano", "español",
    "francès", "francés", "français",
    "italià", "italiano",
    "portuguès", "português",
    "romanès", "română",
    "gallec", "galego",
    "occità", "occitan",
}
