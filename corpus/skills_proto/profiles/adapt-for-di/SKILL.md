---
name: adapt-for-di
description: >
  Use when adapting educational text for a student with intellectual
  disability (discapacitat intel·lectual). Activates when the profile
  includes "discapacitat intel·lectual" at any grade (lleu, moderat,
  sever). Works across all MECR levels but is especially critical for
  A1-B1. Core output principles: one new concept per block, radical
  concretion, systematic repetition, guided generalisation.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
mecr_range: [A1, A2, B1, B2, C1]
agent_role: adapter
tools_required: []
subvariables:
  - grau: [lleu, moderat, sever]
triggers:
  - path: profile.caracteristiques.di.actiu
    equals: true
---

# Adaptar text per a alumnat amb discapacitat intel·lectual

## Quan activar aquesta skill
Activa aquesta skill quan l'adaptació de text sigui per a un alumne amb
discapacitat intel·lectual (DI) — limitacions significatives en el
funcionament intel·lectual i en la conducta adaptativa. Senyals: ritme
d'aprenentatge lent, coneixements previs baixos, baixa autonomia,
dificultat per connectar nous aprenentatges amb els previs, dificultat
per generalitzar, vocabulari limitat, dificultat per seguir instruccions
complexes.

## Barrera nuclear
**Comprensió discursiva.** L'alumnat amb DI té com a barrera principal la
comprensió del discurs com a unitat — la capacitat d'integrar informació
entre frases, inferir relacions i abstraure conceptes. Necessita
concreció extrema i repetició sistemàtica. La capacitat de generalitzar
aprenentatges entre contextos és especialment feble.

## Instruccions principals d'adaptació

```
PERFIL: Discapacitat Intel·lectual
- UN sol concepte nou per bloc
- Concreció radical: cada concepte abstracte → exemple tangible
- Repetició sistemàtica en formats diversos
- Generalització guiada: connectar amb vida quotidiana
```

## Mapa barrera → instruccions (prioritzat)

| Prioritat | Instruccions activades | Justificació (barrera) |
|---|---|---|
| **1a (discursiva)** | H-09 (1 concepte per bloc), H-10 (concreció radical), H-11 (repetició sistemàtica) | Barrera nuclear: comprensió discursiva |
| **2a (inferència)** | C-01 (límit conceptes nous), C-06 (analogies quotidianes) | Barrera inferència |
| **3a (lèxica)** | A-01 (vocab freqüent), A-12 (longitud frase), A-22 (concreció quantificadors) | Vocabulari limitat |
| **4a (visual)** | D-01 (emojis suport), D-08 (pictogrames ARASAAC) | Suport pictogràfic intens |

## Modulació per sub-variables

### Grau de discapacitat
- **Lleu**: LF moderada, vocabulari simplificat però no mínim. Frases
  curtes però el text pot tenir un recorregut raonable. Un concepte nou
  per bloc, amb exemple quotidià. Es pot plantejar alguna inferència
  senzilla si està ben guiada.
- **Moderat**: LF intensa, vocabulari molt controlat, un sol concepte
  per bloc amb exemple tangible i repetició en 2-3 formats diferents
  (text, llista, pictograma). Frases molt curtes (6-8 paraules).
  Analogies amb la vida quotidiana obligatòries.
- **Sever**: LF extrema, text mínim, frases d'una sola clàusula.
  Consignes d'un sol pas. Vocabulari nuclear català. Pictogrames
  ARASAAC obligatoris per a cada concepte. Cada bloc ha de poder
  llegir-se aïlladament. Repetició del concepte principal al final
  de cada bloc.

## Exemple abans → després
Veure `assets/exemple-A2-fotosintesi.md` per a un exemple complet
d'adaptació d'un text de ciències naturals nivell A2 amb grau moderat
de DI.

## Carregar context més profund
Si calen fonaments pedagògics (adaptació curricular significativa vs.
adaptació de format, suport integrat a l'aula ordinària vs. segregació,
coordinació amb EAP, foment de l'autonomia, metodologies
manipulatives i significatives, reconeixement de l'esforç, distinció
entre DI i dificultats per L2 o dislèxia), carregar
`references/perfil-complet.md`. Si cal veure totes les fonts DEIC
(Formació del professorat), carregar `references/fonts.md`.
