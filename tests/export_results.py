"""
export_results.py — Exporta resums de la BD d'avaluacions a CSV/Markdown.

Us:
  python tests/export_results.py                    # tot
  python tests/export_results.py --format csv       # nomes CSV
  python tests/export_results.py --format md        # nomes Markdown
  python tests/export_results.py --output docs/     # escriu a docs/

Genera:
  - individuals_v2.csv/md    Puntuacions individuals rubrica v2
  - trios_v2.csv/md          Resultats trios (ranking branques)
  - cross_v2.csv/md          Resultats cross-model
  - generation_stats.csv/md  Estadistiques de generacio
  - individuals_v1.csv/md    Puntuacions individuals rubrica v1
"""

import sqlite3
import csv
import argparse
import os
from pathlib import Path

DB_PATH = Path(__file__).parent / "results" / "evaluations.db"


def get_db():
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    return db


def query_individuals_v2(db):
    """Puntuacions individuals rubrica v2 per generador/branca/jutge."""
    return db.execute("""
        SELECT g.generator, g.prompt_mode as branca, e.judge, COUNT(*) as n,
            ROUND(AVG(e.a1_coherencia),2) as A1,
            ROUND(AVG(e.a2_correccio),2) as A2,
            ROUND(AVG(e.a3_llegibilitat),2) as A3,
            ROUND(AVG(e.b1_fidelitat),2) as B1,
            ROUND(AVG(e.b2_adequacio_perfil),2) as B2,
            ROUND(AVG(e.b3_scaffolding),2) as B3,
            ROUND(AVG(e.b4_cultura),2) as B4,
            ROUND(AVG(e.c1_potencial),2) as C1,
            ROUND(AVG(e.puntuacio_global),2) as global_avg
        FROM multi_v2_evaluations e
        JOIN multi_llm_generations g ON e.generation_id = g.id
        GROUP BY g.generator, g.prompt_mode, e.judge
        ORDER BY g.generator, g.prompt_mode, e.judge
    """).fetchall()


def query_trios_v2(db):
    """Resultats trios: quantes vegades cada branca queda 1a."""
    return db.execute("""
        SELECT judge, generator,
            SUM(CASE WHEN global_hc = 1 THEN 1 ELSE 0 END) as hc_1st,
            SUM(CASE WHEN global_rag_v1 = 1 THEN 1 ELSE 0 END) as v1_1st,
            SUM(CASE WHEN global_rag_v2 = 1 THEN 1 ELSE 0 END) as v2_1st,
            COUNT(*) as total
        FROM multi_v2_trios
        GROUP BY judge, generator
        ORDER BY judge, generator
    """).fetchall()


def query_cross_v2(db):
    """Resultats cross-model."""
    return db.execute("""
        SELECT judge, pair, global_winner as winner, COUNT(*) as n
        FROM multi_v2_cross
        GROUP BY judge, pair, global_winner
        ORDER BY judge, pair, n DESC
    """).fetchall()


def query_gen_stats(db):
    """Estadistiques de generacio."""
    return db.execute("""
        SELECT generator, prompt_mode, COUNT(*) as n,
            ROUND(AVG(text_adaptat_paraules),0) as avg_words,
            ROUND(AVG(temps_generacio),1) as avg_time_s,
            ROUND(AVG(puntuacio_forma),2) as avg_forma
        FROM multi_llm_generations
        GROUP BY generator, prompt_mode
        ORDER BY generator, prompt_mode
    """).fetchall()


def query_individuals_v1(db):
    """Puntuacions individuals rubrica v1."""
    return db.execute("""
        SELECT g.generator, g.prompt_mode, e.judge, COUNT(*) as n,
            ROUND(AVG(e.c1_coherencia),2) as C1,
            ROUND(AVG(e.c2_adequacio_perfil),2) as C2,
            ROUND(AVG(e.c3_preservacio_curricular),2) as C3,
            ROUND(AVG(e.c4_adequacio_mecr),2) as C4,
            ROUND(AVG(e.c5_prellico_funcional),2) as C5,
            ROUND(AVG(e.puntuacio_fons),2) as fons
        FROM multi_llm_evaluations e
        JOIN multi_llm_generations g ON e.generation_id = g.id
        WHERE e.eval_type = 'individual'
        GROUP BY g.generator, g.prompt_mode, e.judge
        ORDER BY g.generator, g.prompt_mode, e.judge
    """).fetchall()


def rows_to_dicts(rows):
    return [dict(r) for r in rows]


def write_csv(rows, path):
    if not rows:
        return
    dicts = rows_to_dicts(rows)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=dicts[0].keys())
        writer.writeheader()
        writer.writerows(dicts)
    print(f"  CSV: {path}")


def write_md(rows, path, title=""):
    if not rows:
        return
    dicts = rows_to_dicts(rows)
    keys = list(dicts[0].keys())
    with open(path, "w", encoding="utf-8") as f:
        if title:
            f.write(f"# {title}\n\n")
        # Header
        f.write("| " + " | ".join(keys) + " |\n")
        f.write("| " + " | ".join(["---"] * len(keys)) + " |\n")
        for d in dicts:
            f.write("| " + " | ".join(str(d[k]) for k in keys) + " |\n")
    print(f"  MD:  {path}")


QUERIES = {
    "individuals_v2": ("Avaluacions individuals (rubrica v2)", query_individuals_v2),
    "trios_v2": ("Trios intra-model (v2)", query_trios_v2),
    "cross_v2": ("Cross-model (v2)", query_cross_v2),
    "generation_stats": ("Estadistiques de generacio", query_gen_stats),
    "individuals_v1": ("Avaluacions individuals (rubrica v1)", query_individuals_v1),
}


def main():
    parser = argparse.ArgumentParser(description="Exporta resums d'avaluacio")
    parser.add_argument("--format", choices=["csv", "md", "both"], default="both")
    parser.add_argument("--output", default="tests/results", help="Directori de sortida")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    db = get_db()

    for name, (title, query_fn) in QUERIES.items():
        print(f"\n{title}:")
        rows = query_fn(db)
        if args.format in ("csv", "both"):
            write_csv(rows, os.path.join(args.output, f"{name}.csv"))
        if args.format in ("md", "both"):
            write_md(rows, os.path.join(args.output, f"{name}.md"), title)

    db.close()
    print(f"\nExportacio completada a {args.output}/")


if __name__ == "__main__":
    main()
