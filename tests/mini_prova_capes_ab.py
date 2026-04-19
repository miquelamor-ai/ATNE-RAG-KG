"""Mini prova A/B de capes del prompt ATNE.

No és experiment estadístic — és smoke test per veure primera impressió
qualitativa de com 3 variants del system prompt es comporten amb 3 perfils,
2 textos i 2 models (Gemma 3 27B vs GPT-4.1-mini).

Variants:
- V1 = identitat + DUA + gènere + persona-audience (SENSE catàleg)
- V2 = identitat + instruccions filtrades per MECR + gènere (SENSE DUA ni persona)
- V3 = baseline complet (build_system_prompt)

Executa: python tests/mini_prova_capes_ab.py
Sortida: tests/mini_prova_capes_resultats.md

NO executa res al servidor — construeix prompts manualment i fa crides
directes via els SDK (google-genai per a Gemma i openai per a GPT).
"""

from __future__ import annotations

import os
import sys
import time
import traceback
from pathlib import Path
from datetime import datetime

# Afegir el directori arrel del repo al sys.path perquè els imports funcionin
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Carregar variables d'entorn abans de res
from dotenv import load_dotenv  # noqa: E402
load_dotenv(ROOT / ".env")

import corpus_reader  # noqa: E402
import instruction_filter  # noqa: E402
import instruction_catalog  # noqa: E402
import server  # noqa: E402

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓ
# ═══════════════════════════════════════════════════════════════════════════

GEMMA_MODEL = "gemma-3-27b-it"
GPT_MODEL = "gpt-4.1-mini"

TEXT_A = """L'aigua del planeta es troba en un moviment constant que anomenem cicle hidrològic. Aquest procés comença amb l'evaporació: el Sol escalfa l'aigua dels oceans, rius i llacs, i la transforma en vapor que ascendeix a l'atmosfera. A mesura que el vapor s'eleva, es refreda i condensa formant petites gotes que constitueixen els núvols. Quan aquestes gotes esdevenen prou pesades, precipiten en forma de pluja, neu o calamarsa. Una part de l'aigua precipitada s'infiltra al subsòl i alimenta els aqüífers; una altra part circula per la superfície en forma de rius que, finalment, retornen al mar. Els éssers vius també participen en aquest cicle mitjançant la transpiració: les plantes absorbeixen aigua del sòl i n'alliberen part a l'atmosfera a través de les fulles. Sense aquest cicle, la vida tal com la coneixem seria impossible, ja que assegura la disponibilitat d'aigua dolça per a tots els ecosistemes."""

TEXT_B = """La Revolució Industrial va ser un procés de transformacions econòmiques, socials i tecnològiques que s'inicià al Regne Unit a la segona meitat del segle XVIII i s'expandí progressivament per Europa i Amèrica del Nord durant el segle XIX. L'element desencadenant fou la introducció de la màquina de vapor, que permeté mecanitzar la producció tèxtil i substituir la força humana i animal per energia mecànica. Aquesta innovació propicià l'aparició de les primeres fàbriques, on centenars d'obrers treballaven jornades de més de dotze hores en condicions sovint precàries. La ciutat industrial creixé de manera accelerada, atraient població rural i generant barris obrers amb greus problemes de salubritat. Paral·lelament, sorgí una nova classe social, el proletariat, que començà a organitzar-se per reivindicar millores laborals. La burgesia industrial, propietària dels mitjans de producció, consolidà el seu poder econòmic i polític. Les conseqüències d'aquest procés — la producció en massa, el ferrocarril, el capitalisme modern — configuraren el món contemporani tal com el coneixem avui."""

TEXTS = [
    {"id": "A", "titol": "El cicle de l'aigua", "materia": "cientific", "text": TEXT_A},
    {"id": "B", "titol": "La Revolució Industrial", "materia": "humanistic", "text": TEXT_B},
]

