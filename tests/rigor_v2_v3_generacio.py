"""Fase A — generacio rigorosa V2 vs V3 (360 casos).

Pre-registre: docs/estudi_v2_vs_v3_preregistre.md

Disseny factorial:
    5 perfils x 6 textos x 2 variants (V2, V3) x 2 models (Gemma 3 27B, GPT-4.1-mini) x 3 repliques = 360

Temperatura = 0.7 (per capturar variabilitat).
Ordre d'execucio aleatoritzat per minimitzar efectes temporals.

Aquest script NOMES genera. L'avaluacio la fa la Fase B.

Executa:
    python tests/rigor_v2_v3_generacio.py

Sortides:
    - tests/rigor_v2_v3_dades.jsonl   (una linia per cel·la)
    - tests/_rigor_generacio.log      (progress log amb timestamps)
"""

from __future__ import annotations

import json
import os
import random
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv  # noqa: E402
load_dotenv(ROOT / ".env")

import corpus_reader  # noqa: E402
import instruction_filter  # noqa: E402
import server  # noqa: E402
from server import build_system_prompt, build_persona_audience  # noqa: F401,E402

# ═══════════════════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════════════════

GEMMA_MODEL = "gemma-3-27b-it"
GPT_MODEL = "gpt-4.1-mini"

TEMPERATURE = 0.7
MAX_OUTPUT_TOKENS = 8192
MAX_RETRIES = 3

COST_LIMIT_USD = 0.50  # limit dur GPT
RANDOM_SEED = 20260419  # seed per reproduibilitat de l'ordre

OUT_JSONL = ROOT / "tests" / "rigor_v2_v3_dades.jsonl"
LOG_PATH = ROOT / "tests" / "_rigor_generacio.log"

# ═══════════════════════════════════════════════════════════════════════════
# PERFILS (del pre-registre, copia exacte)
# ═══════════════════════════════════════════════════════════════════════════

PROFILES = [
    {
        "id": "P1",
        "perfil": {
            "nom": "Ibrahima Ndiaye",
            "caracteristiques": {
                "nouvingut": {"actiu": True, "l1": "wolof", "mesos_catalunya": 6}
            },
        },
        "context": {"etapa": "ESO", "curs": "2n"},
        "params_base": {
            "mecr_sortida": "A2",
            "dua": "Accés",
            "genere_discursiu": "explicació",
            "complements": {},
        },
    },
    {
        "id": "P2",
        "perfil": {
            "nom": "Júlia Roig",
            "caracteristiques": {"tea": {"actiu": True}},
        },
        "context": {"etapa": "ESO", "curs": "3r"},
        "params_base": {
            "mecr_sortida": "B1",
            "dua": "Core",
            "genere_discursiu": "explicació",
            "complements": {},
        },
    },
    {
        "id": "P3",
        "perfil": {
            "nom": "Èric Vives",
            "caracteristiques": {"tdl": {"actiu": True}},
        },
        "context": {"etapa": "primària", "curs": "5è"},
        "params_base": {
            "mecr_sortida": "B1",
            "dua": "Core",
            "genere_discursiu": "explicació",
            "complements": {},
        },
    },
    {
        "id": "P4",
        "perfil": {
            "nom": "Clara Font",
            "caracteristiques": {"altes_capacitats": {"actiu": True}},
        },
        "context": {"etapa": "primària", "curs": "5è"},
        "params_base": {
            "mecr_sortida": "B2",
            "dua": "Enriquiment",
            "genere_discursiu": "explicació",
            "complements": {},
        },
    },
    {
        "id": "P5",
        "perfil": {
            "nom": "Nil Torras",
            "caracteristiques": {
                "tdah": {"actiu": True, "grau": "moderat"},
                "altes_capacitats": {"actiu": True},
            },
        },
        "context": {"etapa": "ESO", "curs": "4t"},
        "params_base": {
            "mecr_sortida": "B2",
            "dua": "Enriquiment",
            "genere_discursiu": "explicació",
            "complements": {},
        },
    },
]

# ═══════════════════════════════════════════════════════════════════════════
# TEXTOS (del pre-registre, copia exacte)
# ═══════════════════════════════════════════════════════════════════════════

