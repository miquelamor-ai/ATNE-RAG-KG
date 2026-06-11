"""
tests/golden/prompt_checks.py — Capa 1.5 del harness: validador estàtic del prompt.

PROPÒSIT
Detectar bugs del prompt **abans** d'executar cap adapt LLM. Cost zero,
1 segon. Per cada cas del Golden Suite, construeix el system prompt
complet via `build_system_prompt()` i aplica una bateria d'asserts
canònics. Reporta què hi falta, què sobra, què és contradictori.

PER QUÈ EXISTEIX
La Fase A valida triggers de SKILLs i el filtre d'instruccions, però NO
mira el prompt final. La Fase B avalua el text generat (car, tard).
Entre les dues, faltava una capa que validés ESTÀTICAMENT el prompt
construït. Sense aquesta capa, bugs com:
- "A-02 (parèntesi) i A-30 (frase nova) actius alhora a DUA Accés"
- "Notícia: gènere demanat però bloc explícit absent"
- "Esquema visual demanat però sense instrucció específica"
- "Nouvingut amb L1: bloc TILC absent al prompt"
s'han descobert un per un després d'hores d'execució Fase B.

EXECUCIÓ:
    python tests/golden/prompt_checks.py
    python tests/golden/prompt_checks.py --case marc
    python tests/golden/prompt_checks.py --verbose

OUTPUT:
- Resum executiu (PASS/FAIL per cas)
- Detall: per cada cas, llista de checks PASSED i FAILED
- Exit code != 0 si hi ha fallades crítiques
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

try:
    import yaml
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
except ImportError as e:
    print(f"ERROR: cal {e.name}. pip install pyyaml python-dotenv")
    sys.exit(2)


# ─── Definició de checks (declaratius) ─────────────────────────────────────

@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str = ""
    severity: str = "ERROR"  # ERROR | WARN | INFO


CHECKS = []  # llista de funcions check(case, prompt) -> CheckResult


def check(name: str, severity: str = "ERROR"):
    """Decorator per registrar un check."""
    def deco(fn):
        fn._name = name
        fn._severity = severity
        CHECKS.append(fn)
        return fn
    return deco


# ─── Checks universals (apliquen a tot cas) ────────────────────────────────

@check("SEMPRE_basic_blocks", severity="ERROR")
def _c_basic(case, prompt):
    """El prompt ha de tenir blocs estructurals mínims."""
    missing = []
    for needle in ["ATNE", "MECR", "DUA", "Text adaptat"]:
        if needle.lower() not in prompt.lower():
            missing.append(needle)
    if missing:
        return CheckResult("SEMPRE_basic_blocks", False,
                          f"Falten blocs bàsics: {missing}")
    return CheckResult("SEMPRE_basic_blocks", True)


@check("GENERE_present_at_end", severity="ERROR")
def _c_genere(case, prompt):
    """El gènere demanat ha d'aparèixer al bloc obligatori (recency bias)."""
    genere = case["params"].get("genere_discursiu", "")
    if not genere:
        return CheckResult("GENERE_present_at_end", True, "Cas sense gènere")
    last_3k = prompt[-3000:]  # només mira els últims 3K (recency)
    if genere.lower() not in last_3k.lower():
        return CheckResult("GENERE_present_at_end", False,
                          f"Gènere '{genere}' NO apareix als últims 3K del prompt")
    return CheckResult("GENERE_present_at_end", True,
                      f"Gènere '{genere}' present al bloc final")


