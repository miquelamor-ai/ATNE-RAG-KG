---
name: adapt-for-tdl
description: >
  Use when adapting educational text for a student with Developmental
  Language Disorder (TDL — Trastorn del Desenvolupament del Llenguatge,
  CATALISE 2017). Activates when the profile includes "TDL". Works
  across all MECR levels. Core output principles: maximum lexical
  density reduction, key terms modelled across 2-3 different contexts,
  zero subordinate clauses and weak pronouns, definitions embedded next
  to each term.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
mecr_range: [A1, A2, B1, B2, C1]
agent_role: adapter
tools_required: []
subvariables:
  - modalitat: [comprensiu, expressiu, mixt]
  - morfosintaxi: bool
  - semantica: bool
  - pragmatica: bool
  - discurs_narrativa: bool
  - comprensio_lectora: bool
  - grau: [lleu, moderat, sever]
  - bilingue: bool
triggers:
  - path: profile.caracteristiques.tdl.actiu
    equals: true
---

# Adaptar text per a alumnat amb TDL

## Quan activar aquesta skill
Activa aquesta skill quan l'adaptació de text sigui per a un alumne amb
Trastorn del Desenvolupament del Llenguatge (TDL, marc CATALISE Bishop
et al., 2017). Senyals: vocabulari molt limitat per a l'edat,
s'expressa amb paraules generals ("cosa", "fer", "allò"), frases molt
curtes i mal estructurades, gran diferència entre el que entén i el
que produeix, dificultat per seguir instruccions de dos o més passos,
lectura fluida amb comprensió feble.

## Barrera nuclear
**Comprensió lèxica i sintàctica.** L'alumnat amb TDL té com a barrera
principal la comprensió i producció lingüística — tant lèxica
(vocabulari limitat, accés lent al lèxic) com sintàctica (dificultat
amb estructures complexes, pronoms febles, subordinades). La memòria
fonològica compromesa dificulta retenir frases llargues. La capacitat
cognitiva no verbal sovint és normativa o superior: el TDL afecta el
canal, no la capacitat de pensar.

## Instruccions principals d'adaptació

```
PERFIL: TDL (Trastorn del Desenvolupament del Llenguatge)
- Reducció màxima de densitat lèxica
- Cada terme tècnic apareix en 2-3 contextos diferents (modelatge)
- Zero subordinades i pronoms febles (li, els, en, hi)
- Definicions integrades just al costat del terme (no al final)
```

## Mapa barrera → instruccions (prioritzat)

| Prioritat | Instruccions activades | Justificació (barrera) |
|---|---|---|
| **1a (lèxica)** | H-16 (reducció densitat lèxica), A-01 (vocab freqüent), A-02 (termes en negreta), A-20 (control densitat) | Barrera nuclear: comprensió lèxica |
| **2a (sintàctica)** | H-17 (modelatge ús context), A-07 (una idea per frase), A-13 (eliminació subordinades), A-26 (evitar incisos) | Barrera nuclear: comprensió sintàctica |
| **3a (memòria)** | C-04 (chunking 3-5 elements), C-05 (glossari previ Sweller) | Memòria fonològica compromesa |

## Modulació per sub-variables

### Modalitat afectada
- **Comprensiu**: simplificar màxim el text d'entrada. Frases curtes,
  vocabulari freqüent, definicions integrades. Verificar la
  comprensió literal abans de demanar inferències.
- **Expressiu**: simplificar les consignes de producció. Modelar
  l'estructura esperada (plantilles, inicis de frase, bancs de
  paraules). Oferir andamiatge lingüístic explícit.
- **Mixt** (el més freqüent): combinar les dues estratègies —
  simplificar el text i oferir bastida lingüística per produir.

### Components afectats (boolean, s'activen sumats)
- **Morfosintaxi**: estructures SVO simples, evitar passives i
  subordinades, concordances simples, ordre canònic de la frase.
- **Semàntica / Lèxic**: vocabulari d'alta freqüència, definicions
  integrades al text (no al glossari final), no usar sinònims
  innecessaris — repetir el mateix terme.
- **Pragmàtica**: evitar llenguatge figurat, ironies o consignes
  implícites. Explicitar el context comunicatiu ("ara t'explicaré...",
  "aquesta és una pregunta..."). Gestió explícita de torns.
- **Discurs / Narrativa**: guió d'estructura explícit amb blocs
  etiquetats ("Definició / Causes / Conseqüències / Exemple"),
  segmentació amb títols de funció, mapes conceptuals com a suport.
- **Comprensió lectora**: ressaltar paraules funció clau (articles,
  preposicions, conjuncions), verificar comprensió literal abans de
  demanar inferències. No confondre fluïdesa lectora amb comprensió.

### Grau de severitat
- **Lleu**: simplificació moderada, estructura clara, vocabulari
  freqüent però no mínim.
- **Moderat**: reducció sintàctica sistemàtica, suport visual
  explícit, consignes molt curtes, una instrucció per vegada.
- **Sever**: text mínim, frases d'una clàusula, andamiatge màxim,
  opcions no verbals (pictogrames, esquemes) per a totes les
  consignes.

### Context bilingüe / plurilingüe
Si l'alumne rep instrucció en una llengua que no és la seva L1: el
bilingüisme no causa TDL però pot intensificar les dificultats.
Incrementar el suport semàntic, reduir la complexitat morfosintàctica
per sobre del grau base, no atribuir tots els errors al TDL. Valorar
la coexistència amb el perfil nouvingut.

## Exemple abans → després
Veure `assets/exemple-A2-cicle-aigua.md` per a un exemple complet
d'adaptació d'un text de ciències naturals nivell A2 amb modalitat
mixta i grau moderat.

## Carregar context més profund
Si calen fonaments pedagògics (marc CATALISE, dimensionalitat
clínica, diagnòstic diferencial amb TEA / dislèxia / nouvingut,
dissociació competència lingüística–competència conceptual en
l'avaluació, coordinació amb CREDA / EAP / CLC, andamiatge en
producció escrita), carregar `references/perfil-complet.md`. Si cal
veure totes les fonts (Bishop, Norbury, CLC, XTEC, Frontiers),
carregar `references/fonts.md`.
