---
name: generar-illustracions
description: Instrument per generar marcadors d'il·lustracions al text adaptat. Rúbrica seqüencial gradada 5 passos x 6 nivells MECR (pre-A1-C1). Correccions MALL 2026-05-17 aplicades.
type: instrument
categoria_principal: mediacio
categories_secundaries: []
mecr_range: [pre-A1, A1, A2, B1, B2, C1]
agent_roles: [generator]
translanguaging: false
multimodal: true
skill_meta: generate-illustracions@corpusFJE/skills/mediacio/generate-illustracions
version: 3.0.0-bootstrap
---

# Generar il·lustracions — V3 Rúbrica Gradada

## Descripció

El complement d'il·lustracions insereix marcadors `[IMATGE: concepte curt]` al text adaptat per indicar al backend on col·locar una imatge. El backend resol cada marcador via Wikimedia, FLUX o un estil predefinit. Aquesta V3 presenta una rúbrica seqüencial amb **5 passos × 6 nivells MECR** (pre-A1→C1).

**Tipologia MALL**: Mediació (suport multimodal)
**Backend**: Wikimedia (realistes, llicència lliure) · FLUX (generat) · 7 presets d'estil (foto realista, il·lustració, diagrama, pictograma, mapa, infografia, còmic)

## Estructura canònica

Marcadors inline: `[IMATGE: concepte curt]` inserits al punt exacte del text on la imatge aporta ancoratge visual.

## Rúbrica seqüencial gradada

| Pas | Pre-A1 — Emergent | A1 — Inicial | A2 — Funcional | B1 — Estratègic | B2 — Acadèmic | C1 — Crític |
|---|---|---|---|---|---|---|
| **1. Nombre d'il·lustracions** | Màxim 4-5. Una per idea principal. Alta densitat justificada (text ≈ imatge). | 3-4 il·lustracions. Una per paràgraf o per concepte clau. | 2-3 il·lustracions. Als punts de màxim ancoratge conceptual. | 1-2 il·lustracions als conceptes abstractes o processos clau. | 1-2 il·lustracions estratègiques (diagrama, procés, dada visual clau). | 0-1 il·lustració. Reservada per a diagrames o infografies que condensin dades. |
| **2. Posició al text** | Imatge DAVANT de la paraula/frase que il·lustra. Anticipació visual. | Imatge immediatament DAVANT o AL COSTAT del concepte clau. | Imatge al costat del concepte que ancora, dins del paràgraf. | Imatge al concepte abstracte o al procés que beneficia d'ancoratge visual. | Imatge estratègica: diagrama d'un procés, taula de dades, mapa conceptual visual. | Imatge de suport a l'argument: infografia, gràfic, mapa. |
| **3. Especificitat del concepte** | Concepte molt concret i universal: "gat", "arbre", "pluja". Sense ambigüitat. | Concepte concret: "cèl·lula animal", "volcà en erupció". 1-3 paraules. | Concepte concret + context: "fotosíntesi a fulla verda". 2-4 paraules. | Concepte específic del contingut: "cadena tròfica marina", "cambra del parlament". | Concepte disciplinar: "diagrama de l'aparell respiratori", "mapa de la Revolució Francesa". | Concepte complex: "infografia comparativa de sistemes polítics", "gràfic evolució PIB". |
| **4. Estil visual** | Pictograma o il·lustració clara i simple. Sense elements distractors. | Il·lustració o foto realista. Molt clara, sense text a la imatge. | Foto realista o il·lustració educativa. Pot tenir etiquetes simples. | Diagrama o foto científica/geogràfica. Etiquetes disciplinars. | Diagrama, mapa, gràfic. Llegenda si cal. | Infografia, gràfic estadístic, mapa temàtic. |
| **5. Funció de la imatge** | Anticipació: l'alumne veu la imatge ABANS de llegir la paraula. Bastida d'accés. | Ancoratge: la imatge fixa el concepte a la memòria. Redueix càrrega cognitiva. | Ancoratge: la imatge dona concreció a un concepte potencialment abstracte. | Ancoratge / Ampliació: la imatge afegeix informació que el text no pot donar. | Ampliació / Síntesi: la imatge condensa dades o relacions que el text desenvolupa. | Síntesi / Argument: la imatge és evidència o estructura visual d'un argument. |

## Regles crítiques

**FER:** Format estricte `[IMATGE: concepte curt]` · Concepte curt i precís (1-4 paraules) · Imatge DAVANT del concepte que ancora (pre-A1/A1) · Màxim 3-4 per document (A2+).

**NO FER:** ❌ Il·lustracions decoratives sense funció cognitiva · ❌ Concepte vague ("[IMATGE: ciències]") · ❌ Imatge DESPRÉS del concepte a pre-A1/A1 · ❌ Més de 5 il·lustracions en cap text · ❌ Il·lustracions als textos de C1 tret que siguin infografies amb valor argumentatiu.

## Connexions MALL

- **Imatge com a bastida d'accés (pre-A1/A1)**: l'alumne nouvingut o emergent que no coneix la paraula "fotosíntesi" l'aprendrà si veu la imatge PRIMER. La seqüència imatge → paraula és la inversa de la lògica del text, però és la lògica de l'aprenentatge.
- **Imatge com a ampliació cognitiva (B1+)**: als nivells alts, la il·lustració no simplifica — complexifica. Un diagrama pot donar en un cop d'ull la informació que requereix 3 paràgrafs de text.

## Detecció

**Senyals docent**: vol que l'alumne tingui suport visual per als conceptes clau del text.
**Senyals alumne**: llegeix paraules sense imatge mental del concepte · vocabulari desconnectat del significat.
**Anti-senyals**: pictogrames com a sistema alternatiu de comunicació → `pictogrames` · esquema visual del contingut → `mapa-conceptual`.

## Heurístiques docent

**H1 — La imatge respon "com és?"**: una bona il·lustració respon la pregunta "com és X?" o "com funciona X?". Si la imatge no respon cap pregunta concreta, és decorativa.

**H2 — Pre-A1: imatge DAVANT, sempre**: l'ordre natural en el text posa la imatge al costat o darrere del concepte. Per a pre-A1, cal invertir-ho: la imatge anticipa la paraula. Aquesta inversió és pedagògica, no estètica.

## Fonts principals

- MALL (Model d'Aprenentatge de Llengües i Literacitat): suport multimodal, ancoratge visual ZDP.
- Mayer (2009): *Multimedia Learning* — principi de contigüitat imatge-text.
- Decret 175/2022 (currículum Catalunya): competència digital i multimodalitat.
