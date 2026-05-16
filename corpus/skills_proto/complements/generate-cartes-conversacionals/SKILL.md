---
name: generate-cartes-conversacionals
description: >
  Use when the teacher has activated the "cartes_conversacionals" complement.
  Generates role-based conversation cards for structured class discussion or
  debate: sentence starters per role (proposer, objector, mediator, summarizer)
  calibrated to MECR level. Designed for B1+ (secondary school). At A2: simplified
  pair-talk cards. At pre-A1/A1: not generated — oral interaction requires
  in-person scaffolding only.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
complement_key: cartes_conversacionals
agent_role: complements
tools_required: []
triggers:
  - path: params.complements.cartes_conversacionals
    equals: true
---

# Generar cartes conversacionals

## Funció d'aquest instrument

Les **cartes conversacionals** bastiden la participació oral (o escrita en format
debat) donant a cada alumne un repertori d'iniciadors associats al seu **rol** dins
la conversa. No és una llista de connectors: cada carta = un rol + iniciadors
concrets per a aquella funció comunicativa.

El MALL les recomana per:
- Debats argumentats (activitats d'aprofundiment)
- Posades en comú estructurades (post-lectura)
- Discussions filosòfiques o científiques (B1+)

## Rols estàndard (ajusta al context)

| Rol | Funció |
|---|---|
| **Proposador/a** | Presenta una idea o posició |
| **Objector/a** | Qüestiona o contraposa |
| **Mediador/a** | Resumeix, cedeix la paraula, busca consens |
| **Sintetitzador/a** | Resumeix el que s'ha dit i treu conclusions |

Pots usar 2 rols (Proposador/Objector) o els 4. Adapta al nombre de membres del grup.

## Gradació per nivell MALL

| Nivell | Format | Iniciadors |
|---|---|---|
| **pre-A1 / A1** | ❌ No generar — la interacció oral requereix suport docent directe | — |
| **Funcional (A2)** | 2 rols (Proposador / Objector). Frases molt curtes | *"Jo crec que..."* / *"Però potser..."* |
| **Estratègic (B1)** | 3-4 rols. Frases completes per a cada HCL | Argumentar, justificar, reformular |
| **Acadèmic (B2)** | 4 rols. Registre formal. Iniciadors de debat acadèmic | Contrastiu, causal, hipotètic |
| **Crític (C1)** | 4 rols + metacognició del debat | Retòrica, detecció de biaix, citació de fonts |

## Format de sortida (B1)

```markdown
## Cartes per al debat

Cada membre del grup té un rol. Usa les frases de la teva carta per participar.

---

### 🟢 Proposador/a
*El teu rol: Presentes la teva idea principal i la justifiques.*

- «Jo crec que ___ perquè ___»
- «Des del meu punt de vista, ___ ja que ___»
- «La meva posició és ___ i la razó és ___»

---

### 🔴 Objector/a
*El teu rol: Qüestiones o afegeixes un punt de vista diferent.*

- «Tot i que entenc que ___, crec que ___»
- «Discrepo perquè ___»
- «I si en canvi ___?»

---

### 🟡 Mediador/a
*El teu rol: Dones la paraula, resums i busques acords.*

- «[Nom], quin és el teu punt de vista?»
- «Fins ara hem dit que ___. Algú vol afegir alguna cosa?»
- «Sembla que estem d'acord en ___ però no en ___»

---

### 🔵 Sintetitzador/a
*El teu rol: Al final, resums les idees principals i treus una conclusió.*

- «En resum, hem parlat de ___ i ___»
- «La conclusió del grup és ___»
- «El que no hem resolt és ___»
```

## Format simplificat (A2 — parelles)

```markdown
## Cartes per parlar en parella

### 🟢 Qui proposa
- «Jo penso que ___»
- «Crec que ___ perquè ___»

### 🔴 Qui respon
- «Estic d'acord perquè ___»
- «No estic d'acord perquè ___»
- «Potser, però ___»
```

## Regles estrictes de sortida

- Comença **sempre** amb `## Cartes per al debat`.
- **pre-A1 / A1**: NO generar. Retornar silenci o una nota per al docent: *(«A aquest nivell, la interacció oral requereix bastides en temps real del docent.»)*
- Els iniciadors han de ser **específics de la pregunta de debat** del text, no genèrics. Infereix la pregunta del text o dels complements actius (activitats d'aprofundiment).
- Usa **emojis de color** per distingir els rols (millora el reconeixement visual, especialment a A2-B1).
- Cada rol: màxim **3 iniciadors**. Millor pocs i clars que molts i confusos.
- Els iniciadors del rol **Sintetitzador** sempre inclouen un element obert ("El que no hem resolt és...") per fomentar pensament crític.
- A B2+, els iniciadors del rol Objector han d'incloure un iniciador de **citació** o **evidència**: *«Segons el text...», «D'acord amb [autor]...»*
