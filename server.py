"""
ATNE — Adaptador de Textos a Necessitats Educatives
Servidor FastAPI · Jesuïtes Educació

Executa:  python server.py
Obre:     http://localhost:8000
"""

import asyncio
import concurrent.futures
import json
import os
import re
import sys
import time
from pathlib import Path

import requests
import uvicorn
from dotenv import load_dotenv

# Blocs de prompt v2 (arquitectura 4 capes)
from prompt_blocks import (
    IDENTITY_BLOCK, UNIVERSAL_RULES_BLOCK,
    MECR_BLOCKS, DUA_BLOCKS, GENRE_BLOCKS,
    PROFILE_BLOCKS, CROSSING_BLOCKS, FEWSHOT_EXAMPLES,
    COGNITIVE_LOAD_BLOCK, CONFLICT_RESOLUTION_BLOCK,
)
from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse, FileResponse

# ── Configuració ────────────────────────────────────────────────────────────

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")

SUPABASE_HEADERS = {
    "apikey": SUPABASE_ANON_KEY,
    "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
    "Content-Type": "application/json",
}

PROFILES_DIR = Path(__file__).parent / "profiles"
PROFILES_DIR.mkdir(exist_ok=True)

UI_DIR = Path(__file__).parent / "ui"

# Client Gemini (SDK google-genai)
from google import genai
from google.genai import types

gemini_client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options=types.HttpOptions(timeout=180_000),  # 180s per generacions llargues
)

# ── FastAPI app ─────────────────────────────────────────────────────────────

app = FastAPI(title="ATNE", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Pàgines HTML ────────────────────────────────────────────────────────────

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    from fastapi.responses import Response
    return Response(status_code=204)


@app.get("/", response_class=HTMLResponse)
async def index():
    return HTMLResponse(
        (UI_DIR / "index.html").read_text(encoding="utf-8"),
        headers={"Cache-Control": "no-store"},
    )


@app.get("/ui/{path:path}")
async def serve_static(path: str):
    file = UI_DIR / path
    if not file.exists() or not file.is_file():
        raise HTTPException(404, "Fitxer no trobat")
    content_types = {
        ".css": "text/css",
        ".js": "application/javascript",
        ".png": "image/png",
        ".svg": "image/svg+xml",
        ".ico": "image/x-icon",
    }
    ct = content_types.get(file.suffix, "application/octet-stream")
    return FileResponse(file, media_type=ct)


# ── Funcions RAG + KG ──────────────────────────────────────────────────────

def embed_query(text: str) -> list[float]:
    """Genera embedding 768d amb Gemini."""
    result = gemini_client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config=types.EmbedContentConfig(output_dimensionality=768),
    )
    return result.embeddings[0].values


def vector_search(query: str, top_k: int = 30, filter_modul: str = None) -> list[dict]:
    """Cerca semàntica al vector store de Supabase."""
    embedding = embed_query(query)
    payload = {
        "query_embedding": embedding,
        "match_threshold": 0.3,
        "match_count": top_k,
    }
    if filter_modul:
        payload["filter_modul"] = filter_modul
    resp = requests.post(
        f"{SUPABASE_URL}/rest/v1/rpc/match_rag_fje",
        headers=SUPABASE_HEADERS,
        json=payload,
        timeout=15,
    )
    if resp.status_code == 200:
        return resp.json()
    return []


def kg_expand_concept(concepte: str, max_hops: int = 2) -> list[dict]:
    """Expandeix un concepte via Knowledge Graph."""
    resp = requests.post(
        f"{SUPABASE_URL}/rest/v1/rpc/kg_expand",
        headers=SUPABASE_HEADERS,
        json={"concepte": concepte, "max_hops": max_hops},
        timeout=10,
    )
    if resp.status_code == 200:
        return resp.json()
    return []


# Mapa de paraules clau → conceptes KG
KEYWORD_MAP = {
    "nouvingut": ["alumnat_nouvingut", "acollida", "adquisicio_llengua"],
    "nouvinguts": ["alumnat_nouvingut", "acollida", "adquisicio_llengua"],
    "adaptar": ["adaptacio_curricular", "dua", "programacio_multinivell"],
    "adaptació": ["adaptacio_curricular", "dua"],
    "inclusió": ["inclusio", "dua", "mesures_suport"],
    "lectura fàcil": ["lectura_facil", "comunicacio_clara"],
    "dua": ["dua", "disseny_universal_aprenentatge"],
    "tea": ["alumnat_tea", "tea"],
    "tdah": ["tdah", "alumnat_tdah"],
    "nese": ["nese", "neurodiversitat"],
    "dislèxia": ["dislexia", "dificultats_lectores"],
    "altes capacitats": ["altes_capacitats", "superdotacio"],
    "discapacitat": ["discapacitat", "nese"],
    "avaluació": ["avaluacio_formativa", "avaluacio_competencial"],
    "cooperatiu": ["aprenentatge_cooperatiu", "treball_cooperatiu"],
    "llengua": ["llengua", "competencia_linguistica"],
    "acollida": ["acollida", "alumnat_nouvingut"],
}


def extract_concepts(query: str) -> list[str]:
    """Extreu conceptes candidats de la query per buscar al KG."""
    q = query.lower()
    candidates = []
    for keyword, concepts in KEYWORD_MAP.items():
        if keyword in q:
            candidates.extend(concepts)
    return list(set(candidates))


def kg_search_documents(concepts: list[str], max_hops: int = 2) -> dict[str, float]:
    """Puntuació de documents via KG expansion."""
    doc_scores: dict[str, float] = {}
    for concept in concepts:
        neighbors = kg_expand_concept(concept, max_hops)
        for neighbor in neighbors:
            node_id = neighbor.get("node_id", "")
            node_tipus = neighbor.get("node_tipus", "")
            source = neighbor.get("node_source", "")
            dist = neighbor.get("distancia", 1)
            increment = 1.0 / dist
            if node_tipus == "document" and source:
                doc_scores[source] = doc_scores.get(source, 0) + increment * 2.0
            elif source:
                doc_scores[source] = doc_scores.get(source, 0) + increment
    if doc_scores:
        max_score = max(doc_scores.values())
        if max_score > 0:
            doc_scores = {k: v / max_score for k, v in doc_scores.items()}
    return doc_scores


