"""
tests/test_bastides_2call.py — Reproducció focalitzada del bug "bastides buides".

Aïlla la 2a crida (complements) de /api/adapt: construeix el system prompt amb
build_complements_prompt() i el dispara contra el model de complements
(gpt-4.1-mini per defecte) amb un TEXT ADAPTAT fix. Així mesurem NOMÉS la
generació de la secció `## Bastides` sense la variància de la 1a crida (adapter).

Criteri d'èxit per cas amb bastides:
  - apareix la capçalera `## Bastides` (o `## Suports per llegir`), i
  - el COS de la secció té contingut substancial (≥ MIN_BODY_LINES línies no buides
    més enllà de la capçalera) — idealment amb els 3 moments (Abans/Durant/Després)
    o, a pre-A1/Accés, accions físiques/gestuals.

El bug que reproduïm: capçalera present + cos buit (0-1 línies).

Execució:
  python tests/test_bastides_2call.py            # els 5 casos per defecte
  python tests/test_bastides_2call.py ex_di ex_ci # subconjunt
"""
from __future__ import annotations

import sys
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

import re
import yaml

import server
from adaptation.prompt_builder import build_complements_prompt
from adaptation.llm_clients import _call_llm
from adaptation.post_process import clean_gemini_output, _post_process_llm_output

CASES_YAML = ROOT / "tests" / "golden" / "cases.yaml"

# Casos diana: els 4 de la memòria (project_bug_bastides_buides_20260529) + ex_pri
# (únic amb producció activa → activa també generate-bastides-produccio).
DEFAULT_CASE_IDS = ["ex_di", "ex_inf", "ex_l2", "ex_ci", "ex_pri"]

MIN_BODY_LINES = 3  # cos amb < 3 línies no buides = bastida buida/incompleta

# Text adaptat fix (curt, neutre, plausible a A1-B1). El reps com a "TEXT ADAPTAT".
SAMPLE_ADAPTED = """# El cicle de l'aigua

L'aigua és molt important per a la vida. L'aigua es mou en un cicle.

Primer, el **sol** escalfa l'aigua del mar. L'aigua es converteix en vapor i puja al cel.

Després, el vapor es refreda i forma els **núvols**. Quan els núvols són plens, cau la pluja.

La pluja omple els rius. Els rius porten l'aigua altra vegada al mar. El cicle torna a començar.
"""


def load_cases() -> dict:
    data = yaml.safe_load(CASES_YAML.read_text(encoding="utf-8"))
    return {c["id"]: c for c in data["casos"]}


_BASTIDES_HEADER_RE = re.compile(
    r"^## (?:Bastides|Suports per llegir|Suports de lectura)\b.*$",
    re.MULTILINE,
)


def extract_bastides_section(text: str) -> str | None:
    """Retorna el bloc de la secció bastides (capçalera + cos fins al següent `## `)."""
    m = _BASTIDES_HEADER_RE.search(text)
    if not m:
        return None
    start = m.start()
    nxt = re.search(r"^## ", text[m.end():], re.MULTILINE)
    end = m.end() + nxt.start() if nxt else len(text)
    return text[start:end].strip()


def body_metrics(section: str) -> dict:
    """Mètriques del cos (sense la línia de capçalera)."""
    lines = section.splitlines()
    body = lines[1:] if lines else []
    content_lines = [ln for ln in body if ln.strip()]
    moments = sum(
        1 for kw in ("abans", "durant", "després", "despres")
        if re.search(rf"^#+.*{kw}", section, re.IGNORECASE | re.MULTILINE)
    )
    return {
        "content_lines": len(content_lines),
        "chars": len(section),
        "moments": moments,
    }


def run_case(case: dict) -> dict:
    cid = case["id"]
    profile = case["profile"]
    params = case["params"]
    context = {
        "etapa": params.get("etapa", "ESO"),
        "materia": "ciències naturals",
    }

    system = build_complements_prompt(profile, context, params)
    if not system:
        return {"id": cid, "ok": False, "reason": "build_complements_prompt buit (sense SKILLs/complements)"}

    comp_model = server._model_for("complements")
    user = (
        f"TEXT ADAPTAT:\n{SAMPLE_ADAPTED}\n\n"
        "Genera els complements pedagògics sol·licitats."
    )
    raw = _call_llm(comp_model, system, user)
    clean = _post_process_llm_output(clean_gemini_output(raw), lang="ca")

    section = extract_bastides_section(clean)
    if section is None:
        return {"id": cid, "ok": False, "reason": "secció bastides ABSENT", "model": comp_model,
                "raw_len": len(clean)}
    m = body_metrics(section)
    ok = m["content_lines"] >= MIN_BODY_LINES
    return {
        "id": cid, "ok": ok, "model": comp_model, "section": section,
        "metrics": m,
        "reason": "OK" if ok else f"cos buit/incomplet ({m['content_lines']} línies)",
    }


def main():
    # Args: case IDs + opcional --repeat N (per mesurar estabilitat estocàstica).
    argv = sys.argv[1:]
    repeat = 1
    if "--repeat" in argv:
        i = argv.index("--repeat")
        repeat = int(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    ids = argv or DEFAULT_CASE_IDS
    cases = load_cases()

    # Per cas: comptem èxits sobre `repeat` repeticions.
    per_case = {cid: {"ok": 0, "n": 0, "last_section": None, "model": None} for cid in ids if cid in cases}
    last_results = []
    for rep in range(repeat):
        for cid in ids:
            if cid not in cases:
                print(f"[skip] cas desconegut: {cid}")
                continue
            tag = f"{cid}" + (f" (rep {rep+1}/{repeat})" if repeat > 1 else "")
            print(f"[run] {tag} … ", end="", flush=True)
            try:
                r = run_case(cases[cid])
            except Exception as e:
                r = {"id": cid, "ok": False, "reason": f"EXCEPCIÓ: {type(e).__name__}: {e}"}
            per_case[cid]["n"] += 1
            per_case[cid]["ok"] += 1 if r.get("ok") else 0
            per_case[cid]["model"] = r.get("model")
            if r.get("section"):
                per_case[cid]["last_section"] = r["section"]
            icon = "✅" if r.get("ok") else "❌"
            extra = ""
            if r.get("metrics"):
                mm = r["metrics"]
                extra = f" [{mm['content_lines']} línies, {mm['moments']} moments, {mm['chars']} chars]"
            print(f"{icon} {r['reason']}{extra}")
            last_results.append(r)

    print("\n" + "=" * 70)
    total_ok = sum(c["ok"] for c in per_case.values())
    total_n = sum(c["n"] for c in per_case.values())
    print(f"RESULTAT GLOBAL: {total_ok}/{total_n} execucions amb bastida plena")
    for cid, c in per_case.items():
        print(f"  - {cid}: {c['ok']}/{c['n']}")
    print("=" * 70)

    # Detall de l'última secció generada per cas (inspecció humana)
    for cid, c in per_case.items():
        if c.get("last_section"):
            print(f"\n----- {cid} ({c['model']}) -----")
            print(c["last_section"][:1200])

    # Èxit si TOTES les execucions passen (volem estabilitat, no sort).
    sys.exit(0 if total_ok == total_n and total_n > 0 else 1)


if __name__ == "__main__":
    main()
