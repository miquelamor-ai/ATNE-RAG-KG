#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
experiment_models_2026.py — Comparativa de models per a l'Adaptador ATNE
═══════════════════════════════════════════════════════════════════════════
Re-executa la decisió de model amb candidats actualitzats (juny 2026),
seguint el protocol d'avaluació ATNE (rúbriques C1-C5 + mètriques de forma)
amb JUTGE DE PROVEÏDOR DIFERENT del generador (principi anti-self-judging).

Ús:
    # .env amb GEMINI_API_KEY i OPENAI_API_KEY
    python tests/experiment_models_2026.py
    python tests/experiment_models_2026.py --candidates gemini-3.5-flash gpt-5 gpt-4o
    python tests/experiment_models_2026.py --judge gpt-4.1-mini --cases 6

Sortida:
    tests/results/experiment_models_<timestamp>.json   (dades completes)
    tests/results/experiment_models_<timestamp>.md     (informe llegible)

Notes:
  - Crida els proveïdors DIRECTAMENT (google-genai / openai SDK) amb el nom
    exacte de model, sense passar per la taula d'àlies de llm_clients (que
    podria resoldre noms nous a models antics per fallback de prefix).
  - El prompt es construeix amb el build_system_prompt REAL del repo, així
    la comparativa reflecteix el sistema de debò, no un prompt de joguina.
  - Els casos són SINTÈTICS (cap dada real de docent/alumne): es pot executar
    amb el free tier d'AI Studio sense risc de privadesa.
