---
modul: M1
titol: "Trastorn del Desenvolupament del Llenguatge (TDL)"
tipus: caracteristica
subtipus: constitutiva
descripcio: "TDL: definició CATALISE (Bishop et al., 2017), dimensionalitat clínica, components afectats (morfosintaxi, semàntica, pragmàtica, discurs, comprensió lectora), variables configurables per modalitat i grau de severitat"
review_status: revisat
generat_at: 2026-03-18T15:27:36
actualitzat_at: 2026-03-26T22:00:00
variables_configurables:
  - nom: modalitat
    etiqueta: "Modalitat afectada"
    tipus: enum
    valors: [comprensiu, expressiu, mixt]
    obligatori: true
    defecte: mixt
    descripcio: "Comprensiu: dificultats per entendre el que s'escolta o es llegeix. Expressiu: dificultats per produir missatges organitzats i gramaticalment correctes. Mixt: ambdues modalitats afectades (perfil més freqüent)"
    impacte: "Comprensiu: simplificar text d'entrada, frases curtes, vocabulari freqüent. Expressiu: simplificar consignes de producció, modelar estructura esperada, oferir andamiatge. Mixt: ambdues estratègies"
  - nom: morfosintaxi
    etiqueta: "Component morfosintàctic afectat"
    tipus: boolean
    obligatori: false
    defecte: false
    descripcio: "Dificultats amb conjugació verbal, pronoms, concordances, connectors i oracions subordinades"
    impacte: "Usar estructures SVO simples, evitar passives i subordinades, oferir plantilles gramaticals en producció"
  - nom: semantica
    etiqueta: "Component semàntic/lèxic afectat"
    tipus: boolean
    obligatori: false
    defecte: false
    descripcio: "Pobresa de vocabulari, dificultats d'evocació lèxica, accés lent a paraules poc freqüents"
    impacte: "Vocabulari d'alta freqüència, definicions integrades al text, bancs de paraules en producció, evitar sinònims innecessaris"
  - nom: pragmatica
    etiqueta: "Component pragmàtic afectat"
    tipus: boolean
    obligatori: false
    defecte: false
    descripcio: "Dificultats en l'ús funcional del llenguatge: inferències, llenguatge no literal, gestió de torns, adequació al context"
    impacte: "Evitar consignes amb llenguatge figurat o ambigu, explicitar el context comunicatiu, estructurar rols en dinàmiques de grup"
  - nom: discurs_narrativa
    etiqueta: "Component discursiu/narratiu afectat"
    tipus: boolean
    obligatori: false
    defecte: false
    descripcio: "Dificultats per organitzar i seqüenciar informació en textos llargs: coherència, cohesió, estructura narrativa"
    impacte: "Guions d'estructura explícits, segmentació amb etiquetes de funció, mapes conceptuals com a suport de producció"
  - nom: comprensio_lectora
    etiqueta: "Comprensió lectora específica afectada"
    tipus: boolean
    obligatori: false
    defecte: false
    descripcio: "Tendència a usar estratègies semàntiques saltant-se paraules funció (articles, preposicions, conjuncions); comprensió inestable en textos llargs"
    impacte: "Ressaltar paraules funció clau, verificar comprensió literal abans d'inferencial, no assumir comprensió per lectura fluida"
  - nom: grau
    etiqueta: "Grau de severitat"
    tipus: enum
    valors: [lleu, moderat, sever]
    obligatori: true
    defecte: moderat
    descripcio: "Lleu: dificultats compensables amb suport i estructura. Moderat: impacte notable, requereix adaptació sistemàtica. Sever: dificultats persistents i significatives, pot requerir suport AAC"
    impacte: "Lleu: simplificació moderada, estructura clara. Moderat: reducció sintàctica, suport visual explícit, consignes molt curtes. Sever: text mínim, frases d'una clàusula, andamiatge màxim"
  - nom: bilingue
    etiqueta: "Context bilingüe/plurilingüe"
    tipus: boolean
    obligatori: false
    defecte: false
    descripcio: "L'alumne/a rep instrucció en una llengua que no és la seva L1. El bilingüisme no causa TDL, però pot intensificar les dificultats en la llengua vehicular"
    impacte: "Incrementar suport semàntic addicional, reduir complexitat morfosintàctica per sobre del grau base, no atribuir tots els errors al TDL"
