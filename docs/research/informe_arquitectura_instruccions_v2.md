# Informe de recerca: Arquitectura d'instruccions per a l'adaptacio de textos educatius amb LLM

**Projecte**: ATNE -- Adaptador de Textos a Necessitats Educatives
**Institucio**: Jesuites Educacio (FJE)
**Data**: 2026-03-29
**Autors**: Miquel Amor (Jesuites Educacio / FJE) amb suport de Claude Opus 4.6 (Anthropic)

---

## Taula de continguts

1. [Resum executiu](#1-resum-executiu)
2. [Metodologia de la investigacio](#2-metodologia-de-la-investigacio)
3. [Comparativa de dues vies d'implementacio](#3-comparativa-de-dues-vies-dimplementacio)
4. [Analisi del gap: arquitectura vs implementacio](#4-analisi-del-gap-arquitectura-vs-implementacio)
5. [Sensibilitat de l'LLM a la granularitat d'instruccions](#5-sensibilitat-de-lllm-a-la-granularitat-dinstruccions)
6. [Disseny experimental proposat](#6-disseny-experimental-proposat)
7. [Conclusions i proxims passos](#7-conclusions-i-proxims-passos)
8. [Referències](#8-referencies)

---

## 1. Resum executiu

ATNE es un assistent d'intel-ligencia artificial dissenyat per adaptar textos educatius a les necessitats diverses de l'alumnat: nouvinguts, alumnat amb necessitats especifiques de suport educatiu (NESE), disseny universal per a l'aprenentatge (DUA) i altes capacitats. El sistema funciona amb Gemini 2.5 Flash com a model de llenguatge (LLM), un backend FastAPI en Python, i un corpus pedagogic indexat amb cerca vectorial (RAG) i graf de coneixement (KG) a Supabase.

Aquesta recerca documenta el proces complet de redisseny del sistema d'instruccions que guia l'LLM en la transformacio de textos. El treball es va estructurar en tres fases:

1. **Investigacio fonamental** (2026-03-27): Triangulacio de 6 documents de recerca generats per 4 agents Claude Opus i 2 documents d'un model alternatiu, que van produir un banc exhaustiu de 119 instruccions, una taxonomia de 70+ variables, un mapa de barreres per a 13 perfils d'alumnat, i una analisi de capacitats i limits dels LLM actuals.

2. **Sintesi i arquitectura** (2026-03-27): Consolidacio de les fonts en un cataleg desduplicat de 95 instruccions classificades per executor (LLM/codi/frontend), activacio (sempre/perfil/nivell/complement) i prioritat (P0-P3). Disseny d'una arquitectura de prompt en 4 capes: identitat fixa, instruccions universals, instruccions condicionals i context variable.

3. **Implementacio i avaluacio comparativa** (2026-03-28): Construccio de dues branques alternatives (RAG-KG i hardcoded) i execucio d'un batch test de 160 casos (16 textos reals x 10 perfils) per mesurar diferencies en riquesa, velocitat i adherencia.

Les troballes principals son:

- El cataleg de 95 instruccions es robust i te fonament teoric solid (DUA/CAST, MECR, Lectura Facil, Halliday, Sweller, Vygotsky, Mayer, Dehaene).
- La branca RAG genera adaptacions 3 vegades mes riques en contingut i 2 vegades mes rapides que la branca hardcoded.
- Ambdues branques comparteixen un gap fonamental: l'arquitectura defineix 95 instruccions amb regles d'activacio granulars, pero la implementacio col-lapsa tot en ~10 blocs monolitics.
- La combinatoria real per cas varia entre ~28 instruccions (cas simple) i ~50 instruccions (cas extrem), superant el llindar de fiabilitat de Gemini Flash (40-50 regles simultanees).
- Cal un agent avaluador (LLM-as-a-judge) per mesurar si la granularitat millora el resultat real, no nomes la quantitat de text generat.

---

## 2. Metodologia de la investigacio

### 2.1 Disseny de la recerca

La recerca va seguir una metodologia de **triangulacio per convergencia**: multiples agents d'IA van investigar independentment els mateixos eixos, i despres es van creuar les conclusions per identificar convergencies (alta fiabilitat), divergencies (requereixen decisio) i buits (requereixen recerca addicional).

Es van definir 4 eixos de recerca, cadascun amb un o dos agents independents:

| Eix | Agent(s) | Document(s) resultant(s) | Fonts primaries |
|---|---|---|---|
| **A1: Instruccions d'adaptacio** | Claude Opus + model alternatiu | `banc_exhaustiu_instruccions_adaptacio.md` (119 instr.) + `ext_taxonomia_adaptacio_A1.md` (70+ vars.) | CAST/UDL, IFLA, UNE 153101, MECR-CV, WCAG 2.2, Plain Language, Clarity Int. |
| **A2: Marcs teorics** | Claude Opus | `investigacio_marcs_teorics_ATNE.md` | Sweller (CLT), Paivio, Vygotsky, Mayer, Dehaene/Wolf, Halliday (LSF), Graves (SRE), Bloom |
| **B: Barreres per perfil** | Claude Opus | `mapa_barreres_perfil.md` | DSM-5-TR, CIE-11, ICF (OMS), Index for Inclusion, Decret 150/2017 |
| **C: Capacitats i limits LLM** | Claude Opus + model alternatiu | `analisi_capacitats_llm_adaptacio.md` + `ext_modelabilitat_llm_C.md` | Benchmarks dels models, documentacio API, literatura "lost in the middle" |

### 2.2 Triangulacio i consolidacio

El document de sintesi (`docs/decisions/arquitectura_prompt_v2.md`, 951 linies) va creuar sistematicament les troballes dels 6 documents per identificar:

**Convergencies de tots els documents** (seccio 2 de l'arquitectura):
- Les variables linguistiques (longitud frase, complexitat sintactica, frequencia lexica) son les mes rendibles i controlables per l'LLM.
- Halliday (linguistica sistemica funcional) es la llacuna mes important del marc actual: cap dels 4 pilars (DUA, LF, MECR, WCAG) dona un model linguistic de COM funciona un text.
- Cada perfil te una barrera nuclear diferent (TEA: inferencia, TDAH: atencio, dislexia: decodificacio, nouvingut: lexic+cultural).
- 7-12 instruccions simultanees es el rang d'alta fiabilitat per als LLM; per sobre de 20, hi ha degradacio notable.

**Divergencies significatives** (seccio 3):
- Quantitat optima d'instruccions: entre 5-8 (model conservador) i 7-12 (model estendard). Decisio: adoptar 5-8 fixes + 3-5 condicionals = max 13 al prompt.
- Necessitat de canvi de model: l'analisi critica detecta que la funcio `clean_gemini_output()` de 40+ linies al codi es prova directa que Gemini Flash no segueix be les instruccions de format.

**Buits identificats** (seccio 4): 10 llacunes, entre les quals destaquen l'absencia de regles per genere discursiu, la manca de metriques de llegibilitat validades per al catala, i la inexistencia d'evidencia empirica sobre l'impacte real de les adaptacions.

### 2.3 Proces de deduplicacio

Les 119 instruccions del Banc Exhaustiu i les 70+ variables de la Taxonomia A1 es van fusionar mitjancant un proces sistematic:

1. **Alineament semantic**: cada variable A1 (p.ex. `TXT_SENT_LEN`) es va aparellar amb la instruccio equivalent del Banc (p.ex. A2.01 "Frase curta").
2. **Eliminacio de duplicats**: instruccions que descrivien la mateixa operacio amb diferent formulacio es van unificar (p.ex. "simplificar vocabulari" i "usar vocabulari frequent" van esdevenir A-01).
3. **Classificacio triple**: cada instruccio resultant va rebre tres etiquetes:
   - **Executor**: LLM (l'LLM ho fa al prompt), CODI (el backend Python ho fa), FE (CSS/frontend ho fa)
   - **Activacio**: SEMPRE (tota adaptacio), PERFIL (segons perfil alumne), NIVELL (segons MECR), COMPLEMENT (si s'activa)
   - **Prioritat**: P0 (ja implementat), P1 (fer immediatament), P2 (fase seguent), P3 (futur)

El resultat final: **95 instruccions uniques** distribuides en 10 categories (A-J).

### 2.4 Estructura del cataleg resultant

| Categoria | Nom | Instruccions | LLM | CODI | FE |
|---|---|---|---|---|---|
| A | Adaptacio linguistica | 26 | 26 | 0 | 0 |
| B | Estructura i organitzacio | 14 | 14 | 0 | 0 |
| C | Suport cognitiu | 9 | 9 | 0 | 0 |
| D | Multimodalitat | 9 | 7 | 1 | 1 |
| E | Contingut curricular | 12 | 11 | 0 | 1 |
| F | Avaluacio i comprensio | 10 | 10 | 0 | 0 |
| G | Personalitzacio linguistica | 6 | 5 | 1 | 0 |
| H | Adaptacions per perfil | 20 | 18 | 0 | 2 |
| I | Presentacio i layout | 8 | 0 | 0 | 8 |
| J | Verificacio i post-processament | 7 | 1 | 6 | 0 |
| **Total** | | **95** (sense duplicats) | **72** | **12** | **11** |

Les 72 instruccions per a l'LLM son les que es tradueixen directament en linies del system prompt. Les 12 de CODI son verificacions post-generacio (Python). Les 11 de FE son millores de presentacio (CSS).

---

## 3. Comparativa de dues vies d'implementacio

Un cop definida l'arquitectura de 95 instruccions, calia decidir on resideix el coneixement que alimenta el prompt: als fitxers del corpus pedagogic (via RAG) o a constants Python al codi (hardcoded). Es van construir dues branques git per comparar-les experimentalment.

### 3.1 Branca RAG-KG (`prompt-v2-rag`)

**Principi**: Les instruccions d'adaptacio resideixen als fitxers Markdown del corpus FJE, organitzats en moduls temaics (M0-M9). Cada fitxer conte seccions numerades; les seccions &sect;6 contenen les instruccions d'adaptacio especifiques per a cada tema.

**Mecanisme**: Un modul `corpus_reader.py` llegeix els fitxers MD, extreu les seccions rellevants (regles universals, blocs MECR, blocs DUA, blocs per perfil, few-shot, creuaments) i les cacheja en memoria. La funcio `build_system_prompt()` crida `corpus_reader.get_*()` per recuperar els blocs que corresponen al cas concret.

**Avantatges**:
- Les instruccions son riques i detallades (els fitxers MD contenen context, justificacio i exemples).
- El coneixement es actualitzable sense tocar el codi (editar un fitxer MD).
- La cerca vectorial pot recuperar context pedagogic complementari.

**Desavantatges**:
- Depende de la qualitat i estructura dels fitxers MD.
- El parsing de seccions es fragil (canvis de format poden trencar l'extraccio).

### 3.2 Branca Hardcoded (`prompt-v2-hardcoded`)

**Principi**: Les instruccions d'adaptacio resideixen a `prompt_blocks.py`, un fitxer Python de 357 linies amb constants de text organitzades en 10 blocs.

**Mecanisme**: La funcio `build_system_prompt()` importa directament els blocs des de `prompt_blocks.py` i els concatena segons la logica condicional de les 4 capes.

**Blocs implementats**:

| Bloc | Contingut | Seleccio |
|---|---|---|
| `IDENTITY_BLOCK` | Rol, objectiu, restriccions absolutes | Fix (sempre) |
| `UNIVERSAL_RULES_BLOCK` | 15 regles universals (lexic, sintaxi, estructura, cohesio, qualitat) | Fix (sempre) |
| `MECR_BLOCKS` | 1 bloc per nivell (pre-A1, A1, A2, B1, B2) | 1 seleccionat segons `mecr_sortida` |
| `DUA_BLOCKS` | Acces / Core / Enriquiment | 1 seleccionat segons `tipus_dua` |
| `GENRE_BLOCKS` | Explicacio, narracio, instruccio, argumentacio | 0-1 seleccionat |
| `PROFILE_BLOCKS` | 12 perfils (nouvingut, TEA, TDAH, dislexia, TDL, DI, visual, auditiva, AC, 2e, vulnerabilitat, emocional) | 0-N seleccionats |
| `CROSSING_BLOCKS` | 8 creuaments entre perfils/condicions | 0-N condicionals |
| `FEWSHOT_EXAMPLES` | 1 mini-exemple per nivell MECR | 1 seleccionat |
| `COGNITIVE_LOAD_BLOCK` | Regles de carrega cognitiva per nivell | 1 seleccionat |
| `CONFLICT_RESOLUTION_BLOCK` | Jerarquia MECR > DUA > LF | Condicional |

**Avantatges**:
- Control total sobre el contingut exacte del prompt.
- Sense dependencia de fitxers externs.
- Compacte: les instruccions son concises (sense context ni justificacio).

**Desavantatges**:
- Qualsevol canvi requereix editar codi Python.
- Les instruccions compactes perden matisos.

### 3.3 Disseny del batch test

Per comparar les dues branques, es va construir un test harness sintetic amb:

- **16 textos reals en catala**: extrets de fonts educatives reals (Generalitat, XTEC, Savia MENT, Raco de contes, 3Cat, Diari Ara), cobrint:
  - 4 generes discursius: explicacio, narracio, instruccio, argumentacio
  - 4 etapes educatives: Primaria CS, ESO 1-2, ESO 3-4, Batxillerat
- **10 perfils d'adaptacio**: 7 perfils simples (nouvingut A1, TDAH B1, dislexia A2, TEA B1, DI pre-A1, AC B2, vulnerabilitat A2) + 3 creuaments (nouvingut+dislexia, TEA+AC, TDAH+nouvingut)
- **Total**: 160 combinacions (16 x 10)

Cada cas va cridar la funcio `run_adaptation()` directament (sense servidor HTTP) i va recollir:
- Text adaptat complet
- System prompt generat
- Metriques automatiques: nombre de paraules, negretes, encapcalaments, warnings del post-processament, temps d'execucio

### 3.4 Resultats quantitatius

| Metrica | RAG-KG | Hardcoded | Ratio |
|---|---|---|---|
| Casos completats | 160/160 (100%) | 160/160 (100%) | Empat |
| Paraules per cas (mitjana) | **769** | 248 | RAG 3.1x |
| Negretes per cas (mitjana) | **26.5** | 8.5 | RAG 3.1x |
| Temps per cas (mitjana) | **15.0s** | 27.5s | RAG 1.8x mes rapid |
| Warnings per cas (mitjana) | 1.6 | **1.2** | HC lleugerament millor |
| Errors | 0 | 0 | Empat |

### 3.5 Interpretacio dels resultats

**RAG genera adaptacions mes riques**: Les instruccions que l'LLM rep del corpus RAG son mes detallades perque els fitxers MD contenen context, justificacio i exemples. Aixo es tradueix en adaptacions amb mes scaffolding pedagogic (negretes per a termes tecnics amb definicio, glossaris mes complets, transicions entre seccions).

**RAG es mes rapid**: Paradoxalment, tot i generar mes text, RAG es 1.8x mes rapid. La hipotesi es que un prompt mes clar i coherent redueix el temps de "thinking" del model (Gemini 2.5 Flash utilitza un budget de raonament intern). Instruccions compactes i ambigues forcen el model a "pensar mes" per desambiguar.

**Hardcoded genera textos massa curts per perfils extrems**: En casos com DI (discapacitat intel-lectual) o nouvingut+dislexia, la branca hardcoded genera nomes 95-107 paraules, insuficient per a una adaptacio completa. La branca RAG manteeix 400-600 paraules en aquests mateixos perfils.

**Ambdues branques tenen 0 errors**: Cap de les 320 adaptacions (160 + 160) va fallar. Aixo indica que l'arquitectura de 4 capes es estable independentment de la font de les instruccions.

**Limitacio critica**: Aquestes metriques mesuren **forma** (quantitat, velocitat, format). No mesuren **fons** (fidelitat al perfil, rigor curricular, adequacio pedagogica). Sense metriques de fons, la conclusio "RAG es millor" es prematura.

---

## 4. Analisi del gap: arquitectura vs implementacio

### 4.1 El problema monolitic

L'arquitectura dissenyada (seccions 6-8 de `arquitectura_prompt_v2.md`) defineix un sistema granular:

- 95 instruccions individuals amb ID unic (A-01 a J-07)
- Regles d'activacio per a cadascuna (SEMPRE, PERFIL, NIVELL, COMPLEMENT)
- Mapa explicit de quines instruccions s'activen per a cada un dels 13 perfils
- Jerarquia de resolucio de conflictes (MECR > DUA > LF)

La implementacio real (tant a `prompt_blocks.py` com a `corpus_reader.py`) col-lapsa aquesta granularitat en aproximadament 10 blocs monolitics. Per exemple:

| Arquitectura (paper) | Implementacio (codi) |
|---|---|
| 26 instruccions linguistiques (A-01 a A-26), cadascuna amb activacio propia | 1 bloc `UNIVERSAL_RULES_BLOCK` amb 15 regles sempre actives |
| 20 instruccions per perfil (H-01 a H-20), distribuides en 13 perfils | 12 blocs `PROFILE_BLOCKS`, cada bloc amb 3-5 regles fixes |
| 8 creuaments condicionals | 8 linies al `CROSSING_BLOCKS`, activades per presencia de perfils |

El resultat: les sub-variables dels perfils (L1, alfabet llati, escolaritzacio previa, temps a Catalunya, context familiar) alimenten la narrativa `persona-audience` pero **no seleccionen instruccions especifiques**. Un nouvingut marroqui amb alfabet arabic i escolaritzacio parcial rep exactament el mateix bloc d'instruccions que un nouvingut ucranies amb alfabet llati i escolaritzacio completa. La diferencia nomes apareix a la narrativa en prosa que descriu l'alumne.

### 4.2 Les 38 instruccions condicionades per perfil

Del cataleg de 95 instruccions, 38 tenen activacio `PERFIL` (es a dir, nomes s'envien si un perfil concret esta actiu). La distribucio per categoria i executor es:

| Categoria | Instruccions PERFIL | Executor LLM | Executor CODI/FE |
|---|---|---|---|
| A (Linguistica) | 1 (A-21: descomposicio paraules compostes) | 1 | 0 |
| B (Estructura) | 1 (B-13: indicadors de progres) | 1 | 0 |
| D (Multimodalitat) | 2 (D-06, D-07) | 2 | 0 |
| E (Contingut) | 4 (E-08, E-09, E-10, E-11) | 4 | 0 |
| F (Avaluacio) | 2 (F-06, F-09) | 2 | 0 |
| G (Personalitzacio) | 4 (G-01, G-02, G-03, G-05) | 3 | 1 |
| H (Per perfil) | 20 (H-01 a H-20) | 18 | 2 |
| I (Presentacio) | 4 (I-01 a I-05) | 0 | 4 |
| **Total** | **38** | **31** | **7** |

De les 38, **31 van a l'LLM** (son instruccions de prompt) i **7 son CODI/FE** (CSS, disclaimers). La variacio per sub-variables dins d'un perfil es moderada: un nouvingut amb alfabet no llati activa ~4 instruccions extra (G-03 transliteracio, disclaimer L1, generes academics, traduccio consignes) respecte un nouvingut amb alfabet llati.

### 4.3 Contradiccions entre instruccions fixes i perfil

L'analisi ha identificat **5 contradiccions** entre instruccions classificades com a SEMPRE i necessitats de perfils especifics:

| ID | Instruccio SEMPRE | Perfil en conflicte | Naturalesa del conflicte |
|---|---|---|---|
| A-03 | "No sinonims: un terme = un concepte" | Altes Capacitats | L'AC necessita riquesa lexica i variacio estilistica. Repetir "riu Ebre" 5 vegades empobreix un text d'enriquiment. |
| A-07 | "Una idea per frase" | AC / B2 | Textos de nivell B2 o d'enriquiment requereixen frases compostes amb relacions causals, temporals i concessives. |
| A-11 | "Puntuacio simplificada (punts i dos punts)" | Enriquiment | L'escriptura academica requereix punt i coma, guions i parentesis. Eliminar-los empobreix el model linguistic. |
| A-05 | "Eliminar expressions idiomatiques" | AC / Enriquiment | Les expressions idiomatiques son part del registre culte. Eliminar-les empobreix l'aprenentatge per a AC. |
| A-08 | "Veu activa obligatoria" | B2 / Textos cientifics | La veu passiva es convencional en textos cientifics ("l'experiment va ser realitzat..."). Forcar veu activa pot requerir inventar un subjecte. |

La jerarquia definida (MECR > DUA > LF) resol parcialment els conflictes 2, 3 i 5 (un nivell MECR alt relaxa les restriccions de LF). Pero **no resol** els conflictes 1 i 4, que depenen del perfil (AC) mes que del nivell linguistic.

**Proposta de resolucio**: Reclassificar A-03, A-05, A-07, A-08 i A-11 com a instruccions amb **excepcio per perfil**: SEMPRE *excepte* quan el perfil sigui AC o el nivell DUA sigui Enriquiment. Aixo requereix afegir una capa de logica al `build_system_prompt()`.

### 4.4 Implicacions per al disseny

El gap arquitectura-implementacio no es un error: es una decisio implicita de **simplificacio per viabilitat**. Implementar les 95 instruccions amb activacio granular individual requereix un motor de regles complex. La pregunta que cal respondre empiricament es: **la granularitat produeix una diferencia mesurable en la qualitat de l'adaptacio?**

Si la resposta es "si, mesurablement", cal invertir en el motor de regles.
Si la resposta es "no, l'LLM fa basicament el mateix", els 10 blocs monolitics son suficients.

Aquesta es la pregunta central del disseny experimental proposat a la seccio 6.

---

## 5. Sensibilitat de l'LLM a la granularitat d'instruccions

### 5.1 Combinatoria real per cas

El nombre d'instruccions que arriben a l'LLM varia significativament segons la complexitat del cas:

**Cas simple** (1 perfil, nivell mitjao, sense complements):
- Capa 1 (identitat): 4 instruccions fixes
- Capa 2 (universals): 15 instruccions fixes
- Capa 3 (condicionals): 1 bloc MECR (~5 instr.) + 1 bloc DUA (~3 instr.) + 1 bloc perfil (~4 instr.) + 0 creuaments + 1 few-shot
- **Total: ~28 instruccions**

**Cas complex** (2-3 perfils, nivell baix, amb complements):
- Capa 1: 4
- Capa 2: 15
- Capa 3: 1 MECR + 1 DUA + 1 genere (~4) + 2-3 perfils (~12) + 1-2 creuaments (~2) + 1 carrega cognitiva (~3) + 1 conflicte (~3) + 1 few-shot
- **Total: ~43 instruccions**

**Cas extrem** (nouvingut + dislexia, pre-A1, DUA Acces, tots els complements):
- Tot l'anterior + complements (glossari bilingue, esquema, preguntes, pictogrames)
- **Total: ~50 instruccions**

### 5.2 Que detecta l'LLM i que no

La literatura i l'experiencia acumulada amb Gemini 2.5 Flash en el projecte ATNE permeten classificar la sensibilitat de l'LLM a les instruccions:

**Alta sensibilitat (l'LLM ho fa be)**:
- Instruccions especifiques i accionables: "Frases de 5-8 paraules maxim", "Termes tecnics en negreta amb definicio"
- Prohibicions explicites: "ZERO meta-text", "No sinonimat"
- Format de sortida: "Comenca amb ## Text adaptat", "Glossari en taula"
- Simplificacio lexica i sintactica
- Canvi de veu passiva a activa
- Generacio de glossaris monolingues

**Sensibilitat moderada**:
- Matisos entre instruccions similars (p.ex. "vocabulari frequent" vs "vocabulari quotidiao basic" -- l'LLM no distingeix be el grau)
- Graus subtils de simplificacio (diferencia entre pre-A1 i A1 es difusa)
- Glossaris bilingues en llengues poc suportades (arab: mitjana-alta; amazic/wolof: baixa)
- Manteniment de terminologia tecnica en nivells molt baixos (conflicte simplificar vs mantenir)

**Baixa sensibilitat (l'LLM no ho fa be)**:
- Comptar paraules per frase (els LLM no compten, intueixen)
- Contradiccions implicites entre instruccions (no les detecta)
- Seguir mes de 40-50 regles simultanees sense degradacio
- Produir format estricte sense clean_gemini_output() de post-processament
- Metriques quantitatives precises (densitat lexica, ratio paraules contingut/funcionals)

### 5.3 Efecte "lost in the middle"

Liu et al. (2023) van documentar que els LLM presten mes atencio a les instruccions del principi i del final del context, amb una zona de menor atencio al mig. Aixo te implicacions directes per a ATNE:

- Les 15 instruccions universals (Capa 2) estan al principi del prompt: **alta atencio**.
- El text original a adaptar esta al final (Capa 4): **alta atencio**.
- Les instruccions condicionals (Capa 3) estan al mig: **atencio variable**.
- Les instruccions de perfil (dins Capa 3) son les mes vulnerables.

**Implicacio practica**: L'ordre de les instruccions dins del prompt importa. Les instruccions critiqu del perfil haurien d'anar al principi de la Capa 3, no al final. El few-shot example hauria d'anar just abans del text original.

### 5.4 Diferencia RAG enriquit vs Hardcoded: un cas concret

Per il-lustrar la diferencia entre les dues branques, es presenta el cas d'un alumne nouvingut d'origen arab, amb alfabet no llati, escolaritzacio parcial i nivell A1.

**Instruccions que rep l'LLM a la branca hardcoded** (bloc `PROFILE_BLOCKS["nouvingut"]`):

```
PERFIL: Nouvingut
- Referents culturals: substitueix locals per universals o explica
- Glossari bilingue amb traduccio a L1
- Suport visual: imatges, esquemes (la comprensio visual no depen de L2)
- Redundancia modal: text + imatge + esquema
```

Aquestes 4 instruccions son **sempre identiques** per a qualsevol nouvingut, independentment de L1, alfabet, escolaritzacio o temps a Catalunya.

**Instruccions que rep l'LLM a la branca RAG** (extretes dels fitxers MD del corpus):

Les 4 instruccions base identiques + 4 instruccions condicionals addicionals:
- **G-03**: Transliteracio fonetica per a termes clau (activada per alfabet no llati)
- **G-04**: Disclaimer de traduccions orientatives (activada per L1 poc suportada: arab es mitjana-alta, pero activada per cautela)
- **G-02**: Traduccio parcial de consignes a L1 (activada per pre-A1/A1)
- **E-11**: Evitar pressuposar familiaritat amb generes academics (activada per escolaritzacio parcial)

**Diferencia**: 4 instruccions vs 8 instruccions. La diferencia no es un canvi radical de paradigma; es un **afinament** que afegeix precisio al cas concret. La pregunta empirica es: aquest afinament es tradueix en una adaptacio mesurablament millor?

L'observacio qualitativa (revisio manual d'una mostra de 10 adaptacions) suggereix que les instruccions condicionals RAG produeixen diferencies observables:
- El glossari inclou transliteracio fonetica (p.ex. "fotosintesi = التمثيل الضوئي [at-tamthil ad-daw'i]")
- Les consignes d'activitats inclouen traduccio parcial
- El text no presuposa familiaritat amb generes academics (afegeix orientacio explicita)

Pero aquestes diferencies son **marginals** comparades amb la diferencia global entre "adaptacio bona" i "adaptacio dolenta". Cal metriques objectives.

---

## 6. Disseny experimental proposat

Per respondre la pregunta central ("la granularitat millora la qualitat real de l'adaptacio?"), es proposa el seguent experiment.

### 6.1 Hipotesi

**H1**: Les adaptacions generades amb instruccions filtrades per variable individual (branca RAG enriquida) obtenen puntuacions significativament mes altes en fidelitat al perfil i adequacio pedagogica que les generades amb instruccions compactes baseline (branca hardcoded).

**H0**: No hi ha diferencia significativa en qualitat de fons entre les dues branques.

### 6.2 Variables

| Variable | Tipus | Definicio operacional |
|---|---|---|
| **Mode d'instruccions** | Independent (2 nivells) | RAG (instruccions filtrades per variable) vs Hardcoded (instruccions compactes) |
| **Perfil de l'alumnat** | Independent (10 nivells) | 7 perfils simples + 3 creuaments (mateixa matriu que el batch test) |
| **Qualitat de forma** | Dependent | Metriques automatiques: paraules, negretes, longitud frase, estructura |
| **Qualitat de fons** | Dependent | Puntuacio LLM-as-a-judge amb rubrica pedagogica |
| **Fidelitat al perfil** | Dependent | Grau en que l'adaptacio respon a la barrera nuclear del perfil |

### 6.3 Instrument: Agent avaluador (LLM-as-a-judge)

L'agent avaluador es un segon LLM (diferent del que genera l'adaptacio) que avalua cada adaptacio amb una rubrica estructurada. Aixo evita l'autoavaluacio, que la recerca identifica com "majoritariament teatre" dins del mateix prompt.

**Capa 1 (forma, codi Python)**: ja implementada al `post_process_adaptation()`:
- Longitud de frases (max per MECR)
- Presencia de paraules prohibides
- Presencia d'encapcalaments i negretes
- Metriques basiques (paraules, frases, termes en negreta)

**Capa 2 (fons, LLM avaluador)**: per implementar:

| Criteri | Pregunta avaluadora | Escala |
|---|---|---|
| Coherencia | Totes les idees del text adaptat tenen correspondencia amb l'original? | 1-5 |
| Fidelitat al perfil | L'adaptacio respon a la barrera nuclear del perfil indicat? | 1-5 |
| Rigor curricular | S'han mantingut tots els termes tecnics? Les definicions son correctes? | 1-5 |
| Adequacio MECR | El nivell linguistic de sortida correspon al MECR indicat? | 1-5 |
| Adequacio DUA | El nivell d'adaptacio correspon al DUA indicat (Acces/Core/Enriquiment)? | 1-5 |
| Scaffolding | Hi ha suport decreixent (definicions completes > breus > absents)? | 1-5 |
| Completesa | L'adaptacio es completa (no truncada, no parcial)? | 1-5 |

**Gold Standard per perfil**: Per a cada un dels 10 perfils, es defineix un conjunt de criteris que l'adaptacio ha de complir, derivats directament del mapa perfil-instruccions (seccio 8 de l'arquitectura). L'avaluador mesura el recall (quants criteris es compleixen).

### 6.4 Protocol d'execucio

1. Reutilitzar la matriu de 160 casos (16 textos x 10 perfils).
2. Generar cada cas amb ambdues branques (total: 320 adaptacions).
3. Avaluar cada adaptacio amb la Capa 1 (forma, automatica) i la Capa 2 (fons, LLM avaluador).
4. Comparar les distribucions de puntuacions entre branques per a cada criteri.
5. Analitzar si la diferencia es significativa globalment i per subgrup de perfil.

### 6.5 Criteris de decisio

- Si RAG supera Hardcoded en >= 3 dels 7 criteris de fons amb diferencia >= 0.5 punts: **adoptar RAG com a via principal**.
- Si la diferencia es < 0.5 en tots els criteris: **adoptar Hardcoded per simplicitat**.
- Si la diferencia es mixta (RAG millor en uns, Hardcoded en altres): **mode dual amb switch UI**.

---

## 7. Conclusions i proxims passos

### 7.1 Conclusions

**1. El mapa d'instruccions existeix i es robust.**
Les 95 instruccions del cataleg consolidat (seccions 7-8 de `arquitectura_prompt_v2.md`) son el resultat d'una triangulacio sistematica de 8 fonts primaries internacionals (CAST/UDL, IFLA, UNE, MECR-CV, WCAG, Plain Language, Clarity International, DSM-5-TR) i 5 marcs teorics complementaris (Sweller, Vygotsky, Mayer, Halliday, Dehaene/Wolf). Cada instruccio te ID, executor assignat, regla d'activacio i prioritat.

**2. La traduccio fidel del paper al codi es el treball pendent.**
L'arquitectura defineix activacio granular per instruccio; la implementacio agrupa en blocs monolitics. Tancar aquest gap requereix un motor de regles que seleccioni instruccions individuals segons les sub-variables del perfil (L1, alfabet, escolaritzacio, temps, context familiar), no nomes el perfil generic.

**3. RAG genera mes contingut i mes rapid, pero "mes" no vol dir "millor".**
Els resultats del batch test (769 vs 248 paraules/cas, 15s vs 27.5s) son prometedors pero insuficients. Les metriques de forma no mesuren qualitat pedagogica. La decisio final requereix metriques de fons.

**4. L'agent avaluador es imprescindible.**
Sense un termometre de fons (fidelitat al perfil, rigor curricular, adequacio MECR/DUA), qualsevol decisio sobre quina branca es millor es un vol a cegues. L'agent avaluador LLM-as-a-judge amb rubrica pedagogica es el proper pas prioritari.

**5. El llindar de ~50 instruccions simultanees requereix estrategia de priorització.**
Els casos extrems (nouvingut+dislexia, pre-A1, DUA Acces, tots els complements) generen ~50 instruccions simultanees, al limit de fiabilitat de Gemini Flash. Estrategies de mitigacio:
- Pipeline en 2 passos (pas 1: text adaptat, pas 2: complements)
- Priorització per barrera nuclear (enviar primer les instruccions que ataquen la barrera principal del perfil)
- Routing de models (casos simples amb Flash, casos complexos amb Pro o Claude)

**6. Hi ha 5 contradiccions instruccions fixes vs perfil que cal resoldre.**
Les instruccions A-03, A-05, A-07, A-08 i A-11 entren en conflicte amb perfils d'AC i nivells B2/Enriquiment. La jerarquia MECR > DUA > LF no cobreix tots els casos. Cal una capa addicional de logica per excepcions de perfil.

### 7.2 Proxims passos (ordenats per prioritat)

| # | Accio | Impacte | Esforc |
|---|---|---|---|
| 1 | **Implementar agent avaluador** (LLM-as-a-judge amb rubrica de 7 criteris) | Crtic: es la base per a tota decisio posterior | 1-2 sessions |
| 2 | **Merge branques a main** amb switch UI (RAG / Hardcoded / Doble) i pestanya comparador visual | Alt: permet validacio humana i experimentacio | 1 sessio |
| 3 | **Re-correr 160 casos** amb avaluacio de fons (agent avaluador) | Alt: primera evidencia empirica de qualitat | 1 sessio (automatitzat) |
| 4 | **Resoldre contradiccions** (reclassificar 5 instruccions amb excepcio per perfil) | Mitja: millora qualitat per AC/B2 | 0.5 sessions |
| 5 | **Implementar pipeline 2 passos** (text adaptat + complements per separat) | Alt: redueix instruccions per crida de ~50 a ~30+20 | 1-2 sessions |
| 6 | **Motor de regles granular** (seleccio instruccions per sub-variable, no nomes per perfil) | Alt si H1 es confirma; baix si H0 | 2-3 sessions |

---

## 8. Referències

### 8.1 Fonts internes del projecte ATNE

| Document | Ubicacio | Contingut |
|---|---|---|
| Arquitectura prompt v2 | `docs/decisions/arquitectura_prompt_v2.md` | Sintesi triangulacio, 95 instruccions, 4 capes, pla 4 fases |
| Banc exhaustiu d'instruccions | `docs/investigacio/banc_exhaustiu_instruccions_adaptacio.md` | 119 instruccions amb exemples, fonts, graduabilitat |
| Taxonomia A1 de variables | `docs/investigacio/ext_taxonomia_adaptacio_A1.md` | 8 dominis, 70+ variables amb codis |
| Investigacio marcs teorics | `docs/investigacio/investigacio_marcs_teorics_ATNE.md` | 15+ marcs teorics avaluats (Sweller, Vygotsky, Mayer, etc.) |
| Mapa de barreres per perfil | `docs/investigacio/mapa_barreres_perfil.md` | 13 perfils x 10 dimensions de barrera |
| Analisi capacitats LLM | `docs/investigacio/analisi_capacitats_llm_adaptacio.md` | Capacitats i limits dels LLM per a adaptacio textual |
| Modelabilitat LLM | `docs/investigacio/ext_modelabilitat_llm_C.md` | Comparativa models (GPT-4, Claude, Gemini, Mistral, Llama) |
| Sessio batch tests | `docs/sessions/2026-03-28_batch-tests-comparativa.md` | Resultats comparatius 160 casos RAG vs Hardcoded |
| Sessio hardcoded | `docs/sessions/sessio_2026-03-28_prompt-v2-hardcoded.md` | Implementacio branca hardcoded, resultats inicials |

### 8.2 Fonts externes

| Referencia | Aportacio al projecte |
|---|---|
| CAST (2018). *Universal Design for Learning Guidelines version 2.2*. Wakefield, MA. | 3 principis, 9 pautes, 31 checkpoints. Base dels 3 nivells DUA (Acces/Core/Enriquiment) |
| Consell d'Europa (2020). *Common European Framework of Reference for Languages: Companion Volume*. Estrasburg. | Descriptors per nivell (pre-A1 a C2). Base dels 5 blocs MECR del prompt |
| IFLA (2010). *Guidelines for Easy-to-Read Materials*. La Haia. | Regles de Lectura Facil: frases curtes, vocabulari frequent, puntuacio simple |
| Inclusion Europe (2009). *Information for All: European Standards for Easy-to-Read*. Brusselles. | Complement europeu de les directrius IFLA |
| UNE 153101:2018. *Lectura Facil: Pautes y recomendaciones para la elaboracion de documentos*. AENOR. | Norma espanyola de Lectura Facil, referencia per al catala |
| Liu, N., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., & Liang, P. (2023). "Lost in the Middle: How Language Models Use Long Contexts." *Transactions of the Association for Computational Linguistics*, 12, 157-173. | Documentacio de l'efecte de pèrdua d'atencio al mig del context en LLM |
| Mayer, R. E. (2009). *Multimedia Learning* (2a ed.). Cambridge University Press. | Principi de coherencia ("no afegeixis informacio irrelevant") i principi de senyalitzacio |
| Sweller, J. (1988). "Cognitive Load During Problem Solving: Effects on Learning." *Cognitive Science*, 12(2), 257-285. | Teoria de la Carrega Cognitiva: limits de la memoria de treball, split-attention, pre-training |
| Vygotsky, L. S. (1978). *Mind in Society: The Development of Higher Psychological Processes*. Harvard University Press. | Zona de Desenvolupament Proxim i scaffolding |
| Wood, D., Bruner, J. S., & Ross, G. (1976). "The Role of Tutoring in Problem Solving." *Journal of Child Psychology and Psychiatry*, 17(2), 89-100. | Formalitzacio del scaffolding: suport decreixent a mesura que l'aprenent guanya competencia |
| Halliday, M. A. K., & Hasan, R. (1976). *Cohesion in English*. Longman. | Marc de cohesio textual: referencia, substitucio, el-lipsi, conjuncio, cohesio lexica |
| Halliday, M. A. K. (1993). "Towards a Language-Based Theory of Learning." *Linguistics and Education*, 5(2), 93-116. | Linguistica Sistemica Funcional: regles per genere discursiu, desnominalitzacio |
| Dehaene, S. (2009). *Reading in the Brain*. Viking. | Neurociencia de la lectura: implicacions per a dislexia (evitar compostos llargs, alta frequencia lexica) |
| Wolf, M. (2007). *Proust and the Squid: The Story and Science of the Reading Brain*. Harper. | Complement a Dehaene: el cervell lector i les dificultats de decodificacio |
| Paivio, A. (1991). *Images in Mind: The Evolution of a Theory*. Harvester Wheatsheaf. | Teoria del Doble Codificacio: canal verbal + canal visual per millorar retencio |
| Bloom, B. S. (Ed.). (1956). *Taxonomy of Educational Objectives: The Classification of Educational Goals*. Longmans, Green. | Taxonomia de Bloom per graduar nivells DUA: Acces=Recordar/Comprendre, Core=Aplicar, Enriquiment=Analitzar/Avaluar/Crear |
| W3C (2023). *Web Content Accessibility Guidelines (WCAG) 2.2*. | Criteris d'accessibilitat digital aplicables al frontend |

---

*Document generat el 2026-03-29. Projecte ATNE, Jesuites Educacio (FJE).*
*Amb suport de Claude Opus 4.6 (Anthropic).*
