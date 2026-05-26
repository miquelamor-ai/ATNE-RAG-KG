---
modul: M3
titol: "Escriure/adaptar una fàbula"
tipus: genere-discursiu
categoria_principal: generes
categories_secundaries: []
descripcio: "Instrument per adaptar o generar una fàbula: narració breu amb personatges arquetípics i moral explícita al final. HCL Narrar + Interpretar/Valorar. No s'adapta a pre-A1. Rúbrica gradada 7 passos × 5 nivells MECR (A1→C1)."
mecr_range: [A1, A2, B1, B2, C1]
agent_roles: [adapter, generator]
genre_key: fabula
translanguaging: false
multimodal: true
moduls_relacionats: [M3]
variables_configurables:
  fase_lectora: [alfabetica_emergent, alfabetica_fluida]
skill_meta: write-fabula@corpusFJE/skills/generes/write-fabula
review_status: pilot-fusio-3
version: 4.0.0-canonic
generat_at: 2026-05-26
actualitzat_at: 2026-05-26
notebooklm_review:
  data: 2026-05-26
  veredicte: si-amb-correccions-menors
  aplicades_des_d_inici: [patro-canonic-pilots-fase-a, aclariment-us-lectura-vs-produccio-C1, fidelitat-gradada-C2, variabilitat-cardinal-passos-D3]
  aplicades_post_review: [multimodal-true-suport-visual-arquetips-A1-A2, llengua-registre-C1-arcaisme-estilistic-admissible]
  comentari_key: "El pilot de fàbula és l'instrument del corpus que millor operacionalitza el pas de la HCL Narrar a la HCL Valorar mitjançant l'estructura rígida de la moral explícita."
---

# Escriure/adaptar una fàbula

## Descripció

