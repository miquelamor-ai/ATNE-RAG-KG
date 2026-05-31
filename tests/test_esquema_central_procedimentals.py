"""
tests/test_esquema_central_procedimentals.py — Reproducció del cas titella.

Aïlla la 2a crida (complements) i comprova que, per a un text de gènere
procedimental (instructiu/receptari/manual), l'esquema visual posa el
PRODUCTE/OBJECTIU com a node central, NO el primer apartat (Materials/Necessites).

Cas real: feedback Miquel 2026-05-30 (PDF titella). L'esquema generat
posava 'Materials' com a arrel; el docent l'ha hagut de rectificar per
posar 'Titella' al centre.

Execució:
  python tests/test_esquema_central_procedimentals.py            # 1 rep
  python tests/test_esquema_central_procedimentals.py --repeat 3 # estabilitat
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

# Cas: 1r primària · dislèxia · A1 · receptari · esquema_visual activat.
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
    # Cas real del titella: 4 complements competint per l'atenció del model.
    "complements": {
        "esquema_visual": True,
        "bastides": True,
        "glossari": True,
        "pictogrames": True,
    },
}

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

PRODUCT_KEYWORD = "titella"  # producte final del receptari
WRONG_ROOTS = {"materials", "material", "necessites", "passos", "ingredients", "preparació", "instruccions"}


def extract_esquema_section(text: str) -> str | None:
    m = re.search(r"^## Esquema visual\b[^\n]*$", text, re.MULTILINE | re.IGNORECASE)
    if not m:
        return None
    nxt = re.search(r"^## ", text[m.end():], re.MULTILINE)
    end = m.end() + nxt.start() if nxt else len(text)
    return text[m.start():end]


def find_root_node(section: str) -> str | None:
    """Retorna la primera línia de bullet a indent 0 (la 'arrel' de l'esquema).

    Salta capçaleres ## i ###, línies buides i blocs ```. Si veu una línia
    `- ...` sense espais d'indentació (o `* ...`), és l'arrel.
    """
    in_code = False
    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        # Detecta bullet a INDENT 0 (no espais davant del guió)
        m = re.match(r"^[-*•]\s+(.+)$", line)
        if m:
            return m.group(1).strip()
    return None


def root_is_product(root: str | None) -> bool:
    if not root:
        return False
    r = root.lower()
    # Neteja format: treure **bold**, []()...
    r = re.sub(r"[\*_`\[\]\(\)]", "", r)
    r = re.sub(r"\s+", " ", r).strip()
    # Bona: conté la paraula clau del producte
    if PRODUCT_KEYWORD in r:
        return True
    # Dolenta: arrel = una de les seccions seqüencials (materials/passos…)
    for wrong in WRONG_ROOTS:
        if wrong in r:
            return False
    return False


def run_once() -> dict:
    system = build_complements_prompt(PROFILE, CONTEXT, PARAMS)
    user = f"TEXT ADAPTAT:\n{ADAPTED}\n\nGenera els complements pedagògics sol·licitats."
    model = server._model_for("complements")
    raw = _call_llm(model, system, user)
    clean = _post_process_llm_output(clean_gemini_output(raw), lang="ca")
    section = extract_esquema_section(clean)
    if section is None:
        return {"ok": False, "reason": "secció ## Esquema visual ABSENT", "model": model}
    root = find_root_node(section)
    ok = root_is_product(root)
    return {
        "ok": ok,
        "reason": "OK" if ok else f"arrel incorrecta: {root!r}",
        "root": root,
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
        print(f"{icon} {r['reason']}")

    print("\n" + "=" * 70)
    n_ok = sum(1 for r in results if r.get("ok"))
    print(f"RESULTAT: {n_ok}/{len(results)} runs amb arrel = producte")
    print("=" * 70)
    if results and results[-1].get("section"):
        last = results[-1]
        print(f"\n----- esquema generat (últim run, model={last.get('model')}) -----")
        print(last["section"][:1200])
    sys.exit(0 if n_ok == len(results) and len(results) > 0 else 1)


if __name__ == "__main__":
    main()
