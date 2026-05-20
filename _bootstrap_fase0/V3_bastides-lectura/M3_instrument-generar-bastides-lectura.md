---
name: generar-bastides-lectura
description: Instrument per generar bastides de lectura (3 moments × 3 plànols). Rúbrica seqüencial gradada 3 passos x 6 nivells MECR (pre-A1-C1). Correccions MALL 2026-05-17 aplicades.
type: instrument
categoria_principal: mediacio
categories_secundaries: []
mecr_range: [pre-A1, A1, A2, B1, B2, C1]
agent_roles: [generator]
translanguaging: false
multimodal: false
skill_meta: generate-bastides-lectura@corpusFJE/skills/mediacio/generate-bastides-lectura
version: 3.0.0-bootstrap
---

# Generar bastides de lectura — V3 Rúbrica Gradada

## Descripció

Les bastides de lectura guien l'alumne als tres moments del procés lector (Abans / Durant / Després) i als tres plànols de comprensió (literal / inferencial / crític). Sempre actives quan el complement "bastides" és activat. Aquesta V3 presenta una rúbrica seqüencial amb **3 passos × 6 nivells MECR** (pre-A1→C1).

**Tipologia MALL**: Mediació (bastida cognitiva de lectura)
**Estratègies MALL activades**: Formular hipòtesis (Abans) · Visualitzar (Durant) · Fer inferències (Durant/Després) · Recapitular → Resumir (Després)

## Estructura canònica

1. Secció `## Suports de lectura` · 2. Subsecció Abans · 3. Subsecció Durant · 4. Subsecció Després

## Rúbrica seqüencial gradada

| Pas | Pre-A1 — Emergent | A1 — Inicial | A2 — Funcional | B1 — Estratègic | B2 — Acadèmic | C1 — Crític |
|---|---|---|---|---|---|---|
| **1. Moment Abans** | Assenyalar imatges. Predicció oral guiada per l'adult. Zero escriptura. | 1 pregunta d'activació de previs + predicció pel títol. | 2 preguntes + propòsit de lectura explícit ("Llegeix per saber…"). | Activació + predicció + formulació d'hipòtesi pròpia per escrit. | + identificació del gènere i l'autor, posicionament inicial. | + l'alumne formula les seves pròpies preguntes de lectura abans de llegir. |
| **2. Moment Durant** | L'adult llegeix en veu alta. L'alumne assenyala imatges, dramatitza o dibuixa el que entén. | Subratlla 1 mot clau per paràgraf. Cap anotació marginal. | Marca ✓ (entès) / ? (dubte) / ! (important) al marge. Sense notes extenses. | Notes marginals breus + hipòtesi en curs: "Fins aquí, crec que el text dirà que…". | + detecció del posicionament de l'autor: "On es posiciona l'autor?". | + contrast actiu amb coneixements previs: "Aquí l'autor diu X però jo sabia Y". |
| **3. Moment Després** | Dibuixar el que ha après. Dictat oral a l'adult. Ordenació d'imatges. | Frase marc literal: "El text parla de ___". 1 sol buit. | Resum 2-3 frases + 1 pregunta inferencial ("Per què creus que…?"). | Resum (literal) + inferència ("Quin era l'objectiu de l'autor?") + valoració. | + avaluació de fiabilitat: "Fins a quin punt és objectiu l'autor? Per qué?". | + autoregulació: "He entès tot el que calia? Quines preguntes m'han quedat obertes?". |

## Regles crítiques

**FER:** Màxim 3 ítems per moment · Propòsit de lectura específic del text (no genèric) · Cobrir els 3 plànols (literal/inferencial/crític) al moment Després · Pre-A1 = ZERO escriptura autònoma.

**NO FER:** ❌ Repetir les mateixes preguntes que el complement `preguntes_comprensio` · ❌ Més de 3 ítems per moment (menys és més) · ❌ Frase marc amb més d'un buit a A1 · ❌ Preguntes que l'alumne no pot respondre sols amb el text.

## Connexions MALL

- **3 moments com a estructura metacognitiva**: avant/durant/après és la seqüència que fa visible el procés lector. L'alumne que interioritza els 3 moments es converteix en lector estratègic.
- **Plànol crític com a meta**: la bastida de lectura comença en el literal (A1) i avança cap a la valoració i l'autoregulació (C1). No es tracta de passar les preguntes, sinó de construir el lector que es pregunta sol.

## Detecció

**Senyals docent**: el docent activa el complement "bastides" al Pas 2 · vol estructurar el procés lector de l'alumne.
**Senyals alumne**: llegeix sense aturar-se · no sap distingir idea principal de detall · no fa prediccions.
**Anti-senyals**: preguntes de comprensió detallada → `preguntes_comprensio` · base d'orientació de producció → `bastides-produccio`.

## Heurístiques docent

**H1 — El propòsit de lectura és la clau**: "Llegeix per saber X" ha de ser específic i concret. Si el propòsit és genèric ("llegeix el text"), la bastida perd la seva funció orientadora.

**H2 — El Moment Després revela la comprensió**: si l'alumne no pot completar la frase marc del Moment Després, no ha entès el text. La bastida revela el problema ABANS de la pregunta de comprensió.

## Fonts principals

- MALL (Model d'Aprenentatge de Llengües i Literacitat): 3 moments × 3 plànols, estratègies lectives.
- Palincsar & Brown (1984): lectura recíproca — les 4 estratègies (predicció, aclariment, interrogació, resum).
- Decret 175/2022 (currículum Catalunya): competència lectora i comprensió crítica.
