"""
curriculum_reader.py — Lector del currículum LOMLOE (Decret 175/2022 · 21/2023
infantil) DERIVAT del corpusFJE, per al generador de textos (Fil 3, Sub-peça A).

Font única: corpus/external/corpusFJE/curriculum/ (canonitzat per mineraRAG).
ATNE NO manté el currículum; el llegeix del submòdul. Exposa:
  - materies(etapa)            → matèries amb sabers disponibles d'una etapa
  - sabers(etapa, materia, curs) → sabers (o àmbits, a infantil) filtrats pel curs

Nomenclatura 175/2022 (mai CI/CM/CS ni P3): PRI_C1/C2/C3, ESO_C1/C2, BAT_*,
infantil per àmbits (no sabers). El manifest.json indexa etapa→matèria→fitxer.

FASE 1: infantil, primària, ESO, batxillerat. FP queda per a la Fase 2 (estructura
família→cicle→mòdul diferent + manifest no la indexa encara).
"""

from __future__ import annotations

import json
import logging
import unicodedata
from pathlib import Path

logger = logging.getLogger("atne.curriculum")

_CURRICULUM_DIR = (
    Path(__file__).resolve().parent.parent
    / "corpus" / "external" / "corpusFJE" / "curriculum"
)

# ── Mapeig curs (Pas 1) → nivell_norm (currículum 175/2022) ──────────────
# El Pas 1 dona el curs individual; el currículum agrupa per cicle. Retornem la
# llista de nivells_norm candidats (batxillerat té matèries generals BAT_GEN que
# conviuen amb BAT_1R/BAT_2N → cal acceptar múltiples candidats al filtre).
def _nivells_norm_per_curs(etapa: str, curs: str) -> list[str]:
    e = (etapa or "").strip().lower()
    c = (curs or "").strip().lower()

    if e == "infantil":
        return []  # infantil no té sabers per nivell (tractament per àmbits)

    if "prim" in e:
        if any(x in c for x in ("1r", "1er", "2n", "primer", "segon")):
            return ["PRI_C1"]
        if any(x in c for x in ("3r", "3er", "4t", "4rt", "tercer", "quart")):
            return ["PRI_C2"]
        if any(x in c for x in ("5è", "5e", "6è", "6e", "cinqu", "sis")):
            return ["PRI_C3"]
        return ["PRI_C1", "PRI_C2", "PRI_C3"]  # desconegut → tots

    if "eso" in e:
        if "4t" in c or "4rt" in c or "quart" in c:
            return ["ESO_C2"]
        if any(x in c for x in ("1r", "1er", "2n", "3r", "3er", "primer", "segon", "tercer")):
            return ["ESO_C1"]
        return ["ESO_C1", "ESO_C2"]

    if "batx" in e:
        if "1r" in c or "1er" in c or "primer" in c:
            return ["BAT_1R", "BAT_GEN"]
        if "2n" in c or "segon" in c:
            return ["BAT_2N", "BAT_GEN"]
        return ["BAT_1R", "BAT_2N", "BAT_GEN"]

    return []


def _norm_etapa(etapa: str) -> str:
    """Normalitza l'etapa del Pas 1 a la clau del manifest (infantil/primaria/eso/batxillerat)."""
    e = (etapa or "").strip().lower()
    if "infantil" in e:
        return "infantil"
    if "prim" in e:
        return "primaria"
    if "eso" in e:
        return "eso"
    if "batx" in e:
        return "batxillerat"
    if e in ("fp", "formacio professional", "formació professional"):
        return "fp"  # fora d'abast Fase 1; materies() retornarà buit
    return e


# ── Cache ────────────────────────────────────────────────────────────────
_MANIFEST: dict | None = None
_FILE_CACHE: dict[str, dict] = {}   # path relatiu → json carregat


def _load_manifest() -> dict:
    global _MANIFEST
    if _MANIFEST is not None:
        return _MANIFEST
    try:
        p = _CURRICULUM_DIR / "manifest.json"
        _MANIFEST = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        logger.warning("no s'ha pogut carregar manifest.json (%s)", e)
        _MANIFEST = {}
    return _MANIFEST


def _load_file(etapa_key: str, materia_clau: str, fitxer: str) -> dict:
    rel = f"{etapa_key}/{materia_clau}/{fitxer}"
    if rel in _FILE_CACHE:
        return _FILE_CACHE[rel]
    try:
        data = json.loads((_CURRICULUM_DIR / rel).read_text(encoding="utf-8"))
    except Exception as e:
        logger.warning("no s'ha pogut carregar %s (%s)", rel, e)
        data = {}
    _FILE_CACHE[rel] = data
    return data


def build_cache() -> None:
    """Precarrega el manifest a l'arrencada (els fitxers de matèria van sota demanda)."""
    _load_manifest()


# ── API pública ──────────────────────────────────────────────────────────

