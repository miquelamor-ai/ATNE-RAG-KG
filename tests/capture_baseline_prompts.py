"""Captura el prompt complet (system Call 1 adapter + Call 2 complements) per a
casos canon. Serveix com a snapshot anti-regressió per al refactor A2 (post-freeze
rubrica.json v1.0). Quan A2 substitueixi les directives Python per consum del JSON,
els prompts generats ha de ser equivalents — qualsevol diff sorprenent és regressió.

Casos coberts:
  - titella                  · dislèxia A1 + 1r Primària (R3 verified:false + R4)
  - nouvingut_arab_preA1     · TOLC + L1 àrab + translit verified:false (A5 detecció moderna)
  - aacc_b2_divulgatiu        · AACC B2 (expertise reversal: no picto/esquema/glossari)
  - tdah_a2_noticia          · TDAH A2 (cas estàndard de gradació MECR)

Ús:
    python tests/capture_baseline_prompts.py            # genera tots els baselines
    python tests/capture_baseline_prompts.py --diff     # compara amb baselines existents

Output: tests/baseline_prompts/{case_id}.{call}.txt (call ∈ adapter, complements).

⚠️  TROBALLA 2026-06-01: `build_complements_prompt` NO és determinista — execucions
consecutives del mateix input generen sortides amb ordre de seccions lleugerament
diferent (probablement iteració sobre `set` no ordenat). Els baselines `.complements.txt`
són referència aproximada, no exacta. El refactor A2 hauria de corregir l'ordre
estable d'ensamblatge (per ex. ordenar les SKILLs actives per `name` abans
d'injectar-les al prompt). Els baselines `.adapter.txt` SÍ són deterministes.
"""

from __future__ import annotations

import argparse
import difflib
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Carrega .env perquè ATNE_USE_SKILLS i altres env vars del runtime estiguin
# disponibles. Sense això, build_complements_prompt detecta skills_enabled=False
# i retorna string buit.
try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
except Exception:
    pass

# Cal importar el module-level catalog/filter. server.py NO cal aquí (no fem HTTP).
from adaptation.prompt_builder import build_system_prompt, build_complements_prompt

OUTPUT_DIR = ROOT / "tests" / "baseline_prompts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ──────────────────────────────────────────────────────────────────────────────
# Casos canon
# ──────────────────────────────────────────────────────────────────────────────

CASES = [
    {
        "id": "titella",
        "descripcio": "Dislèxia A1 + 1r Primària (R3 verified:false + R4 cas BICS quotidians)",
        "profile": {
            "caracteristiques": {"dislexia": {"actiu": True}},
            "curs": "1r Primària",
        },
        "context": {"materia": "Educació visual", "etapa": "primaria"},
        "params": {
            "mecr_sortida": "A1",
            "dua": "Core",
            "genere_discursiu": "instruccions",
            "complements": {
                # Defaults R3 esperat: NO glossari (treure per dislèxia low),
                # pero la captura ens diu què demana avui ATNE realment.
                "esquema_visual": True,
                "bastides": True,
                "preguntes_comprensio": False,
            },
        },
    },
    {
        "id": "nouvingut_arab_preA1",
        "descripcio": "Nouvingut àrab pre-A1 (TOLC + translit + cas A5 detecció via conditions)",
        "profile": {
            # Estructura moderna: conditions amb nouvingut + L1, SENSE chip 'cat' legacy.
            "conditions": [{"key": "nouvingut", "l1": "àrab"}],
            "caracteristiques": {"nouvingut": {"actiu": True, "alfabet_llati": False, "calp": "emergent"}},
            "curs": "1r Primària",
        },
        "context": {"materia": "Coneixement del medi", "etapa": "primaria"},
        "params": {
            "mecr_sortida": "pre-A1",
            "dua": "Accés",
            "genere_discursiu": "divulgatiu",
            "complements": {
                "glossari": True,
                "pictogrames": True,
                "preguntes_comprensio": True,
            },
        },
    },
    {
        "id": "aacc_b2_divulgatiu",
        "descripcio": "Altes Capacitats B2 + divulgatiu (expertise reversal: no picto/esquema/glossari)",
        "profile": {
            "caracteristiques": {"aacc": {"actiu": True}},
            "curs": "3r ESO",
        },
        "context": {"materia": "Ciències", "etapa": "eso"},
        "params": {
            "mecr_sortida": "B2",
            "dua": "Enriquiment",
            "genere_discursiu": "divulgatiu",
            "complements": {
                "activitats_aprofundiment": True,
                "mapa_mental": True,
                "rubriques": True,
            },
        },
    },
    {
        "id": "tdah_a2_noticia",
        "descripcio": "TDAH A2 + notícia (cas estàndard de gradació MECR + chunking)",
        "profile": {
            "caracteristiques": {"tdah": {"actiu": True, "grau": "moderat"}},
            "curs": "1r ESO",
        },
        "context": {"materia": "Llengua catalana", "etapa": "eso"},
        "params": {
            "mecr_sortida": "A2",
            "dua": "Core",
            "genere_discursiu": "noticia",
            "complements": {
                "glossari": True,
                "esquema_visual": True,
                "preguntes_comprensio": True,
            },
        },
    },
]


