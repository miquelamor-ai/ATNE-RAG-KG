"""Test descriptiu: mesura la distribució del comportament d'adaptació per perfil.

Origen: 8/10 refinaments via rúbrica al pilot marquen «No s'apliquen bé les
estratègies del perfil». Aquest test mesura empíricament què fa /api/adapt
amb diferents perfils i múltiples repeticions, i busca patrons (no llindars
prescriptius).

Plantejament dual (transformacions vs ajuts):
  · TRANSFORMACIONS del text adaptat NET (`## Text adaptat`):
      paraules, complexitat lèxica, longitud de frase.
  · AJUTS (`## Glossari`, `## Preguntes...`, etc.): presència + nombre seccions.

Per separar bé NET vs AJUTS evitem el fals positiu "ha multiplicat paraules":
el total pot créixer perquè s'afegeixen complements i definicions inline,
encara que el text adaptat net sigui més curt.

Mètode (Opció 2 — descriptiu, no prescriptiu):
  - 5 perfils representatius del pilot
  - N repeticions per perfil (default 5)
  - Mesura distribució: min/mitjana/max/std de cada mètrica
  - Flagging d'alertes basat en patrons, no pass/fail rígid

Ús:
    (A) Server local (recomanat — sense JWT):
        Terminal 1: python server.py
        Terminal 2: python tests/test_perfil_application.py

    (B) Cloud Run amb JWT:
        Token al navegador: DevTools → Application → Local Storage → atne_jwt
        python tests/test_perfil_application.py --base-url <CLOUD_URL> --token "eyJ..."

    Opcions:
        --repetitions 3            menys passades (smoke ràpid)
        --model gemini-2.5-flash   força model concret
        --profiles 01_tdah_B2 04_aacc_B2   subset de perfils
        --save report.json         guarda dades raw

Cost estimat: 25 crides × ~30-40s = ~15 min (varia segons rotatiu).
"""

from __future__ import annotations
import argparse
import json
import math
import re
import statistics
import sys
import time
from collections import defaultdict
from pathlib import Path

import requests

DEFAULT_BASE_URL = "http://localhost:8000"
CLOUD_RUN_URL = "https://atne-1050342211642.europe-west1.run.app"

# Text de referència — B2, ciències naturals, ~340 paraules
TEXT_INPUT = """## Ecosistemes: la vida en interacció

Un **ecosistema** és un sistema natural format per un conjunt d'**organismes vius** (components biòtics) i el **medi físic** on viuen (components abiòtics), que interactuen entre ells. Aquesta interacció és essencial per al manteniment de la vida i l'equilibri del sistema.

Els **components biòtics** inclouen tots els éssers vius: plantes, animals, microorganismes (bacteris, fongs, virus...). Es classifiquen segons el seu paper en l'ecosistema:

* **Productors**: són els organismes autòtrofs, com les plantes, que obtenen l'energia del sol a través de la **fotosíntesi** i la transformen en matèria orgànica. Són la base de la cadena tròfica.
* **Consumidors**: són els organismes heteròtrofs que s'alimenten d'altres organismes.
* **Descompositors**: són els organismes que s'alimenten de la matèria orgànica morta, descomponent-la i alliberen nutrients al medi.

Els **components abiòtics** són els factors físics i químics que influeixen en els organismes vius: llum solar, temperatura, aigua, sòl, aire.

La **xarxa tròfica** representa les relacions alimentàries entre els organismes d'un ecosistema. L'energia flueix a través de la xarxa tròfica, des dels productors fins als consumidors i, finalment, als descomponedors."""


