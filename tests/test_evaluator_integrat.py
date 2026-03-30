"""
Test integrat de l'avaluador — 1 cas complet amb les 3 capes.

Simula el flux complet:
  1. Construeix system prompts per les dues branques (Hardcoded vs RAG)
  2. BLOC 1 (CODI): Recall de les instruccions enviades
  3. BLOC 2 (CODI): Metriques de forma sobre textos adaptats (simulats)
  4. BLOC 3 (LLM):  Agent avaluador compara ambdues branques

Execucio: PYTHONIOENCODING=utf-8 python tests/test_evaluator_integrat.py
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, ".")

from instruction_filter import get_instructions, format_instructions_for_prompt
from evaluator_metrics import evaluate_blocs_1_2, extract_instruction_ids, retrieval_recall
from evaluator_agent import build_eval_prompt, evaluate_case, get_hardcoded_profile_block

# ═══════════════════════════════════════════════════════════════════════════════
# CAS DE TEST: Nouvingut arab, alfabet no llati, A1, DUA Acces
# ═══════════════════════════════════════════════════════════════════════════════

CAS_ID = "PRI_EXPL__P1_test"

TEXT_ORIGINAL = """Les plantes no s'alimenten d'altres éssers vius, sinó que es fabriquen el seu propi aliment a través d'un procés anomenat fotosíntesi. Per dur a terme aquest procés, les plantes necessiten quatre elements: llum solar, aigua, diòxid de carboni i sals minerals.

El procés funciona de la manera següent. Primer, les arrels de la planta absorbeixen aigua i sals minerals de la terra. Aquesta barreja, que s'anomena saba bruta, es transporta des de les arrels fins a les fulles a través de la tija. Un cop a les fulles, la planta absorbeix el diòxid de carboni de l'aire.

A les fulles es troba un pigment de color verd anomenat clorofil·la. La clorofil·la atrapa l'energia lluminosa del sol i la transforma en energia química. Gràcies a aquesta energia, l'aigua de la saba bruta i el diòxid de carboni es converteixen en aliment per a la planta, que s'anomena saba elaborada. Durant aquest procés, la planta produeix oxigen i l'expulsa a l'aire a través de les fulles."""

PROFILE = {
    "caracteristiques": {
        "nouvingut": {
            "actiu": True,
            "L1": "àrab",
            "alfabet_llati": "no",
            "escolaritzacio_previa": "no",
            "mesos_a_catalunya": "3",
        }
    }
}

PARAMS = {
    "mecr_sortida": "A1",
    "dua": "Acces",
    "complements": {"glossari": True, "pictogrames": True},
}

PERFILS_ACTIUS = ["nouvingut"]
ETAPA = "primaria"
GENERE = "explicacio"

# ═══════════════════════════════════════════════════════════════════════════════
# TEXTOS ADAPTATS SIMULATS (en un batch real, vindrien del generador)
# ═══════════════════════════════════════════════════════════════════════════════

TEXT_HARDCODED = """## Paraules clau
- **Fotosíntesi** 🌱: les plantes fan menjar amb llum
- **Saba bruta** 💧: aigua que puja per la planta
- **Clorofil·la** 🟢: el color verd de les fulles

## Text adaptat

Les plantes fan el seu menjar. 🌱
Això es diu **fotosíntesi** (quan les plantes fan menjar amb la llum).

Les plantes necessiten quatre coses:
- Llum del sol ☀️
- Aigua 💧
- Aire
- Minerals de la terra

Les arrels agafen l'aigua. 💧
L'aigua puja per la tija.
L'aigua arriba a les fulles.

Les fulles són verdes. 🟢
El verd es diu **clorofil·la**.
La clorofil·la atrapa la llum.

## Argumentació pedagògica
1. **Adaptació lingüística**: frases de 4-7 paraules, vocabulari quotidià.
2. **Atenció a la diversitat**: suport visual amb emojis.

## Notes d'auditoria
| Aspecte | Original | Adaptat | Motiu |
|---|---|---|---|
| Vocabulari | "organismes fotosintètics" | "plantes" | Simplificació A1 |
"""

TEXT_RAG = """## Paraules clau
| Terme | Traducció (àrab) | Explicació simple |
|---|---|---|
| **Fotosíntesi** | تمثيل ضوئي | Les plantes fan menjar amb llum ☀️ |
| **Saba bruta** | نسغ خام | Aigua amb minerals que puja per la planta 💧 |
| **Clorofil·la** | كلوروفيل | El color verd de les fulles 🟢 |
| **Diòxid de carboni** | ثاني أكسيد الكربون | Un gas de l'aire |
| **Saba elaborada** | نسغ معالج | El menjar que fa la planta |

## Text adaptat

Les plantes fan el seu menjar. 🌱
Les plantes usen la llum del sol. ☀️
Aquest procés es diu **fotosíntesi** (quan les plantes fan menjar amb la llum).

Les plantes necessiten quatre coses:
- Llum del sol ☀️
- Aigua 💧
- Un gas de l'aire: **diòxid de carboni** (ثاني أكسيد الكربون)
- Minerals de la terra

Primer, les arrels agafen l'aigua de la terra. 💧
Després, l'aigua puja per la tija fins a les fulles.

Les fulles tenen un color verd especial.
El verd es diu **clorofil·la** (كلوروفيل). 🟢
La **clorofil·la** atrapa la llum del sol.

Amb la llum, la planta barreja l'aigua i el gas.
La barreja es converteix en menjar per a la planta.
El menjar es diu **saba elaborada** (نسغ معالج).

A més, la planta fa oxigen. 🌬️
L'oxigen surt per les fulles a l'aire.
L'oxigen és important per respirar.

## Argumentació pedagògica
1. **Adaptació lingüística**: frases de 4-8 paraules, vocabulari quotidià, subjecte explícit.
2. **Atenció a la diversitat**: glossari bilingüe català-àrab, transliteració implícita, suport visual.
3. **Suport multimodal**: emojis per conceptes clau, taula de glossari amb alfabet àrab.
4. **Preservació curricular**: tots els conceptes mantinguts (fotosíntesi, saba bruta/elaborada, clorofil·la, diòxid de carboni, oxigen).

## Notes d'auditoria
| Aspecte | Original | Adaptat | Motiu |
|---|---|---|---|
| Vocabulari | "organismes fotosintètics" | "plantes" | A1: vocabulari quotidià |
| Glossari | No n'hi ha | Bilingüe cat-àrab | Perfil nouvingut L1 àrab |
| Transliteració | No n'hi ha | Termes en àrab al costat | Alfabet no llatí |
"""