# ─── Perfils ───
PERFILS = [
    {
        "id": "P1",
        "etiqueta": "Marc Ribera — TDAH ESO B1",
        "profile": {
            "nom": "Marc Ribera",
            "caracteristiques": {
                "tdah": {"actiu": True, "grau": "moderat"},
            },
        },
        "context": {"etapa": "ESO", "curs": "3r"},
        "params": {
            "mecr_sortida": "B1",
            "dua": "Core",
            "genere_discursiu": "explicació",
            "complements": {},
        },
    },
    {
        "id": "P2",
        "etiqueta": "Pol Vidal — AACC ESO B2",
        "profile": {
            "nom": "Pol Vidal",
            "caracteristiques": {
                "altes_capacitats": {"actiu": True},
            },
        },
        "context": {"etapa": "ESO", "curs": "4t"},
        "params": {
            "mecr_sortida": "B2",
            "dua": "Enriquiment",
            "genere_discursiu": "explicació",
            "complements": {},
        },
    },
    {
        "id": "P3",
        "etiqueta": "Aya Sellami — nouvingut primària A1",
        "profile": {
            "nom": "Aya Sellami",
            "caracteristiques": {
                "nouvingut": {"actiu": True, "L1": "àrab", "mesos_catalunya": 3},
            },
        },
        "context": {"etapa": "primària", "curs": "4t"},
        "params": {
            "mecr_sortida": "A1",
            "dua": "Accés",
            "genere_discursiu": "explicació",
            "complements": {},
        },
    },
]

MODELS = [
    {"id": "gemma", "nom": "Gemma 3 27B", "model_id": GEMMA_MODEL},
    {"id": "gpt", "nom": "GPT-4.1-mini", "model_id": GPT_MODEL},
]


# ═══════════════════════════════════════════════════════════════════════════
# CONSTRUCTORS DE PROMPTS (V1, V2, V3)
# ═══════════════════════════════════════════════════════════════════════════

def build_prompt_v1(profile: dict, context: dict, params: dict) -> str:
    """V1 = identitat + DUA + gènere + persona-audience (SENSE catàleg)."""
    mecr = params.get("mecr_sortida", "B2")
    dua = params.get("dua", "Core")
    parts = []

    parts.append(corpus_reader.get_identity())

    dua_block = corpus_reader.get_dua_block(dua)
    if dua_block:
        parts.append(dua_block)

    genre = params.get("genere_discursiu", "")
    if genre:
        genre_block = corpus_reader.get_genre_block(genre)
        if genre_block:
            parts.append(genre_block)

    persona = server.build_persona_audience(profile, context, mecr)
    parts.append(f"PERSONA-AUDIENCE:\n{persona}")

    parts.append(
        "FORMAT DE SORTIDA:\n"
        "Respon amb la secció ## Text adaptat amb el text complet adaptat."
    )
    return "\n\n".join(parts)


def build_prompt_v2(profile: dict, context: dict, params: dict) -> str:
    """V2 = identitat + instruccions filtrades per MECR + gènere (SENSE DUA ni persona)."""
    parts = []

    parts.append(corpus_reader.get_identity())

    filtered = instruction_filter.get_instructions(profile, params)
    instructions_text = instruction_filter.format_instructions_for_prompt(filtered)
    parts.append(instructions_text)

    genre = params.get("genere_discursiu", "")
    if genre:
        genre_block = corpus_reader.get_genre_block(genre)
        if genre_block:
            parts.append(genre_block)

    parts.append(
        "FORMAT DE SORTIDA:\n"
        "Respon amb la secció ## Text adaptat amb el text complet adaptat."
    )
    return "\n\n".join(parts)


def build_prompt_v3(profile: dict, context: dict, params: dict) -> str:
    """V3 = baseline complet (equivalent a build_system_prompt actual)."""
    return server.build_system_prompt(profile, context, params, "")


VARIANTS = [
    {"id": "V1", "desc": "identitat + DUA + gènere + persona (sense catàleg)", "fn": build_prompt_v1},
    {"id": "V2", "desc": "identitat + catàleg filtrat + gènere (sense DUA ni persona)", "fn": build_prompt_v2},
    {"id": "V3", "desc": "baseline complet (build_system_prompt)", "fn": build_prompt_v3},
]


# ═══════════════════════════════════════════════════════════════════════════
# CRIDES ALS MODELS
# ═══════════════════════════════════════════════════════════════════════════