# 5 perfils representatius del pilot
PROFILES = [
    {
        "slug": "01_tdah_B2",
        "nom": "Test TDAH B2",
        "caracteristiques": {
            "tdah": {"actiu": True, "grau": "moderat", "subtipus": "Combinat"},
        },
        "mecr": "B2",
        "etapa": "eso",
        "expectation_note": "redueix lleugerament, blocs curts, frases simples",
    },
    {
        "slug": "02_dislexia_B1",
        "nom": "Test Dislèxia B1",
        "caracteristiques": {
            "dislexia": {"actiu": True, "grau": "moderat", "tipus": "fonologica"},
        },
        "mecr": "B1",
        "etapa": "eso",
        "expectation_note": "paraules curtes, frases simples",
    },
    {
        "slug": "03_nouvingut_arab_A1",
        "nom": "Test Nouvingut àrab A1",
        "caracteristiques": {
            "nouvingut": {
                "actiu": True,
                "l1": "Àrab",
                "pais": "Marroc",
                "mesos_catalunya": 6,
                "alfabet_llati": False,
                "alfabetitzacio_l1": True,
                "escolaritzacio": "regular",
            },
        },
        "mecr": "A1",
        "etapa": "eso",
        "expectation_note": "redueix molt, glossari L1, transliteració",
    },
    {
        "slug": "04_aacc_B2",
        "nom": "Test Altes Capacitats B2",
        "caracteristiques": {
            "altes_capacitats": {"actiu": True},
        },
        "mecr": "B2",
        "etapa": "eso",
        "expectation_note": "NO rebaixa: enriqueix, profunditza, vocabulari ric",
    },
    {
        "slug": "05_infantil_I5_preA1",
        "nom": "Test Infantil I5",
        "caracteristiques": {},
        "mecr": "pre-A1",
        "etapa": "infantil",
        "expectation_note": "redueix dràsticament, frases molt curtes",
    },
]


# ══════════════════════════════════════════════════════════════════════════
# HTTP / SSE
# ══════════════════════════════════════════════════════════════════════════

