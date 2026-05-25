# Parking lot — El contrarelat de l'odi com a possible nou gènere

**Origen**: pregunta de Miquel, sessió ATNE 2026-05-25, durant la recerca sobre dimensió crítica de l'opinió.
**Estat**: anàlisi inicial. **Decisió pendent**, requereix recerca acadèmica complementària + validació pedagògica.
**Disparador**: durant la investigació sobre fake news / fal·làcies / discurs d'odi com a dimensions de l'opinió, Miquel pregunta si el **contrarelat** (counter-narrative) pot ser un gènere propi i no només una dimensió de l'opinió.

---

## Què és el contrarelat (counter-narrative)

El contrarelat és **una resposta argumentativa específica al discurs d'odi**, dissenyada per desmuntar prejudicis, narratives extremistes o estereotips estigmatitzants. **No és opinió genèrica**: és resposta a un discurs preexistent identificat com a perjudicial.

### Característiques operatives (no exhaustives)

| Característica | Descripció |
|---|---|
| **Reactivitat** | Sempre respon a un discurs concret previ (notícia, post a xarxes, comentari públic). No és autònom. |
| **Funció social** | Combatre el discurs d'odi, no només refutar arguments. Té dimensió ètica i ciutadana explícita. |
| **Estratègies retòriques específiques** | Empatia, narrativa testimonial, humor desactivant, fets contraposats, redirecció. Tradició diferenciada de la refutació argumentativa clàssica. |
| **Marc institucional** | Consell d'Europa "We CAN!" (2017), UNESCO #SpreadNoHate, Bookmarks (COE 2014/2020), No Hate Speech Movement. |
| **Mitjà natural** | Xarxes socials, mitjans públics, comentaris en línia. Connecta amb alfabetització mediàtica i ciutadania digital. |

---

## Argument 1 — És un gènere propi (postura "GÈNERE NOU")

### Criteris de Schneuwly & Dolz (1997) per definir un gènere

Un gènere es defineix per:
1. **Funció social distinta** ✅ — combatre discurs d'odi (no és persuadir genèric).
2. **Estructura prototípica** ✅ — identificar discurs d'odi → desmuntar (empatia + fets + narrativa) → redirigir.
3. **Situació comunicativa específica** ✅ — emissor compromès, audiència potencialment polaritzada, mitjà generalment digital, urgència temporal (resposta ràpida).

### Diferenciació del gènere d'opinió formal

