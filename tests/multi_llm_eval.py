"""
multi_llm_eval.py — Orquestrador d'avaluació multi-LLM complet.

Matriu: 4 generadors × 2 vies × 20 textos × 10 perfils = 1.600 adaptacions
Avaluació: 4 jutges × 1.600 individual + 4 jutges × 800 comparativa = 9.600 avaluacions

Generadors: Gemini Flash, Claude Sonnet (via API), Llama 3.3 70B (Groq), GPT-4o-mini (OpenAI)
Avaluadors: els mateixos 4 (inclou auto-avaluació per mesurar biaix)
Orquestrador: Claude Opus (analitza resultats en conversa)

Tot queda registrat a la BD SQLite: text original, perfil, prompt, adaptació, complements, mètriques.

Ús:
  python tests/multi_llm_eval.py --phase generate --generator gemini
  python tests/multi_llm_eval.py --phase generate --generator all
  python tests/multi_llm_eval.py --phase evaluate --judge gemini --eval-type individual
  python tests/multi_llm_eval.py --phase evaluate --judge gemini --eval-type comparative
  python tests/multi_llm_eval.py --phase all
"""

import argparse
import json
import os
import random
import re
import sqlite3
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓ
# ═══════════════════════════════════════════════════════════════════════════════

DB_PATH = Path(__file__).parent / "results" / "evaluations.db"
DATA_PATH = Path(__file__).parent / "test_data.json"
ROOT = Path(__file__).parent.parent

GENERATORS = ["gemini", "sonnet", "llama", "gpt", "qwen"]
PROMPT_MODES = ["hardcoded", "rag"]
API_DELAY = 2  # segons entre crides

# ═══════════════════════════════════════════════════════════════════════════════
# CLIENTS LLM
# ═══════════════════════════════════════════════════════════════════════════════

def call_gemini(system_prompt: str, user_prompt: str) -> str:
    """Crida Gemini 2.5 Flash."""
    from google import genai
    from google.genai import types
    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY"),
        http_options=types.HttpOptions(timeout=180_000),
    )
    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[types.Content(role="user", parts=[types.Part(text=user_prompt)])],
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.3,
            max_output_tokens=8192,
        ),
    )
    return resp.text or ""


def call_sonnet(system_prompt: str, user_prompt: str) -> str:
    """Crida Claude Sonnet via Anthropic API."""
    import anthropic
    client = anthropic.Anthropic()  # Usa ANTHROPIC_API_KEY del entorn
    resp = client.messages.create(
        model="claude-sonnet-4-6-20250514",
        max_tokens=8192,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return resp.content[0].text if resp.content else ""


def call_llama(system_prompt: str, user_prompt: str) -> str:
    """Crida Llama 3.3 70B via Groq."""
    from groq import Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=8192,
        temperature=0.3,
    )
    return resp.choices[0].message.content or ""


def call_gpt(system_prompt: str, user_prompt: str) -> str:
    """Crida GPT-4o-mini via OpenAI."""
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=8192,
        temperature=0.3,
    )
    return resp.choices[0].message.content or ""


def call_qwen(system_prompt: str, user_prompt: str) -> str:
    """Crida Qwen3 32B via Groq."""
    from groq import Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    resp = client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=8192,
        temperature=0.3,
    )
    return resp.choices[0].message.content or ""


LLM_CALLERS = {
    "gemini": call_gemini,
    "sonnet": call_sonnet,
    "llama": call_llama,
    "gpt": call_gpt,
    "qwen": call_qwen,
}


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTRUCCIÓ DE PROMPTS
# ═══════════════════════════════════════════════════════════════════════════════

def _flatten_profile(perfil_entry: dict) -> dict:
    """Aplana 'detalls' al nivell de la característica."""
    profile = perfil_entry["profile"]
    flat = {"caracteristiques": {}}
    for key, val in profile.get("caracteristiques", {}).items():
        flat_val = {"actiu": val.get("actiu", True)}
        if "detalls" in val:
            flat_val.update(val["detalls"])
        flat["caracteristiques"][key] = flat_val
    return flat


