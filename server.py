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
import instruction_filter
import requests
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Body, HTTPException, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse, FileResponse

# ── Configuració ────────────────────────────────────────────────────────────

load_dotenv()

GEMINI_API_KEYS = [k for k in [os.getenv(f"GEMINI_API_KEY{s}", "")
                                for s in ["", "_3", "_4", "_5", "_6", "_7"]] if k]
GEMINI_API_KEY = GEMINI_API_KEYS[0] if GEMINI_API_KEYS else ""
_gemini_key_idx = 0  # índex actual de rotació
GEMMA4_API_KEYS = [k for k in [os.getenv(f"GEMMA4_API_KEY{s}", "")
                                for s in ["", "_2", "_3", "_4", "_5", "_6", "_7"]] if k]
GEMMA4_API_KEY = GEMMA4_API_KEYS[0] if GEMMA4_API_KEYS else ""
_gemma4_key_idx = 0  # índex actual de rotació
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
# ATNE_MODEL: gemini | gemma4 | mistral
# Per defecte gemma4 (decidit pel pilot 2026-04-12). Mistral disponible al codi
# però amagat de la UI; s'activarà al pilot HITL cec a partir del 20/04.
ATNE_MODEL = os.getenv("ATNE_MODEL", "gemma4").lower()
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

# Client Gemini (SDK google-genai) — serveix per Gemini i Gemma 4
from google import genai
from google.genai import types

# Triem clau segons ATNE_MODEL
_genai_key = GEMMA4_API_KEY if ATNE_MODEL == "gemma4" else GEMINI_API_KEY
gemini_client = genai.Client(
    api_key=_genai_key or GEMMA4_API_KEY or GEMINI_API_KEY,
    http_options=types.HttpOptions(timeout=300_000),  # 5min per generacions llargues
) if (_genai_key or GEMMA4_API_KEY or GEMINI_API_KEY) else None

print(f"[ATNE] Model actiu: {ATNE_MODEL}")

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
        ".html": "text/html",
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
    tdl_grau = characteristics.get("tdl", {}).get("grau", "lleu")
    if (di_grau == "sever" and "di" in actives) or \
       (tea_nivell == 3 and "tea" in actives) or \
       (tdl_grau == "sever" and "tdl" in actives) or \
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
        dislexia_grau = characteristics.get("dislexia", {}).get("grau", "lleu")
        lf_factors.append({"sever": 4, "moderat": 3, "lleu": 3}.get(dislexia_grau, 3))
    if "tdl" in actives:
        tdl_grau = characteristics.get("tdl", {}).get("grau", "lleu")
        lf_factors.append({"sever": 4, "moderat": 3, "lleu": 3}.get(tdl_grau, 3))
    if "tdah" in actives:
        tdah_grau = characteristics.get("tdah", {}).get("grau", "lleu")
        lf_factors.append({"sever": 3, "moderat": 2, "lleu": 2}.get(tdah_grau, 2))
    if "altes_capacitats" in actives:
        lf_factors.append(1)
    if lf_factors:
        lf = max(lf_factors)

    # ── MECR sortida ──
    # Cada perfil amb barrera lingüística real proposa un MECR candidat.
    # S'agafa el MÉS BAIX (més restrictiu) de tots els candidats.
    # Perfils sense barrera lingüística (TEA, TDAH, dislèxia, disc_visual,
    # disc_motora, trastorn_emocional) NO proposen MECR — usen el default d'etapa.
    # Font: docs/investigacio/mapa_barreres_perfil.md
    MECR_ORDER = ["pre-A1", "A1", "A2", "B1", "B2", "C1"]
    etapa_defaults = {
        "infantil": "A1", "primaria": "B1", "ESO": "B2",
        "batxillerat": "B2", "FP": "B2",
    }
    mecr_base = etapa_defaults.get(etapa, "B2")
    mecr_candidats = []

    # Nouvingut: MECR explícit triat pel docent
    if "nouvingut" in actives and mecr:
        mecr_candidats.append(mecr)

    # DI: barrera cognitiva → lingüística
    if "di" in actives:
        mecr_candidats.append(
            {"sever": "A1", "moderat": "A2", "lleu": "B1"}.get(di_grau, "B1"))

    # TDL: barrera lèxica i sintàctica directa (Bishop 2017)
    if "tdl" in actives:
        mecr_candidats.append(
            {"sever": "A1", "moderat": "A2", "lleu": "B1"}.get(tdl_grau, "B1"))

    # Disc. auditiva prelocutiva (LSC): català escrit funciona com L2
    if "disc_auditiva" in actives and disc_auditiva.get("comunicacio") == "LSC":
        mecr_candidats.append("A1")

    # Vulnerabilitat socioeducativa: retard lector per manca d'estimulació
    # Redueix 1 nivell respecte l'etapa (no tant com DI o TDL)
    if "vulnerabilitat" in actives:
        idx = MECR_ORDER.index(mecr_base)
        mecr_candidats.append(MECR_ORDER[max(0, idx - 1)])

    # Altes capacitats (sense 2e): pujar 1 nivell per permetre més complexitat
    if "altes_capacitats" in actives and not ac_doble:
        idx = MECR_ORDER.index(mecr_base)
        mecr_candidats.append(MECR_ORDER[min(len(MECR_ORDER) - 1, idx + 1)])

    # Resolució: el més restrictiu guanya (excepte si altes_capacitats és l'únic)
    if mecr_candidats:
        mecr_sortida = min(mecr_candidats, key=lambda m: MECR_ORDER.index(m)
                          if m in MECR_ORDER else 99)
    else:
        mecr_sortida = mecr_base

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


def _str_to_bool(val) -> bool:
    """Converteix string a bool de forma tolerant."""
    if isinstance(val, bool):
        return val
    if isinstance(val, str):
        return val.lower() in ("true", "1", "sí", "si")
    return bool(val)


def build_persona_audience(profile: dict, context: dict, mecr: str) -> str:
    """
    Genera narrativa concreta de l'alumne (persona-audience pattern).

    Aprofita TOTES les sub-variables de tipus NARRATIVA per donar a l'LLM
    una imatge rica de per a qui escriu, no només etiquetes abstractes.
    """
    chars = profile.get("caracteristiques", {})
    lines = []

    etapa = context.get("etapa", "ESO")
    curs = context.get("curs", "")
    header = f"Escrius per a un alumne de {etapa}"
    if curs:
        header += f" ({curs})"
    lines.append(header + ".")

    for key, val in chars.items():
        if not val.get("actiu"):
            continue

        if key == "nouvingut":
            l1 = val.get("L1", "")
            frag = "Alumne nouvingut"
            if l1:
                frag += f" que parla {l1} com a L1"
            lines.append(frag + ".")

            alfabet = val.get("alfabet_llati", True)
            if isinstance(alfabet, str):
                alfabet = alfabet.lower() not in ("no", "false", "0")
            if not alfabet:
                lines.append("Alfabet no llatí: necessita transliteració fonètica.")

            esc = val.get("escolaritzacio_previa", "si")
            if esc == "no":
                lines.append("No ha estat escolaritzat regularment al seu país d'origen. No familiaritzat amb gèneres escolars.")
            elif esc == "parcial":
                lines.append("Escolarització prèvia parcial o interrompuda.")

            calp = val.get("calp", "")
            if calp == "inicial":
                lines.append("Llengua acadèmica (CALP) inicial: no domina el registre escolar ni vocabulari abstracte de les matèries. Termes com 'justifica', 'argumenta', 'analitza' poden ser incomprensibles.")
            elif calp == "emergent":
                lines.append("Llengua acadèmica (CALP) emergent: entén consignes bàsiques però li costa el vocabulari abstracte.")

        elif key == "tea":
            nivell = val.get("nivell_suport", "1")
            com = val.get("comunicacio_oral", "fluida")
            frag = f"TEA, nivell de suport {nivell} (DSM-5)"
            if com == "no_verbal":
                frag += ". Comunicació oral no verbal: depèn totalment del canal visual i escrit"
            elif com == "limitada":
                frag += ". Comunicació oral limitada: necessita més suport visual"
            lines.append(frag + ".")

        elif key == "tdah":
            pres = val.get("presentacio", "combinat")
            grau = val.get("grau", "")
            frag = f"TDAH, presentació {pres}"
            if grau:
                frag += f" (grau {grau})"
            lines.append(frag + ".")

            if _str_to_bool(val.get("baixa_memoria_treball", False)):
                lines.append("Memòria de treball baixa: limitar elements simultanis, repetir informació clau.")
            if _str_to_bool(val.get("fatiga_cognitiva", False)):
                lines.append("Fatiga cognitiva: es cansa ràpid amb textos llargs, necessita text reduït i pauses visuals.")

        elif key == "dislexia":
            tipus = val.get("tipus_dislexia", "")
            grau = val.get("grau", "")
            frag = "Dislèxia"
            if tipus:
                frag += f" {tipus}"
            if grau:
                frag += f" (grau {grau})"
            lines.append(frag + ".")

        elif key == "altes_capacitats":
            tipus = val.get("tipus_capacitat", "global")
            if tipus == "talent_especific":
                lines.append("Altes capacitats: talent específic. NO simplificar. Enriquir amb profunditat i connexions interdisciplinars.")
            else:
                lines.append("Altes capacitats globals. NO simplificar. Enriquir amb profunditat i connexions interdisciplinars.")

        elif key in ("di", "discapacitat_intellectual"):
            grau = val.get("grau", "lleu")
            lines.append(f"Discapacitat intel·lectual (grau {grau}). Necessita concreció radical i repetició sistemàtica.")

        elif key == "tdl":
            modalitat = val.get("modalitat", "")
            grau = val.get("grau", "")
            frag = "TDL (Trastorn del Llenguatge)"
            if modalitat:
                frag += f", afectació {modalitat}"
            if grau:
                frag += f" (grau {grau})"
            lines.append(frag + ".")

            afectacions = []
            if _str_to_bool(val.get("morfosintaxi", False)):
                afectacions.append("morfosintaxi")
            if _str_to_bool(val.get("semantica", False)):
                afectacions.append("semàntica/lèxic")
            if _str_to_bool(val.get("pragmatica", False)):
                afectacions.append("pragmàtica")
            if _str_to_bool(val.get("discurs_narrativa", False)):
                afectacions.append("discurs/narrativa")
            if afectacions:
                lines.append(f"Àrees afectades: {', '.join(afectacions)}.")

            if _str_to_bool(val.get("bilingue", False)):
                lines.append("Context bilingüe/plurilingüe.")

        elif key in ("disc_visual", "discapacitat_visual"):
            grau = val.get("grau", "baixa_visio_moderada")
            etiquetes = {
                "baixa_visio_moderada": "baixa visió moderada",
                "baixa_visio_greu": "baixa visió greu",
                "ceguesa": "ceguesa",
            }
            lines.append(f"Discapacitat visual: {etiquetes.get(grau, grau)}.")

        elif key in ("disc_auditiva", "discapacitat_auditiva"):
            com = val.get("comunicacio", "oral")
            impl = _str_to_bool(val.get("implant_coclear", False))
            frag = "Discapacitat auditiva"
            if com == "LSC":
                frag += ", comunicació en Llengua de Signes Catalana. Tractar el català escrit com a L2"
            elif com == "bimodal":
                frag += ", comunicació bimodal (oral + signes)"
            if impl:
                frag += ". Porta implant coclear (accés auditiu parcial)"
            lines.append(frag + ".")

        elif key == "trastorn_emocional":
            if _str_to_bool(val.get("sensibilitat_tematica", False)):
                lines.append("Trastorn emocional/conductual. Sensibilitat temàtica: evitar temes de violència, separació, mort.")
            else:
                lines.append("Trastorn emocional/conductual.")

        elif key == "vulnerabilitat":
            if _str_to_bool(val.get("sensibilitat_tematica", False)):
                lines.append("Vulnerabilitat socioeducativa. Sensibilitat temàtica: evitar temes potencialment traumàtics.")
            else:
                lines.append("Vulnerabilitat socioeducativa.")

        elif key == "tdc":
            grau = val.get("grau", "")
            frag = "TDC/Dispraxia"
            if grau:
                frag += f" (grau {grau})"
            lines.append(frag + ".")

        elif key == "2e":
            lines.append("Doble excepcionalitat (2e): combina altes capacitats amb una necessitat d'accessibilitat. Mantenir repte intel·lectual ALT amb suports de format.")

        else:
            lines.append(f"Amb {key.replace('_', ' ')}.")

    lines.append(f"Nivell MECR de sortida: {mecr}.")

    obs = profile.get("observacions", "")
    if obs:
        lines.append(f"Observació del docent: {obs}")

    return "\n".join(lines)


