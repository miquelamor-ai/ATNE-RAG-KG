# MVP ATNE - servidor local per provar sense PHP.
# Arrancar: python mpv/server_mpv.py
import os
import sys
import threading
from pathlib import Path

# Carrega .env del directori mpv/
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

import requests
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI()

MPV_DIR = Path(__file__).parent

# Claus Gemma amb rotació round-robin per distribuir quota
_GEMMA_KEYS = [
    os.environ.get(f"GEMMA4_API_KEY{s}", "")
    for s in ["", "_2", "_3", "_4", "_5", "_6", "_7"]
    if os.environ.get(f"GEMMA4_API_KEY{s}", "")
]
_GEMMA_KEY = _GEMMA_KEYS[0] if _GEMMA_KEYS else ""
_gemma_key_index = 0
_gemma_key_lock = threading.Lock()


# ── Mapping curs + adaptació → MECR ─────────────────────────────────────────

CURS_MECR = {
    ("primaria_12", "molt_simplificat"): "A1",
    ("primaria_12", "simplificat"):      "A1",
    ("primaria_12", "al_nivell"):        "A1",
    ("primaria_12", "enriquiment"):      "A2",
    ("primaria_34", "molt_simplificat"): "A1",
    ("primaria_34", "simplificat"):      "A1",
    ("primaria_34", "al_nivell"):        "A2",
    ("primaria_34", "enriquiment"):      "B1",
    ("primaria_56", "molt_simplificat"): "A1",
    ("primaria_56", "simplificat"):      "A2",
    ("primaria_56", "al_nivell"):        "B1",
    ("primaria_56", "enriquiment"):      "B2",
    ("eso_12",      "molt_simplificat"): "A2",
    ("eso_12",      "simplificat"):      "B1",
    ("eso_12",      "al_nivell"):        "B2",
    ("eso_12",      "enriquiment"):      "C1",
    ("eso_34",      "molt_simplificat"): "B1",
    ("eso_34",      "simplificat"):      "B1",
    ("eso_34",      "al_nivell"):        "B2",
    ("eso_34",      "enriquiment"):      "C1",
    ("batxillerat", "molt_simplificat"): "B1",
    ("batxillerat", "simplificat"):      "B2",
    ("batxillerat", "al_nivell"):        "C1",
    ("batxillerat", "enriquiment"):      "enriquiment",
}

def resolve_nivell(curs: str, adaptacio: str) -> str:
    return CURS_MECR.get((curs, adaptacio), "B1")


# ── Prompt builder ────────────────────────────────────────────────────────────

def build_system_prompt(nivell: str, perfils: list, complements: list, l1: str = "") -> str:
    p = (
        "Ets un assistent pedagògic especialitzat en adaptació de textos educatius en català.\n"
        "Adapta el text que t'enviaré.\n"
        "IMPORTANT: comença directament amb el text adaptat. "
        "No escriguis cap frase introductòria, cap títol genèric, "
        "cap explicació de què has fet ni cap comentari final.\n\n"
    )

    nivell_map = {
        "A1": "A1 — Lectura Fàcil estricta (AENOR UNE 153101:2018): frases ≤10 paraules, "
              "vocabulari bàsic, veu activa, una idea per frase, sense subordinades.",
        "A2": "A2 — Lectura Fàcil adaptada: frases curtes i directes, vocabulari freqüent, "
              "estructura simple, explica termes amb paraules conegudes.",
        "B1": "B1 — Llenguatge planer: frases clares, vocabulari estàndard, "
              "explica termes tècnics entre parèntesis.",
        "B2": "B2 — Rigor curricular: vocabulari tècnic quan cal, estructura clara, frases fluides.",
        "C1": "C1 — Text acadèmic estàndard: vocabulari tècnic precís, estructures complexes admeses.",
        "enriquiment": "Enriquiment — Taxonomia de Bloom (anàlisi, síntesi, avaluació): "
                       "aprofundeix conceptes, afegeix connexions interdisciplinàries, "
                       "invita a la reflexió crítica.",
    }
    p += "NIVELL:\n" + nivell_map.get(nivell, nivell_map["B1"]) + "\n"

    perfil_map = {
        "nouvingut":        "Nouvingut: vocabulari d'alta freqüència, frases curtes, "
                            "explica referents culturals no universals.",
        "tdah":             "TDAH (principis UDL): paràgrafs de 2-3 línies màxim, paraules clau en **negreta**, "
                            "idea principal al principi de cada bloc. "
                            "Defineix els termes tècnics la primera vegada que apareixen entre parèntesis: terme (definició breu). "
                            "Afegeix una línia de progrés [Secció X de N] entre blocs. "
                            "Inclou una pregunta breu de verificació al final de cada bloc. "
                            "Afegeix un resum curt al final. "
                            "IMPORTANT: no allarguis el text — manté la mateixa extensió que l'original.",
        "dislexia":         "Dislèxia: paraules curtes i freqüents, frases simples (màx. 12 paraules), "
                            "evita sigles i abreviatures, evita encadenar prefixos i sufixos.",
        "tea":              "TEA: llenguatge literal i directe, evita metàfores i ironies, "
                            "estructura previsible i ordenada amb passos numerats, frases afirmatives.",
        "tdl":              "TDL (Trastorn del Desenvolupament del Llenguatge): "
                            "redueix al màxim la densitat lèxica — el mínim de paraules de contingut per frase. "
                            "Estructura SVO estricta (Subjecte-Verb-Object): evita passives, subordinades i oracions de relatiu. "
                            "Cada terme tècnic apareix en 2-3 contextos lleugerament diferents per modelar-ne l'ús. "
                            "Fes explícita tota intenció comunicativa, no pressuposar inferències.",
        "di":               "Discapacitat intel·lectual: frases de màxim 8 paraules, una sola idea per frase. "
                            "Cada concepte abstracte amb un exemple tangible i quotidià immediat. "
                            "Repeteix els conceptes clau en formats diversos (explicació, exemple, resum). "
                            "Vocabulari d'ús quotidià, evita tecnicismes llevat que siguin imprescindibles.",
        "altes_capacitats": "ALERTA — Altes capacitats: PROHIBIT SIMPLIFICAR. "
                            "Mantén o augmenta la complexitat lingüística i conceptual original. "
                            "NO facis servir vocabulari freqüent en substitució del precís, "
                            "NO eliminis subordinades, NO escurcis frases, NO eliminis sentit figurat. "
                            "Afegeix profunditat: excepcions, fronteres del coneixement, debats oberts, "
                            "connexions interdisciplinàries i pensament crític.",
        "vulnerabilitat":   "Vulnerabilitat socioeconòmica: evita supòsits culturals implícits "
                            "(no pressuposar coneixement de festes, tradicions o geografia local). "
                            "Utilitza exemples i referents accessibles i universals. "
                            "Evita terminologia que pressuposi experiència escolar consolidada. "
                            "Tona propera i acollidora, sense condescendència.",
        "trastorn_emocional": "Trastorn emocional / ansietat: evita llenguatge que generi pressió o urgència "
                            "(no usar 'has de', 'cal', 'és obligatori'). "
                            "Tona tranquil·la i neutral. Divideix la informació en passos petits i manejables. "
                            "Evita temes sensibles sense previ avís. Reforça la autonomia: 'pots', 'és possible que'.",
    }
    if perfils:
        p += "\nPERFILS DE L'ALUMNAT:\n"
        for perfil in perfils:
            if perfil in perfil_map:
                p += f"- {perfil_map[perfil]}\n"

    if complements:
        p += "\nCOMPLEMENTS (afegeix al final del text adaptat, separats amb un títol clar en majúscules):\n"
        if "glossari" in complements:
            if "nouvingut" in perfils and l1:
                p += f"- GLOSSARI: 5-8 termes clau del text, definició breu adaptada al nivell i, entre parèntesis, la traducció a {l1}.\n"
            else:
                p += "- GLOSSARI: 5-8 termes clau del text amb definició breu adaptada al nivell indicat.\n"
        if "preguntes" in complements:
            p += "- PREGUNTES DE COMPRENSIÓ: 3-5 preguntes graduades (comprensió literal → aplicació → reflexió crítica).\n"

    return p


