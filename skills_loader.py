"""Skills loader per a ATNE — llegeix SKILL.md d'una carpeta i els activa segons perfil+params.

Disseny portable (Python avui, reimplementable a PHP Slim4 demà):
- Format fitxer: SKILL.md amb frontmatter YAML + body markdown.
- Triggers declaratius (path + equals/in/exists), no expressions Python.
- Interfície mínima: load_skills(), select_active(), render_skill_block().

Activació:
- Per controlar el rollout, el loader s'invoca NOMÉS si la variable d'entorn
  ATNE_USE_SKILLS val "1", "true" o "yes". Per defecte: OFF (comportament actual).
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


# ── Model ──────────────────────────────────────────────────────────────

@dataclass
class Skill:
    path: Path              # carpeta del SKILL.md
    name: str               # identificador únic ("write-noticia")
    description: str        # resum per Tier 1 (taula de contingut)
    agent_role: str         # quin agent la consumeix ("adapter", "complements", "evaluator", "multimodal")
    triggers: list[dict]    # condicions d'activació (OR entre elles)
    tools_required: list[dict]
    frontmatter: dict       # tot el YAML cru per inspecció
    body: str               # el markdown sense frontmatter


# ── Activació global via env var ───────────────────────────────────────

def is_skills_enabled() -> bool:
    """Retorna True si la variable ATNE_USE_SKILLS està activada."""
    return os.getenv("ATNE_USE_SKILLS", "").strip().lower() in ("1", "true", "yes", "on")


# ── Càrrega ────────────────────────────────────────────────────────────

def load_skills(skills_roots) -> list[Skill]:
    """Escaneja un o més directoris recursivament i retorna els Skill vàlids.

    `skills_roots` pot ser un Path o una llista de Paths. S'escaneja en ordre;
    si un `name` apareix a dos roots, guanya el PRIMER (prioritat a la font
    canònica, p.ex. corpusFJE sobre skills_proto local).

    Un SKILL.md ha de començar per `---\n...frontmatter...\n---\nbody`.
    Fitxers mal formats es salten silenciosament (amb print d'avís).
    """
    if isinstance(skills_roots, Path):
        skills_roots = [skills_roots]

    skills: list[Skill] = []
    seen_names: set[str] = set()
    for root in skills_roots:
        if not root.exists():
            continue
        for skill_md in root.rglob("SKILL.md"):
            try:
                content = skill_md.read_text(encoding="utf-8")
                parts = content.split("---", 2)
                if len(parts) < 3:
                    print(f"[skills_loader] ignored (no frontmatter): {skill_md}")
                    continue
                fm = yaml.safe_load(parts[1]) or {}
                body = parts[2].strip()
                name = fm.get("name")
                if not name:
                    print(f"[skills_loader] ignored (no name): {skill_md}")
                    continue
                if name in seen_names:
                    # Guanya la primera font (corpusFJE abans que skills_proto)
                    continue
                seen_names.add(name)
                skills.append(Skill(
                    path=skill_md.parent,
                    name=name,
                    description=str(fm.get("description", "")).strip(),
                    agent_role=fm.get("agent_role", "adapter"),
                    triggers=fm.get("triggers", []) or [],
                    tools_required=fm.get("tools_required", []) or [],
                    frontmatter=fm,
                    body=body,
                ))
            except Exception as e:
                print(f"[skills_loader] error parsing {skill_md}: {e}")
                continue
    return skills


def default_skills_roots() -> list[Path]:
    """Retorna els directoris on buscar skills, en ordre de prioritat.

    1r: `corpus/external/corpusFJE/skills/` — font canònica compartida amb
        els altres assistents FJE (submodule git, veure .gitmodules).
    2n: `corpus/skills_proto/` — contingut local d'ATNE (fallback mentre no
        es migra el contingut a corpusFJE).

    Si un skill amb el mateix `name` apareix a ambdues, guanya corpusFJE.
    """
    here = Path(__file__).resolve().parent
    return [
        here / "corpus" / "external" / "corpusFJE" / "skills",
        here / "corpus" / "skills_proto",
    ]


# ── Triggers ───────────────────────────────────────────────────────────

def _get_nested(obj: Any, path: str) -> Any:
    """Recorre un dict amb notació 'a.b.c'. Retorna None si falta.

    Suporta valors dict, llistes i escalars. Les llistes no es naveguen (retorna None).
    """
    cur = obj
    for part in path.split("."):
        if isinstance(cur, dict):
            cur = cur.get(part)
        else:
            return None
        if cur is None:
            return None
    return cur


def _match_trigger(trigger: dict, context: dict) -> bool:
    """Avalua una condició declarativa. Suporta: equals, in, not_equals, exists, truthy."""
    path = trigger.get("path")
    if not path:
        return False
    value = _get_nested(context, path)
    if "equals" in trigger:
        return value == trigger["equals"]
    if "not_equals" in trigger:
        return value != trigger["not_equals"]
    if "in" in trigger:
        expected = trigger["in"]
        return isinstance(expected, list) and value in expected
    if "exists" in trigger:
        return (value is not None) == bool(trigger["exists"])
    if "truthy" in trigger:
        return bool(value) == bool(trigger["truthy"])
    return False


def _matches_any(triggers: list[dict], context: dict) -> bool:
    """Semàntica OR: la skill s'activa si almenys un trigger matcha."""
    if not triggers:
        return False
    return any(_match_trigger(t, context) for t in triggers)


