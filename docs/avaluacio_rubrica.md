# Rubriques d'avaluacio ATNE

**Fitxer font**: `evaluator_rubrics.py`

---

## 1. Evolucio de la rubrica

| | v1 (marc 2026) | v2 (31 marc 2026) |
|---|---|---|
| **Criteris** | 5 (C1-C5) | 8 (A1-A3, B1-B4, C1) |
| **Dimensions** | Unica | 3 dimensions ponderades |
| **Ancoratges** | No (1-5 sense guia) | Si (descripcio per cada nivell) |
| **Marcs teorics** | Cap explicit | 6 marcs |
| **Chain-of-Thought** | Basic | Obligatori amb evidencies |
| **Pes global** | Mitjana simple | A*0.3 + B*0.5 + C*0.2 |
| **Usada a** | multi_llm_eval.py (Ronda 1) | multi_v2.py (Ronda 2) |

### Per que v2?
1. **v1 era massa generica**: criteris sense ancoratge produien puntuacions inflades (mitjana ~4.3)
2. **Falta de discriminacio**: tots els textos puntuaven similar, poca variancia
3. **Sense fonamentacio teorica**: els criteris no estaven lligats a marcs pedagogics reconeguts
4. **Dimensio unica**: barrejava qualitat textual amb adequacio pedagogica

---

## 2. Rubrica v1 — Original

5 criteris, escala 1-5, sense ancoratges.

| Criteri | Pregunta operativa |
|---------|-------------------|
| **C1 Coherencia** | El text es internament consistent? Les idees flueixen logicament? |
| **C2 Adequacio al perfil** | Les instruccions del perfil declarat s'han aplicat? |
| **C3 Preservacio curricular** | El contingut original s'ha mantingut sense omissions? |
| **C4 Adequacio MECR** | Lexic i sintaxi corresponen al nivell declarat? |
| **C5 Prellico funcional** | El prellico prepara cognitivament, o es decoratiu? |

**Puntuacio**: mitjana simple C1-C5 (rang 1.0-5.0)

### Cas especial v1
- **Perfils creuats** (P8-P10): criteri extra C6 (coherencia del creuament)
- **Altes capacitats** (P7): C2 invertit (puntuar enriquiment, no simplificacio)

---

## 3. Rubrica v2 — Fonamentada

8 criteris en 3 dimensions, ancoratges per nivell, 6 marcs teorics.

### Dimensio A — Qualitat textual (pes 0.3)

**A1 Coherencia i cohesio** (Halliday LSF)
| Nivell | Descripcio |
|--------|-----------|
| 1 | Incoherent: idees desordenades, salts logics, sense connectors |
| 2 | Parcialment coherent: algunes idees connectades, gaps notables |
| 3 | Acceptable: estructura logica clara, connectors basics |
| 4 | Bo: idees ben encadenades, connectors variats, transicions |
| 5 | Excel.lent: flux impecable, frase topic per paragraf |

**A2 Correccio linguistica** (Norma IEC)
| Nivell | Descripcio |
|--------|-----------|
| 1 | Errors greus: agramatical, barreja de llengues |
| 2 | Errors frequents: multiples errors menors |
| 3 | Acceptable: errors ocasionals, registre adequat |
| 4 | Bo: 1-2 errors esporadics en 300 paraules |
| 5 | Impecable: zero errors, registre academic-educatiu correcte |

**A3 Llegibilitat i complexitat** (TSAR/SIERA/Crossley)
| Nivell | Descripcio |
|--------|-----------|
| 1 | Inadequat: nivell completament erroni (B2 per a pre-A1) |
| 2 | Majoritariament inadequat: >50% frases fora del rang MECR |
| 3 | Parcial: 50-75% frases dins del rang MECR |
| 4 | Adequat: >75% frases dins del rang, vocabulari frequent |
| 5 | Perfecte: totes les frases dins del rang, vocabulari calibrat |

### Dimensio B — Adequacio pedagogica (pes 0.5)

**B1 Fidelitat al contingut curricular** (Mayer coherence, QuestEval)
| Nivell | Descripcio |
|--------|-----------|
| 1 | Omissions greus: conceptes clau eliminats o errors |
| 2 | Omissions notables: 2-3 conceptes importants absents |
| 3 | Acceptable: conceptes nuclears presents, detalls omesos |
| 4 | Bo: contingut complet, simplificacio linguistica adequada |
| 5 | Fidel: tots els conceptes i relacions causals preservats |

