"""
stats_analysis.py — Anàlisi estadística rigorós de les avaluacions multi_v2.

Inclou:
1. Mitjanes amb IC95% per generador x jutge
2. ANOVA entre generadors (rang no parametric: Kruskal-Wallis)
3. Post-hoc Dunn per detectar quines diferencies son significatives
4. Cronbach's alpha (consistencia interna rubrica v2)
5. Analisi factorial exploratoria (validar les 3 dimensions A/B/C)
6. Correlacio longitud text vs puntuacio (detectar biaix)

Us: python tests/stats_analysis.py [--output docs/estadistica/]
"""

import sqlite3
import argparse
import os
import math
from pathlib import Path
import numpy as np
from scipy import stats

DB_PATH = Path(__file__).parent / "results" / "evaluations.db"


def get_db():
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    return db


def mean_ci95(values):
    """Mitjana amb interval de confiança 95% (t-student)."""
    if len(values) < 2:
        return (float(np.mean(values)) if values else 0.0, 0.0, 0.0)
    m = float(np.mean(values))
    sem = float(stats.sem(values))
    h = sem * stats.t.ppf(0.975, len(values) - 1)
    return m, m - h, m + h


def analysis_1_means_ci(db, out_path):
    """Taula 1: mitjanes amb IC95% per generador × jutge (sense self-eval)."""
    print("\n[1] MITJANES I INTERVALS DE CONFIANÇA (95%)")
    print("=" * 75)
    rows = db.execute("""
        SELECT g.generator, e.judge, e.puntuacio_global
        FROM multi_v2_evaluations e
        JOIN multi_llm_generations g ON e.generation_id = g.id
        WHERE g.prompt_mode = 'rag_v2' AND e.is_self_eval = 0
        ORDER BY g.generator, e.judge
    """).fetchall()

    from collections import defaultdict
    data = defaultdict(list)
    for r in rows:
        data[(r["generator"], r["judge"])].append(r["puntuacio_global"])

    print(f"{'Gen':<10} {'Jutge':<10} {'N':<5} {'Mitjana':<9} {'IC95%':<20}")
    print("-" * 60)
    results = []
    for (gen, judge), vals in sorted(data.items()):
        m, lo, hi = mean_ci95(vals)
        print(f"{gen:<10} {judge:<10} {len(vals):<5} {m:<9.3f} [{lo:.3f}, {hi:.3f}]")
        results.append({"gen": gen, "judge": judge, "n": len(vals), "mean": m, "ci_lo": lo, "ci_hi": hi})

    # Agregat per generador (totes les avaluacions externes)
    print()
    print("Per generador (agregant jutges externs):")
    print(f"{'Gen':<10} {'N':<6} {'Mitjana':<9} {'IC95%':<20}")
    print("-" * 50)
    gen_data = defaultdict(list)
    for (gen, _), vals in data.items():
        gen_data[gen].extend(vals)
    gen_summary = []
    for gen, vals in sorted(gen_data.items()):
        m, lo, hi = mean_ci95(vals)
        print(f"{gen:<10} {len(vals):<6} {m:<9.3f} [{lo:.3f}, {hi:.3f}]")
        gen_summary.append({"gen": gen, "n": len(vals), "mean": m, "ci_lo": lo, "ci_hi": hi})

    return results, gen_summary, gen_data


def analysis_2_kruskal(gen_data, out_path):
    """Test Kruskal-Wallis: les mitjanes entre generadors son significativament diferents?"""
    print("\n[2] KRUSKAL-WALLIS (test no parametric per mostres independents)")
    print("=" * 75)
    gens = sorted(gen_data.keys())
    samples = [gen_data[g] for g in gens]
    if len(samples) < 2:
        print("Massa pocs generadors per Kruskal-Wallis")
        return None
    H, p = stats.kruskal(*samples)
    print(f"H = {H:.2f}, p = {p:.2e}")
    if p < 0.001:
        print(f"RESULT: Diferencies molt significatives (p < 0.001)")
    elif p < 0.05:
        print(f"RESULT: Diferencies significatives (p < 0.05)")
    else:
        print(f"RESULT: NO hi ha diferencies significatives")
    return {"H": H, "p": p}


