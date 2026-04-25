"""
Afegeix 2 estils a la prova de la fabrica textil:
  - Escala de grisos (dibuix/esbos)
  - Fotografia documental

Mateix subjecte + mateix seed que el test Revolucio Industrial per comparar
directament amb els 5 estils ja generats.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path
from urllib.parse import quote

import requests


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results_illustrations"

SEED = 42

SUBJECT = (
    "the interior of a 19th century textile factory, rows of mechanical looms "
    "powered by steam, a few workers in simple period clothing tending the "
    "machines, warm light filtering through tall windows, waist-up framing, "
    "three-quarter view"
)

POSITIVE_SUFFIX = (
    "single clear focal point, clean composition, "
    "no text, no letters, no captions"
)

EXTRA_STYLES = {
    "06_escala_grisos_carbonet": (
        "monochrome charcoal and graphite drawing, soft grey tones, "
        "hand-drawn on textured cream paper, expressive loose lines, "
        "subtle cross-hatching, high contrast, no color, editorial book "
        "illustration style, dignified historical feel"
    ),
    "07_fotografia_documental": (
        "vintage documentary photograph, warm sepia and amber tones, "
        "35mm film grain, natural soft window light, shallow depth of field, "
        "authentic period atmosphere, editorial photojournalism style, "
        "slight age patina"
    ),
}


def gen(prompt: str, label: str) -> bytes | None:
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
            print(f"  [{label}] error attempt {attempt+1}: {e}", file=sys.stderr)
            time.sleep(5)
    return None


def main():
    # Reutilitza el directori de la prova Revolucio Industrial si existeix
    existing = sorted(RESULTS.glob("revolucio_*"))
    if existing:
        out_dir = existing[-1]
        print(f"Afegint a: {out_dir}")
    else:
        out_dir = RESULTS / f"extra_{time.strftime('%Y%m%d_%H%M%S')}"
        out_dir.mkdir()

    for k, spine in EXTRA_STYLES.items():
        prompt = f"{spine}. {SUBJECT}. {POSITIVE_SUFFIX}."
        print(f"[{k}] generant...")
        img = gen(prompt, k)
        if img:
            (out_dir / f"flux_{k}.png").write_bytes(img)
            print(f"[{k}] OK")
        else:
            print(f"[{k}] FAIL")
        time.sleep(2)

    # Reescriu el report.html afegint les 2 imatges noves
    from glob import glob
    all_flux = sorted(glob(str(out_dir / "flux_*.png")))
    qwen_file = next((f for f in out_dir.glob("qwen_*.webp")), None)

    STYLES_DESC = {
        "01_vectorial_editorial": "Vectorial editorial pla",
        "02_isometric_infografic": "Isometric infografic",
        "03_aquarela_storybook": "Aquarel.la storybook",
        "04_icona_minimalista": "Icona minimalista",
        "05_claymation_plastilina": "Claymation plastilina",
        "06_escala_grisos_carbonet": "Escala grisos - carbonet",
        "07_fotografia_documental": "Fotografia documental",
    }

    blocks = ""
    for f in all_flux:
        name = Path(f).stem.replace("flux_", "")
        title = STYLES_DESC.get(name, name)
        blocks += f'<div class="block"><h3>{title}</h3><img src="{Path(f).name}"><div class="caption">{name}</div></div>'

    qwen_html = ""
    if qwen_file:
        qwen_html = f'<h2>Qwen-Image infografia</h2><img src="{qwen_file.name}">'
    else:
        qwen_html = '<h2>Qwen-Image infografia</h2><div class="err">(pendent, quota esgotada)</div>'

    html = f"""<!DOCTYPE html>
<html lang="ca"><head><meta charset="UTF-8">
<title>Revolucio Industrial - 7 estils</title>
<style>
  body {{ font-family: system-ui, sans-serif; max-width: 1400px; margin: 2em auto; padding: 1em; }}
  h1 {{ color: #1a4b7a; }}
  h2 {{ color: #1a4b7a; border-bottom: 2px solid #e0e0e0; padding-bottom: 0.3em; margin-top: 2em; }}
  .subject {{ background: #f4f4f4; padding: 0.8em; border-radius: 6px; font-size: 0.9em; }}
  .grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.5em; margin-top: 1.5em; }}
  .block {{ border: 1px solid #ddd; border-radius: 8px; padding: 1em; }}
  .block h3 {{ margin-top: 0; color: #1a4b7a; font-size: 1.05em; }}
  .caption {{ font-family: monospace; color: #888; font-size: 0.8em; margin-top: 0.3em; text-align: center; }}
  img {{ width: 100%; border-radius: 6px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }}
  .err {{ color: #b00; padding: 2em; text-align: center; }}
</style></head><body>

<h1>Revolucio Industrial - {len(all_flux)} estils FLUX-schnell</h1>
<p><strong>Subjecte comu</strong> (mateix per a tots, seed={SEED}):</p>
<div class="subject"><code>{SUBJECT}</code></div>
<div class="grid">{blocks}</div>

{qwen_html}

</body></html>"""
    (out_dir / "report.html").write_text(html, encoding="utf-8")
    print(f"\nObre: {out_dir / 'report.html'}")


if __name__ == "__main__":
    main()
