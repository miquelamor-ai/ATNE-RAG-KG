---
modul: M3
titol: "Generar mapa conceptual"
tipus: instrument
categoria_principal: mediacio
categories_secundaries: []
descripcio: "Instrument per generar un organitzador visual adaptat al MECR. Distinció fonamental: Esquema visual (pre-A1/A1, seqüència/parts, Llegir per orientar-se) vs. Mapa conceptual (A2+, Novak, Llegir per comprendre, jerarquia etiquetada) vs. Mapa de contrast (C1, 2 columnes). Format markdown jerarquic, mai ASCII-art. Branques = noms de categoria (Causes, Consequencies, Tipus de), mai generics. Instrument separat del generate-mapa-mental (Buzan, B1+, radial divergent). Rubrica gradada 5 passos x 6 nivells MECR (pre-A1->C1)."
mecr_range: [pre_A1, A1, A2, B1, B2, C1]
agent_roles: [generator]
complement_key: mapa_conceptual
translanguaging: false
multimodal: false
moduls_relacionats: [M2, M3]
variables_configurables:
  fase_lectora: [logografica, alfabetica_emergent, alfabetica_fluida]
skill_meta: generate-mapa-conceptual@corpusFJE/skills/mediacio/generate-mapa-conceptual
review_status: pilot-fusio-8
version: 4.0.0-canonic
generat_at: 2026-05-26
actualitzat_at: 2026-05-26
notebooklm_review:
  data: 2026-05-26
  veredicte: si-amb-correccions-menors
  aplicades_des_d_inici: [patro-canonic-pilots-fase-a, aclariment-us-lectura-vs-produccio-C1, variabilitat-cardinal-passos-D3, modulacio-per-perfil-D1]
  aplicades_post_review: [b10-mapa-c2-branques-a1-validation-hint-2-3, b10-mapa-c3-h6-densitat-nodes]
  comentari_key: "C1-multimodal-false-rebutjat-imatge-concepte-no-embedded; C4-sub-elements-a1-rebutjat-parts-son-branques"
---

# Generar mapa conceptual

## Descripció

