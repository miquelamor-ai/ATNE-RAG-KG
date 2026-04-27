"""
instruction_catalog.py — Catàleg de instruccions LLM amb regles d'activació i macrodirectives.

Font: docs/decisions/arquitectura_prompt_v2.md + mapa_variables_instruccions.md

Arquitectura:
  Cada instrucció pertany a una MACRODIRECTIVA (camp "macro").
  El filtre agrupa instruccions actives per macro i genera blocs temàtics
  per al prompt, sense IDs visibles per l'LLM.

Activació — 4 tipus:
  SEMPRE     → tota adaptació (instruccions nucli)
  NIVELL     → segons MECR de sortida
  PERFIL     → segons perfil alumne + sub-variables
  COMPLEMENT → segons complements activats

Macrodirectives:
  LEXIC, SINTAXI, ESTRUCTURA, COHESIO, COGNITIU, QUALITAT,
  MULTIMODAL, AVALUACIO, PERSONALITZACIO, PERFIL_*

Xifres actuals (no hardcodejar — font única: get_catalog_stats()):
  cridar instruction_catalog.get_catalog_stats() o consultar
  GET /api/stats-instruccions per obtenir recompte viu.
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
            "A-14", "A-15", "A-16", "A-17", "A-18", "A-19",
            "A-20", "A-21", "A-22", "A-23", "A-29", "A-30",
        ],
    },
    "SINTAXI": {
        "label": "SINTAXI",
        "ordre": 2,
        "instruccions_possibles": [
            "A-07", "A-08", "A-09", "A-10", "A-11",
            "A-12", "A-13", "A-24", "A-25", "A-26", "A-28",
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
            "C-01", "C-02", "C-03", "C-04", "C-05", "C-06", "C-08",
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
            "G-01", "G-02", "G-03", "G-06", "G-07",  # G-05 eliminat (fusionat amb E-08)
        ],
    },
    "PERFIL": {
        "label": "ADAPTACIONS PER PERFIL",
        "ordre": 9,
        "instruccions_possibles": [
            "H-01", "H-02", "H-03",
            "H-04", "H-05", "H-06",
            "H-07", "H-08", "H-22",
            "H-09", "H-10", "H-11",
            "H-16", "H-17", "H-23", "H-24", "H-25", "H-26",
            "H-19", "H-20", "H-20b", "H-21",
        ],
    },
    "ENRIQUIMENT": {
        "label": "⚠️ ENRIQUIMENT — NO SIMPLIFIQUIS",
        "ordre": 0,  # ordre 0 = primer bloc del prompt, que soni FORT
        "instruccions_possibles": [
            "H-12", "H-14", "H-15",
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
        "mecr_detail": {
            "pre-A1": "Elimina TOTA polisèmia: cada paraula en un sol sentit. Substitueix qualsevol mot ambigu.",
            "A1": "Elimina polisèmia: cada paraula en un sol sentit. Substitueix mots ambigus.",
            "A2": "Redueix polisèmia: una accepció per mot. Permet polisèmia si el context desambigua clarament.",
            "B1": "Controla polisèmia: evita usos figurats o poc habituals d'un mot. Permet sentits habituals.",
        },
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
        "mecr_detail": {
            "pre-A1": "Veu activa SEMPRE. Zero passives, zero impersonals.",
            "A1": "Veu activa obligatòria. Transforma totes les passives en actives.",
            "A2": "Veu activa preferent. Permet passiva només si és molt habitual ('és considerat').",
            "B1": "Prefereix veu activa. Permet passiva quan sigui natural i clara.",
        },
    },
    "A-09": {
        "text": "Subjecte explícit a cada frase. No l'elideixis.",
        "activation": "NIVELL",
        "macro": "SINTAXI",
        "mecr_detail": {
            "pre-A1": "Subjecte explícit SEMPRE. Repeteix el nom complet a cada frase.",
            "A1": "Subjecte explícit a cada frase. No elideixis mai.",
            "A2": "Subjecte explícit. Permet elisió només si el subjecte és idèntic a la frase anterior.",
            "B1": "Subjecte explícit quan hi hagi risc d'ambigüitat. Permet elisió en contextos clars.",
        },
    },
    "A-10": {
        "text": "Ordre canònic: Subjecte + Verb + Complement. Evita inversions.",
        "activation": "NIVELL",
        "macro": "SINTAXI",
        "mecr_detail": {
            "pre-A1": "Ordre SVO estricte a TOTES les frases. Zero inversions, zero dislocacions.",
            "A1": "Ordre SVO obligatori. Evita qualsevol inversió.",
            "A2": "Ordre SVO preferent. Permet tematització frontal simple ('Ahir, el Joan...').",
            "B1": "Ordre SVO per defecte. Permet inversions estilístiques si no generen ambigüitat.",
        },
    },
    "A-11": {
        "text": "Puntuació simplificada: punts i dos punts. Evita punt i coma, parèntesis llargs, guions.",
        "activation": "NIVELL",
        "macro": "SINTAXI",
        "mecr_detail": {
            "pre-A1": "Puntuació mínima: NOMÉS punts finals. Ni dos punts, ni comes entre clàusules.",
            "A1": "Puntuació simple: punts i comes. Evita dos punts, punt i coma, parèntesis.",
            "A2": "Puntuació simplificada: punts, comes i dos punts. Evita punt i coma i parèntesis llargs.",
            "B1": "Puntuació estàndard simplificada. Permet punt i coma ocasional. Evita parèntesis llargs.",
        },
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
        "activation": "NIVELL",
        "macro": "LEXIC",
        "mecr_detail": {
            "pre-A1": "Scaffolding màxim: 1a aparició = terme + definició completa + exemple visual; 2a = terme + definició; 3a = terme sol amb recordatori ('recorda: X és...').",
            "A1": "Scaffolding complet: 1a aparició = terme + definició completa; 2a = terme + definició breu; 3a en endavant = terme sol.",
            "A2": "Scaffolding estàndard: 1a aparició = terme + definició; repeticions posteriors = terme sol.",
            "B1": "Scaffolding lleuger: defineix un terme la 1a vegada; després usa'l sense definició.",
        },
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
        "mecr_detail": {
            "pre-A1": "ZERO negacions. Reformula TOTES les frases en positiu.",
            "A1": "Evita negacions. Reformula en positiu. Permet 'no' simple només si és imprescindible.",
            "A2": "Evita negacions múltiples. Permet negació simple ('no és', 'no té').",
            "B1": "Evita doble negació. Permet negació simple i natural.",
        },
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
        "mecr_detail": {
            "pre-A1": "Densitat lèxica mínima: màxim 2 paraules de contingut per frase. La resta funcionals.",
            "A1": "Densitat lèxica baixa: màxim 3 paraules de contingut per frase.",
            "A2": "Densitat lèxica controlada: màxim 4-5 paraules de contingut per frase.",
        },
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
        "mecr_detail": {
            "pre-A1": "NOMÉS present d'indicatiu. Zero subjuntiu, zero condicional, zero temps composts.",
            "A1": "Present d'indicatiu i passat simple (perfet perifràstic). Evita subjuntiu i condicional.",
            "A2": "Present, passat simple i futur perifràstic ('anirà'). Evita subjuntiu i condicional.",
        },
    },
    "A-25": {
        "text": "Formes verbals simples. Evita perífrasis verbals i construccions complexes.",
        "activation": "NIVELL",
        "macro": "SINTAXI",
        "mecr_detail": {
            "pre-A1": "ZERO perífrasis. Només formes verbals simples (present, passat, imperatiu).",
            "A1": "Formes simples. Permet 'anar a + infinitiu' i 'haver de + infinitiu'.",
            "A2": "Formes simples preferents. Permet perífrasis d'obligació i futur. Evita gerundis.",
        },
    },
    "A-26": {
        "text": "Evita incisos parentètics llargs. Si la definició allarga la frase, posa-la en frase independent.",
        "activation": "NIVELL",
        "macro": "SINTAXI",
        "mecr_detail": {
            "pre-A1": "ZERO incisos ni parèntesis. Cada informació en frase independent.",
            "A1": "Evita incisos. Definicions en frase separada, mai entre parèntesis.",
            "A2": "Permet incisos curts (3-4 mots). Definicions llargues en frase apart.",
            "B1": "Permet incisos breus i parèntesis explicatius. Evita incisos de >8 mots.",
        },
    },
    # ─── NOVA: retall per fatiga ──────────────────────────────────────────────
    "A-27": {
        "text": "Retalla el text al 60-70% de l'extensió original, prioritzant el nucli curricular. Elimina exemples secundaris i detalls no essencials.",
        "activation": "PERFIL",
        "macro": "COGNITIU",
        "profiles": ["tdah", "di"],
        "subvar_conditions": {"fatiga_o_sever": True},  # tdah.fatiga_cognitiva O tdah.grau=sever O di.grau=sever
    },
    # ─── NOVES: sessions 2026-04-09 ──────────────────────────────────────────
    "A-28": {
        "text": "Evita oracions impersonals (cal, convé, s'ha de). Dirigeix-te directament al lector: 'Tu has de...' / 'Fes...'",
        "activation": "NIVELL",
        "macro": "SINTAXI",
        "mecr_detail": {
            "pre-A1": "ZERO impersonals. Sempre 'tu' directe: 'Mira', 'Fes', 'Escriu'.",
            "A1": "Evita impersonals. Prefereix 'tu has de' a 'cal que' i 'fes' a 's'ha de fer'.",
            "A2": "Redueix impersonals. Permet 'cal' si és molt habitual, però prefereix formes directes.",
        },
    },
    "A-29": {
        "text": "Evita adverbis acabats en -ment. Reformula amb verbs o frases curtes.",
        "activation": "NIVELL",
        "macro": "LEXIC",
        "mecr_detail": {
            "pre-A1": "ZERO adverbis en -ment. 'Ràpidament' → 'molt ràpid'. 'Posteriorment' → 'després'.",
            "A1": "Evita adverbis en -ment. Substitueix per formes simples ('lentament' → 'a poc a poc').",
            "A2": "Redueix adverbis en -ment. Permet els molt habituals ('normalment', 'finalment').",
        },
    },
    "A-30": {
        "text": "Evita anglicismes i paraules d'altres idiomes. Busca equivalents habituals en català.",
        "activation": "PERFIL",
        "macro": "LEXIC",
        "profiles": ["nouvingut", "tdl"],
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
        "mecr_detail": {
            "pre-A1": "SEMPRE llista amb vinyetes. Màxim 3 ítems per llista. Mai enumeració dins del text.",
            "A1": "Llista amb vinyetes si 2+ elements. Màxim 4-5 ítems per llista.",
            "A2": "Llista si 3+ elements. Permet enumeració breu dins del text (2 elements).",
            "B1": "Llista si 4+ elements o si l'enumeració és complexa.",
        },
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
        "mecr_detail": {
            "pre-A1": "Advance organizer molt breu: 'Ara aprendràs 1 cosa: [concepte].'",
            "A1": "Advance organizer breu: 'En aquest bloc veuràs: [concepte 1] i [concepte 2].'",
            "A2": "Resum anticipatiu de 2-3 frases que presenti els conceptes clau de la secció.",
        },
    },
    "B-08": {
        "text": "Resum final recapitulatiu: tanca cada secció llarga amb un resum de les idees principals.",
        "activation": "NIVELL",
        "macro": "ESTRUCTURA",
        "mecr_detail": {
            "pre-A1": "Resum final d'1 frase molt curta: 'Hem après que [idea].'",
            "A1": "Resum final de 1-2 frases amb la idea principal.",
            "A2": "Resum final de 2-3 frases amb les idees principals.",
            "B1": "Resum recapitulatiu d'un paràgraf breu amb les idees clau i connexions.",
        },
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
        "mecr_detail": {
            "pre-A1": "Reforç CADA concepte: exemple visual + connexió amb objecte físic concret. Res en abstracte.",
            "A1": "Reforç cada concepte nou: exemple concret quotidià + suport visual.",
            "A2": "Reforç dels conceptes clau: exemple concret o connexió amb experiència propera.",
            "B1": "Reforç dels conceptes més abstractes: exemple o analogia quan la definició sola no basti.",
        },
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
        # Intensificat a _get_intensified_text: si TDAH+baixa_memoria → "2-3 elements, repeteix info clau, resums parcials"
    },
    # C-04b absorbit dins C-04 via _get_intensified_text (no cal instrucció separada)
    "C-05": {
        "text": "Glossari previ (pre-training, Sweller): comença amb '### Paraules clau' (sub-secció dins del '## Text adaptat') amb els termes essencials.",
        "activation": "NIVELL",
        "macro": "COGNITIU",
        "mecr_detail": {
            "pre-A1": "Glossari previ de 3-4 termes amb suport visual (emoji/icona) i definició de 3-4 mots.",
            "A1": "Glossari previ de 5-6 termes amb definició senzilla (5-8 mots).",
            "A2": "Glossari previ de 8-10 termes amb definició breu i un exemple.",
        },
    },
    "C-06": {
        "text": "Analogies amb experiències quotidianes: cada concepte abstracte amb un exemple del dia a dia.",
        "activation": "NIVELL",
        "macro": "COGNITIU",
        "mecr_detail": {
            "pre-A1": "Analogia amb objecte físic/concret per a CADA concepte ('l'energia és com una pila').",
            "A1": "Analogia amb experiència quotidiana per a cada concepte abstracte.",
            "A2": "Analogia amb situació familiar per als conceptes més abstractes.",
            "B1": "Analogia o comparació per als conceptes nous o complexos.",
        },
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
        "mecr_detail": {
            "pre-A1": "Exemple visual/tàctil per a CADA concepte ('la cèl·lula és com una habitació petita').",
            "A1": "Exemple quotidià concret per a cada concepte abstracte.",
            "A2": "Exemple concret per a cada concepte abstracte. Pot ser del domini de la matèria.",
            "B1": "Exemple concret o cas real per als conceptes més complexos o nous.",
        },
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
        "text": "TEA: zero implicitura — tota metàfora, ironia o sentit figurat → literal explícit. No generis ironia, sarcasme ni inferències socials implícites als exemples o complements.",
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
        # Intensificat a _get_intensified_text: si TDAH sever → "2-3 frases" (absorb H-04b)
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
        "macro": "ENRIQUIMENT",
        "profiles": ["altes_capacitats"],
    },
    # H-14: fusió de H-14 + H-14b
    "H-14": {
        "text": "Altes capacitats: PROHIBIT SIMPLIFICAR. Mantén la complexitat lingüística i conceptual original o augmenta-la. NO facis servir vocabulari freqüent, NO eliminis subordinades, NO escurcis frases, NO desnominalitzis, NO eliminis sentit figurat. Les regles universals de simplificació NO s'apliquen a aquest perfil.",
        "activation": "PERFIL",
        "macro": "ENRIQUIMENT",
        "profiles": ["altes_capacitats"],
    },
    "H-15": {
        "text": "Doble excepcionalitat (2e): EQUILIBRI — mantén repte cognitiu ALT amb suports d'accessibilitat. Adapta FORMAT (visual, segmentat) però NO el CONTINGUT intel·lectual.",
        "activation": "PERFIL",
        "macro": "ENRIQUIMENT",
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
    "H-27": {
        "text": "Discalcúlia: substitueix els nombres abstractes per representacions concretes o visuals. Quan hi hagi mesures, quantitats o estadístiques, afegeix una analogia quotidiana tangible (p.ex. '100 metres → la longitud d'un camp de futbol').",
        "activation": "PERFIL",
        "macro": "PERFIL",
        "profiles": ["discalculia"],
    },
    "H-28": {
        "text": "Discalcúlia: desglossa qualsevol seqüència numèrica o procediment pas a pas, sense saltar-ne cap. Evita que l'alumne hagi de fer càlculs mentals implícits per seguir el text.",
        "activation": "PERFIL",
        "macro": "PERFIL",
        "profiles": ["discalculia"],
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


def get_catalog_stats() -> dict:
    """Recompte viu d'instruccions del catàleg per tipus d'activació.

    Font única de veritat. Qualsevol documentació, HTML o dashboard que
    necessiti el nombre d'instruccions ha de cridar aquesta funció o
    consultar GET /api/stats-instruccions. No hardcodejar en prosa.
    """
    stats = {"total": len(CATALOG), "per_activation": {}, "per_macro": {}}
    for iid, instr in CATALOG.items():
        act = instr.get("activation", "DESCONEGUT")
        stats["per_activation"][act] = stats["per_activation"].get(act, 0) + 1
        macro = instr.get("macro", "DESCONEGUT")
        stats["per_macro"][macro] = stats["per_macro"].get(macro, 0) + 1
    return stats


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
    "discalculia": {
        "1_numerica": ["H-27"],
        "2_procedural": ["H-28"],
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
