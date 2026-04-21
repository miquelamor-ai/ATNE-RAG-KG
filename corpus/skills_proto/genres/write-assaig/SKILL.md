---
name: write-assaig
description: >
  Use when adapting or generating an assaig for students.
  Activates when genre_discursiu == "assaig". Applies clear thesis in
  the introduction, integrated citations, and defined academic
  vocabulary. Output: assaig in markdown with introduction,
  development, and conclusion.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
genre_key: assaig
tipologia: Argumentativa / Reflexiva
mecr_range: [A1, A2, B1, B2, C1]
agent_role: adapter
tools_required: []
triggers:
  - path: params.genere_discursiu
    equals: assaig
---

# Escriure/adaptar un assaig

## Quan activar aquesta skill
Activar quan el docent ha seleccionat el gènere "assaig" al Pas 2 de
l'adaptador. L'assaig és un text reflexiu i argumentatiu amb tesi
clara i desenvolupament ordenat.

## Estructura canònica
Tot assaig adaptat ha de tenir **aquestes parts, en aquest ordre**:

1. **Introducció** — amb la tesi clara.
2. **Desenvolupament** — apartats que desenvolupen la tesi.
3. **Conclusió** — síntesi, no obertura.

## Regles crítiques (FER)
- **Tesi clara a la introducció** (no al final).
- **Cada apartat desenvolupa una idea del paraigua tesi**.
- **Cites integrades, no decoratives**: explicar per què importa
  la cita.
- **Vocabulari acadèmic definit** a la primera aparició.

## Contraindicacions (NO FER)
- ❌ Tesi implícita o ambigua.
- ❌ Digressions sense connexió amb la tesi.
- ❌ Llenguatge barroc o circumlocucions.
- ❌ Conclusions obertes ("cadascú que en pensi el que vulgui").

## Modulació per MECR
- **A1-A2**: assaig breu. Tesi d'una frase. Dos apartats curts.
  Conclusió d'una frase. Sense cites.
- **B1-B2**: assaig estàndard amb tesi + 3 apartats + conclusió.
  Una o dues cites integrades.
- **C1**: assaig complet amb tesi, 3-4 apartats amb cites i
  vocabulari acadèmic.

## Format de sortida
```markdown
# [Títol de l'assaig]

## Introducció
[Tesi clara, explícita.]

## [Apartat 1 - idea del paraigua tesi]
[Desenvolupament. "Cita integrada", diu [autor]. La cita importa
perquè...]

## [Apartat 2 - altra idea del paraigua tesi]
[Desenvolupament amb vocabulari acadèmic definit.]

## Conclusió
[Síntesi que reprèn la tesi.]
```

## Exemple
Veure `assets/exemple-basic-B2.md` per a un assaig nivell B2.
