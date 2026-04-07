# Anàlisi profunda — multi_v2 RAG-v2

**Data**: 5 abril 2026
**Eina**: `tests/deep_analysis.py`
**Dades**: 4.200 avaluacions externes (sense self-eval)

---

## 1. Puntuació per perfil d'alumnat

| Perfil | N | Mitjana | Dificultat |
|--------|---|---------|-----------|
| **P6 DI pre-A1 DUA Accés** | 140 | **4.43** | Més fàcil |
| **P5 Dislèxia A2 DUA Accés** | 130 | **4.33** | Fàcil |
| **P9 TDAH+TEA B1 (creuat)** | 137 | **4.32** | Fàcil (sorprenent) |
| **P10 Vulnerabilitat+TDL A2** | 135 | 4.32 | Fàcil |
| P3 TDAH A2 DUA Core | 136 | 4.31 | Mitjà |
| P4 TEA B1 DUA Core | 137 | 4.31 | Mitjà |
| P8 Nouvingut+Dislèxia A1 | 137 | 4.21 | Mitjà |
| P2 Nouvingut xinès A1 | 135 | 4.08 | Difícil |
| P1 Nouvingut àrab pre-A1 | 138 | 4.06 | Difícil |
| **P7 Altes capacitats B2 Enriquiment** | 139 | **3.99** | **Més difícil** |

### Troballes clau

**Els perfils més DIFÍCILS d'adaptar**:

1. **P7 Altes capacitats** (3.99): els LLMs tendeixen a **simplificar per defecte**, en comptes d'**enriquir**. L'inversió del DUA (C2 invertit) no s'aplica bé.
2. **P1/P2 Nouvinguts** (~4.07): combinació de pre-A1/A1 + necessitat d'L1 real + pictogrames és complexa.

**Els perfils més FÀCILS**:

1. **P6 DI lleugera** (4.43): Lectura Fàcil extrema és un patró ben assimilat pels LLMs.
2. **P5 Dislèxia** (4.33): instruccions clares i fàcils d'aplicar.
3. **P9 TDAH+TEA** (4.32): **sorprenent**, el creuament s'aplica bé.

### Implicacions

