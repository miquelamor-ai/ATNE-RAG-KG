#!/usr/bin/env python3
"""
Eval Questions - 5 jutges (GPT-4o, Gemini Flash, Qwen, Llama, Mistral) amb exclusio auto-avaluacio.
"""
import json, os, sys, time, io, requests
from pathlib import Path
from datetime import datetime

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from dotenv import load_dotenv
load_dotenv()

EXP_DIR = Path(__file__).resolve().parent
RUBRICA_PATH = EXP_DIR / "rubrica.json"
PERFILS_PATH = EXP_DIR / "perfils.json"
TIPUS_PATH = EXP_DIR / "tipus_questions.json"
OUTPUT_PATH = EXP_DIR / "resultats_avaluacio_questions.json"

GEMINI_KEYS = [v for k, v in sorted(os.environ.items()) if k.startswith("GEMINI_API_KEY")]
GROQ_KEYS = [v for k, v in sorted(os.environ.items()) if k.startswith("GROQ_API_KEY")]
MISTRAL_KEY = os.getenv("MISTRAL_API_KEY")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
_gemini_idx = 0
_groq_idx = 0


def parse_json_response(raw):
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0]
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0]
    return json.loads(raw.strip())


def call_gpt4o(prompt, text_to_eval):
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_KEY)
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


def call_gemini_flash(prompt, text_to_eval):
    global _gemini_idx
    from google import genai
    from google.genai import types
    errors = []
    for attempt in range(len(GEMINI_KEYS)):
        idx = (_gemini_idx + attempt) % len(GEMINI_KEYS)
        try:
            client = genai.Client(api_key=GEMINI_KEYS[idx], http_options=types.HttpOptions(timeout=120_000))
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[types.Content(role="user", parts=[types.Part(text=f"{prompt}\n\n---\n\n{text_to_eval}")])],
                config=types.GenerateContentConfig(temperature=0.1, max_output_tokens=2000, thinking_config=types.ThinkingConfig(thinking_budget=0)),
            )
            _gemini_idx = (idx + 1) % len(GEMINI_KEYS)
            return parse_json_response(response.text or "")
        except Exception as e:
            errors.append(f"c{idx+1}:{str(e)[:40]}")
            time.sleep(1)
    raise RuntimeError(f"Gemini fail: {'; '.join(errors[:3])}")


def call_qwen_judge(prompt, text_to_eval):
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
                    "messages": [{"role": "system", "content": prompt}, {"role": "user", "content": text_to_eval}],
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
    raise RuntimeError(f"Qwen fail: {'; '.join(errors)}")


def call_llama_judge(prompt, text_to_eval):
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
                    "messages": [{"role": "system", "content": prompt}, {"role": "user", "content": text_to_eval}],
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
    raise RuntimeError(f"Llama fail: {'; '.join(errors)}")


