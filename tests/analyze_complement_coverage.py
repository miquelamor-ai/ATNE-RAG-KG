"""Anàlisi A2: cobertura real de complements al pilot.

Per cada perfil declarat i per cada model LLM, mesura:
  - % d'adaptacions amb cada complement present a l'output
  - Si el cross-tab perfil × model mostra que algun model és pitjor

Resposta a la pregunta 1 ("sempre es creen quan toca?") amb dades dures
sobre les 155+ adaptacions del pilot.

Ús: PYTHONIOENCODING=utf-8 python tests/analyze_complement_coverage.py
"""

from __future__ import annotations
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
HEADERS = {"apikey": SERVICE_KEY, "Authorization": f"Bearer {SERVICE_KEY}"}
BASE = f"{SUPABASE_URL}/rest/v1"

# Tots els complements coneguts del sistema (frontend + backend)
KNOWN_COMPLEMENTS = {
    "Glossari": ["glossari"],
    "Esquema visual": ["esquema visual", "esquema_visual"],
    "Mapa conceptual": ["mapa conceptual"],
    "Mapa mental": ["mapa mental"],
    "Bastides": ["bastides", "bastida", "scaffolding"],
    "Suports": ["suports"],  # rename MECR baix
    "Preguntes de comprensió": ["preguntes de comprensió", "preguntes"],
    "Activitats d'aprofundiment": ["activitats d'aprofundiment"],
    "Pictogrames": ["pictogrames"],
    "Resum": ["resum"],
    "Argumentació pedagògica": ["argumentació pedagògica"],
    "Notes d'auditoria": ["notes d'auditoria"],
    "TOLC": ["traducció", "tolc"],
}


def detect_complements(adapted_text: str) -> dict[str, bool]:
    """Detecta quins complements apareixen al text.

    Dos formats al pilot:
    - Taller: headers markdown `## Glossari` (capitalitzat)
    - Flash:  headers majúscules `GLOSSARI` (sense ##) o `**GLOSSARI**`
    """
    if not adapted_text:
        return {k: False for k in KNOWN_COMPLEMENTS}
    # Format Taller
    md_headers = [h.strip().lower() for h in re.findall(r"^##\s+(.+?)\s*$", adapted_text, flags=re.M)]
    # Format Flash: línia que comença amb majúscules tot el contingut o **MAJUSC**
    # Pattern: línies amb només majúscules + accents + espais + signe puntuació, possible negreta
    flash_headers = []
    for line in adapted_text.split("\n"):
        line = line.strip()
        if not line:
            continue
        # Treu negretes inicials
        cleaned = re.sub(r"^\*+", "", re.sub(r"\*+$", "", line)).strip()
        cleaned = cleaned.rstrip(":").strip()
        # Heurística: tot majúscules + algun mot + curt (<60 chars)
        if (len(cleaned) < 60 and cleaned
                and cleaned == cleaned.upper()
                and any(c.isalpha() for c in cleaned)
                and not cleaned.startswith("##")):
            flash_headers.append(cleaned.lower())
    all_headers = md_headers + flash_headers
    result = {}
    for comp, keywords in KNOWN_COMPLEMENTS.items():
        result[comp] = any(any(k in h for k in keywords) for h in all_headers)
    return result


def get_perfils(profile_json: dict) -> list[str]:
    """Extreu perfils declarats — combina ambdós formats."""
    perfils = set()
    chars = profile_json.get("caracteristiques") or {}
    if isinstance(chars, dict):
        for k, v in chars.items():
            if isinstance(v, dict) and v.get("actiu"):
                perfils.add(k)
    perfils_list = profile_json.get("perfils") or []
    for p in perfils_list:
        if isinstance(p, str):
            perfils.add(p)
        elif isinstance(p, dict):
            pid = p.get("id") or p.get("nom")
            if pid:
                perfils.add(pid)
    return list(perfils)


def section(title: str) -> None:
    print(f"\n{'=' * 90}\n {title}\n{'=' * 90}")


