---
name: write-manual
description: >
  Use when adapting or generating a manual (text expositiu instructiu) for
  students. Activates when genre_discursiu == "manual". Applies gradual
  progression (simple to complex), explicit causal connectors, and defined
  technical terms. Output: manual in markdown with title, entradeta, and
  ordered sections.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
genre_key: manual
tipologia: Expositiva
mecr_range: [A1, A2, B1, B2, C1]
agent_role: adapter
tools_required: []
triggers:
  - path: params.genere_discursiu
    equals: manual
---

# Escriure/adaptar un manual

## Quan activar aquesta skill
Activar quan el docent ha seleccionat el gènere "manual" al Pas 2 de
l'adaptador. El manual és un text expositiu organitzat en apartats que
presenta coneixements de manera progressiva i requereix definicions
explícites per ser accessible.

## Estructura canònica
Tot manual adaptat ha de tenir **aquestes parts, en aquest ordre**:

1. **Títol** — tema del manual.
2. **Entradeta** — introducció breu que anuncia què s'explicarà.
3. **Apartats amb paràgrafs** — desenvolupament dels continguts,
   un apartat per cada idea principal.

## Regles crítiques (FER)
- **Progressió simple → complex**: cada apartat es recolza en l'anterior.
- **Desnominalitzar processos**: "l'oxidació" → "quan s'oxida".
- **Connectors causals explícits**: "perquè", "per tant", "així doncs".
- **Exemples concrets abans de l'abstracció**.
- **Termes tècnics sempre definits** a la primera aparició, en negreta.

## Contraindicacions (NO FER)
- ❌ Apartats niats de més d'un nivell.
- ❌ Notes al peu que distreuen el flux.
- ❌ Referències a capítols posteriors ("ho veurem més endavant").
- ❌ Apel·lacions al lector adult.

## Modulació per MECR
- **A1-A2**: màxim 3 apartats. Frases curtes (10-12 paraules). Un sol
  terme tècnic per apartat, sempre definit. Exemples visuals i quotidians.
- **B1-B2**: 3-5 apartats. Connectors causals explícits. Definicions
  integrades en negreta.
- **C1**: estructura completa. Apartats amb subseccions si cal.
  Vocabulari tècnic definit a la primera aparició.

## Format de sortida
```markdown
# [Títol del manual]

[Entradeta: una o dues frases que anuncien què s'explicarà.]

## [Apartat 1]
[Paràgraf amb idea principal. **Terme tècnic**: definició breu.
Exemple concret.]

## [Apartat 2]
[Paràgraf que es recolza en l'apartat anterior.]

## [Apartat 3]
[Paràgraf final amb la idea més complexa.]
```

## Exemple
Veure `assets/exemple-basic-B1.md` per a un manual nivell B1.
