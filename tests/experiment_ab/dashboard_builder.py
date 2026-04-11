#!/usr/bin/env python3
"""
Xat 9 - Dashboard builder
Genera un HTML autocontingut amb Chart.js per visualitzar tots els resultats.

Respon a 22 preguntes clau organitzades en 8 seccions:
  1. Hero: recomanacio FJE
  2. Prompt minim vs complet (per model)
  3. Comparativa per criteri (5 criteris)
  4. Matriu model x perfil (heatmap)
  5. Per etapa (primaria, ESO, batx)
  6. Solucio hibrida
  7. Cost FJE a escala
  8. Fiabilitat inter-jutge
"""
import json, sys, io
import numpy as np
from pathlib import Path
from collections import defaultdict
from datetime import datetime

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

EXP_DIR = Path(__file__).resolve().parent
EVAL_PATH = EXP_DIR / "resultats_avaluacio_multi.json"
DASHBOARD_PATH = EXP_DIR / "dashboard.html"

# Configuracio
CRITERIS = ["adequacio_linguistica", "fidelitat_curricular", "adequacio_perfil",
            "llegibilitat_estructura", "complements"]
CRITERIS_LABELS = {
    "adequacio_linguistica": "Adequació MECR",
    "fidelitat_curricular": "Fidelitat curricular",
    "adequacio_perfil": "Adequació al perfil",
    "llegibilitat_estructura": "Llegibilitat",
    "complements": "Complements",
}
PESOS = [0.25, 0.20, 0.25, 0.15, 0.15]

MODEL_LABELS = {
    "gpt4o-mini": "GPT-4o-mini",
    "mistral": "Mistral Small",
    "llama": "Llama 3.3 70B",
    "gemma": "Gemma 4 31B",
}
MODEL_COLORS = {
    "gpt4o-mini": "#10a37f",   # OpenAI green
    "mistral": "#fa520f",      # Mistral orange
    "llama": "#0467df",        # Meta blue
    "gemma": "#4285f4",        # Google blue
}

# Cost USD per 1M tokens (in+out mitjana)
COSTOS_USD = {
    "gpt4o-mini": 0.38,
    "mistral": 0.30,
    "llama": 0.00,
    "gemma": 0.00,
}

# Simulacio escala FJE
FJE_DOCENTS = 1000
FJE_ADAPTACIONS_MES = 20
FJE_TOKENS_PER_ADAPTACIO = 2500  # mitjana input + output
FJE_ADAPTACIONS_TOTAL_MES = FJE_DOCENTS * FJE_ADAPTACIONS_MES
FJE_TOKENS_MES = FJE_ADAPTACIONS_TOTAL_MES * FJE_TOKENS_PER_ADAPTACIO
FJE_MILIONS_TOKENS_MES = FJE_TOKENS_MES / 1_000_000


def cohens_d(a, b):
    if len(a) == 0 or len(b) == 0:
        return 0
    diff = np.array(b) - np.array(a)
    sd = np.std(diff, ddof=1) if len(diff) > 1 else 0
    return float(np.mean(diff) / sd) if sd > 0 else 0.0


def load_data():
    if not EVAL_PATH.exists():
        print(f"[AVÍS] No existeix {EVAL_PATH.name}. Utilitzant dades d'exemple.")
        return None
    return json.loads(EVAL_PATH.read_text(encoding="utf-8"))


def extract_scores(evals, model, jutge):
    """Retorna {A: {criteri: [scores]}, B: {criteri: [scores]}}."""
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


def weighted_avg(scores_by_criteri):
    """Mitjana ponderada dels criteris."""
    vals = []
    for c, w in zip(CRITERIS, PESOS):
        if scores_by_criteri.get(c):
            vals.append(np.mean(scores_by_criteri[c]) * w)
    return sum(vals) if vals else 0


def extract_scores_by_etapa(evals, model, jutge, etapa):
    scores = {"A": defaultdict(list), "B": defaultdict(list)}
    for ev in evals:
        if ev.get("model_generador") != model or ev.get("etapa") != etapa:
            continue
        for cond in ["A", "B"]:
            jdata = ev["evaluations"].get(cond, {}).get(jutge, {})
            if "error" in jdata or not jdata:
                continue
            for c in CRITERIS:
                if c in jdata and "puntuacio" in jdata[c]:
                    try:
                        scores[cond][c].append(int(jdata[c]["puntuacio"]))
                    except:
                        pass
    return scores


