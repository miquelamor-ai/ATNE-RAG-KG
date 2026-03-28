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

import corpus_reader
import requests
import uvicorn
from dotenv import load_dotenv
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


# ── System prompt per Gemini ───────────────────────────────────────────────

# ── Prompt v2 RAG: instruccions carregades del corpus (no hardcoded) ──────
# Inicialitzar cache del corpus al arrencar
corpus_reader.load_corpus()
_corpus_stats = corpus_reader.get_all_loaded_stats()
print(f"[corpus_reader] Carregat: {len(_corpus_stats['profiles'])} perfils, "
      f"{len(_corpus_stats['mecr'])} MECR, {len(_corpus_stats['dua'])} DUA, "
      f"{len(_corpus_stats['genres'])} gèneres, {_corpus_stats['crossings']} creuaments")


def _get_active_profiles(profile: dict) -> list[str]:
    """Retorna llista de claus de perfils actius."""
    chars = profile.get("caracteristiques", {})
    return [key for key, val in chars.items() if val.get("actiu")]


def build_persona_audience(profile: dict, context: dict, mecr: str) -> str:
    """Genera narrativa concreta de l'alumne (persona-audience pattern)."""
    chars = profile.get("caracteristiques", {})
    parts = []

    etapa = context.get("etapa", "ESO")
    curs = context.get("curs", "")
    parts.append(f"Escrius per a un alumne de {etapa}")
    if curs:
        parts.append(f"({curs})")

    for key, val in chars.items():
        if not val.get("actiu"):
            continue
        if key == "nouvingut":
            l1 = val.get("L1", "desconeguda")
            mesos = val.get("mesos_a_catalunya", "")
            parts.append(f"nouvingut, L1 {l1}")
            if mesos:
                parts.append(f"{mesos} mesos a Catalunya")
            if val.get("escolaritzacio_previa") == "no":
                parts.append("sense escolarització prèvia regular")
        elif key == "tea":
            nivell = val.get("nivell_suport", 1)
            parts.append(f"amb TEA nivell {nivell}")
        elif key == "tdah":
            pres = val.get("presentacio", "combinat")
            parts.append(f"amb TDAH ({pres})")
        elif key == "dislexia":
            parts.append("amb dislèxia")
        elif key == "altes_capacitats":
            parts.append("amb altes capacitats")
        elif key == "di":
            parts.append("amb discapacitat intel·lectual")
        else:
            parts.append(f"amb {key.replace('_', ' ')}")

    parts.append(f"Nivell MECR: {mecr}.")
    obs = profile.get("observacions", "")
    if obs:
        parts.append(f"Observació docent: {obs}")

    return " ".join(parts)


