"""
POC de cerca d'imatges a Wikimedia Commons per a conceptes educatius.

Prova si Wikimedia te cobertura suficient per substituir (o complementar)
la generacio FLUX. Concepte de prova: 'fotosintesi' i 'cicle de l'aigua'.

API: MediaWiki Action API (sense clau).
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parent
TS = time.strftime("%Y%m%d_%H%M%S")
OUT = ROOT / "results_illustrations" / f"wikimedia_{TS}"
OUT.mkdir(parents=True, exist_ok=True)

HEADERS = {"User-Agent": "ATNE-FJE-EducationalBot/1.0 (test; contact: fje)"}


def search_commons(query: str, limit: int = 5) -> list[dict]:
    """Cerca a Commons per terme + retorna imatges amb metadata."""
    # Pas 1: buscar pagines que coincideixin amb el terme
    url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": f"{query} filetype:bitmap|drawing",
        "gsrnamespace": 6,  # File:
        "gsrlimit": limit,
        "prop": "imageinfo",
        "iiprop": "url|size|mime|extmetadata",
        "iiurlwidth": 800,
    }
    r = requests.get(url, params=params, headers=HEADERS, timeout=30)
    r.raise_for_status()
    data = r.json()
    results = []
    for pageid, page in data.get("query", {}).get("pages", {}).items():
        info = (page.get("imageinfo") or [{}])[0]
        meta = info.get("extmetadata", {})
        results.append({
            "title": page.get("title"),
            "thumb_url": info.get("thumburl"),
            "full_url": info.get("url"),
            "width": info.get("width"),
            "height": info.get("height"),
            "mime": info.get("mime"),
            "license": meta.get("LicenseShortName", {}).get("value", "?"),
            "artist": meta.get("Artist", {}).get("value", "?"),
            "description": meta.get("ImageDescription", {}).get("value", "")[:200],
        })
    return results


def download(url: str, dst: Path):
    r = requests.get(url, headers=HEADERS, timeout=60)
    r.raise_for_status()
    dst.write_bytes(r.content)


QUERIES = {
    "fotosintesi": "photosynthesis",
    "cicle_aigua": "water cycle diagram",
    "revolucio_industrial_fabrica": "industrial revolution factory 19th century",
    "evaporacio": "evaporation water vapor",
}


def main():
    all_results = {}
    for key, query in QUERIES.items():
        print(f"[{key}] cerca '{query}'...")
        try:
            results = search_commons(query, limit=4)
            all_results[key] = results
            for i, r in enumerate(results[:2]):  # baixem les 2 primeres
                if r["thumb_url"]:
                    dst = OUT / f"{key}_{i+1}.jpg"
                    try:
                        download(r["thumb_url"], dst)
                        print(f"  {i+1}. {r['title']} [{r['license']}] -> {dst.name}")
                    except Exception as e:
                        print(f"  {i+1}. FAIL download: {e}")
        except Exception as e:
            print(f"  FAIL search: {e}", file=sys.stderr)
            all_results[key] = []

    # HTML report
    blocks = ""
    for key, results in all_results.items():
        imgs = ""
        for i, r in enumerate(results[:2]):
            local = OUT / f"{key}_{i+1}.jpg"
            if local.exists():
                imgs += f"""
                <div class="hit">
                  <img src="{local.name}">
                  <div class="meta">
                    <div class="title">{r['title']}</div>
                    <div class="license">Llicencia: <strong>{r['license']}</strong></div>
                    <div class="artist">Autor: {r['artist'][:80]}</div>
                    <a href="{r['full_url']}" target="_blank">Original a Commons</a>
                  </div>
                </div>
                """
        blocks += f'<div class="query"><h2>{key}</h2><p>query: <code>{QUERIES[key]}</code></p><div class="hits">{imgs}</div></div>'

    html = f"""<!DOCTYPE html>
<html lang="ca"><head><meta charset="UTF-8">
<title>POC Wikimedia Commons</title>
<style>
  body {{ font-family: system-ui, sans-serif; max-width: 1400px; margin: 2em auto; padding: 1em; }}
  h1 {{ color: #1a4b7a; }}
  h2 {{ color: #1a4b7a; border-bottom: 2px solid #e0e0e0; padding-bottom: 0.3em; }}
  .query {{ margin: 2em 0; }}
  .hits {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1.5em; }}
  .hit {{ border: 1px solid #ddd; border-radius: 8px; padding: 0.8em; }}
  .hit img {{ width: 100%; max-height: 500px; object-fit: contain; background: #fafafa; border-radius: 4px; }}
  .meta {{ font-size: 0.85em; margin-top: 0.6em; color: #555; }}
  .title {{ font-weight: bold; color: #1a4b7a; margin-bottom: 0.3em; }}
  code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
</style></head><body>

<h1>POC Wikimedia Commons - cerca d'il·lustracions educatives</h1>
<p>4 consultes, top 2 resultats cadascuna. Metadata (llicencia, autor) inclosa.</p>
{blocks}
</body></html>"""
    (OUT / "report.html").write_text(html, encoding="utf-8")
    print(f"\nObre: {OUT / 'report.html'}")


if __name__ == "__main__":
    main()
