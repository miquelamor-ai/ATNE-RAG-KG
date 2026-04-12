# Experiment Complements - Informe Final

**Avaluacions**: 513
**Models generadors**: gemma, gpt4o-mini, llama, mistral
**Jutges**: gemini_flash, gpt4o, llama_judge, mistral_judge, qwen_judge


## Taula 1 - Ranking global per model (mitjana ponderada de criteris)

| Rank | Model | Score Total | n casos |
|---|---|---|---|
| 1 | **Gemma 4 31B (open Google)** | 4.58 | 160 |
| 2 | **GPT-4o-mini (closed)** | 4.46 | 160 |
| 3 | **Llama 3.3 70B (open Meta)** | 4.37 | 33 |
| 4 | **Mistral Small (open EU)** | 4.34 | 160 |

## Taula 2 - Per criteri (mitjana per model)

| Model | correccio_linguistica | adequacio_perfil | carrega_cognitiva | utilitat_practica | coherencia_text | TOTAL |
|---|---|---|---|---|---|---|
| **gemma** | 4.55 | 4.55 | 4.54 | 4.52 | 4.93 | **4.58** |
| **gpt4o-mini** | 4.52 | 4.39 | 4.30 | 4.44 | 4.91 | **4.46** |
| **llama** | 4.15 | 4.32 | 4.39 | 4.36 | 4.90 | **4.37** |
| **mistral** | 4.77 | 4.10 | 4.07 | 4.18 | 4.97 | **4.34** |

## Taula 3 - Per tipus de complement (millor model)

| Tipus complement | Millor model | Score | Pitjor | Score |
|---|---|---|---|---|
| analogies_quotidianes | **gemma** | 4.73 | mistral | 4.38 |
| esquema_visual | **gemma** | 4.44 | mistral | 4.20 |
| glossari_bilingue_arab | **gemma** | 4.64 | llama | 4.18 |
| glossari_simple | **gemma** | 4.45 | gpt4o-mini | 4.34 |
| mapa_conceptual | **gemma** | 4.53 | mistral | 4.33 |
| pictogrames_descrits | **gemma** | 4.76 | mistral | 4.35 |
| preguntes_intercalades | **gemma** | 4.61 | mistral | 4.25 |
| transliteracio_fonetica | **gemma** | 4.68 | mistral | 4.55 |

## Taula 4 - Per perfil (millor model)

| Perfil | Millor model | Score |
|---|---|---|
| altes_capacitats | **gemma** | 4.65 |
| doble_excepcionalitat | **gemma** | 4.42 |
| nouvingut_arabic | **gemma** | 4.66 |
| tdah_di_lleu | **gemma** | 4.61 |
| tdah_lleu | **gemma** | 4.53 |
| tdl_pragmatica | **gemma** | 4.56 |

## Taula 5 - Concordança inter-jutge (correlacio Pearson)

| Jutge 1 | Jutge 2 | r | n |
|---|---|---|---|
| gemini_flash | gpt4o | 0.19 | 45 |
| gemini_flash | llama_judge | 0.23 | 15 |
| gemini_flash | mistral_judge | 0.03 | 45 |
| gemini_flash | qwen_judge | 0.26 | 45 |
| gpt4o | llama_judge | 0.58 | 70 |
| gpt4o | mistral_judge | 0.11 | 800 |
| gpt4o | qwen_judge | 0.17 | 664 |
| llama_judge | mistral_judge | 0.07 | 70 |
| llama_judge | qwen_judge | 0.42 | 65 |
| mistral_judge | qwen_judge | 0.13 | 664 |

## Decisio final

- **Millor model per generar complements**: Gemma 4 31B (open Google) (4.58/5)
- **Millor en correccio_linguistica**: mistral (4.77)
- **Millor en adequacio_perfil**: gemma (4.55)
- **Millor en carrega_cognitiva**: gemma (4.54)
- **Millor en utilitat_practica**: gemma (4.52)
- **Millor en coherencia_text**: mistral (4.97)