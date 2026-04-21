---
name: write-reglament
description: >
  Use when adapting or generating a reglament for students.
  Activates when genre_discursiu == "reglament". Applies one-rule-per-
  item, direct imperative voice, thematic grouping, and separated
  consequences. Output: reglament in markdown with title, grouped
  rules, and consequences.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
genre_key: reglament
tipologia: Instructiva / Prescriptiva
mecr_range: [A1, A2, B1, B2, C1]
agent_role: adapter
tools_required: []
triggers:
  - path: params.genere_discursiu
    equals: reglament
---

# Escriure/adaptar un reglament

## Quan activar aquesta skill
Activar quan el docent ha seleccionat el gènere "reglament" al Pas 2
de l'adaptador. El reglament és un text prescriptiu amb normes
clares, agrupades per tema, i conseqüències separades.

## Estructura canònica
Tot reglament adaptat ha de tenir **aquestes parts, en aquest ordre**:

1. **Títol** — àmbit del reglament.
2. **Normes agrupades** — per tema, una per ítem.
3. **Conseqüències** — separades, en caixa específica.

## Regles crítiques (FER)
- **Una norma per ítem**, sense conjuncions ni comes complexes.
- **Veu imperativa directa**: "Respecta el torn", no "S'ha de
  respectar el torn".
- **Agrupar per tema**, no per ordre d'importància.
- **Conseqüències separades de les normes**, en caixa específica.
- **Positiu abans que negatiu**: "Escolta els altres" > "No
  interrompis".

## Contraindicacions (NO FER)
- ❌ Normes condicionals complexes ("Si X, llavors Y, excepte
  quan Z").
- ❌ Justificacions dins de la norma.
- ❌ Excepcions niades.
- ❌ Llenguatge legal tècnic sense explicar.

## Modulació per MECR
- **A1-A2**: 5-8 normes molt breus (imperatiu + objecte).
  Agrupació simple (2-3 temes). Conseqüències d'una frase.
- **B1-B2**: reglament estàndard amb 10-15 normes agrupades
  en 3-4 temes.
- **C1**: reglament complet amb normes, exemples i
  conseqüències desenvolupades.

## Format de sortida
```markdown
# [Títol del reglament]

## [Tema 1]
1. [Norma en imperatiu directe.]
2. [Norma positiva.]
3. [Norma positiva.]

## [Tema 2]
4. [Norma en imperatiu directe.]
5. [Norma positiva.]

## Conseqüències
[Text breu amb les conseqüències si no es compleixen les normes.]
```

## Exemple
Veure `assets/exemple-basic-A2.md` per a un reglament nivell A2.
