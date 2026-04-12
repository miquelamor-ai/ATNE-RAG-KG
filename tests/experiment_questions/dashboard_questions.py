#!/usr/bin/env python3
"""
Dashboard Questions — Experiment de generacio de preguntes de comprensio lectora.

Genera un HTML autocontingut (Chart.js CDN) amb:
  1. Hero banner amb ranking
  2. Bar chart ranking global (score ponderat)
  3. Radar chart per criteri (5 eixos, 4 models)
  4. Heatmap Model x Tipus pregunta (9 tipus)
  5. Heatmap Model x Perfil (6 perfils)
  6. JSON validity per model
  7. Correlacio inter-jutge

Llegeix: resultats_avaluacio_questions.json
Escriu:  dashboard_questions.html
"""
import json, sys, io
import numpy as np
from pathlib import Path
from collections import defaultdict
from datetime import datetime

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

EXP_DIR = Path(__file__).resolve().parent
EVAL_PATH = EXP_DIR / "resultats_avaluacio_questions.json"
DASHBOARD_PATH = EXP_DIR / "dashboard_questions.html"

# ── Configuracio ──────────────────────────────────────────────
CRITERIS = ["validesa_pedagogica", "adequacio_nivell", "discriminacio",
            "originalitat_redaccio", "format_estructural"]
CRITERIS_LABELS = {
    "validesa_pedagogica": "Validesa pedagogica",
    "adequacio_nivell": "Adequacio nivell",
    "discriminacio": "Discriminacio",
    "originalitat_redaccio": "Originalitat redaccio",
    "format_estructural": "Format estructural",
}
PESOS = [0.30, 0.25, 0.15, 0.15, 0.15]

MODEL_LABELS = {
    "gpt4o-mini": "GPT-4o-mini",
    "mistral": "Mistral Small",
    "llama": "Llama 3.3 70B",
    "gemma": "Gemma 4 31B",
}
MODEL_COLORS = {
    "gpt4o-mini": "#10a37f",
    "mistral": "#fa520f",
    "llama": "#0467df",
    "gemma": "#4285f4",
}
MODEL_ORDER = ["gemma", "mistral", "gpt4o-mini", "llama"]

TIPUS_LABELS = {
    "literals": "Literals",
    "comprensio": "Comprensio",
    "vocabulari_contextual": "Vocabulari ctx.",
    "inferencials": "Inferencials",
    "aplicacio": "Aplicacio",
    "analisi": "Analisi",
    "avaluatives": "Avaluatives",
    "creatives": "Creatives",
    "metacognitives": "Metacognitives",
}
TIPUS_ORDER = ["literals", "comprensio", "vocabulari_contextual", "inferencials",
               "aplicacio", "analisi", "avaluatives", "creatives", "metacognitives"]

PERFIL_LABELS = {
    "nouvingut_arabic": "Nouvingut (arab)",
    "tdah_lleu": "TDAH lleu",
    "altes_capacitats": "Altes capacitats",
    "tdl_pragmatica": "TDL pragmatica",
    "doble_excepcionalitat": "2e (AC+dislexia)",
    "tdah_di_lleu": "TDAH+DI lleu",
}
PERFIL_ORDER = ["nouvingut_arabic", "tdah_lleu", "altes_capacitats",
                "tdl_pragmatica", "doble_excepcionalitat", "tdah_di_lleu"]


# ── Funcions auxiliars ────────────────────────────────────────

def extract_score(jdata, criteri):
    """Treu la puntuacio d'un jutge per un criteri, o None si hi ha error."""
    if not jdata or "error" in jdata:
        return None
    if criteri in jdata and isinstance(jdata[criteri], dict) and "puntuacio" in jdata[criteri]:
        try:
            return int(jdata[criteri]["puntuacio"])
        except (ValueError, TypeError):
            return None
    return None


def load_data():
    if not EVAL_PATH.exists():
        print(f"[ERROR] No existeix {EVAL_PATH}")
        sys.exit(1)
    return json.loads(EVAL_PATH.read_text(encoding="utf-8"))


