"""
gen_slow.py — Generador pacient per free tier.

Fa UNA crida, espera el temps necessari, i repeteix.
Sense rotacio de claus agressiva, sense rafegues.

Us:
  python tests/gen_slow.py --model gemini --delay 30
  python tests/gen_slow.py --model qwen3 --delay 65
"""

import argparse
import json
import os
import re
import sqlite3
import sys
import io
import time
from pathlib import Path

# stdout UTF-8 ja configurat per multi_v2.py al importar

sys.path.insert(0, str(Path(__file__).parent.parent))
from dotenv import load_dotenv
load_dotenv()

DB_PATH = Path(__file__).parent / "results" / "evaluations.db"
DATA_PATH = Path(__file__).parent / "test_data.json"
RUN_ID = "multi_v2"

# Importar funcions de multi_v2 per build_rag_v2_prompt i detect_complements
sys.path.insert(0, str(Path(__file__).parent))


def call_gemini_single(system_prompt, user_prompt, key_name):
    """Una sola crida a Gemini amb UNA clau especifica."""
    from google import genai
    from google.genai import types
    key = os.getenv(key_name)
    if not key:
        raise RuntimeError(f"{key_name} no trobada")
    client = genai.Client(api_key=key, http_options=types.HttpOptions(timeout=180_000))
    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[types.Content(role="user", parts=[types.Part(text=user_prompt)])],
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.3,
            max_output_tokens=8192,
            thinking_config=types.ThinkingConfig(thinking_budget=0),
        ),
    )
    return resp.text or ""