def combined_search(query: str, top_k: int = 8) -> list[dict]:
    """Cerca combinada: vector similarity + KG expansion."""
    vector_results = vector_search(query, top_k=30)
    concepts = extract_concepts(query)
    kg_docs = kg_search_documents(concepts, max_hops=2)

    combined: dict[str, dict] = {}
    for doc in vector_results:
        source = doc["metadata"].get("source", "")
        sim = doc["similarity"]
        if source not in combined or combined[source]["similarity"] < sim:
            combined[source] = {
                "source": source,
                "similarity": sim,
                "kg_score": 0.0,
                "content": doc["content"],
                "metadata": doc["metadata"],
            }

    for source, kg_score in kg_docs.items():
        if source in combined:
            combined[source]["kg_score"] = kg_score
        else:
            combined[source] = {
                "source": source,
                "similarity": 0.0,
                "kg_score": kg_score,
                "content": "",
                "metadata": {"source": source},
            }

    max_sim = max((e["similarity"] for e in combined.values()), default=1) or 1
    for entry in combined.values():
        v = entry["similarity"] / max_sim
        k = entry["kg_score"]
        has_vector = entry["similarity"] > 0
        has_kg = k > 0
        if has_vector and has_kg:
            entry["final_score"] = 0.4 * v + 0.4 * k + 0.2
        elif has_kg:
            entry["final_score"] = 0.3 + 0.4 * k
        else:
            entry["final_score"] = 0.5 * v

    ranked = sorted(combined.values(), key=lambda x: x["final_score"], reverse=True)
    return ranked[:top_k]


def get_mandatory_docs(characteristics: dict) -> list[str]:
    """Retorna noms de documents obligatoris segons les característiques actives."""
    docs = [
        "M3_lectura-facil-comunicacio-clara.md",
        "M2_DUA-principis-pautes.md",
    ]
    if characteristics.get("nouvingut", {}).get("actiu"):
        docs.append("M1_alumnat-nouvingut.md")
        docs.append("M1_acollida-marc-conceptual.md")
    if characteristics.get("tea", {}).get("actiu"):
        docs.append("M1_alumnat-TEA.md")
    if characteristics.get("tdah", {}).get("actiu"):
        docs.append("M1_TDAH.md")
    if characteristics.get("dislexia", {}).get("actiu"):
        docs.append("M1_dislexia-dificultats-lectores.md")
    if characteristics.get("altes_capacitats", {}).get("actiu"):
        docs.append("M1_altes-capacitats.md")
    if characteristics.get("di", {}).get("actiu"):
        docs.append("M1_discapacitat-intel·lectual.md")
    if characteristics.get("disc_visual", {}).get("actiu"):
        docs.append("M1_discapacitat-visual.md")
    if characteristics.get("disc_auditiva", {}).get("actiu"):
        docs.append("M1_discapacitat-auditiva.md")
    if characteristics.get("disc_motora", {}).get("actiu"):
        docs.append("M1_discapacitat-motora.md")
    if characteristics.get("tdl", {}).get("actiu"):
        docs.append("M1_alumnat-TDL-trastorn-llenguatge.md")
    if characteristics.get("vulnerabilitat", {}).get("actiu"):
        docs.append("M1_vulnerabilitat-socioeducativa.md")
    if characteristics.get("trastorn_emocional", {}).get("actiu"):
        docs.append("M1_trastorns-emocionals-conducta.md")
    return docs


def fetch_docs_by_source(source_names: list[str]) -> list[dict]:
    """Recupera chunks de Supabase filtrant per nom de fitxer font."""
    results = []
    for source in source_names:
        resp = requests.get(
            f"{SUPABASE_URL}/rest/v1/rag_fje",
            headers=SUPABASE_HEADERS,
            params={
                "select": "content,metadata",
                "metadata->>source": f"eq.{source}",
                "limit": "3",
            },
            timeout=10,
        )
        if resp.status_code == 200:
            results.extend(resp.json())
    return results


# ── Regles d'auto-activació ────────────────────────────────────────────────

def propose_adaptation(characteristics: dict, context: dict) -> dict:
    """Calcula paràmetres d'adaptació i complements basats en el perfil."""
    # Extreure característiques actives
    actives = {k for k, v in characteristics.items() if v.get("actiu")}

    # Helpers
    nouvingut = characteristics.get("nouvingut", {})
    tea = characteristics.get("tea", {})
    di = characteristics.get("di", {})
    disc_visual = characteristics.get("disc_visual", {})
    disc_auditiva = characteristics.get("disc_auditiva", {})
    ac = characteristics.get("altes_capacitats", {})
    etapa = context.get("etapa", "ESO")

    mecr = nouvingut.get("mecr", "")
    tea_nivell = tea.get("nivell_suport", 1)
    di_grau = di.get("grau", "lleu")
    ac_doble = ac.get("doble_excepcionalitat", False)

    # ── Nivell DUA ──
    dua = "Core"
    if (di_grau == "sever" and "di" in actives) or \
       (tea_nivell == 3 and "tea" in actives) or \
       (mecr == "pre-A1" and not nouvingut.get("alfabet_llati", True) and "nouvingut" in actives):
        dua = "Acces"
    elif "altes_capacitats" in actives and not ac_doble:
        dua = "Enriquiment"

    # ── Intensitat LF (1-5) ──
    lf = 2  # defecte
    lf_factors = []
    if "di" in actives:
        lf_factors.append({"sever": 5, "moderat": 4, "lleu": 3}.get(di_grau, 3))
    if "tea" in actives:
        lf_factors.append({3: 5, 2: 4, 1: 2}.get(tea_nivell, 2))
    if "disc_visual" in actives and disc_visual.get("grau") == "ceguesa":
        lf_factors.append(5)
    if "nouvingut" in actives:
        lf_factors.append({"pre-A1": 4, "A1": 3, "A2": 2, "B1": 1, "B2": 1}.get(mecr, 3))
    if "dislexia" in actives:
        lf_factors.append(3)
    if "tdl" in actives:
        lf_factors.append(3)
    if "tdah" in actives:
        lf_factors.append(2)
    if "altes_capacitats" in actives:
        lf_factors.append(1)
    if lf_factors:
        lf = max(lf_factors)

    # ── MECR sortida ──
    mecr_sortida = "B2"
    etapa_defaults = {
        "infantil": "A1", "primaria": "B1", "ESO": "B2",
        "batxillerat": "B2", "FP": "B2",
    }
    if "nouvingut" in actives and mecr:
        mecr_sortida = mecr
    elif "di" in actives:
        mecr_sortida = {"sever": "A1", "moderat": "A2", "lleu": "B1"}.get(di_grau, "B1")
    else:
        mecr_sortida = etapa_defaults.get(etapa, "B2")

    # ── Complements automàtics ──
    complements = {
        "glossari": True,  # sempre
        "negretes": True,  # sempre
        "definicions_integrades": dua == "Acces" or mecr in ("pre-A1", "A1") or "di" in actives or "tdl" in actives,
        "traduccio_l1": "nouvingut" in actives,
        "pictogrames": dua == "Acces" or (tea_nivell >= 2 and "tea" in actives)
            or (di_grau in ("moderat", "sever") and "di" in actives)
            or (disc_auditiva.get("comunicacio") == "LSC" and "disc_auditiva" in actives),
        "esquema_visual": any(c in actives for c in ("tdah", "dislexia", "tea", "nouvingut")),
        "bastides": any(c in actives for c in ("nouvingut", "di", "tea", "dislexia")),
        "mapa_conceptual": dua in ("Core", "Enriquiment") and etapa in ("ESO", "batxillerat", "FP"),
        "preguntes_comprensio": dua == "Core" and etapa != "infantil",
        "activitats_aprofundiment": dua == "Enriquiment" or "altes_capacitats" in actives,
        "mapa_mental": "altes_capacitats" in actives,
        "argumentacio_pedagogica": True,  # sempre — justificació de les decisions
    }

    return {
        "dua": dua,
        "lf": lf,
        "mecr_sortida": mecr_sortida,
        "complements": complements,
    }


