"""
deep_analysis.py — Analisis profundes de les avaluacions multi_v2.

Inclou:
1. Puntuacio per perfil (quins perfils son mes dificils?)
2. Puntuacio per etapa educativa
3. Puntuacio per genere discursiu
4. Puntuacio per combinacio etapa x genere
5. Analisi d'errors: casos amb puntuacio < 3 (patrons comuns)
6. Inter-judge agreement (Krippendorff's alpha)
7. Correlacio entre jutges (valida consistencia)

Us: python tests/deep_analysis.py [--output docs/estadistica/]
"""

import sqlite3
import argparse
import os
import json
import math
from pathlib import Path
from collections import defaultdict
import numpy as np

DB_PATH = Path(__file__).parent / "results" / "evaluations.db"


def get_db():
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    return db


PERFIL_NOMS = {
    "P1": "Nouvingut arab pre-A1 DUA Acces",
    "P2": "Nouvingut xines A1 DUA Acces",
    "P3": "TDAH A2 DUA Core",
    "P4": "TEA B1 DUA Core",
    "P5": "Dislexia A2 DUA Acces",
    "P6": "DI pre-A1 DUA Acces",
    "P7": "Altes capacitats B2 DUA Enriquiment",
    "P8": "Nouvingut+Dislexia A1 (creuament)",
    "P9": "TDAH+TEA B1 (creuament)",
    "P10": "Vulnerabilitat+TDL A2 (creuament)",
}


def analysis_1_per_perfil(db):
    """Puntuacio per perfil d'alumnat."""
    print("\n[1] PUNTUACIO PER PERFIL D'ALUMNAT (RAG-v2, jutges externs)")
    print("=" * 80)
    rows = db.execute("""
        SELECT SUBSTR(g.cas_id, INSTR(g.cas_id, '__')+2) as perfil_id,
               e.puntuacio_global
        FROM multi_v2_evaluations e
        JOIN multi_llm_generations g ON e.generation_id = g.id
        WHERE g.prompt_mode = 'rag_v2' AND e.is_self_eval = 0
    """).fetchall()
    by_perfil = defaultdict(list)
    for r in rows:
        by_perfil[r["perfil_id"]].append(r["puntuacio_global"])

    def perfil_key(p):
        return int(p[1:]) if p.startswith("P") and p[1:].isdigit() else 99

    print(f"{'ID':<4} {'Perfil':<40} {'N':<5} {'Mitjana':<8} {'Min':<6} {'Max':<6}")
    print("-" * 75)
    results = []
    for perfil in sorted(by_perfil.keys(), key=perfil_key):
        vals = by_perfil[perfil]
        nom = PERFIL_NOMS.get(perfil, perfil)[:38]
        mitjana = np.mean(vals)
        print(f"{perfil:<4} {nom:<40} {len(vals):<5} {mitjana:<8.3f} {min(vals):<6.1f} {max(vals):<6.1f}")
        results.append({"perfil": perfil, "nom": nom, "n": len(vals), "mean": float(mitjana)})

    # Top-3 i bottom-3
    results_sorted = sorted(results, key=lambda r: r["mean"], reverse=True)
    print()
    print("Perfils mes FACILS (puntuacio mes alta):")
    for r in results_sorted[:3]:
        print(f"  {r['perfil']}: {r['mean']:.2f} — {r['nom']}")
    print()
    print("Perfils mes DIFICILS (puntuacio mes baixa):")
    for r in results_sorted[-3:]:
        print(f"  {r['perfil']}: {r['mean']:.2f} — {r['nom']}")
    return results


def analysis_2_per_etapa_genere(db):
    """Puntuacio per etapa educativa i genere discursiu."""
    print("\n[2] PUNTUACIO PER ETAPA I GENERE DISCURSIU")
    print("=" * 80)

    # Per etapa
    rows = db.execute("""
        SELECT g.text_original_etapa as etapa, e.puntuacio_global
        FROM multi_v2_evaluations e
        JOIN multi_llm_generations g ON e.generation_id = g.id
        WHERE g.prompt_mode = 'rag_v2' AND e.is_self_eval = 0 AND g.text_original_etapa IS NOT NULL
    """).fetchall()
    by_etapa = defaultdict(list)
    for r in rows:
        by_etapa[r["etapa"]].append(r["puntuacio_global"])

    print("\nPer ETAPA:")
    print(f"{'Etapa':<12} {'N':<5} {'Mitjana':<8}")
    print("-" * 30)
    etapa_results = []
    for etapa in sorted(by_etapa.keys()):
        vals = by_etapa[etapa]
        m = np.mean(vals)
        print(f"{etapa:<12} {len(vals):<5} {m:<8.3f}")
        etapa_results.append({"etapa": etapa, "n": len(vals), "mean": float(m)})

    # Per genere
    rows = db.execute("""
        SELECT g.text_original_genere as genere, e.puntuacio_global
        FROM multi_v2_evaluations e
        JOIN multi_llm_generations g ON e.generation_id = g.id
        WHERE g.prompt_mode = 'rag_v2' AND e.is_self_eval = 0 AND g.text_original_genere IS NOT NULL
    """).fetchall()
    by_genere = defaultdict(list)
    for r in rows:
        by_genere[r["genere"]].append(r["puntuacio_global"])

    print("\nPer GENERE discursiu:")
    print(f"{'Genere':<15} {'N':<5} {'Mitjana':<8}")
    print("-" * 35)
    genere_results = []
    for genere in sorted(by_genere.keys()):
        vals = by_genere[genere]
        m = np.mean(vals)
        print(f"{genere:<15} {len(vals):<5} {m:<8.3f}")
        genere_results.append({"genere": genere, "n": len(vals), "mean": float(m)})

    return etapa_results, genere_results


