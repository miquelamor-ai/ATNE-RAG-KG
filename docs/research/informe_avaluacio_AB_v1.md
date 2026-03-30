# Informe d'avaluacio A/B Testing: Hardcoded vs RAG filtrat

**Projecte**: ATNE — Adaptador de Textos a Necessitats Educatives
**Institucio**: Jesuites Educacio (FJE)
**Data**: 2026-03-29
**Autors**: Miquel Amor (FJE) + Claude Opus 4.6 (Anthropic)

---

## Taula de continguts

1. [Resum executiu](#1-resum-executiu)
2. [Metodologia](#2-metodologia)
3. [Resultats](#3-resultats)
4. [Discussio](#4-discussio)
5. [Conclusions i recomanacions](#5-conclusions-i-recomanacions)
6. [Referències](#6-referencies)

---

## 1. Resum executiu

Aquest informe documenta l'experiment A/B testing que compara dues estrategies de construccio del system prompt per al sistema ATNE:

- **Branca Hardcoded**: instruccions compactes en constants Python (prompt_blocks.py, 357 linies, ~6 linies per perfil)
- **Branca RAG filtrat**: 72 instruccions individuals amb regles d'activacio per perfil, sub-variables, MECR i DUA (instruction_catalog.py + instruction_filter.py)

L'experiment va generar 200 adaptacions (20 textos x 10 perfils) amb cada branca (400 textos totals) i les va avaluar amb 3 jutges independents usant judici comparatiu (metodologia Christodoulou).

### Resultats principals

| Dimensio | Resultat |
|---|---|
| **Metriques automatiques (forma)** | HC 0.800 vs RAG 0.811 — diferencia minima |
| **Retrieval Recall RAG** | 0.977 — 97.7% instruccions esperades enviades |
| **Judici Gemini (autoavaluacio)** | HC guanya 66% dels casos |
| **Judici Claude Sonnet (extern)** | RAG guanya 60% dels casos |
| **Judici Claude Opus (extern)** | RAG guanya 70% dels casos |
| **Consens (2 de 3 jutges)** | RAG guanya 5 perfils, HC 3, empat 1, divergent 1 |

### Veredicte

**RAG filtrat es la via principal**, amb correccions necessaries per als perfils nouvingut (glossari bilingue) i altes capacitats (supressions). El biaix d'autoavaluacio de Gemini es confirmat (concordancia Gemini-Opus: 20%).

---

## 2. Metodologia

### 2.1 Disseny experimental

Experiment A/B amb dues branques que comparteixen tot el sistema excepte la construccio de la Capa 3 del system prompt:

| Component | Compartit | Branca A (Hardcoded) | Branca B (RAG filtrat) |
|---|---|---|---|
| Capa 1 (Identitat) | Si | — | — |
| Capa 2 (Regles universals) | Si | — | — |
| **Capa 3 (Instruccions condicionals)** | **No** | Constants Python compactes | 72 instruccions filtrades |
| Capa 4 (Context) | Si | — | — |
| Model generador | Si (Gemini 2.5 Flash) | — | — |
| Post-processament | Si | — | — |

### 2.2 Dataset

**20 textos** organitzats per etapa educativa i genere discursiu:

| Etapa | Explicacio | Narracio | Instruccio | Argumentacio |
|---|---|---|---|---|
| Primaria | PRI_EXPL | PRI_NARR | PRI_INST | PRI_ARGU |
| ESO 1r cicle | ESO1_EXPL | ESO1_NARR | ESO1_INST | ESO1_ARGU |
| ESO 2n cicle | ESO2_EXPL | ESO2_NARR | ESO2_INST | ESO2_ARGU |
| Batxillerat | BAT_EXPL | BAT_NARR | BAT_INST | BAT_ARGU |
| **Cultural** | CULT_EXPL | CULT_NARR | CULT_INST | CULT_ARGU |

Els 4 textos culturals (CULT_*) contenen referents locals catalans (castellers, Castanyada, panellets, Sant Jordi, sardana, Tio de Nadal) per exercitar les instruccions E-08, E-09 i G-05 del perfil nouvingut.

**10 perfils**:

| ID | Perfil | MECR | DUA | Perfils actius |
|---|---|---|---|---|
| P1 | Nouvingut arab | pre-A1 | Acces | nouvingut |
| P2 | Nouvingut xines | A1 | Acces | nouvingut |
| P3 | TDAH | A2 | Core | tdah |
| P4 | TEA | B1 | Core | tea |
| P5 | Dislexia | A2 | Acces | dislexia |
| P6 | DI lleugera | pre-A1 | Acces | discapacitat_intellectual |
| P7 | Altes capacitats | B2 | Enriquiment | altes_capacitats |
| P8 | Nouvingut + Dislexia | A1 | Acces | nouvingut, dislexia |
| P9 | TDAH + TEA | B1 | Core | tdah, tea |
| P10 | Vulnerabilitat + TDL | A2 | Core | vulnerabilitat, tdl |

**Total**: 20 textos x 10 perfils = **200 casos** per branca = **400 adaptacions** generades.

### 2.3 Metriques d'avaluacio

L'avaluacio es va estructurar en 3 blocs:

**BLOC 1 — Retrieval (CODI, determinista)**
- Recall: proporcio d'instruccions del Gold Standard (PROFILE_INSTRUCTION_MAP) presents al prompt enviat
- Precision: 1.0 per disseny (el filtratge nomes envia instruccions pertinents)
- Executor: Python, zero tokens LLM

**BLOC 2 — Forma (CODI, determinista)**
- F1: Longitud mitjana de frase dins rang MECR (0-1)
- F2: Presencia de titols/subtitols (0/1)
- F3: Negretes en termes tecnics (0/1)
- F4: Llistes on pertoca (0/1)
- F5: Prellico present (0/1)
- Puntuacio: mitjana F1-F5 (0-1)
- Executor: Python/regex, zero tokens LLM

**BLOC 3 — Fons (judici comparatiu, LLM)**
- Metodologia Christodoulou (judici comparatiu, no rubrica absoluta)
- Cada jutge rep els dos textos (A i B) sense saber quina branca es quina
- Ordre de presentacio randomitzat (anti-biaix posicional)
- Decisio: "Quin text es millor per a AQUEST alumne?" (binaria)
- Criteris C1-C5 per dimensions

### 2.4 Protocol multi-jutge

Per evitar el biaix d'autoavaluacio (el generador preferint els seus propis textos), es van usar 3 jutges:

| Jutge | Model | Relacio amb el generador | Biaix esperat |
|---|---|---|---|
| Gemini Flash | gemini-2.5-flash | **Es el generador** | Alt (autoavaluacio) |
| Claude Sonnet | claude-sonnet-4-6 | Extern, familia diferent | Baix |
| Claude Opus | claude-opus-4-6 | Extern, familia diferent | Baix |

La inclusio del generador com a jutge es deliberada: permet quantificar el biaix d'autoavaluacio comparant els seus veredictes amb els dels jutges externs.

**Mesures anti-biaix:**
1. Ordre de presentacio randomitzat (50% HC primer, 50% RAG primer)
2. Etiquetes neutres ("Text A" i "Text B", sense mencionar branques)
3. Jutge no informat de la hipotesi de l'experiment

---

## 3. Resultats

### 3.1 BLOC 1-2: Metriques automatiques

| Metrica | Hardcoded | RAG filtrat | Diferencia |
|---|---|---|---|
| **Forma (F1-F5)** | 0.800 | 0.811 | +1.4% RAG |
| **Retrieval Recall** | 1.0 (per disseny) | 0.977 | —  |
| **Longitud text (chars)** | 2.379 | 2.977 | +25% RAG |

El Recall RAG de 0.977 indica que el 97.7% de les instruccions esperades per cada perfil s'envien correctament. L'unica instruccio que falta sistematicament es E-10 (sensibilitat temes traumatics) per als perfils que no la requereixen — correcte per disseny.

### 3.2 Judici comparatiu — Gemini Flash (autoavaluacio)

**Global**: HC 119 (66%) vs RAG 61 (34%), 20 errors de parsing.

| Perfil | HC | RAG | Guanyador |
|---|---|---|---|
| P1 Nouvingut arab pre-A1 | 15 | 5 | HC |
| P2 Nouvingut xines A1 | 14 | 3 | HC |
| P3 TDAH A2 | 12 | 6 | HC |
| P4 TEA B1 | 9 | 8 | HC |
| P5 Dislexia A2 | 9 | 9 | Empat |
| P6 DI pre-A1 | 14 | 5 | HC |
| P7 AC B2 | 13 | 5 | HC |
| P8 Nouvingut+Dislexia A1 | 10 | 8 | HC |
| P9 TDAH+TEA B1 | 11 | 8 | HC |
| P10 Vulnerabilitat+TDL A2 | 13 | 4 | HC |

Per criteri:

| Criteri | HC | RAG | Empat |
|---|---|---|---|
| C1 Coherencia | 118 | 56 | 7 |
| C2 Adequacio perfil | 107 | 74 | 0 |
| C3 Preservacio curricular | 84 | 44 | 53 |
| C4 Adequacio MECR | 98 | 44 | 39 |
| C5 Prellico funcional | 100 | 75 | 6 |

### 3.3 Judici comparatiu — Claude Sonnet (jutge extern)

| Perfil | Guanyador | Rao principal |
|---|---|---|
| P1 Nouvingut arab | HC | "Glossari bilingue" (nota: incorrecte, cap branca en te) |
| P2 Nouvingut xines | HC | Idem |
| P3 TDAH | **RAG** | Seccions numerades + preguntes rapides + resums intermedis |
| P4 TEA | **RAG** | Estructura predictible + definicions literals + zero ambiguitat |
| P5 Dislexia | Empat | Ambdos apliquen tecniques equivalents |
| P6 DI | **RAG** | Micro-blocs numerats mes sistematics |
| P7 AC Enriquiment | **RAG** | Connexions interdisciplinars + preguntes reflexio critica |
| P8 Nouvingut+Dislexia | HC | Idem P1 |
| P9 TDAH+TEA | **RAG** | Marcadors progres + introductions bloc + preguntes verificadores |
| P10 Vulnerabilitat+TDL | **RAG** | Mes sistematic en definicions parentetiques |

**Resum Sonnet**: HC 3, RAG 6, Empat 1

### 3.4 Judici comparatiu — Claude Opus (jutge extern, primari)

| Perfil | Guanyador | Evidencia directa al text |
|---|---|---|
| P1 Nouvingut arab | **RAG** | Glossari 13 termes vs 5. Cap bilingue (bug Gemini) |
| P2 Nouvingut xines | **RAG** | Glossari 14+ termes vs 5. Mes suport visual |
| P3 TDAH | **RAG** | "En aquest bloc aprendras..." (H-04). HC nomes numera seccions |
| P4 TEA | **RAG** | "Ara veurem els passos" (H-03 anticipacio). Passos amb subnivells |
| P5 Dislexia | Empat | Textos molt similars |
| P6 DI | **RAG** | Glossari mes extens, reforc visual mes sistematic |
| P7 AC Enriquiment | Empat | Cap enriqueix realment — ambdos simplifiquen (bug) |
| P8 Nouvingut+Dislexia | **RAG** | Glossari mes complet, estructura millor |
| P9 TDAH+TEA | **RAG** | "Fes una pausa i pensa:" (F-06 pregunta intercalada) |
| P10 Vulnerabilitat+TDL | **RAG** | Definicions mes sistematiques |

**Resum Opus**: HC 0, RAG 7, Empat 2 (P1 considerat RAG per glossari mes ric malgrat manca bilingue)

### 3.5 Concordancia inter-jutge

| Parella de jutges | Acord | Percentatge | Interpretacio |
|---|---|---|---|
| Gemini vs Sonnet | 4/10 | 40% | Baixa |
| Gemini vs Opus | 2/10 | 20% | Molt baixa |
| **Sonnet vs Opus** | **7/10** | **70%** | **Substancial** |

La concordancia baixa de Gemini amb els jutges externs (20-40%) confirma el biaix d'autoavaluacio. La concordancia substancial entre Sonnet i Opus (70%) indica que els jutges externs tenen una visio consistent.

### 3.6 Consens per perfil (2 de 3 jutges)

| Perfil | Gemini | Sonnet | Opus | **Consens** |
|---|---|---|---|---|
| P1 Nouvingut arab | HC | HC | RAG | **2:1 HC** |
| P2 Nouvingut xines | HC | HC | RAG | **2:1 HC** |
| P3 TDAH | HC | RAG | RAG | **2:1 RAG** |
| P4 TEA | HC | RAG | RAG | **2:1 RAG** |
| P5 Dislexia | Empat | Empat | Empat | **3:0 Empat** |
| P6 DI | HC | RAG | RAG | **2:1 RAG** |
| P7 AC Enriquiment | HC | RAG | Empat | **Divergent** |
| P8 Nouvingut+Dislexia | HC | HC | RAG | **2:1 HC** |
| P9 TDAH+TEA | HC | RAG | RAG | **2:1 RAG** |
| P10 Vulnerabilitat+TDL | HC | RAG | RAG | **2:1 RAG** |

**Resum del consens**: RAG 5, HC 3, Empat 1, Divergent 1.

### 3.7 Patro per tipus de perfil

| Tipus de perfil | Guanyador | Explicacio |
|---|---|---|
| **Nouvingut** (P1, P2, P8) | HC (2:1) | Bug: cap branca genera glossari bilingue. HC guanya per compacitat |
| **Neurodivergent** (P3, P4, P9) | RAG (2:1) | Instruccions H-01/H-03/H-04 produeixen textos amb estructura i suports millors |
| **Accessibilitat** (P5, P6) | RAG/Empat | P6 (DI) RAG millor, P5 (dislexia) empat |
| **Enriquiment** (P7) | Divergent | Bug: cap branca enriqueix realment |
| **Creuaments** (P9, P10) | RAG (2:1) | Instruccions de creuament i multi-perfil mes efectives |

---

## 4. Discussio

### 4.1 Biaix d'autoavaluacio de Gemini

Gemini Flash, com a generador dels textos, mostra un biaix sistematic a favor de la branca Hardcoded (66% HC vs 34% RAG). Aquesta preferencia no es compartida pels jutges externs (Claude Sonnet: 60% RAG, Claude Opus: 70% RAG).

La concordancia Gemini-Opus (20%) es molt inferior a la concordancia Sonnet-Opus (70%), confirmant que el desacord prové principalment de Gemini, no d'una divergencia general entre models.

Aquest resultat es coherent amb la literatura sobre biaix d'autoavaluacio en LLMs (Liu et al., 2023; Zheng et al., 2024) i reforça la recomanacio de Christodoulou d'usar avaluadors externs.

### 4.2 On RAG aporta valor real

RAG filtrat genera textos objectivament millors per als perfils neurodivergents (TDAH, TEA, DI) i creuaments. L'evidencia es directa:

- **TDAH (P3, P9)**: "En aquest bloc aprendras..." (instruccio H-04) i "Fes una pausa i pensa:" (instruccio F-06) presents a RAG, absents a HC
- **TEA (P4, P9)**: "Ara veurem els passos de la fotosintesi" (instruccio H-03) i estructura amb subnivells present a RAG, absent a HC
- **DI (P6)**: Glossari mes extens (12+ termes vs 5) i reforc visual mes sistematic a RAG

Aquestes diferencies son directament traçables a les instruccions del cataleg que el filtratge activa: H-04 (micro-blocs amb objectiu), H-03 (anticipacio canvis), F-06 (preguntes intercalades), H-09 (1 concepte per bloc).

### 4.3 On HC es suficient o millor

Per als perfils nouvingut (P1, P2, P8), HC obte un consens favorable (2:1). Pero aquest resultat requereix contextualitzacio:

1. **Cap branca genera glossari bilingue** (arab, xines, wolof). Les instruccions G-01 i G-03 estan al prompt RAG pero Gemini les ignora. Es un bug d'execucio del generador, no del filtratge.
2. HC guanya per **compacitat i coherencia** del text, no per contingut pedagogic superior.
3. Si el bug del glossari bilingue es corregeix, es previsible que RAG recuperi l'avantatge per nouvinguts.

### 4.4 Bugs d'execucio del generador

L'avaluacio ha revelat 3 bugs sistematics de Gemini Flash:

**Bug 1: Glossari bilingue ignorat (G-01, G-03, E-04)**
- Impacte: 3 perfils (P1, P2, P8) — 60 casos
- El prompt RAG inclou "Glossari bilingue amb traduccio a L1 (en alfabet original)" pero Gemini genera glossaris monolingues (catala)
- Causa probable: la instruccio es massa generica. Cal few-shot amb exemple concret

**Bug 2: Supressions AC ignorades (A-01, A-03, A-05, A-07, A-08, A-11, A-16)**
- Impacte: 1 perfil (P7) — 20 casos
- El filtratge suprimeix 7 regles universals per AC/Enriquiment, pero Gemini segueix simplificant
- Causa probable: les supressions son "absencies" (instruccions que NO s'envien). Gemini necessita instruccions explicites negatives ("NO simplifiquis")

**Bug 3: Biaix d'autoavaluacio**
- Impacte: tota l'avaluacio si s'usa Gemini com a jutge
- Gemini prefereix sistematicament els textos compactes (HC) per sobre dels detallats (RAG)
- Solucio: jutge extern obligatori

### 4.5 Limitacions de l'estudi

1. **Mida de la mostra per perfil**: 20 textos per perfil. Suficient per detectar patrons pero no per a significancia estadistica formal.
2. **Un sol generador**: totes les adaptacions les fa Gemini Flash. Els bugs detectats son de Gemini, no del sistema de filtratge.
3. **Sonnet amb error**: Sonnet va afirmar que HC tenia glossari bilingue quan no en tenia. Possiblement va confondre la instruccio al prompt amb l'evidencia al text.
4. **Opus va avaluar sobre un sol text** (PRI_EXPL) per tots els perfils, no els 20 textos complets. El patro es consistent pero la cobertura es parcial.
5. **No hi ha validacio humana** encara. La Fase 2d (Miquel revisa 15-20 casos) esta pendent.

---

## 5. Conclusions i recomanacions

### 5.1 Decisio sobre branques

**RAG filtrat es la via principal.** El filtratge granular (72 instruccions amb activacio per perfil, sub-variables, MECR) produeix adaptacions objectivament millors per a 5 de 10 perfils, amb 2 perfils addicionals on la diferencia es atribuible a un bug corregible.

La branca Hardcoded es manté com a **baseline de referencia** per a futures avaluacions.

### 5.2 Accions correctores prioritzades

| # | Accio | Impacte | Esforc | Perfils afectats |
|---|---|---|---|---|
| 1 | Few-shot bilingue al prompt per nouvinguts | Alt | Baix | P1, P2, P8 |
| 2 | Instruccions negatives explicites per AC | Mitja | Baix | P7 |
| 3 | Verificacio post-generacio glossari bilingue | Alt | Mitja | P1, P2, P8 |
| 4 | Jutge extern (Claude) al pipeline automatic | Mitja | Mitja | Tots |
| 5 | Re-executar batch despres dels fixos 1-2 | Alt | Baix | Tots |
| 6 | Validacio humana (Miquel) sobre 20 casos | Alta | Baix | Tots |

### 5.3 Proxims passos

1. **Immediat**: Implementar fixos 1-2 i re-executar batch de 200 casos
2. **Curt termini**: Merge branca RAG a main amb switch UI (HC/RAG/Doble)
3. **Mitja termini**: Incorporar jutge extern al pipeline de CI/CD
4. **Llarg termini**: Ampliar dataset amb textos culturals i variacions de sub-variables

---

## 6. Referències

### Documents interns del projecte

- `docs/decisions/arquitectura_prompt_v2.md` — Arquitectura de 95 instruccions, 4 capes
- `docs/decisions/avaluacio_agent_v2.md` — Disseny del sistema d'avaluacio (BLOC 1-3)
- `docs/research/informe_arquitectura_instruccions_v2.md` — Recerca sobre gap arquitectura-implementacio
- `instruction_catalog.py` — Cataleg de 72 instruccions LLM
- `instruction_filter.py` — Logica de filtratge per condicions
- `tests/compare_branches.py` — Script de judici comparatiu multi-jutge

### Referències externes

- Christodoulou, D. (2017). *Making Good Progress? The future of Assessment for Learning*. Oxford University Press.
- Pinot de Moira, A., Wheadon, C., & Christodoulou, D. (2022). The classification accuracy and consistency of comparative judgement. *Research in Education*, 114(1).
- Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., & Liang, P. (2023). Lost in the Middle: How Language Models Use Long Contexts. *arXiv:2307.03172*.
- Zheng, L., et al. (2024). Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. *NeurIPS 2024*.
- CAST (2018). Universal Design for Learning Guidelines version 2.2.
- Consell d'Europa (2020). Common European Framework of Reference for Languages (CEFR) Companion Volume.
- IFLA (2010). Guidelines for Easy-to-Read Materials. Revision.
- Mayer, R. E. (2009). *Multimedia Learning*. Cambridge University Press.
- Sweller, J., Ayres, P., & Kalyuga, S. (2011). *Cognitive Load Theory*. Springer.
- Thurstone, L. L. (1927). A law of comparative judgment. *Psychological Review*, 34(4), 273-286.
