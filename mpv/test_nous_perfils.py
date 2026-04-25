# Test perfils nous + combinacions + grup a múltiples nivells
# Desa prompts i outputs. Execució: python mpv/test_nous_perfils.py
# Resultats: mpv/resultats/nous_TIMESTAMP/

import ctypes
import json
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

def _keep_awake(enable: bool):
    try:
        ES_CONTINUOUS      = 0x80000000
        ES_SYSTEM_REQUIRED = 0x00000001
        flag = (ES_CONTINUOUS | ES_SYSTEM_REQUIRED) if enable else ES_CONTINUOUS
        ctypes.windll.kernel32.SetThreadExecutionState(flag)
    except Exception:
        pass

env_path = Path(__file__).parent / ".env"
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

import requests

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).parent))

from server_mpv import build_system_prompt, resolve_nivell, _call_gemma

CREAM_URL = "http://localhost:8000/api/adapt"

# ── Textos ────────────────────────────────────────────────────────────────────

TEXT_B1 = """La fotosíntesi

La fotosíntesi és el procés bioquímic mitjançant el qual les plantes, les algues i alguns
microorganismes converteixen l'energia lluminosa en energia química emmagatzemada en glucosa.
Aquest procés es duu a terme als cloroplasts, orgànuls presents a les cèl·lules vegetals.

Durant la fotosíntesi, les plantes absorbeixen diòxid de carboni (CO₂) de l'atmosfera a través
dels estomes de les fulles, i capten l'aigua (H₂O) del sòl per les arrels. La clorofil·la,
el pigment verd dels cloroplasts, absorbeix l'energia solar i l'utilitza per sintetitzar glucosa.

La reacció global és:
6 CO₂ + 6 H₂O + llum solar → C₆H₁₂O₆ (glucosa) + 6 O₂ (oxigen)

La glucosa s'utilitza com a font d'energia per al metabolisme i el creixement de la planta,
mentre que l'oxigen s'allibera a l'atmosfera com a subproducte. La fotosíntesi és la base
de gairebé totes les cadenes tròfiques i la principal font d'oxigen atmosfèric del planeta."""

TEXT_B2 = """La Revolució Industrial

La Revolució Industrial, iniciada a la Gran Bretanya al darrer terç del segle XVIII, va suposar
una transformació radical dels sistemes de producció, substituint la manufactura artesanal per
la producció mecanitzada en fàbriques. L'aplicació de la màquina de vapor als processos
productius —primer en la indústria tèxtil i posteriorment en la siderúrgia i el transport—
va accelerar exponencialment la capacitat productiva de les societats occidentals.

Paral·lelament, es va produir un intens procés d'urbanització: la població rural emigrà en
masses cap a les ciutats industrials a la recerca de feina assalariada. Sorgí així un nou ordre
social polaritzat entre la burgesia industrial, propietària dels mitjans de producció, i el
proletariat, que venia la seva força de treball a canvi d'un salari. Les condicions laborals
eren sovint precàries: jornades de fins a catorze hores, treball infantil generalitzat i
absència de proteccions socials."""

# ── Casos ─────────────────────────────────────────────────────────────────────

