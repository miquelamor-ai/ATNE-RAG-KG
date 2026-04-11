#!/usr/bin/env python3
"""
Xat 9 - Avaluacio multi-jutge per a multi-model
3 jutges: GPT-4o, Claude Sonnet (OpenRouter), Gemini 2.5 Flash
4 generadors: gpt4o-mini, mistral, llama (=qwen), gemma

Avalua tots els resultats_generacio_*.json amb els 3 jutges.
Output: resultats_avaluacio_multi.json
"""
import json, os, sys, time, io, requests
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
RUBRICA_PATH = EXP_DIR / "rubrica.json"
PERFILS_PATH = EXP_DIR / "perfils.json"
OUTPUT_PATH = EXP_DIR / "resultats_avaluacio_multi.json"

GEMINI_KEYS = [v for k, v in sorted(os.environ.items()) if k.startswith("GEMINI_API_KEY")]
GROQ_KEYS = [v for k, v in sorted(os.environ.items()) if k.startswith("GROQ_API_KEY")]
MISTRAL_KEY = os.getenv("MISTRAL_API_KEY")
_gemini_idx = 0
_groq_idx = 0


def load_rubrica():
    return json.loads(RUBRICA_PATH.read_text(encoding="utf-8"))


def build_eval_prompt(rubrica, original, adapted, perfil_desc, mecr):
    criteris_text = ""
    for c in rubrica["criteris"]:
        criteris_text += f"\n### {c['nom']} (pes: {c['pes']})\n"
        for score, desc in c["descriptors"].items():
            criteris_text += f"  {score}: {desc}\n"

    return f"""{rubrica['instruccions_jutge']}

## Perfil de l'alumne
{perfil_desc}
Nivell MECR de sortida: {mecr}

## Criteris d'avaluació
{criteris_text}

## Text original
{original}

## Text adaptat a avaluar
{adapted}

## Format de resposta
Respon EXACTAMENT en JSON valid amb aquesta estructura (sense cap text addicional fora del JSON):
{{
  "adequacio_linguistica": {{"puntuacio": X, "justificacio": "..."}},
  "fidelitat_curricular": {{"puntuacio": X, "justificacio": "..."}},
  "adequacio_perfil": {{"puntuacio": X, "justificacio": "..."}},
  "llegibilitat_estructura": {{"puntuacio": X, "justificacio": "..."}},
  "complements": {{"puntuacio": X, "justificacio": "..."}}
}}
On X es un enter de 1 a 5. Sigues rigoros.
"""


def parse_json_response(raw):
    """Extreu JSON de resposta amb possible markdown."""
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0]
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0]
    return json.loads(raw.strip())


def call_gpt4o(prompt, text_to_eval):
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text_to_eval},
        ],
        max_tokens=2000, temperature=0.1,
        response_format={"type": "json_object"},
    )
    return json.loads(resp.choices[0].message.content)


def call_qwen_judge(prompt, text_to_eval):
    """Qwen 3 32B via Groq com a jutge. Retry rapid, max 3 claus."""
    global _groq_idx
    errors = []
    for attempt in range(min(3, len(GROQ_KEYS))):
        idx = (_groq_idx + attempt) % len(GROQ_KEYS)
        try:
            r = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ_KEYS[idx]}", "Content-Type": "application/json"},
                json={
                    "model": "qwen/qwen3-32b",
                    "messages": [
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": text_to_eval},
                    ],
                    "max_tokens": 2000, "temperature": 0.1,
                    "response_format": {"type": "json_object"},
                },
                timeout=60,
            )
            if r.status_code == 200:
                _groq_idx = (idx + 1) % len(GROQ_KEYS)
                return parse_json_response(r.json()["choices"][0]["message"]["content"])
            errors.append(f"c{idx+1}:HTTP{r.status_code}")
            time.sleep(2)
        except Exception as e:
            errors.append(f"c{idx+1}:{str(e)[:40]}")
            time.sleep(2)
    raise RuntimeError(f"Qwen judge fail: {'; '.join(errors)}")