def analysis_3_heatmap_etapa_genere(db):
    """Matriu etapa x genere."""
    print("\n[3] HEATMAP: etapa x genere")
    print("=" * 80)
    rows = db.execute("""
        SELECT g.text_original_etapa as etapa, g.text_original_genere as genere,
               e.puntuacio_global
        FROM multi_v2_evaluations e
        JOIN multi_llm_generations g ON e.generation_id = g.id
        WHERE g.prompt_mode = 'rag_v2' AND e.is_self_eval = 0
          AND g.text_original_etapa IS NOT NULL AND g.text_original_genere IS NOT NULL
    """).fetchall()
    cell = defaultdict(list)
    for r in rows:
        cell[(r["etapa"], r["genere"])].append(r["puntuacio_global"])

    etapes = sorted({k[0] for k in cell.keys()})
    generes = sorted({k[1] for k in cell.keys()})
    print()
    print(f"{'etapa':<12}" + " ".join(f"{g[:10]:<11}" for g in generes))
    print("-" * (12 + 11 * len(generes)))
    for e in etapes:
        row = f"{e:<12}"
        for g in generes:
            vals = cell.get((e, g), [])
            if vals:
                row += f"{np.mean(vals):<11.2f}"
            else:
                row += f"{'—':<11}"
        print(row)


def analysis_4_error_analysis(db):
    """Casos amb puntuacio < 3: quins models, perfils, criteris fallen?"""
    print("\n[4] ANALISI D'ERRORS (puntuacio global < 3.0)")
    print("=" * 80)
    rows = db.execute("""
        SELECT g.generator, g.cas_id, e.judge, e.puntuacio_global,
               e.a1_coherencia, e.a2_correccio, e.a3_llegibilitat,
               e.b1_fidelitat, e.b2_adequacio_perfil, e.b3_scaffolding, e.b4_cultura,
               e.c1_potencial, g.text_adaptat_paraules
        FROM multi_v2_evaluations e
        JOIN multi_llm_generations g ON e.generation_id = g.id
        WHERE g.prompt_mode = 'rag_v2' AND e.is_self_eval = 0 AND e.puntuacio_global < 3.0
    """).fetchall()

    print(f"Total casos amb puntuacio < 3.0: {len(rows)}")
    if not rows:
        return
    print()

    # Per generador
    by_gen = defaultdict(int)
    for r in rows:
        by_gen[r["generator"]] += 1
    print("Distribucio per generador:")
    for gen, n in sorted(by_gen.items(), key=lambda x: -x[1]):
        print(f"  {gen:<10} {n:>4} casos")

    # Per perfil
    print()
    by_perfil = defaultdict(int)
    for r in rows:
        perfil = r["cas_id"].split("__")[-1] if "__" in r["cas_id"] else "?"
        by_perfil[perfil] += 1
    print("Distribucio per perfil:")
    for p, n in sorted(by_perfil.items(), key=lambda x: -x[1])[:10]:
        print(f"  {p:<4} {n:>4} casos — {PERFIL_NOMS.get(p, '')[:40]}")

    # Criteris que fallen mes
    print()
    print("Criteris mes baixos en casos erronis (mitjana):")
    criteris = {
        "A1": [r["a1_coherencia"] for r in rows if r["a1_coherencia"] is not None],
        "A2": [r["a2_correccio"] for r in rows if r["a2_correccio"] is not None],
        "A3": [r["a3_llegibilitat"] for r in rows if r["a3_llegibilitat"] is not None],
        "B1": [r["b1_fidelitat"] for r in rows if r["b1_fidelitat"] is not None],
        "B2": [r["b2_adequacio_perfil"] for r in rows if r["b2_adequacio_perfil"] is not None],
        "B3": [r["b3_scaffolding"] for r in rows if r["b3_scaffolding"] is not None],
        "B4": [r["b4_cultura"] for r in rows if r["b4_cultura"] is not None],
        "C1": [r["c1_potencial"] for r in rows if r["c1_potencial"] is not None],
    }
    crit_means = [(k, float(np.mean(v))) for k, v in criteris.items() if v]
    for k, m in sorted(crit_means, key=lambda x: x[1]):
        print(f"  {k}: {m:.2f}")

    # Longitud textos
    paraules = [r["text_adaptat_paraules"] for r in rows if r["text_adaptat_paraules"]]
    if paraules:
        print()
        print(f"Longitud textos erronis: avg={int(np.mean(paraules))} par (min={min(paraules)}, max={max(paraules)})")


