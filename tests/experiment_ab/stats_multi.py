#!/usr/bin/env python3
"""
Xat 9 - Analisi estadistica MULTI-MODEL
Compara 4 generadors x 2 condicions x 3 jutges
Genera informe final amb recomanacions per FJE.
"""
import json, sys, io
import numpy as np
from pathlib import Path
from scipy import stats
from collections import defaultdict

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

EXP_DIR = Path(__file__).resolve().parent
EVAL_PATH = EXP_DIR / "resultats_avaluacio_multi.json"
REPORT_PATH = EXP_DIR / "informe_multi_model.md"

CRITERIS = ["adequacio_linguistica", "fidelitat_curricular", "adequacio_perfil",
            "llegibilitat_estructura", "complements"]
PESOS = [0.25, 0.20, 0.25, 0.15, 0.15]

# Cost aproximat per 1M tokens (input+output mitjà en USD)
# Referencia oficial de preus 2025
COSTOS_USD = {
    "gpt4o-mini": 0.38,    # $0.15 in / $0.60 out (mitjana ~0.38 assumint 2:1 in/out)
    "mistral": 0.30,       # mistral-small-latest ~$0.20 in / $0.60 out
    "llama": 0.00,         # llama-3.3-70b via Groq free tier (0 cost per a usuari final)
    "gemma": 0.00,         # gratis via Google free tier
}

# Etiqueta mes descriptiva per al informe
MODEL_LABELS = {
    "gpt4o-mini": "GPT-4o-mini (closed, OpenAI)",
    "mistral": "Mistral Small (open, EU)",
    "llama": "Llama 3.3 70B (open, Meta)",
    "gemma": "Gemma 3 27B (open, Google)",
}

# Jutges que son auto-exclosos (no avaluen les seves propies generacions)
SELF_EXCLUDE = {
    "llama": "llama_judge",
    "mistral": "mistral_judge",
}


def cohens_d(a, b):
    diff = np.array(a) - np.array(b)
    sd = np.std(diff, ddof=1)
    return float(np.mean(diff) / sd) if sd > 0 else 0.0


def interpret_d(d):
    a = abs(d)
    if a < 0.2: return "negligible"
    if a < 0.5: return "petit"
    if a < 0.8: return "mitja"
    return "gran"


def extract_scores_by_model_judge(evals, model, jutge):
    """Retorna scores[A|B][criteri] = list of scores."""
    scores = {"A": defaultdict(list), "B": defaultdict(list)}
    for ev in evals:
        if ev.get("model_generador") != model:
            continue
        for cond in ["A", "B"]:
            jdata = ev["evaluations"].get(cond, {}).get(jutge, {})
            if "error" in jdata or not jdata:
                continue
            for c in CRITERIS:
                if c in jdata and "puntuacio" in jdata[c]:
                    try:
                        scores[cond][c].append(int(jdata[c]["puntuacio"]))
                    except (ValueError, TypeError):
                        pass
    return scores


def avg_score(scores_dict, weighted=True):
    """Mitjana ponderada de tots els criteris."""
    total = []
    n_pairs = max((len(scores_dict[c]) for c in CRITERIS), default=0)
    for i in range(n_pairs):
        s = 0
        valid = True
        for c, w in zip(CRITERIS, PESOS):
            if i < len(scores_dict[c]):
                s += scores_dict[c][i] * (w if weighted else 0.2)
            else:
                valid = False
                break
        if valid:
            total.append(s)
    return total