# ── System prompt v2 — Arquitectura 4 capes (hardcoded) ────────────────────


def _get_active_profiles(profile: dict) -> list[str]:
    """Retorna la llista de claus de perfil actives."""
    chars = profile.get("caracteristiques", {})
    return [key for key, val in chars.items() if val.get("actiu")]


def _get_cognitive_load_level(mecr: str) -> str:
    """Determina el nivell de càrrega cognitiva segons MECR."""
    if mecr in ("pre-A1", "A1", "A2"):
        return "low"
    elif mecr == "B1":
        return "mid"
    return "high"


def _detect_crossing_signals(active_profiles: list[str], profile: dict,
                             mecr: str, genre: str = "") -> list[str]:
    """Detecta creuaments entre perfils actius i retorna blocs aplicables."""
    blocks = []
    chars = profile.get("caracteristiques", {})

    for combo, block_text in CROSSING_BLOCKS.items():
        # Creuaments entre 2 perfils
        if all(p in active_profiles for p in combo):
            blocks.append(block_text)
            continue
        # Creuaments perfil + condició contextual
        if combo == ("nouvingut", "l2_molt_baixa"):
            if "nouvingut" in active_profiles and mecr in ("pre-A1", "A1"):
                blocks.append(block_text)
        elif combo == ("nouvingut", "escolaritzacio_parcial"):
            if "nouvingut" in active_profiles:
                esc = chars.get("nouvingut", {}).get("escolaritzacio", "")
                if esc and "parcial" in str(esc).lower():
                    blocks.append(block_text)
        elif combo == ("tea", "narracio"):
            if "tea" in active_profiles and genre == "narracio":
                blocks.append(block_text)
        elif combo == ("tdah", "text_llarg"):
            if "tdah" in active_profiles:
                blocks.append(block_text)  # Sempre rellevant si TDAH actiu
        elif combo == ("tdl", "vocabulari_dens"):
            if "tdl" in active_profiles:
                blocks.append(block_text)
        elif combo == ("discapacitat_intellectual", "abstracte"):
            if "discapacitat_intellectual" in active_profiles:
                blocks.append(block_text)
        elif combo == ("trastorn_emocional", "trauma"):
            if "trastorn_emocional" in active_profiles:
                trauma = chars.get("trastorn_emocional", {}).get("trauma", False)
                if trauma:
                    blocks.append(block_text)

    return blocks


def build_persona_audience(profile: dict, context: dict, mecr: str) -> str:
    """Genera narrativa concreta de l'alumne (persona-audience pattern)."""
    chars = profile.get("caracteristiques", {})
    etapa = context.get("etapa", "ESO")
    canal = profile.get("canal_preferent", "mixte")
    obs = profile.get("observacions", "")

    parts = [f"Escrius per a un alumne de {etapa}"]

    # Afegir detalls dels perfils actius
    for key, val in chars.items():
        if not val.get("actiu"):
            continue
        if key == "nouvingut":
            l1 = val.get("L1", "desconeguda")
            origen = val.get("origen", "")
            mesos = val.get("mesos_catalunya", "")
            esc = val.get("escolaritzacio", "")
            parts.append(f"nouvingut (L1: {l1}")
            if origen:
                parts[-1] += f", origen: {origen}"
            if mesos:
                parts[-1] += f", {mesos} mesos a Catalunya"
            if esc:
                parts[-1] += f", escolarització: {esc}"
            parts[-1] += ")"
        elif key == "tea":
            parts.append("amb TEA (Trastorn de l'Espectre Autista)")
        elif key == "tdah":
            parts.append("amb TDAH")
        elif key == "dislexia":
            parts.append("amb dislèxia")
        elif key == "tdl":
            parts.append("amb TDL (Trastorn del Desenvolupament del Llenguatge)")
        elif key == "discapacitat_intellectual":
            grau = val.get("grau", "")
            parts.append(f"amb discapacitat intel·lectual{f' ({grau})' if grau else ''}")
        elif key == "altes_capacitats":
            parts.append("amb altes capacitats")
        elif key == "2e":
            parts.append("amb doble excepcionalitat (2e)")
        elif key == "discapacitat_visual":
            parts.append("amb discapacitat visual")
        elif key == "discapacitat_auditiva":
            parts.append("amb discapacitat auditiva")
        elif key == "vulnerabilitat_socioeducativa":
            parts.append("en situació de vulnerabilitat socioeducativa")
        elif key == "trastorn_emocional":
            parts.append("amb trastorn emocional/conductual")

    narrativa = ", ".join(parts) + f".\nNivell MECR de sortida: {mecr}."

    # Canal d'accés preferent
    canal_desc = {
        "mixte": "Mixte (text + visual)",
        "visual": "Principalment visual — prioritzar esquemes, pictogrames, icones",
        "oral": "Principalment oral — text molt curt, pensat per ser llegit en veu alta",
        "text": "Principalment textual — text clar i ben estructurat",
    }
    narrativa += f"\nCanal d'accés preferent: {canal_desc.get(canal, canal)}."

    # Observacions del docent
    if obs:
        narrativa += f"\nObservacions del docent (PRIORITAT ALTA): {obs}"

    return f"PERSONA-AUDIENCE:\n{narrativa}"


