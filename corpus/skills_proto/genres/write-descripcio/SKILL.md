---
name: write-descripcio
description: >
  Use when adapting or generating a descripció for students.
  Activates when genre_discursiu == "descripcio". Applies explicit
  spatial order, concrete comparisons, and separation of physical
  and emotional traits. Output: descripció in markdown with title,
  general description, and characteristics.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
genre_key: descripcio
tipologia: Expositiva / Descriptiva
mecr_range: [A1, A2, B1, B2, C1]
agent_role: adapter
tools_required: []
triggers:
  - path: params.genere_discursiu
    equals: descripcio
---

# Escriure/adaptar una descripció

## Quan activar aquesta skill
Activar quan el docent ha seleccionat el gènere "descripcio" al Pas 2
de l'adaptador. La descripció presenta característiques d'un objecte,
persona o lloc amb ordre espacial i concreció.

## Estructura canònica
Tota descripció adaptada ha de tenir **aquestes parts, en aquest ordre**:

1. **Títol** — objecte/persona/lloc descrit.
2. **Descripció general** — una frase que situa el que es descriu.
3. **Característiques** — detalls ordenats espacialment.

## Regles crítiques (FER)
- **Ordre espacial explícit**: de dalt a baix, de l'exterior a
  l'interior, etc.
- **Comparacions concretes** per a mides ("com una pilota de futbol").
- **Evitar superlatius sintètics**: "molt gran" > "grandíssim".
- **Una característica per frase** en nivells baixos.

## Contraindicacions (NO FER)
- ❌ Adjectius subjectius sense concretar ("molt bonic", "impressionant").
- ❌ Descripcions poètiques amb metàfores.
- ❌ Ordre aleatori de característiques.
- ❌ Barreja de descripció física i emocional.

## Modulació per MECR
- **A1-A2**: descripció general d'una frase. 3-4 característiques,
  una per frase. Comparacions amb objectes molt coneguts.
- **B1-B2**: 5-6 característiques amb ordre espacial clar. Dues
  característiques per frase si es pot.
- **C1**: descripció completa amb detalls i matisos. Ordre espacial
  respectat.

## Format de sortida
```markdown
# [Títol: objecte/persona/lloc]

[Descripció general: una frase que situa.]

- [Característica 1, ordenada espacialment]
- [Característica 2]
- [Característica 3]
- [Característica 4]
```

## Exemple
Veure `assets/exemple-basic-A2.md` per a una descripció nivell A2.
