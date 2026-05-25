---
modul: M3
titol: "Escriure/adaptar un text divulgatiu"
tipus: instrument
categoria_principal: generes
categories_secundaries: []
descripcio: "Instrument per adaptar o generar un text divulgatiu: explicació narrativitzada d'un fenomen científic o tècnic per a un públic no especialitzat. HCL Explicar (causa-efecte accessible) + Justificar (B2+). No s'adapta a pre-A1. Rúbrica gradada 8 passos × 5 nivells MECR (A1→C1)."
mecr_range: [A1, A2, B1, B2, C1]
agent_roles: [adapter, generator]
genre_key: divulgatiu
translanguaging: false
multimodal: false
moduls_relacionats: [M3]
variables_configurables:
  fase_lectora: [alfabetica_emergent, alfabetica_fluida]
skill_meta: write-divulgatiu@corpusFJE/skills/generes/write-divulgatiu
review_status: pilot-fusio-4
version: 4.0.0-canonic
generat_at: 2026-05-26
actualitzat_at: 2026-05-26
notebooklm_review:
  data: 2026-05-26
  veredicte: si-amb-correccions-menors
  aplicades_des_d_inici: [patro-canonic-pilots-fase-a, aclariment-us-lectura-vs-produccio-C1, fidelitat-gradada-C2, variabilitat-cardinal-passos-D3]
  aplicades_post_review: [cardinal-8-passos-frontmatter, llargada-A1-2-3-paragrafs, autoavaluacio-A1-ajustada]
  comentari_key: "El text divulgatiu és l'instrument del corpus que millor operacionalitza el pont BICS→CALP mitjançant la narrativització de la causalitat científica."
---

# Escriure/adaptar un text divulgatiu

## Descripció

El text divulgatiu explica continguts científics o tècnics de manera **narrativitzada** i accessible per a un públic no especialitzat. El seu tret definitori és la **narrativització**: el contingut no es llista com a fets separats, sinó que es construeix com una historia amb causa, efecte i implicació. L'entradeta captadora (pregunta o xifra sorprenent) és la porta d'entrada al gènere.

**Tipologia MALL**: Expositiva.
**HCL principal**: Explicar — construir la relació causa-efecte d'un fenomen de manera accessible i narrativitzada.
**HCL secundàries**: Descriure — context i situació (A1-A2) · Justificar — evidències científiques atribuïdes a fonts (B2+).
**No s'adapta a pre-A1**: el text divulgatiu requereix comprendre la **narrativització d'un fenomen com a abstracció explicativa** — no enumerar fets sinó construir-ne la causalitat i la implicació. La transició BICS→CALP que és el nucli pedagògic del gènere no és accessible sense base lingüística mínima: l'alumne ha d'entendre que "per tant" i "com a conseqüència" senyalen una relació d'idees, no una successió de fets. (Decisió 6 canònica Fase B.)

**Connexions MALL transversals:**
- *Narrativització com a pont BICS→CALP*: el divulgatiu és el gènere que millor fa la transició del coneixement quotidià (BICS) al coneixement acadèmic (CALP). Narrativitzar un fenomen científic significa construir-ne la historia: per què passa, com passa, quines conseqüències té. Sense narrativització, la llista de fets no construeix comprensió.
- *Entradeta com a motivació i bastida*: la pregunta o xifra inicial activa el coneixement previ de l'alumne i crea expectativa. A A1-A2, l'entradeta és la bastida que dona context sense pressuposen coneixements tècnics.
- *Cita com a model de pensament científic*: atribuir una idea a un expert ensenya a diferenciar informació de font, principi bàsic del pensament crític (B1+).

**Aclariment d'ús — què descriu aquesta rúbrica.**
Aquesta rúbrica descriu el **text divulgatiu adaptat per a la LECTURA** de l'alumne. **No descriu la producció autònoma de l'alumne** — la producció és tasca d'un derivat propi. Principi pedagògic MALL: l'alumne llegeix models al màxim del seu abast.
**Sub-granularitat dins de A1**: es treballa amb `fase_lectora: [alfabetica_emergent, alfabetica_fluida]`; no hi ha nivell logogràfic perquè el gènere requereix base lecto-escriptora mínima.

## Detecció

**Senyals docent** (quan adaptar a text divulgatiu):
- El text font és un article de revista científica, de divulgació (National Geographic, SuperSaber, Muy Interesante) o un reportatge temàtic.
- La unitat de Ciències Naturals, Ciències Socials, Tecnologia o Salut treballa un fenomen que cal explicar de manera accessible.
- L'alumne ha de llegir per comprendre com funciona un fenomen (no per memoritzar una llista de fets).
- La matèria demana que l'alumne pugui explicar el fenomen a un altre alumne amb les seves pròpies paraules.

