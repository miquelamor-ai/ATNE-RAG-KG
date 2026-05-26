---
modul: M3
titol: "Generar plantilles de gènere"
tipus: instrument
categoria_principal: mediacio
categories_secundaries: []
descripcio: "Instrument per generar una plantilla de gènere (text model parcial amb forats) que l'alumne omple per produir el seu text. Diferent de la base d'orientació (passos abstractes): la plantilla dona el text concret parcialment complert. Forats decreixents A1→C1; pre-A1 visual (requadres+icones). Rúbrica gradada 5 passos × 6 nivells MECR (pre-A1→C1)."
mecr_range: [pre_A1, A1, A2, B1, B2, C1]
agent_roles: [generator]
complement_key: plantilles_genere
translanguaging: false
multimodal: true
moduls_relacionats: [M2, M3]
variables_configurables:
  fase_lectora: [logografica, alfabetica_emergent, alfabetica_fluida]
skill_meta: generate-plantilles-genere@corpusFJE/skills/mediacio/generate-plantilles-genere
review_status: pilot-fusio-8
version: 4.0.0-canonic
generat_at: 2026-05-26
actualitzat_at: 2026-05-26
notebooklm_review:
  data: 2026-05-26
  veredicte: si-amb-correccions-menors
  aplicades_des_d_inici: [patro-canonic-pilots-fase-a, aclariment-us-lectura-vs-produccio-C1, variabilitat-cardinal-passos-D3, modulacio-per-perfil-D1]
  aplicades_post_review: [b8-plantilles-multimodal-true, b8-plantilles-pas1-c1-hint, b8-plantilles-antisenyal-bastides-produccio]
  comentari_key: "multimodal-true-prea1-icones-requadres; pas1-C1-hint-minimalista-es-correcte; antisenyal-bastides-vs-plantilles-afegit"
---

# Generar plantilles de gènere

## Descripció

