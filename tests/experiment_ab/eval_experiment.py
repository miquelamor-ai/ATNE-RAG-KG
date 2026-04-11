#!/usr/bin/env python3
"""
Xat 9 — Avaluació dual de l'experiment A/B
Jutges: GPT-4o + Claude Sonnet 4.6
Cada jutge avalua cec (no sap si és condició A o B).
Rúbrica de 5 criteris, puntuació 1-5.
"""

import json, os, sys, time, random, io
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from dotenv import load_dotenv
load_dotenv()

# ── Paths ──
EXP_DIR = Path(__file__).resolve().parent
RESULTATS_PATH = EXP_DIR / "resultats_generacio.json"
RUBRICA_PATH = EXP_DIR / "rubrica.json"
PERFILS_PATH = EXP_DIR / "perfils.json"
EVAL_OUTPUT_PATH = EXP_DIR / "resultats_avaluacio.json"


def load_rubrica() -> dict:
    return json.loads(RUBRICA_PATH.read_text(encoding="utf-8"))


def build_eval_prompt(rubrica: dict, original: str, adapted: str, perfil_desc: str, mecr: str) -> str:
    """Construeix el prompt d'avaluació per al jutge."""
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
Respon EXACTAMENT en JSON vàlid amb aquesta estructura (sense cap text addicional fora del JSON):
{{
  "adequacio_linguistica": {{"puntuacio": X, "justificacio": "..."}},
  "fidelitat_curricular": {{"puntuacio": X, "justificacio": "..."}},
  "adequacio_perfil": {{"puntuacio": X, "justificacio": "..."}},
  "llegibilitat_estructura": {{"puntuacio": X, "justificacio": "..."}},
  "complements": {{"puntuacio": X, "justificacio": "..."}}
}}
On X és un enter de 1 a 5. Sigues rigorós.
"""


def call_gpt4o(prompt: str, text_to_eval: str) -> dict:
    """Avalua amb GPT-4o."""
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text_to_eval},
        ],
        max_tokens=2000,
        temperature=0.1,  # quasi determinístic per avaluació
        response_format={"type": "json_object"},
    )
    raw = resp.choices[0].message.content
    return json.loads(raw)


def call_claude_sonnet(prompt: str, text_to_eval: str) -> dict:
    """Avalua amb Claude Sonnet via OpenRouter (no tenim ANTHROPIC_API_KEY directa)."""
    import requests
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    if not openrouter_key:
        raise RuntimeError("No OPENROUTER_API_KEY found")

    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {openrouter_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "anthropic/claude-sonnet-4",
            "messages": [
                {"role": "user", "content": f"{prompt}\n\n---\n\n{text_to_eval}"},
            ],
            "max_tokens": 2000,
            "temperature": 0.1,
        },
        timeout=120,
    )
    if r.status_code != 200:
        raise RuntimeError(f"OpenRouter HTTP {r.status_code}: {r.text[:200]}")

    raw = r.json()["choices"][0]["message"]["content"]
    # Extreure JSON del text (pot venir amb backticks)
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0]
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0]
    return json.loads(raw.strip())


def evaluate_pair(pair: dict, rubrica: dict, perfils_map: dict) -> dict:
    """Avalua un parell A/B amb els dos jutges."""
    pair_id = pair["pair_id"]
    original = pair["original"]
    perfil_id = pair["perfil_id"]
    mecr = pair["mecr"]
    perfil_obj = perfils_map[perfil_id]
    perfil_desc = perfil_obj["descripcio_curta"]

    result_a = pair["condicio_A"]["resultat"]
    result_b = pair["condicio_B"]["resultat"]

    # Saltar parells amb errors
    if result_a.startswith("ERROR") or result_b.startswith("ERROR"):
        return None

    # Avaluació CEGA — l'ordre és aleatori per evitar biaix posicional
    # Però registrem quin és A i quin és B
    evaluations = {}

    for condicio, adapted_text in [("A", result_a), ("B", result_b)]:
        eval_prompt = build_eval_prompt(rubrica, original, adapted_text, perfil_desc, mecr)

        # ── GPT-4o ──
        try:
            gpt_eval = call_gpt4o(eval_prompt, f"Avalua el text adaptat anterior.")
            time.sleep(0.5)
        except Exception as e:
            gpt_eval = {"error": str(e)}

        # ── Claude Sonnet ──
        try:
            claude_eval = call_claude_sonnet(eval_prompt, f"Avalua el text adaptat anterior.")
            time.sleep(0.5)
        except Exception as e:
            claude_eval = {"error": str(e)}

        evaluations[condicio] = {
            "gpt4o": gpt_eval,
            "claude_sonnet": claude_eval,
        }

    return {
        "pair_id": pair_id,
        "text_id": pair["text_id"],
        "perfil_id": perfil_id,
        "etapa": pair["etapa"],
        "mecr": mecr,
        "evaluations": evaluations,
        "timestamp": datetime.now().isoformat(),
    }


def main():
    print("=" * 60)
    print("XAT 9 — Avaluació dual: GPT-4o + Claude Sonnet")
    print("=" * 60)

    rubrica = load_rubrica()
    resultats = json.loads(RESULTATS_PATH.read_text(encoding="utf-8"))
    perfils = json.loads(PERFILS_PATH.read_text(encoding="utf-8"))
    perfils_map = {p["id"]: p for p in perfils}

    parells = resultats["parells"]
    print(f"Parells a avaluar: {len(parells)}")

    # Recuperar avaluacions existents
    if EVAL_OUTPUT_PATH.exists():
        existing = json.loads(EVAL_OUTPUT_PATH.read_text(encoding="utf-8"))
        evals = existing.get("avaluacions", [])
        done_ids = {e["pair_id"] for e in evals}
        print(f"Recuperades {len(evals)} avaluacions existents.")
    else:
        evals = []
        done_ids = set()

    for i, pair in enumerate(parells):
        if pair["pair_id"] in done_ids:
            continue

        print(f"[{i+1}/{len(parells)}] {pair['pair_id']}...", end=" ", flush=True)

        result = evaluate_pair(pair, rubrica, perfils_map)
        if result is None:
            print("SKIP (error en generació)")
            continue

        evals.append(result)
        print("✓")

        # Guardar cada 5
        if len(evals) % 5 == 0:
            output = {
                "experiment": "xat9_avaluacio_dual",
                "jutges": ["gpt-4o", "claude-sonnet-4"],
                "data": datetime.now().isoformat(),
                "total_avaluacions": len(evals),
                "avaluacions": evals,
            }
            EVAL_OUTPUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    # Final
    output = {
        "experiment": "xat9_avaluacio_dual",
        "jutges": ["gpt-4o", "claude-sonnet-4"],
        "data": datetime.now().isoformat(),
        "total_avaluacions": len(evals),
        "avaluacions": evals,
    }
    EVAL_OUTPUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\nCOMPLETAT: {len(evals)} parells avaluats")
    print(f"Fitxer: {EVAL_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
