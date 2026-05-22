"""
Test de la normalització de perfils — BUG-7 (2026-05-22)

Verifica que normalize_profile() converteix correctament els formats
divergents del frontend (Flash, Taller custom) al format canònic del backend.

Format canònic: profile.caracteristiques.X.actiu = True

Execució:
    cd C:\\Users\\miquel.amor\\Documents\\GitHub\\ATNE
    python tests/test_profile_normalization.py
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from server import normalize_profile


def check(label: str, profile_in: dict, expected_chars: dict) -> bool:
    """Compara karakteristiques esperades vs obtingudes. Retorna True si OK."""
    result = normalize_profile(profile_in)
    chars = result.get("caracteristiques", {})
    ok = True
    for key, val in expected_chars.items():
        if key not in chars:
            print(f"  FAIL [{label}] clau '{key}' absent a caracteristiques")
            ok = False
        elif chars[key] != val:
            print(f"  FAIL [{label}] '{key}': esperat {val}, obtingut {chars[key]}")
            ok = False
    if ok:
        print(f"  OK   [{label}]")
    return ok


def test_format_flash_perfils():
    """Cas 1 — Format Flash: profile.perfils = ['nouvingut', 'tdah']"""
    profile = {
        "perfils": ["nouvingut", "tdah"],
        "mecr": "A2",
    }
    return check(
        "Flash: perfils=['nouvingut','tdah']",
        profile,
        {
            "nouvingut": {"actiu": True},
            "tdah": {"actiu": True},
        },
    )


def test_format_taller_caracteristiques():
    """Cas 2 — Format Taller: caracteristiques ja poblades → no tocar res."""
    profile = {
        "caracteristiques": {
            "dislexia": {"actiu": True, "grau": "moderat"},
        },
        "perfils": ["nouvingut"],  # ha de ser ignorat (caracteristiques existeix)
    }
    result = normalize_profile(profile)
    chars = result.get("caracteristiques", {})
    if "nouvingut" in chars:
        print("  FAIL [Taller: chars exist] no hauria d'afegir nouvingut quan chars existeix")
        return False
    if chars.get("dislexia") != {"actiu": True, "grau": "moderat"}:
        print("  FAIL [Taller: chars exist] dislexia modificada incorrectament")
        return False
    print("  OK   [Taller: caracteristiques existent preservades]")
    return True


def test_format_custom_chips():
    """Cas 3 — Format Taller custom: profile.chips = [{'cat': 'tdah'}, {'cat': 'disl'}]"""
    profile = {
        "chips": [{"cat": "tdah"}, {"cat": "disl"}],
    }
    return check(
        "Custom: chips=[tdah, disl]",
        profile,
        {
            "tdah": {"actiu": True},
            "dislexia": {"actiu": True},
        },
    )


def test_nouvingut_l1_top_level():
    """Cas 4 — Nouvingut amb L1 declarada al top level.
    Pilot: 21 nouvinguts tenien l1 al top level → 0/21 generaven glossari bilingüe.
    """
    profile = {
        "perfils": ["nouvingut"],
        "l1": "àrab",
    }
    result = normalize_profile(profile)
    chars = result.get("caracteristiques", {})
    nouv = chars.get("nouvingut", {})
    if not nouv.get("actiu"):
        print("  FAIL [nouvingut+L1] nouvingut.actiu hauria de ser True")
        return False
    if nouv.get("l1") != "àrab":
        print(f"  FAIL [nouvingut+L1] l1 esperat 'arab', obtingut '{nouv.get('l1')}'")
        return False
    print("  OK   [nouvingut+L1 top level => caracteristiques.nouvingut.l1]")
    return True


def test_cat_principal():
    """Cas 5 — profile.cat = 'nouvingut' (categoria principal del perfil)"""
    profile = {"cat": "nouvingut"}
    return check(
        "profile.cat='nouvingut'",
        profile,
        {"nouvingut": {"actiu": True}},
    )


def test_chip_ac_mapping():
    """Cas 6 — chip 'ac' → altes_capacitats"""
    profile = {"chips": [{"cat": "ac"}]}
    return check(
        "chip ac => altes_capacitats",
        profile,
        {"altes_capacitats": {"actiu": True}},
    )


def test_chip_generic_ignorat():
    """Cas 7 — chip 'generic' i 'group' no s'han de mapejar a caracteristiques"""
    profile = {"chips": [{"cat": "generic"}, {"cat": "group"}]}
    result = normalize_profile(profile)
    chars = result.get("caracteristiques", {})
    if "generic" in chars or "group" in chars:
        print("  FAIL [generic/group] no haurien d'aparèixer a caracteristiques")
        return False
    print("  OK   [generic i group ignorats correctament]")
    return True


