"""
tests/test_glossari_filtre_quotidia.py — Reproducció del cas titella.

Aïlla la 2a crida (complements) i comprova que, per a un perfil dislèxia A1
amb un text receptari quotidià (titella), la SKILL generate-glossari NO emet
paraules quotidianes (mitja, botons, agulla, fil…) com a termes del glossari
i que NINGUNA definició conté castellanismes (Muñeco, calcetín…).

Origen del cas: feedback Miquel 2026-05-30 (PDF titella). El SKILL té la regla
"cap paraula quotidiana òbvia" (línia 88 del SKILL.md) i "Llengua de definició:
Català" (línia 87), però estan dins la rúbrica de 17K. El model les ignora.

Execució:
  python tests/test_glossari_filtre_quotidia.py            # 1 rep
  python tests/test_glossari_filtre_quotidia.py --repeat 3 # estabilitat
"""
from __future__ import annotations

import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
except ImportError:
    pass

import server
from adaptation.prompt_builder import build_complements_prompt
from adaptation.llm_clients import _call_llm
from adaptation.post_process import clean_gemini_output, _post_process_llm_output

# Cas: 1r primària · dislèxia · A1 · receptari · glossari + pictogrames activats.
PROFILE = {
    "caracteristiques": {
        "dislexia": {"actiu": True, "grau": "moderat"},
    },
}
CONTEXT = {"etapa": "Primària", "materia": "manualitats"}
PARAMS = {
    "mecr_sortida": "A1",
    "dua": "Core",
    "genere_discursiu": "receptari",
    "complements": {
        "glossari": True,
        "pictogrames": True,
        "bastides": True,
    },
}

# Text adaptat del titella (reproducció del cas real del docent)
ADAPTED = """# Com fer un titella de mitja

Necessites:
- Una mitja vella
- Dos botons
- Una agulla i fil
- Una mica de farciment

Passos:
1. Posa el farciment dins de la mitja.
2. Lliga el cap amb un fil.
3. Cus dos botons per fer els ulls.
4. Dibuixa la boca amb un retolador.

Ja tens el teu titella.
Pots fer-li veu i jugar amb ell.
"""

# Paraules QUOTIDIANES a 1r primària que NO han de sortir com a termes del glossari.
QUOTIDIANES = {"mitja", "botó", "botons", "agulla", "fil", "retolador", "vella", "ulls", "boca", "cap", "veu"}

# Castellanismes que MAI han d'aparèixer com a definició (cas observat: "Muñeco").
CASTELLANISMES = {"muñeco", "muñeca", "calcetín", "calcetin", "calcetines",
                  "agujas", "aguja", "hilo", "boton", "botones",
                  "rotulador", "trapo", "juguete", "jugar con él"}


def extract_glossari_section(text: str) -> str | None:
    m = re.search(r"^## Glossari\b[^\n]*$", text, re.MULTILINE | re.IGNORECASE)
    if not m:
        return None
    nxt = re.search(r"^## ", text[m.end():], re.MULTILINE)
    end = m.end() + nxt.start() if nxt else len(text)
    return text[m.start():end]


def extract_glossary_terms(section: str) -> list[str]:
    """Extreu termes de la 1a columna d'una taula markdown del glossari."""
    terms = []
    for line in section.splitlines():
        line = line.strip()
        if not line.startswith("|") or "|" not in line[1:]:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        t = cells[0].strip()
        # Excloem capçalera ("Terme") i separadors ("---")
        if re.match(r"^[-:\s]+$", t) or t.lower() in ("terme", "term"):
            continue
        # Treure asteriscs/format
        t = re.sub(r"[*_`]", "", t).strip().lower()
        if t:
            terms.append(t)
    return terms


def detect_castellanismes(section: str) -> list[str]:
    sl = section.lower()
    found = []
    for cw in CASTELLANISMES:
        # Cerca per paraula sencera (evita false positives amb substring "boton" en
        # "botons" català → "botons" no és un castellanisme; "boton" sense 's' sí).
        if re.search(rf"\b{re.escape(cw)}\b", sl):
            found.append(cw)
    return found


def run_once() -> dict:
    system = build_complements_prompt(PROFILE, CONTEXT, PARAMS)
    user = f"TEXT ADAPTAT:\n{ADAPTED}\n\nGenera els complements pedagògics sol·licitats."
    model = server._model_for("complements")
    raw = _call_llm(model, system, user)
    clean = _post_process_llm_output(clean_gemini_output(raw), lang="ca")
    section = extract_glossari_section(clean)
    if section is None:
        return {"ok": False, "reason": "secció ## Glossari ABSENT", "model": model}
    terms = extract_glossary_terms(section)
    quotidianes_trobades = sorted(t for t in terms if t in QUOTIDIANES)
    castellanismes = detect_castellanismes(section)
    n_terms = len(terms)
    # Èxit: cap mot quotidià + cap castellanisme + (si hi ha terms) ≤ 3 termes (real tècnics).
    ok = (not quotidianes_trobades) and (not castellanismes)
    reasons = []
    if quotidianes_trobades:
        reasons.append(f"quotidianes trobades: {quotidianes_trobades}")
    if castellanismes:
        reasons.append(f"castellanismes: {castellanismes}")
    return {
        "ok": ok,
        "reason": "OK" if ok else "; ".join(reasons),
        "n_terms": n_terms,
        "terms": terms,
        "quotidianes": quotidianes_trobades,
        "castellanismes": castellanismes,
        "section": section,
        "model": model,
    }


def main():
    argv = sys.argv[1:]
    repeat = 1
    if "--repeat" in argv:
        i = argv.index("--repeat")
        repeat = int(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    results = []
    for k in range(repeat):
        tag = f"rep {k+1}/{repeat}" if repeat > 1 else "1 rep"
        print(f"[run] {tag} … ", end="", flush=True)
        try:
            r = run_once()
        except Exception as e:
            r = {"ok": False, "reason": f"EXCEPCIÓ: {type(e).__name__}: {e}"}
        results.append(r)
        icon = "✅" if r.get("ok") else "❌"
        extra = ""
        if r.get("terms") is not None:
            extra = f"  termes={r.get('n_terms')} ({', '.join(r.get('terms', [])[:5])}...)"
        print(f"{icon} {r['reason']}{extra}")

    print("\n" + "=" * 70)
    n_ok = sum(1 for r in results if r.get("ok"))
    print(f"RESULTAT: {n_ok}/{len(results)} runs amb glossari ben filtrat")
    print("=" * 70)
    if results:
        last = results[-1]
        if last.get("section"):
            print(f"\n----- secció generada (últim run, model={last.get('model')}) -----")
            print(last["section"][:1200])
    sys.exit(0 if n_ok == len(results) and len(results) > 0 else 1)


if __name__ == "__main__":
    main()
