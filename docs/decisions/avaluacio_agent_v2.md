# Sistema d'Avaluacio ATNE — Agent Avaluador v2

**Versio**: 2.0 · 29 marc 2026
**Autors**: Miquel Amor (FJE) + Claude Opus 4.6 (Anthropic)
**Context**: Experiment A/B Testing de dues vies de construccio del system prompt

---

## 0. Esquema de l'agent avaluador

```
                    ┌─────────────────────────────────────────┐
                    │           CAS D'AVALUACIO               │
                    │  text original + perfil + text adaptat   │
                    └────────────┬────────────────────────────┘
                                 │
                    ┌────────────▼────────────────────────────┐
                    │         BLOC 1 — RETRIEVAL (CODI)       │
                    │                                          │
                    │  Gold Standard = PROFILE_INSTRUCTION_MAP │
                    │  Recall = instruccions esperades que     │
                    │           realment s'han enviat          │
                    │  Precision = 1.0 (per disseny)           │
                    │                                          │
                    │  Executor: Python (determinista)          │
                    │  Tokens LLM: 0                           │
                    └────────────┬────────────────────────────┘
                                 │
                    ┌────────────▼────────────────────────────┐
                    │         BLOC 2 — FORMA (CODI)           │
                    │                                          │
                    │  F1: Longitud mitjana frase vs MECR     │
                    │  F2: Presencia titols/subtitols          │
                    │  F3: Negretes en termes tecnics          │
                    │  F4: Llistes on pertoca                  │
                    │  F5: Prellico present                    │
                    │                                          │
                    │  Executor: Python/regex (determinista)    │
                    │  Tokens LLM: 0                           │
                    └────────────┬────────────────────────────┘
                                 │
                    ┌────────────▼────────────────────────────┐
                    │     BLOC 3 — FONS (LLM-as-a-judge)     │
                    │                                          │
                    │  C1: Coherencia i cohesio         1-5   │
                    │  C2: Adequacio al perfil          1-5   │
                    │  C3: Preservacio curricular       1-5   │
                    │  C4: Adequacio al nivell MECR     1-5   │
                    │  C5: Prellico funcional           1-5   │
                    │  C6: Coherencia creuament (si 2+) 1-5   │
                    │                                          │
                    │  Executor: Gemini (LLM esceptic)         │
                    │  Tokens LLM: ~2000/cas                   │
                    └────────────┬────────────────────────────┘
                                 │
                    ┌────────────▼────────────────────────────┐
                    │         OUTPUT CONSOLIDAT                │
                    │                                          │
                    │  JSON amb retrieval + forma + fons       │
                    │  1 fitxer per cas, agregacio al final    │
                    └─────────────────────────────────────────┘
```

### Flux complet per 160 casos:

```
Per cada cas (text x perfil):
  1. Generar adaptacio amb Branca A (Hardcoded)     → text_A
  2. Generar adaptacio amb Branca B (RAG filtrat)    → text_B
  3. BLOC 1 (CODI): calcular Recall de B             → retrieval_B
  4. BLOC 2 (CODI): calcular F1-F5 per A i B         → forma_A, forma_B
  5. BLOC 3 (LLM):  avaluar C1-C5 per A              → fons_A
  6. BLOC 3 (LLM):  avaluar C1-C5 per B              → fons_B
  7. Comparar: forma_A vs forma_B, fons_A vs fons_B

Agregacio final:
  - Mitjanes per branca
  - Desglossament per perfil, etapa, genere
  - Taula de decisions (§8)
```

---

## 1. Proposit

Avaluar si les adaptacions generades per dues branques del sistema ATNE (Hardcoded vs RAG) difereixen en qualitat real, no nomes en quantitat de text generat.

### Problema que resolem

El batch test de 160 casos (2026-03-28) va mesurar **nomes forma**: paraules/cas, negretes/cas, temps/cas. RAG va guanyar en quantitat (3x paraules), pero "mes text" no implica "millor adaptacio". Sense un termometre de fons, qualsevol decisio sobre quina branca es millor es un vol a cegues.

---

## 2. Decisions de disseny i justificacions

### Decisio 1: Tres blocs, dos executors

**Decisio**: BLOC 1 (Retrieval) i BLOC 2 (Forma) els executa Python. BLOC 3 (Fons) l'executa un LLM.

