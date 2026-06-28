"""Smoke test LLM real per a A2 CASCADA — "el JSON canon mana".

Valida el CANVI DE COMPORTAMENT que va introduir la cascada (commit ae80831):
els descriptors del rubrica.json canon manen sobre el text hardcoded d'ATNE.
On hi ha més risc de sorpresa amb un LLM real:

  1. PICTOGRAMES als nivells alts (B1-C1+): el canon baixa molt la densitat
     (de 4-5 fix → B1:2-4, B2:1-3, C1+:0-2). Volem confirmar que el prompt
     transmet la densitat baixa i que el LLM NO sobredimensiona.
  2. IL·LUSTRACIONS als nivells alts (B1-C1+): canon B1:1-2, C1+:0-1
     (abans 3-4 fix). Mateix risc.
  3. ACTIVITATS a pre-A1/A1: el canon hi vol 1-2 manipulatives "sense
     abstracció"; ATNE abans deia "debat / pensament crític" (antipedagògic
     a aquests nivells). Volem confirmar que la sortida és manipulativa i
     NO conté el to "debat / crític / argumentar".

Estratègia de checks (un LLM no posa MAI un nombre exacte → no comptem clavat):
  - FAIL dur només quan la sortida CONTRADIU el canon de forma clara
    (sobredimensió flagrant de pictos/imatges a C1+, "debat" a pre-A1).
  - WARNING (no fail) per desviacions toleràbles del nombre exacte.
  - Sempre imprimim el comptatge real i un fragment del prompt rebut perquè
    Miquel pugui jutjar qualitativament.

Si la sortida empitjora respecte el comportament pre-cascada, els reforços
literals estan a docs/reforcos_generes_arxiu_20260601.md per reaplicar.

Ús: python tests/smoke_a2_cascada_llm.py
Cost: ~$0.04-0.08 amb gpt-4.1-mini (4 crides curtes).
"""
from __future__ import annotations

import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
except Exception:
    pass

from adaptation.prompt_builder import build_complements_prompt, build_system_prompt
from adaptation.llm_clients import _call_llm

# ---- Textos d'ENTRADA (originals) per a la Call 1 / adapter ----
# Pictogrames i il·lustracions són complements INLINE: l'adapter (build_system_prompt,
# Call 1) genera el "## Text adaptat" amb els marcadors [PICTO:]/[IMATGE:] dins.
# Per tant l'usuari rep el text ORIGINAL, no l'adaptat.

# Text de nivell alt (B1-C1): contingut curricular dens, conceptes abstractes.
REVOLUCIO_ORIGINAL = """La Revolució Industrial, iniciada a la Gran Bretanya a finals del segle XVIII
i estesa per Europa durant el segle XIX, va comportar una transformació radical
dels sistemes productius. La mecanització de la indústria tèxtil i la introducció
de la màquina de vapor van substituir progressivament el treball artesanal per la
producció fabril en sèrie. Aquest procés va provocar un intens èxode rural cap als
nuclis urbans industrials, on milers de treballadors —incloent dones i infants—
suportaven jornades extenuants, salaris ínfims i condicions insalubres que acabarien
generant els primers moviments obrers organitzats."""

# Text molt bàsic (pre-A1 / A1): instructiu concret i manipulatiu. Les activitats
# d'aprofundiment es generen a la Call 1 (adapter, build_system_prompt) dins el
# bloc específic governat pel descriptor del canon → text d'entrada = ORIGINAL.
PLANTA_ORIGINAL = """Per germinar una llavor de mongetera necessitarem un test amb
substrat lleuger, aigua i un lloc assolellat. En primer lloc, omplirem el test amb
terra fins a uns dos centímetres de la vora. Tot seguit, hi practicarem un petit
solc on dipositarem la llavor, que cobrirem amb una fina capa de substrat. Finalment,
regarem amb moderació procurant mantenir la humitat constant però sense entollar.
Al cap d'uns dies observarem com emergeix la primera tija."""