def call_gemma(system_prompt: str, text: str, max_retries: int = 3):
    """Crida Gemma 3 27B via google-genai amb rotació de claus i backoff.

    Retorna dict amb keys: ok, response, latency_s, error, tokens_in, tokens_out.
    """
    from google import genai
    from google.genai import types

    keys = server.GEMMA4_API_KEYS
    if not keys:
        return {
            "ok": False, "response": "", "latency_s": 0.0,
            "error": "No hi ha claus GEMMA4 configurades al .env",
            "tokens_in": None, "tokens_out": None,
        }

    errors = []
    t0 = time.time()
    for attempt in range(max_retries):
        for idx in range(len(keys)):
            client = genai.Client(
                api_key=keys[idx],
                http_options=types.HttpOptions(timeout=300_000),
            )
            try:
                full = f"{system_prompt}\n\n---\n\nTEXT ORIGINAL A ADAPTAR:\n\n{text}"
                resp = client.models.generate_content(
                    model=GEMMA_MODEL,
                    contents=[types.Content(role="user", parts=[types.Part(text=full)])],
                    config=types.GenerateContentConfig(
                        temperature=0.4, max_output_tokens=8192,
                    ),
                )
                latency = time.time() - t0
                out = resp.text or ""
                usage = getattr(resp, "usage_metadata", None)
                tin = getattr(usage, "prompt_token_count", None) if usage else None
                tout = getattr(usage, "candidates_token_count", None) if usage else None
                return {
                    "ok": True, "response": out, "latency_s": latency, "error": "",
                    "tokens_in": tin, "tokens_out": tout,
                }
            except Exception as e:
                msg = str(e)[:250]
                errors.append(f"clau {idx+1} (try {attempt+1}): {msg}")
                # Si és quota, esperem abans del pròxim intent
                if "429" in msg or "quota" in msg.lower() or "exhausted" in msg.lower():
                    time.sleep(2 + attempt * 3)
                continue
    latency = time.time() - t0
    return {
        "ok": False, "response": "", "latency_s": latency,
        "error": "; ".join(errors[-4:]),
        "tokens_in": None, "tokens_out": None,
    }


def call_gpt(system_prompt: str, text: str):
    """Crida GPT-4.1-mini via openai SDK."""
    from openai import OpenAI
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return {
            "ok": False, "response": "", "latency_s": 0.0,
            "error": "OPENAI_API_KEY no configurada",
            "tokens_in": None, "tokens_out": None,
        }
    t0 = time.time()
    try:
        client = OpenAI(api_key=key)
        resp = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"TEXT ORIGINAL A ADAPTAR:\n\n{text}"},
            ],
            max_tokens=8192,
            temperature=0.4,
        )
        latency = time.time() - t0
        out = resp.choices[0].message.content or ""
        usage = resp.usage
        return {
            "ok": True, "response": out, "latency_s": latency, "error": "",
            "tokens_in": usage.prompt_tokens if usage else None,
            "tokens_out": usage.completion_tokens if usage else None,
        }
    except Exception as e:
        latency = time.time() - t0
        return {
            "ok": False, "response": "", "latency_s": latency,
            "error": str(e)[:400],
            "tokens_in": None, "tokens_out": None,
        }


def call_model(model_id: str, system_prompt: str, text: str):
    if model_id == "gemma":
        return call_gemma(system_prompt, text)
    elif model_id == "gpt":
        return call_gpt(system_prompt, text)
    raise ValueError(f"Model desconegut: {model_id}")


# ═══════════════════════════════════════════════════════════════════════════
# UTILITATS
# ═══════════════════════════════════════════════════════════════════════════

def word_count(s: str) -> int:
    return len([w for w in s.split() if w.strip()])


