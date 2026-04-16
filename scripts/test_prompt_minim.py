"""Validacio Fase 0.5 del modul generador_lliure.

Actualitzacio del test inicial: aplica els defaults reals de Google AI Studio
(temp=1.0, top_p=0.95) i prova 3 variants de thinking mode per veure si
Gemma 4 31B suporta raonament intern via l'SDK google.genai.

Principi rector: no inventar parametres. Replicar exactament el que AI Studio
usa per defecte i veure si aixi obtenim qualitat equivalent o superior.

Us:
    PYTHONIOENCODING=utf-8 python scripts/test_prompt_minim.py
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

GEMMA4_API_KEYS = [
    k for k in [os.getenv(f"GEMMA4_API_KEY{s}", "")
                for s in ["", "_2", "_3", "_4", "_5", "_6", "_7"]] if k
]
if not GEMMA4_API_KEYS:
    print("ERROR: no s'ha trobat cap GEMMA4_API_KEY al .env", file=sys.stderr)
    sys.exit(1)

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

client = genai.Client(
    api_key=GEMMA4_API_KEYS[0],
    http_options=types.HttpOptions(timeout=180_000),
)


def run_variant(label: str, thinking_config):
    """Executa una variant i retorna (text, ms, error)."""
    config_kwargs = {
        "temperature": 1.0,
        "top_p": 0.95,
        "max_output_tokens": 2048,
    }
    if thinking_config is not None:
        config_kwargs["thinking_config"] = thinking_config

    t0 = time.time()
    try:
        response = client.models.generate_content(
            model="gemma-4-31b-it",
            contents=[types.Content(role="user", parts=[types.Part(text=full_prompt)])],
            config=types.GenerateContentConfig(**config_kwargs),
        )
        text = response.text or ""
        ms = int((time.time() - t0) * 1000)
        return text, ms, None
    except Exception as e:
        ms = int((time.time() - t0) * 1000)
        return "", ms, f"{type(e).__name__}: {e}"


variants = [
    ("A", "sense thinking_config (default SDK)", None),
    ("B", "thinking_budget=-1 (dinamic)",
     types.ThinkingConfig(thinking_budget=-1) if hasattr(types, "ThinkingConfig") else None),
    ("C", "thinking_budget=2048 (alt)",
     types.ThinkingConfig(thinking_budget=2048) if hasattr(types, "ThinkingConfig") else None),
]

print("=" * 70)
print("FASE 0.5 - Test amb defaults AI Studio + variants de thinking mode")
print("=" * 70)
print(f"Model: gemma-4-31b-it")
print(f"Temperature: 1.0")
print(f"Top P: 0.95")
print(f"Max output tokens: 2048")
print(f"Entrada: {len(full_prompt.split())} paraules")
print("=" * 70)
print()

results = []
for label, desc, tc in variants:
    print(f"\n### VARIANT {label}: {desc}")
    print("-" * 70)
    text, ms, err = run_variant(label, tc)
    if err:
        print(f"ERROR: {err}")
        results.append((label, desc, None, ms, err))
        continue
    print(text)
    print("-" * 70)
    print(f"Paraules: {len(text.split())}  |  Durada: {ms} ms")
    results.append((label, desc, text, ms, None))

print()
print("=" * 70)
print("RESUM")
print("=" * 70)
for label, desc, text, ms, err in results:
    if err:
        print(f"  {label}  [{desc}]: ERROR ({err[:80]})")
    else:
        nw = len(text.split())
        print(f"  {label}  [{desc}]: {nw} paraules, {ms} ms")
print()
print("GATE: compara visualment les variants entre si i amb el text d'Arena.")
print("  Guanyador = configuracio que passa al modul nou. Zero tuning mes.")
