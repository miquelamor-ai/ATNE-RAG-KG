---
name: write-carta
description: >
  Use when adapting or generating a carta for students.
  Activates when genre_discursiu == "carta". Applies motive-first
  structure, single concrete petition, and register adjusted to
  addressee. Output: carta in markdown with header, greeting,
  motive, body, petition, farewell, and signature.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
genre_key: carta
tipologia: Argumentativa / Dialogada
mecr_range: [A1, A2, B1, B2, C1]
agent_role: adapter
tools_required: []
triggers:
  - path: params.genere_discursiu
    equals: carta
---

# Escriure/adaptar una carta

## Quan activar aquesta skill
Activar quan el docent ha seleccionat el gènere "carta" al Pas 2 de
l'adaptador. La carta és un text comunicatiu amb estructura fixa i
registre ajustat al destinatari.

## Estructura canònica
Tota carta adaptada ha de tenir **aquestes parts, en aquest ordre**:

1. **Capçalera** — data i lloc.
2. **Salutació** — adreçada al destinatari.
3. **Motiu** — per què s'escriu, al primer paràgraf.
4. **Cos** — desenvolupament breu.
5. **Petició** — concreta i única.
6. **Comiat** — fórmula de cloenda.
7. **Signatura** — nom del remitent.

## Regles crítiques (FER)
- **Motiu al primer paràgraf**: per què escrius.
- **Petició concreta i única**: què vols que faci el destinatari.
- **Una acció per carta**: no barrejar demandes.
- **Registre ajustat al destinatari**: formal (institució) o
  informal (amic).
- **Frases 15-20 paraules màx, veu activa**.

## Contraindicacions (NO FER)
- ❌ Fórmules arcaiques ("En prego acceptació de les més
  distingides salutacions").
- ❌ Introduccions llargues abans del motiu.
- ❌ Múltiples peticions barrejades.
- ❌ Abreviatures sense explicar.

## Modulació per MECR
- **A1-A2**: carta molt breu. Motiu d'una frase. Cos de 2-3
  frases. Petició d'una frase.
- **B1-B2**: carta estàndard amb tots els blocs desenvolupats.
- **C1**: carta completa amb matisos de registre.

## Format de sortida
```markdown
[Lloc], [data]

[Salutació: "Benvolgut/da [nom]," o "Hola [nom],"]

[Motiu: per què escric, al primer paràgraf.]

[Cos: desenvolupament breu.]

[Petició: una sola demanda concreta.]

[Comiat: "Atentament," / "Salutacions cordials," / "Fins aviat,"]

[Signatura]
```

## Exemple
Veure `assets/exemple-basic-B1.md` per a una carta nivell B1.
