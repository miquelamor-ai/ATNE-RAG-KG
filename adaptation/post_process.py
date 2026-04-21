"""Post-processat determinista de la sortida dels LLMs.

Extret de `server.py` (refactor/server-split, 2026-04-21). Aquestes
funcions són pures: prenen text, retornen text (o un dict de mètriques),
sense efectes laterals ni dependències del mòdul `server`.

El pipeline complet s'aplica abans d'enviar la sortida al frontend:

    text = _post_process_llm_output(text)          # LaTeX, typos, anglès
    text = clean_gemini_output(text)               # headings, meta-comentaris
    report = post_process_adaptation(text, mecr)   # warnings + mètriques
"""

import re


MECR_MAX_WORDS = {"pre-A1": 5, "A1": 8, "A2": 12, "B1": 18, "B2": 25}
FORBIDDEN_WORDS = ["cosa", "coses", "allò", "el que fa que", "serveix per", "un tipus de"]


def post_process_adaptation(text: str, mecr: str) -> dict:
    """Verificació post-LLM amb Python. Retorna warnings i mètriques."""
    warnings = []
    max_words = MECR_MAX_WORDS.get(mecr, 25)

    # 1. Longitud de frases
    sentences = re.split(r'[.!?]\s', text)
    long_sentences = []
    for s in sentences:
        s = s.strip()
        if not s or s.startswith("#") or s.startswith("|") or s.startswith("-"):
            continue
        wcount = len(s.split())
        if wcount > max_words + 3:  # marge de 3 paraules
            long_sentences.append((s[:60] + "...", wcount))
    if long_sentences:
        warnings.append(
            f"⚠ {len(long_sentences)} frases superen {max_words} paraules (MECR {mecr})")

    # 2. Paraules prohibides
    text_lower = text.lower()
    found_forbidden = [w for w in FORBIDDEN_WORDS if w in text_lower]
    if found_forbidden:
        warnings.append(f"⚠ Paraules prohibides detectades: {', '.join(found_forbidden)}")

    # 3. Mètriques bàsiques
    words = len(text.split())
    bold_terms = len(re.findall(r'\*\*[^*]+\*\*', text))
    headings = len(re.findall(r'^##+ ', text, re.MULTILINE))

    return {
        "warnings": warnings,
        "metrics": {
            "paraules": words,
            "frases": len(sentences),
            "termes_negreta": bold_terms,
            "encapcalaments": headings,
            "frases_llargues": len(long_sentences),
        },
    }


# ── Adaptació (funció bloquejant per executar en thread pool) ──────────────

