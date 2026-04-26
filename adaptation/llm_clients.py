"""Clients LLM unificats per ATNE.

Aquest mòdul agrupa:
- Càrrega de claus API (GEMINI/GEMMA4/OPENROUTER/MISTRAL) amb suport multi-clau.
- Taula d'àlies de models (_MODEL_ALIASES) i resolució a (provider, model).
- Wrappers `_call_llm`, `_call_llm_raw`, `_call_llm_stream` amb rotació de
  claus, backoff per a errors transitoris de Google, i streaming per SSE.

server.py re-exporta totes aquestes símbols al seu namespace per mantenir el
contracte amb callers externs (generador_lliure, tests, snapshot_contract).
"""

import json
import os
import time

import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# ── Claus API (multi-clau, rotació) ────────────────────────────────────────

GEMINI_API_KEYS = [k for k in [os.getenv(f"GEMINI_API_KEY{s}", "")
                                for s in ["", "_3", "_4", "_5", "_6", "_7"]] if k]
GEMINI_API_KEY = GEMINI_API_KEYS[0] if GEMINI_API_KEYS else ""
_gemini_key_idx = 0  # índex actual de rotació

GEMMA4_API_KEYS = [k for k in [os.getenv(f"GEMMA4_API_KEY{s}", "")
                                for s in ["", "_2", "_3", "_4", "_5", "_6", "_7"]] if k]
GEMMA4_API_KEY = GEMMA4_API_KEYS[0] if GEMMA4_API_KEYS else ""
_gemma4_key_idx = 0  # índex actual de rotació

OPENROUTER_API_KEYS = [k for k in [os.getenv(f"OPENROUTER_API_KEY{s}", "")
                                    for s in ["", "_2", "_3", "_4", "_5"]] if k]
OPENROUTER_API_KEY = OPENROUTER_API_KEYS[0] if OPENROUTER_API_KEYS else ""
_openrouter_key_idx = 0  # índex actual de rotació

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")

# ATNE_MODEL: gemini | gemma4 | mistral | gpt | gpt-4o | mistral-large
# Per defecte gemma4 (decidit pel pilot 2026-04-12). Mistral disponible al codi
# però amagat de la UI; s'activarà al pilot HITL cec a partir del 20/04.
ATNE_MODEL = os.getenv("ATNE_MODEL", "gemma4").lower()

# ── Taula d'àlies de models ────────────────────────────────────────────────
#
# Alies compatibles amb l'API antiga (labels curts) i model_id llargs que
# arriben via /admin. _resolve_model() retorna (provider, model_específic)
# on provider és la branca de _call_llm() i model_específic és el nom real
# del model enviat al proveïdor.
_MODEL_ALIASES: dict[str, tuple[str, str]] = {
    # Aliases curts (backward compat)
    "gemma4":            ("gemma4",  "gemma-4-31b-it"),
    "gemma3":            ("gemma4",  "gemma-3-27b-it"),
    "gemma3-27b":        ("gemma4",  "gemma-3-27b-it"),
    "gemma3-12b":        ("gemma4",  "gemma-3-12b-it"),
    "gemma3n":           ("gemma4",  "gemma-3n-e4b-it"),
    "gemini":            ("gemini",  "gemini-2.5-flash"),
    "mistral":           ("mistral", "mistral-small-latest"),
    "mistral-small":     ("mistral", "mistral-small-latest"),
    "mistral-large":     ("mistral", "mistral-large-latest"),
    "gpt":               ("gpt",     "gpt-4o-mini"),
    "gpt-4o-mini":       ("gpt",     "gpt-4o-mini"),
    "gpt-4o":            ("gpt",     "gpt-4o"),
    "gpt-4.1-mini":      ("gpt",     "gpt-4.1-mini"),
    "qwen":              ("openrouter", "qwen/qwen3.5-27b"),
    # Aliases llargs que vindran de system_config i /admin
    "gemma-4-31b-it":    ("gemma4",  "gemma-4-31b-it"),
    "gemma-3-12b-it":    ("gemma4",  "gemma-3-12b-it"),
    "gemma-3-27b-it":    ("gemma4",  "gemma-3-27b-it"),
    "gemma-3n-e4b-it":   ("gemma4",  "gemma-3n-e4b-it"),
    "gemini-2.5-flash":  ("gemini",  "gemini-2.5-flash"),
    "mistral-small-latest": ("mistral", "mistral-small-latest"),
    "mistral-large-latest": ("mistral", "mistral-large-latest"),
    "gpt-4.1-mini-latest": ("gpt",    "gpt-4.1-mini"),
    "qwen/qwen3.5-27b":  ("openrouter", "qwen/qwen3.5-27b"),
    "qwen/qwen3.5-9b":   ("openrouter", "qwen/qwen3.5-9b"),
    "qwen/qwen3-235b-a22b:free":          ("openrouter", "qwen/qwen3-235b-a22b:free"),
    "qwen/qwen3-30b-a3b:free":            ("openrouter", "qwen/qwen3-30b-a3b:free"),
    "deepseek/deepseek-chat-v3-0324:free":("openrouter", "deepseek/deepseek-chat-v3-0324:free"),
    "deepseek/deepseek-r1:free":          ("openrouter", "deepseek/deepseek-r1:free"),
    "deepseek":          ("openrouter", "deepseek/deepseek-chat-v3-0324:free"),
    "deepseek-r1":       ("openrouter", "deepseek/deepseek-r1:free"),
}


