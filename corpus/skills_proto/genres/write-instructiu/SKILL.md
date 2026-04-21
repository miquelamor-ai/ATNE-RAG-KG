---
name: write-instructiu
description: >
  Use when adapting or generating an instructiu text for students.
  Activates when genre_discursiu == "instructiu". Applies strict
  chronological order, single-verb steps, and independent steps.
  Output: instructiu in markdown with materials, numbered steps,
  and expected result.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
genre_key: instructiu
tipologia: Instructiva
mecr_range: [A1, A2, B1, B2, C1]
agent_role: adapter
tools_required: []
triggers:
  - path: params.genere_discursiu
    equals: instructiu
---

# Escriure/adaptar un text instructiu

## Quan activar aquesta skill
Activar quan el docent ha seleccionat el gènere "instructiu" al Pas 2
de l'adaptador. El text instructiu guia el lector per fer alguna
cosa amb passos clars i ordenats.

## Estructura canònica
Tot text instructiu adaptat ha de tenir **aquestes parts, en aquest
ordre**:

1. **Materials** — llista abans dels passos.
2. **Passos numerats** — un verb d'acció + un objecte concret.
3. **Resultat esperat** — què s'aconsegueix.

## Regles crítiques (FER)
- **Materials en llista** abans dels passos.
- **Cada pas = 1 verb d'acció + 1 objecte concret**.
- **Ordre cronològic estricte**: mai reordenar per legibilitat.
- **Passos independents**: cada pas s'ha de poder executar sense
  mirar el següent.
- **Subjecte "tu" explícit** quan calgui claredat.

## Contraindicacions (NO FER)
- ❌ Passos condicionals niats ("si X, fes Y; si no, fes Z").
- ❌ Passos implícits o omesos.
- ❌ Instruccions en passiva ("s'afegirà l'aigua").
- ❌ Observacions digressives al mig dels passos.

## Modulació per MECR
- **A1-A2**: 3-5 passos molt curts (1 verb + 1 objecte).
  Materials en llista molt simple.
- **B1-B2**: 5-7 passos amb materials detallats. Subjecte "tu"
  si cal claredat.
- **C1**: instructiu complet amb totes les indicacions, però
  passos sempre independents.

## Format de sortida
```markdown
# [Títol: què s'aprendrà a fer]

## Materials
- [Material 1]
- [Material 2]
- [Material 3]

## Passos
1. [Verb + objecte concret.]
2. [Verb + objecte concret.]
3. [Verb + objecte concret.]

## Resultat
[Què s'ha aconseguit.]
```

## Exemple
Veure `assets/exemple-basic-A2.md` per a un instructiu nivell A2.
