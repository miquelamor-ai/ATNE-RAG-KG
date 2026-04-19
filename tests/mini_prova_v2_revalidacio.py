"""Revalidacio A/B V1/V2/V3 — ampliacio de la mini prova anterior.

Amplia la mini prova de 36 -> 120 generacions per confirmar la tesi
"V2 >= V3 en la majoria de casos, amb regressio V3 GPT a AACC".

- 4 textos (2 antics + 2 nous) x 5 perfils (3 antics + 2 nous) x 3 variants x 2 models.
- Mateix esquelet que tests/mini_prova_capes_ab.py.
- Analisi automatica post-execucio: regressions, connectors, terminologia, veredicte.

Executa: python tests/mini_prova_v2_revalidacio.py
Sortida: tests/mini_prova_v2_revalidacio.md
"""

from __future__ import annotations

import os
import re
import sys
import time
import traceback
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv  # noqa: E402
load_dotenv(ROOT / ".env")

import corpus_reader  # noqa: E402
import instruction_filter  # noqa: E402
import instruction_catalog  # noqa: E402
import server  # noqa: E402

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURACIO
# ═══════════════════════════════════════════════════════════════════════════

GEMMA_MODEL = "gemma-3-27b-it"
GPT_MODEL = "gpt-4.1-mini"

COST_LIMIT_USD = 0.30  # límit dur

TEXT_A = """L'aigua del planeta es troba en un moviment constant que anomenem cicle hidrològic. Aquest procés comença amb l'evaporació: el Sol escalfa l'aigua dels oceans, rius i llacs, i la transforma en vapor que ascendeix a l'atmosfera. A mesura que el vapor s'eleva, es refreda i condensa formant petites gotes que constitueixen els núvols. Quan aquestes gotes esdevenen prou pesades, precipiten en forma de pluja, neu o calamarsa. Una part de l'aigua precipitada s'infiltra al subsòl i alimenta els aqüífers; una altra part circula per la superfície en forma de rius que, finalment, retornen al mar. Els éssers vius també participen en aquest cicle mitjançant la transpiració: les plantes absorbeixen aigua del sòl i n'alliberen part a l'atmosfera a través de les fulles. Sense aquest cicle, la vida tal com la coneixem seria impossible, ja que assegura la disponibilitat d'aigua dolça per a tots els ecosistemes."""

TEXT_B = """La Revolució Industrial va ser un procés de transformacions econòmiques, socials i tecnològiques que s'inicià al Regne Unit a la segona meitat del segle XVIII i s'expandí progressivament per Europa i Amèrica del Nord durant el segle XIX. L'element desencadenant fou la introducció de la màquina de vapor, que permeté mecanitzar la producció tèxtil i substituir la força humana i animal per energia mecànica. Aquesta innovació propicià l'aparició de les primeres fàbriques, on centenars d'obrers treballaven jornades de més de dotze hores en condicions sovint precàries. La ciutat industrial creixé de manera accelerada, atraient població rural i generant barris obrers amb greus problemes de salubritat. Paral·lelament, sorgí una nova classe social, el proletariat, que començà a organitzar-se per reivindicar millores laborals. La burgesia industrial, propietària dels mitjans de producció, consolidà el seu poder econòmic i polític. Les conseqüències d'aquest procés — la producció en massa, el ferrocarril, el capitalisme modern — configuraren el món contemporani tal com el coneixem avui."""

TEXT_C = """Els ecosistemes mediterranis constitueixen un dels espais naturals més singulars del planeta, caracteritzats per una combinació única de clima, vegetació i fauna. El clima mediterrani presenta estius càlids i secs, i hiverns suaus amb precipitacions irregulars. Aquesta estacionalitat marcada condiciona la vida de tots els organismes que hi habiten. La vegetació típica està formada per alzines, pins, garrigues i màquies, plantes adaptades a la sequera mitjançant fulles petites i coriàcies que redueixen la pèrdua d'aigua. Molts arbustos desenvolupen olis essencials aromàtics —com el romaní, la farigola o la lavanda— que els protegeixen dels herbívors i dels incendis. La fauna mediterrània inclou espècies emblemàtiques com el linx ibèric, l'àguila imperial, la tortuga mediterrània i una gran varietat d'insectes pol·linitzadors. Els incendis forestals, tot i ser destructius a curt termini, formen part del cicle natural: moltes plantes mediterrànies tenen llavors que només germinen després d'un foc. Avui, aquests ecosistemes estan amenaçats per l'abandonament agrícola, l'expansió urbana, el canvi climàtic i l'increment de la freqüència d'incendis descontrolats. La conservació de la biodiversitat mediterrània exigeix una gestió activa del paisatge i polítiques ambientals coherents."""

TEXT_D = """Mercè Rodoreda va néixer a Barcelona el 10 d'octubre de 1908, en una família modesta del barri de Sant Gervasi. Des de petita, la seva àvia Pepa li va transmetre l'amor pels llibres i per la llengua catalana. Va escriure els seus primers contes i novel·les durant els anys trenta, en plena efervescència cultural de la República, però l'esclat de la Guerra Civil el 1936 i la posterior victòria franquista la van obligar a exiliar-se. Va viure anys difícils a França, Suïssa i Anglaterra, sovint en condicions precàries, però sense deixar d'escriure. El 1962 va publicar «La plaça del Diamant», considerada una de les obres cabdals de la literatura catalana del segle XX. La novel·la narra la vida de Colometa, una dona del barri de Gràcia que travessa les penúries de la guerra i la postguerra, i ha estat traduïda a més de trenta llengües. Altres títols fonamentals són «Aloma», «Mirall trencat» i «El carrer de les Camèlies». Rodoreda va tornar definitivament a Catalunya el 1979 i va morir a Girona el 1983. La seva obra, marcada per una sensibilitat profunda i una prosa precisa, continua sent llegida i estudiada arreu del món, i l'autora és considerada una veu imprescindible de la literatura universal contemporània."""

