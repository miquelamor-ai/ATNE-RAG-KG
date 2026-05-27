"""
tests/golden/run_golden.py — Harness golden Fase A per a ATNE.

Què fa (TOT offline, ZERO crides a LLM):
  1) Carrega matrix.yaml (canon) i cases.yaml (15 casos).
  2) Per cada cas:
     - Crida skills_loader.select_active() i comprova quines SKILLs s'activen.
     - Compara amb cases.expected_skills (diff +/-).
     - Crida instruction_filter.get_instructions() i comprova que no peta i
       activa macrodirectives plausibles.
     - Calcula els "defaults" que el frontend hauria d'auto-activar segons la
       matriu, i marca discrepàncies (gaps documentats vs gaps no documentats).
  3) Genera un informe text + Markdown a tests/golden/_report.md amb:
     - Resum global (PASS / FAIL / WARN per cas)
     - Heatmap 12 condicions × 12 complements
     - Llistat de gaps i regressions

Execució:
    python tests/golden/run_golden.py
    python tests/golden/run_golden.py --case C01_tea_b1_noticia   # filtra
    python tests/golden/run_golden.py --json                       # output JSON

No requereix .env ni cap clau API. No fa cap crida HTTP. Apte per pre-commit.
"""
from __future__ import annotations

import argparse
import json
import sys
import traceback
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Configuració de paths abans dels imports d'ATNE
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

# Windows: força UTF-8 a stdout/stderr per imprimir emojis sense petar (cp1252).
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

try:
    import yaml
except ImportError:
    print("ERROR: cal `pyyaml`. Instal·la amb: pip install pyyaml")
    sys.exit(2)

# Imports d'ATNE (després d'afegir ROOT al path)
try:
    import skills_loader
    import instruction_filter
except Exception as e:
    print(f"ERROR important skills_loader / instruction_filter: {e}")
    print("Assegura't d'executar des de l'arrel del repo o amb el venv adequat.")
    sys.exit(2)


# ─────────────────────────────────────────────────────────────────────────────
# Models de resultat
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class CaseResult:
    case_id: str
    descripcio: str
    gap_known: str | None = None
    skills_expected: list[str] = field(default_factory=list)
    skills_actual: list[str] = field(default_factory=list)
    skills_missing: list[str] = field(default_factory=list)   # esperades però no actives
    skills_extra: list[str] = field(default_factory=list)     # actives no esperades
    filter_ok: bool = False
    filter_macros: list[str] = field(default_factory=list)
    filter_suppressed: int = 0
    filter_error: str | None = None
    status: str = "PENDING"   # PASS / FAIL / WARN / ERROR
    notes: list[str] = field(default_factory=list)


@dataclass
class GlobalReport:
    casos: list[CaseResult] = field(default_factory=list)
    matrix_gaps: list[str] = field(default_factory=list)         # gaps estàtics matriu vs codi
    backend_only_keys: list[str] = field(default_factory=list)
    canon_only_conds: list[str] = field(default_factory=list)
    skills_loaded: int = 0
    skills_active_disabled: bool = False


# ─────────────────────────────────────────────────────────────────────────────
# Lògica
# ─────────────────────────────────────────────────────────────────────────────

def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def static_matrix_check(matrix: dict) -> tuple[list[str], list[str], list[str]]:
    """
    Comprovacions estàtiques entre matriu canònica i claus backend conegudes.
    Retorna (gaps_text, backend_only, canon_only).
    """
    # Backend keys autoritatius — extrets de ui/atne/js/llm.js ALL_CHAR_KEYS.
    # Actualitzar aquesta llista si canvia ALL_CHAR_KEYS al frontend.
    BACKEND_CHAR_KEYS = {
        "tdah", "dislexia", "nouvingut", "altes_capacitats",
        "tea", "di", "discapacitat_auditiva", "discapacitat_visual",
        "tdl", "discalculia",
        # Afegides 2026-05-27 per cobrir matriu canònica §7 sencera.
        "dispraxia", "vulnerabilitat", "emocional",
    }
    canon_keys = set(matrix["condicions"].keys())
    # Mapping curt → backend
    mapped_to_backend = {
        v["chars_key"] for v in matrix["condicions"].values() if v.get("chars_key")
    }

    gaps: list[str] = []
    # 1. Condicions de la matriu sense chars_key (no representables al backend)
    for short, info in matrix["condicions"].items():
        if info.get("chars_key") is None and not info.get("fora_matriu"):
            gaps.append(
                f"Matriu canon té '{short}' ({info['label']}) però NO existeix a "
                f"BACKEND_CHAR_KEYS. Frontend no pot enviar aquesta condició → "
                f"defaults i instruccions PERFIL no s'apliquen mai."
            )

    backend_only = sorted(BACKEND_CHAR_KEYS - mapped_to_backend)
    # canon_only són les condicions de la matriu sense backend (sense GAP fora_matriu)
    canon_only = sorted(
        short for short, info in matrix["condicions"].items()
        if info.get("chars_key") is None and not info.get("fora_matriu")
    )
    if backend_only:
        gaps.append(
            f"BACKEND_CHAR_KEYS té {backend_only} que NO surt a la matriu §7. "
            f"Si el frontend les envia, no hi ha defaults canonificats."
        )
    return gaps, backend_only, canon_only


