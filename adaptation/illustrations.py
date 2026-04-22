"""
Resolucio de marcadors d'il·lustracio per al complement "illustracions".

Disparem Wikimedia Commons i FLUX-schnell (Pollinations) en paral·lel i
retornem les dues opcions al docent, que tria.

Entrada: concepte curt en catala (ex: "cicle de l'aigua") + context (MECR,
materia, seed del document, estil).

Sortida: dict amb 2 opcions (wikimedia + flux) per al frontend.

Veure `corpus/skills_proto/complements/generate-illustracions/SKILL.md` v0.3.
"""

from __future__ import annotations

import json
import os
import re
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field
from typing import Any, Optional
from urllib.parse import quote

import requests


WIKIMEDIA_API = "https://commons.wikimedia.org/w/api.php"
POLLINATIONS_BASE = "https://image.pollinations.ai/prompt/"
USER_AGENT = "ATNE-FJE-EducationalBot/1.0 (https://atne.fje.edu)"

# 7 estils validats empiricament (veure SKILL.md frontmatter).
STYLE_SPINES: dict[str, str] = {
    "vectorial_editorial": (
        "Flat vector illustration, clean geometric shapes, bold simple "
        "outlines, limited flat color palette, smooth shapes, friendly "
        "editorial style, no gradients, no texture, centered composition."
    ),
    "isometric_infografic": (
        "Isometric 3D illustration, 30 degree angle, clean geometric shapes, "
        "crisp edges, limited color palette with soft pastels, subtle "
        "shading, infographic textbook style, high clarity."
    ),
    "aquarela_storybook": (
        "Soft watercolor storybook illustration, gentle wet-edge washes, "
        "warm palette of ochre sap green and dusty blue, hand-drawn feel, "
        "cozy lighting, loose brushwork, paper texture background, children "
        "book aesthetic."
    ),
    "icona_minimalista": (
        "Minimalist flat icon, single concept, centered, thick rounded "
        "outlines, two or three flat colors, solid shapes, no gradient, "
        "generous padding, pictogram style, high legibility."
    ),
    "claymation_plastilina": (
        "Handmade claymation style, stop-motion plasticine figures, soft "
        "studio lighting, visible fingerprint texture, saturated but warm "
        "colors, shallow depth of field, tabletop scene, cheerful children's "
        "educational look."
    ),
    "escala_grisos_carbonet": (
        "Monochrome charcoal and graphite drawing, soft grey tones, "
        "hand-drawn on textured cream paper, expressive loose lines, subtle "
        "cross-hatching, high contrast, no color, editorial book "
        "illustration style, dignified historical feel."
    ),
    "fotografia_documental": (
        "Vintage documentary photograph, warm sepia and amber tones, 35mm "
        "film grain, natural soft window light, shallow depth of field, "
        "authentic atmosphere, editorial photojournalism style, slight age "
        "patina."
    ),
}

POSITIVE_SUFFIX = (
    "Single clear focal point, clean composition, soft cream paper "
    "background, no text, no letters, no captions, no signage."
)

DEFAULT_STYLE = "aquarela_storybook"
MARKER_RE = re.compile(r"\[IMATGE:\s*([^\]]+)\]")


@dataclass
class WikimediaOption:
    kind: str = "wikimedia"
    title: str = ""
    thumb_url: str = ""
    full_url: str = ""
    license: str = ""
    author: str = ""
    description: str = ""

    @property
    def attribution(self) -> str:
        author_plain = re.sub(r"<[^>]+>", "", self.author)[:80].strip() or "anonim"
        return f"Wikimedia Commons · {author_plain} · {self.license}"


@dataclass
class PexelsOption:
    kind: str = "pexels"
    title: str = ""
    thumb_url: str = ""
    full_url: str = ""
    photographer: str = ""
    photographer_url: str = ""
    license: str = "Pexels License"

    @property
    def attribution(self) -> str:
        return f"Pexels · {self.photographer or 'anonim'}"


@dataclass
class FluxOption:
    kind: str = "flux"
    url: str = ""
    style: str = DEFAULT_STYLE
    brief: str = ""
    attribution: str = "Generat amb FLUX.1-schnell (il·lustracio IA)"


