"""Construcci\u00f3 del prompt m\u00ednim per a generaci\u00f3 de textos educatius.

Format h\u00edbrid validat emp\u00edricament a la Fase 0.5 i 0.7:
- SYSTEM fix (~90 paraules) que defineix el rol de redactor de materials escolars.
- USER farcit amb els par\u00e0metres: frase narrativa principal (atributs del
  text) + bloc de destinatari (atributs de l'audi\u00e8ncia) + notes opcionals.

Total context d'entrada: ~110 paraules (vs 800+ del pipeline antic de
`/api/generate-text`). El model (Gemma 4 31B / Gemma 3 12B / Qwen 3.5 27B /
GPT-4o...) rep l'enc\u00e0rrec en format natural, similar al d'Arena/AI Studio.

Zero imports del pipeline d'adaptaci\u00f3.
"""


SYSTEM_PER_LLENGUA: dict[str, str] = {
    "ca": (
        "Ets un redactor de materials escolars en catal\u00e0. Escrius textos clars, "
        "ben estructurats, adequats a l'edat i al curs indicats. Respectes "
        "exactament el g\u00e8nere discursiu, el to i la llargada demanats. Catal\u00e0 "
        "normatiu. Uses negretes per als termes clau i, si el tema ho permet, "
        "acabes amb una breu caixa \"Vocabulari clau\" de 3-5 termes. No inventes "
        "dades: si dubtes d'un fet concret, evita-ho o formula-ho de manera "
        "general. Escriu directament el text, sense introduccions meta ni disclaimers."
    ),
    "es": (
        "Eres un redactor de materiales escolares en castellano. Escribes textos "
        "claros, bien estructurados, adecuados a la edad y al curso indicados. "
        "Respetas exactamente el g\u00e9nero discursivo, el tono y la extensi\u00f3n pedidos. "
        "Castellano normativo. Usas negritas para los t\u00e9rminos clave y, si el tema "
        "lo permite, terminas con un breve recuadro \"Vocabulario clave\" de 3-5 "
        "t\u00e9rminos. No inventes datos. Escribe directamente el texto, sin "
        "introducciones meta ni disclaimers."
    ),
    "en": (
        "You are an educational materials writer. You write clear, well-structured "
        "texts appropriate for the age and year group indicated. You follow exactly "
        "the requested genre, tone and length. Standard English. Use bold for key "
        "terms and, if the topic allows, end with a brief 'Key vocabulary' box of "
        "3-5 terms. Do not invent facts. Write the text directly, without meta "
        "introductions or disclaimers."
    ),
    "fr": (
        "Tu es un r\u00e9dacteur de mat\u00e9riaux scolaires en fran\u00e7ais. Tu \u00e9cris des textes "
        "clairs, bien structur\u00e9s, adapt\u00e9s \u00e0 l'\u00e2ge et au niveau indiqu\u00e9s. Tu respectes "
        "exactement le genre discursif, le ton et la longueur demand\u00e9s. Fran\u00e7ais "
        "normatif. Tu utilises le gras pour les termes cl\u00e9s et, si le sujet le "
        "permet, tu termines avec un bref encadr\u00e9 \u00abVocabulaire cl\u00e9\u00bb de 3-5 termes. "
        "N'invente pas de donn\u00e9es. \u00c9cris directement le texte, sans introductions "
        "m\u00e9ta ni avertissements."
    ),
    "de": (
        "Du bist ein Autor von Schulmaterialien auf Deutsch. Du schreibst klare, "
        "gut strukturierte Texte, die dem angegebenen Alter und der Klassenstufe "
        "angemessen sind. Du h\u00e4ltst dich genau an die gew\u00fcnschte Textsorte, den Ton "
        "und die L\u00e4nge. Normales Deutsch. Verwende Fettdruck f\u00fcr Schl\u00fcsselbegriffe "
        "und beende den Text, wenn das Thema es erlaubt, mit einem kurzen Kasten "
        "\u00abSchl\u00fcsselvokabular\u00bb mit 3-5 Begriffen. Erfinde keine Fakten. Schreib den "
        "Text direkt, ohne Meta-Einleitungen oder Disclaimer."
    ),
}
# Retrocompat: SYSTEM_MINIM apunta al catal\u00e0 per defecte
SYSTEM_MINIM = SYSTEM_PER_LLENGUA["ca"]


# Mapping d'extensi\u00f3 qualitativa a rang num\u00e8ric.
# Sincronitzat amb els valors que el Pas 2 pot enviar al payload.
# Valors aproximats; el model tendeix a respectar-los amb ±15%.
EXTENSIONS = {
    "micro":     (75,  "molt curt (50-100 paraules)"),
    "curt":      (200, "curt"),
    "breu":      (200, "curt"),
    "estandard": (400, "d'extensi\u00f3 est\u00e0ndard"),
    "estandar":  (400, "d'extensi\u00f3 est\u00e0ndard"),
    "mitja":     (400, "d'extensi\u00f3 est\u00e0ndard"),
    "extens":    (700, "extens"),
    "llarg":     (700, "extens"),
}

