---
modul: M3
titol: "Generar glossari"
tipus: instrument
categoria_principal: mediacio
categories_secundaries: [generes]
descripcio: "Instrument de mediació lèxica que acompanya el text adaptat amb definicions dels termes clau. CALP graduat per Cummins + variant bilingüe per a nouvinguts. Rúbrica gradada 6 passos × 6 nivells MECR amb dimensions internes."
mecr_range: [pre-A1, A1, A2, B1, B2, C1]
agent_roles: [adapter, generator]
complement_key: glossari
translanguaging: true
multimodal: true
moduls_relacionats: [M2, M3]
variables_configurables:
  fase_lectora: [logografica, alfabetica_emergent, alfabetica_fluida]
skill_meta: generate-glossari@corpusFJE/skills/complements/generate-glossari
review_status: pilot-fusio-2
version: 4.0.0-canonic
generat_at: 2026-05-24
actualitzat_at: 2026-05-24
notebooklm_review:
  data: 2026-05-24
  veredicte: si-amb-correccions-menors
  aplicades_des_d_inici: [patro-canonic-pilot-noticia, fidelitat-gradada-C2, aclariment-us-lectura-vs-produccio-C1]
  aplicades_post_review: [ordre-alfabetic-B2-C1, polir-autoavaluacio-B1-procés]
  comentari_key: "El patró escala correctament de gènere informatiu (notícia) a instrument de mediació (glossari). Confirma viabilitat de l'extrapolació als 35 instruments."
---

# Generar glossari

## Descripció

El glossari és un instrument de **mediació lèxica** que acompanya el text adaptat i ofereix definicions dels termes clau. La seva funció és reduir la càrrega cognitiva lèxica perquè l'alumne pugui centrar-se en la comprensió del contingut. Inclou una **variant bilingüe** per a alumnat nouvingut amb L1 coneguda.

**Tipologia MALL**: Mediació lèxica (suport).
**HCL principal**: Descriure — definir amb precisió creixent (CALP).
**Principi rector CALP de Cummins** (llargada de la definició per nivell): pre-A1=6 paraules · A1-A2=8-10 paraules · B1=12 paraules · B2=15 paraules · C1=20 paraules.

**Connexions MALL transversals:**
- *Translanguaging / TOLC*: la variant bilingüe és una estratègia de translanguaging explícita. El terme en L1 activa el coneixement previ i redueix l'ansietat lingüística.
- *Multimodalitat*: a pre-A1 i A1, els emojis/pictogrames fan el glossari accessible sense lectura plena.
- *CALP de Cummins*: la gradació de la complexitat de la definició és la implementació directa del concepte de llengua acadèmica.

**Aclariment d'ús — què descriu aquesta rúbrica.**
Aquesta rúbrica descriu el **glossari adaptat per a la LECTURA** de l'alumne (què el docent presenta perquè l'alumne consulti). **No descriu la producció autònoma de l'alumne** — això es treballa amb un derivat propi (rúbrica d'avaluació formativa), pertinent per al cas de **glossari col·laboratiu** (B1+ ; vegeu H4) on l'alumnat construeix el glossari sota la guia del docent.
**Sub-granularitat dins de pre-A1 i A1**: es treballa amb la variable independent `fase_lectora` del frontmatter (logografica · alfabetica_emergent · alfabetica_fluida), no amb columnes addicionals.

## Detecció

**Senyals docent** (quan activar glossari):
- El text conté termes curriculars d'especialitat que l'alumnat probablement desconeix (fotosíntesi, democràcia, equació, monarquia...).
- L'alumnat és nouvingut o té MECR baix en relació al text adaptat.
- La matèria és de ciències, tecnologia o ciències socials (densitat lèxica acadèmica alta).
- El text conté nominalitzacions o passives que dificulten la comprensió ("la realització del procés" en lloc de "quan es fa el procés").
- El docent ha notat que l'alumne usa BICS (llengua quotidiana) on caldria CALP: diu "cosa" en lloc de "recurs", "fer" en lloc de "implementar".

**Senyals alumne** (que indica que necessita glossari):
- Pregunta "Què vol dir...?" més de 3 vegades per paràgraf: la freqüència de bloquejos lèxics supera el llindar de processament.
- Llegeix fluïdament però no pot respondre preguntes sobre el contingut: el text és descodificat però no comprès.
- Nouvingut pre-A1 / A1: s'atura i mira l'adult sense dir res (el vocabulari és completament opac).
- Usa termes col·loquials en lloc dels tècnics quan explica el text ("la cosa que creix" en lloc de "la cèl·lula").
- En el diari de lectura o resposta escrita, bypassa els termes tècnics amb "etc." o "i altres coses".

