---
name: write-cronica
description: >
  Use when adapting or generating a crònica for students.
  Activates when genre_discursiu == "cronica". Applies explicit
  chronology, visible chronicler perspective, and concrete sensory
  descriptions. Output: crònica in markdown with title and moments
  ordered chronologically.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
genre_key: cronica
tipologia: Narrativa / Testimonial
mecr_range: [A1, A2, B1, B2, C1]
agent_role: adapter
tools_required: []
triggers:
  - path: params.genere_discursiu
    equals: cronica
---

# Escriure/adaptar una crònica

## Quan activar aquesta skill
Activar quan el docent ha seleccionat el gènere "cronica" al Pas 2
de l'adaptador. La crònica narra un esdeveniment amb la perspectiva
del cronista i descripcions sensorials concretes.

## Estructura canònica
Tota crònica adaptada ha de tenir **aquestes parts, en aquest ordre**:

1. **Títol** — esdeveniment narrat.
2. **Moments ordenats cronològicament** — amb marcadors temporals
   explícits.

## Regles crítiques (FER)
- **Cronologia explícita amb marcadors** ("A les 9 del matí...").
- **Perspectiva del cronista sempre visible**: "vaig veure",
  "vam anar".
- **Descripcions sensorials concretes** (què es veu, què se sent).
- **Separar fet de valoració**: primer què va passar, després què
  va semblar.

## Contraindicacions (NO FER)
- ❌ Salts temporals (no flashback, no flash-forward).
- ❌ Opinions barrejades amb els fets.
- ❌ Especulació sobre el que altres pensaven.
- ❌ Jocs estilístics (metàfora estesa, ironia).

## Modulació per MECR
- **A1-A2**: 3-4 moments amb marcadors simples ("primer",
  "després"). Frases curtes. Una descripció sensorial per moment.
- **B1-B2**: 4-5 moments amb hores concretes. Descripcions
  sensorials més detallades.
- **C1**: crònica completa amb 5-6 moments, descripcions riques
  i valoracions separades dels fets.

## Format de sortida
```markdown
# [Títol: esdeveniment narrat]

**[Marcador temporal 1]**, [què va passar + descripció sensorial].

**[Marcador temporal 2]**, [fet + perspectiva del cronista].

**[Marcador temporal 3]**, [fet + descripció].

[Valoració final, separada dels fets.]
```

## Exemple
Veure `assets/exemple-basic-B1.md` per a una crònica nivell B1.
