"""Fase 0.7 - Test de la clau OpenRouter i discovery de models.

Objectius:
  1. Confirmar que OPENROUTER_API_KEY_2 (o similars) s'escullen be del .env
  2. Llistar models free disponibles a OpenRouter
  3. Fer una crida real amb el cas del castell medieval a un model Qwen

Us:
    PYTHONIOENCODING=utf-8 python scripts/test_openrouter.py
"""

import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

# Patro de rotacio igual que GEMMA4_API_KEYS
OPENROUTER_API_KEYS = [
    k for k in [os.getenv(f"OPENROUTER_API_KEY{s}", "")
                for s in ["", "_2", "_3", "_4", "_5", "_6", "_7"]] if k
]

print("=" * 70)
print("FASE 0.7 - Test OpenRouter")
print("=" * 70)
print(f"Claus OPENROUTER trobades: {len(OPENROUTER_API_KEYS)}")
for i, k in enumerate(OPENROUTER_API_KEYS):
    print(f"  [{i}] {k[:12]}...{k[-6:]} ({len(k)} char)")
print()

if not OPENROUTER_API_KEYS:
    print("ERROR: no hi ha cap OPENROUTER_API_KEY al .env", file=sys.stderr)
    print("       Prova OPENROUTER_API_KEY, OPENROUTER_API_KEY_2, etc.", file=sys.stderr)
    sys.exit(1)

# OpenRouter es OpenAI-compatible. Reutilitzem l'SDK OpenAI amb base_url.
try:
    from openai import OpenAI
except ImportError:
    print("ERROR: SDK 'openai' no instal\u00b7lat. pip install openai", file=sys.stderr)
    sys.exit(1)

KEY = OPENROUTER_API_KEYS[0]

# ── Test 1: discovery de models (llistar els disponibles) ────────────────
print("### Test 1: Llistar models disponibles a OpenRouter")
print("-" * 70)

import requests
try:
    r = requests.get(
        "https://openrouter.ai/api/v1/models",
        headers={"Authorization": f"Bearer {KEY}"},
        timeout=30,
    )
    if r.status_code == 200:
        data = r.json()
        models = data.get("data", [])
        print(f"Total models disponibles: {len(models)}")
        print()
        # Filtrar els que tenen ':free' al id (tier gratuit)
        free_models = [m for m in models if ":free" in m.get("id", "")]
        print(f"Models amb tier ':free': {len(free_models)}")
        print()
        # Filtrar els que contenen 'qwen' (majuscula/minuscula)
        qwen_models = [m for m in models if "qwen" in m.get("id", "").lower()]
        print(f"Models Qwen disponibles: {len(qwen_models)}")
        for m in qwen_models[:15]:
            mid = m.get("id", "")
            ctx = m.get("context_length", "?")
            pricing = m.get("pricing", {})
            prompt_cost = pricing.get("prompt", "?")
            marker = " [FREE]" if ":free" in mid else ""
            print(f"  - {mid}  (ctx={ctx}, prompt=${prompt_cost}){marker}")
    else:
        print(f"HTTP {r.status_code}: {r.text[:300]}")
        sys.exit(2)
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
    sys.exit(2)

print()

# ── Test 2: crida real al cas del castell amb el millor Qwen free ────────
print()
print("### Test 2: Crida al cas del castell amb un Qwen free")
print("-" * 70)

# Construim una llista de candidats en ordre de preferencia:
# 1. Primer els Qwen :free (gratis, pero sovint rate-limited)
# 2. Despres els Qwen 3.5-9B / 3.5-27B (equivalents al ranking Softcatala, preu ultra-baix)
# 3. Despres altres models open :free que podrien servir
candidates = []

