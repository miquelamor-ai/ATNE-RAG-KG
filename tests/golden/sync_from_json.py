"""
tests/golden/sync_from_json.py — Sincronitza cases.yaml + golden_texts.yaml des del JSON canon.

Font: ui/atne/data/demo_examples.json
Destins:
  - tests/golden/cases.yaml  (un cas per perfil del JSON)
  - tests/golden/golden_texts.yaml  (un text per text del JSON)

Quan modifiquis el JSON, executa aquest script i el harness queda alineat.
NO modifiquis cases.yaml ni golden_texts.yaml a mà a partir d'ara.

Execució:
    python tests/golden/sync_from_json.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent
JSON_PATH = ROOT / "ui" / "atne" / "data" / "demo_examples.json"

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


# ─── Mappings curts → llargs (frontend → backend canòniques) ──────────────
# Coherent amb CAT_TO_CHAR de ui/atne/js/llm.js (font autoritativa).
CAT_TO_CHAR = {
    "tdah": "tdah",
    "disl": "dislexia",
    "cat": "nouvingut",
    "ac": "altes_capacitats",
    "tea": "tea",
    "di": "di",
    "tdl": "tdl",
    "au": "discapacitat_auditiva",
    "vi": "discapacitat_visual",
    "discalculia": "discalculia",
    "tdc": "dispraxia",
    "vuln": "vulnerabilitat",
    "emo": "emocional",
}


# ─── COURSE_TO_MECR (font: profile-canonical.js) ──────────────────────────
COURSE_TO_MECR = {
    "I3": "pre-A1", "I4": "pre-A1", "I5": "pre-A1",
    "1r Primària": "A1", "2n Primària": "A1",
    "3r Primària": "A1", "4t Primària": "A2",
    "5è Primària": "A2", "6è Primària": "B1",
    "1r ESO": "A2", "2n ESO": "B1", "3r ESO": "B1", "4t ESO": "B2",
    "Batxillerat": "C1",
}


def derive_mecr(course: str) -> str:
    """Deriva MECR del curs amb fallback."""
    # Cerca exacta amb stripping
    c = course.strip()
    if c in COURSE_TO_MECR:
        return COURSE_TO_MECR[c]
    # Cerca per prefix
    for k, v in COURSE_TO_MECR.items():
        if c.startswith(k):
            return v
    return "B1"  # fallback raonable


# ─── Matriu canon (saber-ne+ §7 / pas2.html MATRIU_CONDICIONS) ─────────────
# Per a auto-derivar quins complements activar segons condició.
# Ordre columnes:
#   [gloss, esq, bast, mapaC, preg, aprof, picto, mapaM, plant, resum, cartes, rubr]
COMP_KEYS = [
    "glossari", "esquema_visual", "bastides", "mapa_conceptual",
    "preguntes_comprensio", "activitats_aprofundiment", "pictogrames",
    "mapa_mental", "plantilles_genere", "resum_graduat",
    "cartes_conversacionals", "rubriques",
]
MATRIU_PER_CHAR = {
    "tea":           [1,1,1,0,1,0,1,0,0,0,0,1],
    "tdah":          [1,1,1,0,1,0,0,0,0,0,0,0],
    "dislexia":      [1,1,1,0,1,0,0,0,1,0,0,0],
    "di":            [1,1,1,0,0,0,1,0,1,1,0,0],
    "tdl":           [1,1,1,0,1,0,0,0,1,0,0,0],
    "altes_capacitats":[1,1,0,1,1,1,0,1,0,0,0,1],
    "discapacitat_auditiva":[1,1,1,0,1,0,1,0,0,0,0,0],
    "discapacitat_visual": [1,0,0,0,1,0,0,0,0,0,0,0],
    "dispraxia":     [1,0,0,0,1,0,0,0,0,0,0,0],
    "nouvingut":     [1,1,1,0,1,0,1,0,1,1,0,0],
    "vulnerabilitat":[1,1,1,0,1,0,0,0,0,0,0,0],
    "emocional":     [1,1,1,0,1,0,0,0,0,0,0,0],
    "discalculia":   [1,1,0,0,1,0,0,0,0,0,0,0],  # fallback (no a §7 canònic)
}


def defaults_for_profile(chars: dict) -> dict:
    """Unió de defaults per a totes les condicions actives del perfil."""
    actius = [k for k, v in chars.items() if isinstance(v, dict) and v.get("actiu")]
    comp = {k: False for k in COMP_KEYS}
    for cond in actius:
        row = MATRIU_PER_CHAR.get(cond)
        if not row:
            continue
        for i, val in enumerate(row):
            if val:
                comp[COMP_KEYS[i]] = True
    return {k: True for k, v in comp.items() if v}


def expected_skills_for_case(profile: dict, params: dict) -> list[str]:
    """Reprodueix la lògica del Golden Algorithm per derivar expected_skills."""
    complements = params.get("complements", {})
    skills = set()

    # SKILL write-{genere}
    if params.get("genere_discursiu"):
        skills.add(f"write-{params['genere_discursiu']}")

    # SKILLs generate-{complement} segons triggers
    mapping = {
        "glossari": "generate-glossari",
        "bastides": "generate-bastides-lectura",  # sempre que bastides=true
        "mapa_conceptual": "generate-mapa-conceptual",
        "mapa_mental": "generate-mapa-mental",
        "preguntes_comprensio": "generate-preguntes-comprensio",
        "activitats_aprofundiment": "generate-activitats-aprofundiment",
        "pictogrames": "generate-pictogrames",
        "plantilles_genere": "generate-plantilles-genere",
        "resum_graduat": "generate-resum-graduat",
        "cartes_conversacionals": "generate-cartes-conversacionals",
        "rubriques": "generate-rubriques",
    }
    for k, skill in mapping.items():
        if complements.get(k):
            skills.add(skill)

    # bastides-produccio: AND bastides AMB (preguntes OR activitats)
    if complements.get("bastides") and (
        complements.get("preguntes_comprensio") or complements.get("activitats_aprofundiment")
    ):
        skills.add("generate-bastides-produccio")

    # tolc: auto-activa si nouvingut.l1 declarada
    nouv = profile.get("caracteristiques", {}).get("nouvingut", {})
    if isinstance(nouv, dict) and nouv.get("l1"):
        skills.add("generate-tolc")
    if complements.get("tolc"):
        skills.add("generate-tolc")

    return sorted(skills)


def profile_to_caracteristiques(p: dict) -> dict:
    """Tradueix un perfil del JSON a backend caracteristiques."""
    chars = {}
    cat = p.get("cat")
    if cat == "group":
        # Grup: derivar les condicions dels chips (cat: 'tdah', 'cat', 'tea', etc.)
        for chip in p.get("chips", []):
            ck = chip.get("cat")
            if ck in CAT_TO_CHAR and ck != "lv":
                backend_key = CAT_TO_CHAR[ck]
                chars[backend_key] = {"actiu": True}
    elif cat and cat in CAT_TO_CHAR:
        backend_key = CAT_TO_CHAR[cat]
        chars[backend_key] = {"actiu": True}
        # Aplicar subvariables si existeixen
        sv = p.get("subvariables", {})
        if backend_key in sv:
            chars[backend_key].update(sv[backend_key])
    # Subvariables addicionals (per perfils tipus nouvingut amb l1)
    if "subvariables" in p:
        for k, v in p["subvariables"].items():
            if k in chars:
                chars[k].update(v)
            else:
                # nouvingut a vegades ve com a sub sense ser cat principal
                if k == "nouvingut" and chars.get("nouvingut"):
                    chars["nouvingut"].update(v)
                else:
                    chars[k] = {"actiu": True, **v}
    return chars


def build_case(pid: str, p: dict, genere_default: str = "divulgatiu") -> dict:
    """Construeix un cas del Golden Suite des d'un perfil."""
    chars = profile_to_caracteristiques(p)
    mecr = derive_mecr(p.get("course", ""))
    # DUA: Accés si nivell molt baix o DI; Enriquiment si AC; Core altrament
    dua = "Core"
    if "altes_capacitats" in chars:
        dua = "Enriquiment"
    elif mecr in ("pre-A1",) or "di" in chars or (
        "nouvingut" in chars and chars["nouvingut"].get("alfabet_llati") is False
    ):
        dua = "Accés"
    complements = defaults_for_profile(chars)
    params = {
        "mecr_sortida": mecr,
        "dua": dua,
        "genere_discursiu": genere_default,
        "complements": complements,
    }
    case = {
        "id": pid,
        "descripcio": f"{p.get('name','?')} · {p.get('course','?')} · {p.get('cat','?')}",
        "font_atne": f"ui/atne/data/demo_examples.json (perfils.{pid})",
        "condicions_curtes": [p.get("cat")] if p.get("cat") and p.get("cat") != "group" else [c["cat"] for c in p.get("chips", []) if c.get("cat") != "lv"],
        "profile": {"caracteristiques": chars},
        "params": params,
        "expected_skills": expected_skills_for_case({"caracteristiques": chars}, params),
    }
    return case


