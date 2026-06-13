#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rejudge.py — Re-jutja (J2 homogeni) els resultats d'experiment_models_2026.

RECONSTRUÏT 2026-06-13. El rejudge.py original (12/06) era efímer i es va
perdre; aquesta versió el reconstrueix de manera fidel reutilitzant la
rúbrica (JUDGE_SYSTEM) i els CASES EXACTES de tests/experiment_models_2026.py
(font única, sense divergència de criteri).

Què fa:
  - Llegeix un JSON d'experiment (llista de registres amb 'cas', 'model',
    'text_adaptat' i 'fons' = judici J1).
  - Re-jutja TOTS els registres vàlids amb UN sol jutge J2 (homogeni) per
    obtenir una columna comparable (no barrejada amb dos models de jutge).
  - ROTA les claus GEMINI del .env (6 projectes free × 20 req/dia) per
    superar el límit de quota que va deixar la passada del 12/06 a mitges.
  - Combina J1 (del JSON) + J2 (nou) i escriu un informe creuat
    anti-self-judging: per als candidats GPT, el creuat NET surt del jutge
    Gemini (J2); per als candidats Gemini, del jutge OpenAI (J1).

CAVEAT documentat: si el jutge J2 (gemini-2.5-flash) coincideix amb un
candidat (gemini-2.5-flash), els 2 casos d'aquell candidat queden
AUTO-JUTJATS sota J2 (jutge = generador). Per a la decisió NO s'usen: el
creuat fiable d'aquell candidat ja el dona J1 (gpt-4.1-mini).

Ús:
    python tests/rejudge.py \
        --in tests/results/experiment_models_20260612_150946.json \
        --judge2 gemini-2.5-flash --sleep 7