**Context favorable**:
- Aula d'acollida o grup amb nouvinguts recents (beneficien especialment de la variant bilingüe amb L1 en alfabet original).
- Text de matèria no lingüística (TILC) amb densitat lèxica d'especialitat alta.
- Unitat didàctica on els termes clau tornaran a aparèixer al llarg del trimestre (val la pena la inversió en glossari).

**Anti-senyals** (quan NO activar glossari):
- El text ja inclou definicions integrades ("la fotosíntesi, és a dir, el procés pel qual…").
- Text de menys de 100 paraules on els termes desconeguts es poden explicar oralment en 2 minuts.
- L'alumnat coneix bé el vocabulari del tema (text familiar o repàs).
- El temps és limitat i és millor una explicació oral directa.

## Modulació per nivell

| Pas | Dimensió | Pre-A1<br>Emergent | A1<br>Inicial | A2<br>Funcional | B1<br>Estratègic | B2<br>Acadèmic | C1+<br>Crític |
|---|---|---|---|---|---|---|---|
| **1. Selecció de termes** | Nombre | 3-5 termes. | 5-8 termes. | 8-10 termes. | 10-12 termes. | 12-15 termes. | 15-18 termes. |
|  | Tipologia lèxica | Objectes reals i noms concrets. Sense tecnicismes. | Noms i verbs d'acció principals del text. | Noms + verbs + adjectius clau. | Inclou habilitats cognitives lèxicament marcades (hipòtesi, causa, conseqüència). | Lèxic d'especialitat (CALP). Inclou col·locacions ("realitzar una hipòtesi"). | CALP d'especialitat. Pot incloure termes meta-discursius i lèxic conceptual abstracte. |
| **2. Format de presentació** | Estructura | Emoji o pictograma + terme en negreta. Sense taula (massa complexa). | Taula de 2 columnes: Terme \| Explicació. | Taula de 2 columnes; pot afegir una analogia o exemple integrat. | Taula de 2 columnes; **ordre alfabètic** dels termes; pot afegir una tercera columna "Exemple en frase". | Taula de 2-3 columnes; **ordre alfabètic** obligatori; pot incloure referència creuada interna. | Taula completa; **ordre alfabètic** obligatori; pot incloure etimologia breu o distinció entre termes similars. |
|  | Suport visual | Pictograma obligatori a cada terme. L'adult pot complementar amb imatge real. | Emoji recomanat si el terme té representació visual clara. | Emoji opcional per a termes concrets; no per a abstractes. | Referència opcional a la il·lustració del text si n'hi ha. | No necessari; el lector processa el terme sense suport visual. | No necessari. |
| **3. Explicació / definició (CALP)** | Llargada | Fins a 6 paraules. Paraules molt freqüents. | Fins a 8 paraules en català molt senzill (A1). | Fins a 10 paraules. | Fins a 12 paraules. | Fins a 15 paraules. | Fins a 20 paraules. |
|  | Recursos pedagògics | Paraules immediates de l'experiència de l'alumne. | Català A1 sense tecnicismes dins la definició. No repetir el terme. | Pot incloure una analogia simple ("és com…") o un exemple concret del text. | Pot usar vocabulari lleugerament tècnic acompanyat d'un exemple. | Vocabulari acadèmic (CALP) propi del camp; pot referenciar un altre terme del glossari. | Definició precisa amb matís conceptual; pot incloure distinció entre termes similars o etimologia breu. |
| **4. Variant bilingüe (nouvingut L1)** | Inclusió L1 | Afegeix el terme en L1 amb alfabet original (àrab, xinès, urdú, ciríl·lic, armeni…). | Columna addicional "Traducció (L1)" en alfabet original. Taula de 3 columnes. | Columna addicional. Si no existeix paraula exacta en L1, usar la més propera amb aclariment breu. | Columna addicional. Pot afegir nota sobre diferències conceptuals entre L1 i català. | Columna addicional. Pot afegir nota sobre diferències morfosintàctiques rellevants. | Columna opcional. L'alumne ja pot gestionar el text sense suport explícit en L1. |
|  | Notes contrastives | Sense notes. La imatge és el pont. | Sense notes. La traducció directa és el pont. | Aclariment breu quan no hi ha equivalent exacte. | Notes conceptuals quan la categoria L1 difereix de la del català. | Notes morfosintàctiques o de col·locació quan són rellevants per a la comprensió. | Notes autonomes; pot incloure registre o variació diatòpica si és rellevant. |
| **5. Criteris transversals** | No-circularitat | El terme no apareix dins de la pròpia definició a cap nivell. | El terme no apareix dins de la pròpia definició a cap nivell. | El terme no apareix dins de la pròpia definició a cap nivell. | El terme no apareix dins de la pròpia definició a cap nivell. | El terme no apareix dins de la pròpia definició a cap nivell. | El terme no apareix dins de la pròpia definició a cap nivell. |
|  | No-recursivitat | La definició no usa cap paraula més tècnica que el terme mateix. | La definició usa només vocabulari A1 (mai termes més complexos sense explicar-los). | Pot usar termes d'A2 màx.; tecnicismes només si s'expliquen integrats. | Pot usar termes B1 màx.; tecnicismes acompanyats d'exemple. | Pot usar lèxic d'especialitat propi del camp si el lector ja el coneix. | Lèxic d'especialitat lliure dins del camp; referència creuada quan calgui. |
|  | Llengua de definició | Català (mai L1 dins la definició; la L1 va a la columna pròpia). | Català. | Català. | Català. | Català. | Català. |
|  | Selecció pertinent | Cap connector, cap nom propi excepte si és clau per a la matèria, cap paraula quotidiana òbvia (excepte a Emergent on els objectes concrets sí entren). | Idem. | Idem. | Idem. | Idem. | Idem (els meta-discursius sí entren). |
|  | Fidelitat al text font | Tots els termes del glossari apareixen literalment al text adaptat (fidelitat al lèxic nuclear del text). | Tots els termes apareixen literalment al text adaptat. | Tots els termes apareixen literalment al text adaptat. | Tots els termes apareixen al text o són col·locacions necessàries per a la comprensió. | Termes literals + col·locacions + derivacions conceptualment necessàries. | Termes literals + col·locacions + derivacions + termes conceptualment connectats que amplien la xarxa lèxica del camp. |
| **6. Autoavaluació metacognitiva** | Reflexió sobre el procés | "He mirat les imatges del glossari quan al text he trobat una paraula que no he reconegut." | "Quan llegint el text he trobat una paraula difícil, he anat al glossari a buscar-la abans de demanar ajuda." | "He fet servir el glossari per entendre el text. He intentat dir el significat amb les meves paraules a algú." | "He reflexionat sobre si sabia usar els termes del glossari en una frase pròpia, i així he sabut quins encara no domino." | "He pensat quina diferència hi ha entre els termes del glossari que es poden confondre i com triaria un o l'altre." | "He reflexionat sobre com s'usaria el terme en un altre context i si la definició encara seria vàlida." |

