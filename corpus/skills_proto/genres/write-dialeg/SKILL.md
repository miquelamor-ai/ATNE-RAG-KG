---
name: write-dialeg
description: >
  Use when adapting or generating a dialeg (dialogue) for students.
  Activates when genre_discursiu == "dialeg". Applies character list,
  named attribution, present-tense stage directions, and explicit
  subtext. Output: dialeg in markdown with characters, stage
  directions, and turns.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
genre_key: dialeg
tipologia: Dialogada
mecr_range: [A1, A2, B1, B2, C1]
agent_role: adapter
tools_required: []
triggers:
  - path: params.genere_discursiu
    equals: dialeg
---

# Escriure/adaptar un diàleg

## Quan activar aquesta skill
Activar quan el docent ha seleccionat el gènere "dialeg" al Pas 2 de
l'adaptador. El diàleg és un gènere teatral amb personatges,
acotacions i torns de paraula clarament marcats.

## Estructura canònica
Tot diàleg adaptat ha de tenir **aquestes parts, en aquest ordre**:

1. **Personatges** — llista inicial amb descripció breu.
2. **Acotacions** — entre parèntesis o en cursiva.
3. **Torns de paraula** — atribuïts amb el nom del personatge.

## Regles crítiques (FER)
- **Llistar personatges a l'inici** amb descripció breu (1 línia).
- **Atribuir cada torn amb el nom del personatge** (no amb
  lletres/inicials).
- **Acotacions al present i 3a persona**: "En Joan entra a
  l'habitació".
- **Subtext explícit**: si un personatge està enfadat, nomenar-ho
  a l'acotació.
- **Una acció per acotació**, sense subordinades.

## Contraindicacions (NO FER)
- ❌ Acotacions amb ironia o judicis ("Diu amb un to evidentment
  fals").
- ❌ Canvis d'escena implícits (marcar-los amb apartat).
- ❌ Llenguatge teatral arcaic o elevat.
- ❌ Monòlegs interns llargs (el teatre és acció externa).

## Modulació per MECR
- **A1-A2**: 2 personatges. 6-8 torns de paraula curts.
  Acotacions simples.
- **B1-B2**: 2-3 personatges. 10-12 torns. Acotacions clares
  amb subtext explícit.
- **C1**: diàleg complet amb 3-4 personatges i acotacions
  detallades.

## Format de sortida
```markdown
# [Títol del diàleg]

**Personatges:**
- [Nom 1]: [descripció breu d'una línia]
- [Nom 2]: [descripció breu d'una línia]

*([Acotació inicial que situa l'escena, en present.])*

**[Nom 1]:** [Torn de paraula.]

**[Nom 2]:** [Torn de paraula.]

*([Acotació amb una sola acció i subtext explícit.])*

**[Nom 1]:** [Torn de paraula.]
```

## Exemple
Veure `assets/exemple-basic-A2.md` per a un diàleg nivell A2.
