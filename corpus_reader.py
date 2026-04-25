"""
corpus_reader.py — Lector d'instruccions d'adaptació des del corpus MD.

Branca prompt-v2-rag: les instruccions viuen als MD, no al codi Python.
Llegeix les seccions "## 6. INSTRUCCIONS D'ADAPTACIÓ TEXTUAL PER A L'LLM"
dels fitxers del corpus/ i retorna els blocs per a build_system_prompt().

Referència: docs/decisions/arquitectura_prompt_v2.md
"""

import re
from pathlib import Path

from adaptation.lang_config import get_lang_label

CORPUS_DIR = Path(__file__).parent / "corpus"

# ═══════════════════════════════════════════════════════════════════════════════
# Cache en memòria (es carrega 1 cop al iniciar el servidor)
# ═══════════════════════════════════════════════════════════════════════════════

_cache: dict = {}


def _extract_section(text: str, heading: str) -> str:
    """Extreu el contingut d'una secció markdown (fins a la propera ## del mateix nivell).
    El heading es cerca com a prefix (pot tenir text addicional a la línia)."""
    pattern = rf"^{re.escape(heading)}[^\n]*\n(.*?)(?=\n## |\Z)"
    m = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    return m.group(1).strip() if m else ""


def _extract_code_blocks(text: str) -> list[str]:
    """Extreu tots els blocs de codi (```) d'un text markdown."""
    return re.findall(r"```\n?(.*?)```", text, re.DOTALL)