def main():
    if not EVAL_PATH.exists():
        print(f"No existeix: {EVAL_PATH}")
        sys.exit(1)

    data = json.loads(EVAL_PATH.read_text(encoding="utf-8"))
    evals = data["avaluacions"]
    print(f"Avaluacions carregades: {len(evals)}")

    # Detectar models i jutges
    models = sorted(set(e.get("model_generador", "?") for e in evals))
    jutges_disponibles = set()
    for e in evals:
        for cond in ["A", "B"]:
            for j in e["evaluations"].get(cond, {}).keys():
                jutges_disponibles.add(j)
    jutges = sorted(jutges_disponibles)

    print(f"Models: {models}")
    print(f"Jutges: {jutges}")

    lines = []
    lines.append("# Xat 9 - Informe Final MULTI-MODEL\n")
    lines.append(f"**Avaluacions**: {len(evals)} parells")
    lines.append(f"**Models generadors**: {', '.join(models)}")
    lines.append(f"**Jutges**: {', '.join(jutges)}\n")

    # ═══ TAULA 1: Mitjana global per model x condicio (mitjana de jutges) ═══
    lines.append("\n## Taula 1 - Puntuacio global ponderada per model i condicio\n")
    lines.append("(Mitjana dels jutges, escala 1-5)\n")
    lines.append("| Model | A (minim) | B (complet) | Diff B-A | Cohen's d | Decisio |")
    lines.append("|---|---|---|---|---|---|")

    model_decisions = {}
    for model in models:
        all_a, all_b = [], []
        for jutge in jutges:
            sc = extract_scores_by_model_judge(evals, model, jutge)
            a = avg_score(sc["A"])
            b = avg_score(sc["B"])
            n = min(len(a), len(b))
            if n >= 5:
                all_a.extend(a[:n])
                all_b.extend(b[:n])
        if not all_a or not all_b:
            lines.append(f"| {model} | - | - | - | - | sense dades |")
            continue
        n = min(len(all_a), len(all_b))
        mean_a = np.mean(all_a[:n])
        mean_b = np.mean(all_b[:n])
        diff = mean_b - mean_a
        d = cohens_d(all_b[:n], all_a[:n])

        if abs(diff) > 0.5 and abs(d) >= 0.3:
            dec = "**Prompt complet val la pena**" if diff > 0 else "**Prompt minim millor**"
        elif abs(diff) < 0.3:
            dec = "Negligible (minim suficient)"
        else:
            dec = "Zona grisa"

        model_decisions[model] = {"mean_a": mean_a, "mean_b": mean_b, "diff": diff, "d": d, "dec": dec}
        lines.append(f"| **{model}** | {mean_a:.2f} | {mean_b:.2f} | {diff:+.2f} | {d:+.2f} ({interpret_d(d)}) | {dec} |")

    # ═══ TAULA 2: Per criteri (mitjana jutges) ═══
    lines.append("\n## Taula 2 - Per criteri: mitjana de B (prompt complet) per model\n")
    lines.append("| Model | Adequacio MECR | Fidelitat | Perfil | Llegibilitat | Complements | TOTAL |")
    lines.append("|---|---|---|---|---|---|---|")

    model_critics = {}
    for model in models:
        row = [f"**{model}**"]
        critics = {}
        for c, w in zip(CRITERIS, PESOS):
            vals = []
            for jutge in jutges:
                sc = extract_scores_by_model_judge(evals, model, jutge)
                vals.extend(sc["B"][c])
            critics[c] = float(np.mean(vals)) if vals else 0
            row.append(f"{critics[c]:.2f}")
        total = sum(critics[c] * w for c, w in zip(CRITERIS, PESOS))
        critics["_total"] = total
        model_critics[model] = critics
        row.append(f"**{total:.2f}**")
        lines.append("| " + " | ".join(row) + " |")

    # ═══ TAULA 3: Eficiencia (qualitat / cost) ═══
    lines.append("\n## Taula 3 - Eficiencia (qualitat vs cost)\n")
    lines.append("| Model | Qualitat (B total) | Cost relatiu | Ratio Q/Cost | Notes |")
    lines.append("|---|---|---|---|---|")

    for model in models:
        if model not in model_critics:
            continue
        q = model_critics[model]["_total"]
        cost = COSTOS_USD.get(model, 0)
        if cost == 0:
            ratio = "GRATIS"
            note = "Free tier"
        else:
            ratio = f"{q/cost:.1f}"
            note = f"${cost:.2f}/M tok"
        lines.append(f"| {model} | {q:.2f} | {cost} | {ratio} | {note} |")

    # ═══ TAULA 4: Perfils on cada model destaca ═══
    lines.append("\n## Taula 4 - Comparativa per criteri (millor model en cada criteri, condicio B)\n")
    lines.append("| Criteri | Millor model | Puntuacio | Pitjor | Puntuacio |")
    lines.append("|---|---|---|---|---|")
    for c in CRITERIS:
        scores_per_model = []
        for model in models:
            if model in model_critics:
                scores_per_model.append((model, model_critics[model][c]))
        if scores_per_model:
            best = max(scores_per_model, key=lambda x: x[1])
            worst = min(scores_per_model, key=lambda x: x[1])
            lines.append(f"| {c} | **{best[0]}** | {best[1]:.2f} | {worst[0]} | {worst[1]:.2f} |")

    # ═══ TAULA 5: Concordança inter-jutge global ═══
    lines.append("\n## Taula 5 - Concordança inter-jutge (correlacio Pearson)\n")
    lines.append("| Jutge 1 | Jutge 2 | r | n |")
    lines.append("|---|---|---|---|")
    for i, j1 in enumerate(jutges):
        for j2 in jutges[i+1:]:
            all_s1, all_s2 = [], []
            for model in models:
                sc1 = extract_scores_by_model_judge(evals, model, j1)
                sc2 = extract_scores_by_model_judge(evals, model, j2)
                for cond in ["A", "B"]:
                    for c in CRITERIS:
                        n = min(len(sc1[cond][c]), len(sc2[cond][c]))
                        all_s1.extend(sc1[cond][c][:n])
                        all_s2.extend(sc2[cond][c][:n])
            if len(all_s1) >= 5:
                r = float(np.corrcoef(all_s1, all_s2)[0, 1]) if np.std(all_s1) > 0 and np.std(all_s2) > 0 else 0
                lines.append(f"| {j1} | {j2} | {r:.2f} | {len(all_s1)} |")

    # ═══ DECISIO FINAL ═══
    lines.append("\n## Decisio final per a FJE\n")
    if model_critics:
        # Millor en TOTAL
        best_quality = max(model_critics.items(), key=lambda x: x[1]["_total"])
        # Millor en complements
        best_comp = max(model_critics.items(), key=lambda x: x[1]["complements"])
        # Millor en perfil
        best_perfil = max(model_critics.items(), key=lambda x: x[1]["adequacio_perfil"])
        # Millor relacio qualitat/cost
        cost_eff = []
        for m, c in model_critics.items():
            cost = COSTOS_USD.get(m, 1)
            if cost > 0:
                cost_eff.append((m, c["_total"]/cost))
            else:
                cost_eff.append((m, c["_total"] * 100))  # gratuit = altissim
        best_eff = max(cost_eff, key=lambda x: x[1])

        lines.append(f"- **Millor qualitat global**: {best_quality[0]} ({best_quality[1]['_total']:.2f}/5)")
        lines.append(f"- **Millor en complements**: {best_comp[0]} ({best_comp[1]['complements']:.2f}/5)")
        lines.append(f"- **Millor adequacio al perfil**: {best_perfil[0]} ({best_perfil[1]['adequacio_perfil']:.2f}/5)")
        lines.append(f"- **Millor eficiencia (qualitat/cost)**: {best_eff[0]}")

        lines.append("\n### Quan pagar la pena el prompt complet")
        for model, dec in model_decisions.items():
            lines.append(f"- **{model}**: diff = {dec['diff']:+.2f}, d = {dec['d']:+.2f} → {dec['dec']}")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nInforme: {REPORT_PATH}")
    print("\n" + "\n".join(lines))


if __name__ == "__main__":
    main()
