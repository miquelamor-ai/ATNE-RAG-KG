# Mapa complet: Característiques → Variables → Instruccions

**Projecte**: ATNE — Adaptador de Textos a Necessitats Educatives
**Data**: 2026-03-30
**Autor**: Claude Opus 4.6 amb supervisió Miquel Amor
**Fonts**: instruction_catalog.py (89 instr.), arquitectura_prompt_v2.md (95 instr.), banc_exhaustiu (119 instr.), mapa_barreres_perfil.md, analisi_capacitats_llm.md, app.js (36 sub-variables)

---

## 1. Diagnosi de l'estat actual

### 1.1 Xifres clau

| Element | Quantitat | Estat |
|---|---|---|
| Instruccions al banc exhaustiu (font) | 119 | Document de referència |
| Instruccions al catàleg consolidat (arquitectura) | 95 | 72 LLM + 12 CODI + 11 FE |
| Instruccions implementades (instruction_catalog.py) | 89 | Totes LLM |
| Característiques (perfils alumnat) | 13 | Implementades a UI + backend |
| Sub-variables declarades a la UI | 36 | Recollides del docent |
| Sub-variables que fan alguna cosa | 15 | 42% |
| Sub-variables que activen instruccions condicionals | 3 | 8% (totes del nouvingut) |
| Sub-variables que NO fan res | 21 | 58% |

### 1.2 El problema central

El sistema té tres capes desconnectades:

```
CARACTERÍSTIQUES (13)     VARIABLES (36)         INSTRUCCIONS (89)
    nouvingut ──────────── L1 ─────────────────── G-01 ✓ connectat
                           alfabet_llati ────────── G-03 ✓ connectat
                           mecr ──────────────────── NIVELL ✓ connectat
                           calp ──────────────────── ??? ✗ no fa res
                           familia_linguistica ──── ??? ✗ no fa res
                           escolaritzacio_previa ── ??? ✗ no fa res
    tdl ────────────────── modalitat ──────────── ??? ✗ no fa res
                           morfosintaxi ──────────── ??? ✗ no fa res
                           semantica ────────────── ??? ✗ no fa res
                           pragmatica ──────────── ??? ✗ no fa res
                           discurs_narrativa ────── ??? ✗ no fa res
                           comprensio_lectora ───── ??? ✗ no fa res
                           grau ──────────────────── ??? ✗ no fa res
                           bilingue ──────────────── ??? ✗ no fa res
    ...
```

**Conseqüència**: un docent pot dedicar 5 minuts a configurar el perfil d'un alumne amb TDL (8 sub-variables) i el sistema les ignora totes. Rep exactament les mateixes 2 instruccions (H-16, H-17) que si no hagués configurat res.

### 1.3 Què falta (i què aborda aquest document)

| Peça | Existeix? | On es resol |
|---|---|---|
| Catàleg d'instruccions amb classificació moment/fiabilitat | Parcialment (arquitectura §7) | Secció 2 |
| Fitxa de variables per característica (fixes/condicionals/canal) | NO | Secció 3 |
| Matriu matching variable → instruccions | NO | Secció 4 |
| Anàlisi d'eficiència (quantes instruccions per cas?) | NO | Secció 5 |
| Protocol de conflictes entre perfils | Parcial (MECR>DUA>LF) | Secció 6 |

---

## 2. Auditoria del catàleg d'instruccions

### 2.1 Classificació per moment d'execució

Cada instrucció s'executa en un d'aquests moments:

- **LLM-PROMPT**: L'LLM la rep com a instrucció dins del system prompt
- **LLM-NARRATIVA**: Va al bloc persona-audience com a context (no com a ordre)
- **CODI-POST**: Backend Python verifica/corregeix després de la generació
- **FE-CSS**: Frontend ho gestiona amb CSS/HTML/JS

### 2.2 Classificació per fiabilitat LLM

Basada en l'anàlisi de capacitats (analisi_capacitats_llm_adaptacio.md):

- **ALTA** (8-10/10): L'LLM ho fa bé de forma consistent
- **MITJANA** (5-7/10): Ho fa però cal verificar amb codi
- **BAIXA** (2-4/10): L'LLM no pot garantir-ho, cal codi obligatòriament

### 2.3 Taula d'auditoria completa (95 instruccions)

#### A. Adaptació lingüística (26 instruccions)

| ID | Instrucció | Moment | Fiabilitat | Solapament | Estat |
|---|---|---|---|---|---|
| A-01 | Vocabulari freqüent | LLM-PROMPT | ALTA | ≈ H-08 (dislèxia) | P0 ✓ |
| A-02 | Termes tècnics en negreta + definició | LLM-PROMPT | ALTA | — | P0 ✓ |
| A-03 | Repetició lèxica (no sinònims) | LLM-PROMPT | ALTA | ≈ H-08 (dislèxia) | P0 ✓ |
| A-04 | Referents pronominals explícits | LLM-PROMPT | ALTA | — | P0 ✓ |
| A-05 | Eliminar idiomàtiques/figurat | LLM-PROMPT | ALTA | ⊂ H-02 (TEA) | P0 ✓ |
| A-06 | Eliminar polisèmia | LLM-PROMPT | ALTA | — | P0 ✓ |
| A-07 | Una idea per frase | LLM-PROMPT | ALTA | — | P0 ✓ |
| A-08 | Veu activa obligatòria | LLM-PROMPT | ALTA | — | P0 ✓ |
| A-09 | Subjecte explícit | LLM-PROMPT | ALTA | — | P0 ✓ |
| A-10 | Ordre canònic SVO | LLM-PROMPT | ALTA | — | P0 ✓ |
| A-11 | Puntuació simplificada | LLM-PROMPT | ALTA | — | P0 ✓ |
| A-12 | Longitud frase per MECR | LLM-PROMPT | **MITJANA** | — | P0 ✓ |
| A-13 | Reduir subordinades | LLM-PROMPT | ALTA | — | P0 ✓ |
| A-14 | Connectors explícits | LLM-PROMPT | ALTA | — | P0 ✓ |
| A-15 | Scaffolding decreixent (Vygotsky) | LLM-PROMPT | **MITJANA** | — | P0 ✓ |
| A-16 | Desnominalització (Halliday) | LLM-PROMPT | ALTA | — | P0 ✓ |
| A-17 | Evitar negacions múltiples | LLM-PROMPT | ALTA | — | P0 ✓ |
| A-18 | Dates format complet | LLM-PROMPT | ALTA | — | P0 ✓ |
| A-19 | Sigles/abreviatures explicades | LLM-PROMPT | ALTA | — | P0 ✓ |
| A-20 | Control densitat lèxica | LLM-PROMPT | **MITJANA** | — | P0 ✓ |
| A-21 | Descomposició paraules compostes | LLM-PROMPT | ALTA | — | P0 ✓ |
| A-22 | Concretar quantificadors | LLM-PROMPT | ALTA | — | P0 ✓ |
| A-23 | Evitar cultismes/llatinismes | LLM-PROMPT | ALTA | — | P0 ✓ |
| A-24 | Present indicatiu preferent | LLM-PROMPT | ALTA | — | P0 ✓ |
| A-25 | Formes verbals simples | LLM-PROMPT | ALTA | — | P0 ✓ |
| A-26 | Evitar incisos parentètics llargs | LLM-PROMPT | ALTA | — | P0 ✓ |

**Solapaments a resoldre**:
- A-01 ↔ H-08: quan dislèxia és activa, H-08 fa redundant A-01. Recomanació: NO enviar A-01 si H-08 ja s'envia.
- A-03 ↔ H-08: idem. H-08 ja inclou "no sinònims".
- A-05 ⊂ H-02: H-02 (TEA: zero implicitura) és superconjunt d'A-05 (eliminar figurat). Si TEA actiu, A-05 és redundant.

#### B. Estructura i organització (14 instruccions)

| ID | Instrucció | Moment | Fiabilitat | Solapament | Estat |
|---|---|---|---|---|---|
| B-01 | Paràgrafs curts (3-5 frases) | LLM-PROMPT | ALTA | — | P0 ✓ |
| B-02 | Blocs amb títol descriptiu | LLM-PROMPT | ALTA | ∩ H-19 | P0 ✓ |
| B-03 | Frase tòpic al principi | LLM-PROMPT | ALTA | — | P0 ✓ |
| B-04 | Llistes vs enumeracions | LLM-PROMPT | ALTA | — | P0 ✓ |
| B-05 | Estructura deductiva | LLM-PROMPT | ALTA | — | P0 ✓ |
| B-06 | Ordre cronològic | LLM-PROMPT | ALTA | — | P0 ✓ |
| B-07 | Resum anticipatiu (advance organizer) | LLM-PROMPT | **MITJANA** | — | P0 ✓ |
| B-08 | Resum final recapitulatiu | LLM-PROMPT | **MITJANA** | — | P0 ✓ |
| B-09 | Numerar passos/seqüències | LLM-PROMPT | ALTA | — | P0 ✓ |
| B-10 | Transicions entre seccions | LLM-PROMPT | ALTA | — | P0 ✓ |
| B-11 | Salt de línia entre idees | LLM-PROMPT | ALTA | — | P0 ✓ |
| B-12 | Senyalització nucli vs complement | LLM-PROMPT | **MITJANA** | — | P2 pendent |
| B-13 | Indicadors de progrés [X de Y] | LLM-PROMPT | ALTA | — | P0 ✓ |
| B-14 | Taules per info comparativa | LLM-PROMPT | ALTA | — | P0 ✓ |

#### C. Suport cognitiu (9 instruccions)

| ID | Instrucció | Moment | Fiabilitat | Solapament | Estat |
|---|---|---|---|---|---|
| C-01 | Límit conceptes nous per bloc | LLM-PROMPT | **MITJANA** | — | P0 ✓ |
| C-02 | Reforç immediat concepte nou | LLM-PROMPT | ALTA | — | P0 ✓ |
| C-03 | Eliminar redundància decorativa (Mayer) | LLM-PROMPT | ALTA | — | P0 ✓ |
| C-04 | Chunking (3-5 elements) | LLM-PROMPT | **MITJANA** | — | P0 ✓ |
| C-05 | Glossari previ (pre-training Sweller) | LLM-PROMPT | ALTA | — | P0 ✓ |
| C-06 | Analogies quotidianes | LLM-PROMPT | ALTA | — | P0 ✓ |
| C-07 | Connexió aprenentatges anteriors | LLM-PROMPT | ALTA | — | P2 pendent |
| C-08 | Anticipació vocabulari | LLM-PROMPT | ALTA | ∩ C-05 | P0 ✓ |
| C-09 | Espaiament dificultat | LLM-PROMPT | **MITJANA** | — | P2 pendent |

