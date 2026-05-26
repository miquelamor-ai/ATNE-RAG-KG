---
modul: M3
titol: "Generar resum graduat"
tipus: instrument
categoria_principal: mediacio
categories_secundaries: []
descripcio: "Instrument per generar un resum graduat: marc parcial amb forats calibrats al MECR. Principi MALL: forat calibrat a la ZDP (ni massa gran ni massa petit). Distincio essencial: Recapitular (pre-A1/A1, oral, sense escriptura autonoma) vs. Resumir (A2+, produccio textual). Marc adaptat al tipus de text (narratiu: tema/personatge/accio/desenllaç; expositiu: tema/punts clau/conclusio). NO donar el resum fet. Rubrica gradada 5 passos x 6 nivells MECR (pre-A1->C1)."
mecr_range: [pre_A1, A1, A2, B1, B2, C1]
agent_roles: [generator]
complement_key: resum_graduat
translanguaging: false
multimodal: false
moduls_relacionats: [M2, M3]
variables_configurables:
  fase_lectora: [logografica, alfabetica_emergent, alfabetica_fluida]
skill_meta: generate-resum-graduat@corpusFJE/skills/mediacio/generate-resum-graduat
review_status: pilot-fusio-8
version: 4.0.0-canonic
generat_at: 2026-05-26
actualitzat_at: 2026-05-26
notebooklm_review:
  data: 2026-05-26
  veredicte: si-amb-correccions-menors
  aplicades_des_d_inici: [patro-canonic-pilots-fase-a, aclariment-us-lectura-vs-produccio-C1, variabilitat-cardinal-passos-D3, modulacio-per-perfil-D1]
  aplicades_post_review: [b9-resum-c1-translanguaging-false-rebutjat-correcte, b9-resum-c2-pas1-c1-paratext-aclariment, b9-resum-c3-pas2-a1-3-opcions-plausibles]
  comentari_key: "C1-translanguaging-false-rebutjat-marc-genera-catala-L1-mediat-adult; C2-pas1-C1-paratext-no-confondre-write-resum; C3-pas2-A1-exactament-3-opcions-plausibles"
---

# Generar resum graduat

## Descripció

El resum graduat és una **bastida cognitiva per produir un resum** pas a pas: un marc parcial amb forats calibrats al MECR. La gradació no és de complexitat del text sinó de **la mida del forat**: A1 = forats petits amb opcions tancades; A2 = forats d'una frase sense opcions; B2 = criteri obert; C1 = reflexió metacognitiva. L'alumne no copia el resum: el construeix dins de l'estructura que la bastida proporciona.

**Tipologia MALL**: Mediació (bastida cognitiva de producció de resum).
**HCL principals**: Recapitular (pre-A1/A1, oral/visual) · Resumir (A2+, textual) · Seleccionar idees principals.
**Principi rector — Forat calibrat a la ZDP**: un forat massa gran (per sobre del MECR) genera còpia del text o frustració; un forat massa petit (per sota del MECR) no desenvolupa habilitat. El forat ben calibrat manté l'alumne a la seva ZDP i avança cap a la producció autònoma progressivament.

**Distinció MALL fonamental — Recapitular vs. Resumir:**
- **Recapitular** (pre-A1/A1): reordenar informació oral o visual sense producció textual autònoma. El docent pot escriure el que l'alumne dicta. Cognitiu però no escrit.
- **Resumir** (A2+): primera forma de producció de resum escrit. Requereix seleccionar, generalitzar i connectar idees.
Saltar el recapitular i demanar un resum escrit a pre-A1/A1 és un error pedagògic que genera còpia sense comprensió real.

**Principi "No donar el resum fet"**: el complement genera un marc amb forats, no el resum complet. Si el docent dona el resum complet com a "model", l'alumne el copia. El marc indica COM estructurar, no QUÈ escriure.

**Marc adaptat al tipus de text (cross_source)**:
- Narratiu: tema / personatge / acció principal / desenllaç.
- Expositiu (informatiu, científic): tema / punts clau / conclusió.
- Argumentatiu: tesi / arguments principals / conclusió.
Un marc narratiu per a un text expositiu genera un resum incoherent per al tipus de text.

