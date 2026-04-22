---
name: write-informe
description: >
  Use when adapting or generating an informe (report) for students.
  Activates when genre_discursiu == "informe". Applies executive
  summary, visual data presentation, and clear separation of facts
  and conclusions. Output: informe in markdown with resum executiu,
  objectiu, mètode, resultats, and conclusions.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
genre_key: informe
tipologia: Expositiva
mecr_range: [A1, A2, B1, B2, C1]
agent_role: adapter
tools_required: []
triggers:
  - path: params.genere_discursiu
    equals: informe
---

# Escriure/adaptar un informe

## Quan activar aquesta skill
Activar quan el docent ha seleccionat el gènere "informe" al Pas 2
de l'adaptador. L'informe és un text expositiu que presenta dades,
resultats i conclusions d'una manera estructurada i verificable.

## Estructura canònica
Tot informe adaptat ha de tenir **aquestes parts, en aquest ordre**:

1. **Títol** — tema de l'informe.
2. **Resum executiu** — què s'ha fet i què s'ha trobat, al principi.
3. **Objectiu** — per què s'ha fet l'informe.
4. **Mètode** — com s'ha fet.
5. **Resultats** — què s'ha trobat, amb dades visuals.
6. **Conclusions** — frase final prominent amb la idea clau.

## Regles crítiques (FER)
- **Resum executiu al principi** (què s'ha fet i què s'ha trobat).
- **Dades presentades visualment** (taules, llistes) abans de la prosa.
- **Conclusió destacada** com a frase final prominent.
- **Verbs en passat** per a accions fetes; **present** per a conclusions.

## Contraindicacions (NO FER)
- ❌ Opinions personals barrejades amb fets.
- ❌ Conclusions que no derivin dels resultats.
- ❌ Tecnicismes sense glossari.
- ❌ Referències a lectura futura.

## Modulació per MECR
- **A1-A2**: resum executiu d'una frase. Dades en llista simple.
  Conclusió d'una frase. Sense glossari (evitar tecnicismes).
- **B1-B2**: estructura completa amb taules bàsiques. Glossari al
  final si cal.
- **C1**: estructura completa. Taules i llistes detallades.
  Conclusions múltiples si és pertinent.

## Format de sortida
```markdown
# [Títol de l'informe]

### Resum executiu
[1-2 frases: què s'ha fet i què s'ha trobat.]

### Objectiu
[Per què s'ha fet l'informe.]

### Mètode
[Com s'ha fet, en passat.]

### Resultats
- Dada 1
- Dada 2
- Dada 3

### Conclusions
**[Frase final prominent amb la idea clau, en present.]**
```

## Exemple
Veure `assets/exemple-basic-B1.md` per a un informe nivell B1.
