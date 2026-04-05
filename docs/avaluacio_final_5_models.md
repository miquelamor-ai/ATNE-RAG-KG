# Avaluacio final 5 models — RAG-v2

**Data**: 5 abril 2026
**Rubrica**: v2 (8 criteris: A1-A3, B1-B4, C1)
**Jutges externs**: Gemini 2.5 Flash, GPT-4o-mini, Mistral Small
**Generadors**: Gemini, GPT, Sonnet, Gemma 4, Mistral
**Protocol**: self-eval exclos (cada model jutjat nomes per jutges diferents)

---

## 1. Ranking global

Resultats de RAG-v2 (branca nova amb macrodirectives i filtratge granular):

| Pos | Generador | Global | A1 Coher | A2 Gram | A3 Lleg | B1 Contingut | B2 Perfil | B3 Scaffold | B4 Cultura | C1 Aprenentatge |
|-----|-----------|--------|----------|---------|---------|--------------|-----------|-------------|------------|-----------------|
| 🥇 1 | **GPT-4o-mini** | **4.44** | 4.30 | **4.73** | **4.36** | 4.68 | **4.39** | **4.17** | **4.46** | 4.46 |
| 🥈 2 | **Gemma 4 31B** | **4.23** | 3.85 | 4.36 | 4.12 | 4.53 | 4.30 | 4.08 | 4.09 | 4.36 |
| 🥉 3 | **Mistral Small** | **4.19** | **3.96** | 4.74 | 4.03 | **4.81** | 4.02 | 3.74 | 4.23 | 4.11 |
| 4 | Gemini 2.5 Flash | 3.93 | 3.69 | 4.23 | 3.76 | 4.25 | 3.97 | 3.69 | 3.88 | 3.95 |
| 5 | Claude Sonnet 3.5 | 2.04 | 1.90 | 2.40 | 2.06 | 2.13 | 1.89 | 1.80 | 2.25 | 1.96 |

**Nota**: Sonnet RAG-v2 invalid per bug de generacio (textos truncats a 111 paraules).
Es pot veure que en HC/RAG-v1, Sonnet puntua 4.37-4.42.

---

## 2. Per que GPT guanya

- Lidera en **6 de 8 criteris**: A2 (gramatica), A3 (llegibilitat), B2 (perfil), B3 (scaffolding), B4 (cultura)
- Millor equilibri entre qualitat i adequacio pedagogica
- Textos mes concisos (~323 paraules vs 637 Gemini, 520 Mistral, 552 Gemma 4)

---

## 3. Gemma 4 vs Mistral — duel dels models gratuits

| Criteri | Gemma 4 | Mistral | Guanyador |
|---------|---------|---------|-----------|
| A1 Coherencia | 3.85 | 3.96 | Mistral +0.11 |
| A2 Gramatica | 4.36 | 4.74 | Mistral +0.38 |
| A3 Llegibilitat | 4.12 | 4.03 | Gemma 4 +0.09 |
| B1 Contingut | 4.53 | 4.81 | Mistral +0.28 |
| B2 Perfil | 4.30 | 4.02 | **Gemma 4 +0.28** |
| B3 Scaffolding | 4.08 | 3.74 | **Gemma 4 +0.34** |
| B4 Cultura | 4.09 | 4.23 | Mistral +0.14 |
| C1 Aprenentatge | 4.36 | 4.11 | **Gemma 4 +0.25** |
| **Global** | **4.23** | **4.19** | Gemma 4 +0.04 |

### Fortaleses

**Gemma 4** excel.leix en:
- **Adequacio al perfil** (B2): aplica millor les instruccions per perfil
- **Scaffolding** (B3): millor us de glossaris, titols, esquemes
- **Potencial d'aprenentatge** (C1): l'alumne apren mes

**Mistral** excel.leix en:
- **Gramatica** (A2): menys errors linguistics
- **Fidelitat curricular** (B1): preserva millor el contingut original
- **Coherencia** (A1): millor flux de les idees

### Conclusio del duel
- **Empat tecnic** (0.04 punts de diferencia global)
- **Gemma 4** millor per a perfils amb necessitats educatives especifiques (NESE, nouvingut)
- **Mistral** millor per a textos de rigor curricular (ciencies, humanitats)
- **Velocitat**: Mistral es 10x mes rapid (9s vs 107s per adaptacio)

---

## 4. Analisi per jutge (biaix)

Quin jutge es mes exigent?

| Generador | Jutge Gemini | Jutge GPT-4o-mini | Jutge Mistral |
|-----------|-------------|-------------------|---------------|
| gemini | — (self) | 3.71 | 4.28 |
| gpt | 4.75 | — (self) | 4.61 |
| sonnet | 1.86 | 2.28 | 1.90 |
| gemma4 | — | 3.94 | **4.66** |
| mistral | — | 4.19 | — (self) |

### Patrons detectats

- **GPT-4o-mini** es el jutge **mes exigent** (mitjanes mes baixes)
- **Gemini** puntua mes alt en general (tendencia a ser generos)
- **Mistral** puntua Gemma 4 molt alt (4.66) — podria ser afinitat entre models europeus?

### Recomanacio per a futurs benchmarks
Usar **GPT-4o-mini** com a jutge de referencia (mes discriminatiu, mes conservador).

---

## 5. Comparatiu HC vs RAG-v1 vs RAG-v2

| Generador | HC | RAG-v1 | RAG-v2 | Millor |
|-----------|-----|--------|--------|--------|
| gemini | **4.37** | 4.01 | 3.93 | HC |
| gpt | 4.37 | 4.41 | **4.44** | RAG-v2 |
| sonnet | **4.37** | **4.42** | 2.04* | RAG-v1 |
| gemma4 | — | — | **4.23** | — |
| mistral | — | — | **4.19** | — |

*Sonnet RAG-v2 invalid per bug

### Conclusions
- **Per Gemini**: HC es millor (diferencia significativa, -0.44 respecte RAG-v2)
- **Per GPT**: RAG-v2 > RAG-v1 > HC (progres consistent)
- **Per Sonnet**: RAG-v1 es el millor (0.05 millor que HC)
- Els models nous (Gemma 4, Mistral) nomes s'han testat amb RAG-v2

---

## 6. Recomanacio final per ATNE

### Per a produccio

| Prioritat | Model recomanat | Cost |
|-----------|----------------|------|
| **Maxima qualitat** | GPT-4o-mini | ~0.003€/cas |
| **Cost zero + velocitat** | **Mistral Small** | **0€** |
| **Cost zero + open-source** | **Gemma 4 31B** | **0€** |
| **Tria del docent** | Oferir Mistral O Gemma 4 | **0€** |

### Disseny implementat

La UI d'ATNE ara permet al docent triar entre **Mistral** i **Gemma 4** abans de cada adaptacio. Aixo permet:

1. **Comparar qualitats** en casos reals d'aula
2. **Recopilar feedback** docent per validar l'eleccio del model
3. **Evitar vendor lock-in** (si un proveidor canvia termes, tenim backup)
4. **Transparencia**: el docent sap quin model l'adapta

### Fluxe d'auto-avaluacio (futur)

Generate + Verify + Retry:
```
Docent -> Mistral o Gemma 4 genera -> Gemma 4 jutja (rubrica v2)
          Si puntuacio >= 4.0 -> Lliura al docent
          Si puntuacio <  4.0 -> Regenera amb altre model (max 2 intents)
```

Cost: 0€ (tot free tier). Garanteix qualitat minima de 4.0/5.0.