## Metadades de cel·la (per a `build_skills.py`)

Cada dimensió té un **tipus de descriptor** que condiciona com s'ha de transformar al derivat avaluatiu i al derivat-prompt.

**Tipus de descriptor:**
- `countable` — té un llindar quantitatiu verificable mecànicament.
- `binary` — només admet "compleix / no compleix".
- `enumerable` — verificable contra una llista.
- `qualitative` — requereix judici humà o LLM-jutge.
- `structural` — requereix anàlisi sintàctica / discursiva.
- `cross_source` — requereix accés al text font o al text adaptat per comparar.
- `metacognitive` — descriptor de procés en primera persona.

| Pas / Dimensió | Tipus | requires_source_text | validation_hint |
|---|---|---|---|
| 1.1 Selecció — Nombre | `countable` | parcial (text adaptat) | comptar entrades del glossari |
| 1.2 Selecció — Tipologia lèxica | `qualitative` + `enumerable` | parcial | LLM-jutge classifica els termes per tipologia (concret/abstracte/CALP/col·locació) i contrasta amb el nivell |
| 2.1 Format — Estructura | `structural` | no | parsejar el format (HTML/Markdown) i verificar columnes esperades per nivell |
| 2.2 Format — Suport visual | `binary` + `enumerable` | no | comptar emojis/pictogrames per terme; verificar presència obligatòria a pre-A1 |
| 3.1 Definició — Llargada | `countable` | no | comptar paraules de cada definició; verificar llindar per nivell |
| 3.2 Definició — Recursos pedagògics | `qualitative` | no | LLM-jutge detecta analogies, exemples, vocabulari acadèmic segons nivell |
| 4.1 Variant bilingüe — Inclusió L1 | `binary` (per existència) + `qualitative` (alfabet correcte) | no | detectar presència de columna L1 i validar alfabet original |
| 4.2 Variant bilingüe — Notes contrastives | `qualitative` | no | LLM-jutge sobre presència i pertinença de notes |
| 5.1 No-circularitat | `binary` | no | regex: el terme NO apareix dins de la pròpia definició |
| 5.2 No-recursivitat | `qualitative` | no | LLM-jutge: les paraules de la definició són d'un nivell ≤ al terme |
| 5.3 Llengua de definició | `binary` | no | detector de llengua sobre cada definició; ha de ser català |
| 5.4 Selecció pertinent | `qualitative` | no | LLM-jutge contra llista de tipus prohibits (connectors, noms propis, quotidians) |
| 5.5 Fidelitat al text font | `cross_source` | **sí** (text adaptat) | comprovar que cada terme del glossari apareix al text adaptat; a B1+ permet col·locacions i derivacions. LLM-jutge amb tres prompts diferenciats segons nivell objectiu |
| 6 Autoavaluació metacognitiva | `metacognitive` | no | derivat doble: autoavaluació alumne + registre docent de la qualitat |