@check("GENERE_specific_format", severity="WARN")
def _c_genere_format(case, prompt):
    """Cada gènere té un format específic mencionat al prompt."""
    genere = case["params"].get("genere_discursiu", "")
    if not genere:
        return CheckResult("GENERE_specific_format", True, "Cas sense gènere")
    # Format mínim esperat per cada gènere
    format_keywords = {
        "noticia":     ["titular", "lead", "piràmide"],
        "entrevista":  ["pregunta", "resposta", "torns"],
        "opinio":      ["tesi", "argument"],
        "conte":       ["narrativa", "personatges"],
        "fabula":      ["moral", "personatges"],
        "instructiu":  ["passos", "materials"],
        "receptari":   ["passos", "ingredient"],
        "manual":      ["passos", "instrucci"],
        "dialeg":      ["parlants", "torns"],
        "assaig":      ["tesi", "argument"],
    }
    keywords = format_keywords.get(genere, [])
    if not keywords:
        return CheckResult("GENERE_specific_format", True,
                          f"Gènere '{genere}' no té requisit format específic")
    last_3k = prompt[-3000:].lower()
    missing = [k for k in keywords if k.lower() not in last_3k]
    if missing:
        return CheckResult("GENERE_specific_format", False,
                          f"Format '{genere}': falten keywords {missing} al bloc final",
                          severity="WARN")
    return CheckResult("GENERE_specific_format", True,
                      f"Format '{genere}' té tots els keywords: {keywords}")


# ─── Checks UNE 153101 (DUA Accés) ────────────────────────────────────────

@check("UNE_accés_no_parens", severity="ERROR")
def _c_une_no_parens(case, prompt):
    """A DUA Accés, el prompt ha de prohibir explícitament parèntesi a definicions."""
    if case["params"].get("dua") != "Accés":
        return CheckResult("UNE_accés_no_parens", True, "Cas no és DUA Accés")
    # Cerca instruccions A-30 (frase nova) i absència A-02 (parèntesi)
    has_frase_nova = "frase nova" in prompt.lower() or "no parèntesi" in prompt.lower() or "no parentesi" in prompt.lower()
    has_paren_inst = "entre parèntesis" in prompt.lower() or "amb definició entre parèntesi" in prompt.lower()
    if has_paren_inst and not has_frase_nova:
        return CheckResult("UNE_accés_no_parens", False,
                          "DUA Accés però el prompt encara diu 'entre parèntesis' (contradicció A-02)")
    if not has_frase_nova:
        return CheckResult("UNE_accés_no_parens", False,
                          "DUA Accés sense instrucció 'definicions com frase nova' (A-30)")
    return CheckResult("UNE_accés_no_parens", True, "A-30 actiu, A-02 suprimit")


@check("UNE_accés_no_majus", severity="WARN")
def _c_une_no_majus(case, prompt):
    """A DUA Accés/Core, no MAJÚSCULES sostingudes (A-31)."""
    if case["params"].get("dua") == "Enriquiment":
        return CheckResult("UNE_accés_no_majus", True, "Enriquiment exempt")
    if "majúscules" not in prompt.lower() and "majuscules" not in prompt.lower():
        return CheckResult("UNE_accés_no_majus", False,
                          "DUA Accés/Core sense instrucció no MAJÚSCULES (A-31)",
                          severity="WARN")
    return CheckResult("UNE_accés_no_majus", True, "Instrucció no MAJÚSCULES present")


@check("UNE_accés_veu_activa", severity="WARN")
def _c_une_veu_activa(case, prompt):
    """A DUA Accés/Core, veu activa, no passiva reflexa (A-33)."""
    if case["params"].get("dua") == "Enriquiment":
        return CheckResult("UNE_accés_veu_activa", True, "Enriquiment exempt")
    if "veu activa" not in prompt.lower() and "passiva reflexa" not in prompt.lower():
        return CheckResult("UNE_accés_veu_activa", False,
                          "Sense instrucció veu activa (A-33)",
                          severity="WARN")
    return CheckResult("UNE_accés_veu_activa", True, "Instrucció veu activa present")


# ─── Checks per complements activats ──────────────────────────────────────