#### D. Multimodalitat (9 instruccions)

| ID | Instrucció | Moment | Fiabilitat | Solapament | Estat |
|---|---|---|---|---|---|
| D-01 | Emojis suport | LLM-PROMPT | ALTA | — | P0 ✓ |
| D-02 | Esquema procés (flowchart text) | LLM-PROMPT | **MITJANA** | — | P0 ✓ |
| D-03 | Mapa conceptual jeràrquic | LLM-PROMPT | **MITJANA** | — | P0 ✓ |
| D-04 | Taula comparativa | LLM-PROMPT | ALTA | ∩ B-14 | P0 ✓ |
| D-05 | Línia del temps textual | LLM-PROMPT | ALTA | — | P0 ✓ |
| D-06 | Text per lectura veu alta | LLM-PROMPT | ALTA | — | P0 ✓ |
| D-07 | Indicacions tipus imatge | LLM-PROMPT | **MITJANA** | — | P2 pendent |
| D-08 | Pictogrames ARASAAC | **CODI+FE** | N/A | — | P3 futur |
| D-09 | Àudio TTS | **CODI+FE** | N/A | — | P3 futur |

#### E. Contingut curricular (12 instruccions)

| ID | Instrucció | Moment | Fiabilitat | Solapament | Estat |
|---|---|---|---|---|---|
| E-01 | Nucli terminològic intocable | LLM-PROMPT | ALTA | — | P0 ✓ |
| E-02 | Graduació definició per MECR | LLM-PROMPT | ALTA | — | P0 ✓ |
| E-03 | Glossari final complet | LLM-PROMPT | ALTA | — | P0 ✓ |
| E-04 | Glossari bilingüe L1-L2 | LLM-PROMPT | **MITJANA** | **= G-01** duplicat | P0 ✓ |
| E-05 | Exactitud científica | LLM-PROMPT | ALTA | — | P0 ✓ |
| E-06 | Simplificar mantenint causalitat | LLM-PROMPT | ALTA | — | P0 ✓ |
| E-07 | Exemple per concepte abstracte | LLM-PROMPT | ALTA | — | P0 ✓ |
| E-08 | Referents culturalment diversos | LLM-PROMPT | ALTA | **≈ G-05** quasi duplicat | P0 ✓ |
| E-09 | Evitar supòsits culturals | LLM-PROMPT | ALTA | — | P0 ✓ |
| E-10 | Sensibilitat temes traumàtics | LLM-PROMPT | ALTA | — | P0 ✓ |
| E-11 | Pistes etimològiques translingües | LLM-PROMPT | **MITJANA** | — | P0 ✓ |
| E-12 | Contra-exemples | LLM-PROMPT | ALTA | — | P0 ✓ |

**Duplicats a resoldre**:
- E-04 = G-01: són la mateixa instrucció (glossari bilingüe). **Eliminar E-04**, quedar-se amb G-01 (més detallada).
- E-08 ≈ G-05: "referents diversos" i "substitució referents culturals" diuen gairebé el mateix. **Fusionar** en una sola.

#### F. Avaluació i comprensió (10 instruccions)

| ID | Instrucció | Moment | Fiabilitat | Solapament | Estat |
|---|---|---|---|---|---|
| F-01 | Preguntes reconeixement (literal) | LLM-PROMPT | ALTA | — | P0 ✓ |
| F-02 | Preguntes V/F | LLM-PROMPT | ALTA | — | P0 ✓ |
| F-03 | Preguntes inferència | LLM-PROMPT | ALTA | — | P0 ✓ |
| F-04 | Preguntes transferència | LLM-PROMPT | ALTA | — | P0 ✓ |
| F-05 | Graduació format resposta | LLM-PROMPT | **MITJANA** | — | P0 ✓ |
| F-06 | Preguntes comprensió intercalades | LLM-PROMPT | ALTA | — | P0 ✓ |
| F-07 | Objectius aprenentatge explícits | LLM-PROMPT | ALTA | — | P1 pendent |
| F-08 | Activitats aprofundiment | LLM-PROMPT | ALTA | — | P0 ✓ |
| F-09 | Pensament crític | LLM-PROMPT | ALTA | ∩ F-10, H-13 | P0 ✓ |
| F-10 | Connexions interdisciplinars | LLM-PROMPT | ALTA | **= H-13** duplicat | P0 ✓ |

**Duplicat a resoldre**:
- F-10 = H-13: idèntics. **Eliminar H-13**, quedar-se amb F-10 (categoria més lògica).

#### G. Personalització lingüística (6 instruccions)

| ID | Instrucció | Moment | Fiabilitat | Solapament | Estat |
|---|---|---|---|---|---|
| G-01 | Glossari bilingüe complet | LLM-PROMPT | **MITJANA** | = E-04 | P0 ✓ |
| G-02 | Traducció parcial consignes L1 | LLM-PROMPT | **BAIXA** | — | P0 ✓ |
| G-03 | Transliteració fonètica | LLM-PROMPT | **BAIXA** | — | P0 ✓ |
| G-04 | Disclaimer traduccions no fiables | **CODI+FE** | N/A | — | P1 pendent |
| G-05 | Substitució referents culturals | LLM-PROMPT | ALTA | ≈ E-08 | P0 ✓ |
| G-06 | To per nivell MECR | LLM-PROMPT | ALTA | — | P0 ✓ |

#### H. Adaptacions per perfil (20 instruccions)

| ID | Instrucció | Moment | Fiabilitat | Solapament | Estat |
|---|---|---|---|---|---|
| H-01 | TEA: estructura predictible | LLM-PROMPT | ALTA | — | P0 ✓ |
| H-02 | TEA: zero implicitura | LLM-PROMPT | ALTA | ⊃ A-05 | P0 ✓ |
| H-03 | TEA: anticipació canvis | LLM-PROMPT | ALTA | — | P0 ✓ |
| H-04 | TDAH: micro-blocs | LLM-PROMPT | ALTA | — | P0 ✓ |
| H-05 | TDAH: retroalimentació visual | LLM-PROMPT | **MITJANA** | — | P0 ✓ |
| H-06 | TDAH: variació dins text | LLM-PROMPT | ALTA | — | P0 ✓ |
| H-07 | Dislèxia: evitar compostos | LLM-PROMPT | ALTA | ∩ A-21 | P0 ✓ |
| H-08 | Dislèxia: alta freqüència | LLM-PROMPT | ALTA | ⊃ A-01+A-03 | P0 ✓ |
| H-09 | DI: 1 concepte per bloc | LLM-PROMPT | ALTA | — | P0 ✓ |
| H-10 | DI: concreció radical | LLM-PROMPT | ALTA | — | P0 ✓ |
| H-11 | DI: repetició sistemàtica | LLM-PROMPT | **MITJANA** | — | P0 ✓ |
| H-12 | AC: profundització | LLM-PROMPT | ALTA | — | P0 ✓ |
| H-13 | AC: connexions interdisciplinars | LLM-PROMPT | ALTA | **= F-10** | P0 ✓ |
| H-14 | AC: mantenir complexitat | LLM-PROMPT | ALTA | — | P0 ✓ |
| H-14b | AC: PROHIBIT SIMPLIFICAR | LLM-PROMPT | ALTA | ∩ H-14 | P0 ✓ |
| H-15 | 2e: equilibri repte/accessibilitat | LLM-PROMPT | **MITJANA** | — | P0 ✓ |
| H-16 | TDL: reducció densitat lèxica | LLM-PROMPT | **MITJANA** | ∩ A-20 | P0 ✓ |
| H-17 | TDL: modelatge ús en context | LLM-PROMPT | ALTA | — | P0 ✓ |
| H-19 | Disc.visual: estructura semàntica | LLM-PROMPT | ALTA | ∩ B-02 | P0 ✓ |
| H-20 | Disc.auditiva: simplificació L2 | LLM-PROMPT | ALTA | — | P0 ✓ |

**Solapaments a resoldre**:
- H-14 ∩ H-14b: H-14b és la versió "dura" de H-14. Podrien fusionar-se. Recomanació: **fusionar** en una sola instrucció clara.
- H-16 ∩ A-20: A-20 és genèrica (densitat lèxica per MECR), H-16 és específica TDL. Quan TDL actiu, A-20 és redundant.

#### I. Presentació i layout (8 instruccions — totes FE)

| ID | Instrucció | Moment | Fiabilitat | Estat |
|---|---|---|---|---|
| I-01 | Tipografia sans-serif 14pt | **FE-CSS** | N/A | P3 futur |
| I-02 | Interlineat 1.5 | **FE-CSS** | N/A | P3 futur |
| I-03 | Columna estreta 60-70 chars | **FE-CSS** | N/A | P3 futur |
| I-04 | Fons suau (crema/blau) | **FE-CSS** | N/A | P3 futur |
| I-05 | Alineat esquerra | **FE-CSS** | N/A | P3 futur |
| I-06 | Contrast alt | **FE-CSS** | N/A | P3 futur |
| I-07 | Navegable per teclat | **FE-CSS** | N/A | P3 futur |
| I-08 | Reescalat i zoom | **FE-CSS** | N/A | P3 futur |

#### J. Verificació i post-processament (7 instruccions — totes CODI)

| ID | Instrucció | Moment | Fiabilitat | Estat |
|---|---|---|---|---|
| J-01 | Verificar longitud frases | **CODI-POST** | N/A | P1 pendent |
| J-02 | Detectar paraules prohibides | **CODI-POST** | N/A | P1 pendent |
| J-03 | Verificar encapçalaments | **CODI-POST** | N/A | P2 pendent |
| J-04 | Verificar termes en negreta | **CODI-POST** | N/A | P2 pendent |
| J-05 | Mètriques llegibilitat | **CODI-POST** | N/A | P3 futur |
| J-06 | 2n prompt verificació amb rúbrica | **LLM** | MITJANA | P3 futur |
| J-07 | Comptar conceptes nous | **CODI-POST** | N/A | P3 futur |