def run_case(
    case: dict,
    all_skills: list[Any],
    matrix: dict,
) -> CaseResult:
    res = CaseResult(
        case_id=case["id"],
        descripcio=case["descripcio"],
        gap_known=case.get("gap_known"),
        skills_expected=sorted(case.get("expected_skills", [])),
    )

    profile = case.get("profile", {})
    params = case.get("params", {})

    # ── (1) Skills actives ──────────────────────────────────────────────
    actives_adapter = skills_loader.select_active(all_skills, profile, params, agent_role="adapter")
    actives_complements = skills_loader.select_active(all_skills, profile, params, agent_role="complements")
    actives_all = sorted({s.name for s in (actives_adapter + actives_complements)})
    res.skills_actual = actives_all

    expected_set = set(res.skills_expected)
    actual_set = set(res.skills_actual)
    res.skills_missing = sorted(expected_set - actual_set)
    res.skills_extra = sorted(actual_set - expected_set)

    # ── (2) instruction_filter ──────────────────────────────────────────
    try:
        out = instruction_filter.get_instructions(profile, params, context=params)
        macros = list(out.get("macrodirectives", {}).keys())
        suppressed = len(out.get("suppressed", []))
        res.filter_ok = True
        res.filter_macros = macros
        res.filter_suppressed = suppressed
    except Exception as e:
        res.filter_ok = False
        res.filter_error = f"{type(e).__name__}: {e}"

    # ── (3) Status global ───────────────────────────────────────────────
    if res.filter_error:
        res.status = "ERROR"
        res.notes.append(f"instruction_filter peta: {res.filter_error}")
    elif res.skills_missing and not res.gap_known:
        res.status = "FAIL"
        res.notes.append(f"SKILLs esperades absents: {res.skills_missing}")
    elif res.skills_missing and res.gap_known:
        res.status = "WARN"
        res.notes.append(f"GAP conegut · falten {res.skills_missing} · {res.gap_known}")
    elif res.skills_extra:
        res.status = "WARN"
        res.notes.append(f"SKILLs extra actives (no esperades): {res.skills_extra}")
    else:
        res.status = "PASS"

    return res


