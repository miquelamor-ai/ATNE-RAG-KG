---
name: write-diari
description: >
  Use when adapting or generating a diari entry for students.
  Activates when genre_discursiu == "diari". Applies first person,
  separation of facts and emotions, named emotions, and learning-
  oriented conclusion. Output: diari entry in markdown with date
  and entry body.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
genre_key: diari
tipologia: Narrativa / Reflexiva
mecr_range: [A1, A2, B1, B2, C1]
agent_role: adapter
tools_required: []
triggers:
  - path: params.genere_discursiu
    equals: diari
---

# Escriure/adaptar una entrada de diari

## Quan activar aquesta skill
Activar quan el docent ha seleccionat el gènere "diari" al Pas 2 de
l'adaptador. L'entrada de diari és un text personal en primera
persona que combina fets, emocions i reflexió.

## Estructura canònica
Tota entrada de diari adaptada ha de tenir **aquestes parts, en
aquest ordre**:

1. **Data** — quan s'escriu l'entrada.
2. **Entrada** — amb tres blocs: què ha passat, com m'he sentit,
   què penso.

## Regles crítiques (FER)
- **Primera persona sempre**: "he vist", "he pensat".
- **Separar fets d'emocions** en paràgrafs distints.
- **Nomenar les emocions explícitament**: "estava content",
  "em vaig avergonyir".
- **Conclusió orientada a l'aprenentatge**: "el que he après és...".

## Contraindicacions (NO FER)
- ❌ Reflexions filosòfiques abstractes.
- ❌ Dobles sentits o ironia.
- ❌ Crítiques a persones sense anonimitzar.
- ❌ Exageració dramàtica.

## Modulació per MECR
- **A1-A2**: entrada breu (5-7 frases). Tres blocs molt curts.
  Emocions bàsiques ("content", "trist", "enfadat").
- **B1-B2**: entrada estàndard amb tres paràgrafs diferenciats.
  Conclusió d'aprenentatge clara.
- **C1**: entrada completa amb reflexió més elaborada, però
  sempre concreta (no abstracta).

## Format de sortida
```markdown
# Diari — [Data]

**Què ha passat:** [Fets del dia, en primera persona.]

**Com m'he sentit:** [Emocions nomenades explícitament.]

**Què penso:** [Conclusió orientada a l'aprenentatge.]
```

## Exemple
Veure `assets/exemple-basic-A2.md` per a una entrada de diari nivell A2.