def build_output_format(params: dict, l1: str) -> str:
    """Genera les instruccions de format de sortida segons complements actius."""
    comp = params.get("complements", {})
    l1_display = l1 if l1 else "la llengua materna de l'alumne"

    sections = []
    sections.append("""FORMAT DE SORTIDA:
Respon EXACTAMENT amb les seccions següents, separades per encapçalaments ## .
Genera NOMÉS les seccions indicades com ACTIVADES.

## Text adaptat
El text complet adaptat segons tots els paràmetres indicats.
- Estructura clara amb salts de línia entre idees
- Termes tècnics en **negreta** amb definició entre parèntesis la primera vegada
- Una idea per frase
- Si el nivell és A1 o inferior: frases molt curtes, vocabulari quotidià, sense subordinades""")

    if comp.get("glossari"):
        sections.append(f"""## Glossari
ACTIVAT — Genera una TAULA MARKDOWN amb 3 columnes:
| Terme | Traducció ({l1_display}) | Explicació simple |
Inclou tots els termes tècnics o difícils del text adaptat (mínim 8-12 termes).
La columna de traducció ha de contenir la traducció REAL al/a la {l1_display} (en el seu alfabet original si escau: àrab, xinès, urdú, etc.).
L'explicació ha de ser en català molt senzill (nivell A1).""")

    if comp.get("negretes"):
        sections.append("## Negretes\nACTIVAT — Ja integrat al text adaptat (termes clau en **negreta**). No cal secció separada.")

    if comp.get("definicions_integrades"):
        sections.append("## Definicions integrades\nACTIVAT — Ja integrat al text adaptat (definicions entre parèntesis). No cal secció separada.")

    if comp.get("traduccio_l1"):
        sections.append(f"## Traducció L1\nACTIVAT — Ja integrat al glossari (columna de traducció a {l1_display}). No cal secció separada.")

    if comp.get("pictogrames"):
        sections.append("""## Pictogrames
ACTIVAT — Afegeix icones/emojis de suport al costat dels conceptes clau del text adaptat.
Exemples: ☀️ per llum, 💧 per aigua, 🌱 per planta, 🔬 per ciència, etc.
Integra'ls directament al text adaptat, no en secció separada.""")

    if comp.get("esquema_visual"):
        sections.append("""## Esquema visual
ACTIVAT — Genera un esquema/diagrama en format text que mostri el procés o les relacions del contingut.
Format: usa fletxes (→, ↓), símbols (+, =) i emojis per fer-lo visual i intuïtiu.
Ha de ser senzill, visual i comprensible per a l'alumne.""")

    if comp.get("mapa_conceptual"):
        sections.append("""## Mapa conceptual
ACTIVAT — Genera un mapa conceptual en format text amb estructura d'arbre.
Mostra les relacions jeràrquiques entre els conceptes principals del text.""")

    if comp.get("preguntes_comprensio"):
        sections.append("""## Preguntes de comprensió
ACTIVAT — Genera preguntes GRADUADES en 3 nivells de dificultat:
### Nivell 1: Resposta curta (reconeixement) — 3 preguntes directes del text.
### Nivell 2: Verdader o fals — 3 afirmacions ✅ o ❌.
### Nivell 3: Relaciona o completa — 2-3 activitats.
Adapta la dificultat al nivell MECR de sortida.""")

    if comp.get("activitats_aprofundiment"):
        sections.append("""## Activitats d'aprofundiment
ACTIVAT — Genera 2-3 activitats de repte cognitiu:
connexions interdisciplinars, pensament crític, recerca guiada, debat.""")

    if comp.get("bastides"):
        sections.append(f"""## Bastides (scaffolding)
ACTIVAT — Genera suports didàctics en 4 blocs:
### Frases model — 3-5 frases incompletes per completar amb info del text.
### Banc de paraules — 8-12 paraules clau.
### Suport visual — Indicacions d'icones, colors, esquemes recomanats.
### Suport L1 — Pistes en {l1_display} per conceptes abstractes.""")

    if comp.get("mapa_mental"):
        sections.append("""## Mapa mental
ACTIVAT — Genera un mapa mental radial amb el concepte central al mig,
branques amb associacions, preguntes i connexions interdisciplinars.""")

    # Sempre: argumentació pedagògica + auditoria
    sections.append("""## Argumentació pedagògica
SEMPRE GENERAR — Explica les decisions pedagògiques preses (3-5 punts breus):
1. Adaptació lingüística 2. Atenció a la diversitat 3. Suport multimodal
4. Gradació cognitiva 5. Rigor curricular

## Notes d'auditoria
SEMPRE GENERAR — Taula comparativa breu:
| Aspecte | Original | Adaptat | Motiu |
Màxim 5-6 files amb els canvis més significatius.

Omès les seccions NO ACTIVADES. No generis seccions buides.""")

    return "\n\n".join(sections)


def build_system_prompt(profile: dict, context: dict, params: dict, rag_context: str) -> str:
    """Munta el system prompt v2 complet per a Gemini (arquitectura 4 capes)."""
    parts = []

    # ── CAPA 1: Identitat (fixa) ──────────────────────────────────────────
    parts.append(IDENTITY_BLOCK)

    # ── CAPA 2: Instruccions universals (fixa) ────────────────────────────
    parts.append(UNIVERSAL_RULES_BLOCK)

    # ── CAPA 3: Instruccions condicionals (variable) ──────────────────────

    # 3a. MECR — NOMÉS el nivell de sortida
    mecr = params.get("mecr_sortida", "B2")
    parts.append(MECR_BLOCKS.get(mecr, MECR_BLOCKS["B2"]))

    # 3b. DUA
    dua = params.get("dua", "Core")
    parts.append(DUA_BLOCKS.get(dua, DUA_BLOCKS["Core"]))

    # 3c. Gènere discursiu (si indicat pel context)
    genre = context.get("genere_discursiu", "")
    if genre and genre in GENRE_BLOCKS:
        parts.append(GENRE_BLOCKS[genre])

    # 3d. Blocs per perfil — NOMÉS els actius
    active_profiles = _get_active_profiles(profile)
    for p in active_profiles:
        if p in PROFILE_BLOCKS:
            parts.append(PROFILE_BLOCKS[p])

    # 3e. Blocs de creuament — NOMÉS si apliquen
    crossing_blocks = _detect_crossing_signals(active_profiles, profile, mecr, genre)
    for block in crossing_blocks:
        parts.append(block)

    # 3f. Càrrega cognitiva
    cog_level = _get_cognitive_load_level(mecr)
    parts.append(COGNITIVE_LOAD_BLOCK[cog_level])

    # 3g. Resolució de conflictes (només si DUA Accés o nivell baix)
    if dua == "Acces" or mecr in ("pre-A1", "A1", "A2"):
        parts.append(CONFLICT_RESOLUTION_BLOCK)

    # 3h. Few-shot example — 1 per al nivell MECR
    if mecr in FEWSHOT_EXAMPLES:
        parts.append(FEWSHOT_EXAMPLES[mecr])

    # ── CAPA 4: Context (variable) ────────────────────────────────────────

    # 4a. Context educatiu
    parts.append(f"""CONTEXT EDUCATIU:
- Etapa: {context.get('etapa', 'ESO')}
- Curs: {context.get('curs', '')}
- Àmbit: {context.get('ambit', '')}
- Matèria: {context.get('materia', '')}
- Tipus d'aula: {context.get('tipus_aula', 'ordinaria')}""")

    # 4b. Persona-audience
    parts.append(build_persona_audience(profile, context, mecr))

    # 4c. Context RAG
    if rag_context:
        parts.append(f"CONEIXEMENT PEDAGÒGIC DE REFERÈNCIA (corpus FJE):\n{rag_context}")

    # 4d. Format de sortida
    chars = profile.get("caracteristiques", {})
    l1 = ""
    if chars.get("nouvingut", {}).get("actiu") and chars.get("nouvingut", {}).get("L1"):
        l1 = chars["nouvingut"]["L1"]
    parts.append(build_output_format(params, l1))

    return "\n\n".join(parts)