La plantilla de gènere és un **text model parcial** que mostra a l'alumne com queda el gènere acabat, amb algunes seccions completes i d'altres deixades com a buits guiats per omplir. L'alumne no segueix passos: **imita i completa** un text que ja té la forma del gènere. La seva funció pedagògica és descarregar la **càrrega d'estructurar** (saber com s'organitza el gènere) perquè l'alumne pugui centrar-se en el contingut i la llengua.

**Tipologia MALL**: Mediació (bastida de textualització — Fase 4 de la Seqüència Didàctica).
**HCL associada**: cap HCL pròpia — la plantilla emmarca la HCL del gènere actiu. El text donat mostra la HCL en acció; els forats demanen que l'alumne la practiqui.
**Principi cognitiu**: la plantilla elimina la càrrega d'estructurar (pas 2 de la textualització de Flower-Hayes) perquè l'alumne pugui centrar-se en recuperar el contingut (pas 1) i codificar-lo en la nova llengua (pas 3).
**Principi rector**: els forats han de ser **específics del contingut real del text treballat**, no genèrics. "L'any ___, a ___, [nom del personatge concret del text] va..." és específic. "Un personatge va..." és genèric i desconnecta la plantilla del text llegit.

**Distinció fonamental amb la base d'orientació:**
- **Base d'orientació** (Bloc A de bastides-produccio): procediment (GPS de passos) — "1. Escriu el títol. 2. Situa el context..."
- **Plantilla de gènere**: text model parcial — mostra com queda el text acabat, amb buits per omplir.
L'alumne que usa la base d'orientació sap QUÈ fer en cada pas. L'alumne que usa la plantilla veu DIRECTAMENT com ha de quedar el text.

**Pre-A1 SÍ (D6)**: la plantilla visual (requadres + icones) és accessible a lectors logografics perquè no demana produir text autònom — demana dibuixar o enganxar dins d'un esquema estructurat. L'adult llegeix les instruccions en veu alta i l'alumne respon visualment. El significat es construeix per via concreta i visual, mediat per l'adult.

**Connexions MALL transversals:**
- *Text model explícit (Seqüència Didàctica)*: el MALL usa el text model per mostrar com s'escriu el gènere ABANS de demanar que l'alumne l'escrigui. La plantilla és el text model + els forats que converteixen la lectura/observació en producció activa.
- *Gradació dels forats com a ZDP operativa*: el forat petit (A1, 1-2 paraules) es situa a la zona confort; el forat gran (C1, producció lliure per secció) és el repte màxim. La plantilla manté l'alumne a la seva ZDP mentre avança cap a la producció autònoma.
- *Imitació com a aprenentatge legítim*: la plantilla no és una drecera deshonesta. Aprendre un gènere és aprendre les seves convencions, i la imitació guiada és el primer pas cap a la producció autònoma. El text donat és el model, no la còpia.
- *Forats específics com a ancoratge al contingut*: els buits genèrics desconnecten la plantilla del text que l'alumne ha llegit. Els forats específics ("En [nom del personatge del text]...") mantenen el vincle entre la comprensió lectora i la producció escrita.

**Aclariment d'ús — què descriu aquesta rúbrica.**
Aquesta rúbrica descriu la **plantilla que ATNE genera perquè l'alumne produeixi el seu text** (PRODUCCIÓ MEDIADA). **No descriu la producció autònoma de l'alumne**: la plantilla és el suport, la producció de l'alumne és el resultat. El docent observa si l'alumne completa els forats amb contingut rellevant del text treballat.
**Sub-granularitat dins de pre-A1**: `fase_lectora: logografica` → plantilla visual pura (dibuixar/enganxar). `fase_lectora: alfabetica_emergent` → plantilla amb 1-2 paraules per forat, mediat per adult.

## Detecció

**Senyals docent** (quan activar el complement):
- Ha activat "Plantilles de gènere" al Pas 2.
- L'alumne ha de produir un text del gènere treballat i necessita veure com queda el text acabat.
- Primera exposició a un gènere nou: l'alumne sap el contingut però no sap com estructurar-lo.

**Senyals alumne** (que indica que necessita el suport):
- Coneix el contingut però no sap com estructurar el text del gènere.
- Escriu els fets sense l'estructura del gènere: el resultat és correcte en contingut però sense forma reconeixible.
- En producció lliure: comença sempre de la mateixa manera independentment del gènere.

**Context favorable**:
- Primera exposició a un gènere nou en qualsevol matèria.
- Alumnat nouvingut o amb dificultats d'expressió que necessita un model concret.
- Context TILC: l'alumne domina el contingut en L1 però necessita el motlle del gènere en català.

**Anti-senyals** (quan NO activar):
- L'alumne ja domina l'estructura del gènere → la plantilla pot restar autonomia i fluència creativa.
- El text adaptat no té tasca de producció associada → sense contingut que emplenar, la plantilla no té sentit.
- La tasca de producció demana originalitat estructural (assaig creatiu, escriptura experimental) → plantilla mínima o cap.
- L'alumne necessita el GPS de passos per planificar ABANS de textualitzar → `bastides-produccio` (Bloc A, base d'orientació). Seqüència recomanada: bastides-produccio primer (planifica), plantilles-genere després (textualitza).
- El resum del text com a tasca de producció → `resum-graduat`.

## Modulació per nivell

