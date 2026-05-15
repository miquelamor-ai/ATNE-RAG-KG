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
from adaptation.lang_config import get_lang_label
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
            frag = "Dispraxia"
            if grau:
                frag += f" (grau {grau})"
            lines.append(frag + ".")

        elif key == "comprensio_lectora":
            # Patró clínic "poor comprehender": descodifica correctament però no
            # construeix significat (Cain & Oakhill). Adaptacions H-29..H-34.
            lines.append(
                "Comprensió lectora desacoblada: l'alumne descodifica el text "
                "correctament però NO construeix el significat global per si sol. "
                "Cal explicitar propòsit lector, inferències, relacions causa-efecte "
                "i referents pronominals; afegir recapitulacions estructurals i "
                "micro-preguntes intercalades de metacognició."
            )

        elif key == "2e":
            lines.append("Doble excepcionalitat (2e): combina altes capacitats amb una necessitat d'accessibilitat. Mantenir repte intel·lectual ALT amb suports de format.")

        else:
            lines.append(f"Amb {key.replace('_', ' ')}.")

    lines.append(f"Nivell MECR de sortida: {mecr}.")

    obs = profile.get("observacions", "")
    if obs:
        lines.append(f"Observació del docent: {obs}")

    # Capa descriptiva del docent (cura personalis, marc rector ignasià):
    # - punts_forts: ajuda l'LLM a apalancar fortaleses i no només a "rebaixar"
    # - interessos: permet escollir exemples i analogies properes a la persona
    # Són narratives lliures; entren com a context, NO com a regla normativa.
    punts_forts = (profile.get("punts_forts") or "").strip()
    if punts_forts:
        lines.append(
            f"Punts forts a apalancar (parteix d'aquí, no només del que li costa): {punts_forts}"
        )

    interessos = (profile.get("interessos") or "").strip()
    if interessos:
        lines.append(
            f"Interessos, cultura i detonants (usa'ls per escollir exemples, analogies i to): {interessos}"
        )

    return "\n".join(lines)


def build_system_prompt(profile: dict, context: dict, params: dict, rag_context: str = "") -> str:
    """Munta el system prompt en 4 capes — instruccions graduades del catàleg de 98."""
    parts = []
    mecr = params.get("mecr_sortida", "B2")
    dua = params.get("dua", "Core")
    lang = params.get("lang", "ca")
    lang_label = get_lang_label(lang)

    # ═══ CAPA 1: IDENTITAT (fixa) ═══
    parts.append(corpus_reader.get_identity(lang))

    # Directiva de llengua explícita per a idiomes no-catalans
    if lang != "ca":
        parts.append(
            f"⚠️ LLENGUA DE SORTIDA: genera TOT el contingut (text adaptat, glossari, "
            f"preguntes, esquemes, bastides, argumentació pedagògica i notes d'auditoria) "
            f"EN {lang_label.upper()}. Cap secció en català ni en cap altra llengua."
        )

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
- La primera línia ha de ser sempre un **títol** en format `# Títol`. Si el text original ja en té, conserva'l. Si no en té, crea'n un de breu i descriptiu del contingut.
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
L'explicació ha de ser en {lang_label} molt senzill (nivell A1).
""")
        else:
            output_sections.append(f"""
