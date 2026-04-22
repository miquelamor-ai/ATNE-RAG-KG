"""Endpoints d'esborranys (drafts) del Pas 2.

Taula `atne_drafts` a Supabase (veure migrations/2026-04-19_drafts.sql). Permet
al docent desar al servidor el text del Pas 2 abans d'adaptar-lo, de manera
que no es perdi en canviar de navegador/dispositiu.

Contracte (5 endpoints, extret de server.py al refactor 2026-04-21):
    POST   /api/drafts              — desa o actualitza (si `id` al body)
    GET    /api/drafts              — llista per docent_id
    GET    /api/drafts/{draft_id}   — recupera un draft complet
    DELETE /api/drafts/{draft_id}   — esborra
    PATCH  /api/drafts/{draft_id}   — variant PATCH amb camps parcials
"""

import requests
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse


router = APIRouter(prefix="/api/drafts", tags=["drafts"])


def _drafts_error(msg: str) -> JSONResponse:
    """Resposta uniforme d'error 503 per a endpoints de drafts."""
    return JSONResponse({"ok": False, "error": msg}, status_code=503)


def _supabase_conf() -> tuple[str, dict]:
    """Retorna (URL, headers) llegits en temps de crida, no d'import.

    Aixo permet que server.py arrenqui aquest mòdul abans de llegir les vars
    d'entorn i que, si l'admin canvia alguna cosa al runtime, ho agafem.
    """
    # Import perezos per evitar dependencia circular amb server.py
    import server
    return server.SUPABASE_URL, server.SUPABASE_HEADERS


@router.post("")
async def save_draft(payload: dict = Body(...)):
    """Desa un esborrany nou o actualitza un d'existent.

    Body: {docent_id, profile_id?, title?, text, materia?, nivell?, id?}
    Si `id` present → UPDATE; altrament INSERT. Retorna {ok, id, updated_at}.
    """
    SUPABASE_URL, SUPABASE_HEADERS = _supabase_conf()
    docent_id = (payload.get("docent_id") or "").strip()
    text = payload.get("text") or ""
    if not docent_id:
        return JSONResponse({"ok": False, "error": "docent_id buit"}, status_code=400)
    if not text or not text.strip():
        return JSONResponse({"ok": False, "error": "text buit"}, status_code=400)

    draft_id = payload.get("id")
    # Camps acceptats (whitelist). updated_at el posem sempre a now() des del servidor.
    row = {
        "docent_id": docent_id,
        "text": text,
        "profile_id": payload.get("profile_id") or None,
        "title": payload.get("title") or None,
        "materia": payload.get("materia") or None,
        "nivell": payload.get("nivell") or None,
        "updated_at": "now()",
    }

    try:
        if draft_id:
            # UPDATE: cal verificar que el draft pertany al docent (evitem
            # que un docent_id foraster pugui modificar drafts d'un altre).
            resp = requests.patch(
                f"{SUPABASE_URL}/rest/v1/atne_drafts?id=eq.{draft_id}&docent_id=eq.{docent_id}",
                headers={**SUPABASE_HEADERS, "Prefer": "return=representation"},
                json=row,
                timeout=10,
            )
            if resp.status_code in (200, 204):
                data = resp.json() if resp.text else []
                if not data:
                    return JSONResponse(
                        {"ok": False, "error": "Draft no trobat o no autoritzat"},
                        status_code=404,
                    )
                return {"ok": True, "id": data[0]["id"], "updated_at": data[0].get("updated_at")}
            print(f"[ATNE] drafts PATCH failed: {resp.status_code} {resp.text[:200]}")
            return _drafts_error(resp.text or f"Supabase HTTP {resp.status_code}")
        else:
            # INSERT: created_at/updated_at els posa el default de la taula.
            # Traiem `updated_at=now()` del row perquè el DEFAULT ja funciona.
            row.pop("updated_at", None)
            resp = requests.post(
                f"{SUPABASE_URL}/rest/v1/atne_drafts",
                headers={**SUPABASE_HEADERS, "Prefer": "return=representation"},
                json=row,
                timeout=10,
            )
            if resp.status_code in (200, 201):
                data = resp.json()
                if not data:
                    return _drafts_error("Supabase retorna array buit")
                return {"ok": True, "id": data[0]["id"], "updated_at": data[0].get("updated_at")}
            print(f"[ATNE] drafts POST failed: {resp.status_code} {resp.text[:200]}")
            return _drafts_error(resp.text or f"Supabase HTTP {resp.status_code}")
    except Exception as e:
        print(f"[ATNE] drafts POST exception: {e}")
        return _drafts_error(str(e) or type(e).__name__)