def clean_gemini_output(text: str) -> str:
    """Neteja la sortida de Gemini: elimina 'thinking' filtrat i normalitza headings."""
    # 1. Treure qualsevol text abans del primer ## (thinking filtrat)
    match = re.search(r'^## ', text, re.MULTILINE)
    if match and match.start() > 0:
        text = text[match.start():]

    # 2. Arreglar ## que queden enganxats a text anterior (sense salt de línia)
    text = re.sub(r'(?<!\n)(## )', r'\n\1', text)

    # 2b. Normalitzar headings sense espai després del ## / ### / ####
    #     («##Preguntes» → «## Preguntes», «###Abans» → «### Abans»).
    #     Cal perquè parseAdaptedSections exigeix «^## » amb espai; sense aquesta
    #     normalització la secció es queda enganxada a la precedent.
    text = re.sub(r'^(#{2,4})([^\s#])', r'\1 \2', text, flags=re.MULTILINE)
    # 2c. Netejar cometes que algun LLM posa al voltant del títol
    #     («## 'Preguntes de comprensió'», «## "Preguntes…"»): només al títol.
    text = re.sub(r'^(#{2,4} )["\'`«»“”‘’]+', r'\1', text, flags=re.MULTILINE)
    text = re.sub(r'^(#{2,4} .*?)["\'`«»“”‘’]+\s*$', r'\1', text, flags=re.MULTILINE)

    # 3. Treure línies de meta-comentari típiques de Gemini
    lines_to_remove = [
        r"^Final draft.*$",
        r"^I'll proceed.*$",
        r"^Here is the.*$",
        r"^Let me.*$",
        r"^Okay,.*output.*$",
    ]
    for pattern in lines_to_remove:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE | re.MULTILINE)

    # 4. Convertir sub-headings duplicats ## dins de seccions a ###
    #    Gemini a vegades escriu "## Nivell 1:" dins de "## Preguntes"
    #    Lògica: el primer ## de cada secció principal es manté,
    #    els ## dins d'una secció es converteixen a ###
    lines = text.split("\n")
    in_section = False
    fixed_lines = []
    for line in lines:
        if line.startswith("## "):
            title_lower = line[3:].strip().lower()
            # És una secció principal si el títol és un dels principals
            is_main = any(kw in title_lower for kw in [
                "text adaptat", "glossari", "esquema", "mapa conceptual",
                "preguntes", "bastides", "activitats", "mapa mental",
                "argumentació", "argumentacio", "notes d'auditoria",
                "notes d'audit", "pictogrames", "traducció", "negretes",
                "definicions",
            ])
            if is_main:
                in_section = True
                fixed_lines.append(line)
            else:
                # Sub-heading dins d'una secció → convertir a ###
                fixed_lines.append("###" + line[2:])
        else:
            fixed_lines.append(line)
    text = "\n".join(fixed_lines)

    # 5. Treure línies que són només "#" (artefacte de Gemini)
    text = re.sub(r'^#\s*$', '', text, flags=re.MULTILINE)

    # 5b. Normalitza variants dels títols de les tres sub-seccions de preguntes
    #     («Abans de la lectura», «Previ a la lectura»…) als canònics.
    text = re.sub(r'^###\s+(pr[eè]via\s+a\s+la\s+lectura|lectura\s+pr[eè]via)\s*$',
                  '### Abans de llegir', text, flags=re.MULTILINE | re.IGNORECASE)
    text = re.sub(r'^###\s+abans\s+de\s+la\s+lectura\s*$',
                  '### Abans de llegir', text, flags=re.MULTILINE | re.IGNORECASE)
    text = re.sub(r'^###\s+durant\s+la\s+lectura\s*$',
                  '### Durant la lectura', text, flags=re.MULTILINE | re.IGNORECASE)
    text = re.sub(r'^###\s+despr[eé]s\s+de\s+(la\s+)?llegir\s*$',
                  '### Després de llegir', text, flags=re.MULTILINE | re.IGNORECASE)
    text = re.sub(r'^###\s+despr[eé]s\s+de\s+la\s+lectura\s*$',
                  '### Després de llegir', text, flags=re.MULTILINE | re.IGNORECASE)

    # 5c. Xarxa de seguretat: si apareix un encapçalament «### Abans de llegir»
    #     (o variants ja normalitzades a dalt) orfe — sense «## Preguntes de
    #     comprensió» al davant — inserta el wrapper. Alguns LLMs ometen el «##»
    #     pare quan el prompt els mostra el template de sub-seccions amb «###».
    m_abans = re.search(r'^###\s+Abans de llegir\b', text, flags=re.MULTILINE | re.IGNORECASE)
    if m_abans:
        preceding = text[: m_abans.start()]
        last_h2 = list(re.finditer(r'^##\s+(.+)$', preceding, flags=re.MULTILINE))
        last_title = last_h2[-1].group(1).lower() if last_h2 else ""
        if "pregunt" not in last_title and "comprensi" not in last_title:
            text = text[: m_abans.start()] + "## Preguntes de comprensió\n\n" + text[m_abans.start():]

    # 6. Netejar línies buides excessives
    text = re.sub(r'\n{4,}', '\n\n\n', text)

    return text.strip()


# ── Post-processador d'artefactes LaTeX ─────────────────────────────────────
# Alguns LLMs (Gemma 4, GPT-4o-mini i d'altres) injecten espontàniament
# marques LaTeX quan veuen patrons estructurats com "omplir buits", "fletxes"
# o "esquemes". Els prompts del catàleg usen fletxes Unicode pures (→, ↔)
# i guions baixos normals, però els models les reprodueixen en sintaxi LaTeX.
# Aquest post-processador es determinista, sense LLM, i normalitza la sortida
# abans del Quality Report i abans de l'enviament al frontend.

