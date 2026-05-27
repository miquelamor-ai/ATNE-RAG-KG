"""
tests/golden/run_phase_b.py — Harness Fase B (LLM-as-Judge).

Què fa (TENS COST en LLM):
  1) Per cada cas de cases.yaml + cada text de golden_texts.yaml:
     a) Crida `/api/adapt` (servidor ATNE up) o `generar_stream` directe
        per obtenir el text adaptat + complements.
     b) Desa output a tests/golden/outputs/{case_id}__{text_id}.json
  2) Per cada output, demana al judge LLM (Gemini Flash) que apliqui
     judge_rubric.yaml. Desa judgment a tests/golden/judgments/{case_id}__{text_id}.json.
  3) Aggrega tots els judgments i genera _phase_b_report.md amb:
     - Resum global (score mitjà ponderat per pesos de la rúbrica).
     - Heatmap criteris × casos.
     - Llistat de flags (alertes greus E0/E1).
     - Top problemes pedagògics detectats.

Costos estimats (Gemini 2.5 Flash, ~3000 tokens per crida):
  - Adapt (LLM principal): 15 crides × ~0.001 € = ~0.015 €
  - Judge: 15 crides × ~0.001 € = ~0.015 €
  - **TOTAL primera passada: ~0.03 €** (negligible)
  Si es passessin tots els 24 gèneres × 12 condicions = 288 casos, ~0.60 €.

Execució:
  python tests/golden/run_phase_b.py --plan          # mostra pla, NO executa
  python tests/golden/run_phase_b.py --generate      # només genera adaptacions
  python tests/golden/run_phase_b.py --judge         # només judge sobre outputs ja generats
  python tests/golden/run_phase_b.py --full          # generate + judge + aggregate
  python tests/golden/run_phase_b.py --case C01_tea_b1_noticia --full   # un sol cas

Requereix:
  - .env amb GEMINI_API_KEY i opcionalment OPENAI_API_KEY
  - Servidor ATNE up a http://localhost:8000 si s'usa el mode HTTP (default)
  - O bé `--direct` per cridar les funcions Python directament (sense HTTP)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

# Configuració de paths
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

# UTF-8 a stdout (Windows cp1252)
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

try:
    import yaml
    import requests
except ImportError as e:
    print(f"ERROR: cal instal·lar {e.name}. pip install pyyaml requests")
    sys.exit(2)

# ─────────────────────────────────────────────────────────────────────────────
# Paths i constants
# ─────────────────────────────────────────────────────────────────────────────

HERE = Path(__file__).parent
OUTPUTS_DIR = HERE / "outputs"
JUDGMENTS_DIR = HERE / "judgments"
SERVER_DEFAULT = "http://localhost:8000"
ADAPT_ENDPOINT = "/api/adapt"

# Model judge (sobreescriptible amb --judge-model)
JUDGE_MODEL_DEFAULT = "gemini-2.5-flash"
JUDGE_TEMPERATURE = 0.0


# ─────────────────────────────────────────────────────────────────────────────
# Funcions
# ─────────────────────────────────────────────────────────────────────────────

def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def plan(cases: list[dict], texts: dict, args) -> None:
    """Mostra què s'executarà i quant costarà aproximadament. NO executa."""
    text_ids = list(texts["textos"].keys())
    n_cases = len(cases) if not args.case else 1
    n_texts = len(text_ids) if not args.text else 1
    total_combos = n_cases * n_texts

    print("=" * 70)
    print("PLA D'EXECUCIÓ — Fase B (NO s'ha executat res encara)")
    print("=" * 70)
    print(f"\nCasos a executar:       {n_cases}")
    print(f"Textos font:            {n_texts}")
    print(f"Total combinacions:     {total_combos}")
    print(f"\nCrides previstes:")
    print(f"  - LLM adaptador:  {total_combos}  (1 per combo)")
    print(f"  - LLM judge:      {total_combos}  (1 per combo)")
    print(f"  - TOTAL:          {total_combos * 2}")
    print(f"\nCost estimat (Gemini Flash, ~3000 tokens/crida):")
    cost_eur = total_combos * 2 * 0.001
    print(f"  ~{cost_eur:.3f} € (rang real: {cost_eur*0.5:.3f}–{cost_eur*2:.3f} €)")
    print(f"\nServidor ATNE:          {args.server} (mode {'directe' if args.direct else 'HTTP'})")
    print(f"Model judge:            {args.judge_model}")
    print(f"\nOutputs es desaran a:   {OUTPUTS_DIR}")
    print(f"Judgments es desaran a: {JUDGMENTS_DIR}")
    print(f"\nPer executar:")
    print(f"  python tests/golden/run_phase_b.py --full")
    print()


