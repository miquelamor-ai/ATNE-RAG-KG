"""
tests/audit_prompt_size.py — Audit Q5-B: mida del prompt amb/sense slicing per-nivell

Per a 3 casos representatius, mesura:
  - Mida del prompt actual (SKILL.md complet de cada complement actiu).
  - Mida hipotètica amb slicing connectat (preàmbul + llesca del nivell MECR).
  - Reducció en KB i en %.

Sense LLM, instantani. Confirma o refuta l'argument que "el prompt era massa gran".

Execució:
  python tests/audit_prompt_size.py
"""
from __future__ import annotations

import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "corpus" / "external" / "corpusFJE" / "skills"
PREAMBLE_SPLIT = "## Modulació per nivell"

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


CASOS = [
    {
        "id": "titella",
        "desc": "1r primària · dislèxia · A1 · receptari",
        "mecr": "A1",
        "skills": [
            "write-receptari", "generate-glossari", "generate-bastides-lectura",
            "generate-pictogrames",
        ],
    },
    {
        "id": "ex_pri",
        "desc": "5è Primària grup · nouvingut+TDAH · B1 · biografia",
        "mecr": "B1",
        "skills": [
            "write-biografia", "generate-glossari", "generate-bastides-lectura",
            "generate-bastides-produccio", "generate-pictogrames",
            "generate-preguntes-comprensio",
        ],
    },
    {
        "id": "pol",
        "desc": "4t ESO · AC · B2 · assaig (Enriquiment)",
        "mecr": "B2",
        "skills": [
            "write-assaig", "generate-activitats-aprofundiment",
            "generate-mapa-mental", "generate-rubriques",
        ],
    },
]


def find_skill_dir(name: str) -> Path | None:
    for d in SKILLS_ROOT.rglob(name):
        if d.is_dir() and (d / "SKILL.md").exists():
            return d
    return None


def read_skill_body(skill_md_path: Path) -> str:
    content = skill_md_path.read_text(encoding="utf-8")
    parts = content.split("---", 2)
    return parts[2].strip() if len(parts) >= 3 else content


def extract_level_slice(prompt_adapter_path: Path, mecr: str) -> str:
    """Extreu la llesca de descriptors per al MECR donat del prompt_adapter.md."""
    if not prompt_adapter_path.exists():
        return ""
    content = prompt_adapter_path.read_text(encoding="utf-8")
    # Mapeja C1/C2 a C1+
    target = mecr if mecr not in ("C1", "C2") else "C1+"
    # Regex: ### `{{LLISTA_DESCRIPTORS_DEL_NIVELL}}` per a {target} ({etiqueta})
    # Captura fins al següent ### o final
    pattern = rf"###\s+`?\{{\{{LLISTA_DESCRIPTORS_DEL_NIVELL\}}\}}`?\s+per\s+a\s+{re.escape(target)}\s+\(([^)]+)\)\s*\n(.+?)(?=^###\s|\Z)"
    m = re.search(pattern, content, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    if not m:
        return ""
    return m.group(2).strip()


def main():
    print(f"AUDIT mida del prompt — slicing per-nivell vs SKILL.md complet\n")
    print(f"{'Cas':<10} {'MECR':<6} {'SKILLs':<6} {'actual':>10} {'sliced':>10} {'reducció':>12}")
    print("-" * 70)

    for cas in CASOS:
        actual_total = 0
        sliced_total = 0
        details = []
        for sname in cas["skills"]:
            sdir = find_skill_dir(sname)
            if not sdir:
                details.append((sname, "MISSING", 0, 0))
                continue
            body = read_skill_body(sdir / "SKILL.md")
            preamble = body.split(PREAMBLE_SPLIT, 1)[0].strip()
            slice_text = extract_level_slice(sdir / "prompt_adapter.md", cas["mecr"])
            sliced = preamble + "\n\n" + slice_text if slice_text else body  # fallback
            actual_total += len(body)
            sliced_total += len(sliced)
            details.append((sname, "OK", len(body), len(sliced)))

        reduction = actual_total - sliced_total
        pct = (reduction / actual_total * 100) if actual_total else 0
        print(f"{cas['id']:<10} {cas['mecr']:<6} {len(cas['skills']):<6} "
              f"{actual_total/1024:>8.1f}KB {sliced_total/1024:>8.1f}KB "
              f"{reduction/1024:>+8.1f}KB ({pct:.0f}%)")
        for sname, status, actual, sliced in details:
            print(f"  - {sname:<40} {status:<6} {actual/1024:>6.1f}KB → {sliced/1024:>5.1f}KB")
        print()

    print("─" * 70)
    print("Interpretació:")
    print("  - 'actual'  = mida de la concatenació de tots els SKILL.md complets enviada al LLM avui.")
    print("  - 'sliced'  = mida hipotètica si enviéssim preàmbul + llesca per nivell.")
    print("  - 'reducció' = quant baixaria el prompt amb la connexió de prompt_adapter.")
    print("")
    print("L'argument original per a 2-call ('el prompt era massa gran') quedaria atenuat si la")
    print("reducció és substancial. Però la decisió 2-call té altres motius (cost, UX, robustesa)")
    print("que NO depenen del prompt size.")


if __name__ == "__main__":
    main()
