---
modul: M3
titol: "Escriure/adaptar un conte"
tipus: instrument
categoria_principal: generes
categories_secundaries: []
descripcio: "Instrument per adaptar o generar un conte narratiu breu (situació-conflicte-clímax-resolució). HCL Narrar: seqüenciació causal, personatge amb motivació, emoció nomenada, diàleg atribuït. Rúbrica gradada 9 passos × 6 nivells MECR."
mecr_range: [pre-A1, A1, A2, B1, B2, C1]
agent_roles: [adapter, generator]
genre_key: conte
translanguaging: true
multimodal: true
moduls_relacionats: [M3]
variables_configurables:
  fase_lectora: [logografica, alfabetica_emergent, alfabetica_fluida]
skill_meta: write-conte@corpusFJE/skills/generes/write-conte
review_status: pilot-fusio-3
version: 4.0.0-canonic
generat_at: 2026-05-26
actualitzat_at: 2026-05-26
notebooklm_review:
  data: 2026-05-26
  veredicte: si-amb-correccions-menors
  aplicades_des_d_inici: [patro-canonic-pilots-fase-a, aclariment-us-lectura-vs-produccio-C1, fidelitat-gradada-C2, variabilitat-cardinal-passos-D3]
  aplicades_post_review: [metadades-8.2-present-narratiu-excepcio-C1, metadades-7-dialeg-opcional-A1-no-penalitzar]
  comentari_key: "El pilot de conte estableix el model per als gèneres de ficció del corpus, resolent amb èxit la gradació de la complexitat psicològica dels personatges."
---

# Escriure/adaptar un conte

## Descripció

El conte és un gènere narratiu breu amb estructura de cinc parts (situació inicial, conflicte, seqüència d'esdeveniments, clímax i resolució). La seva funció pedagògica és treballar la **HCL Narrar**: seqüenciar fets causalment, presentar personatges amb motivació i emoció explícites, i tancar el relat amb una resolució coherent. És el gènere "porta" a la ficció literària per la universalitat de la seva estructura.

**Tipologia MALL**: Narrativa (imaginar — construir mons possibles).
**HCL principal**: Narrar — seqüenciar fets causalment, presentar personatge amb conflicte i resolució.
**HCL secundàries**: Descriure context i personatges (A2+) · Interpretar motivacions i emocions (B1+) · Valorar intenció estètica i literarietat (B2+).
**Pre-A1 (Emergent)**: Oral i gestual — narració mediada per l'adult amb seqüència d'imatges.

**Connexions MALL transversals:**
- *Translanguaging / TOLC*: a pre-A1 i A1, l'alumne pot narrar oralment en L1 i l'adult fa el pont al català. Al text adaptat, paraules en L1 entre claudàtors `[...]` mantenen el fil narratiu quan el terme en català és opac.
- *Multimodalitat*: a pre-A1 i A1, les il·lustracions seqüenciades sostenen la narració i bastiden la cronologia. L'ordre visual és la bastida de la seqüenciació temporal.
- *Eix oral/escrit*: el conte es treballa primer oralment (narrar en veu alta) i després es passa a la producció escrita. Recomanat fins a A2.

**Aclariment d'ús — què descriu aquesta rúbrica.**
Aquesta rúbrica descriu el **conte adaptat per a la LECTURA** de l'alumne (el que el docent presenta perquè l'alumne llegeixi). **No descriu la producció autònoma de l'alumne** — la producció narrativa de l'alumne s'avalua amb un derivat propi (rúbrica d'avaluació formativa). Principi pedagògic MALL: l'alumne llegeix models bons al màxim del seu abast i en produeix els seus textos; l'adaptació és tasca del docent.
**Sub-granularitat dins de pre-A1 i A1**: es treballa amb la variable independent `fase_lectora` del frontmatter (logografica · alfabetica_emergent · alfabetica_fluida), no amb columnes addicionals.

## Detecció

**Senyals docent** (quan adaptar a gènere conte):
- El text font és narratiu de ficció: té personatge, conflicte i resolució.
- La unitat treballa la HCL Narrar o la competència lectoliterària.
- L'alumne ha de llegir un text narratiu adaptat al seu MECR com a model de lectura.
- L'objectiu inclou la producció de narració com a activitat posterior (relat, conte propi).
- El text original és un conte complex per al nivell de l'alumne i cal adaptar-lo.

