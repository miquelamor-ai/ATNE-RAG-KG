"""
Prova A/B: brief actual vs brief enriquit amb Gemma 3 + rubrica pedagogica.

Usa la imatge 1 de la prova fotosintesi (la fulla amb raigs de sol) com a
cas. Compara resultat FLUX amb el brief simple (actual) vs el brief enriquit
generat per Gemma 3 donat text original + adaptat + rubrica visual.
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from urllib.parse import quote

import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()
API_KEY = os.getenv("GEMMA4_API_KEY")
if not API_KEY:
    print("ERROR: GEMMA4_API_KEY no trobat", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results_illustrations"
TS = time.strftime("%Y%m%d_%H%M%S")
OUT = RESULTS / f"brief_ab_{TS}"
OUT.mkdir(parents=True, exist_ok=True)

SEED = 42

# Context del concepte
TEXT_ORIGINAL = """La fotosintesi es el proces mitjancant el qual les plantes, les algues i
alguns bacteris transformen l'energia luminosa en energia quimica. Aquest
proces ocorre principalment als cloroplasts de les cel·lules vegetals, on es
troba la clorofil·la, un pigment verd que absorbeix la llum solar.

A la primera etapa (fase luminosa), la clorofil·la capta fotons de la llum
solar. L'energia captada trenca molecules d'aigua (H2O) en hidrogen i oxigen,
alliberant O2 com a subproducte. A la segona etapa (cicle de Calvin),
l'energia acumulada s'utilitza per fixar el CO2 atmosferic i convertir-lo en
glucosa (C6H12O6), que servira d'aliment a la planta."""

TEXT_ADAPTAT = """Les plantes fabriquen el seu propi aliment. Aquest proces s'anomena
fotosintesi. Per fer-la, necessiten tres coses: llum del sol, aigua i dioxid
de carboni. Les fulles capten la llum gracies a la clorofil·la, un pigment
verd."""

# Brief actual (el que va generar la prova de fotosintesi, concepte 1)
BRIEF_ACTUAL = (
    "A single green leaf seen up close on a tree branch, bright sunlight rays "
    "shining on the leaf surface, three-quarter view, warm morning light, "
    "faint outlines of chloroplasts visible as tiny green dots inside the "
    "leaf, no people"
)


RUBRIC_PROMPT = """Ets un dissenyador pedagogic expert en il·lustracio cientifica.
Et donare 3 coses:
1. Un text ORIGINAL (detall tecnic)
2. Un text ADAPTAT (mateix concepte simplificat, amb el MECR de l'alumnat)
3. La part del text on s'ha d'inserir una il·lustracio

IMPORTANT: el model que generara la imatge es FLUX.1-schnell, gratuit pero
amb limitacions:
- NO entén bé conceptes tecnics-microscopics (cel·lules, cloroplasts,
  seccions transversals, atoms, electrons, orbitals, enzims, ribosomes).
- SI entén be conceptes macroscopics (paisatges, objectes, animals,
  edificis, eines, processos visibles) i metafores visuals concretes.
- NO rendera text dins la imatge (tot queda com a gargot).

PROCES OBLIGATORI (passos 1-3 abans d'escriure el brief):

PAS 1 — CLASSIFICA el concepte:
  - "macroscopic" = es pot veure amb ulls humans (arbre, fabrica, cicle)
  - "metaphoric" = tecnic pero admet una metafora visual clara (ex: fulla
    = bateria solar, neurona = xarxa d'autopistes)
  - "technical_micro" = nomes te sentit a nivell microscopic/abstracte
    (cloroplast, ADN, orbital, ATP, enzim catalitzant)

PAS 2 — DECIDEIX: si es "technical_micro" i no trobes una metafora
macroscopica solida, retorna {"skip": true, "reason": "..."} i prou.
Millor CAP imatge que una imatge erronia.

PAS 3 — AJUSTA al nivell MECR/edat:
  - A1-A2: visuals molt concrets, sense detalls tecnics. Max 3 elements.
  - B1-B2: visuals concrets amb alguns detalls tecnics simples.
  - C1-C2: pots incloure diagrames amb mes capes.

Si continues (PAS 4), genera JSON amb aquestes claus:
{
  "classificacio": "macroscopic" | "metaphoric" | "technical_micro",
  "skip": false,
  "reason": "",
  "elements_obligatoris": [...],     // 3-5 elements concrets, rendables
  "relacio_entre_elements": "...",   // com s'articulen
  "emfasi_pedagogic": "...",         // que destaca visualment
  "misconception_a_evitar": "...",   // formulat POSITIVAMENT (mira sota)
  "brief_final_angles": "..."        // 30-60 paraules en angles
}

REGLES DE REDACCIO del brief_final_angles:
- Nomes afirmacions POSITIVES. FLUX-schnell ignora "avoid", "no", "not",
  "without". Si cal evitar X, reformula com "show Y instead" o "emphasize Y".
- Vocabulari visual concret: objectes, llocs, accions, llums, enquadrament.
- NO incloguis estil (watercolor, isometric, flat...). Nomes el QUE es veu.
- Per conceptes "metaphoric", explicita la metafora ("leaf acts like a
  solar battery": show a glowing leaf under sun rays, warm light, no
  cellular detail).

Si skip=true, NO cal omplir els altres camps."""