# ── Endpoint adaptar ──────────────────────────────────────────────────────────

OPENAI_MODELS = {"o1-mini", "gpt-4.1", "gpt-4o", "gpt-4o-mini", "gpt-4.1-mini"}
GEMMA_MODELS  = {"gemma-4-31b-it", "gemma-3-27b-it"}
ALLOWED_MODELS = OPENAI_MODELS | GEMMA_MODELS


def _call_openai(model: str, system_prompt: str, text: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY no configurada")
    payload: dict = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": text},
        ],
        "max_tokens": 4000,
    }
    if not model.startswith("o1"):
        payload["temperature"] = 0.7
    resp = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=120,
    )
    if resp.status_code != 200:
        detail = resp.json().get("error", {}).get("message", f"codi {resp.status_code}")
        raise RuntimeError(f"Error API OpenAI: {detail}")
    return resp.json()["choices"][0]["message"]["content"]


def _call_gemma(model: str, system_prompt: str, text: str) -> str:
    global _gemma_key_index
    if not _GEMMA_KEYS:
        raise RuntimeError("GEMMA4_API_KEY no configurada")
    from google import genai as gai
    from google.genai import types as gtypes
    with _gemma_key_lock:
        key = _GEMMA_KEYS[_gemma_key_index % len(_GEMMA_KEYS)]
        _gemma_key_index += 1
    client = gai.Client(api_key=key)
    # Gemma no suporta system_instruction separat: fusionem al missatge d'usuari
    combined = f"{system_prompt}\n\n---\n\nTEXT ORIGINAL A ADAPTAR:\n\n{text}"
    response = client.models.generate_content(
        model=model,
        contents=[gtypes.Content(role="user", parts=[gtypes.Part(text=combined)])],
        config=gtypes.GenerateContentConfig(temperature=0.4, max_output_tokens=8192),
    )
    return response.text or ""


@app.post("/api/adaptar")
async def adaptar(request: Request):
    data         = await request.json()
    text         = (data.get("text") or "").strip()
    curs         = data.get("curs", "eso_12")
    adaptacio    = data.get("adaptacio", "al_nivell")
    perfils      = data.get("perfils", [])
    complements  = data.get("complements", [])
    model        = data.get("model", "gpt-4o")
    l1           = (data.get("l1") or "").strip()

    if model not in ALLOWED_MODELS:
        model = "gpt-4o"
    if not text:
        return JSONResponse({"error": "El text és buit."}, status_code=400)

    nivell        = resolve_nivell(curs, adaptacio)
    system_prompt = build_system_prompt(nivell, perfils, complements, l1)

    try:
        if model in GEMMA_MODELS:
            adapted = _call_gemma(model, system_prompt, text)
        else:
            adapted = _call_openai(model, system_prompt, text)
    except RuntimeError as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    except requests.RequestException as e:
        return JSONResponse({"error": f"Error de xarxa: {e}"}, status_code=500)
    except Exception as e:
        return JSONResponse({"error": f"Error inesperat: {e}"}, status_code=500)

    return JSONResponse({"adapted": adapted})


# ── Serveix index.html ────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def index():
    return (MPV_DIR / "index.html").read_text(encoding="utf-8")


# ── Arrenca ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = 8090
    print(f"\n  ATNE MVP → http://localhost:{port}\n")
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="warning")
