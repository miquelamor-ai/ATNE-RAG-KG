# Test exhaustiu ATNE — MVP vs CREAM
# 3 avaluacions × múltiples perfils × complements × models × N repeticions
# Execució autònoma: python mpv/test_complet.py [--repeticions N]
# Resultats: mpv/resultats/complet_TIMESTAMP/

import argparse
import ctypes
import json
import os
import statistics
import sys
import time
from pathlib import Path

# Impedeix la suspensió del PC mentre el test corre (no requereix admin).
# SetThreadExecutionState és una crida Win32 disponible sense privilegis.
def _keep_awake(enable: bool):
    try:
        ES_CONTINUOUS      = 0x80000000
        ES_SYSTEM_REQUIRED = 0x00000001
        flag = (ES_CONTINUOUS | ES_SYSTEM_REQUIRED) if enable else ES_CONTINUOUS
        ctypes.windll.kernel32.SetThreadExecutionState(flag)
    except Exception:
        pass

# Carrega .env del directori mpv/
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

# ── Textos originals per nivell ───────────────────────────────────────────────

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
absència de proteccions socials.

Aquesta reconfiguració econòmica i social va generar profundes tensions que cristal·litzaren
en els moviments obrers del segle XIX, precursors del sindicalisme modern i de les primeres
legislacions laborals."""

TEXT_C1 = """El problema de la consciència i el dualisme ment-cos

La filosofia de la ment enfronta un dels enigmes més persistents del pensament occidental:
la relació entre els estats mentals —creences, desitjos, percepcions, emocions— i els processos
físics del cervell. El dualisme cartesià postulava l'existència de dues substàncies radicalment
heterogènies: la res cogitans (substància pensant, immaterial) i la res extensa (substància
corporal, espacialment extensa). Aquesta separació ontològica, tot i respondre a intuïcions
fenomenològiques poderoses, genera el problema de la interacció causal: com pot allò immaterial
incidir causalment sobre allò material?

El fisicalisme contemporani intenta resoldre aquesta tensió reduint els estats mentals a
estats cerebrals, ja sigui mitjançant la teoria de la identitat tipus (type identity theory)
—que identifica categories mentals amb categories neuronals— o mitjançant el funcionalisme,
que defineix els estats mentals per les seves relacions causals funcionals, independentment
del substrat físic que els realitzi.