| Pas | Dimensió | Pre-A1 Emergent | A1 Inicial | A2 Funcional | B1 Estratègic | B2 Acadèmic | C1 Crític |
|---|---|---|---|---|---|---|---|
| **1. Tipus de plantilla** | Format i densitat del text donat | Visual: 3-4 requadres amb icones. Cap text autònom. L'adult llegeix les instruccions. | Text quasi complet: 70-80% donat, 20-30% forats. 1-2 paraules per forat. | Text parcialment donat: 50-60% donat, 40-50% forats. Frases curtes per completar. | Text marc: 30-40% donat (connectors, estructura, termes disciplinars clau). | Plantilla minimalista: encapçalaments + 1 frase d'exemple per secció com a model de referència. | Criteris de gènere i estil. Pràcticament sense text donat: el primer mot de cada secció com a únic ancoratge. |
| **2. Especificitat dels forats** | Concretesa del contingut del forat | Requadre de dibuix o icona per completar. Cap text a omplir autònomament. | Forats de 1-2 paraules: nom concret, verb d'acció, un adjectiu. Completables amb paraules del text adaptat. | Forats d'1 frase: "Els protagonistes son ___" · "El conflicte és ___". Completables amb reformulació del text. | Forats de 2-3 frases construïdes per l'alumne amb les seves paraules a partir del text. | Forats que demanen elaboració argumentada (1 paràgraf) que va més enllà del text (connexió, anàlisi). | Forats de producció lliure coherent amb el gènere, inspirada però no limitada pel text. |
| **3. Vinculació al text adaptat** | Ancoratge al contingut llegit | Forats completables amb imatges o paraules que apareixen al text. L'adult mostra on és la resposta. | Forats completables amb paraules o noms extrets directament del text adaptat. | Forats que requereixen selecció i reformulació d'informació del text. | Forats que requereixen inferència o selecció crítica d'informació del text. | Forats que requereixen elaboració que va més enllà del text (connexió amb altres fonts). | Forats de producció pròpia de l'alumne, inspirada però autònoma. |
| **4. Densitat dels forats** | Proporció text donat / forats | Maxima densitat visual: tota la plantilla és un esquema. Cap text en prosa. | Alta densitat forats: 1 forat cada 2-3 paraules. El text donat guia i contextualitza. | Densitat moderada: 1 forat per frase o cada 2 frases. Text donat aporta estructura. | Densitat baixa: 1 forat per paràgraf. L'alumne aporta la major part del contingut. | Densitat mínima: 1 forat per secció. Quasi tot és producció pròpia. | Forat de producció completa per secció. La plantilla és una rúbrica de gènere. |
| **5. Autoavaluació mediada** | Metacognició | "He dibuixat (o enganxat) el que passa al text." (oral, mediat per adult) | "He completat les paraules que faltaven amb informació del text." | "He completat les seccions amb informació del text que he llegit." | "He completat la plantilla amb informació pròpia sobre el contingut. He verificat que els forats son coherents amb el gènere." | "He usat la plantilla com a model de referència i he escrit el text amb les meves pròpies paraules." | "He usat els criteris de gènere per autoregular la meva producció sense suport directe." |

## Metadades de cel·la (per a `build_skills.py`)

**Tipus de descriptor:**
- `binary` — "compleix / no compleix".
- `qualitative` — requereix judici huma o LLM-jutge.
- `countable` — llindar quantitatiu verificable mecanicament.
- `structural` — requereix analisi sintatica o discursiva.
- `metacognitive` — descriptor de proces en primera persona.

| Pas / Dimensió | Tipus | requires_source_text | validation_hint |
|---|---|---|---|
| 1 Tipus de plantilla | `binary` | no | binary: format correcte per nivell (visual pre-A1: requadres presents; A1: ≥70% text donat; B2+: ≤30% text donat); NOTA: plantilla quasi-buida a C1 és CORRECTA (forat = producció completa per secció) — el validador no ha de penalitzar la densitat mínima a C1 |
| 2 Especificitat dels forats | `qualitative` | **si** | LLM-jutge: forats específics del text treballat (positiu) vs forats genèrics "un personatge" (negatiu); cross_source: verificar que els noms, llocs i fets dels forats apareixen al text font |
| 3 Vinculació al text adaptat | `qualitative` | **si** | LLM-jutge sobre si els forats requereixen recuperació d'informació del text (A1-B1, positiu) o inventar informació nova sense ancoratge (negatiu); cross_source: coherencia entre forats i contingut del text font |
| 4 Densitat dels forats | `countable` | no | calcular proporció aproximada text donat / forats; verificar rang per nivell (A1: ≥70% donat; A2: 50-60%; B1: 30-40%; B2: ≤30%; C1: quasi tot forats) |
| 5 Autoavaluació mediada | `metacognitive` | no | pre-A1: autoavaluació oral mediada per l'adult (l'adult pregunta + registra); A1+: derivar a vista d'autoavaluació de l'alumne |