# ── Post-processament v2 ───────────────────────────────────────────────────

# Límits de paraules per frase segons MECR
MECR_SENTENCE_LIMITS = {
    "pre-A1": 5, "A1": 8, "A2": 12, "B1": 18, "B2": 25,
}

# Paraules prohibides en context tècnic
FORBIDDEN_WORDS = [
    "cosa", "coses", "allò", "això", "el que fa que", "serveix per", "un tipus de",
]


def post_process_adaptation(text: str, mecr: str) -> dict:
    """Verifica la sortida de l'LLM i retorna mètriques + avisos.

    No modifica el text — reporta problemes perquè el docent/sistema els vegi.
    """
    warnings = []
    max_words = MECR_SENTENCE_LIMITS.get(mecr, 25)

    # Extreure només el text adaptat (entre ## Text adaptat i el següent ##)
    adapted_match = re.search(
        r'## Text adaptat\s*\n(.*?)(?=\n## |\Z)',
        text, re.DOTALL
    )
    adapted_text = adapted_match.group(1) if adapted_match else text

    # 1. Verificar longitud de frases
    sentences = re.split(r'[.!?]\s+', adapted_text)
    long_sentences = []
    for s in sentences:
        s = s.strip()
        if not s or s.startswith("#") or s.startswith("|") or s.startswith("-"):
            continue
        word_count = len(s.split())
        if word_count > max_words + 3:  # marge de 3 paraules (definicions)
            long_sentences.append((s[:60] + "...", word_count))

    if long_sentences:
        warnings.append({
            "type": "sentence_length",
            "msg": f"{len(long_sentences)} frase(s) superen el límit MECR {mecr} ({max_words} paraules)",
            "details": long_sentences[:3],
        })

    # 2. Detectar paraules prohibides
    text_lower = adapted_text.lower()
    found_forbidden = [w for w in FORBIDDEN_WORDS if w in text_lower]
    if found_forbidden:
        warnings.append({
            "type": "forbidden_words",
            "msg": f"Paraules prohibides detectades: {', '.join(found_forbidden)}",
        })

    # 3. Verificar presència d'encapçalaments
    has_headings = bool(re.search(r'^##\s', text, re.MULTILINE))
    if not has_headings:
        warnings.append({
            "type": "missing_headings",
            "msg": "No s'han detectat encapçalaments ## al text",
        })

    # 4. Verificar presència de termes en negreta
    bold_count = len(re.findall(r'\*\*[^*]+\*\*', adapted_text))
    if bold_count == 0 and mecr in ("pre-A1", "A1", "A2"):
        warnings.append({
            "type": "missing_bold",
            "msg": "No s'han detectat termes en negreta al text adaptat",
        })

    # Mètriques bàsiques
    all_words = adapted_text.split()
    metrics = {
        "total_words": len(all_words),
        "total_sentences": len([s for s in sentences if s.strip()]),
        "bold_terms": bold_count,
        "mecr_limit": max_words,
    }

    return {"warnings": warnings, "metrics": metrics}


# ── Adaptació (funció bloquejant per executar en thread pool) ──────────────

def clean_gemini_output(text: str) -> str:
    """Neteja la sortida de Gemini: elimina 'thinking' filtrat i normalitza headings."""
    # 1. Treure qualsevol text abans del primer ## (thinking filtrat)
    match = re.search(r'^## ', text, re.MULTILINE)
    if match and match.start() > 0:
        text = text[match.start():]

    # 2. Arreglar ## que queden enganxats a text anterior (sense salt de línia)
    text = re.sub(r'(?<!\n)(## )', r'\n\1', text)

    # 3. Treure línies de meta-comentari típiques de Gemini
    lines_to_remove = [
        r"^Final draft.*$",
        r"^I'll proceed.*$",
        r"^Here is the.*$",
        r"^Let me.*$",
        r"^Okay,.*output.*$",
    ]
    for pattern in lines_to_remove:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE | re.MULTILINE)

    # 4. Convertir sub-headings duplicats ## dins de seccions a ###
    #    Gemini a vegades escriu "## Nivell 1:" dins de "## Preguntes"
    #    Lògica: el primer ## de cada secció principal es manté,
    #    els ## dins d'una secció es converteixen a ###
    lines = text.split("\n")
    in_section = False
    fixed_lines = []
    for line in lines:
        if line.startswith("## "):
            title_lower = line[3:].strip().lower()
            # És una secció principal si el títol és un dels principals
            is_main = any(kw in title_lower for kw in [
                "text adaptat", "glossari", "esquema", "mapa conceptual",
                "preguntes", "bastides", "activitats", "mapa mental",
                "argumentació", "argumentacio", "notes d'auditoria",
                "notes d'audit", "pictogrames", "traducció", "negretes",
                "definicions",
            ])
            if is_main:
                in_section = True
                fixed_lines.append(line)
            else:
                # Sub-heading dins d'una secció → convertir a ###
                fixed_lines.append("###" + line[2:])
        else:
            fixed_lines.append(line)
    text = "\n".join(fixed_lines)

    # 5. Treure línies que són només "#" (artefacte de Gemini)
    text = re.sub(r'^#\s*$', '', text, flags=re.MULTILINE)

    # 6. Netejar línies buides excessives
    text = re.sub(r'\n{4,}', '\n\n\n', text)

    return text.strip()


