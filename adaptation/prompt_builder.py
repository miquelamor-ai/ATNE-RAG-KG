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
    """Retorna llista de claus de perfils actius.

    Defensiu: caracteristiques pot contenir valors no-dict (ex: fase_lectora=str).
    Filtra només els que son dict abans de cridar .get("actiu").
    """
    chars = profile.get("caracteristiques", {})
    return [
        key for key, val in chars.items()
        if isinstance(val, dict) and val.get("actiu")
    ]


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

    Fase A (2026-05-15): l'etapa ja no fa fallback silenciós a "ESO". Si el
    frontend no envia etapa, es loggeja un avís i s'omet la línia de
    capçalera per evitar la mentida "alumne de ESO" per a infantil/primària.
    """
    chars = profile.get("caracteristiques", {})
    lines = []

    etapa = (context.get("etapa") or "").strip()
    curs = (context.get("curs") or context.get("nivell_curs") or "").strip()
    if not etapa:
        # Visibilitat del bug: si el frontend no envia etapa, ho sabrem als logs
        # en lloc d'assumir "ESO" silenciosament. Si curs porta pistes (p.ex.
        # "I5", "3r ESO") encara podem orientar la capçalera. Si no, l'ometem.
        print(
            f"[prompt_builder] AVIS: context sense 'etapa' (curs='{curs}'). "
            "El frontend hauria d'enviar-la. Fent inferència minima.",
            flush=True,
        )
        _c = curs.lower()
        if curs.upper().startswith("I") and len(curs) >= 2 and curs[1] in ("3", "4", "5"):
            etapa = "infantil"
        elif "prim" in _c:
            etapa = "primaria"
        elif "eso" in _c:
            etapa = "ESO"
        elif "batx" in _c:
            etapa = "batxillerat"
        elif "fp" in _c or "grau" in _c:
            etapa = "FP"
    if etapa:
        header = f"Escrius per a un alumne de {etapa}"
        if curs:
            header += f" ({curs})"
        lines.append(header + ".")
    elif curs:
        # Sense etapa derivable: almenys diem el curs per no perdre tota la senyal.
        lines.append(f"Escrius per a un alumne del curs «{curs}».")

    for key, val in chars.items():
        # Defensiu: caracteristiques pot contenir valors no-dict (ex: fase_lectora=str).
        if not isinstance(val, dict):
            continue
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


def build_system_prompt(profile: dict, context: dict, params: dict, rag_context: str = "",
                        adapter_only: bool = False) -> str:
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

    # T-04: Ancoratge MECR just abans del catàleg. Bidireccional: SOSTRE (màx
    # paraules) + TERRA (no simplificar per sota del nivell). El terra ataca la
    # sobre-simplificació detectada (C1): el text sortia per sota del MECR demanat.
    _max_words = MECR_MAX_WORDS.get(mecr, 25)
    if mecr in ("pre-A1", "A1", "A2"):
        parts.append(
            f"⚓ REGLA CRÍTICA (MECR {mecr}): màxim {_max_words} paraules per frase, una idea per frase. "
            f"Mantén però el lèxic i el rigor conceptual propis de {mecr}: adapta AL nivell, no per sota."
        )
    else:
        # B1+: terra I sostre alhora (equilibri; atac mesurat a la sobre-simplificació C1).
        parts.append(
            f"⚓ REGLA CRÍTICA (MECR {mecr}): frases de fins a {_max_words} paraules amb la complexitat pròpia "
            f"de {mecr}, ni més simple ni més complexa. NO rebaixis el text per sota de {mecr} (evita l'estil "
            f"fragmentat A1/A2), però tampoc no el compliquis més del compte. Ajusta't EXACTAMENT a {mecr}."
        )

    # ═══ CAPES 2-3: INSTRUCCIONS FILTRADES (catàleg de 89 instruccions LLM) ═══
    # Filtra segons perfils actius, sub-variables, MECR, DUA i complements
    filtered = instruction_filter.get_instructions(profile, params, context=context)
    instructions_text = instruction_filter.format_instructions_for_prompt(filtered)
    parts.append(instructions_text)

    # DUA (bloc del corpus — complementa les instruccions filtrades)
    dua_block = corpus_reader.get_dua_block(dua)
    if dua_block:
        parts.append(dua_block)

    # Gènere discursiu: ara s'injecta com a SKILL (write-<genre>) via
    # skills_loader (bloc 4b-bis), no com a bloc del M3. La crida a
    # corpus_reader.get_genre_block() s'ha eliminat (2026-05-17) per evitar
    # duplicació amb la skill activa. La variable `genre` es manté perquè
    # més avall (regla preservació forma) s'usa per detectar gèneres-forma.
    genre = params.get("genere_discursiu", "")

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
            # Roots per defecte: corpusFJE (submodule) — font única des 2026-05-17.
            _all_skills = skills_loader.load_skills(skills_loader.default_skills_roots())
            # adapter_only=True (2a crida separada): nomes SKILLs d'adaptacio.
            # adapter_only=False (crida unica legacy): adapter + complements junts.
            _roles = ("adapter",) if adapter_only else ("adapter", "complements")
            _active = []
            for _role in _roles:
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

    # Desduplicació SKILL↔hardcoded (2026-05-22): si ATNE_USE_SKILLS està
    # actiu, les SKILLs de glossari/bastides/preguntes_comprensio aporten les
    # instruccions detallades (gradació MECR, variants per perfil, format).
    # En aquest cas, simplifiquem el hardcoded a una capçalera mínima per
    # evitar duplicació i contradiccions (hardcoded deia "mínim 8-12 termes"
    # sempre, SKILL gradua de 3-5 a 12-15 segons MECR). Mantenim el hardcoded
    # complet quan SKILLs OFF perquè continuï essent backup funcional.
    try:
        import skills_loader as _sl
        _skills_on = _sl.is_skills_enabled()
    except Exception:
        _skills_on = False

    # Crida 1 (adapter_only): genera nomes text adaptat + argumentacio + auditoria.
    # Els complements es generaran en una 2a crida separada (build_complements_prompt).
    if adapter_only:
        # ⚠️ Recordatori del gènere demanat al FINAL del prompt (recency bias):
        # detectat 2026-05-27 amb harness Fase B + Sonnet judge — quan el
        # genere no és divulgatiu/expositiu (ex: entrevista, opinió, conte,
        # poema), el LLM ignorava la SKILL WRITE-* del mig del prompt i
        # generava sempre text didàctic expositiu (la directiva del final
        # guanyava). C5 Estructura: 0.86/5.
        _genere_param = (params.get("genere_discursiu") or "").strip()
        _genere_block = ""
        if _genere_param:
            _genere_label = _genere_param.replace("_", " ").replace("-", " ").upper()
            # Fix 2026-05-27 (Bug 3): reforç específic per a "notícia" — sense aquest
            # reforç, el LLM ignorava l'estructura periodística canònica (titular + lead
            # 5W + cos en piràmide invertida + cita) i generava prosa expositiva amb
            # preguntes. Vegeu cas mireia C5_estructura_genere=1/5.
            _genere_lower = _genere_param.lower()
            _is_noticia = "notic" in _genere_lower or "notíc" in _genere_lower
            _noticia_block = ""
            if _is_noticia:
                _noticia_block = """
### 🗞️ FORMAT OBLIGATORI per a NOTÍCIA (piràmide invertida)
El text adaptat HA DE SEGUIR aquesta estructura, NO és opcional:

1. **TITULAR** (1a línia, format `# Titular`):
   - Frase informativa amb subjecte + verb d'acció + complement.
   - NO és el tema genèric ("La fotosíntesi"), sinó el FET noticiable
     ("Els científics descobreixen com les plantes generen oxigen").
   - Sense adjectius valoratius. Llargada segons MECR.

2. **LEAD** (1r paràgraf, sense títol propi):
   - Respon a les 5W en una sola frase o dues curtes:
     QUI · QUÈ · QUAN · ON · PER QUÈ (cobertura segons MECR: A1=2W, A2=4W, B1+=5W).
   - És el resum complet del fet més important. Si el lector només llegís el lead,
     ja sabria l'essencial.

3. **COS** (paràgrafs següents, piràmide invertida):
   - Detalls per ordre DECREIXENT de rellevància (el més important PRIMER).
   - Cada paràgraf afegeix un detall menys central que l'anterior.
   - Pot incloure 1 cita directa atribuïda ("Segons [persona], '…'") a partir d'A2.

4. **CONTEXT FINAL** (opcional, últim paràgraf):
   - Antecedents o conseqüències. La part més prescindible.

