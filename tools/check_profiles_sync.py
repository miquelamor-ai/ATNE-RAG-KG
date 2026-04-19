#!/usr/bin/env python3
"""Auditoria #2: comprova que ATNE_PROFILES és idèntic als 4 fitxers HTML.

Compara el bloc com a text normalitzat (espais i salts de línia col·lapsats).
Ús: python tools/check_profiles_sync.py
Retorna codi 0 si tot és coherent, 1 si hi ha diferències.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent / "ui" / "atne"
FILES = [
    ROOT / "pas1.html",
    ROOT / "pas1-standalone.html",
    ROOT / "pas2.html",
    ROOT / "pas2-standalone.html",
]


def extract_profiles_block(path: Path) -> str:
    """Extreu el bloc window.ATNE_PROFILES = { ... }; i el normalitza."""
    text = path.read_text(encoding="utf-8")
    m = re.search(r"window\.ATNE_PROFILES\s*=\s*(\{)", text)
    if not m:
        raise ValueError(f"ATNE_PROFILES no trobat a {path.name}")
    start = m.start(1)
    depth = 0
    for i, ch in enumerate(text[start:], start):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                raw = text[start : i + 1]
                # Normalitza: col·lapsa espais múltiples i salts de línia
                return re.sub(r"\s+", " ", raw).strip()
    raise ValueError(f"No s'ha pogut delimitar ATNE_PROFILES a {path.name}")


def extract_profile_ids(block: str) -> list[str]:
    """Extreu els IDs dels perfils del bloc JS (format id:'xxx' o "id":'xxx')."""
    return re.findall(r'\bid\s*:\s*[\'"](\w+)[\'"]', block)


def main() -> int:
    blocks = {}
    errors = []
    for f in FILES:
        try:
            blocks[f.name] = extract_profiles_block(f)
        except ValueError as e:
            errors.append(str(e))

    if errors:
        print("ERRORS D'EXTRACCIÓ:")
        for e in errors:
            print(f"  {e}")
        return 1

    reference_name = FILES[0].name
    reference_block = blocks[reference_name]
    reference_ids = extract_profile_ids(reference_block)
    ok = True

    print(f"Referència: {reference_name} ({len(reference_ids)} perfils: {', '.join(reference_ids)})")

    for name, block in blocks.items():
        if name == reference_name:
            continue
        ids = extract_profile_ids(block)
        if block == reference_block:
            print(f"  OK  {name} — idèntic")
        else:
            ok = False
            # Troba diferències superficials
            if set(ids) != set(reference_ids):
                missing = set(reference_ids) - set(ids)
                extra = set(ids) - set(reference_ids)
                if missing:
                    print(f"  DIFF {name} — FALTEN perfils: {sorted(missing)}")
                if extra:
                    print(f"  DIFF {name} — PERFILS EXTRA: {sorted(extra)}")
            else:
                # Mateixos IDs, contingut diferent — busca quin perfil difereix
                # Extrau cada bloc de perfil per ID
                ref_parts = _split_by_profile(reference_block, reference_ids)
                cur_parts = _split_by_profile(block, ids)
                for pid in reference_ids:
                    rp = ref_parts.get(pid, "")
                    cp = cur_parts.get(pid, "")
                    if rp != cp:
                        print(f"  DIFF {name} — perfil '{pid}' difereix")
                        # Mostra primers 200 chars de cada versió
                        print(f"    ref: {rp[:120]}...")
                        print(f"    cur: {cp[:120]}...")

    if ok:
        print(f"\nOK — tots {len(FILES)} fitxers tenen ATNE_PROFILES idèntic.")
    else:
        print(f"\nKO — hi ha diferències. Actualitza els fitxers amb la versió de {reference_name}.")
    return 0 if ok else 1


def _split_by_profile(block: str, ids: list[str]) -> dict[str, str]:
    """Divideix el bloc per ID de perfil per comparació granular."""
    parts = {}
    for i, pid in enumerate(ids):
        # Cerca id:'marc' o id: 'marc' o id:"marc"
        pat = rf'\bid\s*:\s*[\'\"]{re.escape(pid)}[\'"]'
        m = re.search(pat, block)
        if not m:
            continue
        start = m.start()
        end = len(block)
        if i + 1 < len(ids):
            next_pid = ids[i + 1]
            next_pat = rf'\bid\s*:\s*[\'\"]{re.escape(next_pid)}[\'"]'
            m2 = re.search(next_pat, block[start + 1:])
            if m2:
                end = start + 1 + m2.start()
        parts[pid] = block[start:end].strip()
    return parts


if __name__ == "__main__":
    sys.exit(main())