def build_hardcoded_prompt(perfil_entry: dict, text_entry: dict) -> tuple[str, dict]:
    """Construeix prompt via Hardcoded (prompt_blocks.py)."""
    # Carregar prompt_blocks des de git si cal
    tmp_dir = ROOT / "tests" / ".tmp"
    tmp_dir.mkdir(exist_ok=True)
    pb_path = tmp_dir / "prompt_blocks.py"

    if not pb_path.exists():
        import subprocess
        result = subprocess.run(
            ["git", "show", "prompt-v2-hardcoded:prompt_blocks.py"],
            capture_output=True, text=True, cwd=str(ROOT)
        )
        if result.returncode == 0:
            pb_path.write_text(result.stdout, encoding="utf-8")

    # Importar dinàmicament
    import importlib.util
    spec = importlib.util.spec_from_file_location("prompt_blocks", str(pb_path))
    pb = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pb)

    params = perfil_entry["params"]
    mecr = params.get("mecr_sortida", "B2")
    dua = params.get("dua", "Core")
    flat = _flatten_profile(perfil_entry)
    active = [k for k, v in flat["caracteristiques"].items() if v.get("actiu")]

    parts = [pb.IDENTITY_BLOCK, pb.UNIVERSAL_RULES_BLOCK]

    if mecr in pb.MECR_BLOCKS:
        parts.append(pb.MECR_BLOCKS[mecr])
    if dua in pb.DUA_BLOCKS:
        parts.append(pb.DUA_BLOCKS[dua])

    genre = params.get("genere_discursiu", "")
    if genre and genre in pb.GENRE_BLOCKS:
        parts.append(pb.GENRE_BLOCKS[genre])

    for p in active:
        if p in pb.PROFILE_BLOCKS:
            parts.append(pb.PROFILE_BLOCKS[p])

    if mecr in pb.FEWSHOT_EXAMPLES:
        parts.append(pb.FEWSHOT_EXAMPLES[mecr])

    parts.append(f"CONTEXT: Etapa {text_entry['etapa']}, gènere {text_entry['genere']}")

    return "\n\n".join(parts), {"mode": "hardcoded", "instruction_ids": [], "filter_stats": {}}