@dataclass
class Resolution:
    concept: str
    wikimedia: Optional[WikimediaOption] = None
    wikimedia_alternatives: list[WikimediaOption] = field(default_factory=list)
    pexels: Optional[PexelsOption] = None
    pexels_alternatives: list[PexelsOption] = field(default_factory=list)
    flux: Optional[FluxOption] = None
    # Llista interleavada [wiki0, pexels0, wiki1, pexels1, ...] per al carrusel
    # unificat del frontend (una sola columna "Imatge trobada").
    search_results: list[dict] = field(default_factory=list)
    error: Optional[str] = None
    wikimedia_query: str = ""
    flux_brief: str = ""

    def to_dict(self) -> dict[str, Any]:
        d = {
            "concept": self.concept,
            "wikimedia_query": self.wikimedia_query,
            "flux_brief": self.flux_brief,
            "wikimedia": asdict(self.wikimedia) if self.wikimedia else None,
            "wikimedia_alternatives": [asdict(w) for w in self.wikimedia_alternatives],
            "pexels": asdict(self.pexels) if self.pexels else None,
            "pexels_alternatives": [asdict(p) for p in self.pexels_alternatives],
            "flux": asdict(self.flux) if self.flux else None,
            "search_results": self.search_results,
            "error": self.error,
        }
        return d


def extract_markers(text: str) -> list[dict]:
    """Retorna llista de marcadors trobats al text: [{start, end, concept}, ...]."""
    return [
        {"start": m.start(), "end": m.end(), "concept": m.group(1).strip()}
        for m in MARKER_RE.finditer(text)
    ]


# ---- Gemma 3 translator: Catalan concept -> (English query, English brief)

_GEMMA_PROMPT_TEMPLATE = """Converteixes un concepte educatiu en catala en 2 sortides angleses.

CONCEPTE (catala): "{concept}"
NIVELL MECR: {mecr}
MATERIA: {subject}

Retorna UN SOL objecte JSON (sense code fences, sense explicacions):
{{
  "wikimedia_query": "<2-5 paraules clau en angles per cercar a Wikimedia Commons>",
  "flux_brief": "<descripcio d'escena en angles, 20-40 paraules, concreta i visual>"
}}

Regles del flux_brief:
- Concret i visual: subjecte + accio + escenari + llum.
- Nomes afirmacions POSITIVES ("show X"), mai negacions ("no Y", "avoid Y").
- NO incloguis paraules d'estil (watercolor, flat, illustration, painting, cartoon).
- NO descriguis enquadrament fotografic si el concepte no n'ho demana.
- Si el concepte es tecnic-microscopic (cel·lules, atoms), reformula a
  nivell macroscopic observable (ex: "leaf in sunlight" en lloc de "chloroplasts").
- Ajusta la complexitat al nivell MECR si ve donat (A1-A2 simple, C1-C2 mes detalls).

Respon nomes amb el JSON."""


def _gemma_translate(concept: str, context: dict) -> dict:
    """Tradueix concepte catala -> (query angles, brief angles).

    Usa Gemini 2.5 Flash-Lite amb thinking_budget=0: ~0.7-1s per crida.
    Benchmarks: Gemma 3 27B ~10s, Gemini 2.5 Flash ~1.2s, Flash-Lite ~0.7s.
    Regla cost Miquel 2026-04-21: mantenir thinking_budget=0.
    """
    from google import genai
    from google.genai import types

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GEMMA4_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY no disponible")
    client = genai.Client(api_key=api_key)
    prompt = _GEMMA_PROMPT_TEMPLATE.format(
        concept=concept,
        mecr=context.get("mecr") or "B1",
        subject=context.get("subject") or "general",
    )
    resp = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
            thinking_config=types.ThinkingConfig(thinking_budget=0),
        ),
    )
    text = (resp.text or "").strip()
    # Treu fences
    m = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
    if m:
        text = m.group(1)
    # Primer objecte JSON balancejat
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if m:
        text = m.group(0)
    return json.loads(text)


