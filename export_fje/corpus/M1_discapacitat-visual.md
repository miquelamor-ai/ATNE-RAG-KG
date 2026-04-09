---
modul: M1
titol: "Alumnat amb discapacitat visual"
tipus: caracteristica
subtipus: constitutiva
descripcio: "Discapacitat visual (baixa visió i ceguesa): classificació OMS/ICD-11, criteris ONCE, manifestacions escolars, tiflotecnologia, CREDV-ONCE i marc normatiu D150/2017"
review_status: revisat
locked: true
generat_at: 2026-03-18T15:27:31
actualitzat_at: 2026-03-27T22:00:00
variables_configurables:
  - nom: grau
    etiqueta: "Grau de discapacitat visual"
    tipus: enum
    valors: [baixa_visio_moderada, baixa_visio_greu, ceguesa]
    obligatori: true
    defecte: baixa_visio_moderada
    descripcio: "Baixa visió moderada: AV < 0,3. Baixa visió greu: AV < 0,12. Ceguesa: sense percepció de llum o AV < 0,02"
    impacte: "Baixa visió: ampliació, contrast, ajudes òptiques. Ceguesa: Braille, lector de pantalla, estructura lineal, descripcions d'imatges"
---

# 1. CONTINGUT ESPECÍFIC

## Definició i classificació

La **discapacitat visual** comprèn qualsevol alteració de la funció visual que, un cop aplicada la millor correcció òptica possible, afecta significativament la realització d'activitats de la vida quotidiana, l'aprenentatge o la participació social.

S'avalua a partir de dos paràmetres fonamentals:
- **Agudesa visual (AV):** capacitat per discriminar detalls i formes a distància determinada (es mesura en percentatge o fracció Snellen).
- **Camp visual (CV):** amplitud del camp de visió perifèric (es mesura en graus).

### Classificació OMS / ICD-11

| Categoria | Agudesa visual (millor ull, millor correcció) | Camp visual | Implicació funcional |
|:---|:---|:---|:---|
| **Visió normal** | ≥ 0,8 (80%) | ≥ 120° | Sense restriccions funcionals |
| **Baixa visió moderada** | < 0,3 (30%) | < 60° | Dificultats en tasques d'alta exigència visual |
| **Baixa visió greu** | < 0,12 (12%) | < 20° | Limitació important; necessita ajudes òptiques |
| **Baixa visió profunda** | < 0,05 (5%) | < 10° | Dependència d'ajudes i adaptació de materials |
| **Ceguesa quasi total** | < 0,02 (2%) | < 5° | Ús predominant de canals no visuals |
| **Ceguesa total** | Sense percepció de llum | 0° | Codi Braille i tiflotecnologia com a eines principals |

> **Criteri ONCE per a afiliació:** AV ≤ 0,1 (10%) o CV ≤ 10°, amb la millor correcció òptica possible.

### Codis diagnòstics

| Sistema | Codi | Denominació |
|:---|:---|:---|
| **ICD-11** (OMS, 2019) | **9D90** | Visual impairment (inclou low vision i blindness) |
| **ICD-10** (antic) | H54 | Visual impairment including blindness |

## Tipologies i etiologia

### Per moment d'aparició

| Tipus | Descripció | Implicació educativa clau |
|:---|:---|:---|
| **Congènita** | Present des del naixement o primers mesos | No hi ha memòria visual; aprenentatge íntegrament multisensorial des de l'inici |
| **Adquirida primerenca** | Apareix en els primers anys de vida | Pot haver-hi traces de memòria visual; adaptació progressiva |
| **Adquirida tardana** | Apareix en edat escolar o adulta | L'alumne té conceptes visuals consolidats; l'adaptació és diferent |

### Per causa principal (freqüents en edat escolar)

| Causa | Notes |
|:---|:---|
| Retinopatia de la prematuritat | Causa principal en nens prematurs |
| Albinisme ocular | Baixa visió moderada; fotofòbia freqüent |
| Nistagme | Moviment involuntari dels ulls; afecta l'agudesa |
| Glaucoma congènit | Augment de la pressió intraocular; pot afectar el CV |
| Atròfia òptica | Dany al nervi òptic; variabilitat funcional alta |
| Discapacitat visual cortical (DVC/CVI) | D'origen neurològic central; freqüent en alumnes amb pluridiscapacitat |

## Manifestacions a l'escola

