"""
Prova amb text de la Revolucio Industrial:
  - FLUX-schnell x 5 estils per al mateix concepte (fabrica + obrers)
  - Qwen-Image infografia cronologica amb etiquetes en catala

Test d'estres: conceptes sofisticats (humans, maquinaria, historia) que FLUX
trobara mes dificils que "sol + mar".
"""

from __future__ import annotations

import os
import shutil
import sys
import time
from pathlib import Path
from urllib.parse import quote

import requests
from dotenv import load_dotenv
from gradio_client import Client

load_dotenv()
HF_TOKEN = os.getenv("HF_API_TOKEN") or os.getenv("HF_API_KEY")

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results_illustrations"
RESULTS.mkdir(exist_ok=True)

SEED = 42
TS = time.strftime("%Y%m%d_%H%M%S")
OUT = RESULTS / f"revolucio_{TS}"
OUT.mkdir()


# Concepte central per als 5 estils FLUX
FLUX_SUBJECT = (
    "the interior of a 19th century textile factory, rows of mechanical looms "
    "powered by steam, a few workers in simple period clothing tending the "
    "machines, warm light filtering through tall windows, waist-up framing, "
    "three-quarter view"
)

FLUX_POSITIVE_SUFFIX = (
    "single clear focal point, clean composition, soft cream background, "
    "no text, no letters, no captions"
)

