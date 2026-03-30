"""
ATNE — Orquestrador d'avaluació A/B complet.

Executa tot el pipeline d'avaluació comparativa (Hardcoded vs RAG):
  1. Genera adaptacions amb les dues branques (cridant Gemini directament)
  2. Avalua BLOC 1-2 (Python: forma + recall)
  3. Avalua BLOC 3 (LLM judge: comparació)
  4. Emmagatzema tot a SQLite (eval_db)
  5. Exporta JSON

Ús:
    python tests/batch_eval.py                       # tots els casos
    python tests/batch_eval.py --perfil P1           # un sol perfil
    python tests/batch_eval.py --text PRI_EXPL       # un sol text
    python tests/batch_eval.py --dry-run             # mostra casos sense executar
    python tests/batch_eval.py --skip-generation     # avalua resultats existents
    python tests/batch_eval.py --notes "descripció"  # afegeix notes al run

Resultats:
    tests/results/evaluations.db         (SQLite acumulatiu)
    tests/results/{run_id}/summary.json  (resum del run)
    tests/results/{run_id}/cases/        (JSON per cas)
"""

import argparse
import io
import json
import os
import subprocess
import sys
import time
import importlib
import tempfile
import textwrap
from pathlib import Path

# Fix consola Windows (cp1252 no suporta caràcters especials)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP DE PATHS
# ═══════════════════════════════════════════════════════════════════════════════

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from dotenv import load_dotenv
load_dotenv()

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS DEL PROJECTE
# ═══════════════════════════════════════════════════════════════════════════════

import eval_db
from instruction_filter import get_instructions, format_instructions_for_prompt
from evaluator_metrics import (
    evaluate_blocs_1_2,
    extract_instruction_ids,
    evaluate_forma,
)
from evaluator_agent import build_eval_prompt, evaluate_case
import corpus_reader

# Inicialitzar corpus (necessari per build_system_prompt RAG)
corpus_reader.load_corpus()

# ═══════════════════════════════════════════════════════════════════════════════
# CLIENT GEMINI (generació d'adaptacions)
# ═══════════════════════════════════════════════════════════════════════════════

from google import genai
from google.genai import types

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL = "gemini-2.5-flash"

_gemini_client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options=types.HttpOptions(timeout=180_000),
)

# Retard entre crides per respectar la capa gratuita
API_DELAY_SECONDS = 2


def _call_gemini(system_prompt: str, user_text: str) -> str:
    """Crida a Gemini per generar una adaptació. Retorna el text generat."""
    response = _gemini_client.models.generate_content(
        model=MODEL,
        contents=f"TEXT ORIGINAL A ADAPTAR:\n\n{user_text}",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.4,
            max_output_tokens=16384,
            thinking_config=types.ThinkingConfig(thinking_budget=0),
        ),
    )
    return (response.text or "").strip()


# ═══════════════════════════════════════════════════════════════════════════════
# CARREGA DE prompt_blocks.py (BRANCA HARDCODED)
# ═══════════════════════════════════════════════════════════════════════════════

_prompt_blocks = None