El mapa conceptual és un **organitzador visual** que externalitza les relacions entre conceptes del text adaptat. El MALL distingeix tres eines progressives dins d'aquest instrument: l'**esquema visual** (funció executiva, pre-A1/A1: ordena seqüències o parts d'un tot), el **mapa conceptual jeràrquic** (funció epistèmica, A2+: reconstrueix el coneixement en categories i relacions lògiques) i el **mapa de contrast** (funció crítica, C1: compara fonts o ideologies). La tria de l'eina depèn del MECR i de l'objectiu pedagògic.

**Tipologia MALL**: Mediació (organitzador visual cognitiu).
**HCL principals**: Recapitular/Organitzar (pre-A1/A1) · Categoritzar/Relacionar (A2-B1) · Contrastar/Analitzar (B2-C1).
**Principi rector**: La branca ha de dir la **relació** ("Causes", "Conseqüències", "Tipus de", "Processos"), no el contingut. Si la branca s'anomena "Informació" o "Coses", no és un mapa conceptual — és una llista disfressada.
**Format obligatori**: Markdown jeràrquic (exportable a MindMeister/Canva/XMind). **Cap ASCII-art** (caixes │ ├ └ → fletxes).

**Distinció fonamental — 3 eines dins un instrument:**
- **Esquema visual** (pre-A1/A1): "Llegir per orientar-se". Seqüències temporals (antes/durant/après) o parts d'un tot (cap, cos, cua). El pas d'un node és immediat: imatge → paraula. No hi ha jerarquia lògica: és una cadena o un diagrama d'elements.
- **Mapa conceptual** (A2-B2, Novak): "Llegir per comprendre". Jerarquia etiquetada: concepte central → categories → detalls. Les branques reflecteixen relacions lògiques (causes, efectes, tipus, processos). El contingut prové del text adaptat.
- **Mapa de contrast** (C1): "Llegir per avaluar". Dues columnes o dues branques en contraposició. El contingut compara dues fonts, dues ideologies o dos marcs interpretatius.

**Distinció crítica amb `generate-mapa-mental` (instrument separat):**
- `mapa_conceptual` (Novak): "Llegir per comprendre" — contingut **dintre del text** adaptat; estructura jeràrquica; relacions etiquetades; A2-C1.
- `mapa_mental` (Buzan, B1+): "Llegir per connectar" — contingut **més lluny del text**; radial i divergent; lliure; preguntes generadores; per a alumnat amb AACC o exploració creativa.
Quan l'objectiu és comprendre el text → `mapa_conceptual`. Quan l'objectiu és expandir i connectar → `mapa_mental`.

**Mapa com a bastida de composició**: l'alumne que fa el mapa conceptual ABANS d'escriure té ja l'estructura del text. El mapa és la planificació cognitiva que precedeix la producció textual. Per a TILC, el mapa conceptual és alhora instrument de comprensió i esquelet del text expositiu.

**Pre-A1 SÍ (D6)**: l'esquema visual a pre-A1 no demana abstracció ni relacions lògiques. "Ordena les parts" o "Quins moments té?" son operacions cognitives assolibles des de la fase logogràfica, amb imatges com a suport.

**Connexions MALL transversals:**
- *Esquema vs. mapa com a distinció cognitiva*: el pas d'esquema (ordena) a mapa (categoritza i relaciona) no és cosmètic — és cognitiu. Introduir el mapa conceptual a A2 és introduir el pensament categorial: la capacitat de nomenar categories i les relacions entre elles.
- *Noms de branca com a comprensió*: si l'alumne no pot nomenar la branca ("Causes", "Efectes"), no ha comprès la relació. El nom de branca és la prova de comprensió, no el contingut de la branca.
- *Mapa com a metacognició*: construir el mapa DESPRÉS de llegir és diferent que llegir el mapa construït per un altre. La construcció activa (l'alumne organitza) desenvolupa comprensió profunda; la lectura passiva d'un mapa donat desenvolupa reconeixement.

**Aclariment d'ús — què descriu aquesta rúbrica.**
Aquesta rúbrica descriu el **mapa conceptual / esquema visual que es genera com a organitzador del text adaptat** (COMPRENSIÓ ESTRUCTURADA). **No descriu la producció creativa de l'alumne**: el mapa es genera a partir del text adaptat; l'alumne el llegeix, l'usa com a bastida de comprensió i en pot fer un de propi com a activitat posterior.
**Sub-granularitat dins de pre-A1**: `fase_lectora: logografica` → esquema de 2 imatges (imatge → paraula); `fase_lectora: alfabetica_emergent` → esquema de 2-3 nodes amb paraula curta.

## Detecció

**Senyals docent** (quan activar el complement):
- Ha activat "Mapa conceptual" al Pas 2.
- El text té una estructura jeràrquica clara (categories, causes, efectes, seqüències).
- L'alumne no identifica la idea principal o confon categories amb exemples.
- Cal una bastida de comprensió visual per al text expositiu o informatiu.

**Senyals alumne** (que indica que necessita el suport):
- No identifica la idea principal del text.
- Confon categories amb exemples ("Causes: temperatura" vs. "Causes: l'augment de temperatura provoca...").
- No veu la relació entre parts del text.
- Llegeix el text però no pot resumir les idees en categories.

**Context favorable**:
- Text expositiu o informatiu amb estructura de categories (TILC ciències, socials, tecnologia).
- Preparació per escriure un text expositiu: el mapa és el GPS de composició.
- Repàs de final d'unitat: el mapa organitza el coneixement adquirit.
- Alumnat amb TDAH que necessita l'estructura visual per gestionar la càrrega cognitiva.

**Anti-senyals** (quan NO activar):
- Text narratiu sense estructura categorial clara → el mapa és força.
- L'objectiu és suport lexical → `glossari`.
- L'objectiu és guia de passos de producció → `bastides_produccio`.
- L'objectiu és expandir i connectar más del text → `mapa_mental` (instrument separat).
- L'objectiu és ordenar vocabulari visualment → `pictogrames`.

## Modulació per nivell

| Pas | Dimensió | Pre-A1 Emergent | A1 Inicial | A2 Funcional | B1 Estratègic | B2 Acadèmic | C1 Crític |
|---|---|---|---|---|---|---|---|
| **1. Tipus d'eina** | Funció cognitiva | Esquema visual: 2-3 nodes. Imatge → paraula o seqüència temporal (antes/durant/après). | Esquema visual: 3-4 nodes. Parts d'un tot o qualitats simples d'un element concret. | Mapa conceptual: 2 nivells jeràrquics. Primera introducció guiada de branques etiquetades. | Mapa conceptual: 3 nivells. Concepte → categories disciplinars → detalls inferts del text. | Mapa conceptual: 4 nivells màxim. Superestructura del gènere amb lèxic CALP. | Mapa de contrast: 2 columnes o branques en contraposició. Comparació de fonts o ideologies. |
| **2. Concepte central** | Nucli del mapa | Nom d'un personatge o objecte familiar del text. 1-2 paraules. | 1 terme nuclear concret del text adaptat. En negreta. | 1 terme nuclear precís del text adaptat. En negreta. Correspon a la idea central del text. | 1 terme que organitza tot el coneixement del text. Terme disciplinar. | 1 terme nuclear CALP. Pot ser un procés, un fenomen o un concepte abstracte. | 2 termes en contrast o 1 concepte complex amb múltiples dimensions o perspectives. |
| **3. Branques principals** | Noms de categoria | 1-2 elements: parts o qualitats d'un tot. Noms simples i concrets (cap, pit, cua). | 2-3 branques concretes. Noms simples. Pot ser seqüència temporal (1r, 2n, 3r). | 3-4 branques amb noms de categoria clars (Causes / Tipus / Efectes / Processos). Mai genèrics. | 3-5 branques amb noms de categoria disciplinars. Relació lògica explícita (no "Informació"). | 4-6 branques CALP. Les categories reflecteixen l'estructura del gènere treballat. | 2 columnes de contrast o 4-6 branques amb relació de tensió, contrast o complementarietat. |
| **4. Sub-elements** | Detalls de les branques | Cap sub-element: l'esquema és pla (massa nivells per a pre-A1). | Cap sub-element: l'esquema és pla (màxim 1 nivell). | 2-3 sub-elements per branca. Termes curts, no frases llargues. Del text adaptat. | 3-4 sub-elements per branca. Inferts del text, no copiats literalment. | Sub-elements amb matisos. Pot incloure relacions transversals entre branques. | Sub-elements de contrast, evidències o cites de fonts. Pot incloure tensions entre branques. |
| **5. Format de sortida** | Estructura markdown | `## Esquema visual` + llista plana sense sangria. 2-3 ítems màxim. | `## Esquema visual` + llista amb sangria màxima 1 nivell. Cap ASCII-art. | `## Mapa conceptual` + 2 nivells de sangria. Branques en negreta. Cap ASCII-art. | `## Mapa conceptual` + 3 nivells de sangria. Branques en negreta. Cap ASCII-art. | `## Mapa conceptual` + 4 nivells màxim. Branques CALP en negreta. Cap ASCII-art. | `## Mapa de contrast` + 2 columnes (taula markdown) o mapa amb branques de contrast. |

## Metadades de cel·la (per a `build_skills.py`)

**Tipus de descriptor:**
- `binary` — "compleix / no compleix".
- `qualitative` — requereix judici huma o LLM-jutge.
- `countable` — llindar quantitatiu verificable mecanicament.
- `structural` — requereix analisi sintatica o discursiva.
- `metacognitive` — descriptor de proces en primera persona.

| Pas / Dimensió | Tipus | requires_source_text | validation_hint |
|---|---|---|---|
| 1 Tipus d'eina | `binary` + `qualitative` | no | binary: pre-A1/A1 = esquema visual (titol `## Esquema visual`); A2-B2 = mapa conceptual (`## Mapa conceptual`); C1 = mapa de contrast (`## Mapa de contrast`); qualitative: LLM-jutge sobre si l'eina correspon al MECR declarat |
| 2 Concepte central | `qualitative` | **si** | LLM-jutge: el concepte central és un terme nuclear del text adaptat (positiu) o un terme genèric no present al text (negatiu); cross_source: verificar que el concepte central apareix i és central al text font |
| 3 Branques principals | `qualitative` + `binary` | **si** | qualitative: LLM-jutge sobre si els noms de branca son noms de categoria relacional (Causes, Efectes, Tipus de) — positiu — o genèrics ("Informació", "Coses") — negatiu — error crític; binary: nombre de branques dins del rang per MECR (pre-A1: 1-2; A1: 2-3; A2: 3-4; B1: 3-5; B2: 4-6; C1: 2 o 4-6); cross_source: branques corresponents al contingut del text font |
| 4 Sub-elements | `binary` + `structural` | no | binary: pre-A1/A1 = absencia de sub-elements (esquema pla); A2+ = presencia de sub-elements; structural: detectar ASCII-art (caràcters │ ├ └ → o caixes de text) = error crític en qualsevol nivell |
| 5 Format de sortida | `structural` | no | structural: el titol de secció correspon al tipus d'eina (`## Esquema visual` vs `## Mapa conceptual` vs `## Mapa de contrast`); nivells de sangria dins del rang per MECR; absencia d'ASCII-art |

**Notes:**
- Error crític principal: noms de branca genèrics ("Informació", "Coses", "Dades"). Detectar per LLM-jutge + regex (lista negra de noms genèrics).
- Error secundari: ASCII-art (│ ├ └ → [ ]). Detectar per regex. Error en tots els nivells.
- Diferència `mapa_conceptual` vs `mapa_mental`: verificar que l'instrument generat NO té estructura radial lliure (seria mapa mental, instrument diferent). El mapa conceptual té jerarquia clara: un concepte central → branques → sub-elements.
- C1 mapa de contrast: verificar presencia de 2 columnes o branques en tensió explícita. No és simplement 2 branques qualsevol.

## Heurístiques docent

**H1 — El nom de la branca és la prova de comprensió.**
Llegeixo les branques principals del mapa i em pregunto: "Diuen la relació o diuen el contingut?" "Causes de la contaminació" i "Efectes sobre els ecosistemes" diuen la relació. "Informació sobre la contaminació" no diu res. Si no puc nomenar la branca amb un nom de categoria, l'alumne (ni el mapa) ha entès l'estructura del text.

**H2 — Pre-A1/A1 = seqüència, no jerarquia.**
Per als alumnes emergents, la pregunta no és "com es relacionen?" sinó "en quin ordre va?" o "quines parts té?". L'esquema visual treballa la seqüència temporal o les parts d'un tot: 1r passa X, 2n passa Y, 3r passa Z. Introduir jerarquia lògica (causes → efectes) a pre-A1 és una sobrecàrrega cognitiva innecessària.

**H3 — Cap ASCII-art, mai.**
L'ASCII-art (caixes amb │ ├ └ i fletxes) és visualment impactant però no és accessible (no es pot exportar, no té semàntica, trenca la cadena de producció). El markdown jeràrquic (# → - → espais d'indentació) és senzill, exportable a qualsevol eina de mapes mentals i coherent amb el flux de l'eina.

**H4 — Mapa conceptual vs. mapa mental: la pregunta del contingut.**
Em pregunto: "L'alumne ha de comprendre el text o ha d'expandir-se més lluny del text?" Si la resposta és "comprendre el text" → mapa conceptual (contingut del text). Si la resposta és "connectar amb el que sap i generar preguntes noves" → mapa mental (instrument separat, B1+).

**H5 — Mapa com a GPS de composició (TILC).**
Quan l'objectiu és que l'alumne escrigui un text expositiu, el mapa conceptual és la planificació cognitiva: Pas 1 fer el mapa → Pas 2 escriure les branques com a paràgrafs. L'alumne que fa el mapa primer escriu un text més coherent i més complet que l'alumne que escriu directament.

**H6 — Densitat de nodes: menys és més.**
Un mapa amb 15 nodes no és millor que un amb 8. La càrrega cognitiva òptima per nivell: pre-A1 ≤ 3 nodes totals; A1 ≤ 5; A2 ≤ 8; B1 ≤ 12; B2-C1 ≤ 15. Si el mapa supera el llindar, cal eliminar sub-elements o fusionar branques redundants. La densitat excessiva és l'error de qualitat més freqüent dels LLMs amb textos rics en informació.

## Fonts principals

- MALL (Model d'Aprenentatge de Llengues i Literacitat): organitzadors visuals, "llegir per comprendre" vs. "llegir per connectar", GPS de composició.
- Novak, J.D. & Gowin, D.B. (1984): *Learning How to Learn* — mapa conceptual com a eina epistèmica i metacognitiva.
- Ausubel, D.P. (1968): *Educational Psychology: A Cognitive View* — aprenentatge significatiu; ancoratge conceptual.
- Decret 175/2022 (curriculum Catalunya): competencia digital, tractament de la informació i pensament crític.