def build_system_prompt(profile: dict, context: dict, params: dict, rag_context: str = "") -> str:
    """Munta el system prompt en 4 capes — instruccions graduades del catàleg de 98."""
    parts = []
    mecr = params.get("mecr_sortida", "B2")
    dua = params.get("dua", "Core")

    # ═══ CAPA 1: IDENTITAT (fixa) ═══
    parts.append(corpus_reader.get_identity())

    # ═══ CAPES 2-3: INSTRUCCIONS FILTRADES (catàleg de 89 instruccions LLM) ═══
    # Filtra segons perfils actius, sub-variables, MECR, DUA i complements
    filtered = instruction_filter.get_instructions(profile, params)
    instructions_text = instruction_filter.format_instructions_for_prompt(filtered)
    parts.append(instructions_text)

    # DUA (bloc del corpus — complementa les instruccions filtrades)
    dua_block = corpus_reader.get_dua_block(dua)
    if dua_block:
        parts.append(dua_block)

    # Gènere discursiu (si indicat)
    genre = params.get("genere_discursiu", "")
    if genre:
        genre_block = corpus_reader.get_genre_block(genre)
        if genre_block:
            parts.append(genre_block)

    # Creuaments (si 2+ perfils actius)
    active_profiles = _get_active_profiles(profile)
    crossing_blocks = corpus_reader.get_crossing_blocks(active_profiles)
    for cb_text in crossing_blocks:
        parts.append(cb_text)

    # Resolució conflictes: ELIMINAT (2026-04-09) — redundant amb A-26 graduada per MECR
    # Few-shot example: ELIMINAT (2026-04-09) — un sol domini (fotosíntesi), risc sobreajust. Parking lot.

    # ═══ CAPA 4: CONTEXT (variable) ═══

    # 4a. Context educatiu: ELIMINAT del prompt (2026-04-09)
    # L'etapa/curs s'usen al Python (propose_adaptation) per calcular MECR,
    # però l'LLM no els necessita — ja rep les instruccions filtrades pel MECR correcte.

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
        is_nouvingut = "nouvingut" in [k for k, v in chars.items() if v.get("actiu")]
        if is_nouvingut and l1:
            output_sections.append(f"""
## Glossari
ACTIVAT — Genera una TAULA MARKDOWN amb 3 columnes:
| Terme | Traducció ({l1_display}) | Explicació simple |
Inclou tots els termes tècnics o difícils del text adaptat (mínim 8-12 termes).
La columna de traducció ha de contenir la traducció REAL al/a la {l1_display} (en el seu alfabet original si escau: àrab, xinès, urdú, etc.).
L'explicació ha de ser en català molt senzill (nivell A1).
""")
        else:
            output_sections.append("""
## Glossari
ACTIVAT — Genera una TAULA MARKDOWN amb 2 columnes:
| Terme | Explicació simple |
Inclou tots els termes tècnics o difícils del text adaptat (mínim 8-12 termes).
L'explicació ha de ser en català molt senzill.
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

    # Variables de context per als complements pedagògics (MALL/TILC)
    materia_complement = params.get("materia") or context.get("materia") or "la matèria corresponent"
    etapa_complement = params.get("etapa") or context.get("etapa") or "l'etapa educativa corresponent"
    mecr_complement = params.get("mecr") or "el nivell MECR indicat"
    genere_complement = params.get("genere_discursiu") or "no especificat"
    # Detectar si és text literari o informatiu (heurística a partir del gènere)
    literari_keywords = ("conte", "relat", "poesia", "poema", "llegendari", "fantàstic", "narrativa", "literari")
    es_literari = any(k in genere_complement.lower() for k in literari_keywords)
    modalitat_text = "LITERARI (deixa espais interpretatius, afectius, d'identificació)" if es_literari else "INFORMATIU (precisió conceptual, dades, relacions causa-efecte)"

    if comp.get("preguntes_comprensio"):
        output_sections.append(f"""
## Preguntes de comprensió
ACTIVAT — Genera un guió de comprensió lectora segons el model MALL/TILC
(3 moments × 3 nivells de lectura amb formats variats).

### CONTEXT PEDAGÒGIC (l'has d'usar per modular les preguntes)
- Matèria/àmbit: {materia_complement}
- Etapa: {etapa_complement} · Nivell MECR: {mecr_complement}
- Gènere discursiu: {genere_complement}
- Modalitat del text: {modalitat_text}

### MOMENT 1 — Abans de llegir (activació) · 3 preguntes
Objectiu: activar coneixements previs, formular hipòtesis i fixar propòsit.
Genera:
- **[Hipòtesi]** 1 pregunta sobre el títol o imatges ("De què creus que parlarà…?")
- **[Activació]** 1 pregunta per connectar amb el que l'alumne ja sap
- **[Propòsit]** 1 pregunta sobre què volem aprendre amb aquest text

### MOMENT 2 — Durant la lectura (processament actiu) · 3 preguntes
Objectiu: fer l'alumne lector actiu, que verifiqui hipòtesis i treballi el lèxic.
Genera:
- **[Inferència en curs]** 1 pregunta del tipus "Per què creus que diu…?" o "Què vol dir quan afirma…?"
- **[Visualització]** 1 pregunta per crear imatge mental ("Imagina't…", "Quins sons…", "Com el dibuixaries?")
- **[Lèxic en context]** 1 pregunta per deduir el significat d'una paraula difícil del text a partir del context (no donar la resposta)

### MOMENT 3 — Després de llegir · distribuïdes en 3 nivells de comprensió
Genera **7-8 preguntes en TOTAL**, distribuïdes així i amb FORMATS DIFERENTS
(alterna obertes, verdader/fals, opció múltiple, omplir buits, relaciona amb fletxes):

**Nivell LITERAL** — "Llegir les línies" · 2-3 preguntes
Informació explícita. Exemples de format a alternar:
- **[Literal · oberta curta]** "On vivia…?" / "Què servia per…?"
- **[Literal · V/F amb justificació]** 3 afirmacions on l'alumne marca ✓/✗ i cita la frase que ho demostra
- **[Literal · opció múltiple]** 1 pregunta amb 3-4 opcions (1 correcta)
- **[Literal · omplir buits]** "El ______ es feia servir per ______." (amb o sense banc de paraules)
- **[Literal · relaciona]** 2 columnes (concepte ↔ definició del text)

**Nivell INFERENCIAL** — "Llegir entre línies" · 2-3 preguntes
Deducció, causa-efecte, intencions no explícites:
- **[Inferencial · per què]** "Per què creus que …?"
- **[Inferencial · i si…]** "Què passaria si …?" (contrafactual)
- **[Inferencial · relaciona causa-efecte]** 2 columnes (causa ↔ conseqüència)

**Nivell CRÍTIC/PROFUND** — "Llegir rere les línies" · 2 preguntes
Judici, transferència, connexió amb l'experiència pròpia:
- **[Crític · argumentativa]** Pregunta oberta que demana posició argumentada amb dades del text
  (la bastida al complement Bastides ajudarà a respondre-la)
- **[Crític · jo / transferència]** "Què faries tu si…?" o "Com connecta això amb…?"
  (També vàlid: lectura crítica de biaixos si el text n'ha)

### ADEQUACIÓ PER ETAPA (imprescindible)
- **Infantil / Cicle Inicial (A1)**: predomina predicció visual, connexió amb el jo,
  dibuix. EVITA mots com "justifica" o "argumenta". Preguntes molt curtes i concretes.
- **Cicle Mitjà / Superior primària (A2-B1)**: idea principal, relacions entre idees,
  verificació d'hipòtesis, comparacions.
- **Secundària (B1-B2)**: arguments de l'autor, connectors lògics, contrast de fonts,
  explicar vs justificar (connectar amb el model teòric de la matèria).
- **Batxillerat/FP (C1)**: anàlisi crítica, intertextualitat, biaixos, multiplicitat de fonts.

### DISTINCIÓ LITERARI vs INFORMATIU
- Si és LITERARI: deixa "buits" interpretatius — preguntes afectives, d'identificació,
  d'imatges mentals, de reescriptura creativa.
- Si és INFORMATIU: precisió conceptual — dades, definicions, relacions causa-efecte,
  connexió amb el model teòric de {materia_complement}.

### FORMAT DE SORTIDA
- Cada moment amb encapçalament ### i les preguntes numerades.
- Davant de cada pregunta posa entre claudàtors la ETIQUETA del tipus
  (ex: [Literal · V/F], [Inferencial · per què], [Crític · argumentativa]).
- Si és omplir buits o relacionar, presenta-ho visualment (amb fletxes, guions, etc.).
""")

    if comp.get("activitats_aprofundiment"):
        output_sections.append(f"""
## Activitats d'aprofundiment
ACTIVAT — Genera 2-3 activitats de repte cognitiu per a {etapa_complement}:
- Connexions interdisciplinars amb altres matèries
- Pensament crític (per què? i si…? què passaria si…?)
- Recerca guiada (a casa o a biblioteca)
- Debat o reflexió argumentada
- Si el text ho permet: dimensió plurilingüe (com es diu X en altres llengües de l'aula?)
""")

    if comp.get("bastides"):
        output_sections.append(f"""
## Bastides (scaffolding)
ACTIVAT — Suports didàctics reals per AJUDAR L'ALUMNE A PRODUIR les respostes
(model MALL/TILC: patró lingüístic de la matèria + connectors + lèxic temàtic).

### CONTEXT
- Matèria: {materia_complement}
- Etapa: {etapa_complement} · MECR: {mecr_complement}
- Si l'alumne és nouvingut, L1: {l1_display}

### 1. Taula de connectors lògics
Taula amb els connectors del tipus de raonament que demanen les preguntes:
| Funció | Connectors (adequats al MECR {mecr_complement}) |
|---|---|
| Causa | perquè, com que, ja que, a causa de |
| Conseqüència | per tant, així doncs, en conseqüència, per això |
| Oposició / contrast | però, en canvi, tanmateix, malgrat que |
| Exemplificació | per exemple, com ara, en concret |
| Conclusió | en resum, per acabar, en definitiva |
Adapta la quantitat i complexitat al nivell.

### 2. Frases model per argumentar amb el text
4-6 bastides d'inici de frase perquè l'alumne escrigui respostes ben formulades:
- "Segons el text, ______ perquè ______."
- "Podem deduir que ______ ja que el text diu que ______."
- "A diferència de ______, ______ s'assembla a ______ perquè ______."
- "Un exemple d'això és ______."
- "Jo crec que ______, i ho justifico perquè ______."
Adapta la complexitat al MECR: més simples a A1-A2, més sofisticades a B1-C1.

### 3. Banc de paraules (lèxic temàtic de {materia_complement})
8-12 paraules del patró lingüístic de la matèria, extretes del text o complementàries,
que l'alumne pot usar per respondre. Si escau, agrupa-les per camp semàntic.
Format: paraula1 – paraula2 – paraula3 – …

### 4. Suport visual recomanat
Indica 2-3 suports visuals concrets que afegirien valor (icones, colors destacats,
esquemes, línies de temps, mapes, gràfiques, fotografies…) i on ubicar-los al text.

### 5. Crosses de lectura (abans d'engegar)
2-3 pistes concretes perquè l'alumne enfoqui bé la lectura:
- Què ha de buscar mentre llegeix (1-2 elements clau)?
- Com marcar el que és important (subratllar, prendre nota, fletxes)?
- Quin és el propòsit d'aquesta lectura?

### 6. Suport L1
Si l'alumne és nouvingut, tradueix 5-8 conceptes més abstractes a {l1_display}
(en l'alfabet original si escau: àrab, xinès, urdú, etc.).

### ADEQUACIÓ PER ETAPA
- Infantil / Cicle Inicial: crosses FÍSIQUES i VISUALS (imatges, colors, referents sonors).
- Cicle Mitjà / Superior / ESO: crosses PROCEDIMENTALS (estratègies, plantilles, taules).
- Batxillerat / FP: estratègies de SÍNTESI i anàlisi crítica de múltiples fonts.
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


def _call_llm(active_model: str, system_prompt: str, text: str) -> str:
    """Wrapper unificat de crida al LLM (Mistral o Gemma 4)."""
    global _gemma4_key_idx, _gemini_key_idx
    if active_model == "mistral":
        r = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers={"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": "mistral-small-latest",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"TEXT ORIGINAL A ADAPTAR:\n\n{text}"},
                ],
                "max_tokens": 8192,
                "temperature": 0.4,
            },
            timeout=180,
        )
        if r.status_code != 200:
            raise RuntimeError(f"HTTP {r.status_code}: {r.text[:200]}")
        return r.json()["choices"][0]["message"]["content"] or ""
    elif active_model == "gemma4":
        errors = []
        for attempt in range(len(GEMMA4_API_KEYS)):
            idx = (_gemma4_key_idx + attempt) % len(GEMMA4_API_KEYS)
            client = genai.Client(
                api_key=GEMMA4_API_KEYS[idx],
                http_options=types.HttpOptions(timeout=300_000),
            )
            try:
                response = client.models.generate_content(
                    model="gemma-4-31b-it",
                    contents=[types.Content(role="user", parts=[types.Part(text=f"{system_prompt}\n\n---\n\nTEXT ORIGINAL A ADAPTAR:\n\n{text}")])],
                    config=types.GenerateContentConfig(temperature=0.4, max_output_tokens=8192),
                )
                _gemma4_key_idx = (idx + 1) % len(GEMMA4_API_KEYS)  # rotar per la pròxima crida
                return response.text or ""
            except Exception as e:
                errors.append(f"clau {idx+1}: {e}")
                continue
        raise RuntimeError(f"Totes les claus Gemma4 han fallat: {'; '.join(errors)}")
    elif active_model == "gemini":
        errors = []
        for attempt in range(len(GEMINI_API_KEYS)):
            idx = (_gemini_key_idx + attempt) % len(GEMINI_API_KEYS)
            client = genai.Client(
                api_key=GEMINI_API_KEYS[idx],
                http_options=types.HttpOptions(timeout=300_000),
            )
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[types.Content(role="user", parts=[types.Part(text=text)])],
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        temperature=0.4, max_output_tokens=8192,
                        thinking_config=types.ThinkingConfig(thinking_budget=0),
                    ),
                )
                _gemini_key_idx = (idx + 1) % len(GEMINI_API_KEYS)
                return response.text or ""
            except Exception as e:
                errors.append(f"clau {idx+1}: {e}")
                continue
        raise RuntimeError(f"Totes les claus Gemini han fallat: {'; '.join(errors)}")
    elif active_model == "gpt":
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"TEXT ORIGINAL A ADAPTAR:\n\n{text}"},
            ],
            max_tokens=8192, temperature=0.4,
        )
        return resp.choices[0].message.content or ""
    else:
        raise RuntimeError(f"Model desconegut: {active_model}. Opcions: gemini, gpt, mistral, gemma4")


VERIFY_SYSTEM = """Ets un avaluador pedagògic ràpid. Avalua una adaptació de text educatiu amb 3 criteris breus (1-5 cadascun):
- Q (Qualitat textual): coherència, correcció gramatical, llegibilitat
- P (Perfil): s'ha aplicat bé al perfil de l'alumne declarat
- C (Curricular): preserva el contingut original sense errors

Retorna NOMÉS aquest JSON:
{"Q":1-5,"P":1-5,"C":1-5,"j":"una frase justificació"}"""


def _verify_adaptation(active_model: str, text_original: str, text_adapted: str, profile: dict, params: dict):
    """Autoavaluació ràpida amb 3 criteris. Retorna (mitjana, info)."""
    import re
    perfil_nom = profile.get("nom", "genèric")
    mecr = params.get("mecr_sortida", "B2")
    dua = params.get("dua", "Core")
    user_msg = (
        f"PERFIL: {perfil_nom} | MECR sortida: {mecr} | DUA: {dua}\n\n"
        f"TEXT ORIGINAL:\n{text_original[:2000]}\n\n"
        f"TEXT ADAPTAT:\n{text_adapted[:3000]}\n\n"
        f"Puntua Q, P, C (1-5). JSON nomes."
    )
    raw = _call_llm(active_model, VERIFY_SYSTEM, user_msg)
    # Extreure JSON
    m = re.search(r'\{[^}]*"Q"[^}]*\}', raw, re.DOTALL)
    if not m:
        raise RuntimeError(f"No s'ha trobat JSON a la resposta: {raw[:200]}")
    import json as _json
    data = _json.loads(m.group(0))
    q = float(data.get("Q", 0))
    p = float(data.get("P", 0))
    c = float(data.get("C", 0))
    avg = (q + p + c) / 3
    return avg, {"Q": q, "P": p, "C": c, "j": data.get("j", "")}


