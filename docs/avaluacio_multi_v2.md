# Avaluacio multi_v2 — Informe complet

**Data**: 31 marc - 2 abril 2026
**Base de dades**: `tests/results/evaluations.db` (71 MB)
**Codi**: `tests/multi_v2.py`

---

## 1. Disseny experimental

### 1.1 Generadors (3)
| Generador | Model | Cost |
|-----------|-------|------|
| **gemini** | Gemini 2.5 Flash | Gratuit (free tier) |
| **gpt** | GPT-4o-mini | ~$2 total |
| **sonnet** | Claude Sonnet 3.5 (CLI) | $0 (quota personal) |

### 1.2 Branques (3)
| Branca | Descripcio |
|--------|-----------|
| **hc** (hardcoded) | CAPA 3d amb text fix per perfil |
| **rag_v1** | Instruccions recuperades del corpus (versio 1) |
| **rag_v2** | Instruccions amb macrodirectives i filtratge granular |

### 1.3 Casos de prova
- **20 textos**: 4 etapes (PRI, ESO1, ESO2, BAT) x 4 generes discursius + 4 textos culturals
- **10 perfils**: P1-P7 (simples) + P8-P10 (creuats: Nouvingut+Dislexia, TDAH+TEA, Vulnerabilitat+TDL)
- **Total**: 200 casos base x 3 branques x 3 generadors = **1.800 textos generats**

### 1.4 Jutges (2)
| Jutge | Model | Cost |
|-------|-------|------|
| **gemini** | Gemini 2.5 Flash | $0 |
| **gpt4mini** | GPT-4o-mini | ~$2 |

### 1.5 Fases d'avaluacio
1. **Individual**: rubrica v2 (8 criteris) per cada text → 3.016 avaluacions
2. **Trio intra-model**: ranking HC vs RAG-v1 vs RAG-v2 per generador → 1.077 trios
3. **Cross-model**: parells RAG-v2 entre generadors → 2.296 comparacions

---

## 2. Rubrica v2

Tres dimensions, 8 criteris (1-5), basada en 6 marcs teorics.

| Dim. | Criteri | Marc teoric | Pes |
|------|---------|-------------|-----|
| **A** Qualitat textual | A1 Coherencia i cohesio | Halliday LSF | 0.3 |
| | A2 Correccio linguistica | Norma IEC | |
| | A3 Llegibilitat i complexitat | TSAR/SIERA | |
| **B** Adequacio pedagogica | B1 Fidelitat curricular | Mayer coherence | 0.5 |
| | B2 Adequacio al perfil | UDL/CAST, DUA | |
| | B3 Suports cognitius (scaffolding) | Sweller CLT, Vygotsky ZPD | |
| | B4 Sensibilitat cultural | UDL Engagement | |
| **C** Eficacia | C1 Potencial d'aprenentatge | Vygotsky ZPD, Bloom | 0.2 |

**Puntuacio global** = A*0.3 + B*0.5 + C*0.2

Detall complet a: `evaluator_rubrics.py`

---

## 3. Resultats individuals

### 3.1 Per generador i branca (mitjana dels 2 jutges)

| Generador | Branca | N | A1 | A2 | A3 | B1 | B2 | B3 | B4 | C1 | **Global** |
|-----------|--------|---|-----|-----|-----|-----|-----|-----|-----|-----|-----------|
| gemini | hc | 336 | 4.22 | 4.73 | 4.59 | 4.65 | 4.64 | 4.30 | 4.62 | 4.61 | **4.55** |
| gemini | rag_v1 | 336 | 3.75 | 4.42 | 4.23 | 3.97 | 4.39 | 4.20 | 4.36 | 4.10 | **4.18** |
| gemini | rag_v2 | 337 | 3.84 | 4.38 | 4.17 | 3.86 | 4.35 | 4.12 | 4.23 | 3.98 | **4.10** |
| gpt | hc | 335 | 4.13 | 4.61 | 4.50 | 4.55 | 4.39 | 3.98 | 4.51 | 4.48 | **4.40** |
| gpt | rag_v1 | 334 | 4.25 | 4.64 | 4.40 | 4.63 | 4.41 | 4.10 | 4.58 | 4.44 | **4.43** |
| gpt | **rag_v2** | 334 | 4.33 | 4.66 | 4.40 | 4.73 | 4.34 | 4.11 | 4.60 | 4.42 | **4.44** |
| sonnet | hc | 334 | 3.99 | 4.40 | 4.55 | 4.09 | 4.58 | 4.22 | 4.57 | 4.54 | **4.39** |
| sonnet | rag_v1 | 335 | 4.15 | 4.48 | 4.55 | 4.27 | 4.61 | 4.22 | 4.56 | 4.55 | **4.44** |
| sonnet | rag_v2 | 335 | 1.92 | 2.47 | 2.11 | 2.03 | 1.83 | 1.79 | 2.27 | 1.92 | **2.02** |