"""

import argparse
import json
import os
import re
import statistics
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Fix encoding Windows (cp1252): el caràcter ⚠ del tag self-judging feia petar el print
# i es perdia el resultat de TOT candidat del mateix proveïdor que el jutge (gpt-4o amb
# jutge gpt-4.1-mini). Bug detectat 1a passada 12/06.
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

from dotenv import load_dotenv  # noqa: E402
load_dotenv(ROOT / ".env")

from adaptation.prompt_builder import build_system_prompt  # noqa: E402

# ─────────────────────────────────────────────────────────────────────────
# Configuració de proveïdors (crida directa, model exacte)
# ─────────────────────────────────────────────────────────────────────────

def _provider_of(model: str) -> str:
    return "gemini" if model.startswith(("gemini", "gemma")) else "openai"


def call_model(model: str, system_prompt: str, user_text: str,
               temperature: float = 0.4) -> dict:
    """Crida el model i retorna {text, tokens_in, tokens_out, ms}."""
    t0 = time.time()
    if _provider_of(model) == "gemini":
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        # Retry simple per 503 UNAVAILABLE (demanda alta al free tier).
        last_err = None
        for _attempt in range(3):
            try:
                resp = client.models.generate_content(
                    model=model,
                    contents=user_text,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        temperature=temperature,
                        max_output_tokens=8192,
                    ),
                )
                usage = getattr(resp, "usage_metadata", None)
                return {
                    "text": resp.text or "",
                    "tokens_in": getattr(usage, "prompt_token_count", 0) or 0,
                    "tokens_out": getattr(usage, "candidates_token_count", 0) or 0,
                    "ms": int((time.time() - t0) * 1000),
                }
            except Exception as e:
                last_err = e
                if "503" in str(e) or "UNAVAILABLE" in str(e):
                    time.sleep(12)
                    continue
                raise
        raise last_err
    else:
        from openai import OpenAI
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        kwargs = {
            "model": model,
            "messages": [{"role": "system", "content": system_prompt},
                         {"role": "user", "content": user_text}],
        }
        # gpt-5 i o-series (reasoning) NOMÉS accepten temperature per defecte (1)
        # → ometre-la (passar-la peta amb 400 unsupported_value).
        if not re.match(r"^(gpt-5|o\d)", model):
            kwargs["temperature"] = temperature
        resp = client.chat.completions.create(**kwargs)
        u = resp.usage
        return {
            "text": resp.choices[0].message.content or "",
            "tokens_in": u.prompt_tokens if u else 0,
            "tokens_out": u.completion_tokens if u else 0,
            "ms": int((time.time() - t0) * 1000),
        }


# ─────────────────────────────────────────────────────────────────────────
# Casos sintètics (perfils delicats coberts: nouvingut pre-A1, DI, TEA,
# dislèxia, 2e, AACC). Textos breus, curriculars, sense dades reals.
# ─────────────────────────────────────────────────────────────────────────

TEXT_FOTOSINTESI = (
    "La fotosíntesi és el procés mitjançant el qual les plantes, les algues i "
    "alguns bacteris transformen l'energia lumínica del sol en energia química. "
    "Aquest procés té lloc principalment als cloroplasts de les cèl·lules "
    "vegetals, on la clorofil·la capta la llum. A partir de diòxid de carboni i "
    "aigua, la planta sintetitza glucosa i allibera oxigen com a subproducte. "
    "La fotosíntesi és fonamental per a la vida a la Terra, ja que produeix "
    "l'oxigen que respirem i constitueix la base de gairebé totes les cadenes "
    "tròfiques dels ecosistemes."
)

TEXT_REVOLUCIO = (
    "La Revolució Industrial va començar a la Gran Bretanya a finals del segle "
    "XVIII i va transformar profundament l'economia i la societat. La invenció "
    "de la màquina de vapor va permetre mecanitzar la producció tèxtil i "
    "impulsar el ferrocarril. Milers de persones van emigrar del camp a les "
    "ciutats per treballar a les fàbriques, sovint en condicions molt dures. "
    "Aquest procés va donar lloc a noves classes socials, com la burgesia "
    "industrial i el proletariat, i va sembrar les llavors dels moviments "
    "obrers posteriors."
)

CASES = [
    {"id": "NOUV_preA1", "text": TEXT_FOTOSINTESI,
     "profile": {"caracteristiques": {"nouvingut": {"actiu": True, "mecr": "pre-A1", "l1": "àrab", "alfabet_llati": False}}},
     "context": {"etapa": "primaria", "curs": "5è Primària", "materia": "Coneixement del medi"},
     "params": {"mecr_sortida": "pre-A1", "dua": "Acces", "intensitat_lf": 5,
                "complements": {"glossari": True, "pictogrames": True}}},
    {"id": "DI_moderat", "text": TEXT_FOTOSINTESI,
     "profile": {"caracteristiques": {"di": {"actiu": True, "grau": "moderat"}}},
     "context": {"etapa": "ESO", "curs": "2n ESO", "materia": "Biologia"},
     "params": {"mecr_sortida": "A2", "dua": "Core", "intensitat_lf": 4,
                "complements": {"glossari": True, "preguntes_comprensio": True}}},
    {"id": "TEA_n2", "text": TEXT_REVOLUCIO,
     "profile": {"caracteristiques": {"tea": {"actiu": True, "nivell_suport": 2}}},
     "context": {"etapa": "ESO", "curs": "3r ESO", "materia": "Història"},
     "params": {"mecr_sortida": "B1", "dua": "Core", "intensitat_lf": 3,
                "complements": {"esquema_visual": True, "preguntes_comprensio": True}}},
    {"id": "DISLEXIA", "text": TEXT_REVOLUCIO,
     "profile": {"caracteristiques": {"dislexia": {"actiu": True, "grau": "moderat"}}},
     "context": {"etapa": "ESO", "curs": "2n ESO", "materia": "Història"},
     "params": {"mecr_sortida": "B1", "dua": "Core", "intensitat_lf": 3,
                "complements": {"negretes": True, "glossari": True}}},
    {"id": "2E_aacc_dislexia", "text": TEXT_FOTOSINTESI,
     "profile": {"caracteristiques": {"altes_capacitats": {"actiu": True},
                                       "dislexia": {"actiu": True, "grau": "lleu"}}},
     "context": {"etapa": "ESO", "curs": "4t ESO", "materia": "Biologia"},
     "params": {"mecr_sortida": "B2", "dua": "Core", "intensitat_lf": 2,
                "complements": {"activitats_aprofundiment": True, "negretes": True}}},
    {"id": "AACC", "text": TEXT_REVOLUCIO,
     "profile": {"caracteristiques": {"altes_capacitats": {"actiu": True}}},
     "context": {"etapa": "ESO", "curs": "3r ESO", "materia": "Història"},
     "params": {"mecr_sortida": "B2", "dua": "Enriquiment", "intensitat_lf": 1,
                "complements": {"activitats_aprofundiment": True, "mapa_conceptual": True}}},
]

# Rangs F1 de longitud de frase per MECR (de avaluacio_ATNE_agent.md)
MECR_SENT_RANGE = {"pre-A1": (3, 5), "A1": (5, 8), "A2": (8, 12),
                   "B1": (12, 18), "B2": (18, 25)}


def f1_sentence_length(text: str, mecr: str) -> dict:
    """Mètrica determinista F1: longitud mitjana de frase dins el rang MECR."""
    # Fix 12/06: abans feia text.split("## ")[0] → agafava el tros ABANS de
    # "## Text adaptat" (buit/títol) → F1=0 sempre. Ara extreu el COS de
    # "## Text adaptat" (el text per a l'alumne, sense els complements).
    m = re.search(r"##\s*Text adaptat\s*\n(.*?)(?=\n##\s|\Z)", text, re.DOTALL | re.IGNORECASE)
    body = m.group(1) if m else re.split(r"\n##\s", text)[0]
    body = re.sub(r"[#*_>`-]", " ", body)
    sents = [s.strip() for s in re.split(r"[.!?]\s", body) if len(s.strip().split()) >= 2]
    if not sents:
        return {"mitjana": 0, "dins_rang": 0}
    mean = statistics.mean(len(s.split()) for s in sents)
    lo, hi = MECR_SENT_RANGE.get(mecr, (8, 18))
    return {"mitjana": round(mean, 1), "rang": f"{lo}-{hi}",
            "dins_rang": 1 if lo <= mean <= hi else 0}


# ─────────────────────────────────────────────────────────────────────────
# Jutge (rúbriques C1-C5 d'avaluacio_ATNE_agent.md, proveïdor ≠ generador)
# ─────────────────────────────────────────────────────────────────────────

JUDGE_SYSTEM = """Ets un avaluador pedagògic expert i escèptic. No aproves per defecte.
Avalues adaptacions de text per a alumnat amb necessitats educatives (criteris
Lectura Fàcil, DUA, MECR). Puntua cada criteri de l'1 al 5 basant-te exclusivament
en l'evidència del text adaptat. Justifica cada puntuació en una frase.
Respon NOMÉS amb JSON vàlid, sense markdown ni text addicional, amb aquest esquema:
{"C1_coherencia": {"p": int, "j": str}, "C2_adequacio_perfil": {"p": int, "j": str},
 "C3_preservacio_curricular": {"p": int, "j": str}, "C4_adequacio_mecr": {"p": int, "j": str},
 "C5_qualitat_catala": {"p": int, "j": str}}
