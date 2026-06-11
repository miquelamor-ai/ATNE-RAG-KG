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

import os
import re
import threading
import time

import instruction_filter
from adaptation.llm_clients import _call_llm, _call_llm_raw, _call_llm_stream, _resolve_model
from adaptation.post_process import (
    _post_process_llm_output,
    clean_gemini_output,
    post_process_adaptation,
)
from adaptation.pricing import estimate_cost_eur
from adaptation.prompt_builder import (
    build_system_prompt,
    build_complements_prompt,
    build_argumentacio_prompt,
)


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

VERIFY_SYSTEM = """Ets un avaluador pedagògic rigorós ancorat al model MALL/FJE. Avalua una adaptació de text educatiu amb 3 criteris (1-5):

- Q (Qualitat MALL): compleix les regles UNE 153101 i les del nivell MECR? Mira:
  * DUA Accés/A1/A2: NO parèntesi a definicions, NO punt i coma, NO el·lipsis, NO MAJÚSCULES, NO veu passiva reflexa
  * Frases ≤12p a A1/A2, ≤18p a B1, ≤25p a B2
  * NO paraules genèriques ("cosa", "un tipus de", "serveix per") a DUA Accés
  Penalitza si veus aquestes violacions. Q=5 només si NO en veus cap.

- P (Perfil aplicat): es noten transformacions específiques visibles per al perfil?
  * TDAH: chunking, barres progrés, llistes numerades, paràgrafs curts
  * TEA: zero metàfores, estructura predictible, literal
  * Dislèxia: frases curtes, una idea per frase
  * DI: pictogrames + frases molt simples + repetició
  * Nouvingut: glossari L1, definicions inline simples
  * AC: profundització, no infantilització
  P=5 només si les transformacions són evidents i específiques.

- C (Curricular): preserva contingut sense inventar ni perdre dades clau.
  Penalitza si veus dades inventades (noms, xifres) o pèrdua d'idees curriculars.

També compta i reporta violacions concretes al camp "v":
- v_paren: nombre de definicions amb parèntesi a DUA Accés (0 si DUA != Accés)
- v_frases_llargues: nombre de frases que superen el límit MECR
- v_paraules: nombre de paraules genèriques prohibides

Retorna NOMÉS aquest JSON:
{"Q":1-5,"P":1-5,"C":1-5,"j":"frase justificació concreta","v":{"paren":N,"frases_llargues":N,"paraules":N}}"""