TEXTS = [
    {
        "id": "A", "titol": "El cicle de l'aigua", "materia": "cientific",
        "text": TEXT_A,
        "termes": ["cicle hidrològic", "evaporació", "condensació", "precipitació", "aqüífer", "transpiració"],
    },
    {
        "id": "B", "titol": "La Revolució Industrial", "materia": "humanistic",
        "text": TEXT_B,
        "termes": ["Revolució Industrial", "màquina de vapor", "proletariat", "burgesia industrial"],
    },
    {
        "id": "C", "titol": "Els ecosistemes del Mediterrani", "materia": "cientific",
        "text": TEXT_C,
        "termes": ["ecosistemes", "alzines", "garrigues", "linx ibèric", "biodiversitat"],
    },
    {
        "id": "D", "titol": "Biografia breu de Mercè Rodoreda", "materia": "linguistic",
        "text": TEXT_D,
        "termes": ["Rodoreda", "Colometa", "La plaça del Diamant", "exili", "postguerra"],
    },
]

# ─── Perfils ───
PERFILS = [
    {
        "id": "P1",
        "etiqueta": "Marc Ribera — TDAH ESO B1",
        "tipus": "TDAH",
        "profile": {
            "nom": "Marc Ribera",
            "caracteristiques": {
                "tdah": {"actiu": True, "grau": "moderat"},
            },
        },
        "context": {"etapa": "ESO", "curs": "3r"},
        "params": {
            "mecr_sortida": "B1",
            "dua": "Core",
            "genere_discursiu": "explicació",
            "complements": {},
        },
    },
    {
        "id": "P2",
        "etiqueta": "Pol Vidal — AACC ESO B2",
        "tipus": "AACC",
        "profile": {
            "nom": "Pol Vidal",
            "caracteristiques": {
                "altes_capacitats": {"actiu": True},
            },
        },
        "context": {"etapa": "ESO", "curs": "4t"},
        "params": {
            "mecr_sortida": "B2",
            "dua": "Enriquiment",
            "genere_discursiu": "explicació",
            "complements": {},
        },
    },
    {
        "id": "P3",
        "etiqueta": "Aya Sellami — nouvingut primària A1",
        "tipus": "NOUVINGUT",
        "profile": {
            "nom": "Aya Sellami",
            "caracteristiques": {
                "nouvingut": {"actiu": True, "L1": "àrab", "mesos_catalunya": 3},
            },
        },
        "context": {"etapa": "primària", "curs": "4t"},
        "params": {
            "mecr_sortida": "A1",
            "dua": "Accés",
            "genere_discursiu": "explicació",
            "complements": {},
        },
    },
    {
        "id": "P4",
        "etiqueta": "Laia Puig — dislèxia ESO B1",
        "tipus": "DISLEXIA",
        "profile": {
            "nom": "Laia Puig",
            "caracteristiques": {
                "dislexia": {"actiu": True, "tipus_fonologica": True},
            },
        },
        "context": {"etapa": "ESO", "curs": "3r"},
        "params": {
            "mecr_sortida": "B1",
            "dua": "Core",
            "genere_discursiu": "explicació",
            "complements": {},
        },
    },
    {
        "id": "P5",
        "etiqueta": "Pau Sala — TDAH primària B1",
        "tipus": "TDAH",
        "profile": {
            "nom": "Pau Sala",
            "caracteristiques": {
                "tdah": {"actiu": True, "grau": "moderat"},
            },
        },
        "context": {"etapa": "primària", "curs": "5è"},
        "params": {
            "mecr_sortida": "B1",
            "dua": "Core",
            "genere_discursiu": "explicació",
            "complements": {},
        },
    },
]

MODELS = [
    {"id": "gemma", "nom": "Gemma 3 27B", "model_id": GEMMA_MODEL},
    {"id": "gpt", "nom": "GPT-4.1-mini", "model_id": GPT_MODEL},
]


# ═══════════════════════════════════════════════════════════════════════════
# CONSTRUCTORS DE PROMPTS (V1, V2, V3)
# ═══════════════════════════════════════════════════════════════════════════

def build_prompt_v1(profile: dict, context: dict, params: dict) -> str:
    """V1 = identitat + DUA + gènere + persona-audience (SENSE catàleg)."""
    mecr = params.get("mecr_sortida", "B2")
    dua = params.get("dua", "Core")
    parts = []

    parts.append(corpus_reader.get_identity())

    dua_block = corpus_reader.get_dua_block(dua)
    if dua_block:
        parts.append(dua_block)

    genre = params.get("genere_discursiu", "")
    if genre:
        genre_block = corpus_reader.get_genre_block(genre)
        if genre_block:
            parts.append(genre_block)

    persona = server.build_persona_audience(profile, context, mecr)
    parts.append(f"PERSONA-AUDIENCE:\n{persona}")

    parts.append(
        "FORMAT DE SORTIDA:\n"
        "Respon amb la secció ## Text adaptat amb el text complet adaptat."
    )
    return "\n\n".join(parts)


