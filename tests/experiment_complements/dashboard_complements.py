#!/usr/bin/env python3
"""
Dashboard Complements — Generador HTML autocontingut amb Chart.js.

Llegeix resultats_avaluacio_complements.json i genera dashboard_complements.html
amb 6 seccions: hero, ranking global, radar criteris, heatmap tipus, heatmap perfil,
correlació inter-jutge.
"""
import json, sys, io
import numpy as np
from pathlib import Path
from collections import defaultdict
from datetime import datetime

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

EXP_DIR = Path(__file__).resolve().parent
EVAL_PATH = EXP_DIR / "resultats_avaluacio_complements.json"
DASHBOARD_PATH = EXP_DIR / "dashboard_complements.html"

# ── Configuració ──
CRITERIS = ["correccio_linguistica", "adequacio_perfil", "carrega_cognitiva",
            "utilitat_practica", "coherencia_text"]
CRITERIS_LABELS = {
    "correccio_linguistica": "Correcció lingüística",
    "adequacio_perfil": "Adequació al perfil",
    "carrega_cognitiva": "Càrrega cognitiva",
    "utilitat_practica": "Utilitat pràctica",
    "coherencia_text": "Coherència amb el text",
}
PESOS = [0.20, 0.25, 0.20, 0.25, 0.10]

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

TIPUS_LABELS = {
    "glossari_simple": "Glossari simple",
    "glossari_bilingue_arab": "Glossari bilingüe àrab",
    "esquema_visual": "Esquema visual",
    "mapa_conceptual": "Mapa conceptual",
    "pictogrames_descrits": "Pictogrames descrits",
    "transliteracio_fonetica": "Transliteració fonètica",
    "analogies_quotidianes": "Analogies quotidianes",
    "preguntes_intercalades": "Preguntes intercalades",
}

PERFIL_LABELS = {
    "nouvingut_arabic": "Nouvingut (àrab)",
    "tdah_lleu": "TDAH lleu",
    "altes_capacitats": "Altes capacitats",
    "tdl_pragmatica": "TDL pragmàtica",
    "doble_excepcionalitat": "2e (AC + dislèxia)",
    "tdah_di_lleu": "TDAH + DI lleu",
}


def extract_score(jdata, c):
    """Extreu puntuació d'un criteri dins les dades d'un jutge."""
    if not jdata or "error" in jdata:
        return None
    if c in jdata and isinstance(jdata[c], dict) and "puntuacio" in jdata[c]:
        try:
            return int(jdata[c]["puntuacio"])
        except (ValueError, TypeError):
            return None
    return None


def compute_metrics(evals):
    """Calcula totes les mètriques a partir de les avaluacions."""
    models = sorted(set(e["model_generador"] for e in evals))
    jutges = set()
    for e in evals:
        for j in e["evaluations"].keys():
            jutges.add(j)
    jutges = sorted(jutges)

    # Acumuladors
    by_model_crit = defaultdict(lambda: defaultdict(list))
    by_tipus_model = defaultdict(lambda: defaultdict(list))
    by_perfil_model = defaultdict(lambda: defaultdict(list))

    for e in evals:
        m = e["model_generador"]
        tipus = e.get("tipus_complement", "?")
        perfil = e.get("perfil_id", "?")
        case_weighted = []
        case_by_crit = {}

        for c, w in zip(CRITERIS, PESOS):
            crit_scores = []
            for j, jdata in e["evaluations"].items():
                s = extract_score(jdata, c)
                if s is not None:
                    crit_scores.append(s)
            if crit_scores:
                avg_c = float(np.mean(crit_scores))
                by_model_crit[m][c].append(avg_c)
                case_by_crit[c] = avg_c
                case_weighted.append(avg_c * w)

        if case_weighted:
            total = sum(case_weighted)
            by_model_crit[m]["_total"].append(total)
            by_tipus_model[tipus][m].append(total)
            by_perfil_model[perfil][m].append(total)

    # Ranking global
    ranking = []
    for m in models:
        totals = by_model_crit[m]["_total"]
        if totals:
            ranking.append((m, float(np.mean(totals)), len(totals)))
    ranking.sort(key=lambda x: -x[1])

    # Per criteri per model
    criteris_per_model = {}
    for m in models:
        criteris_per_model[m] = {}
        for c in CRITERIS:
            vals = by_model_crit[m][c]
            criteris_per_model[m][c] = float(np.mean(vals)) if vals else 0

    # Heatmap: tipus × model
    tipus_ids = sorted(by_tipus_model.keys())
    heatmap_tipus = {}
    for tipus in tipus_ids:
        heatmap_tipus[tipus] = {}
        for m in models:
            vals = by_tipus_model[tipus][m]
            heatmap_tipus[tipus][m] = float(np.mean(vals)) if vals else 0

    # Heatmap: perfil × model
    perfil_ids = sorted(by_perfil_model.keys())
    heatmap_perfil = {}
    for perfil in perfil_ids:
        heatmap_perfil[perfil] = {}
        for m in models:
            vals = by_perfil_model[perfil][m]
            heatmap_perfil[perfil][m] = float(np.mean(vals)) if vals else 0

    # Correlació inter-jutge
    judge_scores = defaultdict(list)
    for e in evals:
        for c in CRITERIS:
            for j in jutges:
                s = extract_score(e["evaluations"].get(j, {}), c)
                judge_scores[j].append((e["case_id"], c, s))

    judge_corr = {}
    for i, j1 in enumerate(jutges):
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
                    judge_corr[j1][j2] = 0
            else:
                judge_corr[j1][j2] = 0

    return {
        "models": models,
        "jutges": jutges,
        "ranking": ranking,
        "criteris_per_model": criteris_per_model,
        "tipus_ids": tipus_ids,
        "heatmap_tipus": heatmap_tipus,
        "perfil_ids": perfil_ids,
        "heatmap_perfil": heatmap_perfil,
        "judge_corr": judge_corr,
        "total_evals": len(evals),
    }


