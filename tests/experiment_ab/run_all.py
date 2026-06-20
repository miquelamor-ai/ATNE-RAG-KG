#!/usr/bin/env python3
"""
Peça 4 — Orquestrador: generació (skills OFF/ON) + avaluació (Sonnet 4.6) + anàlisi.
Ús: python tests/experiment_ab/run_all.py [--skip-gen] [--skip-eval] [--only-stats]
"""
import subprocess, sys, os, io
from pathlib import Path

# Fix Windows console encoding (consola cp1252 no pot imprimir ▶/✅/❌).
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parent.parent.parent
EXP_DIR = Path(__file__).resolve().parent
os.chdir(ROOT)

# Garanteix UTF-8 també als subprocessos (els fills ja blinden stdout, però el
# print() del subprocés hereta l'encoding de l'entorn si no es força).
os.environ["PYTHONIOENCODING"] = "utf-8"

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
        run("experiment_ab.py", "Pas 1/3: Generació 5 casos × (skills OFF/ON) amb Gemini Lite")
    if "--skip-eval" not in args:
        run("eval_experiment.py", "Pas 2/3: Avaluació amb Claude Sonnet 4.6 (jutge únic)")

run("stats_experiment.py", "Pas 3/3: Anàlisi descriptiva + informe")

print(f"\n{'='*60}")
print("🏁 TOT COMPLETAT")
print(f"{'='*60}")
print(f"Resultats generació: {EXP_DIR / 'resultats_generacio.json'}")
print(f"Resultats avaluació: {EXP_DIR / 'resultats_avaluacio.json'}")
print(f"Informe: {EXP_DIR / 'informe_resultats.md'}")