def build_prompt_v2(profile: dict, context: dict, params: dict) -> str:
    """V2 = identitat + instruccions filtrades per MECR + gènere (SENSE DUA ni persona)."""
    parts = []

    parts.append(corpus_reader.get_identity())

    filtered = instruction_filter.get_instructions(profile, params)
    instructions_text = instruction_filter.format_instructions_for_prompt(filtered)
    parts.append(instructions_text)

    genre = params.get("genere_discursiu", "")
    if genre:
        genre_block = corpus_reader.get_genre_block(genre)
        if genre_block:
            parts.append(genre_block)

    parts.append(
        "FORMAT DE SORTIDA:\n"
        "Respon amb la secció ## Text adaptat amb el text complet adaptat."
    )
    return "\n\n".join(parts)


def build_prompt_v3(profile: dict, context: dict, params: dict) -> str:
    """V3 = baseline complet (equivalent a build_system_prompt actual)."""
    return server.build_system_prompt(profile, context, params, "")


VARIANTS = [
    {"id": "V1", "desc": "identitat + DUA + gènere + persona (sense catàleg)", "fn": build_prompt_v1},
    {"id": "V2", "desc": "identitat + catàleg filtrat + gènere (sense DUA ni persona)", "fn": build_prompt_v2},
    {"id": "V3", "desc": "baseline complet (build_system_prompt)", "fn": build_prompt_v3},
]


# ═══════════════════════════════════════════════════════════════════════════
# CRIDES ALS MODELS
# ═══════════════════════════════════════════════════════════════════════════

def call_gemma(system_prompt: str, text: str, max_retries: int = 3):
    from google import genai
    from google.genai import types

    keys = server.GEMMA4_API_KEYS
    if not keys:
        return {
            "ok": False, "response": "", "latency_s": 0.0,
            "error": "No hi ha claus GEMMA4 configurades al .env",
            "tokens_in": None, "tokens_out": None,
        }

    errors = []
    t0 = time.time()
    for attempt in range(max_retries):
        for idx in range(len(keys)):
            client = genai.Client(
                api_key=keys[idx],
                http_options=types.HttpOptions(timeout=300_000),
            )
            try:
                full = f"{system_prompt}\n\n---\n\nTEXT ORIGINAL A ADAPTAR:\n\n{text}"
                resp = client.models.generate_content(
                    model=GEMMA_MODEL,
                    contents=[types.Content(role="user", parts=[types.Part(text=full)])],
                    config=types.GenerateContentConfig(
                        temperature=0.4, max_output_tokens=8192,
                    ),
                )
                latency = time.time() - t0
                out = resp.text or ""
                usage = getattr(resp, "usage_metadata", None)
                tin = getattr(usage, "prompt_token_count", None) if usage else None
                tout = getattr(usage, "candidates_token_count", None) if usage else None
                return {
                    "ok": True, "response": out, "latency_s": latency, "error": "",
                    "tokens_in": tin, "tokens_out": tout,
                }
            except Exception as e:
                msg = str(e)[:250]
                errors.append(f"clau {idx+1} (try {attempt+1}): {msg}")
                if "429" in msg or "quota" in msg.lower() or "exhausted" in msg.lower():
                    time.sleep(2 + attempt * 3)
                continue
    latency = time.time() - t0
    return {
        "ok": False, "response": "", "latency_s": latency,
        "error": "; ".join(errors[-4:]),
        "tokens_in": None, "tokens_out": None,
    }


def call_gpt(system_prompt: str, text: str):
    from openai import OpenAI
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return {
            "ok": False, "response": "", "latency_s": 0.0,
            "error": "OPENAI_API_KEY no configurada",
            "tokens_in": None, "tokens_out": None,
        }
    t0 = time.time()
    try:
        client = OpenAI(api_key=key)
        resp = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"TEXT ORIGINAL A ADAPTAR:\n\n{text}"},
            ],
            max_tokens=8192,
            temperature=0.4,
        )
        latency = time.time() - t0
        out = resp.choices[0].message.content or ""
        usage = resp.usage
        return {
            "ok": True, "response": out, "latency_s": latency, "error": "",
            "tokens_in": usage.prompt_tokens if usage else None,
            "tokens_out": usage.completion_tokens if usage else None,
        }
    except Exception as e:
        latency = time.time() - t0
        return {
            "ok": False, "response": "", "latency_s": latency,
            "error": str(e)[:400],
            "tokens_in": None, "tokens_out": None,
        }


def call_model(model_id: str, system_prompt: str, text: str):
    if model_id == "gemma":
        return call_gemma(system_prompt, text)
    elif model_id == "gpt":
        return call_gpt(system_prompt, text)
    raise ValueError(f"Model desconegut: {model_id}")


# ═══════════════════════════════════════════════════════════════════════════
# UTILITATS ANALITIQUES
# ═══════════════════════════════════════════════════════════════════════════

def word_count(s: str) -> int:
    return len([w for w in s.split() if w.strip()])


def estimate_cost_gpt(tokens_in: int | None, tokens_out: int | None) -> float:
    if tokens_in is None or tokens_out is None:
        return 0.0
    cin = (tokens_in / 1_000_000) * 0.40
    cout = (tokens_out / 1_000_000) * 1.60
    return cin + cout


def extract_text_adapted(response: str) -> str:
    """Extreu la seccio '## Text adaptat' si existeix; altrament retorna tot."""
    if not response:
        return ""
    # Busca capcalera i talla fins seguent ## (per evitar 'argumentacio pedagogica')
    m = re.search(r"##\s*Text adaptat\s*\n", response, flags=re.IGNORECASE)
    if m:
        start = m.end()
        rest = response[start:]
        # Tallar al seguent ## (altra seccio)
        m2 = re.search(r"\n##\s+", rest)
        if m2:
            return rest[:m2.start()].strip()
        return rest.strip()
    return response.strip()