**Senyals alumne** (que indica que necessita bastida divulgativa):
- Llegeix el text però no extreu la idea principal; reté dades sueltes sense relació causal.
- No distingeix exemples d'afirmacions principals.
- En la producció, llista fets sense narrativitzar ("Primer passa X. Després passa Y. Finalment passa Z." sense connectar-los causalment).
- Usa tecnicismes sense explicar-los, o els evita per por.

**Context favorable**:
- Ciències Naturals i Tecnologia: fenòmens físics, biològics, químics o tecnològics.
- Ciències Socials: processos econòmics, geogràfics o socials explicats de manera accessible.
- Salut i Medi Ambient: temes de salut pública, canvi climàtic, biodiversitat.
- Alumnat nouvingut A1-A2: l'entradeta captadora dona context sense pressuposen coneixements culturals locals.

**Anti-senyals** (quan NO adaptar a divulgatiu):
- El text narra una historia de ficció o real → conte o biografia.
- El text defensa una postura amb arguments → assaig o opinió.
- El text enumera característiques d'un objecte o persona → descripció.
- El text dona instruccions per fer alguna cosa → instructiu o receptari.
- Pre-A1: la comprensió causal abstracta no és accessible sense base lingüística.

## Modulació per nivell

| Pas | Dimensió | A1<br>Inicial | A2<br>Funcional | B1<br>Estratègic | B2<br>Acadèmic | C1<br>Crític |
|---|---|---|---|---|---|---|
| **1. Títol captador** | Claredat i captació | Títol clar i directe. Diu el tema sense metàfores. | Títol informatiu i lleugerament captador. Sense metàfores obscures. | Títol captador (pregunta o xifra sorprenent). Clar i directe. | Títol captador i precís. Pot tenir un subratllat temàtic. | Títol complex i suggeridor. Pot ser provocatiu però no obscur. |
| **2. Entradeta (ganxo)** | Motivació i context | 1 frase que anuncia el tema. | 2 frases: ganxo inicial (pregunta o dada) + anunci del tema. | Entradeta clara que crea expectativa sense revelar tot el contingut. | Entradeta elaborada que contextualitza el fenomen i capta l'atenció. | Entradeta sofisticada que situa el tema en un context ampli i crea intriga. |
| **3. Narrativització del contingut** | Causa-efecte i coherència | 2-3 paràgrafs molt curts. Un fet explicat com a procés (no llista de fets). | 3-4 paràgrafs narrativitzats. No llista de fets. Exemple per paràgraf. | 4-5 paràgrafs. El contingut s'explica com una historia (causa → efecte → implicació). | Narrativització elaborada. Cada paràgraf avança la comprensió del fenomen. | Text narrativitzat complet. Pot incloure controvèrsies científiques presentades de forma accessible. |
| **4. Xifres arrodonides** | Accessibilitat i context | Xifres molt simples i arrodonides: "uns quants milers". | Xifres arrodonides i contextualitzades: "gairebé dos milions". | Xifres arrodonides amb comparació: "més de dos milions, una xifra equivalent a...". | Xifres precises amb font i comparació contextualitzada. | Xifres amb anàlisi crítica de la seva significació estadística. |
| **5. Cites i atribució** | Credibilitat i font | Sense cites (massa complex per a A1). | 1 cita màxim, atribució simple: "diu la científica X". | 1-2 cites breus. Atribució clara: "com explica la doctora X, investigadora de...". | 2-3 cites ben atribuïdes. Contrast de perspectives si escau. | Múltiples fonts ben atribuïdes. Pot incloure controvèrsia científica sobre el fenomen. |
| **6. Exemples concrets** | Accessibilitat i connexió | 1 exemple per paràgraf, pres del context immediat de l'alumne. | 1 exemple concret i quotidià per paràgraf. Accessible per a l'alumne. | Exemples concrets i variats. Connectats al text, no digressius. | Exemples concrets amb connexió explícita amb el concepte que il·lustren. | Exemples variats, alguns trets de contexts no quotidians. |
| **7. Criteris transversals** | Tecnicismes | Sense tecnicismes o amb explicació immediata entre parèntesis. | Tecnicismes en negreta + explicació breu integrada al text. | Tecnicismes amb explicació contextualitzada (no glossari extern). | Tecnicismes amb precisió disciplinar. Explicació en primera menció. | Terminologia completa. Pot assumir coneixements previs en la primera menció. |
|  | Llargada | 2-3 paràgrafs molt curts (2-3 frases cadascun) + entradeta (1 frase). | 4-5 paràgrafs curts + entradeta. | 5-6 paràgrafs + entradeta + tancament. | 6-7 paràgrafs ben estructurats. | Text complet amb tots els elements del gènere. |
|  | Fidelitat al text font | Fidelitat al fenomen principal i a la relació causal bàsica. | Fidelitat al fenomen, a la relació causal i a l'entradeta captadora. | Fidelitat al fenomen, a la relació causal i al to divulgatiu del text original. | Fidelitat al fenomen, a les dades, al context i al to. | Fidelitat a la complexitat causal del text original, incloent matisos i controvèrsies. |
| **8. Autoavaluació metacognitiva** | Reflexió sobre el procés | "He escrit un títol clar i una frase d'introducció. He explicat el tema en 2-3 paràgrafs curts." | "He escrit una entradeta que capta l'atenció. He explicat el tema amb exemples quotidians." | "He narrativitzat el contingut (no he fet una llista de fets). He posat una cita amb nom de l'expert." | "He relacionat causes i efectes del fenomen. He usat dades estadístiques amb la font." | "He presentat el tema des de diverses perspectives i he inclòs el context científic ampli." |

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
| 1 Títol captador — Claredat i captació | `binary` + `qualitative` | no | binary: presència de títol; qualitative: LLM-jutge sobre captació per nivell |
| 2 Entradeta — Motivació i context | `structural` + `qualitative` | no | detectar presència d'entradeta diferenciada del cos; LLM-jutge sobre la creació d'expectativa |
| 3 Narrativització — Causa-efecte | `qualitative` + `structural` | no | LLM-jutge: el contingut s'explica com a procés o historia? Detectar llista de fets sense narrativitzar (senyals: "Primer... Després... Finalment..." sense connectius causals) |
| 4 Xifres arrodonides — Accessibilitat | `binary` + `qualitative` | no | binary: xifres no arrodonides amb decimals o precisió excessiva; qualitative: LLM-jutge sobre adequació al nivell |
| 5 Cites i atribució — Credibilitat | `binary` + `qualitative` | no | binary: presència de cites a B1+; qualitative: LLM-jutge sobre claredat d'atribució |
| 6 Exemples concrets — Accessibilitat | `qualitative` | no | LLM-jutge: exemple concret per paràgraf; accessible per al nivell |
| 7.1 Criteris — Tecnicismes | `binary` + `qualitative` | no | binary: presència de tecnicismes sense explicació a A1-A2; qualitative: adequació de l'explicació |
| 7.2 Criteris — Llargada | `countable` | no | comptar paràgrafs; verificar llindar per nivell |
| 7.3 Criteris — Fidelitat al text font | `cross_source` | **sí** (si adaptació) | comparar fenomen principal, relació causal i entradeta original vs adaptats |
| 8 Autoavaluació metacognitiva | `metacognitive` | no | derivar a vista d'autoavaluació alumne + registre docent |