### Senyals d'alerta per etapes

| Etapa | Senyals d'alerta |
|:---|:---|
| **Ed. Infantil (3-6)** | S'acosta molt als objectes; frota els ulls; evita tasques de motricitat fina; no reconeix cares a distància; no segueix la pilota |
| **Ed. Primària (6-12)** | Lletra molt gran o molt petita; perd el fil en la lectura; fatiga visual; dificultats amb la pissarra; postura atípica en llegir |
| **ESO (12-16)** | Fatiga en tasques llargues de lectura; dificultats amb materials no adaptats; evita activitats esportives amb pilota |

### Per àmbits funcionals

| Àmbit | Alumnat amb baixa visió | Alumnat amb ceguesa |
|:---|:---|:---|
| **Lectoescriptura** | Lletra ampliada; ajudes òptiques (lupa, monocular); fatiga visual | Codi Braille; línia Braille; lector de pantalla |
| **Matemàtiques** | Materials en format ampliat; calculadora parlant | Material tàctil; àbac; calculadora parlant |
| **Educació Física** | Adaptació de regles; contrastar colors; evitar llum directa | Parella de referència; indicadors sonors; activitats sense component de persecució visual |
| **Ús de les TIC** | Magnificadors de pantalla (ZoomText, Windows Magnifier) | Lectors de pantalla (JAWS, NVDA); línia Braille |
| **Organització personal** | Marques tàctils d'organització; llocs fixes per als materials | Entrenament en orientació i mobilitat (bastó blanc) |

## Barreres d'aprenentatge

- **Accés a la informació visual:** El 80-90% de la informació escolar es transmet per via visual (pissarra, llibres, projeccions, gràfics). L'alumnat amb DV té un accés reduït o nul a aquest canal.
- **Fatiga visual:** En baixa visió, l'esforç visual compensatori genera fatiga que redueix el rendiment al llarg de la jornada.
- **Materials no adaptats:** Llibres de text, fitxes, exàmens i materials digitals sense adaptació de format (cos de lletra, contrast, alternatives textuals a imatges).
- **Ritme de treball:** La lectura en Braille o amb magnificació és més lenta; l'alumne necessita més temps per a les mateixes tasques.
- **Orientació espacial:** Dificultats per moure's en espais desconeguts, canvis de distribució de l'aula, sortides.
- **Accés a la comunicació no verbal:** Pèrdua de gestos, expressions facials i informació contextual visual que els companys capten de forma automàtica.
- **Participació en activitats col·lectives:** Esports amb pilota, experiments de laboratori, sortides, activitats amb component visual dominant.

## Necessitats prioritàries

1. **Adaptació de materials:** Tot material ha d'arribar a l'alumne en format accessible ABANS de la sessió (ampliat, Braille, audiodescripció, format digital compatible amb lector de pantalla).
2. **Tiflotecnologia:** Accés a eines específiques (línia Braille, lector de pantalla JAWS/NVDA, magnificador ZoomText, anotador parlant) i formació en el seu ús.
3. **Suport CREDV:** Mestre/a itinerant del CREDV-ONCE per a l'ensenyament del Braille, la tiflotecnologia, l'orientació i mobilitat, i l'assessorament al centre.
4. **Ubicació a l'aula:** Lloc preferent (primera fila, bona il·luminació, lluny de contrallum) i estabilitat de la distribució del mobiliari.
5. **Temps addicional:** En avaluacions i tasques de lectoescriptura. Referència: 1/3 de temps addicional com a mínim (ONCE).
6. **Verbalització sistemàtica:** El docent ha de verbalitzar TOT el que escriu a la pissarra, projecta o assenyala. "Ho estic escrivint a la pissarra" no és suficient; cal dir QUÈ s'escriu.
7. **Orientació i mobilitat:** Entrenament en desplaçaments autònoms pel centre i sortides (responsabilitat del CREDV en coordinació amb el tutor).

## Fortaleses a aprofitar

