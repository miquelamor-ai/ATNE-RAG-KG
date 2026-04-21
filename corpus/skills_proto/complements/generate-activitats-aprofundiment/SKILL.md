---
name: generate-activitats-aprofundiment
description: >
  Use when the teacher has activated the "activitats_aprofundiment" complement.
  Generates 2-3 cognitive challenge activities that extend the adapted text:
  interdisciplinary connections, critical thinking, guided research, debate and
  (when the text allows it) a plurilingual dimension. Modulated by stage and MECR.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
complement_key: activitats_aprofundiment
agent_role: complements
tools_required: []
triggers:
  - path: params.complements.activitats_aprofundiment
    equals: true
---

# Generar activitats d'aprofundiment

## Quan activar aquesta skill
Activar quan el docent ha marcat el complement **"Activitats d'aprofundiment"**
al Pas 2. Són activitats de **repte cognitiu** posteriors al text adaptat, NO
exercicis de comprensió literal. Serveixen per portar l'alumnat una passa més
enllà del text: connectar, qüestionar, investigar, argumentar.

## Què genera
Una secció `## Activitats d'aprofundiment` amb **2-3 activitats** triades entre
els cinc tipus següents (no cal incloure'ls tots — prioritza els que encaixin
amb el text i l'etapa):

1. **Connexions interdisciplinars** amb altres matèries (p.ex. un text de
   ciències connectat amb història o ètica).
2. **Pensament crític**: preguntes «per què?», «i si…?», «què passaria si…?»
   que obliguen a posicionar-se o a imaginar escenaris alternatius.
3. **Recerca guiada** (a casa o a biblioteca): una petita investigació amb
   fonts suggerides i un producte concret (una fitxa, un mapa, una entrevista).
4. **Debat o reflexió argumentada**: una pregunta polèmica amb dos bàndols
   possibles, o una reflexió personal justificada.
5. **Dimensió plurilingüe** (només si el text ho permet): «com es diu X en
   altres llengües de l'aula?», comparació d'expressions entre L1s dels
   alumnes, cerca d'equivalents culturals.

## Modulació per etapa i MECR

Adapta el nivell d'abstracció i la complexitat cognitiva:

| Etapa / MECR | Tipus d'activitat recomanada |
|---|---|
| **Infantil / Cicle Inicial (A1)** | Connexions molt concretes i visuals, recerca amb ajuda familiar, dibuix o creació. Evita debats abstractes. |
| **Cicle Mitjà / Superior (A2-B1)** | Comparacions, petites recerques a casa, preguntes «què passaria si…?» amb exemples propers. |
| **Secundària (B1-B2)** | Debat amb dos bàndols, connexió interdisciplinar explícita, recerca a fonts diverses, argumentació escrita. |
| **Batxillerat / FP (C1)** | Reflexió crítica amb detecció de biaixos, intertextualitat, hipòtesis contrafactuals, treball amb fonts contradictòries. |

Prioritza sempre activitats que **demanin producció de l'alumne** (no
consumir més informació), i que es puguin fer en un temps raonable (15-30
minuts, excepte recerques a casa).

## Format de sortida

La secció ha de començar SEMPRE amb `## Activitats d'aprofundiment` i contenir
2-3 ítems amb breu títol i consigna concreta:

```markdown
## Activitats d'aprofundiment

### 1. [Títol breu de l'activitat — tipus]
[Consigna clara i concreta, 1-3 frases. Inclou què ha de fer l'alumne i, si
escau, el producte final esperat.]

### 2. [Títol breu de l'activitat — tipus]
[Consigna clara i concreta.]

### 3. [Títol breu de l'activitat — tipus] (opcional)
[Consigna clara i concreta.]
```

## Regles estrictes de la sortida

- Comença **sempre** amb la línia literal `## Activitats d'aprofundiment`.
- **2 o 3 activitats**, no més. Millor poques i ben triades que moltes i
  difuses.
- Cada activitat amb un **títol curt** (4-8 paraules) que identifiqui el tipus
  (p.ex. «Debat», «Connexió amb història», «Recerca a casa», «I si…?»).
- Les consignes han de ser **accionables**: l'alumne ha de saber exactament
  què se li demana i com començar.
- **NO** generis activitats que siguin només preguntes de comprensió (això ja
  ho fa el complement `preguntes_comprensio`).
- **NO** generis activitats que requereixin materials que la majoria
  d'aules/llars no tenen (ex: microscopi, laboratori) — proposa alternatives
  accessibles.
- Si incloses una activitat plurilingüe, formula-la de manera que **no
  exposi** cap alumne concret ni l'obligui a parlar de la seva L1 si no
  vol.

## Exemple
Veure `assets/exemple-batxillerat-filosofia.md` (text de filosofia, 1r
Batxillerat, MECR C1).