def _load_file(filename: str) -> str:
    """Llegeix un fitxer MD del corpus. Retorna string buit si no existeix."""
    path = CORPUS_DIR / filename
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def load_corpus():
    """Carrega tots els blocs d'instruccions del corpus a la cache."""
    global _cache
    _cache = {
        "profiles": {},
        "mecr": {},
        "dua": {},
        "genres": {},
        "crossings": [],
        "cognitive_load": {},
        "conflict_resolution": "",
        "fewshot": {},
        "identity": "",
        "universal_rules": "",
    }

    # ── Identitat i regles universals (fixes, hardcoded mínim) ──
    _cache["identity"] = """Ets l'assistent ATNE (Adaptador de Textos a Necessitats Educatives) de Jesuïtes Educació.

OBJECTIU: Transformar textos educatius perquè siguin accessibles a l'alumnat descrit, seguint principis de DUA, Lectura Fàcil i MECR.

TO: Acadèmic neutre. Respecta el registre del text original quan sigui identificable.

FIDELITAT:
- En adaptació: cada element ha de tenir correspondència amb l'original (Mayer). No inventis dades, exemples ni fets.
- En complements (glossari, preguntes, esquemes): crea contingut nou derivat del text adaptat.

RIGOR TERMINOLÒGIC: Conserva sempre els termes curriculars. Defineix-los, no els eliminis. MAI substitueixis per parafrasis buides ("la cosa verda", "el que fa que", "un tipus de").

FORMAT: Comença DIRECTAMENT amb "## Text adaptat". Zero meta-text ("Here is...", "Let me...", "Okay...").

LLENGUA: Català (o la llengua vehicular indicada).

SEGURETAT:
- No reprodueixis dades personals de l'alumne al text adaptat.
- Evita exemples potencialment traumàtics amb perfils vulnerables.
- No inventis estadístiques, dates ni fets no presents al text original."""

    # universal_rules eliminades — totes ja són al catàleg d'instruccions amb gradació MECR
    _cache["universal_rules"] = ""

    # ── Perfils (llegits dels M1) ──
    profile_files = {
        "nouvingut": "M1_alumnat-nouvingut.md",
        "tea": "M1_alumnat-TEA.md",
        "tdah": "M1_TDAH.md",
        "dislexia": "M1_dislexia-dificultats-lectores.md",
        "tdl": "M1_TDL-trastorn-llenguatge.md",
        "discapacitat_intellectual": "M1_discapacitat-intel·lectual.md",
        "discapacitat_visual": "M1_discapacitat-visual.md",
        "discapacitat_auditiva": "M1_discapacitat-auditiva.md",
        "altes_capacitats": "M1_altes-capacitats.md",
        "vulnerabilitat": "M1_vulnerabilitat-socioeducativa.md",
        "trastorn_emocional": "M1_trastorns-emocionals-conducta.md",
        "tdc": "M1_trastorn-coordinacio-dispraxia.md",
    }

    for key, filename in profile_files.items():
        content = _load_file(filename)
        if content:
            section = _extract_section(content, "## 6. INSTRUCCIONS D'ADAPTACIÓ TEXTUAL PER A L'LLM")
            if section:
                # Extreure el bloc de codi amb les instruccions compactes per al prompt
                blocks = _extract_code_blocks(section)
                if blocks:
                    _cache["profiles"][key] = blocks[0].strip()
                else:
                    # Fallback: usar tota la secció (sense taules ni markdown complex)
                    _cache["profiles"][key] = section[:500]

    # ── MECR (llegits del M3) ──
    m3 = _load_file("M3_lectura-facil-comunicacio-clara.md")
    if m3:
        mecr_section = _extract_section(m3, "## 6. INSTRUCCIONS PER NIVELL MECR — BLOCS PER A L'LLM")
        if not mecr_section:
            # Fallback: buscar a partir de "## 6."
            mecr_section = _extract_section(m3, "## 6.")
        if mecr_section:
            for level in ["pre-A1", "A1", "A2", "B1", "B2"]:
                blocks = re.findall(
                    rf"### {re.escape(level)}.*?\n```\n?(.*?)```",
                    mecr_section, re.DOTALL
                )
                if blocks:
                    _cache["mecr"][level] = blocks[0].strip()

        # Càrrega cognitiva
        cog_section = _extract_section(m3, "## 7. CÀRREGA COGNITIVA PER NIVELL MECR")
        if not cog_section:
            cog_section = _extract_section(m3, "## 7.")
        if cog_section:
            for label, key in [("baixos", "low"), ("mitjà", "mid"), ("alts", "high")]:
                blocks = re.findall(
                    rf"### .*?{label}.*?\n```\n?(.*?)```",
                    cog_section, re.DOTALL | re.IGNORECASE
                )
                if blocks:
                    _cache["cognitive_load"][key] = blocks[0].strip()

        # Resolució conflictes
        conflict_section = _extract_section(m3, "## 8. RESOLUCIÓ DE CONFLICTES DUA-MECR-LF")
        if not conflict_section:
            conflict_section = _extract_section(m3, "## 8.")
        if conflict_section:
            blocks = _extract_code_blocks(conflict_section)
            if blocks:
                _cache["conflict_resolution"] = blocks[0].strip()

        # Few-shot examples
        fewshot_section = _extract_section(m3, "## 9. EXEMPLES ABANS")
        if not fewshot_section:
            fewshot_section = _extract_section(m3, "## 9.")
        if fewshot_section:
            for level in ["pre-A1", "A1", "A2", "B1", "B2"]:
                pattern = rf"### Exemple {re.escape(level)}\n(.*?)(?=### Exemple|\Z)"
                m = re.search(pattern, fewshot_section, re.DOTALL)
                if m:
                    _cache["fewshot"][level] = m.group(1).strip()

    # ── DUA (llegits del M2) ──
    m2 = _load_file("M2_DUA-principis-pautes.md")
    if m2:
        dua_section = _extract_section(m2, "## 6. INSTRUCCIONS DUA PER NIVELL")
        if not dua_section:
            dua_section = _extract_section(m2, "## 6.")
        if dua_section:
            for label, key in [("Accés", "Acces"), ("Core", "Core"), ("Enriquiment", "Enriquiment")]:
                blocks = re.findall(
                    rf"### DUA {label}.*?\n```\n?(.*?)```",
                    dua_section, re.DOTALL
                )
                if blocks:
                    _cache["dua"][key] = blocks[0].strip()

    # ── Gèneres discursius (llegits del M3_generes) ──
    genres = _load_file("M3_generes-discursius.md")
    if genres:
        for genre in ["Explicació", "Narració", "Instrucció", "Argumentació"]:
            key = genre.lower()
            # Normalitzar clau
            key = key.replace("ó", "o").replace("ió", "io") if "ó" in key else key
            key = {"explicació": "explicacio", "narració": "narracio",
                   "instrucció": "instruccio", "argumentació": "argumentacio"}.get(genre.lower(), genre.lower())
            blocks = re.findall(
                rf"### \d+\. {re.escape(genre)}.*?```\n?(.*?)```",
                genres, re.DOTALL
            )
            if blocks:
                _cache["genres"][key] = blocks[0].strip()

    # ── Sub-gèneres (M3_generes-22.md, 22 blocs amb format "## <key>") ──
    # Complementa els 4 macro-gèneres amb els 22 sub-gèneres del dropdown del Pas 2.
    # Format: cada bloc comença amb "## <clau>" i continua fins al següent "## " o final.
    subgenres = _load_file("M3_generes-22.md")
    if subgenres:
        # Extreure només el cos del document (després del frontmatter i de la intro)
        # Cerca tots els blocs que comencin amb "## <clau>\n" i capturar fins al següent "## "
        matches = re.findall(r"^## ([a-z]+)\s*\n(.*?)(?=\n## |\Z)", subgenres, re.MULTILINE | re.DOTALL)
        for key, body in matches:
            _cache["genres"][key] = body.strip()

    # ── Aliases: tipologies → macro-gènere més proper ──
    # Permet usar directament el valor del dropdown "Tipologia" del Pas 2 si el
    # sub-gènere no està disponible.
    _typology_aliases = {
        "expositiva": "explicacio",
        "narrativa": "narracio",
        "argumentativa": "argumentacio",
        "instructiva": "instruccio",
        "descriptiva": "explicacio",  # descripció encaixa millor amb explicació
        "dialogada": "narracio",       # dialogat tractat com a variant narrativa
    }
    for alias, target in _typology_aliases.items():
        if alias not in _cache["genres"] and target in _cache["genres"]:
            _cache["genres"][alias] = _cache["genres"][target]

    # ── Creuaments (llegits del M1_creuament) ──
    crossings = _load_file("M1_creuament-variables-dependencies.md")
    if crossings:
        crossing_section = _extract_section(crossings, "## 6. INSTRUCCIONS DE CREUAMENT PER A L'LLM")
        if not crossing_section:
            crossing_section = _extract_section(crossings, "## 6.")
        if crossing_section:
            blocks = _extract_code_blocks(crossing_section)
            _cache["crossings"] = [b.strip() for b in blocks]


