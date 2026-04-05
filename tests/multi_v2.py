"""
multi_v2.py — Generació i avaluació RAG-v2 vs HC i RAG-v1.

Objectiu: Mesurar l'impacte de les millores (macrodirectives + sub-variables connectades)
comparant RAG-v2 amb HC i RAG-v1 (copiats de multi_v1).

Rubrica: v2 (8 criteris: A1-A3, B1-B4, C1) — fonamentada i amb ancoratges.
Ref: docs/decisions/rubrica_avaluacio_v2.md

Generadors: gemini, sonnet, gpt  (3)
Jutges:     gemini ($0), gpt4mini (~$2)
Branques:   hc (copiat multi_v1), rag_v1 (copiat multi_v1), rag_v2 (nou)
Casos:      20 textos × 10 perfils = 200 per generador = 600 noves generacions

Avaluació en 3 fases:
  1. Individual: rúbrica v2 (8 criteris), cada text sol → 1800 avaluacions/jutge
  2. Trio intra-model: HC vs RAG-v1 vs RAG-v2 (rànquing 1r/2n/3r) → 600 trios/jutge
  3. Cross-model: parells RAG-v2 entre generadors → 600 parells/jutge

Ús:
  python tests/multi_v2.py --phase init_db
  python tests/multi_v2.py --phase copy_v1
  python tests/multi_v2.py --phase generate --generator all
  python tests/multi_v2.py --phase evaluate --judge gemini
  python tests/multi_v2.py --phase evaluate --judge gpt4mini
  python tests/multi_v2.py --phase trio --judge gemini
  python tests/multi_v2.py --phase trio --judge gpt4mini
  python tests/multi_v2.py --phase cross --judge gemini
  python tests/multi_v2.py --phase cross --judge gpt4mini
  python tests/multi_v2.py --phase report
"""

import argparse
import io
import json
import os
import random
import re
import sqlite3
import sys
import time
from datetime import datetime
from pathlib import Path

# Forçar UTF-8 a stdout/stderr (evita errors charmap en Windows)
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "buffer"):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).parent.parent))
from dotenv import load_dotenv
load_dotenv()

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓ
# ═══════════════════════════════════════════════════════════════════════════════

RUN_ID       = "multi_v2"
V1_RUN_ID    = "multi_v1"
GENERATORS   = ["gemini", "sonnet", "gpt", "gemma4", "mistral"]
JUDGES       = ["gemini", "gpt4mini", "gemma4", "mistral"]
DB_PATH      = Path(__file__).parent / "results" / "evaluations.db"
DATA_PATH    = Path(__file__).parent / "test_data.json"
ROOT         = Path(__file__).parent.parent
API_DELAY    = 2  # segons entre crides

# ═══════════════════════════════════════════════════════════════════════════════
# CLIENTS LLM
# ═══════════════════════════════════════════════════════════════════════════════

def call_gemini(system_prompt: str, user_prompt: str) -> str:
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
            thinking_config=types.ThinkingConfig(thinking_budget=0),
        ),
    )
    return resp.text or ""


def call_sonnet(system_prompt: str, user_prompt: str) -> str:
    """Crida Claude Sonnet via claude.cmd (usa autenticació Claude Code, sense API key)."""
    import subprocess, os, tempfile
    CLAUDE_CMD = r"C:\Users\miquel.amor\Desktop\nodejs\claude.cmd"
    env = os.environ.copy()
    env["CLAUDE_CODE_GIT_BASH_PATH"] = r"C:\Users\miquel.amor\AppData\Local\Programs\Git\bin\bash.exe"

    # System prompt via fitxer temporal, user prompt via stdin
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False,
                                     encoding="utf-8", dir=os.getenv("TEMP", ".")) as f:
        f.write(system_prompt)
        sp_file = f.name
    try:
        result = subprocess.run(
            [CLAUDE_CMD, "-p", "-",
             "--system-prompt-file", sp_file, "--model", "sonnet"],
            input=user_prompt.encode("utf-8"),
            capture_output=True, env=env, timeout=180
        )
        if result.returncode != 0:
            err = result.stderr.decode("utf-8", errors="replace")[:300]
            raise RuntimeError(err if err else "error desconegut")
        return result.stdout.decode("utf-8", errors="replace").strip()
    finally:
        try:
            os.unlink(sp_file)
        except Exception:
            pass


def call_gpt(system_prompt: str, user_prompt: str) -> str:
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


def call_gpt4mini(system_prompt: str, user_prompt: str) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=4096,
        temperature=0.2,
    )
    return resp.choices[0].message.content or ""


def _call_gemma4_base(system_prompt: str, user_prompt: str, max_tokens: int, temp: float) -> str:
    """Gemma 4 31B via API gratuïta (clau GEMMA4_API_KEY, free tier SENSE billing).
    Retry automàtic per errors 500/504 (servidor inestable, model nou).
    """
    from google import genai
    from google.genai import types
    client = genai.Client(
        api_key=os.getenv("GEMMA4_API_KEY"),
        http_options=types.HttpOptions(timeout=480_000),  # 8 min timeout
    )
    max_retries = 3
    for attempt in range(max_retries):
        try:
            resp = client.models.generate_content(
                model="gemma-4-31b-it",
                contents=[types.Content(role="user", parts=[types.Part(text=f"{system_prompt}\n\n---\n\n{user_prompt}")])],
                config=types.GenerateContentConfig(
                    temperature=temp,
                    max_output_tokens=max_tokens,
                ),
            )
            time.sleep(5)
            return resp.text or ""
        except Exception as e:
            err_str = str(e)
            if ("504" in err_str or "500" in err_str or "DEADLINE" in err_str or "INTERNAL" in err_str) and attempt < max_retries - 1:
                wait = 30 * (attempt + 1)  # 30s, 60s
                print(f"[retry {attempt+1}/{max_retries} en {wait}s] ", end="", flush=True)
                time.sleep(wait)
                continue
            raise


def call_gemma4(system_prompt: str, user_prompt: str) -> str:
    return _call_gemma4_base(system_prompt, user_prompt, max_tokens=8192, temp=0.3)


