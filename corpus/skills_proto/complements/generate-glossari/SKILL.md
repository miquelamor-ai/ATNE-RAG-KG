---
name: generate-glossari
description: >
  Use when the teacher has activated the "glossari" complement. Generates a
  markdown glossary of key terms from the adapted text. Monolingüe or bilingüe
  (with L1 column in native script) depending on whether the student is a
  newcomer. Quantity and format modulated by MECR level: Emergent uses a
  visual icon+word list (no table); from A1 upwards uses a markdown table.
author: FJE — Fundació Jesuïtes Educació
version: 2.0.0-proto
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

Activar quan el docent ha marcat el complement **"Glossari"** al Pas 2.
La variant (monolingüe o bilingüe) es decideix automàticament:

- `nouvingut.actiu=true` i `nouvingut.L1` definit → **variant bilingüe**.
- Qualsevol altre cas → **variant monolingüe**.

## Graduació MALL per nivell

| Nivell | Nombre de termes | Tipus de lèxic | Format |
|---|---|---|---|
| **Emergent (pre-A1)** | 3-5 | Objectes reals, noms concrets. **NO** tecnicismes | Icona + paraula (no taula) |
| **Inicial (A1)** | 5-8 | Noms + verbs d'acció | Taula |
| **Funcional (A2)** | 8-10 | Noms + verbs + adjectius clau | Taula |
| **Estratègic (B1)** | 10-12 | + habilitats (hipòtesi, causa, conseqüència) | Taula |
| **Acadèmic (B2) / Crític (C1)** | 12-15 | Lèxic d'especialitat (CALP) | Taula |

## Format Emergent (pre-A1) — visual, sense taula

A Emergent, la taula és massa complexa. Format: emoji + **terme** (+ L1 si nouvingut).

**Monolingüe Emergent:**
```markdown
## Glossari

☀️ **sol**
💧 **aigua**
🌳 **arbre**
```

**Bilingüe Emergent (nouvingut + L1):**
```markdown
## Per llegir junts: pictograma + L1 + català

☀️ **sol** — شمس
💧 **aigua** — ماء
🌳 **arbre** — شجرة
```

## Variant monolingüe (A1+)

```markdown
## Glossari

| Terme | Explicació simple |
|---|---|
| **[terme]** | [explicació en català molt senzill, màx. 8 paraules] |
```

Regles:
- Explicació en **català molt senzill (nivell A1)**, sigui quin sigui el MECR de l'alumne.
- Màxim 8 paraules per explicació.
- No usar altres termes tècnics dins de l'explicació.
- No repetir el terme dins de la seva explicació.

## Variant bilingüe A1+ (nouvinguts amb L1 coneguda)

```markdown
## Glossari

| Terme | Traducció ({L1}) | Explicació simple |
|---|---|---|
| **[terme]** | [traducció en alfabet original de la L1] | [català A1] |
```

Regles addicionals:
- Usar l'**alfabet original** de la L1: àrab الكتاب, xinès 书, urdú کتاب, ciríl·lic книга, armeni գիրք.
- Si no existeix paraula exacta en L1, usar la més propera + aclariment breu entre parèntesis.

## Criteris de selecció de termes

Prioritzar, per ordre:
1. **Termes curriculars del text** (Matemàtiques: equació; Ciències: fotosíntesi; Història: monarquia).
2. **Paraules d'alta freqüència ambigues** per MECR baix o L1 diferent (ex: "mitjà" té múltiples sentits).
3. **Col·locacions** importants: "prendre una decisió", "tenir en compte".

NO prioritzar:
- Paraules quotidianes òbvies (casa, menjar, aigua) — excepte a Emergent on sí poden ser noves.
- Noms propis excepte si són clau per la matèria.
- Connectors (perquè, però, així).

## Exemples
- `assets/exemple-monolingue-ciencies.md` (MECR B1, ciències)
- `assets/exemple-bilingue-arab-historia.md` (nouvingut A2, L1 àrab, història)
- `assets/exemple-emergent-infantil.md` (pre-A1, infantil, bilingüe)
