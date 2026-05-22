"""Anàlisi de les adaptacions REALS del pilot.

En lloc de fer crides LLM noves, llegeix els 162 textos adaptats que ja
existeixen a Supabase `history`, hi aplica les mètriques de transformació
(text adaptat NET vs ajuts afegits) i agrega per perfil + nivell sortida.

Resultats com mostra empírica gran: 8x més mostres que el test sintètic,
diversitat de textos d'entrada reals, ZERO cost LLM.

Ús:
    PYTHONIOENCODING=utf-8 python tests/analyze_pilot_adaptations.py

    --save report.json   Guarda dades raw per inspecció posterior
    --min-words 50       Ignora adaptacions amb text adaptat curt (default 50)
"""

from __future__ import annotations
import argparse
import json
import os
import re
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
if not SUPABASE_URL or not SERVICE_KEY:
    sys.exit("Falten SUPABASE_URL / SUPABASE_SERVICE_KEY al .env")

HEADERS = {"apikey": SERVICE_KEY, "Authorization": f"Bearer {SERVICE_KEY}"}
BASE = f"{SUPABASE_URL}/rest/v1"


# ──────────────────────────────────────────────────────────────────────
# Parsing / mètriques (mateixes que test_perfil_application.py)
# ──────────────────────────────────────────────────────────────────────

def parse_sections(full_text: str) -> dict[str, str]:
    """Separa text en seccions `## Header`. Retorna {header: body}."""
    if not full_text:
        return {}
    lines = full_text.split("\n")
    sections: dict[str, str] = {}
    current = None
    buf: list[str] = []
    for line in lines:
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            if current is not None:
                sections[current] = "\n".join(buf).strip()
            current = m.group(1).strip()
            buf = []
        else:
            buf.append(line)
    if current is not None:
        sections[current] = "\n".join(buf).strip()
    return sections


def tokenize_words(s: str) -> list[str]:
    return re.findall(r"[A-Za-zÀ-ÿ]{2,}", s)


def split_sentences(s: str) -> list[str]:
    raw = re.split(r"[\.!?]+", s)
    return [x.strip() for x in raw if x.strip()]


def compute_metrics(text: str) -> dict:
    if not text:
        return {"n_words": 0, "n_sents": 0, "avg_words_per_sent": 0.0,
                "complex_words_pct": 0.0}
    words = tokenize_words(text)
    sents = split_sentences(text)
    complex_words = [w for w in words if len(w) > 7]
    return {
        "n_words": len(words),
        "n_sents": len(sents),
        "avg_words_per_sent": round(len(words) / max(len(sents), 1), 2),
        "complex_words_pct": round(len(complex_words) / max(len(words), 1) * 100, 1),
    }


def has_l1_in_glossary(glossari: str, l1_name: str) -> bool:
    if not glossari or not l1_name:
        return False
    if l1_name.lower() in glossari.lower():
        return True
    if re.search(r"[؀-ۿ一-鿿Ѐ-ӿ]", glossari):
        return True
    return False


def aggregate(values: list[float]) -> dict:
    if not values:
        return {"n": 0}
    return {
        "n": len(values),
        "min": round(min(values), 2),
        "mean": round(statistics.mean(values), 2),
        "median": round(statistics.median(values), 2),
        "max": round(max(values), 2),
        "std": round(statistics.stdev(values), 2) if len(values) > 1 else 0.0,
    }


def fmt_agg(label: str, agg: dict, unit: str = "") -> str:
    if agg.get("n", 0) == 0:
        return f"  {label}: (sense dades)"
    return (f"  {label}: "
            f"min={agg['min']}{unit}  med={agg['median']}{unit}  "
            f"mean={agg['mean']}{unit}  max={agg['max']}{unit}  std={agg['std']}")


# ──────────────────────────────────────────────────────────────────────
# Carrega
# ──────────────────────────────────────────────────────────────────────

def fetch_history(limit: int = 1000) -> list[dict]:
    url = (f"{BASE}/history?select=id,created_at,original_text,adapted_text,"
           f"profile_json,params_json,context_json,etapa,model_used,prompt_version,"
           f"rating,comment&adapted_text=not.is.null&order=created_at.desc&limit={limit}")
    r = requests.get(url, headers=HEADERS, timeout=30)
    if r.status_code != 200:
        sys.exit(f"HTTP {r.status_code}: {r.text[:300]}")
    return r.json()