def _verify_adaptation(verify_model: str, text_original: str, text_adapted: str, profile: dict, params: dict):
    """Autoavaluació ràpida amb 3 criteris. Retorna (mitjana, info)."""
    import json as _json
    # Fix 2026-05-27 (bug Call 1 buit): si text adaptat és buit, retornem 0
    # directament. Sense això el judge al·lucina (Q=3, P=4, C=5 sobre text
    # buit) i el retry loop trenca, generant complements sobre buit.
    if not (text_adapted or "").strip():
        return 0.0, {"Q": 0, "P": 0, "C": 0, "j": "text adaptat buit (Call 1 sense contingut)", "model": verify_model}
    perfil_nom = profile.get("nom", "genèric")
    mecr = params.get("mecr_sortida", "B2")
    dua = params.get("dua", "Core")
    user_msg = (
        f"PERFIL: {perfil_nom} | MECR sortida: {mecr} | DUA: {dua}\n\n"
        f"TEXT ORIGINAL:\n{text_original[:2000]}\n\n"
        f"TEXT ADAPTAT:\n{text_adapted[:3000]}\n\n"
        f"Puntua Q, P, C (1-5). JSON nomes."
    )
    raw = _call_llm_raw(
        verify_model,
        VERIFY_SYSTEM,
        user_msg,
        temperature=0.2,
        top_p=0.95,
        max_tokens=600,
    )
    m = re.search(r'\{[^}]*"Q"[^}]*\}', raw, re.DOTALL)
    if not m:
        raise RuntimeError(f"No s'ha trobat JSON a la resposta: {raw[:200]}")
    data = _json.loads(m.group(0))
    q = float(data.get("Q", 0))
    p = float(data.get("P", 0))
    c = float(data.get("C", 0))
    mitjana = (q + p + c) / 3.0
    return mitjana, {"Q": q, "P": p, "C": c, "j": data.get("j", ""), "model": verify_model}


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

    lang = params.get("lang", "ca")

    # Determina si fem 2 crides separades (adapter + complements).
    # Condicio: SKILLs actives + almenys 1 complement seleccionat.
    # Si no, fem crida unica (comportament legacy).
    _comp_params = params.get("complements", {}) if isinstance(params, dict) else {}
    _has_complements = any(_comp_params.values())
    try:
        import skills_loader as _sl_check
        _skills_on_diag = _sl_check.is_skills_enabled()
        _two_call = _skills_on_diag and _has_complements
        # DIAG 2026-06-02: per què la Call 2 (complements) no s'executa a prod?
        try:
            _n_skills_diag = len(_sl_check.load_skills(_sl_check.default_skills_roots()))
        except Exception as _e_sk:
            _n_skills_diag = f"ERROR({type(_e_sk).__name__}: {_e_sk})"
        print(
            f"[diag_two_call] ATNE_USE_SKILLS_env={os.getenv('ATNE_USE_SKILLS')!r} "
            f"is_skills_enabled={_skills_on_diag} skills_carregades={_n_skills_diag} "
            f"has_complements={_has_complements} comp_keys={[k for k,v in _comp_params.items() if v]} "
            f"=> _two_call={_two_call}",
            flush=True,
        )
    except Exception as _e_two:
        _two_call = False
        print(f"[diag_two_call] EXCEPCIÓ calculant _two_call: {type(_e_two).__name__}: {_e_two}", flush=True)

    # System prompt — sense RAG, les instruccions graduades són el motor
    cb({"type": "step", "step": "search", "msg": "Preparant instruccions d'adaptació..."})
    # include_argumentacio=False quan 2-call: «Per al docent» es genera en una crida
    # DEDICADA al final (l'adapter la infra-genera dins la crida gran — validat NLM 2026-06-11).
    # En crida única (no _two_call) es manté inline.
    system_prompt = build_system_prompt(profile, context, params, rag_context="",
                                        adapter_only=_two_call,
                                        include_argumentacio=not _two_call)
    _filtered = instruction_filter.get_instructions(profile, params, context=context)
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
        "prompt_version": getattr(server, "ATNE_PROMPT_VERSION", None),
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
        "gemma-4-26b-a4b-it":   "Gemma 4 26B A4B",
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
    verify_model = (params.get("verify_model") or "").strip()
    if verify_enabled and not verify_model:
        # El verify és una tasca curta. Usar el mateix model que genera penalitza
        # molt Gemma 4 31B, així que deleguem al model auditor configurable.
        try:
            verify_model = server._model_for("auditor")
        except Exception:
            verify_model = active_model
    verify_model = verify_model or active_model
    _verify_prov, _verify_spec = _resolve_model(verify_model)
    verify_label = _labels.get(_verify_spec, verify_model)
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

    _llm_u: dict = {}  # tokens reals + latència LLM de la darrera crida exitosa
    adapted_raw = None
    for attempt in range(1, max_attempts + 1):
        label_attempt = f" (intent {attempt}/{max_attempts})" if verify_enabled else ""
        cb({"type": "step", "step": "adapting", "msg": f"Generant adaptació amb {model_label}{label_attempt}..."})
        try:
            # Streaming: emetem cada chunk com a event SSE «delta» perquè el
            # frontend pugui renderitzar el text progressivament (com ChatGPT).
            # Així reduïm la sensació de lentitud quan el rotatiu treu un model
            # lent (Gemma 4 31B pot trigar ~100s). Acumulem els chunks per tenir
            # el text complet i poder fer verify + post-process al final.
            _t0_stream = time.time()
            _chunks: list[str] = []
            try:
                for _chunk in _call_llm_stream(
                    active_model, system_prompt, user_text,
                    temperature=0.4, top_p=0.95, max_tokens=16384,
                ):
                    _chunks.append(_chunk)
                    cb({"type": "delta", "text": _chunk})
                adapted_raw = "".join(_chunks)
            except Exception as _stream_err:
                # Fallback: si el stream falla (clau, quota, etc.) prova
                # crida no-streaming abans de retornar error a l'usuari.
                print(f"[adapt] Stream fallit, fallback no-stream: {_stream_err}", flush=True)
                adapted_raw = _call_llm(active_model, system_prompt, user_text)

            # Fix 2026-05-27 (bug Call 1 buit): si el stream termina sense
            # excepció però amb 0 chunks útils (Gemma SAFETY/RECITATION o
            # MAX_TOKENS sense contingut), fem fallback a no-stream. Sense
            # això, adapted_raw="" passa silenciosament pel verify (que
            # al·lucina un 4.0 sobre text buit) i Call 2 sobreescriu el
            # buit amb complements genèrics sobre un text inexistent.
            if not (adapted_raw or "").strip():
                print(f"[adapt] Stream va retornar 0 chunks útils, fallback no-stream", flush=True)
                try:
                    adapted_raw = _call_llm(active_model, system_prompt, user_text)
                except Exception as _no_stream_err:
                    print(f"[adapt] Fallback no-stream també ha fallat: {_no_stream_err}", flush=True)

            import adaptation.llm_clients as _llm_mod
            # Si el stream ha funcionat, _LAST_LLM_USAGE no s'ha actualitzat
            # (només ho fa _call_llm). Estimem tokens i temps a partir de
            # longituds del text — aproximació suficient per a telemetria del
            # pilot. Si el fallback no-stream s'ha activat, _LAST_LLM_USAGE
            # ja conté valors reals del proveïdor.
            if _chunks:  # cas streaming
                _llm_u = {
                    "tokens_in": len(system_prompt + user_text) // 4,
                    "tokens_out": len(adapted_raw) // 4,
                    "llm_ms": int((time.time() - _t0_stream) * 1000),
                    "provider": _resolve_model(active_model)[0],
                }
            else:
                _llm_u = dict(_llm_mod._LAST_LLM_USAGE)
            adapted = clean_gemini_output(adapted_raw)
            adapted = _post_process_llm_output(adapted, lang=lang)
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
        cb({"type": "step", "step": "verifying", "msg": f"Autoavaluant qualitat amb {verify_label} (intent {attempt})..."})
        try:
            score, verify_info = _verify_adaptation(verify_model, text, adapted, profile, params)
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
    pp = post_process_adaptation(adapted, mecr, lang=lang)
    for w in pp.get("warnings", []):
        cb({"type": "step", "step": "warning", "msg": w})

    # 6b. Resolucio pictogrames ARASAAC — substitueix [PICTO: terme] per <img>
    # Només s'activa si el complement 'pictogrames' és true i el text conté
    # marcadors. Si ARASAAC falla parcialment, els marcadors sense resolució
    # queden com a emoji de fallback (no es trenca el flux).
    _comps = params.get("complements", {}) if isinstance(params, dict) else {}
    if _comps.get("pictogrames"):
        try:
            from adaptation.pictograms_arasaac import resolve_pictogram_markers
            _n_markers_before = adapted.count("[PICTO")
            if _n_markers_before:
                cb({"type": "step", "step": "pictograms",
                    "msg": f"Resolent {_n_markers_before} pictograma(es) ARASAAC..."})
                adapted = resolve_pictogram_markers(adapted)
        except Exception as _picto_err:
            print(f"[pictograms] resolucio fallida (fallback emoji): {_picto_err}", flush=True)

    # 6c. 2a crida LLM per a complements (quan _two_call=True)
    # El text adaptat ja està net (post-process + ARASAAC). L'enviem com a
    # context per a la generació de glossari, preguntes, bastides, etc.
    # Fix 2026-05-27: si Call 1 va quedar buida (bug ex_di), NO executem
    # Call 2 per evitar generar complements genèrics sobre un text inexistent.
    if _two_call and adapted.strip():
        _comp_system = build_complements_prompt(profile, context, params)
        if _comp_system:
            _comp_model = server._model_for("complements")
            _, _comp_spec = _resolve_model(_comp_model)
            _comp_labels = {
                "gpt-4.1-mini": "GPT-4.1 mini",
                "gpt-4o-mini":  "GPT-4o mini",
                "gpt-4o":       "GPT-4o",
                "gemini-2.5-flash": "Gemini 2.5 Flash",
            }
            _comp_label = _comp_labels.get(_comp_spec, _comp_spec)
            cb({"type": "step", "step": "complements",
                "msg": f"Generant complements amb {_comp_label}..."})
            try:
                _comp_user = (
                    f"TEXT ADAPTAT:\n{adapted}\n\n"
                    "Genera els complements pedagògics sol·licitats."
                )
                # Fix 2026-05-27: _call_llm() no accepta temperature/max_tokens
                # kwargs (signatura: model_id, system_prompt, text). Sense aquest
                # fix la 2a crida petava i NO es generaven mai complements
                # (detectat pel harness Fase B: 22/24 casos amb REGLA:MATRIU).
                _comp_raw = _call_llm(_comp_model, _comp_system, _comp_user)
                _comp_clean = clean_gemini_output(_comp_raw)
                _comp_clean = _post_process_llm_output(_comp_clean, lang=lang)
                # Resolucio pictogrames als complements (si n'hi ha marcadors)
                if _comp_params.get("pictogrames") and "[PICTO" in _comp_clean:
                    try:
                        from adaptation.pictograms_arasaac import resolve_pictogram_markers
                        _comp_clean = resolve_pictogram_markers(_comp_clean)
                    except Exception as _pe:
                        print(f"[complements_call] pictograms error: {_pe}", flush=True)
                # Afegim els complements al text adaptat (el frontend parseja el conjunt)
                adapted = adapted.rstrip() + "\n\n" + _comp_clean.strip()
                print(f"[complements_call] generat {len(_comp_clean)} chars", flush=True)

                # Fix 2026-05-27: filtre post-output que elimina seccions ## no
                # autoritzades pel cas. El LLM tendeix a generar tot el que sap
                # encara que no es demani (vist a mireia: bastides actiu però
                # genera també ## Preguntes; marc: glossari activat + preguntes
                # duplicades). Aquest filtre defensiu manté només les seccions
                # corresponents als complements actius del cas.
                import re as _re_filter
                # Mapping complement → títol de secció (formes principals que el LLM emet)
                _section_aliases = {
                    "glossari": [r"^## Glossari\b"],
                    "esquema_visual": [r"^## Esquema visual\b", r"^## Esquema\b"],
                    "bastides": [r"^## Bastides\b", r"^## Suports per llegir\b"],
                    "mapa_conceptual": [r"^## Mapa conceptual\b"],
                    "mapa_mental": [r"^## Mapa mental\b"],
                    "preguntes_comprensio": [r"^## Preguntes de comprensió\b", r"^## Preguntes\b"],
                    "activitats_aprofundiment": [r"^## Activitats d'aprofundiment\b"],
                    "pictogrames": [r"^## Pictogrames\b"],
                    "plantilles_genere": [r"^## Plantilla", r"^## Plantilles"],
                    "resum_graduat": [r"^## Resum graduat\b"],
                    "cartes_conversacionals": [r"^## Cartes conversacionals\b"],
                    "rubriques": [r"^## R[úu]briques\b"],
                    "tolc": [r"^## TOLC\b", r"^## Transllenguatge\b"],
                }
                # Seccions sempre permeses (no són complements)
                _always_allow = [
                    r"^## Text adaptat\b",
                    r"^## Argumentaci[óo] pedag[òo]gica\b",
                    r"^## Notes d'auditoria\b",
                ]
                # Secció permeses = always + aliases dels complements demanats
                _allowed_patterns = list(_always_allow)
                for _k, _v in _comp_params.items():
                    if _v and _k in _section_aliases:
                        _allowed_patterns.extend(_section_aliases[_k])
                _allowed_re = _re_filter.compile("|".join(_allowed_patterns), _re_filter.M)
                # Tots els títols ## que apareixen al adapted
                _all_titles_re = _re_filter.compile(r"^## [^\n]+", _re_filter.M)
                _stripped_sections = []
                _segments = _re_filter.split(r"(?m)(^## [^\n]+)\n", adapted)
                # _segments: [prefix, title1, body1, title2, body2, ...]
                _new_parts = [_segments[0]]
                _i = 1
                while _i < len(_segments):
                    _title = _segments[_i]
                    _body = _segments[_i + 1] if _i + 1 < len(_segments) else ""
                    if _allowed_re.match(_title):
                        _new_parts.append(_title + "\n" + _body)
                    else:
                        _stripped_sections.append(_title)
                    _i += 2
                if _stripped_sections:
                    print(f"[post_filter] Seccions eliminades (no autoritzades): {_stripped_sections}", flush=True)
                    adapted = "".join(_new_parts)

                # ── Retry de seccions absents (2026-06-02) ────────────────────
                # Bug intermitent confirmat amb DevTools: la Call 2 de vegades
                # OMET una secció de complement demanada (bastides, glossari…) —
                # no-determinisme del model. El frontend (correctament) no mostra
                # el que no rep. Solució general: detectar quins complements
                # actius NO tenen la seva secció a `adapted` i re-demanar NOMÉS
                # aquelles seccions en una crida focalitzada. Cobreix qualsevol
                # complement via `_section_aliases` (font única del mapping).
                # Skills inline (pictogrames/illustracions) NO generen secció ##
                # pròpia → s'exclouen del retry.
                _INLINE_NO_SECTION = {"pictogrames", "illustracions",
                                      "negretes", "definicions_integrades", "traduccio_l1"}
                _missing_sections = []
                for _k, _v in _comp_params.items():
                    if not _v or _k in _INLINE_NO_SECTION or _k not in _section_aliases:
                        continue
                    _pat = _re_filter.compile("|".join(_section_aliases[_k]), _re_filter.M)
                    if not _pat.search(adapted):
                        _missing_sections.append(_k)
                if _missing_sections:
                    print(f"[complements_retry] seccions absents, re-demanant: {_missing_sections}", flush=True)
                    cb({"type": "step", "step": "complements_retry",
                        "msg": f"Recuperant {len(_missing_sections)} complement(s) que falten..."})
                    # Noms llegibles de les seccions per al prompt de retry
                    _missing_titles = [
                        _section_aliases[_k][0].replace(r"^## ", "## ").replace(r"\b", "")
                        for _k in _missing_sections
                    ]
                    _retry_user = (
                        f"TEXT ADAPTAT:\n{adapted}\n\n"
                        "Genera NOMÉS aquestes seccions que falten, amb el mateix format "
                        "i nivell demanats al system prompt. No repeteixis cap altra secció:\n"
                        + "\n".join(f"- {_t}" for _t in _missing_titles)
                    )
                    try:
                        _retry_raw = _call_llm(_comp_model, _comp_system, _retry_user)
                        _retry_clean = clean_gemini_output(_retry_raw)
                        _retry_clean = _post_process_llm_output(_retry_clean, lang=lang)
                        if _comp_params.get("pictogrames") and "[PICTO" in _retry_clean:
                            try:
                                from adaptation.pictograms_arasaac import resolve_pictogram_markers
                                _retry_clean = resolve_pictogram_markers(_retry_clean)
                            except Exception:
                                pass
                        # Afegim NOMÉS les seccions que de debò faltaven (filtre per
                        # evitar que el retry torni a colar seccions no demanades).
                        _retry_allowed = []
                        for _k in _missing_sections:
                            _retry_allowed.extend(_section_aliases[_k])
                        _retry_re = _re_filter.compile("|".join(_retry_allowed), _re_filter.M)
                        _rseg = _re_filter.split(r"(?m)(^## [^\n]+)\n", _retry_clean)
                        _kept = []
                        _j = 1
                        while _j < len(_rseg):
                            _rt = _rseg[_j]
                            _rb = _rseg[_j + 1] if _j + 1 < len(_rseg) else ""
                            if _retry_re.match(_rt):
                                _kept.append(_rt + "\n" + _rb)
                            _j += 2
                        if _kept:
                            adapted = adapted.rstrip() + "\n\n" + "\n\n".join(_kept).strip()
                            print(f"[complements_retry] recuperades {len(_kept)} secció(ns)", flush=True)
                        else:
                            print("[complements_retry] el retry tampoc no ha generat les seccions", flush=True)
                    except Exception as _retry_err:
                        print(f"[complements_retry] error (ignorat): {_retry_err}", flush=True)
            except Exception as _comp_err:
                cb({"type": "step", "step": "warning",
                    "msg": f"Avís: complements fallits ({_comp_err}). Text adaptat conservat."})
                print(f"[complements_call] error: {_comp_err}", flush=True)

    # 6d. Crida DEDICADA «Per al docent» (argumentació pedagògica, 9 cat A-I).
    # Per què separada: dins la Call 1 (adapter), gpt-4o prioritza el text adaptat i
    # infra-genera l'argumentació (2 cards de ~7). Una crida focalitzada amb el TEXT
    # ADAPTAT FINAL (text + complements) com a context produeix les 7-9 cards COHERENTS
    # amb el que realment s'ha generat i amb el perfil. Validat empíricament + NotebookLM
    # 2026-06-11. Només en 2-call (en crida única l'argumentació ja va inline).
    if _two_call and adapted.strip():
        try:
            _arg_system = build_argumentacio_prompt(profile, context, params)
            _arg_model = server._model_for("complements")  # tasca focalitzada (config híbrid: gpt-4o)
            cb({"type": "step", "step": "argumentacio",
                "msg": "Generant «Per al docent» (argumentació pedagògica)..."})
            _arg_user = (
                f"TEXT ADAPTAT FINAL (amb els complements ja generats):\n{adapted}\n\n"
                "Genera NOMÉS la secció «## Argumentació pedagògica» amb una card per a cada "
                "categoria obligatòria del cas. No reprodueixis el text ni cap complement."
            )
            _arg_raw = _call_llm(_arg_model, _arg_system, _arg_user)
            _arg_clean = clean_gemini_output(_arg_raw)
            _arg_clean = _post_process_llm_output(_arg_clean, lang=lang).strip()
            if _arg_clean:
                import re as _re_arg
                # Normalitza la sortida del model (defensiu):
                # 1) Treu TOTS els headings «## Argumentació pedagògica» que el model
                #    hagi posat (sovint l'eco-genera duplicat) → en prependrem un de net.
                #    Nota: «pedagògica» porta ò (U+00F2), no o/ó → cal [oòó] a les dues paraules.
                _body = _re_arg.sub(r"(?im)^#{1,3}\s*Argumentaci[oòó]\s+pedag[oòó]gica\s*$",
                                    "", _arg_clean).strip()
                # 2) Cards amb «## X.» en lloc de «### X.» trenquen el rendering del
                #    frontend (les interpretaria com a seccions top-level) → força ###.
                _body = _re_arg.sub(r"(?m)^##\s+([A-I]\.\s)", r"### \1", _body)
                _arg_final = "## Argumentació pedagògica\n\n" + _body
                adapted = adapted.rstrip() + "\n\n" + _arg_final
                _n_cards = len(_re_arg.findall(r"(?m)^###\s*[A-I]\.", _arg_final))
                print(f"[argumentacio_call] generat {len(_arg_final)} chars, {_n_cards} cards", flush=True)
        except Exception as _arg_err:
            cb({"type": "step", "step": "warning",
                "msg": f"Avís: argumentació «Per al docent» fallida ({_arg_err}). Text conservat."})
            print(f"[argumentacio_call] error (ignorat): {_arg_err}", flush=True)

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
                lang=lang,
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
            if _llm_u:
                _ATNE_LAST_ADAPTATION["tokens_in"] = _llm_u.get("tokens_in", 0)
                _ATNE_LAST_ADAPTATION["tokens_out"] = _llm_u.get("tokens_out", 0)
                _ATNE_LAST_ADAPTATION["llm_ms"] = _llm_u.get("llm_ms", 0)
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

    # Sprint 1C: estimació de cost en EUR per a aquesta crida.
    # Inclou la crida principal (input system_prompt + user_text → output adapted).
    # Si verify ha refet, el cost real serà superior; per simplicitat el comptem
    # només una vegada (l'error és <2× i sempre conservador).
    try:
        _cost_eur = estimate_cost_eur(
            active_model,
            input_chars=len(system_prompt) + len(user_text),
            output_chars=len(adapted),
        )
    except Exception:
        _cost_eur = None
    if _ATNE_LAST_ADAPTATION:
        _ATNE_LAST_ADAPTATION["cost_estimat_eur"] = _cost_eur

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
                "prompt_version":  getattr(server, "ATNE_PROMPT_VERSION", None),
                "cost_estimat_eur": _cost_eur,
            },),
            daemon=True,
        ).start()
    except Exception as _te:
        print(f"[telemetria] error creant thread: {_te}", flush=True)

    return adapted