@router.get("")
async def list_drafts(docent_id: str = "", limit: int = 20):
    """Llista els esborranys del docent (ordenats per updated_at DESC).

    Retorna {ok, items: [{id, profile_id, title, text_preview, materia, nivell,
    created_at, updated_at}]}. `text_preview` = primers 200 caràcters del text.
    """
    SUPABASE_URL, SUPABASE_HEADERS = _supabase_conf()
    docent_id = (docent_id or "").strip()
    if not docent_id:
        return JSONResponse({"ok": False, "error": "docent_id buit"}, status_code=400)
    # Cap per dalt al límit per evitar abusos (mateix esperit que /api/history).
    try:
        limit = max(1, min(int(limit), 100))
    except Exception:
        limit = 20
    try:
        resp = requests.get(
            f"{SUPABASE_URL}/rest/v1/atne_drafts"
            f"?select=id,profile_id,title,text,materia,nivell,created_at,updated_at"
            f"&docent_id=eq.{docent_id}"
            f"&order=updated_at.desc&limit={limit}",
            headers=SUPABASE_HEADERS,
            timeout=10,
        )
        if resp.status_code == 200:
            items = []
            for row in resp.json():
                txt = row.get("text") or ""
                items.append({
                    "id": row.get("id"),
                    "profile_id": row.get("profile_id"),
                    "title": row.get("title"),
                    "text_preview": txt[:200],
                    "materia": row.get("materia"),
                    "nivell": row.get("nivell"),
                    "created_at": row.get("created_at"),
                    "updated_at": row.get("updated_at"),
                })
            return {"ok": True, "items": items}
        print(f"[ATNE] drafts GET failed: {resp.status_code} {resp.text[:200]}")
        return _drafts_error(resp.text or f"Supabase HTTP {resp.status_code}")
    except Exception as e:
        print(f"[ATNE] drafts GET exception: {e}")
        return _drafts_error(str(e) or type(e).__name__)


@router.get("/{draft_id}")
async def get_draft(draft_id: int, docent_id: str = ""):
    """Recupera un draft complet. Verifica que `docent_id` coincideix (evita
    accés creuat entre docents que comparteixen la mateixa instància d'ATNE).
    """
    SUPABASE_URL, SUPABASE_HEADERS = _supabase_conf()
    docent_id = (docent_id or "").strip()
    if not docent_id:
        return JSONResponse({"ok": False, "error": "docent_id buit"}, status_code=400)
    try:
        resp = requests.get(
            f"{SUPABASE_URL}/rest/v1/atne_drafts"
            f"?select=id,profile_id,title,text,materia,nivell,created_at,updated_at"
            f"&id=eq.{draft_id}&docent_id=eq.{docent_id}",
            headers=SUPABASE_HEADERS,
            timeout=10,
        )
        if resp.status_code == 200:
            data = resp.json()
            if not data:
                return JSONResponse(
                    {"ok": False, "error": "Draft no trobat"},
                    status_code=404,
                )
            return {"ok": True, "item": data[0]}
        print(f"[ATNE] drafts GET one failed: {resp.status_code} {resp.text[:200]}")
        return _drafts_error(resp.text or f"Supabase HTTP {resp.status_code}")
    except Exception as e:
        print(f"[ATNE] drafts GET one exception: {e}")
        return _drafts_error(str(e) or type(e).__name__)


@router.delete("/{draft_id}")
async def delete_draft(draft_id: int, docent_id: str = ""):
    """Esborra un draft. Verifica `docent_id` igual que GET/one."""
    SUPABASE_URL, SUPABASE_HEADERS = _supabase_conf()
    docent_id = (docent_id or "").strip()
    if not docent_id:
        return JSONResponse({"ok": False, "error": "docent_id buit"}, status_code=400)
    try:
        resp = requests.delete(
            f"{SUPABASE_URL}/rest/v1/atne_drafts?id=eq.{draft_id}&docent_id=eq.{docent_id}",
            headers={**SUPABASE_HEADERS, "Prefer": "return=minimal"},
            timeout=10,
        )
        if resp.status_code in (200, 204):
            return {"ok": True}
        print(f"[ATNE] drafts DELETE failed: {resp.status_code} {resp.text[:200]}")
        return _drafts_error(resp.text or f"Supabase HTTP {resp.status_code}")
    except Exception as e:
        print(f"[ATNE] drafts DELETE exception: {e}")
        return _drafts_error(str(e) or type(e).__name__)


@router.patch("/{draft_id}")
async def patch_draft(draft_id: int, payload: dict = Body(...)):
    """Variant PATCH (alias de POST amb id). Mateixa lògica: accepta camps
    parcials i només actualitza els enviats. Requereix `docent_id` al body.
    """
    SUPABASE_URL, SUPABASE_HEADERS = _supabase_conf()
    docent_id = (payload.get("docent_id") or "").strip()
    if not docent_id:
        return JSONResponse({"ok": False, "error": "docent_id buit"}, status_code=400)
    update: dict = {}
    for field in ("title", "text", "profile_id", "materia", "nivell"):
        if field in payload:
            update[field] = payload[field]
    if not update:
        return JSONResponse({"ok": False, "error": "Cap camp conegut al payload"}, status_code=400)
    update["updated_at"] = "now()"
    try:
        resp = requests.patch(
            f"{SUPABASE_URL}/rest/v1/atne_drafts?id=eq.{draft_id}&docent_id=eq.{docent_id}",
            headers={**SUPABASE_HEADERS, "Prefer": "return=representation"},
            json=update,
            timeout=10,
        )
        if resp.status_code in (200, 204):
            data = resp.json() if resp.text else []
            if not data:
                return JSONResponse(
                    {"ok": False, "error": "Draft no trobat o no autoritzat"},
                    status_code=404,
                )
            return {"ok": True, "id": data[0]["id"], "updated_at": data[0].get("updated_at")}
        print(f"[ATNE] drafts PATCH failed: {resp.status_code} {resp.text[:200]}")
        return _drafts_error(resp.text or f"Supabase HTTP {resp.status_code}")
    except Exception as e:
        print(f"[ATNE] drafts PATCH exception: {e}")
        return _drafts_error(str(e) or type(e).__name__)
