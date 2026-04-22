"""Endpoints de biblioteca d'adaptacions del Pas 3.

Taula `atne_adaptations` a Supabase (veure migrations/2026-04-22_adaptations.sql).
Desa el resultat FINAL del Pas 3 (HTML adaptat + imatges + edicions) per
permetre al docent recuperar el treball des d'un altre dispositiu o dies
després.

Diferència amb `routes/drafts.py`:
  - drafts → text ORIGINAL del Pas 2 (abans d'adaptar)
  - adaptations → estat FINAL del Pas 3 (amb imatges, edicions, etc.)

Contracte (4 endpoints):
    POST   /api/adaptations              — desa o actualitza (si `id` al body)
    GET    /api/adaptations              — llista per docent_id
    GET    /api/adaptations/{id}         — recupera una adaptació completa
    DELETE /api/adaptations/{id}         — esborra
"""

import requests
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse


router = APIRouter(prefix="/api/adaptations", tags=["adaptations"])


def _err(msg: str, code: int = 503) -> JSONResponse:
    return JSONResponse({"ok": False, "error": msg}, status_code=code)


def _supabase_conf() -> tuple[str, dict]:
    """Llegeix URL/headers de Supabase al moment de la crida."""
    import server
    return server.SUPABASE_URL, server.SUPABASE_HEADERS


@router.post("")
async def save_adaptation(payload: dict = Body(...)):
    """Desa una adaptacio nova o actualitza una d'existent.

    Body: {
      docent_id,
      adapted_html,
      title?, original_text?,
      profile_snapshot?, context_snapshot?, complements_snapshot?,
      multinivell_versions?,
      id?  # si present → UPDATE; si no → INSERT
    }
    Retorna: {ok, id, updated_at}
    """
    SUPABASE_URL, SUPABASE_HEADERS = _supabase_conf()
    docent_id = (payload.get("docent_id") or "").strip()
    adapted_html = payload.get("adapted_html") or ""
    if not docent_id:
        return _err("docent_id buit", 400)
    if not adapted_html.strip():
        return _err("adapted_html buit", 400)

    adaptation_id = payload.get("id")
    row = {
        "docent_id": docent_id,
        "adapted_html": adapted_html,
        "title": payload.get("title") or None,
        "original_text": payload.get("original_text") or None,
        "profile_snapshot": payload.get("profile_snapshot"),
        "context_snapshot": payload.get("context_snapshot"),
        "complements_snapshot": payload.get("complements_snapshot"),
        "multinivell_versions": payload.get("multinivell_versions"),
        "updated_at": "now()",
    }

    try:
        if adaptation_id:
            # UPDATE — verifica que pertany al docent
            resp = requests.patch(
                f"{SUPABASE_URL}/rest/v1/atne_adaptations"
                f"?id=eq.{adaptation_id}&docent_id=eq.{docent_id}",
                headers={**SUPABASE_HEADERS, "Prefer": "return=representation"},
                json=row,
                timeout=10,
            )
            if resp.status_code in (200, 204):
                data = resp.json() if resp.text else []
                if not data:
                    return _err("Adaptacio no trobada o no autoritzada", 404)
                return {"ok": True, "id": data[0]["id"], "updated_at": data[0].get("updated_at")}
            print(f"[ATNE] adaptations PATCH failed: {resp.status_code} {resp.text[:200]}")
            return _err(resp.text or f"Supabase HTTP {resp.status_code}")
        else:
            # INSERT — deixa que el DEFAULT posi created_at/updated_at
            row.pop("updated_at", None)
            resp = requests.post(
                f"{SUPABASE_URL}/rest/v1/atne_adaptations",
                headers={**SUPABASE_HEADERS, "Prefer": "return=representation"},
                json=row,
                timeout=10,
            )
            if resp.status_code in (200, 201):
                data = resp.json()
                if not data:
                    return _err("Supabase retorna array buit")
                return {"ok": True, "id": data[0]["id"], "updated_at": data[0].get("updated_at")}
            print(f"[ATNE] adaptations POST failed: {resp.status_code} {resp.text[:200]}")
            return _err(resp.text or f"Supabase HTTP {resp.status_code}")
    except Exception as e:
        print(f"[ATNE] adaptations POST exception: {e}")
        return _err(str(e) or type(e).__name__)


