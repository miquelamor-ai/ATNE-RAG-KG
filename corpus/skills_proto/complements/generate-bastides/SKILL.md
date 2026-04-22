---
name: generate-bastides
description: >
  Use when the teacher has activated the "bastides" complement. Generates
  scaffolding supports following the MALL/TILC model (linguistic patterns of
  the subject + connectors + thematic vocabulary) to help the student PRODUCE
  answers, not just consume the text. Modulated by subject, stage, MECR, and
  whether the student is a newcomer (L1 known).
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
complement_key: bastides
agent_role: complements
tools_required: []
triggers:
  - path: params.complements.bastides
    equals: true
---

# Generar bastides (scaffolding)

## Quan activar aquesta skill
Activar quan el docent ha marcat el complement **"Bastides"** al Pas 2. Les
bastides no són una explicació del text; són **suports perquè l'alumne
produeixi**. Aquesta skill segueix el model **MALL/TILC**: patró lingüístic de
la matèria + connectors lògics adequats al MECR + lèxic temàtic + crosses per
guiar la lectura.

## Estructura obligatòria
La secció té **6 blocs**, cadascun en el seu ordre. No n'ometis cap (si no
aplica, explica breument per què o deixa un ítem de mínims).

### 1. Taula de connectors lògics
Taula amb els connectors que demanen el tipus de raonament del text/preguntes.
Adapta quantitat i complexitat al MECR.

| Funció | Connectors (modula complexitat segons MECR) |
|---|---|
| Causa | perquè, com que, ja que, a causa de |
| Conseqüència | per tant, així doncs, en conseqüència, per això |
| Oposició / contrast | però, en canvi, tanmateix, malgrat que |
| Exemplificació | per exemple, com ara, en concret |
| Conclusió | en resum, per acabar, en definitiva |

**Modulació per MECR**:
- A1-A2: 2-3 connectors per funció, els més bàsics (`perquè`, `però`,
  `per exemple`).
- B1-B2: gamma mitjana, inclou `en canvi`, `en conseqüència`.
- C1: tota la gamma, inclou sofisticats (`tanmateix`, `en definitiva`,
  `per contra`).

### 2. Frases model per argumentar amb el text
4-6 **bastides d'inici de frase** perquè l'alumne les completi:

```
- "Segons el text, ______ perquè ______."
- "Podem deduir que ______ ja que el text diu que ______."
- "A diferència de ______, ______ s'assembla a ______ perquè ______."
- "Un exemple d'això és ______."
- "Jo crec que ______, i ho justifico perquè ______."
```

**Modulació per MECR**:
- A1-A2: frases més curtes, amb 1-2 forats. Reutilitzar estructures.
- B1-B2: bastides estàndard com les del llistat anterior.
- C1: bastides amb tesi i contratesi, connectors argumentatius sofisticats.

### 3. Banc de paraules (lèxic temàtic)
**8-12 paraules** del patró lingüístic de la matèria, extretes del text adaptat
o complementàries, que l'alumne pot usar per respondre. Si escau, agrupa-les
per camp semàntic.

Format: `paraula1 – paraula2 – paraula3 – …`

Pedagogicament: prioritzar **paraules tècniques de la matèria + col·locacions
importants** (p.ex. Ciències: "fotosíntesi, clorofil·la, oxigen, absorbir…";
Història: "revolució, burgesia, proletariat, consolidar el poder…").

### 4. Suport visual recomanat
Indicar **2-3 suports visuals concrets** que afegirien valor (icones, colors
destacats, línies de temps, mapes, gràfiques, fotografies…) i **on ubicar-los
al text adaptat**. No dibuixes el suport — suggereixes al docent on posar-lo.

Exemples útils:
- "Línia de temps a sobre del paràgraf 2 amb les fases de la Revolució"
- "Icona 💧 al costat del concepte 'evaporació' per reforçar la visualització"
- "Gràfica de barres opcional per comparar les dades dels paràgrafs 3-4"

### 5. Crosses de lectura (abans d'engegar)
**2-3 pistes concretes** perquè l'alumne enfoqui la lectura des del principi:

- Què ha de buscar mentre llegeix (1-2 elements clau)?
- Com marcar el que és important (subratllar, prendre nota, fletxes al marge)?
- Quin és el propòsit d'aquesta lectura?

### 6. Suport L1 (només si l'alumne és nouvingut amb L1 coneguda)
Tradueix **5-8 conceptes més abstractes** del text a la L1 de l'alumne, en
l'alfabet original si escau (àrab: الكتاب, xinès: 书, urdú: کتاب, ciríl·lic:
книга).

Si l'alumne NO és nouvingut o la L1 no està informada, ometre aquest bloc i
escriure: `> No aplica: l'alumne no requereix suport L1.`

## Adequació per etapa educativa

Modula el tipus de crosses segons l'etapa (no només el MECR):

- **Infantil / Cicle Inicial**: crosses **FÍSIQUES i VISUALS** (imatges,
  colors, referents sonors, gestos). Evita conceptes abstractes.
- **Cicle Mitjà / Superior / ESO**: crosses **PROCEDIMENTALS** (estratègies
  de lectura, plantilles de resposta, taules comparatives, esquemes).
- **Batxillerat / FP**: estratègies de **SÍNTESI** i anàlisi crítica de
  múltiples fonts, bastides argumentatives sofisticades.

## Format de sortida

La secció ha de començar SEMPRE amb `## Bastides (scaffolding)` i contenir els
6 blocs en aquest ordre amb subseccions `###`:

```markdown
## Bastides (scaffolding)

### CONTEXT
- Matèria: [matèria]
- Etapa: [etapa] · MECR: [nivell]
- Si l'alumne és nouvingut, L1: [llengua]

### 1. Taula de connectors lògics
[taula markdown]

### 2. Frases model per argumentar amb el text
[bastides d'inici de frase]

### 3. Banc de paraules (lèxic temàtic)
[8-12 paraules]

### 4. Suport visual recomanat
[2-3 suggeriments amb ubicació]

### 5. Crosses de lectura (abans d'engegar)
[2-3 pistes]

### 6. Suport L1
[traduccions o "No aplica"]
```

## Regles estrictes de la sortida

- **SEMPRE** els 6 blocs. Si un no aplica, justificació breu i seguir endavant.
- **NO** inventis paraules o conceptes que no siguin al text adaptat (banc de
  paraules).
- **NO** donis respostes: les bastides són perquè l'alumne les completi.
- Els connectors han d'encaixar amb el MECR (ajustar complexitat).
- Si el text és literari (conte, poema, relat), adapta els connectors i
  bastides al registre (p.ex. `al principi`, `al final`, `de sobte` en comptes
  de `en conseqüència`).

## Exemple
Veure `assets/exemple-ciencies-B1.md` (text informatiu, ESO 3r, MECR B1).