**Diferència crítica amb complements propers:**
- `plantilles_genere`: plantilla amb forats per produir un text del gènere (no és un resum del text llegit).
- `bastides_produccio`: GPS disciplinar + catàleg de recursos per produir text de gènere nou.
- `write-resum` (gènere): producció autònoma d'un resum sense bastida (A2+ autònom).
- `preguntes_comprensio`: comprensió del text (no producció de resum).

**Connexions MALL transversals:**
- *Forat calibrat com a ZDP operativa*: la bastida funciona si i només si el forat és assolible però exigent. La ZDP del resum és l'espai on l'alumne pot construir la resposta amb esforç sense frustrar-se. Calibrar el forat és l'acte pedagògic central d'aquest complement.
- *Selecció com a competència clau (macroregles)*: el MALL descriu tres macroregles del resum (Kintsch & van Dijk): supressió (treure el secundari), generalització (nombrar la categoria), construcció (inferir el que no s'explicita). El resum graduat entrena explícitament aquestes tres operacions progressivament.
- *Marc = GPS discursiu*: igual que la base d'orientació de les bastides de producció, el marc del resum indica el recorregut. La diferència és que el marc és el text parcial del resum, no el recorregut del procés d'escriptura.
- *Bastida retirable (ZDP)*: el marc es retira progressivament: A2 (marc complet), B1 (marc minimal), B2 (criteris), C1 (reflexió). La bastida té vocació d'extingir-se quan l'alumne internalitza l'estructura del resum.

**Aclariment d'ús — què descriu aquesta rúbrica.**
Aquesta rúbrica descriu el **marc de resum graduat que ATNE genera per guiar la producció del resum** (PRODUCCIÓ MEDIADA). **No descriu el resum autònom de l'alumne ni l'avaluació del docent**: el docent observa si l'alumne omple els forats amb les seves pròpies paraules (no copiant) i si el resultat és coherent amb el text font.
**Sub-granularitat dins de pre-A1**: `fase_lectora: logografica` → recapitulació oral total (el docent escriu el que l'alumne diu). `fase_lectora: alfabetica_emergent` → recapitulació oral + 1-2 paraules escrites per l'alumne.

## Detecció

**Senyals docent** (quan activar el complement):
- Ha activat "Resum graduat" al Pas 2.
- Vol que l'alumne produeixi un resum però necessita bastida estructural.
- La comprensió del text és bona però la producció del resum és caòtica o inexistent.
- Activitat de comprensió lectora amb producció textual de síntesi.

**Senyals alumne** (que indica que necessita la bastida):
- No sap per on començar el resum: "full en blanc del resum".
- Copia frases literals del text en lloc de reformular.
- Fa una llista de frases desconnectades en lloc d'un text cohesionat.
- Inclou exemples secundaris però oblida la idea principal.

**Context favorable**:
- Text TILC on la comprensió és prerequisit i el resum és el producte de síntesi de la sessió.
- Unitats de ciències o socials amb textos expositius densos.
- Tasques d'avaluació on el resum és el producte entregable.

**Anti-senyals** (quan NO activar):
- L'alumne pot fer el resum autònom sense bastida → `write-resum` (gènere).
- L'objectiu és una plantilla per al gènere, no un resum → `plantilles_genere`.
- L'objectiu és aprofundir cognitiu → `activitats_aprofundiment`.
- El text és molt curt (< 80 paraules) → 2-3 preguntes de comprensió orals basten.

## Modulació per nivell

| Pas | Dimensió | Pre-A1 Emergent | A1 Inicial | A2 Funcional | B1 Estratègic | B2 Acadèmic | C1 Crític |
|---|---|---|---|---|---|---|---|
| **1. Tipus de marc** | Estructura del suport | Activitat oral: "De qui parla? Qué fa? Com acaba?" El docent escriu el dictat de l'alumne. Sense marc escrit. | Frase marc amb 1-2 forats + opcions tancades a triar. "El text parla de [tria: opció A / opció B / opció C]." | Marc de 2-3 frases amb 3-4 forats oberts (sense opcions). L'alumne omple amb paraules pròpies. | Marc de 3 parts (tema / punts clau / conclusió) amb 1-2 frases lliures per part. Connectors no donats. | Criteris de qualitat del resum (4-5 ítems basats en les macroregles). L'alumne escriu el resum complet. | Rúbrica metacognitiva: l'alumne justifica les tries. Resum lliure + reflexió sobre el que ha inclòs i deixat fora. |
| **2. Mida del forat** | Calibrat ZDP | Cap forat: activitat oral. | Forat de 1-3 paraules. Opcions totes plausibles: una sola correcta. | Forat d'1 frase (5-10 paraules) sense opcions: l'alumne reformula (no copia). Connectors donats entre frases. | Forat de 2-3 frases amb paraules pròpies i reorganització de la informació. | Criteri obert: "Has seleccionat les idees principals (no els exemples)? Has generalitzat?" | Criteri metacognitiu: "Explica per qué has triat incloure aquesta idea i no aquella altra." |
| **3. Estructura adaptada al tipus de text** | Coherència discursiva | Preguntes orals adaptades: narratiu → "Qui? Qué fa? Com acaba?" / expositiu → "De qué parla? Qué és important?" | Marc adaptat: narratiu → personatge / acció / desenllaç. Expositiu → tema / punt clau / final. | Marc de 2-3 frases adaptat amb connectors donats (Primer... Llavors... Al final...). | Marc de 3 seccions etiquetades: Tema / Punts clau / Conclusió. Connectors no donats. | Criteris que cobreixen les macroregles: selecció (excloure exemples), generalització (categoria), construcció (inferit). | Reflexió discursiva: "Qué has decidit NO incloure i per qué? Quin criteri de selecció has usat?" |
| **4. Recapitular vs. resumir** | Modalitat de producció | Recapitular oral: reordenar informació oral o visual. El docent escriu el dictat; l'alumne dicta. | Recapitular assistit: triar la resposta correcta és una forma de recapitular. Cap escriptura de frases pròpies. | Resumir amb bastida completa: primera producció escrita del resum. Marc molt explícit amb connectors donats. | Resumir amb marc parcialment retirat: l'alumne construeix les idees; el marc proposa l'estructura. | Resumir amb criteris: l'alumne usa les macroregles per produir i autoavaluar el resum. | Resumir i reflexionar: el resum és el punt de partida d'una reflexió metacognitiva sobre les decisions de selecció. |
| **5. Autoavaluació mediada** | Metacognició | "He dit el que passava al text en veu alta." (oral, mediat per adult) | "He triat la resposta correcta. He omplert els buits amb la paraula que encaixava." | "He escrit el resum amb el marc. He usat les meves paraules (no he copiat frases del text)." | "He resumit les idees principals en 3 parts. He usat connectors per lligar les idees." | "He seleccionat les idees principals (no els exemples). He comprovat que el resum s'entén sense llegir el text." | "He justificat per qué he triat cada idea i per qué n'he deixat d'altres fora. He revisat que el meu resum és precís i honest." |

## Metadades de cel·la (per a `build_skills.py`)

**Tipus de descriptor:**
- `binary` — "compleix / no compleix".
- `qualitative` — requereix judici huma o LLM-jutge.
- `countable` — llindar quantitatiu verificable mecanicament.
- `structural` — requereix analisi sintatica o discursiva.
- `metacognitive` — descriptor de proces en primera persona.

| Pas / Dimensió | Tipus | requires_source_text | validation_hint |
|---|---|---|---|
| 1 Tipus de marc | `qualitative` | no | LLM-jutge: el marc és un text parcial amb forats (positiu) o el resum complet donat (negatiu — error crític: viola principi "No donar el resum fet"); verificar que pre-A1 no té marc escrit (oral) i A2+ té marc amb forats; C1: l'output és un paratext de reflexió que ACOMPANYA el resum lliure de l'alumne (no el substitueix) — no confondre amb el gènere `write-resum` |
| 2 Mida del forat | `qualitative` + `binary` | **si** | qualitative: LLM-jutge sobre calibrat del forat al MECR (A1: 1-3 paraules; A2: 1 frase; B1+: 2-3 frases); binary: A1 = presencia d'opcions tancades (exactament 3 opcions: 1 correcta + 2 distractors plausibles — cap d'obviament falsa); A2+ = absencia d'opcions (reformulació pròpia exigida); cross_source: verificar que el forat és completable amb contingut del text font |
| 3 Estructura adaptada al tipus de text | `structural` | **si** | structural: el marc usa l'estructura correcta per al tipus de text declarat (narratiu: personatge/acció/desenllaç; expositiu: tema/punts clau/conclusió; argumentatiu: tesi/arguments/conclusió); cross_source: verificar coherència entre estructura del marc i tipus de text font |
| 4 Recapitular vs. resumir | `binary` | no | binary: pre-A1/A1 = no demana escriptura de frases pròpies (recapitular); A2+ = demana reformulació en paraules pròpies (resumir); error: marc A1 amb forat d'una frase sencera sense opcions |
| 5 Autoavaluació mediada | `metacognitive` | no | pre-A1: registre docent d'observació oral; A1+: derivar a vista d'autoavaluació de l'alumne |

**Notes:**
- Error crític principal: "donar el resum fet" — detectar per LLM-jutge si el marc no té forats o si el text marc és un resum complet sense espais d'escriptura.
- Error secundari: forat copiable literalment del text. Detectar per LLM-jutge (cross_source): si la resposta correcta al forat és una frase literal del text font sense reformulació → error pedagògic.
- Marc genèric (independent del tipus de text): detectar si el marc usa "introduccio/cos/conclusio" en lloc de l'estructura específica del gènere. Error pedagògic significatiu.
- A1 opcions: les tres opcions han de ser candidates plausibles al contingut del text. Cap opció obviament falsa. Detectar per LLM-jutge.

## Heurístiques docent

**H1 — Les opcions de A1 son totes plausibles.**
Si una opció és obviament falsa ("El text parla de: a) volcans b) moda c) maquinaria petroliera" per a un text de volcans), l'alumne endevina sense comprendre. Les tres opcions han de ser possibles per al contingut del text: dues d'inadequades però plausibles, una de correcta. Prova: "Podria algun altre text de la matèria tenir aquesta resposta?" Si la resposta és no per a dues opcions, cal reformular-les.

**H2 — Marc narratiu vs. expositiu: no barrejar.**
Per a contes i biografies: tema / personatge / acció principal / desenllaç. Per a textos expositius (manuals, articles de ciències, notícies): tema / punts clau / conclusió. Per a textos argumentatius: tesi / arguments / conclusió. Usar el marc narratiu per a un text expositiu genera un resum que no té sentit per al tipus de text.

**H3 — El forat copiable és un forat inútil.**
Si l'alumne pot omplir el forat copiant una frase literal del text, la bastida no desenvolupa res. El forat ha de requerir reformulació: l'alumne tria i reescriu amb les seves paraules. La prova: "Pot l'alumne omplir el forat sense entendre el text, simplement cercant la frase?" Si la resposta és sí, cal redissenyar el forat.

**H4 — No donar el resum model.**
Sovint el docent vol donar un "exemple" de com hauria de quedar el resum. Resistir-se a la temptació: l'alumne el copia. En lloc d'exemple, mostrar el marc complet sense omplir i dir: "Tu has d'omplir els forats amb les teves paraules, no les del text." La bastida és el model; el resum omplert per l'alumne és el producte.

**H5 — Recapitular com a pas previ imprescindible (pre-A1/A1).**
Quan treballo amb pre-A1 o A1, dedico 5 minuts a la recapitulació oral ABANS de donar el marc escrit. "Qui és el personatge? Qué fa? Com acaba?" — jo escric el que l'alumne diu. Aquest pas consolida la comprensió i dona a l'alumne el material per omplir el marc. Sense recapitulació oral, el marc escrit es converteix en una tasca de còpia.

## Fonts principals

- MALL (Model d'Aprenentatge de Llengues i Literacitat): recapitular vs. resumir, bastida de producció, ZDP operativa.
- Kintsch, W. & van Dijk, T.A. (1978): "Toward a model of text comprehension and production" — macroregles del resum (supressió, generalització, construcció).
- Solé, I. (1992): *Estrategias de lectura* — estratègies de comprensió; resum com a evidència de comprensió.
- Decret 175/2022 (curriculum Catalunya): competencia lectora i produccio de textos.