@router.get("")
async def list_adaptations(docent_id: str = "", limit: int = 50):
    """Llista les adaptacions del docent (per a la biblioteca).

    Retorna {ok, items: [{id, title, profile_snapshot, context_snapshot,
    updated_at, created_at, preview}]}. `preview` = primers 200 chars
    d'adapted_html sense tags per fer-ne thumb text.
    """
    SUPABASE_URL, SUPABASE_HEADERS = _supabase_conf()
    docent_id = (docent_id or "").strip()
    if not docent_id:
        return _err("docent_id buit", 400)
    try:
        limit = max(1, min(int(limit), 200))
    except Exception:
        limit = 50
    try:
        resp = requests.get(
            f"{SUPABASE_URL}/rest/v1/atne_adaptations"
            f"?select=id,title,profile_snapshot,context_snapshot,"
            f"complements_snapshot,adapted_html,created_at,updated_at"
            f"&docent_id=eq.{docent_id}"
            f"&order=updated_at.desc&limit={limit}",
            headers=SUPABASE_HEADERS,
            timeout=10,
        )
        if resp.status_code == 200:
            import re
            items = []
            for row in resp.json():
                html = row.get("adapted_html") or ""
                # Strip HTML tags i trunca a 200 chars per preview
                text = re.sub(r"<[^>]+>", " ", html)
                text = re.sub(r"\s+", " ", text).strip()
                items.append({
                    "id": row.get("id"),
                    "title": row.get("title"),
                    "profile_snapshot": row.get("profile_snapshot"),
                    "context_snapshot": row.get("context_snapshot"),
                    "complements_snapshot": row.get("complements_snapshot"),
                    "preview": text[:200],
                    "created_at": row.get("created_at"),
                    "updated_at": row.get("updated_at"),
                })
            return {"ok": True, "items": items}
        print(f"[ATNE] adaptations GET failed: {resp.status_code} {resp.text[:200]}")
        return _err(resp.text or f"Supabase HTTP {resp.status_code}")
    except Exception as e:
        print(f"[ATNE] adaptations GET exception: {e}")
        return _err(str(e) or type(e).__name__)


@router.get("/{adaptation_id}")
async def get_adaptation(adaptation_id: int, docent_id: str = ""):
    """Recupera una adaptacio completa (amb tot l'estat)."""
    SUPABASE_URL, SUPABASE_HEADERS = _supabase_conf()
    docent_id = (docent_id or "").strip()
    if not docent_id:
        return _err("docent_id buit", 400)
    try:
        resp = requests.get(
            f"{SUPABASE_URL}/rest/v1/atne_adaptations"
            f"?select=*"
            f"&id=eq.{adaptation_id}&docent_id=eq.{docent_id}",
            headers=SUPABASE_HEADERS,
            timeout=10,
        )
        if resp.status_code == 200:
            data = resp.json()
            if not data:
                return _err("Adaptacio no trobada", 404)
            return {"ok": True, "item": data[0]}
        print(f"[ATNE] adaptations GET one failed: {resp.status_code} {resp.text[:200]}")
        return _err(resp.text or f"Supabase HTTP {resp.status_code}")
    except Exception as e:
        print(f"[ATNE] adaptations GET one exception: {e}")
        return _err(str(e) or type(e).__name__)


@router.delete("/{adaptation_id}")
async def delete_adaptation(adaptation_id: int, docent_id: str = ""):
    """Esborra una adaptacio (verifica docent_id)."""
    SUPABASE_URL, SUPABASE_HEADERS = _supabase_conf()
    docent_id = (docent_id or "").strip()
    if not docent_id:
        return _err("docent_id buit", 400)
    try:
        resp = requests.delete(
            f"{SUPABASE_URL}/rest/v1/atne_adaptations"
            f"?id=eq.{adaptation_id}&docent_id=eq.{docent_id}",
            headers={**SUPABASE_HEADERS, "Prefer": "return=minimal"},
            timeout=10,
        )
        if resp.status_code in (200, 204):
            return {"ok": True}
        print(f"[ATNE] adaptations DELETE failed: {resp.status_code} {resp.text[:200]}")
        return _err(resp.text or f"Supabase HTTP {resp.status_code}")
    except Exception as e:
        print(f"[ATNE] adaptations DELETE exception: {e}")
        return _err(str(e) or type(e).__name__)