REGRESSIO_PATTERNS = [
    r"dificultats lectores",
    r"nouvinguts",
    r"alumnes amb dislèxia",
    r"alumnes amb dislexia",
    r"simplificat",
    r"simplificada",
    r"frases senzilles",
    r"evitant subordinades",
    r"llenguatge senzill",
    r"vocabulari senzill",
]

def detect_regressions(text_adapted: str) -> list[str]:
    """Retorna la llista de patrons de regressio detectats al text adaptat."""
    if not text_adapted:
        return []
    lower = text_adapted.lower()
    hits = []
    for pat in REGRESSIO_PATTERNS:
        if re.search(pat, lower):
            hits.append(pat)
    return hits


CONNECTORS_TEMPORALS = [
    "Primer",
    "Després",
    "Després,",
    "Finalment",
    "Finalment,",
    "Per començar",
    "A continuació",
    "Primerament",
    "Llavors",
    "Al principi",
]

def count_connectors(text_adapted: str) -> int:
    """Compta aparicions (case-insensitive) de connectors temporals a inici de frase o enlloc."""
    if not text_adapted:
        return 0
    n = 0
    for c in CONNECTORS_TEMPORALS:
        pattern = r"(?:^|[\.\n\s])" + re.escape(c) + r"\b"
        n += len(re.findall(pattern, text_adapted, flags=re.IGNORECASE))
    return n


def avg_words_per_sentence(text_adapted: str) -> float:
    """Mitjana de paraules per frase (split aproximat per '. ', '! ', '? ', '\n')."""
    if not text_adapted:
        return 0.0
    # Eliminem markdown headers/bullets per no comptar-los com a frases
    clean = re.sub(r"[#*_`>]+", "", text_adapted)
    # Split per punts seguits d'espai/final i per salts de linia
    parts = re.split(r"(?<=[\.\!\?])\s+|\n+", clean)
    sents = [p.strip() for p in parts if p.strip() and len(p.strip()) > 3]
    if not sents:
        return 0.0
    total = sum(word_count(s) for s in sents)
    return total / len(sents)


def count_preserved_terms(text_adapted: str, terms: list[str]) -> tuple[int, list[str]]:
    """Compta quants termes tecnics del text original es preserven a l'adaptacio."""
    if not text_adapted:
        return 0, []
    lower = text_adapted.lower()
    found = []
    for t in terms:
        if t.lower() in lower:
            found.append(t)
    return len(found), found


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 70)
    print("Revalidacio A/B V1/V2/V3 — ampliacio de la mini prova")
    print("=" * 70)

    stats = instruction_catalog.get_catalog_stats()
    print(f"\nCataleg instruccions: {stats}")
    print(f"\nVariants: {[v['id'] for v in VARIANTS]}")
    print(f"Models: {[m['nom'] for m in MODELS]}")
    print(f"Perfils: {[p['id'] for p in PERFILS]}")
    print(f"Textos: {[t['id'] for t in TEXTS]}")
    n_total = len(TEXTS) * len(PERFILS) * len(VARIANTS) * len(MODELS)
    print(f"Total crides previstes: {n_total}\n")

    # Construir els 15 prompts base (5 perfils x 3 variants) — sense matèria
    prompts = {}
    for perfil in PERFILS:
        for variant in VARIANTS:
            pr = variant["fn"](perfil["profile"], perfil["context"], perfil["params"])
            prompts[(perfil["id"], variant["id"])] = pr
            print(f"  Prompt {perfil['id']}-{variant['id']}: {word_count(pr)} paraules, {len(pr)} chars")

    # Executar totes les combinacions
    results = []
    failures = []
    aborted = False
    start_global = time.time()
    n_done = 0
    running_gpt_cost = 0.0

    for text in TEXTS:
        if aborted:
            break
        for perfil in PERFILS:
            if aborted:
                break
            perfil_params = dict(perfil["params"])
            perfil_params["materia"] = text["materia"]
            perfil_params["etapa"] = perfil["context"]["etapa"]
            perfil_params["mecr"] = perfil["params"]["mecr_sortida"]

            for variant in VARIANTS:
                if aborted:
                    break
                try:
                    prompt = variant["fn"](perfil["profile"], perfil["context"], perfil_params)
                except Exception as e:
                    prompt = prompts[(perfil["id"], variant["id"])]
                    print(f"  [AVIS] Error construint prompt: {e} — uso prompt sense materia")

                for model in MODELS:
                    n_done += 1
                    tag = f"[{n_done}/{n_total}] text={text['id']} perfil={perfil['id']} variant={variant['id']} model={model['id']}"
                    print(f"\n{tag}")

                    # Check cost limit abans de la cride GPT
                    if model["id"] == "gpt" and running_gpt_cost >= COST_LIMIT_USD:
                        print(f"   -> ATURAT: cost GPT ${running_gpt_cost:.4f} ha arribat al limit ${COST_LIMIT_USD}")
                        failures.append({
                            "text": text["id"], "perfil": perfil["id"],
                            "variant": variant["id"], "model": model["id"],
                            "error": f"cost limit ${COST_LIMIT_USD} assolit",
                        })
                        aborted = True
                        break

                    try:
                        r = call_model(model["id"], prompt, text["text"])
                        status = "OK" if r["ok"] else "FAILED"
                        print(f"   -> {status} ({r['latency_s']:.1f}s, "
                              f"{word_count(r['response'])} paraules, "
                              f"tokens_in={r['tokens_in']} tokens_out={r['tokens_out']})")
                        if not r["ok"]:
                            print(f"   error: {r['error'][:200]}")
                            failures.append({
                                "text": text["id"], "perfil": perfil["id"],
                                "variant": variant["id"], "model": model["id"],
                                "error": r["error"],
                            })
                        if model["id"] == "gpt" and r["ok"]:
                            running_gpt_cost += estimate_cost_gpt(r["tokens_in"], r["tokens_out"])
                            print(f"   cost GPT acumulat: ${running_gpt_cost:.4f}")
                    except Exception as e:
                        r = {
                            "ok": False, "response": "", "latency_s": 0.0,
                            "error": f"Excepcio Python: {e}\n{traceback.format_exc()[:500]}",
                            "tokens_in": None, "tokens_out": None,
                        }
                        failures.append({
                            "text": text["id"], "perfil": perfil["id"],
                            "variant": variant["id"], "model": model["id"],
                            "error": str(e),
                        })
                        print(f"   -> EXCEPCIO: {e}")

                    # Metriques analitiques
                    text_adapted = extract_text_adapted(r["response"])
                    regressions = detect_regressions(text_adapted)
                    connectors = count_connectors(text_adapted)
                    awps = avg_words_per_sentence(text_adapted)
                    preserved_n, preserved = count_preserved_terms(text_adapted, text["termes"])

                    results.append({
                        "text_id": text["id"],
                        "text_titol": text["titol"],
                        "text_termes": text["termes"],
                        "perfil_id": perfil["id"],
                        "perfil_etiqueta": perfil["etiqueta"],
                        "perfil_tipus": perfil["tipus"],
                        "variant_id": variant["id"],
                        "variant_desc": variant["desc"],
                        "model_id": model["id"],
                        "model_nom": model["nom"],
                        "prompt": prompt,
                        "response": r["response"],
                        "text_adapted": text_adapted,
                        "latency_s": r["latency_s"],
                        "tokens_in": r["tokens_in"],
                        "tokens_out": r["tokens_out"],
                        "error": r.get("error", ""),
                        "ok": r["ok"],
                        "words_out": word_count(r["response"]),
                        "words_adapted": word_count(text_adapted),
                        "regressions": regressions,
                        "connectors_temporals": connectors,
                        "avg_words_per_sentence": awps,
                        "preserved_count": preserved_n,
                        "preserved_terms": preserved,
                        "dua": perfil["params"]["dua"],
                        "mecr": perfil["params"]["mecr_sortida"],
                    })

    total_elapsed = time.time() - start_global
    print(f"\n\nTotal temps: {total_elapsed:.1f}s · exits: {sum(1 for r in results if r['ok'])}/{len(results)}")
    print(f"Cost GPT-4.1-mini estimat: ${running_gpt_cost:.4f}")

    out_path = ROOT / "tests" / "mini_prova_v2_revalidacio.md"
    write_markdown(out_path, results, stats, prompts, failures, total_elapsed, running_gpt_cost, aborted)
    print(f"\nResultats escrits a: {out_path}")


