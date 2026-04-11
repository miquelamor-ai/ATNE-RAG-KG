#!/usr/bin/env python3
"""
Xat 9 — Experiment A/B: Prompt mínim vs prompt complet
Genera 180 parells (30 textos × 6 perfils) amb dues condicions:
  A) Prompt mínim: una línia descrivint perfil + etapa + MECR
  B) Prompt complet: pipeline sencer (identitat + instruccions filtrades + DUA + persona)

Model: Gemini 2.5-flash, temp=0.4, thinking=0
"""

import json, os, sys, time, random, io
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Afegir arrel del projecte al path
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from dotenv import load_dotenv
load_dotenv()

from google import genai
from google.genai import types

# ── Configuració ──
MODEL = "gemini-2.5-flash"
TEMPERATURE = 0.4
MAX_TOKENS = 8192
SEED_OFFSET = 42  # per reproducibilitat relativa

# Claus Gemini (rotació)
GEMINI_KEYS = [v for k, v in sorted(os.environ.items()) if k.startswith("GEMINI_API_KEY")]
if not GEMINI_KEYS:
    raise RuntimeError("Cap GEMINI_API_KEY trobada al .env")
_key_idx = 0

# ── Paths ──
EXP_DIR = Path(__file__).resolve().parent
TEXTOS_PATH = EXP_DIR / "textos.json"
PERFILS_PATH = EXP_DIR / "perfils.json"
OUTPUT_PATH = EXP_DIR / "resultats_generacio.json"

# ── Imports del pipeline ATNE (condició B) ──
import corpus_reader
import instruction_filter
from server import build_system_prompt, build_persona_audience, _get_active_profiles


def call_gemini(system_prompt: str, user_text: str) -> str:
    """Crida Gemini amb rotació de claus."""
    global _key_idx
    errors = []
    for attempt in range(len(GEMINI_KEYS)):
        idx = (_key_idx + attempt) % len(GEMINI_KEYS)
        client = genai.Client(
            api_key=GEMINI_KEYS[idx],
            http_options=types.HttpOptions(timeout=300_000),
        )
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=[types.Content(role="user", parts=[types.Part(text=user_text)])],
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=TEMPERATURE,
                    max_output_tokens=MAX_TOKENS,
                    thinking_config=types.ThinkingConfig(thinking_budget=0),
                ),
            )
            _key_idx = (idx + 1) % len(GEMINI_KEYS)
            return response.text or ""
        except Exception as e:
            errors.append(f"clau {idx+1}: {e}")
            time.sleep(2)
            continue
    raise RuntimeError(f"Totes les claus han fallat: {'; '.join(errors)}")


def build_profile_for_server(perfil_config: dict) -> tuple:
    """Converteix un perfil del JSON a l'estructura que espera server.py."""
    perfil_id = perfil_config["perfil"]
    sub = perfil_config.get("sub_variables", {})

    # Estructura de 'profile' com ho espera build_system_prompt
    characteristics = {}

    if perfil_id == "nouvingut":
        characteristics["nouvingut"] = {
            "actiu": True,
            "L1": sub.get("L1", ""),
            "alfabet_llati": sub.get("alfabet_llati", True),
            "calp": sub.get("calp", "inicial"),
        }
    elif perfil_id == "tdah":
        characteristics["tdah"] = {
            "actiu": True,
            "grau": sub.get("grau", sub.get("grau_tdah", "lleu")),
            "baixa_memoria_treball": sub.get("baixa_memoria_treball", False),
        }
        if sub.get("perfil_di"):
            characteristics["di"] = {
                "actiu": True,
                "grau": sub.get("grau_di", "lleu"),
            }
    elif perfil_id == "altes_capacitats":
        characteristics["altes_capacitats"] = {"actiu": True}
    elif perfil_id == "tdl":
        characteristics["tdl"] = {
            "actiu": True,
            "grau": sub.get("grau", "moderat"),
            "modalitat": sub.get("modalitat", ""),
            "pragmatica": sub.get("pragmatica", False),
            "morfosintaxi": sub.get("morfosintaxi", False),
            "semantica": sub.get("semantica", False),
        }
    elif perfil_id == "2e":
        characteristics["altes_capacitats"] = {"actiu": True}
        characteristics["dislexia"] = {
            "actiu": True,
            "tipus_dislexia": sub.get("tipus_dislexia", "fonologica"),
            "grau": sub.get("grau_dislexia", "moderat"),
        }

    profile = {"caracteristiques": characteristics}

    context = {
        "etapa": perfil_config.get("etapa", "ESO"),
        "curs": perfil_config.get("curs", ""),
    }

    params = {
        "mecr_sortida": perfil_config.get("mecr", "B1"),
        "dua": "Accés" if perfil_config.get("mecr", "B1") in ["pre-A1", "A1", "A2"] else "Core",
        "complements": {"glossari": True, "esquema": False, "pictogrames": False},
        "materia_estil": "generic",
    }

    return profile, context, params


