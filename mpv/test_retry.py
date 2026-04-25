# Reintent dels casos fallits del test complet
# Execució: python mpv/test_retry.py

import json
import os
import sys
import time
from pathlib import Path

env_path = Path(__file__).parent / ".env"
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).parent))

from server_mpv import build_system_prompt, resolve_nivell, _call_gemma
from test_complet import TEXT_B1, AVALUACIONS

OUT = Path(__file__).parent / "resultats" / "complet_20260423_232822"

CASOS_A = {c["tag"]: c for c in AVALUACIONS[0]["casos"]}
NIVELL_A = resolve_nivell("eso_12", "simplificat")

FALLITS = [
    ("gemma-4-31b-it", "grup"),
    ("gemma-4-31b-it", "tdah"),
    ("gemma-4-31b-it", "tea"),
    ("gemma-4-31b-it", "tdah_glossari"),
]

print(f"\n{'='*55}")
print(f"  Reintent {len(FALLITS)} casos Gemma 4 MVP")
print(f"{'='*55}\n")

ok = 0
for model_id, tag in FALLITS:
    cas = CASOS_A[tag]
    print(f"  {model_id} · {tag} ...", end=" ", flush=True)
    t0 = time.time()
    try:
        sp = build_system_prompt(NIVELL_A, cas["perfils_mvp"], cas["comp_mvp"])
        result = _call_gemma(model_id, sp, TEXT_B1)
        elapsed = round(time.time() - t0, 1)
        print(f"OK {elapsed}s")
        safe = model_id.replace("-", "_").replace(".", "_")
        fname = f"A_{safe}_{tag}_MVP.md"
        (OUT / fname).write_text(
            f"# {model_id} · A · {tag} · MVP\n\n"
            f"**Nivell:** {NIVELL_A} | **Curs:** eso_12 | **Adaptació:** simplificat\n"
            f"**Perfils:** {cas['perfils_mvp'] or 'cap'} | **Complements:** {cas['comp_mvp'] or 'cap'}\n\n"
            f"---\n\n{result}\n\n"
            f"---\n\n<details><summary>Prompt enviat</summary>\n\n```\n{sp}\n```\n</details>\n",
            encoding="utf-8"
        )
        ok += 1
    except Exception as e:
        elapsed = round(time.time() - t0, 1)
        print(f"ERR {elapsed}s — {e}")
    time.sleep(2)

print(f"\n  Resultat: {ok}/{len(FALLITS)} correctes")
print(f"  Fitxers a: {OUT}\n")
