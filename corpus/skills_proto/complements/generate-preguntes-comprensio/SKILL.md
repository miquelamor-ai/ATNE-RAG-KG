---
name: generate-preguntes-comprensio
description: >
  Use when the teacher has activated the "preguntes_comprensio" complement.
  Generates a comprehension reading guide following the MALL/TILC model: 3
  reading moments (before, during, after) × 3 cognitive levels (literal,
  inferential, critical). Modulated by matter, stage, MECR level and literary
  vs informative register of the text.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
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
Pas 2. Aquesta skill genera un guió estructurat que acompanya l'alumnat durant
la lectura, no un exàmen final.

## Model pedagògic: MALL/TILC
La comprensió lectora té **3 moments** cadascun amb un propòsit cognitiu propi:

| Moment | Propòsit | Nombre preguntes |
|---|---|---|
| **Abans de llegir** | Activació (hipòtesi + coneixements previs + propòsit) | 3 |
| **Durant la lectura** | Processament actiu (inferència + visualització + lèxic) | 3 |
| **Després de llegir** | Consolidació en 3 nivells cognitius (literal, inferencial, crític) | 7-8 |

Total: **13-14 preguntes**.

## Modulació per context

### Segons MECR i etapa

| Nivell | Adequació |
|---|---|
| **Infantil / Cicle Inicial (A1)** | Predicció visual, connexió amb el jo, dibuix. Evita «justifica» i «argumenta». Preguntes curtes. |
| **Cicle Mitjà / Superior (A2-B1)** | Idea principal, relacions, comparacions. |
| **Secundària (B1-B2)** | Arguments, connectors lògics, contrast de fonts. |
| **Batxillerat/FP (C1)** | Anàlisi crítica, intertextualitat, biaixos. |

### Segons modalitat del text

- **Text LITERARI** (conte, relat, poema, fantàstic, narrativa): preguntes
  afectives, d'identificació, d'imatges mentals, creatives. Deixa espais
  interpretatius.
- **Text INFORMATIU** (tot el que no és literari): precisió conceptual, dades,
  relacions causa-efecte, model teòric de la matèria.

### Tipologia interna (ús del model, NO mostrar a la sortida)

- **Nivell LITERAL**: oberta curta, V/F amb justificació, opció múltiple,
  omplir buits, relaciona amb fletxes.
- **Nivell INFERENCIAL**: «per què creus…?», «i si…?», relaciona causa-efecte.
- **Nivell CRÍTIC**: argumentativa oberta, transferència al jo, detecció de
  biaixos.

Alterna formats a Després de llegir (no totes obertes, no totes V/F).

## Format de sortida — OBLIGATORI

La resposta d'aquesta skill ha de ser EXACTAMENT aquesta estructura
(comença amb `## Preguntes de comprensió` i a dins tres sub-seccions `###`):

```markdown
## Preguntes de comprensió

### Abans de llegir
- [pregunta d'hipòtesi]
- [pregunta de connexió prèvia]
- [pregunta de propòsit]

### Durant la lectura
- [pregunta d'inferència en curs]
- [pregunta de visualització]
- [pregunta de lèxic en context]

### Després de llegir
- [pregunta literal 1]
- [pregunta literal 2]
- [pregunta inferencial 1]
- [pregunta inferencial 2]
- [pregunta crítica 1]
- [pregunta crítica 2]
- [1-2 més si cal, alternant formats]
```

## Regles estrictes de la sortida

- Comença **sempre** amb la línia literal `## Preguntes de comprensió`.
- Les tres sub-seccions han de ser **sempre** i en aquest ordre, amb els
  títols literals: `### Abans de llegir`, `### Durant la lectura`,
  `### Després de llegir`.
- **NO** escriguis la paraula «Moment» ni «Moment 1/2/3» als encapçalaments.
- **NO** posis sub-encapçalaments de nivell («Nivell LITERAL…») visibles.
- **NO** posis etiquetes entre claudàtors davant de cap pregunta
  (`[Literal · V/F]`, `[Inferencial · per què]`, `[Hipòtesi]`, `[Propòsit]`).
- Cada pregunta comença amb `- ` (vinyeta), text directe, sense numerar.
- Per als formats visuals (omplir buits, relaciona), integra'ls dins de la
  pregunta:
  - `- Omple els buits: El ______ serveix per ______.`
  - `- Relaciona amb una fletxa: aigua → …, foc → …`

## Exemple
Veure `assets/exemple-literari-A2.md` (text narratiu, MECR A2) i
`assets/exemple-informatiu-B1.md` (text expositiu, MECR B1).
