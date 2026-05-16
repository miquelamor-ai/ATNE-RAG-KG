---
name: generate-rubriques
description: >
  Use when the teacher has activated the "rubriques" complement. Generates a
  student-facing achievement rubric (rúbrica d'assoliment) for the production
  task derived from the adapted text. The rubric uses the FJE 4-level scale
  (NA/AS/AN/AE) written in first person so the student can self-assess. Modulated
  by MECR level and genre/subject. At Emergent/pre-A1: checklist with icons
  instead of rubric table.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
complement_key: rubriques
agent_role: complements
tools_required: []
triggers:
  - path: params.complements.rubriques
    equals: true
---

# Generar rúbrica d'assoliment

## Quan activar aquesta skill

Activar quan el docent ha marcat el complement **"Rúbrica d'assoliment"** al Pas 2.
Aquesta rúbrica és per a l'**alumne**, no per al docent. Permet l'autoavaluació i la
coavaluació. S'orienta a la producció derivada del text (activitat d'aprofundiment,
pregunta oberta, tasca escrita).

## Escala FJE

| Codi | Nom | Significat |
|---|---|---|
| **NA** | No Assolit | La producció no mostra l'habilitat requerida |
| **AS** | Assolit Satisfactòriament | Mostra l'habilitat amb suport o de forma bàsica |
| **AN** | Assolit Notablement | Mostra l'habilitat de forma clara i autònoma |
| **AE** | Assolit Excel·lentment | Supera les expectatives; creativitat o profunditat |

La rúbrica s'escriu en **primera persona** (l'alumne s'avalua: "He fet...", "He usat...").

## Gradació per nivell MALL

| Nivell | Format | Criteris | Escala |
|---|---|---|---|
| **Emergent (pre-A1)** | Checklist d'icones (✅/⬜) | 2-3 ítems molt concrets i visuals. Zero lèxic abstracte | Sense etiquetes NA/AS/AN/AE — icona ✅/⬜ |
| **Inicial (A1)** | Checklist de 3 ítems | Ítems molt curts (5-8 paraules). Lèxic quotidià | ✅ / ⬜ o Sí/No |
| **Funcional (A2)** | Taula 3 criteris × 3 nivells | Criteris de contingut + llengua | AS / AN / AE (sense NA) |
| **Estratègic (B1)** | Taula 3-4 criteris × 4 nivells | Criteris de contingut + llengua + estructura | NA / AS / AN / AE |
| **Acadèmic (B2)** | Taula 4 criteris × 4 nivells | + criteri de rigor acadèmic i evidències | NA / AS / AN / AE |
| **Crític (C1)** | Taula 4-5 criteris × 4 nivells | + criteri d'intencionalitat i contrast de fonts | NA / AS / AN / AE |

## Criteris a incloure (selecciona els que corresponen)

**Contingut** (sempre):
- He dit el que se'm demanava (contingut central)
- He usat el lèxic de la matèria
- He justificat amb exemples o evidències

**Llengua** (A2+):
- He connectat les idees amb connectors
- He escrit frases clares amb subjecte i verb explícit
- He usat el vocabulari del text

**Estructura** (B1+):
- He seguit els passos del gènere (base d'orientació)
- He organitzat les idees de forma coherent

**Rigor** (B2+):
- He aportat evidències, no només opinions
- He detectat si les fonts que cito són fiables

**Reflexió** (C1):
- He identificat la meva posició i l'he justificada
- He tingut en compte punts de vista alternatius

## Format de sortida

### Format Emergent (pre-A1) — Checklist icones

```markdown
## Comprovo el meu treball

- ⬜ He assenyalat la imatge correcta
- ⬜ He dit el nom en veu alta
- ⬜ He dibuixat el que he après
```

### Format A1-A2 — Checklist text

```markdown
## Comprovo el meu treball

- ⬜ He dit de què tracta el text
- ⬜ He usat paraules del text
- ⬜ He connectat les idees amb *i*, *però*, *perquè*
```

### Format B1+ — Taula d'assoliment

```markdown
## Rúbrica d'assoliment

| Criteri | NA | AS | AN | AE |
|---|---|---|---|---|
| **Contingut**: He explicat [el que demana la tasca] | No ho he fet | Ho he fet de forma bàsica | Ho he fet de forma clara | Ho he fet amb detalls i exemples propis |
| **Lèxic**: He usat el vocabulari de la matèria | No n'he usat | N'he usat poc | N'he usat els principals | N'he usat tots i els he explicat |
| **Estructura**: He seguit els passos del gènere [nom gènere] | No l'he seguit | N'he seguit alguns passos | L'he seguit gairebé tot | L'he seguit completament i l'he adaptat |
| **Llengua**: He connectat les idees amb connectors | No n'he usat | N'he usat 1-2 | N'he usat 3-4 | N'he usat molts i variats |
```

## Regles estrictes de sortida

- Comença **sempre** amb `## Rúbrica d'assoliment` (o `## Comprovo el meu treball` per a Emergent/A1).
- Els descriptors han de ser en **primera persona** i **accionables** (l'alumne sap exactament on se situa).
- **NO** usar termes abstractes ("qualitat", "adequat", "correcte") — substituir per comportaments observables.
- **NO** generar rúbriques si no hi ha cap tasca de producció al context (si no hi ha `preguntes_comprensio` obertes ni `activitats_aprofundiment` actius, avisar al docent).
- El nombre de criteris ha de ser **proporcional al MECR**: 2-3 criteris per a A1-A2, màxim 5 per a C1.
- La columna **AE** ha d'implicar un salt qualitatiu real (no "fer més"), sinó creativitat, autonomia o profunditat.
- Pre-A1: **ZERO taula**, ZERO escriptura autònoma. Usa exclusivament icones i ítems de assenyalar o dictar.
- Infereix el **gènere** del text i la tasca per personalitzar els descriptors (informe, crònica, argument, etc.).

## Exemple (B1, Història, crònica)

```markdown
## Rúbrica d'assoliment

| Criteri | NA | AS | AN | AE |
|---|---|---|---|---|
| **Contingut**: He explicat els fets principals de la crònica | No ho he fet | He explicat 1-2 fets | He explicat els fets principals amb ordre cronològic | He explicat els fets i he afegit causes i conseqüències |
| **Lèxic**: He usat vocabulari d'història | No n'he usat | He usat alguna paraula | He usat les paraules clau del text | He usat el vocabulari i l'he explicat amb les meves paraules |
| **Estructura**: He seguit els passos de la crònica (qui/on/quan → fets → conseqüències) | No l'he seguida | He seguit algun pas | He seguit la majoria dels passos | He seguit tots els passos i he afegit una valoració personal |
| **Llengua**: He usat connectors temporals (*primer*, *després*, *finalment*) | No n'he usat | N'he usat 1 | N'he usat 2-3 | N'he usat molts i de manera variada |
```
