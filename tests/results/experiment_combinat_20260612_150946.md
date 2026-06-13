# Experiment models — informe combinat (jutge creuat) · 20260612_150946

Jutge 1: **gpt-4.1-mini** · Jutge 2: **gemini-2.0-flash** · Casos: 6

| Candidat | Fons J1 | Fons J2 | Δ (concordança) | C5 català (J1/J2) | F1 dins rang | Latència med. (ms) | Tokens out med. | Self-judge |
|---|---|---|---|---|---|---|---|---|
| gemini-3.5-flash | 4.55 | None | None | 4.75/None | 3/4 | 41846 | 1688 | J2 |
| gemini-2.5-flash | 4.84 | None | None | 4.8/None | 3/5 | 32212 | 2387 | J2 |
| gpt-5 | 4.97 | None | None | 4.83/None | 3/6 | 97964 | 8304 | J1 |
| gpt-4o | 4.7 | None | None | 4.67/None | 3/6 | 14589 | 1064 | J1 |

## Com llegir-ho
- **Fons J1/J2** = mitjana C1-C5 (1-5) de cada jutge. **Δ** = concordança (com més petit, més acord).
- **Self-judge**: J1 (gpt-4.1-mini) infla candidats OpenAI; J2 (gemini) infla candidats Gemini.
  → per a un candidat, la puntuació CREUADA (jutge de l'altre proveïdor) és la menys esbiaixada.
- **C5** = qualitat del català. **F1** = casos amb longitud de frase dins el rang MECR.
- Si la diferència entre candidats és petita, **mana compliance (residència UE / Vertex)**, no el benchmark.

## Veredicte per candidat (puntuació CREUADA, menys esbiaixada)
- **gemini-3.5-flash**: creuat ≈ 4.55 · J1=4.55 J2=None (Δ None) · n=4
- **gemini-2.5-flash**: creuat ≈ 4.84 · J1=4.84 J2=None (Δ None) · n=5
- **gpt-5**: creuat ≈ None · J1=4.97 J2=None (Δ None) · n=6
- **gpt-4o**: creuat ≈ None · J1=4.7 J2=None (Δ None) · n=6