def call_gemma4_judge(system_prompt: str, user_prompt: str) -> str:
    return _call_gemma4_base(system_prompt, user_prompt, max_tokens=4096, temp=0.2)


def _call_mistral_base(system_prompt: str, user_prompt: str, max_tokens: int, temp: float) -> str:
    """Mistral Small via API gratuita (Experiment plan, clau MISTRAL_API_KEY sense billing).
    Limits free tier: 60 RPM, 375.000 TPM, 1B tokens/mes. Europeu (GDPR-nativa).
    """
    import requests
    max_retries = 3
    for attempt in range(max_retries):
        try:
            r = requests.post(
                "https://api.mistral.ai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {os.getenv('MISTRAL_API_KEY')}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "mistral-small-latest",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "max_tokens": max_tokens,
                    "temperature": temp,
                },
                timeout=300,
            )
            if r.status_code == 429:  # Rate limit
                wait = 60
                print(f"[rate limit, esperant {wait}s] ", end="", flush=True)
                time.sleep(wait)
                continue
            if r.status_code != 200:
                raise RuntimeError(f"HTTP {r.status_code}: {r.text[:200]}")
            data = r.json()
            return data["choices"][0]["message"]["content"] or ""
        except Exception as e:
            err_str = str(e)
            if attempt < max_retries - 1 and ("timeout" in err_str.lower() or "500" in err_str or "502" in err_str or "503" in err_str):
                wait = 15 * (attempt + 1)
                print(f"[retry {attempt+1}/{max_retries} en {wait}s] ", end="", flush=True)
                time.sleep(wait)
                continue
            raise


def call_mistral(system_prompt: str, user_prompt: str) -> str:
    return _call_mistral_base(system_prompt, user_prompt, max_tokens=8192, temp=0.3)


def call_mistral_judge(system_prompt: str, user_prompt: str) -> str:
    return _call_mistral_base(system_prompt, user_prompt, max_tokens=4096, temp=0.2)


GEN_CALLERS = {"gemini": call_gemini, "sonnet": call_sonnet, "gpt": call_gpt, "gemma4": call_gemma4, "mistral": call_mistral}
JUDGE_CALLERS = {"gemini": call_gemini, "gpt4mini": call_gpt4mini, "sonnet": call_sonnet, "gemma4": call_gemma4_judge, "mistral": call_mistral_judge}

# ═══════════════════════════════════════════════════════════════════════════════
# PROMPTS D'AVALUACIÓ — RÚBRICA V2 (8 criteris)
# ═══════════════════════════════════════════════════════════════════════════════

EVAL_SYSTEM_V2 = """Ets un avaluador pedagògic expert i escèptic. Avalua la qualitat d'una adaptació de text educatiu.

PROCEDIMENT (Chain-of-Thought obligatori):
1. Llegeix el perfil de l'alumnat i el nivell MECR declarat.
2. Per cada criteri, busca EVIDÈNCIES concretes al text adaptat.
3. Raona en 2-3 frases per criteri.
4. DESPRÉS assigna la puntuació (1-5) basant-te EXCLUSIVAMENT en evidències.
5. Si no trobes evidència per a un criteri, puntua 2 (no 1 ni 3).

CRITERIS I ANCORATGES RÀPIDS:

DIMENSIÓ A — Qualitat textual:
A1 COHERÈNCIA I COHESIÓ: text internament consistent, idees flueixen, connectors presents.
  1=incoherent | 3=acceptable amb connectors bàsics | 5=flux impecable, connectors variats
A2 CORRECCIÓ LINGÜÍSTICA: gramàtica, ortografia, registre educatiu en català.
  1=errors greus | 3=errors ocasionals que no impedeixen comprensió | 5=impecable, publicable
A3 LLEGIBILITAT / MECR: complexitat lexicosintàctica corresponent al nivell declarat.
  1=completament fora de rang | 3=50-75% frases dins rang | 5=perfectament calibrat

DIMENSIÓ B — Adequació pedagògica:
B1 FIDELITAT CURRICULAR: contingut acadèmic original preservat sense omissions.
  1=conceptes clau eliminats | 3=tots els conceptes nuclears presents, detalls omesos | 5=tot preservat
B2 ADEQUACIÓ AL PERFIL: instruccions del perfil (TEA/TDAH/nouvingut/etc.) aplicades amb evidència.
  1=text genèric, cap adaptació | 3=elements principals del perfil aplicats | 5=totes les instruccions amb evidència
  INVERSIÓ per AC/Enriquiment: puntua alt si NO simplifica i SÍ enriqueix.
B3 SUPORTS COGNITIUS / SCAFFOLDING: glossari previ, definicions integrades, esquema, títols descriptius.
  1=cap suport, text pla | 3=almenys un suport funcional | 5=scaffolding decreixent complet
B4 SENSIBILITAT CULTURAL I INCLUSIÓ: referents culturals adequats, to inclusiu, no estigmatitza.
  1=referents exclusius, to condescendent | 3=neutre, correcte | 5=referents universals, connexions interculturals

DIMENSIÓ C — Eficàcia:
C1 POTENCIAL D'APRENENTATGE: un alumne amb el perfil declarat, podria aprendre aquest text?
  1=no aprendria res | 3=aprenentatge possible amb docent | 5=aprenentatge assegurat, ZPD perfecte

PUNTUACIÓ GLOBAL = A×0.3 + B×0.5 + C×0.2 (on A=mitj(A1,A2,A3), B=mitj(B1,B2,B3,B4))

Retorna EXACTAMENT aquest JSON (sense text addicional):
{"A1":{"p":1-5,"j":"..."},"A2":{"p":1-5,"j":"..."},"A3":{"p":1-5,"j":"..."},
 "B1":{"p":1-5,"j":"..."},"B2":{"p":1-5,"j":"..."},"B3":{"p":1-5,"j":"..."},"B4":{"p":1-5,"j":"..."},
 "C1":{"p":1-5,"j":"..."}}"""

EVAL_USER_TEMPLATE = """PERFIL: {perfils} | MECR: {mecr} | DUA: {dua} | Etapa: {etapa}

TEXT ORIGINAL:
{text_original}

TEXT ADAPTAT A AVALUAR:
{text_adaptat}"""