@check("ESQUEMA_inst_present", severity="ERROR")
def _c_esquema(case, prompt):
    """Si esquema_visual=true, ha d'haver instrucció específica al prompt.

    L'esquema es genera a la 2a crida (build_complements_prompt) si skills+
    complements actius. Per això mira també el complements_prompt.
    """
    if not case["params"].get("complements", {}).get("esquema_visual"):
        return CheckResult("ESQUEMA_inst_present", True, "Esquema no demanat")
    # Mira tant el system_prompt principal com el complements_prompt
    try:
        from adaptation.prompt_builder import build_complements_prompt
        comp_prompt = build_complements_prompt(
            profile=case["profile"],
            context={"etapa": case["params"].get("etapa", "ESO"), "materia": "ciències naturals"},
            params=case["params"],
        )
    except Exception:
        comp_prompt = ""
    combined = (prompt + "\n\n---COMPLEMENTS---\n\n" + comp_prompt).lower()
    needles = ["esquema visual", "nodes"]
    found = all(n.lower() in combined for n in needles)
    if not found:
        return CheckResult("ESQUEMA_inst_present", False,
                          "Esquema demanat però sense instrucció específica (nodes/format) ni al system_prompt ni al complements_prompt")
    return CheckResult("ESQUEMA_inst_present", True, "Instrucció esquema present al complements_prompt")


@check("GLOSSARI_L1_condicional", severity="WARN")
def _c_glossari_l1(case, prompt):
    """Si glossari demanat però NO nouvingut amb L1: NO ha d'incloure columna L1."""
    if not case["params"].get("complements", {}).get("glossari"):
        return CheckResult("GLOSSARI_L1_condicional", True, "Glossari no demanat")
    chars = case["profile"]["caracteristiques"]
    nouvingut = chars.get("nouvingut", {})
    has_l1 = isinstance(nouvingut, dict) and nouvingut.get("l1")
    # Cerca instrucció que indica "monolingüe" si no hi ha L1
    if not has_l1:
        # Hauria d'haver instrucció que el glossari NO porti L1
        if "monolingüe" not in prompt.lower() and "monolingue" not in prompt.lower():
            return CheckResult("GLOSSARI_L1_condicional", False,
                              "Glossari demanat sense L1 declarada però sense instrucció 'monolingüe'",
                              severity="WARN")
    return CheckResult("GLOSSARI_L1_condicional", True,
                      f"Glossari OK (has_l1={has_l1})")


# ─── Checks de contradicció / coherència ──────────────────────────────────

@check("NO_A02_A30_simultaneous", severity="ERROR")
def _c_no_contradiction(case, prompt):
    """A-02 (parèntesi) i A-30 (frase nova) NO poden estar actius alhora."""
    # Detectem si els 2 textos apareixen al prompt
    has_a02 = "amb definició entre parèntesi" in prompt.lower() or "negreta amb definició entre parèntesis" in prompt.lower()
    has_a30 = "frase nova" in prompt.lower() and "definicions" in prompt.lower()
    if has_a02 and has_a30:
        return CheckResult("NO_A02_A30_simultaneous", False,
                          "CONTRADICCIÓ: A-02 (parèntesi) i A-30 (frase nova) ambdós al prompt")
    return CheckResult("NO_A02_A30_simultaneous", True,
                      f"Sense contradicció (a02={has_a02}, a30={has_a30})")


# ─── Check "Per al docent" — taxonomia 9 categories A-I ────────────────────

# Les 9 categories canòniques A-I (font: ui/saber-ne.html "Categories d'adaptació",
# decisió Miquel 2026-05-27, commits cec9b14+74bf20d). El frontend (pas3.html dimMap)
# les renderitza. El prompt 2-call (adapter_only) ha de GENERAR-les: si genera
# l'estructura antiga de 5 punts, el docent rep argumentació genèrica i el dimMap
# cau als fallbacks legacy. Aquest check captura aquell desync.
_PER_AL_DOCENT_9CAT = [
    "Adaptació Lingüística",
    "Estructura i Organització",
    "Suport Cognitiu",
    "Multimodalitat",
    "Contingut Curricular",
    "Avaluació i Comprensió",
    "Personalització Lingüística",
    "Adaptacions per Perfil",
    "Meta-regles Transversals",
]