---

### 1. CONTINGUT ESPECÍFIC

#### Descripció del tret

##### Definició i marc conceptual

El **Trastorn del Desenvolupament del Llenguatge (TDL)** és un trastorn del neurodesenvolupament caracteritzat per dificultats persistents en l'adquisició i l'ús del llenguatge — comprensiu i/o expressiu — que no s'expliquen per causes neurològiques adquirides, sensorials, motrius ni per un context socioeducatiu desfavorable. La terminologia actual prové del consens internacional **CATALISE** (Bishop et al., 2016, 2017), que va substituir l'anterior TEL (Trastorn Específic del Llenguatge). La raó del canvi és conceptual: "específic" implicava que el TDL era un trastorn pur i aïllat, quan la recerca ha demostrat que és altament heterogeni i de límits difusos.

La prevalença és del **7,6% de la població escolar**, fet que el converteix en un dels trastorns del neurodesenvolupament més freqüents a les aules — més prevalent que el TEA i el TDAH per separat. Apareix sovint en comorbiditat amb dislèxia, TDAH i TEA.

##### El TDL com a espectre, no com a tipologia

La recerca actual desaconsella classificar el TDL en subtipus discrets i estables. Els perfils lingüístics dels alumnes no es reprodueixen de manera consistent: un alumne pot tenir morfosintaxi molt afectada però coherència narrativa relativament preservada, o dificultats severes de comprensió amb producció expressiva acceptable. Per tant, el model adequat de configuració **no és un menú de "tipus de TDL"**, sinó una combinació modular de components afectats amb grau de severitat independent.

##### Prevalença i perfil

- Afecta el **7,6% de la població escolar** en els criteris CATALISE
- Alta comorbiditat: **dislèxia** (fins al 50%), **TDAH** (25-40%), **TEA** (subgrup)
- **No s'associa a baixa intel·ligència**: la capacitat cognitiva no verbal sovint és normativa o superior
- Persisteix a l'adolescència i l'edat adulta en la majoria de casos, tot i que les manifestacions canvien
- El bilingüisme **no causa TDL** però pot complicar la detecció si no s'avalua en totes dues llengües

##### Components del llenguatge afectats

El TDL pot afectar un o diversos components de manera independent i en diferent grau:

| Component | Manifestació principal | Impacte en tasques escrites i orals |
|---|---|---|
| **Morfosintaxi** | Errors de conjugació, concordança, ús de connectors i subordinades | Producció escrita pobra estructuralment; comprensió falla en frases complexes |
| **Semàntica / Vocabulari** | Pobresa lèxica, dificultats d'evocació, menys flexibilitat en l'ús de paraules noves | Resposta amb vocabulari molt bàsic; comprensió falla en textos amb lèxic específic |
| **Pragmàtica** | Inferències, llenguatge no literal, adequació al context comunicatiu | Dificultats en dinàmiques de grup, exposicions, consignes implícites |
| **Discurs / Narrativa** | Coherència i seqüenciació en textos llargs | Textos escrits sense estructura; problemes en projectes, informes i exposicions |
| **Comprensió lectora** | Ús d'estratègies semàntiques compensatòries, saltant-se paraules funció | Comprensió inestable malgrat lectura fluida aparent |

##### Grau de severitat

| Grau | Descripció clínica | Implicació per a l'assistent |
|---|---|---|
| **Lleu** | Dificultats presents però compensables; sovint passa desapercebut | Estructura clara, frases simples, vocabulari freqüent |
| **Moderat** | Impacte notable en comprensió i/o producció; requereix adaptació sistemàtica | Reducció sintàctica, suport visual, consignes d'un sol pas |
| **Sever** | Dificultats persistents significatives; pot requerir suport augmentatiu i alternatiu | Text mínim, frases simples, andamiatge màxim, opcions no verbals |

#### Manifestació per etapa educativa