TRIO_SYSTEM_V2 = """Ets un avaluador pedagògic expert i escèptic. Reps TRES adaptacions anònimes (Text A, Text B, Text C) del MATEIX text original, per al MATEIX perfil d'alumnat, generades pel MATEIX model.

REGLES:
1. NO saps quina versió del prompt ha generat cada text. Avalua NOMÉS el resultat.
2. Per cada criteri, ordena els 3 textos de MILLOR (1r) a PITJOR (3r).
3. Justifica cada rànquing en UNA frase amb evidència concreta.
4. Si dos textos són equivalents en un criteri, pots posar el mateix lloc (ex: 1r, 1r, 3r).
5. Retorna NOMÉS el JSON demanat.

CRITERIS DE RÀNQUING:
- global: Quin text és millor globalment per a l'aprenentatge d'aquest alumne?
- B1_fidelitat: Quin preserva millor el contingut curricular?
- B2_adequacio: Quin aplica millor les adaptacions específiques del perfil?
- B3_scaffolding: Quin ofereix millor suport cognitiu (glossari, esquemes, títols)?
- C1_potencial: En quin l'alumne aprendria més?

Retorna EXACTAMENT aquest JSON:
{"global":{"1st":"A/B/C","2nd":"A/B/C","3rd":"A/B/C","j":"..."},
 "B1":{"1st":"A/B/C","2nd":"A/B/C","3rd":"A/B/C","j":"..."},
 "B2":{"1st":"A/B/C","2nd":"A/B/C","3rd":"A/B/C","j":"..."},
 "B3":{"1st":"A/B/C","2nd":"A/B/C","3rd":"A/B/C","j":"..."},
 "C1":{"1st":"A/B/C","2nd":"A/B/C","3rd":"A/B/C","j":"..."}}"""

TRIO_USER_TEMPLATE = """PERFIL: {perfils} | MECR: {mecr} | DUA: {dua} | Etapa: {etapa}

TEXT ORIGINAL:
{text_original}

---
TEXT A:
{text_a}

---
TEXT B:
{text_b}

---
TEXT C:
{text_c}"""

CROSS_SYSTEM_V2 = """Ets un avaluador pedagògic expert. Reps dos textos adaptats (Text A i Text B) del MATEIX text original, per al MATEIX perfil, generats per models DIFERENTS.

REGLES:
1. NO saps quin model ha generat cada text. Avalua NOMÉS el resultat.
2. Per cada criteri, decideix quin és millor per a AQUEST alumne.
3. Justifica en UNA frase amb evidència concreta.
4. Retorna NOMÉS el JSON demanat.

CRITERIS:
- global: Quin text és millor globalment?
- B1: Fidelitat curricular
- B2: Adequació al perfil
- B3: Suports cognitius / scaffolding
- C1: Potencial d'aprenentatge

Retorna EXACTAMENT:
{"global":{"winner":"A"/"B"/"empat","confidence":"alta"/"mitjana"/"baixa","j":"..."},
 "B1":{"winner":"A"/"B"/"empat","j":"..."},
 "B2":{"winner":"A"/"B"/"empat","j":"..."},
 "B3":{"winner":"A"/"B"/"empat","j":"..."},
 "C1":{"winner":"A"/"B"/"empat","j":"..."}}"""

CROSS_USER_TEMPLATE = """PERFIL: {perfils} | MECR: {mecr} | DUA: {dua}

TEXT ORIGINAL:
{text_original}

---
TEXT A:
{text_a}

---
TEXT B:
{text_b}"""

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTRUCCIÓ DE PROMPT RAG-v2
# ═══════════════════════════════════════════════════════════════════════════════

def build_rag_v2_prompt(perfil_entry: dict, text_entry: dict) -> tuple[str, dict]:
    """Construeix prompt RAG-v2 amb el sistema actual (macrodirectives + sub-variables)."""
    import corpus_reader
    from instruction_filter import get_instructions, format_instructions_for_prompt
    from evaluator_metrics import extract_instruction_ids

    if not corpus_reader._cache:
        corpus_reader.load_corpus()

    profile = perfil_entry["profile"]  # Ja sense detalls, directe
    params = perfil_entry["params"]

    filtered = get_instructions(profile, params)
    instructions_text = format_instructions_for_prompt(filtered)

    parts = [corpus_reader.get_identity()]
    parts.append(instructions_text)

    dua = params.get("dua", "Core")
    dua_block = corpus_reader.get_dua_block(dua)
    if dua_block:
        parts.append(dua_block)

    genre = params.get("genere_discursiu", "")
    if genre:
        genre_block = corpus_reader.get_genre_block(genre)
        if genre_block:
            parts.append(genre_block)

    mecr = params.get("mecr_sortida", "B2")
    fewshot = corpus_reader.get_fewshot_example(mecr)
    if fewshot:
        parts.append(f"EXEMPLE DE SORTIDA ESPERADA ({mecr}):\n{fewshot}")

    parts.append(f"CONTEXT: Etapa {text_entry['etapa']}, gènere {text_entry['genere']}")

    ids = extract_instruction_ids(filtered)
    return "\n\n".join(parts), {
        "mode": "rag_v2",
        "instruction_ids": ids,
        "filter_stats": filtered.get("stats", {}),
    }


def detect_complements(text: str) -> dict:
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


def _parse_json(raw: str) -> dict:
    raw = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL).strip()
    start = raw.find("{")
    end = raw.rfind("}")
    if start != -1 and end != -1:
        try:
            return json.loads(raw[start:end + 1])
        except json.JSONDecodeError:
            pass
    return {}


# ═══════════════════════════════════════════════════════════════════════════════
# FASE 0: INICIALITZAR DB
# ═══════════════════════════════════════════════════════════════════════════════

