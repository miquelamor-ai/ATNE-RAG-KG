---
name: write-opinio
description: >
  Use when adapting or generating an opinió article for students.
  Activates when genre_discursiu == "opinio". Applies thesis-first
  structure, numbered arguments with evidence, and explicit
  argumentative connectors. Output: opinió in markdown with thesis,
  arguments, and conclusion.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
genre_key: opinio
tipologia: Argumentativa
mecr_range: [A1, A2, B1, B2, C1]
agent_role: adapter
tools_required: []
triggers:
  - path: params.genere_discursiu
    equals: opinio
---

# Escriure/adaptar un article d'opinió

## Quan activar aquesta skill
Activar quan el docent ha seleccionat el gènere "opinio" al Pas 2 de
l'adaptador. L'article d'opinió defensa una tesi amb arguments
recolzats en evidències concretes.

## Estructura canònica
Tot article d'opinió adaptat ha de tenir **aquestes parts, en aquest
ordre**:

1. **Tesi** — al primer paràgraf, sense preàmbul.
2. **Arguments amb evidència** — numerats o clarament separats.
3. **Conclusió** — reprèn la tesi.

## Regles crítiques (FER)
- **Tesi al primer paràgraf**, sense preàmbul.
- **Arguments numerats o clarament separats** (1 per paràgraf).
- **Cada argument amb evidència concreta** (dada, exemple, cita).
- **Conclusió que reprèn la tesi**, no n'introdueix cap d'altra.
- **Connectors argumentatius explícits**: "per tant", "en canvi",
  "a més".

## Contraindicacions (NO FER)
- ❌ Retòrica complexa (preguntes retòriques niades, paral·lelismes).
- ❌ Ironia (pot ser entesa literalment).
- ❌ Atacs personals.
- ❌ Tesis múltiples.

## Modulació per MECR
- **A1-A2**: tesi d'una frase. 2 arguments com a màxim, amb un
  exemple simple cada un. Conclusió d'una frase.
- **B1-B2**: tesi clara + 3 arguments amb evidència + conclusió.
- **C1**: estructura completa amb arguments més elaborats i
  evidències variades.

## Format de sortida
```markdown
# [Títol amb la tesi]

[Tesi: frase clara al primer paràgraf.]

**1.** [Argument 1 amb evidència concreta.]

**2.** [Argument 2 amb evidència concreta. A més, ...]

**3.** [Argument 3 amb evidència concreta. Per tant, ...]

[Conclusió: repren la tesi amb força.]
```

## Exemple
Veure `assets/exemple-basic-B1.md` per a un article d'opinió nivell B1.
