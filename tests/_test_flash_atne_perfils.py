"""Test comparatiu amb 2 perfils i textos contrastats per validar generalització.

Perfil 1: Alumne NOUVINGUT (L1 àrab, 6 mesos a Catalunya) + 1r ESO + MECR A2 + DUA Accés
  Text: història (Revolució Industrial) — humanitats, abstracte
  Complements: glossari, traduccio_l1, mapa_conceptual, bastides

Perfil 2: ALTES CAPACITATS + 4t ESO + MECR C1 + DUA Enriquiment
  Text: filosofia (mite de la caverna, Plató) — molt abstracte, requereix pensament crític
  Complements: activitats_aprofundiment, mapa_conceptual, preguntes_comprensio
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
# CAS 1: NOUVINGUT L1 àrab
# ────────────────────────────────────────────────────────────────────────────
PROFILE_NOUVINGUT = {
    "nom": "Yasmin (nouvinguda L1 àrab)",
    "profile_type": "alumne",
    "caracteristiques": {
        "nouvingut": {
            "actiu": True,
            "L1": "àrab",
            "pais": "Marroc",
            "mesos_catalunya": 6,
        },
    },
    "observacions": "Alumna molt motivada. Alfabetitzada en àrab i amb noció bàsica de francès. Comprensió oral incipient en català.",
}

CONTEXT_NOUVINGUT = {
    "etapa": "ESO",
    "curs": "1r ESO",
    "materia": "Geografia i Història",
    "mecr": "A2",
    "alfabet_llati": True,
}

PARAMS_NOUVINGUT = {
    "mecr_sortida": "A2",
    "mecr_base": "B2",
    "dua": "Accés",
    "etapa": "ESO",
    "lang": "ca",
    "materia": "Geografia i Història",
    "genere": "expositiu",
    "complements": {
        "glossari": True,
        "traduccio_l1": True,
        "mapa_conceptual": True,
        "bastides": True,
    },
}

TEXT_HISTORIA = """La Revolució Industrial fou un procés de profundes transformacions econòmiques,
socials i tecnològiques que s'inicià a Gran Bretanya a mitjans del segle XVIII i s'estengué
progressivament per Europa occidental, els Estats Units i el Japó al llarg del segle XIX.
Aquest procés se sustentà en la mecanització de la producció, especialment al sector tèxtil,
gràcies a invents com la spinning jenny de Hargreaves i la màquina de vapor perfeccionada
per James Watt el 1769. La transició del taller artesanal a la fàbrica comportà l'aparició
d'una nova classe social, el proletariat industrial, sotmesa a condicions laborals extenuants:
jornades de 14-16 hores, treball infantil, salaris ínfims i absència de drets. Paral·lelament,
la burgesia capitalista, propietària dels mitjans de producció, acumulà riqueses sense
precedents. L'urbanització accelerada i el creixement demogràfic generaren ciutats fabrils
saturades, amb greus problemes de salubritat, mortalitat infantil elevada i conflictivitat
social, que cristal·litzaren en el sorgiment del moviment obrer, les primeres organitzacions
sindicals i el pensament socialista de Marx i Engels."""

# ────────────────────────────────────────────────────────────────────────────
# CAS 2: ALTES CAPACITATS
# ────────────────────────────────────────────────────────────────────────────
PROFILE_AACC = {
    "nom": "Pau (altes capacitats)",
    "profile_type": "alumne",
    "caracteristiques": {
        "altes_capacitats": {
            "actiu": True,
            "perfil_aacc": "talent acadèmic verbal",
            "interessos": "filosofia, lògica matemàtica, història de les idees",
        },
    },
    "observacions": "Alumne amb gran capacitat d'abstracció. S'avorreix amb continguts rutinaris. Necessita reptes i connexions interdisciplinars.",
}

CONTEXT_AACC = {
    "etapa": "ESO",
    "curs": "4t ESO",
    "materia": "Cultura clàssica i filosofia",
    "mecr": "C1",
    "alfabet_llati": True,
}

PARAMS_AACC = {
    "mecr_sortida": "C1",
    "mecr_base": "B2",
    "dua": "Enriquiment",
    "etapa": "ESO",
    "lang": "ca",
    "materia": "Cultura clàssica i filosofia",
    "genere": "argumentatiu",
    "complements": {
        "activitats_aprofundiment": True,
        "mapa_conceptual": True,
        "preguntes_comprensio": True,
    },
}

TEXT_FILOSOFIA = """Al llibre VII de la República, Plató presenta el conegut mite de la caverna,
una al·legoria sobre l'estat ordinari de coneixement humà i el camí ascendent cap a la veritat.
Imagina uns presoners encadenats des de la infància en una caverna, obligats a mirar només
una paret on es projecten ombres d'objectes que altres homes transporten darrere seu, davant
d'un foc. Per als presoners, aquestes ombres constitueixen tota la realitat: no han vist mai
res més. Si un dels presoners fos alliberat i forçat a girar-se cap a la llum, primer quedaria
enlluernat i incapacitat de veure els objectes que projectaven les ombres; després, conduït
fora de la caverna, contemplaria amb gran dolor la llum del sol, fins arribar a comprendre
que aquesta és la font última de tot allò visible. Si retornés a la caverna per il·luminar
els seus antics companys, aquests, no només no el creurien, sinó que possiblement el matarien.
L'al·legoria condensa l'epistemologia platònica: el coneixement sensible (ombres) és il·lusori,
el coneixement vertader requereix una conversió de l'ànima (paideia) cap a les Idees,
culminant amb la Idea del Bé, anàloga al sol. Aquesta ascensió no és solament gnoseològica
sinó també ètico-política: el filòsof que ha vist la veritat té el deure de tornar i
governar la polis, malgrat el risc i la incomprensió dels altres."""


MODELS = [
    ("gemma-4-31b-it", "Gemma 4 31B"),
    ("gemini-2.5-flash", "Gemini 2.5 Flash"),
    ("gemini-2.5-flash-lite", "Gemini 2.5 Flash-Lite"),
]


CASES = [
    {
        "case_id": "nouvingut_arab_historia",
        "label": "CAS 1: Nouvinguda L1 àrab + Història (A2 / DUA Accés)",
        "profile": PROFILE_NOUVINGUT,
        "context": CONTEXT_NOUVINGUT,
        "params": PARAMS_NOUVINGUT,
        "text": TEXT_HISTORIA,
    },
    {
        "case_id": "aacc_filosofia",
        "label": "CAS 2: Altes capacitats + Filosofia (C1 / DUA Enriquiment)",
        "profile": PROFILE_AACC,
        "context": CONTEXT_AACC,
        "params": PARAMS_AACC,
        "text": TEXT_FILOSOFIA,
    },
]


def main():
    all_results = []
    for case in CASES:
        print(f"\n\n{'#'*80}\n# {case['label']}\n{'#'*80}", flush=True)
        system_prompt = build_system_prompt(case["profile"], case["context"], case["params"], rag_context="")
        print(f"System prompt: {len(system_prompt)} chars / ~{len(system_prompt)//4} tokens", flush=True)

        # Guarda prompt per inspeccio
        with open(f"tests/_atne_prompt_{case['case_id']}.txt", "w", encoding="utf-8") as f:
            f.write(system_prompt)

        case_results = {"case_id": case["case_id"], "label": case["label"], "outputs": []}
        for model_id, model_label in MODELS:
            print(f"\n--- {model_label} ({model_id}) ---", flush=True)
            t0 = time.time()
            try:
                output = _call_llm(model_id, system_prompt, case["text"])
                elapsed = time.time() - t0
                print(f"OK | {elapsed:.1f}s | {len(output)} chars", flush=True)
                case_results["outputs"].append({
                    "model_id": model_id, "label": model_label,
                    "elapsed_s": elapsed, "output_len": len(output), "output": output,
                })
            except Exception as e:
                elapsed = time.time() - t0
                print(f"ERROR {elapsed:.1f}s: {str(e)[:200]}", flush=True)
                case_results["outputs"].append({
                    "model_id": model_id, "label": model_label,
                    "elapsed_s": elapsed, "error": str(e),
                })
        all_results.append(case_results)

    with open("tests/_atne_perfils_report.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print(f"\n\n{'='*80}\nRESUM:\n{'='*80}")
    for case in all_results:
        print(f"\n{case['label']}:")
        for o in case["outputs"]:
            if "error" in o:
                print(f"  {o['label']:<30} | ERROR {o['elapsed_s']:.1f}s")
            else:
                print(f"  {o['label']:<30} | {o['elapsed_s']:5.1f}s | {o['output_len']:>5} chars")


if __name__ == "__main__":
    main()