def run_adaptation(text: str, profile: dict, context: dict, params: dict,
                   progress_callback=None, model_override: str = None):
    """Executa tot el pipeline d'adaptació: instruccions graduades + LLM + Verify + Retry.

    RAG-KG desactivat (2026-04-09): les 98 instruccions graduades del catàleg
    cobreixen el 'què fer' de forma exhaustiva. El RAG recuperava documents
    irrellevants (M0, perfils equivocats) i el resultat era indistingible.
    La infraestructura RAG-KG (Supabase vectors + KG) es manté per a futur ús
    (diagnòstic, generació de material, recerca).
    """
    cb = progress_callback or (lambda ev: None)
    active_model = (model_override or ATNE_MODEL).lower()

    # System prompt — sense RAG, les instruccions graduades són el motor
    cb({"type": "step", "step": "search", "msg": "Preparant instruccions d'adaptació..."})
    system_prompt = build_system_prompt(profile, context, params, rag_context="")

    # 5. Cridar LLM segons active_model (amb Generate+Verify+Retry)
    model_label = {"gemma4": "Gemma 4 31B", "mistral": "Mistral Small"}.get(active_model, active_model)
    adapted = ""
    verify_enabled = params.get("verify_retry", True)  # per defecte ON
    min_score = 4.0
    max_attempts = 2 if verify_enabled else 1
    best_adapted = ""
    best_score = -1
    verify_info = None

    for attempt in range(1, max_attempts + 1):
        label_attempt = f" (intent {attempt}/{max_attempts})" if verify_enabled else ""
        cb({"type": "step", "step": "adapting", "msg": f"Generant adaptació amb {model_label}{label_attempt}..."})
        try:
            adapted = _call_llm(active_model, system_prompt, text)
            adapted = clean_gemini_output(adapted)
        except Exception as e:
            adapted = f"Error en la generació ({active_model}): {e}"
            break

        if not verify_enabled:
            best_adapted = adapted
            break

        # VERIFY: jutge ràpid amb rúbrica simplificada
        cb({"type": "step", "step": "verifying", "msg": f"Autoavaluant qualitat (intent {attempt})..."})
        try:
            score, verify_info = _verify_adaptation(active_model, text, adapted, profile, params)
            cb({"type": "step", "step": "verify_result", "msg": f"Puntuació autoavaluació: {score:.1f}/5.0"})
        except Exception as e:
            cb({"type": "step", "step": "warning", "msg": f"Avís: autoavaluació fallida ({e}). Conservem aquesta versió."})
            best_adapted = adapted
            break

        if score > best_score:
            best_score = score
            best_adapted = adapted

        if score >= min_score:
            break  # OK

        if attempt < max_attempts:
            cb({"type": "step", "step": "retry", "msg": f"Qualitat < {min_score}. Regenerant..."})

    adapted = best_adapted if best_adapted else adapted

    # 6. Post-processament Python
    mecr = params.get("mecr_sortida", "B2")
    pp = post_process_adaptation(adapted, mecr)
    for w in pp.get("warnings", []):
        cb({"type": "step", "step": "warning", "msg": w})

    # 7. Pipeline de qualitat català (LanguageTool + llegibilitat + LLM Auditor)
    #    Fa servir el MECR real de sortida per avaluar la llegibilitat.
    quality_enabled = params.get("quality_check", True)
    use_auditor = params.get("auditor")
    if use_auditor is None:
        use_auditor = ATNE_AUDITOR_ENABLED
    etapa_pp = context.get("etapa", "")
    quality = None
    if quality_enabled:
        cb({"type": "step", "step": "quality",
            "msg": "Verificant qualitat (LanguageTool + llegibilitat + auditor LLM)..."})
        try:
            quality = post_process_catalan(
                adapted,
                target_mecr=mecr,
                enable_lt=True,
                enable_auditor=bool(use_auditor),
                etapa=etapa_pp,
            )
            if quality["n_correccions"] > 0:
                adapted = quality["text"]
                cb({"type": "step", "step": "quality_ok",
                    "msg": f"LanguageTool: {quality['n_correccions']} correccions auto-aplicades"})
            if quality["paraules_sospitoses"]:
                cb({"type": "step", "step": "warning",
                    "msg": f"{len(quality['paraules_sospitoses'])} paraules sospitoses — revisa al Quality Report"})
            if not quality["llegibilitat"].get("ok", True):
                cb({"type": "step", "step": "warning",
                    "msg": quality["llegibilitat"].get("missatge", "Llegibilitat fora del llindar")})
            if quality["avisos_auditor"]:
                cb({"type": "step", "step": "warning",
                    "msg": f"Auditor LLM: {len(quality['avisos_auditor'])} avisos pedagògics"})
        except Exception as e:
            cb({"type": "step", "step": "warning", "msg": f"Quality check fallit: {e}"})

    result_ev = {"type": "result", "adapted": adapted, "post_process": pp}
    if verify_info is not None:
        result_ev["verify"] = {"score": best_score, **verify_info}
    if quality is not None:
        result_ev["quality_report"] = {
            "n_correccions": quality["n_correccions"],
            "correccions": quality["correccions"][:20],
            "paraules_sospitoses": quality["paraules_sospitoses"][:20],
            "avisos_estil": quality["avisos_estil"][:10],
            "llegibilitat": quality["llegibilitat"],
            "avisos_auditor": quality["avisos_auditor"],
            "caracters_exotics": quality.get("caracters_exotics", []),
            "lt_disponible": quality["lt_disponible"],
            "auditor_disponible": quality["auditor_disponible"],
            "auditor_model": quality["auditor_model"],
        }
        if quality.get("caracters_exotics"):
            cb({"type": "step", "step": "warning",
                "msg": f"{len(quality['caracters_exotics'])} caràcter(s) exòtic(s) detectats — revisa al Quality Report"})
    cb(result_ev)
    cb({"type": "done"})
    return adapted


# ── API endpoints ───────────────────────────────────────────────────────────

@app.get("/api/health")
async def health():
    """Verifica connectivitat amb Supabase i Gemini."""
    checks = {"supabase": False, "llm": False, "model": ATNE_MODEL}
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
        if ATNE_MODEL == "mistral":
            r = requests.get("https://api.mistral.ai/v1/models",
                headers={"Authorization": f"Bearer {MISTRAL_API_KEY}"}, timeout=5)
            checks["llm"] = r.status_code == 200
        elif ATNE_MODEL == "gemma4":
            gemini_client.models.get(model="gemma-4-31b-it")
            checks["llm"] = True
        else:
            gemini_client.models.get(model="gemini-2.5-flash")
            checks["llm"] = True
    except Exception:
        pass
    ok = checks["supabase"] and checks["llm"]
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


# ── Extracció de text des de fitxer (PDF/DOCX/MD/TXT) ─────────────────────

MAX_UPLOAD_BYTES = 5 * 1024 * 1024  # 5 MB

@app.post("/api/extract-text")
async def extract_text_from_file(file: UploadFile = File(...)):
    """
    Rep un fitxer PDF/DOCX/MD/TXT i retorna el text pla extret.
    Límit: 5 MB. Format detectat per l'extensió.
    """
    filename = (file.filename or "").lower()
    ext = filename.rsplit(".", 1)[-1] if "." in filename else ""

    if ext not in ("pdf", "docx", "md", "txt"):
        return JSONResponse(
            {"error": f"Format no suportat: .{ext}. Accepta: PDF, DOCX, MD, TXT."},
            status_code=400,
        )

    raw = await file.read()
    if len(raw) > MAX_UPLOAD_BYTES:
        return JSONResponse(
            {"error": f"Fitxer massa gran ({len(raw)//1024} KB). Màxim: 5 MB."},
            status_code=400,
        )
    if not raw:
        return JSONResponse({"error": "Fitxer buit."}, status_code=400)

    text = ""
    try:
        if ext == "txt" or ext == "md":
            # Provar UTF-8 primer, fallback a latin-1
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError:
                text = raw.decode("latin-1", errors="replace")
            # Per MD, mantenim el text tal qual (l'LLM entén markdown)

        elif ext == "pdf":
            import io
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(raw))
            pages = []
            for page in reader.pages:
                try:
                    pages.append(page.extract_text() or "")
                except Exception:
                    continue
            text = "\n\n".join(p.strip() for p in pages if p.strip())

        elif ext == "docx":
            import io
            from docx import Document  # python-docx
            doc = Document(io.BytesIO(raw))
            parts = [p.text for p in doc.paragraphs if p.text.strip()]
            text = "\n\n".join(parts)

    except Exception as e:
        return JSONResponse(
            {"error": f"No s'ha pogut extreure el text: {type(e).__name__}: {e}"},
            status_code=500,
        )

    text = text.strip()
    if not text:
        return JSONResponse(
            {"error": "No s'ha pogut extreure text llegible del fitxer. "
                      "Si és un PDF escanejat, caldria OCR (no suportat ara)."},
            status_code=422,
        )

    paraules = len(text.split())
    return {
        "text": text,
        "paraules": paraules,
        "format_detectat": ext,
        "filename": file.filename,
    }


# ── Generació de text base (per a docents sense text propi) ───────────────

GENERATE_EXTENSIONS = {
    "micro": (
        "Micro (50-100 paraules). Prioritza la SÍNTESI extrema. "
        "Una sola idea principal, sense exemples llargs. Pensa en un tuit o "
        "una entrada d'enciclopèdia molt breu."
    ),
    "curt": (
        "Curt (~200 paraules, marge 180-240). Concís, 2-3 idees principals "
        "lligades. Sense subapartats. Una entrada de blog breu o un paràgraf "
        "introductori d'un manual."
    ),
    "estandard": (
        "Estàndard (~400 paraules, marge 350-450). Amb desenvolupament: "
        "introducció breu, cos amb 3-4 idees connectades amb exemples concrets, "
        "i tancament. Sense subtítols obligatoris però admet 1-2 si ajuden."
    ),
    "extens": (
        "Extens (+600 paraules, marge 600-900). Desenvolupament complet amb "
        "subapartats clars (usa títols H2 o H3), detalls tècnics, exemples "
        "concrets, contextualització i tancament. Estructura editorial."
    ),
}

GENERATE_TONS = {
    "neutre": (
        "neutre i acadèmic. Vocabulari precís, frases ben construïdes, "
        "distancia objectiva. Cap referència personal del tipus 'tu' o 'jo'."
    ),
    "informal": (
        "informal i col·loquial. Tutejant directament al lector ('tu', 'sabies "
        "que...?'), amb expressions properes i exemples del dia a dia. Estàndard "
        "oral català però respectant la normativa de l'IEC."
    ),
    "creatiu": (
        "creatiu i literari. Evocador, amb imatges, metàfores, ritme i música "
        "del llenguatge. Permet recursos retòrics: anàfora, comparació, "
        "personificació. Sense perdre rigor sobre el tema."
    ),
    "motivador": (
        "motivador i engrescador. Comença amb un ganxo (pregunta retòrica, "
        "anècdota intrigant o dada sorprenent) i manté l'interès amb verbs "
        "actius i frases dinàmiques."
    ),
    "reflexiu": (
        "reflexiu. Convida a pensar amb preguntes obertes intercalades, "
        "contrastos, exploració de matisos. No dona respostes tancades."
    ),
    "empatic": (
        "empàtic i cuidadós, especialment sensible amb temes delicats "
        "(trauma, vulnerabilitat, identitat). Vocabulari respectuós, evita "
        "judicis de valor, dona espai al lector."
    ),
    "humoristic": (
        "humorístic i divertit, amb tocs lleugers, jocs de paraules, "
        "comparacions enginyoses. Sense caure en la frivolitat: el contingut "
        "ha de ser rigorós, el to amable."
    ),
    "solemne": (
        "solemne, formal i ple de respecte. Propi de textos històrics, "
        "commemoratius o de memòria. Vocabulari elevat, frases ben mesurades, "
        "absència d'humor."
    ),
}