def main():
    print("Carregant adaptacions...")
    r = requests.get(
        f"{BASE}/history?select=created_at,adapted_text,profile_json,params_json,"
        f"model_used,models_per_phase&adapted_text=not.is.null"
        f"&order=created_at.desc&limit=2000",
        headers=HEADERS, timeout=30
    )
    rows = r.json()
    print(f"  · {len(rows)} adaptacions")

    # Processem
    enriched = []
    for row in rows:
        adapted = row.get("adapted_text") or ""
        if len(adapted) < 100:
            continue
        comps_present = detect_complements(adapted)
        pj = row.get("profile_json") or {}
        perfils = get_perfils(pj)
        params = row.get("params_json") or {}
        # Format profile (per detectar Flash vs Taller)
        has_chars = bool(pj.get("caracteristiques"))
        is_flash_format = bool(pj.get("perfils") and not has_chars)
        enriched.append({
            "comps": comps_present,
            "perfils": perfils,
            "l1": pj.get("l1") or "",
            "nivell": params.get("nivell") or "?",
            "adaptacio": params.get("adaptacio") or "?",
            "model_used": row.get("model_used") or "?",
            "format": "flash" if is_flash_format else "taller" if has_chars else "altre",
        })
    print(f"  · {len(enriched)} processades")

    # ──── Vista global: % presència de cada complement ────
    section("1. PRESÈNCIA GLOBAL DE COMPLEMENTS")
    total = len(enriched)
    print(f"  N total adaptacions: {total}\n")
    print(f"  {'Complement':<32} {'Presents':>10} {'%':>8}")
    print("  " + "-" * 52)
    for comp in KNOWN_COMPLEMENTS:
        n = sum(1 for e in enriched if e["comps"].get(comp))
        pct = n / total * 100 if total else 0
        bar = "█" * int(pct / 5)
        print(f"  {comp:<32} {n:>10} {pct:>7.1f}%  {bar}")

    # ──── Cross-tab perfil × complement ────
    section("2. COBERTURA PER PERFIL (% adaptacions amb el complement)")
    perfils_list = ["nouvingut", "tdah", "dislexia", "altes_capacitats", "vulnerabilitat",
                    "tea", "di"]
    # Header
    short = {
        "Glossari": "Gloss",
        "Esquema visual": "EsqV",
        "Mapa conceptual": "MapaC",
        "Mapa mental": "MapaM",
        "Bastides": "Bast",
        "Suports": "Sup",
        "Preguntes de comprensió": "Preg",
        "Activitats d'aprofundiment": "ActAp",
        "Pictogrames": "Picto",
        "Resum": "Res",
    }
    comps_show = list(short.keys())
    print(f"  {'Perfil':<20} {'N':>4}  " + "  ".join(f"{short[c]:>6}" for c in comps_show))
    print("  " + "-" * (24 + 8 * len(comps_show)))
    for perfil in perfils_list:
        rows_p = [e for e in enriched if perfil in e["perfils"]]
        if not rows_p:
            continue
        row_str = f"  {perfil:<20} {len(rows_p):>4}  "
        for comp in comps_show:
            n = sum(1 for e in rows_p if e["comps"].get(comp))
            pct = n / len(rows_p) * 100
            row_str += f"{pct:>5.0f}%  "
        print(row_str)

    # ──── Per format profile (Flash vs Taller) ────
    section("3. COBERTURA PER FORMAT DE PROFILE (Flash vs Taller)")
    for fmt in ["taller", "flash", "altre"]:
        rows_f = [e for e in enriched if e["format"] == fmt]
        if not rows_f:
            continue
        print(f"\n  ▶ {fmt}  (N={len(rows_f)})")
        for comp in comps_show:
            n = sum(1 for e in rows_f if e["comps"].get(comp))
            pct = n / len(rows_f) * 100
            print(f"    {comp:<30} {pct:>5.1f}%  ({n}/{len(rows_f)})")

    # ──── Per model LLM (afegit segons indicació de Miquel) ────
    section("4. COBERTURA PER MODEL LLM (l'output depèn del model?)")
    model_counter = Counter(e["model_used"] for e in enriched)
    print(f"  Models al pilot: {dict(model_counter.most_common())}\n")
    top_models = [m for m, _ in model_counter.most_common(6) if m and m != "?"]
    print(f"  {'Complement':<30}  " + "  ".join(f"{m[:14]:>15}" for m in top_models))
    print("  " + "-" * (32 + 17 * len(top_models)))
    for comp in comps_show:
        row_str = f"  {comp:<30}  "
        for m in top_models:
            rows_m = [e for e in enriched if e["model_used"] == m]
            if rows_m:
                n = sum(1 for e in rows_m if e["comps"].get(comp))
                pct = n / len(rows_m) * 100
                row_str += f"{pct:>13.0f}%  "
            else:
                row_str += "          —  "
        print(row_str)

    # ──── Per nivell MECR ────
    section("5. COBERTURA PER MECR DE SORTIDA")
    mecr_order = ["pre-A1", "A1", "A2", "B1", "B2", "C1", "?"]
    print(f"  {'Complement':<30}  " + "  ".join(f"{m:>8}" for m in mecr_order))
    print("  " + "-" * (32 + 10 * len(mecr_order)))
    for comp in comps_show:
        row_str = f"  {comp:<30}  "
        for m in mecr_order:
            rows_m = [e for e in enriched if e["nivell"] == m]
            if rows_m:
                n = sum(1 for e in rows_m if e["comps"].get(comp))
                pct = n / len(rows_m) * 100
                row_str += f"{pct:>7.0f}%  "
            else:
                row_str += "       —  "
        print(row_str)

    # ──── Cas crític: nouvinguts L1 × model ────
    section("6. NOUVINGUTS amb L1 — Glossari per format + model")
    nouv = [e for e in enriched if "nouvingut" in e["perfils"] and e["l1"]]
    print(f"  N nouvinguts amb L1: {len(nouv)}")
    if nouv:
        print(f"\n  Per FORMAT:")
        for fmt in ["taller", "flash", "altre"]:
            rows_f = [e for e in nouv if e["format"] == fmt]
            if rows_f:
                with_gloss = sum(1 for e in rows_f if e["comps"].get("Glossari"))
                print(f"    {fmt:<10}  N={len(rows_f)}  amb Glossari: {with_gloss} ({with_gloss/len(rows_f)*100:.0f}%)")
        print(f"\n  Per MODEL:")
        mcount: dict[str, tuple[int, int]] = defaultdict(lambda: (0, 0))
        for e in nouv:
            n, g = mcount[e["model_used"]]
            mcount[e["model_used"]] = (n + 1, g + (1 if e["comps"].get("Glossari") else 0))
        for m, (n, g) in sorted(mcount.items(), key=lambda x: -x[1][0]):
            print(f"    {m:<25}  N={n}  amb Glossari: {g} ({g/n*100:.0f}%)")

    # ──── Diagnòstic global ────
    section("DIAGNÒSTIC")
    diag = []

    # Glossari per nouvinguts
    if nouv:
        with_g = sum(1 for e in nouv if e["comps"].get("Glossari"))
        rate = with_g / len(nouv) * 100
        if rate < 30:
            diag.append(f"🔴 Glossari absent en {100-rate:.0f}% dels nouvinguts amb L1 ({with_g}/{len(nouv)})")

    # Preguntes activades sempre però mai apareixen
    n_preg = sum(1 for e in enriched if e["comps"].get("Preguntes de comprensió"))
    if n_preg / total < 0.3:
        diag.append(f"🔴 Preguntes de comprensió en només {n_preg/total*100:.0f}% adaptacions")

    # Bastides
    n_bast = sum(1 for e in enriched if e["comps"].get("Bastides"))
    if n_bast / total < 0.3:
        diag.append(f"🟡 Bastides en només {n_bast/total*100:.0f}% adaptacions")

    # Pictogrames
    n_pic = sum(1 for e in enriched if e["comps"].get("Pictogrames"))
    if n_pic / total < 0.3:
        diag.append(f"🟡 Pictogrames en només {n_pic/total*100:.0f}% adaptacions")

    # Diferencies entre models
    print("  Observacions principals:")
    for d in diag:
        print(f"  {d}")
    if not diag:
        print("  (sense alertes globals)")


if __name__ == "__main__":
    main()
