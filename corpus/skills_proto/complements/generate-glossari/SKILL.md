---
name: generate-glossari
description: >
  Use when the teacher has activated the "glossari" complement. Generates a
  markdown table of key terms from the adapted text, with simple explanations.
  If the student is a newcomer (nouvingut) with a known L1, includes a
  translation column in that L1 (in its native script).
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
complement_key: glossari
agent_role: complements
tools_required: []
triggers:
  - path: params.complements.glossari
    equals: true
variants:
  - monolingue   # quan l'alumne NO és nouvingut o L1 desconegut
  - bilingue     # quan l'alumne és nouvingut i L1 coneguda
---

# Generar glossari

## Quan activar aquesta skill
Activar quan el docent ha marcat el complement "glossari" al Pas 2.
La variant (monolingüe o bilingüe) es decideix automàticament segons el perfil:

- Si el perfil inclou `nouvingut.actiu=true` i `nouvingut.L1` està definit →
  **variant bilingüe** amb columna de traducció a aquesta L1.
- En qualsevol altre cas → **variant monolingüe**.

## Què genera
Una secció `## Glossari` amb una **taula markdown** que llista tots els termes
tècnics o difícils del text adaptat.

**Mínim 8-12 termes.** Si el text no té prou termes tècnics, completar amb
paraules que podrien ser difícils per a l'alumne concret (segons MECR i perfil).

## Variant monolingüe

```markdown
## Glossari

| Terme | Explicació simple |
|---|---|
| [terme en negreta] | [explicació en català nivell A1] |
```

Regles:
- L'explicació ha de ser en **català molt senzill (nivell A1)**, fins i tot si
  el MECR de l'alumne és superior.
- Frases de màxim 8 paraules.
- No usar altres termes tècnics a l'explicació: "un tipus de..." → especificar
  directament.
- No repetir el terme dins de la seva explicació.

## Variant bilingüe (nouvinguts amb L1 coneguda)

```markdown
## Glossari

| Terme | Traducció ({L1}) | Explicació simple |
|---|---|---|
| [terme] | [traducció real a L1, en alfabet original] | [català A1] |
```

Regles addicionals:
- La traducció ha de ser la **forma real** en la L1, no una transliteració.
- Usar l'**alfabet original** de la L1:
  - Àrab: الكتاب
  - Xinès: 书
  - Urdú: کتاب
  - Ciríl·lic: книга
  - Armeni: գիրք
- Si la L1 no té una paraula exacta per al concepte, usar la més propera i
  afegir aclariment breu entre parèntesis.

## Criteris de selecció de termes

Prioritzar, per aquest ordre:
1. **Termes curriculars del text** (Matemàtiques: equació, variable; Ciències:
   ecosistema, fotosíntesi; Història: monarquia, revolució).
2. **Paraules d'alta freqüència que poden ser ambigües** per MECR baix o L1
   diferent (pex: "mitjà" té múltiples sentits).
3. **Col·locacions** importants: "prendre una decisió", "tenir en compte".

NO prioritzar:
- Paraules quotidianes òbvies (casa, menjar, aigua).
- Noms propis excepte si són clau per la matèria.
- Connectors (perquè, però, així).

## Exemples
- `assets/exemple-monolingue-ciencies.md` (MECR B1, matèria ciències)
- `assets/exemple-bilingue-arab-historia.md` (nouvingut A2, L1 àrab, història)
