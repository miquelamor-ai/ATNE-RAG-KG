"""Test comparatiu cec: Gemma 4 31B (baseline) vs Gemini 2.5 Flash vs Flash-Lite.
Llanca el mateix prompt ATNE-like als 3 models i guarda els outputs per avaluacio
manual per Claude. Mesura latencia + tokens.
"""
import os
import time
import json
import requests

API_KEY = os.getenv("GEMMA4_API_KEY") or "AIzaSyAnM7CI9rbIIDfKOZx_Y4Jg9C_Hb5b1m60"

SYSTEM_PROMPT = """Ets un assistent pedagogic especialista en adaptar textos educatius
a les necessitats de l'alumnat. Adaptes en CATALA.

PERFIL DE L'ALUMNE:
- Curs: 2n d'ESO
- MECR sortida: B1
- Condicions: TDAH + dislexia
- DUA: Core (adaptacio estandard mantenint rigor curricular)
- Genere discursiu: text expositiu cientific

REGLES DE LECTURA FACIL (LF):
- Puntuacio nomes: punts i dos punts (no usar ; ni ...)
- Veu activa sempre, subjecte explicit
- Una idea per frase, frases curtes
- Vocabulari frequent
- Termes tecnics en **negreta** amb explicacio integrada
- Dates completes (no numeros romans)

INSTRUCCIONS ESPECIFIQUES PER TDAH:
- Frases molt curtes (max 15 paraules)
- Estructura visual amb llistes i bullets quan ajudin
- Una sola idea per paragraf
- Connectors clars (perque, despres, finalment)

INSTRUCCIONS ESPECIFIQUES PER DISLEXIA:
- Vocabulari de freqüencia alta
- Evitar sinonims rebuscats
- Repetir conceptes clau amb formulacions diferents

FORMAT DE SORTIDA (obligatori, en aquest ordre):

## Text adaptat
[text adaptat seguint LF i les instruccions de TDAH+dislexia]

## Glossari
[termes tecnics destacats al text amb definicio breu en frase simple]

## Preguntes de comprensio
[3 preguntes de comprensio, una de cada moment: abans/durant/despres de la lectura]

NORMES:
- No incloure "Aqui tens..." ni cap meta-comentari al principi
- No usar emojis
- Mantenir tots els conceptes cientifics del text original (no eliminar contingut curricular)
- Si un concepte es massa abstracte, explicar-lo amb un exemple quotidia
"""

TEXT_ORIGINAL = """La fotosintesi es el proces bioquimic mitjancant el qual les plantes,
les algues i alguns bacteris transformen energia luminica en energia quimica,
sintetitzant glucosa a partir de diòxid de carboni i aigua. Aquest proces
te lloc principalment als cloroplasts, organuls cel·lulars que contenen
clorofil·la, un pigment que absorbeix la llum solar. La reaccio global es
6CO2 + 6H2O + llum -> C6H12O6 + 6O2, alliberant oxigen com a subproducte.
La fotosintesi te dues fases: la fase lluminosa (a les tilacoides, on es genera
ATP i NADPH) i la fase fosca o cicle de Calvin (a l'estroma, on es fixa el
carboni). La importancia ecologica es enorme: sustenta tota la cadena
trofica i regula la concentracio atmosferica d'O2 i CO2."""


MODELS = [
    ("gemma-4-31b-it", "Gemma 4 31B (baseline ATNE)"),
    ("gemini-2.5-flash", "Gemini 2.5 Flash"),
    ("gemini-2.5-flash-lite", "Gemini 2.5 Flash-Lite"),
]


def call_gemma(model_id, system, user_text):
    """Gemma: concatena system + user (no suporta system_instruction separat)."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": f"{system}\n\n---\n\nTEXT ORIGINAL A ADAPTAR:\n\n{user_text}"}]}],
        "generationConfig": {"temperature": 0.4, "maxOutputTokens": 4000},
    }
    t0 = time.time()
    r = requests.post(url, json=payload, timeout=300)
    elapsed = time.time() - t0
    r.raise_for_status()
    data = r.json()
    text = data["candidates"][0]["content"]["parts"][0].get("text", "")
    usage = data.get("usageMetadata", {})
    return text, elapsed, usage


def call_gemini(model_id, system, user_text):
    """Gemini: system_instruction separat + thinking_budget=0."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent?key={API_KEY}"
    payload = {
        "systemInstruction": {"parts": [{"text": system}]},
        "contents": [{"parts": [{"text": f"TEXT ORIGINAL A ADAPTAR:\n\n{user_text}"}]}],
        "generationConfig": {
            "temperature": 0.4,
            "maxOutputTokens": 4000,
            "thinkingConfig": {"thinkingBudget": 0},
        },
    }
    t0 = time.time()
    r = requests.post(url, json=payload, timeout=300)
    elapsed = time.time() - t0
    r.raise_for_status()
    data = r.json()
    text = data["candidates"][0]["content"]["parts"][0].get("text", "")
    usage = data.get("usageMetadata", {})
    return text, elapsed, usage


def main():
    results = []
    for model_id, label in MODELS:
        print(f"\n{'='*70}\nCRIDANT: {label} ({model_id})\n{'='*70}", flush=True)
        try:
            if model_id.startswith("gemma"):
                text, elapsed, usage = call_gemma(model_id, SYSTEM_PROMPT, TEXT_ORIGINAL)
            else:
                text, elapsed, usage = call_gemini(model_id, SYSTEM_PROMPT, TEXT_ORIGINAL)
            print(f"OK | {elapsed:.1f}s | tokens in/out: {usage.get('promptTokenCount')}/{usage.get('candidatesTokenCount')}")
            print(f"--- OUTPUT ---")
            print(text)
            results.append({
                "model_id": model_id,
                "label": label,
                "elapsed_s": elapsed,
                "usage": usage,
                "output": text,
            })
        except Exception as e:
            print(f"ERROR: {e}")
            results.append({"model_id": model_id, "error": str(e)})

    # Desa report json
    with open("tests/_flash_lite_vs_flash_report.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n\nRESUM:")
    for r in results:
        if "error" in r:
            print(f"  {r['model_id']}: ERROR {r['error']}")
        else:
            u = r["usage"]
            print(f"  {r['label']:<35} | {r['elapsed_s']:5.1f}s | in={u.get('promptTokenCount')} out={u.get('candidatesTokenCount')}")


if __name__ == "__main__":
    main()