def _resolve_model(model_id: str) -> tuple[str, str]:
    """Resol un model_id (curt o llarg) a (provider, model_específic).

    Si el model_id no es troba al mapa, cau a l'ATNE_MODEL per defecte.
    El retorn sempre és un tuple vàlid per a les branques de _call_llm().
    """
    if not model_id:
        return _MODEL_ALIASES.get(ATNE_MODEL, ("gemma4", "gemma-4-31b-it"))
    key = model_id.strip().lower()
    if key in _MODEL_ALIASES:
        return _MODEL_ALIASES[key]
    # Fallback: mirem si és un model_id llarg que comenci amb un prefix conegut
    if key.startswith("qwen/"):
        return ("openrouter", model_id.strip())
    if key.startswith("qwen"):
        return ("openrouter", "qwen/qwen3.5-27b")
    if key.startswith("deepseek/"):
        return ("openrouter", model_id.strip())
    if key.startswith("deepseek"):
        return ("openrouter", "deepseek/deepseek-chat-v3-0324:free")
    if key.startswith("gemma-3"):
        return ("gemma4", "gemma-3-12b-it")
    if key.startswith("gemma"):
        return ("gemma4", "gemma-4-31b-it")
    if key.startswith("gemini"):
        return ("gemini", "gemini-2.5-flash")
    if key.startswith("gpt-4.1-mini"):
        return ("gpt", "gpt-4.1-mini")
    if key.startswith("gpt-4o-mini"):
        return ("gpt", "gpt-4o-mini")
    if key.startswith("gpt-4o"):
        return ("gpt", "gpt-4o")
    if key.startswith("gpt"):
        return ("gpt", "gpt-4o-mini")
    if key.startswith("mistral-large"):
        return ("mistral", "mistral-large-latest")
    if key.startswith("mistral"):
        return ("mistral", "mistral-small-latest")
    # Últim fallback: ATNE_MODEL
    return _MODEL_ALIASES.get(ATNE_MODEL, ("gemma4", "gemma-4-31b-it"))


# ── Client Gemini compartit (per a health-check) ───────────────────────────

_genai_key = GEMMA4_API_KEY if ATNE_MODEL == "gemma4" else GEMINI_API_KEY
gemini_client = genai.Client(
    api_key=_genai_key or GEMMA4_API_KEY or GEMINI_API_KEY,
    http_options=types.HttpOptions(timeout=300_000),  # 5min per generacions llargues
) if (_genai_key or GEMMA4_API_KEY or GEMINI_API_KEY) else None


# ── Wrappers de crida al LLM ───────────────────────────────────────────────

