---
name: write-conte
description: >
  Use when adapting or generating a conte (short story) for students.
  Activates when genre_discursiu == "conte". Applies linear chronology,
  explicit motivations, named emotions, and attributed dialogue.
  Output: conte in markdown with initial situation, conflict, and
  resolution.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
genre_key: conte
tipologia: Narrativa
mecr_range: [A1, A2, B1, B2, C1]
agent_role: adapter
tools_required: []
triggers:
  - path: params.genere_discursiu
    equals: conte
---

# Escriure/adaptar un conte

## Quan activar aquesta skill
Activar quan el docent ha seleccionat el gènere "conte" al Pas 2 de
l'adaptador. El conte és una narració breu amb estructura canònica
(situació-nus-resolució) i requereix claredat cronològica i emocional.

## Estructura canònica
Tot conte adaptat ha de tenir **aquestes 3 parts, en aquest ordre**:

1. **Situació inicial** — presentació de personatges i context.
2. **Nus** — conflicte o problema.
3. **Resolució** — final clar que tanca el conflicte.

## Regles crítiques (FER)
- **Cronologia lineal**: no flashbacks, no salts temporals.
- **Motivacions explícites**: "Lluc tenia por perquè estava sol"
  (no inferibles).
- **Emocions nomenades**: "estava trist", "es va enfadar".
- **Personatges principals persistents**: usar els mateixos noms,
  no pronoms.
- **Diàleg atribuït sempre**: "va dir la Marta", "va preguntar en Pau".

## Contraindicacions (NO FER)
- ❌ Narrador no fiable o ambigu.
- ❌ Temps narratius barrejats (passat amb present històric).
- ❌ Referències culturals implícites.
- ❌ Finals oberts o ambigus.
- ❌ Ironia o sarcasme.

## Modulació per MECR
- **A1-A2**: conte molt breu (5-8 frases). Dos personatges màxim.
  Emocions bàsiques ("content", "trist"). Un sol diàleg curt.
- **B1-B2**: conte estàndard amb 2-3 personatges i diàlegs
  atribuïts. Cronologia lineal clara.
- **C1**: conte complet amb descripcions i diàlegs més elaborats,
  però cronologia lineal i final tancat.

## Format de sortida
```markdown
# [Títol del conte]

[Situació inicial: un paràgraf amb personatges i context.]

[Nus: paràgraf amb el problema o conflicte.
"Diàleg atribuït" — va dir [personatge].]

[Resolució: paràgraf final amb desenllaç tancat.]
```

## Exemple
Veure `assets/exemple-basic-A2.md` per a un conte nivell A2.
