# Comparativa MVP vs CREAM — 4 models × 3 perfils × 2 prompts
# Execució: python mpv/test_comparativa.py
# Resultats: mpv/resultats/

import json
import os
import sys
import time
from pathlib import Path

# Carrega .env del directori mpv/
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

import requests

# Afegim el root del projecte al path per importar els mòduls existents
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).parent))

from server_mpv import build_system_prompt, resolve_nivell, _call_gemma

# ── Configuració ──────────────────────────────────────────────────────────────

RESULTATS = Path(__file__).parent / "resultats"
RESULTATS.mkdir(exist_ok=True)
TS = time.strftime("%Y%m%d_%H%M%S")

TEXT_ORIGINAL = """La fotosíntesi

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

MODELS = [
    ("gpt-4o",          "openai"),
    ("gpt-4.1-mini",    "openai"),
    ("gemma-4-31b-it",  "gemma"),
    ("gemma-3-27b-it",  "gemma"),
]

PERFILS = [
    ("tdah",       []),
    ("tea",        []),
    ("nouvingut",  []),
]

# Curs + adaptació → B1
CURS      = "eso_12"
ADAPTACIO = "simplificat"

CREAM_URL = "http://localhost:8000/api/adapt"

# Mapping perfil → profile object per al Cream
# Format correcte: {"caracteristiques": {clau: {"actiu": True, ...}}}
CREAM_PROFILES = {
    "tdah":      {"caracteristiques": {"tdah":      {"actiu": True, "grau": "moderat"}}},
    "tea":       {"caracteristiques": {"tea":        {"actiu": True}}},
    "nouvingut": {"caracteristiques": {"nouvingut":  {"actiu": True, "mecr_entrada": "A1", "l1": ""}}},
}

# ── Funcions de crida ─────────────────────────────────────────────────────────

def call_openai(model: str, system_prompt: str, text: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY no configurada")
    payload: dict = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": text},
        ],
        "max_tokens": 4000,
    }
    if not model.startswith("o1"):
        payload["temperature"] = 0.7
    resp = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=120,
    )
    if resp.status_code != 200:
        detail = resp.json().get("error", {}).get("message", f"HTTP {resp.status_code}")
        raise RuntimeError(f"OpenAI: {detail}")
    return resp.json()["choices"][0]["message"]["content"]


def call_cream(model: str, perfil_key: str, mecr: str) -> str:
    profile = CREAM_PROFILES.get(perfil_key, {})
    payload = {
        "text":    TEXT_ORIGINAL,
        "profile": profile,
        "context": {},
        "params":  {"mecr_sortida": mecr},
        "model":   model,
    }
    try:
        resp = requests.post(
            CREAM_URL, json=payload, timeout=120, stream=True,
            headers={"Accept": "text/event-stream"},
        )
    except requests.ConnectionError:
        raise RuntimeError("Cream server no disponible (localhost:8080)")
    if resp.status_code != 200:
        raise RuntimeError(f"Cream HTTP {resp.status_code}")
    # Parseja l'SSE: busca l'event type=result que conté el text adaptat
    for raw_line in resp.iter_lines(decode_unicode=True):
        if not raw_line or not raw_line.startswith("data:"):
            continue
        json_str = raw_line[5:].strip()
        if not json_str:
            continue
        try:
            ev = json.loads(json_str)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "result":
            adapted = ev.get("adapted", "")
            if adapted:
                return adapted
    raise RuntimeError("Cream: cap event 'result' rebut")


# ── Test principal ─────────────────────────────────────────────────────────────

def run():
    nivell = resolve_nivell(CURS, ADAPTACIO)
    total  = len(MODELS) * len(PERFILS) * 2  # MVP + CREAM
    done   = 0
    errors = []
    resum  = []

    print(f"\n{'='*60}")
    print(f"  ATNE Comparativa MVP vs CREAM")
    print(f"  Nivell: {nivell} | Curs: {CURS} | Adaptació: {ADAPTACIO}")
    print(f"  Total crides previstes: {total}")
    print(f"{'='*60}\n")

    for model_id, provider in MODELS:
        for perfil_key, complements in PERFILS:
            for versio in ("MVP", "CREAM"):
                done += 1
                tag = f"[{done:02}/{total}] {model_id} · {perfil_key} · {versio}"
                print(f"{tag} ...", end=" ", flush=True)
                t0 = time.time()

                try:
                    if versio == "MVP":
                        system_prompt = build_system_prompt(nivell, [perfil_key], complements)
                        if provider == "openai":
                            result = call_openai(model_id, system_prompt, TEXT_ORIGINAL)
                        else:
                            result = _call_gemma(model_id, system_prompt, TEXT_ORIGINAL)
                    else:  # CREAM
                        result = call_cream(model_id, perfil_key, nivell)

                    elapsed = time.time() - t0
                    print(f"OK {elapsed:.1f}s")

                    # Desa fitxer
                    fname = f"{TS}_{model_id.replace('-','_')}_{perfil_key}_{versio}.md"
                    fpath = RESULTATS / fname
                    fpath.write_text(
                        f"# {model_id} · {perfil_key} · {versio}\n\n"
                        f"**Nivell:** {nivell} | **Curs:** {CURS} | **Adaptació:** {ADAPTACIO}\n\n"
                        f"---\n\n{result}\n",
                        encoding="utf-8"
                    )
                    resum.append({
                        "model": model_id, "perfil": perfil_key, "versio": versio,
                        "seg": round(elapsed, 1), "ok": True, "fitxer": fname,
                    })

                except Exception as e:
                    elapsed = time.time() - t0
                    print(f"ERR {e}")
                    errors.append(f"{tag}: {e}")
                    resum.append({
                        "model": model_id, "perfil": perfil_key, "versio": versio,
                        "seg": round(elapsed, 1), "ok": False, "error": str(e),
                    })

                time.sleep(0.5)  # pausa mínima entre crides

    # ── Resum final ───────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  RESUM: {sum(1 for r in resum if r['ok'])}/{len(resum)} correctes")
    if errors:
        print(f"  ERRORS ({len(errors)}):")
        for e in errors:
            print(f"    - {e}")
    print(f"  Resultats a: {RESULTATS}")
    print(f"{'='*60}\n")

    # Escriu índex
    idx = RESULTATS / f"{TS}_INDEX.md"
    lines = [
        f"# Comparativa ATNE {TS}\n",
        f"**Nivell:** {nivell} | **Curs:** {CURS} | **Adaptació:** {ADAPTACIO}\n\n",
        "| Model | Perfil | Versió | Temps | Estat | Fitxer |\n",
        "|-------|--------|--------|-------|-------|--------|\n",
    ]
    for r in resum:
        estat = "OK" if r["ok"] else f"ERR {r.get('error','')[:40]}"
        fitxer = f"[veure]({r.get('fitxer','')})" if r["ok"] else "—"
        lines.append(f"| {r['model']} | {r['perfil']} | {r['versio']} | {r['seg']}s | {estat} | {fitxer} |\n")
    idx.write_text("".join(lines), encoding="utf-8")
    print(f"  Índex: {idx.name}\n")


if __name__ == "__main__":
    run()