# (1) Qwen :free, ordenats per "interes"
qwen_free = [m for m in models if "qwen" in m.get("id", "").lower() and ":free" in m.get("id", "")]
qwen_free.sort(
    key=lambda m: (
        "qwen3" in m["id"].lower(),
        "72b" in m["id"].lower() or "80b" in m["id"].lower(),
        "32b" in m["id"].lower() or "30b" in m["id"].lower(),
    ),
    reverse=True,
)
candidates.extend(m["id"] for m in qwen_free[:5])

# (2) Qwen pay-per-use ultra-baix (equivalents al ranking Softcatala)
qwen_paid_preferred = [
    "qwen/qwen3.5-9b",   # equivalent al model testat per Softcatala (52.4 index)
    "qwen/qwen3.5-27b",
    "qwen/qwen3.5-35b-a3b",
    "qwen/qwen3-next-80b-a3b-instruct",  # versio no-free del que ha fallat
]
for mid in qwen_paid_preferred:
    if any(m.get("id") == mid for m in models):
        candidates.append(mid)

# (3) Altres :free com a ultim recurs
other_free = [m for m in models if ":free" in m.get("id", "") and "qwen" not in m.get("id", "").lower()]
candidates.extend(m["id"] for m in other_free[:3])

print(f"Candidats a provar (en ordre): {len(candidates)}")
for i, c in enumerate(candidates[:10]):
    print(f"  {i+1}. {c}")
print()

SYSTEM_MINIM = (
    "Ets un redactor de materials escolars en catala. Escrius textos clars, "
    "ben estructurats, adequats a l'edat i al nivell indicats. Respectes "
    "exactament el genere, la tipologia, el to i la llargada que et demanen. "
    "Catala normatiu. Uses negretes per als termes clau i, si el tema ho "
    "permet, acabes amb una breu caixa de vocabulari al final. No inventes "
    "dades. Escriu directament el text, sense introduccions meta."
)

USER_CAS = (
    "Escriu un text del genere article divulgatiu, tipologia expositiva, "
    "de to neutre, d'aproximadament 400 paraules (llargada estandard), "
    "sobre: la vida a un castell medieval.\n\n"
    "Destinatari: alumnat de 5e de primaria, materia de Coneixement del medi."
)

client = OpenAI(
    api_key=KEY,
    base_url="https://openrouter.ai/api/v1",
)

def try_model(target: str) -> tuple[str, int, str | None]:
    """Retorna (text, ms, error_or_None)."""
    t0 = time.time()
    try:
        resp = client.chat.completions.create(
            model=target,
            messages=[
                {"role": "system", "content": SYSTEM_MINIM},
                {"role": "user", "content": USER_CAS},
            ],
            temperature=1.0,
            top_p=0.95,
            max_tokens=2048,
            extra_headers={
                "HTTP-Referer": "https://atne.fje.cat",
                "X-Title": "ATNE",
            },
        )
        text = resp.choices[0].message.content or ""
        ms = int((time.time() - t0) * 1000)
        return text, ms, None
    except Exception as e:
        ms = int((time.time() - t0) * 1000)
        return "", ms, f"{type(e).__name__}: {str(e)[:300]}"


winner = None
for target in candidates:
    print(f"Provant: {target}")
    text, ms, err = try_model(target)
    if err is None and text:
        print("─── TEXT ─────────────────────────────────────────────────────")
        print(text)
        print("─── FI ───────────────────────────────────────────────────────")
        print()
        print(f"Paraules: {len(text.split())}  |  Durada: {ms} ms")
        print(f"Model usat: {target}")
        print()
        print(">> OPENROUTER + QWEN FUNCIONA <<")
        winner = target
        break
    else:
        print(f"  ERROR ({ms} ms): {err}")
        print()

if not winner:
    print()
    print("ERROR: cap dels candidats ha respost. Revisa la clau o els cr\u00e8dits a OpenRouter.")
    sys.exit(4)

print()
print(f"Model guanyador: {winner}")
print("Aquest pot ser el model per defecte de l'alias 'qwen' al dispatcher ATNE.")
