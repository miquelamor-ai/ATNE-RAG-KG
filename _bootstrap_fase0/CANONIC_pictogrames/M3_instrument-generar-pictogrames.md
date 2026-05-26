---
modul: M3
titol: "Generar pictogrames"
tipus: instrument
categoria_principal: mediacio
categories_secundaries: []
descripcio: "Instrument per afegir suport pictografic al text adaptat. Dos modes: emoji Unicode (BICS general) i ARASAAC [PICTO: terme_cat|terme_cast] (TEA, CAA, nouvingut+disciplinar). Pre-A1/A1 inline com a anticipacio; A2+ glossari visual al peu. Rubrica gradada 7 passos × 6 nivells MECR (pre-A1→C1). Multimodal obligatori. Modulacio per perfil (TEA, nouvingut, general)."
mecr_range: [pre_A1, A1, A2, B1, B2, C1] # C1: nomes per termes tecnics altament especialitzats sense representacio quotidiana
agent_roles: [generator]
complement_key: pictogrames
translanguaging: false
multimodal: true
moduls_relacionats: [M2, M3]
variables_configurables:
  fase_lectora: [logografica, alfabetica_emergent, alfabetica_fluida]
  modalitat: [emoji, arasaac]
skill_meta: generate-pictogrames@corpusFJE/skills/mediacio/generate-pictogrames
review_status: pilot-fusio-8
version: 4.0.0-canonic
generat_at: 2026-05-26
actualitzat_at: 2026-05-26
notebooklm_review:
  data: 2026-05-26
  veredicte: si-amb-correccions-menors
  aplicades_des_d_inici: [patro-canonic-pilots-fase-a, aclariment-us-lectura-vs-produccio-C1, variabilitat-cardinal-passos-D3, modulacio-per-perfil-D1]
  aplicades_post_review: [b7-picto-pas4-pas6-requires-source, b7-picto-densitat-pre-a1-unificada, b7-picto-mecr-c1-nota]
  comentari_key: "pas4+pas6-requires-source-text-si-pertinença-semantica-vs-font; densitat-pre-a1-unificada-8-10-per-text-o-1-per-frase; mecr-c1-nomes-termes-tecnics-altament-especialitzats"
---

# Generar pictogrames

## Descripció

El complement de pictogrames afegeix suport visual al text adaptat per facilitar la descodificació i l'ancoratge conceptual. Opera en dos modes segons el perfil de l'alumne: **emoji Unicode** per a BICS general i **ARASAAC** per a TEA, CAA i vocabulari disciplinar de nouvinguts. La posicio canvia radicalment per nivell: a pre-A1/A1 el pictograma va **inline** com a anticipacio; a A2+ va al **glossari visual al peu**, mai inline.

**Tipologia MALL**: Mediacio (suport augmentatiu i alternatiu de comunicacio, AAC).
**HCL associada**: cap HCL productiva — el complement suporta la descodificacio lectora sense activar producció escrita autònoma.
**Principi rector**: el pictograma és una bastida de descodificacio a pre-A1/A1, i un glossari visual de referencia a A2+. La mateixa forma serveix funcions completament diferentes.

**Dos modes — quan usar cadascun:**

| Mode | Format | Quan activar |
|---|---|---|
| **Emoji Unicode** | ☀️ 💧 🌱 (inline o glossari) | BICS general: conceptes quotidians, nouvingut A1+ sense vocabulari disciplinar, alumnat general |
| **ARASAAC** | `[PICTO: ecosistema\|ecosistema]` | TEA (sempre), CAA, nouvingut + text disciplinar (CALP), pre-A1 amb vocabulari escolar |

**Per que ARASAAC és superior per a TEA i nouvingut+disciplinar:**
- **TEA**: ARASAAC és l'estandard CAA internacional; els pictogrames son coherents, accessibles i reconeguts pels professionals de suport.
- **Nouvingut + disciplinar**: els emojis no cobreixen "ecosistema", "parlament", "evaporacio" o "fraccio". ARASAAC te ~30.000 pictogrames escolars. El terme castellà en el marcador (`[PICTO: ecosistema|ecosistema]`) actua com a pont TOLC per a nouvinguts hispanofons.
- **General**: emoji suficient per a conceptes que ja tenen representacio visual clara i universal.

