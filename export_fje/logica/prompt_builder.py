

def _get_active_profiles(profile: dict) -> list[str]:
    """Retorna llista de claus de perfils actius."""
    chars = profile.get("caracteristiques", {})
    return [key for key, val in chars.items() if val.get("actiu")]


def _str_to_bool(val) -> bool:
    """Converteix string a bool de forma tolerant."""
    if isinstance(val, bool):
        return val
    if isinstance(val, str):
        return val.lower() in ("true", "1", "sí", "si")
    return bool(val)


def build_persona_audience(profile: dict, context: dict, mecr: str) -> str:
    """
    Genera narrativa concreta de l'alumne (persona-audience pattern).

    Aprofita TOTES les sub-variables de tipus NARRATIVA per donar a l'LLM
    una imatge rica de per a qui escriu, no només etiquetes abstractes.
    """
    chars = profile.get("caracteristiques", {})
    lines = []

    etapa = context.get("etapa", "ESO")
    curs = context.get("curs", "")
    header = f"Escrius per a un alumne de {etapa}"
    if curs:
        header += f" ({curs})"
    lines.append(header + ".")

    for key, val in chars.items():
        if not val.get("actiu"):
            continue

        if key == "nouvingut":
            l1 = val.get("L1", "")
            frag = "Alumne nouvingut"
            if l1:
                frag += f" que parla {l1} com a L1"
            lines.append(frag + ".")

            alfabet = val.get("alfabet_llati", True)
            if isinstance(alfabet, str):
                alfabet = alfabet.lower() not in ("no", "false", "0")
            if not alfabet:
                lines.append("Alfabet no llatí: necessita transliteració fonètica.")

            esc = val.get("escolaritzacio_previa", "si")
            if esc == "no":
                lines.append("No ha estat escolaritzat regularment al seu país d'origen. No familiaritzat amb gèneres escolars.")
            elif esc == "parcial":
                lines.append("Escolarització prèvia parcial o interrompuda.")

            calp = val.get("calp", "")
            if calp == "inicial":
                lines.append("Llengua acadèmica (CALP) inicial: no domina el registre escolar ni vocabulari abstracte de les matèries. Termes com 'justifica', 'argumenta', 'analitza' poden ser incomprensibles.")
            elif calp == "emergent":
                lines.append("Llengua acadèmica (CALP) emergent: entén consignes bàsiques però li costa el vocabulari abstracte.")

        elif key == "tea":
            nivell = val.get("nivell_suport", "1")
            com = val.get("comunicacio_oral", "fluida")
            frag = f"TEA, nivell de suport {nivell} (DSM-5)"
            if com == "no_verbal":
                frag += ". Comunicació oral no verbal: depèn totalment del canal visual i escrit"
            elif com == "limitada":
                frag += ". Comunicació oral limitada: necessita més suport visual"
            lines.append(frag + ".")

        elif key == "tdah":
            pres = val.get("presentacio", "combinat")
            grau = val.get("grau", "")
            frag = f"TDAH, presentació {pres}"
            if grau:
                frag += f" (grau {grau})"
            lines.append(frag + ".")

            if _str_to_bool(val.get("baixa_memoria_treball", False)):
                lines.append("Memòria de treball baixa: limitar elements simultanis, repetir informació clau.")
            if _str_to_bool(val.get("fatiga_cognitiva", False)):
                lines.append("Fatiga cognitiva: es cansa ràpid amb textos llargs, necessita text reduït i pauses visuals.")

        elif key == "dislexia":
            tipus = val.get("tipus_dislexia", "")
            grau = val.get("grau", "")
            frag = "Dislèxia"
            if tipus:
                frag += f" {tipus}"
            if grau:
                frag += f" (grau {grau})"
            lines.append(frag + ".")

        elif key == "altes_capacitats":
            tipus = val.get("tipus_capacitat", "global")
            if tipus == "talent_especific":
                lines.append("Altes capacitats: talent específic. NO simplificar. Enriquir amb profunditat i connexions interdisciplinars.")
            else:
                lines.append("Altes capacitats globals. NO simplificar. Enriquir amb profunditat i connexions interdisciplinars.")

        elif key in ("di", "discapacitat_intellectual"):
            grau = val.get("grau", "lleu")
            lines.append(f"Discapacitat intel·lectual (grau {grau}). Necessita concreció radical i repetició sistemàtica.")

        elif key == "tdl":
            modalitat = val.get("modalitat", "")
            grau = val.get("grau", "")
            frag = "TDL (Trastorn del Llenguatge)"
            if modalitat:
                frag += f", afectació {modalitat}"
            if grau:
                frag += f" (grau {grau})"
            lines.append(frag + ".")

            afectacions = []
            if _str_to_bool(val.get("morfosintaxi", False)):
                afectacions.append("morfosintaxi")
            if _str_to_bool(val.get("semantica", False)):
                afectacions.append("semàntica/lèxic")
            if _str_to_bool(val.get("pragmatica", False)):
                afectacions.append("pragmàtica")
            if _str_to_bool(val.get("discurs_narrativa", False)):
                afectacions.append("discurs/narrativa")
            if afectacions:
                lines.append(f"Àrees afectades: {', '.join(afectacions)}.")

            if _str_to_bool(val.get("bilingue", False)):
                lines.append("Context bilingüe/plurilingüe.")

        elif key in ("disc_visual", "discapacitat_visual"):
            grau = val.get("grau", "baixa_visio_moderada")
            etiquetes = {
                "baixa_visio_moderada": "baixa visió moderada",
                "baixa_visio_greu": "baixa visió greu",
                "ceguesa": "ceguesa",
            }
            lines.append(f"Discapacitat visual: {etiquetes.get(grau, grau)}.")

        elif key in ("disc_auditiva", "discapacitat_auditiva"):
            com = val.get("comunicacio", "oral")
            impl = _str_to_bool(val.get("implant_coclear", False))
            frag = "Discapacitat auditiva"
            if com == "LSC":
                frag += ", comunicació en Llengua de Signes Catalana. Tractar el català escrit com a L2"
            elif com == "bimodal":
                frag += ", comunicació bimodal (oral + signes)"
            if impl:
                frag += ". Porta implant coclear (accés auditiu parcial)"
            lines.append(frag + ".")

        elif key == "trastorn_emocional":
            if _str_to_bool(val.get("sensibilitat_tematica", False)):
                lines.append("Trastorn emocional/conductual. Sensibilitat temàtica: evitar temes de violència, separació, mort.")
            else:
                lines.append("Trastorn emocional/conductual.")

        elif key == "vulnerabilitat":
            if _str_to_bool(val.get("sensibilitat_tematica", False)):
                lines.append("Vulnerabilitat socioeducativa. Sensibilitat temàtica: evitar temes potencialment traumàtics.")
            else:
                lines.append("Vulnerabilitat socioeducativa.")

        elif key == "tdc":
            grau = val.get("grau", "")
            frag = "TDC/Dispraxia"
            if grau:
                frag += f" (grau {grau})"
            lines.append(frag + ".")

        elif key == "2e":
            lines.append("Doble excepcionalitat (2e): combina altes capacitats amb una necessitat d'accessibilitat. Mantenir repte intel·lectual ALT amb suports de format.")

        else:
            lines.append(f"Amb {key.replace('_', ' ')}.")

    lines.append(f"Nivell MECR de sortida: {mecr}.")

    obs = profile.get("observacions", "")
    if obs:
        lines.append(f"Observació del docent: {obs}")

    return "\n".join(lines)


