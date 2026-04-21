"""Orquestrador del pipeline d'adaptació ATNE.

Aquest mòdul conté el nucli del flux end-to-end d'adaptació de text:
  1. Construcció del system prompt (capes DUA + instruccions + persona)
  2. Crida al LLM amb retry + Verify-and-Regenerate (jutge ràpid Q/P/C)
  3. Post-processament Python (UTF-16, typos, english, latex, concat…)
  4. Pipeline de qualitat català (LanguageTool + llegibilitat + auditor opt-in)
  5. Registre en buffer memòria + Supabase (fire-and-forget)
  6. Telemetria a atne_sessions

`run_adaptation` és l'entry point públic — server.py el re-exposa per mantenir
el contracte amb callers externs (snapshot_contract, tests, /api/adapt stream).

Extret de `server.py` (refactor 2026-04-21, Fase 3). Depèn de server.py per
tres peces de configuració runtime (lazy import per evitar circularitat):
- `_model_for` — resolució del model segons fase i rotació admin
- `_AUDITOR_ENABLED_RUNTIME` — flag dinàmic de l'auditor opcional
- `_persist_adaptation_to_supabase`, `_log_session`, `post_process_catalan`
"""

import re
import threading
import time

import instruction_filter
from adaptation.llm_clients import _call_llm, _resolve_model
from adaptation.post_process import (
    _post_process_llm_output,
    clean_gemini_output,
    post_process_adaptation,
)
from adaptation.prompt_builder import build_system_prompt


# ── Buffer d'inspecció d'adaptacions (només memòria) ───────────────────────
#
# S'omple a run_adaptation() i es llegeix des dels endpoints d'audit a
# server.py. Per garantir lectures sempre fresques tot i la reassignació
# de _ATNE_LAST_ADAPTATION, els callers han d'accedir-hi via atribut del
# mòdul (`from adaptation import orchestrator; orchestrator._ATNE_LAST_ADAPTATION`)
# i NO fer `from adaptation.orchestrator import _ATNE_LAST_ADAPTATION`
# (aquesta darrera crea una referència local que queda stale).

_ATNE_LAST_ADAPTATION: dict = {}
_ATNE_ADAPTATIONS_LOG: list = []  # més antiga primer (append); els nous al final
_ATNE_ADAPTATIONS_MAX = 20


# ── Verify: jutge ràpid post-adaptació ─────────────────────────────────────

VERIFY_SYSTEM = """Ets un avaluador pedagògic ràpid. Avalua una adaptació de text educatiu amb 3 criteris breus (1-5 cadascun):
- Q (Qualitat textual): coherència, correcció gramatical, llegibilitat
- P (Perfil): s'ha aplicat bé al perfil de l'alumne declarat
- C (Curricular): preserva el contingut original sense errors

Retorna NOMÉS aquest JSON:
{"Q":1-5,"P":1-5,"C":1-5,"j":"una frase justificació"}"""


def _verify_adaptation(active_model: str, text_original: str, text_adapted: str, profile: dict, params: dict):
    """Autoavaluació ràpida amb 3 criteris. Retorna (mitjana, info)."""
    import json as _json
    perfil_nom = profile.get("nom", "genèric")
    mecr = params.get("mecr_sortida", "B2")
    dua = params.get("dua", "Core")
    user_msg = (
        f"PERFIL: {perfil_nom} | MECR sortida: {mecr} | DUA: {dua}\n\n"
        f"TEXT ORIGINAL:\n{text_original[:2000]}\n\n"
        f"TEXT ADAPTAT:\n{text_adapted[:3000]}\n\n"
        f"Puntua Q, P, C (1-5). JSON nomes."
    )
    raw = _call_llm(active_model, VERIFY_SYSTEM, user_msg)
    m = re.search(r'\{[^}]*"Q"[^}]*\}', raw, re.DOTALL)
    if not m:
        raise RuntimeError(f"No s'ha trobat JSON a la resposta: {raw[:200]}")
    data = _json.loads(m.group(0))
    q = float(data.get("Q", 0))
    p = float(data.get("P", 0))
    c = float(data.get("C", 0))
    mitjana = (q + p + c) / 3.0
    return mitjana, {"Q": q, "P": p, "C": c, "j": data.get("j", "")}


# ── Pipeline principal: run_adaptation ─────────────────────────────────────