@app.post("/api/generate-text")
async def generate_text(payload: dict = Body(...)):
    """
    Genera un text base segons context i paràmetres.
    Per a docents que no disposen del text que volen adaptar.

    Payload:
        tema: str (required)
        genere: str (gènere discursiu, ex: "Article divulgatiu")
        tipologia: str (expositiva | narrativa | descriptiva | argumentativa | instructiva | dialogada)
        to: str (clau de GENERATE_TONS)
        extensio: str (clau de GENERATE_EXTENSIONS)
        notes: str (instruccions addicionals, opcional)
        context: dict amb etapa, curs, ambit (opcional, per ajustar nivell)
    """
    tema = (payload.get("tema") or "").strip()
    if not tema:
        return JSONResponse({"error": "Cal especificar un tema."}, status_code=400)

    genere = (payload.get("genere") or "Article divulgatiu").strip()
    tipologia = (payload.get("tipologia") or "expositiva").strip().lower()
    to = (payload.get("to") or "neutre").strip().lower()
    extensio = (payload.get("extensio") or "estandard").strip().lower()
    notes = (payload.get("notes") or "").strip()
    ctx = payload.get("context") or {}

    etapa = ctx.get("etapa", "ESO")
    curs = ctx.get("curs", "3r")
    ambit = ctx.get("ambit", "")
    materia = ctx.get("materia", "")

    extensio_instr = GENERATE_EXTENSIONS.get(extensio, GENERATE_EXTENSIONS["estandard"])
    to_instr = GENERATE_TONS.get(to, GENERATE_TONS["neutre"])

    notes_block = f"\n## INSTRUCCIONS ADDICIONALS DEL DOCENT (prioritàries)\n{notes}\n" if notes else ""

    prompt = f"""# ROL
Ets un expert en lingüística catalana i comunicació educativa. La teva
tasca és generar textos basant-te estrictament en tres eixos: GÈNERE
DISCURSIU (el motlle social), TIPOLOGIA TEXTUAL (l'esquelet intern) i
TO (la veu). Has de respectar les convencions del currículum escolar
català (Decret 175/2022) i l'estàndard de l'IEC.

# CONTEXT EDUCATIU
- Etapa: {etapa}
- Curs: {curs}
- Àmbit: {ambit}
- Matèria: {materia}

# COMANDA DEL DOCENT
- TEMA / TÒPIC: {tema}
- GÈNERE DISCURSIU: {genere}
- TIPOLOGIA TEXTUAL: {tipologia}
- TO: {to_instr}
- EXTENSIÓ: {extensio_instr}
{notes_block}
# REGLES OBLIGATÒRIES

## 1. Eix Gènere (mana sobre el FORMAT)
El gènere "{genere}" determina l'estructura social del text. Has d'incloure
els elements estructurals propis del gènere (per exemple: titular i lead
en una notícia; salutació i comiat en un correu; passos numerats en un
procediment; referent i valoració en una ressenya).

## 2. Eix Tipologia (mana sobre l'ESTRUCTURA INTERNA)
La tipologia "{tipologia}" determina la intenció comunicativa.
- Expositiva: presentar informació de forma clara i objectiva.
- Narrativa: relatar fets ordenats temporalment, amb personatges i acció.
- Descriptiva: detallar com és un objecte, lloc o persona amb adjectius i precisió sensorial.
- Argumentativa: defensar una tesi amb arguments connectats per connectors causals.
- Instructiva: donar passes en ordre, amb verbs en imperatiu o infinitiu.
- Dialogada: alternança de veus amb marques tipogràfiques.

EXEMPLES DE COMBINACIÓ:
- Gènere "Notícia" + Tipologia "Argumentativa" → article d'opinió periodístic.
- Gènere "Correu" + Tipologia "Instructiva" → e-mail tutorial pas a pas.
- Gènere "Conte" + Tipologia "Descriptiva" → conte amb passatges descriptius rics.

## 3. Eix To (mana sobre la VEU)
Mantén el to "{to}" de manera consistent al llarg de TOT el text. El to
afecta la tria lèxica i la proximitat amb el lector, però NO altera els
fets ni la rigor del contingut.

## 4. Centralitat del tema
El text ha de girar EXCLUSIVAMENT al voltant del tema indicat:
"{tema}". Evita divagacions, exemples genèrics o continguts tangencials.
Cada paràgraf ha de servir el tema central.

## 5. Rigor factual (zero al·lucinacions)
Si el tema implica fets científics, històrics, geogràfics o tècnics,
mantén la PRECISIÓ. NO inventis dades, dates, noms o xifres. Si no
estàs segur d'un fet, expressa-ho amb construccions com "es considera
que", "habitualment", o omet la dada concreta. El to canvia COM expliques
els fets, no QUINS fets són certs.

## 6. Adequació al curs
Adequa el vocabulari, la complexitat sintàctica i el grau d'abstracció
al nivell del curs ({curs} de {etapa}). NO simplifiquis més del necessari:
és un text ESTÀNDARD per al curs, no una adaptació. L'adaptació al
perfil de l'alumne es farà en una segona fase amb un altre pipeline.

## 7. Format de sortida
- Genera NOMÉS el text demanat. Sense títols administratius, sense
  "Aquí tens el text:", sense explicacions meta, sense disclaimers.
- Comença directament amb el contingut.
- Si el gènere ho exigeix (notícia, correu, recepta), inclou els elements
  estructurals propis al començament.
- Usa salts de paràgraf normals. Per a extensions "Extens", usa
  subtítols H2 o H3 amb format markdown (## o ###).

## 8. Català normatiu (IEC) — REGLA CRÍTICA
- TOT el text ha de ser en català estàndard normatiu de l'Institut
  d'Estudis Catalans (IEC). Cap paraula en cap altra llengua.
- ATENCIÓ a les paraules conflictives: usa "èssers vius" (mai "ser vius"),
  "conjunt" (mai "ensemble"), "obstant" (mai "obstant això" si no cal),
  "tanmateix", "no obstant això".
- Vigila les interferències del castellà ("haver-hi" no "haver", "moltes
  vegades" no "moltíssim", "anar-se'n" no "marxar-se").
- Vigila les interferències del francès o l'anglès: cap paraula com
  "ensemble", "rendezvous", "feedback", "skill", "background". Tradueix-ho
  sempre al català.
- Apostrofa correctament: "l'arbre", "d'aquest", "n'hi ha".
- Pluralització: "èssers" (no "essers"), "homes" (no "homens"), "joves"
  (no "jóvens").
- Si dubtes d'una paraula, prefereix sinònims segurs ("conjunt", "grup",
  "unitat") en lloc d'arriscar-te amb termes possiblement mal tokenitzats.

# GENERA EL TEXT ARA"""

    # Selecció de model via payload (fallback a ATNE_MODEL)
    model_payload = (payload.get("model") or "").strip().lower()
    model_usat = model_payload if model_payload in ("gemma4", "mistral", "gpt", "gemini") else ATNE_MODEL

    try:
        text = _call_llm(model_usat, prompt, "")
        text = clean_gemini_output(text).strip()
    except Exception as e:
        return JSONResponse(
            {"error": f"Error generant el text: {type(e).__name__}: {e}"},
            status_code=500,
        )

    if not text:
        return JSONResponse({"error": "L'LLM ha retornat un text buit."}, status_code=500)

    # ═══ Pipeline de qualitat post-generació ═══
    # Deduir MECR objectiu del context educatiu
    target_mecr = payload.get("target_mecr") or _mecr_from_etapa_curs(etapa, curs)
    verify = payload.get("verify") if payload.get("verify") is not None else True
    use_auditor = payload.get("auditor")
    if use_auditor is None:
        use_auditor = ATNE_AUDITOR_ENABLED
    quality = post_process_catalan(
        text,
        target_mecr=target_mecr,
        enable_lt=bool(verify),
        enable_auditor=bool(use_auditor),
        etapa=etapa,
    )

    paraules = len(quality["text"].split())
    return {
        "text": quality["text"],
        "paraules": paraules,
        "tema": tema,
        "genere": genere,
        "tipologia": tipologia,
        "to": to,
        "extensio": extensio,
        "model": model_usat,
        "quality_report": {
            "n_correccions": quality["n_correccions"],
            "correccions": quality["correccions"][:20],
            "paraules_sospitoses": quality["paraules_sospitoses"][:20],
            "avisos_estil": quality["avisos_estil"][:10],
            "llegibilitat": quality["llegibilitat"],
            "avisos_auditor": quality["avisos_auditor"],
            "caracters_exotics": quality.get("caracters_exotics", []),
            "lt_disponible": quality["lt_disponible"],
            "auditor_disponible": quality["auditor_disponible"],
            "auditor_model": quality["auditor_model"],
        },
    }


# ── Refinament de text (sense regenerar) ──────────────────────────────────

REFINE_PRESETS = {
    "catala": (
        "REGLA SUPREMA: actua com un corrector ortogràfic CONSERVADOR. "
        "NOMÉS corregeix errors que estiguis 100% segur que són errors. "
        "Si tens CAP dubte sobre si una paraula o forma és correcta, DEIXA-LA TAL COM ESTÀ. "
        "És PITJOR introduir un error nou que deixar un error existent. "
        "NO reformulis frases. NO canviïs sinònims. NO reorganitzis el text.\n\n"
        "\n"
        "CORRECCIONS CERTES A APLICAR:\n"
        "1. Paraules en altres llengües: tradueix NOMÉS les paraules clarament no catalanes "
        "(castellà, francès, anglès). Ex: 'ensemble' → 'conjunt', 'approach' → 'enfocament'. "
        "Si és un terme tècnic acceptat en català, NO el canviïs.\n"
        "2. Accents diacrítics IEC 2017: només els 15 vigents "
        "(bé, déu, és, mà, més, món, pèl, què, sé, sí, sóc, són, té, ús, vós). "
        "La resta NO porten diacrític: 'dona' (no 'dóna'), 'os' (no 'ós'), 'net' (no 'nét').\n"
        "3. Apostrofacions: l'home, l'escola, l'una, d'ahir. "
        "NO apostrofis davant h aspirada o consonant inicial pronunciada.\n"
        "4. Aglutinacions barbarismes: 'tal i com' → 'tal com', 'donar-se compte' → 'adonar-se'.\n"
        "5. Formes verbals: 'hauries' (no 'hauríes'), 'seria' (no 'séria').\n"
        "6. Concordances de gènere/nombre evidents.\n"
        "\n"
        "COSES QUE NO HAS DE TOCAR SI NO ESTÀS 100% SEGUR:\n"
        "- No canviïs preposicions regim ('pensar en' vs 'pensar a') si l'original funciona.\n"
        "- No afegeixis ni treguis 'ha de', 'cal', 'és menester'.\n"
        "- No transformis estructures passives/actives.\n"
        "- No inventis paraules ni les substitueixis per sinònims.\n"
        "- No canviïs temps verbals ni modes.\n"
        "\n"
        "VERIFICACIÓ FINAL OBLIGATÒRIA: abans de retornar el text, rellegeix-lo "
        "paraula per paraula. Si hi ha CAP paraula que no existeixi al diccionari "
        "normatiu (DIEC2), ELIMINA-LA o substitueix-la per la forma correcta. "
        "Si has introduït canvis que no tens 100% de certesa, REVERTEIX-LOS a "
        "l'original. Retorna NOMÉS text 100% normatiu."
    ),
    "simplificar": (
        "Simplifica el llenguatge sense canviar el contingut ni la longitud. "
        "Substitueix paraules complexes per sinònims més freqüents. Trenca "
        "frases llargues en frases més curtes. Mantén el to general. "
        "OBJECTIU: mateix missatge, vocabulari més senzill."
    ),
    "ampliar": (
        "AMPLIA EL TEXT. El text resultant HA DE SER MÉS LLARG que l'original, "
        "no més curt. Afegeix exemples concrets, contextualització, detalls "
        "explicatius i matisos que enriqueixin el contingut. Mantén l'estructura "
        "general i el to. OBJECTIU OBLIGATORI: el text ampliat ha de tenir "
        "aproximadament entre un 30% i un 50% més de paraules que l'original. "
        "NO escurcis. NO retornis un text més breu. Si l'original té 200 paraules, "
        "el resultat ha de tenir com a mínim 260 paraules."
    ),
    "escurcar": (
        "ESCURÇA EL TEXT. El text resultant HA DE SER MÉS CURT que l'original, "
        "no més llarg. Elimina paraules redundants, repeticions, frases "
        "secundàries, exemples superflus i digressions. Mantén TOTES les idees "
        "principals intactes. OBJECTIU OBLIGATORI: el text escurçat ha de tenir "
        "aproximadament entre un 25% i un 40% menys de paraules que l'original. "
        "NO ampliïs. NO retornis un text més llarg. Si l'original té 200 paraules, "
        "el resultat ha de tenir entre 120 i 150 paraules."
    ),
    "to_mes_proper": (
        "Reescriu el text amb un to més proper i informal, parlant "
        "directament al lector ('tu', 'sabies que...?'). Mantén el contingut "
        "intacte."
    ),
    "to_mes_formal": (
        "Reescriu el text amb un to més formal i acadèmic. Elimina "
        "expressions col·loquials. Mantén el contingut intacte."
    ),
}


LANGUAGETOOL_URL = os.getenv("LANGUAGETOOL_URL", "https://api.languagetool.org/v2/check")

# Model LLM utilitzat per a l'auditor pedagògic (Layer 3 del pipeline de qualitat).
# Per defecte gpt-4o-mini (barat + ràpid). Canviable via env var si cal,
# però ATENCIÓ: usem OPENAI_API_KEY institucional → NO canviar a models premium
# sense aprovació explícita (gpt-4o, gpt-4.1 són 10-30x més cars).
ATNE_AUDITOR_MODEL = os.getenv("ATNE_AUDITOR_MODEL", "gpt-4o-mini")
ATNE_AUDITOR_ENABLED = os.getenv("ATNE_AUDITOR_ENABLED", "true").lower() == "true"


def _languagetool_correct(text: str) -> tuple[str, int, list[dict]]:
    """
    Corregeix un text via LanguageTool API pública (determinista, no LLM).
    Retorna: (text_corregit, n_canvis, llista_canvis).
    Si LanguageTool falla, retorna (text, 0, []).
    """
    try:
        resp = requests.post(
            LANGUAGETOOL_URL,
            data={
                "text": text,
                "language": "ca",
                "level": "picky",
                "enabledOnly": "false",
            },
            headers={"Accept": "application/json"},
            timeout=30,
        )
        if resp.status_code != 200:
            return text, 0, []
        data = resp.json()
    except Exception as e:
        print(f"[LanguageTool] Error: {type(e).__name__}: {e}")
        return text, 0, []

    matches = data.get("matches", [])
    if not matches:
        return text, 0, []

    # Aplicar correccions d'esquerra a dreta inverses (per no desplaçar offsets)
    sorted_matches = sorted(matches, key=lambda m: m.get("offset", 0), reverse=True)

    corrected = text
    changes: list[dict] = []
    for m in sorted_matches:
        offset = m.get("offset", 0)
        length = m.get("length", 0)
        replacements = m.get("replacements", [])
        if not replacements or length <= 0:
            continue
        new_value = replacements[0].get("value", "")
        if new_value is None:
            continue
        old_value = corrected[offset:offset + length]
        # Saltar si la substitució és idèntica
        if new_value == old_value:
            continue
        corrected = corrected[:offset] + new_value + corrected[offset + length:]
        changes.append({
            "original": old_value,
            "corregit": new_value,
            "missatge": m.get("shortMessage") or m.get("message", ""),
            "regla": m.get("rule", {}).get("id", ""),
        })

    # Retornar canvis en ordre d'aparició al text
    changes.reverse()
    return corrected, len(changes), changes


# ═══ Pipeline de qualitat català (post-processament) ══════════════════════════

# Taula etapa+curs → MECR aproximat per al target de llegibilitat
# Usada quan el client no envia target_mecr explícit.
def _mecr_from_etapa_curs(etapa: str, curs: str = "") -> str:
    etapa_lower = (etapa or "").lower()
    curs_lower = (curs or "").lower()
    if "infantil" in etapa_lower:
        return "pre-A1"
    if "primari" in etapa_lower:
        # Cicle inicial (1-2): A1; Mitjà (3-4): A2; Superior (5-6): B1
        if any(x in curs_lower for x in ("1r", "1", "2n", "2")):
            return "A1"
        if any(x in curs_lower for x in ("3r", "3", "4t", "4")):
            return "A2"
        return "B1"
    if "eso" in etapa_lower:
        # 1-2 ESO: B1; 3-4 ESO: B2
        if any(x in curs_lower for x in ("1r", "1", "2n", "2")):
            return "B1"
        return "B2"
    if "batxillerat" in etapa_lower or "batx" in etapa_lower or "fp" in etapa_lower:
        return "C1"
    return "B1"  # default segur


