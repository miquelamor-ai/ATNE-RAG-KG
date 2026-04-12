# Experiment Questions - Informe Final

**Avaluacions**: 767
**Models generadors**: gemma, gpt4o-mini, llama, mistral
**Jutges**: gemini_flash, gpt4o, llama_judge, mistral_judge, qwen_judge


## Taula 0 - Validesa JSON per model

| Model | JSON valids | Total | % |
|---|---|---|---|
| gemma | 250 | 250 | 100.0% |
| gpt4o-mini | 250 | 250 | 100.0% |
| llama | 17 | 17 | 100.0% |
| mistral | 250 | 250 | 100.0% |

## Taula 1 - Ranking global per model

| Rank | Model | Score Total | n casos |
|---|---|---|---|
| 1 | **Gemma 4 31B (open Google)** | 4.40 | 250 |
| 2 | **Mistral Small (open EU)** | 4.20 | 250 |
| 3 | **GPT-4o-mini (closed)** | 4.09 | 250 |
| 4 | **Llama 3.3 70B (open Meta)** | 3.91 | 17 |

## Taula 2 - Per criteri

| Model | validesa_pedagogica | adequacio_nivell | discriminacio | originalitat_redaccio | format_estructural | TOTAL |
|---|---|---|---|---|---|---|
| **gemma** | 4.46 | 4.24 | 3.98 | 4.36 | 4.99 | **4.40** |
| **gpt4o-mini** | 4.03 | 4.01 | 3.57 | 4.00 | 4.97 | **4.09** |
| **llama** | 4.57 | 3.75 | 3.08 | 2.70 | 4.94 | **3.91** |
| **mistral** | 4.30 | 3.94 | 3.87 | 3.99 | 4.98 | **4.20** |

## Taula 3 - Per tipus de pregunta

| Tipus | Millor model | Score | Pitjor | Score |
|---|---|---|---|---|
| analisi | **gemma** | 4.58 | gpt4o-mini | 4.17 |
| aplicacio | **gemma** | 4.67 | gpt4o-mini | 4.19 |
| avaluatives | **gemma** | 4.81 | gpt4o-mini | 4.38 |
| comprensio | **gemma** | 4.38 | gpt4o-mini | 3.92 |
| creatives | **gemma** | 4.74 | gpt4o-mini | 4.59 |
| inferencials | **gemma** | 4.57 | gpt4o-mini | 4.18 |
| literals | **gpt4o-mini** | 3.99 | mistral | 3.87 |
| metacognitives | **gemma** | 4.15 | gpt4o-mini | 3.80 |
| vocabulari_contextual | **mistral** | 4.04 | gpt4o-mini | 3.85 |

## Taula 4 - Per perfil

| Perfil | Millor model | Score |
|---|---|---|
| altes_capacitats | **gemma** | 4.95 |
| doble_excepcionalitat | **gemma** | 4.46 |
| nouvingut_arabic | **gemma** | 3.83 |
| tdah_di_lleu | **llama** | 4.04 |
| tdah_lleu | **gemma** | 4.35 |
| tdl_pragmatica | **gemma** | 4.14 |

## Taula 5 - Concordança inter-jutge

| Jutge 1 | Jutge 2 | r | n |
|---|---|---|---|
| gpt4o | llama_judge | 0.75 | 70 |
| gpt4o | mistral_judge | 0.68 | 1250 |
| gpt4o | qwen_judge | 0.66 | 485 |
| llama_judge | mistral_judge | 0.80 | 70 |
| llama_judge | qwen_judge | 0.55 | 45 |
| mistral_judge | qwen_judge | 0.59 | 485 |

## Decisio final

- **Millor model per generar preguntes**: Gemma 4 31B (open Google) (4.40/5)
- **Millor en validesa_pedagogica**: llama (4.57)
- **Millor en adequacio_nivell**: gemma (4.24)
- **Millor en discriminacio**: gemma (3.98)
- **Millor en originalitat_redaccio**: gemma (4.36)
- **Millor en format_estructural**: gemma (4.99)