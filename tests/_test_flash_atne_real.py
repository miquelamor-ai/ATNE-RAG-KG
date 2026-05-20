"""Test comparatiu cec amb prompt REAL d'ATNE (catàleg complet + complements).

Usa build_system_prompt() i _call_llm() del codi de producció. Compara:
  - Gemma 4 31B (baseline actual)
  - Gemini 2.5 Flash
  - Gemini 2.5 Flash-Lite

Perfil: alumne TDAH + dislèxia, 2n ESO, MECR B1, DUA Core
Complements: glossari + preguntes_comprensio + esquema_visual
"""
import json
import time
import sys
import os

# Ens cal carregar .env perquè _call_llm trobi les claus
from pathlib import Path
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())

# Ara els imports d'ATNE
sys.path.insert(0, str(Path(__file__).parent.parent))
from adaptation.prompt_builder import build_system_prompt
from adaptation.llm_clients import _call_llm

# ────────────────────────────────────────────────────────────────────────────
# Perfil real: TDAH + dislèxia, 2n ESO, B1
# Format compatible amb build_system_prompt (caracteristiques.{key}.actiu)
# ────────────────────────────────────────────────────────────────────────────
PROFILE = {
    "nom": "Marc TDAH+dislèxia",
    "profile_type": "alumne",
    "caracteristiques": {
        "tdah": {
            "actiu": True,
            "tipus": "combinat",
            "intensitat": "moderada",
        },
        "dislexia": {
            "actiu": True,
            "intensitat": "moderada",
        },
    },
    "observacions": "Alumne motivat però amb dificultats d'atenció sostinguda i lectura fluida.",
}

CONTEXT = {
    "etapa": "ESO",
    "curs": "2n ESO",
    "materia": "Biologia i Geologia",
    "mecr": "B1",
    "alfabet_llati": True,
}

PARAMS = {
    "mecr_sortida": "B1",
    "mecr_base": "B2",
    "dua": "Core",
    "etapa": "ESO",
    "lang": "ca",
    "materia": "Biologia i Geologia",
    "genere": "expositiu",
    "complements": {
        "preguntes_comprensio": True,
        "glossari": True,
        "esquema_visual": True,
    },
}

TEXT_ORIGINAL = """La fotosintesi es el proces bioquimic mitjancant el qual les plantes,
les algues i alguns bacteris transformen energia luminica en energia quimica,
sintetitzant glucosa a partir de diòxid de carboni i aigua. Aquest proces
te lloc principalment als cloroplasts, organuls cel·lulars que contenen
clorofil·la, un pigment que absorbeix la llum solar. La reaccio global es
6CO2 + 6H2O + llum -> C6H12O6 + 6O2, alliberant oxigen com a subproducte.
La fotosintesi te dues fases: la fase lluminosa (a les tilacoides, on es genera
ATP i NADPH) i la fase fosca o cicle de Calvin (a l'estroma, on es fixa el
carboni). La importancia ecologica es enorme: sustenta tota la cadena
trofica i regula la concentracio atmosferica d'O2 i CO2."""


MODELS = [
    ("gemma-4-31b-it", "Gemma 4 31B (baseline ATNE)"),
    ("gemini-2.5-flash", "Gemini 2.5 Flash"),
    ("gemini-2.5-flash-lite", "Gemini 2.5 Flash-Lite"),
]


def main():
    # 1. Generem el system prompt REAL una sola vegada (mateix per a tots els models)
    print("Construint system prompt real ATNE...", flush=True)
    system_prompt = build_system_prompt(PROFILE, CONTEXT, PARAMS, rag_context="")
    print(f"System prompt: {len(system_prompt)} caracters / ~{len(system_prompt)//4} tokens estimats", flush=True)

    # Guarda el prompt per inspeccio
    with open("tests/_atne_real_system_prompt.txt", "w", encoding="utf-8") as f:
        f.write(system_prompt)

    # 2. Crida cada model amb el system prompt real + text + complements
    results = []
    for model_id, label in MODELS:
        print(f"\n{'='*70}\nCRIDANT: {label} ({model_id})\n{'='*70}", flush=True)
        t0 = time.time()
        try:
            output = _call_llm(model_id, system_prompt, TEXT_ORIGINAL)
            elapsed = time.time() - t0
            print(f"OK | {elapsed:.1f}s | output_len: {len(output)} chars", flush=True)
            results.append({
                "model_id": model_id,
                "label": label,
                "elapsed_s": elapsed,
                "output_len": len(output),
                "output": output,
            })
        except Exception as e:
            elapsed = time.time() - t0
            print(f"ERROR after {elapsed:.1f}s: {str(e)[:300]}", flush=True)
            results.append({"model_id": model_id, "label": label, "error": str(e), "elapsed_s": elapsed})

    # Guarda report
    with open("tests/_atne_real_report.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n\n{'='*70}\nRESUM:\n{'='*70}")
    for r in results:
        if "error" in r:
            print(f"  {r['label']:<35} | ERROR | {r['elapsed_s']:.1f}s | {r['error'][:80]}")
        else:
            print(f"  {r['label']:<35} | {r['elapsed_s']:5.1f}s | {r['output_len']:>5} chars")


if __name__ == "__main__":
    main()
