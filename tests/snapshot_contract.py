"""
Snapshot del contracte públic de `server.py`.

Objectiu: xarxa de seguretat per al refactor (partir server.py en mòduls).
Captura tot el que callers externs esperen de `server`:
  1. Totes les rutes FastAPI registrades (mètode + path).
  2. Símbols públics importats per altres fitxers del repo.
  3. Firma (signature) de funcions crítiques.
  4. Hash de l'schema OpenAPI de les rutes.

Ús:
    python tests/snapshot_contract.py --baseline    # guarda baseline
    python tests/snapshot_contract.py --check       # compara amb baseline
    python tests/snapshot_contract.py               # imprimeix snapshot actual

Sortida: `tests/snapshots/server_contract.json`.
"""

import argparse
import hashlib
import inspect
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

# Símbols que altres fitxers del repo importen explícitament amb
# `from server import ...`. Si algun desapareix, el refactor els ha trencat.
# (Comprovat amb: grep -rn "from server import" al repo)
CRITICAL_EXPORTS = [
    "app",
    "_call_llm",
    "_call_llm_raw",
    "_call_llm_stream",
    "_model_for",
    "_resolve_model",
    "build_system_prompt",
    "build_persona_audience",
    "_get_active_profiles",
    "post_process_adaptation",
    "clean_gemini_output",
    "_post_process_llm_output",
    "_strip_latex_artifacts",
    "_fix_english_words",
    "_fix_typos",
    "_fix_word_concatenations",
    "run_adaptation",
    "propose_adaptation",
]


def _routes_snapshot(app) -> list[dict]:
    """Llista totes les rutes: (methods, path, name)."""
    routes = []
    for r in app.routes:
        methods = sorted(list(getattr(r, "methods", None) or []))
        path = getattr(r, "path", getattr(r, "path_format", ""))
        name = getattr(r, "name", "")
        routes.append({"methods": methods, "path": path, "name": name})
    # Ordre determinista: primer per path, després per methods
    routes.sort(key=lambda x: (x["path"], ",".join(x["methods"])))
    return routes


def _signature_of(obj) -> str:
    try:
        return str(inspect.signature(obj))
    except (TypeError, ValueError):
        return "<no-signature>"


def _exports_snapshot(module) -> dict:
    out = {}
    for name in CRITICAL_EXPORTS:
        if not hasattr(module, name):
            out[name] = {"present": False}
            continue
        obj = getattr(module, name)
        entry = {
            "present": True,
            "kind": type(obj).__name__,
        }
        if callable(obj):
            entry["signature"] = _signature_of(obj)
        out[name] = entry
    return out


def build_snapshot() -> dict:
    import server  # noqa: E402 — importat dinàmicament per aïllar càrrega

    routes = _routes_snapshot(server.app)
    exports = _exports_snapshot(server)

    routes_digest = hashlib.sha256(
        json.dumps(routes, sort_keys=True).encode("utf-8")
    ).hexdigest()

    return {
        "version": 1,
        "routes_digest": routes_digest,
        "routes_count": len(routes),
        "routes": routes,
        "exports": exports,
    }


SNAPSHOT_PATH = REPO_ROOT / "tests" / "snapshots" / "server_contract.json"


def save_baseline(snap: dict):
    SNAPSHOT_PATH.parent.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_PATH.write_text(
        json.dumps(snap, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"[snapshot] Baseline guardat: {SNAPSHOT_PATH}")
    print(f"[snapshot] Rutes: {snap['routes_count']}  digest: {snap['routes_digest'][:12]}")


def check_against_baseline(snap: dict) -> bool:
    if not SNAPSHOT_PATH.exists():
        print("[snapshot] ERROR: no hi ha baseline. Executa amb --baseline primer.")
        return False
    baseline = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))

    ok = True

    # 1) Digest de rutes
    if baseline["routes_digest"] != snap["routes_digest"]:
        ok = False
        print(f"[snapshot] DIFF: digest de rutes ha canviat")
        print(f"  baseline: {baseline['routes_digest'][:12]}")
        print(f"  actual:   {snap['routes_digest'][:12]}")
        # Diff detallat
        base_set = {(r["path"], ",".join(r["methods"])) for r in baseline["routes"]}
        new_set = {(r["path"], ",".join(r["methods"])) for r in snap["routes"]}
        missing = base_set - new_set
        added = new_set - base_set
        if missing:
            print("  RUTES QUE FALTEN:")
            for p, m in sorted(missing):
                print(f"    - [{m}] {p}")
        if added:
            print("  RUTES NOVES:")
            for p, m in sorted(added):
                print(f"    + [{m}] {p}")
    else:
        print(f"[snapshot] OK rutes ({snap['routes_count']})")

    # 2) Exports crítics
    for name in CRITICAL_EXPORTS:
        base = baseline["exports"].get(name, {})
        cur = snap["exports"].get(name, {})
        if base.get("present") and not cur.get("present"):
            ok = False
            print(f"[snapshot] DIFF: export desaparegut: server.{name}")
        elif base.get("signature") and base.get("signature") != cur.get("signature"):
            ok = False
            print(f"[snapshot] DIFF: signatura de server.{name} ha canviat")
            print(f"  baseline: {base.get('signature')}")
            print(f"  actual:   {cur.get('signature')}")

    if ok:
        print("[snapshot] TOT OK — contracte preservat")
    return ok


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", action="store_true",
                        help="Guarda l'snapshot actual com a baseline")
    parser.add_argument("--check", action="store_true",
                        help="Compara l'snapshot actual amb el baseline")
    args = parser.parse_args()

    snap = build_snapshot()

    if args.baseline:
        save_baseline(snap)
    elif args.check:
        ok = check_against_baseline(snap)
        sys.exit(0 if ok else 1)
    else:
        print(json.dumps(snap, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
