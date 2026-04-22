---
name: write-resum
description: >
  Use when adapting or generating a resum for students.
  Activates when genre_discursiu == "resum". Applies main-idea-first
  structure, logical connectors, and reformulation with accessible
  vocabulary. Output: resum in markdown with title, reference,
  and main/secondary ideas.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
genre_key: resum
tipologia: Expositiva
mecr_range: [A1, A2, B1, B2, C1]
agent_role: adapter
tools_required: []
triggers:
  - path: params.genere_discursiu
    equals: resum
---

# Escriure/adaptar un resum

## Quan activar aquesta skill
Activar quan el docent ha seleccionat el gènere "resum" al Pas 2 de
l'adaptador. El resum condensa un text original respectant-ne la veu
i organitzant les idees de manera lògica.

## Estructura canònica
Tot resum adaptat ha de tenir **aquestes parts, en aquest ordre**:

1. **Títol** — tema del resum.
2. **Referència original** — autor i obra resumida.
3. **Idea principal** — primera frase sense preàmbul.
4. **Idees secundàries** — desenvolupament amb connectors lògics.

## Regles crítiques (FER)
- **Idea principal al primer paràgraf**, sense preàmbul.
- **Conservar la veu del text original** (no interpretar).
- **Connectors d'ordre lògic** entre idees ("primer... després...
  finalment").
- **No citar literalment**: reformular amb vocabulari accessible.

## Contraindicacions (NO FER)
- ❌ Opinions del redactor.
- ❌ Cites textuals llargues.
- ❌ Repeticions del contingut original.
- ❌ Exemples no presents a l'original.

## Modulació per MECR
- **A1-A2**: idea principal en una frase curta. 2-3 idees
  secundàries. Connectors bàsics ("primer", "després").
- **B1-B2**: idea principal clara + 3-4 secundàries amb
  connectors variats.
- **C1**: resum complet amb matisos i connectors lògics
  precisos.

## Format de sortida
```markdown
# [Títol: tema del resum]

*Resum de [obra] de [autor].*

[Idea principal: primera frase sense preàmbul.]

Primer, [idea secundària 1]. Després, [idea secundària 2].
Finalment, [idea secundària 3].
```

## Exemple
Veure `assets/exemple-basic-B1.md` per a un resum nivell B1.