PROHIBIT:
- Generar el text com a prosa expositiva tipus llibre de text ("La fotosíntesi és...").
- Estructurar el cos amb preguntes ("**On passa aquest procés?**", "**Què necessita la planta?**").
  Això és gènere DIVULGATIU/EXPOSITIU, NO notícia.
- Ometre el titular o el lead 5W.
"""
            _genere_block = f"""
## ⚠️ GÈNERE DISCURSIU OBLIGATORI: {_genere_label}
El text adaptat HA DE SEGUIR l'estructura canònica del gènere "{_genere_param}",
tal com es defineix a la SKILL ACTIVA de més amunt al system prompt.
- Si el gènere és entrevista: format de torns Pregunta/Resposta entre entrevistador i entrevistat.
- Si el gènere és opinió: tesi clara + arguments + conclusió.
- Si el gènere és conte/fàbula/poema: narrativa amb personatges i estructura literària.
- Si el gènere és instructiu/receptari/manual: materials + passos numerats + bloc final
  `### Per acabar` (A1-A2) o `### Resultat esperat` (A2+) amb 1-2 frases que diuen
  què s'ha obtingut. PROHIBIT deixar la frase de tancament com a paràgraf solt fora
  d'estructura: ha d'anar dins un encapçalament propi.
- Si el gènere és diàleg: dos parlants identificats amb torns clars.
- Si el gènere és notícia: titular + lead 5W + cos en piràmide invertida + cita opcional.
- Si el gènere és divulgatiu/expositiu: prosa estructurada amb idees jerarquitzades.
{_noticia_block}
PROHIBIT generar prosa expositiva genèrica si el gènere és un altre. La forma del
gènere és tan important com el contingut adaptat.
"""

        # Fix 2026-05-30 (Bug pictogrames absents en 2-call):
        # En mode 2-call, build_system_prompt(adapter_only=True) salta el bloc
        # complement output_sections — incloent la instrucció de pictogrames de
        # la línia ~605 que ensenya el format `[PICTO: terme|terme_castellà]`
        # graduat per MECR. La instrucció D-01 del catàleg sí entra (mencionant
        # `[PICTO: terme]` un cop), però gpt-4o (model d'adapter) la ignora
        # sistemàticament (0/4 markers a Fase B). gemma4 era més obedient.
        # Solució (mirall de bastides): directiva computada en Python a prop
        # de la generació, amb llesca del nivell MECR exacte, format estricte,
        # exemples i anti-emoji-Unicode. La SKILL i el bloc legacy es mantenen
        # als altres camins. La resolució HTTP a <img> ja es fa a
        # orchestrator.py:378 (resolve_pictogram_markers sobre call 1).
        _picto_block = ""
        if comp.get("pictogrames"):
            _mecr_pic = (mecr or "B1").upper().replace("Ç", "C")
            # Cada banda: (rule, mode) — "inline" = marcadors davant els termes
            # clau dins el text corrent; "glossari" = secció final amb la llista.
            # NOTA: la canon SKILL diu "A2+: glossari peu, NO inline". A la pràctica
            # gpt-4o ignora la regla "NO inline" i, si la imposem amb força,
            # acaba ometent pictogrames del tot quan competeixen amb 5+ complements
            # actius (cas ex_pri B1, 0/3 sistemàtic). Estratègia robusta: permet
            # inline DAVANT del terme a TOTS els nivells; la gradació canònica
            # actua sobre la QUANTITAT, no sobre presència/absència d'inline.
            _PICTO_BANDS = {
                "PRE-A1": (
                    "1-2 marcadors per frase davant noms i verbs clau (8-10 max per text). "
                    "POSICIÓ: SEMPRE abans de la paraula (`[PICTO: gat|gato] el gat dorm`, "
                    "MAI després). Afegeix també una capçalera `### Vocabulari del text "
                    "(mira primer!)` al començament amb la llista pictograma·paraula per "
                    "anticipació visual (UNE 153101)."
                ),
                "A1": (
                    "4-6 marcadors per text, 1 per paraula nova o concepte clau. "
                    "POSICIÓ: INLINE DAVANT del terme (`[PICTO: mitja|calcetin] una mitja "
                    "vella`, MAI després)."
                ),
                "A2": (
                    "4-6 marcadors INLINE DAVANT dels termes tècnics o conceptes clau del text "
                    "(`[PICTO: planta|planta] la planta verda`). Opcionalment, també pots "
                    "afegir un `### Glossari visual` al final amb la llista pictograma·terme."
                ),
            }
            _picto_rule = _PICTO_BANDS.get(
                _mecr_pic,
                (
                    "4-5 marcadors INLINE DAVANT dels termes tècnics o conceptes clau del text "
                    "(`[PICTO: clorofil·la|clorofila] la clorofil·la`). Només per a termes "
                    "tècnics o conceptes clau, no per a vocabulari quotidià. Opcionalment, "
                    "també pots afegir un `### Glossari visual` al final."
                ),
            )
            _picto_block = f"""
## ⚠️ PICTOGRAMES ARASAAC — OBLIGATORI a {_mecr_pic}
ACTIVAT — Insereix marcadors `[PICTO: terme]` reals (NO emojis Unicode 🌞🌊🌱).
Gradació per a {_mecr_pic}: {_picto_rule}

Format OBLIGATORI del marcador: `[PICTO: terme_idioma_doc|terme_castellà]`
- Esquerra del `|`: terme en l'idioma del document (català, castellà…).
- Dreta del `|`: equivalent en castellà per a la cerca ARASAAC.
- Terme curt (1-3 paraules), minúscules, concret i visualitzable (objecte, acció, ésser viu).
- Exemples (text català): `[PICTO: sol|sol]` `[PICTO: aigua|agua]` `[PICTO: planta|planta]` `[PICTO: córrer|correr]` `[PICTO: clorofil·la|clorofila]`.
- NO inventis emojis Unicode (🌞 🌊 🌱 ✨…): usa SEMPRE el marcador `[PICTO: …]`.
- NO posis text ni puntuació dins del marcador, només els termes separats per `|`.
- El backend els substitueix per imatges reals ARASAAC (CC BY-NC-SA 4.0).

PROHIBIT generar una secció `## Pictogrames` separada: els marcadors viuen DINS de `## Text adaptat`.
PROHIBIT deixar la sortida sense cap marcador `[PICTO:]` quan pictogrames és ACTIVAT.
"""

        parts.append(f"""
## Argumentació pedagògica
SEMPRE GENERAR — Explica les decisions pedagògiques (adaptació lingüística, atenció a la diversitat, suport multimodal, gradació cognitiva, rigor curricular). Breu, 3-5 punts.

## Notes d'auditoria
SEMPRE GENERAR — Taula comparativa dels canvis principals:
| Aspecte | Original | Adaptat | Motiu |
Màxim 5-6 files.
{_genere_block}
{_picto_block}
## CHECKLIST DE GENERACIÓ — OBLIGATORI
Genera únicament:
1. ## Text adaptat — amb l'ESTRUCTURA del gènere "{_genere_param or 'demanat'}"
2. ## Argumentació pedagògica
3. ## Notes d'auditoria

El text adaptat ha de ser llegible directament per l'alumne, sense intromissions del sistema, i ha de respectar el FORMAT del gènere demanat.
""")
        return "\n".join(parts)

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
        # Defensiu: caracteristiques pot contenir valors no-dict (ex: fase_lectora=str).
        # Filtra només els que son dict abans de cridar .get("actiu").
        is_nouvingut = "nouvingut" in [
            k for k, v in chars.items()
            if isinstance(v, dict) and v.get("actiu")
        ]
        if _skills_on:
            # SKILLs ON: la SKILL aporta context detallat. AQUÍ donem
            # format ACCIONABLE perquè el LLM no ometi la secció.
            if is_nouvingut and l1:
                output_sections.append(f"""
## Glossari
ACTIVAT — Format OBLIGATORI: taula markdown 3 columnes:
| Terme | Traducció ({l1_display}) | Explicació senzilla |

Inclou 5-10 termes clau (gradat per MECR). Traducció REAL a {l1_display} en alfabet original.
Vegeu SKILL generate-glossari per al detall pedagògic.
""")
            else:
                output_sections.append(f"""
## Glossari
ACTIVAT — Format OBLIGATORI: taula markdown 2 columnes:
| Terme | Explicació senzilla |

