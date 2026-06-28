"""
genres_catalog.py — Catàleg de gèneres discursius DERIVAT del corpusFJE.

Font única de veritat: les skills `write-*` (agent_role: adapter) sota
`corpus/external/corpusFJE/skills/generes/`. Afegir un gènere nou = afegir
una skill al corpus; ATNE l'hereta via submòdul. ATNE NO manté el catàleg
hardcoded (excepte el fallback degradat d'emergència).

Cada skill de gènere aporta al frontmatter: genre_key, label_ca, description,
macro_tipologia (família canònica única), mecr_range.

El catàleg es carrega un cop a l'arrencada (build_catalog) i es cacheja; només
canvia amb un bump del submòdul + redeploy.
"""

from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger("atne.genres")

# Ordre estable de les 7 famílies canòniques (macro_tipologia) per al selector.
# Fixat perquè el frontend no balli entre builds.
_FAMILY_ORDER = [
    "narrativa",
    "explicativa",
    "argumentativa",
    "instructiva",
    "conversacional",
    "descriptiva",
    "poetica",
]

# Fallback degradat (emergència): si el submòdul no carrega cap skill, el Pas 2
# mai queda sense selector. Mínim: genre_key + label_ca. Sense description rica.
_DEGRADED_GENRES = [
    {"genre_key": "manual", "label_ca": "Manual / capítol", "macro_tipologia": "explicativa"},
    {"genre_key": "divulgatiu", "label_ca": "Article divulgatiu", "macro_tipologia": "explicativa"},
    {"genre_key": "informe", "label_ca": "Informe / memòria", "macro_tipologia": "explicativa"},
    {"genre_key": "enciclopedic", "label_ca": "Definició enciclopèdica", "macro_tipologia": "explicativa"},
    {"genre_key": "descripcio", "label_ca": "Descripció", "macro_tipologia": "descriptiva"},
    {"genre_key": "resum", "label_ca": "Resum / síntesi", "macro_tipologia": "explicativa"},
    {"genre_key": "conte", "label_ca": "Conte / relat", "macro_tipologia": "narrativa"},
    {"genre_key": "fabula", "label_ca": "Fàbula / llegenda", "macro_tipologia": "narrativa"},
    {"genre_key": "poema", "label_ca": "Poema / vers", "macro_tipologia": "poetica"},
    {"genre_key": "biografia", "label_ca": "Biografia", "macro_tipologia": "narrativa"},
    {"genre_key": "noticia", "label_ca": "Notícia de premsa", "macro_tipologia": "narrativa"},
    {"genre_key": "cronica", "label_ca": "Crònica", "macro_tipologia": "narrativa"},
    {"genre_key": "diari", "label_ca": "Diari / blog", "macro_tipologia": "narrativa"},
    {"genre_key": "opinio", "label_ca": "Article d'opinió", "macro_tipologia": "argumentativa"},
    {"genre_key": "ressenya", "label_ca": "Ressenya / crítica", "macro_tipologia": "argumentativa"},
    {"genre_key": "assaig", "label_ca": "Assaig", "macro_tipologia": "argumentativa"},
    {"genre_key": "carta", "label_ca": "Carta / correu", "macro_tipologia": "argumentativa"},
    {"genre_key": "instruccions", "label_ca": "Instruccions (recepta / manual / protocol)", "macro_tipologia": "instructiva"},
    {"genre_key": "receptari", "label_ca": "Receptari", "macro_tipologia": "instructiva"},
    {"genre_key": "reglament", "label_ca": "Reglament / normes", "macro_tipologia": "instructiva"},
    {"genre_key": "entrevista", "label_ca": "Entrevista", "macro_tipologia": "conversacional"},
    {"genre_key": "dialeg", "label_ca": "Diàleg / guió teatral", "macro_tipologia": "conversacional"},
]

# Cache del catàleg (es construeix a l'arrencada via build_catalog()).
_CATALOG: dict | None = None


def _submodule_commit() -> str | None:
    """Llegeix el commit checkoutejat del submòdul corpusFJE (traçabilitat RIA).

    Llegeix .git/modules/corpus/external/corpusFJE/HEAD. Si és un ref simbòlic
    (ref: refs/...), el resol. Retorna el SHA o None si no es pot determinar.
    """
    try:
        here = Path(__file__).resolve().parent.parent
        gitdir = here / ".git" / "modules" / "corpus" / "external" / "corpusFJE"
        head = (gitdir / "HEAD").read_text(encoding="utf-8").strip()
        if head.startswith("ref:"):
            ref = head.split(":", 1)[1].strip()
            sha = (gitdir / ref).read_text(encoding="utf-8").strip()
            return sha or None
        return head or None
    except Exception:
        return None