CASES = [
    # --- Pictogrames + il·lustracions a nivell ALT (el canvi de densitat) ---
    {
        "id": "picto_illu_B1",
        "call": "adapter",
        "focus": ["pictogrames", "illustracions"],
        "profile": {"caracteristiques": {}},
        "context": {"curs": "3r ESO", "etapa": "secundaria", "materia": "Historia"},
        "params": {
            "mecr_sortida": "B1",
            "dua": "Core",
            "genere_discursiu": "divulgatiu",
            "lang": "ca",
            "complements": {"pictogrames": True, "illustracions": True},
        },
        "user_text": REVOLUCIO_ORIGINAL,
        "max_pictos": 5,   # canon B1=2-4 → tolerància fins 5; >5 = sobredimensió
        "max_imatges": 3,  # canon B1=1-2 → tolerància fins 3; >3 = sobredimensió
    },
    {
        "id": "picto_illu_C1",
        "call": "adapter",
        "focus": ["pictogrames", "illustracions"],
        "profile": {"caracteristiques": {}},
        "context": {"curs": "1r Batxillerat", "etapa": "batxillerat", "materia": "Historia"},
        "params": {
            "mecr_sortida": "C1",
            "dua": "Enriquiment",
            "genere_discursiu": "divulgatiu",
            "lang": "ca",
            "complements": {"pictogrames": True, "illustracions": True},
        },
        "user_text": REVOLUCIO_ORIGINAL,
        "max_pictos": 3,   # canon C1=0-2 → tolerància fins 3
        "max_imatges": 2,  # canon C1=0-1 → tolerància fins 2
    },
    # --- Activitats a nivell BAIX (manipulatiu, no debat) ---
    {
        "id": "activitats_preA1",
        "call": "adapter",
        "focus": ["activitats_aprofundiment"],
        "profile": {"caracteristiques": {"nouvingut": {"actiu": True, "L1": "arab"}}},
        "context": {"curs": "1r Primaria", "etapa": "primaria"},
        "params": {
            "mecr_sortida": "pre-A1",
            "dua": "Acces",
            "genere_discursiu": "instruccions",
            "lang": "ca",
            "complements": {"activitats_aprofundiment": True},
        },
        "user_text": PLANTA_ORIGINAL,
        "forbidden_terms": ["debat", "argument", "crític", "critic", "interdisciplinar"],
    },
    {
        "id": "activitats_A1",
        "call": "adapter",
        "focus": ["activitats_aprofundiment"],
        "profile": {"caracteristiques": {}},
        "context": {"curs": "2n Primaria", "etapa": "primaria"},
        "params": {
            "mecr_sortida": "A1",
            "dua": "Core",
            "genere_discursiu": "instruccions",
            "lang": "ca",
            "complements": {"activitats_aprofundiment": True},
        },
        "user_text": PLANTA_ORIGINAL,
        "forbidden_terms": ["debat", "argument", "crític", "critic", "interdisciplinar"],
    },
]


def assert_check(name: str, ok: bool, detail: str = "", warn: bool = False) -> int:
    if ok:
        mark = "✅"
    elif warn:
        mark = "⚠️ "
    else:
        mark = "❌"
    print(f"   {mark} {name}{(' — ' + detail) if detail else ''}")
    return 0 if (ok or warn) else 1