**Senyals alumne** (que indica que necessita bastida narrativa):
- Explica fets sense ordre: barreja el principi i el final sense connector causal.
- Usa "i llavors" reiteradament sense connectors causals: no ha adquirit la causalitat narrativa.
- Descriu el personatge però no el seu problema: conte "estàtic" sense conflicte.
- Escriu frases aïllades que no s'encadenen causalment ("va anar al parc. Va jugar. Va menjar.").
- Omete el final o el resol en una sola paraula ("i van viure feliços").
- Nouvingut A1-A2: s'atura al primer paràgraf i mira l'adult sense dir res.

**Context favorable**:
- Tutoria, Llengua Catalana, Castellana o estrangera en unitats de narració.
- Alumnat nouvingut A1-A2: el conte és el gènere "porta" a la ficció per la universalitat de la seva estructura narrativa.
- Unitats TILC on el contingut curricular s'explica via relat (conte científic, conte històric).

**Anti-senyals** (quan NO adaptar a conte):
- El text font és informatiu o argumentatiu → adaptar al gènere original.
- El text inclou una moral explícita i personatges animals o simbòlics → fàbula.
- El text tracta d'una persona real amb fets verídics → biografia.
- L'objectiu és la comprensió, no la narració → preguntes de comprensió.
- Pre-A1 sense mediació adulta disponible: el gènere requereix oral sostingut.

## Modulació per nivell

