"""
Resolucio de marcadors de pictograma via API publica ARASAAC.

Motiu: pilot 2026-05-21 — un docent va denunciar que "Pictogrames no son
pictogrames, son emojis. Haurien de ser els ARASAAC". Aquesta decissio
pedagogica queda documentada aqui com a referencia.

Flux:
  LLM emet  [PICTO: terme_en_castella]  ← castella per millor cobertura ARASAAC
  →  ARASAAC API cerca el terme (bestsearch, lang="es")
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
# Accepta [PICTO: terme] o [PICTO: terme_display|terme_cerca]
# El format amb | permet mostrar el terme en l'idioma del document (esquerre)
# i usar el terme de cerca ARASAAC (dret, normalment castellà per cobertura).
MARKER_RE = re.compile(r"\[PICTO(?:GRAMA)?:\s*([^\]]+)\]", re.IGNORECASE)


def _parse_marker(raw: str) -> tuple[str, str]:
    """Retorna (display_term, search_term) del contingut d'un marcador.

    Si el marcador conté '|' (ex: 'gat|gato'), retorna ('gat', 'gato').
    Si no, usa el mateix terme per a display i cerca.
    """
    parts = raw.split("|", 1)
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    return raw.strip(), raw.strip()

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

def _marker_to_html(display_term: str, img_url: Optional[str]) -> str:
    """Converteix un resultat de cerca en HTML o emoji de fallback.

    display_term: terme en l'idioma del document (per a alt/title).
    """
    if img_url:
        kw_escaped = display_term.replace('"', "&quot;")
        return (
            f'<img src="{img_url}" '
            f'alt="{kw_escaped}" '
            f'class="arasaac-picto" '
            f'loading="lazy" '
            f'title="{kw_escaped} — {ARASAAC_ATTRIBUTION}">'
        )
    # Fallback: emoji neutre en <span> amb classe per poder eliminar-lo al PDF
    kw_esc = display_term.replace('"', "&quot;")
    return f'<span class="picto-fallback-text" title="{kw_esc}">{_FALLBACK_EMOJI}</span>'


def resolve_pictogram_markers(text: str, lang: str = "es", max_workers: int = 4) -> str:
    """Substitueix tots els marcadors [PICTO: terme] del text per img ARASAAC.

    Suporta dos formats de marcador:
      [PICTO: gato]          → cerca "gato" en lang, alt="gato"
      [PICTO: gat|gato]      → cerca "gato" en lang, alt="gat" (display en idioma del doc)

    Processa els marcadors en paral·lel (ThreadPoolExecutor) per minimitzar
    la latència total quan hi ha múltiples pictogrames al document.

    Args:
        text:        text que conté marcadors [PICTO: terme].
        lang:        idioma de cerca ARASAAC (per defecte 'es' — millor cobertura).
        max_workers: màxim de fils paral·lels per a les crides ARASAAC.

    Returns:
        Text amb els marcadors substituïts per <img> o emoji de fallback.
        Si no hi ha cap marcador, retorna el text intacte (zero overhead).
    """
    matches = list(MARKER_RE.finditer(text))
    if not matches:
        return text

    # Parsejem cada marcador per obtenir (display, search)
    raw_to_parsed: dict[str, tuple[str, str]] = {}
    for m in matches:
        raw = m.group(1)
        raw_to_parsed[raw] = _parse_marker(raw)

    # Recollim termes de cerca únics per evitar crides duplicades
    search_terms = list({search for _, search in raw_to_parsed.values()})

    # Resolem en paral·lel
    search_to_url: dict[str, Optional[str]] = {}
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(_arasaac_search, kw, lang): kw for kw in search_terms}
        for f, kw in futures.items():
            try:
                search_to_url[kw] = f.result(timeout=10)
            except Exception as exc:
                print(f"[arasaac] timeout/error per '{kw}': {exc}", flush=True)
                search_to_url[kw] = None

    # Substitució de dreta a esquerra per mantenir els índexs vàlids.
    result = text
    for m in reversed(list(MARKER_RE.finditer(text))):
        raw = m.group(1)
        display, search = raw_to_parsed[raw]
        html = _marker_to_html(display, search_to_url.get(search))
        result = result[: m.start()] + html + result[m.end():]

    return result


def extract_pictogram_markers(text: str) -> list[str]:
    """Retorna la llista de termes dels marcadors [PICTO:...] al text."""
    return [m.group(1).strip() for m in MARKER_RE.finditer(text)]