_LATEX_PATTERNS = [
    # Fletxes (més específic primer)
    (r'\$\s*\\xrightarrow\{[^}]*\}\s*\$', '→'),
    (r'\$\s*\\xleftarrow\{[^}]*\}\s*\$', '←'),
    (r'\$\s*\\rightarrow\s*\$', '→'),
    (r'\$\s*\\leftarrow\s*\$', '←'),
    (r'\$\s*\\uparrow\s*\$', '↑'),
    (r'\$\s*\\downarrow\s*\$', '↓'),
    (r'\$\s*\\leftrightarrow\s*\$', '↔'),
    (r'\$\s*\\Rightarrow\s*\$', '⇒'),
    (r'\$\s*\\Leftarrow\s*\$', '⇐'),
    # \text{...} i altres comandos amb arguments — típicament són buits
    # d'omplir ("$\text{\\\\\\\\}$"). Els convertim a ___ (placeholder).
    (r'\$\\text\{[^}]*\}\$', '___'),
    (r'\\text\{[^}]*\}', '___'),
    (r'\$\\textbf\{[^}]*\}\$', '___'),
    (r'\\textbf\{[^}]*\}', '___'),
    (r'\$\\underline\{[^}]*\}\$', '___'),
    (r'\\underline\{[^}]*\}', '___'),
    # Fletxes orfes sense dollars
    (r'\\rightarrow\b', '→'),
    (r'\\leftarrow\b', '←'),
    (r'\\uparrow\b', '↑'),
    (r'\\downarrow\b', '↓'),
    (r'\\leftrightarrow\b', '↔'),
    (r'\\Rightarrow\b', '⇒'),
    (r'\\Leftarrow\b', '⇐'),
]


def _strip_latex_artifacts(text: str) -> str:
    """Neteja artefactes LaTeX que alguns LLMs injecten als complements.

    Normalitza:
    - `$\\rightarrow$`, `$\\xrightarrow{...}$`, etc. → fletxes Unicode
    - `$\\text{...}$`, `\\textbf{...}` → `___` (placeholder omplir buit)
    - Seqüències de 2+ backslashes seguides de `_` → `___`
    - Seqüències de 4+ backslashes soles → `___`
    - LaTeX malformat tipus `$(ightarrow$` (backslash → parèntesi)

    No toca `$` aïllats (preus en euros) ni fletxes Unicode ja correctes.
    """
    if not text:
        return text
    for pattern, replacement in _LATEX_PATTERNS:
        text = re.sub(pattern, replacement, text)
    # Fill-in-the-blank: \\\\\\\\_ → ___
    text = re.sub(r'\\{2,}_', '___', text)
    # Fill-in-the-blank sense underscore: \\\\\\\\ → ___
    text = re.sub(r'\\{4,}', '___', text)
    # LaTeX malformat amb arrow: $(ightarrow$, $\ri(tarrow$, etc.
    # Qualsevol $...rightarrow...$ o $...leftarrow...$ → fletxa Unicode
    text = re.sub(r'\$[^$\n]{0,15}(?:right|rightar|ight)arrow[^$\n]{0,5}\$', '→', text)
    text = re.sub(r'\$[^$\n]{0,15}(?:left|leftar|eft)arrow[^$\n]{0,5}\$', '←', text)
    return text


# ── Substitucions de paraules anglès → català ──────────────────────────────
# Els LLMs a vegades injecten paraules angleses quan els termes catalans són
# baixos en freqüència. Mapping conservador per a termes clarament històrics
# que NO es farien servir en text educatiu català en lliçó normal.
_ENGLISH_REPLACEMENTS = {
    'owners': 'propietaris',
    'owner': 'propietari',
    'workers': 'treballadors',
    'worker': 'treballador',
    'factory': 'fàbrica',
    'factories': 'fàbriques',
    'inventions': 'invencions',
    'invention': 'invenció',
    'employees': 'empleats',
    'employee': 'empleat',
}