**Format dels marcadors ARASAAC:**
```
[PICTO: terme_catala|terme_castella]
```
- El terme catala apareix com a etiqueta visible per a l'alumne.
- El terme castella va a la cerca ARASAAC (cobertura molt superior).
- Compatible amb format antic sense `|` (el backend usa el terme únic per a la cerca).
- Format emoji: emoji directament inline o al glossari.

**Connexions MALL transversals:**
- *Descodificacio visual com a competencia lectora emergent*: a pre-A1, el pictograma és el text per a lectors logografics o amb alfabet diferent. El pictograma i la paraula van junts perque l'alumne associa forma visual amb so i significat.
- *Paratext d'anticipacio com a activacio de coneixement previ*: mostrar el vocabulari visual ABANS de llegir activa els coneixements previs i redueix la carrega cognitiva. Principi "context before text".
- *Glossari visual A2+ com a referencia, no bastida*: a A2+, l'alumne ja pot llegir en flux continu. El glossari al peu és un recurs de consulta, com un diccionari visual. Mantenir-lo inline a A2+ introduiria soroll visual.
- *TOLC via castella (ARASAAC)*: el terme castella al marcador `[PICTO: cat|cast]` actua com a pont interlinguistic per a nouvinguts hispanofons. La imatge ARASAAC ancora el concepte catala via una llengua parcialment accessible.

**Aclariment d'us — que descriu aquesta rubrica.**
Aquesta rubrica descriu el **complement de pictogrames generat per al text adaptat**. **No descriu la produccio autonoma de l'alumne**: el complement es genera i el docent/alumne l'usa per llegir. El registre d'us és del docent (observacio de si l'alumne usa el suport visual).

**Modulacio per perfil (Decisio 1 Fase B):**
- **TEA**: mode ARASAAC sempre, densitat alta (pre-A1/A1), paratext d'anticipacio obligatori.
- **Nouvingut pre-A1/A1 + text BICS**: mode emoji, inline, vocabulari quotidia.
- **Nouvingut + text disciplinar (CALP)**: mode ARASAAC, terme castella al marcador.
- **General (sense condicio especifica)**: emoji si cal, glossari visual al peu (A2+).
- **AACC**: cap pictograma o glossari minimal — el suport visual pot distreure si l'alumne ja te fluencia lectora alta.

## Detecció

**Senyals docent** (quan activar el complement):
- Ha activat "Pictogrames" al Pas 2.
- L'alumnat destinatari és pre-A1, A1, TEA, CAA o nouvingut amb vocabulari disciplinar.
- El text te termes que l'alumne no pot visualitzar mentalment.

**Senyals alumne** (que indica que necessita el suport):
- No reconeix les paraules escrites pero pot reconèixer el referent visual.
- Es "perd" en el text per no saber per on seguir.
- Necessita suport de descodificacio sistematic per mantenir el fil.

**Context favorable**:
- Pre-A1/A1: tots els textos amb vocabulari nou.
- TEA/CAA: sempre, independentment del nivell.
- Ciencies, Historia, Geografia (B1+): per a termes disciplinars sense representacio quotidiana.

**Anti-senyals** (quan NO activar):
- El text és molt abstracte (matematiques de calcul, filosofia pura) → cap pictograma o minimal.
- L'alumne és AACC amb alta fluencia lectora → el suport visual pot distreure.
- El concepte no te representacio visual clara → millor no posar-ne cap.
- Il·lustracions tematiques contextuals → complement `illustracions`.
- Glossari textual amb definicio → complement `glossari`.

## Modulació per nivell

