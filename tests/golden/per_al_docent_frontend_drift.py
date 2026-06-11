"""tests/golden/per_al_docent_frontend_drift.py

Guard de DRIFT frontend ↔ canon per a la taxonomia «Per al docent» (9 categories A-I).

PER QUÈ
El backend (prompt_builder.py) ja CONSUMEIX la taxonomia del canon
`corpusFJE/.tooling/per_al_docent.json` (R0). Però el FRONTEND encara té els 9 noms de
categoria escrits literalment a dos llocs:
  · ui/atne/pas3.html  (dimMap que classifica/renderitza les cards «Per al docent»)
  · ui/saber-ne.html   («Categories d'adaptació» — el contracte didàctic per al docent)

Aquests són còpies que poden DERIVAR del canon silenciosament (ex: si mineriaRAG reanomena
una categoria). Aquest guard NO refactoritza el frontend (evita el risc de trencar el
render: el dimMap també porta regex + mòduls). Només COMPARA: cada nom canònic ha
d'aparèixer literalment als dos fitxers. Si no hi és → drift → el test falla i avisa.

Opció escollida «B-lite» (Miquel, 2026-06-11): 95% del benefici (zero drift silenciós)
amb ~0% del risc. La des-triplicació completa (consum via `.data.js`, com la matriu) queda
per quan toqui tocar el frontend per altres motius.

ÚS:
    python tests/golden/per_al_docent_frontend_drift.py
Exit code != 0 si hi ha drift (algun nom del canon falta a algun fitxer del frontend).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

CANON = ROOT / "corpus" / "external" / "corpusFJE" / ".tooling" / "per_al_docent.json"
FRONTEND_FILES = {
    "pas3.html (dimMap)": ROOT / "ui" / "atne" / "pas3.html",
    "saber-ne.html (Categories d'adaptació)": ROOT / "ui" / "saber-ne.html",
}


def main() -> int:
    if not CANON.exists():
        print(f"⚠️  Canon no trobat ({CANON}). Submodule no inicialitzat? — SKIP.")
        return 0
    names = list(json.loads(CANON.read_text(encoding="utf-8")).get("taxonomia_9cat", {}).values())
    if len(names) != 9:
        print(f"❌ El canon no té 9 categories ({len(names)}). Revisa per_al_docent.json.")
        return 1

    print(f"Canon: {len(names)} categories. Comprovant drift al frontend…\n")
    drift = False
    for label, path in FRONTEND_FILES.items():
        if not path.exists():
            print(f"⚠️  {label}: fitxer no trobat ({path}) — SKIP.")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        missing = [n for n in names if n not in text]
        if missing:
            drift = True
            print(f"❌ {label}: FALTEN {len(missing)} noms del canon: {missing}")
        else:
            print(f"✅ {label}: els 9 noms del canon hi són.")

    print()
    if drift:
        print("DRIFT DETECTAT: el frontend i el canon «Per al docent» han divergit.")
        print("→ Alinea el nom al frontend amb el canon (per_al_docent.json), o viceversa "
              "via mineriaRAG si el canvi és pedagògic.")
        return 1
    print("OK — frontend «Per al docent» alineat amb el canon (sense drift).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