def analysis_5_interjudge_agreement(db):
    """Krippendorff's alpha + correlacio entre jutges."""
    print("\n[5] INTER-JUDGE AGREEMENT (Krippendorff's alpha)")
    print("=" * 80)

    # Construir matriu: files = casos (generation_id), columnes = jutges
    rows = db.execute("""
        SELECT e.generation_id, e.judge, e.puntuacio_global
        FROM multi_v2_evaluations e
        JOIN multi_llm_generations g ON e.generation_id = g.id
        WHERE g.prompt_mode = 'rag_v2' AND e.is_self_eval = 0
    """).fetchall()

    # Agrupar per generation_id
    by_gen = defaultdict(dict)
    for r in rows:
        by_gen[r["generation_id"]][r["judge"]] = r["puntuacio_global"]

    judges = sorted({r["judge"] for r in rows})
    print(f"Jutges: {judges}")
    print(f"Total generacions: {len(by_gen)}")

    # Casos amb almenys 2 jutges
    multi_judged = {gid: scores for gid, scores in by_gen.items() if len(scores) >= 2}
    print(f"Casos amb >= 2 jutges: {len(multi_judged)}")

    # Krippendorff's alpha (interval data)
    alpha = krippendorff_alpha(multi_judged, judges)
    if alpha is not None:
        print(f"\nKrippendorff's alpha (interval): {alpha:.3f}")
        if alpha >= 0.8:
            print("RESULT: Excel.lent (alpha >= 0.8) — jutges molt consistents")
        elif alpha >= 0.667:
            print("RESULT: Acceptable (0.667 <= alpha < 0.8)")
        else:
            print("RESULT: INSUFICIENT (alpha < 0.667) — jutges no consistents entre si")

    # Correlacio parellada (Spearman)
    print()
    print("Correlacions parellades entre jutges (Spearman rho):")
    from scipy import stats
    print(f"{'Parella':<25} {'N':<6} {'rho':<8} {'p':<12}")
    print("-" * 60)
    for i, j1 in enumerate(judges):
        for j2 in judges[i+1:]:
            pairs = [(s[j1], s[j2]) for s in by_gen.values() if j1 in s and j2 in s]
            if len(pairs) < 10:
                continue
            x = [p[0] for p in pairs]
            y = [p[1] for p in pairs]
            rho, pval = stats.spearmanr(x, y)
            print(f"{j1} vs {j2:<18} {len(pairs):<6} {rho:<8.3f} {pval:<12.2e}")


def krippendorff_alpha(data_dict, judges):
    """Krippendorff's alpha per dades d'interval.
    data_dict: {item_id: {judge_name: score}}
    """
    # Construir matriu N (judges × items)
    items = list(data_dict.keys())
    n_items = len(items)
    n_judges = len(judges)
    matrix = np.full((n_judges, n_items), np.nan)
    for j_idx, judge in enumerate(judges):
        for i_idx, item in enumerate(items):
            if judge in data_dict[item]:
                matrix[j_idx, i_idx] = data_dict[item][judge]

    # Valor-per-valor
    # Per interval data: alpha = 1 - Do/De
    # Do = desacord observat, De = desacord esperat
    values = matrix[~np.isnan(matrix)]
    if len(values) < 2:
        return None

    # Comptem parelles per cada item
    Do_sum = 0.0
    Do_count = 0
    for i_idx in range(n_items):
        col = matrix[:, i_idx]
        vals = col[~np.isnan(col)]
        m = len(vals)
        if m < 2:
            continue
        # Sum of squared diffs between all pairs
        diffs = 0.0
        for a in range(m):
            for b in range(a+1, m):
                diffs += (vals[a] - vals[b]) ** 2
        Do_sum += diffs
        Do_count += m * (m - 1) / 2

    if Do_count == 0:
        return None
    Do = Do_sum / Do_count

    # Desacord esperat: tots els valors confrontats entre si
    De_sum = 0.0
    n_total = len(values)
    for a in range(n_total):
        for b in range(a+1, n_total):
            De_sum += (values[a] - values[b]) ** 2
    De_count = n_total * (n_total - 1) / 2
    De = De_sum / De_count

    if De == 0:
        return 1.0
    return 1 - (Do / De)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="docs/estadistica")
    args = parser.parse_args()
    os.makedirs(args.output, exist_ok=True)
    db = get_db()

    print("=" * 80)
    print("ANALISIS PROFUNDES — multi_v2 RAG-v2")
    print("=" * 80)

    r1 = analysis_1_per_perfil(db)
    r2, r3 = analysis_2_per_etapa_genere(db)
    analysis_3_heatmap_etapa_genere(db)
    analysis_4_error_analysis(db)
    analysis_5_interjudge_agreement(db)

    # Summary JSON
    with open(os.path.join(args.output, "deep_analysis.json"), "w", encoding="utf-8") as f:
        json.dump({"per_perfil": r1, "per_etapa": r2, "per_genere": r3}, f, indent=2, ensure_ascii=False)

    print()
    print(f"Summary JSON: {args.output}/deep_analysis.json")
    db.close()


if __name__ == "__main__":
    main()
