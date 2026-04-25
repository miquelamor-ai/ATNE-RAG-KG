"""
Tercera prova: simulacio end-to-end d'un document adaptat amb il·lustracions.

Text: Fotosintesi (adaptat nivell B1-ESO).
Estil: isometric_infografic (preset per defecte per STEM segons la skill).
Genera 3 il·lustracions inline per simular com quedaria un document real.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path
from urllib.parse import quote

import requests


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results_illustrations"
RESULTS.mkdir(exist_ok=True)
TS = time.strftime("%Y%m%d_%H%M%S")
OUT = RESULTS / f"fotosintesi_{TS}"
OUT.mkdir()
SEED = 42

# Estil isometric_infografic (frontmatter de la skill)
STYLE_SPINE = (
    "Isometric 3D illustration, 30 degree angle, clean geometric shapes, "
    "crisp edges, limited color palette with soft pastels, subtle shading, "
    "infographic textbook style, high clarity"
)

POSITIVE_SUFFIX = (
    "Single clear focal point, clean composition, "
    "soft cream paper background, "
    "no text, no letters, no captions, no signage"
)

# Text adaptat (B1-ESO) amb 3 marcadors ja col·locats per simular la sortida del LLM
ADAPTED_TEXT = """### La fotosintesi

Les plantes fabriquen el seu propi aliment. Aquest proces s'anomena **fotosintesi**.

[IMATGE: A single green leaf seen up close on a tree branch, bright sunlight rays shining on the leaf surface, three-quarter view, warm morning light, faint outlines of chloroplasts visible as tiny green dots inside the leaf, no people]

Per fer la fotosintesi, les plantes necessiten tres coses: **llum del sol**, **aigua** i **dioxid de carboni**. Les fulles capten la llum gracies a la clorofil·la, un pigment verd.

[IMATGE: A stylized scene showing a tree with roots absorbing water from the ground (blue arrows pointing up through the trunk) and leaves absorbing carbon dioxide from the air (grey arrows pointing toward the leaves), clear educational diagram style, three-quarter view]

Despres de rebre aquests tres elements, la planta produeix dues substancies: **glucosa** (el seu aliment) i **oxigen**. L'oxigen surt per les fulles i el respirem nosaltres.

[IMATGE: A green leaf releasing small white bubbles of oxygen into the air on its upper side, while a small abstract glucose molecule symbol glows gently inside the leaf, three-quarter view, bright daylight, clean educational infographic style]

Gracies a la fotosintesi, les plantes donen oxigen al planeta. Sense plantes, no podriem respirar."""


def extract_markers(text: str):
    """Parser simple del marcador [IMATGE: ...]. Retorna (posicio, descripcio)."""
    import re
    markers = []
    for m in re.finditer(r"\[IMATGE:\s*([^\]]+)\]", text):
        markers.append((m.start(), m.end(), m.group(1).strip()))
    return markers


def gen_image(prompt: str, label: str) -> bytes | None:
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
    markers = extract_markers(ADAPTED_TEXT)
    print(f"Trobats {len(markers)} marcadors al text adaptat.\n")

    # Generar cada imatge
    images = {}
    for i, (_, _, desc) in enumerate(markers):
        print(f"[{i+1}/{len(markers)}] generant...")
        print(f"  concepte: {desc[:80]}...")
        full_prompt = f"{STYLE_SPINE}. {desc}. {POSITIVE_SUFFIX}."
        img = gen_image(full_prompt, f"img_{i+1}")
        if img:
            fname = f"img_{i+1}.png"
            (OUT / fname).write_bytes(img)
            images[i] = fname
            print(f"  OK -> {fname}")
        else:
            print(f"  FAIL")
        time.sleep(2)

    # Render HTML simulant el document final (text + imatges inline substituint marcadors)
    rendered = ADAPTED_TEXT
    # Reemplacem en ordre invers per no invalidar offsets
    for i in reversed(range(len(markers))):
        start, end, desc = markers[i]
        if i in images:
            img_html = (
                f'<figure class="img-illus">'
                f'<img src="{images[i]}" alt="{desc[:80]}...">'
                f'<figcaption>{desc[:120]}</figcaption>'
                f'</figure>'
            )
        else:
            img_html = f'<div class="err">(imatge no generada)</div>'
        rendered = rendered[:start] + img_html + rendered[end:]

    # Conversio markdown basica (### -> h3, ** ** -> strong, parrafs)
    import re
    def md_to_html(text):
        text = re.sub(r"### (.+)", r"<h3>\1</h3>", text)
        text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
        # parrafs: separar per doble salt de linia
        parts = text.split("\n\n")
        out = []
        for p in parts:
            p = p.strip()
            if not p:
                continue
            if p.startswith("<h3") or p.startswith("<figure") or p.startswith("<div"):
                out.append(p)
            else:
                out.append(f"<p>{p}</p>")
        return "\n".join(out)

    body = md_to_html(rendered)

    html = f"""<!DOCTYPE html>
<html lang="ca"><head><meta charset="UTF-8">
<title>Fotosintesi - simulacio final</title>
<style>
  body {{ font-family: Georgia, serif; max-width: 800px; margin: 2em auto; padding: 2em; background: #fbf8f2; color: #2a2a2a; line-height: 1.7; }}
  h3 {{ color: #1a4b7a; border-bottom: 2px solid #d4c895; padding-bottom: 0.3em; }}
  .img-illus {{ margin: 1.5em auto; text-align: center; }}
  .img-illus img {{ max-width: 100%; border-radius: 8px; box-shadow: 0 3px 10px rgba(0,0,0,0.12); }}
  .img-illus figcaption {{ font-size: 0.82em; color: #777; font-style: italic; margin-top: 0.5em; }}
  strong {{ color: #1a4b7a; }}
  .meta {{ background: #fff; border-left: 4px solid #1a4b7a; padding: 0.7em 1em; margin-bottom: 2em; font-size: 0.88em; }}
  .err {{ color: #b00; padding: 2em; text-align: center; border: 1px dashed #b00; }}
</style></head><body>

<div class="meta">
<strong>Simulacio end-to-end</strong> de com quedaria un text adaptat per ATNE amb
il·lustracions integrades. Estil: <code>isometric_infografic</code> (preset per
STEM). 3 marcadors processats automaticament.
</div>

{body}

</body></html>"""
    (OUT / "document.html").write_text(html, encoding="utf-8")
    print(f"\nObre: {OUT / 'document.html'}")


if __name__ == "__main__":
    main()
