---
name: write-entrevista
description: >
  Use when adapting or generating an entrevista for students.
  Activates when genre_discursiu == "entrevista". Applies direct
  questions, first-person responses, visible labels, and preserved
  Q/A format. Output: entrevista in markdown with presentation and
  question/answer pairs.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
genre_key: entrevista
tipologia: Dialogada
mecr_range: [A1, A2, B1, B2, C1]
agent_role: adapter
tools_required: []
triggers:
  - path: params.genere_discursiu
    equals: entrevista
---

# Escriure/adaptar una entrevista

## Quan activar aquesta skill
Activar quan el docent ha seleccionat el gènere "entrevista" al Pas 2
de l'adaptador. L'entrevista és un gènere dialogat amb parells
pregunta/resposta que cal mantenir en l'adaptació.

## Estructura canònica
Tota entrevista adaptada ha de tenir **aquestes parts, en aquest
ordre**:

1. **Presentació** — qui és l'entrevistat i per què és rellevant.
2. **Parells pregunta/resposta** — amb etiquetes visibles.

## Regles crítiques (FER)
- **Preguntes directes, sense subordinades**: "Què fas quan estàs
  trist?".
- **Respostes simplificades** preservant la veu original (no en
  3a persona).
- **Marcar clarament qui parla** amb etiquetes visibles.
- **No linearitzar**: mantenir el format P/R, no convertir en
  prosa.
- **Explicar termes propis de l'entrevistat**.

## Contraindicacions (NO FER)
- ❌ Preguntes múltiples en una ("Com et dius i què fas?").
- ❌ Preguntes retòriques.
- ❌ Intervencions intermèdies ("i llavors, vostè què va
  pensar...").
- ❌ Respostes sense pregunta anterior.

## Modulació per MECR
- **A1-A2**: presentació d'una frase. 3-4 parells P/R molt
  curts. Vocabulari quotidià.
- **B1-B2**: entrevista estàndard amb 5-6 parells P/R i
  termes tècnics explicats.
- **C1**: entrevista completa amb 6-8 parells i matisos de
  l'entrevistat.

## Format de sortida
```markdown
# Entrevista a [nom de l'entrevistat]

[Presentació: qui és i per què és rellevant.]

**P:** [Pregunta directa 1?]

**R:** [Resposta en primera persona.]

**P:** [Pregunta directa 2?]

**R:** [Resposta en primera persona.]
```

## Exemple
Veure `assets/exemple-basic-B1.md` per a una entrevista nivell B1.
