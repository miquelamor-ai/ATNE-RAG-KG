#!/usr/bin/env python3
"""
Xat 9 — Anàlisi estadística de l'experiment A/B
- Wilcoxon parells aparellats (p<0.05 amb correcció Bonferroni)
- Effect size Cohen's d
- Correlació inter-jutge (GPT-4o vs Claude Sonnet)
- Kappa Cohen per concordança
- Visualitzacions
"""

import json, sys
import numpy as np
from pathlib import Path
from scipy import stats
from collections import defaultdict

EXP_DIR = Path(__file__).resolve().parent
EVAL_PATH = EXP_DIR / "resultats_avaluacio.json"
REPORT_PATH = EXP_DIR / "informe_resultats.md"


def load_data():
    data = json.loads(EVAL_PATH.read_text(encoding="utf-8"))
    return data["avaluacions"]


def extract_scores(evals: list, jutge: str) -> dict:
    """Extreu puntuacions per condició i criteri."""
    criteris = ["adequacio_linguistica", "fidelitat_curricular", "adequacio_perfil",
                "llegibilitat_estructura", "complements"]
    scores = {"A": defaultdict(list), "B": defaultdict(list)}

    for ev in evals:
        for condicio in ["A", "B"]:
            judge_data = ev["evaluations"].get(condicio, {}).get(jutge, {})
            if "error" in judge_data:
                continue
            for c in criteris:
                if c in judge_data and "puntuacio" in judge_data[c]:
                    scores[condicio][c].append(judge_data[c]["puntuacio"])

    return scores


def cohens_d(a, b):
    """Effect size Cohen's d per a mostres aparellades."""
    diff = np.array(a) - np.array(b)
    return np.mean(diff) / np.std(diff, ddof=1) if np.std(diff, ddof=1) > 0 else 0


def interpret_d(d):
    d = abs(d)
    if d < 0.2:
        return "negligible"
    elif d < 0.5:
        return "petit"
    elif d < 0.8:
        return "mitjà"
    else:
        return "gran"


def interpret_decision(mean_diff, d):
    """Decisió segons llindars de l'experiment."""
    if abs(mean_diff) > 0.5 and abs(d) >= 0.3:
        return "PROMPT COMPLET VAL LA PENA" if mean_diff > 0 else "PROMPT MÍNIM SUFICIENT"
    elif abs(mean_diff) < 0.3:
        return "DIFERÈNCIA NEGLIGIBLE — prompt mínim suficient"
    else:
        return "ZONA GRISA — cal més dades"


def kappa_cohen_simple(scores_j1, scores_j2):
    """Kappa Cohen simplificat per a escales ordinals (linealitzat)."""
    if len(scores_j1) != len(scores_j2) or len(scores_j1) == 0:
        return 0
    # Convertir a acord/desacord amb tolerància ±1
    agree = sum(1 for a, b in zip(scores_j1, scores_j2) if abs(a - b) <= 1)
    n = len(scores_j1)
    po = agree / n
    pe = 0.5  # probabilitat d'acord per atzar (simplificat)
    if pe >= 1:
        return 1
    return (po - pe) / (1 - pe)