# ═══════════════════════════════════════════════════════════════════════════════
# EXECUCIO
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 70)
    print(f"TEST INTEGRAT AVALUADOR — {CAS_ID}")
    print("=" * 70)

    # ── BRANCA RAG: instruccions filtrades ──
    print("\n[1] Filtrant instruccions per branca RAG...")
    filtered_rag = get_instructions(PROFILE, PARAMS)
    prompt_rag_text = format_instructions_for_prompt(filtered_rag)
    stats = filtered_rag["stats"]
    print(f"    Instruccions enviades: {stats['total_enviades']}")
    print(f"    SEMPRE={stats['sempre']} NIVELL={stats['nivell']} "
          f"PERFIL={stats['perfil']} CONDICIONAL={stats['perfil_condicional']} "
          f"SUPRIMIDES={stats['suprimides']}")

    # ── BRANCA HARDCODED: bloc fix ──
    print("\n[2] Obtenint bloc Hardcoded...")
    prompt_hc_text = get_hardcoded_profile_block(PERFILS_ACTIUS)
    print(f"    Bloc hardcoded: {len(prompt_hc_text)} chars")

    # ── BLOC 1-2: Metriques automatiques ──
    print("\n[3] BLOC 1-2: Metriques automatiques...")

    # RAG
    blocs_rag = evaluate_blocs_1_2(TEXT_RAG, PARAMS["mecr_sortida"], PERFILS_ACTIUS, filtered_rag)
    print(f"\n    RAG:")
    print(f"      Retrieval Recall: {blocs_rag['retrieval']['recall']}")
    if blocs_rag['retrieval']['absents']:
        print(f"      Instruccions absents: {blocs_rag['retrieval']['absents']}")
    print(f"      Forma: {blocs_rag['forma']['puntuacio_forma']}")
    for k, v in blocs_rag['forma'].items():
        if k.startswith("F"):
            print(f"        {k}: {v}")

    # Hardcoded (Recall = 1.0 per disseny, forma sobre el text)
    from evaluator_metrics import evaluate_forma
    forma_hc = evaluate_forma(TEXT_HARDCODED, PARAMS["mecr_sortida"])
    print(f"\n    Hardcoded:")
    print(f"      Retrieval Recall: 1.0 (per disseny)")
    print(f"      Forma: {forma_hc['puntuacio_forma']}")
    for k, v in forma_hc.items():
        if k.startswith("F"):
            print(f"        {k}: {v}")

    # ── BLOC 3: LLM-as-a-judge ──
    print("\n[4] BLOC 3: Enviant a l'agent avaluador (Gemini)...")

    user_prompt = build_eval_prompt(
        cas_id=CAS_ID,
        perfils_actius=PERFILS_ACTIUS,
        mecr=PARAMS["mecr_sortida"],
        dua=PARAMS["dua"],
        etapa=ETAPA,
        genere=GENERE,
        text_original=TEXT_ORIGINAL,
        prompt_hardcoded=prompt_hc_text,
        text_hardcoded=TEXT_HARDCODED,
        forma_hardcoded=forma_hc,
        prompt_rag=prompt_rag_text,
        text_rag=TEXT_RAG,
        forma_rag=blocs_rag["forma"],
        recall_rag=blocs_rag["retrieval"]["recall"],
    )

    print(f"    Prompt total: {len(user_prompt)} chars")
    print("    Esperant resposta de Gemini...")

    eval_result = evaluate_case(user_prompt)

    # ── RESULTATS ──
    print("\n" + "=" * 70)
    print("RESULTAT AGENT AVALUADOR")
    print("=" * 70)

    if "error" in eval_result:
        print(f"\n  ERROR: {eval_result['error']}")
        print(f"\n  Resposta crua:\n{eval_result.get('raw_response', '')[:1000]}")
    else:
        print(json.dumps(eval_result, ensure_ascii=False, indent=2))

    # Guardar resultat
    out_path = Path("tests/results") / f"eval_{CAS_ID}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    full_result = {
        "cas_id": CAS_ID,
        "perfil": PROFILE,
        "params": PARAMS,
        "blocs_1_2": {
            "rag": {
                "retrieval": blocs_rag["retrieval"],
                "forma": blocs_rag["forma"],
                "filter_stats": filtered_rag["stats"],
            },
            "hardcoded": {
                "retrieval": {"recall": 1.0},
                "forma": forma_hc,
            },
        },
        "bloc_3": eval_result,
    }

    out_path.write_text(json.dumps(full_result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n  Resultat guardat a: {out_path}")


if __name__ == "__main__":
    main()