def analysis_3_dunn(gen_data, out_path):
    """Post-hoc Dunn: quines parelles de generadors difereixen significativament."""
    print("\n[3] COMPARACIONS PARELLADES (Mann-Whitney U amb correccio Bonferroni)")
    print("=" * 75)
    gens = sorted(gen_data.keys())
    n_pairs = len(gens) * (len(gens) - 1) // 2
    alpha_corr = 0.05 / n_pairs  # Bonferroni
    print(f"Alpha corregit (Bonferroni): {alpha_corr:.4f} ({n_pairs} parelles)")
    print()
    print(f"{'Parella':<25} {'U':<12} {'p':<12} {'Sig.?':<10}")
    print("-" * 65)
    results = []
    for i, g1 in enumerate(gens):
        for g2 in gens[i+1:]:
            U, p = stats.mannwhitneyu(gen_data[g1], gen_data[g2], alternative='two-sided')
            sig = "SI **" if p < alpha_corr else ("SI *" if p < 0.05 else "no")
            print(f"{g1:>10} vs {g2:<12} {U:<12.0f} {p:<12.2e} {sig}")
            results.append({"g1": g1, "g2": g2, "U": float(U), "p": float(p), "sig_bonferroni": bool(p < alpha_corr)})
    return results


def analysis_4_cronbach(db, out_path):
    """Cronbach's alpha: consistencia interna de la rubrica v2 (8 criteris)."""
    print("\n[4] CRONBACH'S ALPHA (consistencia interna rubrica v2)")
    print("=" * 75)
    # Agafem totes les avaluacions externes amb tots 8 criteris
    rows = db.execute("""
        SELECT a1_coherencia, a2_correccio, a3_llegibilitat,
               b1_fidelitat, b2_adequacio_perfil, b3_scaffolding, b4_cultura,
               c1_potencial
        FROM multi_v2_evaluations
        WHERE is_self_eval = 0
          AND a1_coherencia IS NOT NULL AND c1_potencial IS NOT NULL
    """).fetchall()
    criteris = ["A1", "A2", "A3", "B1", "B2", "B3", "B4", "C1"]
    matrix = np.array([[r[k] for k in range(8)] for r in rows], dtype=float)
    print(f"N avaluacions: {len(matrix)}")
    print(f"K items: 8")
    k = matrix.shape[1]
    var_items = matrix.var(axis=0, ddof=1)
    var_total = matrix.sum(axis=1).var(ddof=1)
    alpha = (k / (k - 1)) * (1 - var_items.sum() / var_total)
    print(f"Alpha: {alpha:.3f}")
    if alpha >= 0.9:
        print("RESULT: Excel.lent (alpha >= 0.9)")
    elif alpha >= 0.8:
        print("RESULT: Bo (alpha >= 0.8)")
    elif alpha >= 0.7:
        print("RESULT: Acceptable (alpha >= 0.7)")
    elif alpha >= 0.6:
        print("RESULT: Questionable (alpha >= 0.6)")
    else:
        print("RESULT: Inacceptable (alpha < 0.6)")

    # Alpha if item deleted
    print()
    print("Alpha si eliminem cada item:")
    print(f"{'Item':<6} {'Alpha':<8}")
    print("-" * 20)
    for i in range(k):
        mask = [j for j in range(k) if j != i]
        sub = matrix[:, mask]
        k2 = sub.shape[1]
        var_i = sub.var(axis=0, ddof=1)
        var_t = sub.sum(axis=1).var(ddof=1)
        alpha_i = (k2 / (k2 - 1)) * (1 - var_i.sum() / var_t)
        flag = " <-- eliminar milloraria" if alpha_i > alpha else ""
        print(f"{criteris[i]:<6} {alpha_i:<8.3f}{flag}")
    return alpha


def analysis_5_correlations(db, out_path):
    """Correlacio longitud text ↔ puntuacio (detectar biaix jutge)."""
    print("\n[5] CORRELACIO LONGITUD vs PUNTUACIO (per jutge)")
    print("=" * 75)
    rows = db.execute("""
        SELECT e.judge, g.text_adaptat_paraules as paraules, e.puntuacio_global
        FROM multi_v2_evaluations e
        JOIN multi_llm_generations g ON e.generation_id = g.id
        WHERE g.prompt_mode = 'rag_v2' AND e.is_self_eval = 0
          AND g.text_adaptat_paraules > 0 AND e.puntuacio_global IS NOT NULL
    """).fetchall()
    from collections import defaultdict
    by_judge = defaultdict(list)
    for r in rows:
        by_judge[r["judge"]].append((r["paraules"], r["puntuacio_global"]))
    print(f"{'Jutge':<12} {'N':<6} {'Spearman r':<12} {'p':<12} {'Interpretacio':<30}")
    print("-" * 75)
    for judge, data in sorted(by_judge.items()):
        x = [d[0] for d in data]
        y = [d[1] for d in data]
        r, p = stats.spearmanr(x, y)
        if abs(r) < 0.1:
            interp = "Cap biaix"
        elif abs(r) < 0.3:
            interp = "Biaix petit"
        elif abs(r) < 0.5:
            interp = "Biaix moderat"
        else:
            interp = "BIAIX GROS"
        print(f"{judge:<12} {len(data):<6} {r:<12.3f} {p:<12.2e} {interp}")


