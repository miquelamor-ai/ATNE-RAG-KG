#!/usr/bin/env python3
"""
Peça 4 — Anàlisi de l'experiment A/B skills OFF vs ON.

n=5 casos: NO es fa test de significació (Wilcoxon no té potència amb n=5).
Es produeix una taula DESCRIPTIVA per cas (Δ ON−OFF per criteri + mitjana ponderada)
i una taula global de mitjanes per criteri. Verdict orientatiu segons el llindar
del README (Δ>0.5 → skills valen la pena), explícitament marcat com a senyal
qualitatiu, no prova estadística.

Jutge únic: Claude Sonnet 4.6.
"""

import json, sys, io
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

EXP_DIR = Path(__file__).resolve().parent
EVAL_PATH = EXP_DIR / "resultats_avaluacio.json"
REPORT_PATH = EXP_DIR / "informe_resultats.md"

CRITERIS = [
    ("adequacio_linguistica", "Adequació lingüística MECR", 0.25),
    ("fidelitat_curricular",  "Fidelitat curricular",       0.20),
    ("adequacio_perfil",      "Adequació al perfil",        0.25),
    ("llegibilitat_estructura", "Llegibilitat/estructura",  0.15),
    ("complements",           "Complements",                0.15),
]


def score(judge_data: dict, crit_id: str):
    """Retorna la puntuació (1-5) d'un criteri, o None si falta/error."""
    if not isinstance(judge_data, dict) or "error" in judge_data:
        return None
    c = judge_data.get(crit_id)
    if isinstance(c, dict) and isinstance(c.get("puntuacio"), (int, float)):
        return float(c["puntuacio"])
    return None


def weighted_mean(judge_data: dict):
    """Mitjana ponderada dels 5 criteris; None si falta algun."""
    total, w_sum = 0.0, 0.0
    for cid, _nom, pes in CRITERIS:
        s = score(judge_data, cid)
        if s is None:
            return None
        total += s * pes
        w_sum += pes
    return round(total / w_sum, 2) if w_sum else None


def fmt(v):
    return f"{v:.1f}" if isinstance(v, (int, float)) else "—"


def fmt_delta(on, off):
    if isinstance(on, (int, float)) and isinstance(off, (int, float)):
        d = on - off
        return f"{d:+.1f}"
    return "—"


