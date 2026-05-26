---
modul: M3
titol: "Escriure/adaptar un diàleg"
tipus: genere-discursiu
categoria_principal: generes
categories_secundaries: []
descripcio: "Instrument per adaptar o generar un dialeg teatral: personatges llistats a l'inici, torns atribuïts per nom en negreta, acotacions al present en 3a persona, subtext explícit i conflicte graduat. HCL Narrar (language-in-action). No s'adapta a pre-A1. Rúbrica gradada 7 passos × 5 nivells MECR (A1→C1)."
mecr_range: [A1, A2, B1, B2, C1]
agent_roles: [adapter, generator]
genre_key: dialeg
translanguaging: false
multimodal: false
moduls_relacionats: [M3]
variables_configurables:
  fase_lectora: [alfabetica_emergent, alfabetica_fluida]
skill_meta: write-dialeg@corpusFJE/skills/generes/write-dialeg
review_status: pilot-fusio-8
version: 4.0.0-canonic
generat_at: 2026-05-26
actualitzat_at: 2026-05-26
notebooklm_review:
  data: 2026-05-26
  veredicte: si-amb-correccions-menors
  aplicades_des_d_inici: [patro-canonic-pilots-fase-a, aclariment-us-lectura-vs-produccio-C1, variabilitat-cardinal-passos-D3]
  aplicades_post_review: [b6-dialeg-fidelitat-pas6, b6-dialeg-requires-source-text-pas1+4, b6-dialeg-hint-negreta-pas2]
  comentari_key: "pas6-fidelitat-text-font-afegida; requires_source_text-si-pas1+4-cross_source; hint-negreta-obligatoria-regex"
---

# Escriure/adaptar un diàleg

## Descripció

El dialeg és un genere teatral que representa una conversa entre personatges amb estructura formal: llista de personatges, acotacions i torns de paraula clarament atribuïts per nom. El seu tret definitori és el **language-in-action**: el significat no és al text, sino a l'intercanvi entre personatges, al que es diu i al que no es diu (subtext). La seva funcio pedagogica és treballar la representacio de la interaccio social i emocional a traves del text escrit.

**Tipologia MALL**: Dialogada.
**HCL principal**: Narrar (language-in-action) — co-construir un intercanvi seqüenciat entre personatges amb tensio i resolucio.
**HCL secundaries**: Argumentar (conflicte verbal, B1+) · Interpretar/Valorar (subtext i intencio, B2+).
**Nota MALL**: el dialeg escrit és la bastida de la dramatitzacio oral. A A1, llegir els torns en veu alta amb el company és la primera produccio oral estructurada. El dialeg conecta l'eix oral (dramatitzacio) amb l'eix escrit (text formal) en un sol instrument.
**No s'adapta a pre-A1 (D6)**: el format teatral requereix llegir i atribuir torns per nom, seguir l'estructura formal de personatges i acotacions, i comprendre la relacio entre el que es diu i el que es fa (subtext). Aquesta doble cognicao (text + situacio dramatica) no és accessible sense base lectora. Per a pre-A1, millor dramatitzacio oral espontania sense format escrit.

**Connexions MALL transversals:**
- *Subtext com a pensament critic*: el subtext explícit a les acotacions fa visible la diferencia entre el que es diu i el que es pensa. És una entrada natural al pensament critic: "Que diu el personatge? Que vol dir realment?" Aquesta dualitat és la bastida del raonament interpretiu (HCL Interpretar/Valorar, B2+).
- *Atribucio com a responsabilitat discursiva*: aprendre a atribuir torns per nom (no per lletra) és aprendre a fer-se responsable de les paraules propies i alienes. La norma de l'atribucio por nom és una norma de claredad i de respecte.
- *Dramatitzacio com a mediacio*: el dialeg escrit és la bastida de la dramatitzacio oral. A A1, llegir els torns en veu alta per parelles és la primera produccio oral estructurada en la llengua nova (TILC).

**Aclariment d'us — que descriu aquesta rubrica.**
Aquesta rubrica descriu el **dialeg adaptat per a la LECTURA** de l'alumne. **No descriu la produccio autonoma** — la produccio és tasca d'un derivat propi. Principi pedagogic MALL: l'alumne llegeix models al maxim del seu abast.
**Sub-granularitat dins de A1**: es treballa amb `fase_lectora: [alfabetica_emergent, alfabetica_fluida]`; no hi ha nivell logografic perque el genere requereix llegir i atribuir torns.

## Detecció

