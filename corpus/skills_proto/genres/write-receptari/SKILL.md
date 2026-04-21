---
name: write-receptari
description: >
  Use when adapting or generating a receptari (recipe) for students.
  Activates when genre_discursiu == "receptari". Applies ingredients
  in order of use, single-verb steps, explicit quantities, and
  sensory indicators. Output: receptari in markdown with ingredients,
  preparation steps, and result.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
genre_key: receptari
tipologia: Instructiva
mecr_range: [A1, A2, B1, B2, C1]
agent_role: adapter
tools_required: []
triggers:
  - path: params.genere_discursiu
    equals: receptari
---

# Escriure/adaptar una recepta

## Quan activar aquesta skill
Activar quan el docent ha seleccionat el gènere "receptari" al Pas 2
de l'adaptador. La recepta és un text instructiu culinari amb
ingredients i passos específics.

## Estructura canònica
Tota recepta adaptada ha de tenir **aquestes parts, en aquest ordre**:

1. **Ingredients** — llista en ordre d'ús.
2. **Preparació** — passos numerats.
3. **Resultat** — què s'obté al final.

## Regles crítiques (FER)
- **Ingredients en ordre d'ús**, no alfabètic.
- **Cada pas = 1 verb d'acció + 1 objecte concret**.
- **No fusionar passos** ("Barreja i deixa reposar" → 2 passos).
- **Indicacions sensorials preferibles al temps** ("fins que sigui
  daurat" > "5 minuts").
- **Quantitats sempre explícites** amb unitat (2 ous, 200 g farina).

## Contraindicacions (NO FER)
- ❌ Passatges narratius ("La meva àvia sempre deia...").
- ❌ Condicionals opcionals ("Si vols, pots afegir...").
- ❌ Valoracions subjectives ("Quedarà molt bo").
- ❌ Referències culturals implícites.

## Modulació per MECR
- **A1-A2**: 4-6 passos molt curts. Ingredients bàsics (màx 5).
  Quantitats amb unitat visible.
- **B1-B2**: recepta estàndard amb 6-8 passos. Indicacions
  sensorials clares.
- **C1**: recepta completa amb 8-10 passos, però cada pas
  mantenint un verb i objecte concret.

## Format de sortida
```markdown
# [Nom del plat]

### Ingredients
- [Quantitat + ingredient 1]
- [Quantitat + ingredient 2]
- [Quantitat + ingredient 3]

### Preparació
1. [Verb + objecte concret.]
2. [Verb + objecte concret.]
3. [Verb + objecte + indicació sensorial.]

### Resultat
[Plat obtingut, amb indicació de racions.]
```

## Exemple
Veure `assets/exemple-basic-A2.md` per a una recepta nivell A2.
