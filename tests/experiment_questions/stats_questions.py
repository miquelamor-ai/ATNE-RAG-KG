#!/usr/bin/env python3
"""
Stats Questions - ranking 4 models x 5 jutges, per criteri.
"""
import json, sys, io
import numpy as np
from pathlib import Path
from collections import defaultdict

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

EXP_DIR = Path(__file__).resolve().parent
EVAL_PATH = EXP_DIR / "resultats_avaluacio_questions.json"
REPORT_PATH = EXP_DIR / "informe_questions.md"

CRITERIS = ["validesa_pedagogica", "adequacio_nivell", "discriminacio",
            "originalitat_redaccio", "format_estructural"]
PESOS = [0.30, 0.25, 0.15, 0.15, 0.15]

MODEL_LABELS = {
    "gpt4o-mini": "GPT-4o-mini (closed)",
    "mistral": "Mistral Small (open EU)",
    "llama": "Llama 3.3 70B (open Meta)",
    "gemma": "Gemma 4 31B (open Google)",
}


def extract_score(jdata, c):
    if not jdata or "error" in jdata:
        return None
    if c in jdata and isinstance(jdata[c], dict) and "puntuacio" in jdata[c]:
        try:
            return int(jdata[c]["puntuacio"])
        except (ValueError, TypeError):
            return None
    return None


