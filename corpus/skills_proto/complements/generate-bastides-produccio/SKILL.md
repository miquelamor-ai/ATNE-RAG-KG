---
name: generate-bastides-produccio
description: >
  Use when the teacher has activated the "bastides" complement AND at least one
  production complement is active (preguntes_comprensio or activitats_aprofundiment).
  Generates production scaffolds: (A) base d'orientació — genre-specific GPS with
  disciplinary reasoning steps; (B) catàleg de recursos — MECR-graduated connectors
  and HCL initiators; (C) pauta d'interrogació — self-assessment checklist.
  At Emergent/pre-A1: nothing generated — zero written production.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
complement_key: bastides
agent_role: complements
tools_required: []
triggers:
  - path: params.complements.bastides
    equals: true
  - condition: any_of
    paths:
      - params.complements.preguntes_comprensio
      - params.complements.activitats_aprofundiment
---

# Generar bastides de producció

## Funció d'aquest instrument

Les bastides de producció s'activen **únicament si hi ha producció** (preguntes
obertes o activitats d'aprofundiment). Contenen tres blocs:

- **Bloc A — Base d'orientació**: GPS del gènere, específic de matèria i disciplina.
- **Bloc B — Catàleg de recursos**: connectors MECR + iniciadors per HCL.
- **Bloc C — Pauta d'interrogació**: checklist d'autoavaluació específic de la tasca.

**PRE-A1: NO generar cap d'aquests blocs.** Zero escriptura autònoma.

## Context dins la Seqüència Didàctica (SD)

Els tres blocs es generen per a moments **distints** de la SD:

| Bloc | Fase SD | Funció |
|---|---|---|
| **Bloc A** — Base d'orientació | Fase 0-1 (Activació / Presentació del gènere) | GPS del gènere: el docent el presenta ABANS de la producció |
| **Bloc B** — Catàleg de recursos | Fase 2-3 (Comprensió / Teorització) | Es construeix DURANT l'anàlisi del text model |
| **Blocs A+B combinats** | Fase 4 (Transferència / Producció) | L'alumne els consulta com a referència mentre escriu |

## Principi crític: base d'orientació SEMPRE disciplinar

❌ **Genèric** (prohibit): *"Escriu la introducció, el desenvolupament i la conclusió."*

✅ **Disciplinar** (obligatori): *"1. Formula la pregunta investigable. 2. Escriu la hipòtesi (Si… llavors…). 3. Descriu els resultats en taula. 4. Conclou: la hipòtesi era correcta perquè…"*

La base d'orientació **s'infereix del gènere i la matèria del text original**. Si el gènere no és explícit, dedueix-lo del registre i el contingut.

## Gradació per nivell MALL

| Nivell | Bloc A | Bloc B | Bloc C |
|---|---|---|---|
| **Emergent (pre-A1)** | ❌ | ❌ | ❌ |
| **Inicial (A1)** | 2-3 passos molt concrets | 1 iniciador per HCL · connectors: *i, però, perquè* | ❌ |
| **Funcional (A2)** | 3-4 passos + terminologia disciplinar | 2-3 iniciadors · + *primer, llavors, per tant* | 2-3 ítems simples |
| **Estratègic (B1)** | Raonament disciplinar (hipòtesi, evidència, causa) | Inferencials · + *ja que, en canvi, tot i que* | 4-5 ítems |
| **Acadèmic (B2)** | Superestructura del gènere + CALP | CALP argumental · + *no obstant, atès que, en conseqüència* | Amb criteris d'avaluació |
| **Crític (C1)** | Contrast de fonts, biaix, intertextualitat | Dialectics, retòrica | Reflexió sobre fiabilitat i biaix |

## Format de sortida

```markdown
### Per escriure [nom del gènere], segueix aquest ordre:
1. [Pas 1 — terminologia disciplinar específica]
2. [Pas 2]
3. [Pas 3]
(4. [Pas 4 — si B1+])

### Paraules per connectar les idees
[Llista EXACTA dels connectors del nivell MECR — NO la llista completa]

### Frases per començar
- [HCL 1]: «[iniciador 1]» / «[iniciador 2]»
- [HCL 2]: «[iniciador 1]» / «[iniciador 2]»

### Comprova la teva resposta  *(si A2+)*
- Has fet servir el lèxic de la matèria ([2-3 termes clau del text])?
- Has connectat les idees amb connectors?
- [Criteri específic del gènere i la tasca]
```

## Regles estrictes de sortida

- **Pre-A1**: NO generar. Si el MECR és pre-A1, retornar silenci (cap secció).
- Bloc A: **SEMPRE** infós de contingut disciplinar. Els passos han de tenir noms propis de la matèria (no "introducció", "cos", "conclusió").
- Bloc B: usar **EXACTAMENT** els connectors del nivell MECR de les gradacions MALL. No afegir tots els nivells.
- Bloc C: vincular els criteris al gènere i la tasca concreta. Mai genèric.
- **NO** donar les respostes: l'alumne ha d'omplir els buits.
- Els iniciadors del Bloc B corresponen a les HCL rellevants per a la tasca (inferir quines HCL exigeix la producció a partir del gènere).
