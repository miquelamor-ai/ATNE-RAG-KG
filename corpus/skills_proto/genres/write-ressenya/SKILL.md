---
name: write-ressenya
description: >
  Use when adapting or generating a ressenya for students.
  Activates when genre_discursiu == "ressenya". Applies description
  before valuation, fact/judgment separation, and concrete
  recommendation. Output: ressenya in markdown with work,
  description, valuation, and recommendation.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
genre_key: ressenya
tipologia: Argumentativa / Avaluativa
mecr_range: [A1, A2, B1, B2, C1]
agent_role: adapter
tools_required: []
triggers:
  - path: params.genere_discursiu
    equals: ressenya
---

# Escriure/adaptar una ressenya

## Quan activar aquesta skill
Activar quan el docent ha seleccionat el gènere "ressenya" al Pas 2
de l'adaptador. La ressenya descriu i valora una obra amb arguments
separant clarament fets de judicis.

## Estructura canònica
Tota ressenya adaptada ha de tenir **aquestes parts, en aquest ordre**:

1. **Obra** — títol, autor i tipus.
2. **Descripció** — què és, de què tracta.
3. **Valoració** — què en pensem, amb arguments.
4. **Recomanació** — per a qui és adequada.

## Regles crítiques (FER)
- **Descripció abans de valoració**: primer què és, després què
  en pensem.
- **Separar fets de judicis**: "la pel·lícula dura 2 hores" (fet)
  vs "és massa llarga" (judici).
- **Recomanació concreta**: "bona per a nens de 8 a 10 anys" (no
  "recomanable").
- **Evitar spoilers**: no revelar el final.

## Contraindicacions (NO FER)
- ❌ Sarcasme o ironia.
- ❌ Comparacions amb obres no conegudes pel lector.
- ❌ Llenguatge crític especialitzat sense explicar.
- ❌ Valoracions sense argument.

## Modulació per MECR
- **A1-A2**: ressenya breu. Descripció d'una frase. Valoració
  amb un argument. Recomanació d'una frase.
- **B1-B2**: ressenya estàndard amb descripció, 2-3 valoracions
  argumentades i recomanació concreta.
- **C1**: ressenya completa amb anàlisi més elaborada i
  recomanació matisada.

## Format de sortida
```markdown
# [Títol de la ressenya]

**Obra:** [títol, autor, tipus (novel·la, pel·lícula, etc.).]

**Descripció:** [Què és, de què tracta, sense spoilers.]

**Valoració:**
- [Fet + judici argumentat.]
- [Fet + judici argumentat.]

**Recomanació:** [Per a qui és adequada, concret.]
```

## Exemple
Veure `assets/exemple-basic-B1.md` per a una ressenya nivell B1.
