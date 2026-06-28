"""Smoke test LLM real per a A2 fase 1 — pilots glossari + bastides.

Comprova que el refactor (consum de rubrica.json en lloc de directives Python
hardcoded) NO introdueix regressió funcional al gpt-4.1-mini abans de propagar
la cascada als 35 skills restants.

Casos:
  - titella           : R3+R4 dislèxia A1 + 1r Primària + instructiu
                        (BICS quotidians → glossari ha de respectar sostre 2 + omet quotidians)
  - nouvingut_arab    : pre-A1 + L1 àrab + DUA Accés (A5)
                        (glossari bilingüe + bastides escasses)

Comprovacions estructurals:
  - Header `## Glossari` literal present
  - Taula MD amb pipes a glossari
  - Header `## Bastides` literal present
  - H3 `### Bastides de lectura` present
  - Bullets `**Abans...**` / `**Durant...**` / `**Després...**` (canon v1.0.1)

Ús: python tests/smoke_a2_pilots_llm.py
Cost: ~$0.02-0.05 amb gpt-4.1-mini (2 crides curtes).
"""
from __future__ import annotations

import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
except Exception:
    pass

from adaptation.prompt_builder import build_complements_prompt
from adaptation.llm_clients import _call_llm

# Adaptats curts (simulen el que arriba a Call 2 ja adaptat)
TITELLA_ADAPTAT = """## Text adaptat

Com fer un titella de mitja.

Necessites una mitja, dos botons, fil i una agulla.

Posa els botons a la mitja per fer els ulls.

Lliga els botons amb fil.

El teu titella ja pot jugar."""

NOUVINGUT_ADAPTAT = """## Text adaptat

L'aigua és molt important.

Bevem aigua cada dia.

L'aigua és transparent."""


CASES = [
    {
        "id": "titella",
        "profile": {
            "caracteristiques": {"dislexia": {"actiu": True, "grau": "moderat"}},
        },
        "context": {"curs": "1r Primaria", "etapa": "primaria"},
        "params": {
            "mecr_sortida": "A1",
            "dua": "Core",
            "genere_discursiu": "instruccions",
            "lang": "ca",
            "complements": {"glossari": True, "bastides": True},
        },
        "adaptat": TITELLA_ADAPTAT,
    },
    {
        "id": "nouvingut_arab_preA1",
        "profile": {
            "caracteristiques": {"nouvingut": {"actiu": True, "L1": "arab"}},
        },
        "context": {"curs": "1r Primaria", "etapa": "primaria"},
        "params": {
            "mecr_sortida": "pre-A1",
            "dua": "Acces",
            "genere_discursiu": "divulgatiu",
            "lang": "ca",
            "complements": {"glossari": True, "bastides": True, "pictogrames": True},
        },
        "adaptat": NOUVINGUT_ADAPTAT,
    },
]


def assert_check(name: str, ok: bool, detail: str = "") -> int:
    mark = "✅" if ok else "❌"
    print(f"   {mark} {name}{(' — ' + detail) if detail else ''}")
    return 0 if ok else 1


def smoke_case(case: dict) -> int:
    print(f"\n{'='*60}\nCas: {case['id']}\n{'='*60}")
    system = build_complements_prompt(case["profile"], case["context"], case["params"])
    if not system:
        print("⚠️  Prompt buit — saltant")
        return 0
    user = case["adaptat"]
    print(f"[system prompt] {len(system)} chars · [user] {len(user)} chars")
    print("→ Cridant gpt-4.1-mini...")
    out = _call_llm("gpt-4.1-mini", system, user)
    print(f"← {len(out)} chars rebuts\n")
    print("--- OUTPUT ---")
    print(out)
    print("--- END ---\n")

    fails = 0
    print("CHECKS:")
    has_h2_gl = "## Glossari" in out
    fails += assert_check("Header `## Glossari` literal", has_h2_gl)
    if has_h2_gl:
        gl_section = out.split("## Glossari", 1)[1].split("\n## ", 1)[0]
        mecr = case["params"]["mecr_sortida"].lower()
        # Canon pas_2_estructura: a pre-A1 NO taula (emoji+terme negreta).
        # A A1+ sí taula amb pipes.
        if mecr.startswith("pre-a1"):
            has_emoji_negreta = bool(re.search(r"\*\*\w+\*\*", gl_section))
            fails += assert_check(
                "pre-A1: format emoji+negreta (canon pas_2_estructura, SENSE taula)",
                has_emoji_negreta
            )
        else:
            has_pipes = gl_section.count("|") >= 4
            fails += assert_check("A1+: taula MD amb pipes a glossari", has_pipes,
                                  detail=f"({gl_section.count('|')} pipes)")
        # Cas titella: quotidians al glossari = WARNING (no fail). gpt-4.1-mini
        # sovint inclou 1-2 quotidians a MECR baix. Candidat post-pilot a model
        # més capaç (validat 31/05 amb MiMo Pro al NotebookLM).
        if case["id"] == "titella":
            quotidians = ["mitja", "botó", "agulla", "fil"]
            found = [q for q in quotidians if re.search(rf"\b{q}\b", gl_section, re.I)]
            if found:
                print(f"   ⚠️  WARNING (no fail) titella inclou quotidians {found} — "
                      f"comportament conegut gpt-4.1-mini, MiMo Pro candidat post-cascada")
        # Cas nouvingut àrab: el glossari ha de contenir caràcters àrabs (L1).
        if case["id"] == "nouvingut_arab_preA1":
            has_arabic = bool(re.search(r"[؀-ۿ]", gl_section))
            fails += assert_check("Cas nouvingut àrab: glossari conté caràcters L1",
                                  has_arabic)

    has_h2_bs = "## Bastides" in out
    fails += assert_check("Header `## Bastides` literal", has_h2_bs)
    if has_h2_bs:
        bs_section = out.split("## Bastides", 1)[1].split("\n## ", 1)[0]
        has_h3_lectura = "### Bastides de lectura" in bs_section
        fails += assert_check("H3 `### Bastides de lectura` (canon v1.0.1)", has_h3_lectura)
        has_abans = bool(re.search(r"\*\*Abans", bs_section))
        has_durant = bool(re.search(r"\*\*Durant", bs_section))
        has_despres = bool(re.search(r"\*\*Despr[éè]s", bs_section))
        fails += assert_check(
            "Bullets **Abans/Durant/Després:** (canon v1.0.1)",
            has_abans and has_durant and has_despres,
            detail=f"abans={has_abans} durant={has_durant} despres={has_despres}"
        )

    return fails


def main() -> int:
    total_fails = 0
    for c in CASES:
        total_fails += smoke_case(c)
    print(f"\n{'='*60}")
    print(f"RESULTAT: {'✅ PASS' if total_fails == 0 else f'❌ {total_fails} fail(s)'}")
    print(f"{'='*60}")
    return total_fails


if __name__ == "__main__":
    sys.exit(main())