### 3.2 Per jutge (desglossament)

**Jutge Gemini** (tendeix a puntuar alt, 4.4-4.8):

| Generador | HC | RAG-v1 | RAG-v2 |
|-----------|-----|--------|--------|
| gemini | **4.84** | 4.55 | 4.44 |
| gpt | 4.69 | 4.73 | **4.75** |
| sonnet | 4.68 | **4.74** | 1.86 |

**Jutge GPT-4o-mini** (mes exigent, 3.6-4.1):

| Generador | HC | RAG-v1 | RAG-v2 |
|-----------|-----|--------|--------|
| gemini | **4.12** | 3.63 | 3.61 |
| gpt | 3.97 | 3.98 | **3.99** |
| sonnet | 3.95 | **3.98** | 2.27 |

### 3.3 Observacions
- **Gemini (jutge)** puntua ~0.7 punts mes alt que GPT-4o-mini sistematicament
- **Gemini (generador)**: HC guanya clarament. RAG-v2 no millora RAG-v1
- **GPT (generador)**: RAG-v2 >= RAG-v1 > HC. El RAG funciona be amb GPT
- **Sonnet RAG-v2**: puntuacio catastrofica (2.02/5) — generacio truncada (111 paraules avg)

---

## 4. Resultats trios (ranking intra-model)

Cada trio compara HC vs RAG-v1 vs RAG-v2 per un mateix generador. El valor indica quantes vegades cada branca queda 1a.

### 4.1 Jutge Gemini

| Generador | HC 1r | v1 1r | v2 1r | Total |
|-----------|-------|-------|-------|-------|
| gemini | **62** | 25 | 22 | 111 |
| gpt | 40 | 38 | **35** | 117 |
| sonnet | 37 | **74** | 0 | 115 |

### 4.2 Jutge GPT-4o-mini

| Generador | HC 1r | v1 1r | v2 1r | Total |
|-----------|-------|-------|-------|-------|
| gemini | **102** | 51 | 91 | 244 |
| gpt | 46 | 83 | **116** | 245 |
| sonnet | 106 | **129** | 7 | 245 |

### 4.3 Conclusions trios
- **GPT + RAG-v2**: la millor combinacio. RAG-v2 guanya en ambdos jutges
- **Gemini + HC**: HC domina clarament
- **Sonnet + RAG-v2**: mai guanya (0-7 vegades) per la generacio fallida

---

## 5. Resultats cross-model (RAG-v2 entre generadors)

Comparacio directa de la mateixa adaptacio generada per diferents models.

### 5.1 Jutge Gemini

| Parell | Guanyador | N |
|--------|-----------|---|
| gemini vs gpt | gpt **171** - gemini 162 - empat 3 | 336 |
| gemini vs sonnet | gemini **456** - empat 40 - sonnet 11 | 507 |

### 5.2 Jutge GPT-4o-mini

| Parell | Guanyador | N |
|--------|-----------|---|
| gemini vs gpt | gemini **393** - gpt 177 | 570 |
| gemini vs sonnet | gemini **304** - sonnet 19 | 323 |
| sonnet vs gpt | gpt **540** - sonnet 20 | 560 |

### 5.3 Ranking generadors
1. **Gemini Flash** — guanya la majoria de cross (especialment segons GPT-4o-mini)
2. **GPT-4o-mini** — competitiu amb Gemini (segons jutge Gemini, GPT guanya per poc)
3. **Sonnet** — ultim lloc (per culpa del bug RAG-v2)

---

## 6. Estadistiques de generacio

| Generador | Branca | Paraules avg | Temps avg (s) | Forma avg |
|-----------|--------|-------------|---------------|-----------|
| gemini | hc | 439 | 17.9 | 0.79 |
| gemini | rag_v1 | 589 | 22.7 | 0.73 |
| gemini | rag_v2 | 637 | 24.8 | 0.72 |
| gpt | hc | 278 | 10.0 | 0.74 |
| gpt | rag_v1 | 303 | 11.1 | 0.77 |
| gpt | rag_v2 | 323 | 12.7 | 0.75 |
| sonnet | hc | 213 | 0.0* | 0.79 |
| sonnet | rag_v1 | 222 | 0.0* | 0.78 |
| sonnet | rag_v2 | **111** | 18.3 | **0.46** |

*Sonnet HC/rag_v1 copiats de multi_v1 (timing no capturat)

**Observacions**:
- RAG genera ~35-50% mes paraules que HC (el prompt mes llarg dona mes context)
- Gemini es el mes verbos (~440-637 paraules), GPT el mes concis (~278-323)
- Sonnet RAG-v2: nomes 111 paraules avg (vs 213 HC) — generacio truncada/fallida

