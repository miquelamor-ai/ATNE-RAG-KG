---
modul: M3
titol: "Escriure/adaptar una notícia"
tipus: instrument
categoria_principal: generes
categories_secundaries: []
descripcio: "Instrument per adaptar o generar una notícia periodística (piràmide invertida + 5W). Rúbrica gradada 8 passos × 6 nivells MECR amb dimensions internes."
mecr_range: [pre-A1, A1, A2, B1, B2, C1]
agent_roles: [adapter, generator]
genre_key: noticia
translanguaging: true
multimodal: true
moduls_relacionats: [M3]
variables_configurables:
  fase_lectora: [logografica, alfabetica_emergent, alfabetica_fluida]
skill_meta: write-noticia@corpusFJE/skills/genres/write-noticia
review_status: pilot-fusio
version: 4.0.0-canonic
generat_at: 2026-05-21
actualitzat_at: 2026-05-21
notebooklm_review:
  data: 2026-05-21
  veredicte: si-amb-correccions
  aplicades: [C3-pas8-B1-metacognicio, C4-pas2-C1-estil-soft, C1-aclariment-us-lectura-vs-produccio, C2-fidelitat-gradada-nuclear-context-matis]
  decisions_pedagogiques_miquel:
    C1: "Cel·la mantinguda. Afegit aclariment d'ús: la rúbrica descriu text per a LECTURA, no producció autònoma. Sub-pre-A1 via fase_lectora, no columnes noves."
    C2: "Fidelitat gradada (nuclear pre-A1→A2 · fet+context B1 · matís B2-C1+)."
---

# Escriure/adaptar una notícia

## Descripció

La notícia periodística és un gènere informatiu que relata fets reals seguint l'estructura de **piràmide invertida** (el més important primer, el menys important al final). És altament gradable perquè l'estructura es manté constant a tots els nivells i la complexitat s'ajusta per MECR.

**Tipologia MALL**: Narrativa / Informativa.
**HCL principal**: Narrar — seqüenciar un fet real (les 5W: Qui, Què, Quan, On, Per què).
**HCL secundàries**: Descriure context (A2+) · Justificar amb fonts (B1+) · Avaluar fiabilitat de fonts (B2+).

**Connexions MALL transversals:**
- *Translanguaging / TOLC*: a pre-A1 i A1, paraules de la L1 entre claudàtors `[...]`. A B1+, glossari bilingüe annex opcional.
- *Multimodalitat*: pictogrames a l'esquerra a pre-A1 i A1. A B1+, referència a infografies o mapes.
- *Eix oral / escrit*: a pre-A1 i A1, lectura en veu alta mediada per adult. A A2+, lectura autònoma possible.

