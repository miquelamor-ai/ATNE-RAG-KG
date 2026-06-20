#!/usr/bin/env python3
"""
Peça 4 — Experiment A/B: skills OFF vs skills ON
Genera 5 parells (5 casos) amb dues condicions, mateix text+perfil:
  A) OFF: ATNE_USE_SKILLS=false  (prompt cau al catàleg hardcoded + corpus_reader)
  B) ON:  ATNE_USE_SKILLS=true   (s'injecten les SKILL write-* i generate-* via skills_loader)

Generador: gemini-2.5-flash-lite (model de producció actual, system_config.atne_model_adapt).
Temperatura: 0.4 (IDÈNTICA a A i B — el clau de l'A/B és que només canviï el flag).

L'única variable entre A i B és ATNE_USE_SKILLS. El prompt es construeix amb la MATEIXA
funció de producció build_system_prompt(..., adapter_only=True) en tots dos casos; el flag
commuta el bloc 4b-bis de skills (prompt_builder.py:736-761). skills_loader no té cache:
is_skills_enabled() llegeix os.environ en viu, així que n'hi ha prou amb commutar la var.
"""

import json, os, sys, time, io
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
MODEL = "gemini-2.5-flash-lite"   # model de producció actual (system_config.atne_model_adapt)
TEMPERATURE = 0.4                 # IDÈNTICA a OFF i ON
MAX_TOKENS = 8192

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

# ── Imports del pipeline ATNE ──
import skills_loader
from adaptation.prompt_builder import build_system_prompt


def call_gemini(system_prompt: str, user_text: str) -> str:
    """Crida Gemini amb rotació de claus (mateixa lògica que el harness original)."""
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
    """Converteix un perfil del JSON a l'estructura (profile, context, params) del pipeline."""
    perfil_id = perfil_config["perfil"]
    sub = perfil_config.get("sub_variables", {})

    characteristics = {}
    if perfil_id == "nouvingut":
        characteristics["nouvingut"] = {
            "actiu": True,
            "L1": sub.get("L1", ""),
            "alfabet_llati": sub.get("alfabet_llati", True),
            "calp": sub.get("calp", "inicial"),
        }
    elif perfil_id == "tea":
        characteristics["tea"] = {
            "actiu": True,
            "grau": sub.get("grau", "moderat"),
            "suport_visual": sub.get("suport_visual", True),
        }
    elif perfil_id == "tdah":
        characteristics["tdah"] = {
            "actiu": True,
            "grau": sub.get("grau", "moderat"),
            "baixa_memoria_treball": sub.get("baixa_memoria_treball", False),
        }
    elif perfil_id == "altes_capacitats":
        characteristics["altes_capacitats"] = {"actiu": True}
    elif perfil_id == "dislexia":
        characteristics["dislexia"] = {
            "actiu": True,
            "tipus_dislexia": sub.get("tipus_dislexia", "fonologica"),
            "grau": sub.get("grau", "moderat"),
        }

    profile = {"caracteristiques": characteristics}

    context = {
        "etapa": perfil_config.get("etapa", "ESO"),
        "curs": perfil_config.get("curs", ""),
    }

    mecr = perfil_config.get("mecr", "B1")
    params = {
        "mecr_sortida": mecr,
        # DUA: respecta el camp explícit del perfil si existeix (p.ex. cas 4 AC →
        # "Enriquiment", coherent amb M1-altes-capacitats: enriquir, no simplificar).
        # Fallback: derivació automàtica per MECR (Accés a nivells baixos, Core altrament).
        "dua": perfil_config.get("dua") or ("Accés" if mecr in ["pre-A1", "A1", "A2"] else "Core"),
        "genere_discursiu": perfil_config.get("genere", ""),
        "complements": perfil_config.get("complements", {}),
        "materia_estil": "generic",
    }
    return profile, context, params


def active_skills_for(profile: dict, params: dict) -> list:
    """Llista (només informativa) de les skills que select_active activaria amb el flag ON.
    Es calcula a part per registrar-ho a la sortida; NO altera el prompt."""
    try:
        all_skills = skills_loader.load_skills(skills_loader.default_skills_roots())
        active = []
        for role in ("adapter", "complements"):
            active.extend(skills_loader.select_active(all_skills, profile, params, agent_role=role))
        return [s.name for s in active]
    except Exception as e:
        return [f"(error calculant skills: {e})"]


def build_prompt_with_flag(profile, context, params, skills_on: bool) -> str:
    """Construeix el system prompt de producció amb ATNE_USE_SKILLS commutat.
    adapter_only=True replica el Call 1 del flux 2-call de producció."""
    os.environ["ATNE_USE_SKILLS"] = "true" if skills_on else "false"
    assert skills_loader.is_skills_enabled() == skills_on, "El flag no s'ha aplicat"
    return build_system_prompt(profile, context, params, adapter_only=True)