L'alumnat amb discapacitat visual desenvolupa compensatòriament capacitats que són un actiu a l'aula:
- **Memòria auditiva i verbal:** Retenció superior d'informació oral; capacitat d'escoltar i processar explicacions orals complexes.
- **Pensament analític seqüencial:** La lectura en Braille entrena un processament lineal i precís que afavoreix la comprensió textual detallada.
- **Sensibilitat tàctil i propioceptiva:** Capacitat de discriminació tàctil superior, útil en ciències experimentals, arts plàstiques tàctils i tecnologia.
- **Autonomia personal:** L'entrenament en orientació i mobilitat fomenta la presa de decisions i la resolució de problemes en contextos reals.
- **Expressió oral:** Sovint presenten una fluïdesa verbal i una capacitat de síntesi oral superior a la mitjana per edat.

## Perfils associats i comorbiditats

| Perfil associat | Prevalença | Implicació |
|:---|:---|:---|
| **Pluridiscapacitat** | Freqüent en DVC/CVI | Requereix abordatge multidisciplinar; CREDV coordina amb EAP i serveis de salut |
| **Discapacitat auditiva (sordceguesa)** | Poc freqüent però molt greu | Comunicació tàctil (dactilobraille); suport CREDV + CREDA |
| **TEA** | Minoritari | La DV pot emmascarar senyals de TEA; avaluació especialitzada |
| **Discapacitat intel·lectual** | En algunes etiologies congènites | Adaptació curricular significativa + adaptació de format |

> **Alerta:** No confondre mai les dificultats derivades de la manca d'adaptació de materials amb una discapacitat intel·lectual. Un alumne amb DV pot tenir un rendiment baix perquè no hi veu, NO perquè no hi arriba cognitivament.

## Principis d'actuació

1. **Anticipació:** Tot material adaptat ha d'estar disponible ABANS de la sessió. La improvisació exclou.
2. **Verbalització:** El docent ha de fer explícit verbalment tot el que és visual: gràfics, esquemes, canvis a la pissarra, indicacions gestuals.
3. **Multisensorialitat:** Utilitzar canals tàctils, auditius i cinestèsics de forma sistemàtica, no com a recurs d'última hora.
4. **Normalització:** L'alumne ha de participar en les mateixes activitats que els companys, amb les adaptacions necessàries. No excloure de sortides, educació física o laboratori.
5. **Coordinació CREDV:** El mestre itinerant és l'aliat principal del tutor; la comunicació ha de ser fluida, regular i bidireccional.
6. **Autonomia progressiva:** L'objectiu és que l'alumne sigui autònom en l'ús de la tiflotecnologia i en la mobilitat, no que depengui permanentment d'un adult.

## Línies vermelles

- **No excloure de cap activitat per "raons pràctiques":** No treure l'alumne d'educació física, sortides o laboratori perquè "és complicat adaptar-ho". **Per què?** El D150/2017 garanteix la participació en totes les activitats; l'exclusió vulnera drets i empobreix l'experiència educativa.
- **No parlar sobre l'alumne com si no hi fos:** Adreçar-se directament a l'alumne, no al company o a l'acompanyant. **Per què?** La discapacitat visual no afecta la comprensió ni la comunicació; parlar per sobre de l'alumne és una forma de discriminació.
- **No assumir que "ja s'ho arreglarà":** Si no es proporciona material adaptat, no es pot esperar un rendiment acadèmic adequat. **Per què?** L'alumne amb DV no "necessita esforçar-se més"; necessita que l'entorn s'adapti.
- **No tocar l'alumne sense avisar:** Sempre avisar verbalment abans de qualsevol contacte físic (guiar, ajudar a seure). **Per què?** El contacte inesperat genera sobresalt i inseguretat; el respecte al cos és fonamental.
- **No modificar la distribució de l'aula sense avisar:** L'alumne amb DV té un mapa mental de l'espai. **Per què?** Un canvi no anunciat pot provocar desorientació, caigudes i ansietat.

## Marc normatiu català

| Norma | Aplicació |
|:---|:---|
| **Decret 150/2017** | Ceguesa i baixa visió greu → **NEE** (art. 3.2.a) → **PI obligatori** (art. 18). Baixa visió moderada → NESE → mesures addicionals (art. 7). |
| **D150/2017, art. 14** | L'EAP coordina l'avaluació psicopedagògica i la derivació al CREDV-ONCE. |
| **D150/2017, art. 9** | Mesures intensives: mestre/a itinerant del CREDV com a recurs especialitzat. |
| **DOIGC 2025-2026** | Protocols de derivació i coordinació EAP–CREDV–centre. |
| **Conveni Dept. Educació – ONCE** | Base legal del CREDV-ONCE com a servei educatiu específic de Catalunya. |
| **Llei 17/2020** | Accessibilitat universal; eliminació de barreres físiques, comunicatives i digitals. |