## Glossari
ACTIVAT — Genera una TAULA MARKDOWN amb 2 columnes:
| Terme | Explicació simple |
Inclou tots els termes tècnics o difícils del text adaptat (mínim 8-12 termes).
L'explicació ha de ser en {lang_label} molt senzill.
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

    if comp.get("illustracions"):
        output_sections.append(f"""
## Il·lustracions (inline, no secció separada)
ACTIVAT — Insereix marcadors `[IMATGE: <concepte curt en {lang_label}>]` al text adaptat
allà on una il·lustració ajudaria la comprensió.

REGLES ESTRICTES:
- Format exacte: `[IMATGE: concepte]` amb claudàtors i la paraula IMATGE en majúscules.
- **Idioma**: {lang_label}. 3-8 paraules. Concepte nuclear, no descripció d'escena.
- **En línia pròpia**, abans del paràgraf/secció que introdueix el concepte.
- **Màxim 3-4 marcadors per document**. Menys és millor.
- **Un marcador per secció major com a màxim**.
- Només conceptes **visualitzables i concrets** (llocs, objectes, escenes, processos observables).
- **NO** conceptes abstractes purs ("la democràcia", "la justícia").
- **NO** tecnicismes microscòpics ("cloroplasts", "àtoms") — reformula a nivell macroscòpic ("fulla sota el sol").
- **NO** afegeixis descripcions d'estil dins el marcador (el backend s'encarrega de l'estil).
- **NO** generis cap secció final `## Il·lustracions`. Els marcadors viuen inline.

Exemples correctes:
- `[IMATGE: cicle de l'aigua]`
- `[IMATGE: fàbrica tèxtil del segle XIX]`
- `[IMATGE: fulla verda al sol]`

Exemples INCORRECTES:
- `[IMATGE: a beautiful watercolor of...]` (anglès + estil)
- `[IMATGE: la revolució industrial]` (massa abstracte)
- `[IMATGE: cloroplasts i mitocondris]` (microscòpic)
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
ACTIVAT — Genera un mapa conceptual en format text amb estructura d'arbre
usant NOMÉS llistes amb guions i indentació amb 2 espais.

**FORMAT OBLIGATORI (llista jeràrquica markdown, no caràcters de dibuix):**

```
- **CONCEPTE CENTRAL**
  - Branca 1:
    - Element a
    - Element b
  - Branca 2:
    - Element c
  - Branca 3:
    - Element d
    - Element e
```

REGLES CRÍTIQUES:
- NO usis caràcters de dibuix d'arbre (│ ├ └ ─ ╔ ║). Causen corrupció
  en alguns models, que substitueixen lletres al mig de paraules
  ('Causes' → 'Cau—ses').
- NOMÉS guions `-` i indentació amb 2 espais per nivell.
- Negreta opcional al concepte central amb `**...**`.

Mostra les relacions jeràrquiques entre els conceptes principals del text.
""")

    # Variables de context per als complements pedagògics (MALL/TILC)
    materia_complement = params.get("materia") or context.get("materia") or "la matèria corresponent"
    etapa_complement = context.get("etapa") or params.get("etapa") or "l'etapa educativa corresponent"
    mecr_complement = params.get("mecr_sortida") or params.get("mecr") or "el nivell MECR indicat"
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
        # Bastides → dos blocs lògics segons hi hagi tasca de producció o no:
        #   - LECTURA (sempre): pre-lectura + durant + post-lectura
        #   - RESPOSTA (només si preguntes_comprensio o activitats_aprofundiment
        #     estan actives): connectors + frases model
        # Llenguatge adaptat al MECR de l'alumne (A1-A2 = simple/visual; B1+ = més tècnic).
        # El bloc "Suport L1" s'elimina: ja es cobreix amb el complement Glossari
        # (que té traducció L1 + transliteració quan l'alumne és nouvingut).
        # El "Suport visual recomanat" passa a «Notes d'auditoria» (info pel docent).
        _has_production_task = bool(
            comp.get("preguntes_comprensio") or comp.get("activitats_aprofundiment")
        )
        _mecr_norm = (mecr_complement or "B1").upper().replace("Ç", "C")
        _is_low_mecr = _mecr_norm in ("PRE-A1", "A1", "A2")

        if _is_low_mecr:
            _bastides_title = "Eines per llegir i respondre"
            _lang_note = (
                "🟡 LLENGUATGE SIMPLE: l'alumne és MECR baix. Usa títols planers "
                "i emojis. Evita termes tècnics («scaffolding», «connectors lògics», «patró lingüístic»). "
                "Una idea per línia. Frases molt curtes."
            )
        else:
            _bastides_title = "Bastides (ajudes per llegir i respondre)"
            _lang_note = (
                "Llenguatge clar per a l'alumne. Si MECR ≤ B1, evita termes massa tècnics."
            )

        # Blocs comuns: lectura
        _bastides_block = f"""
## {_bastides_title}
ACTIVAT — Ajudes per a l'alumne (NO explicació del text). {_lang_note}

### CONTEXT
- Matèria: {materia_complement}
- Etapa: {etapa_complement} · MECR: {mecr_complement}

### 📖 Abans de llegir
2-3 pistes curtes perquè l'alumne enfoqui la lectura ABANS de començar:
- Una pregunta d'activació: «Què saps de [tema]?»
- Una predicció: «Què creus que diu el text? Mira el títol i pensa.»
- Un propòsit clar: «Llegeix per saber [una cosa concreta del text].»

### 🔍 Durant la lectura
2-3 estratègies pràctiques:
- Què subratllar (1-2 tipus d'informació clau, ex: «verbs d'acció», «dates»).
- Com prendre nota al marge (ex: ✓ entès / ? dubte / ! important).
- Per cada paràgraf, anota la idea principal en 1 paraula.

### 📝 Després de llegir
2-3 activitats curtes per consolidar:
- Resum en 1 frase: «Aquest text parla de ______ i diu que ______.»
- Idea principal vs detalls: distingeix-les.
- Connecta amb la teva vida: «Això em recorda ______.»
"""

        if _has_production_task:
            _bastides_block += f"""

### 🔗 Connectors per respondre
Taula amb els connectors que es poden fer servir a les respostes:
| Per què | Paraules útils ({mecr_complement}) |
|---|---|
| Donar una causa | perquè, com que, ja que |
| Dir una conseqüència | per tant, així doncs, per això |
| Comparar / contrastar | però, en canvi |
| Donar exemples | per exemple, com ara |
| Tancar la resposta | en resum, per acabar |
Adapta la quantitat al MECR de l'alumne (a A1-A2 dóna 1-2 connectors per fila; a B1+ dóna 3-4).

### ✏️ Frases per començar la resposta
4-5 inicis de frase perquè l'alumne completi (no donis la resposta sencera):
- «Segons el text, ______ perquè ______.»
- «Penso que ______ perquè el text diu ______.»
- «Un exemple és ______.»
- «A ______ li passa que ______.»
- (Adapta al MECR: més curtes i amb 1-2 forats a A1-A2; més sofisticades a B2-C1.)

### 🗂️ Paraules clau del text
6-10 paraules importants del text que l'alumne pot reaprofitar a les respostes.
Format llista separada per «–». Si són tècniques, marca-les amb (T): paraula1 – paraula2(T) – paraula3 – …
"""
        else:
            _bastides_block += """

### 💡 Recomanació
No hi ha preguntes ni activitats actives en aquesta adaptació. Per això NO s'inclouen
bastides de resposta (connectors + frases model). Si vols que l'alumne respongui,
activa també el complement «Preguntes de comprensió» o «Activitats d'aprofundiment».
"""

        output_sections.append(_bastides_block)

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

    # Reforç crític per a gèneres on la FORMA és contingut (poema, teatre,
    # recepta…). Sense això, smoke tests 2026-04-20 mostraven que el LLM
    # aplanava poemes a prosa quan MECR era baix, contradient la regla del
    # gènere (parking lot #59). El reforç va al final perquè els LLMs
    # respecten més les normes properes a la generació.
    _form_genres = {
        "poema", "poesia", "vers", "cançó", "canço", "song",
        "teatre", "guió teatral", "guio teatral", "monòleg", "monoleg", "diàleg", "dialeg",
        "recepta", "receptari",
        "reglament", "norma", "instructiu", "manual",
        "fitxa tècnica", "fitxa tecnica",
    }
    _genre_lower = (genre or "").lower()
    _is_form_genre = any(g in _genre_lower for g in _form_genres)
    if _is_form_genre:
        output_sections.append(f"""
REGLA CRÍTICA — PRESERVA LA FORMA DEL GÈNERE «{genre}»:
La forma estructural d'aquest gènere ÉS contingut, no només envoltori.
Si hi ha conflicte entre la simplificació MECR i la preservació de la forma,
GUANYA LA FORMA. Pots simplificar VOCABULARI però NO:
- Convertir versos a prosa (poema, cançó): MAI uneixis dos versos amb una coma o un connector. Cada vers a la seva línia.
- Eliminar acotacions o canvis de personatge (teatre, diàleg): preserva «PERSONATGE:» i les acotacions entre parèntesis o cursiva.
- Reformular llistes numerades a prosa (recepta, instructiu, reglament): manté el «1. 2. 3.» i els passos discrets.
- Treure separadors gràfics significatius (fitxa tècnica): respecta la presentació en taula o llista de camps.

Si simplificar-ho et porta a destruir l'estructura, deixa el text en una versió
mínimament adaptada però FORMALMENT íntegra. La integritat formal és més
important que arribar al MECR exacte en aquests gèneres.
""")

    output_sections.append("""
Omet les seccions NO activades. No generis seccions buides.
Títols: usa literalment «## Text adaptat», «## Glossari», «## Esquema visual», «## Mapa conceptual», «## Mapa mental», «## Preguntes de comprensió», «## Bastides», «## Activitats d'aprofundiment», «## Argumentació pedagògica», «## Notes d'auditoria». Sense prefixos numèrics, emojis ni qualificadors. Sub-apartats amb «###».

REGLA CRÍTICA — NO INVENTIS CONTINGUT NO DEMANAT:
Dins de la secció «## Text adaptat», NO afegeixis:
- Preguntes de comprensió, preguntes retòriques o reflexives («Què en penses?», «Per què creus…?», «*Pregunta:*»). Si el complement «Preguntes de comprensió» NO està ACTIVAT, no n'apareix cap dins del text adaptat.
- Marcadors de progrés tipus «[Secció 1 de 4]», «Part 1», «Capítol 1» si no eren al text original.
- Comentaris meta sobre l'adaptació («Aquí simplifiquem…», «Hem suprimit…»). Aquestes notes pertanyen exclusivament a «## Notes d'auditoria».
- Indicacions per al docent dins del text. Si vols donar context al docent, fes-ho a «## Argumentació pedagògica».

El text adaptat ha de ser un text didàctic acabat, llegible directament per l'alumne, sense intromissions del sistema. Si el bloc de complements actius està buit, NO inventis exercicis ni activitats per omplir.
""")

    parts.append("\n".join(output_sections))

    return "\n".join(parts)