def analyze():
    data = json.loads(EVAL_PATH.read_text(encoding="utf-8"))
    evals = data["avaluacions"]
    jutge = data.get("jutge", "Claude Sonnet 4.6")

    L = []
    L.append("# Informe Peça 4 — Experiment A/B: skills OFF vs ON\n")
    L.append(f"**Jutge**: {jutge}  ·  **Casos avaluats**: {len(evals)}\n")
    L.append("> n=5 → senyal QUALITATIU, no prova estadística. "
             "Δ = ON − OFF. Llindar orientatiu: Δ>0.5 = les skills aporten valor.\n")

    # Acumuladors globals per criteri
    glob = {cid: {"OFF": [], "ON": []} for cid, _n, _p in CRITERIS}
    glob_wmean = {"OFF": [], "ON": []}

    for ev in evals:
        case_id = ev["case_id"]
        genere = ev.get("genere", "")
        mecr = ev.get("mecr", "")
        perfil = ev.get("perfil_id", "")
        skills = ", ".join(ev.get("skills_actives_ON", [])) or "(cap)"
        off = ev["evaluations"].get("OFF", {})
        on = ev["evaluations"].get("ON", {})

        L.append(f"\n## {case_id} — {genere} / {mecr} / {perfil}\n")
        L.append("| Criteri | OFF | ON | Δ (ON−OFF) |")
        L.append("|---|:---:|:---:|:---:|")
        for cid, nom, _pes in CRITERIS:
            s_off = score(off, cid)
            s_on = score(on, cid)
            if s_off is not None:
                glob[cid]["OFF"].append(s_off)
            if s_on is not None:
                glob[cid]["ON"].append(s_on)
            L.append(f"| {nom} | {fmt(s_off)} | {fmt(s_on)} | {fmt_delta(s_on, s_off)} |")

        wm_off = weighted_mean(off)
        wm_on = weighted_mean(on)
        if wm_off is not None:
            glob_wmean["OFF"].append(wm_off)
        if wm_on is not None:
            glob_wmean["ON"].append(wm_on)
        L.append(f"| **Mitjana ponderada** | **{fmt(wm_off)}** | **{fmt(wm_on)}** | **{fmt_delta(wm_on, wm_off)}** |")
        L.append(f"\nSkills actives ON: {skills}")

        # Justificacions del jutge (per a la revisió pedagògica)
        for cond, jd in [("OFF", off), ("ON", on)]:
            just = []
            for cid, nom, _p in CRITERIS:
                c = jd.get(cid) if isinstance(jd, dict) else None
                if isinstance(c, dict) and c.get("justificacio"):
                    just.append(f"  - *{nom}*: {c['justificacio']}")
            if just:
                L.append(f"\nJustificació jutge ({cond}):")
                L.extend(just)

    # Taula global
    L.append("\n## Resum global per criteri (mitjana dels casos)\n")
    L.append("| Criteri | OFF mitjà | ON mitjà | Δ mitjà |")
    L.append("|---|:---:|:---:|:---:|")

    def avg(xs):
        return round(sum(xs) / len(xs), 2) if xs else None

    for cid, nom, _pes in CRITERIS:
        a_off = avg(glob[cid]["OFF"])
        a_on = avg(glob[cid]["ON"])
        L.append(f"| {nom} | {fmt(a_off)} | {fmt(a_on)} | {fmt_delta(a_on, a_off)} |")

    g_off = avg(glob_wmean["OFF"])
    g_on = avg(glob_wmean["ON"])
    L.append(f"| **Mitjana ponderada global** | **{fmt(g_off)}** | **{fmt(g_on)}** | **{fmt_delta(g_on, g_off)}** |")

    # Verdict orientatiu
    L.append("\n## Verdict orientatiu\n")
    if isinstance(g_on, (int, float)) and isinstance(g_off, (int, float)):
        delta = g_on - g_off
        if delta > 0.5:
            verdict = "🟢 Les skills aporten valor clar (Δ>0.5)."
        elif delta < 0.3:
            verdict = "🔴 Diferència negligible (Δ<0.3) — skills sense impacte mesurable."
        else:
            verdict = "🟡 Zona grisa (0.3≤Δ≤0.5) — senyal feble, calen més casos."
        L.append(f"Δ ponderada global = **{delta:+.2f}** → {verdict}")
    else:
        L.append("Dades insuficients per a un verdict global.")
    L.append("\n> Recordatori: n=5. Aquest verdict és orientatiu i requereix la revisió "
             "pedagògica humana dels textos a `resultats_generacio.json`.")

    # ── Limitacions i abast (caveat metodològic obligatori) ──
    L.append("\n## Limitacions i abast\n")
    L.append(
        "Aquest experiment mesura **combinacions concretes** de gènere + perfil + MECR + "
        "complement, una per cas, NO l'efecte d'un perfil en general:\n")
    L.append(
        "- **No extrapolable a un perfil sencer.** El cas 2 mesura «conte + pictogrames per a "
        "TEA a pre-A1», NO «les skills milloren per a TEA en general». El corpus FJE és explícit "
        "que TEA, TDAH, altes capacitats i dislèxia són **independents del nivell MECR** (un mateix "
        "perfil pot tenir qualsevol nivell de llengua), de manera que el MECR de cada cas és una "
        "decisió de disseny de l'experiment, no una propietat del perfil.")
    L.append(
        "- **n=5, un cas per combinació.** Cap criteri té rèpliques; les diferències són un "
        "senyal il·lustratiu, no una estimació estadística. Variació de temperatura (0.4) i de "
        "mostratge del generador no estan controlades per repetició.")
    L.append(
        "- **El judici és d'un sol jutge** (Claude Sonnet 4.6). Sense segon jutge no es pot estimar "
        "la concordança inter-jutge ni descartar biaix sistemàtic del jutge.")
    L.append(
        "- **Abast de la conclusió.** Un Δ favorable a ON indica que, *per a aquestes 5 combinacions "
        "concretes i amb aquest generador (gemini-2.5-flash-lite)*, activar les skills millora la "
        "qualitat segons la rúbrica. Generalitzar a altres gèneres, perfils, nivells o models "
        "requeriria ampliar el disseny (més casos per combinació, més jutges, més models).")

    report = "\n".join(L)
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"Informe generat: {REPORT_PATH}\n")
    print(report)


if __name__ == "__main__":
    analyze()
