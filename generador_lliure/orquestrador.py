"""Orquestrador del m\u00f2dul generador_lliure.

Recep els par\u00e0metres crus del payload `/api/generate-text`, construeix el
prompt m\u00ednim, crida a l'agent (que resol el model via `_call_llm_raw`) i
retorna un dict amb el text generat + metadata.

\u00daltim responsable del pipeline de generaci\u00f3 aliat a Arena:
1. Valida par\u00e0metres m\u00ednims (tema obligatori).
2. Construeix prompt (SYSTEM + USER) via `prompt.build_prompt`.
3. Resol el model a usar via `_model_for("generate", override=payload.model)`.
4. Crida a l'agent i obt\u00e9 el text.
5. Retorna resposta compatible amb l'antic `/api/generate-text` (mateixos
   camps: text, paraules, tema, genere, tipologia, to, extensio, model).

No aplica cap post-processament. El text va directe del model a la resposta.
"""

from __future__ import annotations

import time
from typing import Iterator

from .agent import AgentGenerador
from .prompt import build_prompt, resolve_extension


def generar(params: dict) -> dict:
    """Genera un text educatiu a partir dels par\u00e0metres del Pas 2.

    Par\u00e0metres esperats al dict `params` (tots opcionals excepte `tema`):
        tema (str, obligatori)
        genere (str) — g\u00e8nere discursiu
        tipologia (str) — tipologia textual
        to (str)
        extensio (str) — "curt" | "estandard" | "extens"
        notes (str) — indicacions addicionals opcionals
        context (dict) — curs, etapa, materia, ambit
        model (str) — override expl\u00edcit del model a usar
        saber_curricular (str) — saber curricular a vincular (Sprint C, opcional)
        temperature (float) — override del sampling (default 1.0)
        top_p (float) — override (default 0.95)
        max_tokens (int) — override (default 2048)

    Retorna:
        dict amb:
            text (str) — el text generat
            paraules (int) — nombre de paraules del text
            tema, genere, tipologia, to, extensio — echo dels par\u00e0metres
            model (str) — model_id que ha disparat realment (despr\u00e9s de la
                rotaci\u00f3 aleat\u00f2ria si aplica)
            duration_ms (int) — durada de la crida

    Aixeca:
        ValueError si falta `tema`.
        RuntimeError si tots els providers del model resolen fallen.
    """
    # Import local per evitar cicle a l'arrencada.
    from server import _model_for

    # Validaci\u00f3 m\u00ednima
    tema = (params.get("tema") or "").strip()
    if not tema:
        raise ValueError("Cal especificar un 'tema' per generar text.")

    # Construcci\u00f3 del prompt (pot aixecar ValueError per tema buit, ja ja)
    system, user = build_prompt(params)

    # Resoluci\u00f3 del model a usar per a la fase "generate"
    # Aix\u00f2 respecta:
    #   override expl\u00edcit del payload > _MODEL_CONFIG["generate"] > ATNE_MODEL
    # I en mode rotaci\u00f3, fa random.choice dels models seleccionats a /admin.
    model_override = (params.get("model") or "").strip()
    model_usat = _model_for("generate", override=model_override)

    # Sampling overrides (opcional)
    temperature = float(params.get("temperature") or 1.0)
    top_p = float(params.get("top_p") or 0.95)
    max_tokens = int(params.get("max_tokens") or 2048)

    # Crida a l'agent
    agent = AgentGenerador(
        model_id=model_usat,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )

    t0 = time.time()
    text = agent.generate(system, user)
    duration_ms = int((time.time() - t0) * 1000)

    text = (text or "").strip()
    if not text:
        raise RuntimeError("L'LLM ha retornat un text buit.")

    # Resoluci\u00f3 de l'etiqueta d'extensi\u00f3 per a l'eco de resposta
    n_target, _label = resolve_extension(params.get("extensio"))

    return {
        "text": text,
        "paraules": len(text.split()),
        "tema": tema,
        "genere": (params.get("genere") or "article divulgatiu").strip(),
        "tipologia": (params.get("tipologia") or "expositiva").strip().lower(),
        "to": (params.get("to") or "neutre").strip().lower(),
        "extensio": (params.get("extensio") or "estandard").strip().lower(),
        "model": model_usat,
        "duration_ms": duration_ms,
        "target_words": n_target,
        # quality_report buit per retrocompat amb el frontend del Pas 2
        # (que ja tolera absence o camps buits). El pipeline de qualitat
        # complet no s'aplica a generaci\u00f3; si es vol, s'usa revisi\u00f3 LT
        # opcional post-generaci\u00f3 via botó separat.
        "quality_report": None,
    }


def generar_stream(params: dict) -> Iterator[dict]:
    """Versi\u00f3 streaming de `generar()`.

    Retorna un generador de dicts `event` que el consumidor (endpoint SSE)
    pot serialitzar i re-emetre al frontend. Tipus d'events:

        {"type": "start", "model": "...", "target_words": N}
        {"type": "chunk", "text": "..."}        (repetits N vegades)
        {"type": "done",  "text": "...", "paraules": N, "duration_ms": M, "model": "..."}
        {"type": "error", "message": "..."}

    Motivaci\u00f3: la generaci\u00f3 amb Gemma 4/Qwen triga 60-90s. Veure pantalla
    buida \u00e9s inacceptable per a la UX del pilot. Amb streaming, l'usuari
    veu paraules apareixent des del segon 1-2. Cost i temps total
    id\u00e8ntics a `generar()`; nom\u00e9s canvia el transport.
    """
    from server import _model_for

    try:
        tema = (params.get("tema") or "").strip()
        if not tema:
            yield {"type": "error", "message": "Cal especificar un 'tema' per generar text."}
            return

        system, user = build_prompt(params)

        model_override = (params.get("model") or "").strip()
        model_usat = _model_for("generate", override=model_override)

        temperature = float(params.get("temperature") or 1.0)
        top_p = float(params.get("top_p") or 0.95)
        max_tokens = int(params.get("max_tokens") or 2048)

        n_target, _label = resolve_extension(params.get("extensio"))

        yield {
            "type": "start",
            "model": model_usat,
            "target_words": n_target,
        }

        agent = AgentGenerador(
            model_id=model_usat,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
        )

        t0 = time.time()
        buffer: list[str] = []
        for piece in agent.generate_stream(system, user):
            if not piece:
                continue
            buffer.append(piece)
            yield {"type": "chunk", "text": piece}

        full_text = "".join(buffer).strip()
        duration_ms = int((time.time() - t0) * 1000)

        if not full_text:
            yield {"type": "error", "message": "L'LLM ha retornat un text buit."}
            return

        yield {
            "type": "done",
            "text": full_text,
            "paraules": len(full_text.split()),
            "tema": tema,
            "genere": (params.get("genere") or "article divulgatiu").strip(),
            "tipologia": (params.get("tipologia") or "expositiva").strip().lower(),
            "to": (params.get("to") or "neutre").strip().lower(),
            "extensio": (params.get("extensio") or "estandard").strip().lower(),
            "model": model_usat,
            "duration_ms": duration_ms,
            "target_words": n_target,
        }
    except Exception as e:
        yield {"type": "error", "message": f"{type(e).__name__}: {str(e)[:300]}"}