La fàbula és una narració breu amb personatges arquetípics (animals o éssers personificats) que il·lustren un conflicte moral i el resolen amb una lliçó explícita: la **moral**. El seu tret definitori és la doble estructura: la narració superficial (la historia dels personatges) i la lliçó profunda (la moral, que s'extreu explícitament al final). A diferència del conte, la fàbula té una funció prescriptiva: ensenya com s'ha d'actuar.

**Tipologia MALL**: Narrativa (imaginar — il·lustrar un principi moral via ficció).
**HCL principal**: Narrar — seqüenciar una acció amb personatges arquetípics que il·lustren una tensió moral.
**HCL secundàries**: Interpretar/Valorar — la moral és HCL explícita des de A2 · Argumentar — justificar la moral amb el text, B2+.
**No s'adapta a pre-A1**: la fàbula requereix comprendre dos plans simultanis — la narració superficial i la lliçó moral — i entendre que els personatges *representen* arquetips humans, no que *són* animals. Aquesta abstracció de segon nivell (símbol + inferència) no és accessible a la fase logogràfica/emergent, on el significat es construeix per via visual i concreta. (Decisió 6 canònica Fase B.)

**Connexions MALL transversals:**
- *Arquetip com a bastida transcultural*: els personatges arquetípics (el ràpid i descuidat, el llest i orgullós, l'humil i treballador) son esquemes cognitius universals. L'alumne nouvingut els reconeix fins i tot sense conèixer la tradició literària local perquè els arquetips son transculturals. No cal translanguaging: l'analogia s'activa per les accions del personatge, no per la traducció.
- *Moral com a transició Narrar → Valorar*: escriure la moral és el pas de contar el que ha passat a dir el que significa. Aquesta transició és el nucli de la competència MALL de valoració i el primer pont cap a l'argumentació (B2+).
- *Eix oral/escrit*: la fàbula es presta a la lectura dramatitzada (A1-A2) per activar la percepció dels arquetips abans de la lectura autònoma.

**Aclariment d'ús — què descriu aquesta rúbrica.**
Aquesta rúbrica descriu la **fàbula adaptada per a la LECTURA** de l'alumne (el que el docent presenta perquè l'alumne llegeixi). **No descriu la producció autònoma de l'alumne** — la producció és tasca d'un derivat propi. Principi pedagògic MALL: l'alumne llegeix models al màxim del seu abast i en produeix els seus textos; l'adaptació és tasca del docent.
**Sub-granularitat dins de A1**: es treballa amb `fase_lectora: [alfabetica_emergent, alfabetica_fluida]`; no hi ha nivell logografic perquè la fàbula requereix base lecto-escriptora mínima.

## Detecció

**Senyals docent** (quan adaptar a gènere fàbula):
- El text font és una fàbula (Esop, La Fontaine, Samaniego, fàbules africanes o asiàtiques).
- La unitat treballa la dimensió ètica, la convivència o els valors.
- L'alumne ha de llegir un text que il·lustra un principi moral.
- L'objectiu inclou la producció d'una fàbula com a tasca d'expressió escrita.

**Senyals alumne** (que indica que necessita bastida):
- Escriu la historia però oblida la moral al final.
- La moral és implícita ("ja s'entén qué vol dir").
- El personatge canvia de caràcter sense justificació durant la narració.
- La historia no il·lustra la moral que escriu (desconnexió historia-moral).

**Context favorable**:
- Tutoria (valors, convivència, mediació de conflictes).
- Llengua i literatura en unitats de narración moral.
- Ètica i filosofia: introducció als dilemes morals simples (A2-B1).
- Ciències socials: justícia, equitat, treball col·laboratiu.

**Anti-senyals** (quan NO adaptar a fàbula):
- El text de ficció no té una dimensió moral clara → conte.
- El text defensa una postura amb arguments → assaig o opinió.
- El text informa sobre animals sense personificar-los → divulgatiu.
- L'alumne és pre-A1: la relació historia-moral requereix abstracció inaccessible sense base lingüística.

## Modulació per nivell

| Pas | Dimensió | A1<br>Inicial | A2<br>Funcional | B1<br>Estratègic | B2<br>Acadèmic | C1+<br>Crític |
|---|---|---|---|---|---|---|
| **1. Personatges arquetípics** | Nombre i definició | 2 personatges amb un tret únic cadascun (ràpid/lent, llest/ingenu). Noms genèrics ("La llebre", "La tortuga"). | 2 personatges arquetípics ben definits des del primer paràgraf. Tret únic explícit al text. | 2-3 personatges amb tret únic consistent durant tota la fàbula. El tret s'anuncia al principi. | 3-4 personatges amb trets complementaris o oposats. Les relacions entre trets generen el conflicte. | Personatges amb complexitat arquetípica. El tret pot tenir matisos sense trencar l'arquetip ni la moral. |
| **2. Caràcter mantingut** | Consistència | El personatge ràpid és ràpid de principi a fi. Cap canvi de caràcter. | Caràcter consistent en tots els actes del personatge. | Caràcter mantingut fins al desenllaç. El desenllaç deriva directament del caràcter. | Caràcter consistent. Pot incloure un moment d'auto-engany del personatge (mantenir el tret fins a les últimes conseqüències). | Arquetip consistent però amb matisos que enriqueixen la moral sense contradir-la. |
| **3. Situació i fet desencadenant** | Context i tensió | Situació en 1-2 frases. Incident simple que posa la narració en moviment. | Situació + fet desencadenant diferenciats en paràgrafs o frases separades. El fet crea una tensió senzilla. | Situació amb context del tret dels personatges + fet que posa el tret a prova. | Situació ben construïda que prepara el conflicte moral. Context suficient per comprendre els trets. | Situació elaborada que posa en tensió valors o concepcions del món. El conflicte moral és evident des del principi. |
| **4. Acció i desenllaç** | Causalitat i coherència | Acció en 1-2 frases. Desenllaç clar i directe. Conseqüència evident del tret del personatge. | Acció narrada amb connectors temporals simples. Desenllaç coherent amb el caràcter. | Acció amb causa-efecte explícit. Desenllaç que deriva directament i de forma inequívoca del caràcter. | Acció amb tensió creixent. Desenllaç que justifica plenament la moral, no pot ser d'una altra manera. | Acció elaborada. Desenllaç que pot tenir ironia lleugera si la moral ho suporta i s'explicita. |
| **5. Moral explícita** | Format i universalitat | 1 frase curta. Sempre precedida de "Moral:". Universal: aplicable fora de la historia. | 1-2 frases. Precedida de "Moral:". Aplicable a situacions reals que l'alumne pot reconèixer. | 2 frases. Explícita, universal i ben argumentada. El lector no ha d'inferir-la. | Explícita. Connecta la historia amb un principi general aplicable fora del context concret. | Explícita però no simplista. Pot plantejar una tensió entre valors o un dilema, però mai implícita. |
| **6. Criteris transversals** | Llargada | 6-8 frases totals. Moral d'1 frase. | 8-12 frases. Moral d'1-2 frases. | 3-4 paràgrafs + moral. | 3-4 paràgrafs ben diferenciats + moral (2 frases). | Fàbula completa amb riquesa descriptiva + moral elaborada (fins a 3 frases). |
|  | Llengua i registre | Sense fórmules arcaiques ("En un llunyà temps..."). Llengua actual. Passat simple. | Idem. Sense temps verbals arcaics. | Idem. Registre literari simple admissible sense arcaisme. | Idem. Recursos expressius admissibles si no son arcaics. | Sense arcaismes que dificultin la comprensió. Usos estilístics conscients (pastitx literari) admissibles si no comprometen la claredat. |
|  | Fidelitat al text font | Fidelitat a la moral original i als arquetips. L'acció pot simplificar-se. | Fidelitat a la moral i als personatges arquetípics. | Fidelitat a la moral, als arquetips i a la tensió moral del text original. | Fidelitat a la moral, als arquetips i al to del text original. | Fidelitat a la moral, als arquetips, al to i a la intenció del text original. |
| **7. Autoavaluació metacognitiva** | Reflexió sobre el procés | "He escrit 2 personatges amb un tret diferent cadascun. He escrit la moral al final i comença amb 'Moral:'." | "La historia dels meus personatges mostra per qué la moral és certa. He revisat que la moral sigui una lliçó aplicable fora de la historia." | "El caràcter del personatge no canvia durant la historia. La moral explica una lliçó aplicable a la vida." | "La historia té tensió i el desenllaç és una conseqüència lògica del caràcter dels personatges. He revisat que la moral no sigui massa específica." | "La meva fàbula planteja una complexitat moral i la moral no és simplista, però és explícita. He revisat que l'arquetip sigui consistent tot i tenir matisos." |

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
| 1 Personatges arquetípics — Nombre i definició | `countable` + `qualitative` | no | comptar personatges; LLM-jutge: verificar que cada personatge té un tret únic identificable explícitament al text |
| 2 Caràcter mantingut — Consistència | `binary` + `qualitative` | no | LLM-jutge: traçar el comportament de cada personatge en cada acte; detectar canvi injustificat de caràcter |
| 3 Situació i fet desencadenant — Context i tensió | `structural` + `qualitative` | no | verificar diferenciació situació/fet; LLM-jutge: el fet posa a prova el tret del personatge |
| 4 Acció i desenllaç — Causalitat i coherència | `qualitative` | no | LLM-jutge: coherència desenllaç-caràcter; detectar desenllaç arbitrari o no derivat del tret |
| 5 Moral explícita — Format i universalitat | `binary` + `qualitative` | no | binary: presència de "Moral:" al text (regex); qualitative: LLM-jutge — la moral és universal i no específica de la historia |
| 6.1 Criteris — Llargada | `countable` | no | comptar frases o paràgrafs totals; verificar llindar per nivell |
| 6.2 Criteris — Llengua i registre | `qualitative` | no | LLM-jutge: detectar fórmules arcaiques ("En un llunyà temps", subjuntiu arcaic, vocabulari obsolet) |
| 6.3 Criteris — Fidelitat al text font | `cross_source` | **sí** (si adaptació) | comparar moral original vs moral adaptada i arquetips conservats; no aplica en mode generator |
| 7 Autoavaluació metacognitiva | `metacognitive` | no | derivar a vista d'autoavaluació alumne + registre docent |

**Notes:**
- Moral (Pas 5): presència de "Moral:" és `binary` pur per regex — el descriptor más automatitzable del corpus.
- Caràcter mantingut (Pas 2): el descriptor màss exigent; requereix traçar el comportament del personatge al llarg de tot el text.
- La fàbula té menys `qualitative` que el conte per l'estructura rígida: Pas 1 i Pas 6.1 son parcialment automatitzables.

## Heurístiques docent

**H1 — Primer la moral, després la historia.**
Proposo que l'alumne comenci per escriure la moral ("Moral: qui treballa i estalvia, no passa necessitat") i llavors inventi la historia que la il·lustra. Construir de cap al revés evita el problema de les morals que no encaixen amb la historia. Funciona especialment bé a A2-B1, on la connexió historia-moral és el bloqueig principal.

**H2 — Els arquetips com a plantilla.**
Offer una llista d'arquetips oposats: ràpid/lent · llest/ingenu · golafre/generós · orgullós/humil · impacient/constant. L'alumne tria un parell d'oposats i inventa la situació que els enfronta. Amb dos trets oposats, el conflicte s'escriu sol perquè els personatges actuen de manera previsible i consistent.

**H3 — El test del caràcter consistent.**
Quan l'alumne ha acabat la fàbula, li demano que rellegeixi i marqui tots els moments on cada personatge pren una decisió o fa una acció. Per a cada marca li pregunto: "El personatge A actua d'acord amb el seu tret únic?" Si en algun moment actua de manera diferent sense justificació, cal revisar aquell punt. El caràcter arquetípic no permet excepcions.

**H4 — El test de la moral universal.**
La moral d'una fàbula ha de funcionar fora de la historia. Proposo el test: "Podries usar aquesta moral per explicar una situació real de la teva vida, de la classe o del món?" Si sí, la moral és prou universal. Si la resposta és "només si tens una tortuga i una llebre", és massa específica de la historia i cal reformular-la com a principi general.

## Fonts principals

- MALL (Model d'Aprenentatge de Llengües i Literacitat): HCL Narrar + Interpretar/Valorar, gradació MECR.
- Esop (s. VI aC) i La Fontaine (1668): tradició canònica de la fàbula occidental; models de referència per a la gradació arquetípica.
- Bruner, J. (1990): *Acts of Meaning* — la narració com a vehicle de transmissió de valors i normes culturals; base del paper prescriptiu de la fàbula.
- Decret 175/2022 (currículum Catalunya): competència en comunicació lingüística (dimensió literària) i competència ètica i ciutadana.