# ═══ Filtre de caràcters exòtics (CJK, ciríl·lic, àrab, etc.) ══════════════
# Rangs Unicode permesos per a text català. Tota la resta genera alerta.
_ALLOWED_UNICODE_RANGES = [
    (0x0009, 0x000A),   # Tab, LF
    (0x000D, 0x000D),   # CR
    (0x0020, 0x007E),   # ASCII printable
    (0x00A0, 0x024F),   # Latin-1 Supplement + Latin Extended-A/B (à, é, ç, ñ, etc.)
    (0x2000, 0x206F),   # General Punctuation (em dash, smart quotes, bullet, ellipsis)
    (0x20A0, 0x20CF),   # Currency symbols (€, £, ¥)
    (0x2100, 0x214F),   # Letterlike (™, ℃, ℉)
    (0x2190, 0x21FF),   # Arrows (↑ ↓ → ←) — per esquemes
    (0x2200, 0x22FF),   # Mathematical Operators (+, ±, ×)
    (0x2500, 0x257F),   # Box drawing (├ ─ └) — per esquemes
    (0x25A0, 0x25FF),   # Geometric shapes (● ■ ▲)
    (0x2600, 0x27BF),   # Miscellaneous Symbols (☀ ♪ ⚡)
    (0x1F300, 0x1F9FF), # Emojis (alguns complements demanen pictogrames)
    (0x1FA70, 0x1FAFF), # Emojis v13+
]


def _is_char_allowed(ch: str) -> bool:
    cp = ord(ch)
    for start, end in _ALLOWED_UNICODE_RANGES:
        if start <= cp <= end:
            return True
    return False


def _detect_script(cp: int) -> str:
    """Identifica aproximadament l'script d'un codepoint."""
    if 0x0400 <= cp <= 0x04FF or 0x0500 <= cp <= 0x052F:
        return "ciríl·lic"
    if 0x0590 <= cp <= 0x05FF:
        return "hebreu"
    if 0x0600 <= cp <= 0x06FF or 0x0750 <= cp <= 0x077F or 0x08A0 <= cp <= 0x08FF:
        return "àrab"
    if 0x0900 <= cp <= 0x097F:
        return "devanagari (hindi)"
    if 0x0E00 <= cp <= 0x0E7F:
        return "tailandès"
    if 0x3000 <= cp <= 0x303F:
        return "CJK puntuació"
    if 0x3040 <= cp <= 0x309F:
        return "hiragana (japonès)"
    if 0x30A0 <= cp <= 0x30FF:
        return "katakana (japonès)"
    if 0x4E00 <= cp <= 0x9FFF:
        return "xinès"
    if 0xAC00 <= cp <= 0xD7AF:
        return "coreà (hangul)"
    if 0xE000 <= cp <= 0xF8FF:
        return "ús privat"
    if 0xFB00 <= cp <= 0xFB4F:
        return "presentacions alfabètiques"
    return "desconegut"


def _exotic_char_scan(text: str) -> list[dict]:
    """
    Escaneja el text en cerca de caràcters no esperats per a text català
    (CJK, ciríl·lic, àrab, hangul, ús privat, etc.). Retorna una llista
    amb un màxim de 10 entrades úniques amb {caracter, codepoint, script,
    context, ocurrencies}.

    Motivació: els LLMs (vam veure Gemma amb '홈olatge') ocasionalment
    insereixen caràcters d'altres scripts per artefactes de tokenització.
    Aquest filtre ho detecta de manera determinista abans que cap altre
    pas del pipeline.
    """
    if not text:
        return []

    grouped: dict[str, dict] = {}
    for i, ch in enumerate(text):
        if ch in (" ", "\n", "\t", "\r"):
            continue
        if _is_char_allowed(ch):
            continue
        cp = ord(ch)
        key = ch
        if key not in grouped:
            context_start = max(0, i - 18)
            context_end = min(len(text), i + 18)
            context_raw = text[context_start:context_end]
            context = context_raw.replace(ch, f"«{ch}»", 1)
            grouped[key] = {
                "caracter": ch,
                "codepoint": f"U+{cp:04X}",
                "script": _detect_script(cp),
                "context": context,
                "ocurrencies": 1,
            }
        else:
            grouped[key]["ocurrencies"] += 1
        if len(grouped) >= 10:
            break

    return list(grouped.values())


# Regles de LanguageTool que indiquen paraula desconeguda al diccionari català
_LT_UNKNOWN_WORD_RULES = {
    "MORFOLOGIK_RULE_CA_ES",  # Catalan ortografia general
    "MORFOLOGIK_RULE_CA_ES_V",
    "MORFOLOGIK_RULE_CA_ES_VALENCIA",
}

# Llindars de llegibilitat per MECR (mitjana paraules/frase i % paraules llargues >7 caràcters)
_READABILITY_TARGETS = {
    "pre-A1": {"max_wps": 8, "max_long_pct": 12},
    "A1": {"max_wps": 10, "max_long_pct": 15},
    "A2": {"max_wps": 14, "max_long_pct": 20},
    "B1": {"max_wps": 18, "max_long_pct": 28},
    "B2": {"max_wps": 25, "max_long_pct": 35},
    "C1": {"max_wps": 30, "max_long_pct": 42},
}


def _languagetool_full_analysis(text: str) -> dict:
    """
    Crida LanguageTool i separa matches en 3 categories:
    - correccions automàtiques (ortografia, gramàtica amb suggeriment clar)
    - paraules desconegudes (warnings, no auto-corregides)
    - avisos d'estil (info, no crítics)
    Retorna un dict amb text corregit i les 3 llistes.
    """
    result = {
        "text_original": text,
        "text_corregit": text,
        "correccions": [],
        "paraules_desconegudes": [],
        "avisos_estil": [],
        "lt_disponible": False,
    }

    try:
        resp = requests.post(
            LANGUAGETOOL_URL,
            data={
                "text": text,
                "language": "ca",
                "level": "picky",
                "enabledOnly": "false",
            },
            headers={"Accept": "application/json"},
            timeout=30,
        )
        if resp.status_code != 200:
            return result
        data = resp.json()
        result["lt_disponible"] = True
    except Exception as e:
        print(f"[LanguageTool] Error: {type(e).__name__}: {e}")
        return result

    matches = data.get("matches", [])
    if not matches:
        return result

    sorted_matches = sorted(matches, key=lambda m: m.get("offset", 0), reverse=True)

    corrected = text
    correccions: list[dict] = []
    desconegudes: list[dict] = []
    avisos: list[dict] = []

    for m in sorted_matches:
        offset = m.get("offset", 0)
        length = m.get("length", 0)
        replacements = m.get("replacements", [])
        rule_id = m.get("rule", {}).get("id", "")
        rule_cat = m.get("rule", {}).get("category", {}).get("id", "")
        old_value = text[offset:offset + length] if offset >= 0 else ""
        missatge = m.get("shortMessage") or m.get("message", "")

        # Estil explícit → warning, MAI auto-aplicar
        if rule_cat in _STYLE_WARNING_CATEGORIES:
            avisos.append({
                "fragment": old_value,
                "suggeriment": replacements[0].get("value", "") if replacements else "",
                "missatge": missatge,
                "regla": rule_id,
            })
            continue

        # Si és paraula desconeguda (MORFOLOGIK) → warning, i mirem si és
        # segur auto-aplicar (només si norm igual: accents, majúscules, etc.)
        if rule_id in _LT_UNKNOWN_WORD_RULES or "MORFOLOGIK" in rule_id:
            desconegudes.append({
                "paraula": old_value,
                "suggeriments": [r.get("value", "") for r in replacements[:3]],
                "missatge": missatge,
                "regla": rule_id,
            })
            if replacements and _suggestion_is_safe(
                old_value, replacements[0].get("value", ""), rule_id, rule_cat
            ):
                new_value = replacements[0].get("value", "")
                if new_value and new_value != old_value:
                    corrected = corrected[:offset] + new_value + corrected[offset + length:]
                    correccions.append({
                        "original": old_value,
                        "corregit": new_value,
                        "missatge": missatge,
                        "regla": rule_id,
                    })
            continue

        # Resta → auto-aplicar NOMÉS si és segur (categoria/prefix o norm)
        if replacements and length > 0:
            new_value = replacements[0].get("value", "")
            if new_value and new_value != old_value and _suggestion_is_safe(
                old_value, new_value, rule_id, rule_cat
            ):
                corrected = corrected[:offset] + new_value + corrected[offset + length:]
                correccions.append({
                    "original": old_value,
                    "corregit": new_value,
                    "missatge": missatge,
                    "regla": rule_id,
                })
            elif replacements:
                # No segur → emetre com a avís (l'usuari decideix)
                avisos.append({
                    "fragment": old_value,
                    "suggeriment": new_value,
                    "missatge": missatge,
                    "regla": rule_id,
                })

    # Revertir ordres per lectura natural
    correccions.reverse()
    desconegudes.reverse()
    avisos.reverse()

    result["text_corregit"] = corrected
    result["correccions"] = correccions
    result["paraules_desconegudes"] = desconegudes
    result["avisos_estil"] = avisos
    return result


## Categories de rules de LanguageTool que considerem SEGURES per auto-aplicació
## (no canvien el lema ni la semàntica — només ortografia / apostrofació / etc.)
_SAFE_RULE_CATEGORIES = {
    "PUNCTUATION",
    "TYPOGRAPHY",
    "CASING",
    "HYPHENATION",
    "WHITESPACE",
    "DIACRITICS_CA",
    "DIACRITICS",
}

## Prefixos de rule_id que són segurs (IEC-determinístics)
_SAFE_RULE_PREFIXES = (
    "L_APOSTROF",              # L' apostrofació catalana (el home → l'home)
    "APOSTROPHE",
    "APOSTROFAT",
    "APOSTROF",
    "DIACRITICS",              # accents diacrítics
    "ACCENTUATION",
    "HIAT",                    # hiatus
    "WHITESPACE",
    "DOUBLE_PUNCTUATION",
    "UPPERCASE_SENTENCE_START",
    "UPPERCASE_",
    "NUMBER_SPACE",
    "PUNT_FINAL",              # punt final
    "A_EL",                    # a el → al
    "DE_EL",                   # de el → del
    "PER_A_EL",                # per a el → pel
    "GUIONET",                 # guionet
    "HYPHEN",
    "COMMA_",                  # comes missing o extra
    "COMMA_PARENTHESIS",
)

## Categories que NO auto-apliquem (warnings d'estil, revisió humana recomanada)
_STYLE_WARNING_CATEGORIES = {
    "STYLE",
    "REDUNDANCY",
    "REGISTER",
    "COLLOQUIAL",
}


def _suggestion_is_safe(original: str, suggestion: str,
                        rule_id: str = "", rule_category: str = "") -> bool:
    """
    Un suggeriment es considera "segur" per a auto-aplicació si es compleix
    alguna d'aquestes condicions:
      1. La rule_category o el rule_id coincideix amb les llistes de rules
         segures (apostrofacions, accents, majúscules, puntuació, etc.)
      2. La normalització alfanumèrica (sense accents ni caràcters no alfanums)
         és idèntica entre original i suggeriment — això cobreix variacions
         d'accent, apostrof, majúscules i puntuació sense canviar el lema.

    Exemples de canvis AUTOAPLICABLES:
      - "dona" → "dóna"                (accent)
      - "l home" → "l'home"            (apostrof)
      - "el home" → "l'home"           (apostrof via rule L_APOSTROF)
      - "tambe" → "també"              (accent)
      - "Pompeu fabra" → "Pompeu Fabra" (majúscula)
      - "pel·lícula " → "pel·lícula"   (whitespace)

    Exemples de canvis NO autoaplicables (warnings):
      - "tal i com" → "tal com"        (treu una paraula — canvia lema)
      - "ser vius" → "éssers vius"     (canvia lema)
      - "moltíssim" → "molt"           (sinonimia, revisió humana)
    """
    if not original or not suggestion:
        return False

    rid = (rule_id or "").upper()
    rcat = (rule_category or "").upper()

    # 1. Rule category segura
    if rcat in _SAFE_RULE_CATEGORIES:
        return True

    # 2. Rule ID amb prefix segur
    if any(rid.startswith(p) for p in _SAFE_RULE_PREFIXES):
        return True

    # 3. Categoria explícita de warning d'estil → mai segur
    if rcat in _STYLE_WARNING_CATEGORIES:
        return False

    # 4. Normalització alfanumèrica: iguals?
    #    Elimina accents, puntuació, espais i passa a minúscules.
    import unicodedata

    def _norm(s: str) -> str:
        s_norm = unicodedata.normalize("NFKD", s.lower())
        s_ascii = s_norm.encode("ascii", "ignore").decode("ascii")
        return "".join(c for c in s_ascii if c.isalnum())

    return _norm(original) == _norm(suggestion)


def _readability_score(text: str, target_mecr: str = "") -> dict:
    """
    Calcula indicadors de llegibilitat del text en català:
    - paraules per frase (mitjana)
    - percentatge de paraules llargues (>7 caràcters)
    - longitud mitjana de paraula
    Compara amb els llindars del MECR objectiu i retorna un estat:
    "ok" / "sobre" (text més complex del que caldria) / "sota" (massa simple).
    """
    import re

    text_clean = text.strip()
    if not text_clean:
        return {"ok": True, "wps": 0, "long_pct": 0, "avg_word_len": 0,
                "target_mecr": target_mecr, "estat": "buit",
                "missatge": "Text buit"}

    # Trencar en frases per punts i signes d'interrogació/exclamació finals
    sentences = [s.strip() for s in re.split(r"[.!?]+", text_clean) if s.strip()]
    n_sentences = max(1, len(sentences))

    words = re.findall(r"\b[\wàèéíòóú·ïü]+\b", text_clean, flags=re.IGNORECASE)
    n_words = max(1, len(words))

    wps = round(n_words / n_sentences, 1)
    long_words = [w for w in words if len(w) > 7]
    long_pct = round(100 * len(long_words) / n_words, 1)
    avg_word_len = round(sum(len(w) for w in words) / n_words, 1)

    result = {
        "wps": wps,
        "long_pct": long_pct,
        "avg_word_len": avg_word_len,
        "n_words": n_words,
        "n_sentences": n_sentences,
        "target_mecr": target_mecr,
    }

    target = _READABILITY_TARGETS.get(target_mecr)
    if not target:
        result["ok"] = True
        result["estat"] = "sense_objectiu"
        result["missatge"] = f"Llegibilitat: {wps} par/frase · {long_pct}% paraules llargues"
        return result

    sobrepassa_wps = wps > target["max_wps"]
    sobrepassa_long = long_pct > target["max_long_pct"]

    if sobrepassa_wps and sobrepassa_long:
        result["ok"] = False
        result["estat"] = "sobre"
        result["missatge"] = (
            f"El text és més complex del que caldria per a {target_mecr}: "
            f"{wps} par/frase (màx {target['max_wps']}) i "
            f"{long_pct}% paraules llargues (màx {target['max_long_pct']}%)."
        )
    elif sobrepassa_wps:
        result["ok"] = False
        result["estat"] = "sobre"
        result["missatge"] = (
            f"Frases massa llargues per a {target_mecr}: "
            f"{wps} par/frase (màx recomanat {target['max_wps']})."
        )
    elif sobrepassa_long:
        result["ok"] = False
        result["estat"] = "sobre"
        result["missatge"] = (
            f"Vocabulari potser massa complex per a {target_mecr}: "
            f"{long_pct}% paraules llargues (màx recomanat {target['max_long_pct']}%)."
        )
    else:
        result["ok"] = True
        result["estat"] = "ok"
        result["missatge"] = (
            f"Llegibilitat adequada per a {target_mecr}: "
            f"{wps} par/frase · {long_pct}% paraules llargues."
        )

    return result


