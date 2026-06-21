"""
genre_detector.py — Detecció de gènere discursiu d'un text (Peça B, Gap 1).

Cascada de tres nivells, del més barat al més car:
  1. Heurística lleugera (sense LLM): marques formals inequívoques.
  2. Classificador LLM (gemini-2.5-flash-lite): tria dins el catàleg tancat.
  3. Fallback: gènere neutre "divulgatiu" si res resol amb prou confiança.

El catàleg de gèneres vàlids es llegeix de genres_catalog (derivat del corpusFJE),
no hardcoded: el prompt del classificador es construeix dinàmicament. Afegir un
gènere al canon → el detector el coneix sense tocar aquest codi.

Mai falla cap a l'usuari: qualsevol error (LLM caigut, JSON invàlid, al·lucinació
fora del catàleg) cau al fallback "divulgatiu".
"""

from __future__ import annotations

import json
import logging
import re

logger = logging.getLogger("atne.genre_detector")

# Decisió B.9: primeres 500 paraules (suficient >90% textos escolars).
_MAX_WORDS = 500
# Llindars de la cascada.
_HEURISTIC_MIN_CONF = 0.8
_LLM_MIN_CONF = 0.6
# Gènere neutre de fallback (ha d'existir al catàleg; és dels 22 base).
_FALLBACK_GENRE = "divulgatiu"
# Model per defecte (configurable via system_config.atne_model_detect_genre).
_DEFAULT_MODEL = "gemini-2.5-flash-lite"


def _truncate(text: str, max_words: int = _MAX_WORDS) -> str:
    words = (text or "").split()
    return " ".join(words[:max_words])


# ── Nivell 1: heurística lleugera ──────────────────────────────────────

def _heuristica(text: str) -> dict | None:
    """Retorna {genre_key, confianca, motiu} si una marca formal forta dispara
    inequívocament (cap altra la contradiu), o None per delegar a l'LLM."""
    t = text or ""
    low = t.lower()
    lines = [ln.strip() for ln in t.splitlines() if ln.strip()]
    n_lines = len(lines) or 1

    hits = []

    # Receptari: ingredients + elaboració/preparació
    if re.search(r"\bingredients\b", low) and re.search(r"\b(elaboraci|preparaci|pas\s*\d|passos)\b", low):
        hits.append(("receptari", 0.95, "ingredients + elaboració"))

    # Reglament: articles numerats o fórmules prescriptives
    if len(re.findall(r"\barticle\s+\d+", low)) >= 2 or re.search(r"\b(es prohibeix|queda establert|és obligatori|queda prohibit)\b", low):
        hits.append(("reglament", 0.9, "articles/prescripció"))

    # Carta: salutació + comiat
    has_salut = re.search(r"\b(benvolgut|benvolguda|estimat|estimada|apreciat|apreciada|distingit)\b", low)
    has_comiat = re.search(r"\b(atentament|cordialment|una salutació|ben cordialment|salutacions cordials)\b", low)
    if has_salut and has_comiat:
        hits.append(("carta", 0.9, "salutació + comiat"))

    # Poema: majoria de línies curtes amb salts regulars
    short_lines = sum(1 for ln in lines if len(ln) < 60)
    if n_lines >= 4 and short_lines / n_lines >= 0.6:
        hits.append(("poema", 0.85, "vers (línies curtes)"))

    # Entrevista: diàleg amb guió + patró pregunta/resposta
    dash_lines = sum(1 for ln in lines if ln.startswith("—") or ln.startswith("-"))
    if n_lines >= 4 and dash_lines / n_lines >= 0.4 and re.search(r"\?", t):
        hits.append(("entrevista", 0.8, "torns P/R amb guió"))

    # Instructiu: imperatius seqüencials + passos numerats, sense ingredients
    if re.search(r"^\s*\d+[\.\)]\s", t, re.MULTILINE) and not re.search(r"\bingredients\b", low):
        if re.search(r"\b(connecta|agafa|prem|premeu|munta|col·loca|talla|uneix|encén)\b", low):
            hits.append(("instructiu", 0.8, "passos imperatius numerats"))

    if not hits:
        return None
    # Si dues marques fortes diferents disparen → ambigu, deleguem a l'LLM.
    keys = {h[0] for h in hits}
    if len(keys) > 1:
        return None
    genre_key, conf, motiu = hits[0]
    if conf < _HEURISTIC_MIN_CONF:
        return None
    return {"genre_key": genre_key, "confianca": conf, "motiu": motiu}


# ── Nivell 2: classificador LLM ────────────────────────────────────────