def _load_prompt_blocks():
    """
    Carrega prompt_blocks.py: primer intenta import directe, si no,
    l'extreu de git (branca prompt-v2-hardcoded) i el carrega dinàmicament.
    """
    global _prompt_blocks

    # Intent 1: import directe (si estem en una branca que el té)
    try:
        import prompt_blocks
        _prompt_blocks = prompt_blocks
        print("[prompt_blocks] Carregat per import directe.")
        return
    except ImportError:
        pass

    # Intent 2: extreure de git
    print("[prompt_blocks] No disponible localment, extraient de git...")
    try:
        result = subprocess.run(
            ["git", "show", "prompt-v2-hardcoded:prompt_blocks.py"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=str(ROOT),
        )
        if result.returncode != 0:
            print(f"[prompt_blocks] ERROR git: {result.stderr.strip()}")
            return

        # Escriure a fitxer temporal i carregar com a mòdul
        tmp_dir = ROOT / "tests" / ".tmp"
        tmp_dir.mkdir(parents=True, exist_ok=True)
        tmp_file = tmp_dir / "prompt_blocks.py"
        tmp_file.write_text(result.stdout, encoding="utf-8")

        spec = importlib.util.spec_from_file_location("prompt_blocks", str(tmp_file))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _prompt_blocks = mod
        print(f"[prompt_blocks] Carregat des de git (prompt-v2-hardcoded).")
    except Exception as e:
        print(f"[prompt_blocks] ERROR carregant: {e}")


def _get_prompt_blocks():
    """Retorna el mòdul prompt_blocks, carregant-lo si cal."""
    if _prompt_blocks is None:
        _load_prompt_blocks()
    return _prompt_blocks


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTRUCCIÓ DE SYSTEM PROMPTS
# ═══════════════════════════════════════════════════════════════════════════════

def _flatten_profile_detalls(profile: dict) -> dict:
    """
    Aplana les sub-variables de 'detalls' al nivell arrel de cada característica.

    test_data.json usa:
        {"nouvingut": {"actiu": true, "detalls": {"L1": "àrab", ...}}}

    Però instruction_filter espera:
        {"nouvingut": {"actiu": true, "L1": "àrab", ...}}
    """
    chars = profile.get("caracteristiques", {})
    flat_chars = {}
    for key, val in chars.items():
        flat = dict(val)
        detalls = flat.pop("detalls", {})
        if detalls:
            flat.update(detalls)
        flat_chars[key] = flat
    return {"caracteristiques": flat_chars}


def _get_active_profiles(profile: dict) -> list[str]:
    """Retorna les claus dels perfils actius."""
    chars = profile.get("caracteristiques", {})
    return [key for key, val in chars.items() if val.get("actiu")]


def build_hardcoded_prompt(profile: dict, context: dict, params: dict) -> str:
    """
    Construeix el system prompt de la branca Hardcoded (4 capes constants).

    Capa 1: IDENTITY_BLOCK
    Capa 2: UNIVERSAL_RULES_BLOCK
    Capa 3: MECR + DUA + PROFILE + GENRE + CROSSINGS + COGNITIVE_LOAD + CONFLICT
    Capa 4: context + persona
    """
    pb = _get_prompt_blocks()
    if pb is None:
        return "(ERROR: prompt_blocks.py no disponible)"

    parts = []
    mecr = params.get("mecr_sortida", "B2")
    dua = params.get("dua", "Core")
    genre = params.get("genere_discursiu", "")
    active = _get_active_profiles(profile)

    # ── Capa 1: Identitat ──
    parts.append(pb.IDENTITY_BLOCK)

    # ── Capa 2: Regles universals ──
    parts.append(pb.UNIVERSAL_RULES_BLOCK)

    # ── Capa 3a: MECR ──
    mecr_block = pb.MECR_BLOCKS.get(mecr, "")
    if mecr_block:
        parts.append(mecr_block)

    # ── Capa 3b: DUA ──
    dua_block = pb.DUA_BLOCKS.get(dua, "")
    if dua_block:
        parts.append(dua_block)

    # ── Capa 3c: Gènere ──
    if genre:
        genre_block = pb.GENRE_BLOCKS.get(genre, "")
        if genre_block:
            parts.append(genre_block)

    # ── Capa 3d: Perfils ──
    for pkey in active:
        profile_block = pb.PROFILE_BLOCKS.get(pkey, "")
        if profile_block:
            parts.append(profile_block)

    # ── Capa 3e: Creuaments ──
    if len(active) >= 2:
        crossing_blocks = getattr(pb, "CROSSING_BLOCKS", {})
        for pair_key, block_text in crossing_blocks.items():
            if isinstance(pair_key, tuple) and all(p in active for p in pair_key):
                parts.append(block_text)

    # ── Capa 3f: Càrrega cognitiva ──
    cog_blocks = getattr(pb, "COGNITIVE_LOAD_BLOCK", {})
    if mecr in ("pre-A1", "A1"):
        cog = cog_blocks.get("low", "")
    elif mecr in ("A2", "B1"):
        cog = cog_blocks.get("mid", "")
    else:
        cog = cog_blocks.get("high", "")
    if cog:
        parts.append(cog)

    # ── Capa 3g: Resolució conflictes ──
    if mecr in ("pre-A1", "A1", "A2") or dua == "Acces":
        conflict = getattr(pb, "CONFLICT_RESOLUTION_BLOCK", "")
        if conflict:
            parts.append(conflict)

    # ── Capa 3h: Few-shot ──
    fewshot_examples = getattr(pb, "FEWSHOT_EXAMPLES", {})
    fewshot = fewshot_examples.get(mecr, "")
    if fewshot:
        parts.append(fewshot)

    # ── Capa 4: Context ──
    parts.append(f"""CONTEXT EDUCATIU:
- Etapa: {context.get('etapa', 'ESO')}
- Curs: {context.get('curs', '')}
- Materia: {context.get('materia', '')}""")

    # Persona-audience
    persona_parts = [f"Escrius per a un alumne de {context.get('etapa', 'ESO')}"]
    curs = context.get("curs", "")
    if curs:
        persona_parts.append(f"({curs})")
    for pkey in active:
        persona_parts.append(f"amb {pkey.replace('_', ' ')}")
    persona_parts.append(f"Nivell MECR: {mecr}.")
    parts.append("PERSONA-AUDIENCE:\n" + " ".join(persona_parts))

    return "\n\n".join(parts)


def build_rag_prompt(profile: dict, context: dict, params: dict) -> str:
    """
    Construeix el system prompt de la branca RAG (instruccions filtrades del catàleg).

    Replica la lògica de server.py build_system_prompt(), sense cerca RAG/KG real
    (el context RAG s'omet en mode test, com fa batch_test.py).
    """
    flat_profile = _flatten_profile_detalls(profile)
    mecr = params.get("mecr_sortida", "B2")
    dua = params.get("dua", "Core")
    genre = params.get("genere_discursiu", "")
    active = _get_active_profiles(flat_profile)

    parts = []

    # Capa 1: Identitat
    parts.append(corpus_reader.get_identity())

    # Capes 2-3: Instruccions filtrades
    filtered = get_instructions(flat_profile, params)
    instructions_text = format_instructions_for_prompt(filtered)
    parts.append(instructions_text)

    # DUA bloc del corpus
    dua_block = corpus_reader.get_dua_block(dua)
    if dua_block:
        parts.append(dua_block)

    # Gènere discursiu
    if genre:
        genre_block = corpus_reader.get_genre_block(genre)
        if genre_block:
            parts.append(genre_block)

    # Creuaments
    crossing_blocks = corpus_reader.get_crossing_blocks(active)
    for cb_text in crossing_blocks:
        parts.append(cb_text)

    # Resolució conflictes
    if mecr in ("pre-A1", "A1", "A2") or dua == "Acces":
        conflict = corpus_reader.get_conflict_resolution()
        if conflict:
            parts.append(conflict)

    # Few-shot
    fewshot = corpus_reader.get_fewshot_example(mecr)
    if fewshot:
        parts.append(f"EXEMPLE DE SORTIDA ESPERADA ({mecr}):\n{fewshot}")

    # Capa 4: Context
    parts.append(f"""CONTEXT EDUCATIU:
- Etapa: {context.get('etapa', 'ESO')}
- Curs: {context.get('curs', '')}
- Materia: {context.get('materia', '')}""")

    # Persona-audience
    persona_parts = [f"Escrius per a un alumne de {context.get('etapa', 'ESO')}"]
    curs = context.get("curs", "")
    if curs:
        persona_parts.append(f"({curs})")
    for pkey in active:
        persona_parts.append(f"amb {pkey.replace('_', ' ')}")
    persona_parts.append(f"Nivell MECR: {mecr}.")
    parts.append("PERSONA-AUDIENCE:\n" + " ".join(persona_parts))

    return "\n\n".join(parts)


# ═══════════════════════════════════════════════════════════════════════════════
# CARREGA DE DADES
# ═══════════════════════════════════════════════════════════════════════════════

def load_test_data() -> dict:
    """Carrega la matriu de tests des de test_data.json."""
    data_path = ROOT / "tests" / "test_data.json"
    with open(data_path, encoding="utf-8") as f:
        return json.load(f)


# ═══════════════════════════════════════════════════════════════════════════════
# PIPELINE PER A UN SOL CAS
# ═══════════════════════════════════════════════════════════════════════════════

def _build_case_data(
    cas_id: str,
    branca: str,
    text_entry: dict,
    perfil_entry: dict,
    system_prompt: str,
    text_adaptat: str,
    forma_result: dict,
    retrieval_result: dict | None,
    filter_stats: dict | None,
    temps: float,
) -> dict:
    """Munta el dict per a insert_case d'eval_db."""
    params = perfil_entry["params"]
    profile = perfil_entry["profile"]
    flat_profile = _flatten_profile_detalls(profile)
    active = _get_active_profiles(flat_profile)

    data = {
        "cas_id": cas_id,
        "branca": branca,
        "text_id": text_entry["id"],
        "perfil_id": perfil_entry["id"],
        "etapa": text_entry["etapa"],
        "genere": text_entry["genere"],
        "mecr": params.get("mecr_sortida", "B2"),
        "dua": params.get("dua", "Core"),
        "perfils_actius": active,
        # Retrieval (nomes RAG)
        "recall": retrieval_result.get("recall") if retrieval_result else None,
        "instruccions_absents": retrieval_result.get("absents") if retrieval_result else None,
        # Forma
        "f1_longitud_frase": forma_result.get("F1_longitud_frase"),
        "f2_titols": forma_result.get("F2_titols"),
        "f3_negretes": forma_result.get("F3_negretes"),
        "f4_llistes": forma_result.get("F4_llistes"),
        "f5_prellico": forma_result.get("F5_prellico_present"),
        "puntuacio_forma": forma_result.get("puntuacio_forma"),
        # Filter stats (nomes RAG)
        "total_instruccions_enviades": (filter_stats or {}).get("total_enviades"),
        "instruccions_sempre": (filter_stats or {}).get("sempre"),
        "instruccions_nivell": (filter_stats or {}).get("nivell"),
        "instruccions_perfil": (filter_stats or {}).get("perfil"),
        "instruccions_condicional": (filter_stats or {}).get("perfil_condicional"),
        "instruccions_suprimides": (filter_stats or {}).get("suprimides"),
        # Prompt i sortida
        "system_prompt_length": len(system_prompt),
        "text_adaptat_length": len(text_adaptat),
        "text_adaptat": text_adaptat,
        "temps_generacio": round(temps, 2),
    }
    return data


def _populate_llm_scores(case_data: dict, eval_scores: dict) -> dict:
    """Afegeix les puntuacions C1-C6 de l'avaluador LLM al case_data."""
    for cx in ("C1", "C2", "C3", "C4", "C5", "C6"):
        score_data = eval_scores.get(cx, {})
        col_p = {
            "C1": "c1_coherencia",
            "C2": "c2_adequacio_perfil",
            "C3": "c3_preservacio_curricular",
            "C4": "c4_adequacio_mecr",
            "C5": "c5_prellico_funcional",
            "C6": "c6_coherencia_creuament",
        }[cx]
        col_j = col_p.replace("c1_", "c1_justificacio").replace(
            "c2_", "c2_justificacio").replace(
            "c3_", "c3_justificacio").replace(
            "c4_", "c4_justificacio").replace(
            "c5_", "c5_justificacio").replace(
            "c6_", "c6_justificacio")
        # Mes net:
        col_j = col_p.rsplit("_", 1)[0] + "_justificacio" if "_" in col_p else col_p + "_justificacio"
        case_data[col_p] = score_data.get("p")
        case_data[col_j] = score_data.get("j", "")
    case_data["puntuacio_fons"] = eval_scores.get("puntuacio_fons")
    return case_data


def run_full_case(
    text_entry: dict,
    perfil_entry: dict,
    case_index: int,
    total_cases: int,
    skip_generation: bool = False,
    existing_results: dict | None = None,
) -> dict:
    """
    Executa el pipeline complet per a un cas (text x perfil).

    Retorna dict amb:
        cas_id, prompt_hc, text_hc, prompt_rag, text_rag,
        forma_hc, forma_rag, retrieval_rag, filter_stats,
        hc_case_data, rag_case_data
    """
    text_id = text_entry["id"]
    perfil_id = perfil_entry["id"]
    cas_id = f"{text_id}__{perfil_id}"
    params = dict(perfil_entry["params"])
    params["genere_discursiu"] = text_entry["genere"]
    context = dict(perfil_entry["context"])
    context["etapa"] = text_entry["etapa"]
    profile = perfil_entry["profile"]
    flat_profile = _flatten_profile_detalls(profile)
    active = _get_active_profiles(flat_profile)
    mecr = params.get("mecr_sortida", "B2")
    text_original = text_entry["text"]

    result = {"cas_id": cas_id, "text_id": text_id, "perfil_id": perfil_id}

    # ── PAS 1-2: Construir system prompts ──
    prompt_hc = build_hardcoded_prompt(profile, context, params)
    prompt_rag = build_rag_prompt(profile, context, params)
    result["prompt_hc"] = prompt_hc
    result["prompt_rag"] = prompt_rag

    # Instruccions filtrades (per retrieval recall)
    filtered = get_instructions(flat_profile, params)
    result["filter_stats"] = filtered.get("stats", {})

    # ── PAS 3-4: Generar adaptacions ──
    if skip_generation and existing_results:
        text_hc = existing_results.get("text_hc", "")
        text_rag = existing_results.get("text_rag", "")
        temps_hc = existing_results.get("temps_hc", 0)
        temps_rag = existing_results.get("temps_rag", 0)
    else:
        # Hardcoded
        label_hc = f"[{case_index}/{total_cases}] {cas_id} (HC)"
        print(f"  {label_hc} ...", end=" ", flush=True)
        t0 = time.time()
        try:
            text_hc = _call_gemini(prompt_hc, text_original)
        except Exception as e:
            text_hc = f"ERROR: {e}"
            print(f"ERROR: {e}")
        temps_hc = time.time() - t0
        status_hc = f"{len(text_hc.split())}w {temps_hc:.1f}s"
        print(status_hc)
        time.sleep(API_DELAY_SECONDS)

        # RAG
        label_rag = f"[{case_index}/{total_cases}] {cas_id} (RAG)"
        print(f"  {label_rag} ...", end=" ", flush=True)
        t0 = time.time()
        try:
            text_rag = _call_gemini(prompt_rag, text_original)
        except Exception as e:
            text_rag = f"ERROR: {e}"
            print(f"ERROR: {e}")
        temps_rag = time.time() - t0
        status_rag = f"{len(text_rag.split())}w {temps_rag:.1f}s"
        print(status_rag)
        time.sleep(API_DELAY_SECONDS)

    result["text_hc"] = text_hc
    result["text_rag"] = text_rag
    result["temps_hc"] = temps_hc
    result["temps_rag"] = temps_rag

    # ── PAS 5: BLOC 1-2 (Python) ──
    # Forma per a ambdues branques
    forma_hc = evaluate_forma(text_hc, mecr)
    forma_rag = evaluate_forma(text_rag, mecr)
    result["forma_hc"] = forma_hc
    result["forma_rag"] = forma_rag

    # Retrieval recall (nomes RAG — la branca HC no usa instruction_filter)
    blocs_rag = evaluate_blocs_1_2(text_rag, mecr, active, filtered)
    result["retrieval_rag"] = blocs_rag["retrieval"]

    # ── Muntar case_data per a la BD ──
    result["hc_case_data"] = _build_case_data(
        cas_id=cas_id, branca="hardcoded",
        text_entry=text_entry, perfil_entry=perfil_entry,
        system_prompt=prompt_hc, text_adaptat=text_hc,
        forma_result=forma_hc, retrieval_result=None,
        filter_stats=None, temps=temps_hc,
    )
    result["rag_case_data"] = _build_case_data(
        cas_id=cas_id, branca="rag",
        text_entry=text_entry, perfil_entry=perfil_entry,
        system_prompt=prompt_rag, text_adaptat=text_rag,
        forma_result=forma_rag, retrieval_result=blocs_rag["retrieval"],
        filter_stats=blocs_rag.get("filter_stats"), temps=temps_rag,
    )

    return result


# ═══════════════════════════════════════════════════════════════════════════════
# BLOC 3: AVALUACIÓ LLM JUDGE (COMPARACIÓ)
# ═══════════════════════════════════════════════════════════════════════════════

def run_llm_evaluation(case_result: dict, text_entry: dict, perfil_entry: dict) -> dict:
    """
    Envia el cas a l'avaluador LLM (BLOC 3) i retorna la resposta.

    Retorna dict amb 'eval_json' (resposta de l'avaluador) i
    'hc_case_data'/'rag_case_data' actualitzats amb les puntuacions C1-C6.
    """
    cas_id = case_result["cas_id"]
    params = perfil_entry["params"]
    flat_profile = _flatten_profile_detalls(perfil_entry["profile"])
    active = _get_active_profiles(flat_profile)

    # Construir prompt d'avaluació
    user_prompt = build_eval_prompt(
        cas_id=cas_id,
        perfils_actius=active,
        mecr=params.get("mecr_sortida", "B2"),
        dua=params.get("dua", "Core"),
        etapa=text_entry["etapa"],
        genere=text_entry["genere"],
        text_original=text_entry["text"],
        prompt_hardcoded=case_result["prompt_hc"][:3000],  # Truncar per tokens
        text_hardcoded=case_result["text_hc"],
        forma_hardcoded=case_result["forma_hc"],
        prompt_rag=case_result["prompt_rag"][:3000],
        text_rag=case_result["text_rag"],
        forma_rag=case_result["forma_rag"],
        recall_rag=case_result["retrieval_rag"].get("recall", 0),
    )

    print(f"  [{cas_id}] BLOC 3 (LLM judge) ...", end=" ", flush=True)
    t0 = time.time()
    eval_json = evaluate_case(user_prompt)
    elapsed = time.time() - t0

    if "error" in eval_json:
        print(f"ERROR: {eval_json.get('error', '')[:80]}")
    else:
        veredicte = eval_json.get("comparacio", {}).get("veredicte", "?")
        print(f"veredicte={veredicte} ({elapsed:.1f}s)")

    time.sleep(API_DELAY_SECONDS)

    # ── Actualitzar case_data amb puntuacions LLM ──
    avaluacio = eval_json.get("avaluacio", {})

    hc_scores = avaluacio.get("hardcoded", {})
    if hc_scores:
        _populate_llm_scores(case_result["hc_case_data"], hc_scores)

    rag_scores = avaluacio.get("rag", {})
    if rag_scores:
        _populate_llm_scores(case_result["rag_case_data"], rag_scores)

    # ── Dades de comparació ──
    comparacio = eval_json.get("comparacio", {})
    auditoria = eval_json.get("auditoria_prompt", {})
    comparison_data = {
        "cas_id": cas_id,
        "text_id": case_result["text_id"],
        "perfil_id": case_result["perfil_id"],
        "millor_forma": comparacio.get("millor_forma"),
        "motiu_forma": comparacio.get("motiu_forma"),
        "millor_fons": comparacio.get("millor_fons"),
        "motiu_fons": comparacio.get("motiu_fons"),
        "veredicte": comparacio.get("veredicte"),
        "motiu_veredicte": comparacio.get("motiu_veredicte"),
        "prompt_hc_coherent": 1 if auditoria.get("hardcoded", {}).get("coherent_amb_perfil") else 0,
        "prompt_rag_coherent": 1 if auditoria.get("rag", {}).get("coherent_amb_perfil") else 0,
    }

    return {
        "eval_json": eval_json,
        "comparison_data": comparison_data,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTACIÓ JSON
# ═══════════════════════════════════════════════════════════════════════════════

def save_case_json(output_dir: Path, cas_id: str, case_result: dict, eval_result: dict | None):
    """Guarda el JSON complet d'un cas individual."""
    cases_dir = output_dir / "cases"
    cases_dir.mkdir(parents=True, exist_ok=True)

    export = {
        "cas_id": cas_id,
        "prompt_hc": case_result.get("prompt_hc", ""),
        "prompt_rag": case_result.get("prompt_rag", ""),
        "text_hc": case_result.get("text_hc", ""),
        "text_rag": case_result.get("text_rag", ""),
        "forma_hc": case_result.get("forma_hc"),
        "forma_rag": case_result.get("forma_rag"),
        "retrieval_rag": case_result.get("retrieval_rag"),
        "filter_stats": case_result.get("filter_stats"),
    }
    if eval_result:
        export["eval_llm"] = eval_result.get("eval_json")
        export["comparison"] = eval_result.get("comparison_data")

    filepath = cases_dir / f"{cas_id}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(export, f, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="ATNE — Orquestrador d'avaluacio A/B complet"
    )
    parser.add_argument("--perfil", type=str, default="",
                        help="Filtra per perfil_id (p.ex. P1)")
    parser.add_argument("--text", type=str, default="",
                        help="Filtra per text_id (p.ex. PRI_EXPL)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Mostra casos sense executar")
    parser.add_argument("--skip-generation", action="store_true",
                        help="Nomes avalua, no genera (requereix resultats existents)")
    parser.add_argument("--skip-llm-eval", action="store_true",
                        help="Genera adaptacions pero no executa BLOC 3 (LLM judge)")
    parser.add_argument("--notes", type=str, default="",
                        help="Notes descriptives del run")
    args = parser.parse_args()

    # ── Carregar dades ──
    data = load_test_data()
    textos = data["textos"]
    perfils = data["perfils"]

    # ── Filtres ──
    if args.text:
        textos = [t for t in textos if t["id"] == args.text]
        if not textos:
            print(f"ERROR: text_id '{args.text}' no trobat a test_data.json")
            sys.exit(1)
    if args.perfil:
        perfils = [p for p in perfils if p["id"] == args.perfil]
        if not perfils:
            print(f"ERROR: perfil_id '{args.perfil}' no trobat a test_data.json")
            sys.exit(1)

    # Generar matriu de casos
    cases = [(t, p) for t in textos for p in perfils]
    total = len(cases)

    print("=" * 60)
    print("  ATNE — Avaluacio A/B (Hardcoded vs RAG)")
    print("=" * 60)
    print(f"  Textos: {len(textos)} | Perfils: {len(perfils)} | Casos: {total}")
    if args.notes:
        print(f"  Notes: {args.notes}")
    print()

    # ── Dry run ──
    if args.dry_run:
        for i, (t, p) in enumerate(cases, 1):
            active = _get_active_profiles(
                _flatten_profile_detalls(p["profile"]))
            mecr = p["params"].get("mecr_sortida", "B2")
            dua = p["params"].get("dua", "Core")
            print(f"  [{i:3d}] {t['id']:12s} x {p['id']:4s} "
                  f"({', '.join(active)}) MECR={mecr} DUA={dua}")
        print(f"\n  --dry-run: {total} casos preparats, cap executat.")
        return

    # ── Carregar prompt_blocks ──
    _load_prompt_blocks()
    if _prompt_blocks is None:
        print("\nAVIS: prompt_blocks.py no disponible. La branca Hardcoded generara prompts buits.")
        print("      Continuar? (s/n) ", end="", flush=True)
        resp = input().strip().lower()
        if resp != "s":
            print("Avortat.")
            return

    # ── Inicialitzar BD ──
    conn = eval_db.init_db()
    run_id = eval_db.create_run(
        conn,
        notes=args.notes,
        total_cases=total,
    )
    print(f"  Run ID: {run_id}")

    # Directori de sortida
    output_dir = ROOT / "tests" / "results" / run_id
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"  Resultats: {output_dir}")
    print()

    # ── Executar pipeline ──
    all_results = []
    errors_gen = 0
    errors_eval = 0
    t_total = time.time()

    for i, (t, p) in enumerate(cases, 1):
        # ── PAS 1-5: Generacio + BLOC 1-2 ──
        try:
            case_result = run_full_case(
                text_entry=t,
                perfil_entry=p,
                case_index=i,
                total_cases=total,
                skip_generation=args.skip_generation,
            )
        except Exception as e:
            print(f"  ERROR [{t['id']}__{p['id']}]: {e}")
            errors_gen += 1
            continue

        # Comprovar errors de generacio
        has_gen_error = (
            case_result["text_hc"].startswith("ERROR") or
            case_result["text_rag"].startswith("ERROR")
        )
        if has_gen_error:
            errors_gen += 1

        # ── PAS 6: BLOC 3 (LLM judge) ──
        eval_result = None
        if not args.skip_llm_eval and not has_gen_error:
            try:
                eval_result = run_llm_evaluation(case_result, t, p)
            except Exception as e:
                print(f"  ERROR EVAL [{case_result['cas_id']}]: {e}")
                errors_eval += 1

        # ── PAS 7: Emmagatzemar a BD ──
        try:
            # Inserir cas HC
            eval_db.insert_case(conn, run_id, case_result["hc_case_data"])
            # Inserir cas RAG
            eval_db.insert_case(conn, run_id, case_result["rag_case_data"])
            # Inserir comparacio
            if eval_result and eval_result.get("comparison_data"):
                eval_db.insert_comparison(conn, run_id, eval_result["comparison_data"])
        except Exception as e:
            print(f"  ERROR BD [{case_result['cas_id']}]: {e}")

        # ── PAS 8: Guardar JSON individual ──
        save_case_json(output_dir, case_result["cas_id"], case_result, eval_result)

        all_results.append({
            "cas_id": case_result["cas_id"],
            "text_id": case_result["text_id"],
            "perfil_id": case_result["perfil_id"],
            "forma_hc": case_result["forma_hc"].get("puntuacio_forma"),
            "forma_rag": case_result["forma_rag"].get("puntuacio_forma"),
            "recall_rag": case_result["retrieval_rag"].get("recall"),
            "veredicte": (eval_result or {}).get("comparison_data", {}).get("veredicte"),
            "error_gen": has_gen_error,
        })

    elapsed_total = time.time() - t_total

    # ── Exportar JSON resum ──
    try:
        full_export = eval_db.export_run_json(conn, run_id)
        summary_path = output_dir / "summary.json"
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(full_export, f, ensure_ascii=False, indent=2, default=str)
        print(f"\n  Resum exportat: {summary_path}")
    except Exception as e:
        print(f"\n  ERROR exportant resum: {e}")

    # ── Resum consola ──
    ok_results = [r for r in all_results if not r["error_gen"]]
    veredictes = {}
    for r in ok_results:
        v = r.get("veredicte") or "sense_eval"
        veredictes[v] = veredictes.get(v, 0) + 1

    avg_forma_hc = (
        sum(r["forma_hc"] for r in ok_results if r["forma_hc"] is not None) /
        max(1, sum(1 for r in ok_results if r["forma_hc"] is not None))
    )
    avg_forma_rag = (
        sum(r["forma_rag"] for r in ok_results if r["forma_rag"] is not None) /
        max(1, sum(1 for r in ok_results if r["forma_rag"] is not None))
    )
    avg_recall = (
        sum(r["recall_rag"] for r in ok_results if r["recall_rag"] is not None) /
        max(1, sum(1 for r in ok_results if r["recall_rag"] is not None))
    )

    print()
    print("=" * 60)
    print("  RESUM DEL RUN")
    print("=" * 60)
    print(f"  Run ID:           {run_id}")
    print(f"  Casos totals:     {total}")
    print(f"  Casos OK:         {len(ok_results)}")
    print(f"  Errors generacio: {errors_gen}")
    print(f"  Errors avaluacio: {errors_eval}")
    print(f"  Temps total:      {elapsed_total:.0f}s ({elapsed_total/60:.1f}min)")
    print()
    print(f"  Forma HC (mitjana):   {avg_forma_hc:.3f}")
    print(f"  Forma RAG (mitjana):  {avg_forma_rag:.3f}")
    print(f"  Recall RAG (mitjana): {avg_recall:.3f}")
    print()
    print("  Veredictes:")
    for v, n in sorted(veredictes.items()):
        pct = n / max(1, len(ok_results)) * 100
        print(f"    {v:12s}: {n:3d} ({pct:.0f}%)")
    print()
    print(f"  BD:   {eval_db.DB_PATH}")
    print(f"  JSON: {output_dir}")
    print("=" * 60)

    conn.close()


if __name__ == "__main__":
    main()
