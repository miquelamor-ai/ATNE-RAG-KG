"""
Resolucio de marcadors de pictograma via API publica ARASAAC.

Motiu: pilot 2026-05-21 — un docent va denunciar que "Pictogrames no son
pictogrames, son emojis. Haurien de ser els ARASAAC". Aquesta decissio
pedagogica queda documentada aqui com a referencia.

Flux:
  LLM emet  [PICTO: terme_en_catala]
  →  ARASAAC API cerca el terme (bestsearch)
  →  retorna URL imatge estatica (300 px PNG)
  →  substitut a <img class="arasaac-picto"> dins del text

Fallback: si ARASAAC no retorna cap resultat o la crida falla, el marcador
es substitueix per un emoji Unicode genèric (no es trenca res).

Llicencia ARASAAC: CC BY-NC-SA 4.0
  Pictogrames d'Sergio Palao per a ARASAAC (http://arasaac.org)
  Llicencia: Creative Commons BY-NC-SA 4.0
  Propietat de: Govern d'Aragó (CATEDU)

Veure: https://arasaac.org/desarrolladores/api
"""

from __future__ import annotations

import re
import time as _time_mod
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

import requests

ARASAAC_API_BASE = "https://api.arasaac.org/v1/pictograms"
ARASAAC_STATIC_BASE = "https://static.arasaac.org/pictograms"
USER_AGENT = "ATNE-FJE-EducationalBot/1.0 (https://atne.fje.edu)"

ARASAAC_ATTRIBUTION = (
    "Pictogrames d’ARASAAC (Sergio Palao / Govern d’Aragó, CATEDU)"
    " — CC BY-NC-SA 4.0"
)

# Marcadors que el LLM ha d'emetre.
# Accepta tant [PICTO: terme] com [PICTOGRAMA: terme] per robustesa.
MARKER_RE = re.compile(r"\[PICTO(?:GRAMA)?:\s*([^\]]+)\]", re.IGNORECASE)

# Emoji de fallback quan ARASAAC no troba res per al terme
_FALLBACK_EMOJI = "\U0001f4dd"  # 📝

# Idiomes suportats per ARASAAC bestsearch (per si cal canviar de "ca" a "es")
_LANG_FALLBACK = {"ca": "es"}

# ── Cache in-memory (TTL 60 min) ─────────────────────────────────────────────

_CACHE: dict[str, tuple[float, Optional[str]]] = {}
_CACHE_TTL = 60 * 60.0


def _cache_get(key: str) -> tuple[bool, Optional[str]]:
    """Retorna (hit, valor). Si caducat, esborra i retorna (False, None)."""
    entry = _CACHE.get(key)
    if entry is None:
        return False, None
    expiry, val = entry
    if _time_mod.time() > expiry:
        _CACHE.pop(key, None)
        return False, None
    return True, val


def _cache_put(key: str, val: Optional[str]) -> None:
    if len(_CACHE) > 1000:
        now = _time_mod.time()
        for k in [k for k, (e, _) in _CACHE.items() if e <= now]:
            _CACHE.pop(k, None)
    _CACHE[key] = (_time_mod.time() + _CACHE_TTL, val)


# ── Cerca ARASAAC ─────────────────────────────────────────────────────────────

