---
name: write-biografia
description: >
  Use when adapting or generating a biografia for students.
  Activates when genre_discursiu == "biografia". Applies strict
  chronological order, 3-5 key facts, complete dates, and separation
  of facts and legacy. Output: biografia in markdown from birth to
  death/legacy.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
genre_key: biografia
tipologia: Narrativa
mecr_range: [A1, A2, B1, B2, C1]
agent_role: adapter
tools_required: []
triggers:
  - path: params.genere_discursiu
    equals: biografia
---

# Escriure/adaptar una biografia

## Quan activar aquesta skill
Activar quan el docent ha seleccionat el gènere "biografia" al Pas 2
de l'adaptador. La biografia és una narració cronològica de la vida
d'una persona, amb fets seleccionats i context clar.

## Estructura canònica
Tota biografia adaptada ha de tenir **aquestes parts, en aquest ordre**:

1. **Naixement** — data i lloc.
2. **Infància** — context familiar i educatiu.
3. **Fets principals** — 3-5 fets màxim.
4. **Mort/llegat** — final de la vida i per què importa.

## Regles crítiques (FER)
- **Ordre cronològic estricte**: naixement → infància → fets →
  mort/llegat.
- **3-5 fets principals màxim**; no llista exhaustiva.
- **Dates completes**: "el 15 de març de 1879", no "1879" ni "s. XIX".
- **Contextualitzar lloc i època breument** ("a Alemanya, fa 150 anys").
- **Separar fets de llegat**: primer què va fer, després per què importa.

## Contraindicacions (NO FER)
- ❌ Flashbacks ("però tornem als seus inicis...").
- ❌ Especulació ("potser pensava que...").
- ❌ Detalls íntims sense rellevància.
- ❌ Xifres romanes per a segles.

## Modulació per MECR
- **A1-A2**: biografia molt breu. 2-3 fets màxim. Dates senzilles
  ("l'any 1879" o "fa molts anys"). Llegat en una frase.
- **B1-B2**: biografia estàndard amb 3-4 fets principals i
  context.
- **C1**: biografia completa amb 5 fets, context històric i
  llegat desenvolupat.

## Format de sortida
```markdown
# [Nom de la persona]

[Naixement: data completa + lloc. "A [lloc], fa [X] anys".]

[Infància: context familiar i educatiu.]

[Fet principal 1.]

[Fet principal 2.]

[Fet principal 3.]

[Mort/llegat: data + per què importa.]
```

## Exemple
Veure `assets/exemple-basic-B1.md` per a una biografia nivell B1.