T1 = """El teorema de Pitàgores és un dels resultats més coneguts de la geometria. Afirma que, en qualsevol triangle rectangle, el quadrat de la longitud de la hipotenusa és igual a la suma dels quadrats de les longituds dels dos catets. Matemàticament, si la hipotenusa mesura c i els catets a i b, es compleix la igualtat a² + b² = c². Aquest resultat permet calcular distàncies i longituds en múltiples situacions pràctiques. Els arquitectes l'utilitzen per verificar que les parets són perpendiculars al terra; els topògrafs, per mesurar distàncies inaccessibles directament; i els navegants, per calcular rutes òptimes entre dos punts. El teorema també té profundes implicacions teòriques: va ser una de les primeres demostracions matemàtiques rigoroses de la història i obrí la porta al descobriment dels nombres irracionals, com l'arrel quadrada de dos. La demostració més clàssica es basa en comparar àrees de quadrats construïts sobre els costats del triangle; n'existeixen més de tres-centes demostracions diferents, cadascuna oferint una perspectiva particular sobre la veritat que expressa aquesta relació fonamental entre els costats d'un triangle rectangle."""

T2 = """Els Pirineus són una serralada que s'estén uns 430 quilòmetres entre el mar Cantàbric i el Mediterrani, separant la península Ibèrica de la resta d'Europa. La seva formació s'explica per la teoria de la tectònica de plaques. Fa uns 80 milions d'anys, la placa ibèrica, que llavors era una microplaca independent, es va desplaçar cap al nord i va xocar amb la placa euroasiàtica. La pressió generada durant milions d'anys va plegar i aixecar els sediments marins dipositats entre ambdues plaques, formant la cadena muntanyosa actual. Aquest procés, anomenat orogènesi, encara continua avui de manera gairebé imperceptible, amb moviments verticals de pocs mil·límetres per any. Les roques més antigues dels Pirineus es van formar durant l'era Paleozoica, fa més de 250 milions d'anys, i afloren sobretot a la zona axial, la part més elevada. Les glaciacions del Quaternari van modelar el relleu actual, creant valls en forma d'U, circs glacials i llacs d'alta muntanya. Avui, els Pirineus són un laboratori natural per als geòlegs i una reserva ecològica de gran importància."""

T3 = """La matèria està formada per àtoms, partícules extraordinàriament petites que constitueixen la unitat bàsica dels elements químics. Cada àtom té un nucli central, compost per protons amb càrrega positiva i neutrons sense càrrega, envoltat per electrons amb càrrega negativa que orbiten en diferents nivells d'energia. Quan els àtoms interactuen entre si, poden formar molècules mitjançant enllaços químics. Existeixen dos tipus principals d'enllaç: l'enllaç iònic i l'enllaç covalent. L'enllaç iònic es produeix quan un àtom cedeix un o més electrons a un altre àtom, generant ions de càrrega oposada que s'atrauen electrostàticament. Un exemple clàssic és el clorur de sodi, la sal comuna, on el sodi cedeix un electró al clor. L'enllaç covalent, en canvi, es forma quan dos àtoms comparteixen parells d'electrons per assolir una configuració electrònica estable. La molècula d'aigua, H₂O, és un exemple d'enllaç covalent: cada àtom d'hidrogen comparteix un electró amb l'àtom d'oxigen. La naturalesa de l'enllaç determina moltes propietats físiques i químiques de les substàncies, com el punt de fusió, la solubilitat o la conductivitat elèctrica."""

T4 = """El sistema immunitari és la xarxa de cèl·lules, teixits i òrgans que protegeix l'organisme contra els patògens, agents externs com bacteris, virus i paràsits que poden causar malalties. Aquesta protecció s'estructura en dues línies de defensa complementàries. La immunitat innata és la primera barrera: actua de manera ràpida i inespecífica contra qualsevol intrús. Inclou la pell i les mucoses, que funcionen com a muralles físiques, i cèl·lules com els macròfags i els neutròfils, que engloben i destrueixen els patògens mitjançant un procés anomenat fagocitosi. Quan aquesta primera línia no és suficient, s'activa la immunitat adaptativa, una resposta més lenta però molt més específica. Els limfòcits B produeixen anticossos, proteïnes que reconeixen i neutralitzen antígens específics, mentre que els limfòcits T ataquen directament les cèl·lules infectades. Una característica fonamental de la immunitat adaptativa és la memòria: després d'una primera exposició a un patogen, l'organisme conserva cèl·lules memòria que permeten una resposta molt més ràpida i eficient en futurs contactes. Aquest principi és la base de les vacunes, que ensenyen el sistema immunitari a reconèixer patògens sense provocar la malaltia."""