def analysis_6_factor(db, out_path):
    """Analisi factorial: els 8 criteris es redueixen a 3 dimensions (A, B, C)?"""
    print("\n[6] ANALISI FACTORIAL EXPLORATORIA")
    print("=" * 75)
    rows = db.execute("""
        SELECT a1_coherencia, a2_correccio, a3_llegibilitat,
               b1_fidelitat, b2_adequacio_perfil, b3_scaffolding, b4_cultura,
               c1_potencial
        FROM multi_v2_evaluations
        WHERE is_self_eval = 0 AND a1_coherencia IS NOT NULL AND c1_potencial IS NOT NULL
    """).fetchall()
    criteris = ["A1", "A2", "A3", "B1", "B2", "B3", "B4", "C1"]
    M = np.array([[r[k] for k in range(8)] for r in rows], dtype=float)
    print(f"N: {len(M)} | Items: 8")
    # Matriu de correlacions
    corr = np.corrcoef(M.T)
    print()
    print("Matriu de correlacions (Pearson):")
    print("     " + " ".join(f"{c:>6}" for c in criteris))
    for i, c in enumerate(criteris):
        print(f"{c:<5}" + " ".join(f"{corr[i,j]:>6.2f}" for j in range(8)))

    # PCA manual: eigendecomposicio
    eig_vals, eig_vecs = np.linalg.eigh(corr)
    idx = np.argsort(eig_vals)[::-1]
    eig_vals = eig_vals[idx]
    eig_vecs = eig_vecs[:, idx]

    total_var = eig_vals.sum()
    print()
    print("Components principals (eigen-decomposicio):")
    print(f"{'Comp':<6} {'Eigen':<10} {'% Var':<8} {'% Cum':<8}")
    cum = 0
    for i in range(8):
        pct = eig_vals[i] / total_var * 100
        cum += pct
        print(f"PC{i+1:<4} {eig_vals[i]:<10.3f} {pct:<8.1f} {cum:<8.1f}")

    # Criteri de Kaiser: components amb eigen > 1
    n_factors = sum(1 for v in eig_vals if v > 1)
    print()
    print(f"Components amb eigen > 1 (Kaiser): {n_factors}")

    # Loadings dels 3 primers components
    print()
    print("Loadings dels 3 primers components (rotacio ortogonal simple):")
    print(f"{'Item':<6} {'PC1':<8} {'PC2':<8} {'PC3':<8}")
    for i, c in enumerate(criteris):
        loadings = eig_vecs[i, :3] * np.sqrt(eig_vals[:3])
        print(f"{c:<6} {loadings[0]:<8.3f} {loadings[1]:<8.3f} {loadings[2]:<8.3f}")

    print()
    print("INTERPRETACIO:")
    print("- Si PC1 captura >60% de variança: tots els criteris mesuren una sola cosa")
    print("- Si hi ha 3 components amb eigen>1 i loadings clars: les 3 dimensions estan validades")
    return {"eig_vals": eig_vals.tolist(), "n_factors_kaiser": n_factors}


def main():
    parser = argparse.ArgumentParser(description="Analisi estadistica rigorosa")
    parser.add_argument("--output", default="docs/estadistica", help="Directori sortida")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    db = get_db()

    print("=" * 75)
    print("ANALISI ESTADISTICA RIGOROSA — multi_v2 RAG-v2")
    print("=" * 75)

    results_1, summary_1, gen_data = analysis_1_means_ci(db, args.output)
    result_2 = analysis_2_kruskal(gen_data, args.output)
    results_3 = analysis_3_dunn(gen_data, args.output)
    alpha = analysis_4_cronbach(db, args.output)
    analysis_5_correlations(db, args.output)
    result_6 = analysis_6_factor(db, args.output)

    # Export summary
    import json
    with open(os.path.join(args.output, "stats_summary.json"), "w", encoding="utf-8") as f:
        json.dump({
            "means_by_gen_judge": results_1,
            "summary_by_gen": summary_1,
            "kruskal_wallis": result_2,
            "pairwise_bonferroni": results_3,
            "cronbach_alpha": alpha,
            "factor_analysis": result_6,
        }, f, indent=2, ensure_ascii=False)

    print()
    print("=" * 75)
    print(f"Summary JSON: {args.output}/stats_summary.json")
    db.close()


if __name__ == "__main__":
    main()