# ── Selecció ───────────────────────────────────────────────────────────

def select_active(
    skills: list[Skill],
    profile: dict,
    params: dict,
    agent_role: str = "adapter",
) -> list[Skill]:
    """Filtra les skills pel rol d'agent i evalua els seus triggers.

    - skills: llista de totes les skills carregades.
    - profile: dict del perfil (com arriba a build_system_prompt).
    - params: dict dels paràmetres (mecr, dua, complements...).
    - agent_role: quin agent crida la selecció.

    Retorna les skills que compleixen: agent_role coincideix I algun trigger matcha.
    """
    context = {"profile": profile, "params": params}
    return [
        s for s in skills
        if s.agent_role == agent_role and _matches_any(s.triggers, context)
    ]


# ── Renderització ──────────────────────────────────────────────────────

def render_skill_block(skills: list[Skill]) -> str:
    """Concatena els bodies de les skills com a bloc únic injectable al prompt."""
    if not skills:
        return ""
    parts = []
    for s in skills:
        parts.append(f"=== SKILL ACTIVA: {s.name.upper()} ===\n{s.body}")
    return "\n\n".join(parts)


# ── Debug helper ───────────────────────────────────────────────────────

def debug_dump(skills_roots, profile: dict, params: dict, agent_role: str = "adapter"):
    """Imprimeix un resum de les skills actives per a inspecció humana."""
    if isinstance(skills_roots, Path):
        skills_roots = [skills_roots]
    all_skills = load_skills(skills_roots)
    active = select_active(all_skills, profile, params, agent_role=agent_role)
    print(f"[skills_loader] skills_roots: {[str(r) for r in skills_roots]}")
    print(f"[skills_loader] total carregades: {len(all_skills)}")
    print(f"[skills_loader] actives per agent={agent_role}: {len(active)}")
    for s in active:
        rel = str(s.path).replace(str(Path(__file__).resolve().parent), ".")
        print(f"   - {s.name}  (trig={len(s.triggers)})  [{rel}]")
    return active


if __name__ == "__main__":
    # Smoke test amb un perfil TDAH + gènere notícia + glossari.
    # Usa els roots per defecte: corpusFJE primer, skills_proto com a fallback.
    roots = default_skills_roots()
    profile = {
        "caracteristiques": {
            "tdah": {"actiu": True, "grau": "moderat"},
        },
    }
    params = {
        "mecr_sortida": "A2",
        "genere_discursiu": "noticia",
        "complements": {"glossari": True},
    }
    debug_dump(roots, profile, params)
