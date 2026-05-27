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

# Carrega .env per a GEMINI_API_KEY i altres
try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
except ImportError:
    pass  # python-dotenv no instal·lat → confiem en l'entorn extern

# Carrega test-token si existeix (per a /api/adapt amb auth Supabase)
_TEST_TOKEN_PATH = ROOT / "tests" / ".test-token"
TEST_TOKEN = None
if _TEST_TOKEN_PATH.exists():
    TEST_TOKEN = _TEST_TOKEN_PATH.read_text(encoding="utf-8").strip()

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
        "etapa": case["params"].get("etapa", "ESO"),
        "materia": "ciències naturals",
    }
    url = f"{server.rstrip('/')}{ADAPT_ENDPOINT}"
    headers = {}
    if TEST_TOKEN:
        headers["Authorization"] = f"Bearer {TEST_TOKEN}"
    t0 = time.time()
    resp = requests.post(url, json=payload, headers=headers, timeout=180, stream=True)
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


def call_adapt_direct(case: dict, text_body: str, text_id: str) -> dict:
    """Crida run_adaptation() directament (sense HTTP, sense auth).

    Útil per al harness Fase B en local — bypassa l'auth Supabase/LaNet
    cridant la lògica Python directament. Aquest és el mateix codi que
    executa /api/adapt internament.
    """
    from adaptation.orchestrator import run_adaptation
    events: list[dict] = []
    def cb(ev):
        events.append(ev)
    t0 = time.time()
    try:
        run_adaptation(
            text=text_body,
            profile=case["profile"],
            context={
                "etapa": case["params"].get("etapa", "ESO"),
                "materia": "ciències naturals",
            },
            params=case["params"],
            progress_callback=cb,
        )
        status = 200
    except Exception as e:
        events.append({"type": "error", "msg": f"{type(e).__name__}: {e}"})
        status = 500
    elapsed = time.time() - t0
    return {
        "case_id": case["id"],
        "text_id": text_id,
        "status_code": status,
        "elapsed_s": round(elapsed, 2),
        "events": events,
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

    # Concatena tots els 'delta' events per obtenir el text adaptat complet
    events_all = output.get("events", [])
    text_chunks = []
    complements_chunks = []
    for ev in events_all:
        if ev.get("type") == "delta" and ev.get("text"):
            text_chunks.append(ev["text"])
        elif ev.get("type") in ("complement", "complements", "complement_block"):
            complements_chunks.append(json.dumps(ev, ensure_ascii=False)[:500])
    adapted_text = "".join(text_chunks)[:8000] or "(sense text adaptat)"
    complements_summary = ("\n\n--- Complements detectats ---\n" + "\n".join(complements_chunks)[:2000]) if complements_chunks else ""
    output_str = f"### TEXT ADAPTAT:\n{adapted_text}{complements_summary}"

    return f"""Ets un **avaluador adversarial de qualitat pedagògica** d'un sistema
d'adaptació de textos educatius (ATNE) per a alumnat amb necessitats educatives
diverses (FJE — Fundació Jesuïtes Educació). La teva feina és identificar **on
falla** el sistema, NO on encerta.

# Context del cas
- ID: `{case['id']}`
- Descripció: {case['descripcio']}
- Perfil alumne: {json.dumps(case['profile']['caracteristiques'], ensure_ascii=False)}
- Nivell MECR demanat: **{case['params']['mecr_sortida']}**
- Nivell DUA: **{case['params']['dua']}**
- Gènere discursiu: **{case['params']['genere_discursiu']}**
- Complements demanats: {list((case['params'].get('complements') or {}).keys())}

# Text original (input al sistema)
```
{text_original}
```

# Output del sistema (events SSE finals de /api/adapt)
```
{output_str}
```

# Rúbrica d'avaluació
Aplica aquests 6 criteris amb l'escala 0-5:
{escala_block}

Criteris a avaluar:
{crit_block}

# Format estricte de resposta

Respon **NOMÉS JSON** (sense fence markdown, sense text introductori, sense
text al final). Per cada criteri:
- `score`: enter 0-5
- `comment`: 1-2 frases concretes (màx 200 caràcters)
- `evidence`: cita textual breu del text adaptat o complement on es veu el
  problema/encert. Si no pots citar, "no observable" (màx 200 caràcters).

Camp `summary` (NOU): 1 frase de 80-120 caràcters que sintetitzi el principal
problema (o "OK" si tot és correcte). Pensa-la com a headline llegible.

Camp `flags` (NOU): llista d'alertes greus (només si score ≤ 1 a algun criteri,
o si veus contradicció clara amb regles MALL/DUA/saber-ne+). Formats vàlids:
- "E0:<criteri>:<motiu curt>" (output buit/inservible)
- "E1:<criteri>:<motiu curt>" (defecte greu pedagògic)
- "REGLA:<MALL|DUA|LF|MATRIU>:<motiu curt>" (contradicció amb canon)

Estructura JSON:
{{
  "case_id": "{case['id']}",
  "summary": "...",
  "scores": {{
    "C1_adequacio_mecr":        {{"score": <0-5>, "comment": "...", "evidence": "..."}},
    "C2_perfil_aplicat":        {{"score": <0-5>, "comment": "...", "evidence": "..."}},
    "C3_complements_coherents": {{"score": <0-5>, "comment": "...", "evidence": "..."}},
    "C4_fidelitat_semantica":   {{"score": <0-5>, "comment": "...", "evidence": "..."}},
    "C5_estructura_genere":     {{"score": <0-5>, "comment": "...", "evidence": "..."}},
    "C6_legibilitat_lf":        {{"score": <0-5>, "comment": "...", "evidence": "..."}}
  }},
  "flags": ["..."]
}}

# Criteris de severitat
- **5** només si és impecable per al canon. **3** és "acceptable amb marge".
- Si el text adaptat té el mateix nivell MECR que l'original (no s'ha adaptat),
  baixa C1 i C2 a 1.
- Si un complement esperat (segons matriu saber-ne+ §7) no apareix a l'output,
  marca C3 ≤ 2 i afegeix flag REGLA:MATRIU.
- Si veus dades inventades (noms/dates/xifres) que no eren al text original,
  C4 = 0 i flag E1:C4.
- Si DUA=Accés però el text té punt i coma o exclamacions, C6 ≤ 2 i flag
  REGLA:LF.

Sigues estricte. La teva feina és protegir l'alumne real.
"""


def _judge_provider_for_model(model: str) -> str:
    """Auto-detecció del provider segons el nom del model."""
    m = (model or "").lower()
    if m.startswith("claude-") or "sonnet" in m or "opus" in m or "haiku" in m:
        return "anthropic"
    if m.startswith("gpt-") or m.startswith("o1"):
        return "openai"
    return "google"  # default per a gemini-*


def call_judge(prompt: str, model: str, api_key: str | None) -> dict:
    """Crida el judge LLM. Detecta provider automàticament del nom del model.

    Suportats:
    - Google (gemini-*): GEMINI_API_KEY
    - OpenAI (gpt-*, o1-*): OPENAI_API_KEY
    - Anthropic (claude-*, sonnet, opus, haiku): ANTHROPIC_API_KEY
    """
    provider = _judge_provider_for_model(model)

    if provider == "google":
        key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GEMMA4_API_KEY")
        if not key:
            raise RuntimeError("Falta GEMINI_API_KEY al .env")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
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

    if provider == "openai":
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            raise RuntimeError("Falta OPENAI_API_KEY al .env")
        url = "https://api.openai.com/v1/chat/completions"
        body = {
            "model": model,
            "temperature": JUDGE_TEMPERATURE,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": "Ets un avaluador adversarial. Retornes NOMÉS JSON estricte."},
                {"role": "user", "content": prompt},
            ],
        }
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        r = requests.post(url, json=body, headers=headers, timeout=120)
        r.raise_for_status()
        data = r.json()
        text = data["choices"][0]["message"]["content"]
        return json.loads(text)

    if provider == "anthropic":
        key = os.getenv("ANTHROPIC_API_KEY")
        if not key:
            raise RuntimeError("Falta ANTHROPIC_API_KEY al .env")
        url = "https://api.anthropic.com/v1/messages"
        body = {
            "model": model,
            "max_tokens": 4096,
            "temperature": JUDGE_TEMPERATURE,
            "messages": [{"role": "user", "content": prompt}],
        }
        headers = {
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
        r = requests.post(url, json=body, headers=headers, timeout=120)
        r.raise_for_status()
        data = r.json()
        text = data["content"][0]["text"]
        # Claude pot afegir text abans/després del JSON; intenta extreure el JSON principal
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end > start:
            text = text[start:end + 1]
        return json.loads(text)

    raise RuntimeError(f"Provider desconegut per al model: {model}")


def generate_outputs(cases: list[dict], texts: dict, args) -> None:
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    text_ids = [args.text] if args.text else list(texts["textos"].keys())
    target_cases = [c for c in cases if (not args.case or c["id"] == args.case)]

    for case in target_cases:
        for text_id in text_ids:
            text = texts["textos"][text_id]
            print(f"[generate] {case['id']} × {text_id} … ", end="", flush=True)
            try:
                if args.direct:
                    out = call_adapt_direct(case, text["text"], text_id)
                else:
                    out = call_adapt_http(args.server, case, text["text"], text_id)
                out_path = OUTPUTS_DIR / f"{case['id']}__{text_id}.json"
                out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
                print(f"OK ({out['elapsed_s']}s, {len(out['events'])} events, status={out.get('status_code','?')})")
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
            # Retry simple per a errors temporals (503/429)
            last_err = None
            judgment = None
            for attempt in range(3):
                try:
                    judgment = call_judge(prompt, args.judge_model, api_key)
                    break
                except Exception as e:
                    last_err = e
                    msg = str(e).lower()
                    if any(t in msg for t in ("503", "429", "timeout", "connection")):
                        time.sleep(5 * (attempt + 1))  # backoff: 5s, 10s, 15s
                        continue
                    break
            if judgment is None:
                print(f"ERROR: {last_err}")
                continue
            jud_path = JUDGMENTS_DIR / f"{case['id']}__{text_id}.json"
            jud_path.write_text(json.dumps(judgment, ensure_ascii=False, indent=2), encoding="utf-8")
            scores = judgment.get("scores", {})
            avg = sum(s.get("score", 0) for s in scores.values()) / max(len(scores), 1) if scores else 0
            print(f"OK score~{avg:.1f}")


def _score_icon(score: int | float | None) -> str:
    """Mapeja un score 0-5 a un emoji visual per al heatmap."""
    if score is None or score == "-":
        return "⬜"
    s = float(score)
    if s >= 4.5:
        return "🟢"
    if s >= 3.5:
        return "🟢"
    if s >= 2.5:
        return "🟡"
    if s >= 1.5:
        return "🟠"
    return "🔴"


def _criteri_label(cid: str) -> str:
    """ID -> etiqueta curta per a capçaleres."""
    return {
        "C1_adequacio_mecr":        "C1 MECR",
        "C2_perfil_aplicat":        "C2 Perfil",
        "C3_complements_coherents": "C3 Complem",
        "C4_fidelitat_semantica":   "C4 Fidelitat",
        "C5_estructura_genere":     "C5 Estruct",
        "C6_legibilitat_lf":        "C6 Llegib",
    }.get(cid, cid)


def aggregate(rubric: dict, args) -> None:
    """Llegeix tots els judgments i genera _phase_b_report.md amb visualització."""
    pesos = rubric.get("pesos", {})
    total_pes = sum(pesos.values()) or 1
    crit_ids = list(rubric.get("criteris", {}).keys())

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
            "text_id": jud_path.stem.split("__", 1)[1] if "__" in jud_path.stem else "?",
            "summary": j.get("summary", ""),
            "score_global": round(weighted, 2),
            "scores": {cid: s["score"] for cid, s in scores.items()},
            "comments": {cid: s.get("comment", "") for cid, s in scores.items()},
            "evidence": {cid: s.get("evidence", "") for cid, s in scores.items()},
            "flags": j.get("flags", []),
        })

    out = ["# 📊 Fase B · Informe LLM-as-Judge\n"]
    if not rows:
        out.append("Cap judgment desat encara. Executa `--full` o `--judge`.")
        md = "\n".join(out)
        print(md)
        (HERE / "_phase_b_report.md").write_text(md, encoding="utf-8")
        return

    # ── Resum executiu ──
    avg_global = sum(r["score_global"] for r in rows) / len(rows)
    n_crit = sum(1 for r in rows if r["score_global"] < 2.5)
    n_ok = sum(1 for r in rows if r["score_global"] >= 3.5)
    n_flags = sum(len(r["flags"]) for r in rows)
    out.append(f"_{len(rows)} judgments · model judge: `{args.judge_model}` · "
               f"score global mitjà: **{avg_global:.2f}/5**_\n")
    out.append("## 🎯 Resum executiu\n")
    out.append(f"| Casos | OK (≥3.5) | Crítics (<2.5) | Flags totals |")
    out.append(f"|-------|-----------|----------------|--------------|")
    out.append(f"| {len(rows)} | 🟢 {n_ok} | 🔴 {n_crit} | ⚠️ {n_flags} |\n")

    # ── Heatmap ──
    out.append("## 🌡️ Heatmap qualitat (criteri × cas)\n")
    out.append("Llegenda: 🟢 ≥3.5 · 🟡 2.5-3.4 · 🟠 1.5-2.4 · 🔴 <1.5 · ⬜ no avaluable\n")
    headers = ["Cas", "Global"] + [_criteri_label(c) for c in crit_ids]
    out.append("| " + " | ".join(headers) + " |")
    out.append("|" + "|".join(["---"] * len(headers)) + "|")
    for r in rows:
        scores_row = []
        for cid in crit_ids:
            sc = r["scores"].get(cid)
            scores_row.append(f"{_score_icon(sc)} {sc if sc is not None else '-'}")
        global_icon = _score_icon(r["score_global"])
        out.append(f"| `{r['case_id']}` | {global_icon} **{r['score_global']:.2f}** | "
                   + " | ".join(scores_row) + " |")

    # ── Mitjana per criteri ──
    out.append("\n## 📈 Mitjana per criteri\n")
    out.append("| Criteri | Mitjana | Pes (%) | Cas pitjor | Cas millor |")
    out.append("|---------|---------|---------|------------|------------|")
    for cid in crit_ids:
        vals = [(r["scores"].get(cid), r["case_id"]) for r in rows if r["scores"].get(cid) is not None]
        if not vals:
            continue
        avg = sum(v for v, _ in vals) / len(vals)
        worst = min(vals, key=lambda t: t[0])
        best = max(vals, key=lambda t: t[0])
        out.append(f"| {_criteri_label(cid)} | {_score_icon(avg)} **{avg:.2f}** | "
                   f"{pesos.get(cid, '-')} | `{worst[1]}` ({worst[0]}) | "
                   f"`{best[1]}` ({best[0]}) |")

    # ── Top flags ──
    flag_count: dict[str, int] = {}
    for r in rows:
        for f in r["flags"]:
            key = f.split(":", 2)[0] + ":" + (f.split(":", 2)[1] if ":" in f else "?")
            flag_count[key] = flag_count.get(key, 0) + 1
    if flag_count:
        out.append("\n## ⚠️ Top flags (categoria · freqüència)\n")
        out.append("| Categoria | Freqüència |")
        out.append("|-----------|------------|")
        for k, v in sorted(flag_count.items(), key=lambda kv: -kv[1]):
            out.append(f"| `{k}` | {v} |")

    # ── Casos crítics (detall) ──
    critics = [r for r in rows if r["score_global"] < 2.5]
    if critics:
        out.append("\n## 🔴 Casos crítics (score global < 2.5)\n")
        for r in critics:
            out.append(f"### `{r['case_id']}` — Global: **{r['score_global']:.2f}**")
            if r["summary"]:
                out.append(f"> {r['summary']}")
            out.append("")
            out.append("**Scores per criteri:**")
            for cid in crit_ids:
                sc = r["scores"].get(cid)
                cm = r["comments"].get(cid, "")
                ev = r["evidence"].get(cid, "")
                out.append(f"- {_criteri_label(cid)}: {_score_icon(sc)} **{sc}** — {cm}")
                if ev and ev != "no observable":
                    out.append(f"    - _Evidència:_ \"{ev[:200]}\"")
            if r["flags"]:
                out.append(f"\n**Flags:** {', '.join(r['flags'])}")
            out.append("")

    # ── Detall de tots els casos amb summary ──
    out.append("\n## 📝 Sumaris per cas\n")
    for r in rows:
        summary = r["summary"] or "—"
        out.append(f"- {_score_icon(r['score_global'])} `{r['case_id']}` "
                   f"(text: `{r['text_id']}`) → **{r['score_global']:.2f}** · {summary}")

    md = "\n".join(out)
    print(md)
    (HERE / "_phase_b_report.md").write_text(md, encoding="utf-8")
    print(f"\n[phase_b] Informe escrit a: {HERE / '_phase_b_report.md'}", file=sys.stderr)


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