def run_adaptation(text: str, profile: dict, context: dict, params: dict,
                   progress_callback=None):
    """Executa tot el pipeline d'adaptació: RAG search + Gemini."""
    cb = progress_callback or (lambda ev: None)

    # 1. Cerca RAG+KG
    cb({"type": "step", "step": "search", "msg": "Cercant context pedagògic rellevant..."})

    chars = profile.get("caracteristiques", {})
    # Construir query de cerca: text + característiques
    search_terms = []
    for key, val in chars.items():
        if val.get("actiu"):
            search_terms.append(key.replace("_", " "))
    search_query = " ".join(search_terms) + " " + text[:200]

    try:
        search_results = combined_search(search_query, top_k=8)
        cb({"type": "step", "step": "search_done",
            "msg": f"{len(search_results)} documents trobats via RAG+KG"})
    except Exception as e:
        cb({"type": "step", "step": "search_done",
            "msg": f"Cerca RAG amb error ({e}), continuant sense context..."})
        search_results = []

    # 2. Recuperar documents obligatoris
    cb({"type": "step", "step": "mandatory", "msg": "Afegint documents obligatoris..."})
    mandatory_names = get_mandatory_docs(chars)
    # Comprovar quins ja tenim dels search results
    found_sources = {r["source"] for r in search_results if r.get("source")}
    missing = [n for n in mandatory_names if n not in found_sources]
    if missing:
        mandatory_docs = fetch_docs_by_source(missing)
        for doc in mandatory_docs:
            search_results.append({
                "source": doc["metadata"].get("source", "obligatori"),
                "content": doc["content"],
                "final_score": 1.0,
            })

    # 3. Muntar context RAG
    rag_parts = []
    for r in search_results:
        if r.get("content"):
            source = r.get("source", "")
            rag_parts.append(f"[Font: {source}]\n{r['content'][:500]}")
    rag_context = "\n\n---\n\n".join(rag_parts[:12])

    # 4. System prompt
    system_prompt = build_system_prompt(profile, context, params, rag_context)

    # 5. Cridar Gemini
    cb({"type": "step", "step": "adapting", "msg": "Generant adaptació amb Gemini..."})
    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"TEXT ORIGINAL A ADAPTAR:\n\n{text}",
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.4,
                max_output_tokens=16384,
                thinking_config=types.ThinkingConfig(thinking_budget=0),
            ),
        )
        adapted = response.text or ""
        # Avisar si Gemini ha truncat per max_output_tokens
        try:
            fr = response.candidates[0].finish_reason
            if fr and str(fr).upper() in ("MAX_TOKENS", "2"):
                cb({"type": "step", "step": "warning",
                    "msg": "⚠ La resposta s'ha truncat (massa complements). Considera reduir-ne."})
        except Exception:
            pass
        # Netejar "thinking" filtrat de Gemini (text abans del primer ## )
        adapted = clean_gemini_output(adapted)

        # Post-processament v2: verificar qualitat
        mecr = params.get("mecr_sortida", "B2")
        pp = post_process_adaptation(adapted, mecr)
        for w in pp.get("warnings", []):
            cb({"type": "step", "step": "warning", "msg": f"⚠ {w['msg']}"})

    except Exception as e:
        adapted = f"Error en la generació: {e}"
        pp = {"warnings": [], "metrics": {}}

    cb({"type": "result", "adapted": adapted, "post_process": pp})
    cb({"type": "done"})
    return adapted


# ── API endpoints ───────────────────────────────────────────────────────────

@app.get("/api/health")
async def health():
    """Verifica connectivitat amb Supabase i Gemini."""
    checks = {"supabase": False, "gemini": False}
    try:
        resp = requests.get(
            f"{SUPABASE_URL}/rest/v1/rag_fje",
            headers=SUPABASE_HEADERS,
            params={"select": "id", "limit": "1"},
            timeout=5,
        )
        checks["supabase"] = resp.status_code == 200
    except Exception:
        pass
    try:
        gemini_client.models.get(model="gemini-2.5-flash")
        checks["gemini"] = True
    except Exception:
        pass
    ok = all(checks.values())
    return JSONResponse({"ok": ok, **checks}, status_code=200 if ok else 503)


# ── Perfils CRUD ────────────────────────────────────────────────────────────

