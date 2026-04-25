"""Retry scene 2 (infografia amb text catala) amb esperes llargues."""

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

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results_illustrations" / "qwen_scene2_retry"
OUT.mkdir(parents=True, exist_ok=True)

PROMPT = (
    "Educational textbook infographic poster showing the water cycle with "
    "four clearly labeled stages. The labels are written in Catalan in "
    "clean readable typography: 'EVAPORACIO' above the sea with rising "
    "vapour, 'CONDENSACIO' above the clouds, 'PRECIPITACIO' next to the "
    "falling rain, and 'ESCOLAMENT' next to a river flowing back to the "
    "sea. Arrows connect the four stages in a circular flow. "
    "Flat editorial vector illustration, soft pastel palette of blues and "
    "creams, clean geometric shapes, bold outlines, title 'EL CICLE DE "
    "L'AIGUA' at the top in large letters. Soft cream paper background."
)

client = Client("Qwen/Qwen-Image", token=HF_TOKEN, verbose=False)

for attempt in range(8):
    print(f"[attempt {attempt+1}/8] {time.strftime('%H:%M:%S')}")
    t0 = time.time()
    try:
        result = client.predict(
            prompt=PROMPT,
            seed=42,
            randomize_seed=False,
            aspect_ratio="4:3",
            guidance_scale=4.0,
            num_inference_steps=30,
            prompt_enhance=False,
            api_name="/infer",
        )
        src = result[0] if isinstance(result, (list, tuple)) else result
        if isinstance(src, dict):
            src = src.get("path") or src.get("url")
        if src and Path(src).exists():
            dst = OUT / "infografia_catala.webp"
            shutil.copy(src, dst)
            print(f"  OK ({time.time()-t0:.1f}s) -> {dst}")
            break
        print(f"  PROB: {result}", file=sys.stderr)
    except Exception as e:
        err = str(e)
        print(f"  FAIL ({time.time()-t0:.1f}s): {err[:150]}", file=sys.stderr)
        if attempt < 7:
            wait = 60 + attempt * 30  # 60, 90, 120, 150, 180, 210, 240s
            print(f"  esperant {wait}s...", file=sys.stderr)
            time.sleep(wait)