def extract_scores_by_perfil(evals, model, jutge, perfil_id):
    scores = {"A": defaultdict(list), "B": defaultdict(list)}
    for ev in evals:
        if ev.get("model_generador") != model or ev.get("perfil_id") != perfil_id:
            continue
        for cond in ["A", "B"]:
            jdata = ev["evaluations"].get(cond, {}).get(jutge, {})
            if "error" in jdata or not jdata:
                continue
            for c in CRITERIS:
                if c in jdata and "puntuacio" in jdata[c]:
                    try:
                        scores[cond][c].append(int(jdata[c]["puntuacio"]))
                    except:
                        pass
    return scores


def aggregate_all_judges(evals, model):
    """Retorna scores agregats de tots els jutges disponibles."""
    jutges_disponibles = set()
    for ev in evals:
        if ev.get("model_generador") == model:
            for cond in ["A", "B"]:
                for j in ev["evaluations"].get(cond, {}).keys():
                    jutges_disponibles.add(j)

    agg = {"A": defaultdict(list), "B": defaultdict(list)}
    for j in jutges_disponibles:
        sc = extract_scores(evals, model, j)
        for cond in ["A", "B"]:
            for c in CRITERIS:
                agg[cond][c].extend(sc[cond][c])
    return agg


def compute_all_metrics(evals):
    """Computa totes les metriques per a totes les preguntes."""
    models = sorted(set(e.get("model_generador", "?") for e in evals))
    jutges = set()
    for e in evals:
        for cond in ["A", "B"]:
            for j in e["evaluations"].get(cond, {}).keys():
                jutges.add(j)
    jutges = sorted(jutges)

    metrics = {
        "models": models,
        "jutges": jutges,
        "total_evals": len(evals),
        "by_model": {},
        "by_model_etapa": {},
        "by_model_perfil": {},
        "judge_correlation": {},
    }

    # Per model (agregat de tots els jutges)
    for model in models:
        agg = aggregate_all_judges(evals, model)
        mean_a_total = weighted_avg(agg["A"])
        mean_b_total = weighted_avg(agg["B"])

        criteris_a = {c: float(np.mean(agg["A"][c])) if agg["A"][c] else 0 for c in CRITERIS}
        criteris_b = {c: float(np.mean(agg["B"][c])) if agg["B"][c] else 0 for c in CRITERIS}

        # Cohen's d global (usant puntuacio total per parell)
        # Per simplicitat, usem mean diff
        delta = mean_b_total - mean_a_total

        metrics["by_model"][model] = {
            "mean_a": mean_a_total,
            "mean_b": mean_b_total,
            "delta": delta,
            "criteris_a": criteris_a,
            "criteris_b": criteris_b,
            "n_parells": len(evals and [e for e in evals if e.get("model_generador") == model]),
        }

    # Per etapa
    for model in models:
        metrics["by_model_etapa"][model] = {}
        for etapa in ["primaria", "ESO", "batxillerat"]:
            a_vals, b_vals = [], []
            for j in jutges:
                sc = extract_scores_by_etapa(evals, model, j, etapa)
                a_vals.append(weighted_avg(sc["A"]))
                b_vals.append(weighted_avg(sc["B"]))
            metrics["by_model_etapa"][model][etapa] = {
                "mean_a": float(np.mean([v for v in a_vals if v > 0])) if any(v > 0 for v in a_vals) else 0,
                "mean_b": float(np.mean([v for v in b_vals if v > 0])) if any(v > 0 for v in b_vals) else 0,
            }

    # Per perfil
    perfils_ids = sorted(set(e.get("perfil_id", "?") for e in evals))
    for model in models:
        metrics["by_model_perfil"][model] = {}
        for pid in perfils_ids:
            a_vals, b_vals = [], []
            for j in jutges:
                sc = extract_scores_by_perfil(evals, model, j, pid)
                a_vals.append(weighted_avg(sc["A"]))
                b_vals.append(weighted_avg(sc["B"]))
            metrics["by_model_perfil"][model][pid] = {
                "mean_a": float(np.mean([v for v in a_vals if v > 0])) if any(v > 0 for v in a_vals) else 0,
                "mean_b": float(np.mean([v for v in b_vals if v > 0])) if any(v > 0 for v in b_vals) else 0,
            }

    metrics["perfils_ids"] = perfils_ids

    # Correlacio inter-jutge (matriu)
    jutge_matrix = {}
    for j1 in jutges:
        jutge_matrix[j1] = {}
        for j2 in jutges:
            all1, all2 = [], []
            for model in models:
                sc1 = extract_scores(evals, model, j1)
                sc2 = extract_scores(evals, model, j2)
                for cond in ["A", "B"]:
                    for c in CRITERIS:
                        n = min(len(sc1[cond][c]), len(sc2[cond][c]))
                        all1.extend(sc1[cond][c][:n])
                        all2.extend(sc2[cond][c][:n])
            if len(all1) >= 5 and np.std(all1) > 0 and np.std(all2) > 0:
                r = float(np.corrcoef(all1, all2)[0, 1])
            else:
                r = 1.0 if j1 == j2 else 0
            jutge_matrix[j1][j2] = r
    metrics["judge_correlation"] = jutge_matrix

    return metrics