def smoke_case(case: dict) -> int:
    call = case.get("call", "complements")
    print(f"\n{'='*64}\nCas: {case['id']}  (call: {call} · focus: {', '.join(case['focus'])})\n{'='*64}")
    if call == "adapter":
        # Call 1: l'adapter genera "## Text adaptat" amb marcadors [PICTO:]/[IMATGE:] inline.
        system = build_system_prompt(case["profile"], case["context"], case["params"])
    else:
        system = build_complements_prompt(case["profile"], case["context"], case["params"])
    if not system:
        print("⚠️  Prompt buit — saltant")
        return 0
    user = case["user_text"]
    print(f"[system prompt] {len(system)} chars · [user] {len(user)} chars")

    # Mostra el fragment del prompt rellevant (densitat canon transmesa)
    for kw in ("Gradació per a", "Densitat per a", "ACTIVAT — Per a"):
        m = re.search(re.escape(kw) + r".{0,160}", system, re.S)
        if m:
            frag = re.sub(r"\s+", " ", m.group(0)).strip()
            print(f"[prompt·canon] …{frag[:170]}…")

    print("→ Cridant gpt-4.1-mini...")
    out = _call_llm("gpt-4.1-mini", system, user)
    print(f"← {len(out)} chars rebuts\n")
    print("--- OUTPUT ---")
    print(out)
    print("--- END ---\n")

    fails = 0
    print("CHECKS:")

    if "pictogrames" in case["focus"]:
        pictos = re.findall(r"\[PICTO:", out)
        n = len(pictos)
        mx = case["max_pictos"]
        fails += assert_check(
            f"Pictogrames dins límit canon (≤{mx})", n <= mx,
            detail=f"{n} marcadors [PICTO:] (canon {case['params']['mecr_sortida']} densitat baixa)",
            warn=(n <= mx + 2),  # 1-2 de més = warning, no fail dur
        )

    if "illustracions" in case["focus"]:
        imatges = re.findall(r"\[IMATGE:", out)
        n = len(imatges)
        mx = case["max_imatges"]
        fails += assert_check(
            f"Il·lustracions dins límit canon (≤{mx})", n <= mx,
            detail=f"{n} marcadors [IMATGE:] (canon {case['params']['mecr_sortida']} densitat baixa)",
            warn=(n <= mx + 1),
        )

    if "activitats_aprofundiment" in case["focus"]:
        has_h2 = "Activitats" in out  # H2 pot venir del canon
        fails += assert_check("Secció d'activitats present", has_h2)
        # ⚠️ Acotem la cerca de termes prohibits NOMÉS a la secció d'activitats.
        # La sortida de l'adapter també porta "## Argumentació pedagògica" (capa
        # docent), on apareix legítimament "argumentació" → cercar a tot l'output
        # és un fals positiu. El canon governa el to de LES ACTIVITATS, no del
        # metacomentari pedagògic adreçat al professor.
        if "## Activitats" in out:
            act_section = out.split("## Activitats", 1)[1]
            # Talla a la següent secció ## (argumentació, notes, etc.)
            act_section = re.split(r"\n##\s", act_section, 1)[0]
        else:
            act_section = out  # sense H2 canònic: avalua tot (pitjor cas)
        low = act_section.lower()
        forbidden = [t for t in case["forbidden_terms"] if t in low]
        fails += assert_check(
            "Activitats sense to abstracte/debat (canon = manipulatiu a nivell baix)",
            not forbidden,
            detail=(f"trobats a la secció d'activitats: {forbidden}"
                    if forbidden else "cap terme prohibit a les activitats"),
        )
        # Senyal positiu (informatiu): verbs manipulatius del canon pre-A1.
        manip = [v for v in ["ordenar", "tocar", "moure", "dibuixar", "dramatitzar",
                             "enganxa", "retalla", "pinta", "ordena", "llista"] if v in low]
        print(f"   ℹ️  verbs manipulatius a les activitats: {manip or 'cap (revisar qualitat manualment)'}")

    return fails


def main() -> int:
    total_fails = 0
    for c in CASES:
        total_fails += smoke_case(c)
    print(f"\n{'='*64}")
    print(f"RESULTAT: {'✅ PASS' if total_fails == 0 else f'❌ {total_fails} fail(s)'}")
    print("Nota: WARNINGs (⚠️) no compten com a fail — densitat ±1-2 és tolerable")
    print("amb un LLM real. Revisa els OUTPUT per a judici qualitatiu (Miquel).")
    print(f"{'='*64}")
    return total_fails


if __name__ == "__main__":
    sys.exit(main())