# ═══════════════════════════════════════════════════════════════════════════════
# API pública
# ═══════════════════════════════════════════════════════════════════════════════

def get_identity(lang: str = "ca") -> str:
    if not _cache:
        load_corpus()
    identity = _cache.get("identity", "")
    if lang != "ca":
        lang_label = get_lang_label(lang)
        identity = identity.replace(
            "LLENGUA: Català (o la llengua vehicular indicada).",
            f"LLENGUA: {lang_label.capitalize()}.",
        )
    return identity


def get_universal_rules() -> str:
    if not _cache:
        load_corpus()
    return _cache.get("universal_rules", "")


def get_dua_block(level: str) -> str:
    if not _cache:
        load_corpus()
    return _cache.get("dua", {}).get(level, "")


def get_genre_block(genre: str) -> str:
    if not _cache:
        load_corpus()
    return _cache.get("genres", {}).get(genre, "")


def _normalize(text: str) -> str:
    """Normalitza text per comparació: minúscules + sense accents."""
    import unicodedata
    text = text.lower()
    # Descompon caràcters accentuats i elimina els diacrítics
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def get_crossing_blocks(active_profiles: list[str]) -> list[str]:
    """Retorna els blocs de creuament aplicables a les combinacions actives."""
    if not _cache:
        load_corpus()
    if len(active_profiles) < 2:
        return []
    # Buscar creuaments que mencionen algun dels perfils actius
    result = []
    profiles_norm = [_normalize(p) for p in active_profiles]
    for block in _cache.get("crossings", []):
        block_norm = _normalize(block)
        # Un creuament s'aplica si menciona almenys 2 dels perfils actius
        matches = sum(1 for p in profiles_norm if p in block_norm)
        if matches >= 2:
            result.append(block)
        # Casos especials
        elif "nouvingut" in profiles_norm and "l2 molt baixa" in block_norm:
            result.append(block)
        elif "trauma" in block_norm and ("vulnerabilitat" in profiles_norm or "trastorn_emocional" in profiles_norm):
            result.append(block)
    return result


def get_cognitive_load_block(mecr: str) -> str:
    if not _cache:
        load_corpus()
    if mecr in ("pre-A1", "A1", "A2"):
        return _cache.get("cognitive_load", {}).get("low", "")
    elif mecr == "B1":
        return _cache.get("cognitive_load", {}).get("mid", "")
    return _cache.get("cognitive_load", {}).get("high", "")


def get_conflict_resolution() -> str:
    if not _cache:
        load_corpus()
    return _cache.get("conflict_resolution", "")


def get_fewshot_example(mecr: str) -> str:
    if not _cache:
        load_corpus()
    return _cache.get("fewshot", {}).get(mecr, "")


def get_all_loaded_stats() -> dict:
    """Retorna estadístiques de què s'ha carregat (per debug/test)."""
    if not _cache:
        load_corpus()
    return {
        "profiles": list(_cache.get("profiles", {}).keys()),
        "mecr": list(_cache.get("mecr", {}).keys()),
        "dua": list(_cache.get("dua", {}).keys()),
        "genres": list(_cache.get("genres", {}).keys()),
        "crossings": len(_cache.get("crossings", [])),
        "cognitive_load": list(_cache.get("cognitive_load", {}).keys()),
        "conflict_resolution": bool(_cache.get("conflict_resolution")),
        "fewshot": list(_cache.get("fewshot", {}).keys()),
    }
