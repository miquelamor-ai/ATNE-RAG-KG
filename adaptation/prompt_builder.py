"""Construcció del system prompt ATNE.

Aquest mòdul agrupa les funcions responsables de muntar el prompt que
enviem a l'LLM per adaptar un text: persona-audience (qui és l'alumne),
catàleg filtrat d'instruccions, blocs del corpus (identitat, DUA, gènere,
creuaments), skills opcionals i especificació del format de sortida amb
totes les seccions i complements.

Extret de `server.py` (refactor 2026-04-21). server.py re-exposa els
símbols públics per preservar el contracte amb `snapshot_contract`,
generador_lliure i els tests.
"""

import corpus_reader
import instruction_filter
from adaptation.post_process import MECR_MAX_WORDS


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
            # Fix 2026-04-21: frontend envia 'l1' (minúscula); suportem ambdós.
            l1 = val.get("L1", "") or val.get("l1", "")
            pais = val.get("pais", "")
            mesos = val.get("mesos_catalunya")
            frag = "Alumne nouvingut"
            if l1:
                frag += f" que parla **{l1}** com a llengua materna (L1)"
            if pais:
                frag += f", originari de {pais}"
            if isinstance(mesos, (int, float)):
                frag += f". Porta aproximadament {int(mesos)} mesos a Catalunya"
            lines.append(frag + ".")

            alfabet = val.get("alfabet_llati", True)
            if isinstance(alfabet, str):
                alfabet = alfabet.lower() not in ("no", "false", "0")
            if not alfabet:
                lines.append(
                    f"Alfabet no llatí (la seva L1 {l1 or 'original'} usa un altre sistema d'escriptura): "
                    "és OBLIGATORI incloure transliteració fonètica al glossari i traducció dels termes clau a la seva L1 concreta."
                )
            elif l1:
                lines.append(f"L1 amb alfabet llatí ({l1}): usa analogies etimològiques entre català i {l1} quan ajudin.")

            # Frontend pot enviar 'escolaritzacio' (regular/interrompuda) o
            # 'escolaritzacio_previa' (si/parcial/no) segons la versió del perfil.
            esc = val.get("escolaritzacio_previa") or val.get("escolaritzacio", "")
            if esc == "no" or esc == "cap":
                lines.append("No ha estat escolaritzat regularment al seu país d'origen. No familiaritzat amb gèneres escolars.")
            elif esc == "parcial" or esc == "interrompuda":
                lines.append("Escolarització prèvia parcial o interrompuda.")

            alfL1 = val.get("alfabetitzacio_l1")
            if alfL1 is False:
                lines.append("No alfabetitzat en la seva L1.")

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


