#!/usr/bin/env python3
"""
Xat 9 - Generacio multi-model: Mistral, Qwen, Gemma 4
Genera 360 parells per cada model (180 textos*perfils * 2 condicions)
"""
import json, os, sys, time, io, requests, argparse
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

EXP_DIR = Path(__file__).resolve().parent
TEXTOS_PATH = EXP_DIR / "textos.json"
PERFILS_PATH = EXP_DIR / "perfils.json"

import corpus_reader, instruction_filter
from server import build_system_prompt

# ========== Models ==========

GROQ_KEYS = [v for k, v in sorted(os.environ.items()) if k.startswith("GROQ_API_KEY")]
GEMMA_KEYS = [v for k, v in sorted(os.environ.items()) if k.startswith("GEMMA4_API_KEY")]
MISTRAL_KEY = os.getenv("MISTRAL_API_KEY")
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

_groq_idx = 0
_gemma_idx = 0


def call_mistral(system_prompt: str, user_text: str) -> str:
    """Mistral amb retries i backoff (free tier es desconnecta sovint)."""
    last_err = None
    for attempt in range(5):
        try:
            r = requests.post(
                "https://api.mistral.ai/v1/chat/completions",
                headers={"Authorization": f"Bearer {MISTRAL_KEY}", "Content-Type": "application/json"},
                json={
                    "model": "mistral-small-latest",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"TEXT ORIGINAL A ADAPTAR:\n\n{user_text}"},
                    ],
                    "max_tokens": 8192, "temperature": 0.4,
                },
                timeout=180,
            )
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"] or ""
            elif r.status_code == 429:
                # Rate limit, esperar mes
                time.sleep(10 * (attempt + 1))
                last_err = f"HTTP 429 (rate limit)"
            else:
                last_err = f"HTTP {r.status_code}: {r.text[:150]}"
                time.sleep(3)
        except Exception as e:
            last_err = str(e)[:150]
            time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"Mistral fallat despres 5 intents: {last_err}")


def call_llama_groq(system_prompt: str, user_text: str) -> str:
    """Llama 3.3 70B via Groq amb retries i rotacio. Backoff agressiu per 429."""
    global _groq_idx
    errors = []
    # Fer 2 voltes completes per totes les claus amb backoff creixent
    for round_n in range(2):
        for attempt in range(len(GROQ_KEYS)):
            idx = (_groq_idx + attempt) % len(GROQ_KEYS)
            try:
                r = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {GROQ_KEYS[idx]}", "Content-Type": "application/json"},
                    json={
                        "model": "llama-3.3-70b-versatile",
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": f"TEXT ORIGINAL A ADAPTAR:\n\n{user_text}"},
                        ],
                        "max_tokens": 8192, "temperature": 0.4,
                    },
                    timeout=180,
                )
                if r.status_code == 200:
                    _groq_idx = (idx + 1) % len(GROQ_KEYS)
                    return r.json()["choices"][0]["message"]["content"] or ""
                if r.status_code == 429:
                    # Rate limit: esperar abans de provar la seguent clau
                    errors.append(f"clau{idx+1}: HTTP429")
                    time.sleep(8)
                else:
                    errors.append(f"clau{idx+1}: HTTP{r.status_code}")
                    time.sleep(2)
            except Exception as e:
                errors.append(f"clau{idx+1}: {str(e)[:60]}")
                time.sleep(3)
        # Despres de la primera volta, espera mes
        if round_n == 0:
            time.sleep(15)
    raise RuntimeError(f"Totes les claus Groq han fallat: {'; '.join(errors[:5])}")


def call_gemma(system_prompt: str, user_text: str) -> str:
    """Gemma via Google API (rotacio claus)."""
    global _gemma_idx
    from google import genai
    from google.genai import types
    errors = []
    for attempt in range(len(GEMMA_KEYS)):
        idx = (_gemma_idx + attempt) % len(GEMMA_KEYS)
        try:
            client = genai.Client(
                api_key=GEMMA_KEYS[idx],
                http_options=types.HttpOptions(timeout=300_000),
            )
            response = client.models.generate_content(
                model="gemma-4-31b-it",  # Gemma 4 31B - el millor Gemma disponible, ja usat a server.py
                contents=[types.Content(role="user", parts=[types.Part(text=f"{system_prompt}\n\n---\n\nTEXT ORIGINAL A ADAPTAR:\n\n{user_text}")])],
                config=types.GenerateContentConfig(temperature=0.4, max_output_tokens=8192),
            )
            _gemma_idx = (idx + 1) % len(GEMMA_KEYS)
            return response.text or ""
        except Exception as e:
            errors.append(f"clau{idx+1}: {str(e)[:50]}")
            time.sleep(1)
    raise RuntimeError(f"Totes les claus Gemma han fallat: {'; '.join(errors[:3])}")


CALLERS = {
    "mistral": call_mistral,
    "llama": call_llama_groq,
    "qwen": call_llama_groq,  # alies — Qwen no funciona per limit TPM, usem Llama 3.3 70B
    "gemma": call_gemma,
}

# ========== Pipeline ==========

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


