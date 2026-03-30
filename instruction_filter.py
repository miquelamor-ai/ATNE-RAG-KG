"""
instruction_filter.py — Filtratge d'instruccions i agrupació en macrodirectives.

Aplica les regles d'activació del catàleg (instruction_catalog.py) per retornar
NOMÉS les instruccions rellevants, agrupades en macrodirectives temàtiques.

El prompt de l'LLM rep blocs temàtics nets (LÈXIC, SINTAXI, ESTRUCTURA...) sense IDs.
Els IDs es conserven als logs i a l'auditoria per traçabilitat.

Referència: docs/decisions/mapa_variables_instruccions.md
"""

from instruction_catalog import CATALOG, MACRODIRECTIVES, PROFILE_INSTRUCTION_MAP, LLENGUES_ROMANIQUES


def _is_l1_romanica(l1: str) -> bool:
    """Comprova si la L1 és una llengua romànica."""
    return l1.lower().strip() in LLENGUES_ROMANIQUES


def _check_subvar_conditions(instr: dict, profile_data: dict, mecr: str, chars: dict) -> bool:
    """
    Comprova si les condicions de sub-variables es compleixen.

    Suporta totes les sub-variables connectades:
    - alfabet_llati: bool
    - mecr_low: pre-A1/A1
    - L1_romanica: L1 és llengua romànica o familia_linguistica=romanica
    - sensibilitat_tematica: bool
    - grau_ceguesa: disc_visual.grau == "ceguesa"
    - tipus_fonologica: dislexia.tipus_dislexia == "fonologica" o "mixta"
    - fatiga_o_sever: tdah.fatiga_cognitiva==true O di.grau=="sever"
    """
    conditions = instr.get("subvar_conditions", {})
    if not conditions:
        return True

    for key, expected in conditions.items():
        if key == "alfabet_llati":
            actual = profile_data.get("alfabet_llati", True)
            if isinstance(actual, str):
                actual = actual.lower() not in ("no", "false", "0")
            if actual != expected:
                return False

        elif key == "mecr_low":
            if expected and mecr not in ("pre-A1", "A1"):
                return False

        elif key == "L1_romanica":
            l1 = profile_data.get("L1", "")
            fam = profile_data.get("familia_linguistica", "")
            is_romanic = _is_l1_romanica(l1) or fam == "romanica"
            if expected and not is_romanic:
                return False

        elif key == "sensibilitat_tematica":
            actual = profile_data.get("sensibilitat_tematica", False)
            if isinstance(actual, str):
                actual = actual.lower() in ("true", "1", "sí", "si")
            if actual != expected:
                return False

        elif key == "grau_ceguesa":
            actual = profile_data.get("grau", "")
            if expected and actual != "ceguesa":
                return False

        elif key == "tipus_fonologica":
            actual = profile_data.get("tipus_dislexia", "")
            if expected and actual not in ("fonologica", "mixta"):
                return False

        elif key == "fatiga_o_sever":
            fatiga = profile_data.get("fatiga_cognitiva", False)
            if isinstance(fatiga, str):
                fatiga = fatiga.lower() in ("true", "1")
            grau = profile_data.get("grau", "")
            if expected and not fatiga and grau != "sever":
                return False

    return True


def _should_suppress(instr: dict, active_profiles: list[str], dua: str) -> bool:
    """Comprova si una instrucció SEMPRE s'ha de suprimir per un perfil actiu."""
    suppress_list = instr.get("suppress_if", [])
    if not suppress_list:
        return False

    for profile in suppress_list:
        if profile in active_profiles:
            return True
    if "altes_capacitats" in suppress_list and dua == "Enriquiment":
        return True

    return False


def _should_suppress_by_profile(instr: dict, active_profiles: list[str]) -> bool:
    """Suprimeix instruccions redundants quan un perfil específic ja les cobreix."""
    suppress_profiles = instr.get("suppress_if_profile", [])
    for p in suppress_profiles:
        if p in active_profiles:
            return True
    return False


