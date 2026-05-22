"""
Tests per a adaptation/pictograms_arasaac.py

Comprova:
  - Que [PICTO: agua] es resol en <img> amb URL ARASAAC correcta
  - Que múltiples marcadors es resolen en paral·lel
  - Que el fallback emoji apareix quan ARASAAC retorna 404
  - Que el text sense marcadors es retorna intacte
  - Que la cache in-memory evita crides duplicades

Tots els tests usen mock: zero crides reals a ARASAAC.
"""

from __future__ import annotations

import sys
import os
import time
from unittest.mock import MagicMock, patch

import pytest

# Assegurem que el root del projecte és al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adaptation.pictograms_arasaac import (
    ARASAAC_ATTRIBUTION,
    ARASAAC_STATIC_BASE,
    _FALLBACK_EMOJI,
    _arasaac_search,
    _marker_to_html,
    extract_pictogram_markers,
    resolve_pictogram_markers,
)


# ── Fixtures / helpers ────────────────────────────────────────────────────────

def _mock_arasaac_response(picto_id: int):
    """Simula la resposta JSON d'ARASAAC bestsearch amb un sol resultat."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = [{"_id": picto_id, "keywords": [{"keyword": "water"}]}]
    mock_resp.raise_for_status.return_value = None
    return mock_resp


def _mock_arasaac_404():
    """Simula una resposta 404 (pictograma no trobat)."""
    mock_resp = MagicMock()
    mock_resp.status_code = 404
    # raise_for_status no dispara res (gestionem 404 explícitament)
    return mock_resp


# ── Test 1: resolució bàsica d'un marcador ────────────────────────────────────

def test_single_marker_resolves_to_img():
    """[PICTO: agua] → <img> amb URL ARASAAC correcta."""
    # Purga cache per evitar contaminació entre tests
    import adaptation.pictograms_arasaac as mod
    mod._CACHE.clear()

    picto_id = 2542
    expected_url = f"{ARASAAC_STATIC_BASE}/{picto_id}/{picto_id}_300.png"

    with patch("adaptation.pictograms_arasaac.requests.get",
               return_value=_mock_arasaac_response(picto_id)):
        result = resolve_pictogram_markers("Beu [PICTO: agua] cada dia.", lang="ca")

    assert "<img" in result
    assert expected_url in result
    assert 'class="arasaac-picto"' in result
    assert 'alt="agua"' in result
    assert "[PICTO:" not in result  # marcador substituït


# ── Test 2: fallback quan ARASAAC retorna 404 ─────────────────────────────────

def test_fallback_on_404():
    """Quan ARASAAC retorna 404, el marcador es substitueix per emoji fallback."""
    import adaptation.pictograms_arasaac as mod
    mod._CACHE.clear()

    with patch("adaptation.pictograms_arasaac.requests.get",
               return_value=_mock_arasaac_404()):
        result = resolve_pictogram_markers("Text amb [PICTO: termedesconegut].", lang="ca")

    # El marcador s'ha substituit (no queda al text)
    assert "[PICTO:" not in result
    # El fallback emoji hi és
    assert _FALLBACK_EMOJI in result


# ── Test 3: múltiples marcadors en paral·lel ─────────────────────────────────

def test_multiple_markers_parallel():
    """Tres marcadors diferents es resolen tots en paral·lel."""
    import adaptation.pictograms_arasaac as mod
    mod._CACHE.clear()

    ids = {"sol": 9999, "agua": 2542, "planta": 1234}

    call_count = 0

    def mock_get(url, **kwargs):
        nonlocal call_count
        call_count += 1
        # Determina quin terme s'ha demanat per retornar l'id corresponent
        for terme, pid in ids.items():
            if terme in url:
                return _mock_arasaac_response(pid)
        return _mock_arasaac_404()

    text = "El [PICTO: sol] escalfa. L'[PICTO: agua] cau. La [PICTO: planta] creix."
    with patch("adaptation.pictograms_arasaac.requests.get", side_effect=mock_get):
        result = resolve_pictogram_markers(text, lang="ca", max_workers=3)

    # Cap marcador ha de quedar al text
    assert "[PICTO:" not in result
    # Tenim 3 imatges
    assert result.count("<img") == 3


# ── Test 4: text sense marcadors retorna intacte ─────────────────────────────

def test_no_markers_returns_unchanged():
    """Text sense [PICTO:] no es modifica ni es fa cap crida a ARASAAC."""
    text = "Text sense pictogrames. Res a canviar."
    with patch("adaptation.pictograms_arasaac.requests.get") as mock_get:
        result = resolve_pictogram_markers(text)
    assert result == text
    mock_get.assert_not_called()


# ── Test 5: cache in-memory evita crides duplicades ──────────────────────────

def test_cache_avoids_duplicate_calls():
    """El mateix terme en dos marcadors fa només UNA crida a ARASAAC."""
    import adaptation.pictograms_arasaac as mod
    mod._CACHE.clear()

    call_count = 0

    def mock_get(url, **kwargs):
        nonlocal call_count
        call_count += 1
        return _mock_arasaac_response(2542)

    text = "L'[PICTO: agua] és vida. Beu [PICTO: agua] cada dia."
    with patch("adaptation.pictograms_arasaac.requests.get", side_effect=mock_get):
        result = resolve_pictogram_markers(text, lang="ca")

    # Dos marcadors però UN sol terme únic → una sola crida real
    assert call_count == 1
    # Però tots dos marcadors s'han substituït
    assert "[PICTO:" not in result
    assert result.count("<img") == 2


# ── Test 6: _marker_to_html amb URL vàlida ───────────────────────────────────

def test_marker_to_html_with_url():
    url = f"{ARASAAC_STATIC_BASE}/2542/2542_300.png"
    html = _marker_to_html("agua", url)
    assert "<img" in html
    assert url in html
    assert 'class="arasaac-picto"' in html
    assert ARASAAC_ATTRIBUTION in html


# ── Test 7: _marker_to_html amb URL None → fallback ──────────────────────────

def test_marker_to_html_none_url():
    html = _marker_to_html("termedesconegut", None)
    assert html == _FALLBACK_EMOJI
    assert "<img" not in html


# ── Test 8: extract_pictogram_markers ────────────────────────────────────────

def test_extract_markers():
    text = "El [PICTO: sol] i la [PICTOGRAMA: lluna] brillen."
    termes = extract_pictogram_markers(text)
    assert "sol" in termes
    assert "lluna" in termes
    assert len(termes) == 2


# ── Test 9: fallback quan requests llança excepció ───────────────────────────

def test_fallback_on_exception():
    """Si requests.get llança ConnectionError, el marcador queda com a fallback."""
    import adaptation.pictograms_arasaac as mod
    mod._CACHE.clear()

    with patch("adaptation.pictograms_arasaac.requests.get",
               side_effect=ConnectionError("simulated network error")):
        result = resolve_pictogram_markers("Test [PICTO: sol].", lang="ca")

    assert "[PICTO:" not in result
    assert _FALLBACK_EMOJI in result
