---
name: generar-preguntes-comprensio
description: Instrument per generar preguntes de comprensió lectora. Model MALL 3 moments x 3 plànols cognitius. Inclou Pas d'acarament de llengües L1-L2 per a nouvinguts. Correccions MALL 2026-05-17 aplicades.
type: instrument
categoria_principal: mediacio
categories_secundaries: []
mecr_range: [pre-A1, A1, A2, B1, B2, C1]
agent_roles: [adapter, generator]
translanguaging: true
multimodal: true
skill_meta: generate-preguntes-comprensio@corpusFJE/skills/complements/generate-preguntes-comprensio
version: 2.0.0-bootstrap
---

# Generar preguntes de comprensió lectora — V2 Descriptiu

## Descripció

Les preguntes de comprensió lectora segueixen el **model MALL de 3 moments × 3 plànols cognitius**: abans de llegir (activació), durant la lectura (monitorització) i després de llegir (processament). No és un examen final: és un **guió que acompanya l'alumnat durant la lectura**.

**Tipologia MALL**: Mediació cognitiva (comprensió lectora)
**Principi rector**: "Menys és més" (MALL) — 6-10 preguntes totals, mai més.
**Plànols cognitius**: Literal → Inferencial → Crític/Creatiu

## Estructura canònica — 3 moments

| Moment | Propòsit | Nombre orientatiu |
|---|---|---|
| **Abans de llegir** | Activar coneixements previs, predicció, propòsit de lectura | 2-3 |
| **Durant la lectura** | Aturades estratègiques: dubte lèxic, hipòtesi, resum parcial | 1-2 |
| **Després de llegir** | Interrogar el text als 3 plànols: literal → inferencial → crític | 3-5 |

## Modulació per nivell MECR

### Pre-A1 — Emergent

**Cap escriptura autònoma**. Totes les "preguntes" es formulen com a consignes d'acció: assenyalar imatge, dibuixar, dramatitzar, dictat a l'adult. El plànol literal es treballa via adult ("mostra'm on és..."). El plànol crític s'introdueix oralment ("Què hauries fet tu?"). Format: `- Assenyala la imatge on es veu [concepte].`

### A1 — Inicial

Format permès: Vertader/Fals (paraula clau senzilla, no frase complexa), omplir buits amb llista tancada o suport visual. Plànol dominant: **literal**. El "Per què...?" s'accepta en forma oral o guiada per l'adult. Frases de la pregunta de màxim 10 paraules.

### A2 — Funcional

Format permès: ordenar seqüències, relacionar amb fletxes, elecció múltiple sobre la idea principal. Plànol dominant: **literal amb inici d'inferencial**. Causa literal al text ("Per què...? La resposta és al text"). Frases de la pregunta de màxim 12 paraules.

### B1 — Estratègic

Format permès: resposta breu (2-4 frases), hipòtesis, causa-efecte. Plànol dominant: **inferencial**. El lector ha de deduir relacions que no estan explícites al text. Frases de la pregunta de màxim 15 paraules. Pas d'**acarament de llengües** recomanat per a nouvinguts.

### B2 — Acadèmic

Format permès: argumentació oberta, resum d'idees abstractes, anàlisi de la superestructura del gènere. Plànol dominant: **CALP/epistèmic**. El lector justifica amb referència al text i a models teòrics o exemples externs. Pas d'**acarament de llengües** recomanat.

### C1 — Crític

Format permès: contrast de fonts, anàlisi d'intencionalitat, argumentació fonamentada. Plànol dominant: **crític**. Judici sobre la fiabilitat i el punt de vista de l'autor. El lector avalua i qüestiona, no només respon.

## Pas d'acarament de llengües (L1 ↔ L2) — correcció MALL C

Per a alumnat nouvingut (A1-B2), s'afegeix al final del "Després de llegir" una pregunta d'acarament:

- A1: "Hi ha alguna paraula que sembli a una paraula de la teva llengua? Quina?"
- A2: "Com es diu [terme clau] en la teva llengua? La forma és semblant o diferent?"
- B1: "En la teva llengua, el text s'escriuria de la mateixa manera? Hi hauria diferències?"
- B2: "Quines diferències trobes entre com s'argumenta en català i en la teva llengua?"

## Modulació per modalitat del text

- **Text LITERARI** ("Porta Oberta"): preguntes afectives ("Com et sentiria?"), creatives ("Què hauria passat si...?"), interpretació de metàfores i símbols. Objectiu: gaudi estètic i construcció de sentit personal.
- **Text INFORMATIU** ("Porta Tancada"): monitorització metacognitiva, precisió conceptual, jerarquització, valoració de la fiabilitat de les dades.

## Regles crítiques

**FER:**
- Comença sempre amb `## Preguntes de comprensió`.
- Sub-seccions: `### Abans de llegir`, `### Durant la lectura`, `### Després de llegir`.
- Pre-A1: substitueix preguntes escrites per consignes d'acció.
- Formats visuals integrats a la pregunta: `- Omple els buits: El ______ serveix per ______.`

**NO FER:**
- ❌ Etiquetes visibles de nivell ([Literal], [Inferencial]...) — l'alumne no les veu.
- ❌ Numeració de les preguntes — usar `- `.
- ❌ V/F a pre-A1.
- ❌ Preguntes "copia i enganxa" (resposta copiable sense processament).
- ❌ Més de 10 preguntes en total.

## Connexions MALL

- **Translanguaging/TOLC**: el Pas d'acarament de llengües és la implementació directa del TOLC (Transfer of Literacy and Cognition) de Cummins.
- **Multimodalitat**: a pre-A1 i A1, les consignes d'acció i les imatges substitueixen el text escrit.
- **3 plànols cognitius**: tots 3 es treballen des d'infantil, però sempre via adult a pre-A1. El plànol crític s'introdueix oralment ja al conte de I5 ("Què hauries fet tu?").

## Detecció

> ⚠️ ESBORRANY — requereix validació pedagògica humana (docents FJE)

**Senyals docent** (quan activar preguntes de comprensió):
- El docent vol assegurar la comprensió del text adaptat.
- El text és complex per al nivell de l'alumnat.
- L'alumnat ha de demostrar comprensió per a una avaluació o activitat posterior.

**Anti-senyals** (quan NO activar):
- El text és molt curt i la comprensió és òbvia.
- El docent ha preparat les seves pròpies preguntes.

## Heurístiques docent

> ⚠️ ESBORRANY — requereix captura via entrevistes a docents FJE

- H1: El docent sol prioritzar "Abans de llegir" per a alumnat amb poc coneixement previ del tema.
- H2: Per a textos literaris, el docent afavoreix les preguntes creatives i afectives per sobre de les literals.

## Autoavaluació (descriptors en primera persona)

- *Pre-A1*: "He assenyalat les imatges que m'ha demanat el mestre."
- *A1*: "He respost si és vertader o fals. He omplert els buits."
- *A2*: "He ordenat les idees del text. He trobat la idea principal."
- *B1*: "He deduït informació que no estava explícita al text."
- *B2*: "He argumentat les meves respostes amb referències al text."
- *C1*: "He analitzat la intencionalitat de l'autor i he qüestionat les seves afirmacions."

## Fonts principals

- MALL (Model d'Aprenentatge de Llengües i Literacitat): 3 moments × 3 plànols, "menys és més".
- Cummins (2000): CALP, BICS, Transfer of Literacy and Cognition (TOLC).
- Solé (1992): estratègies de comprensió lectora.
- Decret 175/2022 (currículum Catalunya): competència lectora i plurilingüisme.