def _get_intensified_text(iid: str, instr: dict, chars: dict, mecr: str) -> str:
    """
    Retorna el text de la instrucció, intensificat si sub-variables ho demanen.

    Exemples d'intensificació:
    - C-01 amb baixa_memoria_treball: "1-2 conceptes" → "1 concepte"
    - C-04 amb baixa_memoria_treball: "3-5 elements" → "3 elements màxim"
    - H-04 amb grau=sever: "3-5 frases" → "2-3 frases"
    """
    text = instr["text"]

    # Intensificació de C-01 per baixa memòria de treball
    if iid == "C-01" and "mecr_detail" in instr:
        detail = instr["mecr_detail"].get(mecr, "")
        if detail:
            # Comprovar si tdah.baixa_memoria_treball actiu
            tdah_data = chars.get("tdah", {})
            if tdah_data.get("actiu") and _str_to_bool(tdah_data.get("baixa_memoria_treball", False)):
                detail = detail.replace("1-2", "1").replace("2 conceptes", "1 concepte").replace("3 conceptes", "2 conceptes")
            return detail
        return text

    # Intensificació de C-04 per baixa memòria de treball
    if iid == "C-04":
        tdah_data = chars.get("tdah", {})
        if tdah_data.get("actiu") and _str_to_bool(tdah_data.get("baixa_memoria_treball", False)):
            return "Chunking estricte: agrupa informació en blocs de MÀXIM 3 elements (memòria de treball limitada)."

    # Intensificació de H-04 per grau sever
    if iid == "H-04":
        tdah_data = chars.get("tdah", {})
        if tdah_data.get("actiu") and tdah_data.get("grau") == "sever":
            return "TDAH sever: micro-blocs de 2-3 frases amb objectiu explícit per bloc ('En aquest bloc aprendràs...'). Blocs molt curts."

    # Intensificació de H-20 per comunicació LSC
    if iid == "H-20":
        aud_data = chars.get("disc_auditiva", chars.get("discapacitat_auditiva", {}))
        com = aud_data.get("comunicacio", "")
        impl = _str_to_bool(aud_data.get("implant_coclear", False))
        if com == "LSC":
            return "Discapacitat auditiva (LSC): simplificació intensiva com L2. Eliminar subordinades, una idea per frase, vocabulari molt freqüent."
        if impl:
            return "Discapacitat auditiva (implant coclear): simplificació moderada. Mantenir estructures senzilles però permetre més complexitat que en LSC."

    return text


def _str_to_bool(val) -> bool:
    """Converteix string a bool de forma tolerant."""
    if isinstance(val, bool):
        return val
    if isinstance(val, str):
        return val.lower() in ("true", "1", "sí", "si")
    return bool(val)


def get_instructions(profile: dict, params: dict) -> dict:
    """
    Retorna les instruccions filtrades, agrupades per macrodirectiva.

    Args:
        profile: dict amb 'caracteristiques' (cada una amb sub-variables)
        params: dict amb 'mecr_sortida', 'dua', 'complements', etc.

    Returns:
        dict amb claus:
            'macrodirectives': dict de macro_id → {label, instruccions: [{id, text}]}
            'suppressed': llista d'IDs suprimits
            'audit': llista de {id, text, macro, motiu} per traçabilitat
            'stats': resum del filtratge
    """
    mecr = params.get("mecr_sortida", "B2")
    dua = params.get("dua", "Core")
    complements = params.get("complements", {})
    chars = profile.get("caracteristiques", {})

    active_profiles = [key for key, val in chars.items() if val.get("actiu")]

    # Resultat organitzat per macrodirectiva
    macros = {}
    suppressed = []
    audit = []

    for iid, instr in CATALOG.items():
        activation = instr["activation"]
        macro_id = instr.get("macro", "ALTRES")
        included = False
        motiu = ""

        # ── SEMPRE ──
        if activation == "SEMPRE":
            if _should_suppress(instr, active_profiles, dua):
                suppressed.append(iid)
                audit.append({"id": iid, "macro": macro_id, "motiu": f"suprimit per AC/Enriquiment"})
                continue
            if _should_suppress_by_profile(instr, active_profiles):
                suppressed.append(iid)
                audit.append({"id": iid, "macro": macro_id, "motiu": f"suprimit per perfil redundant"})
                continue
            included = True
            motiu = "SEMPRE"

        # ── NIVELL ──
        elif activation == "NIVELL":
            if "mecr_detail" in instr:
                detail = instr["mecr_detail"].get(mecr, "")
                if detail:
                    included = True
                    motiu = f"NIVELL {mecr}"
            elif "mecr_levels" in instr:
                if mecr in instr["mecr_levels"]:
                    included = True
                    motiu = f"NIVELL {mecr}"
            else:
                included = True
                motiu = "NIVELL (fallback)"

        # ── PERFIL ──
        elif activation == "PERFIL":
            target_profiles = instr.get("profiles", [])
            matching = [p for p in active_profiles if p in target_profiles]
            if matching:
                has_subvar = "subvar_conditions" in instr
                if has_subvar:
                    for p in matching:
                        profile_data = chars.get(p, {})
                        if _check_subvar_conditions(instr, profile_data, mecr, chars):
                            included = True
                            motiu = f"PERFIL {p} + subvar"
                            break
                else:
                    included = True
                    motiu = f"PERFIL {', '.join(matching)}"

        # ── COMPLEMENT ──
        elif activation == "COMPLEMENT":
            comp_key = instr.get("complement", "")
            if comp_key and complements.get(comp_key):
                included = True
                motiu = f"COMPLEMENT {comp_key}"

        # Afegir a macrodirectiva si inclosa
        if included:
            if macro_id not in macros:
                macro_def = MACRODIRECTIVES.get(macro_id, {"label": macro_id, "ordre": 99})
                macros[macro_id] = {
                    "label": macro_def["label"],
                    "ordre": macro_def["ordre"],
                    "instruccions": [],
                }
            # Text potencialment intensificat
            text = _get_intensified_text(iid, instr, chars, mecr)
            macros[macro_id]["instruccions"].append({"id": iid, "text": text})
            audit.append({"id": iid, "macro": macro_id, "motiu": motiu})

    # ── Estadístiques ──
    total = sum(len(m["instruccions"]) for m in macros.values())
    stats = {
        "total_instruccions": total,
        "total_macrodirectives": len(macros),
        "instruccions_per_macro": {k: len(v["instruccions"]) for k, v in macros.items()},
        "suprimides": len(suppressed),
        "perfils_actius": active_profiles,
        "mecr": mecr,
        "dua": dua,
    }

    return {
        "macrodirectives": macros,
        "suppressed": suppressed,
        "audit": audit,
        "stats": stats,
    }