### 2.4 Resum auditoria: 7 solapaments a resoldre

| # | Solapament | Resolució proposada |
|---|---|---|
| 1 | E-04 = G-01 (glossari bilingüe) | **Eliminar E-04**. Quedar-se amb G-01 |
| 2 | E-08 ≈ G-05 (referents culturals) | **Fusionar** en una sola instrucció |
| 3 | F-10 = H-13 (connexions interdisciplinars) | **Eliminar H-13**. Quedar-se amb F-10 |
| 4 | H-14 ∩ H-14b (mantenir complexitat AC) | **Fusionar** en una sola amb text clar |
| 5 | A-01/A-03 ∩ H-08 (freq. lèxica dislèxia) | Quan dislèxia activa, **no enviar A-01+A-03** (ja coberts per H-08) |
| 6 | A-05 ⊂ H-02 (figurat ⊂ implicitura TEA) | Quan TEA actiu, **no enviar A-05** (ja cobert per H-02) |
| 7 | A-20 ∩ H-16 (densitat lèxica ∩ TDL) | Quan TDL actiu, **no enviar A-20** (ja cobert per H-16) |

**Resultat net**: de 89 instruccions LLM actuals, amb les fusions/eliminacions quedarien **84 instruccions efectives** (5 eliminades per duplicat).

---

## 3. Fitxa de variables per característica

Per cada característica: variables que la componen, si són fixes o condicionals, i a quin canal van.

**Llegenda de canals**:
- **ORDRE**: Instrucció explícita dins el system prompt de l'LLM
- **NARRATIVA**: Va al bloc persona-audience (context, no ordre)
- **PROPOSTA**: Calcula automàticament MECR/DUA/LF sense instrucció directa
- **FE**: Frontend CSS/JS
- **RES**: Actualment no fa res (cal connectar o eliminar)

### 3.1 Nouvingut (6 variables)

| Variable | Tipus | Fix/Condicional | Canal actual | Canal correcte |
|---|---|---|---|---|
| `L1` | text | Fix (sempre es demana) | ORDRE (G-01, E-11) | ORDRE + NARRATIVA |
| `familia_linguistica` | select (6 valors) | Condicional | **RES** | PROPOSTA (deduir si L1 romànica → E-11) |
| `alfabet_llati` | bool | Condicional | ORDRE (G-03) | ORDRE ✓ correcte |
| `escolaritzacio_previa` | select (sí/parcial/no) | Condicional | **RES** | NARRATIVA + PROPOSTA |
| `mecr` | select (5 nivells) | Fix | PROPOSTA (MECR sortida) | PROPOSTA ✓ correcte |
| `calp` | select (3 valors) | Condicional | **RES** | NARRATIVA + PROPOSTA |

**Instruccions fixes (pel sol fet de ser nouvingut)**: A-21, E-08/G-05 (fusionades), E-09, G-01

**Variables que cal connectar**:
- `familia_linguistica`: si "romànica" → activar E-11 (pistes etimològiques). Ara la lògica es fa mirant `L1`, però `familia_linguistica` és més fiable
- `escolaritzacio_previa`: si "no" o "parcial" → NARRATIVA ("no ha estat escolaritzat regularment") + PROPOSTA (suggerir DUA Accés, MECR -1 nivell)
- `calp`: NARRATIVA ("llenguatge acadèmic inicial") + PROPOSTA (si "inicial" → reforçar C-05 glossari previ, B-07 advance organizer)

### 3.2 TEA (2 variables)

| Variable | Tipus | Fix/Condicional | Canal actual | Canal correcte |
|---|---|---|---|---|
| `nivell_suport` | select (1/2/3) | Condicional | **RES** | NARRATIVA + PROPOSTA |
| `comunicacio_oral` | select (fluida/limitada/no_verbal) | Condicional | **RES** | NARRATIVA + ORDRE |

**Instruccions fixes**: H-01, H-02, H-03

**Variables que cal connectar**:
- `nivell_suport`: si 3 → PROPOSTA (suggerir DUA Accés) + NARRATIVA ("necessita suport molt significatiu")
- `comunicacio_oral`: si "no_verbal" o "limitada" → ORDRE: activar D-01 (emojis), D-02 (esquemes visuals) com a suport extra. NARRATIVA ("comunicació oral limitada, necessita més canal visual")

### 3.3 TDAH (4 variables)

| Variable | Tipus | Fix/Condicional | Canal actual | Canal correcte |
|---|---|---|---|---|
| `presentacio` | select (inatent/hiperactiu/combinat) | Condicional | **RES** | NARRATIVA |
| `grau` | select (lleu/moderat/sever) | Condicional | **RES** | PROPOSTA + ORDRE |
| `baixa_memoria_treball` | bool | Condicional | **RES** | ORDRE |
| `fatiga_cognitiva` | bool | Condicional | **RES** | ORDRE + PROPOSTA |

**Instruccions fixes**: H-04, H-05, H-06, B-13, F-06

**Variables que cal connectar**:
- `presentacio`: NARRATIVA ("perfil predominantment inatent"). No modifica instruccions (les 3 presentacions reben les mateixes adaptacions textuals)
- `grau`: si "sever" → PROPOSTA (suggerir DUA Accés) + ORDRE (intensificar micro-blocs: 2-3 frases en lloc de 3-5)
- `baixa_memoria_treball`: si true → ORDRE: reforçar C-04 (chunking 3 elements màx), C-01 (1-2 conceptes per paràgraf en lloc de 2-3), B-08 (resum recapitulatiu)
- `fatiga_cognitiva`: si true → ORDRE: textos més curts (activar instrucció nova: "Retalla el text al 60-70% de l'extensió original, prioritzant el nucli curricular") + PROPOSTA (suggerir DUA Accés)

### 3.4 Dislèxia (4 variables)

| Variable | Tipus | Fix/Condicional | Canal actual | Canal correcte |
|---|---|---|---|---|
| `tipus_dislexia` | select (fonològica/superficial/mixta) | Condicional | **RES** | ORDRE |
| `grau` | select (lleu/moderat/sever) | Condicional | **RES** | PROPOSTA |
| `tipografia_adaptada` | bool | Fix | FE ✓ | FE ✓ correcte |
| `columnes_estretes` | bool | Fix | FE ✓ | FE ✓ correcte |

**Instruccions fixes**: H-07, H-08, A-21, D-06

**Variables que cal connectar**:
- `tipus_dislexia`:
  - "fonològica" → ORDRE: reforçar A-21 (descomposició compostes), afegir instrucció: "Evita encadenar prefixos i sufixos (des-en-vol-up-ar → desenvolupa)"
  - "superficial" → ORDRE: reforçar H-08 (alta freqüència encara més estricta), prioritzar paraules amb correspondència grafema-fonema regular
  - "mixta" → ORDRE: activar ambdues línies
- `grau`: si "sever" → PROPOSTA (suggerir DUA Accés) + activar D-01 (emojis) com a suport extra

### 3.5 Altes Capacitats (1 variable)

| Variable | Tipus | Fix/Condicional | Canal actual | Canal correcte |
|---|---|---|---|---|
| `tipus_capacitat` | select (global/talent_específic) | Condicional | **RES** | NARRATIVA |

**Instruccions fixes**: H-12, H-14+H-14b (fusionades), F-09, F-10 + suprimir A-01, A-03, A-05, A-07, A-08, A-11, A-16

**Variable que cal connectar**:
- `tipus_capacitat`: NARRATIVA ("talent específic en l'àmbit científic"). Pot guiar l'LLM a orientar les connexions interdisciplinars cap al talent. Impacte baix, no cal instrucció condicional.

**Nota**: faltaria afegir `doble_excepcionalitat` com a sub-variable per detectar 2e (actualment és una característica separada). Si `altes_capacitats.doble_excepcionalitat = true`, activar automàticament la característica `2e`.

### 3.6 Discapacitat Intel·lectual (1 variable)

| Variable | Tipus | Fix/Condicional | Canal actual | Canal correcte |
|---|---|---|---|---|
| `grau` | select (lleu/moderat/sever) | Condicional | **RES** | PROPOSTA + ORDRE |

**Instruccions fixes**: H-09, H-10, H-11, D-06

**Variable que cal connectar**:
- `grau`:
  - "lleu" → instruccions fixes, sense canvi
  - "moderat" → PROPOSTA (DUA Accés obligatori) + ORDRE: activar D-01 (emojis/pictogrames), reforçar H-09 (1 concepte per secció, no per paràgraf)
  - "sever" → PROPOSTA (DUA Accés + MECR pre-A1 o A1 màxim) + ORDRE: instruccions de DI sever (activar repetició en 3+ formats, concreció absoluta amb objectes tangibles)

### 3.7 TDL — Trastorn del Llenguatge (8 variables)

**EL CAS MÉS CRÍTIC**: 8 sub-variables, 0 connectades.

| Variable | Tipus | Fix/Condicional | Canal actual | Canal correcte |
|---|---|---|---|---|
| `modalitat` | select (comprensiu/expressiu/mixt) | Condicional | **RES** | NARRATIVA + ORDRE |
| `morfosintaxi` | bool | Condicional | **RES** | ORDRE |
| `semantica` | bool | Condicional | **RES** | ORDRE |
| `pragmatica` | bool | Condicional | **RES** | ORDRE |
| `discurs_narrativa` | bool | Condicional | **RES** | ORDRE |
| `comprensio_lectora` | bool | Condicional | **RES** | PROPOSTA |
| `grau` | select (lleu/moderat/sever) | Condicional | **RES** | PROPOSTA |
| `bilingue` | bool | Condicional | **RES** | NARRATIVA |

**Instruccions fixes**: H-16, H-17

**Variables que cal connectar** (totes):