T5 = """L'Odissea és un dels dos grans poemes èpics atribuïts a Homer, poeta grec del segle VIII aC. Consta de vint-i-quatre cants i narra el retorn d'Odisseu (Ulisses en llatí), rei d'Ítaca, cap a casa seva després de la guerra de Troia. El viatge, que havia de durar pocs mesos, s'allarga durant deu anys a causa de la ira del déu Posidó, ofès perquè Odisseu ha cegat el seu fill Polifem, el ciclop. Durant aquest trajecte, l'heroi i els seus companys s'enfronten a múltiples perills mítics: el cant seductor de les sirenes, el monstre Escil·la i el remolí Caribdis, l'illa de la fetillera Circe, que transforma els homes en porcs, i una visita al regne dels morts per consultar el vident Tirèsias. Mentrestant, a Ítaca, la seva esposa Penèlope espera pacientment, mentre nombrosos pretendents la volen forçar a casar-se amb algun d'ells, convençuts que Odisseu ha mort. L'Odissea no només és una història d'aventures extraordinàries, sinó també una reflexió profunda sobre la identitat, la fidelitat, l'astúcia i el desig humà de tornar a casa, temes universals que continuen vigents vint-i-set segles després."""

T6 = """Un tramvia fora de control avança per una via on hi ha cinc persones lligades que moriran inevitablement si no s'actua. Tu pots estirar una palanca i desviar el tramvia a una altra via on només hi ha una persona lligada. La qüestió és: és ètic prémer la palanca? Aquest experiment mental, conegut com el dilema del tramvia, enfronta dues grans tradicions de la filosofia moral. L'enfocament utilitarista, defensat per filòsofs com Jeremy Bentham i John Stuart Mill, sosté que una acció és moralment correcta si produeix el màxim benefici per al major nombre de persones. Des d'aquesta perspectiva, desviar el tramvia és la decisió moralment òptima: salvem cinc vides a canvi d'una. L'enfocament deontològic, en canvi, associat al pensament d'Immanuel Kant, argumenta que certes accions són intrínsecament incorrectes, independentment de les seves conseqüències. Provocar activament la mort d'una persona innocent —encara que sigui per salvar-ne cinc— constitueix una instrumentalització inacceptable d'un ésser humà. El dilema del tramvia no té una resposta fàcil, però il·lumina la tensió fonamental entre dues maneres radicalment diferents d'entendre la moralitat: la que jutja pels resultats i la que jutja pels principis."""

TEXTS = [
    {"id": "T1", "materia": "Matemàtiques", "materia_key": "cientific", "text": T1},
    {"id": "T2", "materia": "Geografia física", "materia_key": "cientific", "text": T2},
    {"id": "T3", "materia": "Química", "materia_key": "cientific", "text": T3},
    {"id": "T4", "materia": "Biologia humana", "materia_key": "cientific", "text": T4},
    {"id": "T5", "materia": "Literatura clàssica", "materia_key": "linguistic", "text": T5},
    {"id": "T6", "materia": "Filosofia / ètica", "materia_key": "humanistic", "text": T6},
]

MODELS = [
    {"id": "gemma", "nom": "Gemma 3 27B", "model_id": GEMMA_MODEL},
    {"id": "gpt", "nom": "GPT-4.1-mini", "model_id": GPT_MODEL},
]

VARIANTS = ["V2", "V3"]
REPLICAS = [1, 2, 3]


# ═══════════════════════════════════════════════════════════════════════════
# CONSTRUCTORS DE PROMPTS
# ═══════════════════════════════════════════════════════════════════════════

def build_prompt_v2(profile: dict, context: dict, params: dict) -> str:
    """V2 = identitat + instruccions filtrades (MECR) + gènere (SENSE DUA, SENSE persona)."""
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
    return "\n\n".join(parts).strip()


def build_prompt_v3(profile: dict, context: dict, params: dict) -> str:
    """V3 = baseline complet (build_system_prompt)."""
    return build_system_prompt(profile, context, params, "")


def build_prompt(variant: str, profile: dict, context: dict, params: dict) -> str:
    if variant == "V2":
        return build_prompt_v2(profile, context, params)
    if variant == "V3":
        return build_prompt_v3(profile, context, params)
    raise ValueError(f"Variant desconeguda: {variant}")