def _build_genres_from_skills() -> list[dict]:
    """Deriva la llista plana de gèneres de les skills write-* del submòdul.

    Filtre: agent_role == "adapter" I la skill viu sota generes/.
    Exclou skills amb frontmatter incomplet (sense macro_tipologia o label_ca):
    el canon n'és l'amo i ha de completar-les abans d'entrar al catàleg.
    """
    import skills_loader

    skills = skills_loader.load_skills(skills_loader.default_skills_roots())
    genres = []
    for s in skills:
        if s.agent_role != "adapter":
            continue
        if "generes" not in s.path.parts:
            continue
        fm = s.frontmatter or {}
        macro = fm.get("macro_tipologia")
        label = fm.get("label_ca")
        if not macro or not label:
            logger.warning(
                "skill %s de gènere sense macro_tipologia/label_ca — exclosa",
                s.name,
            )
            continue
        genres.append({
            "genre_key": fm.get("genre_key") or s.name.replace("write-", ""),
            "label_ca": label,
            "description": (s.description or "").strip(),
            "macro_tipologia": macro,
            "mecr_range": fm.get("mecr_range") or [],
            "skill": s.name,
        })
    return genres


def build_catalog() -> dict:
    """Construeix (i cacheja) el catàleg de gèneres. Cridar a l'arrencada.

    Tolerant a errors: si el submòdul no carrega cap skill o peta, retorna el
    catàleg degradat hardcoded amb degraded=True (el Pas 2 mai queda sense selector).
    """
    global _CATALOG
    version = _submodule_commit()
    try:
        genres = _build_genres_from_skills()
    except Exception as e:
        logger.warning("error derivant el catàleg de gèneres (%s) — fallback degradat", e)
        genres = []

    if not genres:
        logger.warning("0 gèneres derivats del submòdul — catàleg DEGRADAT hardcoded")
        _CATALOG = {
            "ok": True,
            "degraded": True,
            "version": version,
            "total": len(_DEGRADED_GENRES),
            "generes": list(_DEGRADED_GENRES),
        }
    else:
        _CATALOG = {
            "ok": True,
            "degraded": False,
            "version": f"submodule:{version}" if version else None,
            "total": len(genres),
            "generes": genres,
        }
    return _CATALOG


def _ensure_loaded() -> dict:
    """Retorna el catàleg cachejat, construint-lo si encara no ho està."""
    if _CATALOG is None:
        return build_catalog()
    return _CATALOG


def _group_by_family(generes: list[dict]) -> list[dict]:
    """Agrupa els gèneres per macro_tipologia segons l'ordre canònic estable."""
    by_fam: dict[str, list] = {}
    for g in generes:
        by_fam.setdefault(g["macro_tipologia"], []).append(g)
    families = []
    # Famílies en l'ordre canònic; les desconegudes (si n'hi ha) al final, ordenades.
    seen = set()
    for fam in _FAMILY_ORDER:
        if fam in by_fam:
            families.append({"macro_tipologia": fam, "generes": by_fam[fam]})
            seen.add(fam)
    for fam in sorted(by_fam):
        if fam not in seen:
            families.append({"macro_tipologia": fam, "generes": by_fam[fam]})
    return families


def get_catalog(fmt: str = "grouped", refresh: bool = False) -> dict:
    """API pública del catàleg.

    fmt:
      - "grouped" (default): agrupat per família, per al <select> del Pas 2.
      - "flat": llista plana de gèneres, per al classificador (Peça B).
      - "keys": només els genre_key, per a validació ràpida.
    refresh: força reconstruir el catàleg (admin; el catàleg només canvia amb bump).
    """
    cat = build_catalog() if refresh else _ensure_loaded()
    base = {"ok": True, "degraded": cat["degraded"], "version": cat["version"], "total": cat["total"]}

    if fmt == "keys":
        return {**base, "genre_keys": [g["genre_key"] for g in cat["generes"]]}
    if fmt == "flat":
        return {**base, "generes": cat["generes"]}
    # grouped
    return {**base, "families": _group_by_family(cat["generes"])}