**Per que**:
- BLOC 1 i 2 son metriques objectives, deterministes i reproduibles. Un LLM no hi afegeix valor — al contrari, introduiria variabilitat innecessaria.
- BLOC 3 requereix judici semantic: "el text es coherent?", "s'ha aplicat el perfil?". Nomes un LLM (o un expert huma) pot respondre aixo.
- Separar els blocs redueix el cost de tokens (BLOC 3 es l'unic que en consumeix) i augmenta la fiabilitat (BLOC 1-2 donen el mateix resultat cada cop).

### Decisio 2: Gold Standard = PROFILE_INSTRUCTION_MAP (codi, no document extern)

**Decisio**: El Gold Standard per al Recall del BLOC 1 es el mapa `PROFILE_INSTRUCTION_MAP` d'`instruction_catalog.py`, no un document extern.

**Per que**:
- Amb el treball de 2026-03-29 (sessio actual), les 72 instruccions LLM estan catalogades amb regles d'activacio explicites (SEMPRE/PERFIL/NIVELL/COMPLEMENT) i sub-variables.
- El mapa de la seccio 8 de l'arquitectura (`arquitectura_prompt_v2.md`) defineix exactament quines instruccions s'activen per cada perfil, en quin ordre de prioritat.
- Usar el codi com a Gold Standard garanteix coherencia: si el cataleg canvia, el Gold Standard canvia automaticament. No hi ha risc de desincronitzacio entre un document extern i el codi real.

### Decisio 3: Precision = 1.0 per disseny (no cal mesurar)

**Decisio**: Eliminem la metrica de Precision del BLOC 1.

**Per que**:
- Amb el filtratge per cataleg (`instruction_filter.py`), cada instruccio enviada a l'LLM ha passat un filtre explicit d'activacio. Si no pertoca al perfil, no s'envia.
- A la branca Hardcoded, els blocs son fixos per perfil — tampoc envien instruccions irrellevants.
- Per tant, a les dues branques, Precision es 1.0 per construccio. Mesurar-la consumiria tokens sense aportar informacio.

### Decisio 4: L'LLM avaluador rep BLOC 1-2 com a context, pero no els genera

**Decisio**: El BLOC 3 (LLM) rep les puntuacions de BLOC 1-2 ja calculades com a informacio de context, pero no ha de produir-les.

**Per que**:
- L'LLM pot usar les dades de forma ("la longitud de frase es dins del rang MECR: si") per informar el seu judici de fons ("l'adequacio MECR es alta").
- Pero si li demanem que tambe calculi forma, introduim error (els LLM compten malament paraules) i duplicacio de treball.
- Aixo segueix el principi de "cada executor fa el que fa be": Python compta, l'LLM jutja.

### Decisio 5: L'avaluador es un LLM esceptic, no auto-avaluador

**Decisio**: L'agent avaluador te un system prompt esceptic ("no aprovies per defecte") i idealment seria un model diferent del generador. En la practica usem el mateix Gemini Flash pero amb prompt esceptic.

**Per que**:
- Un model que avalua el seu propi output tendeix a auto-aprovar-se (bias d'auto-consistencia).
- El prompt esceptic mitiga parcialment aquest bias: "Puntua basant-te exclusivament en evidencia present al text. No assumeixis que s'han aplicat instruccions si no hi ha evidencia directa."
- A futur, es pot substituir per un model diferent (Gemini Pro, Claude) per eliminar completament el bias.

### Decisio 6: Criteri C2 invertit per Altes Capacitats

**Decisio**: Per al perfil Altes Capacitats (P7, DUA Enriquiment), el criteri C2 ("Adequacio al perfil") es reformula com: "El text ofereix aprofundiment, connexions complexes i repte cognitiu? (No simplificacio, sino enriquiment)".

**Per que**:
- Les instruccions per AC son inversament simètriques a la resta de perfils: en lloc de simplificar, han d'enriquir.
- Si usem el C2 estandard ("s'han aplicat les instruccions del perfil?"), un text simplificat incorrectament podria puntuar alt perque "ha simplificat", quan AC demana el contrari.
- A mes, el cataleg de la sessio actual (2026-03-29) implementa supressions explícites: 7 regles universals es desactiven per AC (A-01, A-03, A-05, A-07, A-08, A-11, A-16). L'avaluador ha de verificar que NO s'han aplicat.

### Decisio 7: Criteri C6 nomes per creuaments

**Decisio**: El criteri C6 ("Coherencia del creuament") nomes s'aplica als perfils multi-caracter (P8: Nouvingut+Dislexia, P9: TDAH+TEA, P10: Vulnerabilitat+TDL).

**Per que**:
- Avaluar coherencia entre perfils nomes te sentit si hi ha 2+ perfils actius.
- Per perfils simples, C2 ja cobreix l'adequacio.
- Afegir C6 a tots els casos inflaria el cost sense aportar informacio.

---

## 3. BLOC 1 — Metriques de Retrieval (CODI)

### 3.1 Retrieval Recall

**Definicio**: Proporcio d'instruccions del Gold Standard (PROFILE_INSTRUCTION_MAP) que realment s'han enviat al prompt.

**Implementacio**:
```python
from instruction_catalog import PROFILE_INSTRUCTION_MAP

def recall(profile_key, instructions_sent):
    """
    profile_key: ex. "nouvingut"
    instructions_sent: llista d'IDs enviats (ex. ["A-01", "A-02", ...])
    """
    expected = set()
    for priority_group in PROFILE_INSTRUCTION_MAP[profile_key].values():
        expected.update(priority_group)
    actual = set(instructions_sent)
    if not expected:
        return 1.0
    return len(expected & actual) / len(expected)
```

**Nota**: Per a la branca Hardcoded, Recall = 1.0 per disseny (els blocs contenen totes les instruccions del perfil, compactades). Per a la branca RAG filtrada, el Recall dependra de si totes les instruccions esperades passen el filtre de sub-variables.

### 3.2 Precision

**No es calcula.** Precision = 1.0 per disseny a les dues branques (veure Decisio 3).

---

## 4. BLOC 2 — Faithfulness de forma (CODI)

> Aplicar a les dues branques. Mesura si l'output segueix les instruccions formals.

### Metriques

| # | Criteri | Com es mesura | Rang |
|---|---|---|---|
| F1 | **Longitud mitjana frase dins rang MECR** | Python: `paraules / frases`. Compara amb rang MECR: pre-A1(3-5), A1(5-8), A2(8-12), B1(12-18), B2(18-25) | 0-1 |
| F2 | **Presencia de titols i subtitols** | Regex: detecta linies que comencen amb `#` | 0-1 |
| F3 | **Presencia de negretes en termes tecnics** | Regex: detecta `**text**` | 0-1 |
| F4 | **Presencia de llistes** | Regex: detecta `- ` o `1. ` en el text | 0-1 |
| F5 | **Prellico present** | Detecta bloc introductori: text entre el primer `##` i el contingut principal | 0-1 |

**Puntuacio forma**: mitjana F1-F5 (rang 0.0-1.0)

### Nota sobre F1

F1 no es un simple 0/1. Es calcula com a proporcio de frases dins del rang MECR:

```python
frases_dins_rang = sum(1 for s in frases if min_mecr <= len(s.split()) <= max_mecr)
F1 = frases_dins_rang / len(frases)
```

Aixo dona un valor continu que reflecteix millor l'adherencia.

---

## 5. BLOC 3 — Faithfulness de fons (LLM-as-a-judge)

### System prompt de l'agent avaluador

L'agent rep un system prompt esceptic amb les instruccions seguents:

```
Ets un avaluador pedagogic expert i esceptic. La teva feina es puntuar la qualitat
d'una adaptacio de text educatiu.

REGLES:
1. NO aprovies per defecte. Puntua basant-te EXCLUSIVAMENT en evidencia present al text.
2. Si una instruccio del perfil NO te evidencia directa al text, puntua baix.
3. Justifica cada puntuacio en UNA frase concisa.
4. Retorna NOMES el JSON demanat, sense text addicional.
```

### Criteris

| # | Criteri | Pregunta operativa | Rang |
|---|---|---|---|
| C1 | **Coherencia i cohesio** | El text es internament consistent? Les idees flueixen de manera logica? Hi ha connectors i transicions? | 1-5 |
| C2 | **Adequacio al perfil** | Les instruccions especifiques del perfil declarat s'han aplicat al text? Hi ha evidencia directa? | 1-5 |
| C3 | **Preservacio curricular** | El contingut original s'ha mantingut sense alteracions de fons, omissions rellevants ni errors conceptuals? | 1-5 |
| C4 | **Adequacio al nivell MECR** | El lexic, la sintaxi i la complexitat corresponen al nivell MECR declarat? | 1-5 |
| C5 | **Prellico funcional** | El prellico prepara cognitivament el que vindra (glossari, organitzador previ), o es merament decoratiu? | 1-5 |
| C6 | **Coherencia creuament** | *(Nomes si 2+ perfils actius)* S'han aplicat les instruccions de tots els perfils sense contradiccio? | 1-5 |

### Inversio C2 per Altes Capacitats

Quan el perfil es `altes_capacitats` o el DUA es `Enriquiment`:

> C2: "El text ofereix aprofundiment, connexions interdisciplinars, pensament critic i repte cognitiu? S'han suprimit correctament les regles de simplificacio (A-01, A-03, A-05, A-07, A-08, A-11, A-16)?"

### Puntuacio fons

- Perfils simples (1 caracter): mitjana C1-C5 (rang 1.0-5.0)
- Perfils creuats (2+ caracters): mitjana C1-C6 (rang 1.0-5.0)

---

## 6. Inputs per cas

Per cada cas avaluat, l'agent rep:

| # | Input | Font |
|---|---|---|
| 1 | ID del cas | ex: `PRI_EXPL__P1` |
| 2 | Branca | `hardcoded` o `rag` |
| 3 | Text original | `test_data.json` |
| 4 | Perfil declarat | Caracteristiques, MECR, DUA, etapa |
| 5 | Instruccions filtrades enviades + stats | Output d'`instruction_filter.get_instructions()` |
| 6 | Text adaptat | Output del generador |
| 7 | Metriques BLOC 1-2 precalculades | Recall + F1-F5 (context informatiu) |

**Canvi respecte v1**: L'input 5 ja no es "bloc monolitic de perfil" sino les instruccions individuals filtrades amb les estadistiques de filtratge (quantes SEMPRE, NIVELL, PERFIL, condicionals, suprimides). Aixo permet a l'avaluador verificar si cada instruccio enviada s'ha aplicat realment.

---

## 7. Output per cas

```json
{
  "cas_id": "PRI_EXPL__P1",
  "branca": "rag",
  "retrieval": {
    "recall": 0.85,
    "criteris_absents": ["B-07", "C-08"]
  },
  "forma": {
    "F1_longitud_frase": 0.82,
    "F2_titols": 1,
    "F3_negretes": 1,
    "F4_llistes": 1,
    "F5_prellico_present": 1,
    "puntuacio_forma": 0.96
  },
  "fons": {
    "C1_coherencia": {"puntuacio": 4, "justificacio": "..."},
    "C2_adequacio_perfil": {"puntuacio": 3, "justificacio": "..."},
    "C3_preservacio_curricular": {"puntuacio": 5, "justificacio": "..."},
    "C4_adequacio_mecr": {"puntuacio": 4, "justificacio": "..."},
    "C5_prellico_funcional": {"puntuacio": 3, "justificacio": "..."},
    "puntuacio_fons": 3.8
  },
  "filter_stats": {
    "total_enviades": 59,
    "sempre": 32,
    "nivell": 18,
    "perfil": 6,
    "perfil_condicional": 2,
    "suprimides": 0
  }
}
```

---

## 8. Logica de comparacio entre branques

Per cada cas (text x perfil), es comparen les dues branques:

| Dimensio | Que es compara | Com |
|---|---|---|
| **Forma** | forma_A vs forma_B | Comparar puntuacio_forma |
| **Fons** | fons_A vs fons_B | Comparar puntuacio_fons |
| **Retrieval** | recall_B | Correlacionar amb puntuacio_fons de B |
| **Eficiencia** | filter_stats_A vs filter_stats_B | Nombre d'instruccions enviades |

### Taula de decisions finals (agregat 160 casos)

| Resultat | Decisio | Accio |
|---|---|---|
| RAG guanya en forma + fons | **Sistema RAG pur** | Merge branca RAG a main |
| Hardcoded guanya en forma + fons | **Sistema Hardcoded pur** | Merge branca Hardcoded a main |
| RAG > fons, Hardcoded > forma | **Hibrid: RAG + post-processament** | RAG per instruccions + CODI per validar forma |
| Hardcoded guanya en fons | **Problema de corpus** | Revisar documents pedagogics del corpus MD |
| Empat estadistic | **RAG per defecte** | RAG es mes mantenible (editar MD vs editar Python) |

---

## 9. Nota sobre el dataset

**160 casos**: 16 textos (4 etapes x 4 generes) x 10 perfils.

**Buit identificat**: cap text amb alta carrega cultural (referents locals catalans). Afecta especialment el perfil nouvingut (instruccions E-08, E-09, G-05 queden sense exercitar). Proposta: afegir 2-4 textos amb carrega cultural explicita en una segona fase.

**Buit addicional identificat (2026-03-29)**: les sub-variables dels perfils (L1, alfabet_llati, escolaritzacio) nomes es varien en els 10 perfils predefinits del batch. Per avaluar completament el filtratge condicional (G-02, G-03, E-11), caldria ampliar la matriu amb variacions de sub-variables dins del mateix perfil.

---

## 10. Resum de fitxers del sistema d'avaluacio

| Fitxer | Funcio |
|---|---|
| `instruction_catalog.py` | Cataleg de 72 instruccions LLM amb regles d'activacio |
| `instruction_filter.py` | Filtratge d'instruccions per perfil, sub-variables, MECR, DUA |
| `evaluator_metrics.py` | BLOC 1 (Recall) + BLOC 2 (Forma) — tot Python |
| `evaluator_agent.py` | BLOC 3 (Fons) — LLM-as-a-judge via Gemini |
| `tests/batch_eval.py` | Orquestrador: genera + avalua + compara 160 casos |
| `tests/test_data.json` | 16 textos x 10 perfils |
| `docs/decisions/avaluacio_agent_v2.md` | Aquest document |