def test_perfils_original_preservats():
    """Cas 8 — Les claus originals (perfils, chips, cat) es preserven per backwards-compat."""
    profile = {
        "perfils": ["tdah"],
        "chips": [{"cat": "disl"}],
        "cat": "tdah",
        "l1": "xinès",
    }
    result = normalize_profile(profile)
    for key in ("perfils", "chips", "cat", "l1"):
        if key not in result:
            print(f"  FAIL [backwards-compat] clau original '{key}' eliminada")
            return False
    print("  OK   [claus originals preservades per backwards-compat]")
    return True


def test_l1_top_propagada_si_chars_existeix():
    """Cas 9 — Si caracteristiques ja existeix però sense nouvingut.l1, propaga L1."""
    profile = {
        "caracteristiques": {
            "nouvingut": {"actiu": True},
        },
        "l1": "urdú",
    }
    result = normalize_profile(profile)
    chars = result.get("caracteristiques", {})
    if chars.get("nouvingut", {}).get("l1") != "urdú":
        print("  FAIL [L1 propagació] l1 no propagada quan chars ja existeix")
        return False
    print("  OK   [L1 propagada a nouvingut.l1 fins i tot quan chars existeix]")
    return True


def test_flash_casos_pilot():
    """Cas 10 — Simula el format real de Flash tal com enviaven 21 nous al pilot.

    Mostra 'Abans / Despres' de la normalització per als 3 perfils contrastats.
    """
    casos = [
        {
            "label": "Flash nouvingut àrab (pilot real)",
            "in": {"perfils": ["nouvingut"], "l1": "àrab", "mecr": "A1"},
            "expect_chars": {"nouvingut": {"actiu": True, "l1": "àrab"}},
        },
        {
            "label": "Taller custom TDAH+dislèxia",
            "in": {"chips": [{"cat": "tdah"}, {"cat": "disl"}]},
            "expect_chars": {"tdah": {"actiu": True}, "dislexia": {"actiu": True}},
        },
        {
            "label": "Taller canònic (ja en format correcte)",
            "in": {"caracteristiques": {"tea": {"actiu": True, "grau": "lleu"}}},
            "expect_chars": {"tea": {"actiu": True, "grau": "lleu"}},
        },
    ]
    all_ok = True
    for cas in casos:
        result = normalize_profile(cas["in"])
        chars = result.get("caracteristiques", {})
        print(f"\n  [{cas['label']}]")
        print(f"    ENTRADA:  {cas['in']}")
        print(f"    SORTIDA:  {{'caracteristiques': {chars}}}")
        for key, val in cas["expect_chars"].items():
            if key not in chars:
                print(f"    FAIL: clau '{key}' absent")
                all_ok = False
            elif chars[key] != val:
                print(f"    FAIL: '{key}' esperat {val}, obtingut {chars[key]}")
                all_ok = False
        else:
            if all_ok:
                print("    RESULTAT: OK")
    return all_ok


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("TEST: normalize_profile() — BUG-7 fix (2026-05-22)")
    print("=" * 60)

    tests = [
        test_format_flash_perfils,
        test_format_taller_caracteristiques,
        test_format_custom_chips,
        test_nouvingut_l1_top_level,
        test_cat_principal,
        test_chip_ac_mapping,
        test_chip_generic_ignorat,
        test_perfils_original_preservats,
        test_l1_top_propagada_si_chars_existeix,
        test_flash_casos_pilot,
    ]

    passed = 0
    failed = 0
    for t in tests:
        try:
            ok = t()
            if ok:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  ERROR [{t.__name__}]: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"RESULTAT: {passed}/{passed + failed} tests passats")
    if failed == 0:
        print("TOTS ELS TESTS HAN PASSAT [OK]")
    else:
        print(f"FALLES: {failed}")
        sys.exit(1)
