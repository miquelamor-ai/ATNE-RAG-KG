---
modul: M3
titol: "Escriure/adaptar un assaig"
tipus: instrument
categoria_principal: generes
categories_secundaries: []
descripcio: "Instrument per adaptar o generar un assaig argumentatiu-reflexiu: tesi explícita a la introducció, arguments ordenats amb evidències, refutació d'una postura contrària (A2+), connectors argumentatius progressius i conclusió tancada. HCL Argumentar + Interpretar/Valorar (A1-A2). No s'adapta a pre-A1. Rúbrica gradada 9 passos × 5 nivells MECR (A1→C1)."
mecr_range: [A1, A2, B1, B2, C1]
agent_roles: [adapter, generator]
genre_key: assaig
translanguaging: true
multimodal: false
moduls_relacionats: [M3]
variables_configurables:
  fase_lectora: [alfabetica_emergent, alfabetica_fluida]
skill_meta: write-assaig@corpusFJE/skills/generes/write-assaig
review_status: pilot-fusio-7
version: 4.0.0-canonic
generat_at: 2026-05-26
actualitzat_at: 2026-05-26
notebooklm_review:
  data: 2026-05-26
  veredicte: si-amb-correccions-menors
  aplicades_des_d_inici: [patro-canonic-pilots-fase-a, aclariment-us-lectura-vs-produccio-C1, fidelitat-gradada-C2, variabilitat-cardinal-passos-D3]
  aplicades_post_review: [b5-assaig-conclusio-b1-proposta-opcional]
  comentari_key: "pas5-b1-proposta-derivada-canviada-a-implicacio-breu-opcional; tesi-implicita-a1-mantinguda-text-model-lectura"
---

# Escriure/adaptar un assaig

## Descripció

L'assaig és un text reflexiu i argumentatiu que defensa una **tesi explícita** amb arguments ordenats i, a partir de B1, amb evidències o cites integrades. A diferència de l'article d'opinió (que prioritza la persuasió directa i el posicionament personal), l'assaig té un to més reflexiu, una estructura formal visible i un vocabulari acadèmic progressiu.

