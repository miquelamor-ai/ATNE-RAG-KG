#!/usr/bin/env python3
"""
Xat 9 — Experiment A/B amb GPT-4o-mini com a generador
Fallback quan Gemini no té quota.
"""
import json, os, sys, time, io
from pathlib import Path
from datetime import datetime

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI

MODEL = "gpt-4o-mini"
TEMPERATURE = 0.4
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EXP_DIR = Path(__file__).resolve().parent
TEXTOS_PATH = EXP_DIR / "textos.json"
PERFILS_PATH = EXP_DIR / "perfils.json"
OUTPUT_PATH = EXP_DIR / "resultats_generacio.json"

import corpus_reader, instruction_filter
from server import build_system_prompt, build_persona_audience, _get_active_profiles


def call_gpt(system_prompt: str, user_text: str) -> str:
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"TEXT ORIGINAL A ADAPTAR:\n\n{user_text}"},
        ],
        max_tokens=8192, temperature=TEMPERATURE,
    )
    return resp.choices[0].message.content or ""


def build_profile_for_server(perfil_config: dict) -> tuple:
    perfil_id = perfil_config["perfil"]
    sub = perfil_config.get("sub_variables", {})
    characteristics = {}

    if perfil_id == "nouvingut":
        characteristics["nouvingut"] = {"actiu": True, "L1": sub.get("L1", ""), "alfabet_llati": sub.get("alfabet_llati", True), "calp": sub.get("calp", "inicial")}
    elif perfil_id == "tdah":
        characteristics["tdah"] = {"actiu": True, "grau": sub.get("grau", sub.get("grau_tdah", "lleu")), "baixa_memoria_treball": sub.get("baixa_memoria_treball", False)}
        if sub.get("perfil_di"):
            characteristics["di"] = {"actiu": True, "grau": sub.get("grau_di", "lleu")}
    elif perfil_id == "altes_capacitats":
        characteristics["altes_capacitats"] = {"actiu": True}
    elif perfil_id == "tdl":
        characteristics["tdl"] = {"actiu": True, "grau": sub.get("grau", "moderat"), "modalitat": sub.get("modalitat", ""), "pragmatica": sub.get("pragmatica", False), "morfosintaxi": sub.get("morfosintaxi", False), "semantica": sub.get("semantica", False)}
    elif perfil_id == "2e":
        characteristics["altes_capacitats"] = {"actiu": True}
        characteristics["dislexia"] = {"actiu": True, "tipus_dislexia": sub.get("tipus_dislexia", "fonologica"), "grau": sub.get("grau_dislexia", "moderat")}

    profile = {"caracteristiques": characteristics}
    context = {"etapa": perfil_config.get("etapa", "ESO"), "curs": perfil_config.get("curs", "")}
    params = {
        "mecr_sortida": perfil_config.get("mecr", "B1"),
        "dua": "Accés" if perfil_config.get("mecr", "B1") in ["pre-A1", "A1", "A2"] else "Core",
        "complements": {"glossari": True, "esquema": False, "pictogrames": False},
        "materia_estil": "generic",
    }
    return profile, context, params


def generate_pair(text_obj, perfil_obj, pair_idx, total):
    text_id = text_obj["id"]
    perfil_id = perfil_obj["id"]
    original = text_obj["text"]

    print(f"  [{pair_idx:3d}/{total}] {text_id} x {perfil_id}...", end=" ", flush=True)

    # A: prompt minim
    try:
        t0 = time.time()
        result_a = call_gpt(perfil_obj["prompt_minim"], original)
        time_a = round(time.time() - t0, 1)
        print(f"A={time_a}s", end=" ", flush=True)
    except Exception as e:
        result_a = f"ERROR: {e}"
        time_a = 0
        print(f"A=ERR", end=" ", flush=True)

    time.sleep(0.3)

    # B: prompt complet
    try:
        profile, context, params = build_profile_for_server(perfil_obj)
        sys_prompt_b = build_system_prompt(profile, context, params)
        t0 = time.time()
        result_b = call_gpt(sys_prompt_b, original)
        time_b = round(time.time() - t0, 1)
        print(f"B={time_b}s OK")
    except Exception as e:
        result_b = f"ERROR: {e}"
        time_b = 0
        sys_prompt_b = ""
        print(f"B=ERR")

    time.sleep(0.3)

    return {
        "pair_id": f"{text_id}_{perfil_id}",
        "text_id": text_id, "perfil_id": perfil_id,
        "etapa": text_obj["etapa"], "materia": text_obj["materia"],
        "dificultat": text_obj["dificultat"], "mecr": perfil_obj["mecr"],
        "original": original,
        "original_paraules": len(original.split()),
        "condicio_A": {"prompt": perfil_obj["prompt_minim"], "resultat": result_a, "paraules": len(result_a.split()) if not result_a.startswith("ERROR") else 0, "temps_s": time_a},
        "condicio_B": {"prompt_length": len(sys_prompt_b) if isinstance(sys_prompt_b, str) else 0, "resultat": result_b, "paraules": len(result_b.split()) if not result_b.startswith("ERROR") else 0, "temps_s": time_b},
        "timestamp": datetime.now().isoformat(),
    }


def main():
    print("=" * 60)
    print("XAT 9 — Generacio A/B amb GPT-4o-mini")
    print("=" * 60)

    textos = json.loads(TEXTOS_PATH.read_text(encoding="utf-8"))
    perfils = json.loads(PERFILS_PATH.read_text(encoding="utf-8"))
    total = len(textos) * len(perfils)

    print(f"Textos: {len(textos)}, Perfils: {len(perfils)}, Total: {total}")
    print(f"Model: {MODEL}, temp={TEMPERATURE}\n")

    resultats = []
    done_ids = set()
    if OUTPUT_PATH.exists():
        existing = json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))
        resultats = existing.get("parells", [])
        done_ids = {r["pair_id"] for r in resultats}
        print(f"Recuperats {len(resultats)} parells. Continuant...\n")

    pair_idx = 0
    for text_obj in textos:
        for perfil_obj in perfils:
            pair_id = f"{text_obj['id']}_{perfil_obj['id']}"
            pair_idx += 1
            if pair_id in done_ids:
                continue

            result = generate_pair(text_obj, perfil_obj, pair_idx, total)
            resultats.append(result)

            if len(resultats) % 10 == 0:
                output = {"experiment": "xat9_ab_gpt4o_mini", "model": MODEL, "temperature": TEMPERATURE, "data": datetime.now().isoformat(), "total_parells": len(resultats), "parells": resultats}
                OUTPUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
                print(f"  [Guardat {len(resultats)} parells]")

    output = {"experiment": "xat9_ab_gpt4o_mini", "model": MODEL, "temperature": TEMPERATURE, "data": datetime.now().isoformat(), "total_parells": len(resultats), "parells": resultats}
    OUTPUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    errors_a = sum(1 for r in resultats if str(r["condicio_A"]["resultat"]).startswith("ERROR"))
    errors_b = sum(1 for r in resultats if str(r["condicio_B"]["resultat"]).startswith("ERROR"))
    print(f"\n{'='*60}")
    print(f"COMPLETAT: {len(resultats)} parells")
    print(f"Errors: A={errors_a}, B={errors_b}")


if __name__ == "__main__":
    main()