**B2 Adequacio al perfil de l'alumnat** (UDL/CAST, DUA)
| Nivell | Descripcio |
|--------|-----------|
| 1 | Ignorat: cap evidencia d'adaptacio al perfil |
| 2 | Minim: 1-2 elements aplicats |
| 3 | Parcial: elements principals aplicats, manquen secundaris |
| 4 | Bo: majoria d'instruccions amb evidencia |
| 5 | Excel.lent: un especialista validaria sense reserves |

*INVERSIO per AC/Enriquiment: puntuar alt si NO simplifica i SI enriqueix*

**B3 Suports cognitius i scaffolding** (Sweller CLT, Vygotsky ZPD)
| Nivell | Descripcio |
|--------|-----------|
| 1 | Absent: cap suport |
| 2 | Minim: un element sense funcionalitat clara |
| 3 | Funcional: glossari previ O definicions integrades O esquema |
| 4 | Complet: multiples suports combinats i funcionals |
| 5 | Optim: scaffolding decreixent, glossari+definicions+titols+resum |

**B4 Sensibilitat cultural i inclusio** (UDL Engagement, CAST 2024)
| Nivell | Descripcio |
|--------|-----------|
| 1 | Inadequat: referents exclusius, to condescendent |
| 2 | Descuidat: referents locals no explicats |
| 3 | Neutre: no estigmatitza, to adequat |
| 4 | Bo: referents explicats o substituits, to respectuos |
| 5 | Proactiu: referents universals, connexions interculturals |

*Per perfils no-nouvingut: minim 3 si el text es neutre*

### Dimensio C — Eficacia (pes 0.2)

**C1 Potencial d'aprenentatge** (Vygotsky ZPD, Bloom)
| Nivell | Descripcio |
|--------|-----------|
| 1 | No aprendria: massa dificil, massa simple, o incoherent |
| 2 | Improbable: parts comprensibles pero el conjunt no funciona |
| 3 | Possible: amb suport docent, l'alumne podria aprendre |
| 4 | Probable: l'alumne podria aprendre autonomament |
| 5 | Assegurat: text perfectament calibrat a la ZPD |

### Puntuacio global
```
qualitat_textual = mitjana(A1, A2, A3)
adequacio_pedagogica = mitjana(B1, B2, B3, B4)
eficacia = C1
global = qualitat*0.3 + adequacio*0.5 + eficacia*0.2
```

---

## 4. Marcs teorics de referencia

| Marc | Aportacio a la rubrica |
|------|----------------------|
| **Halliday LSF** (Linguistica Sistemica Funcional) | A1: cohesio textual, funcions del llenguatge |
| **Norma IEC** | A2: correccio normativa del catala |
| **TSAR/SIERA/Crossley** | A3: metriques de llegibilitat i simplificacio textual |
| **Mayer** (Cognitive Theory of Multimedia Learning) | B1: principi de coherencia (no afegir informacio irrelevant) |
| **CAST/UDL** (Universal Design for Learning) | B2, B4: multiples mitjans de representacio, engagement |
| **Sweller CLT** (Cognitive Load Theory) | B3: reduccio carrega cognitiva, scaffolding |
| **Vygotsky ZPD** (Zona de Desenvolupament Proxim) | B3, C1: suport dins la zona proxima |
| **Bloom** (Taxonomia) | C1: nivells de pensament adequats al perfil |

---

## 5. Metriques automatiques (BLOC 1 i BLOC 2)

Independents de la rubrica LLM. Calculades per `evaluator_metrics.py`.

### BLOC 1 — Retrieval (nomes branca RAG)
- **Recall**: % criteris del Gold Standard presents al prompt recuperat
- **Precision**: % criteris del prompt que son rellevants per al perfil

### BLOC 2 — Forma (totes les branques)
| Metrica | Mesurament |
|---------|-----------|
| F1 Longitud frase | Dins rang MECR (pre-A1: 3-5 paraules, B2: 18-25) |
| F2 Titols | Presencia de `#` i `##` al markdown |
| F3 Negretes | Presencia de `**text**` en conceptes clau |
| F4 Llistes | Presencia de `- ` o `1.` on pertoca |
| F5 Prellico | Bloc introductori al primer paragraf |

**Puntuacio forma**: mitjana F1-F5 (rang 0.0-1.0)

---

## 6. Protocol anti-biaix

Mesures implementades per reduir biaix en l'avaluacio:

1. **Ordre aleatori**: els textos es presenten en ordre aleatoritzat al jutge
2. **Etiquetes cegues**: el jutge no sap quina branca (HC/RAG) ha generat cada text
3. **is_self_eval flag**: quan jutge == generador, es marca per analisi posterior
4. **Multiple jutges**: minim 2 jutges per triangulacio
5. **Chain-of-Thought**: obligar evidencies abans de puntuar (v2)
