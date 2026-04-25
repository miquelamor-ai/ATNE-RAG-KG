"""
Comparativa visual dels 5 estils candidats per a la skill generate-illustracions.

Mateix subjecte + mateixa seed per a tots -> aillar l'efecte de l'estil.
Proveidor: Pollinations.ai (FLUX.1-schnell, gratuit, amb retry).

Estils recerca comunitat 2025-2026:
  1. Vectorial editorial pla
  2. Isometric infografic
  3. Aquarel.la storybook
  4. Icona minimalista
  5. Claymation plastilina
"""

from __future__ import annotations

import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import quote

import requests


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results_illustrations"
RESULTS.mkdir(exist_ok=True)

SEED = 42

SUBJECT = (
    "a warm morning sun shining over a calm sea, "
    "water vapour rising gently from the surface towards the sky, "
    "three-quarter view, eye-level, soft horizon line"
)

POSITIVE_SUFFIX = (
    "single clear focal point, clean composition, "
    "soft cream background, no text, no letters, no captions, no signage"
)

STYLES = {
    "01_vectorial_editorial": (
        "flat vector illustration, clean geometric shapes, bold simple outlines, "
        "limited flat color palette, smooth shapes, friendly editorial style, "
        "no gradients, no texture, centered composition"
    ),
    "02_isometric_infografic": (
        "isometric 3D illustration, 30 degree angle, clean geometric shapes, "
        "crisp edges, limited color palette with soft pastels, subtle shading, "
        "infographic textbook style, high clarity"
    ),
    "03_aquarela_storybook": (
        "soft watercolor storybook illustration, gentle wet-edge washes, "
        "warm palette of ochre sap green and dusty blue, hand-drawn feel, "
        "cozy lighting, loose brushwork, paper texture background, "
        "children book aesthetic"
    ),
    "04_icona_minimalista": (
        "minimalist flat icon, single concept, centered, thick rounded outlines, "
        "two or three flat colors, solid shapes, no gradient, generous padding, "
        "pictogram style, high legibility"
    ),
    "05_claymation_plastilina": (
        "handmade claymation style, stop-motion plasticine figures, "
        "soft studio lighting, visible fingerprint texture, saturated but warm colors, "
        "shallow depth of field, tabletop scene, cheerful children's educational look"
    ),
}


def build_prompt(style_spine: str) -> str:
    return f"{style_spine}. {SUBJECT}. {POSITIVE_SUFFIX}."


def gen_pollinations(prompt: str, label: str) -> bytes | None:
    url = (
        f"https://image.pollinations.ai/prompt/{quote(prompt)}"
        f"?width=768&height=768&nologo=true&model=flux&seed={SEED}&enhance=false"
    )
    for attempt in range(5):
        try:
            r = requests.get(url, timeout=180)
            if r.status_code == 429:
                wait = 12 * (attempt + 1)
                print(f"  [{label}] 429, retry en {wait}s...", file=sys.stderr)
                time.sleep(wait)
                continue
            r.raise_for_status()
            return r.content
        except Exception as e:
            print(f"  [{label}] error (attempt {attempt+1}): {e}", file=sys.stderr)
            time.sleep(8)
    return None


def main():
    ts = time.strftime("%Y%m%d_%H%M%S")
    out_dir = RESULTS / f"styles_{ts}"
    out_dir.mkdir()

    print(f"Generant {len(STYLES)} estils seqüencialment (evita 429)...")
    prompts = {k: build_prompt(v) for k, v in STYLES.items()}

    t0 = time.time()
    results: dict[str, bytes | None] = {}
    for k, p in prompts.items():
        print(f"  [{k}] generant...")
        results[k] = gen_pollinations(p, k)
        status = "OK" if results[k] else "FAIL"
        print(f"  [{k}] {status}")
        time.sleep(2)  # pausa entre crides
    print(f"Fet ({time.time()-t0:.1f}s)")

    for k, img_bytes in results.items():
        if img_bytes:
            (out_dir / f"{k}.png").write_bytes(img_bytes)

    # HTML comparatiu
    blocks = ""
    for k, spine in STYLES.items():
        has_img = results.get(k) is not None
        img_html = f'<img src="{k}.png" alt="{k}">' if has_img else '<div class="err">(error)</div>'
        blocks += f"""
        <div class="block">
          <h3>{k}</h3>
          <p class="spine">{spine}</p>
          {img_html}
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="ca"><head><meta charset="UTF-8">
<title>Comparativa estils FLUX-schnell</title>
<style>
  body {{ font-family: system-ui, sans-serif; max-width: 1400px; margin: 2em auto; padding: 1em; }}
  h1 {{ color: #1a4b7a; }}
  .subject {{ background: #f4f4f4; padding: 0.8em; border-radius: 6px; font-size: 0.9em; }}
  .grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.5em; margin-top: 1.5em; }}
  .block {{ border: 1px solid #ddd; border-radius: 8px; padding: 1em; }}
  .block h3 {{ margin-top: 0; font-family: monospace; color: #1a4b7a; }}
  .spine {{ font-size: 0.8em; color: #555; min-height: 4em; }}
  img {{ width: 100%; border-radius: 6px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }}
  .err {{ color: #b00; padding: 3em; text-align: center; }}
</style></head><body>
<h1>Comparativa d'estils FLUX.1-schnell</h1>
<p><strong>Subjecte comu</strong> (mateix per a tots, seed={SEED}):</p>
<div class="subject"><code>{SUBJECT}</code></div>
<div class="grid">{blocks}</div>
</body></html>"""

    report = out_dir / "report.html"
    report.write_text(html, encoding="utf-8")
    print(f"\nObre: {report}")


if __name__ == "__main__":
    main()