# ---- Pexels search
#
# API gratuïta amb key gratuïta (https://www.pexels.com/api/). Si la variable
# d'entorn PEXELS_API_KEY no està definida, la funció retorna [] i el frontend
# cau al carrusel de Wikimedia sol (backward compat, zero trencament).

PEXELS_API = "https://api.pexels.com/v1/search"


def search_pexels(query: str, limit: int = 3) -> list[PexelsOption]:
    """Cerca a Pexels. Retorna [] si no hi ha PEXELS_API_KEY o si falla."""
    api_key = os.getenv("PEXELS_API_KEY", "").strip()
    if not api_key or not query:
        return []
    try:
        r = requests.get(
            PEXELS_API,
            params={"query": query, "per_page": limit, "orientation": "landscape"},
            headers={"Authorization": api_key, "User-Agent": USER_AGENT},
            timeout=12,
        )
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        print(f"[pexels] search error: {e}")
        return []
    hits: list[PexelsOption] = []
    for photo in data.get("photos", []):
        src = photo.get("src", {}) or {}
        # 'large' ~940x650 (suficient per chooser); 'large2x' ~1880x1300 per al final
        thumb = src.get("large", "") or src.get("medium", "")
        full = src.get("large2x", "") or src.get("large", "") or src.get("original", "")
        if not thumb:
            continue
        hits.append(PexelsOption(
            title=(photo.get("alt") or "")[:120] or (photo.get("photographer") or "")[:120],
            thumb_url=thumb,
            full_url=full,
            photographer=(photo.get("photographer") or "")[:80],
            photographer_url=photo.get("photographer_url") or "",
        ))
    return hits


# ---- Wikimedia search

def search_wikimedia(query: str, limit: int = 1) -> list[WikimediaOption]:
    """Cerca al Commons. Retorna top-N hits amb metadata. Robust a 429/500."""
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": f"{query} filetype:bitmap|drawing",
        "gsrnamespace": 6,  # File:
        "gsrlimit": limit,
        "prop": "imageinfo",
        "iiprop": "url|size|mime|extmetadata",
        "iiurlwidth": 800,
    }
    headers = {"User-Agent": USER_AGENT}
    try:
        r = requests.get(WIKIMEDIA_API, params=params, headers=headers, timeout=15)
        r.raise_for_status()
        data = r.json()
    except Exception:
        return []

    hits: list[WikimediaOption] = []
    for _pid, page in data.get("query", {}).get("pages", {}).items():
        info_list = page.get("imageinfo") or []
        if not info_list:
            continue
        info = info_list[0]
        meta = info.get("extmetadata", {}) or {}
        thumb = info.get("thumburl")
        if not thumb:
            continue
        hits.append(
            WikimediaOption(
                title=page.get("title", ""),
                thumb_url=thumb,
                full_url=info.get("url", ""),
                license=(meta.get("LicenseShortName") or {}).get("value", "?"),
                author=(meta.get("Artist") or {}).get("value", ""),
                description=((meta.get("ImageDescription") or {}).get("value", ""))[:300],
            )
        )
    return hits


# ---- FLUX (Pollinations)

def build_flux_url(brief: str, style: str, seed: int) -> str:
    """Construeix URL Pollinations deterministica (imatge es genera en GET)."""
    spine = STYLE_SPINES.get(style, STYLE_SPINES[DEFAULT_STYLE])
    full = f"{spine} {brief} {POSITIVE_SUFFIX}"
    return (
        f"{POLLINATIONS_BASE}{quote(full)}"
        f"?width=1024&height=768&nologo=true&model=flux&seed={seed}"
        f"&enhance=false&referrer=atne-fje"
    )


def flux_option(brief: str, style: str, seed: int) -> FluxOption:
    """Retorna opcio FLUX (URL directa, el navegador descarrega)."""
    return FluxOption(url=build_flux_url(brief, style, seed), style=style, brief=brief)


# ---- Resolutor principal