| Eix | Opinió | Contrarelat |
|---|---|---|
| **Punt de partida** | Una tesi pròpia | Un discurs aliè concret a refutar |
| **Funció primària** | Persuadir d'una postura | Desactivar un discurs perjudicial |
| **Estratègies dominants** | Tesi + arguments + evidències + connectors | Empatia + narrativa testimonial + redirecció + humor |
| **Tipus de prova** | Dades, cites, exemples | Testimoniatge personal, contrast factual, exposició de mecanismes de manipulació |
| **Audiència** | Lector genèric, interlocutor neutral | Lector polaritzat o exposat al discurs original; **audiència terciària** és sovint la real |
| **Marc ètic** | Pensament crític competencial | **Drets humans + ciutadania activa** (Consell d'Europa) |

### Tradició pedagògica establerta

- **Consell d'Europa** "No Hate Speech Movement" (2013-2017, prorrogat com a campanya juvenil).
- **Manual *Bookmarks*** (Keen & Georgescu 2014/rev. 2020) — material pedagògic operatiu per a Secundària.
- **Manual *We CAN!*** (Consell d'Europa 2017) — específic sobre construcció de contranarratives.
- **UNESCO #SpreadNoHate** — recursos educatius.
- **Decret 175/2022 (Catalunya)** — competència ciutadana exigeix tractament del discurs d'odi.
- **eduCAC (CAC)** — unitats didàctiques sobre hate speech (verificat per Miquel).

### Conclusió de la postura "gènere nou"

El contrarelat **té totes les marques d'un gènere específic**: funció social diferenciada, estructura prototípica, situació comunicativa pròpia, **tradició pedagògica internacional documentada**, **marc curricular català** (175/2022), i **estratègies retòriques que no encaixen** al gènere argumentatiu clàssic (testimoniatge, humor desactivant).

**Implicació**: nou instrument **`generate-contrarelat-odi`** o **`write-contrarelat`** al corpusFJE. Possible categoria: `generes` (si es prioritza producció) o `mediacio` (si es prioritza la funció de prevenció). Cal decidir.

---

## Argument 2 — És una dimensió del gènere d'opinió ampliat (postura "DIMENSIÓ AMPLIADA")

### Argument contra fragmentació

El contrarelat pot integrar-se com a **especialització del Pas 5 (Reconeixement i refutació)** de l'opinió, amb una variant específica per a discurs d'odi:

- Opinió A2: refutació simple amb evidència contraposada.
- Opinió B2+: refutació argumentativa fonamentada.
- **Contrarelat (B2+)**: refutació de discurs d'odi amb estratègies específiques (empatia + testimoniatge + redirecció).

### Risc de fragmentar

Si fem instruments separats per a cada subtipus de refutació (contrarelat d'odi, refutació científica, refutació política, etc.), el corpus es **fragmentaria excessivament** i perdria coherència. Una dimensió ben dissenyada a opinió pot cobrir-ho.

### Posicions documentades en aquesta direcció

- **Walton (1996, 2008)** *Argumentation Schemes*: la refutació és una capa de l'argumentació general; els esquemes específics (incloent-hi el contrarelat) són **subtipus**, no gèneres independents.
- **Argument-Centered Education** (Kialo, ACE): integrar fal·làcies i contranarratives dins el gènere argumentatiu per evitar descontextualització.
- **DigComp 2.2 (JRC, 2022)**: incrustar competència mediàtica dins competències existents, no fer-ne instruments paral·lels.

### Conclusió de la postura "dimensió ampliada"

El contrarelat és **una variant especialitzada de la refutació argumentativa**. Crear-li gènere propi pot fragmentar artificialment el sistema. Millor: una **dimensió específica al M\*.md d'opinió** ("Refutació de discurs d'odi") amb estratègies pròpies a B2+.

**Implicació**: NO cal nou instrument. Afegir dimensió al Pas 5 de l'opinió.

---

## Argument 3 — Postura intermèdia (subgènere o variant tipològica)

### Tesi

El contrarelat és un **subgènere argumentatiu especialitzat**: comparteix l'estructura argumentativa general amb l'opinió, però té estratègies retòriques i propòsit funcional prou diferenciats per justificar **tractament didàctic propi sense gènere autònom**.

### Implementació possible

- **NO** instrument propi al corpusFJE.
- **NO** simplement dimensió de l'opinió.
- **SÍ** **complement/skill propi al cos d'opinió**: per ex. `generate-contrarelat-odi` com a **eina derivada** d'opinió, no gènere autònom.

Aquesta opció existeix arquitectònicament al corpus actual: hi ha `skills/complements/` com a categoria diferent de `skills/generes/` i `skills/mediacio/`. Es podria explorar si el contrarelat encaixa allà.

---

## La meva síntesi (no vinculant)

**Lectura inicial**: el contrarelat **TÉ pes per ser un gènere propi**, però **no és urgent decidir-ho ara**. La recerca preliminar (Consell d'Europa, UNESCO, eduCAC, Decret 175) ho recolza, però **manca recerca acadèmica específica catalana** sobre el tractament del contrarelat en aules de Primària/ESO. Caldria:

1. **Recerca acadèmica específica** sobre contranarratives a aula catalana / espanyola / europea.
2. **Consulta a docents FJE** d'ESO que treballin ciutadania crítica i convivència.
3. **Anàlisi del material existent d'eduCAC i CAC** sobre hate speech educatiu — verificar si proposa estructura argumentativa pròpia.
4. **Mirar si el corpusFJE ja té algun instrument** que toqui el tema (per exemple, `generate-activitats-aprofundiment` o similar podria tenir variants).

---

## Tres opcions per a la decisió pedagògica final

| Opció | Avantatge | Risc |
|---|---|---|
| **A. Gènere propi** (`write-contrarelat-odi`) | Reconeix la funció social diferenciada · Alineat amb Consell d'Europa i UNESCO · Decret 175/2022 té base curricular | Fragmenta el sistema · Pot demanar molts gèneres específics (contrarelat polític, científic...) |
| **B. Dimensió ampliada** al Pas 5 d'opinió | Coherent amb gèneres existents · No multiplica instruments · Camps & Dolz integren la refutació | Pot ser insuficient per a la complexitat retòrica i ètica del contrarelat |
| **C. Subgènere/complement** dins `skills/complements/` o similar | Reconeixement de l'especialitat sense gènere autònom · Flexibilitat arquitectònica | Pot ser confús: ni gènere ni dimensió |

---

## Actualització 2026-05-25 (vespre) — Recerca internacional complementària

Després de l'anàlisi inicial, WebSearch directe aporta dues troballes crítiques:

### Troballa 1 — Consell d'Europa DISTINGEIX dos subtipus

Cita literal del marc Consell d'Europa (manual *Bookmarks* + *We CAN!*):
> "**Counterspeech** is a **short and direct reaction** to hateful messages; **alternative speech** **usually does not challenge or directly refer to hate speech but instead changes the frame of the discussion**."

**Implicacions arquitectòniques:**
- Hi ha **dos subgèneres documentats**, no un de sol:
  - **Counterspeech** (resposta directa): refuta un discurs concret amb fets/argument.
  - **Counter-narrative / Alternative speech** (canvi de marc): proposa narrativa alternativa que no respon directament al discurs d'odi sinó que canvia el frame del debat.
- Si fem un instrument FJE, **caldrà decidir si cobreix tots dos o si fem dos instruments**.

### Troballa 2 — Benesch (Dangerous Speech Project) té taxonomia codificada

Susan Benesch articula una **taxonomia de counterspeech amb 8 estratègies** (citada per Wikipedia i diversos papers de NLP per a generació automàtica de contranarratives):

| # | Estratègia | Descripció |
|---|---|---|
| 1 | **Empatia** | Tonalitat empàtica vers l'autor del discurs d'odi i la víctima |
| 2 | **Fact-checking / Correcció factual** | Presentació de fets que corregeixen falsedats o malentesos |
| 3 | **Humor** | Riure desactivant que treu serietat al discurs d'odi |
| 4 | **Vergonya / Shaming** | Visibilitzar la inacceptabilitat moral de l'enunciat |
| 5 | **Advertència de conseqüències** | "Aquest tipus de discurs porta a X" — apel·lació conseqüencialista |
| 6 | **To** | Tria de tonalitat (no només contingut): respectuós, ferm, etc. |
| 7 | **Identificació tribal** (afiliació) | "Nosaltres no diem aquestes coses" — apel·lació a la pertinença |
| 8 | **Redirecció / Educació** | Reorientar el debat cap a una qüestió més productiva |

**Implicacions per a la rúbrica:** si fem el contrarelat com a gènere, **aquesta tipologia ofereix els passos cardinals**. Per ex., un docent podria ensenyar a l'alumne a triar la combinació adequada d'aquestes 8 estratègies segons el discurs d'odi a refutar i l'audiència.

### Troballa 3 — Però NO és gènere curricular reconegut a cap sistema oficial

Cerca a sistemes alemany (Gegenrede), francès, anglès: **el contrarelat NO apareix com a gènere curricular escolar codificat**. És tractat com:
- **Campanya social** (No Hate Speech Movement, COE).
- **Eina educativa** (manuals com Bookmarks).
- **Estratègia digital** (xarxes socials, mitjans).
- **Activitat dins competència ciutadana** (currículums oficials).

**Conseqüència**: si FJE el codifica com a gènere, **seríem un dels primers currículums escolars del món** que ho fa. Això pot ser un actiu (innovació pedagògica documentable) o un risc (sense referents directes).

### Síntesi actualitzada — tres opcions amb pes redistribuït

| Opció | Pes ara | Comentari |
|---|---|---|
| A. Gènere propi `write-contrarelat-odi` | **Augmenta**: Benesch dóna estructura prototípica (8 estratègies = 8 dimensions possibles). | Innovador, sense referent curricular directe. Possible duplicar en counterspeech + counter-narrative. |
| B. Dimensió ampliada del Pas 5 d'opinió | **Manté**: continua sent l'opció més conservadora. | Limitada — perd el matís counterspeech vs alternative speech. |
| C. Subgènere/complement | **Augmenta lleugerament**: encaixaria a `skills/complements/` com a `generate-contrarelat-odi`. | Híbrida; cal clarificar tipus. |

**Recomanació actualitzada (provisional)**: la troballa Benesch fa l'opció A **viable arquitectònicament** (tipologia codificada). Però la manca de precedent curricular escolar oficial requereix prudència. Caldria valorar:

1. Fer **un únic instrument** `generate-contrarelat-odi` que cobreixi tots dos subtipus (counterspeech directe + alternative narrative), amb dimensió "Tipus de resposta" gradada.
2. O fer **dos instruments separats** (counterspeech vs alternative narrative) — més fragmentació però més precisió.

### Connexió crítica amb la dimensió "Recepció crítica" de l'opinió

La proposta inicial de la sessió incloïa afegir 6 dimensions de "Recepció crítica" al M\*.md d'opinió, incloent-hi "**Detecció de discurs d'odi** + **Disseny de rèplica argumentada (refutació toulminiana)**".

Si fem l'opció A (contrarelat com a gènere propi), aquesta dimensió del M\*.md d'opinió **passa a ser només "Detecció" — la "Producció de rèplica" es trasllada al nou instrument**. Coherent arquitectònicament: l'opinió detecta, el contrarelat refuta.

## Aportació conceptual de Miquel 2026-05-25 (vespre tardà) — Dimensió ignasiana del contrarelat

Miquel argumenta que el contrarelat de l'odi **és clau per a FJE pel seu marc institucional propi**. Aquesta perspectiva afegeix una capa que falta a la literatura genèrica del contrarelat (centrada en pragmàtica i comunicació):

### El contrarelat com a expressió natural de la missió ignasiana

Tradició i missió FJE recolzen el contrarelat com a gènere propi:

| Eix ignasià | Aplicació al contrarelat |
|---|---|
| **Justícia social** | El contrarelat és un acte de justícia: rebutjar el discurs que deshumanitza |
| **Reconciliació** | Categoria nuclear ignasiana actual (Congregació General 35-36). El contrarelat NO és combat retòric — és **construir condicions de reconciliació** |
| **Profunditat i discerniment** | El contrarelat ignasià no respon emocionalment ni instrumentalment; **discerneix** quina resposta serveix més la persona i el bé comú |
| **Cerca de la veritat** | El contrarelat és exercici de veritat contra desinformació i mentida (Decret 175/2022 + tradició ignasiana convergeixen) |
| **Recerca del sentit** | El contrarelat reconstrueix sentit on el discurs d'odi destrueix |
| **Fratelli tutti** (encíclica Papa Francesc, 2020) | El contrarelat és pràctica de la "fraternitat universal" enfront de la fragmentació social |
| **4 C's (Conscients, Competents, Compassius, Compromesos)** | El contrarelat exigeix les 4 C's: ser conscient del discurs d'odi, competent per respondre, compassiu vers tots (autor i víctima), compromès amb l'acció |
| **Ratio Studiorum** | Tradició retòrica jesuïta des dels orígens; el contrarelat és l'aplicació contemporània |

### Implicació arquitectònica reforçada

Aquesta dimensió ignasiana **és exclusiva del corpus FJE** i **no apareix a cap altre marc** (Council of Europe, UNESCO, Benesch són operatius però no espirituals). **Aporta valor diferencial al corpus FJE**.

**Conseqüència**: l'opció A (gènere propi) **es reforça molt**. No només per la tipologia codificada de Benesch (8 estratègies), sinó perquè **integra una dimensió pedagògica-espiritual que cap altre currículum cobreix**.

### Possibles passos del contrarelat (versió ignasianament marcada)

Si construïm `generate-contrarelat-odi` com a gènere propi del corpus FJE, els passos podrien combinar Benesch + tradició ignasiana:

| Pas | Inspiració | Funció |
|---|---|---|
| **1. Identificació del discurs d'odi** | Decret 175/2022 + tradició ignasiana (consciència) | Reconèixer mecanisme: estereotip, generalització, deshumanització |
| **2. Discerniment** | Paradigma Pedagògic Ignasià | Triar resposta: respondre o no? Quina forma serveix més? |
| **3. Empatia activa** | Benesch (1) + Fratelli tutti | Reconèixer humanitat de tots els implicats (autor i víctima) |
| **4. Fact-checking / Cerca de la veritat** | Benesch (2) + tradició ignasiana | Corregir falsedats amb fets verificats |
| **5. Narrativa alternativa** | CoE *We CAN!* + Fratelli tutti | Proposar marc de sentit que dignifica |
| **6. Crida a l'acció comunitària** | 4 C's: Compromesos | Convidar l'audiència a l'acció reconciliadora |
| **7. Criteris transversals** | Tradició + currículum | No-atacs personals · Veritat verificable · To respectuós · Fonts citades |
| **8. Autoavaluació metacognitiva** | Examen ignasià | He respost amb justícia? He buscat reconciliació? He estat fidel a la veritat? |

Aquesta estructura **integra naturalment la dimensió ètica que falta als marcs purament tècnics** (Benesch o CoE).

### Posició reforçada — gènere propi amb identitat FJE

L'opció A (gènere propi) **és ara la recomanació clara** amb fonaments combinats:

1. **Tipologia retòrica codificada** (Benesch, 8 estratègies).
2. **Marc institucional** (CoE *We CAN!*, UNESCO, Decret 175/2022 competència ciutadana).
3. **Dimensió ignasiana** (justícia, reconciliació, discerniment, Fratelli tutti, 4 C's).
4. **Buit curricular oficial** (cap currículum escolar el codifica com a gènere) → **oportunitat d'innovació pedagògica documentable** des de FJE.

### Decisió sobre 1 instrument o 2

Miquel s'inclina cap a **1 instrument** (no està segur si dos). Argument a favor:

- El contrarelat com a **acte de reconciliació** és **unitari** des de la perspectiva ignasiana, encara que tingui dues "modalitats retòriques" (directa = counterspeech, indirecta = alternative narrative).
- Fer-ne dos instruments podria fragmentar la pedagogia ètica essencial.
- Solució: **un instrument** `generate-contrarelat-odi` amb **dimensió "Modalitat de resposta"** (directa o indirecta) — la unitat ètica es manté, la flexibilitat retòrica també.

**Recomanació actualitzada (consolidada)**: **A.1** (un sol instrument amb modalitat configurable).

### Cal recerca exhaustiva sobre contrarelat ignasià

**Buit detectat**: cap recerca consultada (CoE, UNESCO, Benesch, Walton) integra perspectiva espiritual/religiosa. Necessitem:

- Documents de la Companyia de Jesús sobre **justícia i reconciliació** com a missió contemporània.
- **JESEDU** (xarxa jesuïta educativa global): preses de posició sobre discurs d'odi i polarització.
- **ICAJE** documents sobre ciutadania global i pluralisme.
- **Fratelli tutti** (encíclica 2020) — aplicació pedagògica al currículum.
- **Sosa** (Padre General SJ) sobre desafiaments educatius contemporanis i polarització.
- **CG 35 i 36** (Congregacions Generals 2008 i 2016) sobre justícia i reconciliació com a "missió completa".

**Acció**: recerca exhaustiva amb Agent + WebSearch focalitzat. **COMPLETADA — vegeu seccions següents**.

## Recerca exhaustiva tradició ignasiana (2026-05-25)

Confirmem que la tradició ignasiana contemporània **té fonamentació explícita** per al contrarelat com a pràctica pedagògica, encara que no usa aquest terme literalment.

### Documents oficials Companyia de Jesús — xarxa conceptual del contrarelat

| Document / Autor | Aportació clau |
|---|---|
| **Congregació General 32** (1975, Decret 4) | "Servei de la fe i promoció de la justícia" — fonament històric |
| **Congregació General 35** (2008, Decret 3) | Categoria de "**fronteres**" geogràfiques, culturals, religioses i existencials — pedagogia fronterera |
| **Congregació General 36** (2016, Decret 1) | ⭐ **"Reconciliació triple amb Déu, amb la humanitat i amb la creació"** — clau pedagògica central |
| **Universal Apostolic Preferences 2019-2029** (SJ) | 4 prioritats: discerniment · exclosos · joves · casa comuna |
| **Adolfo Nicolás** (Mèxic 2010) | "**Globalització de la superficialitat**" — diagnòstic precís del discurs d'odi en xarxes |
| **Arturo Sosa** (JESEDU-Rio 2017) | "Educació jesuïta forma **ciutadans globals capaços de cooperar en la construcció d'un món reconciliat**" |
| **Arturo Sosa** (*La Civiltà Cattolica* 2019) | Polarització com a **pecat estructural** que demana resposta educativa |
| **JESEDU-Global** (2021) | Categoria operativa "**ciutadans globals reconciliadors**" |
| **Papa Francesc**, *Fratelli tutti* (2020) | ⭐ Cap. VI sobre **diàleg i amistat social**; denúncia de "cultura del descart" (FT 18-20), "nacionalismes tancats" (FT 11), bombolles algorítmiques (FT 44-47) |
| **Papa Francesc**, *Querida Amazonia* (2020) | "Inculturació" del discurs — contrarelats arrelats territorialment |
| **Paradigma Pedagògic Ignasià** (ICAJE 1993) | ⭐ Estructura 5 moments: context · experiència · reflexió · acció · avaluació — **arquitectura natural del contrarelat** |
| **Exercicis Espirituals** (Ignasi 1548) | "Composició de lloc" (EE 47) — visualització prèvia · "Examen" (EE 32-43) — metodologia metacognitiva |

### Connexions amb tradicions cristianes i seculars

- **Bonhoeffer**, *Ethik* (1949): "dir la veritat" com a acte situat, no abstracte.
- **Desmond Tutu** i CVR Sud-àfrica (*No Future Without Forgiveness*, 1999): reconciliació com a procés discursiu.
- **Paulo Freire**, *Pedagogia do oprimido* (1968): la paraula com a acció transformadora.
- ⚠️ *Jean Vanier* (L'Arche): citat sovint però desaconsellat com a referent posthumus per revelacions d'abús (informe L'Arche 2023).

### Conclusió — el contrarelat ignasià és viable

**5 conceptes ignasians clau per estructurar el gènere:**

1. **Reconciliació triple** (CG36) — finalitat última del contrarelat.
2. **Discerniment** (EE + UAP 1) — criteri de selecció de resposta.
3. **Composició de lloc** (EE 47) — pas previ d'empatia.
4. **Magis** ("sempre més") — exigència de qualitat, no només reacció.
5. **PPI experiència-reflexió-acció** — bastida didàctica de cinc moments.

**Cautela necessària**: tractar el marc ignasià com a **arquitectura pedagògica** (PPI, examen, magis) i no com a contingut confessional explícit, perquè el gènere també ha de funcionar amb alumnat no creient. Estratègies Benesch operen com a **tàctiques discursives dins l'estructura PPI**.

## Aportació conceptual de Miquel — dimensions civils i de ciutadania global

Miquel afegeix 4 dimensions noves que enriqueixen el marc:

| Dimensió | Connexió amb contrarelat |
|---|---|
| **Participació democràtica** | Contrarelat com a pràctica de la deliberació democràtica (Hess & McAvoy 2015, *The Political Classroom*) |
| **Inclusió** | Contrarelat com a desactivació de marcs excloents |
| **Diversitat** | Contrarelat reconeix i valora multiplicitat de veus (critical race theory aplicada a educació) |
| **Universalitat** | Apel·lació a drets humans universals com a marc comú (*Fratelli tutti* + DUDH 1948) |

Aquestes 4 dimensions estan **alineades amb la tradició ignasiana** (especialment Fratelli tutti i UAP) i amb el **Decret 175/2022** (competència ciutadana) i amb **UNESCO Global Citizenship Education (GCED)** i **Oxfam Global Citizenship Curriculum**.

### Conseqüència per al gènere

Els passos del contrarelat ignasià podrien explicitar aquestes dimensions com a **horitzó pedagògic transversal**, no com a passos discrets. Per ex.: "**Composició de lloc inclusiva**" (Pas 3, considerant la veu de qui ha estat exclòs); "**Apel·lació a universalitat**" (Pas 5, marc *Fratelli tutti*); "**Crida a participació democràtica**" (Pas 6, l'acció ha de ser deliberativa, no impositiva).

## Recerca catalana específica (2026-05-25)

Aportada per **Miquel** (i ampliada per WebSearch):

### Eix català — UAB GREDICS i Albert Izquierdo Grau

| Font | Aportació crítica |
|---|---|
| **Albert Izquierdo Grau (UAB, 2019)** ⭐ | **Tesi doctoral**: *Contrarelats de l'odi a l'ensenyament i aprenentatge de les Ciències Socials. Una recerca interpretativa i crítica a l'Educació Secundària*. Excel·lent Cum Laude. **PROPOSA UN MODEL CONCEPTUAL específic per construir contrarelats a l'ESO** — exactament el referent que necessitàvem. [Tesi a TDX](https://www.tdx.cat/handle/10803/669789) · [Llibre Bellaterra](https://www.todostuslibros.com/libros/contrarelats-de-l-odi-a-l-ensenyament-i-l-aprenentatge-de-les-ciencies-socials-una-recerca-interpretativa-i-critica-a-l-educacio-secundaria_978-84-490-9263-3) |
| **GREDICS** (UAB) — dir. Antoni Santisteban † | Grup de recerca en Didàctica de les Ciències Socials. Projecte *Enseñar y aprender a interpretar conflictos contemporáneos*. Línia activa sobre **construcció de contranarratives crítiques**. |
| **Guillem Suau Gomila** (UdL) | Recerca *L'odi a les xarxes socials* — narratives antifeministes i contranarratives de gènere |

### Eix internacional NLP / IA

| Font | Aportació |
|---|---|
| **Marco Guerini + Serra Sinem Tekiroğlu** (Fondazione Bruno Kessler, Itàlia) | Projecte **CONAN** — dataset de contranarratives i models de generació automàtica |
| **Susan Benesch** (Dangerous Speech Project, Harvard) | Taxonomia 8 estratègies de counterspeech (ja documentada amunt) |
| **Yi-Ling Chung, Brian Wilk, Suman Kalyan Maity, Linhao Zhang** | Generació de contranarratives basades en fets empírics (immigrants, LGTBIQ+) |

### Eix institucional internacional

| Font | Aportació |
|---|---|
| **Consell d'Europa** — *No Hate Speech Movement* | Marc internacional · manuals *Bookmarks* i *We CAN!* |
| **Justice for Prosperity** (comissió CoE) | Estudis pilot d'**eficàcia empírica** dels contrarelats: redueixen radicalització? |
| **UNESCO** — *Think Critically, Click Wisely!* MIL 2021 | Marc d'alfabetització mediàtica |
| **Recomanació CoE CM/Rec(2022)16** | Marc oficial per combatre hate speech |

### Recerca acadèmica internacional sobre counter-narrative pedagogy

- **Henry & Lo (2020)**, *From deliberation to counter-narration: Toward a critical pedagogy for democratic citizenship*. ⭐ Argument central: la pedagogia tradicional deliberativa serveix una "normativitat blanca" del discurs civil i ignora desigualtats estructurals. **Counter-narrative pedagogy ofereix alternativa més justa**.
- **Miller, Liu & Ball (2020)**, *Critical Counter-Narrative as Transformative Methodology for Educational Equity*.
- **Curriculum Inquiry** (2021): *Using counter-narratives to expand from the margins*.

### Síntesi de les fonts noves

L'eix **Izquierdo Grau + GREDICS** és **decisiu** per a la viabilitat del gènere FJE: hi ha **referent doctoral català** sobre el tema, amb model conceptual aplicat a l'ESO. Això:

1. **Treu el risc de "primer al món sense referent"** que vam identificar abans — hi ha precedent català doctoral.
2. **Connecta directament amb el Decret 175/2022** (competència ciutadana, Ciències Socials).
3. **Permet citar precedent català** al M\*.md del nou instrument: "L'instrument segueix el model conceptual proposat per Izquierdo Grau (UAB, 2019) en la tradició GREDICS".
4. **Facilita validació pedagògica**: caldria contactar GREDICS o el mateix Izquierdo Grau (ara UOC) per a validació externa.

## Recomanació consolidada (revisada 2026-05-25 nit)

### Q2 — el contrarelat de l'odi com a gènere propi al corpus FJE

**Opció recomanada**: **A.1 — gènere propi únic** `write-contrarelat-odi` amb modalitat configurable (counterspeech directe / counter-narrative indirecte).

**Fonaments combinats** (cap més robust que abans):
1. **Marc filosòfic-acadèmic**: Walton (argument schemes), Benesch (8 estratègies), Toulmin (refutació).
2. **Marc institucional**: Council of Europe, UNESCO, Decret 175/2022.
3. **Marc ignasià**: CG36 (reconciliació triple), Fratelli tutti, PPI, UAP, 4 C's, Sosa-Rio.
4. **Marc català doctoral**: Izquierdo Grau (UAB 2019) — **model conceptual ja existent**, GREDICS-Santisteban.
5. **Marc de ciutadania global**: UNESCO GCED, Oxfam, Henry & Lo 2020 (counter-narration democràtica).
6. **Marc tecnològic**: Fondazione Bruno Kessler (CONAN dataset) per validació amb generació automàtica.

**Valor diferencial FJE** respecte de tots aquests marcs:
1. **Fonament antropològic de la dignitat** (*Fratelli tutti*), no només drets humans procedimentals.
2. **Metodologia de discerniment ignasià** com a alternativa a la reacció impulsiva.
3. **Avaluació en clau de fruits** (examen ignasià) més enllà de la rúbrica cognitiva.
4. **Integració de 4 dimensions civils**: participació democràtica · inclusió · diversitat · universalitat.

## Pendent abans de tancar

## Pendent abans de tancar

1. **Recerca acadèmica complementària**: cercar autors catalans/espanyols sobre contranarratives a aula (potser Lluís Casado, materials CAC).
2. **Validació pedagògica de Miquel + docents FJE**: si la postura A (gènere propi) és la que té sentit pedagògic al projecte FJE.
3. **Coordinació amb mineriaRAG**: si es decideix A, afegir al corpusFJE com a 35è+ instrument futur. Si es decideix B o C, no toca pipeline.
4. **Connexió amb la decisió sobre la dimensió "Recepció crítica" del M\*.md d'opinió**: la decisió B aquí (dimensió ampliada) està vinculada a si afegim "Detecció de discurs d'odi" com a dimensió 5 de les 6 dimensions de "Recepció crítica" proposades.

---

## Referències inicials (recerca preliminar)

- Keen, E. & Georgescu, M. (2014/rev. 2020). *Bookmarks — Combating Hate Speech Online through Human Rights Education*. Council of Europe.
- Council of Europe (2017). *We CAN! — Taking action against hate speech through counter and alternative narratives*.
- No Hate Speech Movement (2013-2017, Consell d'Europa).
- UNESCO (2021). *Think Critically, Click Wisely! Media and Information Literacy Curriculum*, 2a ed. Mòdul 4 sobre hate speech.
- Decret 175/2022, Generalitat de Catalunya — competència ciutadana.
- eduCAC, Consell de l'Audiovisual de Catalunya — recursos sobre discurs d'odi (verificat per Miquel 2026-05-25).
- Walton, D. (1996, 2008). *Argumentation Schemes*. Cambridge UP.
- Schneuwly, B. & Dolz, J. (1997). *Les genres scolaires*.
- DigComp 2.2 (JRC, 2022).

---

**Estat del fitxer**: parking lot — esperem decisió pedagògica i recerca complementària.
**Connectat amb**: [parking_opinio_vs_preferencies_2026-05-25.md](parking_opinio_vs_preferencies_2026-05-25.md), [proposta_arquitectura_skill_pipeline_8juny.md](proposta_arquitectura_skill_pipeline_8juny.md), [handoff_mineriaRAG_consolidacio_33_2026-05-25.md](handoff_mineriaRAG_consolidacio_33_2026-05-25.md).
**Propera revisió**: després de la Fase A i la decisió sobre opinio-vs-preferencies (resolució conjunta).

---

## ✅ DECISIÓ DE MIQUEL — 2026-05-25 nit

**Opció A.1 acceptada**: gènere propi únic `write-contrarelat-odi` (o nom equivalent) **amb modalitat configurable**:
- **Counterspeech directe** (resposta puntual a un discurs d'odi concret).
- **Counter-narrative indirecte / alternative speech** (canvi de marc del debat).

**NO** són dos gèneres separats. **SÍ** és un sol instrument amb dimensió interna "Modalitat de resposta".

**Característiques previstes:**
- `categoria_principal: generes` (a confirmar — podria ser `mediacio` si es prioritza la funció social de prevenció)
- `mecr_range: [A1, A2, B1, B2, C1]` (no aplicable a pre-A1; com a opinió)
- 8 passos inspirats en la combinació Izquierdo Grau (UAB) + Benesch + PPI ignasià.

**Coordinació amb mineriaRAG**: pendent (passar handoff perquè afegeixi `write-contrarelat-odi` com a 35è instrument al corpusFJE).

**Validació externa pendent**: contactar Albert Izquierdo Grau (UOC actualment) i grup GREDICS (UAB, continuïtat post-Santisteban) per validació externa del model conceptual abans de publicar a corpusFJE.