Inclou 5-10 termes clau (gradat per MECR).
Vegeu SKILL generate-glossari per al detall pedagògic.
""")
        elif is_nouvingut and l1:
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

    # C.3 MALL: gradació visuals — computa MECR aquí per als blocs pictogrames/esquema/mapa
    _mecr_c3 = (params.get("mecr_sortida") or params.get("mecr") or "B1").upper().replace("Ç", "C")

    if comp.get("pictogrames"):
        # C.3 MALL: gradació ARASAAC per nivell MECR.
        # El LLM emet marcadors [PICTO: terme] — el backend els substitueix per
        # pictogrames reals ARASAAC (CC BY-NC-SA 4.0). NO emojis Unicode.
        # Decisió pedagògica 2026-05-21: docent pilot va denunciar que "emojis
        # no son pictogrames AAC". Veure adaptation/pictograms_arasaac.py.
        _picto_map = {
            "PRE-A1": (
                "1-2 marcadors PER FRASE per als noms i verbs clau (8-10 max per text). "
                "POSICIO OBLIGATORIA: el marcador `[PICTO: ...]` ha d'anar SEMPRE "
                "ABANS de la paraula (a l'esquerra), NO despres. "
                "L'alumne ha de veure el pictograma PRIMER i llavors llegir la paraula "
                "(anticipacio visual segons UNE 153101). "
                "Exemple correcte: `[PICTO: gat|gato] el gat dorm`. "
                "Exemple INCORRECTE: `el gat [PICTO: gat|gato] dorm`. "
                "Afegeix tambe una seccio `### Vocabulari del text (mira primer!)` al "
                "principi amb la llista pictograma·paraula per anticipar."
            ),
            "A1": (
                "4-6 marcadors per text, 1 per paraula nova o concepte clau. "
                "POSICIO OBLIGATORIA: el marcador `[PICTO: ...]` va INLINE DAVANT "
                "del terme clau (a l'esquerra), NO despres. "
                "Exemple correcte: `[PICTO: mitja|calcetin] una mitja vella`. "
                "Exemple INCORRECTE: `una mitja vella [PICTO: mitja|calcetin]`. "
                "NO usis glossari visual al peu — aixo es per A2+."
            ),
            "A2": (
                "Marcadors al glossari visual (peu del text). "
                "NO inline al text corrent. Màxim 5-6 pictogrames per document."
            ),
        }
        _picto_instr = _picto_map.get(_mecr_c3)
        _picto_format = (
            "Format OBLIGATORI del marcador: `[PICTO: terme_idioma_doc|terme_castellà]`\n"
            "  - Usa SEMPRE el format amb barra vertical `|`.\n"
            "  - Esquerra del `|`: terme en l'idioma del document (català, castellà...)\n"
            "  - Dreta del `|`: equivalent en castellà per a la cerca ARASAAC\n"
            "  - Terme curt (1-3 paraules), en minúscules.\n"
            "  - Concepte concret i visualitzable (objecte, acció, ésser viu).\n"
            "  - Exemples (text en català): `[PICTO: aigua|agua]` `[PICTO: sol|sol]` "
            "`[PICTO: planta|planta]` `[PICTO: menjar|comer]` `[PICTO: casa|casa]` "
            "`[PICTO: córrer|correr]`\n"
            "  - NO inventis emojis Unicode. Usa SEMPRE el marcador `[PICTO: ...]`.\n"
            "  - NO poses text ni puntuació dins del marcador, només els termes.\n"
            "  - El backend mostrarà el terme esquerre com a etiqueta i usarà el dret per trobar el pictograma ARASAAC."
        )
        if _picto_instr:
            output_sections.append(f"""
**⚠️ INSTRUCCIÓ PICTOGRAMES ARASAAC — NO generar com a secció ## separada. Afegir INLINE dins "## Text adaptat".**
ACTIVAT — Afegeix pictogrames de suport. Gradació per a {_mecr_c3}: {_picto_instr}

{_picto_format}
""")
        else:
            output_sections.append(f"""
**⚠️ INSTRUCCIÓ PICTOGRAMES ARASAAC — NO generar com a secció ## separada. Afegir INLINE dins "## Text adaptat".**
ACTIVAT — Afegeix pictogrames al glossari visual (peu del text). NO inline per a B1+.
Màxim 4-5 pictogrames per document, només per a termes tècnics o conceptes clau.

{_picto_format}
""")

    if comp.get("illustracions"):
        output_sections.append(f"""