def _arasaac_search(keyword: str, lang: str = "ca", timeout: int = 5) -> Optional[str]:
    """Cerca el terme a ARASAAC i retorna la URL PNG 300px, o None.

    Prova primer amb l'idioma demanat (ex: "ca") i, si no hi ha resultats,
    amb l'idioma de fallback (ex: "es"). ARASAAC suporta ca, es, en, fr, de...

    Returns:
        URL string tipus "https://static.arasaac.org/pictograms/{id}/{id}_300.png"
        o None si no s'ha trobat cap pictograma.
    """
    cache_key = f"{lang}:{keyword}"
    hit, cached = _cache_get(cache_key)
    if hit:
        return cached

    langs_to_try = [lang]
    fallback = _LANG_FALLBACK.get(lang)
    if fallback and fallback != lang:
        langs_to_try.append(fallback)

    headers = {"User-Agent": USER_AGENT}
    url_result: Optional[str] = None

    for try_lang in langs_to_try:
        endpoint = f"{ARASAAC_API_BASE}/{try_lang}/bestsearch/{requests.utils.quote(keyword)}"
        try:
            r = requests.get(endpoint, headers=headers, timeout=timeout)
            if r.status_code == 404:
                continue
            r.raise_for_status()
            data = r.json()
        except Exception as exc:
            print(f"[arasaac] error cercant '{keyword}' ({try_lang}): {exc}", flush=True)
            continue

        # La resposta és un array. El primer element és el millor resultat.
        if isinstance(data, list) and data:
            picto_id = data[0].get("_id")
            if picto_id:
                url_result = f"{ARASAAC_STATIC_BASE}/{picto_id}/{picto_id}_300.png"
                break
        elif isinstance(data, dict) and data.get("_id"):
            picto_id = data["_id"]
            url_result = f"{ARASAAC_STATIC_BASE}/{picto_id}/{picto_id}_300.png"
            break

    _cache_put(cache_key, url_result)
    if url_result:
        print(f"[arasaac] '{keyword}' ({lang}) → {url_result}", flush=True)
    else:
        print(f"[arasaac] '{keyword}' no trobat (fallback emoji)", flush=True)

    return url_result


# ── Substitució de marcadors ──────────────────────────────────────────────────

def _marker_to_html(keyword: str, img_url: Optional[str]) -> str:
    """Converteix un resultat de cerca en HTML o emoji de fallback."""
    if img_url:
        kw_escaped = keyword.replace('"', "&quot;")
        return (
            f'<img src="{img_url}" '
            f'alt="{kw_escaped}" '
            f'class="arasaac-picto" '
            f'loading="lazy" '
            f'title="{kw_escaped} — {ARASAAC_ATTRIBUTION}">'
        )
    # Fallback: emoji neutre; no trenca el text
    return _FALLBACK_EMOJI


def resolve_pictogram_markers(text: str, lang: str = "ca", max_workers: int = 4) -> str:
    """Substitueix tots els marcadors [PICTO: terme] del text per img ARASAAC.

    Processa els marcadors en paral·lel (ThreadPoolExecutor) per minimitzar
    la latència total quan hi ha múltiples pictogrames al document.

    Args:
        text:        text que conté marcadors [PICTO: terme].
        lang:        idioma del terme (per defecte 'ca' = català).
        max_workers: màxim de fils paral·lels per a les crides ARASAAC.

    Returns:
        Text amb els marcadors substituïts per <img> o emoji de fallback.
        Si no hi ha cap marcador, retorna el text intacte (zero overhead).
    """
    matches = list(MARKER_RE.finditer(text))
    if not matches:
        return text

    # Recollim termes únics per evitar crides duplicades
    keywords = list({m.group(1).strip() for m in matches})

    # Resolem en paral·lel
    keyword_to_url: dict[str, Optional[str]] = {}
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(_arasaac_search, kw, lang): kw for kw in keywords}
        for f, kw in futures.items():
            try:
                keyword_to_url[kw] = f.result(timeout=10)
            except Exception as exc:
                print(f"[arasaac] timeout/error per '{kw}': {exc}", flush=True)
                keyword_to_url[kw] = None

    # Substitució d'esquerra a dreta (preservant posicions)
    # Recorrem de dreta a esquerra per mantenir els índexs vàlids.
    result = text
    for m in reversed(list(MARKER_RE.finditer(text))):
        kw = m.group(1).strip()
        html = _marker_to_html(kw, keyword_to_url.get(kw))
        result = result[: m.start()] + html + result[m.end():]

    return result


def extract_pictogram_markers(text: str) -> list[str]:
    """Retorna la llista de termes dels marcadors [PICTO:...] al text."""
    return [m.group(1).strip() for m in MARKER_RE.finditer(text)]