def build_rag_prompt(perfil_entry: dict, text_entry: dict) -> tuple[str, dict]:
    """Construeix prompt via RAG filtrat (instruction_filter)."""
    from instruction_filter import get_instructions, format_instructions_for_prompt
    import corpus_reader

    if not corpus_reader._cache:
        corpus_reader.load_corpus()

    params = perfil_entry["params"]
    mecr = params.get("mecr_sortida", "B2")
    dua = params.get("dua", "Core")
    flat = _flatten_profile(perfil_entry)

    filtered = get_instructions(flat, params)
    instructions_text = format_instructions_for_prompt(filtered)

    parts = [corpus_reader.get_identity()]
    parts.append(instructions_text)

    dua_block = corpus_reader.get_dua_block(dua)
    if dua_block:
        parts.append(dua_block)

    genre = params.get("genere_discursiu", "")
    if genre:
        genre_block = corpus_reader.get_genre_block(genre)
        if genre_block:
            parts.append(genre_block)

    fewshot = corpus_reader.get_fewshot_example(mecr)
    if fewshot:
        parts.append(f"EXEMPLE DE SORTIDA ESPERADA ({mecr}):\n{fewshot}")

    parts.append(f"CONTEXT: Etapa {text_entry['etapa']}, gènere {text_entry['genere']}")

    # Extraure IDs d'instruccions enviades
    from evaluator_metrics import extract_instruction_ids
    ids = extract_instruction_ids(filtered)

    return "\n\n".join(parts), {
        "mode": "rag",
        "instruction_ids": ids,
        "filter_stats": filtered.get("stats", {}),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# DETECCIÓ COMPLEMENTS AL TEXT GENERAT
# ═══════════════════════════════════════════════════════════════════════════════

def detect_complements(text: str) -> dict:
    """Detecta quins complements s'han generat al text adaptat."""
    return {
        "te_glossari": 1 if re.search(r"##\s*(Glossari|Paraules clau)", text, re.I) else 0,
        "te_glossari_bilingue": 1 if any(0x0600 <= ord(c) <= 0x06FF or 0x4E00 <= ord(c) <= 0x9FFF for c in text) else 0,
        "te_negretes": 1 if len(re.findall(r"\*\*[^*]+\*\*", text)) >= 2 else 0,
        "te_prellico": 1 if re.search(r"##\s*(Paraules|Abans|Objectius|Qu[eè]\s*aprend)", text, re.I) else 0,
        "te_esquema": 1 if re.search(r"##\s*(Esquema|Mapa)", text, re.I) else 0,
        "te_preguntes": 1 if re.search(r"##\s*(Preguntes|Comprensió)", text, re.I) else 0,
        "te_argumentacio_pedagogica": 1 if re.search(r"##\s*Argumentació", text, re.I) else 0,
        "te_auditoria": 1 if re.search(r"##\s*(Notes d'auditoria|Auditoria)", text, re.I) else 0,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# FASE 1: GENERACIÓ
# ═══════════════════════════════════════════════════════════════════════════════

def run_generation(conn, run_id: str, generator: str, data: dict, args):
    """Genera adaptacions amb un generador específic."""
    textos = data["textos"]
    perfils = data["perfils"]
    caller = LLM_CALLERS[generator]

    total = len(textos) * len(perfils) * len(PROMPT_MODES)
    i = 0

    for t in textos:
        for p in perfils:
            for mode in PROMPT_MODES:
                i += 1
                cas_id = f"{t['id']}__{p['id']}"

                # Comprovar si ja existeix
                existing = conn.execute(
                    "SELECT id FROM multi_llm_generations WHERE run_id=? AND cas_id=? AND generator=? AND prompt_mode=?",
                    (run_id, cas_id, generator, mode)
                ).fetchone()
                if existing:
                    continue

                print(f"  [{i:4d}/{total}] {cas_id} [{generator}/{mode}] ...", end=" ", flush=True)

                try:
                    # Construir prompt
                    if mode == "hardcoded":
                        system_prompt, meta = build_hardcoded_prompt(p, t)
                    else:
                        system_prompt, meta = build_rag_prompt(p, t)

                    user_prompt = f"Adapta el següent text educatiu segons les instruccions del system prompt:\n\n{t['text']}"

                    # Generar
                    t0 = time.time()
                    text_adaptat = caller(system_prompt, user_prompt)
                    elapsed = time.time() - t0

                    # Mètriques forma
                    from evaluator_metrics import evaluate_forma
                    params = p["params"]
                    mecr = params.get("mecr_sortida", "B2")
                    forma = evaluate_forma(text_adaptat, mecr)

                    # Recall
                    recall = None
                    absents = None
                    if mode == "rag":
                        from evaluator_metrics import retrieval_recall
                        flat = _flatten_profile(p)
                        active = [k for k, v in flat["caracteristiques"].items() if v.get("actiu")]
                        ret = retrieval_recall(active, meta.get("instruction_ids", []))
                        recall = ret["recall"]
                        absents = json.dumps(ret.get("absents", []), ensure_ascii=False)

                    # Complements
                    comps = detect_complements(text_adaptat)

                    paraules = len(text_adaptat.split())
                    print(f"{paraules}w {elapsed:.1f}s")

                    # Guardar a BD
                    conn.execute("""
                        INSERT INTO multi_llm_generations
                        (run_id, cas_id, text_id, perfil_id, generator, prompt_mode,
                         text_original, text_original_tema, text_original_font,
                         text_original_etapa, text_original_genere, text_original_paraules,
                         perfil_nom, perfil_json, perfils_actius, mecr, dua,
                         system_prompt, system_prompt_length, instruction_ids, filter_stats,
                         text_adaptat, text_adaptat_length, text_adaptat_paraules,
                         te_glossari, te_glossari_bilingue, te_negretes, te_prellico,
                         te_esquema, te_preguntes, te_argumentacio_pedagogica, te_auditoria,
                         f1_longitud_frase, f2_titols, f3_negretes, f4_llistes, f5_prellico,
                         puntuacio_forma, recall, instruccions_absents, temps_generacio)
                        VALUES (?,?,?,?,?,?, ?,?,?,?,?,?, ?,?,?,?,?, ?,?,?,?, ?,?,?, ?,?,?,?,?,?,?,?, ?,?,?,?,?,?,?,?,?)
                    """, (
                        run_id, cas_id, t["id"], p["id"], generator, mode,
                        t["text"], t.get("tema", ""), t.get("font", ""),
                        t.get("etapa", ""), t.get("genere", ""), t.get("paraules", 0),
                        p.get("nom", ""), json.dumps(p, ensure_ascii=False),
                        json.dumps([k for k, v in _flatten_profile(p)["caracteristiques"].items() if v.get("actiu")]),
                        mecr, params.get("dua", "Core"),
                        system_prompt, len(system_prompt),
                        json.dumps(meta.get("instruction_ids", []), ensure_ascii=False),
                        json.dumps(meta.get("filter_stats", {}), ensure_ascii=False),
                        text_adaptat, len(text_adaptat), paraules,
                        comps["te_glossari"], comps["te_glossari_bilingue"],
                        comps["te_negretes"], comps["te_prellico"],
                        comps["te_esquema"], comps["te_preguntes"],
                        comps["te_argumentacio_pedagogica"], comps["te_auditoria"],
                        forma["F1_longitud_frase"], forma["F2_titols"],
                        forma["F3_negretes"], forma["F4_llistes"], forma["F5_prellico_present"],
                        forma["puntuacio_forma"], recall, absents, elapsed,
                    ))
                    conn.commit()

                except Exception as e:
                    print(f"ERROR: {e}")
                    conn.execute("""
                        INSERT INTO multi_llm_generations
                        (run_id, cas_id, text_id, perfil_id, generator, prompt_mode, error)
                        VALUES (?,?,?,?,?,?,?)
                    """, (run_id, cas_id, t["id"], p["id"], generator, mode, str(e)))
                    conn.commit()

                time.sleep(API_DELAY)


# ═══════════════════════════════════════════════════════════════════════════════
# FASE 2: AVALUACIÓ INDIVIDUAL (rúbrica C1-C5)
# ═══════════════════════════════════════════════════════════════════════════════

EVAL_INDIVIDUAL_SYSTEM = """Ets un avaluador pedagògic expert i escèptic. Avalua la qualitat d'una adaptació de text educatiu.

PROCEDIMENT (Chain-of-Thought):
1. Llegeix el text adaptat i identifica 3-5 evidències concretes per a cada criteri.
2. Per cada criteri, raona en 1-2 frases per què puntuaries alt o baix.
3. NOMÉS DESPRÉS, assigna la puntuació numèrica.

Criteris (1-5):
C1 COHERÈNCIA: text intern consistent, idees flueixen lògicament, connectors presents
C2 ADEQUACIÓ AL PERFIL: instruccions del perfil aplicades amb evidència directa
C3 PRESERVACIÓ CURRICULAR: contingut original mantingut sense omissions ni errors
C4 ADEQUACIÓ MECR: lèxic/sintaxi al nivell declarat
C5 PRELLIÇÓ: glossari previ o organitzador que prepari cognitivament

Retorna NOMÉS JSON:
{"C1":{"p":1-5,"j":"..."},"C2":{"p":1-5,"j":"..."},"C3":{"p":1-5,"j":"..."},"C4":{"p":1-5,"j":"..."},"C5":{"p":1-5,"j":"..."}}"""


def run_individual_eval(conn, run_id: str, judge: str, args):
    """Avaluació individual C1-C5 per cada adaptació."""
    caller = LLM_CALLERS[judge]

    rows = conn.execute("""
        SELECT id, cas_id, generator, prompt_mode, text_adaptat, text_original,
               perfils_actius, mecr, dua, text_original_etapa, text_original_genere
        FROM multi_llm_generations
        WHERE run_id = ? AND text_adaptat IS NOT NULL AND error IS NULL
        ORDER BY cas_id, generator, prompt_mode
    """, (run_id,)).fetchall()

    total = len(rows)
    for i, r in enumerate(rows, 1):
        gen_id = r["id"]
        cas_id = r["cas_id"]

        # Comprovar si ja avaluat
        existing = conn.execute(
            "SELECT id FROM multi_llm_evaluations WHERE run_id=? AND generation_id=? AND judge=? AND eval_type='individual'",
            (run_id, gen_id, judge)
        ).fetchone()
        if existing:
            continue

        is_self = 1 if r["generator"] == judge else 0
        print(f"  [{i:4d}/{total}] {cas_id} [{r['generator']}/{r['prompt_mode']}] jutge={judge} {'(auto)' if is_self else ''} ...", end=" ", flush=True)

        user_prompt = f"""Perfil: {r['perfils_actius']} | MECR: {r['mecr']} | DUA: {r['dua']} | Etapa: {r['text_original_etapa']}

TEXT ORIGINAL:
{(r['text_original'] or '')[:1500]}

TEXT ADAPTAT ({r['generator']}/{r['prompt_mode']}):
{(r['text_adaptat'] or '')[:3000]}"""

        try:
            raw = caller(EVAL_INDIVIDUAL_SYSTEM, user_prompt)
            # Parsejar JSON
            start = raw.find("{")
            end = raw.rfind("}")
            if start != -1 and end != -1:
                result = json.loads(raw[start:end + 1])
            else:
                result = {}

            scores = {}
            for c in ["C1", "C2", "C3", "C4", "C5"]:
                val = result.get(c, {})
                scores[c] = {"p": val.get("p", 0), "j": val.get("j", "")}

            avg = sum(scores[c]["p"] for c in scores if scores[c]["p"]) / max(1, sum(1 for c in scores if scores[c]["p"]))
            print(f"avg={avg:.1f}")

            conn.execute("""
                INSERT INTO multi_llm_evaluations
                (run_id, cas_id, generation_id, judge, eval_type,
                 c1_coherencia, c1_justificacio, c2_adequacio_perfil, c2_justificacio,
                 c3_preservacio_curricular, c3_justificacio, c4_adequacio_mecr, c4_justificacio,
                 c5_prellico_funcional, c5_justificacio, puntuacio_fons, is_self_eval)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                run_id, cas_id, gen_id, judge, "individual",
                scores["C1"]["p"], scores["C1"]["j"],
                scores["C2"]["p"], scores["C2"]["j"],
                scores["C3"]["p"], scores["C3"]["j"],
                scores["C4"]["p"], scores["C4"]["j"],
                scores["C5"]["p"], scores["C5"]["j"],
                round(avg, 2), is_self,
            ))
            conn.commit()

        except Exception as e:
            print(f"ERROR: {e}")

        time.sleep(API_DELAY)


# ═══════════════════════════════════════════════════════════════════════════════
# FASE 3: AVALUACIÓ COMPARATIVA (HC vs RAG)
# ═══════════════════════════════════════════════════════════════════════════════

EVAL_COMPARATIVE_SYSTEM = """Ets un avaluador pedagògic expert. Reps dos textos adaptats (A i B) del MATEIX original per al MATEIX perfil. Decideix quin és millor.

REGLES:
1. NO saps quina branca ha generat cada text.
2. Per cada criteri, tria A o B (o empat).
3. Justifica en UNA frase.
4. Retorna NOMÉS JSON.

{"global":{"winner":"A" o "B" o "empat","confidence":"alta/mitjana/baixa","justification":"..."},
"C1":{"winner":"A/B/empat","j":"..."},"C2":{"winner":"A/B/empat","j":"..."},
"C3":{"winner":"A/B/empat","j":"..."},"C4":{"winner":"A/B/empat","j":"..."},
"C5":{"winner":"A/B/empat","j":"..."}}"""


def run_comparative_eval(conn, run_id: str, judge: str, args):
    """Avaluació comparativa HC vs RAG per cada generador."""
    caller = LLM_CALLERS[judge]

    # Obtenir parells HC/RAG del mateix generador i cas
    pairs = conn.execute("""
        SELECT g1.id as hc_id, g1.cas_id, g1.generator, g1.text_adaptat as text_hc,
               g2.id as rag_id, g2.text_adaptat as text_rag,
               g1.text_original, g1.perfils_actius, g1.mecr, g1.dua,
               g1.text_original_etapa
        FROM multi_llm_generations g1
        JOIN multi_llm_generations g2
            ON g1.cas_id = g2.cas_id AND g1.generator = g2.generator AND g1.run_id = g2.run_id
        WHERE g1.run_id = ? AND g1.prompt_mode = 'hardcoded' AND g2.prompt_mode = 'rag'
            AND g1.text_adaptat IS NOT NULL AND g2.text_adaptat IS NOT NULL
            AND g1.error IS NULL AND g2.error IS NULL
        ORDER BY g1.cas_id, g1.generator
    """, (run_id,)).fetchall()

    total = len(pairs)
    for i, r in enumerate(pairs, 1):
        # Comprovar si ja avaluat
        existing = conn.execute(
            "SELECT id FROM multi_llm_evaluations WHERE run_id=? AND generation_id=? AND other_generation_id=? AND judge=? AND eval_type='comparative'",
            (run_id, r["hc_id"], r["rag_id"], judge)
        ).fetchone()
        if existing:
            continue

        is_self = 1 if r["generator"] == judge else 0

        # Randomitzar ordre
        if random.random() < 0.5:
            text_a, text_b = r["text_hc"], r["text_rag"]
            order = "hc_first"
        else:
            text_a, text_b = r["text_rag"], r["text_hc"]
            order = "rag_first"

        print(f"  [{i:4d}/{total}] {r['cas_id']} gen={r['generator']} jutge={judge} {'(auto)' if is_self else ''} ...", end=" ", flush=True)

        user_prompt = f"""Perfil: {r['perfils_actius']} | MECR: {r['mecr']} | DUA: {r['dua']}

TEXT ORIGINAL:
{(r['text_original'] or '')[:1000]}

TEXT A:
{(text_a or '')[:2500]}

TEXT B:
{(text_b or '')[:2500]}"""

        try:
            raw = caller(EVAL_COMPARATIVE_SYSTEM, user_prompt)
            start = raw.find("{")
            end = raw.rfind("}")
            if start != -1 and end != -1:
                result = json.loads(raw[start:end + 1])
            else:
                result = {}

            g = result.get("global", {})
            winner_label = g.get("winner", "empat")

            # Desfer randomitzat
            def resolve(w):
                if not w or w == "empat":
                    return "empat"
                if order == "hc_first":
                    return "hardcoded" if w == "A" else "rag"
                else:
                    return "rag" if w == "A" else "hardcoded"

            winner = resolve(winner_label)
            print(f"-> {winner}")

            conn.execute("""
                INSERT INTO multi_llm_evaluations
                (run_id, cas_id, generation_id, other_generation_id, judge, eval_type,
                 winner, confidence, justification,
                 c1_coherencia, c1_justificacio, c2_adequacio_perfil, c2_justificacio,
                 c3_preservacio_curricular, c3_justificacio, c4_adequacio_mecr, c4_justificacio,
                 c5_prellico_funcional, c5_justificacio,
                 is_self_eval, order_presented)
                VALUES (?,?,?,?,?,?, ?,?,?, ?,?,?,?,?,?,?,?,?,?, ?,?)
            """, (
                run_id, r["cas_id"], r["hc_id"], r["rag_id"], judge, "comparative",
                winner, g.get("confidence", ""), g.get("justification", ""),
                resolve(result.get("C1", {}).get("winner", "")),
                result.get("C1", {}).get("j", ""),
                resolve(result.get("C2", {}).get("winner", "")),
                result.get("C2", {}).get("j", ""),
                resolve(result.get("C3", {}).get("winner", "")),
                result.get("C3", {}).get("j", ""),
                resolve(result.get("C4", {}).get("winner", "")),
                result.get("C4", {}).get("j", ""),
                resolve(result.get("C5", {}).get("winner", "")),
                result.get("C5", {}).get("j", ""),
                is_self, order,
            ))
            conn.commit()

        except Exception as e:
            print(f"ERROR: {e}")

        time.sleep(API_DELAY)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="ATNE — Avaluació multi-LLM")
    parser.add_argument("--phase", choices=["generate", "evaluate", "all"], default="all")
    parser.add_argument("--generator", type=str, default="all",
                        help="Generador: gemini|sonnet|llama|gpt|all")
    parser.add_argument("--judge", type=str, default="all",
                        help="Jutge: gemini|sonnet|llama|gpt|all")
    parser.add_argument("--eval-type", choices=["individual", "comparative", "all"], default="all")
    parser.add_argument("--run-id", type=str, default="",
                        help="Run ID (auto-generat si buit)")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    # Carregar dades
    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)

    if args.limit > 0:
        data["textos"] = data["textos"][:args.limit]

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")

    run_id = args.run_id or datetime.now().strftime("%Y%m%d_%H%M%S")

    print("=" * 70)
    print(f"  ATNE — Avaluació Multi-LLM")
    print(f"  Run: {run_id}")
    print(f"  Textos: {len(data['textos'])} | Perfils: {len(data['perfils'])}")
    print(f"  Phase: {args.phase} | Generator: {args.generator} | Judge: {args.judge}")
    print("=" * 70)

    # ── FASE 1: GENERACIÓ ──
    if args.phase in ("generate", "all"):
        generators = GENERATORS if args.generator == "all" else [args.generator]
        for gen in generators:
            print(f"\n{'='*50}")
            print(f"  GENERANT: {gen}")
            print(f"{'='*50}")
            try:
                run_generation(conn, run_id, gen, data, args)
            except Exception as e:
                print(f"  ERROR FATAL {gen}: {e}")

    # ── FASE 2-3: AVALUACIÓ ──
    if args.phase in ("evaluate", "all"):
        judges = GENERATORS if args.judge == "all" else [args.judge]

        for j in judges:
            if args.eval_type in ("individual", "all"):
                print(f"\n{'='*50}")
                print(f"  AVALUACIÓ INDIVIDUAL: jutge={j}")
                print(f"{'='*50}")
                try:
                    run_individual_eval(conn, run_id, j, args)
                except Exception as e:
                    print(f"  ERROR FATAL eval individual {j}: {e}")

            if args.eval_type in ("comparative", "all"):
                print(f"\n{'='*50}")
                print(f"  AVALUACIÓ COMPARATIVA: jutge={j}")
                print(f"{'='*50}")
                try:
                    run_comparative_eval(conn, run_id, j, args)
                except Exception as e:
                    print(f"  ERROR FATAL eval comparativa {j}: {e}")

    # ── RESUM ──
    n_gen = conn.execute("SELECT COUNT(*) FROM multi_llm_generations WHERE run_id=?", (run_id,)).fetchone()[0]
    n_eval = conn.execute("SELECT COUNT(*) FROM multi_llm_evaluations WHERE run_id=?", (run_id,)).fetchone()[0]

    print(f"\n{'='*70}")
    print(f"  COMPLETAT")
    print(f"  Generacions: {n_gen}")
    print(f"  Avaluacions: {n_eval}")
    print(f"  BD: {DB_PATH}")
    print(f"{'='*70}")

    conn.close()


if __name__ == "__main__":
    main()