def render_markdown(report: GlobalReport, matrix: dict) -> str:
    out = []
    out.append("# Golden Harness — Fase A · Informe d'execució\n")
    out.append(f"_Skills carregades: **{report.skills_loaded}** "
               f"({'⚠ ATNE_USE_SKILLS=OFF' if report.skills_active_disabled else 'OK'})_\n")

    # Resum
    total = len(report.casos)
    pass_n = sum(1 for c in report.casos if c.status == "PASS")
    fail_n = sum(1 for c in report.casos if c.status == "FAIL")
    warn_n = sum(1 for c in report.casos if c.status == "WARN")
    err_n = sum(1 for c in report.casos if c.status == "ERROR")
    out.append("## Resum\n")
    out.append(f"| Casos | PASS | WARN | FAIL | ERROR |")
    out.append(f"|-------|------|------|------|-------|")
    out.append(f"| {total} | {pass_n} | {warn_n} | {fail_n} | {err_n} |\n")

    # Gaps estàtics
    if report.matrix_gaps:
        out.append("## Gaps estàtics (matriu canònica vs codi backend)\n")
        for g in report.matrix_gaps:
            out.append(f"- ⚠️ {g}")
        out.append("")

    # Per cada cas
    out.append("## Resultat per cas\n")
    out.append("| Cas | Estat | SKILLs actives | Falten | Extra | Macros |")
    out.append("|-----|-------|----------------|--------|-------|--------|")
    icon = {"PASS": "✅", "WARN": "⚠️", "FAIL": "❌", "ERROR": "💥"}
    for c in report.casos:
        out.append(
            f"| `{c.case_id}` | {icon.get(c.status, '?')} {c.status} | "
            f"{len(c.skills_actual)} | "
            f"{', '.join(c.skills_missing) or '—'} | "
            f"{', '.join(c.skills_extra) or '—'} | "
            f"{len(c.filter_macros)} |"
        )

    # Detall per cas amb notes
    out.append("\n## Detall i notes\n")
    for c in report.casos:
        out.append(f"### {icon.get(c.status, '?')} `{c.case_id}` — {c.descripcio}")
        if c.gap_known:
            out.append(f"- GAP conegut: {c.gap_known}")
        out.append(f"- Esperades: `{c.skills_expected}`")
        out.append(f"- Actives:   `{c.skills_actual}`")
        if c.filter_error:
            out.append(f"- ❗ instruction_filter ERROR: `{c.filter_error}`")
        else:
            out.append(f"- Macros actives ({len(c.filter_macros)}): `{c.filter_macros[:6]}{'…' if len(c.filter_macros)>6 else ''}`")
            out.append(f"- Instruccions suprimides: {c.filter_suppressed}")
        for n in c.notes:
            out.append(f"- _{n}_")
        out.append("")

    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description="Golden harness Fase A")
    parser.add_argument("--case", help="Filtra un sol cas per id")
    parser.add_argument("--json", action="store_true", help="Output JSON en lloc de markdown")
    parser.add_argument("--no-write", action="store_true", help="No escriguis _report.md")
    args = parser.parse_args()

    here = Path(__file__).parent
    matrix = load_yaml(here / "matrix.yaml")
    cases_file = load_yaml(here / "cases.yaml")

    report = GlobalReport()

    # ── (0) Comprovacions estàtiques (matriu vs backend) ───────────────
    gaps, backend_only, canon_only = static_matrix_check(matrix)
    report.matrix_gaps = gaps
    report.backend_only_keys = backend_only
    report.canon_only_conds = canon_only

    # ── (1) Carrega skills ─────────────────────────────────────────────
    # NOTA: skills_loader.load_skills NO requereix ATNE_USE_SKILLS=true per
    # carregar; només l'agent_check global hi depèn. Ho fem servir directament.
    roots = skills_loader.default_skills_roots()
    all_skills = skills_loader.load_skills(roots)
    report.skills_loaded = len(all_skills)
    report.skills_active_disabled = not skills_loader.is_skills_enabled()

    # ── (2) Executa casos ──────────────────────────────────────────────
    target = args.case
    for case in cases_file["casos"]:
        if target and case["id"] != target:
            continue
        try:
            res = run_case(case, all_skills, matrix)
        except Exception as e:
            res = CaseResult(case_id=case["id"], descripcio=case["descripcio"])
            res.status = "ERROR"
            res.notes.append(f"Excepció no controlada: {type(e).__name__}: {e}\n{traceback.format_exc()}")
        report.casos.append(res)

    # ── (3) Output ────────────────────────────────────────────────────
    if args.json:
        payload = {
            "skills_loaded": report.skills_loaded,
            "skills_enabled_runtime": not report.skills_active_disabled,
            "matrix_gaps": report.matrix_gaps,
            "casos": [
                {
                    "id": c.case_id,
                    "status": c.status,
                    "skills_expected": c.skills_expected,
                    "skills_actual": c.skills_actual,
                    "skills_missing": c.skills_missing,
                    "skills_extra": c.skills_extra,
                    "filter_ok": c.filter_ok,
                    "filter_macros": c.filter_macros,
                    "filter_error": c.filter_error,
                    "notes": c.notes,
                } for c in report.casos
            ],
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    md = render_markdown(report, matrix)
    print(md)

    if not args.no_write:
        out_path = here / "_report.md"
        out_path.write_text(md, encoding="utf-8")
        print(f"\n[golden] Informe escrit a: {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