def build_system_prompt(profile: dict, context: dict, params: dict, rag_context: str) -> str:
    """Munta el system prompt v2 en 4 capes — instruccions llegides del corpus MD."""
    parts = []

    # ═══ CAPA 1: IDENTITAT (fixa) ═══
    parts.append(corpus_reader.get_identity())

    # ═══ CAPA 2: INSTRUCCIONS UNIVERSALS (fixa) ═══
    parts.append(corpus_reader.get_universal_rules())

    # ═══ CAPA 3: INSTRUCCIONS CONDICIONALS (variable — del corpus) ═══
    mecr = params.get("mecr_sortida", "B2")
    dua = params.get("dua", "Core")

    # 3a. MECR (només 1 nivell)
    mecr_block = corpus_reader.get_mecr_block(mecr)
    if mecr_block:
        parts.append(mecr_block)

    # 3b. DUA
    dua_block = corpus_reader.get_dua_block(dua)
    if dua_block:
        parts.append(dua_block)

    # 3c. Gènere discursiu (si indicat)
    genre = params.get("genere_discursiu", "")
    if genre:
        genre_block = corpus_reader.get_genre_block(genre)
        if genre_block:
            parts.append(genre_block)

    # 3d. Perfils actius (només els que s'apliquen)
    active_profiles = _get_active_profiles(profile)
    for pkey in active_profiles:
        pblock = corpus_reader.get_profile_block(pkey)
        if pblock:
            parts.append(pblock)

    # 3e. Creuaments (si 2+ perfils actius)
    crossing_blocks = corpus_reader.get_crossing_blocks(active_profiles)
    for cb_text in crossing_blocks:
        parts.append(cb_text)

    # 3f. Càrrega cognitiva
    cog_block = corpus_reader.get_cognitive_load_block(mecr)
    if cog_block:
        parts.append(cog_block)

    # 3g. Resolució conflictes (si nivell baix o DUA Accés)
    if mecr in ("pre-A1", "A1", "A2") or dua == "Acces":
        conflict = corpus_reader.get_conflict_resolution()
        if conflict:
            parts.append(conflict)

    # 3h. Few-shot example
    fewshot = corpus_reader.get_fewshot_example(mecr)
    if fewshot:
        parts.append(f"EXEMPLE DE SORTIDA ESPERADA ({mecr}):\n{fewshot}")

    # ═══ CAPA 4: CONTEXT (variable) ═══

    # 4a. Context educatiu
    parts.append(f"""CONTEXT EDUCATIU:
- Etapa: {context.get('etapa', 'ESO')}
- Curs: {context.get('curs', '')}
- Àmbit: {context.get('ambit', '')}
- Matèria: {context.get('materia', '')}""")

    # 4b. Persona-audience
    persona = build_persona_audience(profile, context, mecr)
    parts.append(f"PERSONA-AUDIENCE:\n{persona}")

    # 4c. Context RAG pedagògic
    if rag_context:
        parts.append(f"CONEIXEMENT PEDAGÒGIC DE REFERÈNCIA (corpus FJE):\n{rag_context}")

    # Complements activats
    comp = params.get("complements", {})
    comp_actius = [k.replace("_", " ").title() for k, v in comp.items() if v]
    parts.append(f"""
COMPLEMENTS A GENERAR (a més del text adaptat):
{chr(10).join('- ' + c for c in comp_actius) if comp_actius else '- Cap complement addicional'}
""")

    # Instruccions de sortida — detallades per complement
    # Detectar quins complements estan actius per donar instruccions específiques
    comp = params.get("complements", {})
    # Extreure L1 del perfil nouvingut (si existeix)
    chars = profile.get("caracteristiques", {})
    l1 = chars.get("nouvingut", {}).get("L1", "")
    l1_display = l1 if l1 else "la llengua materna de l'alumne"

    output_sections = []
    output_sections.append("""
FORMAT DE SORTIDA:
Respon EXACTAMENT amb les seccions següents, separades per encapçalaments ## .
Genera NOMÉS les seccions indicades com ACTIVADES.

## Text adaptat
El text complet adaptat segons tots els paràmetres indicats.
- Estructura clara amb salts de línia entre idees
- Termes tècnics en **negreta** amb definició entre parèntesis la primera vegada
- Una idea per frase
- Si el nivell és A1 o inferior: frases molt curtes, vocabulari quotidià, sense subordinades
""")

    if comp.get("glossari"):
        output_sections.append(f"""
## Glossari
ACTIVAT — Genera una TAULA MARKDOWN amb 3 columnes:
| Terme | Traducció ({l1_display}) | Explicació simple |
Inclou tots els termes tècnics o difícils del text adaptat (mínim 8-12 termes).
La columna de traducció ha de contenir la traducció REAL al/a la {l1_display} (en el seu alfabet original si escau: àrab, xinès, urdú, etc.).
L'explicació ha de ser en català molt senzill (nivell A1).
""")

    if comp.get("negretes"):
        output_sections.append("""
## Negretes
ACTIVAT — Ja integrat al text adaptat (termes clau en **negreta**). No cal secció separada.
""")

    if comp.get("definicions_integrades"):
        output_sections.append("""
## Definicions integrades
ACTIVAT — Ja integrat al text adaptat (definicions entre parèntesis). No cal secció separada.
""")

    if comp.get("traduccio_l1"):
        output_sections.append(f"""
## Traducció L1
ACTIVAT — Ja integrat al glossari (columna de traducció a {l1_display}). No cal secció separada.
""")

    if comp.get("pictogrames"):
        output_sections.append("""
## Pictogrames
ACTIVAT — Afegeix icones/emojis de suport al costat dels conceptes clau del text adaptat.
Exemples: ☀️ per llum, 💧 per aigua, 🌱 per planta, 🔬 per ciència, etc.
Integra'ls directament al text adaptat, no en secció separada.
""")

    if comp.get("esquema_visual"):
        output_sections.append("""
## Esquema visual
ACTIVAT — Genera un esquema/diagrama en format text que mostri el procés o les relacions del contingut.
Format: usa fletxes (→, ↓), símbols (+, =) i emojis per fer-lo visual i intuïtiu.
Exemple de format:
```
ELEMENT A ☀️
  ↓
+ ELEMENT B 💧
  ↓
RESULTAT → PRODUCTE 1 + PRODUCTE 2
```
Ha de ser senzill, visual i comprensible per a l'alumne.
""")

    if comp.get("mapa_conceptual"):
        output_sections.append("""
## Mapa conceptual
ACTIVAT — Genera un mapa conceptual en format text amb estructura d'arbre.
Format:
```
CONCEPTE CENTRAL
│
├── Branca 1:
│   ├─ Element a
│   └─ Element b
│
├── Branca 2:
│   └─ Element c
│
└── Branca 3:
    ├─ Element d
    └─ Element e
```
Mostra les relacions jeràrquiques entre els conceptes principals del text.
""")

    if comp.get("preguntes_comprensio"):
        output_sections.append("""
## Preguntes de comprensió
ACTIVAT — Genera preguntes GRADUADES en 3 nivells de dificultat:

### Nivell 1: Resposta curta (reconeixement)
3 preguntes que es responen buscant informació directa al text.

### Nivell 2: Verdader o fals
3 afirmacions per marcar ✅ o ❌, barrejant correctes i incorrectes.

### Nivell 3: Relaciona o completa
2-3 activitats de relacionar conceptes (amb fletxes) o completar frases.

Adapta la dificultat de les preguntes al nivell MECR de sortida.
""")

    if comp.get("activitats_aprofundiment"):
        output_sections.append("""
## Activitats d'aprofundiment
ACTIVAT — Genera 2-3 activitats de repte cognitiu:
- Connexions interdisciplinars
- Pensament crític (per què? i si...?)
- Recerca guiada
- Debat o reflexió
""")

    if comp.get("bastides"):
        output_sections.append(f"""
## Bastides (scaffolding)
ACTIVAT — Genera suports didàctics estructurats en 4 blocs:

### Frases model
3-5 frases incompletes que l'alumne ha de completar amb informació del text.
Exemple: "Les plantes necessiten ______ per fer la fotosíntesi."

### Banc de paraules
Llista de 8-12 paraules clau que l'alumne pot usar per completar les frases i activitats.
Format: paraula1 – paraula2 – paraula3 – ...

### Suport visual
Indica quins suports visuals usar (icones, colors, esquemes, imatges recomanades).

### Suport L1
Si l'alumne és nouvingut, inclou pistes en {l1_display} per als conceptes més abstractes.
""")

    if comp.get("mapa_mental"):
        output_sections.append("""
## Mapa mental
ACTIVAT — Genera un mapa mental radial (diferent del mapa conceptual).
El concepte central al mig, amb branques que s'expandeixen amb associacions lliures,
preguntes generadores i connexions amb altres matèries.
""")

    # Sempre: argumentació pedagògica + auditoria
    output_sections.append("""
## Argumentació pedagògica
SEMPRE GENERAR — Explica les decisions pedagògiques preses, organitzades per àrees:
1. **Adaptació lingüística**: què s'ha simplificat i per què (nivell MECR, tipus de frases, vocabulari)
2. **Atenció a la diversitat**: com s'han tingut en compte les necessitats específiques (dislèxia, TEA, nouvingut, etc.)
3. **Suport multimodal**: quins canals s'han activat (visual, lingüístic, cognitiu) i per què
4. **Gradació cognitiva**: com s'ha organitzat la progressió (de reconeixement a producció)
5. **Rigor curricular**: quins continguts s'han mantingut íntegres i per què
Breu, 3-5 punts amb explicació de 1-2 frases cadascun.

## Notes d'auditoria
SEMPRE GENERAR — Taula comparativa breu dels canvis principals:
| Aspecte | Original | Adaptat | Motiu |
Màxim 5-6 files amb els canvis més significatius.
""")

    output_sections.append("""
Omès les seccions marcades com NO ACTIVADES. No generis seccions buides.
""")

    parts.append("\n".join(output_sections))

    return "\n".join(parts)