# ═══════════════════════════════════════════════════════════════════════════
# CRIDES ALS MODELS (amb retry / backoff)
# ═══════════════════════════════════════════════════════════════════════════

def call_gemma(system_prompt: str, text: str, max_retries: int = MAX_RETRIES) -> dict:
    """Gemma 3 27B via google-genai amb rotació de claus i backoff exponencial."""
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
                        temperature=TEMPERATURE,
                        max_output_tokens=MAX_OUTPUT_TOKENS,
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
                errors.append(f"try{attempt+1}/key{idx+1}: {msg}")
                if "429" in msg or "quota" in msg.lower() or "exhausted" in msg.lower():
                    # backoff exponencial només si quota
                    time.sleep(min(2 ** attempt, 16))
                continue
        # després de recórrer totes les claus, petit descans abans del pròxim attempt
        if attempt < max_retries - 1:
            time.sleep(min(2 ** attempt, 16))

    latency = time.time() - t0
    return {
        "ok": False, "response": "", "latency_s": latency,
        "error": "; ".join(errors[-6:]),
        "tokens_in": None, "tokens_out": None,
    }


def call_gpt(system_prompt: str, text: str, max_retries: int = MAX_RETRIES) -> dict:
    """GPT-4.1-mini via openai SDK amb backoff exponencial."""
    from openai import OpenAI
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return {
            "ok": False, "response": "", "latency_s": 0.0,
            "error": "OPENAI_API_KEY no configurada",
            "tokens_in": None, "tokens_out": None,
        }

    errors = []
    t0 = time.time()
    client = OpenAI(api_key=key)
    for attempt in range(max_retries):
        try:
            resp = client.chat.completions.create(
                model=GPT_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"TEXT ORIGINAL A ADAPTAR:\n\n{text}"},
                ],
                max_tokens=MAX_OUTPUT_TOKENS,
                temperature=TEMPERATURE,
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
            msg = str(e)[:250]
            errors.append(f"try{attempt+1}: {msg}")
            if "429" in msg or "rate" in msg.lower() or "quota" in msg.lower():
                time.sleep(min(2 ** attempt, 16))
            elif attempt < max_retries - 1:
                time.sleep(min(2 ** attempt, 8))

    latency = time.time() - t0
    return {
        "ok": False, "response": "", "latency_s": latency,
        "error": "; ".join(errors[-3:]),
        "tokens_in": None, "tokens_out": None,
    }


def call_model(model_id: str, system_prompt: str, text: str) -> dict:
    if model_id == "gemma":
        return call_gemma(system_prompt, text)
    if model_id == "gpt":
        return call_gpt(system_prompt, text)
    raise ValueError(f"Model desconegut: {model_id}")


# ═══════════════════════════════════════════════════════════════════════════
# UTILS
# ═══════════════════════════════════════════════════════════════════════════

def word_count(s: str) -> int:
    return len([w for w in s.split() if w.strip()])


def estimate_cost_gpt(tokens_in, tokens_out) -> float:
    """gpt-4.1-mini: $0.40/M input, $1.60/M output (abril 2026)."""
    if tokens_in is None or tokens_out is None:
        return 0.0
    return (tokens_in / 1_000_000) * 0.40 + (tokens_out / 1_000_000) * 1.60