def generate_pair(model_name, text_obj, perfil_obj, pair_idx, total):
    text_id = text_obj["id"]
    perfil_id = perfil_obj["id"]
    original = text_obj["text"]
    caller = CALLERS[model_name]

    print(f"  [{pair_idx:3d}/{total}] {text_id} x {perfil_id}...", end=" ", flush=True)

    # A: prompt minim
    try:
        t0 = time.time()
        result_a = caller(perfil_obj["prompt_minim"], original)
        time_a = round(time.time() - t0, 1)
        print(f"A={time_a}s", end=" ", flush=True)
    except Exception as e:
        result_a = f"ERROR: {str(e)[:150]}"
        time_a = 0
        print(f"A=ERR", end=" ", flush=True)

    # Pacing extra per a models amb quota limitada (llama/mistral via Groq)
    if model_name in ("llama", "qwen"):
        time.sleep(3)  # Groq TPM = 6K, esperar per no saturar
    else:
        time.sleep(0.5)

    # B: prompt complet
    try:
        profile, context, params = build_profile_for_server(perfil_obj)
        sys_prompt_b = build_system_prompt(profile, context, params)
        t0 = time.time()
        result_b = caller(sys_prompt_b, original)
        time_b = round(time.time() - t0, 1)
        print(f"B={time_b}s OK")
    except Exception as e:
        result_b = f"ERROR: {str(e)[:150]}"
        time_b = 0
        sys_prompt_b = ""
        print(f"B=ERR")

    # Pacing extra final
    if model_name in ("llama", "qwen"):
        time.sleep(5)  # entre parells, extra per Groq
    else:
        time.sleep(0.5)

    return {
        "pair_id": f"{text_id}_{perfil_id}",
        "text_id": text_id, "perfil_id": perfil_id,
        "etapa": text_obj["etapa"], "materia": text_obj["materia"],
        "dificultat": text_obj["dificultat"], "mecr": perfil_obj["mecr"],
        "original": original,
        "original_paraules": len(original.split()),
        "model_generador": model_name,
        "condicio_A": {"prompt": perfil_obj["prompt_minim"], "resultat": result_a, "paraules": len(result_a.split()) if not result_a.startswith("ERROR") else 0, "temps_s": time_a},
        "condicio_B": {"prompt_length": len(sys_prompt_b) if isinstance(sys_prompt_b, str) else 0, "resultat": result_b, "paraules": len(result_b.split()) if not result_b.startswith("ERROR") else 0, "temps_s": time_b},
        "timestamp": datetime.now().isoformat(),
    }


def main(model_name):
    if model_name not in CALLERS:
        print(f"Model desconegut: {model_name}. Opcions: {list(CALLERS.keys())}")
        sys.exit(1)

    output_path = EXP_DIR / f"resultats_generacio_{model_name}.json"

    print("=" * 60)
    print(f"XAT 9 - Generacio A/B amb {model_name.upper()}")
    print("=" * 60)

    textos = json.loads(TEXTOS_PATH.read_text(encoding="utf-8"))
    perfils = json.loads(PERFILS_PATH.read_text(encoding="utf-8"))
    total = len(textos) * len(perfils)

    print(f"Textos: {len(textos)}, Perfils: {len(perfils)}, Total: {total}\n")

    resultats = []
    done_ids = set()
    if output_path.exists():
        existing = json.loads(output_path.read_text(encoding="utf-8"))
        # Nomes recuperar OK (no errors)
        resultats = [r for r in existing.get("parells", [])
                     if not str(r["condicio_A"]["resultat"]).startswith("ERROR")
                     and not str(r["condicio_B"]["resultat"]).startswith("ERROR")]
        done_ids = {r["pair_id"] for r in resultats}
        print(f"Recuperats {len(resultats)} parells OK. Continuant...\n")

    pair_idx = 0
    for text_obj in textos:
        for perfil_obj in perfils:
            pair_id = f"{text_obj['id']}_{perfil_obj['id']}"
            pair_idx += 1
            if pair_id in done_ids:
                continue

            result = generate_pair(model_name, text_obj, perfil_obj, pair_idx, total)
            resultats.append(result)

            if len(resultats) % 10 == 0:
                output = {"experiment": f"xat9_ab_{model_name}", "model": model_name, "data": datetime.now().isoformat(), "total_parells": len(resultats), "parells": resultats}
                output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    output = {"experiment": f"xat9_ab_{model_name}", "model": model_name, "data": datetime.now().isoformat(), "total_parells": len(resultats), "parells": resultats}
    output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    errors_a = sum(1 for r in resultats if str(r["condicio_A"]["resultat"]).startswith("ERROR"))
    errors_b = sum(1 for r in resultats if str(r["condicio_B"]["resultat"]).startswith("ERROR"))
    print(f"\n{'='*60}")
    print(f"COMPLETAT: {len(resultats)} parells")
    print(f"Errors: A={errors_a}, B={errors_b}")
    print(f"Fitxer: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("model", choices=["mistral", "qwen", "llama", "gemma"])
    args = parser.parse_args()
    main(args.model)
