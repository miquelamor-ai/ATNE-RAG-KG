"""Configuració de llengües suportades per ATNE.

Cobreix: codi intern, etiqueta display, codi LanguageTool, flag beta.
Default: "ca" (català). Qualsevol codi desconegut recau a "ca".
"""

LANG_CONFIG: dict[str, dict] = {
    "ca": {"label": "català",    "lt_code": "ca",    "beta": False},
    "es": {"label": "castellà",  "lt_code": "es",    "beta": False},
    "en": {"label": "anglès",    "lt_code": "en-US", "beta": False},
    "fr": {"label": "francès",   "lt_code": "fr",    "beta": False},
    "gl": {"label": "gallec",    "lt_code": "gl-ES", "beta": True},
    "eu": {"label": "euskera",   "lt_code": "eu",    "beta": True},
}

_DEFAULT = LANG_CONFIG["ca"]


def get_lang_label(lang: str) -> str:
    """Retorna l'etiqueta legible ('català', 'anglès'…) per a un codi de llengua."""
    return LANG_CONFIG.get(lang, _DEFAULT)["label"]


def get_lt_code(lang: str) -> str:
    """Retorna el codi LanguageTool ('ca', 'en-US'…) per a un codi de llengua."""
    return LANG_CONFIG.get(lang, _DEFAULT)["lt_code"]


def is_beta(lang: str) -> bool:
    """True si la llengua té qualitat LLM limitada (gallec, euskera)."""
    return LANG_CONFIG.get(lang, _DEFAULT)["beta"]