**Aclariment d'ús — què descriu aquesta rúbrica.**
Aquesta rúbrica descriu el **text adaptat per a la LECTURA** de l'alumne (què presenta ATNE o el docent perquè l'alumne llegeixi). **No descriu la producció autònoma de l'alumne** — això és tasca d'un derivat propi (rúbrica d'avaluació formativa), que pot tenir descriptors diferents als nivells baixos. Principi pedagògic MALL: l'alumne llegeix models bons al màxim del seu abast i en produeix els seus textos; són els docents i assistents qui adapten textos.
**Sub-granularitat dins de pre-A1 i A1**: es treballa amb la variable independent `fase_lectora` del frontmatter (logografica · alfabetica_emergent · alfabetica_fluida), no amb columnes addicionals.

## Detecció

**Senyals docent** (quan triar notícia):
- El text font és un article de premsa, una notícia digital o un document informatiu sobre un fet real.
- Vol treballar la distinció fet / opinió (competència crítica, Decret 175/2022).
- L'alumnat ha de llegir un text de CCSS, CN o Llengua amb dimensió social o d'actualitat.
- El grup té alumnat nouvingut que necessita comprendre textos informatius en català per integrar-se a les matèries.
- La matèria treballa la comprensió de text informatiu (avaluació competencial).

**Senyals alumne** (que indica que necessita l'instrument):
- En resumir la notícia, narra lliurement ("hi ha un home que…") sense estructurar Qui / Quan / On: no té la superestructura del gènere.
- Llegeix el text sencer però no pot respondre "per què ha passat?" — *efecte mirall literal* (MALL): llegeix les línies però no entre línies.
- Es bloqueja davant titulars amb metàfores ("La guerra del clima") i no sap de què tracta la notícia.
- Confon la cita d'opinió de l'entrevistat amb el fet objectiu: no distingeix veu de l'autor / veu de la font.
- Nouvingut pre-A1 / A1: descodifica mecànicament però no construeix sentit; s'atura i mira l'adult sense dir res.

**Context favorable** (quan l'instrument és especialment necessari):
- Aula amb alumnat nouvingut (aula d'acollida o integrat): necessiten superestructura del gènere per comprendre textos de matèries.
- Grup heterogeni on el 30%+ pot tenir comprensió lectora baixa (PIRLS Catalunya 2021).
- Matèries no lingüístiques (CCSS, CN) que usen textos informatius com a font d'aprenentatge (TILC).

**Anti-senyals** (quan NO triar notícia):
- El text font és un conte, poema o narrativa de ficció → adaptar al gènere original.
- L'alumnat vol expressar la seva opinió o vivència personal → opinió, diari o carta.
- El text no relata cap fet concret (és especulatiu o filosòfic) → assaig o divulgatiu.

## Modulació per nivell

| Pas | Dimensió | Pre-A1<br>Emergent | A1<br>Inicial | A2<br>Funcional | B1<br>Estratègic | B2<br>Acadèmic | C1+<br>Crític |
|---|---|---|---|---|---|---|---|
| **1. Identificació del fet** | Fets clau | L'adult explica el fet amb una imatge. L'alumne assenyala el personatge principal. | Respon "Qui?" i "Què?" en 1-2 paraules. | Identifica 2-3 fets principals del text font. | Jerarquitza 3-4 fets per rellevància informativa. | Identifica l'angle informatiu i la selecció editorial. | Analitza la intencionalitat i l'enquadrament ideològic de la peça. |
| **2. Titular** | Llargada i forma | 1-5 paraules acompanyades d'un pictograma a l'esquerra. Sense verb obligatori. | Fins a 10 paraules. Verb concret en present o passat. | Fins a 12 paraules. Verb + complement informatiu. | Fins a 15 paraules. Clar i informatiu, sense adjectius valoratius. | Fins a 18 paraules. Pot incloure un matís causal. | Sense límit estricte de paraules; precisió i claredat com a criteri únic. |
|  | Estil literal | Concepte únic, suport visual obligatori. | Sense metàfores ni jocs de paraules. | Sense metàfores. Llenguatge directe. | Sense metàfora. Pot tenir matís però sentit literal. | Sense metàfora. Pot tenir matís complex però unívoc. | Llenguatge precís; els jocs de paraules només són admissibles si no comprometen la claredat informativa. |
| **3. Lead — 5W** | Cobertura 5W | Cobreix 2W: Qui i Què. Lectura mediada per adult. | Cobreix 3W: Qui, Què i On. | Cobreix 4-5W (afegeix Quan i, si escau, Per què). | Cobreix les 5W completes. | Cobreix les 5W més un context breu. | Cobreix 5W més context i implicació informativa. |
|  | Llargada de frase | Frases de fins a 8 paraules. | Frases de fins a 12 paraules. | Frases de fins a 15 paraules. | Frases de fins a 18 paraules. | Frases de fins a 22 paraules. | Sense límit estricte; claredat com a criteri únic. |
|  | Estructura sintàctica | Frase única amb suport visual; sintaxi mínima. | Frase simple Subjecte + Verb + Complement. | Pot incloure una subordinada simple. | Subordinació causal admissible (perquè, ja que). | Subordinació complexa amb connectors elaborats. | Sintaxi lliure amb claredat obligatòria. |
| **4. Cos — piràmide invertida** | Ordre informatiu | 1-2 frases amb pictograma de suport; el fet principal apareix primer. | 2-3 frases ordenades del fet més important al menys important. | 2-3 paràgrafs amb piràmide invertida clara. | 3 paràgrafs amb piràmide invertida explícita i transició lògica. | 3-4 paràgrafs amb detall creixent en zones secundàries. | Estructura de crònica completa amb piràmide flexibilitzada però jerarquitzada. |
|  | Volum del cos | 1-2 frases. | 2-3 frases. | 2-3 paràgrafs breus. | 3 paràgrafs estructurats. | 3-4 paràgrafs estructurats. | Múltiples paràgrafs sense límit estricte. |
| **5. Fonts i cites** | Cita directa | Sense cites. L'adult és la font. | Sense cites. | Una cita directa breu integrada al text. | Una cita directa més una atribució indirecta. | Dues a tres cites amb contrast de punts de vista. | Múltiples cites amb contrast i jerarquització de credibilitat. |
|  | Atribució | No aplica. | No aplica. | Atribució clara: "Segons [persona], '…'". | Font identificada per a cada dada principal. | Atribució explícita i avaluada per a cada font. | Atribució i triangulació explícites; detecció de biaix de selecció. |
| **6. Fiabilitat de fonts** | Avaluació de fonts | No aplicable (mediació adult). | No aplicable. | Opcional: "Qui ho ha dit? On ho diu el text?". | El lector identifica la font de cada dada principal. | El lector avalua la credibilitat de cada font i ho explicita al text. | El lector contrasta fonts, detecta biaix i analitza l'enquadrament. |
| **7. Criteris transversals** | Adjectius valoratius | Cap. | Cap. | Cap. | Cap. | Cap. | Cap (excepte si la font els porta i s'atribueixen explícitament). |
|  | Acrònims | No s'usen; suport oral de l'adult. | Desplegats sempre: "ONU (Organització de les Nacions Unides)". | Desplegats la primera vegada al text. | Desplegats la primera vegada; integrats al context. | Desplegats la primera vegada; lèxic acadèmic neutre. | Acrònims comuns acceptats; els especialitzats es despleguen. |
|  | Context aclarit | L'adult explica el context oralment. | Sense "ahir" / "el president": noms i temps complets. | Dates completes i noms complets sempre. | Context historicogeogràfic breu integrat al text. | Context historicogeogràfic integrat amb precisió. | Context complex jerarquitzat i comparat. |
|  | Fidelitat al text font | Fidelitat al fet nuclear (qui, què, on). | Fidelitat al fet nuclear (qui, què, on). | Fidelitat al fet nuclear (qui, què, on). | Fidelitat al fet i al context principal. | Fidelitat al matís i als punts de vista originals. | Fidelitat al matís, als punts de vista i a la complexitat informativa originals. |
|  | Registre | Bàsic amb pictograma. Vocabulari concret immediat. | Neutre i frequent ("va morir", no "va perdre la vida"). | Neutre amb termes freqüents de la matèria. | Neutre amb termes específics integrats. | Neutre amb lèxic acadèmic propi del camp (CALP inicial). | Formal acadèmic amb lèxic d'especialitat (CALP plena). |
| **8. Autoavaluació metacognitiva** | Reflexió sobre el procés | "He mirat la imatge i he escoltat la notícia; quan no entenia, he assenyalat què no entenia." | "He llegit el text un cop i, quan no entenia una paraula, l'he buscat o he demanat ajuda." | "He revisat el meu text per veure si un lector que no conegui el fet l'entendria." | "He decidit quina era la dada més important del fet i l'he posada al principi pensant en el meu lector." | "He pensat com un lector crític: hi ha alguna afirmació sense font? he donat un punt de vista sense voler?" | "He reflexionat sobre el meu enquadrament: quines fonts he triat, quines he deixat fora, i a qui beneficia aquesta tria." |

## Metadades de cel·la (per a `build_skills.py`)

Cada dimensió té un **tipus de descriptor** que condiciona com s'ha de transformar al derivat avaluatiu i al derivat-prompt. Aquest bloc és la **clau perquè el script automàtic funcioni**.

**Tipus de descriptor:**
- `countable` — té un llindar quantitatiu verificable mecànicament (ex: ≤12 paraules per frase).
- `binary` — només admet "compleix / no compleix" (ex: cap adjectiu valoratiu).
- `enumerable` — verificable contra una llista (ex: 5W al lead → cobertura per ítem).
- `qualitative` — requereix judici humà o LLM-jutge (ex: registre neutre).
- `structural` — requereix anàlisi sintàctica/discursiva (ex: estructura S+V+C, piràmide invertida).
- `cross_source` — requereix accés al text font per comparar (ex: fidelitat al fet).
- `metacognitive` — descriptor de procés en primera persona (Pas 8); no es deriva a graella avaluativa estàndard, requereix vista d'autoavaluació + registre docent.

| Pas / Dimensió | Tipus | requires_source_text | validation_hint |
|---|---|---|---|
| 1.1 Fets clau | `enumerable` | parcial (només si adapta) | comptar identificació de Qui, Què, On, Quan, Per què al text |
| 2.1 Titular — Llargada i forma | `countable` + `structural` | no | comptar paraules; detectar presència de verb i temps verbal |
| 2.2 Titular — Estil literal | `qualitative` | no | LLM-jutge o llista de patrons metafòrics típics |
| 3.1 Lead — Cobertura 5W | `enumerable` | no | comptar quines W apareixen explícitament al lead |
| 3.2 Lead — Llargada de frase | `countable` | no | comptar paraules per frase entre punts |
| 3.3 Lead — Estructura sintàctica | `structural` | no | parser sintàctic o LLM amb regla S+V+C |
| 4.1 Cos — Ordre informatiu | `structural` | no | verificar si primera frase conté el fet principal del lead |
| 4.2 Cos — Volum del cos | `countable` | no | comptar frases o paràgrafs del cos |
| 5.1 Cita directa | `binary` (per existència) + `countable` (per nombre) | no | detectar marques de cita directa (" " o '') i comptar |
| 5.2 Atribució | `qualitative` + `structural` | no | LLM-jutge amb regla "Segons [persona], '…'" |
| 6 Fiabilitat de fonts | `qualitative` | no | LLM-jutge sobre identificació de font per dada |
| 7.1 Adjectius valoratius | `binary` | no | llista de patrons + LLM-jutge |
| 7.2 Acrònims | `binary` (per existència desplegat) | no | detectar sigles i comprovar desplegament |
| 7.3 Context aclarit | `binary` + `qualitative` | no | detectar referències vagues ("ahir", "el president") |
| 7.4 Fidelitat al text font | `cross_source` | **sí** | comparació semàntica amb el text font, **gradada per nivell**: a pre-A1→A2 comprova preservació del fet nuclear (qui, què, on); a B1 fet + context principal; a B2-C1+ matís i punts de vista. LLM-jutge amb tres prompts diferenciats per nivell. |
| 7.5 Registre | `qualitative` | no | LLM-jutge + llista d'eufemismes i floritura |
| 8 Autoavaluació metacognitiva | `metacognitive` | no | derivar a vista d'autoavaluació alumne + registre docent |

**Notes:**
- Els descriptors `countable`, `enumerable`, `binary` i `structural` són **automatitzables sense LLM** (regex + parser).
- Els `qualitative` requereixen **LLM-jutge** o equivalent; són els punts de variància entre execucions.
- `cross_source` (7.4 Fidelitat) **bloqueja** la derivació si no s'ha conservat el text font al pipeline ATNE — atenció a l'arquitectura de dades de la sessió de pilot.
- `metacognitive` (Pas 8) requereix **dues sortides** al derivat avaluatiu: l'autoavaluació de l'alumne + el registre docent de la qualitat d'aquesta autoavaluació.

## Heurístiques docent

**H1 — La prova de les 5W**
Quan un alumne em mostra el resum de la notícia i és una narració lliure sense estructura ("hi ha un home que va fer una cosa important"), li faig la prova de les 5W: "Qui? Quan? On? Per què?". Si no pot respondre 3 de les 5 preguntes, la superestructura del gènere no és interioritzada. En aquests casos, l'instrument notícia amb les 5W explícites és la bastida correcta. No cal que sigui el text complet: de vegades el lead sol ja és suficient per treballar.

**H2 — El bloqueig davant densitat lèxica**
Quan l'alumne nouvingut s'atura a cada paràgraf i em mira sense dir res, o pregunta "Mestre, no entenc res", no és un problema de voluntat sinó de càrrega cognitiva: el vocabulari és opac i no pot construir sentit. Sé que cal adaptar la notícia al seu MECR i afegir glossari. El senyal d'alarma és quan la freqüència de preguntes "Què vol dir...?" supera 3 per paràgraf.

**H3 — La confusió fet / opinió**
A ESO, quan demano que identifiquin el fet principal i em diuen l'opinió de l'entrevistat com si fos un fet ("diu que és molt important"), sé que no distingeixen la veu narrativa de la veu de la font. L'instrument notícia amb la regla "cita directa + atribució clara" és la resposta pedagògica. Abans de passar a un text nou, fem la distinció en el text actual: "Qui diu això? L'autor o la persona entrevistada?".

**H4 — Nouvingut recent (aula d'acollida)**
Per a alumnat nouvingut de 0-3 mesos, el primer instrument que funciona és la notícia amb pictogrames. Trio un fet que l'alumne ja conegui d'alguna manera (esport, temps, escola) per activar el coneixement previ en L1. Si la L1 és àrab o xinès, la variant bilingüe del glossari acompanyant és gairebé obligatòria: el vincle L1→L2 redueix l'ansietat i accelera la comprensió.

**H5 — La piràmide invertida com a prova de comprensió**
Quan un alumne ha llegit la notícia i me la resumeix del revés (comença pels detalls i acaba pel fet principal), sé que la piràmide invertida no és interioritzada. Li demano que subralli la frase més important de cada paràgraf i que les ordeni. Si no sap quina és la més important, el problema és inferencial: cal un text adaptat al seu MECR amb la piràmide molt explícita.

## Fonts principals

- MALL (Model d'Aprenentatge de Llengües i Literacitat): gradació MECR, control de la llengua, HCL.
- Cummins (2000): CALP i BICS — llargada de frase com a indicador de càrrega cognitiva.
- Cummins & Early (2011): Translanguaging i TOLC com a recursos d'aula.
- Decret 175/2022 (currículum Catalunya): competències comunicatives i plurilingüisme.
- PIRLS Catalunya 2021: dades de comprensió lectora a primària com a context epidemiològic.