def generate_html(metrics, data):
    """Genera l'HTML complet del dashboard."""
    models = metrics["models"]
    jutges = metrics["jutges"]
    ranking = metrics["ranking"]
    total = metrics["total_evals"]
    data_timestamp = data.get("data", "-")[:19]

    winner = ranking[0] if ranking else ("?", 0, 0)
    winner_label = MODEL_LABELS.get(winner[0], winner[0])
    winner_score = winner[1]

    # ── JSON per Chart.js ──
    model_labels_json = json.dumps([MODEL_LABELS.get(m, m) for m in models])
    model_colors_json = json.dumps([MODEL_COLORS.get(m, "#888") for m in models])

    # Bar chart: ranking global
    ranking_labels = json.dumps([MODEL_LABELS.get(r[0], r[0]) for r in ranking])
    ranking_scores = json.dumps([round(r[1], 2) for r in ranking])
    ranking_colors = json.dumps([MODEL_COLORS.get(r[0], "#888") for r in ranking])
    ranking_n = json.dumps([r[2] for r in ranking])

    # Radar: per criteri
    criteris_labels_json = json.dumps([CRITERIS_LABELS[c] for c in CRITERIS])
    radar_datasets = []
    for m in models:
        radar_datasets.append({
            "label": MODEL_LABELS.get(m, m),
            "data": [round(metrics["criteris_per_model"][m][c], 2) for c in CRITERIS],
            "backgroundColor": MODEL_COLORS.get(m, "#888") + "33",
            "borderColor": MODEL_COLORS.get(m, "#888"),
            "borderWidth": 2,
            "pointBackgroundColor": MODEL_COLORS.get(m, "#888"),
        })
    radar_datasets_json = json.dumps(radar_datasets)

    # Heatmap: tipus × model
    tipus_ids = metrics["tipus_ids"]
    heatmap_tipus = metrics["heatmap_tipus"]

    # Heatmap: perfil × model
    perfil_ids = metrics["perfil_ids"]
    heatmap_perfil = metrics["heatmap_perfil"]

    # Correlació inter-jutge
    judge_corr = metrics["judge_corr"]

    # ── Hero ranking table rows ──
    hero_rows = ""
    medal = ["🥇", "🥈", "🥉", "4t"]
    for i, (m, sc, n) in enumerate(ranking):
        color = MODEL_COLORS.get(m, "#888")
        hero_rows += f"""
        <tr>
          <td style="font-size:20px;text-align:center;">{medal[i] if i < 4 else str(i+1)}</td>
          <td><span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:{color};margin-right:8px;"></span><strong>{MODEL_LABELS.get(m, m)}</strong></td>
          <td style="font-size:20px;font-weight:bold;color:{color};">{sc:.2f}</td>
          <td style="color:#8b95a5;">{n} casos</td>
        </tr>"""

    # ── Heatmap tipus HTML ──
    heatmap_tipus_html = _build_heatmap_table(
        row_keys=tipus_ids,
        col_keys=models,
        data_dict=heatmap_tipus,
        row_labels=TIPUS_LABELS,
        col_labels=MODEL_LABELS,
        col_colors=MODEL_COLORS,
    )

    # ── Heatmap perfil HTML ──
    heatmap_perfil_html = _build_heatmap_table(
        row_keys=perfil_ids,
        col_keys=models,
        data_dict=heatmap_perfil,
        row_labels=PERFIL_LABELS,
        col_labels=MODEL_LABELS,
        col_colors=MODEL_COLORS,
    )

    # ── Correlació inter-jutge HTML ──
    jutge_labels = {
        "gpt4o": "GPT-4o",
        "gemini_flash": "Gemini Flash",
        "qwen_judge": "Qwen",
        "llama_judge": "Llama",
        "mistral_judge": "Mistral",
    }
    corr_header = "".join(f'<th style="font-size:12px;padding:10px 6px;">{jutge_labels.get(j, j)}</th>' for j in jutges)
    corr_rows = ""
    for j1 in jutges:
        cells = ""
        for j2 in jutges:
            val = judge_corr.get(j1, {}).get(j2, 0)
            val_r = round(val, 2)
            if j1 == j2:
                bg = "#2d2d4a"
                txt = "—"
            elif val >= 0.7:
                bg = "#065f46"
                txt = str(val_r)
            elif val >= 0.4:
                bg = "#78350f"
                txt = str(val_r)
            else:
                bg = "#7f1d1d"
                txt = str(val_r)
            cells += f'<td style="background:{bg};text-align:center;padding:10px 6px;font-weight:600;">{txt}</td>'
        corr_rows += f'<tr><td style="font-weight:600;padding:10px 8px;">{jutge_labels.get(j1, j1)}</td>{cells}</tr>'

    # ── Millor per criteri (per hero) ──
    best_per_crit = []
    for c in CRITERIS:
        scores_c = [(m, metrics["criteris_per_model"][m][c]) for m in models]
        best = max(scores_c, key=lambda x: x[1])
        best_per_crit.append((c, best[0], best[1]))

    best_crit_html = ""
    for c, m, sc in best_per_crit:
        color = MODEL_COLORS.get(m, "#888")
        best_crit_html += f"""
        <div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid #2d2d4a;">
          <span style="color:#a0aec0;">{CRITERIS_LABELS[c]}</span>
          <span><strong style="color:{color};">{MODEL_LABELS.get(m, m)}</strong> <span style="color:#e2e8f0;">{sc:.2f}</span></span>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Experiment Complements · Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
    background: #1a1a2e;
    color: #e2e8f0;
    min-height: 100vh;
  }}
  .container {{ max-width: 1200px; margin: 0 auto; padding: 24px; }}

  /* Hero banner */
  .hero {{
    background: linear-gradient(135deg, #16213e 0%, #0f3460 60%, #1a1a4e 100%);
    border-radius: 16px;
    padding: 48px 40px;
    margin-bottom: 32px;
    border: 1px solid #2d2d4a;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
  }}
  .hero h1 {{
    font-size: 28px;
    color: #94a3b8;
    font-weight: 400;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-size: 13px;
  }}
  .hero .winner-name {{
    font-size: 36px;
    font-weight: 800;
    color: #4285f4;
    margin-bottom: 4px;
  }}
  .hero .winner-subtitle {{
    font-size: 18px;
    color: #a0aec0;
    margin-bottom: 24px;
  }}
  .hero table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
  }}
  .hero table td {{
    padding: 12px 16px;
    border-bottom: 1px solid #2d2d4a;
    font-size: 15px;
  }}
  .hero table tr:last-child td {{ border-bottom: none; }}

  /* Cards */
  .card {{
    background: #16213e;
    border-radius: 12px;
    padding: 28px;
    margin-bottom: 24px;
    border: 1px solid #2d2d4a;
    box-shadow: 0 4px 16px rgba(0,0,0,0.3);
  }}
  .card h2 {{
    font-size: 20px;
    color: #e2e8f0;
    margin-bottom: 6px;
  }}
  .card .subtitle {{
    font-size: 13px;
    color: #64748b;
    margin-bottom: 20px;
  }}
  .chart-container {{
    position: relative;
    height: 400px;
    margin: 16px 0;
  }}

  /* Heatmap tables */
  .heatmap-table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 12px;
  }}
  .heatmap-table th {{
    padding: 10px 12px;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #94a3b8;
    text-align: center;
    border-bottom: 2px solid #2d2d4a;
  }}
  .heatmap-table th:first-child {{ text-align: left; }}
  .heatmap-table td {{
    padding: 12px;
    text-align: center;
    font-weight: 700;
    font-size: 15px;
    border-bottom: 1px solid #1a1a2e;
  }}
  .heatmap-table td:first-child {{
    text-align: left;
    font-weight: 600;
    color: #a0aec0;
    font-size: 13px;
  }}
  .heatmap-table tr:hover {{ background: #1a1a3e; }}

  /* Correlation table */
  .corr-table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 12px;
  }}
  .corr-table th {{
    padding: 10px 8px;
    color: #94a3b8;
    border-bottom: 2px solid #2d2d4a;
    font-size: 12px;
  }}
  .corr-table td {{
    font-size: 14px;
    color: #e2e8f0;
  }}

  /* Grid */
  .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
  @media (max-width: 900px) {{ .grid-2 {{ grid-template-columns: 1fr; }} }}

  /* KPI */
  .kpi-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
  }}
  .kpi {{
    background: #16213e;
    border: 1px solid #2d2d4a;
    border-radius: 10px;
    padding: 20px;
    text-align: center;
  }}
  .kpi-label {{ font-size: 11px; text-transform: uppercase; color: #64748b; letter-spacing: 0.08em; }}
  .kpi-value {{ font-size: 28px; font-weight: 800; margin: 8px 0 4px; }}
  .kpi-sub {{ font-size: 12px; color: #64748b; }}

  .footer {{
    text-align: center;
    color: #475569;
    padding: 32px;
    font-size: 12px;
  }}

  .legend-row {{
    display: flex;
    gap: 20px;
    justify-content: center;
    margin-top: 12px;
    flex-wrap: wrap;
  }}
  .legend-item {{
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    color: #94a3b8;
  }}
  .legend-dot {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
  }}
</style>
</head>
<body>
<div class="container">

  <!-- ═══ Hero ═══ -->
  <div class="hero">
    <h1>Experiment Complements ATNE</h1>
    <div class="winner-name">{winner_label}: millor model per generar complements</div>
    <div class="winner-subtitle">Puntuació ponderada {winner_score:.2f}/5 · {total} avaluacions · {len(jutges)} jutges · {data_timestamp}</div>
    <table>
      {hero_rows}
    </table>
  </div>

  <!-- ═══ KPIs ═══ -->
  <div class="kpi-grid">
    <div class="kpi">
      <div class="kpi-label">Total avaluacions</div>
      <div class="kpi-value" style="color:#4285f4;">{total}</div>
      <div class="kpi-sub">{len(models)} models × {len(tipus_ids)} tipus × {len(perfil_ids)} perfils</div>
    </div>
    <div class="kpi">
      <div class="kpi-label">Millor score</div>
      <div class="kpi-value" style="color:{MODEL_COLORS.get(winner[0], '#fff')};">{winner_score:.2f}</div>
      <div class="kpi-sub">{winner_label}</div>
    </div>
    <div class="kpi">
      <div class="kpi-label">Jutges LLM</div>
      <div class="kpi-value" style="color:#a78bfa;">{len(jutges)}</div>
      <div class="kpi-sub">{', '.join(jutge_labels.get(j, j) for j in jutges)}</div>
    </div>
    <div class="kpi">
      <div class="kpi-label">Criteris avaluats</div>
      <div class="kpi-value" style="color:#fbbf24;">{len(CRITERIS)}</div>
      <div class="kpi-sub">Pesos: {' / '.join(f'{int(w*100)}%' for w in PESOS)}</div>
    </div>
  </div>

  <!-- ═══ Secció 1: Ranking global (bar chart) ═══ -->
  <div class="card">
    <h2>Ranking global per model</h2>
    <div class="subtitle">Puntuació ponderada mitjana (5 criteris × {len(jutges)} jutges) — Pesos: correc. 20% · perfil 25% · càrrega 20% · utilitat 25% · coherència 10%</div>
    <div class="chart-container">
      <canvas id="rankingChart"></canvas>
    </div>
  </div>

  <!-- ═══ Secció 2: Radar per criteri ═══ -->
  <div class="card">
    <h2>Comparativa per criteri (radar)</h2>
    <div class="subtitle">Mitjana de tots els jutges per a cadascun dels 5 criteris d'avaluació</div>
    <div class="chart-container" style="height:500px;">
      <canvas id="radarChart"></canvas>
    </div>
  </div>

  <!-- ═══ Secció 3: Millor per criteri ═══ -->
  <div class="card">
    <h2>Millor model per criteri</h2>
    <div class="subtitle">Quin model destaca en cada dimensió?</div>
    {best_crit_html}
  </div>

  <!-- ═══ Secció 4: Heatmap Model × Tipus complement ═══ -->
  <div class="card">
    <h2>Heatmap: Model × Tipus de complement</h2>
    <div class="subtitle">Puntuació ponderada per a cada combinació model-complement ({len(tipus_ids)} tipus)</div>
    <div style="overflow-x:auto;">
      {heatmap_tipus_html}
    </div>
  </div>

  <!-- ═══ Secció 5: Heatmap Model × Perfil ═══ -->
  <div class="card">
    <h2>Heatmap: Model × Perfil d'alumne</h2>
    <div class="subtitle">Puntuació ponderada per a cada combinació model-perfil ({len(perfil_ids)} perfils)</div>
    <div style="overflow-x:auto;">
      {heatmap_perfil_html}
    </div>
  </div>

  <!-- ═══ Secció 6: Correlació inter-jutge ═══ -->
  <div class="card">
    <h2>Concordança inter-jutge (correlació Pearson)</h2>
    <div class="subtitle">Matriu de correlació entre els {len(jutges)} jutges LLM · Verd (r &ge; 0.7) = forta · Taronja (0.4-0.7) = moderada · Vermell (&lt; 0.4) = baixa</div>
    <div style="overflow-x:auto;">
      <table class="corr-table">
        <thead>
          <tr><th></th>{corr_header}</tr>
        </thead>
        <tbody>
          {corr_rows}
        </tbody>
      </table>
    </div>
  </div>

  <div class="footer">
    Dashboard generat automàticament · Experiment Complements ATNE · {datetime.now().strftime('%Y-%m-%d %H:%M')}
  </div>

</div>

<script>
// ═══ Configuració global Chart.js ═══
Chart.defaults.color = '#94a3b8';
Chart.defaults.borderColor = '#2d2d4a';

// ═══ Secció 1: Ranking global ═══
new Chart(document.getElementById('rankingChart'), {{
  type: 'bar',
  data: {{
    labels: {ranking_labels},
    datasets: [{{
      label: 'Puntuació ponderada',
      data: {ranking_scores},
      backgroundColor: {ranking_colors},
      borderColor: {ranking_colors},
      borderWidth: 2,
      borderRadius: 6,
      barPercentage: 0.6,
    }}]
  }},
  options: {{
    responsive: true,
    maintainAspectRatio: false,
    indexAxis: 'y',
    scales: {{
      x: {{
        min: 3.5,
        max: 5,
        grid: {{ color: '#2d2d4a' }},
        ticks: {{ color: '#94a3b8', font: {{ size: 13 }} }},
        title: {{ display: true, text: 'Puntuació (0-5)', color: '#64748b' }}
      }},
      y: {{
        grid: {{ display: false }},
        ticks: {{ color: '#e2e8f0', font: {{ size: 14, weight: 'bold' }} }}
      }}
    }},
    plugins: {{
      legend: {{ display: false }},
      tooltip: {{
        callbacks: {{
          afterLabel: function(ctx) {{
            const ns = {ranking_n};
            return 'n = ' + ns[ctx.dataIndex] + ' casos';
          }}
        }}
      }}
    }}
  }}
}});

// ═══ Secció 2: Radar per criteri ═══
new Chart(document.getElementById('radarChart'), {{
  type: 'radar',
  data: {{
    labels: {criteris_labels_json},
    datasets: {radar_datasets_json}
  }},
  options: {{
    responsive: true,
    maintainAspectRatio: false,
    scales: {{
      r: {{
        beginAtZero: false,
        min: 3.5,
        max: 5,
        ticks: {{
          stepSize: 0.25,
          color: '#64748b',
          backdropColor: 'transparent',
          font: {{ size: 11 }}
        }},
        grid: {{ color: '#2d2d4a' }},
        pointLabels: {{
          color: '#e2e8f0',
          font: {{ size: 13 }}
        }}
      }}
    }},
    plugins: {{
      legend: {{
        position: 'bottom',
        labels: {{
          color: '#e2e8f0',
          padding: 20,
          usePointStyle: true,
          pointStyleWidth: 12,
          font: {{ size: 13 }}
        }}
      }}
    }}
  }}
}});
</script>

</body>
</html>
"""
    return html


