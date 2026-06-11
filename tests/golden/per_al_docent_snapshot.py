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
    _ARGUMENTACIO_9CAT_BLOCK,
    _COMP_TO_DOCENT_CAT,
    _DOCENT_CAT_NAMES,
    _argumentacio_case_block,
)
from adaptation.post_process import MECR_MAX_WORDS

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
    return {
        "_meta": {
            "version": "ATNE-handoff-1.0",
            "descripcio": "Dump determinista del coneixement «Per al docent» hardcoded a ATNE "
                          "(prompt_builder.py). Per a canonització a mineriaRAG. ATNE el consumirà "
                          "com a derivat quan existeixi. NO és canon.",
            "origen": "adaptation/prompt_builder.py",
        },
        "taxonomia_9cat": dict(_DOCENT_CAT_NAMES),
        "complement_to_categoria": {k: list(v) for k, v in _COMP_TO_DOCENT_CAT.items()},
        "lleis_case_block": {
            "sempre": ["A", "B", "E"],
            "H_si_perfil_actiu": True,
            "I_si_multi_condicio": True,
            "G_si_L1_declarada": True,
            "metrica_A_paraules_per_mecr": dict(MECR_MAX_WORDS),
        },
        "contracte_case_block_per_perfil": {
            nom: _mandatory_cats(prof, par) for nom, (prof, par) in _GOLDEN_PROFILES.items()
        },
        "taxonomia_text_len": len(_ARGUMENTACIO_9CAT_BLOCK),
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
