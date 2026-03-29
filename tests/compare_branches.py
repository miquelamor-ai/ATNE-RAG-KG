"""
ATNE — Comparador de branques (RAG vs Hardcoded)

Llegeix els CSV de mètriques de cada branca i genera un report comparatiu.

Ús:
    python tests/compare_branches.py <rag_csv> <hardcoded_csv>
    python tests/compare_branches.py tests/results/20260328_235135/metrics.csv ../ATNE-hardcoded/tests/results/<ts>/metrics.csv
"""

import csv
import io
import sys
from pathlib import Path
from collections import defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


def load_csv(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            # Normalitzar tipus
            for k in ("paraules", "frases", "termes_negreta", "encapcalaments", "frases_llargues", "warnings"):
                if k in row:
                    row[k] = int(row[k]) if row[k] else 0
            row["temps_s"] = float(row.get("temps_s", 0))
            row["error"] = row.get("error", "False") == "True"
            rows.append(row)
    return rows


def summarize(rows, label):
    ok = [r for r in rows if not r["error"]]
    n = len(ok)
    if n == 0:
        return {}
    return {
        "label": label,
        "total": len(rows),
        "ok": n,
        "errors": len(rows) - n,
        "avg_paraules": sum(r["paraules"] for r in ok) / n,
        "avg_frases": sum(r["frases"] for r in ok) / n,
        "avg_negreta": sum(r["termes_negreta"] for r in ok) / n,
        "avg_temps": sum(r["temps_s"] for r in ok) / n,
        "total_warnings": sum(r["warnings"] for r in ok),
        "avg_warnings": sum(r["warnings"] for r in ok) / n,
    }


def compare_by_group(rag_rows, hc_rows, group_key):
    """Compara mètriques agrupades per una clau (perfil, mecr, genere, etapa)."""
    rag_groups = defaultdict(list)
    hc_groups = defaultdict(list)
    for r in rag_rows:
        rag_groups[r[group_key]].append(r)
    for r in hc_rows:
        hc_groups[r[group_key]].append(r)

    all_keys = sorted(set(list(rag_groups.keys()) + list(hc_groups.keys())))
    lines = []
    for k in all_keys:
        rg = [r for r in rag_groups.get(k, []) if not r["error"]]
        hg = [r for r in hc_groups.get(k, []) if not r["error"]]
        rw = sum(r["paraules"] for r in rg) / len(rg) if rg else 0
        hw = sum(r["paraules"] for r in hg) / len(hg) if hg else 0
        rt = sum(r["temps_s"] for r in rg) / len(rg) if rg else 0
        ht = sum(r["temps_s"] for r in hg) / len(hg) if hg else 0
        rn = sum(r["termes_negreta"] for r in rg) / len(rg) if rg else 0
        hn = sum(r["termes_negreta"] for r in hg) / len(hg) if hg else 0
        rwarn = sum(r["warnings"] for r in rg) / len(rg) if rg else 0
        hwarn = sum(r["warnings"] for r in hg) / len(hg) if hg else 0
        lines.append({
            "key": k,
            "rag_words": rw, "hc_words": hw,
            "rag_time": rt, "hc_time": ht,
            "rag_bold": rn, "hc_bold": hn,
            "rag_warn": rwarn, "hc_warn": hwarn,
        })
    return lines


def print_table(title, lines, key_label=""):
    print(f"\n### {title}")
    print(f"| {key_label or 'Grup':<20} | RAG words | HC words | RAG time | HC time | RAG bold | HC bold | RAG warn | HC warn |")
    print(f"|{'-'*22}|{'-'*11}|{'-'*10}|{'-'*10}|{'-'*9}|{'-'*10}|{'-'*9}|{'-'*10}|{'-'*9}|")
    for l in lines:
        print(f"| {l['key']:<20} | {l['rag_words']:>9.0f} | {l['hc_words']:>8.0f} | {l['rag_time']:>8.1f}s | {l['hc_time']:>7.1f}s | {l['rag_bold']:>8.1f} | {l['hc_bold']:>7.1f} | {l['rag_warn']:>8.1f} | {l['hc_warn']:>7.1f} |")


def main():
    if len(sys.argv) < 3:
        # Auto-detect últims resultats
        rag_dir = Path("tests/results")
        hc_dir = Path("../ATNE-hardcoded/tests/results")
        if rag_dir.exists() and hc_dir.exists():
            rag_csvs = sorted(rag_dir.glob("*/metrics.csv"))
            hc_csvs = sorted(hc_dir.glob("*/metrics.csv"))
            if rag_csvs and hc_csvs:
                rag_path = rag_csvs[-1]
                hc_path = hc_csvs[-1]
                print(f"Auto-detect:\n  RAG: {rag_path}\n  HC:  {hc_path}\n")
            else:
                print("No s'han trobat resultats. Ús: python tests/compare_branches.py <rag.csv> <hc.csv>")
                return
        else:
            print("Ús: python tests/compare_branches.py <rag.csv> <hc.csv>")
            return
    else:
        rag_path = Path(sys.argv[1])
        hc_path = Path(sys.argv[2])

    rag_rows = load_csv(rag_path)
    hc_rows = load_csv(hc_path)

    rag_sum = summarize(rag_rows, "RAG")
    hc_sum = summarize(hc_rows, "Hardcoded")

    print("=" * 70)
    print("  ATNE — Comparativa branques prompt-v2")
    print("=" * 70)

    print(f"\n### Resum global")
    print(f"| Mètrica              | RAG          | Hardcoded    | Diff         |")
    print(f"|{'-'*22}|{'-'*14}|{'-'*14}|{'-'*14}|")
    for key, label, fmt in [
        ("ok", "Casos OK", "d"),
        ("errors", "Errors", "d"),
        ("avg_paraules", "Paraules/cas", ".0f"),
        ("avg_frases", "Frases/cas", ".0f"),
        ("avg_negreta", "Negretes/cas", ".1f"),
        ("avg_temps", "Temps/cas (s)", ".1f"),
        ("total_warnings", "Warnings totals", "d"),
        ("avg_warnings", "Warnings/cas", ".1f"),
    ]:
        rv = rag_sum.get(key, 0)
        hv = hc_sum.get(key, 0)
        diff = rv - hv
        sign = "+" if diff > 0 else ""
        print(f"| {label:<20} | {rv:>{12}{fmt}} | {hv:>{12}{fmt}} | {sign}{diff:>{11}{fmt}} |")

    # Per perfil
    print_table("Per perfil", compare_by_group(rag_rows, hc_rows, "perfil_id"), "Perfil")

    # Per MECR
    print_table("Per MECR", compare_by_group(rag_rows, hc_rows, "mecr"), "MECR")

    # Per gènere
    print_table("Per gènere", compare_by_group(rag_rows, hc_rows, "genere"), "Gènere")

    # Per etapa
    print_table("Per etapa", compare_by_group(rag_rows, hc_rows, "etapa"), "Etapa")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
