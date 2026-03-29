"""
ATNE — Batch Test Runner
Executa la matriu de tests sintètics (16 textos × 10 perfils = 160 adaptacions).

Ús:
    python tests/batch_test.py                   # tots (160)
    python tests/batch_test.py --max 5           # només 5 primers
    python tests/batch_test.py --text PRI_EXPL   # un sol text, 10 perfils
    python tests/batch_test.py --perfil P1       # un sol perfil, 16 textos
    python tests/batch_test.py --text PRI_EXPL --perfil P1   # un sol cas

Resultats: tests/results/<timestamp>/
  - adaptacions/  (un .md per cas)
  - metrics.csv   (mètriques forma per cas)
  - summary.txt   (resum global)
"""

import csv
import io
import json
import os
import sys
import time
from pathlib import Path

# Fix consola Windows (cp1252 no suporta emojis)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# Afegir arrel del projecte al path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from dotenv import load_dotenv
load_dotenv()

# Importar funcions del server sense arrencar FastAPI/uvicorn
import corpus_reader
from server import (
    run_adaptation,
    post_process_adaptation,
    build_system_prompt,
)


def load_test_data():
    """Carrega la matriu de tests."""
    data_path = ROOT / "tests" / "test_data.json"
    with open(data_path, encoding="utf-8") as f:
        return json.load(f)


def run_single(text_entry, perfil_entry, output_dir):
    """Executa una sola adaptació i retorna mètriques."""
    text_id = text_entry["id"]
    perfil_id = perfil_entry["id"]
    case_id = f"{text_id}__{perfil_id}"

    # Override del gènere discursiu amb el del text
    params = dict(perfil_entry["params"])
    params["genere_discursiu"] = text_entry["genere"]

    # Override del context.materia per coherència amb el text
    context = dict(perfil_entry["context"])
    context["etapa"] = text_entry["etapa"]

    profile = perfil_entry["profile"]
    text = text_entry["text"]

    t0 = time.time()
    events = []

    try:
        adapted = run_adaptation(
            text=text,
            profile=profile,
            context=context,
            params=params,
            progress_callback=lambda ev: events.append(ev),
        )
    except Exception as e:
        adapted = f"ERROR: {e}"

    elapsed = time.time() - t0

    # Post-process
    mecr = params.get("mecr_sortida", "B2")
    pp = post_process_adaptation(adapted, mecr)

    # Guardar adaptació
    out_file = output_dir / "adaptacions" / f"{case_id}.md"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    header = (
        f"# {case_id}\n"
        f"**Text:** {text_entry['tema']} ({text_entry['etapa']}, {text_entry['genere']})\n"
        f"**Perfil:** {perfil_entry['nom']}\n"
        f"**MECR:** {mecr} | **DUA:** {params.get('dua', '?')}\n"
        f"**Temps:** {elapsed:.1f}s\n"
        f"**Warnings:** {pp['warnings'] or 'cap'}\n\n---\n\n"
    )
    out_file.write_text(header + adapted, encoding="utf-8")

    # Guardar system prompt per inspecció
    prompt_file = output_dir / "prompts" / f"{case_id}_prompt.txt"
    prompt_file.parent.mkdir(parents=True, exist_ok=True)
    try:
        # Reconstruir el system prompt (sense crida a Gemini)
        rag_context = "[RAG context omès en mode test]"
        sp = build_system_prompt(profile, context, params, rag_context)
        prompt_file.write_text(sp, encoding="utf-8")
    except Exception:
        pass

    return {
        "case_id": case_id,
        "text_id": text_id,
        "perfil_id": perfil_id,
        "etapa": text_entry["etapa"],
        "genere": text_entry["genere"],
        "mecr": mecr,
        "dua": params.get("tipus_dua", ""),
        "perfil_nom": perfil_entry["nom"],
        "temps_s": round(elapsed, 1),
        "paraules": pp["metrics"]["paraules"],
        "frases": pp["metrics"]["frases"],
        "termes_negreta": pp["metrics"]["termes_negreta"],
        "encapcalaments": pp["metrics"]["encapcalaments"],
        "frases_llargues": pp["metrics"]["frases_llargues"],
        "warnings": len(pp["warnings"]),
        "warning_text": " | ".join(pp["warnings"]),
        "error": "ERROR" in adapted,
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="ATNE Batch Test Runner")
    parser.add_argument("--max", type=int, default=0, help="Limita a N casos (0=tots)")
    parser.add_argument("--text", type=str, default="", help="Filtra per text_id (p.ex. PRI_EXPL)")
    parser.add_argument("--perfil", type=str, default="", help="Filtra per perfil_id (p.ex. P1)")
    parser.add_argument("--dry-run", action="store_true", help="Mostra casos sense executar")
    args = parser.parse_args()

    data = load_test_data()
    textos = data["textos"]
    perfils = data["perfils"]

    # Filtres
    if args.text:
        textos = [t for t in textos if t["id"] == args.text]
    if args.perfil:
        perfils = [p for p in perfils if p["id"] == args.perfil]

    # Generar matriu de casos
    cases = [(t, p) for t in textos for p in perfils]
    if args.max > 0:
        cases = cases[:args.max]

    print(f"=== ATNE Batch Test ===")
    print(f"Textos: {len(textos)} | Perfils: {len(perfils)} | Casos: {len(cases)}")

    if args.dry_run:
        for i, (t, p) in enumerate(cases, 1):
            print(f"  [{i:3d}] {t['id']} × {p['id']} ({p['nom']})")
        print(f"\n--dry-run: {len(cases)} casos preparats, cap executat.")
        return

    # Directori de resultats
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_dir = ROOT / "tests" / "results" / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Resultats: {output_dir}\n")

    # Executar
    results = []
    errors = 0
    t_total = time.time()

    for i, (t, p) in enumerate(cases, 1):
        label = f"[{i:3d}/{len(cases)}] {t['id']} × {p['id']}"
        print(f"  {label} ...", end=" ", flush=True)

        row = run_single(t, p, output_dir)
        results.append(row)

        status = "ERROR" if row["error"] else f"{row['paraules']}w {row['temps_s']}s"
        if row["warnings"] > 0:
            status += f" ⚠{row['warnings']}"
        if row["error"]:
            errors += 1
        print(status)

    elapsed_total = time.time() - t_total

    # Escriure CSV
    csv_path = output_dir / "metrics.csv"
    if results:
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)

    # Resum
    ok_results = [r for r in results if not r["error"]]
    avg_words = sum(r["paraules"] for r in ok_results) / len(ok_results) if ok_results else 0
    avg_time = sum(r["temps_s"] for r in ok_results) / len(ok_results) if ok_results else 0
    total_warnings = sum(r["warnings"] for r in ok_results)

    summary = (
        f"=== ATNE Batch Test — Resum ===\n"
        f"Branca: prompt-v2-rag\n"
        f"Data: {time.strftime('%Y-%m-%d %H:%M')}\n"
        f"Casos: {len(cases)} ({len(ok_results)} OK, {errors} errors)\n"
        f"Temps total: {elapsed_total:.0f}s (mitjana {avg_time:.1f}s/cas)\n"
        f"Paraules mitjana: {avg_words:.0f}\n"
        f"Warnings totals: {total_warnings}\n"
        f"\nResultats: {csv_path}\n"
    )
    print(f"\n{summary}")

    summary_path = output_dir / "summary.txt"
    summary_path.write_text(summary, encoding="utf-8")


if __name__ == "__main__":
    main()