**⚠️ INSTRUCCIÓ IL·LUSTRACIONS — NO generar com a secció ## separada. Inserir INLINE dins "## Text adaptat".**
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
        # C.3 MALL: nombre de nodes per nivell
        _esquema_nodes_map = {
            "PRE-A1": "2-3 nodes. Seqüències temporals bàsiques (abans→després) o relacions imatge→paraula.",
            "A1":     "3-4 nodes. Enumeració de qualitats o parts d'un objecte (descripció simple).",
            "A2":     "4-6 nodes. Seqüència de passos d'instrucció o esdeveniments cronològics.",
            "B1":     "6-8 nodes. Relacions causa-efecte o hipòtesi-evidència.",
        }
        _esquema_nodes = _esquema_nodes_map.get(_mecr_c3, "Nombre de nodes a criteri docent. Modelitza processos complexos.")
        output_sections.append(f"""
## Esquema visual
ACTIVAT — Genera un esquema seqüencial en format llista markdown amb sagnia. Per a {_mecr_c3}: {_esquema_nodes}

Format: arrel + ramificacions amb `-` i sagnia de 2 espais. NO usar fletxes Unicode (→, ↓) ni ASCII-art (│ ├ └). El frontend ATNE detecta aquest format i el renderitza com a diagrama SVG (Mermaid flowchart LR). Si no es pot renderitzar, queda com a llista llegible.

Exemple de format:
```
- Pas inicial
  - Estat A
  - Estat B
- Acció central
  - Resultat 1
  - Resultat 2
- Conclusió
```

Ha de ser senzill i comprensible. Bastida temporal: retira-la quan l'alumne pugui representar l'estructura mentalment.
""")

    if comp.get("mapa_conceptual"):
        # C.3 MALL: mapa conceptual inapropiat per a Emergent/Inicial
        if _mecr_c3 in ("PRE-A1", "A1"):
            output_sections.append(f"""
## Mapa conceptual
⚠️ NIVELL {_mecr_c3} — BASTIDA INAPROPIADA: el mapa conceptual requereix autonomia lectora consolidada (mínim A2).
A nivell {_mecr_c3}, substitueix el mapa per un esquema visual simple (2-4 nodes amb imatges).
NO generis el mapa conceptual per a aquest nivell.
""")
        else:
            # Profunditat per nivell (MALL)
            _mapa_depth_map = {
                "A2": "2 nivells (concepte central → idees principals literals del text). Guiat.",
                "B1": "3 nivells (concepte → categories → exemples/detalls inferits). Connectors lògics a les fletxes.",
                "B2": "4+ nivells. Jerarquització complexa abstracta (CALP). Superestructura del gènere.",
                "C1": "Mapa de CONTRAST entre fonts o posicions ideològiques (no només contingut). Multi-font.",
                "C2": "Mapa de CONTRAST entre fonts o posicions ideològiques (no només contingut). Multi-font.",
            }
            _mapa_depth = _mapa_depth_map.get(_mecr_c3, _mapa_depth_map["B1"])
            output_sections.append(f"""
## Mapa conceptual
ACTIVAT — Genera un mapa conceptual en format text. Per a {_mecr_c3}: {_mapa_depth}
Usa NOMÉS llistes amb guions i indentació amb 2 espais.

**FORMAT OBLIGATORI (llista jeràrquica markdown, no caràcters de dibuix):**

```
- **CONCEPTE CENTRAL**
  - Branca 1:
    - Element a
    - Element b
  - Branca 2:
    - Element c
```

REGLES CRÍTIQUES:
- NO usis caràcters de dibuix d'arbre (│ ├ └ ─ ╔ ║). Causen corrupció
  en alguns models, que substitueixen lletres al mig de paraules
  ('Causes' → 'Cau—ses').
- NOMÉS guions `-` i indentació amb 2 espais per nivell.
- Negreta opcional al concepte central amb `**...**`.
- Bastida temporal: retira-la quan l'alumne pugui organitzar les idees sense suport.
""")

    # Variables de context per als complements pedagògics (MALL/TILC)
    materia_complement = params.get("materia") or context.get("materia") or "la matèria corresponent"
    etapa_complement = context.get("etapa") or params.get("etapa") or "l'etapa educativa corresponent"
    mecr_complement = params.get("mecr_sortida") or params.get("mecr") or "el nivell MECR indicat"
    _mecr_norm = (mecr_complement or "B1").upper().replace("Ç", "C")
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

    if comp.get("preguntes_comprensio") and _skills_on:
        # SKILLs ON: la SKILL aporta context detallat. AQUÍ donem format
        # ACCIONABLE perquè el LLM no ometi la secció.
        output_sections.append("""
## Preguntes de comprensió
ACTIVAT — Format OBLIGATORI:

### Abans de llegir
- [1-2 preguntes: predicció + activar coneixements previs]

### Durant la lectura
- [1-2 preguntes per a moments clau del text]

### Després de llegir
- [3-5 preguntes cobrint plànol literal + inferencial + crític, gradades al MECR]

Cada pregunta comença amb «- ». Vegeu SKILL generate-preguntes-comprensio per al detall pedagògic.
""")
    elif comp.get("preguntes_comprensio"):
        # SKILLs OFF: bloc hardcoded legacy (backup funcional)
        # C.2 MALL: formats per nivell + 3 plànols + quantitats per moment
        _pq_format_map = {
            "PRE-A1": "Emergent — NO escriptura autònoma. Formats ÚNICAMENT: assenyalar imatge, dibuixar, dramatitzar, dictat a l'adult.",
            "A1":     "Inicial — V/F textual (sobre paraules clau). Omplir buits AMB opcions donades (mai en blanc).",
            "A2":     "Funcional — relacionar amb fletxes, elecció múltiple de títols, ordenació de seqüències.",
            "B1":     "Estratègic — idem A2 + inferencials oberts (per què? i si...?). Inici d'argumentació breu.",
            "B2":     "Acadèmic — argumentació oberta, transferència al jo, contrast de fonts.",
            "C1":     "Crític — argumentació + valoració d'intencionalitat + judicis fonamentats sobre el text.",
            "C2":     "Crític — argumentació + valoració d'intencionalitat + judicis fonamentats sobre el text.",
        }
        _pq_planol_map = {
            "PRE-A1": "Tot via adult (propedèutic). NO preguntes escrites inferencials ni crítiques.",
            "A1":     "Literal predominant. Inferencial molt simple (màxim 1 pregunta).",
            "A2":     "Literal domina (2 preguntes). Inferencial apareix (1). Crític molt guiat (1).",
            "B1":     "Inferencial és motor (2 preguntes). Literal de base (1). Crític creixent (1-2).",
            "B2":     "Literal i inferencial de base. Crític sòlid (2 preguntes).",
            "C1":     "Crític és motor (3+ preguntes). Literal i inferencial de suport.",
            "C2":     "Crític és motor (3+ preguntes). Literal i inferencial de suport.",
        }
        _pq_format = _pq_format_map.get(_mecr_norm, _pq_format_map["B1"])
        _pq_planol = _pq_planol_map.get(_mecr_norm, _pq_planol_map["B1"])

        output_sections.append(f"""
## Preguntes de comprensió
ACTIVAT — Guió comprensió lectora MALL (3 moments · 3 plànols · formats per nivell).

Context: {materia_complement} · {etapa_complement} · MECR {mecr_complement} · gènere {genere_complement} · {modalitat_text}
Format per a {mecr_complement}: {_pq_format}
Pesos dels 3 plànols (Literal / Inferencial / Crític) per a {mecr_complement}: {_pq_planol}
Modalitat discursiva: {modalitat_linia[2:]}

QUANTITAT PER MOMENT (regla MALL «menys és més»):
- Abans de llegir: 2-3 preguntes (predicció + activació previs + propòsit)
- Durant la lectura: 1-2 aturades (dubte lèxic o hipòtesi en curs)
- Després de llegir: 3-5 preguntes (cobrir els 3 plànols amb el pes indicat amunt)

MODELATGE (Think Aloud): inclou 1 comentari de veu lectora experta que verbalitzi el procés, per exemple: «Com a lector, quan veig aquest títol em pregunto si és la idea clau. I tu, què en penses?»

FORMAT DE SORTIDA (exacte, és el que veu l'alumnat):

## Preguntes de comprensió

### Abans de llegir
- [predicció des del títol o imatge]
- [activació de previs: «Què saps de [tema]?»]
- [propòsit clar: «Llegeix per saber [una cosa concreta]»]

### Durant la lectura
- [aturada 1: dubte lèxic o hipòtesi parcial]
- [aturada 2 si escau: resum parcial o verificació d'hipòtesi]

### Després de llegir
[3-5 preguntes cobrint els 3 plànols amb el pes per a {mecr_complement}; 1 Think Aloud integrat]

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

    if comp.get("bastides") and _skills_on:
        # SKILLs ON: generate-bastides-lectura + generate-bastides-produccio
        # aporten el context pedagògic detallat. AQUÍ donem instrucció de
        # format ACCIONABLE perquè el LLM no ometi la secció (el context SKILL
        # és al mig del prompt; el format va al final).
        output_sections.append("""
## Bastides
ACTIVAT — Format OBLIGATORI:

### Bastides de lectura
- **Abans:** [1 pista per activar coneixement previ o predir]
- **Durant:** [1 pista per a un moment clau del text]
- **Després:** [1 pista per consolidar o verificar]

🚫 REGLA CRITICA — NO REPETIR EL TEXT:
Les bastides son **estrategies de control metacognitiu**, NO un re-llistat dels continguts del text.
- NO copies els passos d'un instructiu ni els fets d'una noticia.
- NO repeteixis les accions ja dites al "## Text adaptat".
- SI dones estrategies transferibles: ✅ "Comprova si has fet tots els passos en ordre",
  ✅ "Senyala el verb d'accio de cada pas", ✅ "Marca el material que ja tens".
- Si el text es INSTRUCTIU, les bastides "Durant" han de ser **estrategies executives**
  (autoregulació de la tasca), no la llista de passos.

### Bastides de resposta (només si preguntes_comprensio o activitats actives)
**Connectors útils:** [3-5 connectors gradats al MECR]
**Frases model:** [2-3 iniciadors per a respondre]

Vegeu SKILLs generate-bastides-lectura i generate-bastides-produccio per al detall pedagògic.
""")
    elif comp.get("bastides"):
        # SKILLs OFF: bloc hardcoded legacy (backup funcional)
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
        _is_low_mecr = _mecr_norm in ("PRE-A1", "A1", "A2")

        if _is_low_mecr:
            _bastides_title = "Suports"
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
            # C.1 MALL: connectors, iniciadors i paraules clau graduats per nivell MECR
            _connector_rows_map = {
                "PRE-A1": None,  # Nivell Emergent: sense taula de connectors
                "A1":  "| Lligar idees | i, després |\n| Contrastar | però |\n| Causa | perquè |",
                "A2":  "| Lligar idees | i, però, perquè |\n| Seqüenciar | primer, llavors |\n| Concloure | per tant |",
                "B1":  "| Causa | ja que, perquè |\n| Contrast | en canvi, però |\n| Afegir | a més a més |\n| Concedir | tot i que |",
                "B2":  "| Causa | ja que, atès que |\n| Conseqüència | en conseqüència, per contra |\n| Contrast | no obstant això, tot i que |\n| Afegir | així mateix |",
                "C1":  "| Causa | ja que, atès que |\n| Conseqüència | en conseqüència, per contra |\n| Contrast | no obstant això, tot i que |\n| Afegir | així mateix |",
                "C2":  "| Causa | ja que, atès que |\n| Conseqüència | en conseqüència, per contra |\n| Contrast | no obstant això, tot i que |\n| Afegir | així mateix |",
            }
            _iniciador_map = {
                "PRE-A1": "«A la imatge veig un ___.» (forat únic; suport visual obligatori)",
                "A1":     "«El personatge es diu ___ i vol ___.» (designació; màxim 2 forats)",
                "A2":     "«Segons el text, ___ va passar perquè ___.» (causa literal)",
                "B1":     "«Jo crec que ___ perquè el text diu ___.» (raonament propi)",
                "B2":     "«Aquest fenomen s'explica mitjançant ___, ja que ___.» (model teòric)",
                "C1":     "«L'autor intenta convèncer el lector de ___ fent servir ___.» (intencionalitat)",
                "C2":     "«L'autor intenta convèncer el lector de ___ fent servir ___.» (intencionalitat)",
            }
            _keyword_map = {
                "PRE-A1": "3-5 paraules + pictograma. Objectes reals del tema. NO tecnicismes.",
                "A1":     "5-8 paraules. Noms + verbs d'acció bàsics.",
                "A2":     "5-8 paraules. Noms + verbs d'acció bàsics.",
                "B1":     "~10 paraules. Inclou habilitats cognitives (hipòtesi, causa, conseqüència).",
                "B2":     "Lèxic d'especialitat pur (CALP). Sense equivalent col·loquial.",
                "C1":     "Lèxic d'especialitat pur (CALP). Sense equivalent col·loquial.",
                "C2":     "Lèxic d'especialitat pur (CALP). Sense equivalent col·loquial.",
            }
            _c_rows = _connector_rows_map.get(_mecr_norm, _connector_rows_map["B1"])
            _c_iniciador = _iniciador_map.get(_mecr_norm, _iniciador_map["B1"])
            _c_keywords = _keyword_map.get(_mecr_norm, _keyword_map["B1"])

            if _c_rows is None:
                _connectors_section = f"""
### 🔗 Connectors ({mecr_complement} — Emergent)
⚠️ Nivell Emergent: NO usis connectors abstractes. Si cal connectar idees, usa ÚNICAMENT «i» o «després».
Prefereix suport visual/oral en lloc de connectors textuals.
"""
            else:
                _connectors_section = f"""
### 🔗 Connectors per respondre ({mecr_complement})
Usa ÚNICAMENT els connectors d'aquesta taula (no n'afegeixis d'altres nivells):
| Per què | Paraules útils |
|---|---|
{_c_rows}
"""

            _bastides_block += f"""{_connectors_section}
### ✏️ Frases per començar la resposta
Model d'iniciador per a {mecr_complement}: {_c_iniciador}
Genera 3-4 variacions d'aquest patró adaptades al text concret (no donis la resposta sencera).

### 🗂️ Paraules clau del text
{_c_keywords}
Format llista separada per «–». Si són tècniques, marca-les amb (T): paraula1 – paraula2(T) – …
"""
        else:
            _bastides_block += """

### 💡 Recomanació
No hi ha preguntes ni activitats actives en aquesta adaptació. Per això NO s'inclouen
bastides de resposta (connectors + frases model). Si vols que l'alumne respongui,
activa també el complement «Preguntes de comprensió» o «Activitats d'aprofundiment».
"""

        output_sections.append(_bastides_block)

    if comp.get("resum"):
        # BUG fix (2026-05-22): Flash tenia branca "resum" a _build_flash_system_prompt
        # (server.py:4553) però el pipeline normal (Taller) no la tenia. Ara el Taller
        # també pot generar resum quan el docent activa el complement.
        output_sections.append(f"""
## Resum
ACTIVAT — Genera un resum del text adaptat en 3-5 frases en {lang_label}.
- Cobreix les idees principals en ordre lògic.
- Usa el nivell lingüístic del text adaptat (no simpliquis més del necessari).
- NO comences amb "Aquest text parla de..." — usa una frase directa sobre el contingut.
""")

    if comp.get("mapa_mental") and _skills_on:
        # SKILLs ON: generate-mapa-mental aporta gradació MECR. AQUÍ donem
        # format ACCIONABLE perquè el LLM no ometi la secció.
        output_sections.append("""
## Mapa mental
ACTIVAT — Format OBLIGATORI (llista markdown radial, NO fletxes Unicode):

```
- **CONCEPTE CENTRAL**
  - Branca 1
    - Idea associada
    - Pregunta generadora?
  - Branca 2
    - Connexió interdisciplinar
```

Pre-A1/A1: 2-3 branques, paraules clau + emojis.
A2/B1+: 3-5 branques amb associacions i preguntes generadores.

Vegeu SKILL generate-mapa-mental per al detall pedagògic.
""")
    elif comp.get("mapa_mental"):
        # SKILLs OFF: bloc backup amb format compatible amb renderer Mermaid (mindmap).
        # Usa llista markdown amb sagnia (-, 2 espais) — NO fletxes Unicode ni ASCII-art.
        output_sections.append("""
## Mapa mental
ACTIVAT — Genera un mapa mental radial (diferent del mapa conceptual).
Format: llista markdown amb sagnia (2 espais per nivell). Concepte central al primer
nivell, branques associatives al segon, idees i preguntes generadores al tercer.
NO usar fletxes Unicode ni ASCII-art. El frontend ATNE el renderitza com a
diagrama mindmap SVG (Mermaid).

Exemple de format:
```
- **CONCEPTE CENTRAL**
  - Branca 1
    - Idea associada
    - Pregunta generadora?
  - Branca 2
    - Connexió interdisciplinar
```
""")

    # Sempre: argumentació pedagògica + auditoria
    # Taxonomia A-G canonica (font: ui/saber-ne.html §"Categories d'adaptacio").
    # Decisio Miquel 2026-05-27: substituir 5 categories generiques per
    # aquesta taxonomia rica que connecta amb el coneixement docent FJE.
    output_sections.append("""
## Argumentació pedagògica
SEMPRE GENERAR — Justifica les decisions usant la taxonomia canonica FJE.
Genera 1 card per a CADA categoria on hi hagi hagut intervencio (omet les que no apliquen).
Per a cada card: identifica les sub-areas concretes (codi+nom) i justifica amb terminologia
pedagogica (MALL/DUA/UNE), NO descriptivament ("hem fet X").

Categories (usa nomes les que apliquen al cas concret):

**A. Adaptació Lingüística**
- Sub-arees: A1 Lèxic · A2 Sintaxi · A3 Cohesio · A4 Registre
- Que cobreix: triar vocabulari, construir frases, organitzar connectors, ajustar el to.
- Format card: indica quina/es sub-area/es s'han activat (ex: "A1+A2") i justifica.

**B. Estructura i Organització**
- Sub-arees: B1 Segmentacio · B2 Jerarquia · B3 Ordre · B4 Senyalitzacio
- Que cobreix: dividir el text, usar titols i llistes, ordre general↔particular.

**C. Suport Cognitiu**
- Sub-arees: C1 Carrega cognitiva · C2 Scaffolding · C3 Coneixements previs · C4 Metacognicio
- Que cobreix: reduir la sobrecarrega, bastides, activar previs, autoavaluacio.

**D. Multimodalitat**
- Sub-arees: D1 Suport visual · D2 Organitzadors grafics · D3 Redundancia canals
- Que cobreix: pictogrames, esquemes, taules, diagrames que faciliten comprensio per multiples vies.

**E. Contingut Curricular**
- Sub-arees: E1 Terminologia · E2 Rigor conceptual · E3 Exemples · E4 Contextualitzacio
- Que cobreix: que es manté del rigor i que s'adapta sense perdre la materia.

**F. Avaluació i Comprensió** (depèn de complements actius — SKILLs)
- Sub-arees: F1 Preguntes · F2 Activitats · F3 Autoavaluacio
- Que cobreix: preguntes graduades i activitats d'aprofundiment.
- IMPORTANT: el contingut detallat ve de les SKILLs canoniques activades
  (generate-preguntes-comprensio, generate-rubriques, etc.), no del catalog
  d'instruccions. Genera la card NOMES si hi ha complements F-actius
  (preguntes_comprensio, activitats_aprofundiment, rubriques, etc.).

**G. Personalització Lingüística** (nomes per a nouvinguts/L2)
- Sub-arees: G1 Suport L1 · G2 Adaptacio cultural
- Que cobreix: glossaris bilingues, referents culturals propers, exemples de l'experiencia de l'alumne.

**H. Adaptacions per Perfil** (cor d'ATNE — instruccions especifiques per condicio)
- Sub-arees: TEA · TDAH · Dislexia · DI · TDL · AACC · 2e · Disc.auditiva · Disc.visual · Discalculia · Vulnerabilitat · Dispraxia
- Que cobreix: instruccions especifiques per a CADA condicio activa al perfil
  (entre 5 i 12 per condicio). Aquesta es l'area MES extensa del prompt (>80 IDs).
- FORMAT: indica nomes les condicions REALMENT actives al perfil
  (ex: "H. TEA + TDAH" si el perfil te tots dos), no totes.

**I. Meta-regles Transversals** (regles que combinen tot l'anterior)
- Sub-arees: I1 Qualitat · I2 Integracio de perfils
- Que cobreix: com es combinen instruccions de multiples condicions sense
  contradiccions, regles de qualitat global (UNE, LF, MECR estricte).
- Genera la card NOMES si hi ha perfil multi-condicio o conflicte declarat
  entre regles.

FORMAT OBLIGATORI per card (encapçalament H3 + body):
```
### A. Adaptació Lingüística — A1+A2
[Justificacio en 1-2 frases amb terminologia pedagogica real, NO descriptiva.]

### B. Estructura i Organització — B1+B2
[Justificacio...]

### H. Adaptacions per Perfil — TDAH + Dislexia
[Justificacio especifica per a CADA condicio activa al perfil rebut.]
```

EXEMPLE CORRECTE:
### A. Adaptació Lingüística — A1+A2
S'ha reduit el lèxic a vocabulari frequent (BICS) per evitar carrega lexica
abans de la descodificacio. Sintaxi a SVO amb verbs en present d'indicatiu
per facilitar el processament a pre-A1 sense subordinacio.

EXEMPLE INCORRECTE:
**Adaptació lingüística**: Hem fet frases curtes i senzilles.
(Massa generic, sense codis, sense fonamentacio.)

Omet les categories que no apliquen. NO inventis sub-arees no llistades.
Cada card comença SEMPRE per `### [LLETRA]. [Nom] — [codis]`.

## Notes d'auditoria
SEMPRE GENERAR — Taula comparativa breu dels canvis principals:
| Aspecte | Original | Adaptat | Motiu |
Màxim 5-6 files amb els canvis més significatius.
""")

    # Recordatori final per evitar omissions (detectat 2026-05-25 al pilot:
    # amb SKILLs ON i 5+ complements activats, Mistral ometia bastides/mapa
    # conceptual/mapa mental). Els LLMs respecten millor les normes properes
    # a la generació, per això repetim la checklist al final amb instrucció
    # imperativa.
    _COMP_HEADERS = {
        "glossari": "Glossari",
        "esquema_visual": "Esquema visual",
        "mapa_conceptual": "Mapa conceptual",
        "mapa_mental": "Mapa mental",
        "preguntes_comprensio": "Preguntes de comprensió",
        "bastides": "Bastides",
        "plantilles_genere": "Plantilla de gènere",
        "resum_graduat": "Resum graduat",
        "cartes_conversacionals": "Cartes conversacionals",
        "rubriques": "Rúbriques d'autoavaluació",
        "activitats_aprofundiment": "Activitats d'aprofundiment",
        # Els següents són INLINE al text adaptat (no secció separada) →
        # NO incloure al CHECKLIST per evitar que el LLM generi secció buida
        # que el frontend interpreti com a "el model no ha generat aquest complement".
        "pictogrames": None,  # marcadors [PICTO: terme] inline; resolts pel backend ARASAAC
        "illustracions": None,  # marcadors [IMATGE: ...] inline; resolts per pipeline
        "negretes": None,  # ja integrat al text
        "definicions_integrades": None,  # ja integrat al text
        "traduccio_l1": None,  # ja al glossari
        "resum": "Resum",
    }
    _comp_actius_final = [_COMP_HEADERS[k] for k, v in comp.items()
                          if v and _COMP_HEADERS.get(k)]
    if _comp_actius_final:
        _lines = [f"{i+2}. ## {c}" for i, c in enumerate(_comp_actius_final)]
        n = len(_comp_actius_final)
        output_sections.append(f"""
## CHECKLIST DE GENERACIÓ — OBLIGATORI

Has de generar TOTES les seccions ## següents (en aquest ordre), independentment de la longitud del text adaptat:
1. ## Text adaptat
{chr(10).join(_lines)}
{n+2}. ## Argumentació pedagògica
{n+3}. ## Notes d'auditoria

Si t'oblides cap secció, l'usuari rep una targeta buida. PROHIBIT ometre seccions activades. Si el contingut és curt, fes-lo curt però NO l'ometis.
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

El text adaptat ha de ser llegible directament per l'alumne i ha de RESPECTAR EL FORMAT del gènere demanat ("{}"). Si el bloc de complements actius està buit, NO inventis exercicis ni activitats per omplir.
""".format(params.get("genere_discursiu", "divulgatiu")))

    parts.append("\n".join(output_sections))

    return "\n".join(parts)


def build_complements_prompt(profile: dict, context: dict, params: dict) -> str:
    """System prompt per a la 2a crida LLM dedicada als complements pedagògics.

    Rep el text ja adaptat com a missatge d'usuari (no en el system prompt).
    Retorna string buit si no hi ha complements actius o SKILLs desactivats
    (en aquest cas l'orquestrador no fa la 2a crida).
    """
    comp = params.get("complements", {})
    comp_actius = {k for k, v in comp.items() if v}
    if not comp_actius:
        return ""

    try:
        import skills_loader
        if not skills_loader.is_skills_enabled():
            return ""
    except Exception:
        return ""

    mecr = params.get("mecr_sortida", "B2")
    lang = params.get("lang", "ca")
    genre = params.get("genere_discursiu") or context.get("genere_discursiu") or ""
    chars = profile.get("caracteristiques", {})
    active_profiles = [k for k, v in chars.items() if isinstance(v, dict) and v.get("actiu")]
    _nouv = chars.get("nouvingut", {})
    l1 = _nouv.get("L1", "") or _nouv.get("l1", "")

    lang_label = get_lang_label(lang)
    parts = [
        f"Ets un generador de complements pedagògics per a textos educatius adaptats ({lang_label}).\n"
        "Reps un text ja adaptat i has de generar ÚNICAMENT els complements sol·licitats, "
        "sense reproduir ni modificar el text adaptat.",
        f"MECR de l'alumne: {mecr}"
        + (f" | Condicions: {', '.join(active_profiles)}" if active_profiles else "")
        + (f" | Gènere: {genre}" if genre else ""),
    ]
    if l1:
        parts.append(f"L1 de l'alumne: {l1} — usa-la als glossaris bilingües (columna Traducció).")

    # SKILLs de complements (aporten instruccions detallades per a cada complement)
    try:
        _all = skills_loader.load_skills(skills_loader.default_skills_roots())
        _active = skills_loader.select_active(_all, profile, params, agent_role="complements")
        if _active:
            _names = ", ".join(s.name for s in _active)
            print(f"[complements_call] SKILLs ({len(_active)}): {_names}", flush=True)
            # Fix 2026-05-29: NO renderitzem el body de generate-bastides-* aquí.
            # Son rúbriques-referència de ~17K (descriuen els 7 nivells MECR) que,
            # a més, repeteixen "PROHIBIT generar ## Preguntes" (priming per negació).
            # Resultat: el model abocava el contingut dels 3 moments sota
            # "## Preguntes de comprensió" i deixava "## Bastides" buit (i
            # l'orchestrator esborrava el "## Preguntes" no autoritzat → contingut
            # perdut). La directiva Python lean de més avall cobreix el contingut
            # operatiu per nivell. La SKILL es manté com a canon de referència.
            _render = [s for s in _active if not s.name.startswith("generate-bastides")]
            if _render:
                parts.append(skills_loader.render_skill_block(_render))
        else:
            # Cap SKILL activa — no val la pena fer la 2a crida
            return ""
    except Exception as _e:
        print(f"[complements_call] skills error: {_e}", flush=True)
        return ""

    # CHECKLIST — enumera les seccions a generar (sense "Text adaptat")
    _COMP_TITLES = {
        "glossari": "Glossari",
        "esquema_visual": "Esquema visual",
        "mapa_conceptual": "Mapa conceptual",
        "mapa_mental": "Mapa mental",
        "preguntes_comprensio": "Preguntes de comprensió",
        "bastides": "Bastides",
        "plantilles_genere": "Plantilla de gènere",
        "resum_graduat": "Resum graduat",
        "cartes_conversacionals": "Cartes conversacionals",
        "rubriques": "Rúbriques d'autoavaluació",
        "activitats_aprofundiment": "Activitats d'aprofundiment",
        "pictogrames": None,   # marcadors inline; resolts per ARASAAC
        "illustracions": None, # marcadors inline; resolts per pipeline imatges
        "negretes": None,
        "definicions_integrades": None,
        "traduccio_l1": None,
        "resum": "Resum",
    }
    _seccions = [_COMP_TITLES[k] for k in comp_actius if _COMP_TITLES.get(k)]
    if not _seccions:
        return ""

    _lines = [f"{i+1}. ## {s}" for i, s in enumerate(_seccions)]
    n = len(_seccions)
    parts.append(f"""
CHECKLIST DE GENERACIÓ — OBLIGATORI
Genera TOTES les seccions ## següents basant-te en el text adaptat que reps:
{chr(10).join(_lines)}

Títols exactes (sense prefixos ni emojis). Sub-apartats amb ###.
PROHIBIT reproduir el text adaptat. PROHIBIT ometre seccions. Si el contingut és curt, fes-lo curt però NO l'ometis.
""")

    # Fix 2026-05-29 (Bug bastides buides en 2-call):
    # El mecanisme real del buit era a clean_gemini_output §5c (post_process.py):
    # una xarxa de seguretat inseria un "## Preguntes de comprensió" fantasma
    # davant de qualsevol "### Abans de llegir", relocant el cos de bastides a una
    # secció que l'orchestrator després esborrava (no autoritzada). Allà es
    # resol l'arrel. Aquí donem el reforç que tots els germans estructurals
    # (rubriques/mapa_mental/esquema_visual) ja tenien i bastides no: una directiva
    # lean computada en Python, a prop de la generació, amb la llesca del nivell
    # EXACTE (Python ja sap mecr/dua/nouvingut/producció). A més, deixem de
    # renderitzar el body de ~17K de les SKILLs-rúbrica en aquesta crida (es queden
    # com a canon de referència) i forcem el títol únic "## Bastides" (= checklist
    # + filtre orchestrator), eliminant la triple ambiguïtat de títol de la SKILL
    # (Bastides / Suports per llegir / Bastides — Estratègia lectora).
    if "bastides" in comp_actius:
        _mecr_b = (mecr or "B1").upper().replace("Ç", "C")
        _dua_b = (params.get("dua") or "Core").strip()
        _produccio_activa = bool(
            comp.get("preguntes_comprensio") or comp.get("activitats_aprofundiment")
        )
        # Plantilla dels 3 moments per banda MECR (derivada de la SKILL canònica,
        # reformulada com a directiva). Cada entrada: (abans, durant, després).
        # CRÍTIC: ítems IMPERATIUS (verb d'acció, sense interrogants). Si es
        # formulen com a preguntes («Què saps de…?») el model relabela la secció
        # com a «## Preguntes de comprensió» i deixa «## Bastides» buida. Les
        # bastides son ESTRATÈGIES (com llegir), no preguntes sobre el contingut.
        _bastides_moments = {
            "PRE-A1": (
                "Mostra una imatge o el títol i deixa que l'alumne assenyali o anomeni el que veu.",
                "Llegeix en veu alta mentre l'alumne assenyala, dramatitza o dibuixa. Sense lectura autònoma.",
                "Demana-li que dibuixi o ordeni imatges del que ha entès (dictat oral a l'adult).",
            ),
            "A1": (
                "Mira el títol, recorda el que ja saps del tema i predigues de què parlarà.",
                "Llegeix amb l'adult, segueix amb el dit i subratlla 1 mot clau per paràgraf.",
                "Completa la frase: «El text parla de ___».",
            ),
            "A2": (
                "Recorda 2 coses que ja saps del tema i fixa't un propòsit: «Llegeix per identificar [X]».",
                "Llegeix sol i marca al marge ✓ (entès) / ? (dubte) / ! (important).",
                "Escriu un resum de 2-3 frases i explica una idea amb «Crec que … perquè …».",
            ),
            "B1": (
                "Escriu la teva hipòtesi abans de llegir: «Crec que el text dirà ___ perquè ___».",
                "Pren notes breus al marge i atura't a mitja lectura per revisar la teva hipòtesi.",
                "Resumeix en 3-4 frases (idea principal + 2 secundàries) i valora si hi estàs d'acord, dient per què.",
            ),
            "B2+": (
                "Identifica el gènere i la font, i anticipa quin pot ser el posicionament de l'autor.",
                "Marca al marge el posicionament de l'autor i contrasta'l amb el que ja sabies.",
                "Fes un resum jeràrquic, detecta pressuposicions i avalua si les dades són fiables.",
            ),
        }
        if _mecr_b in ("B2", "C1", "C2"):
            _band = "B2+"
        elif _mecr_b in _bastides_moments:
            _band = _mecr_b
        else:
            _band = "B1"
        _ab, _du, _de = _bastides_moments[_band]

        # Modulació DUA Accés + nivell baix → cap escriptura autònoma.
        _no_escriptura = _band == "PRE-A1" or (_dua_b == "Accés" and _mecr_b in ("PRE-A1", "A1", "A2"))
        _acces_line = (
            "\n⚠️ DUA Accés / nivell baix: CAP escriptura autònoma. Substitueix «Escriu» per "
            "accions físiques («Assenyala», «Tria entre 2 opcions», «Diu en veu alta»). Plànol crític PROHIBIT. "
            "LF estricta UNE 153101: una idea per frase."
            if _no_escriptura else ""
        )
        # Modificador NOUVINGUT (TILC/TOLC): comparació L1↔català ancorada al glossari.
        _tilc_line = (
            f"\n🌍 Nouvingut (L1 {l1}): inclou 1 iniciador comparat L1↔català per moment "
            f"(ex: «En {l1}, com es diu [paraula]? Mira el glossari») i ancora explícitament al glossari."
            if (l1 and _mecr_b in ("PRE-A1", "A1", "A2")) else ""
        )

        # Desambiguació bastides ↔ preguntes_comprensio. El model té un prior molt
        # fort: tota estructura "abans/durant/després de llegir" la titula
        # "## Preguntes de comprensió", encara que no es demani, i deixa
        # "## Bastides" buida. Cal una redirecció explícita segons si preguntes
        # està activa o no en aquest cas.
        _preguntes_activa = bool(comp.get("preguntes_comprensio"))
        if _preguntes_activa:
            _disambig = (
                "`## Bastides` (estratègies de COM llegir, en imperatiu) i `## Preguntes de comprensió` "
                "(preguntes sobre el CONTINGUT) són seccions DIFERENTS; genera-les totes dues per separat. "
                "Les 3 pistes d'estratègia (abans/durant/després) van a `## Bastides`, MAI barrejades amb les preguntes."
            )
        else:
            _disambig = (
                "⛔ Aquest cas NO demana preguntes de comprensió: NO generis cap secció `## Preguntes de comprensió` "
                "ni cap variant. Les pistes dels 3 moments són BASTIDES i van EXCLUSIVAMENT sota `## Bastides`."
            )

        # Bloc de resposta (producció) — només si hi ha producció activa i no és pre-A1
        # (a pre-A1 la SKILL -produccio no genera res). Mirall de la condició de la SKILL.
        _resposta_block = ""
        if _produccio_activa and _band != "PRE-A1":
            _resposta_block = """
### Bastides de resposta
Genera també (perquè hi ha preguntes/activitats actives):
- **Base d'orientació:** 3-4 passos del procés per construir la resposta del gènere treballat (GPS disciplinar, no «introducció/cos/conclusió» genèric).
- **Connectors útils:** 3-5 connectors graduats al MECR.
- **Frases per començar:** 2-3 iniciadors model (forats, NO la resposta sencera).
"""

        parts.append(f"""
## INSTRUCCIÓ ESPECÍFICA — Bastides (OBLIGATÒRIA)
Reprodueix EXACTAMENT aquest esquema: és la secció `## Bastides` SENCERA, amb la
capçalera literal i les 3 subseccions. Omple cada ítem a partir del text adaptat que
reps. Són pistes d'ESTRATÈGIA LECTORA (com llegir, transferibles a qualsevol text del
mateix gènere/nivell), adaptades a {_mecr_b} — no un re-llistat dels fets del text.

## Bastides

### Abans de llegir — prepara la lectura
- {_ab}

### Durant la lectura — estratègies de lector
- {_du}

### Després de llegir — consolida i revisa
- {_de}
{_resposta_block}{_acces_line}{_tilc_line}

{_disambig}
PROHIBIT deixar `## Bastides` amb el cos buit o només amb la intro: omple SEMPRE els 3 moments amb 1-3 ítems cadascun.
NO incloguis marcadors de pictogrames `[PICTO: …]` en aquesta secció.
""")

    # Fix 2026-05-31 (Cas titella — glossari ple de paraules quotidianes):
    # La SKILL generate-glossari té dues regles canòniques crítiques que es
    # perden a la pràctica:
    #   - M3 §5 "Selecció pertinent: cap paraula quotidiana òbvia"
    #   - M3 §5 "Llengua de definició: Català"
    # Davant un text receptari ("Necessites: mitja, botons, agulla, fil…")
    # i un perfil dislèxia A1, el model genera taula de 6 termes amb 4
    # quotidians + a vegades castellanismes a les definicions ("titella →
    # Muñeco"). Mirall de bastides: directiva Python a prop de la generació
    # que fa prominents aquestes dues regles amb exemples concrets.
    if "glossari" in comp_actius:
        _mecr_gl = (mecr or "B1").upper().replace("Ç", "C")
        _is_low_gl = _mecr_gl in ("PRE-A1", "A1")
        _has_pictos = bool(comp.get("pictogrames"))
        _picto_note = (
            " Si pictogrames està ACTIVAT, el vocabulari quotidià es resol via "
            "pictograma inline (mediació visual), NO al glossari."
            if _has_pictos else ""
        )
        _quotidia_block = (
            f"""
🔴 FILTRE DE SELECCIÓ LÈXICA (regla canònica SKILL §5, prominent a {_mecr_gl}):
SOSTRE ESTRICTE: a {_mecr_gl}, **MÀXIM 2 termes** al glossari. Si en tens 4
candidats en ment, és senyal que n'estàs incloent de quotidians.

EXCLOU del glossari tot el vocabulari QUOTIDIÀ que un alumne de {_mecr_gl}+etapa
inicial JA coneix. Exemples que NO van al glossari:
  • Objectes domèstics i materials comuns: **mitja, botó, agulla, fil, retolador,
    llapis, paper, taula, casa, porta, plat, got…**
  • Parts del cos: cap, mà, ulls, boca, peu…
  • Verbs d'acció bàsics: posar, lligar, dibuixar, jugar, mirar, fer…
  • Connectors, quantificadors i adjectius generals.{_picto_note}

⚠️ AMBIGÜITAT FIDELITAT-vs-QUOTIDIÀ: la regla SKILL "fidelitat al lèxic nuclear
del text" NO obliga a definir tots els termes centrals del text. Obliga que els
que DEFINEIXIS hi siguin literalment. **Si un terme central és quotidià, OMET-LO
del glossari** — el pictograma o el coneixement previ s'encarreguen del suport
lèxic. A {_mecr_gl}, quotidià > fidelitat.

INCLOU NOMÉS termes que siguin: (a) realment tècnics o de la disciplina,
(b) inusuals per al nivell, o (c) específics del text fora del lèxic quotidià.
Si el text no en conté cap de realment nou, escriu sota la capçalera
`## Glossari` la nota: **«Aquest text no necessita glossari nou per al teu nivell.»**
i prou. Millor 0-2 termes ben triats que 4-6 termes redundants.
"""
            if _is_low_gl else ""
        )
        parts.append(f"""
## INSTRUCCIÓ ESPECÍFICA — Glossari (OBLIGATÒRIA)
Reforç de regles canòniques del SKILL generate-glossari que es perden quan hi
ha molts complements actius simultàniament.
{_quotidia_block}
🔴 LLENGUA DE LES DEFINICIONS — CATALÀ ESTRICTE:
Cada cel·la d'explicació ha de ser en català. CAP castellanisme com a definició
(NO «Muñeco» per definir «titella», NO «calcetín» per «mitja», NO «aguja» per
«agulla», NO «hilo» per «fil»). Si no saps la paraula catalana exacta, descriu-la
sense usar la paraula castellana («ninot petit de drap que es mou amb la mà»)
o omet el terme.

🔴 FIDELITAT AL TEXT: tots els termes del glossari han d'aparèixer LITERALMENT
al `## Text adaptat`. NO inventis termes que no hi siguin.
""")

    # Fix 2026-05-27 (Bug 1 — esquema_visual buit en 2-call):
    # esquema_visual NO té SKILL pròpia (vegeu tests/golden/matrix.yaml: skill: null).
    # A la crida 2 dels complements, sense SKILL i amb només "## Esquema visual" al
    # checklist, els LLMs generaven la capçalera però deixaven el cos buit. Reforcem
    # amb instrucció explícita de format + nombre de nodes graduat per MECR.
    # Fix 2026-05-27 — Bug rubriques mai generades:
    # Tot i tenir SKILL i checklist, gpt-4.1-mini ometia la seccio.
    # Reforcem amb format taula explicit + escala FJE concreta.
    if "rubriques" in comp_actius:
        _mecr_r = (mecr or "B1").upper().replace("Ç", "C")
        _r_format = ""
        if _mecr_r in ("PRE-A1",):
            _r_format = (
                "**Format checklist binari** (pre-A1, NO escala FJE):\n"
                "- [ ] He fet [accio observable 1]\n"
                "- [ ] He fet [accio observable 2]\n"
                "- [ ] He fet [accio observable 3]\n"
                "2-3 items, primera persona, accions fisiques visibles."
            )
        elif _mecr_r == "A1":
            _r_format = (
                "**Format taula 3 nivells** (A1, sense vocabulari FJE):\n"
                "| Criteri | Encara no | Si | Si, i alguna cosa mes |\n"
                "|---|---|---|---|\n"
                "| He escrit [tasca 1] | | | |\n"
                "| He usat [tasca 2] | | | |\n"
                "2-3 criteris accionables, primera persona."
            )
        else:
            _r_format = (
                "**Format taula escala FJE** (A2+):\n"
                "| Criteri | NA (No Assolit) | AS (Assolit Suficient) | AN (Assolit Notable) | AE (Assolit Excel·lent) |\n"
                "|---|---|---|---|---|\n"
                "| He [accio observable 1] | [descriptor NA] | [descriptor AS] | [descriptor AN] | [descriptor AE — salt qualitatiu] |\n"
                "| He [accio observable 2] | ... | ... | ... | ... |\n"
                "| He [accio observable 3] | ... | ... | ... | ... |\n"
                f"{'4-5' if _mecr_r in ('B1','B2') else '3-4'} criteris × 4 nivells. "
                "Primera persona SEMPRE ('He escrit...', no 'Has escrit'). "
                "AE = salt qualitatiu (originalitat, transferencia), NO 'AN + esforç'."
            )
        parts.append(f"""
## INSTRUCCIO ESPECIFICA — Rubriques d'autoavaluacio (OBLIGATORIA)
Genera OBLIGATORIAMENT la seccio `## Rubriques d'autoavaluacio` per a un alumne {_mecr_r}.
Es una rubrica ALUMNE-FACING (per a que l'alumne autoavalui la seva propia produccio
basada en el text adaptat), NO una rubrica per al docent.

{_r_format}

PROHIBIT generar la capçalera "## Rubriques d'autoavaluacio" amb el cos buit.
PROHIBIT usar segona ("Has fet") o tercera persona ("L'alumne ha fet").
""")

    # Fix 2026-05-27 — Bug mapa mental confus:
    # Reforcem amb format Buzan radial concret (no llista jerarquica = mapa conceptual).
    if "mapa_mental" in comp_actius:
        parts.append("""
## INSTRUCCIO ESPECIFICA — Mapa mental (OBLIGATORIA)
Genera OBLIGATORIAMENT la seccio `## Mapa mental` amb format **radial Buzan**:
1 concepte central + 4-6 branques primaries + sub-branques associatives.

FORMAT OBLIGATORI (text/markdown — el frontend renderitza com a graf radial):
```
- **[CONCEPTE CENTRAL]** (idea principal del text)
  - **Branca 1: [tema associat]**
    - [associacio lliure 1a]
    - [associacio lliure 1b]
  - **Branca 2: [tema associat]**
    - [associacio lliure 2a]
    - [pregunta generadora]
  - **Branca 3: [connexio interdisciplinar]**
    - [pont amb altra materia]
  - **Branca 4: [pregunta oberta divergent]**
    - [hipotesi alternativa]
```

DIFERENCIA del mapa conceptual:
- Mapa CONCEPTUAL: jerarquia + relacions etiquetades (estructura, convergent).
- Mapa MENTAL: associacio lliure + connexions creatives (divergent, Buzan-style).
PROHIBIT generar el mateix contingut que mapa_conceptual si tots dos estan activats.
PROHIBIT capçalera "## Mapa mental" amb cos buit.
""")

    if "esquema_visual" in comp_actius:
        _mecr_c3 = (mecr or "B1").upper().replace("Ç", "C")
        _esquema_nodes_map = {
            "PRE-A1": "2-3 nodes. Seqüències temporals bàsiques (abans→després) o relacions imatge→paraula.",
            "A1":     "3-4 nodes. Enumeració de qualitats o parts d'un objecte (descripció simple).",
            "A2":     "4-6 nodes. Seqüència de passos d'instrucció o esdeveniments cronològics.",
            "B1":     "6-8 nodes. Relacions causa-efecte o hipòtesi-evidència.",
        }
        _esquema_nodes = _esquema_nodes_map.get(
            _mecr_c3,
            "Nombre de nodes a criteri docent. Modelitza processos complexos."
        )
        parts.append(f"""
## INSTRUCCIÓ ESPECÍFICA — Esquema visual (OBLIGATÒRIA)
Si esquema_visual=true, GENERA OBLIGATÒRIAMENT 3-5 nodes amb relacions; NO deixis la secció buida.
Per a {_mecr_c3}: {_esquema_nodes}

Format OBLIGATORI: llista markdown amb sagnia. NO usar fletxes Unicode (→, ↓) ni ASCII-art (│ ├ └).
El frontend ATNE detecta aquest format i el renderitza com a diagrama SVG (Mermaid flowchart LR).

Exemple de format (adapta'l al text rebut):
```
- Tema central
  - Subtema 1
    - Detall A
  - Subtema 2
    - Detall B
- Conclusió
```

PROHIBIT generar la capçalera "## Esquema visual" amb el cos buit. Si no saps quins nodes
posar, extreu-los del text adaptat (idees principals + relacions causa-efecte o seqüencials).
""")

    return "\n\n".join(parts)