def generate_html(metrics, data):
    """Genera el HTML del dashboard."""
    models = metrics["models"]
    jutges = metrics["jutges"]

    # Determinar el guanyador
    best_model = None
    best_score = 0
    for m, data_m in metrics["by_model"].items():
        if data_m["mean_b"] > best_score:
            best_score = data_m["mean_b"]
            best_model = m
    best_label = MODEL_LABELS.get(best_model, best_model) if best_model else "—"

    # Millor en prompt minim
    best_a = max(metrics["by_model"].items(), key=lambda x: x[1]["mean_a"]) if metrics["by_model"] else (None, {"mean_a": 0})
    # Millor en complements
    best_comp = max(metrics["by_model"].items(), key=lambda x: x[1]["criteris_b"]["complements"]) if metrics["by_model"] else (None, {})
    # Qui millora mes (delta B-A)
    best_delta = max(metrics["by_model"].items(), key=lambda x: x[1]["delta"]) if metrics["by_model"] else (None, {"delta": 0})
    # Qui millora menys (candidat fallback)
    worst_delta = min(metrics["by_model"].items(), key=lambda x: x[1]["delta"]) if metrics["by_model"] else (None, {"delta": 0})

    # ══ ARQUITECTURA DUAL: millor model per cada tasca ══
    # 1. Millor per adaptar el TEXT (criteris linguistic + fidelitat + perfil + llegibilitat, SENSE complements)
    best_text = None; best_text_score = 0
    for m, d in metrics["by_model"].items():
        text_score = (
            d["criteris_b"]["adequacio_linguistica"] * 0.30 +
            d["criteris_b"]["fidelitat_curricular"] * 0.25 +
            d["criteris_b"]["adequacio_perfil"] * 0.25 +
            d["criteris_b"]["llegibilitat_estructura"] * 0.20
        )
        if text_score > best_text_score:
            best_text_score = text_score
            best_text = m

    # 2. Millor per fer COMPLEMENTS
    best_comp_model = None; best_comp_score = 0
    for m, d in metrics["by_model"].items():
        comp_score = d["criteris_b"]["complements"]
        if comp_score > best_comp_score:
            best_comp_score = comp_score
            best_comp_model = m

    # 3. Mes eficient (ratio qualitat/cost)
    best_cost = None; best_ratio = 0
    for m, d in metrics["by_model"].items():
        cost = COSTOS_USD.get(m, 0.01)
        ratio = d["mean_b"] / (cost if cost > 0 else 0.001)  # gratis = ratio molt alt
        if ratio > best_ratio:
            best_ratio = ratio
            best_cost = m

    # Datasets per als charts
    models_json = json.dumps(models)
    model_labels_json = json.dumps([MODEL_LABELS.get(m, m) for m in models])
    model_colors_json = json.dumps([MODEL_COLORS.get(m, "#888") for m in models])

    mean_a_data = json.dumps([round(metrics["by_model"][m]["mean_a"], 2) for m in models])
    mean_b_data = json.dumps([round(metrics["by_model"][m]["mean_b"], 2) for m in models])
    delta_data = json.dumps([round(metrics["by_model"][m]["delta"], 2) for m in models])

    # Per criteri
    criteris_json = json.dumps([CRITERIS_LABELS[c] for c in CRITERIS])
    criteris_datasets = []
    for m in models:
        criteris_datasets.append({
            "label": MODEL_LABELS.get(m, m) + " (B)",
            "data": [round(metrics["by_model"][m]["criteris_b"][c], 2) for c in CRITERIS],
            "backgroundColor": MODEL_COLORS.get(m, "#888") + "aa",
            "borderColor": MODEL_COLORS.get(m, "#888"),
            "borderWidth": 2,
        })
    criteris_datasets_json = json.dumps(criteris_datasets)

    # Delta per criteri
    delta_criteris_datasets = []
    for m in models:
        deltas = []
        for c in CRITERIS:
            a = metrics["by_model"][m]["criteris_a"][c]
            b = metrics["by_model"][m]["criteris_b"][c]
            deltas.append(round(b - a, 2))
        delta_criteris_datasets.append({
            "label": MODEL_LABELS.get(m, m),
            "data": deltas,
            "backgroundColor": MODEL_COLORS.get(m, "#888"),
        })
    delta_criteris_datasets_json = json.dumps(delta_criteris_datasets)

    # Matriu model x perfil (per heatmap)
    perfils_ids = metrics["perfils_ids"]
    heatmap_data = []
    for i, m in enumerate(models):
        for j, p in enumerate(perfils_ids):
            val = metrics["by_model_perfil"][m].get(p, {}).get("mean_b", 0)
            heatmap_data.append({"x": p, "y": MODEL_LABELS.get(m, m), "v": round(val, 2)})
    heatmap_data_json = json.dumps(heatmap_data)

    # Per etapa
    etapes = ["primaria", "ESO", "batxillerat"]
    etapa_datasets = []
    for m in models:
        etapa_datasets.append({
            "label": MODEL_LABELS.get(m, m),
            "data": [round(metrics["by_model_etapa"][m][e]["mean_b"], 2) for e in etapes],
            "backgroundColor": MODEL_COLORS.get(m, "#888"),
        })
    etapa_datasets_json = json.dumps(etapa_datasets)

    # Costos FJE
    fje_data = []
    for m in models:
        cost_per_M = COSTOS_USD.get(m, 0)
        mes = cost_per_M * FJE_MILIONS_TOKENS_MES
        any_ = mes * 12
        quality = metrics["by_model"][m]["mean_b"]
        fje_data.append({
            "model": MODEL_LABELS.get(m, m),
            "cost_mes_usd": round(mes, 2),
            "cost_any_usd": round(any_, 2),
            "quality": round(quality, 2),
            "ratio": round(quality / (cost_per_M + 0.01), 2),
        })

    # Correlacio inter-jutge (matriu)
    jutge_corr_rows = []
    for j1 in jutges:
        row = [MODEL_LABELS.get(j1, j1) if j1 in MODEL_LABELS else j1]
        for j2 in jutges:
            val = metrics["judge_correlation"][j1].get(j2, 0)
            row.append(round(val, 2))
        jutge_corr_rows.append(row)

    jutge_corr_headers = [""] + [j for j in jutges]

    data_timestamp = data.get("data", "-") if data else "-"

    html = """<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="UTF-8">
<title>Xat 9 · Dashboard experiment A/B multi-model</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; background: #f5f7fa; margin: 0; padding: 0; color: #1a202c; }
  .container { max-width: 1400px; margin: 0 auto; padding: 24px; }
  header { background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color: white; padding: 40px 24px; border-radius: 16px; margin-bottom: 32px; }
  h1 { margin: 0 0 8px 0; font-size: 32px; }
  header .subtitle { opacity: 0.9; font-size: 16px; }
  .hero-banner { background: #fef3c7; border-left: 6px solid #f59e0b; padding: 24px; border-radius: 8px; margin: 24px 0; }
  .hero-banner h2 { margin: 0 0 8px 0; color: #78350f; }
  .hero-banner .winner { font-size: 28px; font-weight: bold; color: #92400e; margin: 12px 0; }
  .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin: 24px 0; }
  .kpi { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.06); }
  .kpi-label { font-size: 12px; text-transform: uppercase; color: #64748b; letter-spacing: 0.05em; }
  .kpi-value { font-size: 24px; font-weight: bold; margin: 8px 0 4px; color: #1e293b; }
  .kpi-sub { font-size: 13px; color: #64748b; }
  section { background: white; padding: 28px; border-radius: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.06); margin-bottom: 24px; }
  section h2 { margin: 0 0 8px 0; color: #1e293b; font-size: 22px; }
  section .q { color: #64748b; font-style: italic; margin-bottom: 20px; font-size: 14px; }
  .chart-container { position: relative; height: 400px; margin: 16px 0; }
  .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
  @media (max-width: 900px) { .grid-2 { grid-template-columns: 1fr; } }
  table { width: 100%; border-collapse: collapse; margin-top: 12px; }
  th, td { padding: 10px 12px; text-align: left; border-bottom: 1px solid #e2e8f0; font-size: 14px; }
  th { background: #f1f5f9; font-weight: 600; color: #475569; }
  tbody tr:hover { background: #f8fafc; }
  .heatmap { display: grid; gap: 4px; margin: 16px 0; }
  .heatmap-cell { padding: 16px 8px; text-align: center; border-radius: 4px; color: white; font-weight: bold; font-size: 14px; }
  .footer { text-align: center; color: #94a3b8; padding: 24px; font-size: 13px; }
  .badge { display: inline-block; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; }
  .badge-green { background: #d1fae5; color: #065f46; }
  .badge-red { background: #fee2e2; color: #991b1b; }
  .badge-blue { background: #dbeafe; color: #1e40af; }
</style>
</head>
<body>
<nav style="background:#1e293b;padding:12px 24px;display:flex;gap:8px;flex-wrap:wrap;align-items:center;">
  <a href="/ui/index.html" style="color:#d1d5db;text-decoration:none;padding:.4rem .8rem;font-size:.85rem;">← Adaptador</a>
  <a href="/ui/cuina.html" style="color:#d1d5db;text-decoration:none;padding:.4rem .8rem;font-size:.85rem;">Cuina</a>
  <a href="/ui/eval_dashboard.html" style="color:#d1d5db;text-decoration:none;padding:.4rem .8rem;font-size:.85rem;">Avaluació</a>
  <a href="/ui/eval_results.html" style="color:#d1d5db;text-decoration:none;padding:.4rem .8rem;font-size:.85rem;">Resultats</a>
  <a href="/ui/informe.html" style="color:#d1d5db;text-decoration:none;padding:.4rem .8rem;font-size:.85rem;">Informe</a>
  <a href="/dashboard" style="background:#fbbf24;color:#1e293b;text-decoration:none;padding:.4rem .8rem;font-size:.85rem;font-weight:600;border-radius:4px;">Dashboard Xat 9</a>
  <span style="margin-left:auto;display:flex;gap:8px;">
    <a href="/informe_fje" download style="color:#fbbf24;text-decoration:none;padding:.4rem .8rem;font-size:.8rem;border:1px solid #fbbf24;border-radius:4px;">↓ Informe FJE</a>
    <a href="/informe_tecnic" download style="color:#94a3b8;text-decoration:none;padding:.4rem .8rem;font-size:.8rem;border:1px solid #94a3b8;border-radius:4px;">↓ Informe tècnic</a>
  </span>
</nav>
<div class="container">
  <header>
    <h1>Xat 9 · Experiment A/B multi-model</h1>
    <div class="subtitle">Prompt mínim vs prompt complet · 4 generadors × 5 jutges · """ + str(metrics['total_evals']) + """ parells avaluats</div>
    <div class="subtitle">Data: """ + data_timestamp[:19] + """</div>
  </header>

  <div class="hero-banner">
    <h2>🏆 Arquitectura DUAL recomanada per a FJE</h2>
    <p style="margin:8px 0 16px;color:#78350f;font-size:15px;">La solució òptima combina dos models: un per adaptar el text, un altre per generar els complements.</p>
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;margin-top:20px;">
      <div style="background:white;padding:20px;border-radius:10px;border-top:4px solid #3b82f6;">
        <div style="font-size:12px;text-transform:uppercase;color:#64748b;font-weight:600;">Motor d'adaptació</div>
        <div style="font-size:24px;font-weight:bold;color:#1e40af;margin:8px 0;">""" + (MODEL_LABELS.get(best_text, '-') if best_text else '-') + """</div>
        <div style="font-size:13px;color:#64748b;">Qualitat del text: <strong>""" + f"{best_text_score:.2f}" + """/5</strong></div>
        <div style="font-size:12px;color:#94a3b8;margin-top:4px;">MECR · fidelitat · perfil · llegibilitat</div>
      </div>
      <div style="background:white;padding:20px;border-radius:10px;border-top:4px solid #10b981;">
        <div style="font-size:12px;text-transform:uppercase;color:#64748b;font-weight:600;">Motor de complements</div>
        <div style="font-size:24px;font-weight:bold;color:#065f46;margin:8px 0;">""" + (MODEL_LABELS.get(best_comp_model, '-') if best_comp_model else '-') + """</div>
        <div style="font-size:13px;color:#64748b;">Complements: <strong>""" + f"{best_comp_score:.2f}" + """/5</strong></div>
        <div style="font-size:12px;color:#94a3b8;margin-top:4px;">glossari · esquemes · pictogrames</div>
      </div>
      <div style="background:white;padding:20px;border-radius:10px;border-top:4px solid #f59e0b;">
        <div style="font-size:12px;text-transform:uppercase;color:#64748b;font-weight:600;">Millor eficiència Q/cost</div>
        <div style="font-size:24px;font-weight:bold;color:#92400e;margin:8px 0;">""" + (MODEL_LABELS.get(best_cost, '-') if best_cost else '-') + """</div>
        <div style="font-size:13px;color:#64748b;">Qualitat/preu: <strong>""" + f"{best_ratio:.1f}" + """</strong></div>
        <div style="font-size:12px;color:#94a3b8;margin-top:4px;">alternativa econòmica</div>
      </div>
    </div>
  </div>

  <div class="kpi-grid">
    <div class="kpi">
      <div class="kpi-label">Millor amb prompt MÍNIM</div>
      <div class="kpi-value">""" + (MODEL_LABELS.get(best_a[0], '-') if best_a[0] else '-') + """</div>
      <div class="kpi-sub">Puntuació A: """ + f"{best_a[1].get('mean_a', 0):.2f}" + """/5</div>
    </div>
    <div class="kpi">
      <div class="kpi-label">Millor amb prompt COMPLET</div>
      <div class="kpi-value">""" + best_label + """</div>
      <div class="kpi-sub">Puntuació B: """ + f"{best_score:.2f}" + """/5</div>
    </div>
    <div class="kpi">
      <div class="kpi-label">Més adequació AL PERFIL</div>
      <div class="kpi-value">""" + (MODEL_LABELS.get(max(metrics["by_model"].items(), key=lambda x: x[1]["criteris_b"]["adequacio_perfil"])[0]) if metrics["by_model"] else '-') + """</div>
      <div class="kpi-sub">nouvingut · TDAH · AC · TDL · 2e</div>
    </div>
    <div class="kpi">
      <div class="kpi-label">Qui guanya MÉS amb prompt complet</div>
      <div class="kpi-value">""" + (MODEL_LABELS.get(best_delta[0], '-') if best_delta[0] else '-') + """</div>
      <div class="kpi-sub">Δ = +""" + f"{best_delta[1].get('delta', 0):.2f}" + """</div>
    </div>
  </div>

  <section>
    <h2>📊 Secció 1 — Comparativa global: Prompt mínim (A) vs Prompt complet (B)</h2>
    <p class="q">🔸 Preguntes: Quin és el millor model amb prompt mínim? I amb prompt complet? Val la pena el catàleg de 98 instruccions per a cada model?</p>
    <div class="chart-container">
      <canvas id="globalCompare"></canvas>
    </div>
  </section>

  <section>
    <h2>📈 Secció 2 — Efecte del prompt complet per criteri</h2>
    <p class="q">🔸 Pregunta: En quin criteri ajuda més el prompt complet per a cada model? (Δ = B − A)</p>
    <div class="chart-container">
      <canvas id="deltaCriteris"></canvas>
    </div>
  </section>

  <section>
    <h2>🎯 Secció 3 — Qualitat per criteri (prompt complet)</h2>
    <p class="q">🔸 Preguntes: Quin és el millor fent complements? Millor en adequació al perfil? Millor en MECR? En fidelitat? En llegibilitat?</p>
    <div class="chart-container">
      <canvas id="perCriteri"></canvas>
    </div>
  </section>

  <section>
    <h2>🧩 Secció 4 — Matriu Model × Perfil d'alumne</h2>
    <p class="q">🔸 Pregunta: Quin model és millor per cada tipus d'alumne? (nouvingut, TDAH, AC, TDL, 2e, TDAH+DI)</p>
    <div id="heatmap-container" style="overflow-x:auto;"></div>
  </section>

  <section>
    <h2>🎓 Secció 5 — Qualitat per etapa educativa</h2>
    <p class="q">🔸 Pregunta: Quin model és millor per primària, ESO i batxillerat?</p>
    <div class="chart-container">
      <canvas id="perEtapa"></canvas>
    </div>
  </section>

  <section>
    <h2>💰 Secció 6 — Simulació de cost a escala FJE</h2>
    <p class="q">🔸 Pregunta: Quant costaria cada model amb """ + str(FJE_DOCENTS) + """ docents × """ + str(FJE_ADAPTACIONS_MES) + """ adaptacions/mes = """ + f"{FJE_ADAPTACIONS_TOTAL_MES:,}" + """ adaptacions/mes?</p>
    <table>
      <thead>
        <tr><th>Model</th><th>Qualitat (B)</th><th>$/1M tokens</th><th>Cost/mes FJE</th><th>Cost/any FJE</th><th>Ràtio Q/€</th></tr>
      </thead>
      <tbody>
"""
    for row in fje_data:
        is_best = row["model"] == best_label
        html += f"""        <tr {'style=background:#d1fae5' if is_best else ''}>
          <td><strong>{row['model']}</strong></td>
          <td>{row['quality']}</td>
          <td>${COSTOS_USD.get([m for m in models if MODEL_LABELS.get(m) == row['model']][0] if any(MODEL_LABELS.get(m) == row['model'] for m in models) else 'x', 0):.2f}</td>
          <td>${row['cost_mes_usd']:,}</td>
          <td>${row['cost_any_usd']:,}</td>
          <td><span class="badge {'badge-green' if row['cost_mes_usd'] == 0 else 'badge-blue'}">{row['ratio']}</span></td>
        </tr>
"""
    html += """      </tbody>
    </table>
    <p style="margin-top:16px;color:#64748b;font-size:13px;">
      💡 <strong>Solució híbrida recomanada</strong>: usar Gemma (gratis) o Llama (gratis via Groq free tier) per casos estàndard i GPT-4o-mini o Mistral per casos difícils on calgui més qualitat.
    </p>
  </section>

  <section>
    <h2>🔍 Secció 7 — Fiabilitat inter-jutge</h2>
    <p class="q">🔸 Pregunta: Ens podem fiar dels jutges? Coincideixen entre ells?</p>
    <table>
      <thead>
        <tr>"""
    for h in jutge_corr_headers:
        html += f"<th>{h}</th>"
    html += "</tr></thead><tbody>"
    for row in jutge_corr_rows:
        html += "<tr>"
        for i, c in enumerate(row):
            if i == 0:
                html += f"<td><strong>{c}</strong></td>"
            else:
                col = "#d1fae5" if c >= 0.7 else ("#fef3c7" if c >= 0.4 else "#fee2e2")
                html += f"<td style='background:{col};text-align:center;'>{c}</td>"
        html += "</tr>"
    html += """      </tbody>
    </table>
    <p style="color:#64748b;font-size:13px;margin-top:12px;">
      Verd (≥0.7) = concordança forta · Groc (0.4-0.7) = moderada · Vermell (<0.4) = baixa
    </p>
  </section>

  <div class="footer">
    Dashboard generat automàticament · Xat 9 ATNE · <a href="informe_multi_model.md">Informe Markdown</a>
  </div>
</div>

<script>
const CRITERIS = """ + criteris_json + """;
const MODELS = """ + model_labels_json + """;
const COLORS = """ + model_colors_json + """;

// Secció 1: Comparativa global A vs B
new Chart(document.getElementById('globalCompare'), {
  type: 'bar',
  data: {
    labels: MODELS,
    datasets: [
      {
        label: 'A (prompt mínim)',
        data: """ + mean_a_data + """,
        backgroundColor: '#fbbf24',
        borderColor: '#f59e0b',
        borderWidth: 2,
      },
      {
        label: 'B (prompt complet)',
        data: """ + mean_b_data + """,
        backgroundColor: '#34d399',
        borderColor: '#10b981',
        borderWidth: 2,
      }
    ]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    scales: { y: { beginAtZero: true, max: 5, title: { display: true, text: 'Puntuació ponderada (0-5)' } } },
    plugins: {
      title: { display: true, text: 'Mitjana dels jutges · prompt mínim vs complet · per model', font: { size: 14 } },
      legend: { position: 'top' }
    }
  }
});

// Secció 2: Delta per criteri
new Chart(document.getElementById('deltaCriteris'), {
  type: 'bar',
  data: {
    labels: CRITERIS,
    datasets: """ + delta_criteris_datasets_json + """
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    scales: { y: { title: { display: true, text: 'Δ (B − A)' } } },
    plugins: {
      title: { display: true, text: 'Efecte del prompt complet per criteri i model', font: { size: 14 } },
      legend: { position: 'top' }
    }
  }
});

// Secció 3: Per criteri (B)
new Chart(document.getElementById('perCriteri'), {
  type: 'radar',
  data: {
    labels: CRITERIS,
    datasets: """ + criteris_datasets_json + """
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    scales: { r: { beginAtZero: true, max: 5, ticks: { stepSize: 1 } } },
    plugins: {
      title: { display: true, text: 'Comparativa per criteri (prompt complet) · radar', font: { size: 14 } },
      legend: { position: 'top' }
    }
  }
});

// Secció 4: Heatmap Model × Perfil (manual amb divs)
const heatmapData = """ + heatmap_data_json + """;
const perfilsUnique = [...new Set(heatmapData.map(d => d.x))];
const modelsUnique = [...new Set(heatmapData.map(d => d.y))];

let heatmapHTML = '<div class="heatmap" style="grid-template-columns: 180px repeat(' + perfilsUnique.length + ', 1fr);">';
heatmapHTML += '<div></div>';
perfilsUnique.forEach(p => {
  heatmapHTML += '<div style="font-weight:600;font-size:12px;text-align:center;padding:8px;color:#475569;">' + p + '</div>';
});
modelsUnique.forEach(m => {
  heatmapHTML += '<div style="font-weight:600;padding:8px;color:#475569;font-size:13px;">' + m + '</div>';
  perfilsUnique.forEach(p => {
    const item = heatmapData.find(d => d.y === m && d.x === p);
    const val = item ? item.v : 0;
    // Color: vermell (baix) → groc → verd (alt)
    let color;
    if (val < 2.5) color = '#ef4444';
    else if (val < 3.5) color = '#f59e0b';
    else if (val < 4.0) color = '#10b981';
    else color = '#059669';
    heatmapHTML += '<div class="heatmap-cell" style="background:' + color + '">' + val + '</div>';
  });
});
heatmapHTML += '</div>';
document.getElementById('heatmap-container').innerHTML = heatmapHTML;

// Secció 5: Per etapa
new Chart(document.getElementById('perEtapa'), {
  type: 'bar',
  data: {
    labels: ['Primària', 'ESO', 'Batxillerat'],
    datasets: """ + etapa_datasets_json + """
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    scales: { y: { beginAtZero: true, max: 5, title: { display: true, text: 'Puntuació B (prompt complet)' } } },
    plugins: {
      title: { display: true, text: 'Qualitat per etapa educativa', font: { size: 14 } },
      legend: { position: 'top' }
    }
  }
});
</script>
</body>
</html>
"""

    return html


def main():
    data = load_data()
    if data is None or not data.get("avaluacions"):
        print("Sense dades suficients. Abortant.")
        return

    evals = data["avaluacions"]
    print(f"Carregades {len(evals)} avaluacions")

    metrics = compute_all_metrics(evals)
    print(f"Models: {metrics['models']}")
    print(f"Jutges: {metrics['jutges']}")

    html = generate_html(metrics, data)
    DASHBOARD_PATH.write_text(html, encoding="utf-8")
    print(f"\nDashboard generat: {DASHBOARD_PATH}")


if __name__ == "__main__":
    main()