| Etapa | Manifestacions lingüístiques | Impacte en tasques | Impacte emocional |
|---|---|---|---|
| **Infantil (I3–I5)** | Retard en l'adquisició del vocabulari; frases curtes i mal estructurades; dificultat per seguir instruccions orals | Dificultats en rutines que depenen del llenguatge | Frustració en comunicar necessitats |
| **Primària (1r–3r)** | Errors morfosintàctics persistents; vocabulari pobre; comprensió oral inferior als iguals | Problemes en comprensió lectora inicial; textos escrits molt simples | Baixa autoestima lingüística |
| **Primària (4t–6è)** | Dificultats amb textos narratius i expositius; problemes de discurs i cohesió | Treballs escrits pobres; exposicions orals desorganitzades | Evitació de tasques de producció |
| **ESO** | Dificultats en textos acadèmics complexos; problemes amb inferències i pragmàtica | Redaccions, treballs per projectes, debats; impacte en totes les àrees curriculars | Frustració, comparació negativa amb iguals |
| **Batxillerat / FP** | Dificultat en llengua tècnica i especialitzada; producció escrita estructuralment feble | Informes, treballs de recerca, defensa oral de projectes | Síndrome de l'impostor; dubtes vocacionals |

#### Barreres d'aprenentatge

- **Comprensió d'instruccions:** Instruccions multistep, consignes amb subordinades o condicionals i vocabulari específic representen una barrera d'accés directa
- **Producció escrita:** La dificultat morfosintàctica i lèxica fa que el producte escrit no reflecteixi la capacitat conceptual real de l'alumne
- **Velocitat de processament lingüístic:** El temps de reacció per evocar paraules i construir frases és superior al dels iguals, generant pressió en contextos temporals
- **Comprensió lectora:** No és una barrera visible — l'alumne pot llegir en veu alta correctament però no haver-ho comprès; el docent pot confondre fluïdesa amb comprensió
- **Participació oral:** Les dificultats expressives limiten la participació en debats, exposicions i dinàmiques de grup, infrarepresentant la competència cognitiva real
- **Pragmàtica:** El llenguatge figurat, les consignes implícites i el sarcasme educatiu ("ara ens falten 5 minuts per acabar...") poden generar confusió genuïna, no manca d'atenció

#### Necessitats prioritàries

1. **Instrucció explícita del vocabulari** acadèmic i específic de cada àrea, no exposició incidental
2. **Modelatge d'estructures lingüístiques** esperades (plantilles, inicis de frase, mapes d'estructura) en tasques de producció
3. **Adaptació d'instruccions**: una instrucció alhora, en llenguatge literal, amb suport visual
4. **Temps addicional** per a totes les tasques amb component lingüístic (comprensió o producció)
5. **Dissociació entre competència lingüística i competència conceptual** en l'avaluació
6. **Col·laboració logopeda–docent** per a la transferència de les estratègies d'intervenció a l'aula

#### Fortaleses a aprofitar

- Capacitat de raonament no verbal sovint normativa o superior a la mitjana
- Memòria visual i processament espacial freqüentment preservats
- Alta motivació quan les barreres lingüístiques s'eliminen i s'accedeix al contingut per canals alternatius
- Capacitat per a tasques pràctiques, manipulatives i visuals no dependents del codi escrit
- Resiliència i creativitat en la cerca d'estratègies compensatòries

#### Senyals identificadors a l'aula

**Senyals d'alarma:**
- Vocabulari molt limitat per a l'edat; s'expressa amb paraules molt generals ("cosa", "fer", "allò")
- Frases molt curtes, simples i mal estructurades en la producció oral i escrita
- Gran diferència entre el que sembla que ha entès i el que és capaç de produir
- Dificultat per seguir instruccions de dos o més passos
- Problemes persistents per estructurar un relat o exposició oral amb coherència
- Dificultats en totes les àrees que requereixen lectura i escriptura, sense component específicament lector

**Senyals de context:**
- Historial familiar de dificultats de llenguatge
- Derivació o seguiment logopèdic previ o actual
- Dificultats ja presents en l'etapa d'Infantil (retard en primeres paraules, frases curtes a I3)

**Anti-senyals (que no apunten a TDL):**
- Dificultats úniques en L2, però no en L1 — probable barrera lingüística, no TDL
- Dificultats aparegudes sobtadament — descartar causes neurològiques adquirides
- Millora ràpida i completa amb instrucció ordinària
- Dificultats exclusivament en lectura i escriptura sense afectació oral — valorar dislèxia en lloc de TDL

#### Perfils associats i comorbiditats

