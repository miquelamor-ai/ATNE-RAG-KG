"""
Prova de generacio d'il.lustracions per a ATNE (iteracio 2).

Canvis respecte iteracio 1:
  - Prompt reforcat amb estil explicit (textbook catala, watercolor pastel).
  - Evitat conflicte "white on white" (fons de color soft, no blanc pur).
  - Proveidor: Pollinations.ai (FLUX schnell, sense clau, amb retry).

HF Inference Providers ja no util: quota gratuita esgotada a tots els routers
(nscale/together/replicate/fal-ai retornen 402 Payment Required).

Flux:
  - Text d'exemple (adaptat LF)
  - Gemini text extreu 3 conceptes visualitzables + prompt en angles amb estil pinat
  - Genera imatges via Pollinations amb seed compartida per consistencia
  - HTML comparatiu
"""

from __future__ import annotations

import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import quote

import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("ERROR: GEMINI_API_KEY no trobat a .env", file=sys.stderr)
    sys.exit(1)


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results_illustrations"
RESULTS.mkdir(exist_ok=True)


SAMPLE_TEXT = """El cicle de l'aigua

L'aigua es mou pel planeta. No es gasta. Canvia de forma.

Primer, el sol escalfa l'aigua del mar. L'aigua es converteix en vapor.
El vapor puja al cel. Aixo es diu evaporacio.

Despres, el vapor es fa fred a dalt. El vapor es converteix en gotes petites.
Les gotes formen els nuvols. Aixo es diu condensacio.

Quan hi ha moltes gotes, cauen a terra. Cauen com pluja, neu o pedra.
Aixo es diu precipitacio.

L'aigua torna als rius. Els rius porten l'aigua al mar. I el cicle comenca de nou."""


STYLE_SUFFIX = (
    "educational illustration in the style of a modern Catalan children's textbook, "
    "warm pastel watercolor palette with cream and soft blue tones, "
    "gentle hand-drawn look, consistent storybook style, visible main subject with "
    "high contrast against a soft colored background (never pure white on white), "
    "friendly rounded shapes, no text, no letters, no labels, "
    "age-appropriate for 8-10 year olds, high pedagogical clarity"
)


def extract_concepts(text: str) -> list[dict]:
    """Demana a Gemini text que identifiqui 3 conceptes visualitzables.

    Retorna: [{"label": str, "illustration_prompt": str}, ...]
    """
    client = genai.Client(api_key=API_KEY)

    system = (
        "Ets un dissenyador pedagogic. Extreu 3 conceptes clau d'un text educatiu "
        "que es beneficiarien d'una il.lustracio. Per a cada un, escriu:\n"
        "- label: etiqueta curta en catala (2-4 paraules)\n"
        "- illustration_prompt: prompt en ANGLES per generar la imatge, descriptiu "
        "pero net, sense text dins la imatge, 1-2 frases maxim.\n\n"
        "Respon nomes amb JSON valid: {\"concepts\": [{\"label\": ..., \"illustration_prompt\": ...}, ...]}"
    )

    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[system, f"\n\nTEXT:\n{text}"],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.3,
        ),
    )
    data = json.loads(resp.text)
    concepts = data["concepts"][:3]
    # Afegim el sufix d'estil al prompt
    for c in concepts:
        c["illustration_prompt"] = f"{c['illustration_prompt']}. Style: {STYLE_SUFFIX}"
    return concepts


DOC_SEED = 42  # mateixa seed per a totes les imatges del mateix document


def gen_pollinations(prompt: str) -> bytes | None:
    """Pollinations.ai FLUX schnell amb retry en 429."""
    url = (
        f"https://image.pollinations.ai/prompt/{quote(prompt)}"
        f"?width=768&height=768&nologo=true&model=flux&seed={DOC_SEED}"
    )
    for attempt in range(4):
        try:
            r = requests.get(url, timeout=180)
            if r.status_code == 429:
                wait = 15 * (attempt + 1)
                print(f"  [Pollinations] 429, retry en {wait}s...", file=sys.stderr)
                time.sleep(wait)
                continue
            r.raise_for_status()
            return r.content
        except Exception as e:
            print(f"  [Pollinations] error (attempt {attempt+1}): {e}", file=sys.stderr)
            time.sleep(5)
    return None


