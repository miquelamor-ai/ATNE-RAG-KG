---
name: adapt-for-altes-capacitats
description: >
  Use when adapting educational text for a student with high abilities
  (altes capacitats: superdotació intel·lectual, talent específic or
  precocitat). Activates when the profile includes "altes_capacitats".
  Works across all MECR levels but especially B1–C1. Core output
  principles: DO NOT simplify — add depth, interdisciplinary connections,
  critical-thinking prompts and open questions.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
mecr_range: [A1, A2, B1, B2, C1]
agent_role: adapter
tools_required: []
subvariables:
  - tipus_capacitat: [global, talent_especific]
  - doble_excepcionalitat: bool
triggers:
  - path: profile.caracteristiques.altes_capacitats.actiu
    equals: true
---

# Adaptar text per a alumnat amb altes capacitats

## Quan activar aquesta skill
Activa aquesta skill quan l'adaptació de text sigui per a un alumne amb
altes capacitats (AC): superdotació intel·lectual, talent específic
(verbal, matemàtic, artístic...) o precocitat intel·lectual. Senyals:
comprensió ràpida, avorriment davant material repetitiu, preguntes
existencials o abstractes, pensament divergent, producció original.

## Barrera nuclear
**Cap barrera lingüística.** L'alumnat amb AC NO necessita simplificació
— al contrari, necessita profunditat, complexitat i repte cognitiu. La
barrera real és l'**avorriment i la desmotivació** davant material massa
senzill. Si el text és trivial, l'alumne desconnecta, produeix menys del
que pot i pot arribar al fracàs escolar malgrat el seu potencial.

## Instruccions principals d'adaptació

```
PERFIL: Altes Capacitats
- NO simplifiquis: mantén complexitat lingüística i conceptual
- Afegeix profunditat: excepcions, fronteres del coneixement, debats oberts
- Connexions interdisciplinars
- Preguntes de pensament crític (per què? i si...? quines alternatives?)
```

## Mapa barrera → instruccions (prioritzat)

| Prioritat | Instruccions activades | Justificació |
|---|---|---|
| **1a (profunditat)** | H-12 (profundització conceptual), H-13 (connexions interdisciplinars), H-14 (mantenir complexitat) | Necessitat d'enriquiment |
| **2a (pensament crític)** | F-09 (preguntes pensament crític), F-10 (connexions interdisciplinars) | Estimulació cognitiva |

## Modulació per sub-variables

### Tipus de capacitat
- **Global (superdotació)**: enriquiment transversal. El text ha
  d'obrir finestres a diverses àrees (ciència, història, filosofia,
  art) des del mateix contingut curricular. Preguntes de pensament
  crític que connectin disciplines.
- **Talent específic** (verbal, matemàtic, artístic, científic...):
  aprofundiment en l'àrea de talent. Si el talent és matemàtic,
  afegir formalització simbòlica, demostracions, problemes oberts.
  Si és verbal, afegir anàlisi retòrica, registres, intertextualitat.
  Fora de l'àrea de talent, adaptació estàndard pel MECR sense
  enriquiment forçat.

### Doble excepcionalitat
- **No**: enriquiment pur. El text pot ser llarg, complex i
  lingüísticament exigent.
- **Sí**: equilibri entre **repte cognitiu** (mantingut!) i **suports
  per a la dificultat associada** (TDAH, dislèxia, TEA, etc.). Per
  exemple, per a AC+TDAH: contingut profund però en micro-blocs amb
  indicadors de progrés. Per a AC+dislèxia: contingut conceptual
  exigent però amb lèxica simplificada i suport oral. Per a AC+TEA:
  contingut complex però amb estructura predictible i zero
  implicitura. **No reduir mai les expectatives cognitives** per la
  dificultat associada; combinar les dues skills.

## Exemple abans → després
Veure `assets/exemple-B2-fotosintesi.md` per a un exemple complet
d'adaptació (enriquiment) d'un text de ciències naturals nivell B2.

## Carregar context més profund
Si calen fonaments pedagògics (enriquiment vs. compactació vs.
acceleració, detecció primerenca, graelles d'observació DAC per edats,
doble excepcionalitat, col·laboració amb EAP i famílies, gestió de
l'alta sensibilitat emocional), carregar `references/perfil-complet.md`.
Si cal veure totes les fonts DAC (Departament d'Ensenyament — altes
capacitats), carregar `references/fonts.md`.