# ═══════════════════════════════════════════════════════════════════════════
# VEREDICTE AUTOMATIC
# ═══════════════════════════════════════════════════════════════════════════

def compute_verdict_cell(v2: dict, v3: dict, perfil: dict) -> tuple[str, str]:
    """Per un (text, perfil, model), dona veredicte V2 vs V3 amb justificacio.
    Retorna (veredicte, motiu).
    Regles:
      - Si (perfil AACC + Enriquiment) i V3 te regressions i V2 no -> V2 > V3
      - Si (perfil NOUVINGUT + A1) i V3 te mes connectors i frases mes curtes -> V3 > V2
      - Si |diff paraules|<15% i preservacio similar -> V2 ≈ V3
      - Cas generic: comparar regressions, connectors i preservacio
      - Altres -> AMBIGU
    """
    if not (v2 and v3 and v2.get("ok") and v3.get("ok")):
        return "N/A", "alguna crida FAILED"

    v2_regs = v2["regressions"]
    v3_regs = v3["regressions"]
    v2_con = v2["connectors_temporals"]
    v3_con = v3["connectors_temporals"]
    v2_awps = v2["avg_words_per_sentence"]
    v3_awps = v3["avg_words_per_sentence"]
    v2_wa = v2["words_adapted"] or 1
    v3_wa = v3["words_adapted"] or 1
    v2_pres = v2["preserved_count"]
    v3_pres = v3["preserved_count"]

    diff_words_pct = abs(v2_wa - v3_wa) / max(v2_wa, v3_wa) * 100.0
    pres_similar = abs(v2_pres - v3_pres) <= 1

    # Regla 1: AACC + Enriquiment amb regressio V3 no V2
    if perfil["tipus"] == "AACC" and perfil["params"]["dua"] == "Enriquiment":
        if len(v3_regs) > 0 and len(v2_regs) == 0:
            return "V2 > V3", f"V3 te regressio ({','.join(v3_regs)}), V2 no"
        if len(v3_regs) > 0 and len(v2_regs) > 0:
            if len(v3_regs) > len(v2_regs):
                return "V2 > V3", f"V3 mes regressions ({len(v3_regs)}) que V2 ({len(v2_regs)})"
        if len(v3_regs) == 0 and len(v2_regs) == 0:
            # no regressio detectada; comparar paraules/preservacio
            if diff_words_pct < 15 and pres_similar:
                return "V2 ≈ V3", f"sense regressio, diff paraules {diff_words_pct:.0f}%, preservacio similar"

    # Regla 2: Nouvingut A1
    if perfil["tipus"] == "NOUVINGUT" and perfil["params"]["mecr_sortida"] == "A1":
        if v3_con > v2_con and v3_awps < v2_awps:
            return "V3 > V2", f"V3 mes connectors ({v3_con}>{v2_con}) i frases curtes ({v3_awps:.1f}<{v2_awps:.1f})"
        if v2_con > v3_con and v2_awps < v3_awps:
            return "V2 > V3", f"V2 mes connectors ({v2_con}>{v3_con}) i frases curtes ({v2_awps:.1f}<{v3_awps:.1f})"

    # Regla generica: empat si tot similar
    if diff_words_pct < 15 and pres_similar and len(v2_regs) == len(v3_regs):
        return "V2 ≈ V3", f"diff paraules {diff_words_pct:.0f}%, preservacio similar ({v2_pres}/{v3_pres}), regressions iguals"

    # Si V2 te mes regressio -> V3 > V2
    if len(v2_regs) > len(v3_regs):
        return "V3 > V2", f"V2 mes regressions ({len(v2_regs)}) que V3 ({len(v3_regs)})"
    if len(v3_regs) > len(v2_regs):
        return "V2 > V3", f"V3 mes regressions ({len(v3_regs)}) que V2 ({len(v2_regs)})"

    # Preservacio divergent
    if v2_pres > v3_pres + 1:
        return "V2 > V3", f"V2 preserva mes termes ({v2_pres} vs {v3_pres})"
    if v3_pres > v2_pres + 1:
        return "V3 > V2", f"V3 preserva mes termes ({v3_pres} vs {v2_pres})"

    return "AMBIGU", f"diff paraules {diff_words_pct:.0f}%, preservacio {v2_pres}/{v3_pres}, regressions {len(v2_regs)}/{len(v3_regs)}"