def _build_llm_prompt(generes: list[dict]) -> str:
    """Construeix el system prompt del classificador a partir del catàleg viu."""
    linies = []
    for g in generes:
        desc = (g.get("description") or "").replace("\n", " ").strip()
        linies.append(f"- {g['genre_key']}: {desc}")
    cataleg = "\n".join(linies)
    return (
        "Ets un classificador de gènere discursiu per a textos educatius en català.\n"
        "Identifica a QUIN dels gèneres SEGÜENTS pertany el text. Tria EXACTAMENT UN\n"
        "valor de la clau (la paraula abans dels dos punts), o \"incert\" si no encaixa\n"
        "amb prou claredat.\n\n"
        "GÈNERES VÀLIDS:\n"
        f"{cataleg}\n\n"
        "REGLA: classifica pel gènere REAL del text, no pel tema. Un text sobre cuina\n"
        "que no és una recepta no és \"receptari\". Si dubtes, tria el més probable i\n"
        "baixa la confiança.\n\n"
        "Respon NOMÉS amb aquest JSON, sense cap text addicional:\n"
        '{"genere": "<clau o incert>", "confianca": <0.0-1.0>, "motiu": "<max 10 paraules>"}'
    )


def _parse_llm_json(raw: str) -> dict | None:
    """Parseig tolerant: extreu el JSON encara que vingui amb ```json o backticks."""
    if not raw:
        return None
    s = raw.strip()
    if "```json" in s:
        s = s.split("```json", 1)[1].split("```", 1)[0]
    elif "```" in s:
        s = s.split("```", 1)[1].split("```", 1)[0]
    s = s.strip()
    try:
        return json.loads(s)
    except Exception:
        # Últim recurs: primer objecte {...} de la cadena.
        m = re.search(r"\{.*\}", s, re.DOTALL)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                return None
    return None


def _resolve_detect_model() -> str:
    """Model del classificador: system_config.atne_model_detect_genre o default Flash Lite."""
    try:
        import server
        cfg = getattr(server, "_MODEL_CONFIG", {}) or {}
        entry = cfg.get("detect_genre")
        if isinstance(entry, dict):
            return entry.get("model") or _DEFAULT_MODEL
        if isinstance(entry, str) and entry:
            return entry
    except Exception:
        pass
    return _DEFAULT_MODEL


def _classifica_llm(text: str, generes: list[dict], valid_keys: set) -> dict | None:
    """Crida el LLM i retorna {genre_key, confianca, motiu} validat, o None."""
    try:
        from adaptation.llm_clients import _call_llm_raw
    except Exception as e:
        logger.warning("no es pot importar _call_llm_raw (%s)", e)
        return None

    system_prompt = _build_llm_prompt(generes)
    user_text = f"TEXT A CLASSIFICAR:\n\n{text}"
    model = _resolve_detect_model()
    try:
        raw = _call_llm_raw(model, system_prompt, user_text, temperature=0.0, max_tokens=120)
    except Exception as e:
        logger.warning("classificador LLM ha fallat (%s)", e)
        return None

    data = _parse_llm_json(raw)
    if not isinstance(data, dict):
        return None
    genere = data.get("genere")
    if genere not in valid_keys:
        # "incert" o al·lucinació fora del catàleg → confiança insuficient.
        return None
    try:
        conf = float(data.get("confianca"))
    except (TypeError, ValueError):
        conf = 0.0
    return {"genre_key": genere, "confianca": conf, "motiu": (data.get("motiu") or "")[:120]}


# ── Cascada pública ────────────────────────────────────────────────────

def detect_genre(text: str, lang: str = "ca") -> dict:
    """Detecta el gènere discursiu d'un text via cascada heurística → LLM → fallback.

    Retorna sempre un dict (mai llança):
      {ok, genere, label_ca, confianca, origen, motiu}
      origen ∈ {"heuristica", "llm", "fallback"}
    """
    from adaptation import genres_catalog
    flat = genres_catalog.get_catalog("flat")
    generes = flat.get("generes", [])
    valid_keys = {g["genre_key"] for g in generes}
    label_by_key = {g["genre_key"]: g.get("label_ca", "") for g in generes}

    text_curt = _truncate(text)

    def _resposta(genre_key, confianca, origen, motiu):
        return {
            "ok": True,
            "genere": genre_key,
            "label_ca": label_by_key.get(genre_key, ""),
            "confianca": confianca,
            "origen": origen,
            "motiu": motiu,
        }

    # Text massa curt per classificar → fallback directe.
    if len((text or "").split()) < 40:
        return _resposta(_FALLBACK_GENRE, None, "fallback", "text massa curt per classificar")

    # Nivell 1: heurística (defensiva: una regla mal formada no ha de tombar la cascada)
    try:
        h = _heuristica(text_curt)
    except Exception as e:
        logger.warning("heurística ha fallat (%s) — es delega a l'LLM", e)
        h = None
    if h and h["genre_key"] in valid_keys:
        return _resposta(h["genre_key"], h["confianca"], "heuristica", h["motiu"])

    # Nivell 2: LLM (defensiva: qualsevol error de la crida → fallback, mai crash)
    try:
        r = _classifica_llm(text_curt, generes, valid_keys)
    except Exception as e:
        logger.warning("classificador LLM ha llançat (%s) — fallback", e)
        r = None
    if r and r["confianca"] >= _LLM_MIN_CONF:
        return _resposta(r["genre_key"], r["confianca"], "llm", r["motiu"])

    # Nivell 3: fallback
    return _resposta(_FALLBACK_GENRE, None, "fallback", "no determinat amb prou confiança")
