---
modul: M3
titol: "Escriure/adaptar un informe"
tipus: genere-discursiu
categoria_principal: generes
categories_secundaries: []
descripcio: "Instrument per adaptar o generar un informe: presentació organitzada de fets, dades i conclusions sobre un tema de manera objectiva, amb separació neta entre dades i conclusions. HCL Explicar + Justificar (B1+) + Avaluar (B2+). No s'adapta a pre-A1. Rúbrica gradada 7 passos × 5 nivells MECR (A1→C1)."
mecr_range: [A1, A2, B1, B2, C1]
agent_roles: [adapter, generator]
genre_key: informe
translanguaging: false
multimodal: true
moduls_relacionats: [M3]
variables_configurables:
  fase_lectora: [alfabetica_emergent, alfabetica_fluida]
skill_meta: write-informe@corpusFJE/skills/generes/write-informe
review_status: pilot-fusio-4
version: 4.0.0-canonic
generat_at: 2026-05-26
actualitzat_at: 2026-05-26
notebooklm_review:
  data: 2026-05-26
  veredicte: si-amb-correccions-menors
  aplicades_des_d_inici: [patro-canonic-pilots-fase-a, aclariment-us-lectura-vs-produccio-C1, fidelitat-gradada-C2, variabilitat-cardinal-passos-D3]
  aplicades_post_review: [multimodal-A1-taula-bastida-visual, impersonal-B1-prioritari-sobre-passiva, resum-executiu-B1-objectiu-i-conclusio, fidelitat-C1-limitacions-biaixos]
  comentari_key: "L'informe és l'instrument del corpus que millor operacionalitza el CALP pur: la veu impersonal, la separació dades/conclusions i la hipòtesi Si/llavors son les bastides del pensament científic acadèmic."
---

# Escriure/adaptar un informe

## Descripció

L'informe presenta fets, dades i conclusions sobre un tema de manera organitzada, **objectiva** i sense opinió personal. El seu tret definitori és la **separació neta entre dades i conclusions**: primer es presenten els resultats observats, i al final s'expliciten les conclusions derivades. La veu impersonal consistent és el marcador estilístic nuclear del gènere.

**Tipologia MALL**: Expositiva/Justificativa.
**HCL principal**: Explicar — relació entre dades observades i conclusions derivades.
**HCL secundàries**: Descriure — les dades i el context (A1-B1) · Justificar — conclusions argumentades amb dades (B1+) · Avaluar — discussió de limitacions i implicacions (B2+).
**No s'adapta a pre-A1**: l'informe requereix la **distinció fets/conclusions com a operació metacognitiva** — ser capaç de reconèixer que "observar" i "concloure" son actes epistèmics diferenciats (el que he vist vs el que puc deduir del que he vist). Aquesta abstracció de segon nivell, combinada amb la veu impersonal consistent i la presentació de dades en format tècnic, no és accessible sense base lecto-escriptora i sense coneixements acadèmics mínims. (Decisió 6 canònica Fase B.)

**Connexions MALL transversals:**
- *CALP en acció*: l'informe és el gènere acadèmic per excel·lència. La veu impersonal, les dades numèriques i les conclusions argumentades son el CALP en la seva expressió més pura. Llegir un informe és accedir al discurs científic formal.
- *Separació dades/conclusions com a bastida del pensament crític*: la capacitat de dir "he observat X" (descripció objectiva) i "per tant puc concloure Y" (inferència justificada) és la competència nuclear del mètode científic. El connector "per tant" marca l'epistemologia de l'informe.
- *Hipòtesi "Si..., llavors..." com a bastida del pensament científic*: formular una hipòtesi explícita és el primer pas del mètode científic (B1+). La bastida lingüística ("Si..., llavors...") és el pont entre la pregunta de recerca i la metodologia.
- *Multimodalitat al servei de la precisió*: taules i gràfics no son decoració sinó el format natiu de les dades quantitatives. A B2+, la capacitat de llegir i interpretar representacions visuals és part de la competència científica.