def call_mistral_judge(prompt, text_to_eval):
    last_err = None
    for attempt in range(3):
        try:
            r = requests.post(
                "https://api.mistral.ai/v1/chat/completions",
                headers={"Authorization": f"Bearer {MISTRAL_KEY}", "Content-Type": "application/json"},
                json={
                    "model": "mistral-small-latest",
                    "messages": [{"role": "system", "content": prompt}, {"role": "user", "content": text_to_eval}],
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
    raise RuntimeError(f"Mistral fail: {last_err}")


JUDGES = {
    "gpt4o": call_gpt4o,
    "gemini_flash": call_gemini_flash,
    "qwen_judge": call_qwen_judge,
    "llama_judge": call_llama_judge,
    "mistral_judge": call_mistral_judge,
}

SELF_EXCLUDE = {
    "llama": "llama_judge",
    "mistral": "mistral_judge",
}


def build_eval_prompt(rubrica, preguntes_raw, perfil_desc, mecr, tipus_nom, text_original):
    criteris_text = ""
    for c in rubrica["criteris"]:
        criteris_text += f"\n### {c['nom']} (pes: {c['pes']})\n"
        for score, desc in c["descriptors"].items():
            criteris_text += f"  {score}: {desc}\n"

    return f"""{rubrica['instruccions_jutge']}

## Perfil de l'alumne
{perfil_desc}
Nivell MECR: {mecr}

## Tipus de preguntes avaluades
{tipus_nom}

## Criteris d'avaluació
{criteris_text}

## Text original (sobre el qual s'han generat les preguntes)
{text_original}

## Preguntes generades a avaluar
{preguntes_raw}

## Format de resposta
Respon EXACTAMENT en JSON valid sense text fora:
{{
  "validesa_pedagogica": {{"puntuacio": X, "justificacio": "..."}},
  "adequacio_nivell": {{"puntuacio": X, "justificacio": "..."}},
  "discriminacio": {{"puntuacio": X, "justificacio": "..."}},
  "originalitat_redaccio": {{"puntuacio": X, "justificacio": "..."}},
  "format_estructural": {{"puntuacio": X, "justificacio": "..."}}
}}
"""


def main():
    print("=" * 60)
    print("EVAL QUESTIONS - 5 jutges")
    print("=" * 60)

    rubrica = json.loads(RUBRICA_PATH.read_text(encoding="utf-8"))
    perfils = json.loads(PERFILS_PATH.read_text(encoding="utf-8"))
    perfils_map = {p["id"]: p for p in perfils}
    tipus_list = json.loads(TIPUS_PATH.read_text(encoding="utf-8"))
    tipus_map = {t["id"]: t for t in tipus_list}

    all_cases = []
    for model in ["gpt4o-mini", "mistral", "llama", "gemma"]:
        f = EXP_DIR / f"resultats_questions_{model}.json"
        if f.exists():
            d = json.load(open(f, "r", encoding="utf-8"))
            for c in d.get("casos", []):
                if not str(c.get("preguntes_raw", "")).startswith("ERROR"):
                    all_cases.append(c)
            print(f"  {model}: {len(d.get('casos', []))} casos carregats")

    print(f"\nTotal casos valids: {len(all_cases)}")

    if OUTPUT_PATH.exists():
        existing = json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))
        evals = existing.get("avaluacions", [])
        done = {(e["case_id"], e["model_generador"]) for e in evals}
        print(f"Recuperades {len(evals)} avaluacions existents")
    else:
        evals = []
        done = set()

    for i, case in enumerate(all_cases):
        model_gen = case["model_generador"]
        key = (case["case_id"], model_gen)

        excluded = SELF_EXCLUDE.get(model_gen)
        applicable = [j for j in JUDGES if j != excluded]

        existing_eval = None
        for e in evals:
            if (e["case_id"], e["model_generador"]) == key:
                existing_eval = e
                break

        if existing_eval:
            judges_done = set(existing_eval["evaluations"].keys())
            judges_to_use = [j for j in applicable if j not in judges_done]
            if not judges_to_use:
                continue
        else:
            judges_to_use = applicable

        perfil = perfils_map[case["perfil_id"]]
        tipus = tipus_map[case["tipus_question"]]

        eval_prompt = build_eval_prompt(
            rubrica,
            case["preguntes_raw"],
            perfil["descripcio_curta"],
            case["mecr"],
            tipus["nom"],
            case["text_original"],
        )

        print(f"[{i+1}/{len(all_cases)}] {model_gen}/{case['case_id']} ({len(judges_to_use)}j)...", end=" ", flush=True)

        new_evals = {}
        for jutge_name in judges_to_use:
            try:
                result = JUDGES[jutge_name](eval_prompt, "Avalua les preguntes.")
                new_evals[jutge_name] = result
                time.sleep(0.3)
            except Exception as e:
                new_evals[jutge_name] = {"error": str(e)[:200]}

        if existing_eval:
            existing_eval["evaluations"].update(new_evals)
            existing_eval["timestamp"] = datetime.now().isoformat()
        else:
            evals.append({
                "case_id": case["case_id"],
                "model_generador": model_gen,
                "tipus_question": case["tipus_question"],
                "perfil_id": case["perfil_id"],
                "text_id": case["text_id"],
                "etapa": case.get("etapa", "?"),
                "mecr": case["mecr"],
                "json_valid": case.get("json_valid", False),
                "n_preguntes": case.get("n_preguntes", 0),
                "evaluations": new_evals,
                "timestamp": datetime.now().isoformat(),
            })

        print("OK")

        if (i + 1) % 5 == 0:
            output = {
                "experiment": "questions_eval_multi",
                "jutges": list(JUDGES.keys()),
                "data": datetime.now().isoformat(),
                "total_avaluacions": len(evals),
                "avaluacions": evals,
            }
            OUTPUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    output = {
        "experiment": "questions_eval_multi",
        "jutges": list(JUDGES.keys()),
        "data": datetime.now().isoformat(),
        "total_avaluacions": len(evals),
        "avaluacions": evals,
    }
    OUTPUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nCOMPLETAT: {len(evals)} avaluacions")


if __name__ == "__main__":
    main()
