"""Cache de transliteracions verificades per docents FJE.

Taula `atne_translits` a Supabase (migrations/2026-06-01_atne_translits.sql).

Decisió 31/05 (cross-check ATNE↔mineriaRAG):
  · corpusFJE = canon estable (regles per L1 a docs/transliteracio_standards_l1_2026-05-31.md)
  · Supabase BD = cache operatiu (terme × L1 → translit validada)

Flux esperat al pipeline glossari (A6):
  1. Abans de demanar la translit al LLM, fer lookup_batch() sobre els termes.
  2. Reutilitzar les translits verified=true sense crida LLM.
  3. Per als termes restants, demanar al LLM i fer store_translit(verified=False).
  4. Quan el docent corregeix al Pas 3, store_translit(verified=True, verified_by=email)
     via l'endpoint /api/translit/verify.

Política d'upsert (rellevant per a evitar regressions):
  · verified=True  → merge-duplicates (la versió humana sempre prevalèixer)
  · verified=False → ignore-duplicates (mai sobreescriure verified=true existent)
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Optional

import requests

logger = logging.getLogger(__name__)

# Timeouts conservadors — el cache és un best-effort optimization, no pot
# bloquejar el pipeline. Si Supabase no respon, caiem silenciosament i el
# LLM tornarà a generar (pitjor: una crida LLM addicional, no error visible).
_TIMEOUT_LOOKUP = 3.0
_TIMEOUT_STORE = 5.0


def _supabase_conf() -> tuple[str, dict]:
    """Retorna (URL, headers) llegits en temps de crida (no d'import).

    Mateix patró que routes/drafts.py per evitar dependència circular amb server.py
    i recollir canvis de runtime si l'admin actualitza credencials.
    """
    import server  # type: ignore  # lazy
    return server.SUPABASE_URL, server.SUPABASE_HEADERS


# ─────────────────────────────────────────────────────────────────────────────
# LOOKUP
# ─────────────────────────────────────────────────────────────────────────────

def lookup_translit(terme: str, l1: str) -> Optional[str]:
    """Retorna la transliteració verified=true per (terme, l1) si existeix.

    Retorna None si no existeix, si falla la crida o si Supabase no està
    configurat. L'absència de cache no és error: simplement el LLM la regenera.
    """
    if not terme or not l1:
        return None
    url, headers = _supabase_conf()
    if not url:
        return None
    try:
        resp = requests.get(
            f"{url}/rest/v1/atne_translits",
            headers=headers,
            params={
                "terme": f"eq.{terme}",
                "l1": f"eq.{l1}",
                "verified": "eq.true",
                "select": "transliteracio",
                "limit": "1",
            },
            timeout=_TIMEOUT_LOOKUP,
        )
        if resp.status_code == 200:
            data = resp.json()
            if data:
                return data[0].get("transliteracio")
    except Exception as e:
        logger.warning("translit_cache.lookup_translit failed (%r,%r): %s", terme, l1, e)
    return None


def lookup_batch(pairs: list[tuple[str, str]]) -> dict[tuple[str, str], str]:
    """Lookup batch — una sola crida HTTP per a múltiples termes.

    Args:
        pairs: llista de (terme, l1) a buscar.

    Returns:
        Dict {(terme, l1): translit} només amb les claus que existeixen verified=true.
        Diferència fonamental amb lookup_translit: pairs absents NO apareixen al dict.
    """
    if not pairs:
        return {}
    url, headers = _supabase_conf()
    if not url:
        return {}
    termes = sorted({t for t, _ in pairs if t})
    l1s = sorted({l for _, l in pairs if l})
    if not termes or not l1s:
        return {}
    try:
        # PostgREST in() accepta llistes separades per coma. Els termes amb comes
        # o cometes necessitarien escaping; els nostres termes són paraules
        # normals (no contenen `,` o `"`), però fem una neteja conservadora.
        def _safe(s: str) -> str:
            return s.replace(",", "").replace('"', "").replace("(", "").replace(")", "")
        termes_q = ",".join(_safe(t) for t in termes)
        l1s_q = ",".join(_safe(l) for l in l1s)
        resp = requests.get(
            f"{url}/rest/v1/atne_translits",
            headers=headers,
            params={
                "terme": f"in.({termes_q})",
                "l1": f"in.({l1s_q})",
                "verified": "eq.true",
                "select": "terme,l1,transliteracio",
            },
            timeout=_TIMEOUT_LOOKUP,
        )
        if resp.status_code == 200:
            return {(r["terme"], r["l1"]): r["transliteracio"] for r in resp.json()}
    except Exception as e:
        logger.warning("translit_cache.lookup_batch failed: %s", e)
    return {}


# ─────────────────────────────────────────────────────────────────────────────
# STORE
# ─────────────────────────────────────────────────────────────────────────────

def store_translit(
    terme: str,
    l1: str,
    transliteracio: str,
    estandard: Optional[str] = None,
    verified: bool = False,
    verified_by: Optional[str] = None,
) -> bool:
    """Desa o actualitza una entrada al cache.

    Política d'upsert:
      - verified=True  → merge-duplicates: la correcció humana sobreescriu sempre
        l'entrada existent (ja sigui LLM o versió humana anterior).
      - verified=False → ignore-duplicates: si ja existeix una entrada per
        (terme, l1), NO es toca. Així evitem regressions sobre una entrada
        verified=true (cas: dos generacions LLM consecutives amb diferent text).

    Returns:
        True si l'operació ha tingut èxit (HTTP 200/201/204), False altrament.
    """
    if not terme or not l1 or not transliteracio:
        return False
    url, headers = _supabase_conf()
    if not url:
        return False

    row: dict = {
        "terme": terme,
        "l1": l1,
        "transliteracio": transliteracio,
        "verified": bool(verified),
    }
    if estandard:
        row["estandard"] = estandard
    if verified:
        if verified_by:
            row["verified_by"] = verified_by
        row["verified_at"] = datetime.now(timezone.utc).isoformat()

    resolution = "merge-duplicates" if verified else "ignore-duplicates"
    try:
        # `on_conflict=terme,l1` indica a PostgREST quina UNIQUE constraint
        # gestionar; sense això el header Prefer no s'aplica i el server
        # retorna 409 davant duplicats (cas: dues generacions consecutives).
        resp = requests.post(
            f"{url}/rest/v1/atne_translits",
            headers={**headers, "Prefer": f"resolution={resolution},return=minimal"},
            params={"on_conflict": "terme,l1"},
            json=row,
            timeout=_TIMEOUT_STORE,
        )
        if resp.status_code in (200, 201, 204):
            return True
        logger.warning(
            "translit_cache.store HTTP %s for (%r,%r,verified=%s): %s",
            resp.status_code, terme, l1, verified, resp.text[:200],
        )
        return False
    except Exception as e:
        logger.warning("translit_cache.store_translit failed (%r,%r): %s", terme, l1, e)
        return False


def store_batch(rows: list[dict]) -> int:
    """Desa múltiples entrades en una sola crida HTTP.

    Args:
        rows: llista de dicts amb claus {terme, l1, transliteracio, estandard?, verified?, verified_by?}.

    Returns:
        Nombre d'entrades acceptades. 0 si fallada o llista buida.

    Nota: tots els rows del batch comparteixen la mateixa política de resolució.
    Per a mesclar verified=True i verified=False, fer 2 crides separades.
    """
    if not rows:
        return 0
    url, headers = _supabase_conf()
    if not url:
        return 0
    # Política: si TOTS són verified, merge; si TOTS són no-verified, ignore;
    # mixed → split en 2 crides (fora d'aquest helper).
    all_verified = all(r.get("verified") for r in rows)
    resolution = "merge-duplicates" if all_verified else "ignore-duplicates"
    # Normalitza files (afegeix verified_at als verified si falta)
    now_iso = datetime.now(timezone.utc).isoformat()
    payload = []
    for r in rows:
        if not r.get("terme") or not r.get("l1") or not r.get("transliteracio"):
            continue
        row = {
            "terme": r["terme"],
            "l1": r["l1"],
            "transliteracio": r["transliteracio"],
            "verified": bool(r.get("verified")),
        }
        if r.get("estandard"):
            row["estandard"] = r["estandard"]
        if r.get("verified"):
            if r.get("verified_by"):
                row["verified_by"] = r["verified_by"]
            row["verified_at"] = r.get("verified_at") or now_iso
        payload.append(row)
    if not payload:
        return 0
    try:
        resp = requests.post(
            f"{url}/rest/v1/atne_translits",
            headers={**headers, "Prefer": f"resolution={resolution},return=minimal"},
            params={"on_conflict": "terme,l1"},
            json=payload,
            timeout=_TIMEOUT_STORE * 2,
        )
        if resp.status_code in (200, 201, 204):
            return len(payload)
        logger.warning(
            "translit_cache.store_batch HTTP %s (%d rows): %s",
            resp.status_code, len(payload), resp.text[:200],
        )
        return 0
    except Exception as e:
        logger.warning("translit_cache.store_batch failed (%d rows): %s", len(payload), e)
        return 0