def capture_case(case: dict) -> dict[str, str]:
    """Genera els 2 prompts (adapter Call 1 + complements Call 2) per a un cas."""
    profile = case["profile"]
    context = case["context"]
    params = case["params"]
    adapter_prompt = build_system_prompt(profile, context, params, rag_context="", adapter_only=True)
    complements_prompt = build_complements_prompt(profile, context, params)
    return {"adapter": adapter_prompt, "complements": complements_prompt}


def write_baselines() -> int:
    written = 0
    for case in CASES:
        prompts = capture_case(case)
        for call_kind, content in prompts.items():
            out_path = OUTPUT_DIR / f"{case['id']}.{call_kind}.txt"
            header = (
                f"# Baseline prompt · {case['id']} · {call_kind}\n"
                f"# Descripció: {case['descripcio']}\n"
                f"# Generat per capture_baseline_prompts.py (versió pre-A2 refactor)\n"
                f"# NO editar a mà. Per regenerar: python tests/capture_baseline_prompts.py\n"
                f"# ────────────────────────────────────────────────────────────────\n\n"
            )
            out_path.write_text(header + content, encoding="utf-8")
            written += 1
    return written


def diff_with_baselines() -> int:
    """Compara la captura actual amb els baselines existents. Retorna nombre de
    fitxers amb diff (0 si tot coincideix)."""
    diffs = 0
    for case in CASES:
        prompts = capture_case(case)
        for call_kind, content in prompts.items():
            path = OUTPUT_DIR / f"{case['id']}.{call_kind}.txt"
            if not path.exists():
                print(f"⚠️  Baseline absent: {path.name}")
                diffs += 1
                continue
            existing = path.read_text(encoding="utf-8")
            # Strip header lines (les que comencen amb '#' i fins primera línia buida)
            lines = existing.splitlines()
            try:
                first_blank = lines.index("")
                existing_body = "\n".join(lines[first_blank + 1:])
            except ValueError:
                existing_body = existing
            if existing_body.strip() != content.strip():
                diffs += 1
                d = difflib.unified_diff(
                    existing_body.splitlines(keepends=True),
                    content.splitlines(keepends=True),
                    fromfile=f"baseline/{path.name}",
                    tofile=f"current/{path.name}",
                    n=3,
                )
                print(f"❌ DIFF a {path.name}:")
                print("".join(list(d)[:60]))  # primeres 60 línies de diff
            else:
                print(f"✓  {path.name} sense canvis")
    return diffs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--diff", action="store_true", help="Compara amb baselines en lloc d'escriure")
    args = parser.parse_args()

    if args.diff:
        diffs = diff_with_baselines()
        if diffs:
            print(f"\n{diffs} fitxer(s) amb diff. Revisa abans de regenerar.")
            sys.exit(1)
        print("\n✓ Tots els baselines coincideixen.")
        return

    n = write_baselines()
    print(f"✓ Escrits {n} fitxers de baseline a {OUTPUT_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