- `modalitat`:
  - "comprensiu" → ORDRE: reforçar C-05 (glossari previ), A-01 (vocab freqüent), B-07 (advance organizer). La comprensió lectora és el problema central
  - "expressiu" → menys impacte en adaptació de TEXT (afecta producció, no recepció). NARRATIVA per a l'LLM
  - "mixt" → activar tot
- `morfosintaxi` (si afectada): ORDRE → reforçar A-13 (eliminar subordinades), A-10 (SVO), A-24 (present indicatiu), A-25 (formes simples), A-26 (evitar incisos)
- `semantica` (si afectada): ORDRE → reforçar A-01 (vocab freqüent), A-20/H-16 (densitat lèxica), A-06 (eliminar polisèmia), C-05 (glossari previ), A-02 (termes en negreta)
- `pragmatica` (si afectada): ORDRE → reforçar B-03 (frase tòpic), B-10 (transicions), A-14 (connectors explícits). Nota: comparteix barrera amb TEA (inferència)
- `discurs_narrativa` (si afectat): ORDRE → reforçar B-05 (estructura deductiva), B-06 (ordre cronològic), B-07 (advance organizer), B-08 (resum recapitulatiu)
- `comprensio_lectora` (si afectada): PROPOSTA → suggerir MECR -1 nivell, DUA Accés
- `grau`: si "sever" → PROPOSTA (DUA Accés) + intensificar totes les instruccions actives
- `bilingue`: NARRATIVA ("context bilingüe, risc de confusió diagnòstica TDL/bilingüisme")

### 3.8 TDC / Dispraxia (4 variables)

| Variable | Tipus | Fix/Condicional | Canal actual | Canal correcte |
|---|---|---|---|---|
| `grau` | select (lleu/moderat/sever) | Condicional | **RES** | PROPOSTA |
| `motricitat_fina` | bool | Condicional | **RES** | FE |
| `motricitat_grossa` | bool | Condicional | **RES** | FE (poc rellevant per text digital) |
| `acces_teclat` | bool | Fix | FE ✓ | FE ✓ correcte |

**Instruccions fixes**: B-02, B-09, H-19, B-04, B-14

**Variables que cal connectar**:
- `grau`: si "sever" → PROPOSTA (considerar suports extra, DUA Accés si afecta lectura)
- `motricitat_fina`: FE (botons grans, espai interactiu ample)
- `motricitat_grossa`: FE (poc impacte en adaptació textual digital)

### 3.9 Discapacitat Visual (1 variable)

| Variable | Tipus | Fix/Condicional | Canal actual | Canal correcte |
|---|---|---|---|---|
| `grau` | select (baixa_visió_moderada/greu/ceguesa) | Condicional | **RES** | FE + ORDRE |

**Instruccions fixes**: H-19

**Variable que cal connectar**:
- `grau`:
  - "baixa_visió_moderada" → FE (contrast alt, mida font gran)
  - "baixa_visió_greu" → FE (contrast alt, mida font molt gran) + ORDRE: reforçar H-19 (estructura semàntica estricta, zero info per color/posició)
  - "ceguesa" → FE (compatible lector pantalla) + ORDRE: H-19 intensificat + instrucció nova: "Descriu textualment qualsevol element visual (taules, esquemes) de forma seqüencial"

### 3.10 Discapacitat Auditiva (2 variables)

| Variable | Tipus | Fix/Condicional | Canal actual | Canal correcte |
|---|---|---|---|---|
| `comunicacio` | select (oral/LSC/bimodal) | Condicional | **RES** | ORDRE + NARRATIVA |
| `implant_coclear` | bool | Condicional | **RES** | NARRATIVA + PROPOSTA |

**Instruccions fixes**: H-20

**Variables que cal connectar**:
- `comunicacio`:
  - "oral" → menys simplificació necessària, H-20 s'aplica en grau lleu. NARRATIVA
  - "LSC" → ORDRE: intensificar H-20 (tractar com L2 de ple), activar simplificació sintàctica addicional (A-13 eliminació subordinades, A-07 una idea per frase)
  - "bimodal" → grau intermedi
- `implant_coclear`:
  - si true → NARRATIVA ("porta implant coclear, accés auditiu parcial") + PROPOSTA (menys simplificació necessària)
  - si false → mantenir intensitat plena de H-20

### 3.11 Discapacitat Motora (1 variable)

| Variable | Tipus | Fix/Condicional | Canal actual | Canal correcte |
|---|---|---|---|---|
| `acces_teclat` | bool | Fix | FE ✓ | FE ✓ correcte |

**Instruccions fixes LLM**: Cap rellevant. Gairebé tot és FE.

**Nota**: aquesta característica gairebé no afecta l'LLM. L'estructura semàntica (B-02) és l'únic impacte, i ja s'envia sempre.

### 3.12 Vulnerabilitat Socioeducativa (1 variable)

| Variable | Tipus | Fix/Condicional | Canal actual | Canal correcte |
|---|---|---|---|---|
| `sensibilitat_tematica` | bool | Condicional | **RES** | ORDRE |

**Instruccions fixes**: E-10, E-08/G-05 (fusionades), E-09

**Variable que cal connectar**:
- `sensibilitat_tematica`: si true → ORDRE: reforçar E-10 (sensibilitat traumàtica) + NARRATIVA ("evitar temes de violència, separació familiar, mort"). **BUG ACTUAL**: E-10 ja s'envia pel perfil, però la sub-variable no es consulta. Si `sensibilitat_tematica = false`, E-10 s'hauria de relaxar o no enviar.

### 3.13 Trastorn Emocional/Conductual (1 variable)

| Variable | Tipus | Fix/Condicional | Canal actual | Canal correcte |
|---|---|---|---|---|
| `sensibilitat_tematica` | bool | Condicional | **RES** | ORDRE |

**Instruccions fixes**: E-10, H-04, B-01, B-07

**Variable que cal connectar**:
- `sensibilitat_tematica`: idem vulnerabilitat (veure 3.12)

---

## 4. Matriu de matching: Variable → Instruccions

### 4.1 Llegenda

