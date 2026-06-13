# ADR-002 — Selecció de model per a l'Adaptador (juny 2026)

- **Estat:** Acceptat i **FIRMAT** (jutge creuat J2 completat) · 🔁 re-test trimestral programat
- **Data:** 2026-06-12 · jutge creuat J2 completat i ADR firmat **2026-06-13**
- **Decisió de:** Miquel Amor · sobre l'experiment comparatiu `tests/experiment_models_2026.py`
- **Relacionat:** `tests/results/experiment_combinat_20260613_113558.{md,json}` (J2 creuat COMPLET) ·
  `tests/results/experiment_combinat_20260612_150946.{md,json}` (parcial, J2 incomplet) ·
  `tests/rejudge.py` (re-judge homogeni) · [[project_models_gpt4o_decision_20260527]] ·
  `spec/synthetic-monitoring.md` (Fase 4)

## Context

Re-execució de la decisió de model amb candidats actualitzats (juny 2026), seguint el
protocol d'avaluació ATNE (rúbriques C1-C5 + F1 longitud per MECR) amb **jutge creuat**
(anti-self-judging): 6 casos sintètics que cobreixen els perfils delicats (nouvingut pre-A1,
DI, TEA, dislèxia, 2e, AACC), generats amb el `build_system_prompt` REAL del repo.

**Candidats:** gemini-3.5-flash · gemini-2.5-flash · gpt-5 · gpt-4o (baseline producció).
**Jutges:** J1 = gpt-4.1-mini · **J2 = gemini-2.5-flash** (creuat). Cost total ≈ €1.0 (< cap 2€).

> ⚠️ Caveat metodològic (RESOLT 2026-06-13): el free tier de Gemini limita a 20 req/dia per
> model. La passada del 12/06 va quedar incompleta (7/21 judicis). L'intent de refer-la amb
> **gemini-2.0-flash va resultar `limit: 0`** a TOTES les 6 claus — el 2.0-flash no té
> assignació de free tier (NO és quota diària resetejable), així que mai va produir cap judici.
> El 13/06 el J2 es va completar amb un únic jutge homogeni **gemini-2.5-flash**, re-jutjant els
> **21 resultats sencers** (sense barrejar models de jutge, per fer la columna comparable),
> mitjançant **rotació de 6 claus** per superar el límit de 20 req/dia. Veure `tests/rejudge.py`.
>
> ⚠️ Auto-jutge: gemini-2.5-flash és alhora candidat i jutge J2 → els seus casos queden
> auto-jutjats sota J2 (inflats) i **NO s'usen** per a la decisió; el seu creuat fiable és J1.

## Resultats (puntuació CREUADA NET = jutge de l'altre proveïdor, la menys esbiaixada)

Jutge creuat J2 COMPLET (gemini-2.5-flash, 21/21) combinat amb J1 (gpt-4.1-mini):

| Candidat | Creuat NET | Via | Latència med. | Cost/gen |
|---|---|---|---|---|
| gpt-4o | **4.90** | J2 (Gemini) | ~15s | €0.03 |
| gemini-2.5-flash | **4.84** | J1 (GPT) | ~32s | €0 (free) |
| gpt-5 | **4.77** | J2 (Gemini) | ~98s ⚠ | €0.15 ⚠ |
| gemini-3.5-flash | **4.55** | J1 (GPT) | ~42s | €0 (free) |

**Candidats EMPATATS dins la variància del jutge.** El rang (0.35) és **inferior al soroll** del
jutge LLM: el mateix gemini-2.5-flash va donar gpt-4o NOUV_preA1 fons **3.2 (12/06) vs 4.4
(13/06)**. → El benchmark **no destria** entre els viables; **la decisió la pren compliance, NO
el benchmark**.

**Correcció d'un artefacte de l'esborrany del 12/06.** L'informe previ marcava com a bandera
vermella "gpt-4o cau al català (C5=3) a NOUV_preA1". Aquell 3 era el judici **J1 = gpt-4.1-mini,
MATEIX proveïdor que gpt-4o → self-judging**. El **creuat NET (jutge Gemini) ho desmenteix:
gpt-4o C5 = 5** al cas extrem. gpt-4o NO fluixeja al català; el seu creuat global és, de fet, el
més alt (empatat amb gemini-2.5 dins el soroll).

**gpt-5 — descart REFORÇAT.** Creuat NET 4.77 (el més baix dels viables) i, sobretot, **C5 català
pre-A1 = 2** sota el jutge creuat (s'esfondra al català a l'extrem, coherent amb la
sobre-elaboració del reasoning), a més de ~98s/gen i €0.15. Cap avantatge de qualitat que
compensi la latència/cost.

## Decisió

1. **Prototip personal → es manté `gemini-2.5-flash`.** Motiu: **free tier + compliance
   (residència UE / Vertex)**, NO superioritat de qualitat. En qualitat està **empatat amb
   gpt-4o** dins la variància del jutge (4.84 vs 4.90, rang < soroll). Com que el benchmark no
   destria, decideixen el cost i la residència de dades.
2. **`gpt-5` DESCARTAT** per a l'adaptador: latència (~98s) i cost de raonament (€0.15/gen)
   desproporcionats, i **sense cap avantatge de qualitat** — creuat NET 4.77 (el més baix dels
   viables) i C5 català pre-A1 = 2. Reasoning model = eina equivocada per a aquesta tasca.
3. **`gpt-4o` NO queda desqualificat per qualitat.** El seu creuat NET és el més alt (4.90,
   empatat amb gemini-2.5 dins el soroll) i el seu català a l'extrem és sòlid (C5 NOUV = 5 sota
   el jutge creuat); la "caiguda al català" de l'esborrany era un **artefacte de self-judging** de
   gpt-4.1-mini, desmentit pel creuat net. És una **opció vàlida**: el motiu per preferir Gemini
   al prototip és **compliance + free tier**, no qualitat. **Si l'stack institucional queda lligat
   a OpenAI**, gpt-4o és defensable; igualment es pot fer un **mini-run de `gpt-4.1-mini` i
   `gpt-5-mini`** per optimitzar cost/latència.
4. **Re-test TRIMESTRAL** via synthetic monitoring (Fase 4): els models evolucionen ràpid;
   aquesta decisió té data de caducitat.

## Conseqüències / notes

- Config **VIGENT a producció** (`system_config`): adapter = gpt-4o (híbrid). Aquest ADR NO
  el canvia automàticament; documenta que **per al prototip personal el criteri de cost +
  compliance afavoreix gemini-2.5-flash** (en qualitat empata amb gpt-4o), i que la decisió
  institucional OpenAI queda pendent del mini-run + compliance. Canviar el model de producció
  és un `scripts/set_models_*.py` + `system_config`, traçable.
- Si es valida Vertex (residència UE), Gemini és l'opció preferent **per compliance** (la
  qualitat creuada està empatada amb gpt-4o; el desempat el dona la residència de dades + free tier).
- L'anàlisi per cas (C5 català + perfils extrems com NOUV_preA1) pesa més que la mitjana —
  veure el JSON i la secció corresponent de l'informe combinat.
