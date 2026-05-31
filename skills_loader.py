"""Skills loader per a ATNE — llegeix SKILL.md d'una carpeta i els activa segons perfil+params.

Disseny portable (Python avui, reimplementable a PHP Slim4 demà):
- Format fitxer: SKILL.md amb frontmatter YAML + body markdown.
- Triggers declaratius (path + equals/in/exists), no expressions Python.
- Interfície mínima: load_skills(), select_active(), render_skill_block().

Activació:
- Per controlar el rollout, el loader s'invoca NOMÉS si la variable d'entorn
  ATNE_USE_SKILLS val "1", "true" o "yes". Per defecte: OFF (comportament actual).

Slicing per nivell (2026-05-31):
- ATNE_USE_PROMPT_ADAPTER (default ON): si està actiu, el loader també llegeix
  el sibling `prompt_adapter.md` i n'extreu els descriptors per nivell MECR.
  `render_skill_block(skills, mecr=...)` envia llavors NOMÉS la llesca del nivell
  actiu + el preàmbul del SKILL.md (preserva blocs canon condicionals com
  `⚠️ FORMAT BILINGÜE — CONDICIONAL`). Reducció mesurada del prompt: ~50%
  (audits a tests/audit_*.py, 2026-05-31).
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
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
    body: str               # el markdown sense frontmatter (SKILL.md complet)
    # Camps afegits 2026-05-31 per al slicing per nivell:
    preamble: str = ""      # body abans de `## Modulació per nivell` (canon condicional)
    level_descriptors: dict[str, str] = field(default_factory=dict)  # {nivell: bullets text}


# ── Activació global via env var ───────────────────────────────────────

def is_skills_enabled() -> bool:
    """Retorna True si la variable ATNE_USE_SKILLS està activada."""
    return os.getenv("ATNE_USE_SKILLS", "").strip().lower() in ("1", "true", "yes", "on")


def is_prompt_adapter_enabled() -> bool:
    """Retorna True si el slicing per nivell està actiu (default ON 2026-05-31).

    Permet rollback ràpid via env var sense canvi de codi:
      ATNE_USE_PROMPT_ADAPTER=false → torna al comportament anterior (body sencer).
    """
    val = os.getenv("ATNE_USE_PROMPT_ADAPTER", "true").strip().lower()
    return val in ("1", "true", "yes", "on")


# ── Slicing per nivell: parseig del prompt_adapter.md ──────────────────

_PREAMBLE_SPLIT = "## Modulació per nivell"
_NIVELLS_CANONICS = {"pre-A1", "A1", "A2", "B1", "B2", "C1+"}
_NIVELL_ETIQUETA = {
    "pre-A1": "Emergent", "A1": "Inicial", "A2": "Funcional",
    "B1": "Estratègic",   "B2": "Acadèmic", "C1+": "Crític",
}


def _normalize_mecr(mecr: str | None) -> str | None:
    """Normalitza un MECR runtime ('A1', 'PRE-A1', 'C1', 'C2'...) al nivell
    canònic del prompt_adapter ('pre-A1', 'A1', 'A2', 'B1', 'B2', 'C1+').

    Retorna None si el MECR és buit o no normalitzable.
    """
    if not mecr:
        return None
    m = mecr.strip()
    # Variants comunes: "pre-a1", "PRE-A1", "Pre-A1" → "pre-A1"
    m_lower = m.lower()
    if m_lower in ("pre-a1", "prea1"):
        return "pre-A1"
    m_upper = m.upper().replace("Ç", "C")
    if m_upper in ("A1", "A2", "B1", "B2"):
        return m_upper
    if m_upper in ("C1", "C2", "C1+"):
        return "C1+"
    return None


_LEVEL_HEADER_RE = re.compile(
    # Coincideix amb: ### `{{LLISTA_DESCRIPTORS_DEL_NIVELL}}` per a {nivell} ({etiqueta})
    r"^###\s+`?\{\{LLISTA_DESCRIPTORS_DEL_NIVELL\}\}`?\s+per\s+a\s+(\S+)\s*\([^)]+\)\s*$",
    re.MULTILINE | re.IGNORECASE,
)


def _parse_prompt_adapter(text: str) -> dict[str, str]:
    """Parseja un prompt_adapter.md i retorna {nivell_canonic: descriptors_text}.

    Si el fitxer no segueix l'esquema esperat (sense la secció "## Llistes per
    nivell" o sense capçaleres reconeixibles), retorna dict buit i caldrà fer
    fallback al body del SKILL.md.
    """
    if not text:
        return {}
    # Tallem el frontmatter si hi és
    parts = text.split("---", 2)
    body = parts[2] if len(parts) >= 3 else text
    # Trobem totes les capçaleres de nivell amb les seves posicions
    matches = list(_LEVEL_HEADER_RE.finditer(body))
    if not matches:
        return {}
    result: dict[str, str] = {}
    for i, m in enumerate(matches):
        nivell_raw = m.group(1).strip()
        # Normalitzem (el prompt_adapter usa "pre-A1", "A1"... — ja són les claus que volem)
        if nivell_raw not in _NIVELLS_CANONICS:
            # Variant ortogràfica (per exemple "Pre-A1") — provem normalitzar
            norm = _normalize_mecr(nivell_raw)
            if not norm:
                continue
            nivell_raw = norm
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        block = body[start:end].strip()
        result[nivell_raw] = block
    return result


# ── Càrrega ────────────────────────────────────────────────────────────

def load_skills(skills_roots) -> list[Skill]:
    """Escaneja un o més directoris recursivament i retorna els Skill vàlids.

    `skills_roots` pot ser un Path o una llista de Paths. S'escaneja en ordre;
    si un `name` apareix a dos roots, guanya el PRIMER. Des de 2026-05-17 hi ha
    una sola font productiva (corpusFJE/skills/); el paràmetre es manté com a
    llista per si en algun moment cal un overlay de testing.

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
                    # Guanya la primera font (preserva semàntica per overlays).
                    continue
                # BUG bastides deprecated (2026-05-22): exclou skills amb
                # active=false o deprecated=true per evitar instruccions dobles.
                # generate-bastides és substituïda per -lectura i -produccio.
                if fm.get("active") is False or (
                    fm.get("deprecated") is True and fm.get("active") is not True
                ):
                    continue
                seen_names.add(name)
                # Slicing per nivell (2026-05-31): si hi ha sibling prompt_adapter.md,
                # extreiem el preàmbul (canon condicional, per exemple FORMAT BILINGÜE)
                # i el dict de descriptors per nivell. Si no en té, els camps queden
                # buits i el render() farà fallback al body sencer.
                preamble = body.split(_PREAMBLE_SPLIT, 1)[0].rstrip()
                level_descriptors: dict[str, str] = {}
                adapter_path = skill_md.parent / "prompt_adapter.md"
                if adapter_path.exists():
                    try:
                        adapter_text = adapter_path.read_text(encoding="utf-8")
                        level_descriptors = _parse_prompt_adapter(adapter_text)
                    except Exception as _e:
                        print(f"[skills_loader] error parsing prompt_adapter at {adapter_path}: {_e}")
                skills.append(Skill(
                    path=skill_md.parent,
                    name=name,
                    description=str(fm.get("description", "")).strip(),
                    agent_role=fm.get("agent_role", "adapter"),
                    triggers=fm.get("triggers", []) or [],
                    tools_required=fm.get("tools_required", []) or [],
                    frontmatter=fm,
                    body=body,
                    preamble=preamble,
                    level_descriptors=level_descriptors,
                ))
            except Exception as e:
                print(f"[skills_loader] error parsing {skill_md}: {e}")
                continue
    return skills