## El CREDV-ONCE: servei de referència

El **Centre de Recursos Educatius per a Deficients Visuals (CREDV-ONCE)** és el servei educatiu específic de Catalunya per a l'alumnat amb ceguesa o baixa visió greu, fruit del conveni Departament d'Educació–ONCE. Seu central: Barcelona. Subseus: Girona, Lleida i Tarragona.

### Àmbits d'intervenció

| Àmbit | Funcions principals |
|:---|:---|
| **Alumnat i famílies** | Atenció primerenca (0-3 anys); avaluació funcional visual; entrenament Braille, tiflotecnologia i orientació/mobilitat; suport emocional |
| **Centres i professorat** | Assessorament sobre adaptació de materials; formació del claustre; préstec de material tiflotècnic; modelatge d'estratègies inclusives |
| **Zona educativa** | Coordinació amb EAP, serveis socials i salut; orientació a l'etapa postobligatòria |

### Grups d'atenció del CREDV

| Grup | Criteri | Modalitat de suport |
|:---|:---|:---|
| **Atenció directa intensiva** | Ceguesa total o baixa visió greu; ús de Braille | Mestre/a itinerant al centre; sessions setmanals |
| **Atenció directa moderada** | Baixa visió moderada amb impacte acadèmic significatiu | Suport periòdic + assessorament al tutor/a |
| **Seguiment i assessorament** | Baixa visió lleu o estabilitzada | Seguiment anual; recursos i orientació al centre |

### Protocol d'accés al CREDV

1. Detecció a l'aula o informe oftalmològic → tutor/a informa EAP
2. EAP valora i emet informe psicopedagògic
3. Derivació formal al CREDV-ONCE
4. Avaluació funcional visual per part del CREDV
5. Assignació de grup d'atenció i pla de suport
6. Coordinació trimestral: CREDV–tutor/a–EAP–família

## Tiflotecnologia: eines clau

| Eina | Funció | Quan |
|:---|:---|:---|
| **Línia Braille** | Lectura tàctil de text digital | Ceguesa; lectura i escriptura |
| **JAWS / NVDA** | Lector de pantalla (veu sintetitzada) | Ceguesa; accés a TIC |
| **ZoomText** | Magnificador de pantalla | Baixa visió; ús de l'ordinador |
| **Lupa electrònica** | Ampliació de text imprès en temps real | Baixa visió; lectura de materials no digitals |
| **Anotador parlant (Braille Sense)** | Presa d'apunts en Braille amb sortida de veu | Ceguesa; classe, estudi |
| **Magnificador Windows** | Integrat al SO; ampliació bàsica | Baixa visió; solució ràpida sense instal·lació |
| **Calculadora parlant** | Resultat per veu | Tots els graus; matemàtiques |
| **Impressora Braille** | Impressió de materials en relleu | Ceguesa; adaptació de materials |

# 2. CONNEXIONS AMB ALTRES DOCUMENTS DEL CORPUS

- **M1_model-caracteritzacio-diversitat.md** → Marc de 3 nivells; discapacitat visual = característica constitutiva
- **M1_neurodiversitat-NESE.md** → Ceguesa/baixa visió greu = NEE dins D150/2017
- **M1_plans-individuals-PAD-PI.md** → PI obligatori per a NEE; el CREDV participa en l'elaboració
- **M1_discapacitat-auditiva.md** → Perfil associat: sordceguesa (co-ocurrència)
- **M2_mesures-suports-inclusius.md** → Escala de mesures: universals (DUA) → addicionals → intensives (PI + CREDV)
- **M2_carrega-cognitiva-adaptacio-textos.md** → Adaptació de textos: format ampliat, estructura lineal, descripcions alternatives
- **M5_tecnopedagogia** → Accessibilitat digital: WCAG 2.1, lectors de pantalla, disseny universal
- **M9_normativa-inclusio.md** → D150/2017, Llei 17/2020 (accessibilitat)

# 3. DETECCIÓ (Variables de Context)

**Senyals del docent:**
- "Tinc un alumne que s'acosta molt a la pissarra i no copia bé els apunts."
- "L'alumne evita les activitats amb lletra petita i triga molt a llegir."
- "Necessito saber com adaptar els exàmens per a un alumne amb baixa visió."
- "L'alumne amb ceguesa acaba d'arribar i no sé com preparar els materials."
- "El mestre itinerant del CREDV ve setmanalment; com coordino les adaptacions?"