def estimate_cost_gpt(tokens_in: int | None, tokens_out: int | None) -> float:
    """gpt-4.1-mini preus (estimació 2026-04): $0.40/M input, $1.60/M output."""
    if tokens_in is None or tokens_out is None:
        return 0.0
    cin = (tokens_in / 1_000_000) * 0.40
    cout = (tokens_out / 1_000_000) * 1.60
    return cin + cout


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 70)
    print("Mini prova A/B de capes del prompt ATNE")
    print("=" * 70)

    stats = instruction_catalog.get_catalog_stats()
    print(f"\nCatàleg instruccions: {stats}")
    print(f"\nVariants: {[v['id'] for v in VARIANTS]}")
    print(f"Models: {[m['nom'] for m in MODELS]}")
    print(f"Perfils: {[p['id'] for p in PERFILS]}")
    print(f"Textos: {[t['id'] for t in TEXTS]}")
    print(f"Total crides previstes: {len(TEXTS) * len(PERFILS) * len(VARIANTS) * len(MODELS)}\n")

    # Construir els 9 prompts (3 perfils × 3 variants) — els prompts no depenen del text
    prompts = {}  # (perfil_id, variant_id) → prompt text
    for perfil in PERFILS:
        for variant in VARIANTS:
            pr = variant["fn"](perfil["profile"], perfil["context"], perfil["params"])
            prompts[(perfil["id"], variant["id"])] = pr
            print(f"  Prompt {perfil['id']}-{variant['id']}: {word_count(pr)} paraules, {len(pr)} chars")

    # Executar totes les combinacions
    results = []  # list of dicts
    failures = []
    start_global = time.time()
    n_done = 0
    n_total = len(TEXTS) * len(PERFILS) * len(VARIANTS) * len(MODELS)

    for text in TEXTS:
        for perfil in PERFILS:
            # Injectar matèria als params per a complements
            perfil_params = dict(perfil["params"])
            perfil_params["materia"] = text["materia"]
            perfil_params["etapa"] = perfil["context"]["etapa"]
            perfil_params["mecr"] = perfil["params"]["mecr_sortida"]

            for variant in VARIANTS:
                # Reconstruir prompt amb matèria injectada (afecta V3)
                try:
                    prompt = variant["fn"](perfil["profile"], perfil["context"], perfil_params)
                except Exception as e:
                    prompt = prompts[(perfil["id"], variant["id"])]
                    print(f"  [AVÍS] Error construint prompt: {e} — uso prompt sense matèria")

                for model in MODELS:
                    n_done += 1
                    tag = f"[{n_done}/{n_total}] text={text['id']} perfil={perfil['id']} variant={variant['id']} model={model['id']}"
                    print(f"\n{tag}")
                    try:
                        r = call_model(model["id"], prompt, text["text"])
                        status = "OK" if r["ok"] else "FAILED"
                        print(f"   -> {status} ({r['latency_s']:.1f}s, "
                              f"{word_count(r['response'])} paraules sortida, "
                              f"tokens_in={r['tokens_in']} tokens_out={r['tokens_out']})")
                        if not r["ok"]:
                            print(f"   error: {r['error'][:200]}")
                            failures.append({
                                "text": text["id"], "perfil": perfil["id"],
                                "variant": variant["id"], "model": model["id"],
                                "error": r["error"],
                            })
                    except Exception as e:
                        r = {
                            "ok": False, "response": "", "latency_s": 0.0,
                            "error": f"Excepció Python: {e}\n{traceback.format_exc()[:500]}",
                            "tokens_in": None, "tokens_out": None,
                        }
                        failures.append({
                            "text": text["id"], "perfil": perfil["id"],
                            "variant": variant["id"], "model": model["id"],
                            "error": str(e),
                        })
                        print(f"   -> EXCEPCIÓ: {e}")

                    results.append({
                        "text_id": text["id"],
                        "text_titol": text["titol"],
                        "perfil_id": perfil["id"],
                        "perfil_etiqueta": perfil["etiqueta"],
                        "variant_id": variant["id"],
                        "variant_desc": variant["desc"],
                        "model_id": model["id"],
                        "model_nom": model["nom"],
                        "prompt": prompt,
                        "response": r["response"],
                        "latency_s": r["latency_s"],
                        "tokens_in": r["tokens_in"],
                        "tokens_out": r["tokens_out"],
                        "error": r.get("error", ""),
                        "ok": r["ok"],
                        "words_out": word_count(r["response"]),
                    })

    total_elapsed = time.time() - start_global
    print(f"\n\nTotal temps: {total_elapsed:.1f}s · èxits: {sum(1 for r in results if r['ok'])}/{len(results)}")

    # ═══════════════════════════════════════════════════════════════════════
    # Escriure markdown
    # ═══════════════════════════════════════════════════════════════════════
    out_path = ROOT / "tests" / "mini_prova_capes_resultats.md"
    write_markdown(out_path, results, stats, prompts, failures, total_elapsed)
    print(f"\nResultats escrits a: {out_path}")

    # Cost GPT total
    total_cost = sum(
        estimate_cost_gpt(r["tokens_in"], r["tokens_out"])
        for r in results if r["model_id"] == "gpt" and r["ok"]
    )
    print(f"Cost GPT-4.1-mini estimat: ${total_cost:.4f}")