- **TDL + Dislèxia**: comorbiditat del 40-50%. Ambdós canals (oral i escrit) compromesos. Les dificultats fonològiques del TDL contribueixen als problemes lectors
- **TDL + TDAH**: la dificultat d'evocació lèxica i la disfunció executiva s'intensifiquen mútuament. Les instruccions llargues generen una doble barrera (atenció + processament lingüístic)
- **TDL + TEA**: superposició clínica en el component pragmàtic. El diagnòstic diferencial és complex i sovint ambdós coexisteixen
- **TDL + Nouvingut**: la barrera de la L2 pot emmascarar o amplificar el TDL. L'avaluació en L1 és imprescindible per al diagnòstic diferencial
- **TDL + Altes capacitats (2e)**: el potencial cognitiu compensa parcialment les dificultats lingüístiques, retardant la detecció fins que les demandes lingüístiques acadèmiques augmenten (generalment ESO)

#### Principis d'actuació

- **Adaptar continguts:** Usar vocabulari d'alta freqüència, estructures SVO simples, definicions integrades, frases d'una sola clàusula. No reduir la profunditat conceptual — adaptar el canal lingüístic, no el contingut cognitiu.
- **Adaptar activitats:** Oferir andamiatge lingüístic explícit en les tasques de producció (plantilles, guions, bancs de paraules). Proporcionar alternatives d'accés no exclusivament verbal (mapes conceptuals, suport visual, oral).
- **Adaptar avaluació:** Dissociar la competència conceptual de la lingüística. Permetre respostes orals, esquemes, mapes o suport visual. Valorar el contingut per sobre de la forma lingüística. Proporcionar rúbriques que facin explícits els criteris d'avaluació.
- **Adaptar interacció:** En dinàmiques de grup, estructurar explícitament els rols comunicatius. En exposicions orals, proporcionar guió previ i temps de preparació. Evitar consignes amb llenguatge figurat o implícit.

#### Línies vermelles

- **No confondre TDL amb baixa capacitat intel·lectual.** **Per què?** La capacitat no verbal és normativa o superior en la majoria de casos. El TDL afecta el canal lingüístic, no el raonament.
- **No confondre TDL amb barrera lingüística en alumnat nouvingut.** **Per què?** El diagnòstic diferencial requereix avaluació en L1. Fins que no es descarta la causa lingüística, no és ètic ni rigorós assumir TDL.
- **No avaluar la competència conceptual exclusivament a través de la producció escrita.** **Per què?** L'alumne pot saber la resposta però no poder-la expressar en el format requerit — la nota mesurarà el TDL, no el coneixement.
- **No usar consignes implícites, iròniques o amb doble sentit.** **Per què?** Les dificultats pragmàtiques fan que el llenguatge no literal sigui genuïnament incomprensible, no una falta d'atenció.
- **No donar múltiples instruccions simultànies.** **Per què?** La memòria de treball verbal limitada fa que l'alumne perdi parts de la instrucció, sense que sigui negligència.
- **No esperar que el TDL "se superi" amb l'edat sense suport.** **Per què?** És un trastorn persistent. Les manifestacions canvien (les dificultats orals bàsiques milloren), però l'impacte en la comprensió i producció de textos acadèmics complexos persisteix a l'adolescència i l'edat adulta.

#### Detecció i protocols

##### Principis de detecció

La detecció precoç del TDL es basa en l'observació sistemàtica de les etapes d'adquisició del llenguatge i la resposta a la instrucció. No existeix una prova única diagnòstica: el diagnòstic és clínic, realitzat per logopedes i/o psicòlegs, i requereix:

1. **Avaluació multicomponent**: comprensió i expressió en vocabulari, morfosintaxi, discurs i pragmàtica
2. **Avaluació en totes les llengües** del repertori de l'alumne (especialment en contextos bilingües)
3. **Descart de causes alternatives**: audició, visió, context socioeducatiu, trastorn neurològic adquirit
4. **Perspectiva longitudinal**: les dificultats han de ser persistents (no transitòries)

##### Protocols a Catalunya

