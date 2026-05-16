---
name: generate-resum-graduat
description: >
  Use when the teacher has activated the "resum_graduat" complement. Generates
  a graduated summary scaffold: a partially completed frame that guides the student
  to identify and express the main idea at the right level of abstraction for their
  MECR. NOT a comprehension question ("resumeix el text") — a structural frame
  with blanks calibrated to the level. At Emergent/pre-A1: visual/oral summary
  only. Modulated by MECR and text type.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
complement_key: resum_graduat
agent_role: complements
tools_required: []
triggers:
  - path: params.complements.resum_graduat
    equals: true
---

# Generar resum graduat

## Distinció fonamental

El **resum graduat** és una **bastida cognitiva**, NO una tasca oberta.
No li demanem a l'alumne "fes un resum" — li donem una estructura parcialmente
completa que li permet construir el resum pas a pas.

La gradació no és de complexitat del text sinó de **mida del forat**:
- A nivells baixos, la majoria del marc ja és donat; l'alumne omple 1-2 buits.
- A nivells alts, el marc és mínim (criteris) i l'alumne construeix lliurement.

## Recapitular com a pas previ

El MALL distingeix dos processos que sovint es confonen:

- **Recapitular** (pas previ, oral o visual): ordenar i seleccionar la informació sense produir
  text autònom — ordenar imatges, dictat a l'adult, respondre "qui / on / quan".
- **Resumir** (producció): generar un text coherent que condensa el principal.

A pre-A1 i A1, el resum graduat treballa el **recapitular**. El resumir escrit és la
fita final d'un procés progressiu.

### Eines de bastida per a A1-A2 (validat MALL)

- **Textos amb llacunes (cloze)**: frase marc amb 1-3 buits — l'alumne tria d'una llista o omple.
- **Ordenació de seqüències**: frases o imatges desordenades que l'alumne ordena lògicament.
- **Columna de selecció**: llista d'idees on l'alumne marca les que pertanyen al tema principal.

## Diferència amb altres instruments

| Instrument | Funció |
|---|---|
| **Resum graduat** | Bastida per *produir* un resum propi pas a pas |
| **Preguntes de comprensió** | Avaluació de comprensió literal/inferencial |
| **Base d'orientació** | GPS per a gèneres de producció complexa (informe, argumentació) |

## Gradació per nivell MALL

| Nivell | Format | Forat | Producció |
|---|---|---|---|
| **Emergent (pre-A1)** | Seqüència d'imatges a ordenar + dictat oral | Cap escriptura | Adult escriu el que l'alumne diu |
| **Inicial (A1)** | Frase marc amb 1-2 buits i opcions | Mínim | Triar la paraula correcta d'una llista |
| **Funcional (A2)** | Marc de 2-3 frases amb 3-4 buits clau | Moderat | Completar els buits sense opcions |
| **Estratègic (B1)** | Marc de 3 frases (tema / punts clau / conclusió) | Mig obert | Completar amb paraules pròpies |
| **Acadèmic (B2)** | Criteris de qualitat del resum (3-4 ítems) | Obert | Produir el resum complert |
| **Crític (C1)** | Rúbrica de metacognició | Autoregulat | Resum + reflexió sobre les tria |

## Format de sortida

### Format Emergent (pre-A1)

```markdown
## Resum del text (amb el teu mestre/a)

🗣️ Activitat oral: Explica amb paraules teves (o assenyalant les imatges)...
- De qui parla el text?
- Què fa o li passa?
- Com acaba?

*(El docent o un company escriu el que l'alumne diu.)*
```

### Format A1

```markdown
## Resum

Completa la frase:

El text parla de **___** [tria: *[opció 1]* / *[opció 2]* / *[opció 3]*].

El [personatge/tema] **___** [tria: *[opció 1]* / *[opció 2]*] perquè **___**.
```

### Format A2

```markdown
## Resum

Completa el resum del text:

El text explica [tema principal] _____________________________.

Els punts més importants són: _____________________________ i _____________________________.

Al final, _____________________________.
```

### Format B1

```markdown
## Resum

Escriu el resum en 3 parts:

**Tema**: De què tracta el text? (1 frase) → ___________________________

**Punts clau**: Quines idees principals desenvolupa? (2-3 frases) → ___________________________

**Conclusió o valoració**: Amb quina idea es tanca? (1 frase) → ___________________________
```

### Format B2+

```markdown
## Resum

Escriu el teu resum (5-8 línies). Assegura't que:
- [ ] Has identificat el tema central (no els exemples)
- [ ] Has seleccionat les idees principals, no les secundàries
- [ ] Has usat les teves paraules (no has copiat frases literals)
- [ ] Has fet servir connectors per cohesionar ([connectors MECR])
- [ ] El resum es pot entendre sense llegir el text original
```

## Regles estrictes de sortida

- Comença **sempre** amb `## Resum`.
- **Pre-A1**: ZERO escriptura autònoma. Proposta oral amb imatges; el docent o company escriu.
- Els buits han de ser **completables en 1-3 paraules** (A1-A2). No demanes frases senceres on no toca.
- Les opcions a triar (A1) han de tenir **una resposta clarament correcta** i opcions plausibles però incorrectes.
- El marc ha de reflectir l'estructura del **text concret** (si és narratiu, usa *personatge/acció/desenllaç*; si és informatiu, usa *tema/punts clau/conclusió*).
- **NO** generies un resum model: l'alumne ha de construir el seu.
- A B2+, els criteris han de ser específics del text, no genèrics.
