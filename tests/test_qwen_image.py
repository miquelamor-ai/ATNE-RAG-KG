"""
Prova de Qwen-Image via HuggingFace Space oficial (Qwen/Qwen-Image).

Dos escenaris:
  1. Mateix subjecte que les proves FLUX (sol + mar + vapor) per comparativa directa.
  2. Infografia amb text en catala DINS la imatge (l'avantatge real de Qwen-Image).

Sense API key. Via gradio_client. Cua compartida -> pot trigar 30-120s per imatge.
"""

from __future__ import annotations

import os
import shutil
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from gradio_client import Client

load_dotenv()
HF_TOKEN = os.getenv("HF_API_TOKEN") or os.getenv("HF_API_KEY")
if not HF_TOKEN:
    print("ERROR: HF_API_TOKEN no trobat a .env", file=sys.stderr)
    sys.exit(1)


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results_illustrations"
RESULTS.mkdir(exist_ok=True)


STYLE_SPINE = (
    "soft watercolor storybook illustration, gentle wet-edge washes, "
    "warm palette of ochre sap green and dusty blue, hand-drawn feel, "
    "cozy lighting, loose brushwork, paper texture background, "
    "children book aesthetic"
)

POSITIVE_SUFFIX = (
    "single clear focal point, clean composition, "
    "soft cream background"
)

SCENES = {
    "01_sense_text": {
        "description": "Escena d'evaporacio (mateix subjecte que les proves FLUX)",
        "prompt": (
            f"{STYLE_SPINE}. A warm morning sun shining over a calm sea, "
            f"water vapour rising gently from the surface towards the sky, "
            f"three-quarter view, eye-level, soft horizon line. "
            f"{POSITIVE_SUFFIX}. No text, no letters."
        ),
    },
    "02_infografia_catala": {
        "description": "Infografia del cicle de l'aigua amb etiquetes en catala",
        "prompt": (
            "Educational textbook infographic poster showing the water cycle with "
            "four clearly labeled stages. The labels are written in Catalan in "
            "clean readable typography: 'EVAPORACIO' above the sea with rising "
            "vapour, 'CONDENSACIO' above the clouds, 'PRECIPITACIO' next to the "
            "falling rain, and 'ESCOLAMENT' next to a river flowing back to the "
            "sea. Arrows connect the four stages in a circular flow. "
            "Flat editorial vector illustration, soft pastel palette of blues and "
            "creams, clean geometric shapes, bold outlines, title 'EL CICLE DE "
            "L'AIGUA' at the top in large letters. Soft cream paper background."
        ),
    },
}


def main():
    ts = time.strftime("%Y%m%d_%H%M%S")
    out_dir = RESULTS / f"qwen_{ts}"
    out_dir.mkdir()

    print("Connectant a HuggingFace Space Qwen/Qwen-Image (autenticat)...")
    client = Client("Qwen/Qwen-Image", token=HF_TOKEN, verbose=False)
    print("  OK connectat.\n")

    for key, scene in SCENES.items():
        print(f"[{key}] {scene['description']}")
        print(f"  prompt: {scene['prompt'][:100]}...")
        t0 = time.time()
        # 3 intents per escena si falla per "No GPU"
        for attempt in range(3):
            try:
                result = client.predict(
                    prompt=scene["prompt"],
                    seed=42,
                    randomize_seed=False,
                    aspect_ratio="4:3",
                    guidance_scale=4.0,
                    num_inference_steps=30,
                    prompt_enhance=False,
                    api_name="/infer",
                )
                elapsed = time.time() - t0
                print(f"  DEBUG result type={type(result).__name__}")
                image_info = result[0] if isinstance(result, (list, tuple)) else result
                print(f"  DEBUG image_info={image_info}")
                # gradio_client pot retornar: dict amb path | str path directe | URL
                src_path = None
                if isinstance(image_info, dict):
                    src_path = image_info.get("path") or image_info.get("url")
                elif isinstance(image_info, str):
                    src_path = image_info
                dst = out_dir / f"{key}.png"
                if src_path and Path(src_path).exists():
                    shutil.copy(src_path, dst)
                    print(f"  OK ({elapsed:.1f}s) -> {dst}")
                    break
                elif src_path and src_path.startswith("http"):
                    import requests
                    r = requests.get(src_path, timeout=60)
                    dst.write_bytes(r.content)
                    print(f"  OK via URL ({elapsed:.1f}s) -> {dst}")
                    break
                else:
                    print(f"  PROB: path invalid ({src_path}). result={result}", file=sys.stderr)
                    break
            except Exception as e:
                err = str(e)
                print(f"  FAIL attempt {attempt+1} ({time.time()-t0:.1f}s): {err[:200]}", file=sys.stderr)
                if "No GPU was available" in err and attempt < 2:
                    print(f"  ZeroGPU saturat, esperant 30s i reintentant...", file=sys.stderr)
                    time.sleep(30)
                    t0 = time.time()
                    continue
                break

    # HTML comparatiu
    blocks = ""
    for key, scene in SCENES.items():
        img = f'<img src="{key}.png">' if (out_dir / f"{key}.png").exists() else '<div class="err">(error)</div>'
        blocks += f"""
        <div class="block">
          <h3>{key} — {scene['description']}</h3>
          <p class="prompt"><code>{scene['prompt']}</code></p>
          {img}
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="ca"><head><meta charset="UTF-8">
<title>Qwen-Image test</title>
<style>
  body {{ font-family: system-ui, sans-serif; max-width: 1200px; margin: 2em auto; padding: 1em; }}
  h1 {{ color: #1a4b7a; }}
  .block {{ margin: 2em 0; border-top: 1px solid #ddd; padding-top: 1em; }}
  .prompt {{ font-size: 0.85em; color: #555; background: #f8f8f8; padding: 0.6em; border-radius: 4px; }}
  img {{ max-width: 100%; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.15); }}
  .err {{ color: #b00; padding: 2em; text-align: center; }}
</style></head><body>
<h1>Qwen-Image (HF Space oficial) — proves</h1>
{blocks}
</body></html>"""
    (out_dir / "report.html").write_text(html, encoding="utf-8")
    print(f"\nObre: {out_dir / 'report.html'}")


if __name__ == "__main__":
    main()