# Format: (etiqueta, curs, adaptacio, perfils_mvp, perfils_cream, text)
CASOS = [
    # Nota: format CREAM correcte → {"caracteristiques": {clau: {"actiu": True, ...}}}

    # ── Perfils nous individuals ──────────────────────────────────────────────
    ("tdl_B1",          "eso_12",      "simplificat",  ["tdl"],
     {"caracteristiques": {"tdl": {"actiu": True}}},                TEXT_B1),

    ("di_B1",           "eso_12",      "simplificat",  ["di"],
     {"caracteristiques": {"discapacitat_intellectual": {"actiu": True}}}, TEXT_B1),

    ("aacc_B2",         "eso_34",      "al_nivell",    ["altes_capacitats"],
     {"caracteristiques": {"altes_capacitats": {"actiu": True}}},   TEXT_B2),

    # ── Combinacions de perfils ───────────────────────────────────────────────
    ("tdah_dislexia_B1","eso_12",      "simplificat",  ["tdah", "dislexia"],
     {"caracteristiques": {"tdah": {"actiu": True, "grau": "moderat"},
                           "dislexia": {"actiu": True}}},           TEXT_B1),

    ("tea_tdl_B1",      "eso_12",      "simplificat",  ["tea", "tdl"],
     {"caracteristiques": {"tea": {"actiu": True},
                           "tdl": {"actiu": True}}},                TEXT_B1),

    ("tdah_aacc_B2",    "eso_34",      "al_nivell",    ["tdah", "altes_capacitats"],
     {"caracteristiques": {"tdah": {"actiu": True, "grau": "moderat"},
                           "altes_capacitats": {"actiu": True}}},   TEXT_B2),

    # ── Perfils nous addicionals ──────────────────────────────────────────────
    ("vulnerabilitat_B1",      "eso_12", "simplificat", ["vulnerabilitat"],
     {"caracteristiques": {"vulnerabilitat": {"actiu": True}}},     TEXT_B1),

    ("trastorn_emocional_B1",  "eso_12", "simplificat", ["trastorn_emocional"],
     {"caracteristiques": {"trastorn_emocional": {"actiu": True}}}, TEXT_B1),

    ("vuln_nouvingut_B1",      "eso_12", "simplificat", ["vulnerabilitat", "nouvingut"],
     {"caracteristiques": {"vulnerabilitat": {"actiu": True},
                           "nouvingut": {"actiu": True, "mecr_entrada": "A1", "l1": ""}}}, TEXT_B1),

    # ── Grup sense perfils — 5 nivells incloent A1 ────────────────────────────
    ("grup_A1",  "primaria_12", "simplificat", [], {}, TEXT_B1),
    ("grup_A2",  "primaria_56", "simplificat", [], {}, TEXT_B1),
    ("grup_B1",  "eso_12",      "simplificat", [], {}, TEXT_B1),
    ("grup_B2",  "eso_34",      "al_nivell",   [], {}, TEXT_B2),
    ("grup_C1",  "batxillerat", "al_nivell",   [], {}, TEXT_B2),
]

MODELS = [
    ("gpt-4o",          "openai"),
    ("gpt-4.1-mini",    "openai"),
    ("gemma-4-31b-it",  "gemma"),
    ("gemma-3-27b-it",  "gemma"),
]

# ── Funcions ──────────────────────────────────────────────────────────────────

def call_openai(model: str, system_prompt: str, text: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY no configurada")
    resp = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": model, "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": text},
        ], "max_tokens": 4000, "temperature": 0.7},
        timeout=120,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"OpenAI: {resp.json().get('error',{}).get('message', resp.status_code)}")
    return resp.json()["choices"][0]["message"]["content"]


def call_cream_sse(model: str, profile: dict, mecr: str, text: str) -> str:
    resp = requests.post(
        CREAM_URL,
        json={"text": text, "profile": profile, "context": {},
              "params": {"mecr_sortida": mecr}, "model": model},
        timeout=180, stream=True, headers={"Accept": "text/event-stream"},
    )
    if resp.status_code != 200:
        raise RuntimeError(f"Cream HTTP {resp.status_code}")
    for raw in resp.iter_lines(decode_unicode=True):
        if not raw or not raw.startswith("data:"):
            continue
        try:
            ev = json.loads(raw[5:].strip())
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "result" and ev.get("adapted"):
            return ev["adapted"]
    raise RuntimeError("Cream: cap event 'result'")


# ── Execució ──────────────────────────────────────────────────────────────────

