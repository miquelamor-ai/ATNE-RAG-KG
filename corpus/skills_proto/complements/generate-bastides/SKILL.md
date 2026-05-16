---
name: generate-bastides
deprecated: true
superseded_by: [generate-bastides-lectura, generate-bastides-produccio]
description: >
  DEPRECATED — substituïda per generate-bastides-lectura i generate-bastides-produccio.
  Use when the teacher has activated the "bastides" complement. Generates
  reading scaffolds (3 moments: before/during/after) and production
  scaffolds (4 blocks: base d'orientació, HCL starters, connectors,
  checklist). At Emergent/pre-A1: reading scaffolds only — no written
  production. Modulated by MECR level and genre/subject.
author: FJE — Fundació Jesuïtes Educació
version: 4.0.0-proto
complement_key: bastides
agent_role: complements
tools_required: []
triggers:
  - path: params.complements.bastides
    equals: true
---

# Generar bastides (suports de lectura i producció)

## Distinció fonamental (MALL)

Aquesta skill genera **dos tipus de bastides**:

- **Bastides de LECTURA** (sempre actives): guien l'alumne als 3 moments
  (Abans / Durant / Després) i als 3 plànols (literal / inferencial / crític).
- **Bastides de PRODUCCIÓ** (condicionals): s'activen **únicament** si hi ha
  `preguntes_comprensio` o `activitats_aprofundiment` actius. Contenen
  4 blocs: **A** base d'orientació · **B** iniciadors HCL · **C** connectors · **D** checklist.

El suport L1 (glossari + transliteració) va al complement Glossari. No repetir aquí.

## Gradació per nivell MALL

| Nivell | Bastides lectura | Producció | Bloc A | Bloc B | Bloc C | Bloc D |
|---|---|---|---|---|---|---|
| **Emergent (pre-A1)** | Físic/gestual: assenyalar, dibuixar, dramatitzar | ❌ Cap escriptura autònoma | ❌ | ❌ | ❌ | ❌ |
| **Inicial (A1)** | 1 ítem visual per moment | ✅ simplificada | 2-3 passos del gènere | 1 iniciador per HCL | `i`, `però`, `perquè` | ❌ |
| **Funcional (A2)** | 2 ítems per moment | ✅ blocs A+B+C | 3-4 passos + terminologia disciplinar | 2-3 per HCL, literals | + `primer`, `llavors`, `per tant` | 2-3 ítems |
| **Estratègic (B1)** | 2-3 ítems per moment | ✅ blocs A+B+C+D | Raonament disciplinar (hipòtesi, evidència) | Inferencials, causals | + `ja que`, `en canvi`, `tot i que` | 4-5 ítems |
| **Acadèmic (B2)** | 3 ítems + metacognició | ✅ blocs A+B+C+D | Superestructura del gènere + CALP | CALP, argumental | + `no obstant`, `atès que`, `en conseqüència` | Amb criteris avaluació |
| **Crític (C1)** | 3 ítems + autoregulació | ✅ blocs A+B+C+D | Contrast de fonts/arguments | Intencionalitat, retòrica | Dialectics | Reflexió fiabilitat/biaix |

## Principi: base d'orientació = GPS disciplinar

La base d'orientació (Bloc A) NO és genèrica. El LLM ha d'inferir els passos
concrets a partir del **gènere textual** i la **matèria**:

- ❌ genèric: *"Escriu la introducció, el desenvolupament i la conclusió."*
- ✅ disciplinar: *"Pregunta investigable: formula-la amb 'Si... llavors...' | Hipòtesi: el que creus que passarà | Resultats: presenta les dades en taula | Conclusió: torna a la pregunta i diu si la hipòtesi era correcta."*

## Format de sortida — OBLIGATORI

**Bastides de LECTURA (sempre):**
```markdown
## [Suports | Bastides (scaffolding)]

### Abans de llegir
- Activació: «Què saps de [tema]?»
- Predicció: «Mira el títol. Què creus que explicarà?»
- Propòsit: «Llegeix per saber [una cosa concreta].»

### Durant la lectura
- Subratlla [1-2 tipus d'informació clau]
- Marca al marge: ✓ entès · ? dubte · ! important

### Després de llegir
- Resum literal: «[buit per completar sobre la idea principal]»
- Inferència: «Quin creus que era l'objectiu de l'autor?»
- Valoració: «Amb quina idea estàs d'acord? Per què?»
```

**Bastides de PRODUCCIÓ (si `preguntes_comprensio` o `activitats_aprofundiment` actius):**
```markdown
### Per escriure [gènere], segueix aquest ordre:
1. [Pas 1 — terminologia disciplinar específica]
2. [Pas 2]
3. [Pas 3]

### Paraules per connectar les idees
[connectors del nivell MECR, NO la llista completa]

### Frases per començar
- [Habilitat]: «[iniciador 1]» / «[iniciador 2]»

### Comprova la teva resposta
- Has fet servir el lèxic de la matèria ([termes clau del text])?
- Has connectat les idees amb connectors?
- Has justificat amb evidències del text?
```

## Regles estrictes de sortida

- Pre-A1: **ZERO producció escrita autònoma**. Substitucions: assenyalar, dibuixar, dramatitzar, dictat a l'adult.
- Bloc A: **SEMPRE** infós de contingut disciplinar específic (gènere + matèria). Mai seqüència genèrica.
- Blocs B/C/D: **CONDICIONALS** — ometre si cap complement de producció actiu.
- Connectors: usar **EXACTAMENT** els del nivell MECR (no llista completa).
- **NO** repetir suport L1 (és al Glossari).
- **NO** donar respostes: l'alumne ha de completar els buits.
- Bloc D: vincular als criteris d'avaluació del docent si disponibles.

## Exemple
Veure `assets/exemple-ciencies-B1.md` (informe experimental, ESO 2n, MECR B1) i
`assets/exemple-historia-A2.md` (crònica, Primària Superior, MECR A2).