def _call_llm(model_id: str, system_prompt: str, text: str) -> str:
    """Wrapper unificat de crida al LLM.

    `model_id` pot ser un àlies curt (`gemma4`, `gpt`, `mistral`, ...) o un
    model_id llarg (`gemma-4-31b-it`, `gpt-4o`, `mistral-large-latest`, ...).
    _resolve_model() el tradueix a (provider, specific_model).
    """
    global _gemma4_key_idx, _gemini_key_idx
    provider, specific_model = _resolve_model(model_id)
    if provider == "mistral":
        r = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers={"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": specific_model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"TEXT ORIGINAL A ADAPTAR:\n\n{text}"},
                ],
                "max_tokens": 8192,
                "temperature": 0.4,
            },
            timeout=180,
        )
        if r.status_code != 200:
            raise RuntimeError(f"HTTP {r.status_code}: {r.text[:200]}")
        return r.json()["choices"][0]["message"]["content"] or ""
    elif provider == "gemma4":
        errors = []
        # Retry amb backoff per errors transitoris (500 INTERNAL, 503 UNAVAILABLE,
        # timeouts). Google Gemma 4 API tè hipos puntuals, sense retry perds la
        # crida sencera. Amb [2s, 4s] resolem la majoria.
        _RETRYABLE = ("INTERNAL", "UNAVAILABLE", "RESOURCE_EXHAUSTED",
                      "DEADLINE_EXCEEDED", "500", "502", "503", "504")
        for attempt in range(len(GEMMA4_API_KEYS)):
            idx = (_gemma4_key_idx + attempt) % len(GEMMA4_API_KEYS)
            client = genai.Client(
                api_key=GEMMA4_API_KEYS[idx],
                http_options=types.HttpOptions(timeout=300_000),
            )
            last_err = None
            for retry_delay in (0, 2, 4):
                if retry_delay > 0:
                    time.sleep(retry_delay)
                try:
                    response = client.models.generate_content(
                        model=specific_model,
                        contents=[types.Content(role="user", parts=[types.Part(text=f"{system_prompt}\n\n---\n\nTEXT ORIGINAL A ADAPTAR:\n\n{text}")])],
                        config=types.GenerateContentConfig(temperature=0.4, max_output_tokens=8192),
                    )
                    _gemma4_key_idx = (idx + 1) % len(GEMMA4_API_KEYS)  # rotar per la pròxima crida
                    return response.text or ""
                except Exception as e:
                    last_err = e
                    err_str = str(e)
                    if not any(code in err_str for code in _RETRYABLE):
                        break  # error no transitori (auth, quota, etc.) — passa a la seguent clau
                    print(f"[Gemma4 retry] clau {idx+1}: {err_str[:120]} — backoff {retry_delay}s", flush=True)
            errors.append(f"clau {idx+1}: {last_err}")
        raise RuntimeError(f"Totes les claus Gemma4 han fallat: {'; '.join(errors)}")
    elif provider == "gemini":
        errors = []
        _RETRYABLE = ("INTERNAL", "UNAVAILABLE", "RESOURCE_EXHAUSTED",
                      "DEADLINE_EXCEEDED", "500", "502", "503", "504")
        for attempt in range(len(GEMINI_API_KEYS)):
            idx = (_gemini_key_idx + attempt) % len(GEMINI_API_KEYS)
            client = genai.Client(
                api_key=GEMINI_API_KEYS[idx],
                http_options=types.HttpOptions(timeout=300_000),
            )
            last_err = None
            for retry_delay in (0, 2, 4):
                if retry_delay > 0:
                    time.sleep(retry_delay)
                try:
                    response = client.models.generate_content(
                        model=specific_model,
                        contents=[types.Content(role="user", parts=[types.Part(text=text)])],
                        config=types.GenerateContentConfig(
                            system_instruction=system_prompt,
                            temperature=0.4, max_output_tokens=8192,
                            thinking_config=types.ThinkingConfig(thinking_budget=0),
                        ),
                    )
                    _gemini_key_idx = (idx + 1) % len(GEMINI_API_KEYS)
                    return response.text or ""
                except Exception as e:
                    last_err = e
                    err_str = str(e)
                    if not any(code in err_str for code in _RETRYABLE):
                        break
                    print(f"[Gemini retry] clau {idx+1}: {err_str[:120]} — backoff {retry_delay}s", flush=True)
            errors.append(f"clau {idx+1}: {last_err}")
        raise RuntimeError(f"Totes les claus Gemini han fallat: {'; '.join(errors)}")
    elif provider == "gpt":
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        resp = client.chat.completions.create(
            model=specific_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"TEXT ORIGINAL A ADAPTAR:\n\n{text}"},
            ],
            max_tokens=8192, temperature=0.4,
        )
        return resp.choices[0].message.content or ""
    elif provider == "openrouter":
        global _openrouter_key_idx
        if not OPENROUTER_API_KEYS:
            raise RuntimeError("OPENROUTER_API_KEY no configurada al .env")
        from openai import OpenAI
        errors = []
        for attempt in range(len(OPENROUTER_API_KEYS)):
            idx = (_openrouter_key_idx + attempt) % len(OPENROUTER_API_KEYS)
            client = OpenAI(
                api_key=OPENROUTER_API_KEYS[idx],
                base_url="https://openrouter.ai/api/v1",
            )
            try:
                resp = client.chat.completions.create(
                    model=specific_model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"TEXT ORIGINAL A ADAPTAR:\n\n{text}"},
                    ],
                    max_tokens=2048, temperature=0.4,
                    extra_headers={
                        "HTTP-Referer": "https://atne.fje.cat",
                        "X-Title": "ATNE",
                    },
                )
                _openrouter_key_idx = (idx + 1) % len(OPENROUTER_API_KEYS)
                return resp.choices[0].message.content or ""
            except Exception as e:
                errors.append(f"clau {idx+1}: {str(e)[:200]}")
                continue
        raise RuntimeError(f"Totes les claus OpenRouter han fallat: {'; '.join(errors)}")
    else:
        raise RuntimeError(f"Model desconegut: {model_id}. Opcions: gemini, gemma4, gemma3, gpt, gpt-4o, gpt-4.1-mini, mistral, mistral-large, qwen")


