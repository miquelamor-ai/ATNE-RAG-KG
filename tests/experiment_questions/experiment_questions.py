#!/usr/bin/env python3
"""
Experiment Questions - generador multi-model
Genera preguntes de comprensio lectora (9 tipus, taxonomia Bloom) per a perfils especifics.
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
TIPUS_PATH = EXP_DIR / "tipus_questions.json"

GROQ_KEYS = [v for k, v in sorted(os.environ.items()) if k.startswith("GROQ_API_KEY")]
GEMMA_KEYS = [v for k, v in sorted(os.environ.items()) if k.startswith("GEMMA4_API_KEY")]
MISTRAL_KEY = os.getenv("MISTRAL_API_KEY")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

_groq_idx = 0
_gemma_idx = 0


def call_gpt(system_prompt, user_text):
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_KEY)
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text},
        ],
        max_tokens=4096, temperature=0.4,
        response_format={"type": "json_object"},
    )
    return resp.choices[0].message.content or ""


def call_mistral(system_prompt, user_text):
    last_err = None
    for attempt in range(3):
        try:
            r = requests.post(
                "https://api.mistral.ai/v1/chat/completions",
                headers={"Authorization": f"Bearer {MISTRAL_KEY}", "Content-Type": "application/json"},
                json={
                    "model": "mistral-small-latest",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_text},
                    ],
                    "max_tokens": 4096, "temperature": 0.4,
                    "response_format": {"type": "json_object"},
                },
                timeout=120,
            )
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"] or ""
            last_err = f"HTTP{r.status_code}"
            time.sleep(3)
        except Exception as e:
            last_err = str(e)[:100]
            time.sleep(3)
    raise RuntimeError(f"Mistral fail: {last_err}")


def call_llama(system_prompt, user_text):
    global _groq_idx
    errors = []
    for attempt in range(min(3, len(GROQ_KEYS))):
        idx = (_groq_idx + attempt) % len(GROQ_KEYS)
        try:
            r = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ_KEYS[idx]}", "Content-Type": "application/json"},
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_text},
                    ],
                    "max_tokens": 1500, "temperature": 0.4,
                    "response_format": {"type": "json_object"},
                },
                timeout=120,
            )
            if r.status_code == 200:
                _groq_idx = (idx + 1) % len(GROQ_KEYS)
                return r.json()["choices"][0]["message"]["content"] or ""
            errors.append(f"c{idx+1}:HTTP{r.status_code}")
            time.sleep(3)
        except Exception as e:
            errors.append(f"c{idx+1}:{str(e)[:30]}")
            time.sleep(3)
    raise RuntimeError(f"Llama fail: {'; '.join(errors)}")


def call_gemma(system_prompt, user_text):
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
                model="gemma-4-31b-it",
                contents=[types.Content(role="user", parts=[types.Part(text=f"{system_prompt}\n\n---\n\n{user_text}")])],
                config=types.GenerateContentConfig(temperature=0.4, max_output_tokens=4096),
            )
            _gemma_idx = (idx + 1) % len(GEMMA_KEYS)
            return response.text or ""
        except Exception as e:
            errors.append(f"c{idx+1}:{str(e)[:50]}")
            time.sleep(1)
    raise RuntimeError(f"Gemma fail: {'; '.join(errors[:3])}")


CALLERS = {
    "gpt4o-mini": call_gpt,
    "mistral": call_mistral,
    "llama": call_llama,
    "gemma": call_gemma,
}


def build_system_prompt(perfil, tipus_question):
    return f"""Ets un especialista en avaluacio educativa i taxonomia de Bloom.
La teva tasca es generar PREGUNTES DE COMPRENSIO LECTORA d'un tipus pedagogic concret.

PERFIL DE L'ALUMNE:
- Nom: {perfil['nom']}
- Descripcio: {perfil['descripcio_curta']}
- Etapa: {perfil['etapa']} ({perfil.get('curs', '')})
- MECR: {perfil['mecr']}
- Caracteristiques: {json.dumps(perfil.get('sub_variables', {}), ensure_ascii=False)}

TIPUS DE PREGUNTES A GENERAR:
- Nom: {tipus_question['nom']}
- Instruccions: {tipus_question['instruccio']}