def call_adapt_http(server: str, case: dict, text_body: str, text_id: str) -> dict:
    """Crida /api/adapt via HTTP. Retorna dict amb output i metadades."""
    payload = {
        "profile": case["profile"],
        "params": case["params"],
        "text": text_body,
        # Camps que el backend pot exigir:
        "etapa": case["params"].get("etapa", "ESO"),
        "materia": "ciències naturals",
    }
    url = f"{server.rstrip('/')}{ADAPT_ENDPOINT}"
    t0 = time.time()
    resp = requests.post(url, json=payload, timeout=180, stream=True)
    chunks = []
    for line in resp.iter_lines(decode_unicode=True):
        if line and line.startswith("data:"):
            try:
                evt = json.loads(line[5:].strip())
                chunks.append(evt)
            except Exception:
                pass
    elapsed = time.time() - t0
    return {
        "case_id": case["id"],
        "text_id": text_id,
        "status_code": resp.status_code,
        "elapsed_s": round(elapsed, 2),
        "events": chunks,
    }


def build_judge_prompt(case: dict, text_original: str, output: dict, rubric: dict) -> str:
    """Construeix el prompt per al judge LLM. Retorna text complet."""
    criteris = rubric["criteris"]
    crit_descs = []
    for cid, c in criteris.items():
        pautes = c.get("pautes", []) or c.get("pautes_core_enriquiment", [])
        pautes_txt = "\n".join(f"      - {p}" for p in pautes)
        crit_descs.append(
            f"   {cid}: {c['titol']}\n"
            f"      Pregunta: {c['pregunta_judge'].strip()}\n"
            f"      Pautes:\n{pautes_txt}"
        )
    crit_block = "\n\n".join(crit_descs)

    escala_block = "\n".join(f"   {k}: {v}" for k, v in rubric["escala"].items())

    output_str = json.dumps(output.get("events", [])[-3:], ensure_ascii=False, indent=2)[:6000]

    return f"""Ets un **avaluador adversarial de qualitat pedagògica** d'un sistema
d'adaptació de textos educatius per a alumnat amb necessitats educatives diverses.
La teva feina és identificar **on falla** el sistema, no on encerta.

# Cas avaluat
- ID: {case['id']}
- Descripció: {case['descripcio']}
- Perfil: {json.dumps(case['profile']['caracteristiques'], ensure_ascii=False)}
- Params: MECR={case['params']['mecr_sortida']}, DUA={case['params']['dua']}, gènere={case['params']['genere_discursiu']}
- Complements demanats: {list((case['params'].get('complements') or {}).keys())}

# Text original
{text_original}

# Output del sistema (últimes events SSE de /api/adapt)
{output_str}

# Rúbrica
Aplica aquests 6 criteris amb l'escala 0-5 següent:
{escala_block}

Criteris a avaluar:
{crit_block}

# Format de resposta (JSON estricte, NOMÉS JSON, sense markdown)
{{
  "case_id": "{case['id']}",
  "scores": {{
    "C1_adequacio_mecr":       {{"score": <0-5>, "comment": "...", "evidence": "..."}},
    "C2_perfil_aplicat":       {{"score": <0-5>, "comment": "...", "evidence": "..."}},
    "C3_complements_coherents":{{"score": <0-5>, "comment": "...", "evidence": "..."}},
    "C4_fidelitat_semantica":  {{"score": <0-5>, "comment": "...", "evidence": "..."}},
    "C5_estructura_genere":    {{"score": <0-5>, "comment": "...", "evidence": "..."}},
    "C6_legibilitat_lf":       {{"score": <0-5>, "comment": "...", "evidence": "..."}}
  }},
  "flags": ["..."]
}}

Sigues estricte. 5 només si és impecable per al canon. 3 és "acceptable amb marge". Si veus una contradicció amb les regles MALL/DUA, afegeix-la a flags.
"""


def call_judge(prompt: str, model: str, api_key: str | None) -> dict:
    """Crida el judge LLM. Implementació mínima per a Gemini Flash via REST."""
    if not api_key:
        raise RuntimeError("Falta GEMINI_API_KEY al .env")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": JUDGE_TEMPERATURE,
            "responseMimeType": "application/json",
        },
    }
    r = requests.post(url, json=body, timeout=120)
    r.raise_for_status()
    data = r.json()
    text = data["candidates"][0]["content"]["parts"][0]["text"]
    return json.loads(text)


def generate_outputs(cases: list[dict], texts: dict, args) -> None:
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    text_ids = [args.text] if args.text else list(texts["textos"].keys())
    target_cases = [c for c in cases if (not args.case or c["id"] == args.case)]

    for case in target_cases:
        for text_id in text_ids:
            text = texts["textos"][text_id]
            print(f"[generate] {case['id']} × {text_id} … ", end="", flush=True)
            try:
                out = call_adapt_http(args.server, case, text["text"], text_id)
                out_path = OUTPUTS_DIR / f"{case['id']}__{text_id}.json"
                out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
                print(f"OK ({out['elapsed_s']}s, {len(out['events'])} events)")
            except Exception as e:
                print(f"ERROR: {e}")