def default_skills_roots() -> list[Path]:
    """Retorna els directoris on buscar skills.

    Font única (2026-05-17): `corpus/external/corpusFJE/skills/` — submodule
    canònic compartit amb els altres assistents FJE (veure `.gitmodules`).

    Es manté com a llista per si en el futur cal un overlay (testing,
    skills experimentals per branch, etc.).
    """
    here = Path(__file__).resolve().parent
    return [
        here / "corpus" / "external" / "corpusFJE" / "skills",
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
    """Avalua una condició declarativa.

    Suporta:
    - Combinadors (no requereixen path): all_of, any_of, not.
    - Triggers simples (requereixen path): equals, in, not_equals, exists, truthy.

    Els combinadors es poden anidar (un all_of pot contenir any_of, etc.).
    """
    # ── Combinadors ──────────────────────────────────────────────────────
    if "all_of" in trigger:
        subs = trigger["all_of"]
        if not isinstance(subs, list) or not subs:
            return False
        return all(_match_trigger(sub, context) for sub in subs)
    if "any_of" in trigger:
        subs = trigger["any_of"]
        if not isinstance(subs, list) or not subs:
            return False
        return any(_match_trigger(sub, context) for sub in subs)
    if "not" in trigger:
        return not _match_trigger(trigger["not"], context)

    # ── Triggers simples (requereixen path) ──────────────────────────────
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

def render_skill_block(skills: list[Skill], mecr: str | None = None) -> str:
    """Concatena les skills com a bloc únic injectable al prompt.

    Modes:
      - Slicing per nivell (default si mecr donat i ATNE_USE_PROMPT_ADAPTER on):
        envia `preamble` + descriptors NOMÉS del nivell MECR actiu.
        Reducció ~50% vs body sencer (mesurat 2026-05-31). Preserva blocs
        canon condicionals (FORMAT BILINGÜE, etc.) via preamble.
      - Fallback al body sencer si: mecr=None, env flag off, skill sense
        prompt_adapter, o nivell no trobat al dict de descriptors.
    """
    if not skills:
        return ""
    use_slicing = bool(mecr) and is_prompt_adapter_enabled()
    nivell = _normalize_mecr(mecr) if use_slicing else None
    parts = []
    for s in skills:
        header = f"=== SKILL ACTIVA: {s.name.upper()} ==="
        # Intent de slicing per nivell
        if nivell and s.level_descriptors and nivell in s.level_descriptors:
            etiqueta = _NIVELL_ETIQUETA.get(nivell, "")
            label = f"### Criteris per a {nivell}" + (f" ({etiqueta})" if etiqueta else "")
            preamble_part = (s.preamble + "\n\n") if s.preamble else ""
            parts.append(f"{header}\n{preamble_part}{label}\n\n{s.level_descriptors[nivell]}")
        else:
            # Fallback: body sencer (comportament pre-2026-05-31)
            parts.append(f"{header}\n{s.body}")
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
    # Usa els roots per defecte: corpusFJE (font única).
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