**Senyals docent** (quan adaptar a dialeg):
- El text font és un dialeg o una escena teatral.
- La unitat vol treballar la interaccio oral o la dramatitzacio escrita.
- L'alumne ha de produir un dialeg com a tasca d'expressio dramatica o creativa.
- El docent vol treballar la distincio entre el que es diu i el que es pensa (subtext, pensament critic).

**Senyals alumne** (que indica que necessita bastida):
- Escriu dialeg "flotant" sense atribuir qui parla.
- Barreja acotacio i torn de paraula en el mateix text.
- No inclou conflicte: el dialeg és una conversa sense tensio.
- Usa inicials (A:, B:) en lloc del nom del personatge.

**Context favorable**:
- Llengua i literatura (dramatitzacio, text teatral, expressio oral).
- Tutoria (dialegs sobre situacions de convivencia o resolucio de conflictes).
- Ciencies Socials (representacio de dialegs historics o politics, B2+).
- Totes les materies: el dialeg permet treballar continguts a traves del format teatral.

**Anti-senyals** (quan NO adaptar a dialeg):
- El text font és narratiu sense intercanvi dialogat → conte o cronica.
- El text vol transmetre informacio de manera sistematica → informe o divulgatiu.
- El text és un monolog interior llarg → diari personal.
- El text vol expressar una opinio argumentada sense intercanvi → assaig.

## Modulació per nivell

| Pas | Dimensió | A1 Inicial | A2 Funcional | B1 Estratègic | B2 Acadèmic | C1 Crític |
|---|---|---|---|---|---|---|
| **1. Llista de personatges** | Presentació | 2 personatges llistats amb nom. Sense descripcio. | 2 personatges amb 1 linia de descripcio cadascun. | 2-3 personatges amb descripcio i relacio entre ells. | 3-4 personatges amb tret diferenciador i funcio en el conflicte. | 3-4 personatges amb motivacio i postura explícites. |
| **2. Atribucio de torns** | Claredat formal | Torns atribuïts per nom en negreta: **Marc:** / **Sofia:**. Mai amb inicials o lletres (A:, B:). | Torns atribuïts per nom en negreta. Format consistent al llarg del dialeg. | Torns atribuïts per nom. L'atribucio mai és ambigua (cap torn "flotant"). | Torns atribuïts amb nom + acotacio breu si la veu pot confondre's. | Torns atribuïts per nom. La veu de cada personatge és diferenciada lingüísticament. |
| **3. Acotacions** | Subtext i accio | Acotacio molt simple: "En Marc entra." / "La Sofia somriu." Present, 3a persona. 1 accio. | 1 accio per acotacio, sense subordinades. Present, 3a persona. Subtext explícit senzill. | Acotacio amb subtext emocional explícit: "[La Sofia fa un pas enrere, preocupada.]" | Acotacions que revelen intencions no dites. 1 accio per acotacio. | Acotacions detallades amb subtext complex. Sense ironia ni judicis sobre el personatge. |
| **4. Conflicte** | Tensio dramatica | Tensio simple en 1 torn: "Vull X. — No pots." | Conflicte simple i resolucio clara en 6-8 torns. | Conflicte amb 2 punts de vista diferenciats. Inclou 1 moment d'argumentacio. | Conflicte complex amb postures elaborades per cada personatge. | Conflicte de valors o de visions del mon. Resolucio no necessariament clara. |
| **5. Nombre de torns** | Extensio | 6-8 torns totals. 1-2 frases per torn. | 8-10 torns. Frases fins a 10 paraules per torn. | 10-12 torns. Frases de fins a 15 paraules per torn. | 12-15 torns. Frases elaborades. | 12-15+ torns. Llargada variable segons el ritme dramatic. |
| **6. Criteris transversals** | Format i fidelitat | Llista de personatges present al principi. Cap torn amb inicials. Cap acotacio amb ironia. Manté personatges i conflicte principals del text font. | Idem. Subtext explícit a les acotacions. La resolucio del conflicte és clara. Manté l'ordre i la resolucio del text font. | Idem. Les acotacions no confonen accio amb judici. Manté els punts de vista dels personatges del text font. | Idem. Manté matisos i complexitat del conflicte original. L'acotacio pot contradir o matisar el torn si escau. | Idem. Manté intencio retorica i matisos del text font. Sense monolegs interns llargs. |
| **7. Autoavaluacio** | Metacognicao | "He escrit qui parla a cada torn. He posat 6-8 torns entre 2 personatges." | "He posat acotacions que expliquen el que fa el personatge." | "He escrit un conflicte i una resolucio. He explicat el subtext a les acotacions." | "He escrit torns que mostren les postures dels personatges sense explicar-les totes." | "He creat un conflicte complex amb subtext ric i intencio retorica visible." |

