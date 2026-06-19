# Peça 4 — Experiment A/B: skills OFF vs skills ON

## Objectiu

Mesurar si activar les SKILLs (`ATNE_USE_SKILLS=true`) millora la qualitat de
l'adaptació respecte a tenir-les desactivades (`false`, prompt al catàleg hardcoded
+ corpus_reader), amb el **model de producció actual** com a generador.

## Disseny

- **Variable única**: `ATNE_USE_SKILLS` (`false` = OFF / `true` = ON).
  L'única diferència entre les dues condicions és el flag; el prompt es construeix
  amb la mateixa funció de producció `build_system_prompt(..., adapter_only=True)`.
- **Generador**: `gemini-2.5-flash-lite` (el valor viu de `system_config.atne_model_adapt`
  a Supabase, posat per admin). Temperatura **0.4 IDÈNTICA** a OFF i ON.
- **Jutge**: `anthropic/claude-sonnet-4.6` via OpenRouter (DIFERENT del generador, obligatori).
  Verificat contra el catàleg d'OpenRouter abans d'avaluar.
- **5 casos** (`text_id` aparella text↔perfil):

  | # | Gènere | MECR | Perfil | Complement | Skills esperades ON |
  |---|---|---|---|---|---|
  | 1 | notícia | A2 | nouvingut | glossari L1 | write-noticia + adapt |
  | 2 | conte | pre-A1 | TEA | pictogrames | write-conte + generate-pictogrames |
  | 3 | instructiu | B1 | TDAH | — | write-instructiu + adapt |
  | 4 | opinió | B2 | altes capacitats | — | write-opinio + adapt |
  | 5 | descripció | A2 | dislèxia | glossari | write-descripcio + generate-glossari |

- **Rúbrica**: 5 criteris 1-5 (`rubrica.json`), mateixos pesos de sempre.
- **Anàlisi**: descriptiva (Δ ON−OFF per criteri + mitjana ponderada). **NO** test de
  significació: n=5 no té potència. El verdict és un senyal qualitatiu, no una prova.

## Fitxers

| Fitxer | Descripció |
|--------|-----------|
| `textos.json` | 5 textos (un per cas) |
| `perfils.json` | 5 perfils + `text_id` + `complements` + `genere` |
| `rubrica.json` | 5 criteris amb descriptors 1-5 |
| `experiment_ab.py` | Generació 5 casos × (OFF/ON), commuta `ATNE_USE_SKILLS` per cas |
| `eval_experiment.py` | Avaluació amb Claude Sonnet 4.6 (verifica slug abans) |
| `stats_experiment.py` | Taula descriptiva Δ ON−OFF + informe |
| `run_all.py` | Orquestrador |

## Com executar

```bash
cd c:\Users\miquel.amor\Documents\GitHub\ATNE

# Tot en seqüència:
python tests/experiment_ab/run_all.py

# Pas a pas:
python tests/experiment_ab/experiment_ab.py     # 5 casos × (OFF/ON), Gemini Lite
python tests/experiment_ab/eval_experiment.py   # judici Claude Sonnet 4.6
python tests/experiment_ab/stats_experiment.py  # informe

# Saltar generació si ja tens resultats_generacio.json:
python tests/experiment_ab/run_all.py --skip-gen
```

## Sortida per a la revisió pedagògica

- **`resultats_generacio.json`** — per cas: original + adaptat OFF + adaptat ON +
  skills actives + temps. AQUÍ es llegeixen els dos textos costat a costat.
- **`resultats_avaluacio.json`** — puntuacions + justificacions del jutge per cas/condició.
- **`informe_resultats.md`** — taula Δ ON−OFF per criteri i cas + resum global + verdict orientatiu.

## Requisits .env

- `GEMINI_API_KEY` (una o més, amb rotació) — generador.
- `OPENROUTER_API_KEY` — jutge Claude Sonnet 4.6.

## Cost estimat

- Generació: 5 × 2 = 10 crides a `gemini-2.5-flash-lite` (free tier) ≈ **0 €**.
- Judici: 5 × 2 = 10 avaluacions a Sonnet 4.6 ≈ **0,25–0,35 €**.
- **Total ≈ 0,25–0,35 €.**