def headers(token: str) -> dict:
    h = {"Content-Type": "application/json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def build_payload(profile_def: dict, model: str = "") -> dict:
    base_profile = {
        "nom": profile_def["nom"],
        "caracteristiques": profile_def.get("caracteristiques", {}),
        "canal_preferent": "text",
        "observacions": "",
        "_via": "diagnostic",
        "group": False,
    }
    params = {
        "mecr_sortida": profile_def["mecr"],
        "levels": ["single"],
        "complements": {
            "glossari": True,
            "esquema_visual": True,
            "bastides": True,
            "pictogrames": True,
            "preguntes_comprensio": True,
        },
    }
    return {
        "text": TEXT_INPUT,
        "profile": base_profile,
        "context": {
            "materia": "Ciències Naturals",
            "etapa": profile_def.get("etapa", "eso"),
            "nivell_curs": "3r ESO" if profile_def.get("etapa") != "infantil" else "I5",
            "titol": "## Ecosistemes",
        },
        "params": params,
        "model": model,
    }


def call_adapt_sse(base_url: str, token: str, payload: dict, timeout: int = 300) -> tuple[str, str]:
    """Crida SSE bloquejant. Retorna (text_final, model_usat)."""
    url = f"{base_url}/api/adapt"
    resp = requests.post(url, headers=headers(token), json=payload, stream=True, timeout=timeout)
    if resp.status_code != 200:
        raise RuntimeError(f"HTTP {resp.status_code}: {resp.text[:300]}")
    text_chunks: list[str] = []
    final_text = ""
    model_used = ""
    got_done = False
    for line in resp.iter_lines(decode_unicode=True):
        if not line or not line.startswith("data: "):
            continue
        try:
            ev = json.loads(line[6:])
        except Exception:
            continue
        et = ev.get("type")
        if et == "delta":
            chunk = ev.get("text") or ""
            if chunk:
                text_chunks.append(chunk)
        elif et == "result":
            final_text = ev.get("adapted") or ""
        elif et == "step":
            msg = ev.get("msg") or ""
            # Captura el model usat del missatge "Generant adaptació amb X..."
            m = re.search(r"amb ([^.\(]+?)(?:\s*\(|\.|$)", msg)
            if m and "Generant" in msg:
                model_used = m.group(1).strip()
        elif et == "error":
            raise RuntimeError(f"SSE error: {ev.get('error') or ev.get('message')}")
        elif et == "done":
            got_done = True
            break
    if not got_done:
        raise RuntimeError("SSE closed without 'done'")
    return (final_text or "".join(text_chunks)), model_used


# ══════════════════════════════════════════════════════════════════════════
# Parsing seccions del text adaptat
# ══════════════════════════════════════════════════════════════════════════

def parse_sections(full_text: str) -> dict[str, str]:
    """Separa el text complet en seccions `## Header`. Retorna {header: body}."""
    if not full_text:
        return {}
    pattern = r"^##\s+(.+?)\s*$"
    lines = full_text.split("\n")
    sections: dict[str, str] = {}
    current_header = None
    buf: list[str] = []
    for line in lines:
        m = re.match(pattern, line)
        if m:
            if current_header is not None:
                sections[current_header] = "\n".join(buf).strip()
            current_header = m.group(1).strip()
            buf = []
        else:
            buf.append(line)
    if current_header is not None:
        sections[current_header] = "\n".join(buf).strip()
    return sections


# ══════════════════════════════════════════════════════════════════════════
# Mètriques pedagògiques (sobre text adaptat NET)
# ══════════════════════════════════════════════════════════════════════════

def tokenize_words(s: str) -> list[str]:
    return re.findall(r"[A-Za-zÀ-ÿ]{2,}", s)


def split_sentences(s: str) -> list[str]:
    raw = re.split(r"[\.!?]+", s)
    return [x.strip() for x in raw if x.strip()]


def compute_metrics(text: str) -> dict:
    if not text:
        return {"n_words": 0, "n_sents": 0, "avg_words_per_sent": 0.0,
                "complex_words_pct": 0.0, "n_chars": 0}
    words = tokenize_words(text)
    sents = split_sentences(text)
    complex_words = [w for w in words if len(w) > 7]
    return {
        "n_words": len(words),
        "n_sents": len(sents),
        "avg_words_per_sent": round(len(words) / max(len(sents), 1), 2),
        "complex_words_pct": round(len(complex_words) / max(len(words), 1) * 100, 1),
        "n_chars": len(text),
    }


def has_l1_in_glossary(glossari_text: str, l1_name: str) -> bool:
    """Detecta si el glossari té traducció a L1."""
    if not glossari_text:
        return False
    t = glossari_text.lower()
    if l1_name.lower() in t:
        return True
    # Heurística per alfabets no llatins (àrab, xinès, ciríl·lic)
    if re.search(r"[؀-ۿ一-鿿Ѐ-ӿ]", glossari_text):
        return True
    return False


# ══════════════════════════════════════════════════════════════════════════
# Estadístiques agregades
# ══════════════════════════════════════════════════════════════════════════

def aggregate(values: list[float]) -> dict:
    """Min/mean/max/std d'una llista de valors numèrics."""
    if not values:
        return {"n": 0}
    return {
        "n": len(values),
        "min": round(min(values), 2),
        "mean": round(statistics.mean(values), 2),
        "max": round(max(values), 2),
        "std": round(statistics.stdev(values), 2) if len(values) > 1 else 0.0,
    }


def histogram_str(values: list[float], bins: int = 5, width: int = 20) -> str:
    """ASCII histogram horitzontal compacte."""
    if not values:
        return ""
    lo, hi = min(values), max(values)
    if hi == lo:
        return f"  · tots {lo}"
    step = (hi - lo) / bins
    buckets = [0] * bins
    for v in values:
        idx = min(int((v - lo) / step), bins - 1)
        buckets[idx] += 1
    max_b = max(buckets)
    rows = []
    for i in range(bins):
        bound_lo = lo + i * step
        bound_hi = lo + (i + 1) * step
        bar = "█" * int(buckets[i] / max_b * width) if max_b else ""
        rows.append(f"  [{bound_lo:.2f}-{bound_hi:.2f}] {bar} ({buckets[i]})")
    return "\n".join(rows)


# ══════════════════════════════════════════════════════════════════════════
# Anàlisi de patrons per perfil
# ══════════════════════════════════════════════════════════════════════════

def analyze_profile(profile_def: dict, runs: list[dict]) -> dict:
    """Agrega resultats de N runs i detecta patrons + alertes."""
    original_metrics = compute_metrics(TEXT_INPUT)
    valid = [r for r in runs if r.get("ok")]

    if not valid:
        return {"profile": profile_def["slug"], "n_ok": 0, "n_failed": len(runs),
                "alerts": [{"level": "RED", "msg": "Cap execució exitosa"}]}

    ratios = [r["net_metrics"]["n_words"] / max(original_metrics["n_words"], 1) for r in valid]
    avg_wps = [r["net_metrics"]["avg_words_per_sent"] for r in valid]
    complex_pct = [r["net_metrics"]["complex_words_pct"] for r in valid]
    net_word_counts = [r["net_metrics"]["n_words"] for r in valid]

    # Complements presents per execució
    sections_per_run = [r.get("complement_sections", []) for r in valid]
    all_complements = set()
    for s in sections_per_run:
        all_complements.update(s)
    presence_rate = {}
    for c in all_complements:
        presence_rate[c] = round(
            sum(1 for s in sections_per_run if c in s) / len(valid) * 100, 0
        )

    # Per nouvinguts: % runs amb L1 al glossari
    l1_rate = None
    is_nouvingut = "nouvingut" in profile_def.get("caracteristiques", {})
    if is_nouvingut:
        l1 = profile_def["caracteristiques"]["nouvingut"].get("l1", "")
        l1_hits = sum(1 for r in valid if r.get("has_l1_in_glossary"))
        l1_rate = round(l1_hits / len(valid) * 100, 0)

    # Models usats
    models_used = [r.get("model_used", "?") for r in valid]
    model_counts = {}
    for m in models_used:
        model_counts[m] = model_counts.get(m, 0) + 1

    # ─── Generació d'alertes basades en patrons ───
    alerts = []
    ratio_agg = aggregate(ratios)

    # Cas 1: nouvingut + A1 — hauria de reduir paraules
    if profile_def["slug"] == "03_nouvingut_arab_A1":
        if ratio_agg["mean"] > 0.85:
            alerts.append({"level": "RED",
                "msg": f"Nouvingut A1 NO redueix prou: ratio mitjà {ratio_agg['mean']} (esperat <0.7)"})
        elif ratio_agg["mean"] > 0.7:
            alerts.append({"level": "YELLOW",
                "msg": f"Nouvingut A1 redueix poc: ratio mitjà {ratio_agg['mean']}"})
        if l1_rate is not None and l1_rate < 80:
            alerts.append({"level": "RED",
                "msg": f"Glossari L1 absent en {100-l1_rate:.0f}% de les execucions"})

    # Cas 2: TDAH+B2 — frases curtes esperades
    if profile_def["slug"] == "01_tdah_B2":
        wps_agg = aggregate(avg_wps)
        if wps_agg["mean"] > 14:
            alerts.append({"level": "YELLOW",
                "msg": f"TDAH: frases massa llargues, mitjana {wps_agg['mean']} (esperat <12)"})

    # Cas 3: AC+B2 — NO rebaixa
    if profile_def["slug"] == "04_aacc_B2":
        if ratio_agg["mean"] < 0.9:
            alerts.append({"level": "RED",
                "msg": f"AC: rebaixa el text (ratio {ratio_agg['mean']}). Hauria d'enriquir"})
        complex_agg = aggregate(complex_pct)
        if complex_agg["mean"] < 18:
            alerts.append({"level": "YELLOW",
                "msg": f"AC: vocabulari pobre ({complex_agg['mean']}% paraules complexes)"})

    # Cas 4: Infantil — reducció dràstica esperada
    if profile_def["slug"] == "05_infantil_I5_preA1":
        if ratio_agg["mean"] > 0.6:
            alerts.append({"level": "RED",
                "msg": f"Infantil: no redueix prou (ratio {ratio_agg['mean']}, esperat <0.5)"})
        wps_agg = aggregate(avg_wps)
        if wps_agg["mean"] > 10:
            alerts.append({"level": "RED",
                "msg": f"Infantil: frases massa llargues ({wps_agg['mean']} p/frase, esperat <8)"})

    # Cas 5: dislèxia B1 — paraules curtes esperades
    if profile_def["slug"] == "02_dislexia_B1":
        complex_agg = aggregate(complex_pct)
        if complex_agg["mean"] > 20:
            alerts.append({"level": "YELLOW",
                "msg": f"Dislèxia: massa paraules llargues ({complex_agg['mean']}%)"})

    # Patró universal: dispersió molt alta = LLM inestable
    if ratio_agg.get("std", 0) > 0.25:
        alerts.append({"level": "YELLOW",
            "msg": f"Output inestable: std del ratio paraules = {ratio_agg['std']} (>0.25)"})

    # Si tot OK, marca verd implícit
    if not alerts:
        alerts.append({"level": "GREEN", "msg": "Comportament dins l'esperat"})

    return {
        "profile": profile_def["slug"],
        "expectation_note": profile_def["expectation_note"],
        "n_ok": len(valid),
        "n_failed": len(runs) - len(valid),
        "original_words": original_metrics["n_words"],
        "ratio_net": ratio_agg,
        "net_words": aggregate(net_word_counts),
        "avg_words_per_sent": aggregate(avg_wps),
        "complex_words_pct": aggregate(complex_pct),
        "ratios_raw": [round(r, 2) for r in ratios],
        "complement_presence_pct": presence_rate,
        "l1_in_glossary_pct": l1_rate,
        "models_used": model_counts,
        "alerts": alerts,
    }


# ══════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════

def run_one(base_url: str, token: str, profile_def: dict, model: str) -> dict:
    t0 = time.time()
    try:
        full_text, model_used = call_adapt_sse(base_url, token, build_payload(profile_def, model))
    except Exception as e:
        return {"ok": False, "error": str(e), "latency_s": round(time.time() - t0, 1)}

    sections = parse_sections(full_text)
    text_net = sections.get("Text adaptat", "")
    net_metrics = compute_metrics(text_net)
    complement_sections = [k for k in sections if k != "Text adaptat" and sections[k].strip()]

    has_l1 = False
    nouvingut = profile_def.get("caracteristiques", {}).get("nouvingut")
    if nouvingut:
        has_l1 = has_l1_in_glossary(sections.get("Glossari", ""), nouvingut.get("l1", ""))

    return {
        "ok": True,
        "latency_s": round(time.time() - t0, 1),
        "model_used": model_used,
        "full_text_len": len(full_text),
        "net_metrics": net_metrics,
        "sections_present": list(sections.keys()),
        "complement_sections": complement_sections,
        "has_l1_in_glossary": has_l1,
        "text_net_sample": text_net[:300],
    }


def print_profile_report(report: dict) -> None:
    print(f"\n{'─'*78}")
    print(f"  {report['profile']}  ·  {report['expectation_note']}")
    print(f"{'─'*78}")
    print(f"  Execucions OK: {report['n_ok']} (errors: {report['n_failed']})")
    if report["n_ok"] == 0:
        for a in report["alerts"]:
            print(f"  {a['level']}: {a['msg']}")
        return
    r = report["ratio_net"]
    print(f"\n  Original: {report['original_words']} paraules")
    print(f"  RATIO NET (out_net/in):  min={r['min']}  mean={r['mean']}  max={r['max']}  std={r['std']}")
    print(f"  raw: {report['ratios_raw']}")
    w = report["net_words"]
    print(f"  Paraules NET adaptat:    min={w['min']}  mean={w['mean']}  max={w['max']}")
    s = report["avg_words_per_sent"]
    print(f"  Paraules per frase:      min={s['min']}  mean={s['mean']}  max={s['max']}")
    c = report["complex_words_pct"]
    print(f"  % paraules >7 lletres:   min={c['min']}%  mean={c['mean']}%  max={c['max']}%")
    print(f"  Models usats: {report['models_used']}")
    print(f"\n  Complements presents (% execucions):")
    for comp, pct in sorted(report["complement_presence_pct"].items(), key=lambda x: -x[1]):
        print(f"    {comp:30s} {pct:.0f}%")
    if report.get("l1_in_glossary_pct") is not None:
        print(f"  L1 al glossari: {report['l1_in_glossary_pct']:.0f}% de les execucions")
    print(f"\n  Alertes:")
    for a in report["alerts"]:
        marker = {"GREEN": "✓", "YELLOW": "~", "RED": "✗"}.get(a["level"], "?")
        print(f"    {marker} {a['level']}: {a['msg']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--token", default="", help="JWT (cal per Cloud Run, opcional localhost)")
    ap.add_argument("--base-url", default=DEFAULT_BASE_URL)
    ap.add_argument("--model", default="", help="Model override (default: rotatiu)")
    ap.add_argument("--repetitions", type=int, default=5, help="Repeticions per perfil")
    ap.add_argument("--profiles", nargs="*", help="Slugs perfils (default: tots)")
    ap.add_argument("--save", default="", help="Guarda runs raw a aquest fitxer JSON")
    args = ap.parse_args()

    profiles = PROFILES
    if args.profiles:
        profiles = [p for p in PROFILES if p["slug"] in args.profiles]
        if not profiles:
            sys.exit(f"Cap perfil coincideix amb {args.profiles}")

    total_runs = len(profiles) * args.repetitions
    print(f"\n{'='*78}")
    print(f"  Test descriptiu d'aplicació del perfil")
    print(f"  {len(profiles)} perfils × {args.repetitions} repeticions = {total_runs} crides")
    print(f"  Base: {args.base_url}")
    print(f"  Model: {args.model or '(rotatiu)'}")
    print(f"{'='*78}\n")

    all_data: dict[str, list[dict]] = defaultdict(list)
    t_start = time.time()
    run_idx = 0

    for p in profiles:
        for rep in range(args.repetitions):
            run_idx += 1
            print(f"  [{run_idx}/{total_runs}] {p['slug']} rep {rep+1}/{args.repetitions}...", end="", flush=True)
            r = run_one(args.base_url, args.token, p, args.model)
            all_data[p["slug"]].append(r)
            if r["ok"]:
                print(f" ✓ {r['latency_s']}s · ratio_net="
                      f"{r['net_metrics']['n_words']/max(compute_metrics(TEXT_INPUT)['n_words'],1):.2f} "
                      f"({r['model_used']})")
            else:
                print(f" ✗ {r['latency_s']}s · {r.get('error','')[:80]}")

    elapsed = time.time() - t_start
    print(f"\n  Temps total: {elapsed:.1f}s ({elapsed/60:.1f} min)")

    # Anàlisi per perfil
    print(f"\n{'='*78}")
    print(f"  ANÀLISI PER PERFIL")
    print(f"{'='*78}")

    all_reports = []
    for p in profiles:
        report = analyze_profile(p, all_data[p["slug"]])
        all_reports.append(report)
        print_profile_report(report)

    # Resum executiu
    print(f"\n{'='*78}")
    print(f"  RESUM EXECUTIU")
    print(f"{'='*78}")
    counts = {"GREEN": 0, "YELLOW": 0, "RED": 0}
    for r in all_reports:
        level = "GREEN"
        for a in r["alerts"]:
            if a["level"] == "RED":
                level = "RED"
                break
            if a["level"] == "YELLOW" and level != "RED":
                level = "YELLOW"
        counts[level] += 1
        print(f"  · {r['profile']:30s} → {level}  ({r['n_ok']}/{r['n_ok']+r['n_failed']} OK)")
    print()
    print(f"  GREEN: {counts['GREEN']}   YELLOW: {counts['YELLOW']}   RED: {counts['RED']}")

    if args.save:
        out = {
            "meta": {
                "base_url": args.base_url,
                "model_override": args.model,
                "repetitions": args.repetitions,
                "total_seconds": round(elapsed, 1),
            },
            "runs": dict(all_data),
            "reports": all_reports,
        }
        Path(args.save).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n  Report raw guardat a: {args.save}")


if __name__ == "__main__":
    main()