@check("PER_AL_DOCENT_9_categories", severity="ERROR")
def _c_per_al_docent_9cat(case, prompt):
    """La secció 'Per al docent' (## Argumentació pedagògica) ha d'usar la
    taxonomia canònica de 9 categories A-I, NO l'estructura antiga de 5 punts.

    El prompt es construeix amb adapter_only=True (camí 2-call real). El bug
    històric: aquest camí va quedar desincronitzat i generava els 5 punts
    genèrics ('adaptació lingüística, atenció a la diversitat, suport
    multimodal, gradació cognitiva, rigor curricular'), mai les 9 categories.
    """
    low = prompt.lower()
    present = [c for c in _PER_AL_DOCENT_9CAT if c.lower() in low]
    # Signatura inequívoca de l'estructura ANTIGA de 5 punts.
    has_legacy_5 = (
        "atenció a la diversitat, suport multimodal, gradació cognitiva" in low
    )
    if len(present) < 9:
        absent = [c for c in _PER_AL_DOCENT_9CAT if c.lower() not in low]
        extra = " (encara hi ha l'estructura antiga de 5 punts)" if has_legacy_5 else ""
        return CheckResult(
            "PER_AL_DOCENT_9_categories", False,
            f"Falten {len(absent)}/9 categories canòniques: {absent}{extra}",
        )
    if has_legacy_5:
        return CheckResult(
            "PER_AL_DOCENT_9_categories", False,
            "Les 9 categories hi són però també queda l'estructura antiga de 5 punts (duplicació)",
        )
    return CheckResult("PER_AL_DOCENT_9_categories", True,
                       "Taxonomia 9 cat A-I present, sense estructura antiga")


@check("PER_AL_DOCENT_dedicated_mandatory", severity="ERROR")
def _c_per_al_docent_dedicated(case, prompt):
    """La crida DEDICADA «Per al docent» (build_argumentacio_prompt, producció 2-call) ha de
    contenir les 9 cat + el checklist de categories OBLIGATÒRIES del cas. Concretament: si el
    perfil és nouvingut amb L1, la categoria G ha de ser a la llista obligatòria (era el bug
    empíric: G mai apareixia). Validat NotebookLM 2026-06-11.
    """
    try:
        from adaptation.prompt_builder import build_argumentacio_prompt
        arg_prompt = build_argumentacio_prompt(
            profile=case["profile"],
            context={"etapa": case["params"].get("etapa", "ESO"), "materia": "ciències naturals"},
            params=case["params"],
        )
    except Exception as e:
        return CheckResult("PER_AL_DOCENT_dedicated_mandatory", False,
                           f"Excepció construint build_argumentacio_prompt: {e}")
    low = arg_prompt.lower()
    if "categories obligatòries per a aquest cas" not in low:
        return CheckResult("PER_AL_DOCENT_dedicated_mandatory", False,
                           "Falta el checklist de categories obligatòries del cas")
    n9 = sum(1 for c in _PER_AL_DOCENT_9CAT if c.lower() in low)
    if n9 < 9:
        return CheckResult("PER_AL_DOCENT_dedicated_mandatory", False,
                           f"Falten categories canòniques al prompt dedicat ({n9}/9)")
    # Si nouvingut amb L1 → G obligatòria a la llista del cas.
    chars = case["profile"].get("caracteristiques", {})
    nouv = chars.get("nouvingut", {})
    has_l1 = isinstance(nouv, dict) and (nouv.get("l1") or nouv.get("L1"))
    if has_l1 and "g. personalització lingüística" not in low:
        return CheckResult("PER_AL_DOCENT_dedicated_mandatory", False,
                           "Nouvingut amb L1 però la categoria G no és obligatòria al cas")
    return CheckResult("PER_AL_DOCENT_dedicated_mandatory", True,
                       "Crida dedicada amb 9 cat + checklist obligatori correcte")


# ─── Checks per perfil ────────────────────────────────────────────────────

@check("PERFIL_TILC_si_nouvingut", severity="WARN")
def _c_tilc_nouvingut(case, prompt):
    """Si nouvingut + L1 + MECR baix, hauria d'haver-hi bloc TILC/TOLC."""
    chars = case["profile"]["caracteristiques"]
    nouv = chars.get("nouvingut", {})
    has_l1 = isinstance(nouv, dict) and nouv.get("l1")
    mecr = case["params"].get("mecr_sortida", "")
    if not has_l1 or mecr not in ("pre-A1", "A1", "A2"):
        return CheckResult("PERFIL_TILC_si_nouvingut", True, "Cas no aplica")
    if "tilc" not in prompt.lower() and "tolc" not in prompt.lower() and "transllenguatge" not in prompt.lower():
        return CheckResult("PERFIL_TILC_si_nouvingut", False,
                          "Nouvingut amb L1 + MECR baix però sense bloc TILC/TOLC",
                          severity="WARN")
    return CheckResult("PERFIL_TILC_si_nouvingut", True, "Bloc TILC/TOLC present")


