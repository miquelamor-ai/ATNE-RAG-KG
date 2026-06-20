#!/usr/bin/env python3
"""
Peça 4 — Avaluació de l'experiment A/B skills OFF vs ON
Jutge ÚNIC: Claude Sonnet 4.6 (via OpenRouter) — DIFERENT del generador (Gemini Lite), obligatori.
Cada condició (OFF/ON) s'avalua amb la mateixa rúbrica de 5 criteris, puntuació 1-5.

Verificació pre-execució: comprova que l'slug JUDGE_MODEL existeix realment a OpenRouter
abans de gastar cap crida d'avaluació (no s'avalua si l'slug no és vàlid).
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

import requests

# ── Jutge ──
JUDGE_MODEL = "anthropic/claude-sonnet-4.6"   # Sonnet 4.6 — diferent del generador
JUDGE_TEMPERATURE = 0.1                        # quasi determinístic per avaluació


class JudgeAuthError(Exception):
    """Error d'autenticació del jutge (HTTP 401/403). Avorta tot el pas: si la clau
    no és vàlida, totes les crides fallaran i no té sentit generar un informe buit."""

# ── Paths ──
EXP_DIR = Path(__file__).resolve().parent
RESULTATS_PATH = EXP_DIR / "resultats_generacio.json"
RUBRICA_PATH = EXP_DIR / "rubrica.json"
PERFILS_PATH = EXP_DIR / "perfils.json"
EVAL_OUTPUT_PATH = EXP_DIR / "resultats_avaluacio.json"

CRITERIS_IDS = [
    "adequacio_linguistica", "fidelitat_curricular", "adequacio_perfil",
    "llegibilitat_estructura", "complements",
]


def verify_judge_slug():
    """Comprova que JUDGE_MODEL existeix a OpenRouter. Atura si no hi és (no gasta crides)."""
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        raise RuntimeError("No OPENROUTER_API_KEY al .env")
    try:
        r = requests.get("https://openrouter.ai/api/v1/models", timeout=30)
        r.raise_for_status()
        ids = {m["id"] for m in r.json().get("data", [])}
    except Exception as e:
        print(f"⚠️  No s'ha pogut verificar l'slug a OpenRouter ({e}).")
        print(f"   Comprova manualment que '{JUDGE_MODEL}' és vàlid abans de continuar.")
        raise
    if JUDGE_MODEL not in ids:
        cands = sorted(i for i in ids if "claude" in i and "sonnet" in i)
        raise RuntimeError(
            f"L'slug '{JUDGE_MODEL}' NO existeix a OpenRouter.\n"
            f"Slugs Sonnet disponibles: {cands}\n"
            f"Edita JUDGE_MODEL a eval_experiment.py amb l'slug correcte."
        )
    print(f"✓ Jutge verificat a OpenRouter: {JUDGE_MODEL}")


def load_rubrica() -> dict:
    return json.loads(RUBRICA_PATH.read_text(encoding="utf-8"))


def build_eval_prompt(rubrica: dict, original: str, adapted: str, perfil_desc: str, mecr: str) -> str:
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


def call_judge(prompt: str) -> dict:
    """Avalua amb Claude Sonnet 4.6 via OpenRouter."""
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        raise RuntimeError("No OPENROUTER_API_KEY al .env")
    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={
            "model": JUDGE_MODEL,
            "messages": [{"role": "user", "content": f"{prompt}\n\n---\n\nAvalua el text adaptat anterior."}],
            "max_tokens": 2000,
            "temperature": JUDGE_TEMPERATURE,
        },
        timeout=120,
    )
    if r.status_code in (401, 403):
        # Error d'autenticació: no té sentit continuar (totes les crides fallaran).
        raise JudgeAuthError(f"OpenRouter HTTP {r.status_code}: {r.text[:200]}")
    if r.status_code != 200:
        raise RuntimeError(f"OpenRouter HTTP {r.status_code}: {r.text[:200]}")
    raw = r.json()["choices"][0]["message"]["content"]
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0]
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0]
    return json.loads(raw.strip())


def evaluate_case(case: dict, rubrica: dict, perfils_map: dict) -> dict:
    case_id = case["case_id"]
    original = case["original"]
    mecr = case["mecr"]
    perfil_obj = perfils_map.get(case_id, {})
    perfil_desc = perfil_obj.get("descripcio_curta", case_id)

    result_off = case["condicio_OFF"]["resultat"]
    result_on = case["condicio_ON"]["resultat"]

    if result_off.startswith("ERROR") or result_on.startswith("ERROR"):
        return None

    evaluations = {}
    for cond, adapted_text in [("OFF", result_off), ("ON", result_on)]:
        eval_prompt = build_eval_prompt(rubrica, original, adapted_text, perfil_desc, mecr)
        try:
            evaluations[cond] = call_judge(eval_prompt)
            time.sleep(0.5)
        except JudgeAuthError:
            raise  # error d'auth: NO l'engolim, ha d'avortar tot el pas (no informe buit silenciós)
        except Exception as e:
            evaluations[cond] = {"error": str(e)}

    return {
        "case_id": case_id,
        "text_id": case["text_id"],
        "perfil_id": case["perfil_id"],
        "genere": case.get("genere", ""),
        "mecr": mecr,
        "skills_actives_ON": case.get("skills_actives_ON", []),
        "evaluations": evaluations,
        "timestamp": datetime.now().isoformat(),
    }


def main():
    print("=" * 60)
    print("PEÇA 4 — Avaluació amb Claude Sonnet 4.6 (jutge únic)")
    print("=" * 60)

    verify_judge_slug()  # atura si l'slug no és vàlid (abans de gastar crides)

    rubrica = load_rubrica()
    resultats = json.loads(RESULTATS_PATH.read_text(encoding="utf-8"))
    perfils = json.loads(PERFILS_PATH.read_text(encoding="utf-8"))
    perfils_map = {p["id"]: p for p in perfils}

    casos = resultats["casos"]
    print(f"Casos a avaluar: {len(casos)}")

    evals, done_ids = [], set()
    if EVAL_OUTPUT_PATH.exists():
        try:
            existing = json.loads(EVAL_OUTPUT_PATH.read_text(encoding="utf-8"))
            # Només recupera avaluacions d'AQUEST experiment (amb 'case_id'); ignora
            # formats antics incompatibles (p.ex. xat9 amb 'pair_id').
            evals = [e for e in existing.get("avaluacions", []) if "case_id" in e]
            done_ids = {e["case_id"] for e in evals}
            if evals:
                print(f"Recuperades {len(evals)} avaluacions existents.")
            else:
                print("Fitxer d'avaluació previ incompatible o buit — es regenera.")
        except Exception as e:
            print(f"No s'ha pogut llegir l'avaluació prèvia ({e}) — es regenera.")

    for i, case in enumerate(casos, 1):
        if case["case_id"] in done_ids:
            continue
        print(f"[{i}/{len(casos)}] {case['case_id']}...", end=" ", flush=True)
        try:
            result = evaluate_case(case, rubrica, perfils_map)
        except JudgeAuthError as e:
            print("✗")
            print("\n" + "=" * 60, file=sys.stderr)
            print("ERROR D'AUTENTICACIÓ DEL JUTGE — s'avorta l'avaluació.", file=sys.stderr)
            print(f"  {e}", file=sys.stderr)
            print("  La OPENROUTER_API_KEY del .env no és vàlida (401/403).", file=sys.stderr)
            print("  Cap informe generat: arregla la clau i torna a executar.", file=sys.stderr)
            print("=" * 60, file=sys.stderr)
            sys.exit(2)
        if result is None:
            print("SKIP (error en generació)")
            continue
        evals.append(result)
        print("✓")
        _save(evals)

    _save(evals)
    print(f"\nCOMPLETAT: {len(evals)} casos avaluats")
    print(f"Fitxer: {EVAL_OUTPUT_PATH}")


def _atomic_write(path: Path, text: str, retries: int = 5):
    """Escriptura atòmica amb reintents (evita PermissionError per locks transitoris Windows)."""
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


def _save(evals):
    output = {
        "experiment": "peca4_avaluacio_skills_off_vs_on",
        "jutge": JUDGE_MODEL,
        "data": datetime.now().isoformat(),
        "total_avaluacions": len(evals),
        "avaluacions": evals,
    }
    _atomic_write(EVAL_OUTPUT_PATH, json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
