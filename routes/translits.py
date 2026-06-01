"""Endpoints de transliteracions verificades.

Taula `atne_translits` a Supabase (veure migrations/2026-06-01_atne_translits.sql).
Decisió 31/05 (cross-check ATNE↔mineriaRAG): corpusFJE = canon (regles per L1);
Supabase BD = cache operatiu (terme × L1 → translit validada).

Contracte mínim (A6 fase preparatòria — pre-publicació rubrica.json):
    POST   /api/translits/verify    — el docent valida/corregeix una translit del glossari

Endpoints addicionals previstos per a A6 complet (post-rubrica.json):
    GET    /api/translits/lookup    — lookup HTTP (avui el backend usa directament translit_cache)
    GET    /api/translits/recent    — entrades verified=false per a panel admin

La lògica viu a adaptation/translit_cache.py (mòdul Python reutilitzable pel pipeline).
"""

from __future__ import annotations

from fastapi import APIRouter, Body, Request
from fastapi.responses import JSONResponse

from adaptation.translit_cache import store_translit


router = APIRouter(prefix="/api/translits", tags=["translits"])


@router.post("/verify")
async def verify_translit(request: Request, payload: dict = Body(...)):
    """El docent confirma o corregeix una transliteració del glossari.

    Body esperat:
        {
          "terme": "كتاب",
          "l1": "ar",
          "transliteracio": "kitab",
          "estandard": "ALA-LC simplificat"   (opcional)
        }

    Identitat docent: derivada de `request.state.user_login` (login Supabase
    Google OAuth @fje.edu validat al middleware). El client NO l'envia.

    Política:
      - L'UPSERT marca l'entrada com `verified=true` amb `verified_by`+`verified_at`.
      - Si ja existia una entrada verified=true diferent, la versió més recent
        guanya (merge-duplicates) — la correcció humana sempre prevalèixer.
      - Per a invalidar una entrada verified=true, cal un endpoint separat
        (futura tasca: PATCH /api/translits/{id}/invalidate).

    Returns:
        200 {ok, verified_by} si OK; 400/401/503 en error.
    """
    terme = (payload.get("terme") or "").strip()
    l1 = (payload.get("l1") or "").strip()
    translit = (payload.get("transliteracio") or "").strip()
    estandard = (payload.get("estandard") or "").strip() or None

    if not terme or not l1 or not translit:
        return JSONResponse(
            {"ok": False, "error": "terme, l1 i transliteracio són obligatoris"},
            status_code=400,
        )

    # Sanity check a la mida (evita atacs DoS amb camps gegants).
    if len(terme) > 200 or len(l1) > 32 or len(translit) > 200:
        return JSONResponse(
            {"ok": False, "error": "valor massa llarg (terme/translit ≤200 chars, l1 ≤32)"},
            status_code=400,
        )

    login = (getattr(request.state, "user_login", "") or "").strip()
    if not login:
        return JSONResponse(
            {"ok": False, "error": "No autenticat"},
            status_code=401,
        )

    ok = store_translit(
        terme=terme,
        l1=l1,
        transliteracio=translit,
        estandard=estandard,
        verified=True,
        verified_by=login,
    )
    if not ok:
        return JSONResponse(
            {"ok": False, "error": "Error desant al cache de transliteracions"},
            status_code=503,
        )

    return {"ok": True, "verified_by": login}