def log(msg: str, log_fp) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    log_fp.write(line + "\n")
    log_fp.flush()


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    # Construir la llista completa de cel·les
    cells = []
    cell_idx = 0
    for profile in PROFILES:
        for text in TEXTS:
            for variant in VARIANTS:
                for model in MODELS:
                    for replica in REPLICAS:
                        cell_idx += 1
                        cells.append({
                            "idx": cell_idx,
                            "perfil_id": profile["id"],
                            "perfil_nom": profile["perfil"]["nom"],
                            "profile_obj": profile,
                            "text_id": text["id"],
                            "text_materia": text["materia"],
                            "text_obj": text,
                            "variant": variant,
                            "model_id": model["id"],
                            "model_nom": model["nom"],
                            "replica": replica,
                        })
    n_total = len(cells)

    # Aleatoritzar l'ordre d'execucio per minimitzar efectes temporals
    rng = random.Random(RANDOM_SEED)
    exec_order = list(range(n_total))
    rng.shuffle(exec_order)

    # Prepare output files
    OUT_JSONL.parent.mkdir(parents=True, exist_ok=True)
    # truncar els fitxers anteriors (re-run net)
    out_fp = open(OUT_JSONL, "w", encoding="utf-8")
    log_fp = open(LOG_PATH, "w", encoding="utf-8")

    log("=" * 70, log_fp)
    log("Fase A — generacio rigorosa V2 vs V3 (360 casos)", log_fp)
    log("=" * 70, log_fp)
    log(f"Total cel·les: {n_total}", log_fp)
    log(f"Perfils: {[p['id'] for p in PROFILES]}", log_fp)
    log(f"Textos: {[t['id'] for t in TEXTS]}", log_fp)
    log(f"Variants: {VARIANTS}", log_fp)
    log(f"Models: {[m['nom'] for m in MODELS]}", log_fp)
    log(f"Repliques per cel·la: {len(REPLICAS)}", log_fp)
    log(f"Temperatura: {TEMPERATURE}", log_fp)
    log(f"Seed ordre d'execucio: {RANDOM_SEED}", log_fp)
    log(f"Sortida JSONL: {OUT_JSONL}", log_fp)
    log(f"Limit cost GPT: ${COST_LIMIT_USD}", log_fp)

    # Pre-compute prompts (10 perfils x 2 variants = 10 combinacions) — la materia NO entra a V2/V3 directament
    # pero build_system_prompt ho pot utilitzar via complements. Els complements estan buits, aixi que ho ignorem.
    # Perfil x variant prompts (reutilitzats). Els recomputem amb materia injectada per si build_system_prompt ho usa.

    start_global = time.time()
    n_done = 0
    n_ok = 0
    n_failed = 0
    running_gpt_cost = 0.0
    aborted_cost = False

    for pos, idx_cell in enumerate(exec_order, start=1):
        cell = cells[idx_cell]
        cell_id = f"cell_{cell['idx']:04d}"

        profile = cell["profile_obj"]["perfil"]
        context = cell["profile_obj"]["context"]
        # Parametres: combinar base + materia injectada
        params = dict(cell["profile_obj"]["params_base"])
        params["materia"] = cell["text_obj"]["materia_key"]
        params["etapa"] = context["etapa"]
        params["mecr"] = params["mecr_sortida"]

        # Construir prompt (pot fallar si hi ha bug, ho capturem)
        prompt_error = None
        try:
            system_prompt = build_prompt(cell["variant"], profile, context, params)
        except Exception as e:
            system_prompt = ""
            prompt_error = f"build_prompt: {e}\n{traceback.format_exc()[:500]}"

        tag = (f"[{pos}/{n_total}] {cell_id} perfil={cell['perfil_id']} text={cell['text_id']} "
               f"variant={cell['variant']} model={cell['model_id']} rep={cell['replica']}")

        # Cost guard
        if cell["model_id"] == "gpt" and running_gpt_cost >= COST_LIMIT_USD:
            if not aborted_cost:
                log(f"ATURAT GPT: cost acumulat ${running_gpt_cost:.4f} >= limit ${COST_LIMIT_USD}", log_fp)
                aborted_cost = True
            record = {
                "id": cell_id,
                "perfil_id": cell["perfil_id"],
                "perfil_nom": cell["perfil_nom"],
                "text_id": cell["text_id"],
                "text_matèria": cell["text_materia"],
                "variant": cell["variant"],
                "model": cell["model_id"] == "gemma" and GEMMA_MODEL or GPT_MODEL,
                "replica": cell["replica"],
                "prompt_system": system_prompt,
                "text_original": cell["text_obj"]["text"],
                "text_adaptat": "",
                "paraules_sortida": 0,
                "latencia_s": 0.0,
                "tokens_in": None,
                "tokens_out": None,
                "temperatura": TEMPERATURE,
                "timestamp": datetime.now().isoformat(),
                "ok": False,
                "error": f"cost limit GPT ${COST_LIMIT_USD} assolit",
            }
            out_fp.write(json.dumps(record, ensure_ascii=False) + "\n")
            out_fp.flush()
            n_done += 1
            n_failed += 1
            log(f"{tag} -> SKIP (cost limit)", log_fp)
            continue

        if prompt_error:
            log(f"{tag} -> BUILD_ERROR: {prompt_error[:200]}", log_fp)
            record = {
                "id": cell_id,
                "perfil_id": cell["perfil_id"],
                "perfil_nom": cell["perfil_nom"],
                "text_id": cell["text_id"],
                "text_matèria": cell["text_materia"],
                "variant": cell["variant"],
                "model": GEMMA_MODEL if cell["model_id"] == "gemma" else GPT_MODEL,
                "replica": cell["replica"],
                "prompt_system": "",
                "text_original": cell["text_obj"]["text"],
                "text_adaptat": "",
                "paraules_sortida": 0,
                "latencia_s": 0.0,
                "tokens_in": None,
                "tokens_out": None,
                "temperatura": TEMPERATURE,
                "timestamp": datetime.now().isoformat(),
                "ok": False,
                "error": prompt_error[:500],
            }
            out_fp.write(json.dumps(record, ensure_ascii=False) + "\n")
            out_fp.flush()
            n_done += 1
            n_failed += 1
            continue

        # Cridar el model
        try:
            r = call_model(cell["model_id"], system_prompt, cell["text_obj"]["text"])
        except Exception as e:
            r = {
                "ok": False, "response": "", "latency_s": 0.0,
                "error": f"Excepcio Python: {e}",
                "tokens_in": None, "tokens_out": None,
            }

        # Cost acumulat GPT
        if cell["model_id"] == "gpt" and r.get("ok"):
            running_gpt_cost += estimate_cost_gpt(r.get("tokens_in"), r.get("tokens_out"))

        record = {
            "id": cell_id,
            "perfil_id": cell["perfil_id"],
            "perfil_nom": cell["perfil_nom"],
            "text_id": cell["text_id"],
            "text_matèria": cell["text_materia"],
            "variant": cell["variant"],
            "model": GEMMA_MODEL if cell["model_id"] == "gemma" else GPT_MODEL,
            "replica": cell["replica"],
            "prompt_system": system_prompt,
            "text_original": cell["text_obj"]["text"],
            "text_adaptat": r.get("response", ""),
            "paraules_sortida": word_count(r.get("response", "")),
            "latencia_s": round(r.get("latency_s", 0.0), 2),
            "tokens_in": r.get("tokens_in"),
            "tokens_out": r.get("tokens_out"),
            "temperatura": TEMPERATURE,
            "timestamp": datetime.now().isoformat(),
            "ok": bool(r.get("ok")),
            "error": None if r.get("ok") else (r.get("error") or "")[:800],
        }
        out_fp.write(json.dumps(record, ensure_ascii=False) + "\n")
        out_fp.flush()

        n_done += 1
        if r.get("ok"):
            n_ok += 1
            status = "OK"
        else:
            n_failed += 1
            status = "FAIL"

        elapsed = time.time() - start_global
        rate = n_done / elapsed if elapsed > 0 else 0.0
        eta_s = (n_total - n_done) / rate if rate > 0 else 0.0
        log(
            f"{tag} -> {status} "
            f"{record['paraules_sortida']}w "
            f"{record['latencia_s']:.1f}s "
            f"tok_in={record['tokens_in']} tok_out={record['tokens_out']} | "
            f"acum {n_ok}ok/{n_failed}fail, gpt$={running_gpt_cost:.4f}, eta={eta_s/60:.1f}min",
            log_fp,
        )
        if not r.get("ok"):
            log(f"    error: {(r.get('error') or '')[:300]}", log_fp)

    out_fp.close()

    total_elapsed = time.time() - start_global
    ok_ratio = n_ok / n_done if n_done > 0 else 0.0

    log("=" * 70, log_fp)
    log(f"FINAL — durada total: {total_elapsed/60:.1f} min", log_fp)
    log(f"OK: {n_ok}/{n_done} ({ok_ratio*100:.1f}%)", log_fp)
    log(f"FAILED: {n_failed}/{n_done}", log_fp)
    log(f"Cost GPT-4.1-mini estimat: ${running_gpt_cost:.4f}", log_fp)
    log(f"Sortida: {OUT_JSONL}", log_fp)

    if ok_ratio < 0.95:
        log(f"AVIS: taxa d'exit {ok_ratio*100:.1f}% < 95% — revisa errors abans de Fase B", log_fp)
    if aborted_cost:
        log(f"AVIS: es va aturar cost GPT al limit ${COST_LIMIT_USD}", log_fp)

    log_fp.close()


if __name__ == "__main__":
    main()