**Notes:**
- Forat específic vs genèric: l'error más freqüent. Detectar forats del tipus "un personatge va..." per regex + LLM-jutge. Si el forat podria servir per a qualsevol text del mon, és genèric.
- Pre-A1 visual: detectar presencia de `🖊`, `🖼`, `[Dibuixa aquí]` o `[Enganxa aquí]` com a indicadors de plantilla visual. Absencia = error si fase_lectora = logografica.
- Plantilla vs base d'orientació: si la "plantilla" generada és una llista de passos en comptes d'un text parcial, és una base d'orientació equivocada — LLM-jutge.
- Forats completables en 15-20 minuts: si la plantilla demana produccions massa extenses per al nivell, reducció de densitat recomanada.

## Heurístiques docent

**H1 — El test del forat genèric.**
Llegeixo cada forat de la plantilla i em pregunto: "Podria omplir-lo un alumne sense haver llegit el text treballat?" Si la resposta és sí, el forat és massa genèric. Cal anclar-lo al contingut real: "El científic [nom del text] va descobrir que ___" en comptes de "Un científic va descobrir que ___". El forat específic verifica la comprensió lectora a la vegada que orienta la producció.

**H2 — La plantilla com a pòster de classe.**
Proposo penjar la plantilla a la paret com a referència visual mentre els alumnes escriuen. Poden consultar-la sense haver d'obrir el document. La visibilitat contínua redueix la sensació d'estar "en blanc" i normalitza la consulta del model.

**H3 — Completar oralment primer (A1-A2).**
Proposo que l'alumne completi els forats verbalment en parella ABANS d'escriure. "Jo diria... i tu?" El company valida o proposa alternatives. La versió oral no necessita ser perfecta; és la prova de foc de la comprensió. Llavors escriuen. La seqüència oral→escrit és la lògica natural de l'aprenentatge de la L2.

**H4 — Plantilla vs base d'orientació: la pregunta de la funció.**
Quan dubto si generar una plantilla o una base d'orientació, em pregunto: "L'alumne necessita veure com QUEDA el text acabat, o necessita saber els PASSOS per construir-lo?" Si vol veure el text acabat → plantilla. Si vol els passos → base d'orientació (Bloc A de bastides-produccio). Els dos son compatibles i complementaris: base d'orientació per planificar, plantilla per textualitzar.

**H5 — Retirar la bastida progressivament.**
La plantilla és una bastida temporal. A mesura que l'alumne interioritza el gènere, redueixo el nombre de forats (del 70% de text donat al 30%). El docent decideix quan la plantilla ja no és necessaria i l'alumne escriu a partir del model interioritzat. Un indicador fiable: si l'alumne omple els forats en menys de 5 minuts sense consultar el text, la bastida és massa fàcil i cal reduir-la.

## Fonts principals

- MALL (Model d'Aprenentatge de Llengues i Literacitat): Seqüència Didàctica, Fase 4 textualitzacio, text model explícit.
- Flower, L. & Hayes, J.R. (1981): "A cognitive process theory of writing" — model de textualitzacio (planificació + traducció + revisió); la plantilla descarrega la traducció per alliberar capacitat cognitiva.
- Vygotsky, L.S. (1978): *Mind in Society* — zona de desenvolupament proper; andamiatge i retirada progressiva de la bastida.
- Gibbons, P. (2002): *Scaffolding Language, Scaffolding Learning* — text model i plantilla com a suport de producció per a alumnat EAL.
- Decret 175/2022 (curriculum Catalunya): competencia en comunicacio lingüística i produccio de textos.