def _build_heatmap_table(row_keys, col_keys, data_dict, row_labels, col_labels, col_colors):
    """Genera una taula HTML heatmap amb colors per intensitat."""
    # Trobar min i max per al gradient
    all_vals = []
    for rk in row_keys:
        for ck in col_keys:
            v = data_dict.get(rk, {}).get(ck, 0)
            if v > 0:
                all_vals.append(v)

    if all_vals:
        vmin = min(all_vals)
        vmax = max(all_vals)
    else:
        vmin, vmax = 0, 5

    def val_to_color(v):
        """Retorna color de fons segons la puntuació."""
        if v == 0:
            return "#1a1a2e"
        if v >= 4.6:
            return "#065f46"  # verd fosc
        elif v >= 4.4:
            return "#047857"  # verd
        elif v >= 4.2:
            return "#0d9488"  # teal
        elif v >= 4.0:
            return "#0e7490"  # cyan fosc
        elif v >= 3.8:
            return "#b45309"  # taronja fosc
        else:
            return "#9f1239"  # vermell fosc

    # Trobar millor per fila (per marcar)
    best_per_row = {}
    for rk in row_keys:
        best_m = None
        best_v = -1
        for ck in col_keys:
            v = data_dict.get(rk, {}).get(ck, 0)
            if v > best_v:
                best_v = v
                best_m = ck
        best_per_row[rk] = best_m

    header = '<th style="min-width:180px;"></th>'
    for ck in col_keys:
        color = col_colors.get(ck, "#888")
        label = col_labels.get(ck, ck)
        header += f'<th><span style="color:{color};">{label}</span></th>'

    rows = ""
    for rk in row_keys:
        label = row_labels.get(rk, rk)
        cells = f'<td>{label}</td>'
        for ck in col_keys:
            v = data_dict.get(rk, {}).get(ck, 0)
            bg = val_to_color(v)
            is_best = (best_per_row.get(rk) == ck)
            border = f"border:2px solid #fbbf24;" if is_best else ""
            display_v = f"{v:.2f}" if v > 0 else "—"
            cells += f'<td style="background:{bg};{border}border-radius:4px;">{display_v}</td>'
        rows += f'<tr>{cells}</tr>'

    return f"""
    <table class="heatmap-table">
      <thead><tr>{header}</tr></thead>
      <tbody>{rows}</tbody>
    </table>
    <div class="legend-row" style="margin-top:16px;">
      <span class="legend-item"><span class="legend-dot" style="background:#9f1239;"></span> &lt; 3.8</span>
      <span class="legend-item"><span class="legend-dot" style="background:#b45309;"></span> 3.8-4.0</span>
      <span class="legend-item"><span class="legend-dot" style="background:#0e7490;"></span> 4.0-4.2</span>
      <span class="legend-item"><span class="legend-dot" style="background:#0d9488;"></span> 4.2-4.4</span>
      <span class="legend-item"><span class="legend-dot" style="background:#047857;"></span> 4.4-4.6</span>
      <span class="legend-item"><span class="legend-dot" style="background:#065f46;"></span> &ge; 4.6</span>
      <span class="legend-item"><span style="width:10px;height:10px;border:2px solid #fbbf24;border-radius:2px;"></span> Millor de la fila</span>
    </div>"""


