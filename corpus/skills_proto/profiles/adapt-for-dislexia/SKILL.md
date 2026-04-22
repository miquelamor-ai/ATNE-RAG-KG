---
name: adapt-for-dislexia
description: >
  Use when adapting educational text for a student with dyslexia or reading
  difficulties of neurobiological origin. Activates when the profile
  includes "dislèxia" or marked decoding fatigue. Works across all MECR
  levels. Core output principles: short high-frequency words, avoid long
  compounds, repeat key terms instead of using synonyms, visual relief.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
mecr_range: [A1, A2, B1, B2, C1]
agent_role: adapter
tools_required: []
subvariables: []
triggers:
  - path: profile.caracteristiques.dislexia.actiu
    equals: true
---

# Adaptar text per a alumnat amb dislèxia

## Quan activar aquesta skill
Activa aquesta skill quan l'adaptació de text sigui per a un alumne amb
dislèxia o dificultats lectores de base neurobiològica. Senyals: fatiga
lectora precoç, errors sistemàtics amb paraules llargues o poc freqüents,
lentitud lectora sense alteració de la comprensió oral, dificultats amb
paraules compostes i morfologia complexa (prefix+arrel+sufix).

## Barrera nuclear
**Descodificació.** El processament fonològic i la conversió grafema-fonema
són la dificultat clau. Les paraules llargues, poc freqüents o amb
estructura morfològica complexa generen fatiga lectora exponencial. La
memòria de treball es consumeix en la descodificació i no queda prou per a
la comprensió.

## Instruccions principals d'adaptació

```
PERFIL: Dislèxia (Dehaene/Wolf)
- Evita paraules compostes llargues: divideix o reformula
- Prefereix paraules d'alta freqüència lèxica
- Repeteix termes clau en lloc d'usar sinònims
- Frases 2-3 paraules més curtes que el màxim MECR
- Evita encadenar prefixos i sufixos
```

## Mapa barrera → instruccions (prioritzat)

| Prioritat | Instruccions activades | Justificació (barrera) |
|---|---|---|
| **1a (descodificació)** | H-07 (evitar compostos llargs), H-08 (alta freqüència, no sinònims), A-21 (descomposició compostos) | Barrera nuclear: descodificació |
| **2a (fatiga visual)** | I-01 (sans-serif 14pt), I-02 (interlineat 1.5), I-03 (columna estreta), I-04 (fons suau), I-05 (alineat esquerra) | Reduir fatiga visual (CSS/FE) |
| **3a (compensació)** | D-06 (text per veu alta), A-03 (coherència terminològica) | Canal oral com a complement |

## Modulació per sub-variables
Aquesta skill no té sub-variables configurables. Les adaptacions de format
(tipografia, espaiat, frases curtes, suport visual) s'apliquen de manera
universal. La variabilitat es cobreix amb la intensitat de LF (Lectura
Fàcil), que es calcula a partir del perfil global de l'alumne i del MECR.

Notes operatives per al renderitzador:
- La font recomanada és sans-serif (Atkinson Hyperlegible, Lexie Readable
  o OpenDyslexic si la preferència està activa al perfil docent).
- Interlineat mínim 1.5, alineat a l'esquerra (mai justificat).
- Columna estreta (~60-70 caràcters per línia).
- Fons lleugerament tintat (mai blanc pur) si el docent ho preveu.

## Exemple abans → després
Veure `assets/exemple-B1-fotosintesi.md` per a un exemple complet
d'adaptació d'un text de ciències naturals nivell B1.

## Carregar context més profund
Si calen fonaments pedagògics (model Dehaene/Wolf sobre descodificació,
distinció entre dislèxia de base neurobiològica i dificultats lectores per
L2, compensacions orals), carregar `references/perfil-complet.md`. Cal
tenir present que el corpus ATNE documenta específicament que "dificultats
lectores" no equival a "dislèxia": el perfil de dislèxia pròpiament dita
requereix diagnòstic específic, mentre que les dificultats lectores per L2
es cobreixen amb la skill `adapt-for-nouvingut`.