def call_gemini_flash(prompt, text_to_eval):
    """Gemini 2.5 Flash via Google API (rotacio claus)."""
    global _gemini_idx
    from google import genai
    from google.genai import types
    errors = []
    for attempt in range(len(GEMINI_KEYS)):
        idx = (_gemini_idx + attempt) % len(GEMINI_KEYS)
        try:
            client = genai.Client(
                api_key=GEMINI_KEYS[idx],
                http_options=types.HttpOptions(timeout=120_000),
            )
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[types.Content(role="user", parts=[types.Part(text=f"{prompt}\n\n---\n\n{text_to_eval}")])],
                config=types.GenerateContentConfig(
                    temperature=0.1, max_output_tokens=2000,
                    thinking_config=types.ThinkingConfig(thinking_budget=0),
                ),
            )
            _gemini_idx = (idx + 1) % len(GEMINI_KEYS)
            return parse_json_response(response.text or "")
        except Exception as e:
            errors.append(f"clau{idx+1}: {str(e)[:50]}")
            time.sleep(1)
    raise RuntimeError(f"Totes les claus Gemini han fallat: {'; '.join(errors[:3])}")


def call_llama_judge(prompt, text_to_eval):
    """Llama 3.3 70B via Groq com a jutge. Retry rapid, max 3 claus."""
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
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": text_to_eval},
                    ],
                    "max_tokens": 2000, "temperature": 0.1,
                    "response_format": {"type": "json_object"},
                },
                timeout=60,
            )
            if r.status_code == 200:
                _groq_idx = (idx + 1) % len(GROQ_KEYS)
                return parse_json_response(r.json()["choices"][0]["message"]["content"])
            errors.append(f"c{idx+1}:HTTP{r.status_code}")
            time.sleep(2)
        except Exception as e:
            errors.append(f"c{idx+1}:{str(e)[:40]}")
            time.sleep(2)
    raise RuntimeError(f"Llama judge fail: {'; '.join(errors)}")


def call_mistral_judge(prompt, text_to_eval):
    """Mistral Small com a jutge, retries rapids."""
    last_err = None
    for attempt in range(3):
        try:
            r = requests.post(
                "https://api.mistral.ai/v1/chat/completions",
                headers={"Authorization": f"Bearer {MISTRAL_KEY}", "Content-Type": "application/json"},
                json={
                    "model": "mistral-small-latest",
                    "messages": [
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": text_to_eval},
                    ],
                    "max_tokens": 2000, "temperature": 0.1,
                    "response_format": {"type": "json_object"},
                },
                timeout=60,
            )
            if r.status_code == 200:
                return parse_json_response(r.json()["choices"][0]["message"]["content"])
            last_err = f"HTTP{r.status_code}"
            time.sleep(3)
        except Exception as e:
            last_err = str(e)[:60]
            time.sleep(3)
    raise RuntimeError(f"Mistral judge fail: {last_err}")


JUDGES = {
    "gpt4o": call_gpt4o,
    "qwen_judge": call_qwen_judge,      # Open-source, substitueix Sonnet per falta credits OpenRouter
    "gemini_flash": call_gemini_flash,
    "llama_judge": call_llama_judge,    # Open-source (amb exclusio auto-avaluacio Llama->Llama)
    "mistral_judge": call_mistral_judge, # Open-source (amb exclusio auto-avaluacio Mistral->Mistral)
}

# Exclusio auto-avaluacio: quin model NO pot jutjar les seves propies generacions
SELF_EXCLUDE = {
    "llama": "llama_judge",       # Llama generador no pot ser avaluat per Llama jutge
    "mistral": "mistral_judge",   # Mistral generador no pot ser avaluat per Mistral jutge
}


def evaluate_pair(pair, rubrica, perfils_map, judges_to_use):
    pair_id = pair["pair_id"]
    original = pair["original"]
    perfil_id = pair["perfil_id"]
    mecr = pair["mecr"]
    perfil_obj = perfils_map[perfil_id]
    perfil_desc = perfil_obj["descripcio_curta"]

    result_a = pair["condicio_A"]["resultat"]
    result_b = pair["condicio_B"]["resultat"]

    if str(result_a).startswith("ERROR") or str(result_b).startswith("ERROR"):
        return None

    evaluations = {}

    for condicio, adapted in [("A", result_a), ("B", result_b)]:
        eval_prompt = build_eval_prompt(rubrica, original, adapted, perfil_desc, mecr)
        evaluations[condicio] = {}

        for jutge_name in judges_to_use:
            try:
                eval_data = JUDGES[jutge_name](eval_prompt, "Avalua el text adaptat anterior.")
                evaluations[condicio][jutge_name] = eval_data
                time.sleep(0.3)
            except Exception as e:
                evaluations[condicio][jutge_name] = {"error": str(e)[:200]}

    return {
        "pair_id": pair_id,
        "model_generador": pair.get("model_generador", "gpt-4o-mini"),
        "text_id": pair["text_id"],
        "perfil_id": perfil_id,
        "etapa": pair["etapa"],
        "mecr": mecr,
        "evaluations": evaluations,
        "timestamp": datetime.now().isoformat(),
    }