def main():
    if not EVAL_PATH.exists():
        print(f"No existeix: {EVAL_PATH}")
        sys.exit(1)

    data = json.loads(EVAL_PATH.read_text(encoding="utf-8"))
    evals = data["avaluacions"]
    print(f"Carregades {len(evals)} avaluacions")

    metrics = compute_metrics(evals)
    print(f"Models: {metrics['models']}")
    print(f"Jutges: {metrics['jutges']}")
    print(f"Tipus: {metrics['tipus_ids']}")
    print(f"Perfils: {metrics['perfil_ids']}")

    # Imprimir ranking a stdout
    print("\n" + "=" * 60)
    print("  RANKING GLOBAL — Experiment Complements")
    print("=" * 60)
    medal = ["1r", "2n", "3r", "4t"]
    for i, (m, sc, n) in enumerate(metrics["ranking"]):
        prefix = medal[i] if i < 4 else f"{i+1}e"
        print(f"  {prefix}  {MODEL_LABELS.get(m, m):20s}  {sc:.2f}/5  (n={n})")
    print("=" * 60)

    # Generar HTML
    html = generate_html(metrics, data)
    DASHBOARD_PATH.write_text(html, encoding="utf-8")
    print(f"\nDashboard generat: {DASHBOARD_PATH}")
    print(f"Mida: {DASHBOARD_PATH.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