# ═══════════════════════════════════════════════════════════════════════════
# ESCRIPTURA MARKDOWN
# ═══════════════════════════════════════════════════════════════════════════

def write_markdown(path: Path, results: list, catalog_stats: dict, prompts: dict, failures: list, total_elapsed: float):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = []
    lines.append("# Mini prova A/B de capes del prompt — resultats")
    lines.append("")
    lines.append(f"**Data execució**: {now}")
    lines.append(f"**Durada total**: {total_elapsed:.1f}s")
    lines.append(f"**Crides totals**: {len(results)}")
    n_ok = sum(1 for r in results if r["ok"])
    lines.append(f"**Crides OK**: {n_ok}")
    lines.append(f"**Crides FAILED**: {len(results) - n_ok}")
    lines.append("")
    lines.append("## Paràmetres")
    lines.append("")
    lines.append(f"- **Catàleg**: {catalog_stats}")
    lines.append(f"- **Models**: Gemma 3 27B (`{GEMMA_MODEL}`) · GPT-4.1-mini (`{GPT_MODEL}`)")
    lines.append(f"- **Perfils**: {', '.join(p['etiqueta'] for p in PERFILS)}")
    lines.append(f"- **Textos**: A — El cicle de l'aigua ({word_count(TEXT_A)} paraules) · B — La Revolució Industrial ({word_count(TEXT_B)} paraules)")
    lines.append("")
    lines.append("## Variants")
    lines.append("")
    for v in VARIANTS:
        lines.append(f"- **{v['id']}**: {v['desc']}")
    lines.append("")

    # Per cada (text, perfil): 3 taules (V1, V2, V3) amb 2 columnes (Gemma/GPT)
    for text in TEXTS:
        for perfil in PERFILS:
            lines.append(f"---")
            lines.append("")
            lines.append(f"## Text {text['id']} — {text['titol']} · Perfil {perfil['id']} — {perfil['etiqueta']}")
            lines.append("")

            for variant in VARIANTS:
                lines.append(f"### Variant {variant['id']} — {variant['desc']}")
                lines.append("")
                gemma_r = next((r for r in results if r["text_id"] == text["id"] and r["perfil_id"] == perfil["id"] and r["variant_id"] == variant["id"] and r["model_id"] == "gemma"), None)
                gpt_r = next((r for r in results if r["text_id"] == text["id"] and r["perfil_id"] == perfil["id"] and r["variant_id"] == variant["id"] and r["model_id"] == "gpt"), None)

                # Taula amb metadades
                lines.append("| | Gemma 3 27B | GPT-4.1-mini |")
                lines.append("|---|---|---|")
                g_words = gemma_r["words_out"] if gemma_r and gemma_r["ok"] else "—"
                p_words = gpt_r["words_out"] if gpt_r and gpt_r["ok"] else "—"
                lines.append(f"| Paraules sortida | {g_words} | {p_words} |")
                g_lat = f"{gemma_r['latency_s']:.1f}s" if gemma_r and gemma_r["ok"] else "—"
                p_lat = f"{gpt_r['latency_s']:.1f}s" if gpt_r and gpt_r["ok"] else "—"
                lines.append(f"| Latència | {g_lat} | {p_lat} |")
                g_tok = f"{gemma_r['tokens_in']} → {gemma_r['tokens_out']}" if gemma_r and gemma_r["ok"] and gemma_r["tokens_in"] is not None else "—"
                p_tok = f"{gpt_r['tokens_in']} → {gpt_r['tokens_out']}" if gpt_r and gpt_r["ok"] and gpt_r["tokens_in"] is not None else "—"
                lines.append(f"| Tokens (in → out) | {g_tok} | {p_tok} |")
                g_stat = "OK" if gemma_r and gemma_r["ok"] else ("FAILED" if gemma_r else "—")
                p_stat = "OK" if gpt_r and gpt_r["ok"] else ("FAILED" if gpt_r else "—")
                lines.append(f"| Estat | {g_stat} | {p_stat} |")
                lines.append("")

                # Sortida Gemma
                lines.append("#### Sortida Gemma 3 27B")
                lines.append("")
                if gemma_r and gemma_r["ok"]:
                    lines.append("```markdown")
                    lines.append(gemma_r["response"].strip())
                    lines.append("```")
                else:
                    err = gemma_r["error"] if gemma_r else "No executat"
                    lines.append(f"_FAILED_: `{err}`")
                lines.append("")

                # Sortida GPT
                lines.append("#### Sortida GPT-4.1-mini")
                lines.append("")
                if gpt_r and gpt_r["ok"]:
                    lines.append("```markdown")
                    lines.append(gpt_r["response"].strip())
                    lines.append("```")
                else:
                    err = gpt_r["error"] if gpt_r else "No executat"
                    lines.append(f"_FAILED_: `{err}`")
                lines.append("")

            # Observacions automàtiques per cas (text × perfil)
            lines.append("#### Observacions automàtiques (cas)")
            lines.append("")
            obs = generar_observacions_cas(results, text["id"], perfil["id"])
            for o in obs:
                lines.append(f"- {o}")
            lines.append("")

    # Taula resum global
    lines.append("---")
    lines.append("")
    lines.append("## Resum global — paraules de sortida")
    lines.append("")
    lines.append("| Text | Perfil | Variant | Gemma paraules | GPT paraules |")
    lines.append("|---|---|---|---|---|")
    for text in TEXTS:
        for perfil in PERFILS:
            for variant in VARIANTS:
                g = next((r for r in results if r["text_id"] == text["id"] and r["perfil_id"] == perfil["id"] and r["variant_id"] == variant["id"] and r["model_id"] == "gemma"), None)
                p = next((r for r in results if r["text_id"] == text["id"] and r["perfil_id"] == perfil["id"] and r["variant_id"] == variant["id"] and r["model_id"] == "gpt"), None)
                gw = g["words_out"] if g and g["ok"] else "FAIL"
                pw = p["words_out"] if p and p["ok"] else "FAIL"
                lines.append(f"| {text['id']} | {perfil['id']} | {variant['id']} | {gw} | {pw} |")
    lines.append("")

    # Observacions globals
    lines.append("## Observacions automàtiques globals")
    lines.append("")
    obs_global = generar_observacions_globals(results)
    for o in obs_global:
        lines.append(f"- {o}")
    lines.append("")

    # Failures
    if failures:
        lines.append("## Errors (FAILED)")
        lines.append("")
        for f in failures:
            lines.append(f"- text={f['text']} perfil={f['perfil']} variant={f['variant']} model={f['model']}: `{f['error'][:300]}`")
        lines.append("")

    # Annex prompts
    lines.append("---")
    lines.append("")
    lines.append("## Annex — prompts generats (9 combinacions perfil × variant)")
    lines.append("")
    for perfil in PERFILS:
        for variant in VARIANTS:
            key = (perfil["id"], variant["id"])
            pr = prompts.get(key, "")
            lines.append(f"<details>")
            lines.append(f"<summary>Prompt {perfil['id']} — {perfil['etiqueta']} · Variant {variant['id']} ({word_count(pr)} paraules, {len(pr)} chars)</summary>")
            lines.append("")
            lines.append("```text")
            lines.append(pr)
            lines.append("```")
            lines.append("")
            lines.append("</details>")
            lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def generar_observacions_cas(results: list, text_id: str, perfil_id: str) -> list[str]:
    """Observacions automàtiques per (text, perfil) — només mètriques objectives."""
    obs = []
    subset = [r for r in results if r["text_id"] == text_id and r["perfil_id"] == perfil_id and r["ok"]]
    if not subset:
        return ["Sense resultats OK en aquest cas."]

    # Paraules per variant (mitjana entre Gemma i GPT)
    for variant in VARIANTS:
        v_results = [r for r in subset if r["variant_id"] == variant["id"]]
        if v_results:
            avg = sum(r["words_out"] for r in v_results) / len(v_results)
            obs.append(f"Variant {variant['id']}: mitjana {avg:.0f} paraules ({len(v_results)} models OK)")

    # Per model, quina variant dona més paraules
    for model in MODELS:
        m_results = [r for r in subset if r["model_id"] == model["id"]]
        if m_results:
            m_results_sorted = sorted(m_results, key=lambda r: r["words_out"], reverse=True)
            top = m_results_sorted[0]
            obs.append(f"{model['nom']}: variant més llarga = {top['variant_id']} ({top['words_out']} paraules)")

    return obs