# ──────────────────────────────────────────────────────────────────────
# Processament per fila
# ──────────────────────────────────────────────────────────────────────

def process_row(row: dict) -> dict | None:
    orig = row.get("original_text") or ""
    adapt = row.get("adapted_text") or ""
    if not orig or not adapt:
        return None
    sections = parse_sections(adapt)
    # Si no hi ha "## Text adaptat", tractem tot el text com a net (cas legacy)
    text_net = sections.get("Text adaptat") or adapt

    orig_m = compute_metrics(orig)
    net_m = compute_metrics(text_net)
    full_m = compute_metrics(adapt)

    if orig_m["n_words"] < 30 or net_m["n_words"] < 10:
        return None  # massa curt per ser fiable

    ratio_net = round(net_m["n_words"] / orig_m["n_words"], 3)
    ratio_full = round(full_m["n_words"] / orig_m["n_words"], 3)

    profile_json = row.get("profile_json") or {}
    params_json = row.get("params_json") or {}
    perfils_list = profile_json.get("perfils") or []
    perfils_str: list[str] = []
    for p in perfils_list:
        if isinstance(p, str):
            perfils_str.append(p)
        elif isinstance(p, dict):
            perfils_str.append(p.get("id") or p.get("nom") or "?")
    l1 = profile_json.get("l1") or ""
    nivell = params_json.get("nivell") or "?"
    adaptacio_kind = params_json.get("adaptacio") or "?"

    complement_sections = [k for k in sections if k != "Text adaptat" and sections[k].strip()]

    return {
        "id": row.get("id"),
        "ts": row.get("created_at"),
        "etapa": row.get("etapa") or "",
        "model_used": row.get("model_used") or "",
        "perfils": perfils_str,
        "l1": l1,
        "nivell": nivell,
        "adaptacio": adaptacio_kind,
        "rating": row.get("rating"),
        "n_orig_words": orig_m["n_words"],
        "n_net_words": net_m["n_words"],
        "n_full_words": full_m["n_words"],
        "ratio_net": ratio_net,
        "ratio_full": ratio_full,
        "avg_wps_net": net_m["avg_words_per_sent"],
        "avg_wps_orig": orig_m["avg_words_per_sent"],
        "complex_pct_net": net_m["complex_words_pct"],
        "complex_pct_orig": orig_m["complex_words_pct"],
        "complement_sections": complement_sections,
        "n_complements": len(complement_sections),
        "has_glossari": "Glossari" in sections,
        "has_l1_in_glossari": has_l1_in_glossary(sections.get("Glossari", ""), l1) if l1 else None,
        "has_text_adaptat_header": "Text adaptat" in sections,
    }


# ──────────────────────────────────────────────────────────────────────
# Agregacions
# ──────────────────────────────────────────────────────────────────────

def group_by(rows: list[dict], key) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        out[key(r)].append(r)
    return dict(out)


def summarize_group(rows: list[dict]) -> dict:
    if not rows:
        return {"n": 0}
    ratios_net = [r["ratio_net"] for r in rows]
    ratios_full = [r["ratio_full"] for r in rows]
    wps = [r["avg_wps_net"] for r in rows]
    complex_pct = [r["complex_pct_net"] for r in rows]
    n_comp = [r["n_complements"] for r in rows]
    ratings = [r["rating"] for r in rows if r["rating"] is not None]
    has_text_header = sum(1 for r in rows if r["has_text_adaptat_header"])
    return {
        "n": len(rows),
        "ratio_net": aggregate(ratios_net),
        "ratio_full": aggregate(ratios_full),
        "avg_wps_net": aggregate(wps),
        "complex_pct_net": aggregate(complex_pct),
        "n_complements": aggregate(n_comp),
        "with_text_adaptat_header_pct": round(has_text_header / len(rows) * 100, 0),
        "rating": aggregate(ratings) if ratings else {"n": 0},
    }


def section(title: str) -> None:
    print(f"\n{'=' * 78}\n {title}\n{'=' * 78}")