REGLES:
1. Genera NOMES el JSON demanat, sense text fora del JSON.
2. Les preguntes han de respectar el nivell MECR i el perfil.
3. Les preguntes NO han de copiar literalment frases del text - reformula sempre.
4. Cada pregunta ha de ser pedagogicament valida (mesura el que diu mesurar).
5. JSON valid, parseable amb json.loads().
"""


def generate_one(model_name, text_obj, perfil, tipus, idx, total):
    text_id = text_obj["id"]
    perfil_id = perfil["id"]
    tipus_id = tipus["id"]

    print(f"  [{idx:3d}/{total}] {model_name}/{tipus_id}/{perfil_id}/{text_id}...", end=" ", flush=True)

    sys_prompt = build_system_prompt(perfil, tipus)
    user_text = f"TEXT ORIGINAL:\n\n{text_obj['text']}\n\nGenera les preguntes en JSON valid."

    try:
        t0 = time.time()
        result = CALLERS[model_name](sys_prompt, user_text)
        t = round(time.time() - t0, 1)
        # Validar que sigui JSON parseable (strip markdown fences si cal)
        clean = result
        if "```json" in clean:
            clean = clean.split("```json", 1)[1].split("```", 1)[0]
        elif "```" in clean:
            clean = clean.split("```", 1)[1].split("```", 1)[0]
        try:
            parsed = json.loads(clean.strip())
            json_valid = True
            n_preguntes = len(parsed.get("preguntes", []))
        except:
            parsed = None
            json_valid = False
            n_preguntes = 0
        print(f"OK ({t}s, {n_preguntes}q, json_ok={json_valid})")
    except Exception as e:
        result = f"ERROR: {str(e)[:150]}"
        t = 0
        json_valid = False
        n_preguntes = 0
        parsed = None
        print(f"ERR")

    if model_name == "llama":
        time.sleep(3)
    else:
        time.sleep(0.3)

    return {
        "case_id": f"{tipus_id}_{perfil_id}_{text_id}",
        "model_generador": model_name,
        "tipus_question": tipus_id,
        "perfil_id": perfil_id,
        "text_id": text_id,
        "etapa": text_obj["etapa"],
        "materia": text_obj["materia"],
        "mecr": perfil["mecr"],
        "text_original": text_obj["text"],
        "preguntes_raw": result,
        "preguntes_parsed": parsed,
        "json_valid": json_valid,
        "n_preguntes": n_preguntes,
        "temps_s": t,
        "timestamp": datetime.now().isoformat(),
    }


def main(model_name):
    if model_name not in CALLERS:
        print(f"Model desconegut: {model_name}")
        sys.exit(1)

    output_path = EXP_DIR / f"resultats_questions_{model_name}.json"

    print("=" * 60)
    print(f"EXPERIMENT QUESTIONS - {model_name.upper()}")
    print("=" * 60)

    textos = json.loads(TEXTOS_PATH.read_text(encoding="utf-8"))
    perfils = json.loads(PERFILS_PATH.read_text(encoding="utf-8"))
    perfils_map = {p["id"]: p for p in perfils}
    tipus_list = json.loads(TIPUS_PATH.read_text(encoding="utf-8"))

    cases = []
    for tipus in tipus_list:
        for perfil_id in tipus["perfils_aplicables"]:
            if perfil_id not in perfils_map:
                continue
            perfil = perfils_map[perfil_id]
            for text_obj in textos:
                cases.append((text_obj, perfil, tipus))

    total = len(cases)
    print(f"Casos totals: {total}")
    print(f"  Tipus: {len(tipus_list)}, Perfils: {len(perfils)}, Textos: {len(textos)}\n")

    resultats = []
    done = set()
    if output_path.exists():
        existing = json.loads(output_path.read_text(encoding="utf-8"))
        resultats = [r for r in existing.get("casos", [])
                     if not str(r.get("preguntes_raw", "")).startswith("ERROR")]
        done = {r["case_id"] for r in resultats}
        print(f"Recuperats {len(resultats)} casos OK\n")

    for idx, (text_obj, perfil, tipus) in enumerate(cases, 1):
        case_id = f"{tipus['id']}_{perfil['id']}_{text_obj['id']}"
        if case_id in done:
            continue

        result = generate_one(model_name, text_obj, perfil, tipus, idx, total)
        resultats.append(result)

        if len(resultats) % 10 == 0:
            output = {
                "experiment": f"questions_{model_name}",
                "model": model_name,
                "data": datetime.now().isoformat(),
                "total_casos": len(resultats),
                "casos": resultats,
            }
            output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    output = {
        "experiment": f"questions_{model_name}",
        "model": model_name,
        "data": datetime.now().isoformat(),
        "total_casos": len(resultats),
        "casos": resultats,
    }
    output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    err = sum(1 for r in resultats if str(r.get("preguntes_raw", "")).startswith("ERROR"))
    json_ok = sum(1 for r in resultats if r.get("json_valid"))
    print(f"\nCOMPLETAT: {len(resultats)} casos, errors: {err}, json valid: {json_ok}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("model", choices=["gpt4o-mini", "mistral", "llama", "gemma"])
    args = parser.parse_args()
    main(args.model)