def build_system_prompt(profile: dict, context: dict, params: dict, rag_context: str = "") -> str:
    """Munta el system prompt en 4 capes — instruccions graduades del catàleg de 98."""
    parts = []
    mecr = params.get("mecr_sortida", "B2")
    dua = params.get("dua", "Core")

    # ═══ CAPA 1: IDENTITAT (fixa) ═══
    parts.append(corpus_reader.get_identity())

    # T-05: Role prompting docent (si hi ha matèria definida)
    materia = params.get("materia") or context.get("materia", "")
    etapa = context.get("etapa") or params.get("etapa", "")
    if materia:
        role_parts = [f"Ets un especialista en {materia}"]
        if etapa:
            role_parts.append(f"que ensenya a {etapa}")
        role_parts.append("i pedagog DUA: escrius amb precisió conceptual i màxima accessibilitat.")
        parts.append(" ".join(role_parts))

    # T-04: Ancoratge MECR max-paraules just abans del catàleg d'instruccions.
    _max_words = MECR_MAX_WORDS.get(mecr, 25)
    parts.append(f"⚓ REGLA CRÍTICA (MECR {mecr}): màxim {_max_words} paraules per frase. Una idea per frase.")

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

    # Resolució conflictes: ELIMINAT (2026-04-09) — redundant amb A-26 graduada per MECR
    # Few-shot example: ELIMINAT (2026-04-09) — un sol domini (fotosíntesi), risc sobreajust. Parking lot.

    # ═══ CAPA 4: CONTEXT (variable) ═══

    # 4a. Context educatiu: ELIMINAT del prompt (2026-04-09)
    # L'etapa/curs s'usen al Python (propose_adaptation) per calcular MECR,
    # però l'LLM no els necessita — ja rep les instruccions filtrades pel MECR correcte.

    # 4b. Persona-audience
    persona = build_persona_audience(profile, context, mecr)
    parts.append(f"PERSONA-AUDIENCE:\n{persona}")

    # 4b-bis. SKILLS (feature flag ATNE_USE_SKILLS=true) — additiu per defecte.
    # Si la skill aporta coneixement específic (gènere, perfil, complement),
    # l'injectem al prompt. No reemplacem res del catàleg actual en aquesta
    # iteració: això facilita el rollback i l'A/B.
    try:
        import skills_loader
        if skills_loader.is_skills_enabled():
            # Roots per defecte: corpusFJE (submodule) primer, skills_proto fallback.
            _all_skills = skills_loader.load_skills(skills_loader.default_skills_roots())
            # MVP single-call: carreguem adapter + complements en un sol prompt.
            # Quan migrem a multiagent, cada agent carregarà només el seu rol.
            _active = []
            for _role in ("adapter", "complements"):
                _active.extend(skills_loader.select_active(
                    _all_skills, profile, params, agent_role=_role
                ))
            if _active:
                _names = ", ".join(s.name for s in _active)
                print(f"[skills] actives ({len(_active)}): {_names}", flush=True)
                parts.append(skills_loader.render_skill_block(_active))
    except Exception as _e:
        # Fail-safe: si el loader peta, seguim sense skills (comportament actual).
        print(f"[skills] error (ignorat): {_e}", flush=True)

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
    # Fix 2026-04-21: suportem tant L1 (legacy) com l1 (frontend nou).
    _nouv = chars.get("nouvingut", {})
    l1 = _nouv.get("L1", "") or _nouv.get("l1", "")
    l1_display = l1 if l1 else "la llengua materna de l'alumne"

    output_sections = []
    output_sections.append("""
FORMAT DE SORTIDA:
Respon EXACTAMENT amb les seccions següents, separades per encapçalaments ## .
Genera NOMÉS les seccions indicades com ACTIVADES.

## Text adaptat
El text complet adaptat segons tots els paràmetres indicats.
- **Conserva el títol** del text original com a primera línia (en **negreta** o com a `# Títol`). Si el text original no en té, no n'inventis cap.
- **Conserva l'estructura original del text**: si el text original té apartats (qualsevol nivell de títol), **reprodueix-los com a `### Apartat` DINS de `## Text adaptat`** (mai com a `##`, reservat per a seccions top-level com «## Glossari»). Les llistes numerades (`1.` `2.` `3.`) i les llistes amb bullets (`- item`) es mantenen igual. **No les converteixis a prosa** ni les reformulis amb connectors ("Primer... Segon... Tercer...").
- **Textos llargs** (més de 150 paraules sense apartats): organitza'ls en 2-4 sub-apartats descriptius amb `### Apartat` (tres hashes, com a subseccions dins de «## Text adaptat») seguint l'estructura canònica del gènere indicat. No inventis subtítols per a textos curts.
- Estructura clara amb salts de línia entre idees
- Termes tècnics en **negreta** amb definició entre parèntesis la primera vegada
- Una idea per frase
- Si el nivell és A1 o inferior: frases molt curtes, vocabulari quotidià, sense subordinades
""")

    if comp.get("glossari"):
        is_nouvingut = "nouvingut" in [k for k, v in chars.items() if v.get("actiu")]
        if is_nouvingut and l1:
            output_sections.append(f"""
## Glossari
ACTIVAT — Genera una TAULA MARKDOWN amb 3 columnes:
| Terme | Traducció ({l1_display}) | Explicació simple |
Inclou tots els termes tècnics o difícils del text adaptat (mínim 8-12 termes).
La columna de traducció ha de contenir la traducció REAL al/a la {l1_display} (en el seu alfabet original si escau: àrab, xinès, urdú, etc.).
L'explicació ha de ser en català molt senzill (nivell A1).
""")
        else:
            output_sections.append("""
## Glossari
ACTIVAT — Genera una TAULA MARKDOWN amb 2 columnes:
| Terme | Explicació simple |
Inclou tots els termes tècnics o difícils del text adaptat (mínim 8-12 termes).
L'explicació ha de ser en català molt senzill.
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

    # Variables de context per als complements pedagògics (MALL/TILC)
    materia_complement = params.get("materia") or context.get("materia") or "la matèria corresponent"
    etapa_complement = params.get("etapa") or context.get("etapa") or "l'etapa educativa corresponent"
    mecr_complement = params.get("mecr") or "el nivell MECR indicat"
    genere_complement = params.get("genere_discursiu") or "no especificat"
    # Detectar si és text literari o informatiu (heurística a partir del gènere)
    literari_keywords = ("conte", "relat", "poesia", "poema", "llegendari", "fantàstic", "narrativa", "literari")
    es_literari = any(k in genere_complement.lower() for k in literari_keywords)
    modalitat_text = "LITERARI (deixa espais interpretatius, afectius, d'identificació)" if es_literari else "INFORMATIU (precisió conceptual, dades, relacions causa-efecte)"

    # Una sola línia de modalitat segons el gènere detectat
    modalitat_linia = (
        "- Literari: preguntes afectives, d'identificació, d'imatges mentals, creatives."
        if es_literari else
        f"- Informatiu: precisió conceptual, dades, causa-efecte, model teòric de {materia_complement}."
    )

    # Línia d'adequació segons l'etapa (filtra només la rama rellevant)
    _etapa_lower = (etapa_complement or "").lower()
    if any(k in _etapa_lower for k in ("infantil", "cicle inicial")):
        adequacio_linia = "- Predicció visual, connexió amb el jo, dibuix. Evita «justifica» i «argumenta». Preguntes curtes."
    elif any(k in _etapa_lower for k in ("cicle mitjà", "cicle mitja", "cicle superior", "primària", "primaria")):
        adequacio_linia = "- Idea principal, relacions, comparacions."
    elif any(k in _etapa_lower for k in ("batxillerat", "fp", "cicle formatiu", "cfgm", "cfgs")):
        adequacio_linia = "- Anàlisi crítica, intertextualitat, biaixos."
    else:
        # ESO / secundària i fallback
        adequacio_linia = "- Arguments, connectors lògics, contrast de fonts."

    if comp.get("preguntes_comprensio"):
        output_sections.append(f"""
## Preguntes de comprensió
ACTIVAT — Guió de comprensió lectora MALL/TILC (3 moments · formats variats).

Context: {materia_complement} · {etapa_complement} · MECR {mecr_complement} · gènere {genere_complement} · {modalitat_text}
Adequació a l'etapa: {adequacio_linia[2:]}
Modalitat: {modalitat_linia[2:]}

FORMAT DE SORTIDA (exacte, és el que veu l'alumnat):

## Preguntes de comprensió

### Abans de llegir
- [hipòtesi sobre títol]
- [connexió amb coneixements previs]
- [propòsit de lectura]

### Durant la lectura
- [inferència en curs]
- [visualització / imatge mental]
- [lèxic en context]

### Després de llegir
- [literal 1: V/F amb justificació, omplir buits, relaciona amb fletxes…]
- [literal 2: format diferent de l'anterior]
- [inferencial 1: per què creus…? i si…?]
- [inferencial 2: causa-efecte]
- [crític 1: argumentativa oberta]
- [crític 2: transferència al jo / biaixos]

Regles: NO escriguis «Moment», «Nivell LITERAL», ni etiquetes [Literal · V/F]. Cada pregunta comença amb «- ». Integra els formats visuals dins la pregunta («- Omple els buits: El ___ serveix per ___.»).
""")

    if comp.get("activitats_aprofundiment"):
        output_sections.append(f"""
## Activitats d'aprofundiment
ACTIVAT — Genera 2-3 activitats de repte cognitiu per a {etapa_complement}:
- Connexions interdisciplinars amb altres matèries
- Pensament crític (per què? i si…? què passaria si…?)
- Recerca guiada (a casa o a biblioteca)
- Debat o reflexió argumentada
- Si el text ho permet: dimensió plurilingüe (com es diu X en altres llengües de l'aula?)
""")

    if comp.get("bastides"):
        output_sections.append(f"""
## Bastides (scaffolding)
ACTIVAT — Suports didàctics reals per AJUDAR L'ALUMNE A PRODUIR les respostes
(model MALL/TILC: patró lingüístic de la matèria + connectors + lèxic temàtic).

### CONTEXT
- Matèria: {materia_complement}
- Etapa: {etapa_complement} · MECR: {mecr_complement}
- Si l'alumne és nouvingut, L1: {l1_display}

### 1. Taula de connectors lògics
Taula amb els connectors del tipus de raonament que demanen les preguntes:
| Funció | Connectors (adequats al MECR {mecr_complement}) |
|---|---|
| Causa | perquè, com que, ja que, a causa de |
| Conseqüència | per tant, així doncs, en conseqüència, per això |
| Oposició / contrast | però, en canvi, tanmateix, malgrat que |
| Exemplificació | per exemple, com ara, en concret |
| Conclusió | en resum, per acabar, en definitiva |
Adapta la quantitat i complexitat al nivell.

### 2. Frases model per argumentar amb el text
4-6 bastides d'inici de frase perquè l'alumne escrigui respostes ben formulades:
- "Segons el text, ______ perquè ______."
- "Podem deduir que ______ ja que el text diu que ______."
- "A diferència de ______, ______ s'assembla a ______ perquè ______."
- "Un exemple d'això és ______."
- "Jo crec que ______, i ho justifico perquè ______."
Adapta la complexitat al MECR: més simples a A1-A2, més sofisticades a B1-C1.

### 3. Banc de paraules (lèxic temàtic de {materia_complement})
8-12 paraules del patró lingüístic de la matèria, extretes del text o complementàries,
que l'alumne pot usar per respondre. Si escau, agrupa-les per camp semàntic.
Format: paraula1 – paraula2 – paraula3 – …

### 4. Suport visual recomanat
Indica 2-3 suports visuals concrets que afegirien valor (icones, colors destacats,
esquemes, línies de temps, mapes, gràfiques, fotografies…) i on ubicar-los al text.

### 5. Crosses de lectura (abans d'engegar)
2-3 pistes concretes perquè l'alumne enfoqui bé la lectura:
- Què ha de buscar mentre llegeix (1-2 elements clau)?
- Com marcar el que és important (subratllar, prendre nota, fletxes)?
- Quin és el propòsit d'aquesta lectura?

### 6. Suport L1
Si l'alumne és nouvingut, tradueix 5-8 conceptes més abstractes a {l1_display}
(en l'alfabet original si escau: àrab, xinès, urdú, etc.).

### ADEQUACIÓ PER ETAPA
- Infantil / Cicle Inicial: crosses FÍSIQUES i VISUALS (imatges, colors, referents sonors).
- Cicle Mitjà / Superior / ESO: crosses PROCEDIMENTALS (estratègies, plantilles, taules).
- Batxillerat / FP: estratègies de SÍNTESI i anàlisi crítica de múltiples fonts.
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
Omet les seccions NO activades. No generis seccions buides.
Títols: usa literalment «## Text adaptat», «## Glossari», «## Esquema visual», «## Mapa conceptual», «## Mapa mental», «## Preguntes de comprensió», «## Bastides», «## Activitats d'aprofundiment», «## Argumentació pedagògica», «## Notes d'auditoria». Sense prefixos numèrics, emojis ni qualificadors. Sub-apartats amb «###».
""")

    parts.append("\n".join(output_sections))

    return "\n".join(parts)