# ──────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--save", default="", help="Guarda dades raw a JSON")
    ap.add_argument("--min-words", type=int, default=30, help="Mínim paraules originals (default: 30)")
    args = ap.parse_args()

    print("Descarregant adaptacions del pilot...")
    raw = fetch_history(limit=2000)
    print(f"  · {len(raw)} adaptacions amb adapted_text")

    processed = [p for p in (process_row(r) for r in raw) if p is not None]
    print(f"  · {len(processed)} amb prou paraules (>={args.min_words})")

    # ─── Vista global ───
    section("VISTA GLOBAL — totes les adaptacions")
    glob = summarize_group(processed)
    print(f"  N = {glob['n']}")
    print(fmt_agg("Ratio NET (text adaptat net / original)", glob["ratio_net"]))
    print(fmt_agg("Ratio FULL (text + complements / original)", glob["ratio_full"]))
    print(fmt_agg("Paraules per frase NET", glob["avg_wps_net"]))
    print(fmt_agg("% paraules >7 lletres NET", glob["complex_pct_net"], "%"))
    print(fmt_agg("Nombre complements per adaptació", glob["n_complements"]))
    print(f"  Adaptacions amb header '## Text adaptat': {glob['with_text_adaptat_header_pct']}%")

    # ─── Per tipus d'adaptació (molt_simplificat/simplificat/al_nivell/enriquiment) ───
    section("PER TIPUS D'ADAPTACIÓ (params.adaptacio)")
    by_kind = group_by(processed, lambda r: r["adaptacio"])
    order = ["molt_simplificat", "simplificat", "al_nivell", "enriquiment", "?"]
    for kind in order:
        if kind in by_kind:
            rows = by_kind[kind]
            summ = summarize_group(rows)
            print(f"\n  ▶ {kind}  (N={summ['n']})")
            print(fmt_agg("    ratio_net", summ["ratio_net"]))
            print(fmt_agg("    ratio_full", summ["ratio_full"]))
            print(fmt_agg("    paraules/frase", summ["avg_wps_net"]))
            print(fmt_agg("    complex %", summ["complex_pct_net"], "%"))

    # ─── Per nivell sortida ───
    section("PER NIVELL DE SORTIDA (MECR)")
    by_lvl = group_by(processed, lambda r: r["nivell"])
    mecr_order = ["pre-A1", "A1", "A2", "B1", "B2", "C1", "C2", "?"]
    for lvl in mecr_order:
        if lvl in by_lvl:
            rows = by_lvl[lvl]
            summ = summarize_group(rows)
            print(f"\n  ▶ MECR={lvl}  (N={summ['n']})")
            print(fmt_agg("    ratio_net", summ["ratio_net"]))
            print(fmt_agg("    paraules/frase", summ["avg_wps_net"]))
            print(fmt_agg("    complex %", summ["complex_pct_net"], "%"))

    # ─── Per perfil declarat ───
    section("PER PERFIL DECLARAT")
    by_perfil: dict[str, list[dict]] = defaultdict(list)
    for r in processed:
        for p in r["perfils"]:
            by_perfil[p].append(r)
        if not r["perfils"]:
            by_perfil["(sense perfil)"].append(r)
    for perfil, rows in sorted(by_perfil.items(), key=lambda x: -len(x[1])):
        summ = summarize_group(rows)
        print(f"\n  ▶ {perfil}  (N={summ['n']})")
        print(fmt_agg("    ratio_net", summ["ratio_net"]))
        print(fmt_agg("    paraules/frase", summ["avg_wps_net"]))
        print(fmt_agg("    complex %", summ["complex_pct_net"], "%"))
        print(fmt_agg("    n complements", summ["n_complements"]))
        if summ["rating"].get("n", 0):
            print(fmt_agg("    rating", summ["rating"]))

    # ─── Cas crític: nouvinguts + L1 ───
    section("NOUVINGUTS — Glossari amb L1?")
    nouvinguts = [r for r in processed if "nouvingut" in r["perfils"] and r["l1"]]
    if nouvinguts:
        with_l1 = sum(1 for r in nouvinguts if r["has_l1_in_glossari"])
        with_gloss = sum(1 for r in nouvinguts if r["has_glossari"])
        print(f"  Adaptacions nouvingut amb L1 declarada: {len(nouvinguts)}")
        print(f"  Tenen secció Glossari: {with_gloss} ({with_gloss/len(nouvinguts)*100:.0f}%)")
        print(f"  Glossari conté L1: {with_l1} ({with_l1/len(nouvinguts)*100:.0f}%)")
        print(f"\n  L1 més freqüents:")
        l1_c = Counter(r["l1"] for r in nouvinguts)
        for l1, n in l1_c.most_common(10):
            with_l1_l1 = sum(1 for r in nouvinguts if r["l1"] == l1 and r["has_l1_in_glossari"])
            print(f"    {l1:20s} N={n}  amb L1 al glossari: {with_l1_l1}/{n}")

    # ─── Cas crític: AACC ───
    section("ALTES CAPACITATS — enriqueix o rebaixa?")
    aacc = [r for r in processed if "altes_capacitats" in r["perfils"]]
    if aacc:
        summ = summarize_group(aacc)
        print(f"  N = {summ['n']}")
        print(fmt_agg("    ratio_net", summ["ratio_net"]))
        print(fmt_agg("    complex_pct_net", summ["complex_pct_net"], "%"))
        reduces = sum(1 for r in aacc if r["ratio_net"] < 0.95)
        enriches = sum(1 for r in aacc if r["ratio_net"] > 1.1)
        print(f"  Rebaixa (ratio_net<0.95): {reduces}/{summ['n']}")
        print(f"  Enriqueix (ratio_net>1.1): {enriches}/{summ['n']}")

    # ─── Distribució ratings per perfil ───
    section("RATING per PERFIL (qualitat percebuda)")
    for perfil, rows in sorted(by_perfil.items(), key=lambda x: -len(x[1])):
        ratings = [r["rating"] for r in rows if r["rating"] is not None]
        if ratings:
            print(f"  {perfil:30s}  ratings: n={len(ratings)}  mean={statistics.mean(ratings):.2f}  "
                  f"dist={dict(Counter(ratings))}")

    # ─── Detecció de patrons / alertes ───
    section("ALERTES (patrons globals)")
    alerts = []

    # AACC: si rebaixa més que enriqueix
    if aacc:
        aacc_summ = summarize_group(aacc)
        if aacc_summ["ratio_net"]["mean"] < 0.95:
            alerts.append(f"AC rebaixa el text (ratio_net mean={aacc_summ['ratio_net']['mean']}), hauria d'enriquir")

    # Nouvinguts: % amb L1 al glossari
    if nouvinguts:
        with_l1 = sum(1 for r in nouvinguts if r["has_l1_in_glossari"])
        rate = with_l1 / len(nouvinguts)
        if rate < 0.5:
            alerts.append(f"Només {rate*100:.0f}% adaptacions nouvingut tenen L1 al glossari ({with_l1}/{len(nouvinguts)})")

    # Header "Text adaptat" mancat
    if glob["with_text_adaptat_header_pct"] < 70:
        alerts.append(f"Només {glob['with_text_adaptat_header_pct']:.0f}% adaptacions tenen header '## Text adaptat' (parsing complicat)")

    # Per nivells baixos: si NO redueixen
    for lvl in ["pre-A1", "A1", "A2"]:
        if lvl in by_lvl:
            s = summarize_group(by_lvl[lvl])
            if s["ratio_net"]["mean"] > 1.0:
                alerts.append(f"MECR={lvl}: ratio_net mean={s['ratio_net']['mean']} (no redueix; pot ser problema)")

    # AACC: enriquiment esperat
    if "enriquiment" in by_kind:
        s = summarize_group(by_kind["enriquiment"])
        if s["ratio_net"]["mean"] < 1.0:
            alerts.append(f"adaptacio=enriquiment: ratio_net mean={s['ratio_net']['mean']} (NO enriqueix realment)")

    if alerts:
        for a in alerts:
            print(f"  ⚠  {a}")
    else:
        print("  ✓ Cap alerta global detectada")

    if args.save:
        Path(args.save).write_text(json.dumps(processed, ensure_ascii=False, indent=2),
                                    encoding="utf-8")
        print(f"\n  Dades raw guardades a: {args.save}")


if __name__ == "__main__":
    main()