def format_instructions_for_prompt(filtered: dict) -> str:
    """
    Formata les instruccions filtrades com a macrodirectives per al system prompt.

    Genera blocs temàtics NETS (sense IDs) per a l'LLM.
    L'LLM veu 6-9 blocs coherents en lloc de 40+ regles atòmiques.
    """
    macros = filtered["macrodirectives"]

    # Ordenar per ordre definit a MACRODIRECTIVES
    sorted_macros = sorted(macros.items(), key=lambda x: x[1]["ordre"])

    sections = []

    for macro_id, macro in sorted_macros:
        if not macro["instruccions"]:
            continue

        label = macro["label"]
        texts = [instr["text"] for instr in macro["instruccions"]]

        # Agrupar en bloc compacte (prosa, no llista numerada)
        block = f"**{label}**: {' '.join(texts)}"
        sections.append(block)

    # Info de supressions per altes capacitats
    if filtered["suppressed"]:
        n = len(filtered["suppressed"])
        sections.append(
            f"⚠️ IMPORTANT: {n} regles de simplificació DESACTIVADES per aquest perfil. "
            "NO simplifiquis el text. Enriqueix-lo."
        )

    return "\n\n".join(sections)


def format_audit_log(filtered: dict) -> str:
    """
    Genera un log d'auditoria amb IDs per traçabilitat interna.
    NO s'envia a l'LLM — és per logs i debug.
    """
    lines = []
    stats = filtered["stats"]

    lines.append(f"=== AUDITORIA INSTRUCCIONS ===")
    lines.append(f"Perfils actius: {', '.join(stats['perfils_actius'])}")
    lines.append(f"MECR: {stats['mecr']} | DUA: {stats['dua']}")
    lines.append(f"Total instruccions: {stats['total_instruccions']} en {stats['total_macrodirectives']} macrodirectives")
    lines.append(f"Suprimides: {stats['suprimides']}")
    lines.append("")

    macros = filtered["macrodirectives"]
    sorted_macros = sorted(macros.items(), key=lambda x: x[1]["ordre"])

    for macro_id, macro in sorted_macros:
        ids = [i["id"] for i in macro["instruccions"]]
        lines.append(f"  {macro['label']} [{', '.join(ids)}] ({len(ids)} instr.)")

    if filtered["suppressed"]:
        lines.append(f"\n  SUPRIMIDES: {', '.join(filtered['suppressed'])}")

    return "\n".join(lines)
