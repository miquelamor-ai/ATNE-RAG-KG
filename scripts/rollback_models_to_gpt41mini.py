"""Rollback temporal: torna les 4 keys d'adaptacio a gpt-4.1-mini.

Motivacio 2026-06-01: el cross-check de rubrica.json (mineriaRAG) ha
trobat 2 issues critics (Q1 transversals.format_output h2_exact absent
als 38 skills + bug parser determinista) que afecten qualsevol model
adapter. Mentre no es resol, mantenim el model conegut (gpt-4.1-mini,
estat previ al switch a MiMo Pro) per reduir risc al pilot real.

Quan els 4 issues estiguin resolts al rubrica, re-executar
set_models_mimo_pro.py per tornar al pla validat.

Usage:
    python scripts/rollback_models_to_gpt41mini.py
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

NEW_CONFIG = {
    "atne_model_adapt":                  "gpt-4.1-mini",
    "atne_model_generate":               "gpt-4.1-mini",
    "atne_model_refine":                 "gpt-4.1-mini",
    "atne_model_adapt_flash":            "gpt-4.1-mini",
    "atne_model_complements":            "gpt-4.1-mini",
    "atne_model_auditor":                "gpt-4.1-mini",
    "atne_model_illustration_translate": "gpt-4.1-mini",
}

rows = [
    {
        "key": k,
        "value": {"mode": "fixed", "model": v, "set_by": "rollback_models_to_gpt41mini.py"},
        "updated_by": "rollback_models_to_gpt41mini.py",
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
print("\nEstat ABANS (rollback):")
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
print("\nEstat DESPRES (post-rollback):")
for k in NEW_CONFIG:
    print(f"  {k}: {json.dumps(after.get(k), ensure_ascii=False)}")

print("\nRollback fet. Cal reiniciar el servidor.")
print("Quan els 4 issues rubrica.json es resolguin: re-executar set_models_mimo_pro.py.")
