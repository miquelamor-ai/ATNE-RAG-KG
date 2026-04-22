"""Smoke test · Pollinations rate-limit amb staggered loads (5s).

Simula el patró de càrrega del Pas 3: 4 imatges FLUX amb el mateix delay
que usa staggerFluxLoads() al pas3.html. Reporta codi HTTP de cadascuna.

Ús:
    python tests/smoke_pollinations_rate.py
Exit 0 si cap 429, exit 1 altrament.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

# Import local sense instal·lar el paquet
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import requests  # noqa: E402

from adaptation.illustrations import build_flux_url  # noqa: E402


CONCEPTS = [
    "cicle de l'aigua",
    "fàbrica tèxtil del segle XIX",
    "fulla verda al sol",
    "muntanya nevada amb riu",
]
STYLE = "aquarela_storybook"
SEED = 42
DELAY_S = 5.0


def probe(idx: int, concept: str) -> tuple[int, float, int]:
    url = build_flux_url(concept, STYLE, SEED + idx)
    t0 = time.time()
    # HEAD no el suporten bé; GET amb stream=True i tanquem.
    r = requests.get(url, stream=True, timeout=120)
    try:
        # Llegeix 1 KB per confirmar que el servidor respon body, no només header.
        next(r.iter_content(chunk_size=1024), b"")
    finally:
        size = int(r.headers.get("Content-Length") or 0)
        r.close()
    dt = time.time() - t0
    return r.status_code, dt, size


def main() -> int:
    print(f"Test Pollinations · {len(CONCEPTS)} imatges · delay {DELAY_S}s")
    results = []
    for i, concept in enumerate(CONCEPTS):
        if i > 0:
            print(f"  ... dormint {DELAY_S}s", flush=True)
            time.sleep(DELAY_S)
        print(f"[{i+1}/{len(CONCEPTS)}] {concept!r}", flush=True)
        try:
            code, dt, size = probe(i, concept)
        except requests.RequestException as e:
            print(f"  !! excepció: {e}")
            results.append((concept, None, 0, 0))
            continue
        tag = "OK" if code == 200 else "RL" if code == 429 else "??"
        print(f"  {tag} HTTP {code} · {dt:.1f}s · {size} bytes")
        results.append((concept, code, dt, size))

    print()
    print("-- Resum ------------------------------------------")
    ok = sum(1 for _, c, *_ in results if c == 200)
    rate = sum(1 for _, c, *_ in results if c == 429)
    err = sum(1 for _, c, *_ in results if c not in (200, 429))
    print(f"OK 200: {ok}/{len(CONCEPTS)}")
    print(f"RL 429 (rate limit): {rate}")
    print(f"?? altres/error: {err}")
    return 0 if rate == 0 and err == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