def judge_outputs(cases: list[dict], texts: dict, rubric: dict, args) -> None:
    JUDGMENTS_DIR.mkdir(parents=True, exist_ok=True)
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GEMMA4_API_KEY")
    target_cases = [c for c in cases if (not args.case or c["id"] == args.case)]
    text_ids = [args.text] if args.text else list(texts["textos"].keys())

    for case in target_cases:
        for text_id in text_ids:
            out_path = OUTPUTS_DIR / f"{case['id']}__{text_id}.json"
            if not out_path.exists():
                print(f"[judge] SKIP {case['id']}__{text_id}: no output desat")
                continue
            output = json.loads(out_path.read_text(encoding="utf-8"))
            text_body = texts["textos"][text_id]["text"]
            prompt = build_judge_prompt(case, text_body, output, rubric)
            print(f"[judge] {case['id']} × {text_id} … ", end="", flush=True)
            try:
                judgment = call_judge(prompt, args.judge_model, api_key)
                jud_path = JUDGMENTS_DIR / f"{case['id']}__{text_id}.json"
                jud_path.write_text(json.dumps(judgment, ensure_ascii=False, indent=2), encoding="utf-8")
                scores = judgment.get("scores", {})
                avg = sum(s["score"] for s in scores.values()) / max(len(scores), 1)
                print(f"OK score~{avg:.1f}")
            except Exception as e:
                print(f"ERROR: {e}")


def aggregate(rubric: dict, args) -> None:
    """Llegeix tots els judgments i genera _phase_b_report.md"""
    pesos = rubric.get("pesos", {})
    total_pes = sum(pesos.values()) or 1
    rows = []
    for jud_path in sorted(JUDGMENTS_DIR.glob("*.json")):
        try:
            j = json.loads(jud_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        scores = j.get("scores", {})
        if not scores:
            continue
        weighted = sum(s["score"] * pesos.get(cid, 0) for cid, s in scores.items()) / total_pes
        rows.append({
            "id": jud_path.stem,
            "case_id": j.get("case_id", "?"),
            "score_global": round(weighted, 2),
            "scores": {cid: s["score"] for cid, s in scores.items()},
            "flags": j.get("flags", []),
        })

    out = ["# Fase B · Informe LLM-as-Judge\n"]
    if not rows:
        out.append("Cap judgment desat encara. Executa `--full` o `--judge`.")
    else:
        out.append(f"_{len(rows)} judgments avaluats · model judge: {args.judge_model}_\n")
        out.append("| Cas | Global | C1 | C2 | C3 | C4 | C5 | C6 | Flags |")
        out.append("|-----|--------|----|----|----|----|----|----|-------|")
        for r in rows:
            s = r["scores"]
            flag = ", ".join(r["flags"][:2]) if r["flags"] else "—"
            out.append(
                f"| `{r['case_id']}` | **{r['score_global']:.2f}** | "
                f"{s.get('C1_adequacio_mecr','-')} | {s.get('C2_perfil_aplicat','-')} | "
                f"{s.get('C3_complements_coherents','-')} | {s.get('C4_fidelitat_semantica','-')} | "
                f"{s.get('C5_estructura_genere','-')} | {s.get('C6_legibilitat_lf','-')} | {flag} |"
            )

    md = "\n".join(out)
    print(md)
    (HERE / "_phase_b_report.md").write_text(md, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Golden harness Fase B (LLM-as-Judge)")
    parser.add_argument("--plan", action="store_true", help="Mostra pla d'execució (no executa)")
    parser.add_argument("--generate", action="store_true", help="Només generar adaptacions (cost)")
    parser.add_argument("--judge", action="store_true", help="Només judge (cost)")
    parser.add_argument("--full", action="store_true", help="generate + judge + aggregate")
    parser.add_argument("--aggregate", action="store_true", help="Només recalcular report")
    parser.add_argument("--case", help="Filtra un sol cas")
    parser.add_argument("--text", help="Filtra un sol text font")
    parser.add_argument("--server", default=SERVER_DEFAULT, help="URL del servidor ATNE")
    parser.add_argument("--direct", action="store_true", help="(reservat) cridar funcions Python directament")
    parser.add_argument("--judge-model", default=JUDGE_MODEL_DEFAULT, help="Model del judge")
    args = parser.parse_args()

    if not any([args.plan, args.generate, args.judge, args.full, args.aggregate]):
        # Per defecte: pla
        args.plan = True

    cases_file = load_yaml(HERE / "cases.yaml")
    texts = load_yaml(HERE / "golden_texts.yaml")
    rubric = load_yaml(HERE / "judge_rubric.yaml")
    cases = cases_file["casos"]

    if args.plan:
        plan(cases, texts, args)
        return
    if args.full or args.generate:
        generate_outputs(cases, texts, args)
    if args.full or args.judge:
        judge_outputs(cases, texts, rubric, args)
    if args.full or args.aggregate:
        aggregate(rubric, args)


if __name__ == "__main__":
    main()