PROVIDERS = {
    "flux_schnell_pollinations": gen_pollinations,
}


def generate_all(concepts: list[dict], out_dir: Path) -> list[dict]:
    """Genera imatges per a tots els conceptes x proveidors en paral.lel."""
    tasks = []
    for i, c in enumerate(concepts):
        for provider_name, fn in PROVIDERS.items():
            tasks.append((i, c, provider_name, fn))

    results: dict[tuple[int, str], bytes | None] = {}
    with ThreadPoolExecutor(max_workers=len(tasks)) as ex:
        futures = {
            ex.submit(fn, c["illustration_prompt"]): (i, provider_name)
            for (i, c, provider_name, fn) in tasks
        }
        for fut in as_completed(futures):
            key = futures[fut]
            try:
                results[key] = fut.result()
            except Exception as e:
                print(f"  [task {key}] error: {e}", file=sys.stderr)
                results[key] = None

    enriched = []
    for i, c in enumerate(concepts):
        entry = {"label": c["label"], "prompt": c["illustration_prompt"], "images": {}}
        for provider_name in PROVIDERS:
            img_bytes = results.get((i, provider_name))
            if img_bytes:
                fname = f"{i:02d}_{provider_name}.png"
                (out_dir / fname).write_bytes(img_bytes)
                entry["images"][provider_name] = fname
            else:
                entry["images"][provider_name] = None
        enriched.append(entry)
    return enriched


def build_html_report(text: str, entries: list[dict], out_dir: Path) -> Path:
    """HTML comparatiu."""
    rows = ""
    for e in entries:
        cells = ""
        for provider_name in PROVIDERS:
            fname = e["images"].get(provider_name)
            if fname:
                cells += f'<td><img src="{fname}" alt="{provider_name}"><div class="caption">{provider_name}</div></td>'
            else:
                cells += f'<td class="err">(error {provider_name})</td>'
        rows += f"""
        <div class="block">
          <h3>{e['label']}</h3>
          <p class="prompt"><code>{e['prompt']}</code></p>
          <table><tr>{cells}</tr></table>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="UTF-8">
<title>Prova il.lustracions ATNE</title>
<style>
  body {{ font-family: system-ui, sans-serif; max-width: 1400px; margin: 2em auto; padding: 1em; }}
  h1 {{ color: #1a4b7a; }}
  .text {{ background: #f4f4f4; padding: 1em; border-radius: 6px; white-space: pre-wrap; }}
  .block {{ margin: 2em 0; border-top: 1px solid #ddd; padding-top: 1em; }}
  .prompt {{ font-size: 0.85em; color: #555; }}
  table {{ width: 100%; border-collapse: collapse; }}
  td {{ padding: 0.5em; text-align: center; vertical-align: top; }}
  img {{ max-width: 100%; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.15); }}
  .caption {{ margin-top: 0.5em; font-family: monospace; font-size: 0.9em; color: #666; }}
  .err {{ color: #b00; }}
</style>
</head>
<body>
<h1>Prova il.lustracions ATNE</h1>
<h2>Text font</h2>
<div class="text">{text}</div>
<h2>Il.lustracions generades</h2>
{rows}
</body>
</html>"""

    report = out_dir / "report.html"
    report.write_text(html, encoding="utf-8")
    return report


def main():
    ts = time.strftime("%Y%m%d_%H%M%S")
    out_dir = RESULTS / ts
    out_dir.mkdir()

    print(f"[1/3] Extraient conceptes amb Gemini...")
    t0 = time.time()
    concepts = extract_concepts(SAMPLE_TEXT)
    print(f"      {len(concepts)} conceptes ({time.time()-t0:.1f}s)")
    for c in concepts:
        print(f"      - {c['label']}")

    print(f"[2/3] Generant imatges ({len(concepts)} conceptes x {len(PROVIDERS)} proveidors)...")
    t0 = time.time()
    entries = generate_all(concepts, out_dir)
    print(f"      fet ({time.time()-t0:.1f}s)")

    print(f"[3/3] Construint HTML comparatiu...")
    report = build_html_report(SAMPLE_TEXT, entries, out_dir)
    print(f"\nOK. Obre: {report}")


if __name__ == "__main__":
    main()
