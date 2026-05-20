"""Test 3 nivells MECR contrastats: pre-A1, A2 (TEA), B1 (sord LSC).
Compara 4 models: Gemma 4 31B, Gemma 4 26B MoE, Gemini 2.5 Flash, Flash-Lite.
"""
import json
import time
import sys
import os
from pathlib import Path

env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())

sys.path.insert(0, str(Path(__file__).parent.parent))
from adaptation.prompt_builder import build_system_prompt
from adaptation.llm_clients import _call_llm

# ────────────────────────────────────────────────────────────────────────────
# CAS 4: PRIMÀRIA / pre-A1 — alumne 4t Primària sense condicions específiques
# ────────────────────────────────────────────────────────────────────────────
PROFILE_PRIMARIA = {
    "nom": "Alumne genèric 4t Primària",
    "profile_type": "alumne",
    "caracteristiques": {},  # sense condicions actives
    "observacions": "Alumne sense necessitats educatives específiques. Lectura en desenvolupament normal.",
}
CONTEXT_PRIMARIA = {
    "etapa": "Primària",
    "curs": "4t Primària",
    "materia": "Ciències de la Naturalesa",
    "mecr": "pre-A1",
    "alfabet_llati": True,
}
PARAMS_PRIMARIA = {
    "mecr_sortida": "pre-A1",
    "mecr_base": "A2",
    "dua": "Accés",
    "etapa": "Primària",
    "lang": "ca",
    "materia": "Ciències de la Naturalesa",
    "genere": "expositiu",
    "complements": {
        "glossari": True,
        "esquema_visual": True,
        "preguntes_comprensio": True,
    },
}
TEXT_CICLE_AIGUA = """L'aigua del nostre planeta es troba en un moviment constant que els
científics anomenen cicle hidrològic. L'energia solar escalfa l'aigua dels mars, rius i llacs,
fent que s'evapori i pugi a l'atmosfera en forma de vapor d'aigua. A mesura que aquest vapor
ascendeix, troba temperatures més fredes i es condensa formant petites gotes que s'agrupen
en núvols. Quan aquestes gotes es fan prou grosses o pesades, cauen a la superfície terrestre
en forma de precipitació, ja sigui pluja, neu o calamarsa, segons la temperatura. L'aigua
que cau pot acumular-se als oceans, infiltrar-se al subsòl formant aqüífers, o circular per
rius cap al mar, completant així el cicle."""

# ────────────────────────────────────────────────────────────────────────────
# CAS 5: A2 + TEA (Trastorn de l'Espectre Autista) — 1r ESO
# ────────────────────────────────────────────────────────────────────────────
PROFILE_TEA = {
    "nom": "Joan (TEA nivell 1)",
    "profile_type": "alumne",
    "caracteristiques": {
        "tea": {
            "actiu": True,
            "nivell": "1",  # autisme amb suport
        },
    },
    "observacions": "Alumne amb TEA nivell 1. Bon raonament lògic. Dificultats amb llenguatge figurat, ironia i ambigüitats. Necessita estructura clara i explicitació.",
}
CONTEXT_TEA = {
    "etapa": "ESO",
    "curs": "1r ESO",
    "materia": "Ciències Socials",
    "mecr": "A2",
    "alfabet_llati": True,
}
PARAMS_TEA = {
    "mecr_sortida": "A2",
    "mecr_base": "B1",
    "dua": "Core",
    "etapa": "ESO",
    "lang": "ca",
    "materia": "Ciències Socials",
    "genere": "expositiu",
    "complements": {
        "glossari": True,
        "esquema_visual": True,
        "preguntes_comprensio": True,
    },
}
TEXT_FEUDALISME = """El feudalisme va ser el sistema polític, econòmic i social que va dominar
Europa occidental durant l'edat mitjana, especialment entre els segles IX i XV. Es basava en
una relació de dependència entre el senyor feudal, propietari de la terra, i els seus vassalls,
que li devien obediència i serveis a canvi de protecció. La societat feudal s'organitzava de
manera molt jerarquitzada: a dalt hi havia el rei, després els nobles i el clergat (que tenien
els privilegis), i a baix els pagesos, que constituïen la majoria de la població i havien de
treballar les terres del senyor a canvi de poder cultivar una petita parcel·la per a ells.
Les ciutats medievals, on residien artesans i comerciants, anaren guanyant importància a partir
del segle XII gràcies al renaixement del comerç i a l'aparició d'una nova classe social: la
burgesia."""