# Per a infantil (pre-A1), frases de 3-6 paraules per a lectura compartida.
INFANTIL_MAX_PARAULES = 40


def resolve_lang(lang_raw: str | None) -> str:
    """Normalitza el codi de llengua al codi intern ('ca', 'es', 'en', 'fr', 'de').

    Qualsevol codi desconegut retorna 'ca'.
    """
    if not lang_raw:
        return "ca"
    code = lang_raw.strip().lower()
    return code if code in SYSTEM_PER_LLENGUA else "ca"


def resolve_extension(extensio_raw: str | None) -> tuple[int, str]:
    """Tradueix l'etiqueta d'extensi\u00f3 del Pas 2 a (n_paraules, etiqueta_llegible).

    Si l'etiqueta no es reconeix, cau a 'estandard' (400 paraules).
    """
    if not extensio_raw:
        return EXTENSIONS["estandard"]
    key = extensio_raw.strip().lower()
    return EXTENSIONS.get(key, EXTENSIONS["estandard"])


def build_user(params: dict) -> str:
    """Construeix el missatge d'usuari a partir dels par\u00e0metres del Pas 2.

    Par\u00e0metres esperats (tots opcionals excepte `tema`):
        tema: str (obligatori) — de qu\u00e8 va el text
        genere: str — g\u00e8nere discursiu (p.ex. "article divulgatiu")
        tipologia: str — tipologia textual (expositiva|narrativa|...)
        to: str — to discursiu (neutre|proper|formal|...)
        extensio: str — etiqueta qualitativa (curt|estandard|extens)
        context: dict amb curs, etapa, ambit, materia (del Pas 1)
        notes: str — indicacions addicionals del docent (opcional)
        saber_curricular: str — saber curricular a vincular (Sprint C, opcional)
    """
    tema = (params.get("tema") or "").strip()
    if not tema:
        raise ValueError("Cal un 'tema' per generar el text.")

    genere = (params.get("genere") or "article divulgatiu").strip()
    to = (params.get("to") or "neutre").strip().lower()
    notes = (params.get("notes") or "").strip()
    saber = (params.get("saber_curricular") or "").strip()
    override_cap = bool(params.get("override_cap", False))

    ctx = params.get("context") or {}
    curs = (ctx.get("curs") or "").strip()
    etapa = (ctx.get("etapa") or "").strip()
    materia = (ctx.get("materia") or "").strip()
    ambit = (ctx.get("ambit") or "").strip()

    extensio_raw = params.get("extensio") or "estandard"
    n_paraules, etiqueta_llarg = resolve_extension(extensio_raw)
    # Cap per a infantil: independentment de l'extensió triada, els textos
    # per a I3-I5 han de ser molt curts (lectura compartida adult/infant).
    # Cap pedagògic per a infantil (MALL G-09, lectura compartida).
    # Soft: si override_cap=True el docent ha decidit conscientment sobrepassar-lo.
    if etapa.lower() == "infantil" and n_paraules > INFANTIL_MAX_PARAULES and not override_cap:
        n_paraules = INFANTIL_MAX_PARAULES
        etiqueta_llarg = f"molt curt ({INFANTIL_MAX_PARAULES} paraules màxim, frases de 3-6 paraules)"

    # Frase narrativa principal — atributs del TEXT
    frase = (
        f"Escriu un text del g\u00e8nere \u00ab{genere}\u00bb, "
        f"de to {to}, d'aproximadament {n_paraules} paraules ({etiqueta_llarg}), "
        f"sobre: {tema}."
    )

    # Bloc de destinatari — atributs de l'AUDI\u00c8NCIA
    dest_parts = []
    if curs and etapa:
        dest_parts.append(f"{curs} de {etapa}")
    elif curs:
        dest_parts.append(curs)
    elif etapa:
        dest_parts.append(etapa)
    if materia:
        dest_parts.append(f"mat\u00e8ria de {materia}")
    if ambit:
        dest_parts.append(f"\u00e0mbit {ambit}")
    if dest_parts:
        destinatari = "Destinatari: alumnat de " + ", ".join(dest_parts) + "."
    else:
        destinatari = "Destinatari: alumnat escolar (curs no especificat)."

    # Notes opcionals
    blocs_opcionals = []
    if notes:
        blocs_opcionals.append(f"Indicacions del docent: {notes}")
    if saber:
        blocs_opcionals.append(
            f"Saber curricular a cobrir: {saber}. "
            f"Assegura't d'introduir aquest concepte al text de manera natural."
        )

    parts = [frase, "", destinatari]
    if blocs_opcionals:
        parts.append("")
        parts.extend(blocs_opcionals)

    return "\n".join(parts)


def build_prompt(params: dict) -> tuple[str, str]:
    """Retorna (system, user) preparats per passar a `_call_llm_raw`."""
    lang = resolve_lang(params.get("lang") or params.get("llengua"))
    system = SYSTEM_PER_LLENGUA.get(lang, SYSTEM_PER_LLENGUA["ca"])
    return system, build_user(params)