- Cal **reforçar el prompt per altes capacitats** (instruccions clares d'enriquiment, no simplificació)
- Cal **millorar la gestió L1** per a perfils nouvinguts
- Els **perfils creuats (2e)** no són sistemàticament més difícils que els simples

---

## 2. Puntuació per etapa educativa

| Etapa | N | Mitjana |
|-------|---|---------|
| **Primària** | 349 | **4.32** |
| ESO | 702 | 4.27 |
| **Batxillerat** | 313 | **4.07** |

**Interpretació**: els models adapten millor textos **de primària** (simples, concrets) que de **batxillerat** (abstractes, argumentació complexa).

---

## 3. Puntuació per gènere discursiu

| Gènere | N | Mitjana |
|--------|---|---------|
| **Instrucció** | 330 | **4.31** |
| Argumentació | 371 | 4.29 |
| Explicació | 330 | 4.23 |
| **Narració** | 333 | **4.11** |

**Interpretació**: la **narració** és el gènere més difícil d'adaptar. Els models tenen dificultats per preservar la veu narrativa simplificant el llenguatge.

---

## 4. Heatmap etapa × gènere

| etapa/gènere | argumentació | explicació | instrucció | narració |
|--------------|-------------|-----------|-----------|----------|
| Primària | 4.32 | **4.38** | 4.35 | 4.25 |
| ESO | 4.32 | 4.23 | 4.34 | 4.17 |
| **Batxillerat** | 4.15 | 4.13 | 4.20 | **3.78** |

**El cas més difícil**: **narració de batxillerat (3.78)** — els LLMs tenen més problemes amb narratives complexes d'alt nivell.

---

## 5. Anàlisi d'errors (68 casos amb puntuació < 3.0)

### Distribució per generador

| Generador | Casos erronis | % del total |
|-----------|---------------|-------------|
| **Gemini** | **54** | **79%** |
| Gemma 4 | 9 | 13% |
| GPT | 5 | 7% |

**Confirma**: Gemini sense thinking tokens falla sistemàticament. Cal regenerar.

### Perfils més problemàtics en errors

| Perfil | Casos erronis |
|--------|---------------|
| **P7 Altes capacitats** | **20** |
| **P1 Nouvingut àrab** | **20** |
| P2 Nouvingut xinès | 15 |
| P8 Nouvingut+Dislèxia | 12 |
| P5 Dislèxia | 1 |

### Criteris més baixos en casos erronis

| Criteri | Mitjana casos erronis |
|---------|---------------------|
| **A3 Llegibilitat** | **1.53** |
| **B3 Scaffolding** | **1.69** |
| **C1 Aprenentatge** | **1.72** |
| B2 Perfil | 1.74 |
| A1 Coherència | 1.90 |
| A2 Gramàtica | 2.34 |
| B1 Fidelitat | 2.34 |
| B4 Cultura | 2.57 |

**Patró clar**: quan un text adaptat falla, falla en els criteris **pedagògics** (llegibilitat, scaffolding, aprenentatge) més que en els **textuals** (gramàtica, fidelitat).

**Implicació**: els LLMs poden generar textos gramaticalment correctes però **pedagògicament inútils**. Calen prompts més pedagògics, no més gramaticals.

---

## 6. Inter-judge agreement (Krippendorff's α)

### Resultat principal: **α = 0.359**

**CRÍTIC**: els 3 jutges **NO estan d'acord entre ells** (llindar mínim acceptable: 0.667).

### Correlacions parellades (Spearman ρ)

| Parella jutges | ρ | p | Interpretació |
|----------------|---|---|---------------|
| GPT-4o-mini vs Mistral | 0.44 | <0.001 | Correlació moderada |
| Gemini vs Mistral | 0.30 | <0.001 | Correlació petita |
| **Gemini vs GPT-4o-mini** | **0.14** | 0.053 | **Quasi cap correlació** |

### Implicacions

Això és el **problema metodològic més greu** que hem detectat:

1. **Gemini i GPT veuen coses diferents** (ρ = 0.14): el seu acord és quasi aleatori
2. **Sense validació humana, no podem saber quin té raó**
3. El rànquing depèn de **quin jutge fem servir**, més que de la qualitat real dels models

### Com es resol

Només hi ha una manera: **validació humana**. Experts pedagògics jutgen una mostra aleatòria (p.ex. 100 casos). Aleshores:
- Calculem correlació jutge-humà per cada jutge LLM
- El jutge més correlacionat amb humans és el "vàlid"
- O bé, es pot fer **mitjana ponderada** dels jutges LLM amb pesos inversos al desacord

### Veredicte honest

Els rànquings actuals són **orientatius, no definitius**. Per presentar dades fiables a direcció FJE:

- ✅ Podem dir: "hi ha diferències significatives entre models" (Kruskal-Wallis p<0.001)
- ✅ Podem dir: "GPT surt per davant en múltiples anàlisis"
- ⚠️ **NO podem afirmar**: "Gemma 4 és millor que Mistral" (Krippendorff insuficient)
- ⚠️ Cal validació humana abans de conclusions definitives

---

## Conclusions i plans d'acció

### Què ens diuen les dades

1. **Altes capacitats és el perfil pitjor servit** → cal millorar el prompt per Enriquiment
2. **Narrativa de batxillerat és el cas més difícil** → cal afegir instruccions específiques
3. **Els errors són pedagògics, no textuals** → calen prompts més centrats en aprenentatge
4. **Els jutges LLM no es posen d'acord** → validació humana imprescindible

### Millores concretes al prompt

**Per P7 (Altes capacitats)**:
- Afegir instrucció explícita: "NO simplifiquis. Afegeix complexitat, vocabulari tècnic, connexions interdisciplinars"
- Exemples concrets d'enriquiment

**Per P1/P2 (Nouvinguts)**:
- Glossari L1 com a **requisit obligatori** (no opcional)
- Limitar text principal a 300 paraules

**Per narració**:
- Instruccions específiques de preservar estructura narrativa
- Mantenir personatges, veu, temps verbals

### Pla d'acció derivat

1. **Curt termini**: reforçar prompts per P7 i narració (1h)
2. **Mitjà termini**: validació humana FJE durant el pilot
3. **Llarg termini**: refer rúbrica v3 amb només 2 dimensions validades (qualitat + fidelitat)
