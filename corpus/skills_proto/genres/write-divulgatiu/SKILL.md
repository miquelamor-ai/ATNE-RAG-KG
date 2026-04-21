---
name: write-divulgatiu
description: >
  Use when adapting or generating a text divulgatiu for students.
  Activates when genre_discursiu == "divulgatiu". Applies narrativitzed
  exposition, hook entradeta, short cites, and rounded figures.
  Output: text divulgatiu in markdown with title, entradeta, and
  narrative development.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
genre_key: divulgatiu
tipologia: Expositiva
mecr_range: [A1, A2, B1, B2, C1]
agent_role: adapter
tools_required: []
triggers:
  - path: params.genere_discursiu
    equals: divulgatiu
---

# Escriure/adaptar un text divulgatiu

## Quan activar aquesta skill
Activar quan el docent ha seleccionat el gènere "divulgatiu" al Pas 2
de l'adaptador. El text divulgatiu explica continguts científics o
tècnics amb to narratiu i accessible per a públic no expert.

## Estructura canònica
Tot text divulgatiu adaptat ha de tenir **aquestes parts, en aquest ordre**:

1. **Títol** — captador, clar, sense metàfores.
2. **Entradeta** — ganxo que captiva el lector i anuncia el tema.
3. **Desenvolupament narrativitzat** — el contingut s'explica com una
   història, amb exemples i cites.

## Regles crítiques (FER)
- **Entradeta captadora** però sense metàfores obscures.
- **Narrativitzar el contingut** (explicar com una història).
- **Cites curtes amb atribució clara** ("diu X, expert en Y").
- **Arrodonir xifres** ("més de 2 milions" enlloc de "2.347.812").

## Contraindicacions (NO FER)
- ❌ Tecnicismes sense explicar.
- ❌ Referències culturals implícites.
- ❌ Humor irònic (pot confondre).
- ❌ Frases incompletes o suspensives.

## Modulació per MECR
- **A1-A2**: entradeta d'una frase. Desenvolupament en 3-4 paràgrafs
  curts. Xifres molt arrodonides ("uns quants milers"). Una cita
  màxim.
- **B1-B2**: entradeta de dues frases. Desenvolupament amb 2-3 cites
  breus. Exemples concrets.
- **C1**: estructura completa amb múltiples fonts i exemples.

## Format de sortida
```markdown
# [Títol captador]

[Entradeta: ganxo inicial que anuncia el tema.]

[Paràgraf narratiu que explica una part del contingut.
"Cita curta" — atribució clara.]

[Paràgraf amb exemple concret i xifra arrodonida.]

[Paràgraf final que tanca la història.]
```

## Exemple
Veure `assets/exemple-basic-B1.md` per a un text divulgatiu nivell B1.