def _call_llm_raw(
    model_id: str,
    system_prompt: str,
    user_text: str,
    temperature: float = 1.0,
    top_p: float = 0.95,
    max_tokens: int = 2048,
) -> str:
    """Wrapper unificat de crida al LLM **per a generació pura**.

    Diferències clau amb `_call_llm()`:
    - NO prepend "TEXT ORIGINAL A ADAPTAR:" al missatge d'usuari.
    - Paràmetres de sampling per defecte segons AI Studio (temp 1.0, top_p 0.95),
      no 0.4 com a adaptació.
    - max_tokens per defecte més baix (2048 vs 8192), adequat per a textos
      generats de 100-1000 paraules.
    - Exposa `temperature`, `top_p` i `max_tokens` com a paràmetres opcionals
      per si el mòdul generador_lliure vol afinar-los.

    Aquesta funció existeix perquè el pipeline d'adaptació injecta la frase
    "TEXT ORIGINAL A ADAPTAR" que contamina el registre quan la tasca és
    generar des de zero. Veure l'anàlisi del castell medieval (Fase 0-0.7).

    `model_id` pot ser un àlies curt o un model_id llarg; `_resolve_model()`
    el tradueix a (provider, specific_model). Rotació de claus igual que
    `_call_llm()`.
    """
    global _gemma4_key_idx, _gemini_key_idx, _openrouter_key_idx
    provider, specific_model = _resolve_model(model_id)
    if provider == "mistral":
        r = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers={"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": specific_model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_text},
                ],
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
            },
            timeout=180,
        )
        if r.status_code != 200:
            raise RuntimeError(f"HTTP {r.status_code}: {r.text[:200]}")
        return r.json()["choices"][0]["message"]["content"] or ""
    elif provider == "gemma4":
        # Nota: Gemma via google.genai no suporta system_instruction separat
        # ni thinking_config (confirmat empíricament a Fase 0.5). Concatenem
        # system + user en un sol missatge amb separador i no passem thinking.
        errors = []
        for attempt in range(len(GEMMA4_API_KEYS)):
            idx = (_gemma4_key_idx + attempt) % len(GEMMA4_API_KEYS)
            client = genai.Client(
                api_key=GEMMA4_API_KEYS[idx],
                http_options=types.HttpOptions(timeout=180_000),
            )
            try:
                full = f"{system_prompt}\n\n---\n\n{user_text}" if system_prompt else user_text
                response = client.models.generate_content(
                    model=specific_model,
                    contents=[types.Content(role="user", parts=[types.Part(text=full)])],
                    config=types.GenerateContentConfig(
                        temperature=temperature,
                        top_p=top_p,
                        max_output_tokens=max_tokens,
                    ),
                )
                _gemma4_key_idx = (idx + 1) % len(GEMMA4_API_KEYS)
                return response.text or ""
            except Exception as e:
                errors.append(f"clau {idx+1}: {str(e)[:200]}")
                continue
        raise RuntimeError(f"Totes les claus Gemma han fallat: {'; '.join(errors)}")
    elif provider == "gemini":
        errors = []
        for attempt in range(len(GEMINI_API_KEYS)):
            idx = (_gemini_key_idx + attempt) % len(GEMINI_API_KEYS)
            client = genai.Client(
                api_key=GEMINI_API_KEYS[idx],
                http_options=types.HttpOptions(timeout=180_000),
            )
            try:
                response = client.models.generate_content(
                    model=specific_model,
                    contents=[types.Content(role="user", parts=[types.Part(text=user_text)])],
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt if system_prompt else None,
                        temperature=temperature,
                        top_p=top_p,
                        max_output_tokens=max_tokens,
                        thinking_config=types.ThinkingConfig(thinking_budget=0),
                    ),
                )
                _gemini_key_idx = (idx + 1) % len(GEMINI_API_KEYS)
                return response.text or ""
            except Exception as e:
                errors.append(f"clau {idx+1}: {str(e)[:200]}")
                continue
        raise RuntimeError(f"Totes les claus Gemini han fallat: {'; '.join(errors)}")
    elif provider == "gpt":
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_text})
        resp = client.chat.completions.create(
            model=specific_model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
        )
        return resp.choices[0].message.content or ""
    elif provider == "openrouter":
        if not OPENROUTER_API_KEYS:
            raise RuntimeError("OPENROUTER_API_KEY no configurada al .env")
        from openai import OpenAI
        errors = []
        for attempt in range(len(OPENROUTER_API_KEYS)):
            idx = (_openrouter_key_idx + attempt) % len(OPENROUTER_API_KEYS)
            client = OpenAI(
                api_key=OPENROUTER_API_KEYS[idx],
                base_url="https://openrouter.ai/api/v1",
            )
            try:
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": user_text})
                resp = client.chat.completions.create(
                    model=specific_model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    extra_headers={
                        "HTTP-Referer": "https://atne.fje.cat",
                        "X-Title": "ATNE",
                    },
                )
                _openrouter_key_idx = (idx + 1) % len(OPENROUTER_API_KEYS)
                return resp.choices[0].message.content or ""
            except Exception as e:
                errors.append(f"clau {idx+1}: {str(e)[:200]}")
                continue
        raise RuntimeError(f"Totes les claus OpenRouter han fallat: {'; '.join(errors)}")
    else:
        raise RuntimeError(
            f"Model desconegut: {model_id}. Opcions: gemini, gemma4, gemma3, "
            f"gpt, gpt-4o, gpt-4.1-mini, mistral, mistral-large, qwen"
        )