**Notes:**
- A diferència de notícia, glossari té **molts descriptors `qualitative`** (tipologia lèxica, recursos pedagògics, no-recursivitat, selecció pertinent). LLM-jutge serà més carregat aquí.
- `cross_source` a 5.5 requereix el **text adaptat** com a font (no el text original del docent). Cal accedir a `atne_adaptations.adapted_html` o `history.adapted_text` al pipeline.
- 5.1 No-circularitat és `binary` mecànic — es pot validar amb regex sense LLM (gran avantatge per cost).
- 5.3 Llengua de definició és `binary` amb detector lingüístic (langdetect o equivalent) — sense LLM.

## Heurístiques docent

**H1 — La marca mental de preguntes anteriors.**
Selecciono els termes del glossari llegint el text i marcant els que l'alumnat m'ha preguntat en unitats anteriors sobre el mateix tema. Tinc una llista mental (o física) de "paraules conflictives" per matèria i nivell: a ciències 3r ESO, "osmosi", "membrana" i "ions" sempre necessiten glossari. Si els trobo al text nou, el glossari és automàtic.

**H2 — La prova de la substitució.**
Per decidir si un terme va al glossari, faig la prova de la substitució: "Podria l'alumne entendre la frase si tragués aquesta paraula i la substituís per 'cosa'?". Si la resposta és "sí, quasi bé", el terme no és crític per a la comprensió. Si és "no, perdria tot el sentit", el terme va al glossari. Aquesta prova em permet ser selectiu i no sobrecarregar l'alumne amb 20 termes.

**H3 — Variant bilingüe amb L1 d'alfabet no llatí.**
Per a alumnat nouvingut d'àrab, xinès, urdú o armeni, el glossari bilingüe amb l'alfabet original de la L1 és gairebé sempre necessari els primers 3 mesos. El terme en L1 actua com a "ancoratge cognitiu": l'alumne ja sap el concepte en la seva llengua i el glossari bilingüe simplement li dóna la paraula en català. Sense aquest pont, l'alumne ha d'aprendre simultàniament el concepte i la paraula, cosa que dobla la càrrega cognitiva.

**H4 — Glossari col·laboratiu (B1+).**
A partir de B1, proposo que sigui l'alumnat qui construeixi el glossari col·lectivament: primer identifiquen els termes que no entenen, després busquen la definició en parelles. El docent valida i corregeix. Aquesta estratègia té un efecte doble: l'alumne pren consciència del seu propi desconeixement lèxic (metacognició) i el glossari resultant és més ajustat a les necessitats reals del grup. **És el cas de PRODUCCIÓ d'alumnat** — per a avaluar-ho cal el derivat propi (rúbrica d'avaluació formativa de producció), no aquesta rúbrica de producte.

**H5 — El glossari com a avaluació diagnòstica.**
Abans d'adaptar un text complex, demano a l'alumnat que subratlli les paraules que no entenen. El resultat és un diagnòstic lèxic ràpid: si la majoria del grup subratlla els mateixos termes, el problema és col·lectiu i cal glossari comú. Si cada alumne subratlla paraules diferents, el problema és individual i cal suport personalitzat (o glossari diferenciat per nivell).

## Fonts principals

- Cummins (2000): CALP i BICS — la definició com a exercici de llengua acadèmica. Principi de gradació CALP.
- MALL (Model d'Aprenentatge de Llengües i Literacitat): gradació lèxica per MECR.
- Cummins & Early (2011): Translanguaging — glossari bilingüe com a pont cognitiu entre L1 i L2.
- Decret 175/2022 (currículum Catalunya): competències comunicatives i plurilingüisme.