def main():
    print("=" * 60)
    print("XAT 9 - Avaluacio MULTI-JUTGE i MULTI-MODEL")
    print("=" * 60)

    rubrica = load_rubrica()
    perfils = json.loads(PERFILS_PATH.read_text(encoding="utf-8"))
    perfils_map = {p["id"]: p for p in perfils}

    # Carregar tots els fitxers de generacio
    gen_files = {
        "gpt4o-mini": EXP_DIR / "resultats_generacio.json",
        "mistral": EXP_DIR / "resultats_generacio_mistral.json",
        "llama": EXP_DIR / "resultats_generacio_llama.json",
        "gemma": EXP_DIR / "resultats_generacio_gemma.json",
    }

    all_pairs = []
    for model, path in gen_files.items():
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            for p in data["parells"]:
                p["model_generador"] = model
                # Filtrar errors
                if not str(p["condicio_A"]["resultat"]).startswith("ERROR") and not str(p["condicio_B"]["resultat"]).startswith("ERROR"):
                    all_pairs.append(p)
            print(f"  {model}: {len(data['parells'])} parells carregats")
        else:
            print(f"  {model}: NO existeix {path.name}")

    print(f"\nTotal parells valids: {len(all_pairs)}")

    # Recuperar avaluacions existents
    if OUTPUT_PATH.exists():
        existing = json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))
        evals = existing.get("avaluacions", [])
        # done_keys: (pair_id, model_generador)
        done_keys = {(e["pair_id"], e.get("model_generador", "gpt-4o-mini")) for e in evals}
        print(f"Recuperades {len(evals)} avaluacions existents.")
    else:
        evals = []
        done_keys = set()

    # Per cada pair, decidir quins jutges falten (aplicant exclusio auto-avaluacio)
    for i, pair in enumerate(all_pairs):
        model_gen = pair.get("model_generador", "gpt-4o-mini")
        key = (pair["pair_id"], model_gen)

        # Determinar jutges aplicables per aquest model generador
        excluded_judge = SELF_EXCLUDE.get(model_gen)
        applicable_judges = [j for j in JUDGES if j != excluded_judge]

        # Si ja existeix, comprovar quins jutges falten
        existing_eval = None
        for e in evals:
            if (e["pair_id"], e.get("model_generador", "gpt-4o-mini")) == key:
                existing_eval = e
                break

        if existing_eval:
            judges_done = set(existing_eval["evaluations"].get("A", {}).keys())
            judges_to_use = [j for j in applicable_judges if j not in judges_done]
            if not judges_to_use:
                continue
            print(f"[{i+1}/{len(all_pairs)}] {model_gen}/{key[0]} (afegir {judges_to_use})...", end=" ", flush=True)
        else:
            judges_to_use = applicable_judges
            print(f"[{i+1}/{len(all_pairs)}] {model_gen}/{key[0]} ({len(judges_to_use)} jutges)...", end=" ", flush=True)

        result = evaluate_pair(pair, rubrica, perfils_map, judges_to_use)
        if result is None:
            print("SKIP")
            continue

        if existing_eval:
            # Merge: afegir nous jutges al avaluat existent
            for cond in ["A", "B"]:
                for jutge in judges_to_use:
                    if jutge in result["evaluations"].get(cond, {}):
                        existing_eval["evaluations"][cond][jutge] = result["evaluations"][cond][jutge]
            existing_eval["timestamp"] = result["timestamp"]
        else:
            evals.append(result)

        print("OK")

        if (i + 1) % 5 == 0:
            output = {"experiment": "xat9_multi", "jutges": list(JUDGES.keys()), "data": datetime.now().isoformat(), "total_avaluacions": len(evals), "avaluacions": evals}
            OUTPUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    output = {"experiment": "xat9_multi", "jutges": list(JUDGES.keys()), "data": datetime.now().isoformat(), "total_avaluacions": len(evals), "avaluacions": evals}
    OUTPUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\nCOMPLETAT: {len(evals)} avaluacions")
    print(f"Fitxer: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