def generate_pair(text_obj: dict, perfil_obj: dict, pair_idx: int) -> dict:
    """Genera un parell A/B per a un text i un perfil."""
    text_id = text_obj["id"]
    perfil_id = perfil_obj["id"]
    original = text_obj["text"]

    print(f"  [{pair_idx:3d}/180] {text_id} × {perfil_id}...", end=" ", flush=True)

    # ── Condició A: Prompt mínim ──
    prompt_minim = perfil_obj["prompt_minim"]
    try:
        t0 = time.time()
        result_a = call_gemini(
            system_prompt=prompt_minim,
            user_text=f"TEXT ORIGINAL A ADAPTAR:\n\n{original}"
        )
        time_a = round(time.time() - t0, 1)
        print(f"A={time_a}s", end=" ", flush=True)
    except Exception as e:
        result_a = f"ERROR: {e}"
        time_a = 0
        print(f"A=ERROR", end=" ", flush=True)

    time.sleep(1)  # rate limit

    # ── Condició B: Prompt complet (pipeline ATNE) ──
    try:
        profile, context, params = build_profile_for_server(perfil_obj)
        system_prompt_b = build_system_prompt(profile, context, params)

        t0 = time.time()
        result_b = call_gemini(
            system_prompt=system_prompt_b,
            user_text=f"TEXT ORIGINAL A ADAPTAR:\n\n{original}"
        )
        time_b = round(time.time() - t0, 1)
        print(f"B={time_b}s ✓")
    except Exception as e:
        result_b = f"ERROR: {e}"
        time_b = 0
        system_prompt_b = f"ERROR building prompt: {e}"
        print(f"B=ERROR")

    time.sleep(1)  # rate limit

    return {
        "pair_id": f"{text_id}_{perfil_id}",
        "text_id": text_id,
        "perfil_id": perfil_id,
        "etapa": text_obj["etapa"],
        "materia": text_obj["materia"],
        "dificultat": text_obj["dificultat"],
        "mecr": perfil_obj["mecr"],
        "original": original,
        "original_paraules": len(original.split()),
        "condicio_A": {
            "prompt": prompt_minim,
            "resultat": result_a,
            "paraules": len(result_a.split()) if not result_a.startswith("ERROR") else 0,
            "temps_s": time_a,
        },
        "condicio_B": {
            "prompt_length": len(system_prompt_b) if isinstance(system_prompt_b, str) else 0,
            "resultat": result_b,
            "paraules": len(result_b.split()) if not result_b.startswith("ERROR") else 0,
            "temps_s": time_b,
        },
        "timestamp": datetime.now().isoformat(),
    }


def main():
    print("=" * 60)
    print("XAT 9 — Experiment A/B: Prompt mínim vs complet")
    print("=" * 60)

    # Carregar dades
    textos = json.loads(TEXTOS_PATH.read_text(encoding="utf-8"))
    perfils = json.loads(PERFILS_PATH.read_text(encoding="utf-8"))

    print(f"Textos: {len(textos)}")
    print(f"Perfils: {len(perfils)}")
    print(f"Total parells: {len(textos) * len(perfils)}")
    print(f"Model: {MODEL}, temp={TEMPERATURE}")
    print(f"Claus Gemini disponibles: {len(GEMINI_KEYS)}")
    print()

    # Generar parells
    resultats = []
    pair_idx = 0

    # Recuperar resultats existents si hi ha un fitxer parcial
    if OUTPUT_PATH.exists():
        existing = json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))
        done_ids = {r["pair_id"] for r in existing.get("parells", [])}
        resultats = existing.get("parells", [])
        print(f"Recuperats {len(resultats)} parells existents. Continuant...")
    else:
        done_ids = set()

    for text_obj in textos:
        for perfil_obj in perfils:
            pair_id = f"{text_obj['id']}_{perfil_obj['id']}"
            pair_idx += 1

            if pair_id in done_ids:
                continue

            result = generate_pair(text_obj, perfil_obj, pair_idx)
            resultats.append(result)

            # Guardar progressivament cada 5 parells
            if len(resultats) % 5 == 0:
                output = {
                    "experiment": "xat9_ab_prompt_minim_vs_complet",
                    "model": MODEL,
                    "temperature": TEMPERATURE,
                    "data": datetime.now().isoformat(),
                    "total_parells": len(resultats),
                    "parells": resultats,
                }
                OUTPUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
                print(f"  [Guardat {len(resultats)} parells]")

    # Guardat final
    output = {
        "experiment": "xat9_ab_prompt_minim_vs_complet",
        "model": MODEL,
        "temperature": TEMPERATURE,
        "data": datetime.now().isoformat(),
        "total_parells": len(resultats),
        "parells": resultats,
    }
    OUTPUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    # Stats
    errors_a = sum(1 for r in resultats if r["condicio_A"]["resultat"].startswith("ERROR"))
    errors_b = sum(1 for r in resultats if r["condicio_B"]["resultat"].startswith("ERROR"))
    print(f"\n{'=' * 60}")
    print(f"COMPLETAT: {len(resultats)} parells generats")
    print(f"Errors A: {errors_a}, Errors B: {errors_b}")
    print(f"Fitxer: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
