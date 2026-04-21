---
name: adapt-for-tdc
description: >
  Use when adapting educational text for a student with Developmental
  Coordination Disorder (TDC / Dispraxia, DSM-5-TR 315.4 / F82, ICD-11
  6A04). Activates when the profile includes "TDC" or "dispraxia".
  Works across all MECR levels. Motor barrier: adaptations are mostly
  CSS/frontend; for the prompt LLM, guarantee clear semantic structure,
  avoid instructions that presuppose fine motor skills, and offer
  response alternatives (oral, digital, selection) instead of free
  handwriting.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
mecr_range: [A1, A2, B1, B2, C1]
agent_role: adapter
tools_required: []
subvariables:
  - grau: [lleu, moderat, sever]
  - motricitat_fina: bool
  - motricitat_grossa: bool
  - acces_teclat: bool
triggers:
  - path: profile.caracteristiques.tdc.actiu
    equals: true
---

# Adaptar text per a alumnat amb TDC / dispraxia

## Quan activar aquesta skill
Activa aquesta skill quan l'adaptació de text sigui per a un alumne
amb Trastorn del Desenvolupament de la Coordinació (TDC, també
anomenat dispraxia). Senyals: escriptura molt lenta o il·legible amb
gran diferència entre el potencial oral (fluid, ric) i la producció
escrita (pobra, curta, desordenada); fatiga motora en escriure (dolor,
pauses); evitació d'activitats d'EF, plàstica i manualitats;
desorganització del material. **Important:** no és mandra ni falta de
pràctica — és una condició neurològica que afecta la via motora, no la
capacitat de pensar.

## Barrera nuclear
**Accés motriu.** L'alumnat amb TDC/dispraxia té com a barrera
principal l'accés motriu al material (escriptura manual, manipulació
d'instruments, moviment coordinat). La capacitat cognitiva és
normativa o superior — el TDC afecta el canal de sortida, no el
contingut que l'alumne és capaç de processar. Les adaptacions textuals
per a l'LLM són mínimes: la majoria de necessitats són CSS/frontend
(navegació per teclat, mida clicable dels elements, temps addicional,
alternatives al motor manual).

## Instruccions principals d'adaptació

```
PERFIL: TDC / Dispraxia
- Estructura semàntica clara per navegació per teclat/commutador
- Evitar instruccions que requereixin motricitat fina (retallar, dibuixar, escriure a mà)
- Adaptar activitats: resposta oral o selecció en lloc d'escriptura lliure
```

## Mapa barrera → instruccions (prioritzat)

| Prioritat | Instruccions activades | Justificació (barrera) |
|---|---|---|
| **1a (accés)** | I-07 (navegació per teclat/commutador) | Barrera nuclear: accés motriu |
| **2a (estructura)** | H-19 (estructura semàntica H1-H3), B-02 (blocs amb títol) | Navegació accessible |
| **3a (consignes)** | F-XX (formats de resposta alternatius: oral, selecció, digital) | Dissociar motor i cognitiu |

**Nota**: La majoria d'adaptacions per a TDC/dispraxia són CSS/FE
(àrees clicables grans, navegació per teclat, mida de font ampliada,
alternatives a l'escriptura manual). L'LLM ha de garantir estructura
semàntica i evitar instruccions que pressuposin motricitat fina.

## Modulació per sub-variables

### Grau de severitat
- **Lleu**: el text ha de ser llegible amb temps addicional; cap
  consigna que exigeixi escriure llistes llargues a mà. Pauta clara
  a la pàgina. Les activitats de producció poden demanar escriptura
  breu.
- **Moderat**: les consignes de producció escrita llarga han
  d'oferir alternativa per teclat o resposta oral. Adaptar les
  activitats manipulatives (plantilles, rols complementaris). Els
  exercicis d'emplenar buits o seleccionar opcions són preferibles
  a la redacció lliure.
- **Sever**: totes les consignes d'escriptura han d'oferir
  alternativa no motora (resposta oral gravada, teclat, selecció).
  L'avaluació no pot dependre de la quantitat escrita ni de la
  cal·ligrafia. Temps addicional substancial (+50% com a mínim).

### Motricitat fina afectada
Quan està afectada (cas més freqüent): evitar consignes que demanin
retallar, dibuixar amb precisió, manipular objectes petits, escriure
amb lletra petita o curosa. Oferir alternatives: marcar amb creu,
seleccionar opcions, usar plantilles, treballar amb teclat. Permetre
lletra Arial o equivalent amb interlineat 1.5.

### Motricitat grossa afectada
No afecta directament l'adaptació textual, però sí que cal evitar
activitats amb component motor gruixut com a mode d'avaluació del
contingut textual (p. ex., "escriu al suro del fons de l'aula"
exigeix desplaçament i equilibri).

### Accés al teclat com a alternativa
- **Sí**: oferir sistemàticament alternativa digital per a les
  consignes de producció escrita llarga. El text ha de ser compatible
  amb processadors de text habituals i correctors.
- **No**: valorar tecnologia assistiva específica o resposta oral.
  Les consignes han d'admetre resposta oral o selecció. Reduir
  l'extensió esperada de la resposta escrita.

## Exemple abans → després
Veure `assets/exemple-B1-experiment.md` per a un exemple complet
d'adaptació d'un text de ciències naturals nivell B1 amb TDC moderat
i accés al teclat.

## Carregar context més profund
Si calen fonaments pedagògics (criteris DSM-5-TR i ICD-11,
comorbiditats amb TDAH / dislèxia / TDL / TEA / AC, instruments
d'avaluació MABC-2 / BOT-2 / DCD-Q, intervenció CO-OP i task-oriented,
diagnòstic diferencial amb paràlisi cerebral, marc normatiu D150/2017
i rol del CREDA / fisioterapeutes / terapeutes ocupacionals,
dissociació competència motora–competència conceptual en l'avaluació,
gestió de la fatiga motora al llarg del dia escolar), carregar
`references/perfil-complet.md`. Si cal veure totes les fonts (APA,
WHO, EACD-Blank 2012, Missiuna, Zwicker, DOGC), carregar
`references/fonts.md`.