| Pas | Dimensió | Pre-A1<br>Emergent | A1<br>Inicial | A2<br>Funcional | B1<br>Estratègic | B2<br>Acadèmic | C1+<br>Crític |
|---|---|---|---|---|---|---|---|
| **1. Situació inicial** | Personatges i context | Adult narra. L'alumne assenyala el personatge principal a la imatge. | 1 personatge + 1 lloc en 1-2 frases. Sense descripció de trets. | 1-2 personatges amb un tret cadascun. Lloc en 1 frase de context. | 1-2 personatges amb tret i desig inicial clars. Lloc amb ambient breu. | Personatges amb motivació explícita. Context temporal i espacial integrat al relat. | Personatges complexos amb motivació i tensió interna. Context ric i funcional per a la trama. |
| **2. Conflicte** | Obstacle i causa | Adult explica el problema. L'alumne escolta i assenyala la imatge del conflicte. | 1 problema en 1 frase. "El lleó té gana però no hi ha menjar." | Conflicte clar: el personatge vol X però hi ha un obstacle. Causa no obligatòria. | Conflicte amb causa explícita. L'obstacle és comprensible per al lector. | Conflicte amb dimensió emocional. La causa s'explicita i impacta el personatge. | Conflicte complex: pot incloure tensions morals, dilemes o contradicció interna del personatge. |
| **3. Seqüència d'esdeveniments** | Ordre i causalitat | 2-3 imatges amb una frase oral per imatge. L'adult transcriu si l'alumne dicta. | 2-3 frases de fets en ordre cronològic. Sense connectors causals obligatoris. | 3-4 frases ordenades amb connectors temporals simples ("primer", "després", "llavors"). | 3-4 esdeveniments amb connectors variats (temporals + causals). Causa i efecte explícits. | Seqüència de 4-5 actes amb causa-efecte i tensió creixent cap al clímax. | Seqüència causal elaborada. Cada acte prepara el clímax. Pot incloure paral·lelisme o recursivitat. |
| **4. Clímax** | Punt de màxima tensió | L'adult assenyala el moment de tensió. L'alumne el reconeix ("aquí és on tot va malament"). | 1 frase sobre el moment decisiu. Visual i inequívoc. | El moment de màxima tensió es pot identificar clarament al text. | Clímax marcat amb connector de contrast ("però", "de sobte"). Tensió nomenada. | Clímax amb emoció nomenada del personatge + acció decisiva. Tensió crescuda gradualment. | Clímax amb decisió moral, reversió o canvi de perspectiva. Pot incloure ironia si el context ho justifica. |
| **5. Resolució** | Coherència i tancament | L'adult llegeix la resolució. L'alumne identifica si ha anat bé o malament. | 1 frase de resolució. Positiva o negativa, clara i inequívoca. | Resolució en 1-2 frases. Coherent amb el conflicte plantejat. | Resolució que connecta causalment amb el conflicte (com s'ha resolt). | Resolució amb reflex emocional del personatge. Final tancat amb matís moderat. | Resolució oberta, irònica o ambigua si el context literari ho requereix. Ha de ser significativa. |
| **6. Emocions nomenades** | Varietat i situació | Cap escriptura d'emocions. L'adult pot preguntar oralment "Com es sent?" | 1 emoció nomenada en un moment clau. Vocabulari bàsic ("content", "trist", "tenia por"). | 1-2 emocions nomenades situades en moments clau del conte. | 2-3 emocions variades situades en el moment de l'acció. Connexió causa-emoció explícita. | Emocions integrades al text sense aparèixer llistades. Matisades i variades. | Emocions complexes o contradictòries. Descripció interior del personatge possible. |
| **7. Diàleg** | Atribució i funció | Sense diàleg escrit. L'adult pot dramatitzar les veus oralment. | Sense diàleg o 1 frase molt simple, clarament atribuïda. | 1-2 torns de diàleg atribuïts per nom ("En Marc va dir: '...'"). Diàleg informatiu. | 2-3 torns de diàleg atribuïts que fan avançar la trama. Veus diferenciades per nom. | Diàleg que revela caràcter o conflicte. Format narratiu o teatral ben marcat. | Diàleg amb subtext: el que es diu i el que es vol dir. Pot incloure ironia o doble sentit. |
| **8. Criteris transversals** | Cronologia | Imatges en ordre. L'adult sostè la seqüència. | Ordre temporal clar. No flashbacks. | Connectors temporals garanteixen l'ordre. No flashbacks. | Cronologia lineal estricta. Connectors causals i temporals variats. No flashbacks. | Cronologia lineal. Pot incloure una pausa narrativa breu (aturada reflexiva). | Cronologia lineal o anacronia marcada intencionadament i clara per al lector. |
|  | Temps verbals | L'adult usa el passat simple. L'alumne imita. | Passat simple consistent. Cap barreja amb present. | Passat simple consistent. Imperfet per a descripcions ("era", "tenia"). | Passat simple + imperfet correctes. Pluscuamperfet bàsic admissible. | Temps narratius consistents. Usos elaborats del pluscuamperfet. | Domini complet dels temps narratius. Pot usar present narratiu com a recurs estilístic. |
|  | Fidelitat al text font | Fidelitat al personatge i l'acció nuclear (qui, on, què passa). | Fidelitat al personatge, l'acció i el final. | Fidelitat al personatge, l'acció, el conflicte i el final. | Fidelitat al conflicte, la seqüència principal i el to general. | Fidelitat al matís emocional, el to i les relacions entre personatges. | Fidelitat a la veu narrativa, el to, els recursos literaris i la intenció estètica. |
| **9. Autoavaluació metacognitiva** | Reflexió sobre el procés | "He vist les imatges i he dit el que passa a cada una." (oral, mediat per l'adult) | "He escrit qui és el personatge, on és i què li passa. He escrit el final." | "El meu conte té un problema i un final. He nomenat com se sent el personatge." | "He escrit els 5 moments del conte en ordre. He explicat per què el personatge fa el que fa." | "El meu conte té tensió creixent i resolució coherent. Les emocions estan integrades al text, no llistades." | "El meu conte té personatges complexos, clímax ben construït i resolució significativa. He revisat que la veu narrativa sigui consistent." |

## Metadades de cel·la (per a `build_skills.py`)

Cada dimensió té un **tipus de descriptor** que condiciona com s'ha de transformar al derivat avaluatiu i al derivat-prompt.

**Tipus de descriptor:**
- `countable` — té un llindar quantitatiu verificable mecànicament.
- `binary` — només admet "compleix / no compleix".
- `qualitative` — requereix judici humà o LLM-jutge.
- `structural` — requereix anàlisi sintàctica o discursiva.
- `cross_source` — requereix accés al text font per comparar.
- `metacognitive` — descriptor de procés en primera persona.

| Pas / Dimensió | Tipus | requires_source_text | validation_hint |
|---|---|---|---|
| 1 Situació inicial — Personatges i context | `qualitative` + `countable` | no | LLM-jutge: comptar personatges presents; verificar presència de tret/motivació per nivell |
| 2 Conflicte — Obstacle i causa | `qualitative` | no | LLM-jutge: detectar obstacle explícit; verificar causa explícita (B1+) |
| 3 Seqüència — Ordre i causalitat | `structural` + `enumerable` | no | detectar connectors temporals i causals; verificar ordre cronològic del relat |
| 4 Clímax — Punt de màxima tensió | `qualitative` | no | LLM-jutge: identificar moment de màxima tensió; verificar marcadors de contrast (B1+) |
| 5 Resolució — Coherència i tancament | `qualitative` + `binary` | no | binary: resolució present/absent; qualitative: coherència resolució-conflicte per nivell |
| 6 Emocions — Varietat i situació | `qualitative` + `countable` | no | comptar emocions nomenades; LLM-jutge: verificar si estan situades en moment del text (B1+) o llistades |
| 7 Diàleg — Atribució i funció | `binary` (per existència) + `structural` | no | detectar marques de diàleg ("va dir", "va preguntar"); verificar atribució per nom (A2+). A A1, diàleg és opcional: no penalitzar l'absència ni incloure'l a l'autoavaluació del derivat. A C1+, el subtext requereix la intenció autoral com a entrada: si no es declara, el derivat marca la cel·la com `revisio-humana` en lloc de LLM-jutge |
| 8.1 Criteris — Cronologia lineal | `binary` + `structural` | no | detectar anacronia no marcada; verificar que connectors temporals sostenen l'ordre |
| 8.2 Criteris — Temps verbals | `qualitative` + `binary` | no | LLM-jutge: consistència de temps narratius; detectar barreja no intencionada passat/present. Excepció C1+: el present narratiu és recurs estilístic vàlid si és consistent — no marcar com a error |
| 8.3 Criteris — Fidelitat al text font | `cross_source` | **sí** (text original si adaptació) | comparació semàntica gradada per nivell: pre-A1→A2 personatge+acció nuclear; B1 conflicte+to; B2-C1 matís emocional+veu narrativa. Només aplica quan s'adapta un text, no quan es genera de zero |
| 9 Autoavaluació metacognitiva | `metacognitive` | no | derivar a vista d'autoavaluació alumne + registre docent de la qualitat de la reflexió |

**Notes:**
- El conte és gairebé tot `qualitative`: el LLM-jutge és el mecanisme de validació principal.
- Diàleg (7) és parcialment automatitzable: regex per detectar `va dir`, `va preguntar`, `va cridar`.
- Cronologia (8.1) és parcialment automatitzable per connectors; la detecció d'anacronia no marcada requereix LLM.
- Fidelitat (8.3) és condicional: si el mode és `generator` (nou conte), no es valida fidelitat al font.

## Heurístiques docent

**H1 — El diagnòstic narratiu ràpid.**
Demano a l'alumne que m'expliqui el conte en tres frases: "Qui és? Què li passa? Com acaba?" Si no pot respondre les tres, identifico el buit: personatge sense conflicte, conflicte sense resolució, o resolució sense connexió al conflicte. El conte ben adaptat ha de respondre les tres preguntes de manera clara i encadenada.

**H2 — "I llavors, i llavors, i llavors..." com a senyal de causalitat absent.**
Quan l'alumne usa "i llavors" repetidament per connectar accions, no ha adquirit els connectors causals. El problema no és estilístic sinó conceptual: no distingeix seqüència temporal de causa i efecte. Introdueixo 3 connectors específics per sessió ("però", "de sobte", "perquè") escrits a la pissarra i demano que almenys 2 apareguin al text. La pregunta "Per què fa això el personatge?" activa la causalitat on falta.

**H3 — L'emoció al marge.**
Per a alumnat A1-A2, proposo un cartell a l'aula amb 10-15 emocions en paraules i pictograma. Quan l'alumne escriu "estava bé" o "es va posar content", li demano que triï una emoció més precisa del cartell. El cartell substitueix el diccionari i entrena la vocabulari emocional de forma autònoma sense interrompre la redacció.

**H4 — Pre-A1: el conte de 3 imatges.**
Per a alumnat emergent, proposo tres imatges en ordre (inici/conflicte/resolució) i demano que expliqui oralment el que passa a cada una. Transcric el que diu i li llegeixo el "seu conte". L'efecte és doble: l'alumne veu que és capaç de narrar i connecta per primera vegada l'oral amb l'escrit. La seqüència d'imatges bastida la cronologia que encara no pot construir per escrit.

**H5 — Diàleg atribuït vs. diàleg flotant.**
El diàleg flotant ("—Hola! —Hola!") és molt freqüent als contes d'alumnat A1-A2 i dificulta la comprensió. Mostro la diferència en viu: escric el diàleg flotant a la pissarra, pregunto "Qui parla?" i quan no ho saben, afegim "va dir en Marc" i "va respondre la Laia". La regla és simple i visual: cada vegada que hi ha parèntesi o guió de diàleg, cal dir qui parla.

## Fonts principals

- MALL (Model d'Aprenentatge de Llengües i Literacitat): HCL Narrar, estructura narrativa, gradació MECR.
- Propp, V. (1928): *Morfologia del conte* — les funcions narratives com a estructura universal transferible a tots els contextos d'aula.
- Labov, W. i Waletzky, J. (1967): estructura narrativa canònica (situació-nus-resolució) com a unitat mínima de narració.
- Bruner, J. (1990): *Acts of Meaning* — el pensament narratiu com a mode de cognició universal, anterior i paral·lel al lògic-científic.
- Decret 175/2022 (currículum Catalunya): competència en comunicació lingüística, dimensió literària i narrativa.
