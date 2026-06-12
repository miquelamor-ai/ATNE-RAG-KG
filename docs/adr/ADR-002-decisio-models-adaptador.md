# ADR-002 — Selecció de model per a l'Adaptador (juny 2026)

- **Estat:** Acceptat · 🔁 re-test trimestral programat
- **Data:** 2026-06-12
- **Decisió de:** Miquel Amor · sobre l'experiment comparatiu `tests/experiment_models_2026.py`
- **Relacionat:** `tests/results/experiment_combinat_20260612_150946.{md,json}` ·
  [[project_models_gpt4o_decision_20260527]] · `spec/synthetic-monitoring.md` (Fase 4)

## Context

Re-execució de la decisió de model amb candidats actualitzats (juny 2026), seguint el
protocol d'avaluació ATNE (rúbriques C1-C5 + F1 longitud per MECR) amb **jutge creuat**
(anti-self-judging): 6 casos sintètics que cobreixen els perfils delicats (nouvingut pre-A1,
DI, TEA, dislèxia, 2e, AACC), generats amb el `build_system_prompt` REAL del repo.

**Candidats:** gemini-3.5-flash · gemini-2.5-flash · gpt-5 · gpt-4o (baseline producció).
**Jutges:** J1 = gpt-4.1-mini · J2 = gemini-2.0-flash (creuat). Cost total ≈ €1.0 (< cap 2€).

> ⚠️ Caveat metodològic: el free tier de Gemini limita a 20 req/dia per model; la 1a versió
> del jutge creuat (gemini-2.5-flash) va quedar incompleta i es va refer amb gemini-2.0-flash
> (quota fresca) per tenir un J2 d'un sol jutge, internament comparable.

## Resultats (puntuació CREUADA = jutge de l'altre proveïdor, la menys esbiaixada)

- **gemini-2.5-flash:** la més forta (cross ≈ 4.8/5, jutge GPT). Free tier, ~30s/gen.
- gemini-3.5-flash: cross ≈ 4.5.
- **gpt-5:** cross ≈ 4.5 PERÒ **~98s/generació i ~8.300 tokens de raonament** (€0.15/gen).
  Sobredimensionat i lent per a adaptar text. **Self-judging confirmat:** gpt-4.1-mini
  l'inflava (4.97 auto → 4.53 creuat).
- gpt-4o: ràpid (~15s) però puntuació creuada més baixa.

Diferències PETITES entre candidats → segons el criteri ATNE, **mana compliance
(residència UE / Vertex), no el benchmark**.

## Decisió

1. **Prototip personal → es manté `gemini-2.5-flash`.** Millor puntuació creuada, free tier,
   latència raonable. No hi ha motiu de benchmark per canviar-lo.
2. **`gpt-5` DESCARTAT** per a l'adaptador: latència (~98s) i cost (raonament) desproporcionats
   per a una qualitat equivalent. Reasoning model = eina equivocada per a aquesta tasca.
3. **`gpt-4o` QÜESTIONAT:** ràpid però puntuació creuada inferior. Decisió condicionada:
   **si l'stack institucional queda lligat a OpenAI**, fer un **mini-run de `gpt-4.1-mini` i
   `gpt-5-mini`** (alternatives OpenAI més barates/ràpides) abans de fixar el model OpenAI.
4. **Re-test TRIMESTRAL** via synthetic monitoring (Fase 4): els models evolucionen ràpid;
   aquesta decisió té data de caducitat.

## Conseqüències / notes

- Config **VIGENT a producció** (`system_config`): adapter = gpt-4o (híbrid). Aquest ADR NO
  el canvia automàticament; documenta que **per al prototip personal el criteri tècnic
  afavoreix gemini-2.5-flash**, i que la decisió institucional OpenAI queda pendent del
  mini-run + compliance. Canviar el model de producció és un `scripts/set_models_*.py` +
  `system_config`, traçable.
- Si es valida Vertex (residència UE), Gemini guanya pel doble motiu: qualitat creuada +
  compliance.
- L'anàlisi per cas (C5 català + perfils extrems com NOUV_preA1) pesa més que la mitjana —
  veure el JSON i la secció corresponent de l'informe combinat.