def _call_llm_stream(
    model_id: str,
    system_prompt: str,
    user_text: str,
    temperature: float = 1.0,
    top_p: float = 0.95,
    max_tokens: int = 2048,
):
    """Variant streaming de `_call_llm_raw`.

    Retorna un generador síncron que produeix strings (chunks de text) a
    mesura que el model els genera. El consumidor els pot re-emetre com
    a events SSE al frontend.

    Motivat pel pilot 2026-04-16: amb textos de 300-700 paraules i models
    com Gemma/Qwen que triguen 60-90s, veure pantalla buida és insostenible
    per a la UX. Amb streaming, l'usuari veu paraules apareixent des del
    segon 1-2. Cost i temps total idèntics a `_call_llm_raw`.

    Tots els providers suporten streaming via els seus SDK:
    - Google genai: `generate_content_stream(...)` retorna iterador de chunks
    - OpenAI (+ OpenRouter compat): `stream=True` retorna iterador de deltes
    - Mistral: HTTP `"stream": true` + parseig SSE
    """
    global _gemma4_key_idx, _gemini_key_idx, _openrouter_key_idx
    provider, specific_model = _resolve_model(model_id)
    if provider in ("gemma4", "gemini"):
        keys = GEMMA4_API_KEYS if provider == "gemma4" else GEMINI_API_KEYS
        if not keys:
            raise RuntimeError(f"No hi ha claus per al provider {provider}")
        errors = []
        for attempt in range(len(keys)):
            if provider == "gemma4":
                idx = (_gemma4_key_idx + attempt) % len(keys)
            else:
                idx = (_gemini_key_idx + attempt) % len(keys)
            client = genai.Client(
                api_key=keys[idx],
                http_options=types.HttpOptions(timeout=180_000),
            )
            try:
                # Gemma concatena system+user en un sol missatge; Gemini
                # passa el system via system_instruction (separat).
                if provider == "gemma4":
                    full = f"{system_prompt}\n\n---\n\n{user_text}" if system_prompt else user_text
                    stream = client.models.generate_content_stream(
                        model=specific_model,
                        contents=[types.Content(role="user", parts=[types.Part(text=full)])],
                        config=types.GenerateContentConfig(
                            temperature=temperature,
                            top_p=top_p,
                            max_output_tokens=max_tokens,
                        ),
                    )
                else:
                    stream = client.models.generate_content_stream(
                        model=specific_model,
                        contents=[types.Content(role="user", parts=[types.Part(text=user_text)])],
                        config=types.GenerateContentConfig(
                            system_instruction=system_prompt if system_prompt else None,
                            temperature=temperature,
                            top_p=top_p,
                            max_output_tokens=max_tokens,
                            thinking_config=types.ThinkingConfig(thinking_budget=0),
                        ),
                    )
                # Itera chunks. El primer chunk pot fallar (key quota), però si
                # arribem a iterar, ja està enganxat. Rotaci\u00f3 de clau només
                # al pre-stream.
                if provider == "gemma4":
                    _gemma4_key_idx = (idx + 1) % len(keys)
                else:
                    _gemini_key_idx = (idx + 1) % len(keys)
                for chunk in stream:
                    # google-genai: chunk.text pot ser None en heartbeats
                    txt = getattr(chunk, "text", None) or ""
                    if txt:
                        yield txt
                return  # stream consumit OK
            except Exception as e:
                errors.append(f"clau {idx+1}: {str(e)[:200]}")
                continue
        raise RuntimeError(f"Totes les claus {provider} han fallat (stream): {'; '.join(errors)}")
    elif provider in ("gpt", "openrouter"):
        from openai import OpenAI
        if provider == "openrouter":
            if not OPENROUTER_API_KEYS:
                raise RuntimeError("OPENROUTER_API_KEY no configurada")
            # Rotem entre claus d'OpenRouter fins que una accepti
            errors = []
            for attempt in range(len(OPENROUTER_API_KEYS)):
                idx = (_openrouter_key_idx + attempt) % len(OPENROUTER_API_KEYS)
                client = OpenAI(
                    api_key=OPENROUTER_API_KEYS[idx],
                    base_url="https://openrouter.ai/api/v1",
                )
                try:
                    messages = []
                    if system_prompt:
                        messages.append({"role": "system", "content": system_prompt})
                    messages.append({"role": "user", "content": user_text})
                    stream = client.chat.completions.create(
                        model=specific_model,
                        messages=messages,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        top_p=top_p,
                        stream=True,
                        extra_headers={
                            "HTTP-Referer": "https://atne.fje.cat",
                            "X-Title": "ATNE",
                        },
                    )
                    _openrouter_key_idx = (idx + 1) % len(OPENROUTER_API_KEYS)
                    for chunk in stream:
                        delta = chunk.choices[0].delta if chunk.choices else None
                        piece = getattr(delta, "content", None) if delta else None
                        if piece:
                            yield piece
                    return
                except Exception as e:
                    errors.append(f"clau {idx+1}: {str(e)[:200]}")
                    continue
            raise RuntimeError(f"Totes les claus OpenRouter han fallat (stream): {'; '.join(errors)}")
        else:
            # OpenAI directe (una sola clau)
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": user_text})
            stream = client.chat.completions.create(
                model=specific_model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                stream=True,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta if chunk.choices else None
                piece = getattr(delta, "content", None) if delta else None
                if piece:
                    yield piece
            return
    elif provider == "mistral":
        # Mistral via HTTP directe amb stream=true retorna SSE chunks
        r = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {MISTRAL_API_KEY}",
                "Content-Type": "application/json",
                "Accept": "text/event-stream",
            },
            json={
                "model": specific_model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_text},
                ],
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "stream": True,
            },
            stream=True,
            timeout=180,
        )
        if r.status_code != 200:
            raise RuntimeError(f"Mistral HTTP {r.status_code}: {r.text[:200]}")
        for line in r.iter_lines():
            if not line:
                continue
            if not line.startswith(b"data: "):
                continue
            data_str = line[6:].decode("utf-8", errors="ignore").strip()
            if data_str == "[DONE]":
                break
            try:
                obj = json.loads(data_str)
                piece = obj.get("choices", [{}])[0].get("delta", {}).get("content", "")
                if piece:
                    yield piece
            except Exception:
                continue
    else:
        raise RuntimeError(
            f"Model desconegut per a streaming: {model_id}. "
            f"Opcions: gemma4, gemma3, gemini, gpt, gpt-4o, qwen, mistral, mistral-large"
        )
