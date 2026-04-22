"""Estimació de cost per crida LLM (Sprint 1C, 2026-04-22).

Aquest mòdul converteix `(model, input_chars, output_chars)` en una estimació
del cost econòmic de la crida en EUR. S'usa per:
  - Capturar `cost_estimat_eur` a `atne_sessions` i `history`
  - Mostrar el cost acumulat al dashboard `/admin/pilot`
  - Activar alertes quan s'acosta a `admin_budget_eur_max`

És una **estimació** — els proveïdors no retornen sempre el comptatge exact
de tokens i el ràtio chars→tokens varia per tokenitzador. La diferència
sol ser <15%. Per al pilot (16 docents × 3 setmanes) és més que suficient
per a vigilar despeses i comparar models.

Preus consultats 2026-04-22. Cal revisar trimestralment.
USD → EUR: 0.92 (taxa conservadora; cal recalcular si fluctua >5%).
"""

from typing import Optional


# ── Conversió USD → EUR ────────────────────────────────────────────────────

USD_TO_EUR = 0.92


# ── Estimació tokens ───────────────────────────────────────────────────────
# 1 token ≈ 4 caràcters (BPE/tiktoken/SentencePiece estàn entre 3-5 per al
# català/castellà). Aquest ràtio dóna un error <15% per a textos pedagògics.
CHARS_PER_TOKEN = 4.0


def _chars_to_tokens(chars: int) -> int:
    if not chars or chars <= 0:
        return 0
    return int(chars / CHARS_PER_TOKEN) + 1


# ── Taula de preus per model (USD per 1M tokens) ──────────────────────────
#
# Format: (input_per_1M_usd, output_per_1M_usd)
# 0.0 = free tier (Google AI Studio per a Gemma 3/4 sense billing actiu).
#
# Si afegeixes un model nou aquí, recorda actualitzar també:
#   - adaptation/llm_clients.py::_MODEL_ALIASES (perquè es resolgui)
#   - docs/sql/sprint1b_admin_config.sql::system_config (default si cal)

_PRICES_USD_PER_1M: dict[str, tuple[float, float]] = {
    # Google — Gemma free tier (AI Studio sense billing)
    "gemma-4-31b-it":   (0.0, 0.0),
    "gemma-3-27b-it":   (0.0, 0.0),
    "gemma-3-12b-it":   (0.0, 0.0),
    "gemma-3n-e4b-it":  (0.0, 0.0),

    # Google — Gemini de pagament (vigent 2026-04)
    "gemini-2.5-flash":     (0.075, 0.30),
    "gemini-2.5-pro":       (1.25, 5.00),

    # OpenAI (vigent 2026-04, model "small/mini" line)
    "gpt-4o-mini":          (0.15,  0.60),
    "gpt-4o":               (2.50,  10.00),
    "gpt-4.1-mini":         (0.40,  1.60),
    "gpt-4.1":              (2.00,  8.00),

    # Mistral (vigent 2026-04)
    "mistral-small-latest": (0.10,  0.30),
    "mistral-large-latest": (2.00,  6.00),

    # OpenRouter / Qwen (variable; uso preus mitjans de mercat 2026-04)
    "qwen/qwen3.5-27b":     (0.20,  0.60),
    "qwen/qwen3.5-9b":      (0.10,  0.30),

    # Anthropic Claude (vigent 2026-04)
    "claude-haiku-4-5":     (1.00,  5.00),
    "claude-sonnet-4-6":    (3.00,  15.00),
    "claude-opus-4-7":      (15.00, 75.00),
}


def estimate_cost_eur(
    model: Optional[str],
    input_chars: int,
    output_chars: int,
) -> Optional[float]:
    """Estima el cost en EUR d'una crida LLM.

    Retorna None si no coneixem el model — millor NULL a la BD que un cost
    fals. El dashboard pot agregar només els valors no-NULL.
    """
    if not model:
        return None
    prices = _PRICES_USD_PER_1M.get(model)
    if prices is None:
        # Intenta normalitzar: alguns models arriben amb prefixos
        # (ex: "openai/gpt-4o-mini") que no tenim a la taula
        for known, p in _PRICES_USD_PER_1M.items():
            if known in model:
                prices = p
                break
        if prices is None:
            return None

    in_t = _chars_to_tokens(input_chars)
    out_t = _chars_to_tokens(output_chars)
    in_usd = (in_t / 1_000_000) * prices[0]
    out_usd = (out_t / 1_000_000) * prices[1]
    total_usd = in_usd + out_usd
    return round(total_usd * USD_TO_EUR, 6)


def is_free_model(model: Optional[str]) -> bool:
    """True si el model és free tier (preus = 0). Útil per al dashboard."""
    if not model:
        return False
    prices = _PRICES_USD_PER_1M.get(model)
    return prices == (0.0, 0.0)


def known_models() -> list[str]:
    """Llista de models amb preu definit. Útil per validar configuració."""
    return sorted(_PRICES_USD_PER_1M.keys())