- **ACTIVA**: La variable activa la instrucció (no s'enviaria sense ella)
- **REFORÇA**: La instrucció ja s'envia (SEMPRE/PERFIL), la variable intensifica el text
- **INTENSIFICA**: Canvia el paràmetre numèric (ex: "3-5 frases" → "2-3 frases")

### 4.2 Variables del Nouvingut

| Variable | Valor | Efecte | Instruccions | Tipus |
|---|---|---|---|---|
| `L1` | (qualsevol) | Glossari bilingüe en L1 | G-01 | ACTIVA |
| `L1` | llengua romànica | Pistes etimològiques | E-11 | ACTIVA |
| `familia_linguistica` | "romanica" | Deduir L1 romànica | E-11 (backup de L1) | ACTIVA |
| `alfabet_llati` | false | Transliteració fonètica | G-03 | ACTIVA |
| `alfabet_llati` | false | Traducció consignes | G-02 (si mecr ≤ A1) | ACTIVA |
| `escolaritzacio_previa` | "no" / "parcial" | Glossari previ obligatori | C-05 | REFORÇA |
| `escolaritzacio_previa` | "no" / "parcial" | Advance organizer | B-07 | REFORÇA |
| `escolaritzacio_previa` | "no" | Suggerir DUA Accés | (proposta) | PROPOSTA |
| `mecr` | (valor) | Totes les instruccions NIVELL | A-12, A-13, A-20, etc. | ACTIVA |
| `calp` | "inicial" | Glossari previ | C-05 | REFORÇA |
| `calp` | "inicial" | Advance organizer | B-07 | REFORÇA |
| `calp` | "inicial" | Anticipació vocabulari | C-08 | REFORÇA |

### 4.3 Variables del TEA

| Variable | Valor | Efecte | Instruccions | Tipus |
|---|---|---|---|---|
| `nivell_suport` | 3 | Suggerir DUA Accés | (proposta) | PROPOSTA |
| `nivell_suport` | 2-3 | Estructura molt fixa | H-01 | INTENSIFICA |
| `comunicacio_oral` | "limitada" / "no_verbal" | Suport visual extra | D-01, D-02 | ACTIVA |
| `comunicacio_oral` | "no_verbal" | Simplificació com L2 | Aplicar regles tipus nouvingut | ACTIVA |

### 4.4 Variables del TDAH

| Variable | Valor | Efecte | Instruccions | Tipus |
|---|---|---|---|---|
| `presentacio` | (qualsevol) | Context per a l'LLM | — | NARRATIVA |
| `grau` | "sever" | Micro-blocs més curts (2-3 frases) | H-04 | INTENSIFICA |
| `grau` | "sever" | Suggerir DUA Accés | (proposta) | PROPOSTA |
| `baixa_memoria_treball` | true | Chunking 3 elements (no 5) | C-04 | INTENSIFICA |
| `baixa_memoria_treball` | true | 1-2 conceptes/paràgraf (no 2-3) | C-01 | INTENSIFICA |
| `baixa_memoria_treball` | true | Resum recapitulatiu | B-08 | ACTIVA |
| `fatiga_cognitiva` | true | Text retallat al 60-70% | *NOVA INSTRUCCIÓ* | ACTIVA |
| `fatiga_cognitiva` | true | Suggerir DUA Accés | (proposta) | PROPOSTA |

### 4.5 Variables de la Dislèxia

| Variable | Valor | Efecte | Instruccions | Tipus |
|---|---|---|---|---|
| `tipus_dislexia` | "fonologica" | Prioritzar descomposició compostes | A-21, H-07 | REFORÇA |
| `tipus_dislexia` | "superficial" | Prioritzar alta freqüència estricta | H-08 | REFORÇA |
| `tipus_dislexia` | "mixta" | Activar ambdues línies | A-21, H-07, H-08 | REFORÇA |
| `grau` | "sever" | Suport visual extra | D-01 | ACTIVA |
| `grau` | "sever" | Suggerir DUA Accés | (proposta) | PROPOSTA |
| `tipografia_adaptada` | true | CSS dislèxia | I-01, I-02, I-05 | FE |
| `columnes_estretes` | true | CSS columna estreta | I-03 | FE |

### 4.6 Variables d'Altes Capacitats

| Variable | Valor | Efecte | Instruccions | Tipus |
|---|---|---|---|---|
| `tipus_capacitat` | (qualsevol) | Context per a l'LLM | — | NARRATIVA |

### 4.7 Variables de DI

| Variable | Valor | Efecte | Instruccions | Tipus |
|---|---|---|---|---|
| `grau` | "moderat" | DUA Accés + pictogrames | D-01 | ACTIVA |
| `grau` | "moderat" | 1 concepte per secció | H-09 | INTENSIFICA |
| `grau` | "sever" | DUA Accés + MECR ≤ A1 | (proposta) | PROPOSTA |
| `grau` | "sever" | Repetició en 3+ formats | H-11 | INTENSIFICA |
| `grau` | "sever" | Concreció absoluta (objectes tangibles) | H-10 | INTENSIFICA |

### 4.8 Variables del TDL (EL MAPA MÉS COMPLEX)

| Variable | Valor | Efecte | Instruccions | Tipus |
|---|---|---|---|---|
| `modalitat` | "comprensiu" | Glossari previ + vocab freqüent | C-05, A-01, B-07 | REFORÇA |
| `modalitat` | "expressiu" | Menys impacte en text | — | NARRATIVA |
| `modalitat` | "mixt" | Tot | C-05, A-01, B-07 | REFORÇA |
| `morfosintaxi` | true | Eliminar subordinades | A-13 (MECR ≤ A2) | REFORÇA |
| `morfosintaxi` | true | Ordre SVO estricte | A-10 | REFORÇA |
| `morfosintaxi` | true | Present indicatiu | A-24 | ACTIVA |
| `morfosintaxi` | true | Formes verbals simples | A-25 | ACTIVA |
| `morfosintaxi` | true | Evitar incisos | A-26 | ACTIVA |
| `semantica` | true | Vocabulari freqüent intens | A-01 | REFORÇA |
| `semantica` | true | Densitat lèxica mínima | H-16 | REFORÇA |
| `semantica` | true | Eliminar polisèmia | A-06 | REFORÇA |
| `semantica` | true | Glossari previ | C-05 | ACTIVA |
| `semantica` | true | Termes en negreta | A-02 | REFORÇA |
| `pragmatica` | true | Frase tòpic | B-03 | REFORÇA |
| `pragmatica` | true | Transicions explícites | B-10 | REFORÇA |
| `pragmatica` | true | Connectors explícits | A-14 | REFORÇA |
| `discurs_narrativa` | true | Estructura deductiva | B-05 | REFORÇA |
| `discurs_narrativa` | true | Ordre cronològic | B-06 | REFORÇA |
| `discurs_narrativa` | true | Advance organizer | B-07 | ACTIVA |
| `discurs_narrativa` | true | Resum recapitulatiu | B-08 | ACTIVA |
| `comprensio_lectora` | true | Suggerir MECR -1 | (proposta) | PROPOSTA |
| `comprensio_lectora` | true | Suggerir DUA Accés | (proposta) | PROPOSTA |
| `grau` | "sever" | Intensificar tot | totes les actives | INTENSIFICA |
| `grau` | "sever" | DUA Accés | (proposta) | PROPOSTA |
| `bilingue` | true | Context diagnòstic | — | NARRATIVA |

### 4.9 Variables de TDC

| Variable | Valor | Efecte | Instruccions | Tipus |
|---|---|---|---|---|
| `grau` | "sever" | Considerar suports extra | (proposta) | PROPOSTA |
| `motricitat_fina` | true | Botons grans, espai interactiu | — | FE |
| `motricitat_grossa` | true | (poc impacte text digital) | — | FE |
| `acces_teclat` | true | Navegació teclat | I-07 | FE |

### 4.10 Variables de Disc. Visual

| Variable | Valor | Efecte | Instruccions | Tipus |
|---|---|---|---|---|
| `grau` | "baixa_visio_moderada" | Contrast alt, font gran | I-06 | FE |
| `grau` | "baixa_visio_greu" | H-19 intensificat | H-19 | REFORÇA |
| `grau` | "ceguesa" | Descriure elements visuals | *NOVA INSTRUCCIÓ* | ACTIVA |
| `grau` | "ceguesa" | Compatible lector pantalla | I-07, I-08 | FE |

### 4.11 Variables de Disc. Auditiva

| Variable | Valor | Efecte | Instruccions | Tipus |
|---|---|---|---|---|
| `comunicacio` | "oral" | H-20 grau lleu | H-20 | REFORÇA (lleu) |
| `comunicacio` | "LSC" | Simplificació com L2 | A-13, A-07 | ACTIVA |
| `comunicacio` | "LSC" | H-20 intensificat | H-20 | INTENSIFICA |
| `comunicacio` | "bimodal" | Grau intermedi | H-20 | REFORÇA |
| `implant_coclear` | true | Menys simplificació | H-20 | ATENUA |
| `implant_coclear` | false | Mantenir intensitat | H-20 | — |

### 4.12 Variables de Vulnerabilitat

| Variable | Valor | Efecte | Instruccions | Tipus |
|---|---|---|---|---|
| `sensibilitat_tematica` | true | Sensibilitat traumàtica | E-10 | REFORÇA |
| `sensibilitat_tematica` | false | Relaxar E-10 | E-10 | ATENUA o NO ENVIAR |

### 4.13 Variables de Trastorn Emocional

| Variable | Valor | Efecte | Instruccions | Tipus |
|---|---|---|---|---|
| `sensibilitat_tematica` | true | Sensibilitat traumàtica | E-10 | REFORÇA |
| `sensibilitat_tematica` | false | Relaxar E-10 | E-10 | ATENUA o NO ENVIAR |

---

## 5. Anàlisi d'eficiència: quantes instruccions arriben al prompt?

### 5.1 Cinc casos tipus

Per avaluar si el sistema és eficient, simulem el recompte d'instruccions per a 5 casos reals habituals:

#### Cas 1: Nouvingut àrab, A1, ESO, text explicatiu

**Perfil**: nouvingut (L1=àrab, alfabet_llati=false, mecr=A1, calp=inicial)
**Paràmetres**: MECR sortida=A1, DUA=Accés

| Capa | Instruccions | Quantes |
|---|---|---|
| SEMPRE | A-02 a A-19 (menys A-12, A-13, A-20) + B-01 a B-14 + C-03, C-04 + E-01, E-05, E-06 | ~24 |
| NIVELL (A1) | A-12(A1), A-13(A1), A-20, A-22, A-23, A-24, A-25, A-26, B-07, B-08, C-01(A1), C-02, C-05, C-06, C-08, E-02(A1), E-07, G-06(A1) | ~18 |
| PERFIL (nouvingut) | A-21, E-08, E-09, G-01, G-03, G-05 | 6 |
| PERFIL COND. | G-02 (mecr_low), E-11❌ (àrab no romànic) | 1 |
| **TOTAL** | | **~49** |

**PROBLEMA**: 49 instruccions al prompt. Molt per sobre del rang 7-12 d'alta fiabilitat. Fins i tot per sobre de 20 (degradació notable).

#### Cas 2: TDAH moderat, B1, primària, text narratiu

**Perfil**: tdah (grau=moderat)
**Paràmetres**: MECR sortida=B1, DUA=Core

| Capa | Instruccions | Quantes |
|---|---|---|
| SEMPRE | (totes les universals) | ~24 |
| NIVELL (B1) | A-12(B1), A-13(B1), A-26, B-08, C-01(B1), C-02, C-06, E-02(B1), E-07, E-12, G-06(B1) | ~11 |
| PERFIL (tdah) | H-04, H-05, H-06, B-13, F-06 | 5 |
| **TOTAL** | | **~40** |

**PROBLEMA**: 40 instruccions. Massa.

#### Cas 3: Altes capacitats, B2, batxillerat

**Perfil**: altes_capacitats
**Paràmetres**: MECR sortida=B2, DUA=Enriquiment

| Capa | Instruccions | Quantes |
|---|---|---|
| SEMPRE (amb supressions) | (24 − 7 suprimides) | ~17 |
| NIVELL (B2) | A-12(B2), A-13(B2), C-01(B2), E-02(B2), E-12, G-06(B2) | ~6 |
| PERFIL (AC) | H-12, H-14+H-14b, F-09, F-10 | 4 |
| **TOTAL** | | **~27** |

**PROBLEMA**: 27 instruccions. Encara massa.

#### Cas 4: TEA + Dislèxia, A2, ESO (comorbiditat)

**Perfil**: tea + dislexia (tipus=fonologica)
**Paràmetres**: MECR sortida=A2, DUA=Accés

| Capa | Instruccions | Quantes |
|---|---|---|
| SEMPRE | ~24 |
| NIVELL (A2) | ~14 |
| PERFIL (tea) | H-01, H-02, H-03 | 3 |
| PERFIL (dislèxia) | H-07, H-08, A-21, D-06 | 4 |
| **TOTAL** | | **~45** |

**PROBLEMA GREU**: 45 instruccions amb comorbiditat.

#### Cas 5: DI sever, pre-A1, primària

**Perfil**: di (grau=sever)
**Paràmetres**: MECR sortida=pre-A1, DUA=Accés

| Capa | Instruccions | Quantes |
|---|---|---|
| SEMPRE | ~24 |
| NIVELL (pre-A1) | ~18 |
| PERFIL (DI) | H-09, H-10, H-11, D-06 | 4 |
| **TOTAL** | | **~46** |

### 5.2 Diagnòstic: el coll d'ampolla són les instruccions SEMPRE

| Capa | Rang | Problema |
|---|---|---|
| **SEMPRE** | **24 instruccions** | **Massa. Hauria de ser 12-15 màx.** |
| NIVELL | 6-18 segons MECR | Acceptable per pre-A1/A1, massa per A2+ |
| PERFIL | 3-7 segons cas | Correcte |
| TOTAL | **27-49** | **2-5x per sobre del rang òptim (7-12)** |

### 5.3 Proposta de reducció

**Estratègia**: convertir instruccions SEMPRE en NIVELL (només s'envien per MECR baixos) o agrupar-les en macrodirectives.

**Opcions per reduir les SEMPRE de 24 a ~12**:

| Instruccions a moure de SEMPRE → NIVELL (≤A2) | Justificació |
|---|---|
| A-06 (eliminar polisèmia) | A B2 no cal prohibir polisèmia |
| A-08 (veu activa) | A B2 la passiva és legítima |
| A-09 (subjecte explícit) | A B2 l'el·lipsi és correcta |
| A-10 (ordre SVO) | A B2 les inversions són legítimes |
| A-11 (puntuació simplificada) | A B2 el punt i coma és acceptable |
| A-17 (evitar negacions múltiples) | A B2 no és problem real |
| B-04 (llistes) | No sempre cal, depèn del text |
| B-05 (estructura deductiva) | Limita gèneres (la narració no és deductiva) |
| B-06 (ordre cronològic) | Només aplica a processos |
| B-09 (numerar passos) | Només aplica a seqüències |
| B-11 (salt línia entre idees) | Format, no contingut |
| B-14 (taules) | Complement, no universal |

**Resultat**: SEMPRE passaria de 24 a **12 instruccions**. Les 12 restants passen a NIVELL (≤A2 o ≤B1).

**Instruccions SEMPRE que queden (12 nucli)**:

1. A-01: Vocabulari freqüent
2. A-02: Termes tècnics en negreta + definició
3. A-03: Repetició lèxica (no sinònims)
4. A-04: Referents pronominals explícits
5. A-07: Una idea per frase
6. A-14: Connectors explícits
7. A-15: Scaffolding decreixent (Vygotsky)
8. A-16: Desnominalització (Halliday)
9. B-01: Paràgrafs curts
10. B-02: Blocs amb títol descriptiu
11. B-03: Frase tòpic
12. B-10: Transicions entre seccions
+ E-01, E-05, E-06, C-03 (qualitat/rigor — es poden posar a la CAPA 1 Identitat)

### 5.4 Simulació post-reducció

Amb la redistribució, els 5 casos quedarien:

| Cas | Abans | Després | Dins rang? |
|---|---|---|---|
| Nouvingut àrab A1 | 49 | ~25 | ⚠️ Millorat però encara alt |
| TDAH moderat B1 | 40 | ~22 | ⚠️ Millorat |
| AC B2 | 27 | ~18 | ⚠️ Acceptable |
| TEA+Dislèxia A2 | 45 | ~26 | ⚠️ Millorat |
| DI sever pre-A1 | 46 | ~28 | ⚠️ Millorat |

**Conclusió**: la redistribució SEMPRE→NIVELL millora (~40% menys), però no és suficient per arribar al rang 7-12.

### 5.5 Solució real: macrodirectives agrupades

Per arribar al rang 7-12, cal **agrupar instruccions en macrodirectives** en lloc d'enviar-les individualment:

En lloc d'enviar:
```
A-01: Usa vocabulari freqüent.
A-02: Termes tècnics en negreta amb definició.
A-03: Repetició lèxica coherent, no sinònims.
A-04: Referents pronominals explícits.
A-05: Elimina expressions idiomàtiques.
A-06: Elimina polisèmia.
```

Enviar:
```
LÈXIC: Usa vocabulari freqüent. Termes tècnics en **negreta** amb definició. Un terme = un concepte (no sinònims). Referents pronominals explícits. Elimina expressions idiomàtiques i polisèmia.
```

Amb aquest enfocament:

| Macrodirectiva | Instruccions agrupades | Compta com |
|---|---|---|
| LÈXIC | A-01 a A-06, A-15, A-16 | 1 directiva |
| SINTAXI | A-07 a A-13 | 1 directiva |
| ESTRUCTURA | B-01 a B-03, B-10 | 1 directiva |
| QUALITAT | E-01, E-05, E-06, C-03 | 1 directiva |
| NIVELL MECR | (bloc compacte del nivell) | 1 directiva |
| PERFIL | (bloc compacte del perfil) | 1-2 directives |
| PERSONA | (narrativa) | 1 directiva |

**Total efectiu**: 6-9 macrodirectives → **dins del rang 7-12**.

### 5.6 Simulació amb macrodirectives

| Cas | Macrodirectives | Dins rang? |
|---|---|---|
| Nouvingut àrab A1 | LÈXIC + SINTAXI + ESTRUCTURA + QUALITAT + MECR(A1) + PERFIL(nouvingut) + PERSONA | **7** ✓ |
| TDAH moderat B1 | LÈXIC + SINTAXI + ESTRUCTURA + QUALITAT + MECR(B1) + PERFIL(tdah) + PERSONA | **7** ✓ |
| AC B2 | LÈXIC(reduït) + ESTRUCTURA + QUALITAT + MECR(B2) + PERFIL(AC) + PERSONA | **6** ✓ |
| TEA+Dislèxia A2 | LÈXIC + SINTAXI + ESTRUCTURA + QUALITAT + MECR(A2) + PERFIL(tea) + PERFIL(dislèxia) + PERSONA | **8** ✓ |
| DI sever pre-A1 | LÈXIC + SINTAXI + ESTRUCTURA + QUALITAT + MECR(pre-A1) + PERFIL(DI) + PERSONA | **7** ✓ |

**Nota important**: les macrodirectives agregen text, no eliminen instruccions. El contingut complet segueix al prompt, però l'LLM el processa com a 7-8 blocs coherents en lloc de 40-50 regles atòmiques desconnectades.

---

## 6. Protocol de resolució de conflictes

### 6.1 Conflictes MECR vs DUA vs LF

Ja documentat a arquitectura_prompt_v2.md §6.6. Jerarquia:

```
MECR (límit dur) > DUA (intensitat) > LF (intensificador d'Accés)
```

### 6.2 Conflictes entre perfils (NO documentat — **NOU**)

| Conflicte | Exemple | Resolució |
|---|---|---|
| Simplificar vs NO simplificar | TEA + Altes Capacitats | **AC guanya en contingut, TEA guanya en format**: mantenir complexitat conceptual, però amb estructura predictible i zero implicitura |
| Variació vs Predictibilitat | TDAH (vol variació) + TEA (vol predictibilitat) | **TEA guanya**: la predictibilitat és una necessitat més fonamental. Variació DINS de l'estructura fixa (alternar lectura/esquema, però sempre en el mateix ordre) |
| Macro-blocs vs Micro-blocs | DI (1 concepte per bloc) + TDAH (micro-blocs curts) | **Compatible**: 1 concepte per micro-bloc de 2-3 frases. Cap conflicte real |
| Densitat visual alta vs baixa | TDAH (negretes, icones, colors) + Dislèxia (reduir densitat visual) | **Dislèxia guanya en tipografia**, TDAH guanya en senyalització: negretes sí, però amb fons neutre i sense italics |
| Vocabulari ric vs freqüent | AC (mantenir riquesa) + Nouvingut (vocab freqüent) | **Perfil 2e**: mantenir riquesa lèxica + glossari bilingüe complet. No simplificar, però explicar |

### 6.3 Regla general de conflictes entre perfils

```
1. ACCESSIBILITAT > ENRIQUIMENT (si cal triar, que sigui accessible)
2. FORMAT adaptable, CONTINGUT no negociable
3. El perfil amb barrera nuclear més severa (escala 0-4 del mapa de barreres) guanya en la seva dimensió
4. Si dubte, enviar AMBDUES instruccions i deixar que l'LLM equilibri (millor redundància que omissió)
```

---

## 7. Arquitectura de macrodirectives (IMPLEMENTAT)

### 7.1 Què és una macrodirectiva

Una macrodirectiva és l'agrupació de 3-15 instruccions individuals (atòmiques) en un sol bloc temàtic coherent que l'LLM processa com una unitat.

```
CODI INTERN (traçabilitat)              PROMPT LLM (el que veu el model)
────────────────────────────            ────────────────────────────────
LÈXIC [A-01, A-02, A-03,        →      **LÈXIC**: Usa vocabulari freqüent.
       A-04, A-05, A-14,                Termes tècnics en negreta amb
       A-15, A-16, A-18, A-19]          definició. Un terme = un concepte
                                        (no sinònims). Referents pronominals
                                        explícits. Elimina idiomàtiques...

SINTAXI [A-07, A-12, A-13]      →      **SINTAXI**: Una idea per frase.
                                        Màxim 8-12 paraules (A2). Coordinades
                                        simples, NO subordinades complexes.
```

- **L'LLM NO veu IDs** (A-01, A-02...) — només prosa agrupada
- **El codi INTERN SÍ conserva IDs** — per logs, auditoria i traçabilitat
- El contingut de les instruccions no canvia, només l'organització

### 7.2 Les 9 macrodirectives

| # | ID intern | Etiqueta al prompt | Instruccions possibles | Sempre/Variable |
|---|---|---|---|---|
| 1 | LEXIC | **LÈXIC** | A-01 a A-06, A-14 a A-23 | Nucli fix (8) + condicionals per MECR/perfil |
| 2 | SINTAXI | **SINTAXI** | A-07 a A-13, A-24 a A-26 | Nucli fix (1: A-07) + condicionals per MECR |
| 3 | ESTRUCTURA | **ESTRUCTURA** | B-01 a B-14 | Nucli fix (4) + condicionals per MECR/perfil |
| 4 | COGNITIU | **SUPORT COGNITIU** | C-01, C-02, C-04 a C-08, A-27 | Tots condicionals per MECR/perfil |
| 5 | QUALITAT | **RIGOR CURRICULAR** | C-03, E-01 a E-12 | Nucli fix (4: C-03, E-01, E-05, E-06) + condicionals |
| 6 | MULTIMODAL | **MULTIMODALITAT** | D-01 a D-06, H-21 | Tots condicionals (complement/perfil) |
| 7 | AVALUACIO | **AVALUACIÓ I COMPRENSIÓ** | F-06, F-09, F-10 | Tots condicionals (perfil) |
| 8 | PERSONALITZACIO | **PERSONALITZACIÓ LINGÜÍSTICA** | G-01 a G-06 | Condicionals (nouvingut/MECR) |
| 9 | PERFIL | **ADAPTACIONS PER PERFIL** | H-01 a H-22 | Condicionals (perfil actiu) |

### 7.3 Com es construeix una macrodirectiva (procés)

```
1. get_instructions() filtra el CATALOG segons perfil + MECR + complements
   → Resultat: llista d'instruccions actives, cadascuna amb camp "macro"

2. Les instruccions actives s'agrupen per "macro"
   → Exemple: A-01 (macro=LEXIC), A-02 (macro=LEXIC) → grup LEXIC

3. Dins de cada grup, es concatenen els textos en prosa
   → "Usa vocabulari freqüent. Termes tècnics en negreta amb definició."

4. Cada grup es presenta amb etiqueta en negreta
   → "**LÈXIC**: Usa vocabulari freqüent. Termes tècnics en..."

5. L'audit log conserva els IDs:
   → "LÈXIC [A-01, A-02, A-14, A-15, A-18, A-19] (6 instr.)"
```

### 7.4 Resultats reals (post-implementació)

Simulació amb els 5 casos tipus. **Instruccions individuals → macrodirectives**:

| Cas | Instruccions individuals | Macrodirectives (blocs LLM) | Dins rang 7-12? |
|---|---|---|---|
| Nouvingut àrab A1 | 56 | **6 blocs** | ✓ |
| TDAH moderat B1 (baixa mem. treball) | 47 | **8 blocs** | ✓ |
| Altes Capacitats B2 | 25 | **8 blocs** | ✓ |
| TEA + Dislèxia fonològica A2 | 55 | **8 blocs** | ✓ |
| DI sever pre-A1 | 55 | **8 blocs** | ✓ |

### 7.5 Exemple real de prompt generat (TDAH moderat B1)

```
**LÈXIC**: Usa vocabulari freqüent. Termes tècnics en negreta amb definició.
Un terme = un concepte (no sinònims). Referents pronominals explícits.
Elimina idiomàtiques i sentit figurat. Elimina polisèmia. Connectors
explícits. Scaffolding decreixent. Desnominalitza. Evita negacions
múltiples. Dates completes. Sigles explicades.

**SINTAXI**: Una idea per frase. Veu activa. Subjecte explícit. Ordre SVO.
Puntuació simplificada. Màxim 12-18 paraules per frase. Subordinades
simples (que, quan, si). Evita incisos parentètics llargs.

**ESTRUCTURA**: Paràgrafs curts. Títols descriptius. Frase tòpic.
Llistes. Estructura deductiva. Ordre cronològic. Resum recapitulatiu.
Numera passos. Transicions. Indicadors progrés [X de Y]. Taules.

**SUPORT COGNITIU**: Màxim 2 conceptes nous per paràgraf. Reforç
immediat. Chunking estricte: màxim 3 elements (memòria treball limitada).
Analogies quotidianes.

**RIGOR CURRICULAR**: Coherència Mayer. Nucli terminològic intocable.
Exactitud científica. Causalitat completa. Exemple per concepte abstracte.
Contra-exemples.

**AVALUACIÓ**: Preguntes comprensió intercalades cada 2-3 paràgrafs.

**PERSONALITZACIÓ**: To proper i acadèmic bàsic.

**ADAPTACIONS TDAH**: Micro-blocs 3-5 frases amb objectiu explícit.
Retroalimentació visual progrés. Variació dins text.
```

### 7.6 Exemple d'audit log (NO visible per l'LLM)

```
=== AUDITORIA INSTRUCCIONS ===
Perfils actius: tdah
MECR: B1 | DUA: Core
Total instruccions: 47 en 8 macrodirectives
Suprimides: 0

  LÈXIC [A-01, A-02, A-03, A-04, A-05, A-06, A-14, A-15, A-16,
         A-17, A-18, A-19] (12 instr.)
  SINTAXI [A-07, A-08, A-09, A-10, A-11, A-12, A-13, A-26] (8 instr.)
  ESTRUCTURA [B-01, B-02, B-03, B-04, B-05, B-06, B-08, B-09,
              B-10, B-13, B-14] (11 instr.)
  SUPORT COGNITIU [C-01, C-02, C-04, C-06] (4 instr.)
  RIGOR CURRICULAR [C-03, E-01, E-02, E-05, E-06, E-07, E-12] (7 instr.)
  AVALUACIÓ [F-06] (1 instr.)
  PERSONALITZACIÓ [G-06] (1 instr.)
  PERFIL [H-04, H-05, H-06] (3 instr.)
```

### 7.7 Fitxers que implementen les macrodirectives

| Fitxer | Rol |
|---|---|
| `instruction_catalog.py` | Defineix MACRODIRECTIVES (composició) + CATALOG (cada instrucció amb camp `macro`) |
| `instruction_filter.py` | `get_instructions()` filtra i agrupa per macro. `format_instructions_for_prompt()` genera text net. `format_audit_log()` genera traçabilitat amb IDs |

---

## 8. Noves instruccions (IMPLEMENTADES a instruction_catalog.py)

| ID | Text | Activació | Sub-variable que l'activa |
|---|---|---|---|
| **A-27** | "Retalla el text al 60-70% de l'extensió original, prioritzant el nucli curricular." | PERFIL: tdah, di | `fatiga_cognitiva=true` O `grau=sever` |
| **H-21** | "Descriu textualment qualsevol element visual del text original de forma seqüencial i completa." | PERFIL: disc_visual | `grau=ceguesa` |
| **H-22** | "Evita encadenar prefixos i sufixos. Reformula: 'descontextualitzar' → 'treure del context'." | PERFIL: dislexia | `tipus_dislexia=fonologica` o `mixta` |

---

## 9. Resum: canal de cada sub-variable (les 36)

### 9.1 Taula resum completa (actualitzada post-implementació)

| # | Característica | Variable | Canal | Estat |
|---|---|---|---|---|
| 1 | nouvingut | L1 | ORDRE + NARRATIVA | ✓ Connectat (G-01, E-11) |
| 2 | nouvingut | familia_linguistica | PROPOSTA | ✓ **NOU** (E-11 via L1_romanica) |
| 3 | nouvingut | alfabet_llati | ORDRE | ✓ Connectat (G-03) |
| 4 | nouvingut | escolaritzacio_previa | NARRATIVA + PROPOSTA | ⏳ Pendent (narrativa) |
| 5 | nouvingut | mecr | PROPOSTA | ✓ Connectat (MECR sortida) |
| 6 | nouvingut | calp | NARRATIVA + PROPOSTA | ⏳ Pendent (narrativa) |
| 7 | tea | nivell_suport | NARRATIVA + PROPOSTA | ⏳ Pendent (narrativa) |
| 8 | tea | comunicacio_oral | NARRATIVA + ORDRE | ⏳ Pendent (narrativa) |
| 9 | tdah | presentacio | NARRATIVA | ⏳ Pendent (narrativa) |
| 10 | tdah | grau | PROPOSTA + ORDRE | ✓ **NOU** (intensifica H-04) |
| 11 | tdah | baixa_memoria_treball | ORDRE | ✓ **NOU** (intensifica C-01, C-04) |
| 12 | tdah | fatiga_cognitiva | ORDRE + PROPOSTA | ✓ **NOU** (activa A-27) |
| 13 | dislexia | tipus_dislexia | ORDRE | ✓ **NOU** (activa H-22 si fonològica) |
| 14 | dislexia | grau | PROPOSTA | ⏳ Pendent (proposta DUA) |
| 15 | dislexia | tipografia_adaptada | FE | ✓ Connectat |
| 16 | dislexia | columnes_estretes | FE | ✓ Connectat |
| 17 | altes_cap | tipus_capacitat | NARRATIVA | ⏳ Pendent (narrativa) |
| 18 | di | grau | PROPOSTA + ORDRE | ✓ **NOU** (activa A-27 si sever) |
| 19 | tdl | modalitat | NARRATIVA + ORDRE | ⏳ Pendent (narrativa + ordres) |
| 20 | tdl | morfosintaxi | ORDRE | ⏳ Pendent (ordres condicionals) |
| 21 | tdl | semantica | ORDRE | ⏳ Pendent (ordres condicionals) |
| 22 | tdl | pragmatica | ORDRE | ⏳ Pendent (ordres condicionals) |
| 23 | tdl | discurs_narrativa | ORDRE | ⏳ Pendent (ordres condicionals) |
| 24 | tdl | comprensio_lectora | PROPOSTA | ⏳ Pendent (proposta MECR) |
| 25 | tdl | grau | PROPOSTA | ⏳ Pendent (proposta DUA) |
| 26 | tdl | bilingue | NARRATIVA | ⏳ Pendent (narrativa) |
| 27 | tdc | grau | PROPOSTA | ⏳ Pendent (proposta) |
| 28 | tdc | motricitat_fina | FE | ⏳ Pendent (FE) |
| 29 | tdc | motricitat_grossa | FE | ⏳ Pendent (FE, mantingut per ampliació futura) |
| 30 | tdc | acces_teclat | FE | ✓ Connectat |
| 31 | disc_visual | grau | FE + ORDRE | ✓ **NOU** (activa H-21 si ceguesa) |
| 32 | disc_auditiva | comunicacio | ORDRE + NARRATIVA | ✓ **NOU** (intensifica H-20) |
| 33 | disc_auditiva | implant_coclear | NARRATIVA + PROPOSTA | ✓ **NOU** (atenua H-20) |
| 34 | disc_motora | acces_teclat | FE | ✓ Connectat |
| 35 | vulnerabilitat | sensibilitat_tematica | ORDRE | ✓ **NOU** (condiciona E-10) |
| 36 | trastorn_emocional | sensibilitat_tematica | ORDRE | ✓ **NOU** (condiciona E-10) |

### 9.2 Distribució per canal (actualitzada)

| Canal | Variables | Connectades | Pendents |
|---|---|---|---|
| ORDRE (instruccions al prompt) | 14 | **12** | 2 (TDL sub-variables) |
| NARRATIVA (persona-audience) | 12 | 1 | **11** (pendent `build_persona_narrative()`) |
| PROPOSTA (MECR/DUA automàtic) | 13 | 2 | **11** (pendent `suggest_dua_mecr()`) |
| FE (CSS/JS) | 7 | 5 | 2 (tdc motricitats) |
| **Progrés** | | **20 de 36 (56%)** | **16 pendents** |

**De 15 connectades (42%) a 20 connectades (56%)**. Les 16 pendents són canal NARRATIVA (funció `build_persona_narrative()`) i PROPOSTA (`suggest_dua_mecr()`), que requereixen canvis a `server.py`.

---

## 10. Accions derivades (prioritzades)

### P0 — FET ✓

| # | Acció | Estat |
|---|---|---|
| 1 | Agrupar instruccions en macrodirectives | ✓ `instruction_filter.py` reescrit |
| 2 | Eliminar duplicats (E-04, H-13, E-08+G-05, H-14+H-14b) | ✓ `instruction_catalog.py` actualitzat |
| 3 | Moure 12 instruccions SEMPRE → NIVELL(≤A2/B1) | ✓ Implementat |
| 4 | Connectar sensibilitat_tematica | ✓ E-10 ara mira sub-variable |
| 5 | Crear 3 noves instruccions (A-27, H-21, H-22) | ✓ Implementades |
| 6 | Connectar 9 variables ORDRE (tdah, dislèxia, DI, disc_visual, disc_auditiva) | ✓ Intensificació i activació condicional |
| 7 | Supressió intel·ligent per perfil redundant | ✓ `suppress_if_profile` implementat |

### P1 — Pròxim pas

| # | Acció | Fitxer(s) | Descripció |
|---|---|---|---|
| 8 | **Generar narrativa persona-audience** | server.py | Funció `build_persona_narrative()` que construeix "alumne de 14 anys que..." a partir de les 11 variables NARRATIVA |
| 9 | **Implementar PROPOSTA automàtica** | server.py + ui/app.js | Funció `suggest_dua_mecr()`: quan di.grau="sever" o tdl.comprensio_lectora=true → suggerir DUA Accés / MECR -1 |
| 10 | **Connectar sub-variables TDL** (6 pendents) | instruction_catalog.py + instruction_filter.py | Les 6 sub-variables de TDL (morfosintaxi, semantica, pragmatica, discurs, comprensio_lectora, grau) necessiten instruccions condicionals dedicades |
| 11 | **Integrar macrodirectives a server.py** | server.py | Substituir `build_system_prompt()` actual per usar `get_instructions()` + `format_instructions_for_prompt()` |

### P2 — Mitjà termini

| # | Acció | Fitxer(s) | Descripció |
|---|---|---|---|
| 12 | Implementar regles de conflicte entre perfils | instruction_filter.py | Lògica per resoldre TEA+TDAH, AC+nouvingut, etc. (secció 6) |
| 13 | Few-shot examples per macrodirectiva | fitxer separat | 1 mini-exemple per nivell MECR × gènere |
| 14 | Verificació post-processament (J-01, J-02) | server.py | Verificar longitud frases i paraules prohibides amb Python |

---

## 10. Composicio de les macrodirectives

### 10.1 Concepte

Una **macrodirectiva** es un bloc tematic que agrupa instruccions atomiques relacionades. En comptes d'enviar a l'LLM una llista plana de 30-50 instruccions (on es perd el context i l'ordre d'importancia), les macrodirectives organitzen les instruccions en seccions coherents amb un encapcalament clar.

Cada macrodirectiva te:
- **Clau interna** (LEXIC, SINTAXI...): per al codi i els logs.
- **Label** (Lexic, Sintaxi...): text net que apareix al prompt de l'LLM.
- **Ordre**: posicio fixa dins del prompt (1 = primer bloc, 9 = ultim).
- **Instruccions possibles**: llista d'IDs que poden formar part del bloc. El filtre (instruction_filter.py) selecciona quines s'activen segons el perfil i les variables del docent.

### 10.2 Taula completa de macrodirectives

| # | Clau interna | Label al prompt | IDs que la componen |
|---|---|---|---|
| 1 | LEXIC | LEXIC | A-01, A-02, A-03, A-04, A-05, A-06, A-14, A-15, A-16, A-17, A-18, A-19, A-20, A-21, A-22, A-23 |
| 2 | SINTAXI | SINTAXI | A-07, A-08, A-09, A-10, A-11, A-12, A-13, A-24, A-25, A-26 |
| 3 | ESTRUCTURA | ESTRUCTURA | B-01, B-02, B-03, B-04, B-05, B-06, B-07, B-08, B-09, B-10, B-11, B-13, B-14 |
| 4 | COGNITIU | SUPORT COGNITIU | C-01, C-02, C-04, C-05, C-06, C-08, A-27 |
| 5 | QUALITAT | RIGOR CURRICULAR | C-03, E-01, E-02, E-05, E-06, E-07, E-08, E-09, E-10, E-11, E-12 |
| 6 | MULTIMODAL | MULTIMODALITAT | D-01, D-02, D-03, D-06, H-21 |
| 7 | AVALUACIO | AVALUACIO I COMPRENSIO | F-06, F-09, F-10 |
| 8 | PERSONALITZACIO | PERSONALITZACIO LINGUEISTICA | G-01, G-02, G-03, G-06 |
| 9 | PERFIL | ADAPTACIONS PER PERFIL | H-01 a H-22 (totes les instruccions H-) |

**Notes**:
- B-12 esta exclosa d'ESTRUCTURA (duplicada o obsoleta).
- H-21 apareix tant a MULTIMODAL com a PERFIL: el filtre evita duplicats.
- A-27 esta a COGNITIU (no a LEXIC/SINTAXI) perque el seu objectiu es suport cognitiu malgrat el prefix A-.
- C-03 esta a QUALITAT (no a COGNITIU) perque fa referencia a rigor curricular.

### 10.3 Exemple: prompt AMB macrodirectives vs SENSE

**SENSE macrodirectives** (llista plana):

```
Instruccions per adaptar el text:
- Utilitza vocabulari frequent i evita paraules poc habituals.
- Posa els termes tecnics en negreta amb una definicio breu al costat.
- Repeteix el mateix mot; no facis servir sinonims.
- Una idea per frase.
- Veu activa obligatoria.
- Subjecte explicit a cada frase.
- Afegeix un titol clar al principi.
- Divideix el text en seccions amb subenuncalaments.
- ...30 instruccions mes barrejades sense ordre...
```

**AMB macrodirectives** (blocs tematics):

```
## LEXIC
- Utilitza vocabulari frequent i evita paraules poc habituals.
- Posa els termes tecnics en negreta amb una definicio breu al costat.
- Repeteix el mateix mot; no facis servir sinonims.

## SINTAXI
- Una idea per frase.
- Veu activa obligatoria.
- Subjecte explicit a cada frase.

## ESTRUCTURA
- Afegeix un titol clar al principi.
- Divideix el text en seccions amb subenuncalaments.
- ...
```

L'LLM processa millor el segon format: cada bloc actua com una "mini-tasca" amb context propi, i l'ordre dels blocs reflecteix la prioritat d'adaptacio (primer el lexic, despres la sintaxi, etc.).

### 10.4 Principi de disseny: IDs nomes al codi, prosa neta per a l'LLM

Els identificadors (A-01, B-03, H-17...) son necessaris per a:
- **Codi**: instruction_filter.py, instruction_catalog.py, logs del servidor.
- **Auditoria**: saber exactament quines instruccions s'han activat per a cada adaptacio.
- **Resolucio de conflictes**: detectar solapaments (A-05 vs H-02) i desactivar duplicats.

Pero l'LLM **mai no veu IDs**. El prompt que rep conte nomes prosa natural organitzada en macrodirectives. Aixo es critic perque:
1. Els IDs consumeixen tokens sense aportar informacio util a l'LLM.
2. L'LLM no pot "obeir" un codi com A-07; nomes pot seguir una instruccio en llenguatge natural.
3. La separacio permet canviar IDs o reorganitzar el cataleg sense afectar la qualitat de les adaptacions.

```
instruction_catalog.py          instruction_filter.py          prompt final
(IDs + text + condicions)  -->  (selecciona per perfil)  -->   (nomes prosa + macrodirectives)
     A-01: "Vocabulari..."           [A-01, A-07, B-01]         ## LEXIC
     A-07: "Una idea..."                                        - Vocabulari frequent...
     B-01: "Titol clar..."                                      ## SINTAXI
                                                                - Una idea per frase...
                                                                ## ESTRUCTURA
                                                                - Titol clar...
```

---

## Annex A: Variables que es podrien ELIMINAR

Algunes variables declaren informació que no genera cap acció diferent, ni com a ORDRE, ni NARRATIVA, ni PROPOSTA, ni FE:

| Variable | Per què no genera acció | Proposta |
|---|---|---|
| `tdah.presentacio` | Les 3 presentacions reben les mateixes instruccions textuals | NARRATIVA pura (mantenir, cost zero, dóna context) |
| `altes_cap.tipus_capacitat` | Impacte molt baix en instruccions | NARRATIVA pura (mantenir) |
| `tdl.bilingue` | Informació de context, no genera instrucció | NARRATIVA pura (mantenir) |
| `tdc.motricitat_grossa` | Poc impacte en adaptació de text digital | NARRATIVA pura (mantenir per futura ampliació a altres àmbits) |

**Nota**: cap variable proposada per eliminar. Les de NARRATIVA pura es mantenen perquè enriqueixen el persona-audience amb cost zero i permeten futura ampliació.

---

## Annex B: Glossari de termes d'aquest document

- **Macrodirectiva**: agrupació de 3-8 instruccions atòmiques en un sol bloc temàtic coherent per a l'LLM
- **ORDRE**: instrucció imperativa que l'LLM ha de seguir
- **NARRATIVA**: informació contextual que ajuda l'LLM a entendre el cas sense ser una ordre
- **PROPOSTA**: càlcul automàtic que el sistema fa (ex: suggerir DUA Accés) sense intervenció de l'LLM
- **REFORÇA**: la instrucció ja s'envia, la variable fa que el text sigui més intens
- **INTENSIFICA**: la variable canvia el paràmetre numèric d'una instrucció (ex: "3-5 frases" → "2-3 frases")
- **ACTIVA**: la instrucció NOMÉS s'envia si la variable té el valor indicat
- **ATENUA**: la variable redueix la intensitat d'una instrucció que s'enviaria per defecte