STYLE_SPINE = (
    "Isometric 3D illustration, 30 degree angle, clean geometric shapes, "
    "crisp edges, limited color palette with soft pastels, subtle shading, "
    "infographic textbook style, high clarity"
)
POSITIVE_SUFFIX = (
    "Single clear focal point, clean composition, soft cream paper background, "
    "no text, no letters, no captions, no signage"
)


def get_enriched_brief() -> dict:
    """Crida a Gemma 3 27B per enriquir el brief."""
    print("  [Gemma3] generant brief enriquit...")
    t0 = time.time()
    client = genai.Client(api_key=API_KEY)
    # Gemma no suporta system_instruction separat -> tot dins contents
    user_msg = (
        f"{RUBRIC_PROMPT}\n\n"
        f"TEXT ORIGINAL:\n{TEXT_ORIGINAL}\n\n"
        f"TEXT ADAPTAT:\n{TEXT_ADAPTAT}\n\n"
        f"PART DEL TEXT ADAPTAT on s'inserira la imatge (concepte a il·lustrar):\n"
        f'"Les fulles capten la llum gracies a la clorofil·la, un pigment verd."\n\n'
        f"Respon nomes amb el JSON."
    )
    resp = client.models.generate_content(
        model="gemma-3-27b-it",
        contents=user_msg,
        config=types.GenerateContentConfig(temperature=0.3),
    )
    import json, re
    text = resp.text.strip()
    # Treu possible ```json ... ``` si Gemma els afegeix
    m = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
    if m:
        text = m.group(1)
    # Busca la primera { ... } balancejada
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if m:
        text = m.group(0)
    data = json.loads(text)
    print(f"  [Gemma3] {time.time()-t0:.1f}s")
    return data


def gen_flux(description: str, label: str) -> bytes | None:
    prompt = f"{STYLE_SPINE}. {description}. {POSITIVE_SUFFIX}."
    url = (
        f"https://image.pollinations.ai/prompt/{quote(prompt)}"
        f"?width=768&height=768&nologo=true&model=flux&seed={SEED}&enhance=false"
    )
    for attempt in range(5):
        try:
            r = requests.get(url, timeout=180)
            if r.status_code in (429, 500, 502, 503):
                wait = 12 * (attempt + 1)
                print(f"  [{label}] {r.status_code}, retry en {wait}s...", file=sys.stderr)
                time.sleep(wait)
                continue
            r.raise_for_status()
            return r.content
        except Exception as e:
            print(f"  [{label}] attempt {attempt+1}: {e}", file=sys.stderr)
            time.sleep(5)
    return None