def generar_observacions_globals(results: list) -> list[str]:
    """Observacions automàtiques globals — comparacions entre variants."""
    obs = []
    ok = [r for r in results if r["ok"]]

    # Mitjana paraules per variant
    for v in VARIANTS:
        rs = [r for r in ok if r["variant_id"] == v["id"]]
        if rs:
            avg = sum(r["words_out"] for r in rs) / len(rs)
            obs.append(f"Variant {v['id']}: mitjana {avg:.0f} paraules de sortida ({len(rs)} crides OK)")

    # Count casos on V2 < V3 i V2 < V1
    n_cases = len(TEXTS) * len(PERFILS) * len(MODELS)
    v2_shorter_v3 = 0
    v2_shorter_v1 = 0
    v1_shorter_v3 = 0
    for text in TEXTS:
        for perfil in PERFILS:
            for model in MODELS:
                v1 = next((r for r in ok if r["text_id"] == text["id"] and r["perfil_id"] == perfil["id"] and r["variant_id"] == "V1" and r["model_id"] == model["id"]), None)
                v2 = next((r for r in ok if r["text_id"] == text["id"] and r["perfil_id"] == perfil["id"] and r["variant_id"] == "V2" and r["model_id"] == model["id"]), None)
                v3 = next((r for r in ok if r["text_id"] == text["id"] and r["perfil_id"] == perfil["id"] and r["variant_id"] == "V3" and r["model_id"] == model["id"]), None)
                if v2 and v3 and v2["words_out"] < v3["words_out"]:
                    v2_shorter_v3 += 1
                if v2 and v1 and v2["words_out"] < v1["words_out"]:
                    v2_shorter_v1 += 1
                if v1 and v3 and v1["words_out"] < v3["words_out"]:
                    v1_shorter_v3 += 1

    obs.append(f"V2 produeix text més curt que V3 en {v2_shorter_v3} de {n_cases} casos")
    obs.append(f"V2 produeix text més curt que V1 en {v2_shorter_v1} de {n_cases} casos")
    obs.append(f"V1 produeix text més curt que V3 en {v1_shorter_v3} de {n_cases} casos")

    # Mitjana latència per model
    for m in MODELS:
        rs = [r for r in ok if r["model_id"] == m["id"]]
        if rs:
            avg_lat = sum(r["latency_s"] for r in rs) / len(rs)
            obs.append(f"{m['nom']}: latència mitjana {avg_lat:.1f}s ({len(rs)} crides OK)")

    # Cost GPT
    gpt_in = sum(r["tokens_in"] or 0 for r in ok if r["model_id"] == "gpt")
    gpt_out = sum(r["tokens_out"] or 0 for r in ok if r["model_id"] == "gpt")
    cost = (gpt_in / 1_000_000) * 0.40 + (gpt_out / 1_000_000) * 1.60
    obs.append(f"GPT-4.1-mini: {gpt_in} tokens input + {gpt_out} tokens output totals · cost estimat ${cost:.4f}")

    return obs


if __name__ == "__main__":
    main()