**Senyals de l'alumne:**
- "No veig bé la pissarra, encara que m'assegui a primera fila."
- "Em canso molt de llegir i em fa mal el cap."
- "No puc seguir la presentació perquè les lletres són massa petites."
- "Necessito més temps per fer l'examen perquè llegeixo amb Braille."
- "Com puc accedir a aquest PDF amb el lector de pantalla?"

**Senyals de context:**
- Inici de curs amb alumne amb DV que necessita adaptació d'aula i materials.
- Activitat amb component visual dominant (laboratori, mapes, gràfics, vídeo sense audiodescripció).
- Examen o prova escrita amb format estàndard (cos de lletra 10-11, interlineat simple).
- Sortida escolar a espai desconegut per a l'alumne.
- Canvi de distribució de l'aula o d'aula.

**Anti-senyals:**
- L'alumne porta ulleres i no presenta dificultats funcionals significatives (visió corregida dins rang normal).
- Les dificultats de l'alumne són exclusivament de comprensió lectora però no de percepció visual (considerar dislèxia, TDL).
- L'alumne manifesta "no veure" només en situacions d'avaluació (explorar component emocional).

# 4. HEURÍSTIQUES I RAONAMENT PER A L'AGENT

**Principi general:** L'adaptació per a l'alumnat amb DV és fonamentalment d'accés al format, NO de simplificació del contingut. L'exigència curricular és la mateixa; el que canvia és COM arriba la informació.

## Heurístiques per a l'Agent DOCENT

### H1: Adaptació de format, NO de contingut
- **Quan aplica:** Quan un docent demana "com simplifico els materials per a l'alumne amb DV".
- **Raonament:** La DV no és una discapacitat intel·lectual. L'alumne necessita que la informació li arribi per un canal accessible (ampliat, Braille, oral, tàctil), però el nivell d'exigència no ha de baixar. Si el docent simplifica, està creant una barrera nova (curricular) sobre la que ja existeix (sensorial).
- **Resposta tipus:** "No cal simplificar el contingut. Cal adaptar el format: lletra Arial 18-22pt, interlineat 1,5, contrast alt (negre sobre blanc o blanc sobre negre), alternatives textuals per a imatges. Si l'alumne usa Braille, el material s'ha d'enviar al CREDV amb antelació perquè el transcriguin."

### H2: Verbalització sistemàtica
- **Quan aplica:** Quan un docent projecta, escriu a la pissarra o fa servir gestos indicatius ("això", "aquí", "com veieu").
- **Raonament:** Díctics i gestos són invisibles per a l'alumne amb DV. Cada "mireu" o "com veieu" és una microexclusió. El docent ha d'adquirir l'hàbit de fer explícit verbalment TOT el que és visual.
- **Resposta tipus:** "Substitueix 'com podeu veure al gràfic' per 'al gràfic de barres que tenim a la pantalla, l'eix X mostra els anys 2020-2025 i l'eix Y mostra el nombre d'alumnes; la barra més alta correspon al 2024 amb 350 alumnes'. Descriu, no assenyalis."

### H3: Temps addicional en avaluació
- **Quan aplica:** Quan un docent prepara un examen per a un grup que inclou un alumne amb DV.
- **Raonament:** La lectura en Braille és ~3x més lenta que la lectura visual. La lectura amb magnificació és ~2x més lenta. L'ONCE recomana un mínim d'1/3 de temps addicional, però pot arribar al doble segons el grau.
- **Resposta tipus:** "Dona un mínim d'1/3 de temps addicional (si l'examen és de 60 min, dona 80 min). Per a alumnes amb ceguesa i lectura Braille, considera el doble de temps. Format: Arial 18+, interlineat 1,5, un exercici per pàgina, enumera clarament les preguntes."

## Heurístiques per a l'Agent ALUMNE

### H1: Gestió de la fatiga visual
- **Quan aplica:** Quan l'alumne amb baixa visió reporta cansament, mal de cap, visió borrosa després de llegir.
- **Raonament:** La fatiga visual és acumulativa al llarg del dia. No és mandra; és un límit fisiològic. L'alumne pot necessitar alternar entre lectura visual i auditiva, o fer pauses regulars.
- **Resposta tipus:** "Pots alternar entre llegir i escoltar (activa el lector de pantalla per als textos llargs). Fes pauses de 5 min cada 20-30 min de lectura. Si el text és important i llarg, demana'l en format digital per poder ampliar-lo al teu gust."