- **CREDA (Centres de Recursos Educatius per a Deficients Auditius)** amb competència en TDL: suport especialitzat a centres ordinaris per a alumnat amb trastorns del llenguatge
- **EAP (Equip d'Assessorament Psicopedagògic)**: primera porta d'entrada escolar per a la derivació al logopeda o al CREDA
- **Col·legi de Logopedes de Catalunya (CLC)**: guies de bones pràctiques actualitzades el 2025
- **XTEC / Educació Inclusiva**: recursos de formació docent sobre TDL, amb materials actualitzats 2022-2026

### 2. CONNEXIONS AMB ALTRES DOCUMENTS DEL CORPUS

- **M1_dislexia-dificultats-lectores**: Comorbiditat 40-50%. Dificultats fonològiques del TDL contribueixen als problemes lectors. Veure dependència #10
- **M1_TDAH**: Doble barrera atenció + processament lingüístic. Instruccions llargues especialment problemàtiques
- **M1_TEA**: Superposició en el component pragmàtic. Diagnòstic diferencial complex
- **M1_alumnat-nouvingut**: Barrera L2 pot emmascarar o amplificar el TDL. Veure dependència #2
- **M1_altes-capacitats**: Doble excepcionalitat (2e) possible. Detecció tardana per compensació
- **M1_creuament-variables-dependencies**: Dependencies #2, #10 (TDL × dislèxia), #TDL-TDAH, #TDL-TEA
- **M3_lectura-facil-comunicacio-clara**: Tècniques de simplificació directament aplicables al component semàntic i morfosintàctic
- **M2_carrega-cognitiva-adaptacio-textos**: La càrrega cognitiva del TDL es concentra en el processament lingüístic, no en la capacitat conceptual
- **M2_DUA-principis-pautes**: Marc general d'accessibilitat; principi de representació múltiple especialment rellevant

### 3. DETECCIÓ (Variables de Context)

- **Senyals del docent:**
  - "S'expressa amb frases molt curtes i simples, sobretot per escrit, però quan li pregunto oralment demostra que ho ha entès."
  - "Té molt poca variació de vocabulari — sempre usa les mateixes paraules bàsiques."
  - "No segueix instruccions de més d'un pas sense que li hagi de repetir."
  - "Les seves redaccions no tenen estructura — és una llista de frases sense connexió."
  - "En els treballs en grup, no participa gaire, però quan se li pregunta directament, respon bé."
  - "Llegeix amb fluïdesa però no respon bé les preguntes de comprensió."

- **Senyals de l'alumne:**
  - Frustració o bloqueig davant tasques d'expressió escrita llarga
  - Evitació de les exposicions orals i del treball en grup
  - Dificultat per trobar les paraules ("se m'ha anat del cap", "com es diu...?")
  - Rendiment molt variable depenent del format de la tasca (millora molt amb suport visual o oral)

- **Senyals de context:**
  - Seguiment logopèdic previ o actual
  - Historial familiar de dificultats de llenguatge
  - Dificultats presents des de l'etapa d'Infantil

- **Anti-senyals:**
  - Dificultats únicament en L2 (possible barrera lingüística, no TDL)
  - Dificultats aparegudes sobtadament o associades a un event concret
  - Millora ràpida i completa amb instrucció ordinària
  - Dificultats exclusivament en lectura i escriptura sense afectació oral (valorar dislèxia)

### 4. HEURÍSTIQUES I RAONAMENT PER A L'AGENT

- **Principi general:** L'agent ha d'adaptar la complexitat lingüística (sintàctica i lèxica) dels textos i consignes, sense reduir la profunditat conceptual ni cognitiva. El TDL afecta el canal, no la capacitat de pensar.

- **Heurístiques per a l'Agent DOCENT:**

  - **Nom:** Adaptació per component afectat
  - **Quan aplica:** Quan el docent indica que l'alumne té TDL i es coneixen els components afectats.
  - **Fonament:** El TDL és heterogeni — un alumne amb morfosintaxi afectada però semàntica preservada necessita una intervenció diferent que un amb dificultats de discurs i pragmàtica.
  - **Exemple complet de raonament:** "El docent indica que l'alumna té TDL amb component morfosintàctic i de discurs afectats, grau moderat. L'agent ha de raonar que les frases han d'estar en SVO simple, evitar subordinades, i que els textos llargs han d'estar segmentats amb titulars de funció ('Primer fem X / Després fem Y / Al final...'). A més, en les consignes de producció ha d'oferir un guió d'estructura explícit ('Escriu 3 frases: una sobre el problema, una sobre la solució, una sobre el resultat'). No ha de simplificar el contingut conceptual — l'alumna pot entendre el tema al nivell del curs, però necessita el canal lingüístic adaptat."

  - **Nom:** Detecció vs. diagnòstic — el paper del docent
  - **Quan aplica:** Quan un docent pregunta si un alumne nouvingut o amb dificultats d'expressió "podria tenir TDL".
  - **Fonament:** El TDL requereix avaluació especialitzada en totes les llengües del repertori. La barrera L2 pot produir un perfil superficialment idèntic al TDL.
  - **Exemple complet de raonament:** "Un docent descriu un alumne que es va incorporar fa 6 mesos, parla poc i s'expressa amb frases molt simples en català i castellà. L'agent ha de raonar que primer cal saber si les dificultats apareixen també en la L1. Si l'alumne s'expressa amb normalitat en la seva llengua familiar, probablement és una barrera lingüística i no TDL. L'agent recomanaria: (1) observar l'alumne en contextos informals en la seva L1, (2) consultar la família sobre el desenvolupament del llenguatge en etapa primerenca, (3) si les dificultats es confirmen en L1, derivar a l'EAP per a avaluació logopèdica. No diagnosticar TDL sense avaluació professional."

  - **Nom:** Dissociació competència lingüística–competència conceptual en l'avaluació
  - **Quan aplica:** Quan es dissenyen activitats, rúbriques o criteris d'avaluació per a alumnat amb TDL.
  - **Fonament:** Avaluar la producció lingüística com a mesura de la competència conceptual invalida els resultats per a l'alumne amb TDL.
  - **Exemple complet de raonament:** "Un docent demana una rúbrica per a un treball de ciències socials per a un alumne amb TDL moderat. L'agent ha de separar els criteris lingüístics (estructura del text, riquesa de vocabulari, correcció gramatical) dels criteris conceptuals (identifica causes i conseqüències, relaciona conceptes, argumenta la seva opinió). Per a l'alumne amb TDL, els criteris lingüístics s'avaluen sobre el seu nivell adaptat, no sobre el nivell del curs. Els criteris conceptuals s'avaluen igual que la resta d'alumnes, i si cal, l'alumne pot demostrar la competència per via oral o amb suport visual."

- **Heurístiques per a l'Agent ALUMNE:**

  - **Nom:** Andamiatge lingüístic en producció escrita
  - **Quan aplica:** Quan l'alumne ha de fer una redacció, informe, projecte o qualsevol tasca de producció escrita.
  - **Fonament:** Les dificultats morfosintàctiques i discursives del TDL fan que la pàgina en blanc sigui una barrera paralitzant.
  - **Exemple complet de raonament:** "Un alumne amb TDL ha d'escriure un informe sobre el canvi climàtic. L'agent suggeriria: (1) un esquema amb blocs etiquetats ('Definició / Causes / Conseqüències / Solucions'), (2) entre 1 i 3 preguntes guia per a cada bloc ('Quina és la principal causa? Dona un exemple'), (3) un banc de paraules clau del tema, (4) opcions d'inici de frase per a cada bloc ('La causa principal és... / Una conseqüència és... / Una possible solució seria...'). L'objectiu és eliminar la barrera de l'organització i el lèxic perquè l'alumne pugui demostrar el seu coneixement del tema."

  - **Nom:** Comprensió de consignes complexes
  - **Quan aplica:** Quan l'alumne no entén o no executa correctament una consigna de tasca o activitat.
  - **Fonament:** Les instruccions multistep o amb vocabulari implícit generen una barrera d'accés a la tasca independent del coneixement del contingut.
  - **Exemple complet de raonament:** "Un alumne amb TDL diu que no sap com fer una activitat de ciències. L'agent, en lloc de repetir la consigna, la reformularia en passos numerats: '1. Llegeix el text del pas 1. 2. Busca la paraula [terme clau]. 3. Escriu la definició amb les teves paraules.' Si el vocabulari de la consigna és abstracte, l'agent el substituiria per exemples concrets. No suposaria que l'alumne no sap el contingut — el problema pot ser la barrera lingüística de la consigna, no el coneixement."

---

## 6. INSTRUCCIONS D'ADAPTACIÓ TEXTUAL PER A L'LLM

### Barrera nuclear
**Comprensió lèxica i sintàctica**: L'alumnat amb TDL té com a barrera principal la comprensió i producció lingüística — tant lèxica (vocabulari limitat, accés lent al lèxic) com sintàctica (dificultat amb estructures complexes, pronoms febles, subordinades). La memòria fonològica compromesa dificulta retenir frases llargues.

### Instruccions per al prompt LLM

```
PERFIL: TDL (Trastorn del Desenvolupament del Llenguatge)
- Reducció màxima de densitat lèxica
- Cada terme tècnic apareix en 2-3 contextos diferents (modelatge)
- Zero subordinades i pronoms febles (li, els, en, hi)
- Definicions integrades just al costat del terme (no al final)
```

### Mapa barrera → instruccions (prioritzat)

| Prioritat | Instruccions activades | Justificació (barrera) |
|---|---|---|
| **1a (lèxica)** | H-16 (reducció densitat lèxica), A-01 (vocab freqüent), A-02 (termes en negreta), A-20 (control densitat) | Barrera nuclear: comprensió lèxica |
| **2a (sintàctica)** | H-17 (modelatge ús context), A-07 (una idea per frase), A-13 (eliminació subordinades), A-26 (evitar incisos) | Barrera nuclear: comprensió sintàctica |
| **3a (memòria)** | C-04 (chunking 3-5 elements), C-05 (glossari previ Sweller) | Memòria fonològica compromesa |

### Exemple ABANS → DESPRÉS (A2, ciències naturals)

**Original:**
> L'aigua dels rius i els mars s'evapora per l'acció del sol, forma núvols, i quan els núvols es refreden, l'aigua cau en forma de pluja.

**Adaptat (TDL, A2, DUA Core):**

## Text adaptat
El sol escalfa l'aigua dels rius.
L'aigua es converteix en vapor. L'aigua **s'evapora**.

El vapor puja al cel.
El vapor forma **núvols**. Els núvols estan fets de gotes molt petites.

Els núvols es refreden.
Les gotes cauen. L'aigua cau en forma de **pluja**.

> Nota: "s'evapora" apareix com a terme, després com a definició, després en context. Modelatge en 3 contextos.

---

## 5. FONTS DEL CORPUS

| # | Referència | Tipus | Any |
|---|-----------|-------|-----|
| 1 | Bishop, D.V.M. et al. *CATALISE-2: a multinational and multidisciplinary Delphi consensus study.* PLOS ONE. | Consens internacional | 2017 |
| 2 | Norbury, C.F. et al. *The impact of nonverbal ability on prevalence and clinical presentation of language disorder.* JCPP. | Prevalença i perfil clínic | 2016 |
| 3 | Bishop, D.V.M. *Reconceptualizing DLD as a spectrum disorder.* JSLHR. | Marc dimensional | 2018 |
| 4 | RADLD — Research Autism DLD. *Trastorn del Desenvolupament del Llenguatge (TDL/TEL).* radld.org | Divulgació científica | Vigent |
| 5 | CREDA Cat Central / XTEC. *Actualització TDL: Terminologia i criteris d'identificació.* | Protocol Catalunya | 2026 |
| 6 | XTEC / Educació Inclusiva. *Del TEL al TDL.* projectes.xtec.cat | Recursos docents | 2022 |
| 7 | Col·legi de Logopedes de Catalunya. *Trastorns del Llenguatge Infantil.* Guia BP_05. | Guia clínica | 2025 |
| 8 | Portal GVA Educació. *TDL: vocabulari i morfosintaxi (Julián Palazón López).* | Recurs educatiu | 2026 |
| 9 | Frontiers in Education. *Educational practices for language development with DLD.* | Recerca educativa | 2024 |
| 10 | De las Heras et al. *Reading Strategies for Children with DLD.* PMC / NIH. | Recerca estratègies lectores | 2022 |
| 11 | Wiley / Cognitive Science. *What children with DLD teach us about word learning.* | Recerca aprenentatge lèxic | 2022 |
| 12 | RedCenit. *Adaptaciones para el aula en el TEL/TDL.* redcenit.com | Pràctica educativa | 2016 |
| 13 | Integratek Plus. *TDL en la escuela: Adaptaciones, pautas y normativa.* | Pràctica educativa | Vigent |

*13 fonts referencials · document actualitzat 2026-03-26*