def resolve_marker(
    concept_ca: str,
    context: Optional[dict] = None,
    style: str = DEFAULT_STYLE,
    seed: int = 42,
) -> Resolution:
    """Resol un marcador [IMATGE: concept_ca] en paral·lel (Gemma 3, Wikimedia, FLUX).

    Args:
        concept_ca: concepte curt en catala (ex: "cicle de l'aigua").
        context: {"mecr": "B1", "subject": "ciencies_naturals", ...}.
        style: un dels 7 presets a STYLE_SPINES.
        seed: mateixa per a totes les imatges del mateix document.

    Returns:
        Resolution amb up to 2 opcions + metadata. Error si ambdues fallen.
    """
    ctx = context or {}
    result = Resolution(concept=concept_ca)

    # 1. Traduccio concept -> query + brief (via Gemma 3)
    try:
        translated = _gemma_translate(concept_ca, ctx)
        result.wikimedia_query = (translated.get("wikimedia_query") or "").strip()
        result.flux_brief = (translated.get("flux_brief") or "").strip()
    except Exception as e:
        # Fallback: fem servir el concepte catala brut (Wikimedia de vegades hi va)
        result.wikimedia_query = concept_ca
        result.flux_brief = concept_ca
        result.error = f"gemma_translate: {str(e)[:100]}"

    # 2. Paral·lel: Wikimedia (3 hits) + Pexels (3 hits) + FLUX URL
    with ThreadPoolExecutor(max_workers=3) as ex:
        f_wiki = ex.submit(search_wikimedia, result.wikimedia_query, 3)
        f_pex = ex.submit(search_pexels, result.wikimedia_query, 3)
        f_flux = ex.submit(flux_option, result.flux_brief, style, seed)
        try:
            wiki_hits = f_wiki.result(timeout=20)
        except Exception:
            wiki_hits = []
        try:
            pex_hits = f_pex.result(timeout=15)
        except Exception:
            pex_hits = []
        try:
            flux_opt = f_flux.result(timeout=10)
        except Exception:
            flux_opt = None

    if wiki_hits:
        result.wikimedia = wiki_hits[0]
        result.wikimedia_alternatives = wiki_hits[1:]
    if pex_hits:
        result.pexels = pex_hits[0]
        result.pexels_alternatives = pex_hits[1:]
    if flux_opt:
        result.flux = flux_opt

    # 3. Llista unificada interleavada [wiki0, pexels0, wiki1, pexels1, ...]
    #    El docent la recorre com a un sol carrusel (la primera columna del
    #    chooser) i veu alternança natural de fonts.
    unified: list[dict] = []
    max_len = max(len(wiki_hits), len(pex_hits))
    for i in range(max_len):
        if i < len(wiki_hits):
            w = wiki_hits[i]
            unified.append({
                "source": "wikimedia",
                "title": w.title,
                "thumb_url": w.thumb_url,
                "full_url": w.full_url or w.thumb_url,
                "attribution": w.attribution,
                "license": w.license,
            })
        if i < len(pex_hits):
            p = pex_hits[i]
            unified.append({
                "source": "pexels",
                "title": p.title,
                "thumb_url": p.thumb_url,
                "full_url": p.full_url,
                "attribution": p.attribution,
                "license": p.license,
                "photographer_url": p.photographer_url,
            })
    result.search_results = unified

    return result


def resolve_all_markers(
    text: str,
    context: Optional[dict] = None,
    style: str = DEFAULT_STYLE,
    seed: int = 42,
    max_workers: int = 3,
) -> list[dict]:
    """Extreu tots els marcadors del text i els resol en paral·lel.

    Retorna llista de dicts: [{start, end, concept, resolution}, ...]
    mantenint l'ordre original i la posicio al text.
    """
    markers = extract_markers(text)
    if not markers:
        return []

    results: list[dict] = []
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {
            ex.submit(resolve_marker, m["concept"], context, style, seed): m
            for m in markers
        }
        for f in futures:
            m = futures[f]
            try:
                res = f.result()
            except Exception as e:
                res = Resolution(concept=m["concept"], error=str(e)[:200])
            results.append({
                "start": m["start"],
                "end": m["end"],
                "concept": m["concept"],
                "resolution": res.to_dict(),
            })
    # Mantenim ordre per posicio
    results.sort(key=lambda r: r["start"])
    return results