# ═══════════════════════════════════════════════════════════════════════════
# ESCRIPTURA MARKDOWN
# ═══════════════════════════════════════════════════════════════════════════

def write_markdown(path: Path, results: list, catalog_stats: dict, prompts: dict,
                   failures: list, total_elapsed: float, gpt_cost: float, aborted: bool):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = []
    lines.append("# Revalidacio A/B V1/V2/V3 — resultats")
    lines.append("")
    lines.append(f"**Data execucio**: {now}")
    lines.append(f"**Durada total**: {total_elapsed:.1f}s")
    lines.append(f"**Crides totals**: {len(results)}")
    n_ok = sum(1 for r in results if r["ok"])
    lines.append(f"**Crides OK**: {n_ok}")
    lines.append(f"**Crides FAILED**: {len(results) - n_ok}")
    lines.append(f"**Cost GPT-4.1-mini estimat**: ${gpt_cost:.4f}")
    if aborted:
        lines.append(f"**AVIS**: execucio aturada pel limit de cost ${COST_LIMIT_USD}")
    lines.append("")

    # Parametres
    lines.append("## Parametres")
    lines.append("")
    lines.append(f"- **Cataleg**: {catalog_stats}")
    lines.append(f"- **Models**: Gemma 3 27B (`{GEMMA_MODEL}`) · GPT-4.1-mini (`{GPT_MODEL}`)")
    lines.append(f"- **Perfils**: {', '.join(p['etiqueta'] for p in PERFILS)}")
    lines.append("- **Textos**:")
    for t in TEXTS:
        lines.append(f"  - {t['id']} — {t['titol']} ({word_count(t['text'])} paraules, materia {t['materia']})")
    lines.append("")

    # ═════════ SECCIO 1: VEREDICTE GLOBAL (PRIMER) ═════════
    lines.append("---")
    lines.append("")
    lines.append("## 1. Veredicte global (V2 vs V3)")
    lines.append("")
    lines.append("Sobre 40 comparacions (5 perfils × 4 textos × 2 models):")
    lines.append("")

    counts = {"V2 > V3": 0, "V2 ≈ V3": 0, "V3 > V2": 0, "AMBIGU": 0, "N/A": 0}
    verdict_rows = []

    for perfil in PERFILS:
        for model in MODELS:
            cell_counts = {"V2 > V3": 0, "V2 ≈ V3": 0, "V3 > V2": 0, "AMBIGU": 0, "N/A": 0}
            for text in TEXTS:
                v2 = next((r for r in results if r["text_id"] == text["id"] and r["perfil_id"] == perfil["id"] and r["variant_id"] == "V2" and r["model_id"] == model["id"]), None)
                v3 = next((r for r in results if r["text_id"] == text["id"] and r["perfil_id"] == perfil["id"] and r["variant_id"] == "V3" and r["model_id"] == model["id"]), None)
                verdict, motiu = compute_verdict_cell(v2, v3, perfil)
                counts[verdict] += 1
                cell_counts[verdict] += 1
                verdict_rows.append({
                    "perfil": perfil["id"], "perfil_tipus": perfil["tipus"],
                    "model": model["id"], "text": text["id"],
                    "verdict": verdict, "motiu": motiu,
                })
            # Cell summary
            resum_cel = " ".join(f"{k}:{v}" for k, v in cell_counts.items() if v > 0)
            # Veredicte dominant de la cel·la
            if cell_counts["V2 > V3"] > cell_counts["V3 > V2"]:
                dom = "V2 guanya"
            elif cell_counts["V3 > V2"] > cell_counts["V2 > V3"]:
                dom = "V3 guanya"
            else:
                dom = "empat"
            lines.append(f"- **{perfil['etiqueta']} · {model['nom']}**: {resum_cel} → {dom}")

    lines.append("")
    lines.append("### Distribucio global (sobre 40 comparacions)")
    lines.append("")
    lines.append(f"- **V2 > V3**: {counts['V2 > V3']} ({100*counts['V2 > V3']/40:.0f}%)")
    lines.append(f"- **V2 ≈ V3**: {counts['V2 ≈ V3']} ({100*counts['V2 ≈ V3']/40:.0f}%)")
    lines.append(f"- **V3 > V2**: {counts['V3 > V2']} ({100*counts['V3 > V2']/40:.0f}%)")
    lines.append(f"- **AMBIGU**: {counts['AMBIGU']} ({100*counts['AMBIGU']/40:.0f}%)")
    lines.append(f"- **N/A (failed)**: {counts['N/A']}")
    lines.append("")

    # Tesi: V2 >= V3 i regressio V3 GPT a AACC
    v2_o_empat = counts["V2 > V3"] + counts["V2 ≈ V3"]
    v3_wins = counts["V3 > V2"]
    tesi_ok = v2_o_empat >= v3_wins
    lines.append("### Avaluacio de la tesi inicial")
    lines.append("")
    lines.append(f"> Tesi: \"V2 ≥ V3 en la majoria de casos, amb regressio V3 GPT a AACC\".")
    lines.append("")
    lines.append(f"- V2 ≥ V3 (suma de V2>V3 + V2≈V3): **{v2_o_empat}** / V3>V2: **{v3_wins}** → tesi **{'CONFIRMADA' if tesi_ok else 'NO CONFIRMADA'}**.")
    # Regressions en AACC
    aacc_v3_regs = [r for r in results if r["perfil_tipus"] == "AACC" and r["variant_id"] == "V3" and r["ok"] and len(r["regressions"]) > 0]
    aacc_v3_regs_gpt = [r for r in aacc_v3_regs if r["model_id"] == "gpt"]
    aacc_v3_regs_gemma = [r for r in aacc_v3_regs if r["model_id"] == "gemma"]
    lines.append(f"- Regressions V3 a AACC: {len(aacc_v3_regs_gpt)}/4 GPT · {len(aacc_v3_regs_gemma)}/4 Gemma.")
    lines.append("")

    # Taula resum (perfil, model, text, veredicte)
    lines.append("### Taula resum (40 comparacions)")
    lines.append("")
    lines.append("| Perfil | Model | Text | Veredicte | Motiu |")
    lines.append("|---|---|---|---|---|")
    for row in verdict_rows:
        lines.append(f"| {row['perfil']} ({row['perfil_tipus']}) | {row['model']} | {row['text']} | **{row['verdict']}** | {row['motiu']} |")
    lines.append("")

    # ═════════ SECCIO 2: METRIQUES DETALLADES ═════════
    lines.append("---")
    lines.append("")
    lines.append("## 2. Metriques detallades per cel·la")
    lines.append("")
    lines.append("Per cada (text, perfil, model): paraules, latencia, connectors temporals, frases mitjana, termes preservats, regressions.")
    lines.append("")
    lines.append("| Text | Perfil | Variant | Model | Paraules | Latencia | Connectors | Pal/frase | Termes preservats | Regressions |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|")
    for r in results:
        if not r["ok"]:
            lines.append(f"| {r['text_id']} | {r['perfil_id']} | {r['variant_id']} | {r['model_id']} | FAIL | — | — | — | — | — |")
            continue
        regs = ",".join(r["regressions"]) if r["regressions"] else "—"
        lines.append(
            f"| {r['text_id']} | {r['perfil_id']} | {r['variant_id']} | {r['model_id']} | "
            f"{r['words_adapted']} | {r['latency_s']:.1f}s | {r['connectors_temporals']} | "
            f"{r['avg_words_per_sentence']:.1f} | {r['preserved_count']}/{len(r['text_termes'])} | {regs} |"
        )
    lines.append("")

    # Mitjanes per perfil i variant
    lines.append("### Mitjanes per perfil × variant (agregades entre models i textos)")
    lines.append("")
    lines.append("| Perfil | Variant | Mitjana paraules | Mitjana connectors | Mitjana pal/frase | Mitjana termes preservats |")
    lines.append("|---|---|---|---|---|---|")
    for perfil in PERFILS:
        for variant in VARIANTS:
            rs = [r for r in results if r["ok"] and r["perfil_id"] == perfil["id"] and r["variant_id"] == variant["id"]]
            if not rs:
                lines.append(f"| {perfil['id']} | {variant['id']} | — | — | — | — |")
                continue
            aw = sum(r["words_adapted"] for r in rs) / len(rs)
            ac = sum(r["connectors_temporals"] for r in rs) / len(rs)
            awps = sum(r["avg_words_per_sentence"] for r in rs) / len(rs)
            ap = sum(r["preserved_count"] for r in rs) / len(rs)
            lines.append(f"| {perfil['id']} | {variant['id']} | {aw:.0f} | {ac:.1f} | {awps:.1f} | {ap:.1f} |")
    lines.append("")

    # ═════════ SECCIO 3: CASOS INTERESSANTS ═════════
    lines.append("---")
    lines.append("")
    lines.append("## 3. Casos interessants")
    lines.append("")

    # 3a. Regressions detectades
    lines.append("### 3a. Regressions detectades (mencions explicites a al text adaptat)")
    lines.append("")
    regs_all = [r for r in results if r["ok"] and r["regressions"]]
    if not regs_all:
        lines.append("Cap regressio detectada als textos adaptats.")
    else:
        lines.append(f"Total: {len(regs_all)} casos amb una o mes mencions explicites.")
        lines.append("")
        lines.append("| Perfil | Text | Variant | Model | Patrons detectats |")
        lines.append("|---|---|---|---|---|")
        for r in regs_all:
            lines.append(f"| {r['perfil_id']} ({r['perfil_tipus']}) | {r['text_id']} | {r['variant_id']} | {r['model_id']} | {', '.join(r['regressions'])} |")
    lines.append("")

    # 3b. Connectors nouvingut (Aya)
    lines.append("### 3b. Connectors temporals en perfil nouvingut (Aya, P3)")
    lines.append("")
    lines.append("| Model | Text | V1 connectors | V2 connectors | V3 connectors | V3 > V2? |")
    lines.append("|---|---|---|---|---|---|")
    for model in MODELS:
        for text in TEXTS:
            v1 = next((r for r in results if r["perfil_id"] == "P3" and r["text_id"] == text["id"] and r["variant_id"] == "V1" and r["model_id"] == model["id"] and r["ok"]), None)
            v2 = next((r for r in results if r["perfil_id"] == "P3" and r["text_id"] == text["id"] and r["variant_id"] == "V2" and r["model_id"] == model["id"] and r["ok"]), None)
            v3 = next((r for r in results if r["perfil_id"] == "P3" and r["text_id"] == text["id"] and r["variant_id"] == "V3" and r["model_id"] == model["id"] and r["ok"]), None)
            c1 = v1["connectors_temporals"] if v1 else "—"
            c2 = v2["connectors_temporals"] if v2 else "—"
            c3 = v3["connectors_temporals"] if v3 else "—"
            mes = "SI" if (v2 and v3 and v3["connectors_temporals"] > v2["connectors_temporals"]) else "no"
            lines.append(f"| {model['id']} | {text['id']} | {c1} | {c2} | {c3} | {mes} |")
    lines.append("")

    # 3c. Complexitat sintactica Aya
    lines.append("### 3c. Complexitat sintactica en perfil nouvingut A1 (Aya, P3)")
    lines.append("")
    lines.append("| Model | Text | V1 pal/frase | V2 pal/frase | V3 pal/frase | V3 < V2? |")
    lines.append("|---|---|---|---|---|---|")
    for model in MODELS:
        for text in TEXTS:
            v1 = next((r for r in results if r["perfil_id"] == "P3" and r["text_id"] == text["id"] and r["variant_id"] == "V1" and r["model_id"] == model["id"] and r["ok"]), None)
            v2 = next((r for r in results if r["perfil_id"] == "P3" and r["text_id"] == text["id"] and r["variant_id"] == "V2" and r["model_id"] == model["id"] and r["ok"]), None)
            v3 = next((r for r in results if r["perfil_id"] == "P3" and r["text_id"] == text["id"] and r["variant_id"] == "V3" and r["model_id"] == model["id"] and r["ok"]), None)
            a1 = f"{v1['avg_words_per_sentence']:.1f}" if v1 else "—"
            a2 = f"{v2['avg_words_per_sentence']:.1f}" if v2 else "—"
            a3 = f"{v3['avg_words_per_sentence']:.1f}" if v3 else "—"
            mes = "SI" if (v2 and v3 and v3["avg_words_per_sentence"] < v2["avg_words_per_sentence"]) else "no"
            lines.append(f"| {model['id']} | {text['id']} | {a1} | {a2} | {a3} | {mes} |")
    lines.append("")

    # ═════════ SECCIO 4: SORTIDES SENCERES (DESPLEGABLES) ═════════
    lines.append("---")
    lines.append("")
    lines.append("## 4. Sortides senceres (desplegables)")
    lines.append("")

    for text in TEXTS:
        for perfil in PERFILS:
            lines.append(f"### Text {text['id']} ({text['titol']}) · Perfil {perfil['id']} ({perfil['etiqueta']})")
            lines.append("")
            for variant in VARIANTS:
                for model in MODELS:
                    r = next((x for x in results if x["text_id"] == text["id"] and x["perfil_id"] == perfil["id"] and x["variant_id"] == variant["id"] and x["model_id"] == model["id"]), None)
                    if not r:
                        continue
                    status = "OK" if r["ok"] else "FAILED"
                    lines.append("<details>")
                    summary = f"{variant['id']} · {model['nom']} · {status} · {r['words_adapted']} paraules · {r['latency_s']:.1f}s"
                    if r["ok"] and r["regressions"]:
                        summary += f" · REGRESSIO ({len(r['regressions'])})"
                    lines.append(f"<summary>{summary}</summary>")
                    lines.append("")
                    if r["ok"]:
                        lines.append("```markdown")
                        lines.append(r["response"].strip())
                        lines.append("```")
                    else:
                        lines.append(f"_FAILED_: `{r['error'][:400]}`")
                    lines.append("")
                    lines.append("</details>")
                    lines.append("")

    # ═════════ SECCIO 5: ANNEX PROMPTS ═════════
    lines.append("---")
    lines.append("")
    lines.append("## 5. Annex — prompts generats (15 combinacions perfil × variant)")
    lines.append("")
    for perfil in PERFILS:
        for variant in VARIANTS:
            key = (perfil["id"], variant["id"])
            pr = prompts.get(key, "")
            lines.append("<details>")
            lines.append(f"<summary>Prompt {perfil['id']} — {perfil['etiqueta']} · Variant {variant['id']} ({word_count(pr)} paraules, {len(pr)} chars)</summary>")
            lines.append("")
            lines.append("```text")
            lines.append(pr)
            lines.append("```")
            lines.append("")
            lines.append("</details>")
            lines.append("")

    # Failures
    if failures:
        lines.append("---")
        lines.append("")
        lines.append("## Errors (FAILED)")
        lines.append("")
        for f in failures:
            lines.append(f"- text={f['text']} perfil={f['perfil']} variant={f['variant']} model={f['model']}: `{f['error'][:300]}`")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