# ─── Runner ────────────────────────────────────────────────────────────────

def build_prompt_for_case(case):
    """Construeix el system prompt complet per a un cas."""
    from adaptation.prompt_builder import build_system_prompt
    return build_system_prompt(
        profile=case["profile"],
        context={
            "etapa": case["params"].get("etapa", "ESO"),
            "materia": "ciències naturals",
        },
        params=case["params"],
        rag_context="",
        adapter_only=True,
    )


def run_checks_for_case(case):
    """Executa tots els checks per a un cas. Retorna llista de CheckResult."""
    try:
        prompt = build_prompt_for_case(case)
    except Exception as e:
        return [CheckResult("PROMPT_BUILD", False, f"Excepció construint prompt: {e}")]
    results = []
    for fn in CHECKS:
        try:
            r = fn(case, prompt)
            results.append(r)
        except Exception as e:
            results.append(CheckResult(fn._name, False,
                                       f"Excepció al check: {e}"))
    return results


def main():
    parser = argparse.ArgumentParser(description="Validador estàtic del prompt")
    parser.add_argument("--case", help="Filtra un sol cas")
    parser.add_argument("--verbose", action="store_true", help="Detall complet")
    args = parser.parse_args()

    cases_yaml = yaml.safe_load((Path(__file__).parent / "cases.yaml").read_text(encoding="utf-8"))
    cases = cases_yaml["casos"]
    if args.case:
        cases = [c for c in cases if c["id"] == args.case]

    print("=" * 80)
    print("CAPA 1.5 — VALIDADOR ESTÀTIC DEL PROMPT")
    print("=" * 80)
    print(f"\nCases: {len(cases)} · Checks per cas: {len(CHECKS)}\n")

    total_pass = 0
    total_fail_err = 0
    total_fail_warn = 0
    case_summary = []

    for case in cases:
        results = run_checks_for_case(case)
        n_pass = sum(1 for r in results if r.passed)
        n_fail_err = sum(1 for r in results if not r.passed and r.severity == "ERROR")
        n_fail_warn = sum(1 for r in results if not r.passed and r.severity == "WARN")
        status = "✅" if n_fail_err == 0 else "❌"
        case_summary.append((case["id"], status, n_pass, n_fail_err, n_fail_warn, results))
        total_pass += n_pass
        total_fail_err += n_fail_err
        total_fail_warn += n_fail_warn

    # Resum
    print(f"{'Cas':30s} | {'Estat':6s} | PASS | ❌ER | ⚠️WR | Fallades destacades")
    print("-" * 100)
    for cid, status, npa, ner, nwr, results in case_summary:
        failed = [r for r in results if not r.passed and r.severity == "ERROR"]
        msg = ", ".join(r.name for r in failed[:3]) if failed else "—"
        if len(failed) > 3:
            msg += f" (+{len(failed)-3} més)"
        print(f"{cid:30s} | {status:6s} | {npa:4d} | {ner:4d} | {nwr:4d} | {msg}")

    print()
    print(f"TOTAL: PASS={total_pass}  ❌ERROR={total_fail_err}  ⚠️WARN={total_fail_warn}")

    # Detall
    if args.verbose or args.case:
        print("\n" + "=" * 80)
        print("DETALL")
        print("=" * 80)
        for cid, status, npa, ner, nwr, results in case_summary:
            print(f"\n── {cid} {status} ──")
            for r in results:
                icon = "✅" if r.passed else ("❌" if r.severity == "ERROR" else "⚠️")
                print(f"  {icon} {r.name}: {r.detail or '(OK)'}")

    sys.exit(0 if total_fail_err == 0 else 1)


if __name__ == "__main__":
    main()