**Tipologia MALL**: Argumentativa-reflexiva.
**HCL principal**: Argumentar — defensar una tesi amb arguments ordenats i evidència. A A1-A2, el pes real recau sobre la HCL Interpretar/Valorar (posicionar-se davant d'una idea i justificar el posicionament), que és el camí d'entrada a l'Argumentar formal.
**HCL secundàries**: Justificar (B1+, evidències vinculades a fonts) · Avaluar (B2+, contrast de postures i ponderació d'arguments).
**No s'adapta a pre-A1**: l'assaig requereix la producció d'una tesi explícita amb arguments ordenats, la comprensió de la relació entre tesi, argument i evidència com a estructura lògica abstracta, i la capacitat de refutar o matisar una postura contrària. Aquesta combinació d'operacions cognitives abstractes requereix base lecto-escriptora mínima i capacitat de pensament formal. (Decisió 6 canònica Fase B.)

**Connexions MALL transversals:**
- *CALP de Cummins — l'assaig com a cim de la llengua acadèmica*: l'assaig és el gènere on el CALP (llengua acadèmica de pensament abstracte) és més visible i dens. La gradació del vocabulari i les cites implementa la progressió BICS→CALP de manera explícita. Treballar l'assaig des de A1 (en format molt simplificat) construeix la base per a l'escriptura acadèmica de llarg recorregut.
- *Refutació com a pensament crític*: reconèixer i respondre al punt de vista contrari és el nucli del pensament crític. A B1, és la transició de "defenso la meva postura" a "entenc la postura dels altres i hi respoc". La HCL Argumentar no és un monòleg, és un diàleg amb l'interlocutor implícit.
- *Translanguaging*: a A1, l'alumne pot usar paraules de la L1 entre claudàtors [...] per mantenir el fil argumentatiu quan no troba el terme en català. A B1+, pot integrar cites en la L1 si s'acompanyen de traducció o paràfrasi en català.

**Aclariment d'ús — què descriu aquesta rúbrica.**
Aquesta rúbrica descriu el **text adaptat per a la LECTURA** de l'alumne. **No descriu la producció autònoma** — la producció és tasca d'un derivat propi. Principi pedagògic MALL: l'alumne llegeix models al màxim del seu abast.
**Sub-granularitat dins de A1**: es treballa amb `fase_lectora: [alfabetica_emergent, alfabetica_fluida]`; no hi ha nivell logogràfic perquè el gènere requereix base lecto-escriptora mínima.

## Detecció

**Senyals docent** (quan adaptar a assaig):
- El text font és reflexiu o argumentatiu amb veu autorial clara (assaig acadèmic, article d'opinió d'expert, columna d'anàlisi).
- La unitat demana a l'alumne la producció d'un text argumentatiu formal sobre un tema curricular o de convivència.
- El context és Filosofia, Ciències Socials, Llengua, Batxillerat o FP.
- L'alumne té MECR A1+ i l'objectiu és treballar la HCL Argumentar en registre acadèmic.

**Senyals alumne** (que indica que necessita bastida):
- Presenta arguments però la tesi no apareix fins al final (estructura invertida).
- Usa "m'agrada / no m'agrada" sense evidència — HCL Interpretar/Valorar sense Argumentar.
- Barreja arguments de naturalesa molt diferent sense ordenar-los per grau o tipus.
- Les cites apareixen sense explicació ("Com diu Kant: [cita]. Ara parlarem de...").
- No distingeix entre l'assaig (acadèmic, reflexiu) i l'article d'opinió (personal, persuasiu).

**Context favorable**:
- Filosofia, Ètica: la tesi és sobre un concepte abstracte o dilema moral.
- Ciències Socials: assaig sobre fenòmens socials, polítics o econòmics amb dades.
- Llengua i Literatura: anàlisi d'una obra des d'una postura argumentada.
- Batxillerat i FP: text model d'un autor expert que cal analitzar i adaptar.

**Anti-senyals** (quan NO adaptar a assaig):
- El text valora una obra concreta → ressenya.
- El text narra una experiència o fets → crònica o diari.
- El text informa neutralment → notícia, manual o divulgatiu.
- El text té preàmbul anecdòtic com a ganxo → divulgatiu.
- Pre-A1: la combinació tesi + argument + evidència no és accessible sense base lecto-escriptora.

## Modulació per nivell

| Pas | Dimensió | A1<br>Inicial | A2<br>Funcional | B1<br>Estratègic | B2<br>Acadèmic | C1<br>Crític |
|---|---|---|---|---|---|---|
| **1. Tesi o postura inicial** | Claredat i explicitació | 1 frase que diu el que es defensa: "Crec que [tesi]." Al primer paràgraf. | Tesi clara de 1-2 frases amb connector d'opinió. Al primer paràgraf. | Tesi explícita que anuncia el tema i la postura. La tesi delimita l'abast de l'assaig. | Tesi matisada que reconeix la complexitat del tema sense diluir la postura. | Tesi sofisticada amb matisos conceptuals i posicionament acadèmic precís. |
| **2. Arguments** | Coherència i progressió | 1 argument simple. "Crec que... perquè...". | 2 arguments en paràgrafs separats. 1 connector causal per argument. | 3 arguments ben diferenciats. 1 per paràgraf. Connector explícit per a cada un. | 3-4 arguments jerarquitzats (del menys al més fort o a la inversa). | 3-5 arguments amb relació entre si. Pot incloure argumentació per analogia. |
| **3. Exemples i evidències** | Suport i credibilitat | 1 exemple personal o molt proper per argument. | 1 exemple concret per argument. Pot ser un fet quotidià o una observació directa. | 1 exemple o evidència per argument. Pot ser un fet, una dada o una cita breu. | 1-2 evidències per argument. Cites breus amb atribució clara. | Evidències variades (dades, cites, analogies). Jerarquitzades per credibilitat. |
| **4. Refutació o matís** | Pensament crític | Sense refutació a A1 (massa complex). Acceptable que la postura sigui unilateral. | Reconeixement d'un punt de vista diferent en 1 frase: "Alguns pensen que... però jo crec que..." | Refutació d'un argument contrari. Connector de contrast: "tot i que", "però", "tanmateix". | Refutació elaborada d'1-2 arguments contraris amb evidències de suport. | Refutació sistemàtica de les objeccions principals i integració dels matisos. |
| **5. Conclusió** | Tancament i coherència | 1 frase: "Per tot això, crec que [tesi]." No introdueix arguments nous. | Conclusió de 2 frases que reprèn la tesi. No obre noves preguntes. | Conclusió de 3 frases: resum de la postura + una implicació breu (opcional). | Conclusió argumentada que connecta la tesi amb el context més ampli. | Conclusió que sintetitza, pot obrir noves preguntes i té veu acadèmica pròpia. |
| **6. Connectors argumentatius** | Varietat i precisió | "Crec que... perquè..." (1 connector causal). | "A més", "però", "per exemple", "per tot això". Variats mínimament. | "Tanmateix", "per contra", "en conseqüència", "d'una banda... de l'altra". | Connectors argumentatius variats i precisos. Distinció entre contrast, causa i conclusió. | Connectors sofisticats. Pot usar modalitzadors i connectors concessius. |
| **7. Cites (B1+)** | Integració i atribució | Sense cites a A1. | Opcional: paràfrasi d'una idea d'algú altre sense cita formal. | 1 cita breu integrada al text amb atribució clara. Explicació de per qué importa. | 2-3 cites integrades i comentades. Cada cita suporta l'argument del paràgraf. | Múltiples cites ben atribuïdes i comentades críticament. Fonts diverses. |
| **8. Criteris transversals** | No tesi implícita | Cap obertura vaga ("Hi ha moltes opinions sobre...") sense posicionar-se. | Idem. | Idem. | Idem. | Idem. |
|  | Conclusió tancada | Cap argument nou a la conclusió que no hagi aparegut al cos del text. | Idem. | Idem. | Idem. | Idem. |
|  | Fidelitat al text font | Fidelitat a la postura principal i als arguments centrals del text font. | Fidelitat a la postura, als arguments i a les evidències essencials. | Fidelitat als arguments, a les evidències i als connectors argumentatius del text font. | Fidelitat a la complexitat argumentativa i al context disciplinar del text original. | Fidelitat a la complexitat, als matisos i als debats del text original. |
| **9. Autoavaluació metacognitiva** | Reflexió sobre el procés | "He escrit la meva opinió en una frase al principi. He donat 1 argument amb un exemple." | "He escrit la tesi al principi. He donat 2 arguments amb un exemple cadascun." | "He escrit 3 arguments, 1 per paràgraf. He reconegut un punt de vista diferent." | "He jerarquitzat els arguments i he refutat una objecció amb evidències." | "L'assaig té tesi, arguments jerarquitzats, refutació i conclusió amb veu acadèmica pròpia." |

## Metadades de cel·la (per a `build_skills.py`)

**Tipus de descriptor:**
- `countable` — llindar quantitatiu verificable mecànicament.
- `binary` — "compleix / no compleix".
- `qualitative` — requereix judici humà o LLM-jutge.
- `structural` — requereix anàlisi sintàctica o discursiva.
- `cross_source` — requereix accés al text font per comparar.
- `metacognitive` — descriptor de procés en primera persona.

| Pas / Dimensió | Tipus | requires_source_text | validation_hint |
|---|---|---|---|
| 1 Tesi — Claredat | `binary` + `qualitative` | no | binary: tesi present al 1r paràgraf (no implícita ni al final); qualitative: LLM-jutge sobre si la postura és clara i delimita l'abast |
| 2 Arguments — Coherència | `countable` + `qualitative` | no | comptar arguments; qualitative: LLM-jutge sobre si cada argument desenvolupa la tesi (no és una digressió) i té connector causal explícit |
| 3 Exemples i evidències — Suport | `binary` + `qualitative` | no | binary: exemple o evidència present per a cada argument; qualitative: LLM-jutge sobre si l'evidència és rellevant i integrada (no merament decorativa) |
| 4 Refutació — Pensament crític | `binary` + `qualitative` | no | binary: absent a A1 (correcte); qualitative: LLM-jutge sobre si la refutació respon efectivament l'objecció (A2+) |
| 5 Conclusió — Tancament | `binary` + `qualitative` | no | binary: conclusió present; qualitative: LLM-jutge sobre si reprèn la tesi sense introduir arguments nous |
| 6 Connectors argumentatius — Varietat | `structural` + `countable` | no | detectar i comptar connectors argumentatius; verificar varietat per nivell; detectar absència de connectors en paràgrafs d'argument (B1+) |
| 7 Cites — Integració | `binary` + `qualitative` | no | binary: cites presents i atribuïdes a B1+; absència a A1-A2 correcta; qualitative: LLM-jutge sobre si la cita és integrada i comentada (no inserida sola) |
| 8.1 Criteris — No tesi implícita | `binary` + `qualitative` | no | regex: detectar obertures vagues ("Hi ha moltes opinions", "Tothom sap que", "Des de sempre"); qualitative: LLM-jutge sobre si la postura de l'autor és identificable a la primera lectura |
| 8.2 Criteris — Conclusió tancada | `binary` | no | binary: detectar arguments nous a la conclusió que no apareixien al cos del text; qualitative: LLM-jutge sobre si la conclusió és síntesi o obertura |
| 8.3 Criteris — Fidelitat al text font | `cross_source` + `qualitative` | **sí** (si adaptació) | comparar postura, arguments principals i evidències original vs adaptat; LLM-jutge sobre si la simplificació preserva la coherència argumentativa |
| 9 Autoavaluació metacognitiva | `metacognitive` | no | derivar a vista d'autoavaluació alumne + registre docent |

**Notes:**
- Tesi implícita (Pas 8.1): detectable per patrons d'obertura vaga. Si la primera frase del text és una pregunta retòrica, una dada general o un preàmbul contextual sense posicionament, és candidat a tesi implícita. Un LLM-jutge verifica si el posicionament de l'autor és localitzable a l'inici.
- Arguments nous a la conclusió (Pas 8.2): parcialment automatitzable. Si la conclusió conté un connector d'addició ("a més", "també cal considerar") seguit d'una idea nova, és candidat a argument nou.
- Cites sense comentari (Pas 7): detectable per estructura. Si una cita (entre cometes o en cursiva) va seguida immediatament d'un altre paràgraf sense explicació, és una cita decorativa.

## Heurístiques docent

**H1 — La tesi en una frase.**
Demano a l'alumne: "Digues en una frase el que defenses." Si no pot fer-ho en menys de 30 segons, la tesi no és clara. El primer pas de qualsevol assaig, fins i tot a B2, és formular la tesi oralment en una frase sola. Si no pot fer-ho oralment, no podrà fer-ho per escrit.

**H2 — El títol com a brúixola (B1+).**
Proposo que l'alumne escrigui el títol ABANS de l'assaig. Un bon títol d'assaig anticipa la tesi o el conflicte central: "Per qué la intel·ligència artificial no pot substituir la creativitat humana." Si el títol no diu res específic ("Reflexió sobre la IA"), la tesi és feble.

**H3 — La cita com a font, no com a decoració (B1+).**
Per a alumnat que insereix cites però no les comenta, el model d'integració en 3 temps: (1) presento l'autor i el context, (2) cito, (3) explico per qué la cita és rellevant per a la tesi. La cita sola no parla: l'autor de l'assaig ha de parlar per ella.

**H4 — L'apartat com a argument + evidència.**
L'estructura mínima de cada paràgraf: idea → "per exemple" / "com demostra" → evidència. Si un paràgraf té idea però no evidència, queda feble. Si té evidència però no idea, és un exemple flotant. La bastida ajuda a veure si cada paràgraf té els dos elements.

**H5 — La conclusió no és un argument nou.**
Quan l'alumne escriu a la conclusió un argument nou ("i a més, caldria tenir en compte que..."), llegim la conclusió en veu alta i preguntem: "Aquesta idea ha aparegut abans?" Si no, o es retira o es puja al cos. La conclusió és síntesi, no ampliació.

## Fonts principals

- MALL (Model d'Aprenentatge de Llengües i Literacitat): HCL Argumentar, gradació BICS→CALP, integració de cites.
- Toulmin, S. (1958): *The Uses of Argument* — estructura tesi, arguments, evidències i refutació com a model universal d'argumentació.
- Cummins, J. (2000): *Language, Power and Pedagogy* — l'assaig com a gènere de CALP pur; progressió BICS→CALP.
- Camps, A. & Dolz, J. (1995): *Enseñar a argumentar* — didàctica de la seqüència argumentativa escolar.
- Decret 175/2022 (currículum Catalunya): competència en comunicació lingüística, pensament crític i plurilingüisme.
