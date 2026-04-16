"""Fase 1 validation - test end-to-end del modul generador_lliure.

Crida directament generador_lliure.generar() amb el cas del castell
per comprovar tot el pipeline: prompt building + agent + _call_llm_raw +
resposta estructurada.

Us:
    PYTHONIOENCODING=utf-8 python scripts/test_generador_e2e.py [model]

model pot ser: gemma4 (default), gemma3, qwen, gpt-4o-mini, mistral-small, etc.
"""

import sys
import time
from pathlib import Path

# Fem que l'script trobi server.py i generador_lliure/ al parent dir.
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Import del m\u00f2dul ATNE. Ha d'anar primer perqu\u00e8 carregui .env i claus.
import server  # noqa: F401
from generador_lliure import generar

MODELS_A_PROVAR = sys.argv[1:] if len(sys.argv) > 1 else ["gemma4"]

PAYLOAD_BASE = {
    "tema": "la vida a un castell medieval",
    "genere": "article divulgatiu",
    "tipologia": "expositiva",
    "to": "neutre",
    "extensio": "estandard",
    "context": {
        "curs": "5è",
        "etapa": "primària",
        "materia": "Coneixement del medi",
    },
}

for model in MODELS_A_PROVAR:
    print("=" * 70)
    print(f"MODEL: {model}")
    print("=" * 70)
    payload = dict(PAYLOAD_BASE)
    payload["model"] = model
    t0 = time.time()
    try:
        result = generar(payload)
    except Exception as e:
        ms = int((time.time() - t0) * 1000)
        print(f"ERROR ({ms} ms): {type(e).__name__}: {str(e)[:300]}")
        continue
    total_ms = int((time.time() - t0) * 1000)
    print("─── TEXT ──────────────────────────────────────────────────────")
    print(result["text"])
    print("─── FI ────────────────────────────────────────────────────────")
    print()
    print(f"Paraules: {result['paraules']}  |  Target: {result.get('target_words', '?')}")
    print(f"Model usat: {result['model']}")
    print(f"Durada model: {result['duration_ms']} ms  |  Total: {total_ms} ms")
    print()