def main():
    print("[1/3] Obtenint brief enriquit amb Gemma 3...")
    try:
        enriched = get_enriched_brief()
    except Exception as e:
        print(f"  FAIL Gemma: {e}", file=sys.stderr)
        return

    print(f"\n  Elements obligatoris: {enriched.get('elements_obligatoris')}")
    print(f"  Relacio: {enriched.get('relacio_entre_elements')}")
    print(f"  Emfasi: {enriched.get('emfasi_pedagogic')}")
    print(f"  Evitar: {enriched.get('misconception_a_evitar')}")
    print(f"\n  BRIEF FINAL:\n    {enriched.get('brief_final_angles')}\n")

    # Desa el JSON
    import json
    (OUT / "gemma_brief.json").write_text(
        json.dumps(enriched, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print("[2/3] Generant imatge A (brief actual)...")
    img_a = gen_flux(BRIEF_ACTUAL, "brief_actual")
    if img_a:
        (OUT / "a_brief_actual.png").write_bytes(img_a)

    print("[3/3] Generant imatge B (brief enriquit)...")
    img_b = gen_flux(enriched.get("brief_final_angles", BRIEF_ACTUAL), "brief_enriquit")
    if img_b:
        (OUT / "b_brief_enriquit.png").write_bytes(img_b)

    # HTML
    html = f"""<!DOCTYPE html>
<html lang="ca"><head><meta charset="UTF-8">
<title>A/B brief simple vs brief enriquit</title>
<style>
  body {{ font-family: system-ui, sans-serif; max-width: 1400px; margin: 2em auto; padding: 1em; }}
  h1 {{ color: #1a4b7a; }}
  .context {{ background: #f4f4f4; padding: 0.8em; border-radius: 6px; font-size: 0.88em; margin: 0.5em 0; }}
  .cols {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1.5em; margin-top: 1.5em; }}
  .col {{ border: 1px solid #ddd; border-radius: 8px; padding: 1em; }}
  .col h2 {{ margin-top: 0; color: #1a4b7a; }}
  .brief {{ font-size: 0.82em; background: #fffae5; padding: 0.6em; border-radius: 4px; min-height: 6em; }}
  img {{ width: 100%; border-radius: 6px; box-shadow: 0 2px 6px rgba(0,0,0,0.12); }}
  .rubric {{ background: #eaf5ff; padding: 0.8em; border-radius: 6px; font-size: 0.88em; }}
  .rubric ul {{ margin: 0.4em 0; padding-left: 1.2em; }}
</style></head><body>

<h1>A/B — brief simple vs brief enriquit amb Gemma 3</h1>
<p>Concepte: "les fulles capten la llum gracies a la clorofil·la". Estil FLUX idèntic (isomètric), seed 42.</p>

<h3>Text original (referencia)</h3>
<div class="context">{TEXT_ORIGINAL}</div>

<h3>Text adaptat (B1-ESO)</h3>
<div class="context">{TEXT_ADAPTAT}</div>

<h3>Rubrica pedagogica aplicada per Gemma 3</h3>
<div class="rubric">
<strong>Elements obligatoris:</strong>
<ul>{"".join(f"<li>{e}</li>" for e in enriched.get("elements_obligatoris", []))}</ul>
<strong>Relacio entre elements:</strong> {enriched.get("relacio_entre_elements", "-")}<br>
<strong>Emfasi pedagogic:</strong> {enriched.get("emfasi_pedagogic", "-")}<br>
<strong>Misconception a evitar:</strong> {enriched.get("misconception_a_evitar", "-")}
</div>

<div class="cols">
  <div class="col">
    <h2>A. Brief actual (simulat pel LLM adaptador)</h2>
    <div class="brief"><code>{BRIEF_ACTUAL}</code></div>
    <img src="a_brief_actual.png" alt="brief actual">
  </div>
  <div class="col">
    <h2>B. Brief enriquit (Gemma 3 + rubrica)</h2>
    <div class="brief"><code>{enriched.get('brief_final_angles', '')}</code></div>
    <img src="b_brief_enriquit.png" alt="brief enriquit">
  </div>
</div>

</body></html>"""
    (OUT / "report.html").write_text(html, encoding="utf-8")
    print(f"\nObre: {OUT / 'report.html'}")


if __name__ == "__main__":
    main()
