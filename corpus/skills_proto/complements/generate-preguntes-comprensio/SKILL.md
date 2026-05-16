---
name: generate-preguntes-comprensio
description: >
  Use when the teacher has activated the "preguntes_comprensio" complement.
  Generates a comprehension reading guide following the MALL/TILC model: 3
  reading moments (before, during, after) × 3 cognitive planes (literal,
  inferential, critical). Modulated by MECR level and literary vs informative
  register. Pre-A1: no autonomous writing — pointing, drawing, dramatisation,
  adult dictation only.
author: FJE — Fundació Jesuïtes Educació
version: 2.0.0-proto
complement_key: preguntes_comprensio
agent_role: complements
tools_required: []
triggers:
  - path: params.complements.preguntes_comprensio
    equals: true
---

# Generar preguntes de comprensió lectora

## Quan activar aquesta skill
Activar quan el docent ha marcat el complement **"Preguntes de comprensió"** al
Pas 2. Genera un guió que acompanya l'alumnat durant la lectura, no un examen final.

## Model pedagògic: MALL — 3 moments × 3 plànols

Principi rector: **"Menys és més"** (MALL). No fatigar l'alumne. Total: **6-10 preguntes**.

| Moment | Propòsit | Nombre |
|---|---|---|
| **Abans de llegir** | Activar coneixements previs, predicció, propòsit de lectura | 2-3 |
| **Durant la lectura** | Aturades estratègiques: dubtes lèxics, hipòtesi, resum parcial | 1-2 |
| **Després de llegir** | Interrogar el text als 3 plànols: literal → inferencial → crític | 3-5 |

## Modulació per MECR: format i plànol dominant

| Nivell MALL | Format permès | Plànol dominant (Després) | "Per què…?" |
|---|---|---|---|
| **Emergent (pre-A1)** | Assenyalar imatge, dibuixar, dramatitzar, dictat a l'adult. **Cap escriptura autònoma** | Via adult (propedèutic) | Oral i mediat per l'adult |
| **Inicial (A1)** | V/F textual senzill, omplir buits amb llista tancada o suport visual | Literal | Causa oral o guiada |
| **Funcional (A2)** | Ordenar seqüències, relacionar amb fletxes, elecció múltiple (idea principal) | Literal | Causa literal al text |
| **Estratègic (B1)** | Resposta breu, hipòtesis, causa-efecte | Inferencial | Deducció relacional |
| **Acadèmic (B2)** | Argumentació oberta, resum d'idees abstractes, superestructura del gènere | CALP / epistèmic | Justificació + model teòric |
| **Crític (C1)** | Contrast de fonts, anàlisi d'intencionalitat, argumentació fonamentada | Crític | Judici sobre fiabilitat |

> Els 3 plànols es treballen des d'infantil, però sempre **via adult** a pre-A1.
> El plànol crític s'introdueix oralment ja al conte de I5 («Què hauries fet tu?»).

## Modulació per modalitat del text

- **Text LITERARI** («Porta Oberta»): preguntes afectives («Com et sentiria?»),
  creatives («Què hauria passat si…?»), interpretació de metàfores i símbols.
  L'objectiu és el gaudi estètic i la construcció de sentit personal.
- **Text INFORMATIU** («Porta Tancada»): monitorització metacognitiva, precisió
  conceptual, jerarquització amb connectors, valoració de la fiabilitat de les dades.

## Format de sortida — OBLIGATORI

```markdown
## Preguntes de comprensió

### Abans de llegir
- [pregunta d'activació / predicció]
- [pregunta de propòsit: «Llegeix per saber…»]

### Durant la lectura
- [aturada: dubte lèxic o hipòtesi a verificar]

### Després de llegir
- [pregunta literal — format adequat al MECR]
- [pregunta inferencial — si MECR ≥ A2]
- [pregunta crítica / creativa — si literari o MECR ≥ B1]
```

## Regles estrictes de sortida

- Comença **sempre** amb `## Preguntes de comprensió`.
- Sub-seccions literals: `### Abans de llegir`, `### Durant la lectura`, `### Després de llegir`.
- **NO** etiquetes visibles de nivell (`[Literal]`, `[Inferencial]`, `[Hipòtesi]`…).
- **NO** numeració; cada pregunta comença amb `- `.
- Formats visuals integrats a la pregunta:
  - `- Omple els buits: El ______ serveix per ______.`
  - `- Relaciona amb una fletxa: sol → …, pluja → …`
- **Pre-A1**: substitueix les preguntes escrites per consignes d'acció:
  - `- Assenyala la imatge on es veu [concepte].`
  - `- Dibuixa com se sent el personatge.`
  - `- Fes com el personatge: [acció].`
- **NO** generar mai preguntes «copia i enganxa» (resposta copiable sense processament).
- **NO** V/F a pre-A1. V/F només des d'A1 i sempre senzill (paraula clau, no frase complexa).

## Exemple
Veure `assets/exemple-literari-A2.md` (text narratiu, MECR A2) i
`assets/exemple-informatiu-B1.md` (text expositiu, MECR B1).
