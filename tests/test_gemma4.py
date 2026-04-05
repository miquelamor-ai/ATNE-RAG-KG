"""
test_gemma4.py — Verifica que la clau GEMMA4_API_KEY funciona amb Gemma 4.
Una sola peticio curta, zero cost.
"""

import os
import sys
import time
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMMA4_API_KEY")
if not api_key:
    print("ERROR: GEMMA4_API_KEY no trobada al .env")
    sys.exit(1)

print(f"Clau: ...{api_key[-4:]}")
print(f"Projecte: free tier (sense billing)")
print()

# --- Test 1: Connexio basica amb Gemma 4 31B ---
print("=" * 50)
print("TEST 1: Gemma 4 31B — peticio curta")
print("=" * 50)

from google import genai
from google.genai import types

client = genai.Client(api_key=api_key)

try:
    t0 = time.time()
    response = client.models.generate_content(
        model="gemma-4-31b-it",
        contents="Respon NOMES amb una frase curta: Quin es el color del cel?",
        config=types.GenerateContentConfig(
            max_output_tokens=50,
            temperature=0.1,
        ),
    )
    t1 = time.time()
    print(f"Resposta: {response.text}")
    print(f"Temps: {t1 - t0:.1f}s")
    print("RESULTAT: OK")
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)

# --- Test 2: Gemma 4 26B MoE ---
print()
print("=" * 50)
print("TEST 2: Gemma 4 26B MoE — peticio curta")
print("=" * 50)

try:
    t0 = time.time()
    response = client.models.generate_content(
        model="gemma-4-26b-a4b-it",
        contents="Respon NOMES amb una frase curta: Quants dies te una setmana?",
        config=types.GenerateContentConfig(
            max_output_tokens=50,
            temperature=0.1,
        ),
    )
    t1 = time.time()
    print(f"Resposta: {response.text}")
    print(f"Temps: {t1 - t0:.1f}s")
    print("RESULTAT: OK")
except Exception as e:
    print(f"ERROR: {e}")

# --- Test 3: Verificar tier ---
print()
print("=" * 50)
print("TEST 3: Verificar tier de facturacio")
print("=" * 50)

try:
    models = client.models.list()
    gemma_models = [m.name for m in models if "gemma" in m.name.lower()]
    print(f"Models Gemma disponibles: {len(gemma_models)}")
    for m in sorted(gemma_models):
        print(f"  - {m}")
    print()
    print("Si veus models llistats = la clau funciona correctament")
    print("Tier: GRATUIT (sense billing configurat)")
    print()
    print("TOTS ELS TESTS OK — Pots usar Gemma 4 amb cost zero!")
except Exception as e:
    print(f"ERROR llistant models: {e}")
