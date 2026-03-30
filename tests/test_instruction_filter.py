"""
Test del filtratge d'instruccions — verifica que el catàleg de 72 instruccions
es filtra correctament segons perfil, sub-variables, MECR i DUA.
"""
import sys
sys.path.insert(0, ".")

from instruction_filter import get_instructions, format_instructions_for_prompt


def print_stats(label, result):
    s = result["stats"]
    print(f"\n{'='*70}")
    print(f"CAS: {label}")
    print(f"{'='*70}")
    print(f"  Perfils actius: {s['perfils_actius']}")
    print(f"  MECR: {s['mecr']}  |  DUA: {s['dua']}")
    print(f"  ─────────────────────────────────")
    print(f"  SEMPRE (fixes):        {s['sempre']}")
    print(f"  NIVELL (MECR):         {s['nivell']}")
    print(f"  PERFIL (base):         {s['perfil']}")
    print(f"  PERFIL (condicional):  {s['perfil_condicional']}")
    print(f"  COMPLEMENT:            {s['complement']}")
    print(f"  SUPRIMIDES:            {s['suprimides']}")
    print(f"  ─────────────────────────────────")
    print(f"  TOTAL ENVIADES:        {s['total_enviades']}")

    if result["perfil_condicional"]:
        print(f"\n  📌 Instruccions CONDICIONALS activades:")
        for instr in result["perfil_condicional"]:
            print(f"     → {instr}")

    if result["suppressed"]:
        print(f"\n  🚫 Instruccions SUPRIMIDES:")
        for instr in result["suppressed"]:
            print(f"     → {instr}")


# ── CAS 1: Nouvingut àrab, alfabet no llatí, escolarització parcial, A1 ──
cas1 = get_instructions(
    profile={
        "caracteristiques": {
            "nouvingut": {
                "actiu": True,
                "L1": "àrab",
                "alfabet_llati": "no",
                "escolaritzacio_previa": "no",
                "mesos_a_catalunya": "3",
            }
        }
    },
    params={
        "mecr_sortida": "A1",
        "dua": "Acces",
        "complements": {"glossari": True, "pictogrames": True},
    },
)
print_stats("Nouvingut àrab, alfabet no llatí, A1, DUA Accés", cas1)

# ── CAS 2: Nouvingut castellà, alfabet llatí, escolaritzat, B1 ──
cas2 = get_instructions(
    profile={
        "caracteristiques": {
            "nouvingut": {
                "actiu": True,
                "L1": "castellà",
                "alfabet_llati": "si",
                "escolaritzacio_previa": "si",
                "mesos_a_catalunya": "8",
            }
        }
    },
    params={
        "mecr_sortida": "B1",
        "dua": "Core",
        "complements": {"glossari": True},
    },
)
print_stats("Nouvingut castellà, alfabet llatí, B1, DUA Core", cas2)

# ── CAS 3: Altes capacitats, B2, Enriquiment ──
cas3 = get_instructions(
    profile={
        "caracteristiques": {
            "altes_capacitats": {"actiu": True}
        }
    },
    params={
        "mecr_sortida": "B2",
        "dua": "Enriquiment",
        "complements": {"activitats_aprofundiment": True},
    },
)
print_stats("Altes capacitats, B2, DUA Enriquiment", cas3)

# ── CAS 4: TEA + TDAH (multi-perfil), A2, Core ──
cas4 = get_instructions(
    profile={
        "caracteristiques": {
            "tea": {"actiu": True, "nivell_suport": 2},
            "tdah": {"actiu": True, "presentacio": "combinat"},
        }
    },
    params={
        "mecr_sortida": "A2",
        "dua": "Core",
        "complements": {"esquema_visual": True},
    },
)
print_stats("TEA + TDAH, A2, DUA Core", cas4)

# ── CAS 5: Nouvingut xinès + dislèxia, pre-A1, Accés ──
cas5 = get_instructions(
    profile={
        "caracteristiques": {
            "nouvingut": {
                "actiu": True,
                "L1": "xinès",
                "alfabet_llati": "no",
                "escolaritzacio_previa": "no",
                "mesos_a_catalunya": "1",
            },
            "dislexia": {"actiu": True},
        }
    },
    params={
        "mecr_sortida": "pre-A1",
        "dua": "Acces",
        "complements": {"glossari": True, "pictogrames": True},
    },
)
print_stats("Nouvingut xinès + dislèxia, pre-A1, DUA Accés", cas5)

# ── COMPARACIÓ: Cas 1 vs Cas 2 (ambdós nouvinguts, diferent config) ──
print(f"\n{'='*70}")
print("COMPARACIÓ: Nouvingut àrab (cas1) vs Nouvingut castellà (cas2)")
print(f"{'='*70}")
# Instruccions que cas1 té i cas2 no
only_cas1 = set(cas1["perfil_condicional"]) - set(cas2["perfil_condicional"])
only_cas2 = set(cas2["perfil_condicional"]) - set(cas1["perfil_condicional"])
print(f"\n  Només àrab (cas1): {len(only_cas1)}")
for i in only_cas1:
    print(f"     + {i}")
print(f"\n  Només castellà (cas2): {len(only_cas2)}")
for i in only_cas2:
    print(f"     + {i}")
print(f"\n  MECR cas1={cas1['stats']['nivell']} instruccions vs cas2={cas2['stats']['nivell']} instruccions")

# ── Mostrar prompt formatat per cas 1 ──
print(f"\n{'='*70}")
print("PROMPT FORMATAT (cas 1 — nouvingut àrab):")
print(f"{'='*70}")
prompt_text = format_instructions_for_prompt(cas1)
print(prompt_text[:2000])
print(f"\n... [{len(prompt_text)} caràcters totals]")
