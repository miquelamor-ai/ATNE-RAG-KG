---
name: generar-resum-graduat
description: Instrument per generar un resum graduat (bastida de producció: marc parcial amb forats). Rúbrica seqüencial gradada 5 passos x 6 nivells MECR (pre-A1-C1). Correccions MALL 2026-05-17 aplicades.
type: instrument
categoria_principal: mediacio
categories_secundaries: []
mecr_range: [pre-A1, A1, A2, B1, B2, C1]
agent_roles: [generator]
translanguaging: false
multimodal: false
skill_meta: generate-resum-graduat@corpusFJE/skills/mediacio/generate-resum-graduat
version: 3.0.0-bootstrap
---

# Generar resum graduat — V3 Rúbrica Gradada

## Descripció

El resum graduat és una bastida cognitiva per produir un resum pas a pas: un marc parcial amb forats calibrats al MECR. La gradació no és de complexitat del text, sinó de la mida del forat (A1 = forats petits amb opcions; C1 = producció lliure amb criteris). Aquesta V3 presenta una rúbrica seqüencial amb **5 passos × 6 nivells MECR** (pre-A1→C1).

**Tipologia MALL**: Mediació (bastida cognitiva de producció de resum)
**Distinció MALL**: Recapitular (pas previ oral/visual, pre-A1/A1) ≠ Resumir (producció textual, A2+).

## Estructura canònica

Secció `## Resum` + marc parcial amb forats `___` calibrats al MECR del text adaptat (narratiu: tema/personatge/acció/desenllaç · expositiu: tema/punts clau/conclusió)

## Rúbrica seqüencial gradada

| Pas | Pre-A1 — Emergent | A1 — Inicial | A2 — Funcional | B1 — Estratègic | B2 — Acadèmic | C1 — Crític |
|---|---|---|---|---|---|---|
| **1. Tipus de marc** | Activitat oral: "De qui parla? Qué fa? Com acaba?" El docent escriu el que l'alumne diu. Sense escriptura autònoma. | Frase marc amb 1-2 buits + opcions a triar. "El text parla de [tria: opció A / opció B / opció C]." | Marc de 2-3 frases amb 3-4 buits sense opcions. L'alumne omple amb paraules pròpies. | Marc de 3 parts (tema / punts clau / conclusió) amb espai d'1-2 frases per part. | Criteris de qualitat del resum (4-5 ítems). L'alumne escriu el resum complet. | Rúbrica metacognitiva + reflexió sobre les tries. Resum lliure + justificació. |
| **2. Mida del forat** | ❌ Cap forat — activitat oral. | Buit de 1-3 paraules. Una resposta clarament correcta. Opcions plausibles però incorrectes. | Buit de 1 frase (5-10 paraules). Sense opcions: l'alumne reformula amb les seves paraules. | Buit de 2-3 frases. Paraules pròpies i reorganització de la informació. | Criteri obert: "Has seleccionat les idees principals (no els exemples)?" | Criteri metacognitiu: "Explica per qué has triat incloure aquesta idea i no aquella altra." |
| **3. Estructura del marc** | Preguntes orals adaptades al tipus de text (narratiu/expositiu). | Marc adaptat al tipus de text: narratiu (personatge/acció/desenllaç) · expositiu (tema/punt clau/final). | Marc de 2-3 frases adaptat al tipus de text. Connectors donats entre les frases marc. | Marc de 3 seccions amb etiquetes: Tema / Punts clau / Conclusió. | Criteris que cobreixen les macroregles del resum: selecció, generalització, construcció. | Reflexió que va més enllà del resum: "Qué has decidit NO incloure i per qué?" |
| **4. Recapitular vs. resumir** | Recapitular: reordenar informació oral/visual sense producció textual autònoma. | Recapitular assistit: triar la resposta correcta és una forma de recapitular. | Resumir amb bastida: la primera forma de producció de resum escrit. | Resumir amb marc mínim: el marc es va retirant progressivament. | Resumir amb criteris: l'alumne usa criteris interns per produir i avaluar el resum. | Resumir i reflexionar: el resum és el punt de partida d'una reflexió metacognitiva. |
| **5. NO donar el resum** | El docent escriu el dictat de l'alumne — no dona el resum ell. | Les opcions a triar son TOTES candidates plausibles. Cap opció obviament falsa. | El marc indica COM escriure, no QUÈ escriure. L'alumne tria el contingut. | El marc proposa l'estructura, no el contingut. L'alumne construeix les idees. | Els criteris guien, no substitueixen la producció. L'alumne escriu el resum sencer. | La rúbrica metacognitiva exigeix reflexió pròpia, no es pot copiar de cap font. |

## Regles crítiques

**FER:** Marc adaptat al tipus de text del text font (narratiu vs. expositiu) · Forats completables en 1-3 paraules a A1 · No donar el resum fet · Pre-A1 = activitat oral (el docent escriu el dictat) · Secció comença amb `## Resum`.

**NO FER:** ❌ Forats que l'alumne pot omplir copiant literalment frases del text · ❌ Opcions a triar on una és obviament falsa · ❌ Marc genèric que no s'adapta al tipus de text · ❌ Donar el resum model com a exemple (l'alumne el copiaria).

## Connexions MALL

- **Recapitular com a pas previ essencial**: el MALL distingeix recapitular (oral/visual, selecció d'informació) de resumir (producció textual). Saltar-se el recapitular (pre-A1/A1) porta a un resum per copiar sense comprensió real.
- **Mida del forat com a ZDP operativa**: un forat massa gran (per sobre del MECR) genera frustració; un forat massa petit (per sota) no desenvolupa. El forat ben calibrat manté l'alumne a la seva ZDP i l'avança cap a la producció autònoma.

## Detecció

**Senyals docent**: vol que l'alumne produeixi un resum però necessita bastida · activitat de comprensió lectora amb producció.
**Senyals alumne**: no sap per on començar el resum · copia frases literals del text · fa una llista en lloc d'un text cohesionat.
**Anti-senyals**: resum autònom sense bastida → `write-resum` (gènere) · plantilla del gènere → `plantilles-genere` · preguntes de comprensió → `preguntes_comprensio`.

## Heurístiques docent

**H1 — Les opcions de A1 son totes plausibles**: si una opció és obviament falsa ("El text parla de: a) volcans b) moda c) maquinaria petroliera"), l'alumne endevina sense comprendre. Les tres opcions han de ser possibles per al text — però una sola és la correcta.

**H2 — El marc narratiu vs. expositiu**: per a contes i biografies usar tema/personatge/acció/desenllaç. Per a textos expositius (manuals, enciclopèdics) usar tema/punts clau/conclusió. El marc equivocat genera un resum que no té sentit per al tipus de text.

## Fonts principals

- MALL (Model d'Aprenentatge de Llengües i Literacitat): recapitular vs. resumir, bastida de producció.
- Kintsch & van Dijk (1978): macroregles del resum (supressió, generalització, construcció).
- Decret 175/2022 (currículum Catalunya): competència lectora i producció de textos.