**Aclariment d'ús — què descriu aquesta rúbrica.**
Aquesta rúbrica descriu l'**informe adaptat per a la LECTURA** de l'alumne. **No descriu la producció autònoma de l'alumne** — la producció és tasca d'un derivat propi. Principi pedagògic MALL: l'alumne llegeix models al màxim del seu abast.
**Sub-granularitat dins de A1**: es treballa amb `fase_lectora: [alfabetica_emergent, alfabetica_fluida]`; no hi ha nivell logogràfic perquè el gènere requereix base lecto-escriptora mínima.

## Detecció

**Senyals docent** (quan adaptar a informe):
- La unitat vol que l'alumne llegeixi els resultats d'una recerca, un experiment o una observació.
- El text font és un informe científic, un article de recerca, un informe institucional o un dossier tècnic.
- L'alumne ha de distingir el que s'ha observat del que es conclou.
- La matèria demana objectivitat i veu impersonal (Ciències Naturals, Ciències Socials, Tecnologia).

**Senyals alumne** (que indica que necessita bastida d'informe):
- Barreja dades i opinions al mateix paràgraf.
- Posa les conclusions abans de les dades.
- Usa "jo crec que..." en un text que hauria de ser objectiu.
- Les conclusions no deriven de les dades presentades.

**Context favorable**:
- Ciències Naturals: resultats d'experiments de laboratori, observacions de camp.
- Ciències Socials: resultats d'enquestes, anàlisi de dades estadístiques, estudis de cas.
- Tecnologia i Enginyeria: informes de disseny, proves de materials, prototipatge.
- Tutoria i Orientació: informes d'autoavaluació, reflexions sobre el procés d'aprenentatge (versió simplificada).

**Anti-senyals** (quan NO adaptar a informe):
- El text narra una experiència en primera persona amb implicació emocional → diari o crònica.
- El text defensa una postura → assaig o opinió.
- El text explica un fenomen de manera narrativitzada → divulgatiu.
- El text dona instruccions per fer un experiment → instructiu.
- Pre-A1: la distinció fets/conclusions com a operació metacognitiva no és accessible sense base lingüística.

## Modulació per nivell

| Pas | Dimensió | A1<br>Inicial | A2<br>Funcional | B1<br>Estratègic | B2<br>Acadèmic | C1<br>Crític |
|---|---|---|---|---|---|---|
| **1. Introducció / Resum executiu** | Orientació i síntesi | 1-2 frases que diuen de qué tracta l'informe. | Introducció de 2-3 frases: qué s'ha estudiat i per qué. | Resum executiu: 1 paràgraf que indica l'objectiu i la conclusió principal. No detalla les dades (per evitar duplicació amb el cos). | Resum executiu amb les conclusions principals davant dels resultats. | Resum executiu professional que permet comprendre l'informe sense llegir el cos complet. |
| **2. Presentació de dades** | Format i objectivitat | 3-5 dades en frases simples o llista simple (dada / valor). Nombre + unitat. Taula de 2 columnes admissible com a bastida visual. | Dades organitzades en llista o taula simple. Unitats explícites. | Dades organitzades per categories. Pot incloure comparació entre valors. | Dades en taules o gràfics simples. Descripció objectiva de les dades (sense conclusió). | Dades en formats variats (taules, gràfics, diagrames). Anàlisi estadística si escau. |
| **3. Separació dades / conclusions** | Rigor epistèmic | Dades primer ("hem vist que X"). Conclusions separades ("per tant, Y"). | Dades i conclusions en blocs separats. Connector explícit: "per tant", "com a conclusió". | Separació neta entre resultats i conclusions en seccions diferenciades. Sense barreja. | Dades comentades objectivament i conclusions argumentades per separat amb connector explícit. | Separació rigorosa. Les conclusions deriven explícitament i raonada de les dades. |
| **4. Objectivitat (veu impersonal)** | Coherència estilística | Sense frases personals ("jo crec que..."). Impersonal simple. | Veu impersonal consistent: "s'observa que", "els resultats indiquen que". | Vocabulari objectiu i tècnic. Sense adjectius subjectius. Impersonal (es + verb) prioritari; passiva opcional. | Objectivitat rigurosa. Pot incloure citació de fonts per a afirmacions. | Objectivitat acadèmica amb reconeixement de limitacions i incerteses del procés. |
| **5. Hipòtesi i metodologia** | Rigor metodològic | Sense hipòtesi (massa complex per a A1). Una descripció mínima del procediment. | Pot incloure una pregunta inicial que l'informe respon. | Hipòtesi "Si..., llavors..." explícita. Metodologia en 2-3 frases. | Hipòtesi i metodologia ben descrites. Variables identificades (independent/dependent). | Hipòtesi, variables, limitacions metodològiques i fonts en la metodologia. |
| **6. Conclusions i recomanacions** | Profunditat argumentativa | 1 conclusió simple derivada de les dades: "Hem après que..." | 1-2 conclusions derivades de les dades. Connector "per tant". | 2-3 conclusions argumentades. Pot incloure 1 recomanació derivada de les conclusions. | Conclusions argumentades + recomanacions basades en les dades. Connexió explícita dades→conclusions. | Conclusions amb discussió de les limitacions, propostes de recerca futures i reconeixement d'incerteses. |
| **7. Criteris transversals** | Opinió personal | Cap frase en primera persona singular valorativa ("jo crec", "m'agrada", "penso que"). | Idem. Passiva o impersonal en tot el text. | Idem. Les opinions es reformulen en impersonal o s'eliminen. | Idem. Pot incloure valoració de la metodologia en impersonal ("la mostra podria ser més gran"). | Les limitacions i els dubtes s'expliciten com a observació científica, no com a opinió. |
|  | Dades sense font | A A1: no cal font. | A A2: la font de les dades s'indica si és externa. | A B1+: totes les dades externes porten font atribuïda. | Idem. Les dades sense font son observacions pròpies (s'indica explícitament). | Rigor bibliogràfic complet. Diferència entre dades pròpies, dades secundàries i estimacions. |
|  | Fidelitat al text font | Fidelitat a les dades principals i a la conclusió bàsica. | Fidelitat a les dades, a la conclusió i a la separació dades/conclusions. | Fidelitat a les dades, a la metodologia, a la conclusió i al to objectiu. | Fidelitat a les dades, a la metodologia, al context i al to acadèmic. | Fidelitat a la complexitat analítica del text original, incloent limitacions i debats. |
| **8. Autoavaluació metacognitiva** | Reflexió sobre el procés | "He presentat les dades i les conclusions per separat." | "He organitzat les dades. He escrit qué hem après al final." | "He escrit la hipòtesi i la metodologia. Les conclusions deriven de les dades." | "Les meves conclusions estan argumentades amb dades. He separat dades d'opinions." | "L'informe és rigorós, objectiu i les conclusions estan justificades. He reconegut les limitacions." |

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
| 1 Introducció / Resum executiu — Orientació | `qualitative` + `binary` | no | binary: presència d'introducció; qualitative: LLM-jutge sobre síntesi i orientació per nivell |
| 2 Presentació de dades — Format | `structural` + `qualitative` | no | detectar format de les dades (llista, taula, text); LLM-jutge sobre presència d'unitats i objectivitat |
| 3 Separació dades/conclusions — Rigor | `structural` + `binary` | no | detectar barreja (conclusió dins del bloc de dades o viceversa); binary: connectors causals davant de conclusions |
| 4 Objectivitat — Veu impersonal | `binary` + `qualitative` | no | binary: detectar frases en primera persona singular valorativa (jo crec, penso que, m'agrada); qualitative: LLM-jutge sobre consistència de la veu impersonal |
| 5 Hipòtesi i metodologia — Rigor | `structural` + `qualitative` | no | binary (B1+): presència de hipòtesi en format "Si..., llavors..."; qualitative: LLM-jutge sobre adequació metodològica |
| 6 Conclusions — Profunditat | `qualitative` + `countable` | no | comptar conclusions; LLM-jutge: les conclusions deriven explícitament de les dades |
| 7.1 Criteris — Opinió personal | `binary` | no | regex: detectar "jo crec", "penso que", "m'agrada", "trobo que" al text de l'informe |
| 7.2 Criteris — Dades sense font | `binary` + `qualitative` | no | binary (B1+): dades externes sense font; qualitative: adequació de l'atribució |
| 7.3 Criteris — Fidelitat al text font | `cross_source` + `qualitative` | **sí** (si adaptació) | comparar dades principals, metodologia i conclusió original vs adaptats; a C1, verificar presència de "limitacions", "biaixos" o "incerteses" si el text font els conté |
| 8 Autoavaluació metacognitiva | `metacognitive` | no | derivar a vista d'autoavaluació alumne + registre docent |

**Notes:**
- Opinió personal (Pas 7.1) és el descriptor més automatitzable del corpus d'informe: binary pur per regex sobre patrons de primera persona singular valorativa.
- Separació dades/conclusions (Pas 3) és parcialment verificable per estructura (seccions, connectors); casos ambigus requereixen LLM-jutge.
- Hipòtesi (Pas 5): l'estructura "Si..., llavors..." és detectables per regex a B1+. L'adequació de la hipòtesi al disseny de l'informe requereix LLM-jutge.

## Heurístiques docent

**H1 — Dues columnes: "el que he observat" / "el que concloc".**
Proposo que l'alumne empleni dues columnes ABANS d'escriure. La primera columna és les dades; la segona, les conclusions. La separació visual prèvia evita la barreja al text. Especialment eficaç a A2-B1, quan la distinció dades/conclusions és el bloqueig principal.

**H2 — "Qui ho diu?" com a test d'objectivitat.**
Quan una frase té una valoració ("això és molt important", "és sorprenent que..."), pregunto: "Qui ho diu?" Si és l'alumne, cal reformular en impersonal ("els resultats mostren que...") o eliminar. Si és una font externa, cal atribuir-ho. El test funciona des de A2.

**H3 — El connector "per tant" com a marca epistèmica.**
Explico als alumnes que "per tant" és la frontissa entre les dades i les conclusions. Proposo: "Escriu totes les dades sense cap 'per tant'. Quan hagis acabat les dades, escriu 'Per tant...' i posa les conclusions." El connector explicita la relació epistèmica i en garanteix la separació.

**H4 — El resum executiu al revés.**
A B1+, proposo escriure el resum executiu DESPRÉS d'haver escrit el cos de l'informe. Quan l'alumne ha escrit tot l'informe, li pregunto: "Si hagués de llegir-lo en 30 segons, qué no es podria perdre?" La resposta és el resum executiu. Escriure'l al revés garanteix que sigui una síntesi real, no un índex de temes.

## Fonts principals

- MALL (Model d'Aprenentatge de Llengües i Literacitat): HCL Explicar + Justificar + Avaluar, CALP i discurs acadèmic.
- Cummins, J. (2000): *Language, Power and Pedagogy* — CALP i el discurs objectiu acadèmic.
- Halliday, M.A.K. i Martin, J.R. (1993): *Writing Science* — gèneres científics i la veu impersonal com a construcció ideològica del discurs científic.
- Veel, R. (1997): "Learning how to mean — scientifically speaking" a Christie, F. i Martin, J.R. (eds.) *Genre and institutions* — els gèneres de l'escriptura científica escolar.
- Decret 175/2022 (currículum Catalunya): competència científica i competència en comunicació lingüística.
