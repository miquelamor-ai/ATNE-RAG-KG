"""
tests/diag_cobertura.py — Diagnostic de cobertura del cataleg d'instruccions.

Objectiu: mesurar quantes instruccions ARRIBEN al prompt per perfil, amb el
DENOMINADOR CORRECTE (instruccions que *poden* aplicar a aquell perfil), no
sobre les 122 totals (que inclouen H-* d'altres perfils que mai han d'arribar).

Per cada perfil canonic mostra:
  - SEMPRE: total / incloses / suprimides (amb ID i motiu)
  - NIVELL: aplicables al MECR / incloses / forats (mecr_detail sense entrada)
  - PERFIL: que apunten a perfils actius / incloses
  - COMPLEMENT: actius / inclosos
  - Cobertura "ingenua" (sobre 122) vs "real" (sobre aplicables)
  - DESTACAT: SEMPRE suprimides per suppress_if_dua (sospita de bug UNE 153101)

Offline, zero crides LLM. Executa: python tests/diag_cobertura.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from instruction_catalog import CATALOG
import instruction_filter

# ── 6 perfils canonics (definicions de tests/golden/cases.yaml) ──────────────
PERFILS = {
    "Viatger (ex_l2) nouvingut": {
        "profile": {"caracteristiques": {"nouvingut": {"actiu": True, "l1": "Àrab", "alfabet_llati": False, "alfabetitzacio_l1": True}}},
        "params": {"mecr_sortida": "A2", "dua": "Accés", "complements": {"glossari": True, "bastides": True, "pictogrames": True}},
    },
    "Marc (marc) tdah": {
        "profile": {"caracteristiques": {"tdah": {"actiu": True}}},
        "params": {"mecr_sortida": "B1", "dua": "Core", "complements": {"glossari": True, "esquema_visual": True, "preguntes_comprensio": True}},
    },
    "Exploradora (ex_aacc) AACC": {
        "profile": {"caracteristiques": {"altes_capacitats": {"actiu": True}}},
        "params": {"mecr_sortida": "B2", "dua": "Enriquiment", "complements": {"glossari": True, "mapa_conceptual": True, "preguntes_comprensio": True, "activitats_aprofundiment": True, "mapa_mental": True, "rubriques": True}},
    },
    "Mireia (mireia) dislexia": {
        "profile": {"caracteristiques": {"dislexia": {"actiu": True}}},
        "params": {"mecr_sortida": "A2", "dua": "Core", "complements": {"glossari": True, "esquema_visual": True, "bastides": True}},
    },
    "Astronom (ex_tea) tea": {
        "profile": {"caracteristiques": {"tea": {"actiu": True}}},
        "params": {"mecr_sortida": "A2", "dua": "Core", "complements": {"glossari": True, "esquema_visual": True, "bastides": True, "pictogrames": True}},
    },
    "Constructora (ex_di) di": {
        "profile": {"caracteristiques": {"di": {"actiu": True, "grau": "moderat"}}},
        "params": {"mecr_sortida": "B1", "dua": "Accés", "complements": {"glossari": True, "esquema_visual": True, "bastides": True, "pictogrames": True}},
    },
}

TOTAL_CATALOG = len(CATALOG)


def classify(cfg):
    """Retorna comptadors de cobertura per a un perfil/params concrets."""
    profile, params = cfg["profile"], cfg["params"]
    mecr = params["mecr_sortida"]
    dua = params["dua"]
    complements = params.get("complements", {})
    chars = profile.get("caracteristiques", {})
    active = [k for k, v in chars.items() if isinstance(v, dict) and v.get("actiu")]

    filtered = instruction_filter.get_instructions(profile, params, context=params)
    included_ids = set()
    for m in filtered["macrodirectives"].values():
        for i in m["instruccions"]:
            included_ids.add(i["id"])

    res = {
        "active": active, "mecr": mecr, "dua": dua,
        "included_ids": included_ids,
        "n_included": len(included_ids),
        "sempre": {"total": 0, "incl": 0, "supr": []},
        "nivell": {"aplicables": 0, "incl": 0, "forats": []},
        "perfil": {"aplicables": 0, "incl": 0},
        "complement": {"actius": 0, "incl": 0},
        "supr_dua": [],  # SEMPRE suprimides per suppress_if_dua (sospita bug)
    }

    for iid, instr in CATALOG.items():
        act = instr["activation"]
        inc = iid in included_ids

        if act == "SEMPRE":
            res["sempre"]["total"] += 1
            if inc:
                res["sempre"]["incl"] += 1
            else:
                # esbrina el motiu
                motiu = "?"
                if dua in instr.get("suppress_if_dua", []):
                    motiu = f"suppress_if_dua={instr['suppress_if_dua']}"
                    res["supr_dua"].append((iid, motiu))
                elif any(p in active for p in instr.get("suppress_if_profile", [])):
                    motiu = f"suppress_if_profile={instr['suppress_if_profile']}"
                elif any(p in active for p in instr.get("suppress_if", [])):
                    motiu = f"suppress_if={instr['suppress_if']}"
                elif "altes_capacitats" in instr.get("suppress_if", []) and dua == "Enriquiment":
                    motiu = "suppress_if=altes_capacitats + DUA Enriquiment"
                res["sempre"]["supr"].append((iid, motiu))

        elif act == "NIVELL":
            # aplicable a aquest MECR?
            aplicable = False
            if "mecr_detail" in instr:
                aplicable = bool(instr["mecr_detail"].get(mecr, ""))
                if not aplicable:
                    # forat: te detail pero no per a aquest nivell
                    res["nivell"]["forats"].append((iid, sorted(instr["mecr_detail"].keys())))
            elif "mecr_levels" in instr:
                aplicable = mecr in instr["mecr_levels"]
            else:
                aplicable = True
            if aplicable:
                res["nivell"]["aplicables"] += 1
                if inc:
                    res["nivell"]["incl"] += 1

        elif act == "PERFIL":
            targets = instr.get("profiles", [])
            if any(p in active for p in targets):
                res["perfil"]["aplicables"] += 1
                if inc:
                    res["perfil"]["incl"] += 1

        elif act == "COMPLEMENT":
            ck = instr.get("complement", "")
            if ck and complements.get(ck):
                res["complement"]["actius"] += 1
                if inc:
                    res["complement"]["incl"] += 1

    aplicables = (res["sempre"]["total"] - len(res["sempre"]["supr"])
                  + res["nivell"]["aplicables"]
                  + res["perfil"]["aplicables"]
                  + res["complement"]["actius"])
    res["aplicables"] = aplicables
    res["cob_ingenua"] = 100.0 * res["n_included"] / TOTAL_CATALOG
    res["cob_real"] = 100.0 * res["n_included"] / aplicables if aplicables else 0.0
    return res


def main():
    print(f"Total instruccions al CATALOG: {TOTAL_CATALOG}\n")
    print("=" * 78)
    for nom, cfg in PERFILS.items():
        r = classify(cfg)
        print(f"\n### {nom}")
        print(f"  Perfils actius: {r['active']} | MECR={r['mecr']} | DUA={r['dua']}")
        print(f"  Instruccions incloses al prompt: {r['n_included']}")
        print(f"  SEMPRE:     {r['sempre']['incl']}/{r['sempre']['total']} incloses "
              f"({len(r['sempre']['supr'])} suprimides)")
        print(f"  NIVELL:     {r['nivell']['incl']}/{r['nivell']['aplicables']} aplicables a {r['mecr']} "
              f"({len(r['nivell']['forats'])} forats mecr_detail)")
        print(f"  PERFIL:     {r['perfil']['incl']}/{r['perfil']['aplicables']} (perfils actius)")
        print(f"  COMPLEMENT: {r['complement']['incl']}/{r['complement']['actius']} (complements actius)")
        print(f"  >> COBERTURA INGENUA (sobre {TOTAL_CATALOG}): {r['cob_ingenua']:.0f}%")
        print(f"  >> COBERTURA REAL (sobre {r['aplicables']} aplicables): {r['cob_real']:.0f}%")
        if r["supr_dua"]:
            print(f"  🔴 SEMPRE suprimides per suppress_if_dua (sospita UNE 153101):")
            for iid, m in r["supr_dua"]:
                print(f"       {iid}: {m}")
        if r["sempre"]["supr"]:
            altres = [(i, m) for i, m in r["sempre"]["supr"] if not any(i == d[0] for d in r["supr_dua"])]
            if altres:
                print(f"  Altres SEMPRE suprimides:")
                for iid, m in altres:
                    print(f"       {iid}: {m}")
        if r["nivell"]["forats"]:
            print(f"  Forats mecr_detail (NIVELL sense entrada per a {r['mecr']}):")
            for iid, keys in r["nivell"]["forats"]:
                print(f"       {iid}: te {keys}")
    print("\n" + "=" * 78)


if __name__ == "__main__":
    main()