def materies(etapa: str) -> list[dict]:
    """Matèries d'una etapa que tenen contingut curricular per oferir.

    Retorna [{clau, nom, codi}], ordenat per nom. Per a infantil retorna els
    «àmbits» com a matèries (tractament especial). Per a FP, buit (Fase 2).
    """
    etapa_key = _norm_etapa(etapa)
    mf = _load_manifest()
    sub = mf.get(etapa_key)
    if not isinstance(sub, dict) or not sub:
        return []

    # Infantil: no té matèries amb sabers; oferim els àmbits del segon cicle.
    if etapa_key == "infantil":
        items = sub.get("segon_cicle", [])
        # Infantil 21/2023: l'estructura és Àmbit → Àrea → ODA (objectiu) → blocs.
        # El "selector de matèria" d'infantil ofereix els OBJECTIUS (ODA), agrupats
        # per àmbit, perquè el docent triï l'objectiu a treballar.
        return objectius_infantil()

    # Primària/ESO/batxillerat: matèries amb te_sabers=True i no obsoletes.
    out = []
    for materia_clau, items in sub.items():
        if not isinstance(items, list):
            continue
        vig = _vigent_item(items)
        if vig and vig.get("te_sabers"):
            out.append({
                "clau": materia_clau,
                "nom": vig.get("area_materia") or materia_clau,
                "codi": vig.get("codi_area") or "",
                "tipus": "materia",
            })
    out.sort(key=lambda m: (m["nom"] or "").lower())
    return out


def sabers(etapa: str, materia_clau: str, curs: str) -> list[dict]:
    """Sabers d'una matèria+curs, per al selector del generador (primària/ESO/batx).

    Per a infantil NO s'usa aquesta funció: infantil té el seu model propi
    (objectius_infantil + continguts_infantil), perquè l'estructura és
    Àmbit→Àrea→ODA→blocs, no matèria→sabers.

    Resta d'etapes: sabers_items filtrats pels nivells_norm candidats del curs,
    agrupats per bloc/subapartat. Retorna [{bloc, subapartat, text, nivell_norm}].
    Mai llança: si no hi ha res, retorna llista buida.
    """
    etapa_key = _norm_etapa(etapa)
    mf = _load_manifest()
    sub = mf.get(etapa_key)
    if not isinstance(sub, dict):
        return []

    if etapa_key == "infantil":
        # Infantil: el "materia_clau" és el codi d'ODA → retorna els seus blocs.
        return continguts_infantil(materia_clau)

    items = sub.get(materia_clau)
    if not isinstance(items, list):
        return []
    vig = _vigent_item(items)
    if not vig:
        return []
    data = _load_file(etapa_key, materia_clau, vig["fitxer"])

    candidats = set(_nivells_norm_per_curs(etapa, curs))
    out = []
    for si in data.get("sabers_items", []):
        nn = si.get("nivell_norm")
        if candidats and nn not in candidats:
            continue
        out.append({
            "bloc": si.get("bloc", ""),
            "subapartat": si.get("subapartat", ""),
            "text": si.get("text", ""),
            "nivell_norm": nn,
        })
    return out


# ── Infantil (model propi: Àmbit → Àrea → ODA → blocs, decret 21/2023) ──────

def _infantil_data() -> dict:
    """Carrega el fitxer vigent (no-obsolet) del segon cicle d'infantil."""
    mf = _load_manifest()
    sub = mf.get("infantil")
    if not isinstance(sub, dict):
        return {}
    fitxer = _vigent(sub.get("segon_cicle", []))
    if not fitxer:
        return {}
    return _load_file("infantil", "segon_cicle", fitxer)


def objectius_infantil() -> list[dict]:
    """Objectius de Desenvolupament i Aprenentatge (ODA) d'infantil, per al primer
    selector. Agrupats per àmbit (el `nom` de l'àmbit fa de bloc al <optgroup>).

    Retorna [{clau: codi_ODA, nom: text_ODA, codi, tipus:'oda', ambit, area}].
    """
    data = _infantil_data()
    out = []
    for amb in data.get("ambits", []):
        amb_nom = amb.get("nom", "")
        for area in amb.get("arees", []):
            area_nom = area.get("nom", "")
            for oda in area.get("objectius_desenvolupament", []):
                out.append({
                    "clau": oda.get("codi", ""),
                    "nom": oda.get("text", ""),
                    "codi": oda.get("codi", ""),
                    "tipus": "oda",
                    "ambit": amb_nom,
                    "area": area_nom,
                })
    return out


def continguts_infantil(oda_codi: str) -> list[dict]:
    """Blocs de contingut d'un ODA concret (segon selector, múltiple opcional).

    Retorna [{bloc, subapartat, text, nivell_norm}] homogeni amb sabers():
      - `subapartat` = nom del bloc ("El cos i la pròpia imatge")
      - `text` = nom del bloc (el valor seleccionable; els ítems detallats es
        poden adjuntar com a context, però el bloc és la unitat de selecció)
    Si oda_codi és buit, retorna []. Mai llança.
    """
    if not oda_codi:
        return []
    data = _infantil_data()
    out = []
    for amb in data.get("ambits", []):
        for area in amb.get("arees", []):
            for oda in area.get("objectius_desenvolupament", []):
                if oda.get("codi") != oda_codi:
                    continue
                for b in oda.get("blocs_contingut", []):
                    items = b.get("items", [])
                    out.append({
                        "bloc": oda.get("text", "")[:60],
                        "subapartat": b.get("bloc", ""),
                        "text": b.get("bloc", ""),
                        "items": items,
                        "nivell_norm": "INF_2C",
                    })
    return out


# ── Helpers manifest ───────────────────────────────────────────────────────

def _vigent_item(items: list) -> dict | None:
    """De la llista d'items d'una matèria, retorna el no-obsolet (o el primer)."""
    if not items:
        return None
    for it in items:
        if not it.get("obsolet"):
            return it
    return items[0]


def _vigent(items: list) -> str:
    """Nom del fitxer no-obsolet (per a infantil, on els items no tenen materia_clau)."""
    it = _vigent_item(items)
    return it.get("fitxer", "") if it else ""


def _strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s or "") if not unicodedata.combining(c)).lower()
