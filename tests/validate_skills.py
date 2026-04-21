"""Validador d'skills — útil per a docents que editen un SKILL.md.

Valida cada SKILL.md del directori corpus/skills_proto/:
- YAML frontmatter parsejable
- Camps obligatoris presents (name, description, agent_role, triggers)
- Triggers ben formats (path + operador conegut)
- Body no buit
- Nom del fitxer coherent amb `name` al frontmatter

Ús:
    python tests/validate_skills.py
    # surt amb codi 0 si tot OK, codi 1 si hi ha errors

Pots afegir-lo a pre-commit o a CI més endavant.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import yaml

SKILLS_ROOT = ROOT / "corpus" / "skills_proto"
REQUIRED_FIELDS = ("name", "description", "agent_role", "triggers")
VALID_AGENT_ROLES = {"adapter", "complements", "evaluator", "multimodal", "generator"}
VALID_TRIGGER_OPS = {"equals", "not_equals", "in", "exists", "truthy"}


def validate_skill(skill_md: Path) -> list[str]:
    """Retorna llista d'errors (buida si tot OK)."""
    errors: list[str] = []
    rel = skill_md.relative_to(ROOT)

    try:
        content = skill_md.read_text(encoding="utf-8")
    except Exception as e:
        return [f"{rel}: no es pot llegir el fitxer ({e})"]

    parts = content.split("---", 2)
    if len(parts) < 3:
        return [f"{rel}: falta el frontmatter YAML (cal '---' al principi i al final)"]

    try:
        fm = yaml.safe_load(parts[1])
    except Exception as e:
        return [f"{rel}: YAML invàlid ({e})"]

    if not isinstance(fm, dict):
        return [f"{rel}: el frontmatter no és un diccionari YAML"]

    # Camps obligatoris
    for field in REQUIRED_FIELDS:
        if field not in fm:
            errors.append(f"{rel}: falta camp obligatori '{field}'")

    # agent_role vàlid
    role = fm.get("agent_role")
    if role and role not in VALID_AGENT_ROLES:
        errors.append(
            f"{rel}: agent_role='{role}' no és vàlid (opcions: {VALID_AGENT_ROLES})"
        )

    # Triggers ben formats
    triggers = fm.get("triggers", []) or []
    if not isinstance(triggers, list):
        errors.append(f"{rel}: triggers ha de ser una llista")
    else:
        for i, t in enumerate(triggers):
            if not isinstance(t, dict):
                errors.append(f"{rel}: trigger #{i} no és un diccionari")
                continue
            if "path" not in t:
                errors.append(f"{rel}: trigger #{i} no té 'path'")
            ops = set(t.keys()) & VALID_TRIGGER_OPS
            if not ops:
                errors.append(
                    f"{rel}: trigger #{i} no té cap operador vàlid "
                    f"(esperat: {VALID_TRIGGER_OPS})"
                )

    # Nom coherent
    name = fm.get("name", "")
    parent = skill_md.parent.name
    if name and name != parent:
        errors.append(
            f"{rel}: name='{name}' no coincideix amb el nom de la carpeta '{parent}'"
        )

    # Body no buit
    body = parts[2].strip()
    if len(body) < 50:
        errors.append(f"{rel}: body molt curt ({len(body)} chars) — probablement buit")

    return errors


def main() -> int:
    if not SKILLS_ROOT.exists():
        print(f"ERROR: no existeix {SKILLS_ROOT}")
        return 1

    all_skills = sorted(SKILLS_ROOT.rglob("SKILL.md"))
    print(f"Validant {len(all_skills)} skills a {SKILLS_ROOT}...\n")

    all_errors: list[str] = []
    for s in all_skills:
        errs = validate_skill(s)
        if errs:
            all_errors.extend(errs)

    if all_errors:
        print(f"[FAIL] {len(all_errors)} error(s) trobats:")
        for e in all_errors:
            print(f"  - {e}")
        return 1

    print(f"[OK] Totes les {len(all_skills)} skills validen correctament.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