def run_adaptation(text: str, profile: dict, context: dict, params: dict,
                   progress_callback=None, model_override: str = None, docent_id: str = ""):
    """Executa tot el pipeline d'adaptació: instruccions graduades + LLM + Verify + Retry.

    RAG-KG desactivat (2026-04-09): les 98 instruccions graduades del catàleg
    cobreixen el 'què fer' de forma exhaustiva. El RAG recuperava documents
    irrellevants (M0, perfils equivocats) i el resultat era indistingible.
    La infraestructura RAG-KG (Supabase vectors + KG) es manté per a futur ús
    (diagnòstic, generació de material, recerca).
    """
    # Lazy import: server.py és fully-loaded quan aquesta funció s'executa.
    # L'evita en temps de càrrega del mòdul (server importa orchestrator).
    import server

    global _ATNE_LAST_ADAPTATION

    cb = progress_callback or (lambda ev: None)
    t_start = time.time()
    # Sprint 1B: el model de l'adapt es resol via _MODEL_CONFIG["adapt"]
    # (configurable des de /admin) amb override puntual via payload.model.
    active_model = server._model_for("adapt", override=model_override or "")

    # System prompt — sense RAG, les instruccions graduades són el motor
    cb({"type": "step", "step": "search", "msg": "Preparant instruccions d'adaptació..."})
    system_prompt = build_system_prompt(profile, context, params, rag_context="")
    _filtered = instruction_filter.get_instructions(profile, params)
    _instruction_ids = [
        instr["id"]
        for _macro in _filtered.get("macrodirectives", {}).values()
        for instr in _macro.get("instruccions", [])
    ]

    # Debug: desem el context de la darrera adaptació al buffer per poder
    # inspeccionar des de /api/audit/adaptations* (admin). Només memòria.
    _entry = {
        "id": f"adapt-{int(time.time() * 1000)}",  # timestamp ms com a id únic
        "ts": time.time(),
        "iso": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "docent_id": docent_id or "",
        "model": active_model,
        "profile": profile,
        "context": context,
        "params": params,
        "text_input": text,
        "text_input_len": len(text),
        "system_prompt": system_prompt,
        "system_prompt_len": len(system_prompt),
        "system_prompt_words": len(system_prompt.split()),
        "instruction_ids": _instruction_ids,
        "n_instructions": len(_instruction_ids),
        "adapted_output": "",  # s'emplena després
        "adapted_output_len": 0,
    }
    _ATNE_LAST_ADAPTATION = _entry  # backwards-compat
    _ATNE_ADAPTATIONS_LOG.append(_entry)
    if len(_ATNE_ADAPTATIONS_LOG) > _ATNE_ADAPTATIONS_MAX:
        _ATNE_ADAPTATIONS_LOG[:] = _ATNE_ADAPTATIONS_LOG[-_ATNE_ADAPTATIONS_MAX:]

    # 5. Cridar LLM segons active_model (amb Generate+Verify+Retry)
    _prov, _spec = _resolve_model(active_model)
    _labels = {
        "gemma-4-31b-it":       "Gemma 4 31B",
        "gemma-3-12b-it":       "Gemma 3 12B",
        "gemma-3-27b-it":       "Gemma 3 27B",
        "gemma-3n-e4b-it":      "Gemma 3n E4B",
        "gemini-2.5-flash":     "Gemini 2.5 Flash",
        "gpt-4o-mini":          "GPT-4o mini",
        "gpt-4o":               "GPT-4o",
        "gpt-4.1-mini":         "GPT-4.1 mini",
        "mistral-small-latest": "Mistral Small",
        "mistral-large-latest": "Mistral Large",
        "qwen/qwen3.5-27b":     "Qwen 3.5 27B",
        "qwen/qwen3.5-9b":      "Qwen 3.5 9B",
    }
    model_label = _labels.get(_spec, _spec)
    adapted = ""
    verify_enabled = params.get("verify_retry", True)  # per defecte ON
    min_score = 4.0
    max_attempts = 2 if verify_enabled else 1
    best_adapted = ""
    best_score = -1
    verify_info = None

    # Correccions de la rúbrica del docent (regeneració amb feedback)
    corrections = params.get("corrections") or []
    user_text = text
    if corrections:
        corrections_block = "\n".join(f"- {c}" for c in corrections)
        user_text = (
            f"{text}\n\n"
            f"IMPORTANT — CORRECCIONS DEL DOCENT (prioritat màxima):\n"
            f"L'adaptació anterior no era satisfactòria. Aplica aquestes correccions:\n"
            f"{corrections_block}"
        )
        cb({"type": "step", "step": "corrections", "msg": f"Aplicant {len(corrections)} correcció(ns) del docent..."})

    adapted_raw = None
    for attempt in range(1, max_attempts + 1):
        label_attempt = f" (intent {attempt}/{max_attempts})" if verify_enabled else ""
        cb({"type": "step", "step": "adapting", "msg": f"Generant adaptació amb {model_label}{label_attempt}..."})
        try:
            adapted_raw = _call_llm(active_model, system_prompt, user_text)
            adapted = clean_gemini_output(adapted_raw)
            adapted = _post_process_llm_output(adapted)
            # Diagnòstic verbós
            try:
                _comp_active = params.get("complements", {}) if isinstance(params, dict) else {}
                _lower = adapted.lower()
                _has_preg_raw = bool(re.search(r'^##\s*["\'`«»]*pregunt', adapted_raw or "", re.MULTILINE | re.IGNORECASE))
                _has_preg_clean = bool(re.search(r'^##\s+preguntes\s+de\s+comprensi', adapted, re.MULTILINE | re.IGNORECASE))
                _missing = []
                if _comp_active.get("preguntes_comprensio") and not _has_preg_clean:
                    _missing.append("preguntes_comprensio")
                if _comp_active.get("glossari") and "## glossari" not in _lower:
                    _missing.append("glossari")
                if _comp_active.get("esquema_visual") and not re.search(r'^##\s+esquema', adapted, re.MULTILINE | re.IGNORECASE):
                    _missing.append("esquema_visual")
                print(
                    f"[adapt] model={active_model} raw_len={len(adapted_raw or '')} "
                    f"clean_len={len(adapted)} preg_raw={_has_preg_raw} preg_clean={_has_preg_clean} "
                    f"missing={_missing} comp={_comp_active}",
                    flush=True,
                )
                if _missing:
                    _ts = int(time.time())
                    _path = f"tests/debug_adapt_{_ts}_{active_model.replace('/', '_')}.txt"
                    try:
                        with open(_path, "w", encoding="utf-8") as _f:
                            _f.write(f"### MODEL: {active_model}\n### PARAMS complements: {_comp_active}\n\n")
                            _f.write("=" * 40 + " RAW " + "=" * 40 + "\n")
                            _f.write(adapted_raw or "")
                            _f.write("\n\n" + "=" * 40 + " CLEAN " + "=" * 40 + "\n")
                            _f.write(adapted)
                        print(f"[adapt] Debug dump a {_path}", flush=True)
                    except Exception as _e:
                        print(f"[adapt] No s'ha pogut guardar dump: {_e}", flush=True)
            except Exception as _e:
                print(f"[adapt] diagnostic err: {_e}", flush=True)
        except Exception as e:
            adapted = f"Error en la generació ({active_model}): {e}"
            break

        if not verify_enabled:
            best_adapted = adapted
            break

        # VERIFY: jutge ràpid amb rúbrica simplificada
        cb({"type": "step", "step": "verifying", "msg": f"Autoavaluant qualitat (intent {attempt})..."})
        try:
            score, verify_info = _verify_adaptation(active_model, text, adapted, profile, params)
            cb({"type": "step", "step": "verify_result", "msg": f"Puntuació autoavaluació: {score:.1f}/5.0"})
        except Exception as e:
            cb({"type": "step", "step": "warning", "msg": f"Avís: autoavaluació fallida ({e}). Conservem aquesta versió."})
            best_adapted = adapted
            break

        if score > best_score:
            best_score = score
            best_adapted = adapted

        if score >= min_score:
            break  # OK

        if attempt < max_attempts:
            cb({"type": "step", "step": "retry", "msg": f"Qualitat < {min_score}. Regenerant..."})

    adapted = best_adapted if best_adapted else adapted

    # 6. Post-processament Python
    mecr = params.get("mecr_sortida", "B2")
    pp = post_process_adaptation(adapted, mecr)
    for w in pp.get("warnings", []):
        cb({"type": "step", "step": "warning", "msg": w})

    # 7. Pipeline de qualitat català (LanguageTool + llegibilitat + LLM Auditor)
    quality_enabled = params.get("quality_check", True)
    use_auditor = params.get("auditor")
    if use_auditor is None:
        use_auditor = server._AUDITOR_ENABLED_RUNTIME  # lectura dinàmica
    etapa_pp = context.get("etapa", "")
    quality = None
    if quality_enabled:
        cb({"type": "step", "step": "quality",
            "msg": "Verificant qualitat (LanguageTool + llegibilitat + auditor LLM)..."})
        try:
            quality = server.post_process_catalan(
                adapted,
                target_mecr=mecr,
                enable_lt=True,
                enable_auditor=bool(use_auditor),
                etapa=etapa_pp,
            )
            if quality["n_correccions"] > 0:
                adapted = quality["text"]
                cb({"type": "step", "step": "quality_ok",
                    "msg": f"LanguageTool: {quality['n_correccions']} correccions auto-aplicades"})
            if quality["paraules_sospitoses"]:
                cb({"type": "step", "step": "warning",
                    "msg": f"{len(quality['paraules_sospitoses'])} paraules sospitoses — revisa al Quality Report"})
            if not quality["llegibilitat"].get("ok", True):
                cb({"type": "step", "step": "warning",
                    "msg": quality["llegibilitat"].get("missatge", "Llegibilitat fora del llindar")})
            if quality["avisos_auditor"]:
                cb({"type": "step", "step": "warning",
                    "msg": f"Auditor LLM: {len(quality['avisos_auditor'])} avisos pedagògics"})
        except Exception as e:
            cb({"type": "step", "step": "warning", "msg": f"Quality check fallit: {e}"})

    result_ev = {"type": "result", "adapted": adapted, "post_process": pp}
    if verify_info is not None:
        result_ev["verify"] = {"score": best_score, **verify_info}
    # Debug: emplenar la sortida adaptada al registre en memòria + persistir
    # a Supabase perquè sobrevisqui canvis d'instància a Cloud Run.
    try:
        if _ATNE_LAST_ADAPTATION:
            _ATNE_LAST_ADAPTATION["adapted_output"] = adapted
            _ATNE_LAST_ADAPTATION["adapted_output_len"] = len(adapted)
            if adapted_raw is not None:
                _ATNE_LAST_ADAPTATION["adapted_raw"] = adapted_raw or ""
                _ATNE_LAST_ADAPTATION["adapted_raw_len"] = len(adapted_raw or "")
            # Persisteix a Supabase (fire-and-forget, en thread per no bloquejar SSE)
            try:
                threading.Thread(
                    target=server._persist_adaptation_to_supabase,
                    args=(dict(_ATNE_LAST_ADAPTATION),),
                    daemon=True,
                ).start()
            except Exception:
                pass
    except Exception:
        pass
    if quality is not None:
        result_ev["quality_report"] = {
            "n_correccions": quality["n_correccions"],
            "correccions": quality["correccions"][:20],
            "paraules_sospitoses": quality["paraules_sospitoses"][:20],
            "avisos_estil": quality["avisos_estil"][:10],
            "llegibilitat": quality["llegibilitat"],
            "avisos_auditor": quality["avisos_auditor"],
            "caracters_exotics": quality.get("caracters_exotics", []),
            "lt_disponible": quality["lt_disponible"],
            "auditor_disponible": quality["auditor_disponible"],
            "auditor_model": quality["auditor_model"],
        }
        if quality.get("caracters_exotics"):
            cb({"type": "step", "step": "warning",
                "msg": f"{len(quality['caracters_exotics'])} caràcter(s) exòtic(s) detectats — revisa al Quality Report"})
    cb(result_ev)
    cb({"type": "done"})

    # Telemetria pilot: log asíncron a atne_sessions (fire-and-forget)
    try:
        _raw_conds = profile.get("conditions") or profile.get("caracteristiques") or []
        if isinstance(_raw_conds, str):
            _conditions = [_raw_conds]
        elif isinstance(_raw_conds, dict):
            _conditions = [k for k, v in _raw_conds.items()
                           if isinstance(v, dict) and v.get("actiu")]
        else:
            _conditions = list(_raw_conds)
        threading.Thread(
            target=server._log_session,
            args=({
                "profile_type":    profile.get("profile_type") or profile.get("tipus") or "desconegut",
                "conditions":      list(_conditions),
                "etapa":           params.get("etapa", ""),
                "mecr_entrada":    params.get("mecr_base") or params.get("mecr", ""),
                "mecr_sortida":    params.get("mecr_sortida", ""),
                "model":           active_model,
                "instruction_ids": _instruction_ids,
                "n_instructions":  len(_instruction_ids),
                "latency_ms":      int((time.time() - t_start) * 1000),
                "input_chars":     len(text),
                "output_chars":    len(adapted),
                "verify_score":    best_score if verify_enabled and best_score >= 0 else None,
                "docent_id":       docent_id or None,
            },),
            daemon=True,
        ).start()
    except Exception as _te:
        print(f"[telemetria] error creant thread: {_te}", flush=True)

    return adapted
