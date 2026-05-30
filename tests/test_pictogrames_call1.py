"""
tests/test_pictogrames_call1.py — Reproducció focalitzada del bug "pictogrames absents".

Aïlla la 1a crida (adapter) de /api/adapt: construeix el system prompt amb
build_system_prompt(adapter_only=True) i el dispara amb un text font fix. Així
mesurem NOMÉS si l'LLM emet marcadors `[PICTO: terme]` dins de `## Text adaptat`,
sense la variància/cost de la 2a crida ni de la resolució ARASAAC (HTTP).

Criteri d'èxit per cas amb pictogrames=true:
  - apareix ≥ MIN_MARKERS marcadors `[PICTO:` dins de la secció `## Text adaptat`.

Bug que reproduïm: pictogrames=true demanat però call 1 no rep cap instrucció
de pictogrames i emet 0 marcadors → cap pictograma a la sortida final.

Execució:
  python tests/test_pictogrames_call1.py            # els 4 casos per defecte
  python tests/test_pictogrames_call1.py ex_di      # subconjunt
  python tests/test_pictogrames_call1.py --repeat 2 # mesurar estabilitat
"""
from __future__ import annotations

import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
except ImportError:
    pass

import yaml

import server
from adaptation.prompt_builder import build_system_prompt
from adaptation.llm_clients import _call_llm
from adaptation.post_process import clean_gemini_output, _post_process_llm_output

CASES_YAML = ROOT / "tests" / "golden" / "cases.yaml"

# Casos diana: 4 cas amb pictogrames=true on Fase B va detectar 0 pictos a la
# sortida (ex_di, ex_l2, ex_pri) o pocs (ex_inf). ex_inf serveix com a control:
# té MULTIMODALITAT al catàleg via nouvingut → ja en feia 3 abans del fix.
DEFAULT_CASE_IDS = ["ex_di", "ex_inf", "ex_l2", "ex_pri"]

MIN_MARKERS = 1  # almenys 1 marcador a ## Text adaptat per considerar OK

# Text font fix: paràgraf de ciències amb conceptes visualitzables (sol, aigua,
# planta, oxigen) i un parell de tecnicismes (clorofil·la, glucosa).
SAMPLE_TEXT = """La fotosíntesi és el procés que fan les plantes per fabricar
el seu aliment. Les plantes capten la llum del sol amb les fulles. També
necessiten aigua i diòxid de carboni de l'aire. Dins de les cèl·lules, la
clorofil·la, que és verda, fa la reacció.

El resultat és la glucosa (sucre) i l'oxigen, que les plantes alliberen a
l'aire. Per això sense fotosíntesi no hi hauria oxigen per respirar."""


def load_cases() -> dict:
    return {c["id"]: c for c in yaml.safe_load(CASES_YAML.read_text(encoding="utf-8"))["casos"]}


def extract_text_adaptat(clean: str) -> str | None:
    """Retorna el cos de la secció `## Text adaptat` (fins al següent `## `)."""
    m = re.search(r'^## Text adaptat\b[^\n]*$', clean, re.MULTILINE)
    if not m:
        return None
    nxt = re.search(r'^## ', clean[m.end():], re.MULTILINE)
    end = m.end() + nxt.start() if nxt else len(clean)
    return clean[m.start():end]


def run_case(case: dict) -> dict:
    cid = case["id"]
    profile = case["profile"]
    params = case["params"]
    ctx = {"etapa": params.get("etapa", "ESO"), "materia": "ciències naturals"}
    system = build_system_prompt(profile, ctx, params, adapter_only=True)
    # NOTA: la clau correcta és "adapt" (sense "er") — _MODEL_CONFIG mapeja
    # "adapt"→gpt-4o; "adapter" no existeix i cauria a ATNE_MODEL (gemma4),
    # cosa que NO és la del pipeline de producció.
    model = server._model_for("adapt")
    raw = _call_llm(model, system, SAMPLE_TEXT)
    clean = _post_process_llm_output(clean_gemini_output(raw), lang="ca")
    sec = extract_text_adaptat(clean)
    if sec is None:
        return {"id": cid, "ok": False, "reason": "no ## Text adaptat", "markers": 0, "model": model}
    markers = len(re.findall(r'\[PICTO:', sec))
    emojis = len(re.findall(r'[\U0001F300-\U0001F6FF\U0001F900-\U0001F9FF]', sec))
    ok = markers >= MIN_MARKERS
    return {
        "id": cid, "ok": ok, "markers": markers, "emojis": emojis,
        "text_chars": len(sec), "text_excerpt": sec[:600],
        "model": model,
        "reason": "OK" if ok else f"0 marcadors [PICTO:] (emojis trobats={emojis})",
    }


def main():
    argv = sys.argv[1:]
    repeat = 1
    if "--repeat" in argv:
        i = argv.index("--repeat")
        repeat = int(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    ids = argv or DEFAULT_CASE_IDS
    cases = load_cases()

    per_case = {cid: {"ok": 0, "n": 0, "last": None, "model": None} for cid in ids if cid in cases}
    for rep in range(repeat):
        for cid in ids:
            if cid not in cases:
                print(f"[skip] {cid}")
                continue
            tag = cid + (f" (rep {rep+1}/{repeat})" if repeat > 1 else "")
            print(f"[run] {tag} … ", end="", flush=True)
            try:
                r = run_case(cases[cid])
            except Exception as e:
                r = {"id": cid, "ok": False, "reason": f"EXCEPCIÓ: {type(e).__name__}: {e}", "markers": 0}
            per_case[cid]["n"] += 1
            per_case[cid]["ok"] += 1 if r.get("ok") else 0
            per_case[cid]["model"] = r.get("model")
            per_case[cid]["last"] = r
            icon = "✅" if r.get("ok") else "❌"
            print(f"{icon} markers={r.get('markers',0)} emojis={r.get('emojis',0)}  ({r.get('reason')})")

    print("\n" + "=" * 70)
    total_ok = sum(c["ok"] for c in per_case.values())
    total_n = sum(c["n"] for c in per_case.values())
    print(f"RESULTAT GLOBAL: {total_ok}/{total_n} execucions amb [PICTO:] inline")
    for cid, c in per_case.items():
        print(f"  - {cid}: {c['ok']}/{c['n']}")
    print("=" * 70)
    for cid, c in per_case.items():
        if c.get("last", {}).get("text_excerpt"):
            print(f"\n----- {cid} ({c['model']}) -----")
            print(c["last"]["text_excerpt"])
    sys.exit(0 if total_ok == total_n and total_n > 0 else 1)


if __name__ == "__main__":
    main()
