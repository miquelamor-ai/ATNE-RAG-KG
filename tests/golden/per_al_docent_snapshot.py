"""tests/golden/per_al_docent_snapshot.py

Snapshot determinista + guard anti-regressió del coneixement HARDCODED de la secció
«Per al docent» (taxonomia 9 cat A-I + mapeig complement→categoria + lleis del case-block).

PER QUÈ EXISTEIX
Aquest coneixement és pedagògic i ARA viu hardcoded a ATNE (prompt_builder.py), no al
canon (corpusFJE). Viola el principi «ATNE = consumidor, mai origen». Mentre mineriaRAG no
el canonitzi (handoff: docs/handoff_per_al_docent_canon_20260611.md), aquest snapshot
congela el comportament actual com a CONTRACTE byte-a-byte. Quan arribi el derivat JSON del
canon i ATNE refactoritzi per consumir-lo, ha de seguir produint EXACTAMENT aquest snapshot.

Mateix patró que tests/test_complements_matriu.js (matriu R0).

ÚS:
    python tests/golden/per_al_docent_snapshot.py            # valida (deep-equal)
    python tests/golden/per_al_docent_snapshot.py --update   # regenera el snapshot
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from adaptation.prompt_builder import (
    _argumentacio_case_block,
    _comp_to_docent_cat,
    _docent_cat_names,
    _load_per_al_docent_canon,
    _per_al_docent_lleis,
)

SNAPSHOT_PATH = Path(__file__).parent / "per_al_docent_snapshot.json"

# Matriu de perfils golden (cobreix: cada llei del case-block, amb/sense L1, multi-condició).
_GOLDEN_PROFILES = {
    "nouvingut_A2_arab__glos_bast_picto": (
        {"caracteristiques": {"nouvingut": {"actiu": True, "l1": "Àrab"}}},
        {"mecr_sortida": "A2", "complements": {"glossari": True, "bastides": True, "pictogrames": True}}),
    "tdah_dislexia_B1__glos_esq_preg": (
        {"caracteristiques": {"tdah": {"actiu": True}, "dislexia": {"actiu": True}}},
        {"mecr_sortida": "B1", "complements": {"glossari": True, "esquema_visual": True, "preguntes_comprensio": True}}),
    "aacc_B2__mapa_act_rub": (
        {"caracteristiques": {"altes_capacitats": {"actiu": True}}},
        {"mecr_sortida": "B2", "complements": {"mapa_conceptual": True, "activitats_aprofundiment": True, "rubriques": True}}),
    "tea_A2__esq_picto": (
        {"caracteristiques": {"tea": {"actiu": True}}},
        {"mecr_sortida": "A2", "complements": {"esquema_visual": True, "pictogrames": True}}),
    "sense_perfil_B1__glossari": (
        {"caracteristiques": {}},
        {"mecr_sortida": "B1", "complements": {"glossari": True}}),
}


def _mandatory_cats(profile: dict, params: dict) -> list[str]:
    """Extreu els codis de categoria obligatoris del case-block (determinista)."""
    block = _argumentacio_case_block(profile, params)
    return re.findall(r"(?m)^- ([A-I])\.", block)


def build_snapshot() -> dict:
    """Captura el comportament EFECTIU (valors que ATNE consumeix del canon, amb fallback).
    Si el canon canvia (mineriaRAG actualitza per_al_docent.json), aquest snapshot detecta
    el drift → cal revisar i regenerar conscientment."""
    lleis = _per_al_docent_lleis()
    return {
        "_meta": {
            "version": "ATNE-canon-consum-1.0",
            "descripcio": "Contracte de comportament «Per al docent». ATNE CONSUMEIX la "
                          "taxonomia/mapeig/lleis del canon corpusFJE/.tooling/per_al_docent.json "
                          "(fallback hardcoded). Aquest snapshot congela el comportament esperat.",
            "canon_present": _load_per_al_docent_canon() is not None,
        },
        "taxonomia_9cat": dict(_docent_cat_names()),
        "complement_to_categoria": {k: list(v) for k, v in _comp_to_docent_cat().items()},
        "lleis_case_block": {
            "sempre": list(lleis.get("sempre", [])),
            "H_si_perfil_actiu": lleis.get("H_si_perfil_actiu"),
            "I_si_multi_condicio": lleis.get("I_si_multi_condicio"),
            "G_si_L1_declarada": lleis.get("G_si_L1_declarada"),
            "metrica_A_paraules_per_mecr": dict(lleis.get("metrica_A_paraules_per_mecr", {})),
        },
        "contracte_case_block_per_perfil": {
            nom: _mandatory_cats(prof, par) for nom, (prof, par) in _GOLDEN_PROFILES.items()
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--update", action="store_true", help="Regenera el snapshot")
    args = ap.parse_args()

    current = build_snapshot()
    if args.update or not SNAPSHOT_PATH.exists():
        SNAPSHOT_PATH.write_text(json.dumps(current, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[snapshot] escrit a {SNAPSHOT_PATH}")
        return

    saved = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    if saved == current:
        print("[snapshot] OK — el comportament «Per al docent» coincideix amb el contracte.")
        sys.exit(0)
    else:
        print("[snapshot] ❌ DRIFT detectat. El comportament «Per al docent» ha canviat.")
        for k in current:
            if saved.get(k) != current.get(k):
                print(f"  · difereix: {k}")
                print(f"     snapshot: {json.dumps(saved.get(k), ensure_ascii=False)[:300]}")
                print(f"     actual:   {json.dumps(current.get(k), ensure_ascii=False)[:300]}")
        print("\nSi el canvi és INTENCIONAT: python tests/golden/per_al_docent_snapshot.py --update")
        sys.exit(1)


if __name__ == "__main__":
    main()