FLUX_STYLES = {
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


QWEN_PROMPT = (
    "Educational textbook infographic timeline poster about the Industrial "
    "Revolution with clearly readable labels in Catalan. Large title at the "
    "top: 'LA REVOLUCIO INDUSTRIAL'. Horizontal timeline with four labeled "
    "milestones from left to right: '1769 - MAQUINA DE VAPOR' with a small "
    "steam engine icon, '1807 - VAIXELL DE VAPOR' with a steamboat icon, "
    "'1825 - FERROCARRIL' with a locomotive icon, '1876 - TELEFON' with a "
    "telephone icon. Each milestone has the year and the Catalan label "
    "clearly written. Flat editorial vector illustration, soft pastel palette "
    "of sepia, cream and dusty blue, clean geometric shapes, thin connecting "
    "arrow running along the timeline. Soft cream paper background."
)


def build_flux_prompt(style_spine: str) -> str:
    return f"{style_spine}. {FLUX_SUBJECT}. {FLUX_POSITIVE_SUFFIX}."


def gen_flux_pollinations(prompt: str, label: str) -> bytes | None:
    url = (
        f"https://image.pollinations.ai/prompt/{quote(prompt)}"
        f"?width=768&height=768&nologo=true&model=flux&seed={SEED}&enhance=false"
    )
    for attempt in range(5):
        try:
            r = requests.get(url, timeout=180)
            if r.status_code == 429:
                wait = 12 * (attempt + 1)
                print(f"    [{label}] 429, retry en {wait}s...", file=sys.stderr)
                time.sleep(wait)
                continue
            r.raise_for_status()
            return r.content
        except Exception as e:
            print(f"    [{label}] error attempt {attempt+1}: {e}", file=sys.stderr)
            time.sleep(5)
    return None


def gen_qwen(prompt: str) -> Path | None:
    if not HF_TOKEN:
        print("  QWEN: sense HF_TOKEN", file=sys.stderr)
        return None
    try:
        client = Client("Qwen/Qwen-Image", token=HF_TOKEN, verbose=False)
    except Exception as e:
        print(f"  QWEN: fail connect {e}", file=sys.stderr)
        return None
    for attempt in range(4):
        t0 = time.time()
        try:
            result = client.predict(
                prompt=prompt,
                seed=SEED,
                randomize_seed=False,
                aspect_ratio="16:9",
                guidance_scale=4.0,
                num_inference_steps=30,
                prompt_enhance=False,
                api_name="/infer",
            )
            src = result[0] if isinstance(result, (list, tuple)) else result
            if isinstance(src, dict):
                src = src.get("path") or src.get("url")
            if src and Path(src).exists():
                dst = OUT / "qwen_infografia.webp"
                shutil.copy(src, dst)
                print(f"  QWEN OK ({time.time()-t0:.1f}s) -> {dst}")
                return dst
        except Exception as e:
            err = str(e)
            print(f"  QWEN FAIL attempt {attempt+1} ({time.time()-t0:.1f}s): {err[:150]}", file=sys.stderr)
            if "No GPU" in err and attempt < 3:
                wait = 60 + attempt * 30
                print(f"    esperant {wait}s...", file=sys.stderr)
                time.sleep(wait)
    return None


def main():
    print(f"=== Prova Revolucio Industrial ({TS}) ===\n")
    print(f"Resultats: {OUT}\n")

    # FLUX 5 estils
    print("[FASE 1] FLUX-schnell × 5 estils (Pollinations, seqüencial)")
    print(f"  Subjecte: {FLUX_SUBJECT[:100]}...\n")
    flux_results: dict[str, bytes | None] = {}
    t0 = time.time()
    for k, spine in FLUX_STYLES.items():
        print(f"  [{k}] generant...")
        flux_results[k] = gen_flux_pollinations(build_flux_prompt(spine), k)
        if flux_results[k]:
            (OUT / f"flux_{k}.png").write_bytes(flux_results[k])
            print(f"  [{k}] OK")
        else:
            print(f"  [{k}] FAIL")
        time.sleep(2)
    print(f"  FLUX fase: {time.time()-t0:.1f}s\n")

    # Qwen infografia
    print("[FASE 2] Qwen-Image infografia cronologica amb text catala")
    qwen_path = gen_qwen(QWEN_PROMPT)

    # HTML
    flux_blocks = ""
    for k, spine in FLUX_STYLES.items():
        img = f'<img src="flux_{k}.png">' if flux_results.get(k) else '<div class="err">(error)</div>'
        flux_blocks += f'<div class="block"><h3>{k}</h3><p class="spine">{spine}</p>{img}</div>'

    qwen_block = ""
    if qwen_path and qwen_path.exists():
        qwen_block = f'<img src="{qwen_path.name}" alt="Qwen infografia">'
    else:
        qwen_block = '<div class="err">(Qwen no ha pogut generar - ZeroGPU saturat)</div>'

    html = f"""<!DOCTYPE html>
<html lang="ca"><head><meta charset="UTF-8">
<title>Prova Revolucio Industrial - FLUX vs Qwen</title>
<style>
  body {{ font-family: system-ui, sans-serif; max-width: 1400px; margin: 2em auto; padding: 1em; }}
  h1 {{ color: #1a4b7a; }}
  h2 {{ color: #1a4b7a; border-bottom: 2px solid #e0e0e0; padding-bottom: 0.3em; margin-top: 2em; }}
  .subject {{ background: #f4f4f4; padding: 0.8em; border-radius: 6px; font-size: 0.9em; }}
  .grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.5em; margin-top: 1.5em; }}
  .block {{ border: 1px solid #ddd; border-radius: 8px; padding: 1em; }}
  .block h3 {{ margin-top: 0; font-family: monospace; color: #1a4b7a; }}
  .spine {{ font-size: 0.78em; color: #555; min-height: 4em; }}
  img {{ width: 100%; border-radius: 6px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }}
  .err {{ color: #b00; padding: 3em; text-align: center; }}
  .qwen-prompt {{ font-size: 0.82em; color: #555; background: #f8f8f8; padding: 0.6em; border-radius: 4px; }}
</style></head><body>

<h1>Prova Revolucio Industrial - FLUX-schnell vs Qwen-Image</h1>

<h2>FLUX-schnell x 5 estils (subjecte: fabrica textil amb obrers)</h2>
<p><strong>Subjecte comu</strong> (mateix per a tots, seed={SEED}):</p>
<div class="subject"><code>{FLUX_SUBJECT}</code></div>
<div class="grid">{flux_blocks}</div>

<h2>Qwen-Image: infografia cronologica amb etiquetes en catala</h2>
<p class="qwen-prompt"><code>{QWEN_PROMPT}</code></p>
{qwen_block}

</body></html>"""
    (OUT / "report.html").write_text(html, encoding="utf-8")
    print(f"\nObre: {OUT / 'report.html'}")


if __name__ == "__main__":
    main()