@app.get("/api/profiles")
async def list_profiles():
    profiles = []
    for f in sorted(PROFILES_DIR.glob("*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            profiles.append({"nom": data.get("nom", f.stem), "fitxer": f.stem})
        except Exception:
            pass
    return profiles


@app.post("/api/profiles")
async def save_profile(payload: dict = Body(...)):
    nom = payload.get("nom", "sense_nom")
    # Sanititzar nom per a filename
    safe = re.sub(r'[^\w\s-]', '', nom).strip().replace(" ", "_")[:50]
    if not safe:
        safe = "perfil"
    path = PROFILES_DIR / f"{safe}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": True, "fitxer": safe}


@app.get("/api/profiles/{nom}")
async def load_profile(nom: str):
    path = PROFILES_DIR / f"{nom}.json"
    if not path.exists():
        raise HTTPException(404, "Perfil no trobat")
    return json.loads(path.read_text(encoding="utf-8"))


@app.delete("/api/profiles/{nom}")
async def delete_profile(nom: str):
    path = PROFILES_DIR / f"{nom}.json"
    if path.exists():
        path.unlink()
    return {"ok": True}


# ── Historial i feedback ──────────────────────────────────────────────────

@app.get("/api/history")
async def list_history(limit: int = 30):
    """Llista les últimes adaptacions de l'historial."""
    try:
        resp = requests.get(
            f"{SUPABASE_URL}/rest/v1/history"
            f"?select=id,created_at,profile_name,original_text,profile_json,context_json,params_json,rating"
            f"&order=created_at.desc&limit={limit}",
            headers=SUPABASE_HEADERS,
            timeout=10,
        )
        if resp.status_code == 200:
            return {"ok": True, "items": resp.json()}
        return {"ok": False, "items": [], "error": resp.text}
    except Exception as e:
        return {"ok": False, "items": [], "error": str(e)}


@app.post("/api/history")
async def save_history(payload: dict = Body(...)):
    """Desa una adaptació a l'historial de Supabase."""
    row = {
        "profile_name": payload.get("profile_name", ""),
        "profile_json": payload.get("profile", {}),
        "context_json": payload.get("context", {}),
        "params_json": payload.get("params", {}),
        "original_text": payload.get("original", ""),
        "adapted_text": payload.get("adapted", ""),
    }
    try:
        resp = requests.post(
            f"{SUPABASE_URL}/rest/v1/history",
            headers={**SUPABASE_HEADERS, "Prefer": "return=representation"},
            json=row,
            timeout=10,
        )
        if resp.status_code in (200, 201):
            data = resp.json()
            return {"ok": True, "id": data[0]["id"] if data else None}
        return {"ok": False, "error": resp.text}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@app.patch("/api/history/{history_id}")
async def update_history_feedback(history_id: int, payload: dict = Body(...)):
    """Actualitza el rating i comentari d'una entrada de l'historial."""
    update = {}
    if "rating" in payload:
        update["rating"] = payload["rating"]
    if "comment" in payload:
        update["comment"] = payload["comment"]
    update["rated_at"] = "now()"
    try:
        resp = requests.patch(
            f"{SUPABASE_URL}/rest/v1/history?id=eq.{history_id}",
            headers={**SUPABASE_HEADERS, "Prefer": "return=representation"},
            json=update,
            timeout=10,
        )
        if resp.status_code in (200, 204):
            return {"ok": True}
        return {"ok": False, "error": resp.text}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ── Proposta d'adaptació ───────────────────────────────────────────────────

@app.post("/api/propose")
async def propose(payload: dict = Body(...)):
    characteristics = payload.get("caracteristiques", {})
    context = payload.get("context", {})
    result = propose_adaptation(characteristics, context)
    return result


# ── Adaptació (SSE stream) ─────────────────────────────────────────────────

@app.post("/api/adapt")
async def adapt_stream(payload: dict = Body(...)):
    text = payload.get("text", "")
    profile = payload.get("profile", {})
    context = payload.get("context", {})
    params = payload.get("params", {})

    if not text.strip():
        return JSONResponse({"error": "Cal proporcionar un text"}, status_code=400)

    async def gen():
        events: list[dict] = []
        def cb(ev):
            events.append(ev)

        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor() as pool:
            task = loop.run_in_executor(
                pool,
                lambda: run_adaptation(text, profile, context, params, cb),
            )
            while not task.done():
                while events:
                    yield f"data: {json.dumps(events.pop(0), ensure_ascii=False)}\n\n"
                # Keepalive: evita QUIC_NETWORK_IDLE_TIMEOUT mentre Gemini genera
                yield ": keepalive\n\n"
                await asyncio.sleep(0.5)
            # Drenar events restants (run_adaptation ja envia 'done')
            while events:
                yield f"data: {json.dumps(events.pop(0), ensure_ascii=False)}\n\n"

    return StreamingResponse(gen(), media_type="text/event-stream")


# ── Exportació ──────────────────────────────────────────────────────────────

@app.post("/api/export")
async def export_doc(payload: dict = Body(...)):
    fmt = payload.get("format", "txt")
    adapted = payload.get("adapted", "")
    original = payload.get("original", "")
    profile_name = payload.get("profile_name", "adaptacio")

    import tempfile
    safe_name = re.sub(r'[^\w\s-]', '', profile_name).strip().replace(" ", "_")[:30] or "adaptacio"
    timestamp = time.strftime("%Y%m%d_%H%M")
    base_name = f"ATNE_{safe_name}_{timestamp}"

    def pdf_safe(text):
        """Filtra text per PDF: només caràcters que Arial/Liberation pot renderitzar.
        Whitelist: ASCII, Latin Extended, àrab, puntuació general, fletxes, math."""
        cleaned = []
        for c in text:
            cp = ord(c)
            if c in (' ', '\t', '\n', '\r'):
                cleaned.append(c)
            elif 0x20 <= cp <= 0x7E:       # ASCII imprimible
                cleaned.append(c)
            elif 0x00A0 <= cp <= 0x024F:   # Latin Extended (à é í ò ú ç · ñ ü)
                cleaned.append(c)
            elif 0x0600 <= cp <= 0x06FF:   # Àrab
                cleaned.append(c)
            elif 0x2000 <= cp <= 0x206F:   # Puntuació general (— ' " …)
                cleaned.append(c)
            elif 0x2070 <= cp <= 0x209F:   # Superíndexs/subíndexs (₂)
                cleaned.append(c)
            elif 0x20A0 <= cp <= 0x20CF:   # Símbols de moneda (€ £)
                cleaned.append(c)
            elif 0x2190 <= cp <= 0x21FF:   # Fletxes (↓ → ← ↑)
                cleaned.append(c)
            elif 0x2200 <= cp <= 0x22FF:   # Símbols matemàtics (± × ÷)
                cleaned.append(c)
            # Tot el resta (emojis, box-drawing, variation selectors, ZWJ): omès
        return "".join(cleaned)

    def clean_for_plain(text):
        """Neteja markdown per a TXT pla."""
        text = text.replace("**", "").replace("*", "").replace("`", "")
        text = re.sub(r'^#{1,4}\s+', '', text, flags=re.MULTILINE)  # Treure headings #
        text = re.sub(r'^\|[-:\s|]+\|$', '', text, flags=re.MULTILINE)  # Treure separadors taula
        return text

    if fmt == "txt":
        tmp = Path(tempfile.gettempdir()) / f"{base_name}.txt"
        clean_adapted = clean_for_plain(adapted)
        content = f"ADAPTACIÓ ATNE — {profile_name}\n{'='*50}\n\n{clean_adapted}\n\n{'='*50}\nTEXT ORIGINAL:\n\n{original}"
        # BOM UTF-8 perquè Windows/Notepad el reconegui correctament
        with open(tmp, "w", encoding="utf-8-sig") as f:
            f.write(content)
        return FileResponse(tmp, filename=f"{base_name}.txt", media_type="text/plain; charset=utf-8")

    elif fmt == "docx":
        from docx import Document as DocxDocument
        from docx.shared import Pt
        doc = DocxDocument()
        doc.add_heading(f"Adaptació ATNE — {profile_name}", level=1)
        # Text adaptat + complements (tot el contingut)
        for line in adapted.split("\n"):
            stripped = line.strip()
            if line.startswith("## "):
                doc.add_heading(line[3:].replace("**", ""), level=2)
            elif line.startswith("### "):
                doc.add_heading(line[4:].replace("**", ""), level=3)
            elif stripped.startswith("|"):
                clean = stripped.replace("|", "  ").strip()
                if clean and not all(c in "-: " for c in clean):
                    p = doc.add_paragraph(clean)
                    p.style.font.size = Pt(9)
            elif stripped.startswith("```"):
                continue
            elif re.match(r'^[\s]*[-*]\s+(?!\*)', line) and not stripped.startswith("**"):
                clean = re.sub(r'^[\s]*[-*]\s+', '', line).strip()
                doc.add_paragraph(clean.replace("**", ""), style="List Bullet")
            elif re.match(r'^[\s]*\d+\.\s+', line):
                clean = re.sub(r'^[\s]*\d+\.\s+', '', line).strip()
                doc.add_paragraph(clean.replace("**", ""), style="List Number")
            elif stripped:
                p = doc.add_paragraph()
                # Gestionar negretes inline
                parts = re.split(r'(\*\*.*?\*\*)', stripped)
                for part in parts:
                    if part.startswith("**") and part.endswith("**"):
                        run = p.add_run(part[2:-2])
                        run.bold = True
                    else:
                        p.add_run(part)
        # Separador + text original
        doc.add_page_break()
        doc.add_heading("Text original", level=2)
        for line in original.split("\n"):
            if line.strip():
                doc.add_paragraph(line)
        tmp = Path(tempfile.gettempdir()) / f"{base_name}.docx"
        doc.save(str(tmp))
        return FileResponse(tmp, filename=f"{base_name}.docx",
                          media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

    elif fmt == "pdf":
        from fpdf import FPDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        # Font Unicode del sistema (Arial suporta català, àrab, etc.)
        font_name = "Helvetica"  # fallback
        for ttf_normal, ttf_bold, fname in [
            ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf", "ArialUni"),
            ("C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/segoeuib.ttf", "SegoeUI"),
            # Linux (Cloud Run / Docker)
            ("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
             "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", "LiberationSans"),
            ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
             "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "DejaVuSans"),
        ]:
            if Path(ttf_normal).exists():
                try:
                    pdf.add_font(fname, "", ttf_normal)
                    pdf.add_font(fname, "B", ttf_bold)
                    font_name = fname
                    break
                except Exception:
                    continue
        pdf.add_page()
        w = pdf.w - pdf.l_margin - pdf.r_margin  # amplada efectiva

        def pdf_clean(txt):
            """Neteja markdown inline i caràcters no-renderitzables per PDF."""
            txt = pdf_safe(txt)
            return txt.replace("**", "").replace("*", "").replace("`", "")

        def pdf_write_line(line):
            """Escriu una línia al PDF amb detecció de format."""
            stripped = line.strip()
            if not stripped:
                pdf.ln(3)
                return
            # Heading ##
            if line.startswith("## "):
                pdf.set_font(font_name, "B", 13)
                pdf.ln(4)
                pdf.multi_cell(w, 8, pdf_clean(line[3:]), align="L",
                               new_x="LMARGIN", new_y="NEXT")
                pdf.set_font(font_name, "", 11)
                pdf.ln(2)
            # Heading ###
            elif line.startswith("### "):
                pdf.set_font(font_name, "B", 11)
                pdf.ln(2)
                pdf.multi_cell(w, 7, pdf_clean(line[4:]), align="L",
                               new_x="LMARGIN", new_y="NEXT")
                pdf.set_font(font_name, "", 11)
            # Taules markdown
            elif stripped.startswith("|"):
                clean = stripped.replace("|", "  ").strip()
                # Saltar línies separadores (|---|---|)
                if clean and not all(c in "-: " for c in clean):
                    pdf.set_font(font_name, "", 9)
                    pdf.multi_cell(w, 5, pdf_clean(clean), align="L",
                                   new_x="LMARGIN", new_y="NEXT")
                    pdf.set_font(font_name, "", 11)
            # Bloc de codi
            elif stripped.startswith("```"):
                pass  # Saltar delimitadors
            # Bullets: "- text" o "* text" (però NO "**negreta**")
            elif re.match(r'^[\s]*[-*]\s+(?!\*)', line) and not stripped.startswith("**"):
                clean = re.sub(r'^[\s]*[-*]\s+', '', line).strip()
                pdf.multi_cell(w, 6, f"  - {pdf_clean(clean)}", align="L",
                               new_x="LMARGIN", new_y="NEXT")
            # Llistes numerades: "1. text"
            elif re.match(r'^[\s]*\d+\.\s+', line):
                clean = re.sub(r'^[\s]*\d+\.\s+', '', line).strip()
                num = re.match(r'[\s]*(\d+)\.', line).group(1)
                pdf.multi_cell(w, 6, f"  {num}. {pdf_clean(clean)}", align="L",
                               new_x="LMARGIN", new_y="NEXT")
            # Línia normal
            else:
                pdf.multi_cell(w, 6, pdf_clean(stripped), align="L",
                               new_x="LMARGIN", new_y="NEXT")

        pdf.set_font(font_name, "B", 16)
        pdf.cell(w, 10, pdf_safe(f"Adaptació ATNE — {profile_name}"), new_x="LMARGIN", new_y="NEXT")
        pdf.set_font(font_name, "", 11)
        pdf.ln(5)

        for line in adapted.split("\n"):
            pdf_write_line(line)

        # Text original
        pdf.add_page()
        pdf.set_font(font_name, "B", 13)
        pdf.cell(w, 10, "Text original", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font(font_name, "", 11)
        pdf.ln(3)
        for orig_line in original.split("\n"):
            if orig_line.strip():
                pdf.multi_cell(w, 6, pdf_safe(orig_line), align="L",
                               new_x="LMARGIN", new_y="NEXT")
            else:
                pdf.ln(3)
        # Footer
        pdf.ln(10)
        pdf.set_font(font_name, "", 8)
        pdf.cell(w, 5, "Generat per ATNE — Jesuïtes Educació",
                 new_x="LMARGIN", new_y="NEXT", align="C")
        tmp = Path(tempfile.gettempdir()) / f"{base_name}.pdf"
        pdf.output(str(tmp))
        return FileResponse(tmp, filename=f"{base_name}.pdf", media_type="application/pdf")

    return JSONResponse({"error": f"Format '{fmt}' no suportat"}, status_code=400)


# ── Main ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print("=" * 50)
    print("  ATNE — Adaptador de Textos")
    print(f"  http://localhost:{port}")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=port)
