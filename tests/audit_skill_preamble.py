"""
tests/audit_skill_preamble.py — Audit Q5-A: pèrdua de canon

Per a cada SKILL.md a corpusFJE/skills/, mesura:
  - Mida total del body.
  - Mida del preàmbul (tot el que va abans de `## Modulació per nivell`).
  - Si el preàmbul conté marcadors de canon crític (⚠️, OBLIGATORI, CONDICIONAL,
    FORMAT, MAI, PROHIBIT), els flagueja.
  - Si el SKILL té un `prompt_adapter.md` germà.

L'objectiu: identificar quins SKILLs tenen contingut canònic FORA del per-nivell
que es perdria si només enviéssim la llesca de prompt_adapter.

Sortida: taula + alertes per consola. Sense LLM, instantani.

Execució:
  python tests/audit_skill_preamble.py
"""
from __future__ import annotations

import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "corpus" / "external" / "corpusFJE" / "skills"

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# Marcadors que indiquen canon crític al preàmbul
CRITICAL_MARKERS = ["⚠️", "OBLIGATORI", "CONDICIONAL", "FORMAT", "MAI ", "PROHIBIT", "🚫", "🔴"]
PREAMBLE_SPLIT = "## Modulació per nivell"


def parse_skill_body(skill_md_path: Path) -> tuple[str, str]:
    """Retorna (body, preamble). body = tot sense frontmatter; preamble = before '## Modulació per nivell'."""
    content = skill_md_path.read_text(encoding="utf-8")
    parts = content.split("---", 2)
    if len(parts) < 3:
        return "", ""
    body = parts[2].strip()
    preamble = body.split(PREAMBLE_SPLIT, 1)[0].strip()
    return body, preamble


def count_critical_markers(text: str) -> dict[str, int]:
    counts = {}
    for marker in CRITICAL_MARKERS:
        n = text.count(marker)
        if n > 0:
            counts[marker] = n
    return counts


def main():
    if not SKILLS_ROOT.exists():
        print(f"ERROR: no existeix {SKILLS_ROOT}")
        sys.exit(2)

    print(f"AUDIT preàmbul SKILL.md — {SKILLS_ROOT}\n")
    print(f"{'SKILL':<45} {'body':>7} {'preamb':>7} {'adapter':>8} {'markers'}")
    print("-" * 100)

    skill_files = sorted(SKILLS_ROOT.rglob("SKILL.md"))
    n_with_adapter = 0
    n_with_substantive_preamble = 0
    flags = []

    for skill_md in skill_files:
        body, preamble = parse_skill_body(skill_md)
        name = skill_md.parent.name
        body_kb = len(body) / 1024
        preamb_kb = len(preamble) / 1024
        has_adapter = (skill_md.parent / "prompt_adapter.md").exists()
        markers = count_critical_markers(preamble)
        if has_adapter:
            n_with_adapter += 1
        # Preàmbul "substantiu" = >500 chars OR conté marcadors crítics
        is_substantive = len(preamble) > 500 or bool(markers)
        if is_substantive and has_adapter:
            n_with_substantive_preamble += 1
            flags.append((name, len(preamble), markers))
        marker_str = ", ".join(f"{m}×{n}" for m, n in markers.items()) if markers else ""
        adapter_str = "✓" if has_adapter else "—"
        print(f"{name:<45} {body_kb:>6.1f}K {preamb_kb:>6.1f}K {adapter_str:>8} {marker_str}")

    print()
    print("─" * 100)
    print(f"TOTAL SKILLs: {len(skill_files)}")
    print(f"  amb prompt_adapter.md: {n_with_adapter}")
    print(f"  sense prompt_adapter.md: {len(skill_files) - n_with_adapter}")
    print()
    print(f"SKILLs amb preàmbul SUBSTANTIU (>500 chars o marcadors crítics) i prompt_adapter:")
    print(f"  → CALDRÀ preservar aquest preàmbul si activem la slicing per-nivell")
    print(f"  → Total: {n_with_substantive_preamble}")
    print()

    if flags:
        print("Detall dels flagueats (top per longitud de preàmbul):")
        flags.sort(key=lambda f: -f[1])
        for name, plen, markers in flags[:10]:
            marker_str = ", ".join(f"{m}×{n}" for m, n in markers.items()) if markers else ""
            print(f"  {name:<45} preàmbul={plen:>5}c  {marker_str}")


if __name__ == "__main__":
    main()