def call_qwen3_single(system_prompt, user_prompt):
    """Una sola crida a Qwen 3 via Groq."""
    import requests
    # Rotar entre claus Groq fresques
    global _groq_key_idx
    groq_keys = [k for k in [os.getenv("GROQ_API_KEY_2"), os.getenv("GROQ_API_KEY_3"),
                              os.getenv("GROQ_API_KEY_4"), os.getenv("GROQ_API_KEY_5"),
                              os.getenv("GROQ_API_KEY_6"), os.getenv("GROQ_API_KEY")] if k]
    if not hasattr(call_qwen3_single, '_idx'):
        call_qwen3_single._idx = 0
    groq_key = groq_keys[call_qwen3_single._idx % len(groq_keys)]
    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {groq_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "qwen/qwen3-32b",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "max_tokens": 8192,
            "temperature": 0.3,
        },
        timeout=300,
    )
    if r.status_code in (429, 413):
        call_qwen3_single._idx += 1  # provar seguent clau
        raise RuntimeError(f"RATE_LIMIT_{r.status_code}")
    if r.status_code != 200:
        raise RuntimeError(f"HTTP {r.status_code}: {r.text[:200]}")
    text = r.json()["choices"][0]["message"]["content"] or ""
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
    call_qwen3_single._idx += 1  # rotar per repartir quota
    return text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, choices=["gemini", "qwen3"])
    parser.add_argument("--delay", type=int, default=30, help="Segons entre crides exitoses")
    parser.add_argument("--retry-delay", type=int, default=120, help="Segons despres d'un error")
    parser.add_argument("--key", default="GEMINI_API_KEY_3", help="Nom de la clau per Gemini (una sola)")
    parser.add_argument("--limit", type=int, default=0, help="Max generacions (0=totes)")
    args = parser.parse_args()

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=30000")

    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)

    from multi_v2 import build_rag_v2_prompt, detect_complements

    textos = data["textos"]
    perfils = data["perfils"]
    total = len(textos) * len(perfils)
    generated = 0
    errors = 0

    print(f"=== GEN SLOW [{args.model}] clau={args.key if args.model=='gemini' else 'GROQ'} delay={args.delay}s ===")

    for i, t in enumerate(textos):
        for j, p in enumerate(perfils):
            cas_id = f"{t['id']}__{p['id']}"
            idx = i * len(perfils) + j + 1

            # Skip si ja existeix
            existing = conn.execute(
                "SELECT id FROM multi_llm_generations WHERE run_id=? AND cas_id=? AND generator=? AND prompt_mode='rag_v2' AND text_adaptat IS NOT NULL AND text_adaptat != ''",
                (RUN_ID, cas_id, args.model)
            ).fetchone()
            if existing:
                continue

            # Esborrar errors previs d'aquest cas
            conn.execute(
                "DELETE FROM multi_llm_generations WHERE run_id=? AND cas_id=? AND generator=? AND prompt_mode='rag_v2' AND error IS NOT NULL",
                (RUN_ID, cas_id, args.model)
            )
            conn.commit()

            print(f"  [{idx:3d}/{total}] {cas_id} ...", end=" ", flush=True)
            t0 = time.time()

            system_prompt, meta = build_rag_v2_prompt(p, t)
            user_prompt = f"Adapta el text seguent:\n\n{t['text']}"

            text_adaptat = ""
            error = None
            try:
                if args.model == "gemini":
                    text_adaptat = call_gemini_single(system_prompt, user_prompt, args.key)
                else:
                    text_adaptat = call_qwen3_single(system_prompt, user_prompt)
            except Exception as e:
                error = str(e)[:200]
                if "RATE_LIMIT" in error or "429" in error or "413" in error:
                    print(f"RATE LIMIT — esperant {args.retry_delay}s", flush=True)
                    time.sleep(args.retry_delay)
                    # Reintentar UNA vegada
                    try:
                        if args.model == "gemini":
                            text_adaptat = call_gemini_single(system_prompt, user_prompt, args.key)
                        else:
                            text_adaptat = call_qwen3_single(system_prompt, user_prompt)
                        error = None
                    except Exception as e2:
                        error = str(e2)[:200]
                        print(f"FAIL 2n intent", flush=True)

            temps = round(time.time() - t0, 1)

            if text_adaptat and not error:
                # Netejar thinking
                text_adaptat = re.sub(r"<think>.*?</think>", "", text_adaptat, flags=re.DOTALL).strip()
                if text_adaptat.find("##") > 100:
                    text_adaptat = text_adaptat[text_adaptat.find("##"):]

                paraules = len(text_adaptat.split())
                comps = detect_complements(text_adaptat)

                try:
                    from evaluator_metrics import evaluate_forma
                    forma = evaluate_forma(text_adaptat, p["params"].get("mecr_sortida", "B2"))
                except Exception:
                    forma = {}

                recall_val = None
                absents_val = None
                try:
                    from evaluator_metrics import retrieval_recall
                    active_profs = meta["filter_stats"].get("perfils_actius", [])
                    ret = retrieval_recall(active_profs, meta.get("instruction_ids", []))
                    recall_val = ret["recall"]
                    absents_val = json.dumps(ret.get("absents", []), ensure_ascii=False)
                except Exception:
                    pass

                conn.execute("""
                    INSERT INTO multi_llm_generations (
                        run_id, cas_id, text_id, perfil_id, generator, prompt_mode,
                        text_original, text_original_tema, text_original_font,
                        text_original_etapa, text_original_genere, text_original_paraules,
                        perfil_nom, perfil_json, perfils_actius, mecr, dua,
                        system_prompt, system_prompt_length, instruction_ids, filter_stats,
                        text_adaptat, text_adaptat_length, text_adaptat_paraules,
                        te_glossari, te_glossari_bilingue, te_negretes, te_prellico,
                        te_esquema, te_preguntes, te_argumentacio_pedagogica, te_auditoria,
                        f1_longitud_frase, f2_titols, f3_negretes, f4_llistes, f5_prellico,
                        puntuacio_forma, recall, instruccions_absents, temps_generacio, error
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """, (
                    RUN_ID, cas_id, t["id"], p["id"], args.model, "rag_v2",
                    t["text"], t.get("tema", ""), t.get("font", ""),
                    t.get("etapa", ""), t.get("genere", ""), t.get("paraules", 0),
                    p["nom"], json.dumps(p["profile"], ensure_ascii=False),
                    json.dumps(meta["filter_stats"].get("perfils_actius", []), ensure_ascii=False),
                    p["params"].get("mecr_sortida", "B2"),
                    p["params"].get("dua", "Core"),
                    system_prompt, len(system_prompt),
                    json.dumps(meta.get("instruction_ids", []), ensure_ascii=False),
                    json.dumps(meta.get("filter_stats", {}), ensure_ascii=False),
                    text_adaptat, len(text_adaptat), paraules,
                    comps.get("te_glossari", 0), comps.get("te_glossari_bilingue", 0),
                    comps.get("te_negretes", 0), comps.get("te_prellico", 0),
                    comps.get("te_esquema", 0), comps.get("te_preguntes", 0),
                    comps.get("te_argumentacio_pedagogica", 0), comps.get("te_auditoria", 0),
                    forma.get("f1_longitud_frase", 0), forma.get("f2_titols", 0),
                    forma.get("f3_negretes", 0), forma.get("f4_llistes", 0),
                    forma.get("f5_prellico", 0),
                    forma.get("puntuacio_forma", 0),
                    recall_val, absents_val, temps, None
                ))
                conn.commit()
                generated += 1
                print(f"OK ({paraules} par, {temps}s)")
            else:
                errors += 1
                print(f"ERR: {error[:80] if error else 'buit'}")

            # DELAY FIX entre crides (la clau del exit)
            wait = args.delay if not error else args.retry_delay
            time.sleep(wait)

            if args.limit and generated >= args.limit:
                break
        if args.limit and generated >= args.limit:
            break

    print(f"\n=== RESULTAT: {generated} generats, {errors} errors ===")
    conn.close()


if __name__ == "__main__":
    main()
