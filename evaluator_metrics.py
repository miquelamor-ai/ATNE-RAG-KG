"""
evaluator_metrics.py — BLOC 1 (Retrieval) + BLOC 2 (Forma).

Tot en Python, zero tokens LLM.
Referencia: docs/decisions/avaluacio_agent_v2.md

BLOC 1 - Retrieval Recall:
  Quantes instruccions del Gold Standard (PROFILE_INSTRUCTION_MAP) s'han enviat?
  Precision = 1.0 per disseny (el filtre nomes envia instruccions pertinents).

BLOC 2 - Faithfulness de forma:
  F1: Longitud mitjana de frase dins rang MECR
  F2: Presencia de titols/subtitols
  F3: Negretes en termes tecnics
  F4: Llistes
  F5: Prellico present
"""

import re
from instruction_catalog import PROFILE_INSTRUCTION_MAP

# ═══════════════════════════════════════════════════════════════════════════════
# BLOC 1 — RETRIEVAL
# ═══════════════════════════════════════════════════════════════════════════════

def retrieval_recall(profile_keys: list[str], instructions_sent: list[str]) -> dict:
    """
    Calcula el Recall: instruccions esperades vs enviades.

    Args:
        profile_keys: perfils actius (ex: ["nouvingut", "dislexia"])
        instructions_sent: IDs d'instruccions enviades (ex: ["A-01", "A-02", ...])

    Returns:
        dict amb recall, expected, actual, absents
    """
    expected = set()
    for pkey in profile_keys:
        profile_map = PROFILE_INSTRUCTION_MAP.get(pkey, {})
        for priority_group in profile_map.values():
            expected.update(priority_group)

    actual = set(instructions_sent)

    if not expected:
        return {
            "recall": 1.0,
            "expected_count": 0,
            "sent_count": len(actual),
            "absents": [],
        }

    present = expected & actual
    absents = sorted(expected - actual)

    return {
        "recall": round(len(present) / len(expected), 3),
        "expected_count": len(expected),
        "sent_count": len(actual),
        "matched_count": len(present),
        "absents": absents,
    }


def extract_instruction_ids(filtered_result: dict) -> list[str]:
    """
    Extreu els IDs d'instruccions d'un resultat d'instruction_filter.get_instructions().

    Cada linia te format "A-01: text..." — extraiem el prefix abans del ':'.
    """
    ids = []
    for group in ("sempre", "nivell", "perfil", "perfil_condicional", "complement"):
        for line in filtered_result.get(group, []):
            match = re.match(r"^([A-Z]-\d+):", line)
            if match:
                ids.append(match.group(1))
    return ids


# ═══════════════════════════════════════════════════════════════════════════════
# BLOC 2 — FORMA
# ═══════════════════════════════════════════════════════════════════════════════

# Rangs de paraules per frase segons MECR
MECR_RANGES = {
    "pre-A1": (3, 5),
    "A1": (5, 8),
    "A2": (8, 12),
    "B1": (12, 18),
    "B2": (18, 25),
}


def _split_sentences(text: str) -> list[str]:
    """Divideix text en frases (per punt, signe d'exclamacio o interrogacio)."""
    # Eliminar blocs de codi, titols i linies buides
    lines = []
    in_code = False
    for line in text.split("\n"):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if line.strip().startswith("#"):
            continue
        if line.strip().startswith("- ") or line.strip().startswith("| "):
            continue
        if line.strip():
            lines.append(line.strip())

    text_clean = " ".join(lines)
    # Dividir per . ! ? (ignorant punts en numeros com 1.5)
    sentences = re.split(r'(?<=[.!?])\s+', text_clean)
    # Filtrar frases buides o molt curtes (menys de 2 paraules)
    return [s for s in sentences if len(s.split()) >= 2]


def f1_sentence_length(text: str, mecr: str) -> float:
    """F1: Proporcio de frases dins del rang MECR."""
    sentences = _split_sentences(text)
    if not sentences:
        return 0.0

    min_w, max_w = MECR_RANGES.get(mecr, (5, 25))
    in_range = sum(1 for s in sentences if min_w <= len(s.split()) <= max_w)
    return round(in_range / len(sentences), 3)


def f2_headings(text: str) -> int:
    """F2: Presencia de titols/subtitols (## o ###)."""
    return 1 if re.search(r"^#{1,4}\s+\S", text, re.MULTILINE) else 0


def f3_bold_terms(text: str) -> int:
    """F3: Presencia de negretes en termes tecnics."""
    bold_matches = re.findall(r"\*\*[^*]+\*\*", text)
    return 1 if len(bold_matches) >= 2 else 0  # minim 2 negretes


def f4_lists(text: str) -> int:
    """F4: Presencia de llistes (- o 1.)."""
    return 1 if re.search(r"^[\s]*[-*]\s+\S|^\s*\d+\.\s+\S", text, re.MULTILINE) else 0


def f5_prelesson(text: str) -> int:
    """F5: Prellico present (glossari previ o organitzador)."""
    # Buscar bloc de "Paraules clau", "Glossari", "Abans de llegir", "Objectius"
    patterns = [
        r"##\s*(Paraules|Mots)\s*(clau|important)",
        r"##\s*Glossari",
        r"##\s*Abans\s*de\s*llegir",
        r"##\s*Objectius",
        r"##\s*Qu[eè]\s*aprend",
        r"\*\*Paraules clau\*\*",
    ]
    for pat in patterns:
        if re.search(pat, text, re.IGNORECASE):
            return 1
    return 0


def evaluate_forma(text: str, mecr: str) -> dict:
    """
    Avalua les 5 metriques de forma. Retorna dict amb F1-F5 i puntuacio global.
    """
    f1 = f1_sentence_length(text, mecr)
    f2 = f2_headings(text)
    f3 = f3_bold_terms(text)
    f4 = f4_lists(text)
    f5 = f5_prelesson(text)

    puntuacio = round((f1 + f2 + f3 + f4 + f5) / 5, 3)

    return {
        "F1_longitud_frase": f1,
        "F2_titols": f2,
        "F3_negretes": f3,
        "F4_llistes": f4,
        "F5_prellico_present": f5,
        "puntuacio_forma": puntuacio,
        "detall_f1": {
            "frases_totals": len(_split_sentences(text)),
            "mecr": mecr,
            "rang": MECR_RANGES.get(mecr, (5, 25)),
        },
    }


# ═══════════════════════════════════════════════════════════════════════════════
# AVALUACIO COMPLETA BLOC 1+2
# ═══════════════════════════════════════════════════════════════════════════════

def evaluate_blocs_1_2(
    text_adaptat: str,
    mecr: str,
    profile_keys: list[str],
    filtered_result: dict,
) -> dict:
    """
    Executa BLOC 1 (Retrieval) + BLOC 2 (Forma) i retorna resultats consolidats.

    Args:
        text_adaptat: el text generat pel model
        mecr: nivell MECR de sortida (ex: "A1")
        profile_keys: perfils actius (ex: ["nouvingut"])
        filtered_result: output d'instruction_filter.get_instructions()
    """
    # BLOC 1
    sent_ids = extract_instruction_ids(filtered_result)
    retrieval = retrieval_recall(profile_keys, sent_ids)

    # BLOC 2
    forma = evaluate_forma(text_adaptat, mecr)

    return {
        "retrieval": retrieval,
        "forma": forma,
        "filter_stats": filtered_result.get("stats", {}),
    }