def generate_case(text_obj: dict, perfil_obj: dict, idx: int, total: int) -> dict:
    """Genera el parell OFF/ON per a un cas (mateix text+perfil, només canvia el flag)."""
    case_id = perfil_obj["id"]
    original = text_obj["text"]
    profile, context, params = build_profile_for_server(perfil_obj)
    skills_detected = active_skills_for(profile, params)

    print(f"  [{idx}/{total}] {case_id} ({perfil_obj.get('genere')}/{perfil_obj.get('mecr')})...", flush=True)

    # ── Condició A: skills OFF ──
    try:
        prompt_off = build_prompt_with_flag(profile, context, params, skills_on=False)
        t0 = time.time()
        result_off = call_gemini(prompt_off, f"TEXT ORIGINAL A ADAPTAR:\n\n{original}")
        time_off = round(time.time() - t0, 1)
        print(f"      OFF={time_off}s", flush=True)
    except Exception as e:
        prompt_off, result_off, time_off = f"ERROR: {e}", f"ERROR: {e}", 0
        print(f"      OFF=ERROR: {e}", flush=True)

    time.sleep(1)

    # ── Condició B: skills ON ──
    try:
        prompt_on = build_prompt_with_flag(profile, context, params, skills_on=True)
        t0 = time.time()
        result_on = call_gemini(prompt_on, f"TEXT ORIGINAL A ADAPTAR:\n\n{original}")
        time_on = round(time.time() - t0, 1)
        print(f"      ON={time_on}s  skills={skills_detected}", flush=True)
    except Exception as e:
        prompt_on, result_on, time_on = f"ERROR: {e}", f"ERROR: {e}", 0
        print(f"      ON=ERROR: {e}", flush=True)

    time.sleep(1)

    # Restaurem el flag a OFF per no contaminar res posterior
    os.environ["ATNE_USE_SKILLS"] = "false"

    return {
        "case_id": case_id,
        "text_id": text_obj["id"],
        "perfil_id": perfil_obj["perfil"],
        "etapa": text_obj["etapa"],
        "materia": text_obj["materia"],
        "genere": text_obj.get("genere", ""),
        "mecr": perfil_obj["mecr"],
        "skills_actives_ON": skills_detected,
        "original": original,
        "original_paraules": len(original.split()),
        "condicio_OFF": {
            "skills": False,
            "prompt_length": len(prompt_off) if isinstance(prompt_off, str) else 0,
            "resultat": result_off,
            "paraules": len(result_off.split()) if not result_off.startswith("ERROR") else 0,
            "temps_s": time_off,
        },
        "condicio_ON": {
            "skills": True,
            "prompt_length": len(prompt_on) if isinstance(prompt_on, str) else 0,
            "resultat": result_on,
            "paraules": len(result_on.split()) if not result_on.startswith("ERROR") else 0,
            "temps_s": time_on,
        },
        "timestamp": datetime.now().isoformat(),
    }


def main():
    print("=" * 60)
    print("PEÇA 4 — Experiment A/B: skills OFF vs skills ON")
    print("=" * 60)

    textos = json.loads(TEXTOS_PATH.read_text(encoding="utf-8"))
    perfils = json.loads(PERFILS_PATH.read_text(encoding="utf-8"))
    textos_map = {t["id"]: t for t in textos}

    print(f"Casos: {len(perfils)}")
    print(f"Model generador: {MODEL}, temp={TEMPERATURE} (idèntica OFF/ON)")
    print(f"Claus Gemini disponibles: {len(GEMINI_KEYS)}")
    print()

    # Recuperació de progrés
    if OUTPUT_PATH.exists():
        existing = json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))
        resultats = existing.get("casos", [])
        done_ids = {r["case_id"] for r in resultats}
        print(f"Recuperats {len(resultats)} casos existents. Continuant...")
    else:
        resultats, done_ids = [], set()

    total = len(perfils)
    for i, perfil_obj in enumerate(perfils, 1):
        if perfil_obj["id"] in done_ids:
            continue
        text_obj = textos_map.get(perfil_obj["text_id"])
        if text_obj is None:
            print(f"  [{i}/{total}] {perfil_obj['id']} SKIP: text_id '{perfil_obj['text_id']}' no trobat")
            continue
        resultats.append(generate_case(text_obj, perfil_obj, i, total))
        _save(resultats)

    _save(resultats)

    errors_off = sum(1 for r in resultats if r["condicio_OFF"]["resultat"].startswith("ERROR"))
    errors_on = sum(1 for r in resultats if r["condicio_ON"]["resultat"].startswith("ERROR"))
    print(f"\n{'=' * 60}")
    print(f"COMPLETAT: {len(resultats)} casos")
    print(f"Errors OFF: {errors_off}, Errors ON: {errors_on}")
    print(f"Fitxer: {OUTPUT_PATH}")


def _atomic_write(path: Path, text: str, retries: int = 5):
    """Escriptura atòmica amb reintents (evita PermissionError per locks transitoris
    de Windows: antivirus/indexador). Escriu a un .tmp i fa os.replace (atòmic)."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    for attempt in range(retries):
        try:
            tmp.write_text(text, encoding="utf-8")
            os.replace(tmp, path)
            return
        except PermissionError:
            if attempt == retries - 1:
                raise
            time.sleep(0.5 * (attempt + 1))


def _save(resultats):
    output = {
        "experiment": "peca4_ab_skills_off_vs_on",
        "model_generador": MODEL,
        "temperature": TEMPERATURE,
        "variable": "ATNE_USE_SKILLS (false=OFF, true=ON)",
        "data": datetime.now().isoformat(),
        "total_casos": len(resultats),
        "casos": resultats,
    }
    _atomic_write(OUTPUT_PATH, json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