def _llm_audit(text: str, target_mecr: str = "", etapa: str = "") -> dict:
    """
    Layer 3 del pipeline: auditor pedagògic via LLM (GPT-4o-mini per defecte).
    NO modifica el text — només emet avisos qualitatius que LanguageTool no veu:
    frases confuses, salts lògics, vocabulari desajustat, repeticions, connectors
    mal usats, calcs d'altres llengües.

    Retorna: {"avisos": [...], "disponible": bool, "model": str, "error": str?}
    - avisos és una llista de dicts {"tipus", "fragment", "motiu"}
    - disponible indica si s'ha pogut fer la crida (fallback silent a LT si no)
    """
    result = {"avisos": [], "disponible": False, "model": ATNE_AUDITOR_MODEL}

    if not text or not text.strip():
        result["error"] = "text buit"
        return result

    if not os.getenv("OPENAI_API_KEY"):
        result["error"] = "OPENAI_API_KEY no configurada"
        return result

    contexte_etapa = f"alumne de {etapa}" if etapa else "un alumne d'escola catalana"
    contexte_mecr = f"nivell MECR {target_mecr}" if target_mecr else "nivell estàndard"

    prompt = f"""Ets un inspector pedagògic en català. Has d'auditar el text següent pensant en un {contexte_etapa} amb {contexte_mecr}.

NO modifiquis el text. NOMÉS emet fins a 6 avisos qualitatius sobre:
- Frases ambigües o confuses
- Salts lògics o idees que perden el fil
- Vocabulari massa complex o inadequat per al nivell
- Repeticions que no aporten
- Connectors mal usats (connectors causals, consecutius, adversatius usats incorrectament)
- Construccions no naturals en català (calcs del castellà, francès o anglès)

Retorna NOMÉS un objecte JSON vàlid (sense marcadors markdown, sense explicacions extra), amb aquesta estructura exacta:

{{"avisos": [{{"tipus": "confusa|salt|vocabulari|repeticio|connector|calc", "fragment": "fragment literal del text (max 100 car)", "motiu": "explicació breu del problema"}}]}}

Si el text és adequat al nivell i no hi ha problemes rellevants, retorna {{"avisos": []}}.

TEXT A AUDITAR:
{text}"""

    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        resp = client.chat.completions.create(
            model=ATNE_AUDITOR_MODEL,
            messages=[
                {"role": "system", "content": "Ets un auditor pedagògic que retorna NOMÉS JSON vàlid, sense marcadors markdown ni text addicional."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=1200,
            temperature=0.2,
            timeout=20,
        )
        raw = (resp.choices[0].message.content or "").strip()
    except Exception as e:
        print(f"[LLM Auditor] Error: {type(e).__name__}: {e}")
        result["error"] = f"{type(e).__name__}: {e}"
        return result

    # Netejar markdown fences si existeixen
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)

    try:
        data = json.loads(raw)
        avisos_raw = data.get("avisos", [])
        if not isinstance(avisos_raw, list):
            avisos_raw = []
        clean_avisos: list[dict] = []
        for a in avisos_raw[:10]:
            if isinstance(a, dict) and a.get("fragment"):
                clean_avisos.append({
                    "tipus": str(a.get("tipus", "")).strip()[:30],
                    "fragment": str(a.get("fragment", "")).strip()[:300],
                    "motiu": str(a.get("motiu", "")).strip()[:300],
                })
        result["avisos"] = clean_avisos
        result["disponible"] = True
    except Exception as e:
        print(f"[LLM Auditor] JSON parse error: {e}. Raw: {raw[:200]}")
        result["error"] = f"JSON invàlid: {e}"

    return result


def post_process_catalan(text: str, target_mecr: str = "", enable_lt: bool = True,
                         enable_auditor: bool = None, etapa: str = "") -> dict:
    """
    Pipeline complet de qualitat català per a un text generat o adaptat.

    Capes:
      1. LanguageTool (determinista): ortografia, gramàtica, paraules desconegudes
      2. Llegibilitat (heurística): paraules/frase + % paraules llargues vs MECR
      3. LLM Auditor (opcional): avisos pedagògics qualitatius (GPT-4o-mini)

    Les capes 1 i 3 s'executen EN PARAL·LEL amb ThreadPoolExecutor.

    Retorna un dict amb:
      - text: text final (amb correccions auto-aplicades si enable_lt)
      - n_correccions, correccions: LanguageTool
      - paraules_sospitoses: paraules no trobades al diccionari
      - avisos_estil: avisos estilístics de LanguageTool (no crítics)
      - llegibilitat: indicadors + estat vs MECR objectiu
      - avisos_auditor: warnings qualitatius del LLM auditor
      - lt_disponible, auditor_disponible, auditor_model
    """
    if enable_auditor is None:
        enable_auditor = ATNE_AUDITOR_ENABLED

    if not text or not text.strip():
        return {
            "text": text,
            "n_correccions": 0,
            "correccions": [],
            "paraules_sospitoses": [],
            "avisos_estil": [],
            "llegibilitat": _readability_score("", target_mecr),
            "avisos_auditor": [],
            "caracters_exotics": [],
            "lt_disponible": False,
            "auditor_disponible": False,
            "auditor_model": ATNE_AUDITOR_MODEL,
        }

    # Capa 0 (determinista, ràpid): detectar caràcters exòtics abans de res.
    #    Capta glitches com '홈olatge' (coreà) o lletres ciríl·liques inserides
    #    per errors de tokenització.
    caracters_exotics = _exotic_char_scan(text)

    # Paral·lelitzar LanguageTool + LLM Auditor per estalviar temps
    lt_result = None
    audit_result = {"avisos": [], "disponible": False, "model": ATNE_AUDITOR_MODEL}

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        lt_future = pool.submit(_languagetool_full_analysis, text) if enable_lt else None
        audit_future = pool.submit(_llm_audit, text, target_mecr, etapa) if enable_auditor else None

        if lt_future is not None:
            try:
                lt_result = lt_future.result(timeout=45)
            except Exception as e:
                print(f"[LT] Timeout/Error: {e}")
                lt_result = None
        if audit_future is not None:
            try:
                audit_result = audit_future.result(timeout=30)
            except Exception as e:
                print(f"[Auditor] Timeout/Error: {e}")
                audit_result = {"avisos": [], "disponible": False, "model": ATNE_AUDITOR_MODEL, "error": str(e)}

    if lt_result:
        text_final = lt_result["text_corregit"]
        correccions = lt_result["correccions"]
        desconegudes = lt_result["paraules_desconegudes"]
        avisos_estil = lt_result["avisos_estil"]
        lt_disponible = lt_result["lt_disponible"]
    else:
        text_final = text
        correccions = []
        desconegudes = []
        avisos_estil = []
        lt_disponible = False

    llegibilitat = _readability_score(text_final, target_mecr)

    return {
        "text": text_final,
        "n_correccions": len(correccions),
        "correccions": correccions,
        "paraules_sospitoses": desconegudes,
        "avisos_estil": avisos_estil,
        "llegibilitat": llegibilitat,
        "avisos_auditor": audit_result.get("avisos", []),
        "caracters_exotics": caracters_exotics,
        "lt_disponible": lt_disponible,
        "auditor_disponible": audit_result.get("disponible", False),
        "auditor_model": audit_result.get("model", ATNE_AUDITOR_MODEL),
    }


@app.post("/api/refine-text")
async def refine_text(payload: dict = Body(...)):
    """
    Refina un text existent segons una instrucció.
    No regenera des de zero — modifica el text actual.

    Payload:
        text: str (required) — el text a refinar
        preset: str (opcional) — clau de REFINE_PRESETS per instruccions ràpides
        instruccio: str (opcional) — instrucció lliure del docent
    """
    text = (payload.get("text") or "").strip()
    if not text:
        return JSONResponse({"error": "Cal proporcionar el text a refinar."}, status_code=400)

    preset = (payload.get("preset") or "").strip().lower()
    instruccio_lliure = (payload.get("instruccio") or "").strip()

    # Preset "catala" → LanguageTool (determinista, no LLM)
    if preset == "catala" and not instruccio_lliure:
        corrected, n_canvis, canvis = _languagetool_correct(text)
        return {
            "text": corrected,
            "paraules": len(corrected.split()),
            "preset_aplicat": "catala",
            "mode": "languagetool",
            "n_canvis": n_canvis,
            "canvis": canvis,
        }

    instruccio_final = ""
    if preset and preset in REFINE_PRESETS:
        instruccio_final = REFINE_PRESETS[preset]
    if instruccio_lliure:
        if instruccio_final:
            instruccio_final += "\n\nA més, el docent demana específicament: " + instruccio_lliure
        else:
            instruccio_final = instruccio_lliure

    if not instruccio_final:
        return JSONResponse(
            {"error": "Cal especificar un preset o una instrucció lliure."},
            status_code=400,
        )

    # Per ampliar/escurcar, injectar objectius numèrics explícits basats en
    # el recompte real de paraules per evitar que Gemma 4 faci el contrari.
    paraules_in = len(text.split())
    if preset == "ampliar":
        target_min = int(paraules_in * 1.30)
        target_max = int(paraules_in * 1.50)
        instruccio_final += (
            f"\n\nRECOMPTE OBLIGATORI: l'original té {paraules_in} paraules. "
            f"El text resultant HA DE TENIR entre {target_min} i {target_max} paraules. "
            f"Si retornes menys de {target_min} paraules, és un ERROR. "
            f"Compta les paraules del resultat abans de retornar-lo."
        )
    elif preset == "escurcar":
        target_min = int(paraules_in * 0.60)
        target_max = int(paraules_in * 0.75)
        instruccio_final += (
            f"\n\nRECOMPTE OBLIGATORI: l'original té {paraules_in} paraules. "
            f"El text resultant HA DE TENIR entre {target_min} i {target_max} paraules. "
            f"Si retornes més de {target_max} paraules, és un ERROR. "
            f"Compta les paraules del resultat abans de retornar-lo."
        )

    prompt = f"""# ROL
Ets un expert en lingüística catalana. Has de REFINAR el text que
et passen segons les instruccions del docent. NO el regeneris des de
zero — modifica'l mantenint l'estructura general i el contingut.

# REGLES
1. Tot el text final ha de ser en català estàndard normatiu (IEC).
2. NO afegeixis explicacions meta del tipus "Aquí tens el text refinat:".
   Retorna NOMÉS el text corregit, directament.
3. NO canviïs el contingut substantiu del text. Només aplica les
   instruccions de refinament demanades.
4. Si detectes paraules en altres llengües (francès, castellà, anglès),
   tradueix-les al català correcte sempre.
5. Vigila errors típics: "ser vius" → "èssers vius", "ensemble" → "conjunt",
   apostrofacions, concordances de gènere i nombre.

# INSTRUCCIONS DEL DOCENT
{instruccio_final}

# TEXT A REFINAR
{text}

# RETORNA EL TEXT REFINAT (NOMÉS EL TEXT, RES MÉS)"""

    try:
        result = _call_llm("gemma4", prompt, "")
        result = clean_gemini_output(result).strip()
    except Exception as e:
        return JSONResponse(
            {"error": f"Error refinant el text: {type(e).__name__}: {e}"},
            status_code=500,
        )

    if not result:
        return JSONResponse({"error": "L'LLM ha retornat un text buit."}, status_code=500)

    return {
        "text": result,
        "paraules": len(result.split()),
        "preset_aplicat": preset or None,
    }


# ── Adaptació (SSE stream) ─────────────────────────────────────────────────

# ── Multinivell: desplaçar MECR ±1 per a mode grup ─────────────────────────

_MECR_SCALE = ["pre-A1", "A1", "A2", "B1", "B2"]

def _shift_mecr(mecr: str, shift: int) -> str:
    """Desplaça el MECR N graons amb límits pre-A1..B2."""
    try:
        idx = _MECR_SCALE.index(mecr)
    except ValueError:
        return mecr
    new_idx = max(0, min(len(_MECR_SCALE) - 1, idx + shift))
    return _MECR_SCALE[new_idx]

# Mapa de nivells per a mode grup: label → desplaçament relatiu al MECR base
LEVEL_SHIFTS = {
    "accessible": -1,
    "estandard": 0,
    "exigent": +1,
}


@app.post("/api/adapt")
async def adapt_stream(payload: dict = Body(...)):
    text = payload.get("text", "")
    profile = payload.get("profile", {})
    context = payload.get("context", {})
    params = payload.get("params", {})
    model = payload.get("model", "")  # mistral | gemma4 | (buit = default ATNE_MODEL)

    if not text.strip():
        return JSONResponse({"error": "Cal proporcionar un text"}, status_code=400)

    # Nivells a generar. Per defecte: una sola versió.
    # Si arriba 'levels' amb més d'un element, generem cada un en paral·lel
    # amb MECR ajustat (accessible=-1, estandard=0, exigent=+1).
    levels = params.get("levels") or ["single"]
    base_mecr = params.get("mecr_sortida", "B1")

    async def gen():
        events: list[dict] = []
        done_count = {"n": 0}

        def make_cb(level_id: str):
            def _cb(ev):
                # Afegim la identificació del nivell a cada event, perquè el
                # frontend pugui enrutar-lo a la pestanya corresponent.
                ev_tagged = {**ev, "level": level_id}
                if ev.get("type") == "done":
                    done_count["n"] += 1
                    # El 'done' global l'enviem quan tots els nivells han acabat.
                    # Reemetem un 'done_level' individual perquè el frontend sàpiga
                    # que aquest nivell concret ja està llest.
                    ev_tagged["type"] = "done_level"
                events.append(ev_tagged)
            return _cb

        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor(max_workers=max(3, len(levels))) as pool:
            tasks = []
            for lvl in levels:
                shift = LEVEL_SHIFTS.get(lvl, 0)
                params_lvl = {**params, "mecr_sortida": _shift_mecr(base_mecr, shift)}
                # level 'single' ⇒ passem id buit (frontend tracta com a mode alumne)
                level_id = lvl if lvl != "single" else ""
                t = loop.run_in_executor(
                    pool,
                    lambda p=params_lvl, l=level_id: run_adaptation(
                        text, profile, context, p, make_cb(l), model_override=model or None
                    ),
                )
                tasks.append(t)

            total = len(tasks)
            all_done = lambda: all(t.done() for t in tasks)
            while not all_done():
                while events:
                    yield f"data: {json.dumps(events.pop(0), ensure_ascii=False)}\n\n"
                yield ": keepalive\n\n"
                await asyncio.sleep(0.5)
            while events:
                yield f"data: {json.dumps(events.pop(0), ensure_ascii=False)}\n\n"

            # 'done' global quan tots els nivells han acabat
            yield f"data: {json.dumps({'type': 'done', 'total_levels': total}, ensure_ascii=False)}\n\n"

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


# ── Cuina (dashboard intern) ───────────────────────────────────────────────

@app.get("/cuina", response_class=HTMLResponse)
async def cuina_page():
    """Serveix la pàgina de cuina (flux + catàleg d'instruccions)."""
    html_path = UI_DIR / "cuina.html"
    if html_path.exists():
        return HTMLResponse(
            html_path.read_text(encoding="utf-8"),
            headers={"Cache-Control": "no-cache, no-store, must-revalidate"},
        )
    return HTMLResponse("<h1>Cuina no disponible</h1>", status_code=404)


@app.get("/saber-ne", response_class=HTMLResponse)
async def saber_ne_page():
    """Serveix la pàgina Saber-ne+ (fonaments pedagògics per a docents)."""
    html_path = UI_DIR / "saber-ne.html"
    if html_path.exists():
        return HTMLResponse(
            html_path.read_text(encoding="utf-8"),
            headers={"Cache-Control": "no-cache, no-store, must-revalidate"},
        )
    return HTMLResponse("<h1>Saber-ne+ no disponible</h1>", status_code=404)


@app.get("/avaluacio", response_class=HTMLResponse)
async def avaluacio_page():
    """Serveix el hub d'avaluació i decisions (Bloc 3 de Saber-ne+)."""
    html_path = UI_DIR / "avaluacio.html"
    if html_path.exists():
        return HTMLResponse(
            html_path.read_text(encoding="utf-8"),
            headers={"Cache-Control": "no-cache, no-store, must-revalidate"},
        )
    return HTMLResponse("<h1>Avaluació no disponible</h1>", status_code=404)


@app.get("/demo", response_class=HTMLResponse)
async def demo_v7_page():
    """Serveix el mockup visual V7 de Stitch (Pas 1 redissenyat). Estàtic."""
    html_path = UI_DIR / "v7_demo.html"
    if html_path.exists():
        return HTMLResponse(
            html_path.read_text(encoding="utf-8"),
            headers={"Cache-Control": "no-cache, no-store, must-revalidate"},
        )
    return HTMLResponse("<h1>Demo V7 no disponible</h1>", status_code=404)


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_xat9_page():
    """Serveix el dashboard del Xat 9 (experiment A/B multi-model)."""
    html_path = UI_DIR / "dashboard_xat9.html"
    if html_path.exists():
        return HTMLResponse(
            html_path.read_text(encoding="utf-8"),
            headers={"Cache-Control": "no-cache, no-store, must-revalidate"},
        )
    return HTMLResponse("<h1>Dashboard Xat 9 no disponible</h1>", status_code=404)


@app.get("/dashboard_complements", response_class=HTMLResponse)
async def dashboard_complements_page():
    html_path = UI_DIR / "dashboard_complements.html"
    if html_path.exists():
        return HTMLResponse(
            html_path.read_text(encoding="utf-8"),
            headers={"Cache-Control": "no-cache, no-store, must-revalidate"},
        )
    return HTMLResponse("<h1>Dashboard Complements no disponible</h1>", status_code=404)


@app.get("/dashboard_questions", response_class=HTMLResponse)
async def dashboard_questions_page():
    html_path = UI_DIR / "dashboard_questions.html"
    if html_path.exists():
        return HTMLResponse(
            html_path.read_text(encoding="utf-8"),
            headers={"Cache-Control": "no-cache, no-store, must-revalidate"},
        )
    return HTMLResponse("<h1>Dashboard Questions no disponible</h1>", status_code=404)


@app.get("/informe_fje")
async def informe_fje_md():
    """Descàrrega de l'informe executiu FJE en Markdown."""
    md_path = Path(__file__).parent / "tests" / "experiment_ab" / "informe_executiu_FJE.md"
    if md_path.exists():
        return FileResponse(
            str(md_path),
            filename="informe_executiu_FJE.md",
            media_type="text/markdown; charset=utf-8",
        )
    return HTMLResponse("<h1>Informe FJE no disponible</h1>", status_code=404)


@app.get("/informe_tecnic")
async def informe_tecnic_md():
    """Descàrrega de l'informe tècnic multi-model en Markdown."""
    md_path = Path(__file__).parent / "tests" / "experiment_ab" / "informe_multi_model.md"
    if md_path.exists():
        return FileResponse(
            str(md_path),
            filename="informe_multi_model.md",
            media_type="text/markdown; charset=utf-8",
        )
    return HTMLResponse("<h1>Informe tècnic no disponible</h1>", status_code=404)


@app.get("/validacio", response_class=HTMLResponse)
async def validacio_page():
    """Serveix la pàgina de validació humana."""
    html_path = UI_DIR / "validacio.html"
    if html_path.exists():
        return HTMLResponse(html_path.read_text(encoding="utf-8"),
                            headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
    return HTMLResponse("<h1>Validació no disponible</h1>", status_code=404)


@app.get("/validacio_data.json")
async def validacio_data():
    """Serveix les dades de validació estàtiques (det)."""
    json_path = UI_DIR / "validacio_data.json"
    if json_path.exists():
        return JSONResponse(json.loads(json_path.read_text(encoding="utf-8")))
    return JSONResponse([])


@app.get("/api/validacio/{tanda}")
async def api_validacio_tanda(tanda: str):
    """Retorna textos adaptats + puntuacions per a una tanda (prompt_mode)."""
    import sqlite3
    db_path = Path(__file__).parent / "tests" / "results" / "evaluations.db"
    if not db_path.exists():
        return JSONResponse([])
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    # Agafar tots els casos d'aquesta tanda amb avaluació GPT
    rows = conn.execute("""
        SELECT g.cas_id, g.generator, g.perfil_nom, g.mecr, g.dua, g.text_adaptat_paraules,
               g.text_original, g.text_adaptat, g.system_prompt, g.perfil_id,
               e.a1_coherencia, e.a2_correccio, e.a3_llegibilitat,
               e.b1_fidelitat, e.b2_adequacio_perfil, e.b3_scaffolding, e.b4_cultura,
               e.c1_potencial, e.puntuacio_global
        FROM multi_llm_generations g
        LEFT JOIN multi_v2_evaluations e ON e.generation_id = g.id AND e.judge = 'gpt4mini'
        WHERE g.run_id = 'multi_v2' AND g.prompt_mode = ?
          AND g.text_adaptat IS NOT NULL AND g.text_adaptat != ''
          AND g.generator IN ('gemini', 'gpt', 'mistral')
        ORDER BY g.cas_id, g.generator
        LIMIT 200
    """, (tanda,)).fetchall()
    data = []
    for r in rows:
        data.append({
            "cas_id": r["cas_id"], "generator": r["generator"],
            "perfil": r["perfil_nom"] or "", "perfil_id": r["perfil_id"] or "",
            "mecr": r["mecr"] or "", "dua": r["dua"] or "",
            "paraules": r["text_adaptat_paraules"] or 0,
            "original": r["text_original"] or "", "adaptat": r["text_adaptat"] or "",
            "system_prompt": r["system_prompt"] or "",
            "gpt": {
                "A1": r["a1_coherencia"] or 0, "A2": r["a2_correccio"] or 0,
                "A3": r["a3_llegibilitat"] or 0, "B1": r["b1_fidelitat"] or 0,
                "B2": r["b2_adequacio_perfil"] or 0, "B3": r["b3_scaffolding"] or 0,
                "B4": r["b4_cultura"] or 0, "C1": r["c1_potencial"] or 0,
                "global": r["puntuacio_global"] or 0,
            }
        })
    conn.close()
    return JSONResponse(data)


@app.get("/api/catalog")
async def api_catalog():
    """Retorna el catàleg complet d'instruccions amb metadades."""
    from instruction_catalog import CATALOG, PROFILE_INSTRUCTION_MAP

    category_labels = {
        "A": "Adaptació Lingüística",
        "B": "Estructura i Organització",
        "C": "Suport Cognitiu",
        "D": "Multimodalitat",
        "E": "Contingut Curricular",
        "F": "Avaluació i Comprensió",
        "G": "Personalització Lingüística",
        "H": "Adaptacions per Perfil",
    }

    items = []
    for iid, instr in CATALOG.items():
        item = {
            "id": iid,
            "text": instr["text"],
            "activation": instr["activation"],
            "category": iid.split("-")[0],
        }
        if "profiles" in instr:
            item["profiles"] = instr["profiles"]
        if "mecr_levels" in instr:
            item["mecr_levels"] = instr["mecr_levels"]
        if "mecr_detail" in instr:
            item["mecr_detail"] = instr["mecr_detail"]
        if "suppress_if" in instr:
            item["suppress_if"] = instr["suppress_if"]
        if "subvar_conditions" in instr:
            item["subvar_conditions"] = instr["subvar_conditions"]
        if "complement" in instr:
            item["complement"] = instr["complement"]
        items.append(item)

    return {
        "items": items,
        "total": len(items),
        "category_labels": category_labels,
        "profile_map": PROFILE_INSTRUCTION_MAP,
    }


# ── API Corpus (visor de documents MD) ────────────────────────────────────

CORPUS_DIR = Path(__file__).parent / "corpus"

@app.get("/api/corpus")
async def api_corpus_list():
    """Retorna la llista de fitxers del corpus amb títol i mòdul."""
    files = []
    for f in sorted(CORPUS_DIR.glob("*.md")):
        name = f.stem
        modul = name.split("_")[0]  # M1, M2, M3
        modul_noms = {
            "M1": "Subjecte (perfils alumnat)",
            "M2": "Mètode (metodologies)",
            "M3": "Llengua",
        }
        files.append({
            "filename": f.name,
            "stem": name,
            "modul": modul,
            "modul_nom": modul_noms.get(modul, modul),
            "titol": name.split("_", 1)[1].replace("-", " ").replace("·", "·").title() if "_" in name else name,
            "size_kb": round(f.stat().st_size / 1024, 1),
        })
    return {"files": files, "total": len(files)}


@app.get("/api/corpus/{filename}")
async def api_corpus_file(filename: str):
    """Retorna el contingut d'un fitxer del corpus."""
    filepath = CORPUS_DIR / filename
    if not filepath.exists() or not filepath.suffix == ".md":
        return {"error": "Fitxer no trobat"}, 404
    content = filepath.read_text(encoding="utf-8")
    # Extreure seccions (## headings)
    sections = []
    current = {"title": "Introducció", "content": ""}
    for line in content.split("\n"):
        if line.startswith("## "):
            if current["content"].strip():
                sections.append(current)
            current = {"title": line[3:].strip(), "content": ""}
        else:
            current["content"] += line + "\n"
    if current["content"].strip():
        sections.append(current)
    return {
        "filename": filename,
        "content": content,
        "sections": sections,
        "length": len(content),
        "words": len(content.split()),
    }


# ── API Prompt Preview ───────────────────────────────────────────────────

@app.post("/api/prompt-preview")
async def api_prompt_preview(request: Request):
    """Genera el prompt complet per a un perfil donat (sense cridar l'LLM)."""
    data = await request.json()
    profile = data.get("profile", {})
    context = data.get("context", {"etapa": "ESO", "curs": "3r"})
    params = data.get("params", {"mecr_sortida": "B2", "dua": "Core"})

    mecr = params.get("mecr_sortida", "B2")

    # 1. Instruccions filtrades
    filtered = instruction_filter.get_instructions(profile, params)
    instructions_text = instruction_filter.format_instructions_for_prompt(filtered)
    instruction_ids = [f["id"] for f in filtered]

    # 2. Persona-audience
    persona = build_persona_audience(profile, context, mecr)

    # 3. Prompt complet (sense RAG — no fem cerca real)
    prompt = build_system_prompt(profile, context, params, "[Aquí anirien 8-12 fragments del corpus FJE cercats per similitud vectorial]")

    # 4. Capes separades per visualització
    identity = corpus_reader.get_identity()
    dua_block = corpus_reader.get_dua_block(params.get("dua", "Core")) or ""
    genre_block = ""
    genre = params.get("genere_discursiu", "")
    if genre:
        genre_block = corpus_reader.get_genre_block(genre) or ""
    fewshot = corpus_reader.get_fewshot_example(mecr) or ""

    return {
        "prompt_complet": prompt,
        "prompt_length": len(prompt),
        "prompt_words": len(prompt.split()),
        "capes": {
            "identitat": identity,
            "instruccions": instructions_text,
            "dua": dua_block,
            "genere": genre_block,
            "persona_audience": persona,
            "fewshot": fewshot,
        },
        "instruction_ids": instruction_ids,
        "total_instructions": len(filtered),
    }


# ── API Avaluació (dashboard) ──────────────────────────────────────────────

@app.get("/eval", response_class=HTMLResponse)
async def eval_dashboard():
    """Serveix el dashboard d'avaluació (resultats complets)."""
    html_path = UI_DIR / "eval_dashboard.html"
    if html_path.exists():
        return HTMLResponse(html_path.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>Dashboard no disponible</h1>", status_code=404)


@app.get("/eval/progress", response_class=HTMLResponse)
async def eval_progress_page():
    """Serveix la pàgina de monitoratge en temps real."""
    html_path = UI_DIR / "eval_progress.html"
    if html_path.exists():
        return HTMLResponse(html_path.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>Pàgina de progrés no disponible</h1>", status_code=404)


@app.get("/eval/results", response_class=HTMLResponse)
async def eval_results_page():
    """Serveix la pàgina de resultats amb infografies."""
    html_path = UI_DIR / "eval_results.html"
    if html_path.exists():
        return HTMLResponse(html_path.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>Resultats no disponibles</h1>", status_code=404)


@app.get("/eval/cases", response_class=HTMLResponse)
async def eval_cases_page():
    """Serveix la pàgina de visualització de casos (textos adaptats)."""
    html_path = UI_DIR / "eval_cases.html"
    if html_path.exists():
        return HTMLResponse(html_path.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>Cases no disponibles</h1>", status_code=404)


@app.get("/api/eval/cases/{run_id}")
async def eval_cases_detail(run_id: str, limit: int = 20, offset: int = 0,
                            perfil: str = "", etapa: str = "", genere: str = ""):
    """Retorna els casos amb textos adaptats complets per visualitzar."""
    try:
        import eval_db
        conn = eval_db.init_db()

        # Build optional filters
        filters = ""
        params = [run_id]
        if perfil:
            filters += " AND c1.perfil_id = ?"
            params.append(perfil)
        if etapa:
            filters += " AND c1.etapa = ?"
            params.append(etapa)
        if genere:
            filters += " AND c1.genere = ?"
            params.append(genere)

        rows = conn.execute(f"""
            SELECT c1.cas_id, c1.text_id, c1.perfil_id, c1.etapa, c1.genere, c1.mecr, c1.dua,
                   c1.perfils_actius,
                   c1.text_adaptat as text_hc, c1.puntuacio_forma as forma_hc,
                   c1.system_prompt_length as prompt_hc_len,
                   c2.text_adaptat as text_rag, c2.puntuacio_forma as forma_rag,
                   c2.recall as recall_rag,
                   c2.system_prompt_length as prompt_rag_len,
                   c2.total_instruccions_enviades as instr_rag
            FROM eval_cases c1
            JOIN eval_cases c2 ON c1.cas_id = c2.cas_id AND c1.run_id = c2.run_id
            WHERE c1.run_id = ? AND c1.branca = 'hardcoded' AND c2.branca = 'rag'
            {filters}
            ORDER BY c1.cas_id
            LIMIT ? OFFSET ?
        """, (*params, limit, offset)).fetchall()

        total = conn.execute(f"""
            SELECT COUNT(DISTINCT c1.cas_id) FROM eval_cases c1
            JOIN eval_cases c2 ON c1.cas_id = c2.cas_id AND c1.run_id = c2.run_id
            WHERE c1.run_id = ? AND c1.branca = 'hardcoded' AND c2.branca = 'rag'
            {filters}
        """, params).fetchone()[0]

        # Get comparative judgements if available
        judgements = {}
        jrows = conn.execute(
            "SELECT cas_id, judge, winner, justification FROM comparative_judgements WHERE run_id = ?",
            (run_id,)
        ).fetchall()
        for j in jrows:
            cid = j["cas_id"]
            if cid not in judgements:
                judgements[cid] = []
            judgements[cid].append({"judge": j["judge"], "winner": j["winner"],
                                    "justification": j["justification"]})

        cases = []
        for r in rows:
            cases.append({
                "cas_id": r["cas_id"],
                "text_id": r["text_id"],
                "perfil_id": r["perfil_id"],
                "etapa": r["etapa"],
                "genere": r["genere"],
                "mecr": r["mecr"],
                "dua": r["dua"],
                "perfils": r["perfils_actius"],
                "text_hc": r["text_hc"],
                "text_rag": r["text_rag"],
                "forma_hc": r["forma_hc"],
                "forma_rag": r["forma_rag"],
                "recall_rag": r["recall_rag"],
                "prompt_hc_len": r["prompt_hc_len"],
                "prompt_rag_len": r["prompt_rag_len"],
                "instr_rag": r["instr_rag"],
                "judgements": judgements.get(r["cas_id"], []),
            })

        conn.close()
        return JSONResponse({"cases": cases, "total": total, "offset": offset, "limit": limit})
    except Exception as e:
        return JSONResponse({"error": str(e)})


@app.get("/api/eval/originals")
async def eval_originals():
    """Retorna els textos originals del dataset."""
    import json as json_mod
    data_path = Path(__file__).parent / "tests" / "test_data.json"
    with open(data_path, encoding="utf-8") as f:
        data = json_mod.load(f)
    return JSONResponse({"textos": data["textos"], "perfils": data["perfils"]})


@app.get("/api/eval/comparative")
async def eval_comparative():
    """Retorna totes les dades del judici comparatiu per al dashboard."""
    try:
        import eval_db
        conn = eval_db.init_db()

        # Judicis per jutge i guanyador
        judges = conn.execute("""
            SELECT judge, winner, COUNT(*) as n
            FROM comparative_judgements
            GROUP BY judge, winner ORDER BY judge, winner
        """).fetchall()

        # Per perfil
        by_profile = conn.execute("""
            SELECT judge, perfil_id, winner, COUNT(*) as n
            FROM comparative_judgements
            GROUP BY judge, perfil_id, winner
            ORDER BY perfil_id, judge
        """).fetchall()

        # Per criteri
        criteria = {}
        for c in ["c1_winner", "c2_winner", "c3_winner", "c4_winner", "c5_winner"]:
            rows = conn.execute(f"""
                SELECT judge, {c} as winner, COUNT(*) as n
                FROM comparative_judgements WHERE {c} IS NOT NULL AND {c} != ''
                GROUP BY judge, {c}
            """).fetchall()
            criteria[c.replace("_winner", "")] = [dict(r) for r in rows]

        # Justificacions (últims 20)
        justifications = conn.execute("""
            SELECT cas_id, judge, winner, confidence, justification
            FROM comparative_judgements
            ORDER BY id DESC LIMIT 20
        """).fetchall()

        # Mètriques forma de la BD
        forma = conn.execute("""
            SELECT branca,
                   AVG(puntuacio_forma) as avg_forma,
                   AVG(recall) as avg_recall,
                   AVG(text_adaptat_length) as avg_len,
                   COUNT(*) as n
            FROM eval_cases WHERE run_id = (SELECT run_id FROM eval_runs ORDER BY timestamp DESC LIMIT 1)
            GROUP BY branca
        """).fetchall()

        conn.close()

        return JSONResponse({
            "judges": [dict(r) for r in judges],
            "by_profile": [dict(r) for r in by_profile],
            "criteria": criteria,
            "justifications": [dict(r) for r in justifications],
            "forma": [dict(r) for r in forma],
        })
    except Exception as e:
        return JSONResponse({"error": str(e)})


@app.get("/api/eval/runs")
async def eval_runs():
    """Llista totes les execucions d'avaluació."""
    try:
        import eval_db
        conn = eval_db.init_db()
        runs = eval_db.get_all_runs(conn)
        conn.close()
        return JSONResponse(runs)
    except Exception as e:
        return JSONResponse({"error": str(e), "runs": []})


@app.get("/api/eval/run/{run_id}")
async def eval_run_detail(run_id: str):
    """Retorna totes les dades d'una execució (per al dashboard)."""
    try:
        import eval_db
        conn = eval_db.init_db()
        data = eval_db.export_run_json(conn, run_id)
        conn.close()
        return JSONResponse(data)
    except Exception as e:
        return JSONResponse({"error": str(e)})


@app.get("/api/eval/progress")
async def eval_progress():
    """Monitoratge en temps real del batch en curs — llegeix directament la BD."""
    try:
        import eval_db
        import sqlite3
        conn = eval_db.init_db()

        # Últim run
        last_run = conn.execute(
            "SELECT run_id, timestamp, total_cases, notes FROM eval_runs ORDER BY timestamp DESC LIMIT 1"
        ).fetchone()
        if not last_run:
            return JSONResponse({"status": "idle", "message": "Cap execució registrada"})

        run_id = last_run["run_id"]
        total_expected = last_run["total_cases"] or 0

        # Casos completats (cada cas genera 2 files: HC + RAG)
        count = conn.execute(
            "SELECT COUNT(*) as n FROM eval_cases WHERE run_id = ?", (run_id,)
        ).fetchone()["n"]
        cases_done = count // 2  # 2 branques per cas

        # Comparacions completades (BLOC 3)
        evals_done = conn.execute(
            "SELECT COUNT(*) as n FROM eval_comparisons WHERE run_id = ?", (run_id,)
        ).fetchone()["n"]

        # Mètriques parcials
        stats = conn.execute("""
            SELECT branca,
                   AVG(puntuacio_forma) as avg_forma,
                   AVG(puntuacio_fons) as avg_fons,
                   AVG(recall) as avg_recall,
                   AVG(text_adaptat_length) as avg_len
            FROM eval_cases WHERE run_id = ?
            GROUP BY branca
        """, (run_id,)).fetchall()

        branca_stats = {}
        for row in stats:
            branca_stats[row["branca"]] = {
                "avg_forma": round(row["avg_forma"], 3) if row["avg_forma"] else None,
                "avg_fons": round(row["avg_fons"], 3) if row["avg_fons"] else None,
                "avg_recall": round(row["avg_recall"], 3) if row["avg_recall"] else None,
                "avg_len": int(row["avg_len"]) if row["avg_len"] else None,
            }

        # Últims 5 casos processats
        recent = conn.execute("""
            SELECT cas_id, branca, puntuacio_forma, text_adaptat_length
            FROM eval_cases WHERE run_id = ?
            ORDER BY id DESC LIMIT 10
        """, (run_id,)).fetchall()
        recent_list = [
            {"cas_id": r["cas_id"], "branca": r["branca"],
             "forma": r["puntuacio_forma"], "len": r["text_adaptat_length"]}
            for r in recent
        ]

        # Veredictes (si n'hi ha)
        veredictes = {}
        if evals_done > 0:
            vrows = conn.execute("""
                SELECT veredicte, COUNT(*) as n
                FROM eval_comparisons WHERE run_id = ?
                GROUP BY veredicte
            """, (run_id,)).fetchall()
            veredictes = {r["veredicte"] or "sense_eval": r["n"] for r in vrows}

        # ── Multi-LLM progress ──
        multi_llm = {}
        try:
            mlg = conn.execute("""
                SELECT generator, prompt_mode, COUNT(*) as n, AVG(puntuacio_forma) as avg_forma,
                       AVG(text_adaptat_paraules) as avg_words
                FROM multi_llm_generations WHERE error IS NULL
                GROUP BY generator, prompt_mode ORDER BY generator
            """).fetchall()
            multi_llm["generations"] = [dict(r) for r in mlg]

            mle = conn.execute("""
                SELECT judge, eval_type, COUNT(*) as n
                FROM multi_llm_evaluations
                GROUP BY judge, eval_type ORDER BY judge
            """).fetchall()
            multi_llm["evaluations"] = [dict(r) for r in mle]

            mlr = conn.execute("""
                SELECT cas_id, generator, prompt_mode, text_adaptat_paraules as words
                FROM multi_llm_generations WHERE error IS NULL
                ORDER BY id DESC LIMIT 10
            """).fetchall()
            multi_llm["recent"] = [dict(r) for r in mlr]

            multi_llm["total_generations"] = conn.execute(
                "SELECT COUNT(*) FROM multi_llm_generations WHERE error IS NULL"
            ).fetchone()[0]
            multi_llm["total_evaluations"] = conn.execute(
                "SELECT COUNT(*) FROM multi_llm_evaluations"
            ).fetchone()[0]
        except Exception:
            pass

        # ── Multi-v2 progress (mateixa BD, taules multi_v2_*) ──
        multi_v2 = {}
        try:
            ind = conn.execute(
                "SELECT judge, COUNT(*) as n FROM multi_v2_evaluations "
                "WHERE run_id='multi_v2' GROUP BY judge"
            ).fetchall()
            multi_v2["individual"] = {r["judge"]: r["n"] for r in ind}

            tri = conn.execute(
                "SELECT judge, COUNT(*) as n FROM multi_v2_trios "
                "WHERE run_id='multi_v2' GROUP BY judge"
            ).fetchall()
            multi_v2["trios"] = {r["judge"]: r["n"] for r in tri}

            cro = conn.execute(
                "SELECT judge, pair, COUNT(*) as n FROM multi_v2_cross "
                "WHERE run_id='multi_v2' GROUP BY judge, pair"
            ).fetchall()
            cross_data = {}
            for r in cro:
                cross_data.setdefault(r["judge"], {})[r["pair"]] = r["n"]
            multi_v2["cross"] = cross_data

            recent_v2 = conn.execute("""
                SELECT e.cas_id, e.judge, g.generator, g.prompt_mode, e.puntuacio_global
                FROM multi_v2_evaluations e
                LEFT JOIN multi_llm_generations g ON e.generation_id = g.id
                WHERE e.run_id = 'multi_v2'
                ORDER BY e.id DESC LIMIT 8
            """).fetchall()
            multi_v2["recent"] = [dict(r) for r in recent_v2]
            multi_v2["_n_recent_raw"] = len(recent_v2)
        except Exception:
            pass

        conn.close()

        is_running = cases_done < total_expected
        pct = round(cases_done / total_expected * 100, 1) if total_expected > 0 else 0

        return JSONResponse({
            "status": "running" if is_running else "completed",
            "run_id": run_id,
            "notes": last_run["notes"],
            "timestamp": last_run["timestamp"],
            "progress": {
                "cases_done": cases_done,
                "total_expected": total_expected,
                "evals_done": evals_done,
                "percentage": pct,
            },
            "partial_stats": branca_stats,
            "veredictes": veredictes,
            "recent_cases": recent_list,
            "multi_llm": multi_llm,
            "multi_v2": multi_v2,
        })
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)})


@app.get("/api/eval/v2debug")
async def eval_v2debug():
    """Debug endpoint per testar multi_v2 recent query."""
    import eval_db, sqlite3
    conn = eval_db.init_db()
    try:
        n_evals = conn.execute("SELECT COUNT(*) FROM multi_v2_evaluations").fetchone()[0]
        n_gens = conn.execute("SELECT COUNT(*) FROM multi_llm_generations").fetchone()[0]
        rows = conn.execute("""
            SELECT e.cas_id, e.judge, g.generator, g.prompt_mode, e.puntuacio_global
            FROM multi_v2_evaluations e
            LEFT JOIN multi_llm_generations g ON e.generation_id = g.id
            WHERE e.run_id = 'multi_v2'
            ORDER BY e.id DESC LIMIT 3
        """).fetchall()
        conn.close()
        return JSONResponse({
            "n_evals": n_evals, "n_gens": n_gens,
            "recent": [dict(r) for r in rows]
        })
    except Exception as e:
        conn.close()
        return JSONResponse({"error": str(e)})


# ── Main ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print("=" * 50)
    print("  ATNE — Adaptador de Textos")
    print(f"  http://localhost:{port}")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=port)