def run():
    _keep_awake(True)
    TS = time.strftime("%Y%m%d_%H%M%S")
    OUT = Path(__file__).parent / "resultats" / f"nous_{TS}"
    OUT.mkdir(parents=True, exist_ok=True)

    total = len(CASOS) * len(MODELS) * 2
    resum = []
    lock = threading.Lock()

    print(f"\n{'='*65}")
    print(f"  Test Perfils Nous + Combinacions — {TS}")
    print(f"  {len(CASOS)} casos × {len(MODELS)} models × MVP+CREAM = {total} crides")
    print(f"  Execució en paral·lel ({len(MODELS)} fils simultanis)")
    print(f"{'='*65}\n")

    def run_model(model_id: str, provider: str):
        local = []
        for tag, curs, adaptacio, perfils_mvp, perfils_cream, text in CASOS:
            nivell = resolve_nivell(curs, adaptacio)
            for versio in ("MVP", "CREAM"):
                t0 = time.time()
                try:
                    sp = ""
                    cream_payload_log = ""
                    if versio == "MVP":
                        sp = build_system_prompt(nivell, perfils_mvp, [])
                        result = call_openai(model_id, sp, text) if provider == "openai" \
                                 else _call_gemma(model_id, sp, text)
                    else:
                        cream_payload_log = json.dumps(
                            {"profile": perfils_cream, "params": {"mecr_sortida": nivell}},
                            ensure_ascii=False, indent=2
                        )
                        result = call_cream_sse(model_id, perfils_cream, nivell, text)

                    elapsed = round(time.time() - t0, 1)
                    with lock:
                        print(f"  {model_id:<16} {versio:<5} {tag:<28} OK {elapsed}s", flush=True)

                    safe = model_id.replace("-", "_").replace(".", "_")
                    fname = f"{tag}_{safe}_{versio}.md"
                    log_block = ""
                    if sp:
                        log_block = f"\n\n---\n\n<details><summary>Prompt MVP</summary>\n\n```\n{sp}\n```\n</details>\n"
                    elif cream_payload_log:
                        log_block = f"\n\n---\n\n<details><summary>Payload CREAM</summary>\n\n```json\n{cream_payload_log}\n```\n</details>\n"
                    (OUT / fname).write_text(
                        f"# {model_id} · {tag} · {versio}\n\n"
                        f"**Nivell:** {nivell} | **Curs:** {curs} | **Adaptació:** {adaptacio}\n"
                        f"**Perfils:** {perfils_mvp or 'cap (grup)'}\n\n"
                        f"---\n\n{result}{log_block}",
                        encoding="utf-8",
                    )
                    local.append({"tag": tag, "model": model_id, "versio": versio,
                                  "seg": elapsed, "ok": True, "nivell": nivell})

                except Exception as e:
                    elapsed = round(time.time() - t0, 1)
                    with lock:
                        print(f"  {model_id:<16} {versio:<5} {tag:<28} ERR {e}", flush=True)
                    local.append({"tag": tag, "model": model_id, "versio": versio,
                                  "seg": elapsed, "ok": False, "error": str(e), "nivell": nivell})
        return local

    with ThreadPoolExecutor(max_workers=len(MODELS)) as executor:
        futures = {executor.submit(run_model, mid, prov): mid for mid, prov in MODELS}
        for fut in as_completed(futures):
            try:
                resum.extend(fut.result())
            except Exception as e:
                print(f"  [FATAL] {futures[fut]}: {e}")

    # Reordena per l'ordre original (cas, model, versió)
    tag_order   = {c[0]: i for i, c in enumerate(CASOS)}
    model_order = {m[0]: i for i, m in enumerate(MODELS)}
    resum.sort(key=lambda r: (tag_order.get(r["tag"], 99),
                              model_order.get(r["model"], 99),
                              r["versio"]))

    ok_count = sum(1 for r in resum if r["ok"])
    print(f"\n{'='*65}")
    print(f"  RESUM: {ok_count}/{len(resum)} correctes  |  {OUT.name}")
    print(f"{'='*65}\n")

    lines = [
        f"# Test Perfils Nous — {TS}\n\n",
        f"**Resultat:** {ok_count}/{len(resum)} correctes\n\n",
        "| Cas | Nivell | Model | Versió | Temps | Estat |\n",
        "|-----|--------|-------|--------|-------|-------|\n",
    ]
    for r in resum:
        estat = "OK" if r["ok"] else f"ERR {r.get('error','')[:45]}"
        lines.append(f"| {r['tag']} | {r['nivell']} | {r['model']} | {r['versio']} | {r['seg']}s | {estat} |\n")
    (OUT / "INDEX.md").write_text("".join(lines), encoding="utf-8")

    _keep_awake(False)
    print("  [PC] Suspensió restaurada. Test completat.\n")


if __name__ == "__main__":
    run()
