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


SYSTEM_MINIM = (
    "Ets un redactor de materials escolars en catal\u00e0. Escrius textos clars, "
    "ben estructurats, adequats a l'edat i al curs indicats. Respectes "
    "exactament el g\u00e8nere discursiu, la tipologia textual, el to i la "
    "llargada demanats. Catal\u00e0 normatiu. Uses negretes per als termes clau "
    "i, si el tema ho permet, acabes amb una breu caixa \"Vocabulari clau\" "
    "de 3-5 termes. No inventes dades: si dubtes d'un fet concret, evita-ho "
    "o formula-ho de manera general. Escriu directament el text, sense "
    "introduccions meta ni disclaimers."
)


# Mapping d'extensi\u00f3 qualitativa a rang num\u00e8ric.
# Sincronitzat amb els valors que el Pas 2 pot enviar al payload.
# Valors aproximats; el model tendeix a respectar-los amb ±15%.
EXTENSIONS = {
    "curt":      (250, "curt"),
    "breu":      (250, "curt"),
    "estandard": (400, "d'extensi\u00f3 est\u00e0ndard"),
    "estandar":  (400, "d'extensi\u00f3 est\u00e0ndard"),
    "mitja":     (400, "d'extensi\u00f3 est\u00e0ndard"),
    "extens":    (700, "extens"),
    "llarg":     (700, "extens"),
}


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
    tipologia = (params.get("tipologia") or "expositiva").strip().lower()
    to = (params.get("to") or "neutre").strip().lower()
    extensio_raw = params.get("extensio") or "estandard"
    n_paraules, etiqueta_llarg = resolve_extension(extensio_raw)
    notes = (params.get("notes") or "").strip()
    saber = (params.get("saber_curricular") or "").strip()

    ctx = params.get("context") or {}
    curs = (ctx.get("curs") or "").strip()
    etapa = (ctx.get("etapa") or "").strip()
    materia = (ctx.get("materia") or "").strip()
    ambit = (ctx.get("ambit") or "").strip()

    # Frase narrativa principal — atributs del TEXT
    frase = (
        f"Escriu un text del g\u00e8nere \u00ab{genere}\u00bb, tipologia {tipologia}, "
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
    return SYSTEM_MINIM, build_user(params)
