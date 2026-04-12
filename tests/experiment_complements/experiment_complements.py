#!/usr/bin/env python3
"""
Experiment Complements - generador multi-model
Genera complements pedagogics (8 tipus) per a perfils especifics amb 4 models.
Reusa la infraestructura de l'experiment Xat 9.
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
TIPUS_PATH = EXP_DIR / "tipus_complements.json"

# ── Models ──
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


def build_system_prompt(text, perfil, tipus_complement):
    """Construeix el prompt per generar UN complement concret."""
    return f"""Ets un especialista en disseny de materials educatius adaptats a la diversitat.
La teva tasca és generar UN COMPLEMENT PEDAGOGIC concret per a un text educatiu.

PERFIL DE L'ALUMNE:
- Nom del perfil: {perfil['nom']}
- Descripcio: {perfil['descripcio_curta']}
- Etapa: {perfil['etapa']} ({perfil.get('curs', '')})
- Nivell MECR de sortida: {perfil['mecr']}
- Caracteristiques especifiques: {json.dumps(perfil.get('sub_variables', {}), ensure_ascii=False)}

TIPUS DE COMPLEMENT A GENERAR:
- Tipus: {tipus_complement['nom']}
- Instruccions especifiques: {tipus_complement['instruccio']}

REGLES GENERALS:
1. Genera NOMES el complement demanat, sense text introductori ni explicacions externes.
2. El complement ha de ser util per a aquest perfil concret, no generic.
3. Respecta el nivell MECR i la carrega cognitiva apropiada.
4. Si es format markdown, fes que sigui visualment clar.
5. Si es format JSON, ha de ser JSON valid sense text fora.
"""


def generate_one(model_name, text_obj, perfil, tipus, idx, total):
    text_id = text_obj["id"]
    perfil_id = perfil["id"]
    tipus_id = tipus["id"]

    print(f"  [{idx:3d}/{total}] {model_name}/{tipus_id}/{perfil_id}/{text_id}...", end=" ", flush=True)

    sys_prompt = build_system_prompt(text_obj["text"], perfil, tipus)
    user_text = f"TEXT ORIGINAL:\n\n{text_obj['text']}"

    try:
        t0 = time.time()
        result = CALLERS[model_name](sys_prompt, user_text)
        t = round(time.time() - t0, 1)
        print(f"OK ({t}s)")
    except Exception as e:
        result = f"ERROR: {str(e)[:150]}"
        t = 0
        print(f"ERR")

    # Pacing per groq
    if model_name == "llama":
        time.sleep(3)
    else:
        time.sleep(0.3)

    return {
        "case_id": f"{tipus_id}_{perfil_id}_{text_id}",
        "model_generador": model_name,
        "tipus_complement": tipus_id,
        "perfil_id": perfil_id,
        "text_id": text_id,
        "etapa": text_obj["etapa"],
        "materia": text_obj["materia"],
        "mecr": perfil["mecr"],
        "text_original": text_obj["text"],
        "complement_generat": result,
        "temps_s": t,
        "timestamp": datetime.now().isoformat(),
    }


def main(model_name):
    if model_name not in CALLERS:
        print(f"Model desconegut: {model_name}. Opcions: {list(CALLERS.keys())}")
        sys.exit(1)

    output_path = EXP_DIR / f"resultats_complements_{model_name}.json"

    print("=" * 60)
    print(f"EXPERIMENT COMPLEMENTS - {model_name.upper()}")
    print("=" * 60)

    textos = json.loads(TEXTOS_PATH.read_text(encoding="utf-8"))
    perfils = json.loads(PERFILS_PATH.read_text(encoding="utf-8"))
    perfils_map = {p["id"]: p for p in perfils}
    tipus_list = json.loads(TIPUS_PATH.read_text(encoding="utf-8"))

    # Construir totes les combinacions valides
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

    # Recuperar resultats existents (nomes OK)
    resultats = []
    done = set()
    if output_path.exists():
        existing = json.loads(output_path.read_text(encoding="utf-8"))
        resultats = [r for r in existing.get("casos", [])
                     if not str(r.get("complement_generat", "")).startswith("ERROR")]
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
                "experiment": f"complements_{model_name}",
                "model": model_name,
                "data": datetime.now().isoformat(),
                "total_casos": len(resultats),
                "casos": resultats,
            }
            output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    output = {
        "experiment": f"complements_{model_name}",
        "model": model_name,
        "data": datetime.now().isoformat(),
        "total_casos": len(resultats),
        "casos": resultats,
    }
    output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    err = sum(1 for r in resultats if str(r.get("complement_generat", "")).startswith("ERROR"))
    print(f"\nCOMPLETAT: {len(resultats)} casos, errors: {err}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("model", choices=["gpt4o-mini", "mistral", "llama", "gemma"])
    args = parser.parse_args()
    main(args.model)