"""

import argparse
import itertools
import json
import os
import re
import statistics
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
sys.path.insert(0, str(ROOT))
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

from dotenv import load_dotenv  # noqa: E402
load_dotenv(ROOT / ".env")

# Font única: mateixa rúbrica i mateixos casos que la generació.
from experiment_models_2026 import JUDGE_SYSTEM, CASES  # noqa: E402

CASE_BY_ID = {c["id"]: c for c in CASES}
CANDIDATS = ["gemini-3.5-flash", "gemini-2.5-flash", "gpt-5", "gpt-4o"]


# ── Claus Gemini en rotació ────────────────────────────────────────────────
def gemini_keys():
    keys = []
    for n in ["GEMINI_API_KEY"] + [f"GEMINI_API_KEY_{i}" for i in range(2, 9)]:
        v = os.environ.get(n)
        if v:
            keys.append((n, v))
    return keys


KEYS = gemini_keys()
KEY_CYCLE = itertools.cycle(range(len(KEYS))) if KEYS else None


def gemini_judge_raw(model: str, system: str, prompt: str,
                     temperature: float = 0.1) -> tuple[str, str]:
    """Crida Gemini amb ROTACIÓ de claus. Retorna (text, nom_clau).
    Davant 429/quota o resposta buida, prova la clau següent (fins a esgotar-les."""
    from google import genai
    from google.genai import types
    errs = []
    for _ in range(len(KEYS)):
        ki = next(KEY_CYCLE)
        kname, key = KEYS[ki]
        try:
            client = genai.Client(api_key=key)
            resp = client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system,
                    temperature=temperature,
                    max_output_tokens=8192,
                ),
            )
            txt = resp.text or ""
            if txt.strip():
                return txt, kname
            errs.append((kname, "resposta buida"))
        except Exception as e:
            s = str(e)
            tag = "429/quota" if ("429" in s or "RESOURCE_EXHAUSTED" in s) else s[:60]
            errs.append((kname, tag))
            continue
    raise RuntimeError(f"cap clau ha respost ({len(KEYS)} provades): {errs}")


def parse_scores(raw: str) -> dict:
    raw = re.sub(r"```json|```", "", raw).strip()
    scores = json.loads(raw)
    vals = [v["p"] for v in scores.values() if isinstance(v, dict) and "p" in v]
    scores["mitjana"] = round(statistics.mean(vals), 2) if vals else None
    return scores


def build_judge_prompt(case: dict, adapted: str) -> str:
    # Idèntic a experiment_models_2026.judge() (font única del prompt de jutge).
    return (
        f"PERFIL DECLARAT: {json.dumps(case['profile'], ensure_ascii=False)}\n"
        f"PARÀMETRES: MECR {case['params']['mecr_sortida']} · DUA {case['params']['dua']}\n\n"
        f"TEXT ORIGINAL:\n{case['text']}\n\n"
        f"TEXT ADAPTAT A AVALUAR:\n{adapted[:6000]}"
    )


def is_gemini(m: str) -> bool:
    return m.startswith(("gemini", "gemma"))


def fons2_ok(r: dict) -> bool:
    f2 = r.get("fons2")
    return isinstance(f2, dict) and f2.get("mitjana") is not None


def fmt(x, nd=2):
    return "—" if x is None else (round(x, nd) if isinstance(x, float) else x)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="infile", required=True,
                    help="JSON d'experiment_models_* a re-jutjar")
    ap.add_argument("--judge2", default="gemini-2.5-flash",
                    help="Model jutge J2 homogeni (Gemini, per al creuat dels candidats GPT)")
    ap.add_argument("--judge1-name", default="gpt-4.1-mini",
                    help="Nom del jutge J1 ja present al JSON (només per a l'informe)")
    ap.add_argument("--sleep", type=float, default=7.0,
                    help="Pausa entre judicis (free tier: 6-8s recomanat)")
    args = ap.parse_args()

    if not KEYS:
        print("ERROR: cap GEMINI_API_KEY al .env", file=sys.stderr)
        sys.exit(1)

    src = Path(args.infile)
    records = json.loads(src.read_text(encoding="utf-8"))
    valid = [r for r in records
             if (r.get("fons") or {}).get("mitjana") is not None
             and (r.get("text_adaptat") or "").strip()]

    print(f"Re-jutjant {len(valid)}/{len(records)} registres VÀLIDS de {src.name}")
    print(f"  judge2 = {args.judge2} · {len(KEYS)} claus en rotació "
          f"({', '.join(n for n, _ in KEYS)}) · sleep = {args.sleep}s\n")

    judged = 0
    for r in records:
        fons = r.get("fons") or {}
        if fons.get("mitjana") is None or not (r.get("text_adaptat") or "").strip():
            r["fons2"] = None
            print(f"  [{r['cas']}] {r['model']} … SKIP (generació fallida, sense text adaptat)")
            continue
        case = CASE_BY_ID[r["cas"]]
        prompt = build_judge_prompt(case, r["text_adaptat"])
        try:
            raw, kname = gemini_judge_raw(args.judge2, JUDGE_SYSTEM, prompt)
            scores = parse_scores(raw)
            r["fons2"] = scores
            judged += 1
            sj = "  ⚠ AUTO-JUTGE (jutge=candidat)" if r["model"] == args.judge2 else ""
            print(f"  [{r['cas']}] {r['model']} (judge2) … fons2={scores.get('mitjana')} (key={kname}){sj}")
        except Exception as e:
            r["fons2"] = {"error": str(e)[:200]}
            print(f"  [{r['cas']}] {r['model']} (judge2) … ERROR: {str(e)[:120]}")
        time.sleep(args.sleep)

    print(f"\nJudicis J2 fets: {judged}/{len(valid)}")

    # ── Agregació creuada per candidat ──
    rows = []
    for m in CANDIDATS:
        rs = [r for r in records if r["model"] == m
              and (r.get("fons") or {}).get("mitjana") is not None]
        rs2 = [r for r in rs if fons2_ok(r)]
        j1 = statistics.mean([r["fons"]["mitjana"] for r in rs]) if rs else None
        j2 = statistics.mean([r["fons2"]["mitjana"] for r in rs2]) if rs2 else None
        c5_1 = statistics.mean([r["fons"]["C5_qualitat_catala"]["p"] for r in rs
                                if isinstance(r["fons"].get("C5_qualitat_catala"), dict)]) if rs else None
        c5_2 = statistics.mean([r["fons2"]["C5_qualitat_catala"]["p"] for r in rs2
                                if isinstance(r["fons2"].get("C5_qualitat_catala"), dict)]) if rs2 else None
        creuat = j1 if is_gemini(m) else j2  # anti-self-judging: jutge de l'ALTRE proveïdor
        delta = abs(j1 - j2) if (j1 is not None and j2 is not None) else None
        rows.append(dict(model=m, j1=j1, j2=j2, c5_1=c5_1, c5_2=c5_2,
                         creuat=creuat, delta=delta, n=len(rs), n2=len(rs2),
                         selfj2=(m == args.judge2)))

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    outdir = ROOT / "tests" / "results"
    out_json = outdir / f"experiment_combinat_{ts}.json"
    out_md = outdir / f"experiment_combinat_{ts}.md"
    out_json.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")

    L = []
    L.append(f"# Experiment models — informe combinat (jutge creuat) · {ts}")
    L.append("")
    L.append(f"Jutge 1 (J1): **{args.judge1_name}** · Jutge 2 (J2): **{args.judge2}** · Casos: 6")
    L.append("")
    L.append("## Taula creuada per candidat")
    L.append("")
    L.append("| Candidat | Fons J1 | Fons J2 | Δ | C5 català (J1/J2) | **Creuat NET** | n (J1/J2) |")
    L.append("|---|---|---|---|---|---|---|")
    for x in rows:
        crew = f"**{fmt(x['creuat'])}**"
        star = " ⚠*" if x["selfj2"] else ""
        L.append(f"| {x['model']}{star} | {fmt(x['j1'])} | {fmt(x['j2'])} | {fmt(x['delta'])} "
                 f"| {fmt(x['c5_1'])}/{fmt(x['c5_2'])} | {crew} | {x['n']}/{x['n2']} |")
    L.append("")
    L.append("**Creuat NET** = puntuació del jutge de l'ALTRE proveïdor (la menys esbiaixada):")
    L.append(f"- Candidats Gemini → J1 ({args.judge1_name}, OpenAI).")
    L.append(f"- Candidats GPT → J2 ({args.judge2}, Gemini).")
    L.append("")
    L.append(f"⚠* **{args.judge2} és alhora candidat i jutge J2**: els seus casos queden AUTO-JUTJATS "
             f"sota J2 (jutge = generador) → la seva columna J2 està inflada i **NO s'usa** per a la "
             f"decisió. El seu creuat fiable és J1 = {fmt(next(x['j1'] for x in rows if x['model']==args.judge2))}.")
    L.append("")

    # ── Detall per cas: Fons (J1/J2) ──
    cas_order = [c["id"] for c in CASES]
    L.append("## Fons per cas (J1 / J2)")
    L.append("")
    L.append("| Cas | " + " | ".join(CANDIDATS) + " |")
    L.append("|---|" + "---|" * len(CANDIDATS))
    for cas in cas_order:
        cells = []
        for m in CANDIDATS:
            r = next((r for r in records if r["cas"] == cas and r["model"] == m), None)
            if not r or (r.get("fons") or {}).get("mitjana") is None:
                cells.append("(gen. fallida)")
                continue
            j1 = r["fons"]["mitjana"]
            j2 = r["fons2"]["mitjana"] if fons2_ok(r) else None
            cells.append(f"{fmt(j1)} / {fmt(j2)}")
        L.append(f"| {cas} | " + " | ".join(cells) + " |")
    L.append("")

    # ── Detall per cas: C5 català (J1/J2) ──
    L.append("## C5 català per cas (J1 / J2) — on el català fluixeja a l'extrem")
    L.append("")
    L.append("| Cas | " + " | ".join(CANDIDATS) + " |")
    L.append("|---|" + "---|" * len(CANDIDATS))
    for cas in cas_order:
        cells = []
        for m in CANDIDATS:
            r = next((r for r in records if r["cas"] == cas and r["model"] == m), None)
            if not r or not isinstance((r.get("fons") or {}).get("C5_qualitat_catala"), dict):
                cells.append("(gen. fallida)")
                continue
            c1 = r["fons"]["C5_qualitat_catala"]["p"]
            c2 = (r["fons2"]["C5_qualitat_catala"]["p"]
                  if fons2_ok(r) and isinstance(r["fons2"].get("C5_qualitat_catala"), dict) else None)
            cells.append(f"{fmt(c1)} / {fmt(c2)}")
        L.append(f"| {cas} | " + " | ".join(cells) + " |")
    L.append("")

    out_md.write_text("\n".join(L), encoding="utf-8")
    print(f"\nInforme combinat: {out_md}")
    print(f"JSON combinat:    {out_json}")

    # Resum compacte a stdout
    print("\n=== RESUM CREUAT ===")
    for x in rows:
        prov = "Gemini" if is_gemini(x["model"]) else "GPT"
        src_j = "J1" if is_gemini(x["model"]) else "J2"
        print(f"  {x['model']:18} J1={fmt(x['j1'])!s:>5} J2={fmt(x['j2'])!s:>5} "
              f"→ CREUAT={fmt(x['creuat'])!s:>5} (via {src_j}) "
              f"C5 J1/J2={fmt(x['c5_1'])}/{fmt(x['c5_2'])}")


if __name__ == "__main__":
    main()