def compute_metrics(evals):
    """Calcula totes les metriques necessaries per al dashboard."""
    models = sorted(set(e["model_generador"] for e in evals))
    jutges = set()
    for e in evals:
        for j in e["evaluations"].keys():
            jutges.add(j)
    jutges = sorted(jutges)

    # ── Per model + per criteri ──
    by_model_crit = defaultdict(lambda: defaultdict(list))
    by_tipus_model = defaultdict(lambda: defaultdict(list))
    by_perfil_model = defaultdict(lambda: defaultdict(list))
    json_valid = defaultdict(lambda: {"ok": 0, "total": 0})

    for e in evals:
        m = e["model_generador"]
        tipus = e.get("tipus_question", "?")
        perfil = e.get("perfil_id", "?")
        json_valid[m]["total"] += 1
        if e.get("json_valid"):
            json_valid[m]["ok"] += 1

        case_scores = []
        for c, w in zip(CRITERIS, PESOS):
            crit_vals = []
            for j, jdata in e["evaluations"].items():
                s = extract_score(jdata, c)
                if s is not None:
                    crit_vals.append(s)
            if crit_vals:
                avg = np.mean(crit_vals)
                by_model_crit[m][c].append(avg)
                case_scores.append(avg * w)
        if case_scores:
            total = sum(case_scores)
            by_model_crit[m]["_total"].append(total)
            by_tipus_model[tipus][m].append(total)
            by_perfil_model[perfil][m].append(total)

    # ── Ranking global ──
    ranking = []
    for m in models:
        totals = by_model_crit[m]["_total"]
        if totals:
            ranking.append({
                "model": m,
                "score": float(np.mean(totals)),
                "n": len(totals),
            })
    ranking.sort(key=lambda x: -x["score"])

    # ── Per criteri per model ──
    criteris_per_model = {}
    for m in models:
        criteris_per_model[m] = {}
        for c in CRITERIS:
            vals = by_model_crit[m][c]
            criteris_per_model[m][c] = float(np.mean(vals)) if vals else 0.0

    # ── Heatmap: model x tipus ──
    tipus_found = sorted(set(e.get("tipus_question", "?") for e in evals))
    heatmap_tipus = {}
    for m in models:
        heatmap_tipus[m] = {}
        for t in tipus_found:
            vals = by_tipus_model[t].get(m, [])
            heatmap_tipus[m][t] = float(np.mean(vals)) if vals else None

    # ── Heatmap: model x perfil ──
    perfils_found = sorted(set(e.get("perfil_id", "?") for e in evals))
    heatmap_perfil = {}
    for m in models:
        heatmap_perfil[m] = {}
        for p in perfils_found:
            vals = by_perfil_model[p].get(m, [])
            heatmap_perfil[m][p] = float(np.mean(vals)) if vals else None

    # ── Correlacio inter-jutge ──
    judge_scores = defaultdict(list)
    for e in evals:
        for c in CRITERIS:
            for j in jutges:
                s = extract_score(e["evaluations"].get(j, {}), c)
                judge_scores[j].append((e["case_id"], c, s))

    judge_corr = {}
    for j1 in jutges:
        judge_corr[j1] = {}
        for j2 in jutges:
            if j1 == j2:
                judge_corr[j1][j2] = 1.0
                continue
            map1 = {(cid, c): s for cid, c, s in judge_scores[j1] if s is not None}
            map2 = {(cid, c): s for cid, c, s in judge_scores[j2] if s is not None}
            common = set(map1.keys()) & set(map2.keys())
            if len(common) >= 5:
                a = [map1[k] for k in common]
                b = [map2[k] for k in common]
                if np.std(a) > 0 and np.std(b) > 0:
                    judge_corr[j1][j2] = float(np.corrcoef(a, b)[0, 1])
                else:
                    judge_corr[j1][j2] = 0.0
            else:
                judge_corr[j1][j2] = 0.0

    return {
        "models": models,
        "jutges": jutges,
        "ranking": ranking,
        "criteris_per_model": criteris_per_model,
        "heatmap_tipus": heatmap_tipus,
        "heatmap_perfil": heatmap_perfil,
        "tipus_found": tipus_found,
        "perfils_found": perfils_found,
        "json_valid": dict(json_valid),
        "judge_corr": judge_corr,
        "total": len(evals),
    }


