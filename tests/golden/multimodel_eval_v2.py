"""Validacio empirica MiMo Pro vs GPT-4o sobre 6 casos representatius.

Cobreix Pre-A1 → B2 amb perfils diversos (nouvingut, dislexia, TDAH,
discap. auditiva, AACC) per validar si MiMo v2.5 Pro és consistent o
si el bon resultat sobre `ex_l2` era sobreajustat.

Output: tests/golden/_multimodel_v2/{model}__{case}.json
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

OUTDIR = Path(__file__).parent / "_multimodel_v2"
OUTDIR.mkdir(exist_ok=True)

CASES_TO_TEST = [
    ("ex_inf",  "fotosintesi"),   # Pre-A1 conte (Infantil 5)
    ("ex_ci",   "fotosintesi"),   # A1 descripcio (1r Prim, dislexia)
    ("ex_l2",   "fotosintesi"),   # A2 descripcio (1r ESO, nouvingut)
    ("marc",    "fotosintesi"),   # B1 divulgatiu (3r ESO, TDAH)
    ("ex_aud",  "fotosintesi"),   # B1 entrevista (discap. auditiva)
    ("pol",     "fotosintesi"),   # B2 assaig (4t ESO, AACC)
]

MODELS_TO_TEST = [
    "gpt-4o",                # baseline premium actual
    "xiaomi/mimo-v2.5-pro",  # candidat
]

from adaptation.orchestrator import run_adaptation


def get_case(cid: str) -> dict:
    return next(c for c in cases_data["casos"] if c["id"] == cid)


def get_text(tid: str) -> str:
    return texts_data["textos"][tid]["text"]


print(f"\n{'='*72}")
print(f"= Validacio v2: {len(CASES_TO_TEST)} casos × {len(MODELS_TO_TEST)} models = {len(CASES_TO_TEST)*len(MODELS_TO_TEST)} adaptacions")
print(f"{'='*72}\n")

for case_id, text_id in CASES_TO_TEST:
    case = get_case(case_id)
    text = get_text(text_id)
    profile = case["profile"]
    params = case["params"]
    mecr = params.get("mecr_sortida", "?")
    genere = params.get("genere_discursiu", "?")
    dua = params.get("dua", "?")
    desc = case.get("descripcio", "")

    print(f"\n{'#'*72}")
    print(f"# CAS: {case_id} | {desc}")
    print(f"# MECR={mecr} | DUA={dua} | genere={genere}")
    print(f"{'#'*72}")

    for model in MODELS_TO_TEST:
        out_path = OUTDIR / f"{model.replace('/', '_').replace(':', '_')}__{case_id}.json"
        if out_path.exists():
            print(f"\n  [SKIP] Ja existeix: {out_path.name}")
            continue

        print(f"\n  === Model: {model} ===")
        events: list[dict] = []
        def cb(ev, _evs=events):
            _evs.append(ev)
            if ev.get("type") == "step":
                print(f"    [{ev.get('step')}] {ev.get('msg','')[:80]}", flush=True)
        try:
            run_adaptation(
                text=text,
                profile=profile,
                context={
                    "etapa": params.get("etapa", "ESO"),
                    "materia": "ciències naturals",
                },
                params=params,
                progress_callback=cb,
                model_override=model,
            )
            status = 200
        except Exception as e:
            events.append({"type": "error", "msg": f"{type(e).__name__}: {e}"})
            status = 500
            print(f"    ❌ ERROR: {e}")

        adapted = ""
        for ev in events:
            if ev.get("type") == "result":
                adapted = ev.get("adapted", "")
                break

        out = {
            "case_id": case_id,
            "case_desc": desc,
            "model": model,
            "mecr": mecr,
            "dua": dua,
            "genere": genere,
            "status": status,
            "adapted_len": len(adapted),
            "has_text_adaptat": "## Text adaptat" in adapted,
            "has_glossari": "## Glossari" in adapted,
            "has_bastides": "## Bastides" in adapted,
            "has_picto_marker": "[PICTO" in adapted,
            "has_picto_real": "arasaac" in adapted.lower(),
            "adapted": adapted,
        }
        out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"    ✅ {out_path.name}  len={len(adapted)}  ta={out['has_text_adaptat']}  pic={out['has_picto_real']}")

print("\n\nValidacio v2 completada.")