# ── Post-processament Python (verificació post-LLM) ──────────────────────

MECR_MAX_WORDS = {"pre-A1": 5, "A1": 8, "A2": 12, "B1": 18, "B2": 25}
FORBIDDEN_WORDS = ["cosa", "coses", "allò", "el que fa que", "serveix per", "un tipus de"]


def post_process_adaptation(text: str, mecr: str) -> dict:
    """Verificació post-LLM amb Python. Retorna warnings i mètriques."""
    warnings = []
    max_words = MECR_MAX_WORDS.get(mecr, 25)

    # 1. Longitud de frases
    sentences = re.split(r'[.!?]\s', text)
    long_sentences = []
    for s in sentences:
        s = s.strip()
        if not s or s.startswith("#") or s.startswith("|") or s.startswith("-"):
            continue
        wcount = len(s.split())
        if wcount > max_words + 3:  # marge de 3 paraules
            long_sentences.append((s[:60] + "...", wcount))
    if long_sentences:
        warnings.append(
            f"⚠ {len(long_sentences)} frases superen {max_words} paraules (MECR {mecr})")

    # 2. Paraules prohibides
    text_lower = text.lower()
    found_forbidden = [w for w in FORBIDDEN_WORDS if w in text_lower]
    if found_forbidden:
        warnings.append(f"⚠ Paraules prohibides detectades: {', '.join(found_forbidden)}")

    # 3. Mètriques bàsiques
    words = len(text.split())
    bold_terms = len(re.findall(r'\*\*[^*]+\*\*', text))
    headings = len(re.findall(r'^##+ ', text, re.MULTILINE))

    return {
        "warnings": warnings,
        "metrics": {
            "paraules": words,
            "frases": len(sentences),
            "termes_negreta": bold_terms,
            "encapcalaments": headings,
            "frases_llargues": len(long_sentences),
        },
    }


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
    except Exception as e:
        adapted = f"Error en la generació: {e}"

    # 6. Post-processament Python
    mecr = params.get("mecr_sortida", "B2")
    pp = post_process_adaptation(adapted, mecr)
    for w in pp.get("warnings", []):
        cb({"type": "step", "step": "warning", "msg": w})

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