def init_db(conn):
    """Crea taules v2 si no existeixen."""
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS multi_v2_evaluations (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        run_id          TEXT NOT NULL,
        cas_id          TEXT NOT NULL,
        generation_id   INTEGER,
        judge           TEXT NOT NULL,
        -- Rubrica v2: 8 criteris
        a1_coherencia       REAL, a1_justificacio TEXT,
        a2_correccio        REAL, a2_justificacio TEXT,
        a3_llegibilitat     REAL, a3_justificacio TEXT,
        b1_fidelitat        REAL, b1_justificacio TEXT,
        b2_adequacio_perfil REAL, b2_justificacio TEXT,
        b3_scaffolding      REAL, b3_justificacio TEXT,
        b4_cultura          REAL, b4_justificacio TEXT,
        c1_potencial        REAL, c1_justificacio TEXT,
        -- Puntuacions agregades
        puntuacio_a     REAL,  -- mitj(A1,A2,A3)
        puntuacio_b     REAL,  -- mitj(B1,B2,B3,B4)
        puntuacio_global REAL, -- A×0.3 + B×0.5 + C1×0.2
        -- Metadades
        is_self_eval    INTEGER DEFAULT 0,
        timestamp       TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS multi_v2_trios (
        id                  INTEGER PRIMARY KEY AUTOINCREMENT,
        run_id              TEXT NOT NULL,
        cas_id              TEXT NOT NULL,
        generator           TEXT NOT NULL,
        judge               TEXT NOT NULL,
        order_presented     TEXT,  -- ex: "A=hc,B=rag_v2,C=rag_v1"
        is_self_eval        INTEGER DEFAULT 0,
        -- Rànquing global (1=millor, 3=pitjor)
        global_hc       INTEGER, global_rag_v1   INTEGER, global_rag_v2   INTEGER, global_j TEXT,
        b1_hc           INTEGER, b1_rag_v1       INTEGER, b1_rag_v2       INTEGER, b1_j TEXT,
        b2_hc           INTEGER, b2_rag_v1       INTEGER, b2_rag_v2       INTEGER, b2_j TEXT,
        b3_hc           INTEGER, b3_rag_v1       INTEGER, b3_rag_v2       INTEGER, b3_j TEXT,
        c1_hc           INTEGER, c1_rag_v1       INTEGER, c1_rag_v2       INTEGER, c1_j TEXT,
        timestamp           TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS multi_v2_cross (
        id                  INTEGER PRIMARY KEY AUTOINCREMENT,
        run_id              TEXT NOT NULL,
        cas_id              TEXT NOT NULL,
        judge               TEXT NOT NULL,
        pair                TEXT NOT NULL,  -- 'gemini_vs_sonnet' | 'gemini_vs_gpt' | 'sonnet_vs_gpt'
        model_a             TEXT NOT NULL,
        model_b             TEXT NOT NULL,
        order_presented     TEXT,  -- 'a_first' | 'b_first'
        is_self_eval        INTEGER DEFAULT 0,
        global_winner   TEXT, global_confidence TEXT, global_j TEXT,
        b1_winner       TEXT, b1_j TEXT,
        b2_winner       TEXT, b2_j TEXT,
        b3_winner       TEXT, b3_j TEXT,
        c1_winner       TEXT, c1_j TEXT,
        timestamp           TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS multi_v2_runs (
        run_id      TEXT PRIMARY KEY,
        timestamp   TEXT,
        generators  TEXT,
        judges      TEXT,
        total_cases INTEGER,
        notes       TEXT
    );
    """)
    conn.commit()
    print("[init_db] Taules multi_v2 creades/verificades.")


# ═══════════════════════════════════════════════════════════════════════════════
# FASE 1: COPIAR HC + RAG-v1 DE MULTI_V1
# ═══════════════════════════════════════════════════════════════════════════════

def copy_v1(conn):
    """Copia HC i RAG-v1 de multi_v1 per als 3 generadors de multi_v2."""
    rows = conn.execute("""
        SELECT * FROM multi_llm_generations
        WHERE run_id = ? AND generator IN ('gemini','sonnet','gpt')
          AND prompt_mode IN ('hardcoded','rag')
        ORDER BY cas_id, generator, prompt_mode
    """, (V1_RUN_ID,)).fetchall()

    cols = [d[1] for d in conn.execute("PRAGMA table_info(multi_llm_generations)").fetchall()]
    copied = 0
    skipped = 0

    for row in rows:
        r = dict(zip(cols, row))
        # Renomenar 'rag' → 'rag_v1' per diferenciar
        mode_v2 = "rag_v1" if r["prompt_mode"] == "rag" else "hc"

        existing = conn.execute(
            "SELECT id FROM multi_llm_generations WHERE run_id=? AND cas_id=? AND generator=? AND prompt_mode=?",
            (RUN_ID, r["cas_id"], r["generator"], mode_v2)
        ).fetchone()
        if existing:
            skipped += 1
            continue

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
            RUN_ID, r["cas_id"], r["text_id"], r["perfil_id"], r["generator"], mode_v2,
            r["text_original"], r["text_original_tema"], r["text_original_font"],
            r["text_original_etapa"], r["text_original_genere"], r["text_original_paraules"],
            r["perfil_nom"], r["perfil_json"], r["perfils_actius"], r["mecr"], r["dua"],
            r["system_prompt"], r["system_prompt_length"], r["instruction_ids"], r["filter_stats"],
            r["text_adaptat"], r["text_adaptat_length"], r["text_adaptat_paraules"],
            r["te_glossari"], r["te_glossari_bilingue"], r["te_negretes"], r["te_prellico"],
            r["te_esquema"], r["te_preguntes"], r["te_argumentacio_pedagogica"], r["te_auditoria"],
            r["f1_longitud_frase"], r["f2_titols"], r["f3_negretes"], r["f4_llistes"], r["f5_prellico"],
            r["puntuacio_forma"], r["recall"], r["instruccions_absents"], r["temps_generacio"], r["error"]
        ))
        copied += 1

    conn.commit()
    print(f"[copy_v1] Copiats {copied} registres ({skipped} ja existien).")
    # Registrar run
    conn.execute("INSERT OR IGNORE INTO multi_v2_runs VALUES (?,?,?,?,?,?)",
        (RUN_ID, datetime.now().isoformat(), ",".join(GENERATORS), ",".join(JUDGES),
         len(rows) // 2, f"Còpia HC+RAG-v1 + RAG-v2 nou. Rubrica v2 (8 criteris)."))
    conn.commit()


# ═══════════════════════════════════════════════════════════════════════════════
# FASE 2: GENERACIÓ RAG-v2
# ═══════════════════════════════════════════════════════════════════════════════

def run_generation(conn, generator: str, data: dict):
    """Genera adaptacions RAG-v2 per un generador."""
    from evaluator_metrics import evaluate_forma, retrieval_recall

    textos = data["textos"]
    perfils = data["perfils"]
    caller = GEN_CALLERS[generator]
    total = len(textos) * len(perfils)
    i = 0

    for t in textos:
        for p in perfils:
            i += 1
            cas_id = f"{t['id']}__{p['id']}"

            existing = conn.execute(
                "SELECT id, text_adaptat FROM multi_llm_generations WHERE run_id=? AND cas_id=? AND generator=? AND prompt_mode='rag_v2'",
                (RUN_ID, cas_id, generator)
            ).fetchone()
            if existing and existing[1]:  # skip only if text_adaptat is non-empty
                print(f"  [{i:3d}/{total}] {cas_id} [{generator}] ja existeix, skip")
                continue
            elif existing:
                # Row with error — delete it to regenerate
                conn.execute("DELETE FROM multi_llm_generations WHERE run_id=? AND cas_id=? AND generator=? AND prompt_mode='rag_v2'",
                             (RUN_ID, cas_id, generator))

            print(f"  [{i:3d}/{total}] {cas_id} [{generator}] generant...", end=" ", flush=True)
            t0 = time.time()

            system_prompt, meta = build_rag_v2_prompt(p, t)
            user_prompt = f"Adapta el text següent:\n\n{t['text']}"

            text_adaptat = ""
            error = None
            try:
                text_adaptat = caller(system_prompt, user_prompt)
            except Exception as e:
                error = str(e)[:200]
                print(f"ERR: {error}")

            temps = round(time.time() - t0, 1)
            comps = detect_complements(text_adaptat) if text_adaptat else {}
            paraules = len(text_adaptat.split()) if text_adaptat else 0

            # Mètriques de forma
            try:
                from evaluator_metrics import evaluate_forma
                forma = evaluate_forma(text_adaptat, p["params"].get("mecr_sortida", "B2"))
            except Exception:
                forma = {}

            # Recall d'instruccions
            recall_val = None
            absents_val = None
            try:
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
                RUN_ID, cas_id, t["id"], p["id"], generator, "rag_v2",
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
                recall_val, absents_val, temps, error
            ))
            conn.commit()

            if text_adaptat:
                print(f"OK ({paraules} par, {temps}s)")
            time.sleep(API_DELAY)


# ═══════════════════════════════════════════════════════════════════════════════
# FASE 3: AVALUACIÓ INDIVIDUAL (rúbrica v2)
# ═══════════════════════════════════════════════════════════════════════════════

def run_evaluate(conn, judge: str, limit: int = 0):
    """Avaluació individual de totes les generacions multi_v2 (hc + rag_v1 + rag_v2)."""
    caller = JUDGE_CALLERS[judge]

    rows = conn.execute("""
        SELECT id, cas_id, generator, prompt_mode, text_adaptat, text_original,
               perfils_actius, mecr, dua, text_original_etapa, text_original_genere
        FROM multi_llm_generations
        WHERE run_id = ? AND text_adaptat IS NOT NULL AND text_adaptat != '' AND error IS NULL
        ORDER BY cas_id, generator, prompt_mode
    """, (RUN_ID,)).fetchall()
    cols = ["id","cas_id","generator","prompt_mode","text_adaptat","text_original",
            "perfils_actius","mecr","dua","etapa","genere"]

    total = len(rows)
    done = 0
    new_count = 0
    for i, row in enumerate(rows, 1):
        r = dict(zip(cols, row))

        existing = conn.execute(
            "SELECT id FROM multi_v2_evaluations WHERE run_id=? AND generation_id=? AND judge=?",
            (RUN_ID, r["id"], judge)
        ).fetchone()
        if existing:
            done += 1
            continue

        if limit > 0 and new_count >= limit:
            print(f"\n  [límit {limit} assolit, aturant]")
            break

        is_self = 1 if judge == r["generator"] else 0
        print(f"  [{i:4d}/{total}] {r['cas_id']} [{r['generator']}/{r['prompt_mode']}] jutge={judge}{'*' if is_self else ''} ...",
              end=" ", flush=True)

        user = EVAL_USER_TEMPLATE.format(
            perfils=r["perfils_actius"], mecr=r["mecr"], dua=r["dua"], etapa=r["etapa"],
            text_original=(r["text_original"] or "")[:1500],
            text_adaptat=(r["text_adaptat"] or "")[:3000],
        )

        try:
            result = _parse_json(caller(EVAL_SYSTEM_V2, user))
            scores = {}
            for c in ["A1","A2","A3","B1","B2","B3","B4","C1"]:
                v = result.get(c, {})
                scores[c] = {"p": v.get("p", 0) or 0, "j": v.get("j", "")}

            def s(c):
                return scores[c]["p"]

            pA = round((s("A1") + s("A2") + s("A3")) / 3, 2) if all(s(c) for c in ["A1","A2","A3"]) else 0
            pB = round((s("B1") + s("B2") + s("B3") + s("B4")) / 4, 2) if all(s(c) for c in ["B1","B2","B3","B4"]) else 0
            pC = s("C1")
            pG = round(pA * 0.3 + pB * 0.5 + pC * 0.2, 2) if pA and pB and pC else 0

            print(f"A={pA:.1f} B={pB:.1f} C={pC} G={pG:.2f}")

            conn.execute("""
                INSERT INTO multi_v2_evaluations (
                    run_id, cas_id, generation_id, judge,
                    a1_coherencia, a1_justificacio, a2_correccio, a2_justificacio,
                    a3_llegibilitat, a3_justificacio, b1_fidelitat, b1_justificacio,
                    b2_adequacio_perfil, b2_justificacio, b3_scaffolding, b3_justificacio,
                    b4_cultura, b4_justificacio, c1_potencial, c1_justificacio,
                    puntuacio_a, puntuacio_b, puntuacio_global, is_self_eval
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                RUN_ID, r["cas_id"], r["id"], judge,
                s("A1"), scores["A1"]["j"], s("A2"), scores["A2"]["j"],
                s("A3"), scores["A3"]["j"], s("B1"), scores["B1"]["j"],
                s("B2"), scores["B2"]["j"], s("B3"), scores["B3"]["j"],
                s("B4"), scores["B4"]["j"], s("C1"), scores["C1"]["j"],
                pA, pB, pG, is_self
            ))
            conn.commit()
            new_count += 1

        except Exception as e:
            print(f"ERR: {str(e)[:80]}")

        time.sleep(API_DELAY)

    if done:
        print(f"  ({done} ja avaluats, saltats)")


# ═══════════════════════════════════════════════════════════════════════════════
# FASE 4: COMPARACIÓ TRIO INTRA-MODEL (HC vs RAG-v1 vs RAG-v2)
# ═══════════════════════════════════════════════════════════════════════════════

BRANCH_ORDER = ["hc", "rag_v1", "rag_v2"]

def run_trio(conn, judge: str):
    """Trio intra-model: per cada (cas, generador), rànquing de HC vs RAG-v1 vs RAG-v2."""
    caller = JUDGE_CALLERS[judge]

    # Obtenir trios: per cada cas_id × generator, agafar les 3 branques
    trios_raw = conn.execute("""
        SELECT cas_id, generator,
               MAX(CASE WHEN prompt_mode='hc' THEN text_adaptat END) as text_hc,
               MAX(CASE WHEN prompt_mode='rag_v1' THEN text_adaptat END) as text_rag_v1,
               MAX(CASE WHEN prompt_mode='rag_v2' THEN text_adaptat END) as text_rag_v2,
               MAX(text_original) as text_original,
               MAX(perfils_actius) as perfils_actius,
               MAX(mecr) as mecr, MAX(dua) as dua,
               MAX(text_original_etapa) as etapa
        FROM multi_llm_generations
        WHERE run_id = ? AND generator IN ('gemini','sonnet','gpt')
          AND text_adaptat IS NOT NULL AND text_adaptat != '' AND error IS NULL
        GROUP BY cas_id, generator
        HAVING COUNT(DISTINCT prompt_mode) = 3
        ORDER BY cas_id, generator
    """, (RUN_ID,)).fetchall()

    tcols = ["cas_id","generator","text_hc","text_rag_v1","text_rag_v2",
             "text_original","perfils_actius","mecr","dua","etapa"]
    total = len(trios_raw)
    done = 0

    for i, row in enumerate(trios_raw, 1):
        r = dict(zip(tcols, row))

        existing = conn.execute(
            "SELECT id FROM multi_v2_trios WHERE run_id=? AND cas_id=? AND generator=? AND judge=?",
            (RUN_ID, r["cas_id"], r["generator"], judge)
        ).fetchone()
        if existing:
            done += 1
            continue

        is_self = 1 if judge == r["generator"] else 0

        # Randomitzar ordre (6 permutacions)
        branches = list(BRANCH_ORDER)
        random.shuffle(branches)
        label_map = {}  # "A" -> branch_name
        texts = {}
        for idx, branch in enumerate(branches):
            letter = chr(65 + idx)  # A, B, C
            label_map[letter] = branch
            texts[letter] = r[f"text_{branch}"]
        order_str = ",".join(f"{chr(65+i)}={b}" for i, b in enumerate(branches))

        print(f"  [{i:3d}/{total}] {r['cas_id']} [{r['generator']}] jutge={judge}{'*' if is_self else ''} ...",
              end=" ", flush=True)

        user = TRIO_USER_TEMPLATE.format(
            perfils=r["perfils_actius"], mecr=r["mecr"], dua=r["dua"], etapa=r["etapa"],
            text_original=(r["text_original"] or "")[:1200],
            text_a=(texts["A"] or "")[:2000],
            text_b=(texts["B"] or "")[:2000],
            text_c=(texts["C"] or "")[:2000],
        )

        try:
            result = _parse_json(caller(TRIO_SYSTEM_V2, user))

            def resolve_ranks(crit_data):
                """Converteix {"1st":"A","2nd":"C","3rd":"B"} a ranks per branca."""
                ranks = {"hc": 0, "rag_v1": 0, "rag_v2": 0}
                for pos, pos_name in [(1, "1st"), (2, "2nd"), (3, "3rd")]:
                    letter = crit_data.get(pos_name, "")
                    if letter in label_map:
                        ranks[label_map[letter]] = pos
                return ranks

            g = resolve_ranks(result.get("global", {}))
            b1 = resolve_ranks(result.get("B1", {}))
            b2 = resolve_ranks(result.get("B2", {}))
            b3 = resolve_ranks(result.get("B3", {}))
            c1 = resolve_ranks(result.get("C1", {}))

            winner = min(g, key=lambda k: g[k] if g[k] > 0 else 99)
            print(f"1r={winner} (hc={g['hc']} v1={g['rag_v1']} v2={g['rag_v2']})")

            conn.execute("""
                INSERT INTO multi_v2_trios (
                    run_id, cas_id, generator, judge, order_presented, is_self_eval,
                    global_hc, global_rag_v1, global_rag_v2, global_j,
                    b1_hc, b1_rag_v1, b1_rag_v2, b1_j,
                    b2_hc, b2_rag_v1, b2_rag_v2, b2_j,
                    b3_hc, b3_rag_v1, b3_rag_v2, b3_j,
                    c1_hc, c1_rag_v1, c1_rag_v2, c1_j
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                RUN_ID, r["cas_id"], r["generator"], judge, order_str, is_self,
                g["hc"], g["rag_v1"], g["rag_v2"], result.get("global",{}).get("j",""),
                b1["hc"], b1["rag_v1"], b1["rag_v2"], result.get("B1",{}).get("j",""),
                b2["hc"], b2["rag_v1"], b2["rag_v2"], result.get("B2",{}).get("j",""),
                b3["hc"], b3["rag_v1"], b3["rag_v2"], result.get("B3",{}).get("j",""),
                c1["hc"], c1["rag_v1"], c1["rag_v2"], result.get("C1",{}).get("j",""),
            ))
            conn.commit()

        except Exception as e:
            print(f"ERR: {str(e)[:80]}")

        time.sleep(API_DELAY)

    if done:
        print(f"  ({done} ja avaluats, saltats)")


# ═══════════════════════════════════════════════════════════════════════════════
# FASE 5: COMPARACIÓ CROSS-MODEL (parells RAG-v2)
# ═══════════════════════════════════════════════════════════════════════════════

CROSS_PAIRS = [
    ("gemini_vs_sonnet", "gemini", "sonnet"),
    ("gemini_vs_gpt",    "gemini", "gpt"),
    ("sonnet_vs_gpt",    "sonnet", "gpt"),
]

def run_cross(conn, judge: str):
    """Comparació cross-model: parells de RAG-v2 entre generadors."""
    caller = JUDGE_CALLERS[judge]

    for pair_id, model_a, model_b in CROSS_PAIRS:
        pairs = conn.execute("""
            SELECT g1.cas_id,
                   g1.text_adaptat as text_a, g2.text_adaptat as text_b,
                   g1.text_original, g1.perfils_actius, g1.mecr, g1.dua
            FROM multi_llm_generations g1
            JOIN multi_llm_generations g2
              ON g1.cas_id = g2.cas_id AND g1.run_id = g2.run_id
            WHERE g1.run_id = ? AND g1.prompt_mode = 'rag_v2' AND g2.prompt_mode = 'rag_v2'
              AND g1.generator = ? AND g2.generator = ?
              AND g1.text_adaptat != '' AND g2.text_adaptat != ''
              AND g1.error IS NULL AND g2.error IS NULL
            ORDER BY g1.cas_id
        """, (RUN_ID, model_a, model_b)).fetchall()

        pcols = ["cas_id","text_a","text_b","text_original","perfils_actius","mecr","dua"]
        total = len(pairs)
        print(f"\n  === {pair_id} ({total} parells) jutge={judge} ===")
        done = 0

        for i, row in enumerate(pairs, 1):
            r = dict(zip(pcols, row))

            existing = conn.execute(
                "SELECT id FROM multi_v2_cross WHERE run_id=? AND cas_id=? AND judge=? AND pair=?",
                (RUN_ID, r["cas_id"], judge, pair_id)
            ).fetchone()
            if existing:
                done += 1
                continue

            is_self = 1 if judge in (model_a, model_b) else 0

            # Randomitzar ordre
            if random.random() < 0.5:
                ta, tb, order = r["text_a"], r["text_b"], "a_first"
                la, lb = model_a, model_b
            else:
                ta, tb, order = r["text_b"], r["text_a"], "b_first"
                la, lb = model_b, model_a

            print(f"  [{i:3d}/{total}] {r['cas_id']} jutge={judge}{'*' if is_self else ''} ...",
                  end=" ", flush=True)

            user = CROSS_USER_TEMPLATE.format(
                perfils=r["perfils_actius"], mecr=r["mecr"], dua=r["dua"],
                text_original=(r["text_original"] or "")[:1000],
                text_a=(ta or "")[:2500],
                text_b=(tb or "")[:2500],
            )

            try:
                result = _parse_json(caller(CROSS_SYSTEM_V2, user))
                g = result.get("global", {})
                raw_winner = g.get("winner", "empat")

                def resolve(w):
                    if not w or w == "empat":
                        return "empat"
                    return la if w == "A" else lb

                winner = resolve(raw_winner)
                print(f"-> {winner}")

                conn.execute("""
                    INSERT INTO multi_v2_cross (
                        run_id, cas_id, judge, pair, model_a, model_b,
                        order_presented, is_self_eval,
                        global_winner, global_confidence, global_j,
                        b1_winner, b1_j, b2_winner, b2_j,
                        b3_winner, b3_j, c1_winner, c1_j
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """, (
                    RUN_ID, r["cas_id"], judge, pair_id, model_a, model_b,
                    order, is_self,
                    winner, g.get("confidence",""), g.get("j",""),
                    resolve(result.get("B1",{}).get("winner","")), result.get("B1",{}).get("j",""),
                    resolve(result.get("B2",{}).get("winner","")), result.get("B2",{}).get("j",""),
                    resolve(result.get("B3",{}).get("winner","")), result.get("B3",{}).get("j",""),
                    resolve(result.get("C1",{}).get("winner","")), result.get("C1",{}).get("j",""),
                ))
                conn.commit()

            except Exception as e:
                print(f"ERR: {str(e)[:80]}")

            time.sleep(API_DELAY)

        if done:
            print(f"  ({done} ja avaluats, saltats)")


# ═══════════════════════════════════════════════════════════════════════════════
# FASE 5: INFORME
# ═══════════════════════════════════════════════════════════════════════════════

def run_report(conn):
    """Imprimeix un resum dels resultats de multi_v2."""
    print("\n" + "="*70)
    print("INFORME multi_v2")
    print("="*70)

    # Generacions
    r = conn.execute("""
        SELECT prompt_mode, generator, COUNT(*) as n,
               SUM(CASE WHEN error IS NULL AND text_adaptat != '' THEN 1 ELSE 0 END) as ok,
               ROUND(AVG(text_adaptat_paraules),0) as avg_par
        FROM multi_llm_generations WHERE run_id=?
        GROUP BY prompt_mode, generator ORDER BY prompt_mode, generator
    """, (RUN_ID,)).fetchall()
    print("\n--- GENERACIONS ---")
    for row in r:
        print(f"  {row[0]:12s} {row[1]:8s}: {row[2]} total, {row[3]} OK, avg {row[4]} par")

    # Avaluació individual: nota per branca × jutge
    r = conn.execute("""
        SELECT g.prompt_mode, e.judge,
               ROUND(AVG(e.puntuacio_global),2) as global,
               ROUND(AVG(e.puntuacio_a),2) as dim_a,
               ROUND(AVG(e.puntuacio_b),2) as dim_b,
               ROUND(AVG(e.c1_potencial),2) as c1,
               COUNT(*) as n
        FROM multi_v2_evaluations e
        JOIN multi_llm_generations g ON e.generation_id = g.id
        WHERE e.run_id=?
        GROUP BY g.prompt_mode, e.judge
        ORDER BY global DESC
    """, (RUN_ID,)).fetchall()
    if r:
        print("\n--- NOTA PER BRANCA (rúbrica v2) ---")
        print(f"  {'Mode':12s} {'Jutge':10s} {'Global':>7} {'Dim-A':>7} {'Dim-B':>7} {'C1':>5} {'N':>5}")
        for row in r:
            print(f"  {row[0]:12s} {row[1]:10s} {row[2]:>7} {row[3]:>7} {row[4]:>7} {row[5]:>5} {row[6]:>5}")

    # Avaluació per branca × generador
    r = conn.execute("""
        SELECT g.prompt_mode, g.generator,
               ROUND(AVG(e.puntuacio_global),2) as global,
               COUNT(*) as n
        FROM multi_v2_evaluations e
        JOIN multi_llm_generations g ON e.generation_id = g.id
        WHERE e.run_id=?
        GROUP BY g.prompt_mode, g.generator
        ORDER BY g.generator, global DESC
    """, (RUN_ID,)).fetchall()
    if r:
        print("\n--- NOTA PER BRANCA × GENERADOR ---")
        print(f"  {'Mode':12s} {'Generator':10s} {'Global':>7} {'N':>5}")
        for row in r:
            print(f"  {row[0]:12s} {row[1]:10s} {row[2]:>7} {row[3]:>5}")

    # Trios: rànquing mitjà per branca
    r = conn.execute("""
        SELECT judge,
               ROUND(AVG(global_hc),2) as avg_hc,
               ROUND(AVG(global_rag_v1),2) as avg_v1,
               ROUND(AVG(global_rag_v2),2) as avg_v2,
               COUNT(*) as n
        FROM multi_v2_trios WHERE run_id=?
        GROUP BY judge
    """, (RUN_ID,)).fetchall()
    if r:
        print("\n--- TRIO INTRA-MODEL: RÀNQUING MITJÀ (1=millor, 3=pitjor) ---")
        print(f"  {'Jutge':10s} {'HC':>6} {'RAG-v1':>8} {'RAG-v2':>8} {'N':>5}")
        for row in r:
            print(f"  {row[0]:10s} {row[1]:>6} {row[2]:>8} {row[3]:>8} {row[4]:>5}")

    # Trios per generador
    r = conn.execute("""
        SELECT generator,
               ROUND(AVG(global_hc),2) as avg_hc,
               ROUND(AVG(global_rag_v1),2) as avg_v1,
               ROUND(AVG(global_rag_v2),2) as avg_v2,
               SUM(CASE WHEN global_rag_v2 = 1 THEN 1 ELSE 0 END) as v2_wins,
               COUNT(*) as n
        FROM multi_v2_trios WHERE run_id=?
        GROUP BY generator
    """, (RUN_ID,)).fetchall()
    if r:
        print("\n--- TRIO PER GENERADOR ---")
        print(f"  {'Generator':10s} {'HC':>6} {'RAG-v1':>8} {'RAG-v2':>8} {'v2 1r':>6} {'N':>5}")
        for row in r:
            print(f"  {row[0]:10s} {row[1]:>6} {row[2]:>8} {row[3]:>8} {row[4]:>6} {row[5]:>5}")

    # Cross-model
    r = conn.execute("""
        SELECT pair, global_winner, COUNT(*) as n
        FROM multi_v2_cross WHERE run_id=?
        GROUP BY pair, global_winner ORDER BY pair, n DESC
    """, (RUN_ID,)).fetchall()
    if r:
        print("\n--- CROSS-MODEL (RAG-v2) ---")
        current_pair = None
        for row in r:
            if row[0] != current_pair:
                current_pair = row[0]
                print(f"\n  {current_pair}:")
            print(f"    {row[1]:12s}: {row[2]:4d} victòries")

    print("\n" + "="*70)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="multi_v2 — Avaluació RAG-v2 vs HC i RAG-v1")
    parser.add_argument("--phase", required=True,
        choices=["init_db","copy_v1","generate","evaluate","trio","cross","report","all"])
    parser.add_argument("--generator", default="all",
        choices=["gemini","sonnet","gpt","gemma4","mistral","all"])
    parser.add_argument("--judge", default=None,
        choices=["gemini","gpt4mini","sonnet","gemma4","mistral"])
    parser.add_argument("--limit", type=int, default=0,
        help="Limita el nombre d'avaluacions noves (0 = sense límit)")
    args = parser.parse_args()

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")

    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)

    if args.phase in ("init_db", "all"):
        init_db(conn)

    if args.phase in ("copy_v1", "all"):
        copy_v1(conn)

    if args.phase in ("generate", "all"):
        gens = GENERATORS if args.generator == "all" else [args.generator]
        for gen in gens:
            print(f"\n=== GENERACIÓ RAG-v2 [{gen}] ===")
            run_generation(conn, gen, data)

    if args.phase in ("evaluate", "all"):
        judges = JUDGES if args.judge is None else [args.judge]
        for j in judges:
            print(f"\n=== AVALUACIÓ INDIVIDUAL [{j}] ===")
            run_evaluate(conn, j, limit=args.limit)

    if args.phase in ("trio", "all"):
        judges = JUDGES if args.judge is None else [args.judge]
        for j in judges:
            print(f"\n=== TRIO INTRA-MODEL [{j}] ===")
            run_trio(conn, j)

    if args.phase in ("cross", "all"):
        judges = JUDGES if args.judge is None else [args.judge]
        for j in judges:
            print(f"\n=== CROSS-MODEL [{j}] ===")
            run_cross(conn, j)

    if args.phase in ("report", "all"):
        run_report(conn)

    print("\nFet.")

    conn.close()
    print("\nFet.")
