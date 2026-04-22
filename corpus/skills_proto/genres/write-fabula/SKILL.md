---
name: write-fabula
description: >
  Use when adapting or generating a fàbula for students.
  Activates when genre_discursiu == "fabula". Applies explicit moral,
  archetypal characters, and maintained character traits.
  Output: fàbula in markdown with situation, action, denouement,
  and explicit moral.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
genre_key: fabula
tipologia: Narrativa
mecr_range: [A1, A2, B1, B2, C1]
agent_role: adapter
tools_required: []
triggers:
  - path: params.genere_discursiu
    equals: fabula
---

# Escriure/adaptar una fàbula

## Quan activar aquesta skill
Activar quan el docent ha seleccionat el gènere "fabula" al Pas 2 de
l'adaptador. La fàbula és una narració breu amb personatges
arquetípics (sovint animals) i una moral explícita al final.

## Estructura canònica
Tota fàbula adaptada ha de tenir **aquestes 4 parts, en aquest ordre**:

1. **Situació** — presentació dels personatges arquetípics.
2. **Acció** — el que fan els personatges.
3. **Desenllaç** — el resultat de les seves accions.
4. **Moral explícita** — la lliçó, al final, no subentesa.

## Regles crítiques (FER)
- **Moral explícita al final**, no subentesa.
- **Personatges arquetípics amb trets únics** (la llebre ràpida,
  la tortuga lenta).
- **Caràcters mantinguts**: si un personatge és llest al principi,
  ho és fins al final.
- **Llegendes**: situar en temps i lloc reals tot i ser ficció.

## Contraindicacions (NO FER)
- ❌ Morals ambigües o debatables.
- ❌ Evolució psicològica dels personatges.
- ❌ Referències històriques no explicades (llegendes).
- ❌ Llenguatge arcaic.

## Modulació per MECR
- **A1-A2**: fàbula molt breu (5-7 frases). Dos personatges amb un
  tret únic cada un. Moral d'una frase.
- **B1-B2**: fàbula estàndard amb 2-3 personatges arquetípics.
  Moral explícita clara.
- **C1**: fàbula completa amb descripcions més riques, però
  caràcters mantinguts i moral explícita.

## Format de sortida
```markdown
# [Títol de la fàbula]

[Situació: paràgraf amb personatges arquetípics i el seu tret únic.]

[Acció: paràgraf amb les accions dels personatges.]

[Desenllaç: paràgraf amb el resultat.]

**Moral:** [Frase explícita amb la lliçó.]
```

## Exemple
Veure `assets/exemple-basic-A2.md` per a una fàbula nivell A2.