# ────────────────────────────────────────────────────────────────────────────
# CAS 6: B1 + Discapacitat auditiva LSC — 3r ESO
# ────────────────────────────────────────────────────────────────────────────
PROFILE_SORD = {
    "nom": "Aina (sorda profunda, L1 LSC)",
    "profile_type": "alumne",
    "caracteristiques": {
        "disc_auditiva": {
            "actiu": True,
            "tipus": "profunda",
            "L1": "LSC (llengua de signes catalana)",
        },
    },
    "observacions": "Alumna sorda profunda des de naixement. L1 = LSC. El català escrit és L2. Necessita simplificació sintàctica reforçada i suport visual integral.",
}
CONTEXT_SORD = {
    "etapa": "ESO",
    "curs": "3r ESO",
    "materia": "Llengua catalana i literatura",
    "mecr": "B1",
    "alfabet_llati": True,
}
PARAMS_SORD = {
    "mecr_sortida": "B1",
    "mecr_base": "B2",
    "dua": "Core",
    "etapa": "ESO",
    "lang": "ca",
    "materia": "Llengua catalana i literatura",
    "genere": "narratiu",
    "complements": {
        "glossari": True,
        "pictogrames": True,
        "esquema_visual": True,
        "preguntes_comprensio": True,
    },
}
TEXT_LITERATURA = """El protagonista, després d'haver vagat durant hores per aquells carrerons
estrets i bruts, va arribar finalment a la plaça major, on l'esperava una sorpresa que mai
no hauria pogut imaginar. Enmig de la multitud que es congregava al voltant del mercat, hi
havia una figura familiar que feia anys que no veia: era la seva germana, presumptament morta
durant la guerra. Sense poder-se contenir, va córrer cap a ella amb el cor bategant fort,
mentre les llàgrimes li brollaven dels ulls. La germana, en girar-se i veure'l, va deixar
caure el cistell que portava i es va llançar als seus braços. Mai abans no havien sentit
una emoció tan intensa, una barreja de joia, dolor i incredulitat que els deixava sense
paraules. La gent del mercat els mirava sense entendre res, però ells dos sabien que aquell
moment marcaria les seves vides per sempre."""


MODELS = [
    ("gemma-4-31b-it", "Gemma 4 31B"),
    ("gemma-4-26b-a4b-it", "Gemma 4 26B MoE"),
    ("gemini-2.5-flash", "Gemini 2.5 Flash"),
    ("gemini-2.5-flash-lite", "Gemini 2.5 Flash-Lite"),
]

CASES = [
    {
        "case_id": "primaria_pre_a1",
        "label": "CAS 4: Primària 4t / pre-A1 / cicle aigua",
        "profile": PROFILE_PRIMARIA,
        "context": CONTEXT_PRIMARIA,
        "params": PARAMS_PRIMARIA,
        "text": TEXT_CICLE_AIGUA,
    },
    {
        "case_id": "eso_a2_tea",
        "label": "CAS 5: 1r ESO / A2 / TEA / feudalisme",
        "profile": PROFILE_TEA,
        "context": CONTEXT_TEA,
        "params": PARAMS_TEA,
        "text": TEXT_FEUDALISME,
    },
    {
        "case_id": "eso_b1_sord",
        "label": "CAS 6: 3r ESO / B1 / disc. auditiva LSC / narratiu",
        "profile": PROFILE_SORD,
        "context": CONTEXT_SORD,
        "params": PARAMS_SORD,
        "text": TEXT_LITERATURA,
    },
]


def main():
    all_results = []
    for case in CASES:
        print(f"\n\n{'#'*80}\n# {case['label']}\n{'#'*80}", flush=True)
        sp = build_system_prompt(case["profile"], case["context"], case["params"], "")
        print(f"System prompt: {len(sp)} chars / ~{len(sp)//4} tokens", flush=True)
        with open(f"tests/_atne_prompt_{case['case_id']}.txt", "w", encoding="utf-8") as f:
            f.write(sp)
        case_res = {"case_id": case["case_id"], "label": case["label"], "outputs": []}
        for model_id, model_label in MODELS:
            print(f"\n--- {model_label} ---", flush=True)
            t0 = time.time()
            try:
                out = _call_llm(model_id, sp, case["text"])
                el = time.time() - t0
                print(f"OK | {el:.1f}s | {len(out)} chars", flush=True)
                case_res["outputs"].append({
                    "model_id": model_id, "label": model_label,
                    "elapsed_s": el, "output_len": len(out), "output": out,
                })
            except Exception as e:
                el = time.time() - t0
                print(f"ERROR {el:.1f}s: {str(e)[:200]}", flush=True)
                case_res["outputs"].append({
                    "model_id": model_id, "label": model_label,
                    "elapsed_s": el, "error": str(e),
                })
        all_results.append(case_res)

    with open("tests/_atne_3casos_report.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print(f"\n\n{'='*80}\nRESUM:\n{'='*80}")
    for case in all_results:
        print(f"\n{case['label']}:")
        for o in case["outputs"]:
            if "error" in o:
                print(f"  {o['label']:<32} | ERROR {o['elapsed_s']:.1f}s")
            else:
                print(f"  {o['label']:<32} | {o['elapsed_s']:5.1f}s | {o['output_len']:>6} chars")


if __name__ == "__main__":
    main()