## Metadades de cel·la (per a `build_skills.py`)

**Tipus de descriptor:**
- `countable` — llindar quantitatiu verificable mecanicament.
- `binary` — "compleix / no compleix".
- `qualitative` — requereix judici huma o LLM-jutge.
- `structural` — requereix analisi sintatica o discursiva.
- `metacognitive` — descriptor de proces en primera persona.

| Pas / Dimensió | Tipus | requires_source_text | validation_hint |
|---|---|---|---|
| 1 Llista de personatges | `binary` + `qualitative` | **si** | binary: llista de personatges present al principi del text; qualitative: LLM-jutge sobre si els personatges son els mateixos que al text font (cross_source) i si la descripcio és adequada al nivell |
| 2 Atribucio de torns | `binary` | no | binary: tots els torns atribuïts per nom en negreta (regex detecta inicials A:, B: i torns sense atribucio); la negreta és obligatoria per a la detecci?o estructural automatitzada |
| 3 Acotacions | `binary` + `qualitative` | no | binary: acotacions al present 3a persona; 1 accio per acotacio; qualitative: LLM-jutge sobre si el subtext és explícit i adequat al nivell (A1 sense subtext; A2+ amb subtext) |
| 4 Conflicte | `qualitative` | **si** | LLM-jutge sobre si hi ha tensio dramatica i si la resolucio és adequada al nivell (A1 simple i clara; B2+ complexa i oberta); cross_source: verificar que el conflicte del text adaptat no inventa situacions alienes al text font |
| 5 Nombre de torns | `countable` | no | comptar torns totals i paraules per torn; verificar que esta dins del rang del nivell |
| 6 Criteris transversals | `binary` + `qualitative` | no | binary: llista de personatges present; cap inicial; cap monolog llarg; qualitative: LLM-jutge sobre coherencia del format |
| 7 Autoavaluacio | `metacognitive` | no | derivar a vista d'autoavaluacio alumne + registre docent |

**Notes:**
- L'atribucio de torns per nom (Pas 2) és el criteri mes automatitzable i el mes crític pedagogicament: un dialeg sense atribucio clara no és llegible. Regex detecta inicials (A:, B:) o torns sense atribucio.
- Subtext (Pas 3): parcialment automatitzable. Detectar presencia d'acotacions. Qualitat del subtext requereix LLM-jutge.
- Conflicte (Pas 4): no automatitzable. Requereix comprensio de la tensi?o narrativa — LLM-jutge.

## Heurístiques docent

**H1 — Llegir en veu alta com a primer pas.**
Proposo que llegim el dialeg adaptat en veu alta per parelles: un fa el personatge A, l'altre el B. La lectura dramatitzada revela immediatament si els torns son clars, si les acotacions aporten o estorben, i si el conflicte és real o nomes un intercanvi de frases.

**H2 — "Que vols dir realment?" per treballar el subtext.**
Quan l'alumne escriu un torn, li pregunto: "El personatge diu X, pero que vol dir realment?" La resposta va a l'acotacio. Aquest exercici de desdoblament és la bastida del pensament critic literari: distingir el que es diu del que es pensa.

**H3 — Conflicte minim obligatori.**
Un dialeg sense conflicte és una conversa, no un drama. Insisteixo que hi hagi com a minim un punt de desacord o de tensio. A A1: "Vull X. — No pots." és la bastida minima. Sense tensio, el dialeg no té dinamica narrativa.

**H4 — 1 accio per acotacio.**
Les acotacions amb subordinades confonen. Proposo la regla d'1 accio per acotacio: "En Marc entra." (no "En Marc entra i, tot i que sembla content, en realitat esta enfadat"). Si hi ha dues accions, dues acotacions.

**H5 — Llistar els personatges abans d'escriure.**
Proposo que l'alumne escrigui primer la llista de personatges amb una linia de descripcio cadascun. Aquesta llista es converteix en el mapa del dialeg: qui és cada personatge, que vol, i per que esta en conflicte amb l'altre.

## Fonts principals

- MALL (Model d'Aprenentatge de Llengues i Literacitat): HCL Narrar (language-in-action), eix oral-escrit, dramatitzacio com a mediacio.
- Bruner, J. (1990): *Acts of Meaning* — narrative mode of thought; el dialeg com a forma de negociar significats socialment.
- Stanislavski, C. (1936): *An Actor Prepares* — subtext com a la vida interior del personatge; motor de la dramatitzacio.
- Decret 175/2022 (curriculum Catalunya): comunicacio oral, dramatitzacio i expressio creativa.