| Pas | Dimensió | Pre-A1 Emergent | A1 Inicial | A2 Funcional | B1 Estratègic | B2 Acadèmic | C1 Crític |
|---|---|---|---|---|---|---|---|
| **1. Mode pictograma** | Emoji vs ARASAAC | ARASAAC si TEA/CAA; emoji si nouvingut BICS. Sempre inline com a anticipacio. | ARASAAC si TEA o text disciplinar; emoji si vocabulari quotidia. Inline discret. | ARASAAC per termes disciplinars (TEA o nouvingut+CALP); emoji si BICS. Al glossari visual, mai inline. | ARASAAC per termes disciplinars especifics de la materia. Al glossari visual. | ARASAAC o emoji per termes molt tecnics sense equivalent quotidià. Glossari visual. | Rarament. Nomes si hi ha termes molt especialitzats sense representacio coneguda. |
| **2. Posicio al text** | Inline vs glossari | Inline DAVANT de la paraula: l'alumne veu el pictograma PRIMER, llavors llegeix la paraula. | Inline discret davant o al costat del terme clau. 1 pictograma per paraula nova. | Glossari visual al peu (mai inline). Llista de termes + pictograma + definicio breu. | Glossari visual al peu. Reservat per a termes disciplinars no familiars. | Glossari visual al peu. Maxim 3-4 termes realment necessaris. | Glossari visual minimal o absent. |
| **3. Densitat** | Nombre per text | 8-10 pictogrames maxim per text (maxim 1-2 per frase inline). Alta densitat justificada. | 4-6 pictogrames. 1 per paraula nova o concepte clau. | 3-5 al glossari visual. 1 per terme disciplinar. | 2-4 al glossari visual. Termes disciplinars de la materia. | 1-3 al glossari visual. Termes molt especialitzats. | 0-2. Rarament necessari. |
| **4. Especificitat del concepte** | Concret vs disciplinar | Conceptes molt concrets i universals (mode emoji) o conceptes escolars basics (mode ARASAAC). | Conceptes concrets: objectes, essers vius, accions fisiques observables. | Termes disciplinars: "volca", "cel·lula", "parlament" (si te representacio visual). | Termes disciplinars especifics de la materia sense equivalent quotidia. | Termes tecnics que beneficien d'ancoratge visual. | Termes molt especialitzats sense representacio quotidiana accessible. |
| **5. Paratext d'anticipacio** | Pre-lectura visual | Obligatori: vocabulari visual ABANS del text. Docent presenta els pictogrames oralment. Format: `### Vocabulari del text (mira primer!)` + llista pictograma·paraula. | Recomanat: presentar el vocabulari visual abans de llegir. | No cal. El glossari visual al peu és consultat durant la lectura. | No cal. | No cal. | No cal. |
| **6. Criteris transversals** | Coherencia i qualitat | Mateix pictograma per al mateix concepte en tot el document. Cap pictograma decoratiu. Cap emoji de flags o gestos ambigus. | Idem. Coherencia entre seccions. | Idem. El glossari visual no substitueix el glossari textual. | Idem. Si un terme no te representacio visual clara, millor no posar-ne. | Idem. Densitat minima: nomes els termes que realment aporten. | Idem. |
| **7. Autoavaluacio mediada** | Metacognicao | Docent observa: "L'alumne ha vist els pictogrames i ha dit el nom de cada concepte." (oral, mediat) | "He usat els pictogrames per entendre les paraules difícils." | "He usat el glossari visual al peu per recordar el significat dels termes." | "He identificat quins termes necessitaven un pictograma de referencia." | Idem. | — |

## Metadades de cel·la (per a `build_skills.py`)

**Tipus de descriptor:**
- `binary` — "compleix / no compleix".
- `qualitative` — requereix judici huma o LLM-jutge.
- `countable` — llindar quantitatiu verificable mecanicament.
- `structural` — requereix analisi sintatica o discursiva.
- `metacognitive` — descriptor de proces en primera persona.

| Pas / Dimensió | Tipus | requires_source_text | validation_hint |
|---|---|---|---|
| 1 Mode pictograma | `binary` | no | binary: format emoji (unicode) o ARASAAC (`[PICTO: ...\|...]`); verificar coherencia amb el perfil (TEA → ARASAAC obligatori; general → emoji acceptable) |
| 2 Posicio al text | `binary` | no | binary pre-A1/A1: pictogrames inline presents (regex: detectar emojis o `[PICTO:]` dins del text); binary A2+: absencia d'inline + presencia de glossari visual al peu |
| 3 Densitat | `countable` | no | comptar pictogrames totals (emojis o marcadors `[PICTO:]`); verificar que esta dins del rang per nivell |
| 4 Especificitat del concepte | `qualitative` | **si** | LLM-jutge sobre si el concepte és visualitzable i concret (positiu) o abstracte sense representacio (negatiu); cross_source: verificar que el terme triat és pertinent al vocabulari del text font |
| 5 Paratext d'anticipacio | `binary` | no | binary pre-A1: presencia de seccio de vocabulari visual abans del text (`### Vocabulari del text` o equivalent); A2+: absent (correcte) |
| 6 Criteris transversals | `binary` + `qualitative` | **si** | binary: coherencia del pictograma (mateix emoji per al mateix concepte); absencia d'emojis decoratius; qualitative: LLM-jutge sobre si els pictogrames triats son clars, universals i semanticament pertinents al text font (cross_source) |
| 7 Autoavaluacio mediada | `metacognitive` | no | pre-A1: registre docent d'observacio; A1+: derivar a vista d'autoavaluacio alumne |