def _fix_english_words(text: str) -> str:
    """Substitueix paraules angleses injectades pel LLM per l'equivalent català.
    Preserva majúscules inicials. Cas-sensible en el sentit que 'Owners' → 'Propietaris'.
    """
    if not text:
        return text
    for en, cat in _ENGLISH_REPLACEMENTS.items():
        text = re.sub(r'\b' + re.escape(en) + r'\b', cat, text)
        text = re.sub(r'\b' + re.escape(en.capitalize()) + r'\b', cat.capitalize(), text)
        text = re.sub(r'\b' + re.escape(en.upper()) + r'\b', cat.upper(), text)
    return text


# ── Typos coneguts del LLM ─────────────────────────────────────────────────
# Catàleg conservador: només errors que hem observat empíricament a les
# proves del 14-15/04 i que tenen una correcció inequívoca.
_TYPO_FIXES = {
    'possuïen': 'posseïen',
    'possuïa': 'posseïa',
    'possuïr': 'posseir',
    'possuïm': 'posseïm',
    'possuïs': 'posseïs',
    'luitar': 'lluitar',
    'luitava': 'lluitava',
    'luitaven': 'lluitaven',
    'luita': 'lluita',
    'produïguessin': 'produïssin',
    'produïguessi': 'produïssi',
    'collhita': 'collita',
    'feudum': 'feu',
    'sobrecarga': 'sobrecàrrega',
    'localizar': 'localitzar',
    'localizada': 'localitzada',
}


def _fix_typos(text: str) -> str:
    """Corregeix typos del LLM a partir d'un catàleg conservador observat empíricament."""
    if not text:
        return text
    for bad, good in _TYPO_FIXES.items():
        text = re.sub(r'\b' + re.escape(bad) + r'\b', good, text)
        text = re.sub(r'\b' + re.escape(bad.capitalize()) + r'\b', good.capitalize(), text)
    return text


# ── Concatenacions repetides (Revolrevolució, sociasocials, ...) ───────────
# Patro observat: el LLM de vegades comença a escriure una paraula, es talla
# a mig, i reinicia la mateixa paraula sencera — produint "Revol"+"revolució"
# = "Revolrevolució". Detecció algorísmica: si una paraula de 8-25 caràcters
# conté una repetició de prefix (les N primeres lletres tornen a aparèixer
# a partir de la posició N), col·lapsem a la segona meitat.

_CONCAT_WORD_RE = re.compile(r'\b[A-Za-zÀ-ÿ]{8,25}\b')


def _fix_word_concatenations(text: str) -> str:
    """Elimina repeticions de prefix dins d'una mateixa paraula.

    Exemples que col·lapsa:
    - 'Revolrevolució' → 'revolució' (i=5, head='Revol', tail comença amb 'revol')
    - 'Revolucirevolució' → 'revolució' (i=8, head='Revoluci')
    - 'sociasocials' → 'socials' (i=5, head='socia')

    Ignora paraules <8 caràcters o >25 (no afecta vocabulari normal).
    """
    if not text:
        return text

    def repl(m):
        word = m.group(0)
        # Provem cada punt de tall entre 3 i len-3
        for i in range(3, len(word) - 2):
            head = word[:i].lower()
            tail = word[i:].lower()
            if tail.startswith(head):
                return word[i:]
        return word

    return _CONCAT_WORD_RE.sub(repl, text)


def _post_process_llm_output(text: str) -> str:
    """Pipeline complet de neteja post-LLM abans del Quality Report.

    Aplica en ordre:
    1. Strip artefactes LaTeX
    2. Fix concatenacions de prefix (Revolrevolució → revolució)
    3. Substitució de paraules angleses (owners → propietaris)
    4. Correcció de typos coneguts (possuïen → posseïen)

    Ordre crític: el LaTeX primer (pot contenir fragments que trenquin els
    altres regex), concatenacions abans que typos (una concatenació pot
    contenir un typo com a substring).
    """
    text = _strip_latex_artifacts(text)
    text = _fix_word_concatenations(text)
    text = _fix_english_words(text)
    text = _fix_typos(text)
    return text