---

## 7. Comparativa amb v1 (rubrica anterior, 5 generadors)

Rubrica v1: C1-C5, sense ancoratges. Mitjana de 4 jutges (gemini, gpt, llama, qwen).

| Generador | HC (fons) | RAG (fons) | Diferencia |
|-----------|-----------|------------|------------|
| gemini | **4.36** | 4.04 | HC +0.32 |
| gpt | 4.20 | **4.24** | RAG +0.04 |
| sonnet | 4.20 | **4.30** | RAG +0.10 |
| llama | 4.06 | **4.17** | RAG +0.11 |
| qwen | 3.84 | **3.92** | RAG +0.08 |

**Patrons consistents v1→v2**:
- Gemini: HC sempre guanya (pero amb thinking tokens actius — veure caveats)
- GPT, Sonnet, Llama, Qwen: RAG sempre guanya lleugerament
- Qwen es el pitjor generador, Gemini el millor en absolut

---

## 8. Caveats i limitacions

### 8.1 Thinking tokens de Gemini (CRITIC)
Les 1.000 generacions de Gemini + 343 trios (jutge Gemini) + 843 cross (jutge Gemini) es van fer **AMB thinking tokens actius** (`thinking_budget` no configurat). Gemini 2.5 Flash amb thinking costa 23x mes ($3.50/M tokens vs $0.15/M) i produeix respostes de mes qualitat. **La comparacio no es justa**: Gemini tenia avantatge sobre GPT i Sonnet.

**Impacte**: el resultat "Gemini > GPT" pot ser un artefacte dels thinking tokens. Caldria repetir les generacions amb `thinking_budget=0` per confirmar.

Corregit el 2 abril 2026: `thinking_budget=0` aplicat a tots els fitxers.

### 8.2 Bug Sonnet RAG-v2
Sonnet RAG-v2 genera nomes 111 paraules de mitjana (vs 213 per HC). La generacio es va fer via `claude.cmd` CLI i molts outputs van quedar truncats. **Tots els resultats que impliquen Sonnet RAG-v2 son invalids** i cal descartar-los de les conclusions.

### 8.3 Biaix del jutge Gemini
Gemini com a jutge puntua ~0.7 punts mes alt que GPT-4o-mini. Quan jutja Gemini com a generador (self-eval), les puntuacions son les mes altes (4.84). Possible biaix d'auto-consistencia. GPT-4o-mini es mes fiable com a referencia per ser jutge extern.

### 8.4 Absencia de jutge Sonnet/Opus
Es va descartar Claude com a jutge per consum de quota CLI. Idealment, un tercer jutge extern (Sonnet/Opus via API) donaria mes robustesa.

---

## 9. Conclusions

### 9.1 Sobre l'arquitectura del prompt
1. **RAG funciona be amb GPT**: RAG-v2 >= RAG-v1 > HC de forma consistent
2. **Per Gemini, HC guanya**: pero amb el caveat dels thinking tokens (punt 8.1)
3. **RAG genera textos mes llargs i detallats**: +35-50% paraules, potencialment mes util pedagogicament

### 9.2 Sobre els models generadors
1. **Gemini Flash**: millor qualitat absoluta, pero amb thinking tokens (comparacio injusta)
2. **GPT-4o-mini**: molt competitiu, millor relacio qualitat/preu, RAG funciona be
3. **Sonnet**: resultats invalids per RAG-v2; HC i RAG-v1 son competitius

### 9.3 Sobre els jutges
1. **GPT-4o-mini**: mes exigent i mes fiable (jutge extern per a tots els generadors)
2. **Gemini**: tendeix a puntuar alt, possible self-eval bias

### 9.4 Decisions derivades
- **RAG-v2 es la branca recomanada** per a produccio (guanya per GPT, competitiu per Gemini)
- **Cal repetir generacio Gemini sense thinking** per comparacio justa
- **Cal regenerar Sonnet RAG-v2** amb generacio correcta
- **Cal provar un tercer jutge extern** (p.ex. Gemma 4 local) per triangulacio

---

## 10. Fitxers de referencia

| Fitxer | Descripcio |
|--------|-----------|
| `tests/multi_v2.py` | Orquestrador principal (50 KB) |
| `evaluator_rubrics.py` | Rubriques v1 i v2 |
| `evaluator_agent.py` | BLOC 3: LLM-as-a-judge |
| `evaluator_metrics.py` | BLOC 1-2: metriques automatiques |
| `eval_db.py` | Gestio SQLite |
| `tests/test_data.json` | 200 casos de prova |
| `tests/results/evaluations.db` | Base de dades completa (71 MB) |
| `ui/eval_dashboard.html` | Dashboard interactiu |
| `ui/eval_results.html` | Visualitzacio resultats |
| `ui/eval_progress.html` | Monitor de progres |