def print_ranking(metrics):
    """Imprimeix el ranking per stdout."""
    print("\n" + "=" * 60)
    print("  RANKING GLOBAL — Generacio de preguntes de comprensio")
    print("=" * 60)
    for i, r in enumerate(metrics["ranking"], 1):
        label = MODEL_LABELS.get(r["model"], r["model"])
        medal = {1: "  [1r]", 2: "  [2n]", 3: "  [3r]", 4: "  [4t]"}.get(i, "")
        print(f"  {medal}  {label:20s}  {r['score']:.2f}/5   (n={r['n']})")
    print("=" * 60)
    if metrics["ranking"]:
        winner = metrics["ranking"][0]
        print(f"\n  Millor model: {MODEL_LABELS.get(winner['model'], winner['model'])}")
    print()


def generate_html(metrics, raw_data):
    """Genera tot el HTML del dashboard."""
    models = metrics["models"]
    ranking = metrics["ranking"]
    cp = metrics["criteris_per_model"]
    ht = metrics["heatmap_tipus"]
    hp = metrics["heatmap_perfil"]
    jv = metrics["json_valid"]
    jc = metrics["judge_corr"]
    jutges = metrics["jutges"]
    total = metrics["total"]

    # Ordenar models per ranking
    ranked_models = [r["model"] for r in ranking]
    winner = ranking[0] if ranking else {"model": "?", "score": 0}
    winner_label = MODEL_LABELS.get(winner["model"], winner["model"])

    data_timestamp = raw_data.get("data", "-")[:19] if raw_data else "-"

    # ── Dades JSON per Chart.js ──
    # Ranking bar chart
    bar_labels = json.dumps([MODEL_LABELS.get(r["model"], r["model"]) for r in ranking])
    bar_scores = json.dumps([round(r["score"], 2) for r in ranking])
    bar_colors = json.dumps([MODEL_COLORS.get(r["model"], "#888") for r in ranking])

    # Radar chart
    radar_labels = json.dumps([CRITERIS_LABELS[c] for c in CRITERIS])
    radar_datasets = []
    for m in ranked_models:
        radar_datasets.append({
            "label": MODEL_LABELS.get(m, m),
            "data": [round(cp[m][c], 2) for c in CRITERIS],
            "backgroundColor": MODEL_COLORS.get(m, "#888") + "33",
            "borderColor": MODEL_COLORS.get(m, "#888"),
            "borderWidth": 2,
            "pointBackgroundColor": MODEL_COLORS.get(m, "#888"),
        })
    radar_datasets_json = json.dumps(radar_datasets)

    # ── Ranking table HTML ──
    ranking_rows = ""
    for i, r in enumerate(ranking, 1):
        m = r["model"]
        label = MODEL_LABELS.get(m, m)
        color = MODEL_COLORS.get(m, "#888")
        medal = {1: "1r", 2: "2n", 3: "3r", 4: "4t"}.get(i, str(i))
        is_winner = i == 1
        bg = "rgba(66,133,244,0.15)" if is_winner else "transparent"
        ranking_rows += f"""<tr style="background:{bg}">
          <td style="font-weight:700;font-size:1.1em;">{medal}</td>
          <td><span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:{color};margin-right:8px;vertical-align:middle;"></span>{label}</td>
          <td style="font-weight:700;font-size:1.1em;color:{color}">{r['score']:.2f}</td>
          <td>{r['n']}</td>
        </tr>\n"""

    # ── Heatmap Model x Tipus HTML ──
    tipus_ordered = [t for t in TIPUS_ORDER if t in metrics["tipus_found"]]
    # Also add any types found but not in our order
    for t in metrics["tipus_found"]:
        if t not in tipus_ordered:
            tipus_ordered.append(t)

    heatmap_tipus_html = '<table style="width:100%;border-collapse:collapse;">\n<thead><tr><th style="text-align:left;padding:12px;">Model</th>'
    for t in tipus_ordered:
        heatmap_tipus_html += f'<th style="text-align:center;padding:12px;font-size:0.8em;">{TIPUS_LABELS.get(t, t)}</th>'
    heatmap_tipus_html += '</tr></thead>\n<tbody>'
    for m in ranked_models:
        label = MODEL_LABELS.get(m, m)
        color = MODEL_COLORS.get(m, "#888")
        heatmap_tipus_html += f'<tr><td style="padding:10px;font-weight:600;"><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:{color};margin-right:6px;"></span>{label}</td>'
        for t in tipus_ordered:
            val = ht[m].get(t)
            if val is not None:
                # Color: gradient from red to green
                if val < 3.5:
                    bg = "#ef444480"
                elif val < 4.0:
                    bg = "#f59e0b80"
                elif val < 4.5:
                    bg = "#10b98180"
                else:
                    bg = "#05966980"
                heatmap_tipus_html += f'<td style="text-align:center;padding:10px;background:{bg};font-weight:600;border-radius:4px;">{val:.2f}</td>'
            else:
                heatmap_tipus_html += '<td style="text-align:center;padding:10px;color:#555;">—</td>'
        heatmap_tipus_html += '</tr>\n'
    heatmap_tipus_html += '</tbody></table>'

    # ── Heatmap Model x Perfil HTML ──
    perfils_ordered = [p for p in PERFIL_ORDER if p in metrics["perfils_found"]]
    for p in metrics["perfils_found"]:
        if p not in perfils_ordered:
            perfils_ordered.append(p)

    heatmap_perfil_html = '<table style="width:100%;border-collapse:collapse;">\n<thead><tr><th style="text-align:left;padding:12px;">Model</th>'
    for p in perfils_ordered:
        heatmap_perfil_html += f'<th style="text-align:center;padding:12px;font-size:0.8em;">{PERFIL_LABELS.get(p, p)}</th>'
    heatmap_perfil_html += '</tr></thead>\n<tbody>'
    for m in ranked_models:
        label = MODEL_LABELS.get(m, m)
        color = MODEL_COLORS.get(m, "#888")
        heatmap_perfil_html += f'<tr><td style="padding:10px;font-weight:600;"><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:{color};margin-right:6px;"></span>{label}</td>'
        for p in perfils_ordered:
            val = hp[m].get(p)
            if val is not None:
                if val < 3.5:
                    bg = "#ef444480"
                elif val < 4.0:
                    bg = "#f59e0b80"
                elif val < 4.5:
                    bg = "#10b98180"
                else:
                    bg = "#05966980"
                heatmap_perfil_html += f'<td style="text-align:center;padding:10px;background:{bg};font-weight:600;border-radius:4px;">{val:.2f}</td>'
            else:
                heatmap_perfil_html += '<td style="text-align:center;padding:10px;color:#555;">—</td>'
        heatmap_perfil_html += '</tr>\n'
    heatmap_perfil_html += '</tbody></table>'

    # ── JSON validity table ──
    json_valid_html = '<table style="width:100%;border-collapse:collapse;">\n<thead><tr><th>Model</th><th>JSON valids</th><th>Total</th><th>%</th></tr></thead>\n<tbody>'
    for m in ranked_models:
        v = jv.get(m, {"ok": 0, "total": 0})
        pct = (v["ok"] / v["total"] * 100) if v["total"] > 0 else 0
        color = MODEL_COLORS.get(m, "#888")
        pct_color = "#4ade80" if pct >= 99 else ("#fbbf24" if pct >= 90 else "#ef4444")
        json_valid_html += f'<tr><td style="font-weight:600;"><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:{color};margin-right:6px;"></span>{MODEL_LABELS.get(m, m)}</td>'
        json_valid_html += f'<td>{v["ok"]}</td><td>{v["total"]}</td>'
        json_valid_html += f'<td style="font-weight:700;color:{pct_color}">{pct:.1f}%</td></tr>\n'
    json_valid_html += '</tbody></table>'

    # ── Inter-judge correlation table ──
    judge_labels = {
        "gpt4o": "GPT-4o",
        "gemini_flash": "Gemini Flash",
        "qwen_judge": "Qwen",
        "llama_judge": "Llama",
        "mistral_judge": "Mistral",
    }
    judge_html = '<table style="width:100%;border-collapse:collapse;">\n<thead><tr><th></th>'
    for j in jutges:
        judge_html += f'<th style="text-align:center;font-size:0.85em;">{judge_labels.get(j, j)}</th>'
    judge_html += '</tr></thead>\n<tbody>'
    for j1 in jutges:
        judge_html += f'<tr><td style="font-weight:600;font-size:0.85em;">{judge_labels.get(j1, j1)}</td>'
        for j2 in jutges:
            val = jc.get(j1, {}).get(j2, 0)
            if j1 == j2:
                bg = "#4285f440"
                txt = "1.00"
            elif val >= 0.7:
                bg = "#4ade8060"
                txt = f"{val:.2f}"
            elif val >= 0.4:
                bg = "#fbbf2460"
                txt = f"{val:.2f}"
            elif val > 0:
                bg = "#ef444460"
                txt = f"{val:.2f}"
            else:
                bg = "transparent"
                txt = "—"
            judge_html += f'<td style="text-align:center;padding:10px;background:{bg};font-weight:600;">{txt}</td>'
        judge_html += '</tr>\n'
    judge_html += '</tbody></table>'

    # ── Per criteri: best model per each ──
    best_per_criteri = {}
    for c in CRITERIS:
        best_m = max(ranked_models, key=lambda m: cp[m].get(c, 0))
        best_per_criteri[c] = (best_m, cp[best_m][c])

    # ── KPI cards ──
    kpi_html = ""
    for c in CRITERIS:
        bm, bv = best_per_criteri[c]
        color = MODEL_COLORS.get(bm, "#888")
        kpi_html += f"""<div class="kpi">
          <div class="kpi-label">{CRITERIS_LABELS[c]}</div>
          <div class="kpi-value" style="color:{color}">{MODEL_LABELS.get(bm, bm)}</div>
          <div class="kpi-sub">{bv:.2f} / 5</div>
        </div>\n"""

    # ══════════════════════════════════════════════════════════════
    # HTML
    # ══════════════════════════════════════════════════════════════
    html = f"""<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dashboard Questions — Experiment ATNE</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
    background: #1a1a2e;
    color: #e0e0e0;
    line-height: 1.6;
  }}
  .container {{ max-width: 1200px; margin: 0 auto; padding: 24px; }}

  /* Hero */
  .hero {{
    background: linear-gradient(135deg, #16213e 0%, #0f3460 50%, #1a1a2e 100%);
    padding: 48px 32px;
    border-radius: 16px;
    margin-bottom: 32px;
    border: 1px solid #233554;
    text-align: center;
  }}
  .hero h1 {{
    font-size: 2.2em;
    color: #4285f4;
    margin-bottom: 8px;
  }}
  .hero .subtitle {{
    color: #94a3b8;
    font-size: 1em;
    margin-bottom: 24px;
  }}
  .hero .winner-score {{
    font-size: 3em;
    font-weight: 800;
    color: #4285f4;
    margin: 12px 0;
  }}
  .hero .meta {{
    color: #64748b;
    font-size: 0.85em;
    margin-top: 8px;
  }}

  /* Ranking table in hero */
  .ranking-table {{
    margin: 24px auto 0;
    max-width: 600px;
  }}
  .ranking-table table {{
    width: 100%;
    border-collapse: collapse;
  }}
  .ranking-table th {{
    padding: 10px 16px;
    text-align: left;
    color: #94a3b8;
    font-size: 0.8em;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    border-bottom: 1px solid #233554;
  }}
  .ranking-table td {{
    padding: 12px 16px;
    border-bottom: 1px solid #1e293b;
    font-size: 0.95em;
  }}

  /* Cards */
  .card {{
    background: #16213e;
    border: 1px solid #233554;
    border-radius: 12px;
    padding: 28px;
    margin-bottom: 24px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  }}
  .card h2 {{
    font-size: 1.3em;
    color: #e2e8f0;
    margin-bottom: 6px;
  }}
  .card .desc {{
    color: #64748b;
    font-size: 0.85em;
    font-style: italic;
    margin-bottom: 20px;
  }}

  /* Chart */
  .chart-container {{
    position: relative;
    height: 400px;
    margin: 16px 0;
  }}

  /* KPI grid */
  .kpi-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
    margin: 24px 0;
  }}
  .kpi {{
    background: #16213e;
    border: 1px solid #233554;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
  }}
  .kpi-label {{
    font-size: 0.7em;
    text-transform: uppercase;
    color: #64748b;
    letter-spacing: 0.05em;
  }}
  .kpi-value {{
    font-size: 1.3em;
    font-weight: 700;
    margin: 6px 0;
  }}
  .kpi-sub {{
    font-size: 0.85em;
    color: #94a3b8;
  }}

  /* Tables inside cards */
  .card table {{
    width: 100%;
    border-collapse: collapse;
  }}
  .card th {{
    padding: 10px 12px;
    text-align: left;
    color: #94a3b8;
    font-size: 0.8em;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    border-bottom: 1px solid #233554;
    background: #0f1a2e;
  }}
  .card td {{
    padding: 10px 12px;
    border-bottom: 1px solid #1e293b;
    font-size: 0.9em;
  }}
  .card tbody tr:hover {{
    background: #1e293b;
  }}

  /* Grid layouts */
  .grid-2 {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
  }}
  @media (max-width: 900px) {{
    .grid-2 {{ grid-template-columns: 1fr; }}
    .hero h1 {{ font-size: 1.5em; }}
  }}

  /* Legend */
  .legend {{
    color: #64748b;
    font-size: 0.8em;
    margin-top: 12px;
    padding: 8px 12px;
    background: #0f1a2e;
    border-radius: 6px;
    display: inline-block;
  }}

  /* Footer */
  .footer {{
    text-align: center;
    color: #475569;
    padding: 32px;
    font-size: 0.8em;
  }}
  .footer a {{ color: #4285f4; text-decoration: none; }}

  /* Responsive tables */
  .table-wrap {{ overflow-x: auto; }}
</style>
</head>
<body>
<div class="container">

  <!-- ═══ 1. Hero Banner ═══ -->
  <div class="hero">
    <h1>{winner_label}: millor model per generar preguntes</h1>
    <div class="subtitle">Experiment de generacio de preguntes de comprensio lectora — 4 models x 5 jutges</div>
    <div class="winner-score">{winner['score']:.2f}<span style="font-size:0.4em;color:#94a3b8"> / 5</span></div>
    <div class="meta">{total} avaluacions totals &middot; {data_timestamp}</div>

    <div class="ranking-table">
      <table>
        <thead><tr><th>Pos.</th><th>Model</th><th>Score ponderat</th><th>n casos</th></tr></thead>
        <tbody>
          {ranking_rows}
        </tbody>
      </table>
    </div>
  </div>

  <!-- ═══ KPI: Millor per criteri ═══ -->
  <div class="kpi-grid">
    {kpi_html}
  </div>

  <!-- ═══ 2. Bar chart: Ranking global ═══ -->
  <div class="card">
    <h2>Ranking global (score ponderat)</h2>
    <div class="desc">Mitjana ponderada dels 5 criteris, agregant tots els jutges disponibles per cas.</div>
    <div class="chart-container">
      <canvas id="rankingBar"></canvas>
    </div>
  </div>

  <!-- ═══ 3. Radar chart: Per criteri ═══ -->
  <div class="card">
    <h2>Comparativa per criteri</h2>
    <div class="desc">5 criteris d'avaluacio: validesa pedagogica (30%), adequacio al nivell (25%), discriminacio (15%), originalitat (15%), format (15%).</div>
    <div class="chart-container">
      <canvas id="radarCriteri"></canvas>
    </div>
  </div>

  <!-- ═══ 4. Heatmap: Model x Tipus pregunta ═══ -->
  <div class="card">
    <h2>Matriu Model x Tipus de pregunta</h2>
    <div class="desc">Score ponderat per cada combinacio model-tipus. 9 tipus de Bloom (recordar ... crear) + metacognitives.</div>
    <div class="table-wrap">
      {heatmap_tipus_html}
    </div>
    <div class="legend">Vermell &lt;3.5 &middot; Groc 3.5-4.0 &middot; Verd clar 4.0-4.5 &middot; Verd fosc &gt;4.5</div>
  </div>

  <!-- ═══ 5. Heatmap: Model x Perfil ═══ -->
  <div class="card">
    <h2>Matriu Model x Perfil d'alumne</h2>
    <div class="desc">Score ponderat per cada combinacio model-perfil. 6 perfils d'alumnat divers.</div>
    <div class="table-wrap">
      {heatmap_perfil_html}
    </div>
    <div class="legend">Vermell &lt;3.5 &middot; Groc 3.5-4.0 &middot; Verd clar 4.0-4.5 &middot; Verd fosc &gt;4.5</div>
  </div>

  <!-- ═══ 6. JSON validity ═══ -->
  <div class="card">
    <h2>Validesa del JSON generat</h2>
    <div class="desc">Percentatge de respostes amb JSON valid (parsejable i amb l'estructura correcta).</div>
    <div class="table-wrap">
      {json_valid_html}
    </div>
  </div>

  <!-- ═══ 7. Inter-judge correlation ═══ -->
  <div class="card">
    <h2>Concordanca inter-jutge</h2>
    <div class="desc">Correlacio de Pearson entre parelles de jutges sobre totes les puntuacions compartides.</div>
    <div class="table-wrap">
      {judge_html}
    </div>
    <div class="legend">Verd (&ge;0.7) = concordanca forta &middot; Groc (0.4-0.7) = moderada &middot; Vermell (&lt;0.4) = baixa &middot; Blau = diagonal</div>
  </div>

  <div class="footer">
    Dashboard generat automaticament &middot; ATNE Experiment Questions &middot; {datetime.now().strftime("%Y-%m-%d %H:%M")}
  </div>
</div>

<script>
// ── Chart defaults (dark theme) ──
Chart.defaults.color = '#94a3b8';
Chart.defaults.borderColor = '#233554';

// ── 2. Ranking bar chart ──
new Chart(document.getElementById('rankingBar'), {{
  type: 'bar',
  data: {{
    labels: {bar_labels},
    datasets: [{{
      label: 'Score ponderat',
      data: {bar_scores},
      backgroundColor: {bar_colors},
      borderColor: {bar_colors},
      borderWidth: 2,
      borderRadius: 6,
    }}]
  }},
  options: {{
    responsive: true,
    maintainAspectRatio: false,
    scales: {{
      y: {{
        beginAtZero: false,
        min: 3.0,
        max: 5.0,
        title: {{ display: true, text: 'Score ponderat (0-5)', color: '#94a3b8' }},
        grid: {{ color: '#233554' }},
      }},
      x: {{
        grid: {{ display: false }},
      }}
    }},
    plugins: {{
      legend: {{ display: false }},
      title: {{
        display: true,
        text: 'Ranking global per model (mitjana ponderada dels jutges)',
        color: '#e2e8f0',
        font: {{ size: 14 }}
      }}
    }}
  }}
}});

// ── 3. Radar per criteri ──
new Chart(document.getElementById('radarCriteri'), {{
  type: 'radar',
  data: {{
    labels: {radar_labels},
    datasets: {radar_datasets_json}
  }},
  options: {{
    responsive: true,
    maintainAspectRatio: false,
    scales: {{
      r: {{
        beginAtZero: false,
        min: 2.5,
        max: 5.0,
        ticks: {{ stepSize: 0.5, color: '#94a3b8', backdropColor: 'transparent' }},
        grid: {{ color: '#233554' }},
        pointLabels: {{ color: '#e2e8f0', font: {{ size: 12 }} }},
        angleLines: {{ color: '#233554' }},
      }}
    }},
    plugins: {{
      title: {{
        display: true,
        text: 'Comparativa per criteri — 4 models',
        color: '#e2e8f0',
        font: {{ size: 14 }}
      }},
      legend: {{ position: 'bottom', labels: {{ padding: 20 }} }}
    }}
  }}
}});
</script>
</body>
</html>"""

    return html


def main():
    data = load_data()
    evals = data.get("avaluacions", [])
    if not evals:
        print("Sense dades. Abortant.")
        sys.exit(1)

    print(f"Carregades {len(evals)} avaluacions")
    print(f"Jutges: {', '.join(data.get('jutges', []))}")

    metrics = compute_metrics(evals)
    print_ranking(metrics)

    html = generate_html(metrics, data)
    DASHBOARD_PATH.write_text(html, encoding="utf-8")
    print(f"Dashboard generat: {DASHBOARD_PATH}")


if __name__ == "__main__":
    main()