def build_system_prompt(profile: dict, context: dict, params: dict, rag_context: str) -> str:
    """Munta el system prompt v2 en 4 capes — instruccions filtrades del catàleg de 89."""
    parts = []
    mecr = params.get("mecr_sortida", "B2")
    dua = params.get("dua", "Core")

    # ═══ CAPA 1: IDENTITAT (fixa) ═══
    parts.append(corpus_reader.get_identity())

    # ═══ CAPES 2-3: INSTRUCCIONS FILTRADES (catàleg de 89 instruccions LLM) ═══
    # Filtra segons perfils actius, sub-variables, MECR, DUA i complements
    filtered = instruction_filter.get_instructions(profile, params)
    instructions_text = instruction_filter.format_instructions_for_prompt(filtered)
    parts.append(instructions_text)

    # DUA (bloc del corpus — complementa les instruccions filtrades)
    dua_block = corpus_reader.get_dua_block(dua)
    if dua_block:
        parts.append(dua_block)

    # Gènere discursiu (si indicat)
    genre = params.get("genere_discursiu", "")
    if genre:
        genre_block = corpus_reader.get_genre_block(genre)
        if genre_block:
            parts.append(genre_block)

    # Creuaments (si 2+ perfils actius)
    active_profiles = _get_active_profiles(profile)
    crossing_blocks = corpus_reader.get_crossing_blocks(active_profiles)
    for cb_text in crossing_blocks:
        parts.append(cb_text)

    # Resolució conflictes (si nivell baix o DUA Accés)
    if mecr in ("pre-A1", "A1", "A2") or dua == "Acces":
        conflict = corpus_reader.get_conflict_resolution()
        if conflict:
            parts.append(conflict)

    # Few-shot example
    fewshot = corpus_reader.get_fewshot_example(mecr)
    if fewshot:
        parts.append(f"EXEMPLE DE SORTIDA ESPERADA ({mecr}):\n{fewshot}")

    # ═══ CAPA 4: CONTEXT (variable) ═══

    # 4a. Context educatiu
    parts.append(f"""CONTEXT EDUCATIU:
- Etapa: {context.get('etapa', 'ESO')}
- Curs: {context.get('curs', '')}
- Àmbit: {context.get('ambit', '')}
- Matèria: {context.get('materia', '')}""")

    # 4b. Persona-audience
    persona = build_persona_audience(profile, context, mecr)
    parts.append(f"PERSONA-AUDIENCE:\n{persona}")

    # 4c. Context RAG pedagògic
    if rag_context:
        parts.append(f"CONEIXEMENT PEDAGÒGIC DE REFERÈNCIA (corpus FJE):\n{rag_context}")

    # Complements activats
    comp = params.get("complements", {})
    comp_actius = [k.replace("_", " ").title() for k, v in comp.items() if v]
    parts.append(f"""
COMPLEMENTS A GENERAR (a més del text adaptat):
{chr(10).join('- ' + c for c in comp_actius) if comp_actius else '- Cap complement addicional'}
""")

    # Instruccions de sortida — detallades per complement
    # Detectar quins complements estan actius per donar instruccions específiques
    comp = params.get("complements", {})
    # Extreure L1 del perfil nouvingut (si existeix)
    chars = profile.get("caracteristiques", {})
    l1 = chars.get("nouvingut", {}).get("L1", "")
    l1_display = l1 if l1 else "la llengua materna de l'alumne"

    output_sections = []
    output_sections.append("""
FORMAT DE SORTIDA:
Respon EXACTAMENT amb les seccions següents, separades per encapçalaments ## .
Genera NOMÉS les seccions indicades com ACTIVADES.

## Text adaptat
El text complet adaptat segons tots els paràmetres indicats.
- Estructura clara amb salts de línia entre idees
- Termes tècnics en **negreta** amb definició entre parèntesis la primera vegada
- Una idea per frase
- Si el nivell és A1 o inferior: frases molt curtes, vocabulari quotidià, sense subordinades
""")

    if comp.get("glossari"):
        output_sections.append(f"""
## Glossari
ACTIVAT — Genera una TAULA MARKDOWN amb 3 columnes:
| Terme | Traducció ({l1_display}) | Explicació simple |
Inclou tots els termes tècnics o difícils del text adaptat (mínim 8-12 termes).
La columna de traducció ha de contenir la traducció REAL al/a la {l1_display} (en el seu alfabet original si escau: àrab, xinès, urdú, etc.).
L'explicació ha de ser en català molt senzill (nivell A1).
""")

    if comp.get("negretes"):
        output_sections.append("""
## Negretes
ACTIVAT — Ja integrat al text adaptat (termes clau en **negreta**). No cal secció separada.
""")

    if comp.get("definicions_integrades"):
        output_sections.append("""
## Definicions integrades
ACTIVAT — Ja integrat al text adaptat (definicions entre parèntesis). No cal secció separada.
""")

    if comp.get("traduccio_l1"):
        output_sections.append(f"""
## Traducció L1
ACTIVAT — Ja integrat al glossari (columna de traducció a {l1_display}). No cal secció separada.
""")

    if comp.get("pictogrames"):
        output_sections.append("""
## Pictogrames
ACTIVAT — Afegeix icones/emojis de suport al costat dels conceptes clau del text adaptat.
Exemples: ☀️ per llum, 💧 per aigua, 🌱 per planta, 🔬 per ciència, etc.
Integra'ls directament al text adaptat, no en secció separada.
""")

    if comp.get("esquema_visual"):
        output_sections.append("""
## Esquema visual
ACTIVAT — Genera un esquema/diagrama en format text que mostri el procés o les relacions del contingut.
Format: usa fletxes (→, ↓), símbols (+, =) i emojis per fer-lo visual i intuïtiu.
Exemple de format:
```
ELEMENT A ☀️
  ↓
+ ELEMENT B 💧
  ↓
RESULTAT → PRODUCTE 1 + PRODUCTE 2
```
Ha de ser senzill, visual i comprensible per a l'alumne.
""")

    if comp.get("mapa_conceptual"):
        output_sections.append("""
## Mapa conceptual
ACTIVAT — Genera un mapa conceptual en format text amb estructura d'arbre.
Format:
```
CONCEPTE CENTRAL
│
├── Branca 1:
│   ├─ Element a
│   └─ Element b
│
├── Branca 2:
│   └─ Element c
│
└── Branca 3:
    ├─ Element d
    └─ Element e
```
Mostra les relacions jeràrquiques entre els conceptes principals del text.
""")

    if comp.get("preguntes_comprensio"):
        output_sections.append("""
## Preguntes de comprensió
ACTIVAT — Genera preguntes GRADUADES en 3 nivells de dificultat:

### Nivell 1: Resposta curta (reconeixement)
3 preguntes que es responen buscant informació directa al text.

### Nivell 2: Verdader o fals
3 afirmacions per marcar ✅ o ❌, barrejant correctes i incorrectes.

### Nivell 3: Relaciona o completa
2-3 activitats de relacionar conceptes (amb fletxes) o completar frases.

Adapta la dificultat de les preguntes al nivell MECR de sortida.
""")

    if comp.get("activitats_aprofundiment"):
        output_sections.append("""
## Activitats d'aprofundiment
ACTIVAT — Genera 2-3 activitats de repte cognitiu:
- Connexions interdisciplinars
- Pensament crític (per què? i si...?)
- Recerca guiada
- Debat o reflexió
""")

    if comp.get("bastides"):
        output_sections.append(f"""
## Bastides (scaffolding)
ACTIVAT — Genera suports didàctics estructurats en 4 blocs:

### Frases model
3-5 frases incompletes que l'alumne ha de completar amb informació del text.
Exemple: "Les plantes necessiten ______ per fer la fotosíntesi."

### Banc de paraules
Llista de 8-12 paraules clau que l'alumne pot usar per completar les frases i activitats.
Format: paraula1 – paraula2 – paraula3 – ...

### Suport visual
Indica quins suports visuals usar (icones, colors, esquemes, imatges recomanades).

### Suport L1
Si l'alumne és nouvingut, inclou pistes en {l1_display} per als conceptes més abstractes.
""")

    if comp.get("mapa_mental"):
        output_sections.append("""
## Mapa mental
ACTIVAT — Genera un mapa mental radial (diferent del mapa conceptual).
El concepte central al mig, amb branques que s'expandeixen amb associacions lliures,
preguntes generadores i connexions amb altres matèries.
""")

    # Sempre: argumentació pedagògica + auditoria
    output_sections.append("""
## Argumentació pedagògica
SEMPRE GENERAR — Explica les decisions pedagògiques preses, organitzades per àrees:
1. **Adaptació lingüística**: què s'ha simplificat i per què (nivell MECR, tipus de frases, vocabulari)
2. **Atenció a la diversitat**: com s'han tingut en compte les necessitats específiques (dislèxia, TEA, nouvingut, etc.)
3. **Suport multimodal**: quins canals s'han activat (visual, lingüístic, cognitiu) i per què
4. **Gradació cognitiva**: com s'ha organitzat la progressió (de reconeixement a producció)
5. **Rigor curricular**: quins continguts s'han mantingut íntegres i per què
Breu, 3-5 punts amb explicació de 1-2 frases cadascun.

## Notes d'auditoria
SEMPRE GENERAR — Taula comparativa breu dels canvis principals:
| Aspecte | Original | Adaptat | Motiu |
Màxim 5-6 files amb els canvis més significatius.
""")

    output_sections.append("""
Omès les seccions marcades com NO ACTIVADES. No generis seccions buides.
""")

    parts.append("\n".join(output_sections))

    return "\n".join(parts)
