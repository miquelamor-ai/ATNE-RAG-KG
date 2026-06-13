# Experiment models — informe combinat (jutge creuat) · 20260613_113558

Jutge 1 (J1): **gpt-4.1-mini** · Jutge 2 (J2): **gemini-2.5-flash** · Casos: 6

## Taula creuada per candidat

| Candidat | Fons J1 | Fons J2 | Δ | C5 català (J1/J2) | **Creuat NET** | n (J1/J2) |
|---|---|---|---|---|---|---|
| gemini-3.5-flash | 4.55 | 4.75 | 0.2 | 4.75/5 | **4.55** | 4/4 |
| gemini-2.5-flash ⚠* | 4.84 | 4.88 | 0.04 | 4.8/4.8 | **4.84** | 5/5 |
| gpt-5 | 4.97 | 4.77 | 0.2 | 4.83/4.17 | **4.77** | 6/6 |
| gpt-4o | 4.7 | 4.9 | 0.2 | 4.67/5 | **4.9** | 6/6 |

**Creuat NET** = puntuació del jutge de l'ALTRE proveïdor (la menys esbiaixada):
- Candidats Gemini → J1 (gpt-4.1-mini, OpenAI).
- Candidats GPT → J2 (gemini-2.5-flash, Gemini).

⚠* **gemini-2.5-flash és alhora candidat i jutge J2**: els seus casos queden AUTO-JUTJATS sota J2 (jutge = generador) → la seva columna J2 està inflada i **NO s'usa** per a la decisió. El seu creuat fiable és J1 = 4.84.

## Fons per cas (J1 / J2)

| Cas | gemini-3.5-flash | gemini-2.5-flash | gpt-5 | gpt-4o |
|---|---|---|---|---|
| NOUV_preA1 | 3.6 / 4 | 4.6 / 5 | 4.8 / 4.2 | 4 / 4.4 |
| DI_moderat | 4.8 / 5 | 5 / 4.8 | 5 / 4.8 | 4.8 / 5 |
| TEA_n2 | 5 / 5 | 4.8 / 4.8 | 5 / 5 | 4.8 / 5 |
| DISLEXIA | (gen. fallida) | 4.8 / 5 | 5 / 4.8 | 4.8 / 5 |
| 2E_aacc_dislexia | (gen. fallida) | (gen. fallida) | 5 / 4.8 | 4.8 / 5 |
| AACC | 4.8 / 5 | 5 / 4.8 | 5 / 5 | 5 / 5 |

## C5 català per cas (J1 / J2) — on el català fluixeja a l'extrem

| Cas | gemini-3.5-flash | gemini-2.5-flash | gpt-5 | gpt-4o |
|---|---|---|---|---|
| NOUV_preA1 | 4 / 5 | 4 / 5 | 4 / 2 | 3 / 5 |
| DI_moderat | 5 / 5 | 5 / 5 | 5 / 5 | 5 / 5 |
| TEA_n2 | 5 / 5 | 5 / 4 | 5 / 5 | 5 / 5 |
| DISLEXIA | (gen. fallida) | 5 / 5 | 5 / 4 | 5 / 5 |
| 2E_aacc_dislexia | (gen. fallida) | (gen. fallida) | 5 / 4 | 5 / 5 |
| AACC | 5 / 5 | 5 / 5 | 5 / 5 | 5 / 5 |