**Notes:**
- Format ARASAAC: `[PICTO: terme_catala|terme_castella]`. Compatible amb format antic sense `|` (el backend usa el terme unic). El terme catala apareix com a etiqueta visible; el terme castella va a la cerca ARASAAC (cobertura superior).
- Format emoji: unicode directament al text (inline A1) o al glossari visual (A2+). Cap marcador especial — el backend no processa emojis, el LLM els insereix directament.
- Modalitat per perfil: el camp `modalitat: [emoji, arasaac]` al `variables_configurables` permet que el sistema seleccioni el mode automaticament (TEA → arasaac; general → emoji per defecte).
- Paratext d'anticipacio (Pas 5): altament recomanat a pre-A1. La sequencia pedagogica optima és: veure el pictograma → escoltar la paraula (docent) → llegir la paraula al text.

## Heurístiques docent

**H1 — El test "pots visualitzar-ho?" (seleccio del mode).**
Per a cada terme del text, pregunto: "Pots imaginar una imatge d'aquest concepte?" Si és un concepte escolar que no te emoji clar → ARASAAC. Si és un objecte quotidià amb emoji recognoscible → emoji. Si no hi ha cap representacio visual clara (la justicia, l'infinit) → millor no posar-ne cap.

**H2 — Pre-A1: pictograma DAVANT, sempre.**
La sequencia es presenta el pictograma oral i visualment ABANS que l'alumne llegeixi la paraula: veure la imatge → escoltar la paraula → llegir la paraula. No al reves. El paratext d'anticipacio és la implementacio escrita d'aquesta sequencia.

**H3 — ARASAAC per a TEA: coherencia de sistema.**
Si l'alumne amb TEA ja treballa amb un sistema de pictogrames ARASAAC amb el logoped o el/la vetllador/a, cal usar els mateixos pictogrames al text adaptat. La coherencia del sistema AAC és critica per a l'alumne amb TEA: pictogrames nous o d'un sistema diferent requereixen aprenentatge nou i poden generar confusio.

**H4 — A2+: el glossari visual és discret.**
Posar el glossari visual al peu és respectar la fluencia lectora de l'alumne A2+. L'alumne que interromp la lectura per un emoji inline perd el fil. El glossari al peu manté el flux: llegeix, para si necessita, consulta el glossari, reprèn.

**H5 — Coherencia de l'emoji com a norma de classe.**
Per a textos llargs o projectes multi-sessio, estableixo un "diccionari d'emojis" de classe: els mateixos emojis per als mateixos conceptes en tots els textos del trimestre. La coherencia entre textos reforça la memoria semantica i evita la confusio.

## Fonts principals

- MALL (Model d'Aprenentatge de Llengues i Literacitat): multimodalitat, paratext d'anticipacio, eix oral-escrit.
- ARASAAC (Aragonese Portal of Augmentative and Alternative Communication): sistema estandard de pictogrames per a CAA, TEA i educacio inclusiva.
- Mayer, R.E. (2009): *Multimedia Learning* — principi de contigüitat imatge-text; redundancia de codis visual+verbal per a la memoria.
- Cummins, J. (2001): *Negotiating Identities* — TOLC; transferencia lingüistica via L1/L2 accessible (castella → catala per a nouvinguts hispanofons).
- Decret 175/2022 (curriculum Catalunya): accessibilitat, inclusio educativa i competencia en comunicacio multimodal.