def main():
    if not JSON_PATH.exists():
        print(f"ERROR: no trobo {JSON_PATH}")
        sys.exit(2)

    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    perfils = data["perfils"]
    textos = data["textos"]

    # ── cases.yaml ──────────────────────────────────────────────────────
    casos = []
    for pid, p in perfils.items():
        casos.append(build_case(pid, p))

    # Format YAML manualment (sense pyyaml.dump per controlar ordre i strings)
    lines = [
        "# =============================================================================",
        "# tests/golden/cases.yaml — REGENERAT AUTOMÀTICAMENT (v3.0.0)",
        "# =============================================================================",
        "# NO EDITAR A MÀ. Font canon: ui/atne/data/demo_examples.json",
        "# Per regenerar: python tests/golden/sync_from_json.py",
        "# =============================================================================",
        "",
        "meta:",
        '  versio: "3.0.0"',
        '  generat_at: "2026-05-27"',
        '  font: "ui/atne/data/demo_examples.json (perfils)"',
        f'  total_casos: {len(casos)}',
        "",
        "casos:",
        "",
    ]
    for c in casos:
        lines.append(f"  - id: \"{c['id']}\"")
        lines.append(f"    descripcio: \"{c['descripcio']}\"")
        lines.append(f"    font_atne: \"{c['font_atne']}\"")
        cc = c["condicions_curtes"]
        lines.append(f"    condicions_curtes: {json.dumps(cc, ensure_ascii=False)}")
        lines.append("    profile:")
        lines.append("      caracteristiques:")
        chars = c["profile"]["caracteristiques"]
        if not chars:
            lines.append("        {}")
        for ck, cv in chars.items():
            lines.append(f"        {ck}: {json.dumps(cv, ensure_ascii=False)}")
        lines.append("    params:")
        p = c["params"]
        lines.append(f"      mecr_sortida: \"{p['mecr_sortida']}\"")
        lines.append(f"      dua: \"{p['dua']}\"")
        lines.append(f"      genere_discursiu: \"{p['genere_discursiu']}\"")
        lines.append("      complements:")
        for k, v in p["complements"].items():
            lines.append(f"        {k}: {str(v).lower()}")
        lines.append("    expected_skills:")
        for s in c["expected_skills"]:
            lines.append(f"      - {s}")
        lines.append("")

    cases_path = HERE / "cases.yaml"
    cases_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[sync] cases.yaml regenerat amb {len(casos)} casos -> {cases_path}")

    # ── golden_texts.yaml ───────────────────────────────────────────────
    lines = [
        "# =============================================================================",
        "# tests/golden/golden_texts.yaml — REGENERAT AUTOMÀTICAMENT (v3.0.0)",
        "# =============================================================================",
        "# NO EDITAR A MÀ. Font canon: ui/atne/data/demo_examples.json",
        "# Per regenerar: python tests/golden/sync_from_json.py",
        "# =============================================================================",
        "",
        "textos:",
        "",
    ]
    for tid, t in textos.items():
        lines.append(f"  {tid}:")
        lines.append(f"    descripcio: \"{t['descripcio']}\"")
        lines.append(f"    font_atne: \"ui/atne/data/demo_examples.json (textos.{tid})\"")
        lines.append(f"    etapa: \"{t.get('etapa','')}\"")
        lines.append(f"    curs: \"{t.get('curs','')}\"")
        lines.append(f"    fase_lectora: \"{t.get('fase_lectora','')}\"")
        lines.append(f"    mecr_origen: \"{t.get('mecr_origen','')}\"")
        lines.append(f"    genere: \"{t.get('genere','')}\"")
        lines.append(f"    materia: \"{t.get('materia','')}\"")
        lines.append(f"    paraules_aprox: {t.get('paraules_aprox', 0)}")
        # Text com a bloc literal YAML
        lines.append("    text: |")
        for line in t["text"].split("\n"):
            lines.append(f"      {line}")
        lines.append("")

    texts_path = HERE / "golden_texts.yaml"
    texts_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[sync] golden_texts.yaml regenerat amb {len(textos)} textos -> {texts_path}")

    print()
    print("Sincronització completa. Ara executa: python tests/golden/run_golden.py")


if __name__ == "__main__":
    main()
