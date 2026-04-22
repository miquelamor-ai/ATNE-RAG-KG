---
name: write-poema
description: >
  Use when adapting or generating a poema for students.
  Activates when genre_discursiu == "poema". Preserves strophic
  structure, concrete metaphors, and rhythm. Does not convert to
  prose. Output: poema in markdown with title, stanzas, and verses.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
genre_key: poema
tipologia: Narrativa / Expressiva
mecr_range: [A1, A2, B1, B2, C1]
agent_role: adapter
tools_required: []
triggers:
  - path: params.genere_discursiu
    equals: poema
---

# Escriure/adaptar un poema

## Quan activar aquesta skill
Activar quan el docent ha seleccionat el gènere "poema" al Pas 2 de
l'adaptador. El poema és un gènere líric amb estructura estròfica
que cal preservar en tota adaptació.

## Estructura canònica
Tot poema adaptat ha de tenir **aquestes parts**:

1. **Títol** — títol del poema.
2. **Estrofes** — grups de versos, preservats com a l'original.
3. **Versos** — línies individuals, mantingudes.

## Regles crítiques (FER)
- **Preservar estructura estròfica**: no fusionar estrofes ni
  aplanar versos.
- **No reescriure en prosa** (seria un altre gènere).
- **Simplificar vocabulari mantenint el ritme** quan sigui possible.
- **Metàfores concretes**: "el sol és una taronja" > "l'astre flamíger".
- **Rima**: conservar-la si es pot; si no, prioritzar la claredat.

## Contraindicacions (NO FER)
- ❌ Convertir en narrativa.
- ❌ Eliminar la divisió en estrofes.
- ❌ Explicar la metàfora dins del poema (trencaria la forma).
- ❌ Afegir comentaris o notes entre versos.

## Modulació per MECR
- **A1-A2**: versos curts (5-7 síl·labes). Metàfores molt
  concretes i visuals. Vocabulari quotidià. Rima si facilita
  la memòria.
- **B1-B2**: estrofes clares. Vocabulari accessible. Metàfores
  simples però suggerents.
- **C1**: estructura completa preservada. Vocabulari poètic
  accessible.

## Format de sortida
```markdown
# [Títol del poema]

[Vers 1]
[Vers 2]
[Vers 3]
[Vers 4]

[Vers 5]
[Vers 6]
[Vers 7]
[Vers 8]
```

## Exemple
Veure `assets/exemple-basic-A2.md` per a un poema nivell A2.
