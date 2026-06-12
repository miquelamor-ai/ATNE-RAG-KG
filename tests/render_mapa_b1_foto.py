"""Renderitza un mapa conceptual B1 (branques = verbs d'enllaç, proposició Novak)
amb el renderitzador REAL d'ATNE (ui/atne/js/mermaid-converter.js, buildConceptMap)
i en desa una foto PNG. Verificació visual del canon v4.1.0 (graduació de branca per
MECR) — punt 5 del follow-up. La foto és material per ensenyar al DOP què fa l'eina.

Ús:  python tests/render_mapa_b1_foto.py
Surt: docs/mapa_conceptual_b1_verbal.png
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
CONVERTER = (ROOT / "ui" / "atne" / "js" / "mermaid-converter.js").read_text(encoding="utf-8")

# Mapa B1 representatiu: el cas de producció del handoff (Revolució Industrial), amb
# branques = verbs d'enllaç. Cada branca forma una proposició Novak llegible amb l'arrel:
#   «La Revolució Industrial ÉS PROVOCADA PER la màquina de vapor».
MAPA_B1 = """## Mapa conceptual

- **La Revolució Industrial**
  - **és provocada per**
    - la màquina de vapor
    - el carbó com a combustible
  - **provoca**
    - el creixement de les fàbriques
    - l'èxode cap a les ciutats
  - **es divideix en**
    - primera revolució (1760)
    - segona revolució (1870)
"""

# Mateix contingut a A2: branques = noms de categoria (bastida classificatòria).
# Il·lustra la graduació del canon v4.1.0 (A2 agrupa, B1+ explicita la relació).
MAPA_A2 = """## Mapa conceptual

- **La Revolució Industrial**
  - **Causes**
    - la màquina de vapor
    - el carbó com a combustible
  - **Conseqüències**
    - el creixement de les fàbriques
    - l'èxode cap a les ciutats
  - **Etapes**
    - primera revolució (1760)
    - segona revolució (1870)
"""

CASOS = [("b1_verbal", MAPA_B1), ("a2_categories", MAPA_A2)]

HTML = """<!doctype html><html><head><meta charset="utf-8">
<style>body{margin:0;background:#fff;font-family:'Segoe UI',system-ui,sans-serif}
#diagram{padding:24px;display:inline-block}</style></head>
<body><div id="diagram" class="schema"></div></body></html>"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    for slug, md in CASOS:
        page = browser.new_page(viewport={"width": 1100, "height": 800}, device_scale_factor=2)
        page.set_content(HTML)
        page.add_script_tag(content=CONVERTER)
        page.evaluate(
            """(md) => {
                const cont = document.getElementById('diagram');
                window.ATNE_MERMAID.renderMermaidBlock(cont, md, 'mapa_conceptual');
            }""",
            md,
        )
        page.wait_for_timeout(400)
        out = ROOT / "docs" / f"mapa_conceptual_{slug}.png"
        page.locator("#diagram svg").first.screenshot(path=str(out))
        page.close()
        print(f"OK -> {out.relative_to(ROOT)}")
    browser.close()
