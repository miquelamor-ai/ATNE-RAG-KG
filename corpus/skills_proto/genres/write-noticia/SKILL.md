---
name: write-noticia
description: >
  Use when adapting or generating a news article (notícia periodística) for
  students. Activates when genre_discursiu == "noticia". Applies inverted
  pyramid structure, 5W lead, and contextual explanation for accessibility.
  Output: news article in markdown with titular, lead, and body.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
genre_key: noticia
tipologia: Narrativa / Expositiva
mecr_range: [A1, A2, B1, B2, C1]
---

# Escriure/adaptar una notícia

## Quan activar aquesta skill
Activar quan el docent ha seleccionat el gènere "notícia" al Pas 2 de
l'adaptador. La notícia és una narrativa informativa amb estructura canònica
(piràmide invertida) que requereix decisions específiques per ser accessible.

## Estructura canònica
Tota notícia adaptada ha de tenir **aquestes 3 parts, en aquest ordre**:

1. **Titular** — una frase que resumeix què ha passat. Sense jocs de paraules.
2. **Lead** (entradeta) — primera frase o paràgraf que respon les **5W**:
   - **Qui** (subjecte principal)
   - **Què** (acció o esdeveniment)
   - **Quan** (data o moment)
   - **On** (lloc concret)
   - **Per què** (motivació o causa, si es coneix)
3. **Cos** — desenvolupament amb estructura de **piràmide invertida**: el més
   important al principi, el menys important al final.

## Regles crítiques (FER)
- **Piràmide invertida**: si el lector deixa de llegir al 2n paràgraf, ja ha
  d'entendre la notícia.
- **5W explícites**: mai assumir que el lector sap el context.
- **Context aclarit**: "ahir" no val per a text LF → escriure la data. "El
  president" no val → "el president francès Emmanuel Macron".
- **Cites curtes amb atribució clara**: "Segons X, 'la frase exacta'."
- **Vocabulari neutre**: "va morir" > "va perdre la vida"; "va ser condemnat" >
  "va ser considerat culpable".
- **Acrònims desplegats** la primera vegada: "UE (Unió Europea)".

## Contraindicacions (NO FER)
- ❌ Titulars metafòrics: "La guerra del clima" → "Acord de l'ONU contra el
  canvi climàtic".
- ❌ Jocs de paraules al titular.
- ❌ Acrònims sense explicar.
- ❌ Referències a notícies anteriors sense context: "com ja vam informar..."
- ❌ Adjectius valoratius: "escandalós", "vergonyós", "històric".
- ❌ Frases en estil indirecte llarg ("va dir que hauria pogut ser pitjor...")
  → preferible cita directa breu.

## Modulació per MECR
- **A1-A2**: titular i lead de màxim 10-12 paraules. Cos de 3-4 frases curtes.
  No més d'una cita.
- **B1-B2**: lead complet amb totes 5W. Cos amb 2-3 paràgrafs. Una cita
  directa + una atribució indirecta.
- **C1**: estructura completa. Context històric si és pertinent. Múltiples
  fonts.

## Format de sortida
```markdown
# [Titular — una sola línia]

**[Lead en negreta: una o dues frases amb les 5W]**

[Cos: paràgrafs desenvolupant del més al menys important]

> [Cita directa si hi ha] — [atribució]
```

## Exemple
Veure `assets/exemple-noticia-A2.md` per a una notícia completa nivell A2.