def analyze():
    evals = load_data()
    print(f"Avaluacions carregades: {len(evals)}")

    criteris = ["adequacio_linguistica", "fidelitat_curricular", "adequacio_perfil",
                "llegibilitat_estructura", "complements"]
    pesos = [0.25, 0.20, 0.25, 0.15, 0.15]

    report_lines = []
    report_lines.append("# Informe Xat 9 — Experiment A/B: Prompt mínim vs complet\n")
    report_lines.append(f"**Data**: {EXP_DIR / 'resultats_avaluacio.json'}\n")
    report_lines.append(f"**Parells avaluats**: {len(evals)}\n")

    for jutge in ["gpt4o", "claude_sonnet"]:
        jutge_nom = "GPT-4o" if jutge == "gpt4o" else "Claude Sonnet"
        report_lines.append(f"\n## Resultats — Jutge: {jutge_nom}\n")

        scores = extract_scores(evals, jutge)

        report_lines.append("| Criteri | Mitjana A | Mitjana B | Diff (B-A) | Wilcoxon p | Cohen's d | Interpretació |")
        report_lines.append("|---|---|---|---|---|---|---|")

        all_weighted_a = []
        all_weighted_b = []

        for i, c in enumerate(criteris):
            sa = scores["A"][c]
            sb = scores["B"][c]
            n = min(len(sa), len(sb))

            if n < 5:
                report_lines.append(f"| {c} | — | — | — | n<5 | — | — |")
                continue

            sa, sb = sa[:n], sb[:n]
            mean_a = np.mean(sa)
            mean_b = np.mean(sb)
            diff = mean_b - mean_a

            # Wilcoxon
            try:
                stat_w, p_val = stats.wilcoxon(sb, sa, alternative='two-sided')
            except Exception:
                p_val = 1.0

            # Bonferroni
            p_bonferroni = min(p_val * len(criteris), 1.0)

            # Cohen's d
            d = cohens_d(sb, sa)

            sig = "**" if p_bonferroni < 0.05 else ""
            report_lines.append(
                f"| {c} | {mean_a:.2f} | {mean_b:.2f} | {diff:+.2f} | "
                f"{p_bonferroni:.4f}{sig} | {d:+.2f} ({interpret_d(d)}) | "
                f"{interpret_decision(diff, d)} |"
            )

            # Acumular per puntuació global ponderada
            for j in range(n):
                if len(all_weighted_a) <= j:
                    all_weighted_a.append(0)
                    all_weighted_b.append(0)
                all_weighted_a[j] += sa[j] * pesos[i]
                all_weighted_b[j] += sb[j] * pesos[i]

        # Puntuació global
        if len(all_weighted_a) >= 5:
            ga = np.array(all_weighted_a)
            gb = np.array(all_weighted_b)
            global_diff = np.mean(gb) - np.mean(ga)
            try:
                _, gp = stats.wilcoxon(gb, ga)
            except Exception:
                gp = 1.0
            gd = cohens_d(gb, ga)
            report_lines.append(f"\n**Puntuació global ponderada**: A={np.mean(ga):.2f}, B={np.mean(gb):.2f}, "
                              f"Diff={global_diff:+.2f}, p={gp:.4f}, d={gd:+.2f}")
            report_lines.append(f"\n**Decisió**: {interpret_decision(global_diff, gd)}\n")

    # Concordança inter-jutge
    report_lines.append("\n## Concordança inter-jutge (GPT-4o vs Claude Sonnet)\n")
    scores_gpt = extract_scores(evals, "gpt4o")
    scores_claude = extract_scores(evals, "claude_sonnet")

    for c in criteris:
        for condicio in ["A", "B"]:
            sg = scores_gpt[condicio][c]
            sc = scores_claude[condicio][c]
            n = min(len(sg), len(sc))
            if n >= 5:
                kappa = kappa_cohen_simple(sg[:n], sc[:n])
                corr = np.corrcoef(sg[:n], sc[:n])[0, 1] if n >= 3 else 0
                report_lines.append(f"- **{c}** ({condicio}): Kappa={kappa:.2f}, r={corr:.2f}, n={n}")

    # Anàlisi per etapa
    report_lines.append("\n## Diferències per etapa\n")
    for etapa in ["primaria", "ESO", "batxillerat"]:
        evals_etapa = [e for e in evals if e.get("etapa") == etapa]
        if len(evals_etapa) < 3:
            continue
        scores_e = extract_scores(evals_etapa, "gpt4o")
        for c in criteris:
            sa = scores_e["A"][c]
            sb = scores_e["B"][c]
            n = min(len(sa), len(sb))
            if n >= 3:
                diff = np.mean(sb[:n]) - np.mean(sa[:n])
                report_lines.append(f"- {etapa} / {c}: diff={diff:+.2f} (n={n})")

    # Escriure informe
    report = "\n".join(report_lines)
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"\nInforme generat: {REPORT_PATH}")
    print("\n" + report)


if __name__ == "__main__":
    analyze()