No obstant, el problema difícil de la consciència (Chalmers, 1995) assenyala que cap explicació
funcional o neurocientífica no sembla poder donar compte de l'aspecte qualitatiu de l'experiència
subjectiva —el que s'anomena qualia: el «com és» ser un subjecte que percep el vermell,
experimenta el dolor o escolta una melodia."""

# ── Definicions de les avaluacions ───────────────────────────────────────────

AVALUACIONS = [
    {
        "id": "A",
        "nom": "ESO 1-2 · B1 · Fotosíntesi",
        "curs": "eso_12",
        "adaptacio": "simplificat",
        "text": TEXT_B1,
        "models": ["gpt-4o", "gpt-4.1-mini", "gemma-4-31b-it"],
        "casos": [
            {"tag": "grup",           "perfils_mvp": [],          "perfils_cream": {},
             "comp_mvp": [],           "comp_cream": {}},
            {"tag": "tdah",           "perfils_mvp": ["tdah"],
             "perfils_cream": {"caracteristiques": {"tdah": {"actiu": True, "grau": "moderat"}}},
             "comp_mvp": [],           "comp_cream": {}},
            {"tag": "tea",            "perfils_mvp": ["tea"],
             "perfils_cream": {"caracteristiques": {"tea": {"actiu": True}}},
             "comp_mvp": [],           "comp_cream": {}},
            {"tag": "nouvingut",      "perfils_mvp": ["nouvingut"],
             "perfils_cream": {"caracteristiques": {"nouvingut": {"actiu": True, "mecr_entrada": "A1", "l1": ""}}},
             "comp_mvp": [],           "comp_cream": {}},
            {"tag": "tdah_glossari",  "perfils_mvp": ["tdah"],
             "perfils_cream": {"caracteristiques": {"tdah": {"actiu": True, "grau": "moderat"}}},
             "comp_mvp": ["glossari"], "comp_cream": {"glossari": True}},
            {"tag": "tdah_preguntes", "perfils_mvp": ["tdah"],
             "perfils_cream": {"caracteristiques": {"tdah": {"actiu": True, "grau": "moderat"}}},
             "comp_mvp": ["preguntes"], "comp_cream": {"preguntes_comprensio": True}},
        ],
    },
    {
        "id": "B",
        "nom": "ESO 3-4 · B2 · Revolució Industrial",
        "curs": "eso_34",
        "adaptacio": "al_nivell",
        "text": TEXT_B2,
        "models": ["gpt-4o", "gpt-4.1-mini"],
        "casos": [
            {"tag": "grup",              "perfils_mvp": [],           "perfils_cream": {},
             "comp_mvp": [],           "comp_cream": {}},
            {"tag": "tdah",              "perfils_mvp": ["tdah"],
             "perfils_cream": {"caracteristiques": {"tdah": {"actiu": True, "grau": "moderat"}}},
             "comp_mvp": [],           "comp_cream": {}},
            {"tag": "dislexia",          "perfils_mvp": ["dislexia"],
             "perfils_cream": {"caracteristiques": {"dislexia": {"actiu": True}}},
             "comp_mvp": [],           "comp_cream": {}},
            {"tag": "dislexia_glossari", "perfils_mvp": ["dislexia"],
             "perfils_cream": {"caracteristiques": {"dislexia": {"actiu": True}}},
             "comp_mvp": ["glossari"], "comp_cream": {"glossari": True}},
        ],
    },
    {
        "id": "C",
        "nom": "Batxillerat · C1 · Filosofia ment",
        "curs": "batxillerat",
        "adaptacio": "al_nivell",
        "text": TEXT_C1,
        "models": ["gpt-4o", "gpt-4.1-mini"],
        "casos": [
            {"tag": "grup",           "perfils_mvp": [],           "perfils_cream": {},
             "comp_mvp": [],           "comp_cream": {}},
            {"tag": "dislexia",       "perfils_mvp": ["dislexia"],
             "perfils_cream": {"caracteristiques": {"dislexia": {"actiu": True}}},
             "comp_mvp": [],           "comp_cream": {}},
            {"tag": "tdah_preguntes", "perfils_mvp": ["tdah"],
             "perfils_cream": {"caracteristiques": {"tdah": {"actiu": True, "grau": "moderat"}}},
             "comp_mvp": ["preguntes"], "comp_cream": {"preguntes_comprensio": True}},
        ],
    },
]

# ── Funcions de crida ─────────────────────────────────────────────────────────

def call_openai(model: str, system_prompt: str, text: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY no configurada")
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": text},
        ],
        "max_tokens": 4000,
        "temperature": 0.7,
    }
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


def call_cream_sse(model: str, profile: dict, mecr: str, complements: dict, text: str) -> str:
    payload = {
        "text":    text,
        "profile": profile,
        "context": {},
        "params":  {"mecr_sortida": mecr, "complements": complements},
        "model":   model,
    }
    resp = requests.post(
        CREAM_URL, json=payload, timeout=180, stream=True,
        headers={"Accept": "text/event-stream"},
    )
    if resp.status_code != 200:
        raise RuntimeError(f"Cream HTTP {resp.status_code}")
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


# ── Execució ──────────────────────────────────────────────────────────────────

def run(repeticions: int = 1):
    _keep_awake(True)
    print(f"  [PC] Suspensió bloquejada mentre duri el test.")

    TS = time.strftime("%Y%m%d_%H%M%S")
    OUT = Path(__file__).parent / "resultats" / f"complet_{TS}"
    OUT.mkdir(parents=True, exist_ok=True)

    crides_per_rep = sum(len(av["models"]) * len(av["casos"]) * 2 for av in AVALUACIONS)
    total = crides_per_rep * repeticions
    done = 0
    resum = []   # llista de dicts per construir l'índex i estadística
    errors = []

    print(f"\n{'='*65}")
    print(f"  ATNE Test Complet — {TS}")
    print(f"  Repeticions: {repeticions}  |  Total crides: {total}")
    print(f"  Resultats: {OUT.name}")
    print(f"{'='*65}\n")

    for rep in range(1, repeticions + 1):
        if repeticions > 1:
            print(f"\n{'─'*65}")
            print(f"  REPETICIÓ {rep}/{repeticions}")
            print(f"{'─'*65}")

        for av in AVALUACIONS:
            nivell = resolve_nivell(av["curs"], av["adaptacio"])
            print(f"\n── Av {av['id']}: {av['nom']} [{nivell}] ──")

            for model_id in av["models"]:
                provider = "gemma" if "gemma" in model_id else "openai"

                for cas in av["casos"]:
                    tag = cas["tag"]

                    for versio in ("MVP", "CREAM"):
                        done += 1
                        rep_tag = f"r{rep}" if repeticions > 1 else ""
                        label = f"[{done:03}/{total}] {av['id']} | {model_id:<18} | {tag:<20} | {versio}{(' '+rep_tag) if rep_tag else ''}"
                        print(f"{label} ...", end=" ", flush=True)
                        t0 = time.time()

                        try:
                            sp = ""
                            if versio == "MVP":
                                sp = build_system_prompt(nivell, cas["perfils_mvp"], cas["comp_mvp"])
                                if provider == "openai":
                                    result = call_openai(model_id, sp, av["text"])
                                else:
                                    result = _call_gemma(model_id, sp, av["text"])
                            else:
                                result = call_cream_sse(
                                    model_id, cas["perfils_cream"], nivell,
                                    cas["comp_cream"], av["text"]
                                )

                            elapsed = round(time.time() - t0, 1)
                            print(f"OK {elapsed}s")

                            safe_model = model_id.replace("-", "_").replace(".", "_")
                            r_suffix = f"_r{rep}" if repeticions > 1 else ""
                            fname = f"{av['id']}_{safe_model}_{tag}_{versio}{r_suffix}.md"
                            prompt_block = (
                                f"\n\n---\n\n<details><summary>Prompt enviat</summary>\n\n```\n{sp}\n```\n</details>\n"
                                if sp else ""
                            )
                            (OUT / fname).write_text(
                                f"# {model_id} · {av['id']} · {tag} · {versio}{(' · rep'+str(rep)) if repeticions>1 else ''}\n\n"
                                f"**Nivell:** {nivell} | **Curs:** {av['curs']} | **Adaptació:** {av['adaptacio']}\n"
                                f"**Perfils:** {cas['perfils_mvp'] or 'cap'} | **Complements:** {cas['comp_mvp'] or 'cap'}\n\n"
                                f"---\n\n{result}{prompt_block}",
                                encoding="utf-8"
                            )
                            resum.append({
                                "av": av["id"], "model": model_id, "tag": tag,
                                "versio": versio, "rep": rep, "seg": elapsed,
                                "ok": True, "fname": fname,
                                "words": len(result.split()),
                            })

                        except Exception as e:
                            elapsed = round(time.time() - t0, 1)
                            print(f"ERR {e}")
                            errors.append(f"{label}: {e}")
                            resum.append({
                                "av": av["id"], "model": model_id, "tag": tag,
                                "versio": versio, "rep": rep, "seg": elapsed,
                                "ok": False, "error": str(e),
                            })

                        time.sleep(0.4)

    # ── Estadística per combinació (si repeticions > 1) ───────────────────────
    stats_lines = []
    if repeticions > 1:
        from collections import defaultdict
        groups: dict = defaultdict(list)
        for r in resum:
            if r["ok"]:
                key = (r["av"], r["model"], r["tag"], r["versio"])
                groups[key].append(r["words"])

        stats_lines = [
            "\n## Estadística paraules per combinació\n\n",
            "| Av | Model | Cas | Versió | Mitjana | Desv.Est | Min | Max |\n",
            "|----|-------|-----|--------|---------|----------|-----|-----|\n",
        ]
        for (av_id, model, tag, versio), vals in sorted(groups.items()):
            if len(vals) > 1:
                mean = round(statistics.mean(vals), 1)
                stdev = round(statistics.stdev(vals), 1)
            else:
                mean = vals[0]
                stdev = 0.0
            stats_lines.append(
                f"| {av_id} | {model} | {tag} | {versio} | {mean} | {stdev} | {min(vals)} | {max(vals)} |\n"
            )

    # ── Índex final ───────────────────────────────────────────────────────────
    ok_count = sum(1 for r in resum if r["ok"])
    print(f"\n{'='*65}")
    print(f"  RESUM: {ok_count}/{len(resum)} correctes")
    if errors:
        print(f"  ERRORS ({len(errors)}):")
        for e in errors[:10]:
            print(f"    - {e}")
    print(f"  Resultats a: {OUT}")
    print(f"{'='*65}\n")

    lines = [
        f"# Test Complet ATNE — {TS}\n\n",
        f"**Repeticions:** {repeticions} | **Resultat:** {ok_count}/{len(resum)} correctes\n\n",
        "| Av | Model | Cas | Versió | Rep | Paraules | Temps | Estat |\n",
        "|----|-------|-----|--------|-----|----------|-------|-------|\n",
    ]
    for r in resum:
        estat = "OK" if r["ok"] else f"ERR {r.get('error','')[:40]}"
        words = r.get("words", "—")
        lines.append(
            f"| {r['av']} | {r['model']} | {r['tag']} | {r['versio']} | {r['rep']} | {words} | {r['seg']}s | {estat} |\n"
        )
    lines += stats_lines

    (OUT / "INDEX.md").write_text("".join(lines), encoding="utf-8")
    print(f"  Índex: {OUT / 'INDEX.md'}\n")
    _keep_awake(False)
    print("  [PC] Suspensió restaurada. Test completat.\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test exhaustiu ATNE MVP vs CREAM")
    parser.add_argument("--repeticions", type=int, default=1,
                        help="Nombre de mostres per combinació (default: 1)")
    args = parser.parse_args()
    run(repeticions=args.repeticions)