**Notes:**
- Narrativització (Pas 3) és el descriptor de major càrrega qualitativa: distingir una llista narrativitzada d'una llista de fets requereix LLM-jutge. Senyal negatiu clau: connectors addició ("i", "també", "a més") en lloc de connectors causals ("per tant", "com a conseqüència", "això fa que").
- Tecnicismes (Pas 7.1): detectables per corpus de termes tècnics per matèria, però l'adequació de l'explicació requereix LLM-jutge.

## Heurístiques docent

**H1 — L'entradeta com a pregunta o xifra.**
Dues fórmules que sempre funcionen: (1) Pregunta directa: "Saps per qué el cel és blau?" (2) Xifra sorprenent: "Cada any es llencen 1.300 milions de tones de menjar al món." A A1-A2, proposo una de les dues plantilles i l'alumne omple el buit amb el tema de la unitat.

**H2 — "Explica-m'ho com si tingués 10 anys".**
Quan l'alumne perd el to narratiu i cau en la llista de fets, la pregunta és: "Com ho explicaries a un nen de 10 anys que no sap res del tema?" La resposta és gairebé sempre un paràgraf divulgatiu ben narrativitzat. Funciona des de A2.

**H3 — La cadena causal com a estructura.**
Per a cada paràgraf del cos, proposo l'esquema: "PER QUÈ passa X? COM passa X? QUÈ implica X?" Cada pregunta és una frase o dues. Tres preguntes = un paràgraf narrativitzat. L'alumne no ha de saber escriure divulgatiu; ha de saber respondre tres preguntes.

**H4 — Arrodonir sempre, contextualitzar sempre.**
Cada xifra necessita dues operacions: (1) arrodonir fins a un número significatiu ("gairebé dos milions" en lloc de "1.983.421"); (2) contextualitzar amb una comparació familiar ("el doble de la població de Catalunya"). Sense contextualització, la xifra no construeix comprensió.

## Fonts principals

- MALL (Model d'Aprenentatge de Llengües i Literacitat): HCL Explicar, transició BICS→CALP, narrativització com a pont conceptual.
- Cassany, D. (2006): *Rere les línies* — llegibilitat i accessibilitat de textos expositius; narrativització com a estratègia de divulgació.
- Cummins, J. (2000): *Language, Power and Pedagogy* — BICS/CALP i el text divulgatiu com a pont entre coneixement quotidià i acadèmic.
- Decret 175/2022 (currículum Catalunya): competència en comunicació lingüística i competència científica.
