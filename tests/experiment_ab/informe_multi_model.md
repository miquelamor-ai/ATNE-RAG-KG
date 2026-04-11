# Xat 9 - Informe Final MULTI-MODEL

**Avaluacions**: 604 parells
**Models generadors**: gemma, gpt4o-mini, llama, mistral
**Jutges**: claude_sonnet, gemini_flash, gpt4o, llama_judge, mistral_judge, qwen_judge


## Taula 1 - Puntuacio global ponderada per model i condicio

(Mitjana dels jutges, escala 1-5)

| Model | A (minim) | B (complet) | Diff B-A | Cohen's d | Decisio |
|---|---|---|---|---|---|
| **gemma** | 4.62 | 4.77 | +0.14 | +0.33 (petit) | Negligible (minim suficient) |
| **gpt4o-mini** | 3.57 | 4.19 | +0.62 | +1.19 (gran) | **Prompt complet val la pena** |
| **llama** | 4.00 | 4.27 | +0.26 | +0.52 (mitja) | Negligible (minim suficient) |
| **mistral** | 4.47 | 4.64 | +0.17 | +0.53 (mitja) | Negligible (minim suficient) |

## Taula 2 - Per criteri: mitjana de B (prompt complet) per model

| Model | Adequacio MECR | Fidelitat | Perfil | Llegibilitat | Complements | TOTAL |
|---|---|---|---|---|---|---|
| **gemma** | 4.48 | 4.74 | 4.88 | 4.90 | 4.87 | **4.75** |
| **gpt4o-mini** | 4.02 | 4.50 | 4.08 | 4.18 | 4.25 | **4.19** |
| **llama** | 4.04 | 4.35 | 4.38 | 4.14 | 4.46 | **4.26** |
| **mistral** | 4.27 | 4.83 | 4.71 | 4.76 | 4.74 | **4.64** |

## Taula 3 - Eficiencia (qualitat vs cost)

| Model | Qualitat (B total) | Cost relatiu | Ratio Q/Cost | Notes |
|---|---|---|---|---|
| gemma | 4.75 | 0.0 | GRATIS | Free tier |
| gpt4o-mini | 4.19 | 0.38 | 11.0 | $0.38/M tok |
| llama | 4.26 | 0.0 | GRATIS | Free tier |
| mistral | 4.64 | 0.3 | 15.5 | $0.30/M tok |

## Taula 4 - Comparativa per criteri (millor model en cada criteri, condicio B)

| Criteri | Millor model | Puntuacio | Pitjor | Puntuacio |
|---|---|---|---|---|
| adequacio_linguistica | **gemma** | 4.48 | gpt4o-mini | 4.02 |
| fidelitat_curricular | **mistral** | 4.83 | llama | 4.35 |
| adequacio_perfil | **gemma** | 4.88 | gpt4o-mini | 4.08 |
| llegibilitat_estructura | **gemma** | 4.90 | llama | 4.14 |
| complements | **gemma** | 4.87 | gpt4o-mini | 4.25 |

## Taula 5 - Concordança inter-jutge (correlacio Pearson)

| Jutge 1 | Jutge 2 | r | n |
|---|---|---|---|
| claude_sonnet | gemini_flash | 0.68 | 470 |
| claude_sonnet | gpt4o | 0.63 | 470 |
| claude_sonnet | llama_judge | 0.63 | 60 |
| claude_sonnet | mistral_judge | 0.61 | 470 |
| claude_sonnet | qwen_judge | 0.55 | 470 |
| gemini_flash | gpt4o | 0.75 | 1170 |
| gemini_flash | llama_judge | 0.39 | 140 |
| gemini_flash | mistral_judge | 0.66 | 1170 |
| gemini_flash | qwen_judge | 0.43 | 998 |
| gpt4o | llama_judge | 0.37 | 190 |
| gpt4o | mistral_judge | 0.68 | 3818 |
| gpt4o | qwen_judge | 0.44 | 2221 |
| llama_judge | mistral_judge | 0.43 | 140 |
| llama_judge | qwen_judge | 0.29 | 190 |
| mistral_judge | qwen_judge | 0.41 | 2216 |

## Decisio final per a FJE

- **Millor qualitat global**: gemma (4.75/5)
- **Millor en complements**: gemma (4.87/5)
- **Millor adequacio al perfil**: gemma (4.88/5)
- **Millor eficiencia (qualitat/cost)**: gemma

### Quan pagar la pena el prompt complet
- **gemma**: diff = +0.14, d = +0.33 → Negligible (minim suficient)
- **gpt4o-mini**: diff = +0.62, d = +1.19 → **Prompt complet val la pena**
- **llama**: diff = +0.26, d = +0.52 → Negligible (minim suficient)
- **mistral**: diff = +0.17, d = +0.53 → Negligible (minim suficient)