### H2: Autoadvocacia
- **Quan aplica:** Quan l'alumne no rep el material adaptat, no entén alguna cosa visual, o necessita un suport que no se li ofereix.
- **Raonament:** L'alumne ha d'aprendre a demanar el que necessita sense sentir-se una càrrega. L'autoadvocacia és una competència clau per a la vida adulta.
- **Resposta tipus:** "Tens dret a rebre el material adaptat ABANS de la classe. Si no te l'han donat, pots dir al professor/a: 'Necessito el material en format ampliat/digital per poder seguir la classe.' No és una molèstia; és un dret recollit al teu PI."

# 5. FONTS

| # | Referència | Rellevància |
|---|-----------|-------------|
| 1 | OMS (2019). *ICD-11: International Classification of Diseases, 11th Revision.* Codi 9D90. | Classificació diagnòstica de referència |
| 2 | ONCE (2023). *Criteris d'afiliació i serveis educatius.* | Criteris AV ≤ 0,1 / CV ≤ 10° |
| 3 | CREDV-ONCE (2024). *Guia de serveis educatius per a alumnat amb discapacitat visual a Catalunya.* | Grups d'atenció, protocol d'accés |
| 4 | Decret 150/2017, de 17 d'octubre, de l'atenció educativa a l'alumnat en el marc d'un sistema educatiu inclusiu. DOGC 7477. | NEE, PI obligatori, mesures intensives |
| 5 | Llei 17/2020, de 22 de desembre, de modificació de la Llei 13/2014, d'accessibilitat. DOGC 8303. | Accessibilitat universal |
| 6 | DOIGC 2025-2026. Departament d'Educació. *Educació inclusiva: protocols de derivació.* | Coordinació EAP–CREDV–centre |
| 7 | Corn, A. L. & Erin, J. N. (2010). *Foundations of Low Vision: Clinical and Functional Perspectives.* AFB Press. | Marc teòric de la baixa visió funcional |
| 8 | Holbrook, M. C. & Koenig, A. J. (2000). *Foundations of Education: Instructional Strategies for Teaching Children and Youths with Visual Impairments.* AFB Press. | Estratègies educatives per a DV |
| 9 | WCAG 2.1 (2018). *Web Content Accessibility Guidelines.* W3C Recommendation. | Accessibilitat digital |
| 10 | Barraga, N. C. & Erin, J. N. (2001). *Visual Handicaps and Learning.* Pro-Ed. | Impacte de la DV en l'aprenentatge |

*10 fonts · document revisat manualment amb contingut clínic i normatiu*

---

## 6. INSTRUCCIONS D'ADAPTACIÓ TEXTUAL PER A L'LLM

### Barrera nuclear
**Percepció visual**: L'alumnat amb discapacitat visual té com a barrera principal l'accés a la informació presentada visualment. Les adaptacions per a l'LLM se centren en l'estructura semàntica del text (encapçalaments, alt-text), ja que la majoria d'adaptacions són CSS/frontend (contrast, mida, zoom).

### Instruccions per al prompt LLM

```
PERFIL: Discapacitat Visual
- Estructura semàntica amb encapçalaments (H1-H3) per lector de pantalla
- Alt-text descriptiu per a cada element visual mencionat
- NO dependre d'elements visuals (colors, posicions) per transmetre informació
```

### Mapa barrera → instruccions (prioritzat)

| Prioritat | Instruccions activades | Justificació (barrera) |
|---|---|---|
| **1a (percepció)** | H-18 (alt-text imatges), H-19 (estructura semàntica H1-H3), I-06 (contrast alt), I-08 (reescalat) | Barrera nuclear: percepció |
| **2a (estructura)** | B-02 (blocs amb títol), B-14 (taules per comparació) | Navegació amb lector de pantalla |

**Nota**: La majoria d'adaptacions per a disc. visual són CSS/FE (contrast, mida tipografia, zoom), no de prompt LLM. L'LLM ha de garantir: estructura semàntica, descripcions textuals d'elements visuals, i no dependre de color o posició per transmetre significat.
