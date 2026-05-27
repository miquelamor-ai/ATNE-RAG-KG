"""Actualitza `system_config` a Supabase per fixar:
- Tasques grans (adapt/generate/refine/adapt_flash) -> gpt-4o
- Tasques petites (complements/auditor/illustration_translate) -> gpt-4.1-mini

Decisio 2026-05-27: substituir Gemma 4 31B per GPT-4o a les fases criticas
despres que Gemma falles rigor UNE/MECR a A1 inicial nouvingut.

Usage:
    python scripts/set_models_gpt4o.py
"""
import os
import sys
import json
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "").rstrip("/")
SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SERVICE_KEY:
    print("ERROR: SUPABASE_URL o SUPABASE_SERVICE_KEY no configurats a .env")
    sys.exit(1)

HEADERS = {
    "apikey": SERVICE_KEY,
    "Authorization": f"Bearer {SERVICE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates,return=minimal",
}

# Mapeig de claus -> model (segons _ALLOWED_MODEL_KEYS a server.py)
NEW_CONFIG = {
    "atne_model_adapt":                  "gpt-4o",
    "atne_model_generate":               "gpt-4o",
    "atne_model_refine":                 "gpt-4o",
    "atne_model_adapt_flash":            "gpt-4o",
    "atne_model_complements":            "gpt-4.1-mini",
    "atne_model_auditor":                "gpt-4.1-mini",
    "atne_model_illustration_translate": "gpt-4.1-mini",
}

rows = [
    {
        "key": k,
        "value": {"mode": "fixed", "model": v, "set_by": "set_models_gpt4o.py"},
        "updated_by": "set_models_gpt4o.py",
    }
    for k, v in NEW_CONFIG.items()
]

print(f"[1/2] Llegint estat actual de system_config...")
r = requests.get(
    f"{SUPABASE_URL}/rest/v1/system_config?select=key,value",
    headers={"apikey": SERVICE_KEY, "Authorization": f"Bearer {SERVICE_KEY}"},
    timeout=10,
)
r.raise_for_status()
current = {row["key"]: row["value"] for row in r.json()}
print("\nEstat ABANS:")
for k in NEW_CONFIG:
    print(f"  {k}: {json.dumps(current.get(k, '(no existeix)'), ensure_ascii=False)}")

print(f"\n[2/2] UPSERT {len(rows)} files a Supabase...")
r = requests.post(
    f"{SUPABASE_URL}/rest/v1/system_config?on_conflict=key",
    headers=HEADERS,
    json=rows,
    timeout=15,
)
if r.status_code not in (200, 201, 204):
    print(f"ERROR HTTP {r.status_code}: {r.text[:500]}")
    sys.exit(2)

print("OK. Verificant estat NOU...")
r = requests.get(
    f"{SUPABASE_URL}/rest/v1/system_config?select=key,value",
    headers={"apikey": SERVICE_KEY, "Authorization": f"Bearer {SERVICE_KEY}"},
    timeout=10,
)
r.raise_for_status()
after = {row["key"]: row["value"] for row in r.json()}
print("\nEstat DESPRES:")
for k in NEW_CONFIG:
    print(f"  {k}: {json.dumps(after.get(k), ensure_ascii=False)}")

print("\nFet. Cal reiniciar el servidor (uvicorn / Cloud Run) perque carregui la nova config.")
