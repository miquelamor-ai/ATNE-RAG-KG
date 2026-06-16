"""
tests/golden/multimodel_test.py — Test empíric multi-model

Compara el mateix cas (ex_l2 A1 nouvingut) adaptat amb 3 models adapter
diferents per veure si el model és el factor que determina el respecte
a les regles MALL.

Output: tests/golden/_multimodel/{model}.json per cada model
"""
from __future__ import annotations
import json, sys, os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

import yaml
cases_data = yaml.safe_load(open(ROOT / "tests/golden/cases.yaml", encoding="utf-8"))
texts_data = yaml.safe_load(open(ROOT / "tests/golden/golden_texts.yaml", encoding="utf-8"))

case = next(c for c in cases_data["casos"] if c["id"] == "ex_l2")
text = texts_data["textos"]["fotosintesi"]["text"]

OUTDIR = Path(__file__).parent / "_multimodel"
OUTDIR.mkdir(exist_ok=True)

MODELS_TO_TEST = [
    "gemma-4-31b-it",                       # baseline: default actual ATNE
    "gpt-4o",                               # baseline premium: adapter actual
    "xiaomi/mimo-v2.5-pro",                 # candidat principal — $0.435/$0.87, reasoning, 1M ctx
    "xiaomi/mimo-v2.5",                     # variant no-Pro, més barata
    "qwen/qwen3-235b-a22b:free",            # multilingüe fort (201 llengües, català inclòs)
    "deepseek/deepseek-chat-v3-0324:free",  # cost mínim baseline
]

from adaptation.orchestrator import run_adaptation

for model in MODELS_TO_TEST:
    print(f"\n{'='*60}\n=== Model: {model} ===\n{'='*60}")
    events: list[dict] = []
    def cb(ev, _evs=events):
        _evs.append(ev)
        if ev.get("type") == "step":
            print(f"  [{ev.get('step')}] {ev.get('msg','')[:90]}", flush=True)
    try:
        run_adaptation(
            text=text,
            profile=case["profile"],
            context={
                "etapa": case["params"].get("etapa", "ESO"),
                "materia": "ciències naturals",
            },
            params=case["params"],
            progress_callback=cb,
            model_override=model,
        )
        status = 200
    except Exception as e:
        events.append({"type": "error", "msg": f"{type(e).__name__}: {e}"})
        status = 500
        print(f"  ❌ ERROR: {e}")

    # Extreu adapted
    adapted = ""
    for ev in events:
        if ev.get("type") == "result":
            adapted = ev.get("adapted", "")
            break

    out = {
        "case_id": "ex_l2",
        "model": model,
        "status": status,
        "adapted_len": len(adapted),
        "has_text_adaptat": "## Text adaptat" in adapted,
        "has_glossari": "## Glossari" in adapted,
        "has_bastides": "## Bastides" in adapted,
        "has_picto_marker": "[PICTO" in adapted,
        "has_picto_real": "arasaac" in adapted.lower(),
        "events_count": len(events),
        "adapted": adapted,
    }
    out_path = OUTDIR / f"{model.replace('/', '_').replace(':', '_')}.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  ✅ Desat: {out_path.name}  adapted_len={len(adapted)}  "
          f"text_adaptat={out['has_text_adaptat']}  picto_real={out['has_picto_real']}")

print("\n\nTest multi-model completat.")
