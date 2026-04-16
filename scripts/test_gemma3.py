"""Fase 0.6 - Test de gemma-3-12b-it amb les claus actuals.

Softcatala ha publicat un ranking de qualitat en catala: Gemma 3-12B
tries millor que Gemma 4 en gramatica (0.332 vs 0.183 - 1.8x millor)
i en index agregat (51.6 vs 49.9). Si les claus GEMMA4_API_KEY actuals
serveixen tambe per a Gemma 3-12B, es un canvi d'una linia al modul.

Aquest script prova el mateix cas del castell amb gemma-3-12b-it per
comprovar (a) que el model es accesible, (b) si la qualitat en catala
millora realment i (c) si els errors tipics de Gemma 4 (fosse,
menjavaient, etc.) desapareixen.

Us:
    PYTHONIOENCODING=utf-8 python scripts/test_gemma3.py
"""

import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

from google import genai
from google.genai import types

# Mateixes claus que usem per a Gemma 4
GEMMA4_API_KEYS = [
    k for k in [os.getenv(f"GEMMA4_API_KEY{s}", "")
                for s in ["", "_2", "_3", "_4", "_5", "_6", "_7"]] if k
]
# Tambe provem GEMINI_API_KEY per si Gemma 3 nomes funciona amb clau Gemini
GEMINI_API_KEYS = [
    k for k in [os.getenv(f"GEMINI_API_KEY{s}", "")
                for s in ["", "_3", "_4", "_5", "_6", "_7"]] if k
]

print("=" * 70)
print("FASE 0.6 - Test de gemma-3-12b-it")
print("=" * 70)
print(f"Claus GEMMA4 disponibles: {len(GEMMA4_API_KEYS)}")
print(f"Claus GEMINI disponibles: {len(GEMINI_API_KEYS)}")
print()

# Mateix prompt que a la Fase 0.5
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

full_prompt = f"{SYSTEM_MINIM}\n\n---\n\n{USER_CAS}"

# Llista de (nom_clau, clau, model) per provar - rotacio de totes les claus
tests = []
for i, k in enumerate(GEMMA4_API_KEYS):
    tests.append((f"GEMMA4_API_KEY[{i}]", k, "gemma-3-12b-it"))
for i, k in enumerate(GEMINI_API_KEYS):
    tests.append((f"GEMINI_API_KEY[{i}]", k, "gemma-3-12b-it"))

if not tests:
    print("ERROR: no hi ha cap clau d'API al .env", file=sys.stderr)
    sys.exit(1)

for key_name, key, model in tests:
    print(f"\n### Intent: model={model}  clau={key_name}")
    print("-" * 70)
    client = genai.Client(api_key=key, http_options=types.HttpOptions(timeout=180_000))
    t0 = time.time()
    try:
        response = client.models.generate_content(
            model=model,
            contents=[types.Content(role="user", parts=[types.Part(text=full_prompt)])],
            config=types.GenerateContentConfig(
                temperature=1.0,
                top_p=0.95,
                max_output_tokens=2048,
            ),
        )
        text = response.text or ""
        ms = int((time.time() - t0) * 1000)
        print(text)
        print("-" * 70)
        print(f"OK: {len(text.split())} paraules en {ms} ms amb {key_name}")
        print(f">> gemma-3-12b-it FUNCIONA amb {key_name} <<")
        break  # primera clau que funcioni, parem
    except Exception as e:
        ms = int((time.time() - t0) * 1000)
        print(f"ERROR ({ms} ms): {type(e).__name__}: {str(e)[:300]}")
        continue

print()
print("=" * 70)
print("GATE: si el text es clarament millor (menys errors, millor catala),")
print("canviem el model del modul nou a gemma-3-12b-it.")
print("Si es igual o pitjor, ens quedem amb gemma-4-31b-it.")
