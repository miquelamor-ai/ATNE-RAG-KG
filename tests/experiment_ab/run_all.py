#!/usr/bin/env python3
"""
Xat 9 — Orquestrador: llança generació + avaluació + anàlisi en seqüència.
Ús: python tests/experiment_ab/run_all.py [--skip-gen] [--skip-eval] [--only-stats]
"""
import subprocess, sys, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXP_DIR = Path(__file__).resolve().parent
os.chdir(ROOT)

def run(script_name, desc):
    print(f"\n{'='*60}")
    print(f"▶ {desc}")
    print(f"{'='*60}\n")
    result = subprocess.run(
        [sys.executable, str(EXP_DIR / script_name)],
        cwd=str(ROOT),
    )
    if result.returncode != 0:
        print(f"\n❌ {script_name} ha fallat amb codi {result.returncode}")
        sys.exit(1)
    print(f"\n✅ {desc} — completat")

args = sys.argv[1:]

if "--only-stats" not in args:
    if "--skip-gen" not in args:
        run("experiment_ab.py", "Pas 1/3: Generació de 180 parells A/B")
    if "--skip-eval" not in args:
        run("eval_experiment.py", "Pas 2/3: Avaluació dual (GPT-4o + Claude Sonnet)")

run("stats_experiment.py", "Pas 3/3: Anàlisi estadística + informe")

print(f"\n{'='*60}")
print("🏁 TOT COMPLETAT")
print(f"{'='*60}")
print(f"Resultats generació: {EXP_DIR / 'resultats_generacio.json'}")
print(f"Resultats avaluació: {EXP_DIR / 'resultats_avaluacio.json'}")
print(f"Informe: {EXP_DIR / 'informe_resultats.md'}")
