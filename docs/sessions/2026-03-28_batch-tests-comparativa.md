# Sessió 2026-03-28 nit — Batch tests sintètics i comparativa branques

## Què s'ha fet

### 1. Matriu de tests sintètics
- 16 textos reals en català (fonts: GEC, XTEC, SaviaMENT, Racó de contes, 3Cat, Diari Ara)
- 4 gèneres discursius × 4 etapes educatives (Primària CS, ESO 1-2, ESO 3-4, Batxillerat)
- 10 perfils d'adaptació (7 simples + 3 creuaments)
- Total: 160 combinacions

### 2. Test harness
- `tests/test_data.json` — matriu completa amb textos i perfils
- `tests/batch_test.py` — runner que crida `run_adaptation()` directament
- `tests/compare_branches.py` — comparador CSV entre branques

### 3. Execució i resultats

| Mètrica | RAG | Hardcoded |
|---|---|---|
| Casos OK | 160/160 | 160/160 |
| Paraules/cas | **769** | 248 |
| Negretes/cas | **26.5** | 8.5 |
| Temps/cas | **15.0s** | 27.5s |
| Warnings/cas | 1.6 | **1.2** |

### 4. Observacions
- RAG genera adaptacions ~3x més riques (instruccions del corpus són més detallades)
- RAG és ~2x més ràpid (prompt més clar → menys thinking de Gemini)
- Hardcoded genera textos curts per perfils extrems (DI, nouvingut+dislèxia: 95-107w)
- Negretes RAG 3x superiors = més scaffolding pedagògic
- 0 errors en ambdues branques

### 5. Bugs arreglats
- `corpus_reader.py`: tots els blocs carreguen OK (DUA, fewshot, crossings arreglats sessió anterior)
- `batch_test.py`: fix encoding Windows (cp1252 → utf-8), fix claus DUA (`tipus_dua` → `dua`)
- Compatibilitat cross-branch: normalització mètriques (claus diferents entre branques)

## Decisió presa
**Branca RAG guanya** en riquesa i velocitat. Proper pas: merge ambdues a main amb switch UI (RAG | Hardcoded | Doble) + pestanya comparador visual.

## Fitxers creats/modificats
- `tests/test_data.json` (nou)
- `tests/batch_test.py` (nou)
- `tests/compare_branches.py` (nou)
- `tests/results/20260328_235135/` (resultats RAG)
- `../ATNE-hardcoded/tests/results/20260328_235915/` (resultats hardcoded, worktree temporal)