C5 avalua específicament la correcció i naturalitat del CATALÀ (normativa, lèxic genuí,
sense calcs del castellà o l'anglès)."""


def judge(judge_model: str, case: dict, adapted: str) -> dict:
    prompt = (
        f"PERFIL DECLARAT: {json.dumps(case['profile'], ensure_ascii=False)}\n"
        f"PARÀMETRES: MECR {case['params']['mecr_sortida']} · DUA {case['params']['dua']}\n\n"
        f"TEXT ORIGINAL:\n{case['text']}\n\n"
        f"TEXT ADAPTAT A AVALUAR:\n{adapted[:6000]}"
    )
    raw = call_model(judge_model, JUDGE_SYSTEM, prompt, temperature=0.1)["text"]
    raw = re.sub(r"```json|```", "", raw).strip()
    try:
        scores = json.loads(raw)
        vals = [v["p"] for v in scores.values() if isinstance(v, dict) and "p" in v]
        scores["mitjana"] = round(statistics.mean(vals), 2) if vals else None
        return scores
    except Exception as e:
        return {"error": f"judge parse: {e}", "raw": raw[:300]}


# ─────────────────────────────────────────────────────────────────────────
# Execució
# ─────────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates", nargs="+",
                    default=["gemini-3.5-flash", "gpt-5", "gpt-4o"],
                    help="Models generadors a comparar (gpt-4o = baseline actual)")
    ap.add_argument("--judge", default="gpt-4.1-mini",
                    help="Model jutge (HA DE SER de proveïdor diferent dels candidats Gemini; per a candidats GPT el jutge ideal seria Gemini — el creuament es comprova)")
    ap.add_argument("--cases", type=int, default=len(CASES))
    ap.add_argument("--sleep", type=float, default=2.0,
                    help="Pausa entre crides (free tier: puja-la a 6-8s)")
    args = ap.parse_args()

    cases = CASES[: args.cases]
    results = []
    print(f"Experiment: {len(cases)} casos × {len(args.candidates)} candidats · jutge: {args.judge}\n")

    for case in cases:
        sp = build_system_prompt(case["profile"], case["context"], case["params"], rag_context="")
        for model in args.candidates:
            same_vendor = _provider_of(model) == _provider_of(args.judge)
            tag = " ⚠ jutge del MATEIX proveïdor (self-judging!)" if same_vendor else ""
            print(f"  [{case['id']}] {model} …", end=" ", flush=True)
            try:
                gen = call_model(model, sp, case["text"])
                f1 = f1_sentence_length(gen["text"], case["params"]["mecr_sortida"])
                time.sleep(args.sleep)
                jd = judge(args.judge, case, gen["text"])
                time.sleep(args.sleep)
                print(f"ok ({gen['ms']} ms · F1={f1['dins_rang']} · fons={jd.get('mitjana')}){tag}")
                results.append({"cas": case["id"], "model": model, "latencia_ms": gen["ms"],
                                "tokens_in": gen["tokens_in"], "tokens_out": gen["tokens_out"],
                                "f1_longitud": f1, "fons": jd, "self_judging": same_vendor,
                                "text_adaptat": gen["text"]})
            except Exception as e:
                print(f"ERROR: {e}")
                results.append({"cas": case["id"], "model": model, "error": str(e)})

    # ── Agregació i informe ──
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    outdir = ROOT / "tests" / "results"
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / f"experiment_models_{ts}.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [f"# Experiment models Adaptador — {ts}",
             f"Jutge: {args.judge} · Casos: {len(cases)}", "",
             "| Model | Fons mitjà (C1-C5) | C5 català | F1 dins rang | Latència mediana | Tokens out mitjà |",
             "|---|---|---|---|---|---|"]
    for model in args.candidates:
        rs = [r for r in results if r["model"] == model and "error" not in r]
        if not rs:
            lines.append(f"| {model} | ERROR en tots els casos | — | — | — | — |")
            continue
        fons = [r["fons"]["mitjana"] for r in rs if r["fons"].get("mitjana")]
        c5 = [r["fons"]["C5_qualitat_catala"]["p"] for r in rs
              if isinstance(r["fons"].get("C5_qualitat_catala"), dict)]
        f1 = sum(r["f1_longitud"]["dins_rang"] for r in rs)
        lat = statistics.median(r["latencia_ms"] for r in rs)
        tok = round(statistics.mean(r["tokens_out"] for r in rs))
        lines.append(f"| {model} | {round(statistics.mean(fons),2) if fons else '—'} "
                     f"| {round(statistics.mean(c5),2) if c5 else '—'} "
                     f"| {f1}/{len(rs)} | {lat} ms | {tok} |")
    lines += ["", "## Notes",
              "- Fons = mitjana C1-C5 del jutge (1-5). C5 = qualitat del català.",
              "- F1 = casos amb longitud mitjana de frase dins el rang MECR.",
              "- Revisa el JSON per a justificacions per criteri i textos complets.",
              "- ⚠ Si algun candidat comparteix proveïdor amb el jutge, repeteix",
              "  aquell amb un jutge creuat abans de decidir (anti-self-judging)."]
    (outdir / f"experiment_models_{ts}.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"\nInforme: tests/results/experiment_models_{ts}.md")
    print(f"Dades:   tests/results/experiment_models_{ts}.json")


if __name__ == "__main__":
    main()