def main():
    if not EVAL_PATH.exists():
        print(f"No existeix: {EVAL_PATH}")
        sys.exit(1)

    data = json.loads(EVAL_PATH.read_text(encoding="utf-8"))
    evals = data["avaluacions"]
    print(f"Avaluacions: {len(evals)}")

    models = sorted(set(e["model_generador"] for e in evals))
    jutges = set()
    for e in evals:
        for j in e["evaluations"].keys():
            jutges.add(j)
    jutges = sorted(jutges)

    by_model_crit = defaultdict(lambda: defaultdict(list))
    by_tipus_model = defaultdict(lambda: defaultdict(list))
    by_perfil_model = defaultdict(lambda: defaultdict(list))
    json_valid_by_model = defaultdict(lambda: {"ok": 0, "total": 0})

    for e in evals:
        m = e["model_generador"]
        tipus = e.get("tipus_question", "?")
        perfil = e.get("perfil_id", "?")
        json_valid_by_model[m]["total"] += 1
        if e.get("json_valid"):
            json_valid_by_model[m]["ok"] += 1

        case_total = []
        for c, w in zip(CRITERIS, PESOS):
            crit_scores = []
            for j, jdata in e["evaluations"].items():
                s = extract_score(jdata, c)
                if s is not None:
                    crit_scores.append(s)
            if crit_scores:
                avg_c = np.mean(crit_scores)
                by_model_crit[m][c].append(avg_c)
                case_total.append(avg_c * w)
        if case_total:
            by_model_crit[m]["_total"].append(sum(case_total))
            by_tipus_model[tipus][m].append(sum(case_total))
            by_perfil_model[perfil][m].append(sum(case_total))

    lines = []
    lines.append("# Experiment Questions - Informe Final\n")
    lines.append(f"**Avaluacions**: {len(evals)}")
    lines.append(f"**Models generadors**: {', '.join(models)}")
    lines.append(f"**Jutges**: {', '.join(jutges)}\n")

    # Taula 0 - JSON validity
    lines.append("\n## Taula 0 - Validesa JSON per model\n")
    lines.append("| Model | JSON valids | Total | % |")
    lines.append("|---|---|---|---|")
    for m in models:
        v = json_valid_by_model[m]
        pct = (v["ok"] / v["total"] * 100) if v["total"] > 0 else 0
        lines.append(f"| {m} | {v['ok']} | {v['total']} | {pct:.1f}% |")

    # Taula 1 - Ranking
    lines.append("\n## Taula 1 - Ranking global per model\n")
    lines.append("| Rank | Model | Score Total | n casos |")
    lines.append("|---|---|---|---|")
    ranking = []
    for m in models:
        totals = by_model_crit[m]["_total"]
        if totals:
            ranking.append((m, np.mean(totals), len(totals)))
    ranking.sort(key=lambda x: -x[1])
    for i, (m, s, n) in enumerate(ranking, 1):
        lines.append(f"| {i} | **{MODEL_LABELS.get(m, m)}** | {s:.2f} | {n} |")

    # Taula 2 - Per criteri
    lines.append("\n## Taula 2 - Per criteri\n")
    header = "| Model | " + " | ".join(CRITERIS) + " | TOTAL |"
    sep = "|" + "---|" * (len(CRITERIS) + 2)
    lines.append(header)
    lines.append(sep)
    for m in models:
        row = [f"**{m}**"]
        for c in CRITERIS:
            vals = by_model_crit[m][c]
            row.append(f"{np.mean(vals):.2f}" if vals else "-")
        totals = by_model_crit[m]["_total"]
        row.append(f"**{np.mean(totals):.2f}**" if totals else "-")
        lines.append("| " + " | ".join(row) + " |")

    # Taula 3 - Per tipus de pregunta
    lines.append("\n## Taula 3 - Per tipus de pregunta\n")
    lines.append("| Tipus | Millor model | Score | Pitjor | Score |")
    lines.append("|---|---|---|---|---|")
    for tipus in sorted(by_tipus_model.keys()):
        scores = []
        for m in models:
            vals = by_tipus_model[tipus][m]
            if vals:
                scores.append((m, np.mean(vals)))
        if scores:
            best = max(scores, key=lambda x: x[1])
            worst = min(scores, key=lambda x: x[1])
            lines.append(f"| {tipus} | **{best[0]}** | {best[1]:.2f} | {worst[0]} | {worst[1]:.2f} |")

    # Taula 4 - Per perfil
    lines.append("\n## Taula 4 - Per perfil\n")
    lines.append("| Perfil | Millor model | Score |")
    lines.append("|---|---|---|")
    for perfil in sorted(by_perfil_model.keys()):
        scores = []
        for m in models:
            vals = by_perfil_model[perfil][m]
            if vals:
                scores.append((m, np.mean(vals)))
        if scores:
            best = max(scores, key=lambda x: x[1])
            lines.append(f"| {perfil} | **{best[0]}** | {best[1]:.2f} |")

    # Taula 5 - Inter-jutge
    lines.append("\n## Taula 5 - Concordança inter-jutge\n")
    lines.append("| Jutge 1 | Jutge 2 | r | n |")
    lines.append("|---|---|---|---|")
    judge_scores = defaultdict(list)
    for e in evals:
        for c in CRITERIS:
            for j in jutges:
                s = extract_score(e["evaluations"].get(j, {}), c)
                judge_scores[j].append((e["case_id"], c, s))

    for i, j1 in enumerate(jutges):
        for j2 in jutges[i+1:]:
            map1 = {(cid, c): s for cid, c, s in judge_scores[j1] if s is not None}
            map2 = {(cid, c): s for cid, c, s in judge_scores[j2] if s is not None}
            common = set(map1.keys()) & set(map2.keys())
            if len(common) >= 5:
                a = [map1[k] for k in common]
                b = [map2[k] for k in common]
                if np.std(a) > 0 and np.std(b) > 0:
                    r = float(np.corrcoef(a, b)[0, 1])
                    lines.append(f"| {j1} | {j2} | {r:.2f} | {len(common)} |")

    # Decisio final
    lines.append("\n## Decisio final\n")
    if ranking:
        winner = ranking[0]
        lines.append(f"- **Millor model per generar preguntes**: {MODEL_LABELS.get(winner[0], winner[0])} ({winner[1]:.2f}/5)")
        for c in CRITERIS:
            scores = [(m, np.mean(by_model_crit[m][c])) for m in models if by_model_crit[m][c]]
            if scores:
                best = max(scores, key=lambda x: x[1])
                lines.append(f"- **Millor en {c}**: {best[0]} ({best[1]:.2f})")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nInforme: {REPORT_PATH}")
    print("\n".join(lines[:30]))


if __name__ == "__main__":
    main()
