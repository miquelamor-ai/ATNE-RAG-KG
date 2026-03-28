---
modul: M1
titol: "Trastorn del Desenvolupament de la Coordinació (TDC / Dispraxia)"
tipus: caracteristica
subtipus: constitutiva
descripcio: "TDC/Dispraxia: criteris diagnòstics complets DSM-5-TR (315.4/F82) i ICD-11 (6A04), prevalença 5-6% amb comorbiditats, manifestació per dominis motors, senyals d'alerta per etapes, instruments d'avaluació (MABC-2, BOT-2, DCD-Q), diagnòstic diferencial, evidència intervenció (CO-OP, task-oriented), marc normatiu català D150/2017, variables configurables per grau i àrea afectada"
review_status: revisat
locked: true
generat_at: 2026-03-27T03:00:00
actualitzat_at: 2026-03-27T03:30:00
variables_configurables:
  - nom: grau
    etiqueta: "Grau de severitat"
    tipus: enum
    valors: [lleu, moderat, sever]
    obligatori: true
    defecte: moderat
    descripcio: "Lleu: dificultats compensables, afecta principalment velocitat. Moderat: impacte notable en escriptura i activitats manipulatives. Sever: dificultats significatives en autonomia motora quotidiana"
    impacte: "Lleu: temps addicional, pauta clara. Moderat: adaptació instruments d'escriptura, alternatives digitals. Sever: tecnologia assistiva, eliminació barreres motores"
  - nom: motricitat_fina
    etiqueta: "Motricitat fina afectada"
    tipus: boolean
    obligatori: false
    defecte: true
    descripcio: "Dificultats en moviments precisos de mans i dits: escriptura manual, retallat, manipulació d'objectes petits, ús de ratolí"
    impacte: "Permetre alternatives digitals per a escriptura, adaptar activitats manipulatives, temps addicional, ús de teclat"
  - nom: motricitat_grossa
    etiqueta: "Motricitat grossa afectada"
    tipus: boolean
    obligatori: false
    defecte: false
    descripcio: "Dificultats en moviments grans del cos: equilibri, coordinació, esports d'equip, pujar escales"
    impacte: "Adaptar activitats d'EF, evitar esports competitius sense adaptació, valorar alternatives"
  - nom: acces_teclat
    etiqueta: "Accés al teclat com a alternativa"
    tipus: boolean
    obligatori: false
    defecte: true
    descripcio: "L'alumne pot usar teclat com a alternativa a l'escriptura manual"
    impacte: "Si true: oferir teclat/tauleta per a producció escrita llarga. Si false: valorar tecnologia assistiva específica"
---

### 1. CONTINGUT ESPECÍFIC

#### Descripció del tret

##### Definició i marc conceptual

El **Trastorn del Desenvolupament de la Coordinació (TDC)** — també conegut com a **dispraxia** en contextos europeus — és un trastorn del neurodesenvolupament caracteritzat per una **dificultat marcada en l'adquisició i l'execució d'habilitats motores coordinades**, que interfereix significativament en les activitats de la vida quotidiana i el rendiment acadèmic.

La terminologia varia segons el context: el DSM-5 usa *Developmental Coordination Disorder (DCD)*, mentre que el terme **dispraxia** és més freqüent en la literatura europea i britànica. En l'àmbit educatiu català, sovint apareix com a "dificultats de coordinació motora" o "dispraxia" en els informes psicopedagògics. Malgrat la variació terminològica, el constructe clínic és el mateix: un trastorn neurològic de base que afecta la planificació, l'organització i l'execució d'accions motores.

**Important:** El TDC **no és mandra, falta de pràctica ni descurança.** És una condició neurològica que afecta la manera com el cervell planifica i executa els moviments. L'alumne amb TDC s'esforça més que els seus iguals per produir resultats motors inferiors.

##### Criteris diagnòstics DSM-5-TR (315.4 / F82)

| Criteri | Descripció |
|---------|------------|
| **A** | L'adquisició i l'execució d'habilitats motores coordinades estan substancialment per sota del que s'espera donada l'edat cronològica i l'oportunitat d'aprenentatge. Les dificultats es manifesten com a maldestre (p. ex., deixar caure o xocar amb objectes), lentitud i imprecisió en habilitats motores (p. ex., agafar objectes, usar tisores o coberts, escriure, anar en bicicleta, participar en esports). |
| **B** | El dèficit d'habilitats motores del criteri A interfereix significativament i de forma persistent en les activitats de la vida diària apropiades a l'edat (p. ex., cura personal i autocontrol) i afecta la productivitat acadèmica/escolar, les activitats prevocacionals i vocacionals, el lleure i el joc. |
| **C** | L'inici dels símptomes és en el període primerenc del desenvolupament. |
| **D** | Els dèficits d'habilitats motores no s'expliquen millor per discapacitat intel·lectual o deficiència visual i no són atribuïbles a una condició neurològica que afecti el moviment (p. ex., paràlisi cerebral, distròfia muscular, trastorn degeneratiu). |

La **ICD-11 (6A04)** classifica el TDC com a *Developmental motor coordination disorder* i el defineix com: *"A neurodevelopmental disorder characterised by a significant delay in the acquisition of gross and fine motor skills and impairment in the execution of coordinated motor skills that manifest in clumsiness, slowness, or inaccuracy of motor performance."* Els criteris d'exclusió són equivalents als del DSM-5-TR.

##### Correspondència de codis diagnòstics

| Sistema | Codi | Denominació |
|---------|------|-------------|
| DSM-5-TR | 315.4 / F82 | Developmental Coordination Disorder |
| ICD-11 | 6A04 | Developmental motor coordination disorder |
| ICD-10 | F82 | Trastorn específic del desenvolupament de la funció motriu |

##### Prevalença i perfil epidemiològic

| Indicador | Dada | Font |
|-----------|------|------|
| **Prevalença global** | 5-6% de la població escolar | Blank et al., 2012 (EACD) |
| **Ràtio per sexe** | 2:1 (nens:nenes), possible infradetecció en nenes | Barnhart et al., 2003 |
| **Comorbiditat amb TDAH** | ≈ 50% | Barnhart et al., 2003 |
| **Comorbiditat amb dislèxia** | 40-50% | Blank et al., 2012 |
| **Comorbiditat amb TEA** | Subgrup significatiu (dades variables) | Blank et al., 2012 |
| **Persistència a l'edat adulta** | Majoria de casos — les manifestacions canvien, la condició es manté | Kirby & Sugden, 2007 |
| **Capacitat intel·lectual** | No s'associa a baixa intel·ligència; sovint normativa o superior | Polatajko, 1995 |
| **Infradetecció** | Molt menys detectat que dislèxia o TDAH; molts arriben a ESO sense diagnòstic | Missiuna et al., 2007 |

##### Manifestacions per domini

| Domini | Manifestació | Impacte escolar |
|--------|-------------|-----------------|
| **Motricitat fina** | Dificultats en escriptura, dibuix, retallat, abotonament, ús de cremalleres i coberts | Escriptura lenta i il·legible; problemes en plàstica, tecnologia, laboratoris |
| **Motricitat grossa** | Dificultats en equilibri, coordinació bilateral, saltar, llançar i atrapar | Problemes en EF, esports d'equip, jocs de pati; risc de caigudes |
| **Planificació motora (praxia)** | Dificultat per seqüenciar moviments nous i complexos; aprendre noves habilitats motores costa molt més | Dificultat en activitats que requereixen passos motors seqüenciats: experiments, manualitats, cuina |
| **Funcions executives vinculades al motor** | Dificultat per organitzar l'espai de treball, anticipar passos motors, canviar d'estratègia motora | Treballs desorganitzats al paper; motxilla i pupitre desordenats; pèrdua freqüent de materials |
| **Escriptura (component transversal)** | Velocitat reduïda (×2 o ×3), il·legibilitat, fatiga acumulativa, dolor a la mà | Producció escrita molt inferior al potencial oral; exàmens incomplets; fatiga progressiva al llarg del dia |
| **Autonomia personal** | Dificultat per vestir-se, lligar sabates, usar coberts, preparar material | Dependència de l'adult en autonomia bàsica; temps addicional en transicions |
| **Impacte socioemocional** | Evitació de tasques motores, baixa autoestima, exclusió en jocs i esports d'equip | Aïllament, ansietat davant EF/plàstica, sentiment crònic de ser "maldestre" |

##### Senyals d'alerta per etapes

| Etapa | Senyals d'alerta principals |
|-------|----------------------------|
| **Infantil (I3-I5)** | Retard en grafisme (no dibuixa cercles, creu); dificultat amb tisores; no es vesteix sol; caigudes freqüents; evita jocs de construcció i manualitats; agafa el llapis amb presa immadura |
| **Primària (1r-3r)** | Escriptura lenta i il·legible; gran diferència oral-escrit; problemes amb geometria (regle, compàs); dificultat en esports; fatiga motora en escriure; perd materials |
| **Primària (4t-6è)** | Producció escrita molt per sota del potencial oral; evitació d'EF i plàstica; fatiga motora evident; treballs desorganitzats; impacte en totes les àrees amb component escrit |
| **ESO** | Escriptura manual molt costosa; problemes amb instruments de laboratori; exàmens escrits no reflecteixen el coneixement real; dificultats en treballs manuals de tecnologia; frustració acadèmica |
| **Batxillerat / FP** | Impacte en exàmens escrits llargs (PAU); dificultats en pràctiques de laboratori i treballs manuals d'FP; ansietat avaluativa; limitació percebuda d'opcions professionals |

##### Grau de severitat

| Grau | Descripció clínica | Implicació per a l'assistent |
|------|------|------|
| **Lleu** | Dificultats compensables; afecta principalment la velocitat i la fluïdesa motora; sovint passa desapercebut | Temps addicional, pauta clara, instruments adaptats opcionals |
| **Moderat** | Impacte notable en escriptura manual i activitats manipulatives; requereix adaptació sistemàtica | Accés a teclat/tauleta per a producció escrita, adaptació d'EF, instruments ergonòmics |
| **Sever** | Dificultats significatives en l'autonomia motora quotidiana; pot requerir tecnologia assistiva | Tecnologia assistiva, eliminació de barreres motores, alternatives no motores per a totes les tasques |

#### Barreres d'aprenentatge

- **Escriptura manual:** La velocitat, la llegibilitat i la fatiga motora fan que l'escriptura manual sigui la barrera més visible i quotidiana. L'alumne pot trigar el doble o el triple que els seus iguals a escriure la mateixa quantitat de text, i el resultat és sovint il·legible
- **Activitats manipulatives:** Laboratoris de ciències (instruments de precisió), plàstica (tisores, pinzells), tecnologia (eines), cuina (utensilis) — qualsevol activitat amb component motor fi representa una barrera d'accés
- **Educació física:** Esports d'equip, exercicis de coordinació, gimnàstica — l'alumne amb TDC pot ser sistemàticament l'últim en ser triat i el primer en ser ridiculitzat
- **Organització:** Gestionar materials, organitzar la motxilla, mantenir l'espai de treball net, trobar coses — la planificació motora afecta també l'organització de l'entorn físic
- **Temps:** Totes les tasques amb component motor triguen més. L'alumne amb TDC paga un "impost temporal" en cada activitat escolar que requereix moviment, escriptura o manipulació

#### Necessitats prioritàries

1. **Accés al teclat/tauleta** per a producció escrita llarga — és l'adaptació amb més impacte i evidència (Missiuna et al., 2008)
2. **Temps addicional** en totes les tasques amb component motor: escriptura, manualitats, experiments, exàmens
3. **Adaptació d'EF**: alternatives no competitives, valoració de l'esforç i la millora personal per sobre del rendiment absolut
4. **Instruments adaptats**: llapis ergonòmics (secció triangular, grip engruixit), tisores adaptades, regles amb grip, compàs amb adaptador
5. **Dissociació entre qualitat motora i qualitat cognitiva en l'avaluació**: la cal·ligrafia no pot determinar la nota de coneixement del medi ni de ciències

#### Fortaleses a aprofitar

- Capacitat cognitiva sovint **normativa o superior** — el TDC afecta el motor, no el raonament
- **Creativitat verbal i oral**: compensen la via motora amb la verbal; sovint són alumnes molt expressius oralment
- **Perseverança**: estan acostumats a esforçar-se més que els iguals per a resultats inferiors; quan es retira la barrera motora, la perseverança es converteix en un avantatge
- **Pensament visual i espacial** pot estar intacte o fins i tot ser un punt fort (Zwicker et al., 2012)
- **Capacitat d'autoconsciència**: molts alumnes amb TDC desenvolupen estratègies compensatòries pròpies si se'ls dona l'espai i les eines

#### Senyals identificadors a l'aula

**Senyals d'alarma:**
- Escriptura molt lenta, il·legible o desorganitzada al paper
- Gran diferència entre la capacitat oral (fluida, rica) i la producció escrita (pobra, curta, desordenada)
- Evitació d'activitats d'EF, plàstica i manualitats
- Dificultat per vestir-se, lligar-se les sabates, usar coberts al menjador
- Cansament excessiu després d'escriure — es queixa de dolor a la mà, para sovint, sacseja els dits
- Sembla "maldestre" o "desorganitzat" però és clarament intel·ligent
- Perd materials freqüentment; pupitre i motxilla desordenats

**Senyals de context:**
- Historial de retard en fites motores (caminar, pujar escales, vestir-se sol)
- Derivació o seguiment previ per dificultats motores o psicomotrius
- Dificultats ja presents a l'etapa d'Infantil (grafisme, autonomia)
- Historial familiar de dificultats de coordinació

**Anti-senyals (que no apunten a TDC):**
- Dificultats només en L2 oral, sense component motor — probable barrera lingüística, no TDC
- Dificultats motores aparegudes sobtadament — descartar causes neurològiques adquirides (lesió, tumor)
- Millora ràpida i completa amb pràctica — el TDC és persistent; la pràctica millora parcialment però no resol
- Dificultats exclusivament en lectura i escriptura sense afectació motora general — valorar dislèxia, no TDC
- Dificultat motora explicable per una condició visual no corregida

#### Avaluació i diagnòstic

##### Instruments d'avaluació estandarditzats

| Instrument | Àrea | Edat | Ús |
|------------|------|------|-----|
| **MABC-2** (Movement Assessment Battery for Children – 2) | Destresa manual, punteria/recepció, equilibri | 3-16 anys | Diagnòstic clínic; gold standard per a TDC |
| **BOT-2** (Bruininks-Oseretsky Test of Motor Proficiency – 2) | Motricitat fina i grossa (8 subtests) | 4-21 anys | Avaluació motora completa; identifica àrees afectades |
| **DCD-Q** (Developmental Coordination Disorder Questionnaire) | Screening via qüestionari (pares/docents) | 5-15 anys | Detecció precoç; útil per cribratge escolar |
| **DCDQ-07** (versió actualitzada) | Screening funcional | 5-15 anys | Versió revisada amb millors propietats psicomètriques |

**Principis de detecció:** La detecció del TDC es basa en l'observació del desenvolupament motor i la resposta funcional en les activitats quotidianes i escolars. No existeix una prova única diagnòstica: el diagnòstic és clínic, realitzat per fisioterapeutes, terapeutes ocupacionals i/o psicòlegs, i requereix:

1. **Avaluació motora estandarditzada**: proves com el MABC-2 o el BOT-2
2. **Observació funcional**: com les dificultats motores afecten l'escriptura, l'autonomia i la participació escolar
3. **Descart de causes alternatives**: deficiència visual, condició neurològica adquirida, discapacitat intel·lectual
4. **Perspectiva longitudinal**: les dificultats han de ser persistents (no transitòries) i presents des de les primeres etapes

##### Diagnòstic diferencial

| Condició | Tret diferenciador respecte al TDC |
|----------|-----------------------------------|
| **Paràlisi cerebral** | Origen perinatal, signes neurològics durs (espasticitat, hipertonia); en TDC el to muscular és normal |
| **TDAH** | Pot coexistir (50%); la impulsivitat motora del TDAH no és el mateix que la incoordinació del TDC; cal avaluar ambdós si coexisteixen |
| **Dislèxia** | Pot coexistir (40-50%); la dislèxia afecta la via fonològica (ortografia, decodificació), el TDC la via motora (velocitat, llegibilitat, fatiga); l'escriptura es veu afectada per vies diferents |
| **TEA** | Solapament en rigidesa motora i planificació; el TEA té criteris propis (comunicació social, interessos restringits); molts alumnes TEA tenen perfil motor compatible amb TDC |
| **Baixa condició física / sedentarisme** | Millora amb entrenament; el TDC és persistent malgrat la pràctica; la incoordinació del TDC no respon a l'exercici de la mateixa manera que la baixa forma física |

#### Marc normatiu català

| Referència normativa | Rellevància per al TDC |
|---------------------|----------------------|
| **Decret 150/2017** d'atenció educativa a l'alumnat en el marc d'un sistema educatiu inclusiu | Estableix el dret a mesures i suports universals, addicionals i intensius. L'alumne amb TDC pot requerir mesures **addicionals** (adaptació d'accés) o **intensives** (PI) segons el grau |
| **DOIGC 2025-2026** (Instruccions d'inici de curs) | Concreta els criteris de dotació de recursos i les funcions de l'EAP en la detecció i seguiment de NESE |
| **Llei 17/2020** de modificació de la Llei 12/2009 d'Educació | Reforça el model d'escola inclusiva i el dret a ajustaments raonables per a tot l'alumnat amb diversitat funcional |

**Nota:** A Catalunya, no existeix un protocol específic de TDC tan desenvolupat com els de TEA o dislèxia. La detecció depèn en gran mesura de la sensibilització del centre educatiu i de l'EAP de referència. Això fa que molts alumnes amb TDC arribin a secundària sense diagnòstic formal.

##### Protocols a Catalunya

- **EAP (Equip d'Assessorament Psicopedagògic)**: primera porta d'entrada escolar per a la valoració psicomotriu i la derivació
- **Possible derivació a fisioterapeuta o terapeuta ocupacional** per a avaluació motora estandarditzada i intervenció
- **CDIAP (Centres de Desenvolupament Infantil i Atenció Precoç)**: detecció en etapa 0-6 anys
- **XTEC / Educació Inclusiva**: recursos de formació docent sobre diversitat funcional motora

#### Evidència científica sobre intervenció

| Enfocament | Tipus | Evidència | Descripció |
|------------|-------|-----------|------------|
| **CO-OP** (Cognitive Orientation to daily Occupational Performance) | Orientat a la tasca | **Forta** | L'alumne identifica objectius motors funcionals i aprèn estratègies cognitives (Goal-Plan-Do-Check) per resoldre'ls. Transferència a noves tasques demostrada |
| **Task-oriented / task-specific** | Orientat a la tasca | **Forta** | Pràctica repetida de tasques funcionals concretes (escriptura, ús de tisores) amb feedback; millora l'habilitat específica entrenada |
| **Integració sensorial (SI)** | Orientat al procés | **Feble-moderada** | Treballa el processament sensorial de base; evidència limitada de transferència a habilitats funcionals escolars |
| **Neuromotor Task Training (NTT)** | Orientat a la tasca | **Moderada** | Combina pràctica de tasques funcionals amb entrenament de components neuromotors; resultats prometedors |
| **Educació física adaptada** | Orientat a la tasca | **Moderada** | Programes d'EF amb instrucció individualitzada i objectius adaptats; millora la participació i la competència percebuda |

**Nota sobre l'evidència:** Els enfocaments **orientats a la tasca** (CO-OP, task-specific) mostren consistentment millors resultats que els enfocaments **orientats al procés** (integració sensorial, entrenament perceptivomotor). La recomanació actual (EACD, Blank et al., 2012) és prioritzar les intervencions task-oriented. A l'escola, això significa **adaptar i practicar les tasques reals** (escriure, retallar, vestir-se) amb estratègies cognitives, en lloc d'exercicis perceptivomotors abstractes.

#### Perfils associats i comorbiditats

- **TDC + Dislèxia**: comorbiditat del **40-50%**. Ambdós afecten la producció escrita però per vies diferents: el TDC per la via motora (velocitat, llegibilitat, fatiga), la dislèxia per la via fonològica (ortografia, decodificació). Quan coexisteixen, l'escriptura manual es converteix en una barrera doblement costosa
- **TDC + TDAH**: comorbiditat del **50%** (Barnhart et al., 2003). La disfunció executiva del TDAH s'afegeix a la dificultat de planificació motora del TDC. L'alumne és alhora desatent i maldestre — combinació que genera una infrarepresentació severa de la capacitat real
- **TDC + TEA**: solapament significatiu en planificació motora i integració sensorial. Molts alumnes amb TEA presenten perfils motors compatibles amb TDC; la rigidesa motora i la dificultat en habilitats motores noves són comunes en ambdós
- **TDC + TDL**: la planificació motora de la parla pot estar afectada (**dispraxia verbal**). L'alumne pot tenir dificultats tant en el motor oral (articulació, fluïdesa) com en el motor manual (escriptura, manipulació)
- **TDC + Altes capacitats (2e)**: la compensació intel·lectual retarda la detecció del TDC. L'alumne usa estratègies cognitives per compensar les dificultats motores, fins que les demandes motores superen la capacitat de compensació (generalment a primària mitjana o ESO)

#### Principis d'actuació

- **Adaptar el canal de sortida:** Oferir alternatives al motor manual — teclat, oral, visual, esquemes — sense reduir mai la profunditat conceptual ni cognitiva. El TDC afecta el canal de sortida, no el contingut que l'alumne és capaç de processar.
- **Adaptar l'educació física:** Proposar alternatives individuals, adaptar les regles dels esports d'equip, valorar l'esforç i la millora personal per sobre del rendiment absolut. L'exclusió d'EF no és acceptable; l'adaptació ho és.
- **Adaptar l'avaluació:** Permetre respostes orals, digitals o amb suport visual. Separar els criteris de presentació dels criteris de contingut. Proporcionar temps addicional en exàmens escrits.
- **Adaptar materials i entorn:** Instruments ergonòmics (llapis triangulars, tisores adaptades, grip per a regles), espai de treball organitzat, suport per organitzar materials (codis de colors, guia d'organització visual).

#### Línies vermelles

- **No confondre TDC amb mandra o falta de pràctica.** **Per què?** El TDC és neurològic. L'alumne s'esforça més que els iguals per a resultats inferiors. Exigir-li "més pràctica" sense adaptació és com exigir a un alumne miop que llegeixi millor sense ulleres.
- **No avaluar la competència conceptual a través de la producció escrita manual.** **Per què?** L'escriptura manual mesura l'habilitat motora (el TDC), no el coneixement de la matèria. Si un alumne pot explicar-ho oralment i no per escrit, la nota ha de reflectir el coneixement, no la cal·ligrafia.
- **No excloure d'EF.** **Per què?** L'alumne amb TDC necessita moviment adaptat, no exclusió. L'exclusió reforça l'estigma i priva d'oportunitats de millora. L'adaptació (alternatives, regles modificades, valoració de l'esforç) és la resposta educativa adequada.
- **No ridiculitzar la cal·ligrafia o la coordinació.** **Per què?** L'impacte en l'autoestima és devastador i persistent (Missiuna et al., 2008). Comentaris com "quina lletra més lletja" o "ets molt maldestre" tenen un efecte acumulatiu que genera evitació, ansietat i retraïment.
- **No esperar que "ja aprendrà amb pràctica".** **Per què?** El TDC és persistent i requereix **adaptació**, no repetició. La pràctica pot millorar parcialment habilitats concretes, però no elimina el trastorn de base. La resposta és adaptar el canal, no repetir el que no funciona.
- **No subestimar el cost energètic de l'escriptura manual.** **Per què?** Per a l'alumne amb TDC, escriure a mà és un exercici d'esforç cognitiu i motor que consumeix recursos que els iguals dediquen al contingut. La fatiga motora és real i acumulativa al llarg del dia escolar.

### 2. CONNEXIONS AMB ALTRES DOCUMENTS DEL CORPUS

- **M1_dislexia-dificultats-lectores**: Comorbiditat 40-50%. Ambdós afecten l'escriptura per vies diferents: motora (TDC) i fonològica (dislèxia). Veure dependència TDC×dislèxia
- **M1_TDAH**: Comorbiditat 50%. Disfunció executiva compartida. Doble barrera: desatenció + dificultat motora
- **M1_alumnat-TEA**: Solapament en planificació motora i integració sensorial
- **M1_TDL-trastorn-llenguatge**: Dispraxia verbal — connexió entre planificació motora oral i manual
- **M1_altes-capacitats**: Doble excepcionalitat (2e) possible. Compensació intel·lectual retarda la detecció
- **M1_creuament-variables-dependencies**: Dependencies TDC×dislèxia, TDC×TDAH
- **M2_carrega-cognitiva-adaptacio-textos**: L'escriptura manual augmenta la càrrega cognitiva extrínseca — l'alumne amb TDC dedica recursos a la mecànica motora que els iguals dediquen al contingut

### 3. DETECCIÓ (Variables de Context)

- **Senyals del docent:**
  - "Escriu molt lent i la lletra és gairebé il·legible, però quan li pregunto oralment, ho sap tot perfectament."
  - "No vol fer res a plàstica — diu que no li agrada, però crec que li costa molt retallat, enganxar i dibuixar."
  - "Sempre és l'últim a copiar de la pissarra, i a la meitat de la línia ja ha perdut el fil."
  - "A EF és molt maldestre — es cau, no atrapa la pilota, els companys ja no el volen al seu equip."
  - "Té el pupitre i la motxilla fets un desastre, perd els fulls constantment."
  - "Després d'un examen escrit llarg, em diu que li fa mal la mà i que no ha pogut acabar."

- **Senyals de l'alumne:**
  - Frustració o bloqueig davant tasques d'escriptura llarga — para, sacseja la mà, es queixa de dolor
  - Evitació d'activitats d'EF, plàstica, manualitats i laboratoris
  - Diferència molt marcada entre l'expressió oral (fluida, elaborada) i l'escrita (breu, il·legible, desorganitzada)
  - Rendiment molt variable depenent del format: millora dràsticament quan pot respondre oralment o amb teclat
  - Dificultat per gestionar materials: pèrdua de fulls, motxilla caòtica, pupitre desordenat

- **Senyals de context:**
  - Retard en fites motores a primera infància (caminar, vestir-se sol, usar coberts)
  - Derivació o seguiment previ per dificultats psicomotrius
  - Dificultats presents des de l'etapa d'Infantil (grafisme, autonomia)
  - Historial familiar de dificultats de coordinació o dispraxia

- **Anti-senyals:**
  - Dificultats únicament en L2 oral, sense component motor (possible barrera lingüística, no TDC)
  - Dificultats motores aparegudes sobtadament o associades a un event concret (descartar neurològic)
  - Millora ràpida i completa amb pràctica (el TDC és persistent)
  - Dificultats exclusivament en lectura i escriptura sense afectació motora general (valorar dislèxia)
  - Dificultat motora explicable per condició visual no corregida

### 4. HEURÍSTIQUES I RAONAMENT PER A L'AGENT

- **Principi general:** L'agent ha d'adaptar el canal de sortida motor (escriptura, manipulació, moviment) sense reduir la profunditat conceptual ni cognitiva. El TDC afecta la via motora, no la capacitat de pensar ni d'aprendre.

- **Heurístiques per a l'Agent DOCENT:**

  - **Nom:** Adaptació del canal de sortida per component motor afectat
  - **Quan aplica:** Quan el docent indica que l'alumne té TDC i es coneixen les àrees motores afectades (motricitat fina, grossa, o ambdues).
  - **Fonament:** El TDC és heterogeni — un alumne amb motricitat fina molt afectada però motricitat grossa acceptable necessita prioritàriament accés al teclat i instruments adaptats, mentre que un amb motricitat grossa predominant necessita adaptació d'EF i entorn físic.
  - **Exemple complet de raonament:** "El docent indica que l'alumna té TDC amb motricitat fina molt afectada, grau moderat, i accés al teclat disponible. L'agent ha de raonar que totes les tasques de producció escrita llarga (redaccions, exàmens, treballs) han de permetre l'ús del teclat o la tauleta. Les activitats de plàstica i tecnologia necessiten alternatives o adaptacions (tisores adaptades, plantilles prèvies, treball en parella amb rols complementaris). L'avaluació escrita ha de separar els criteris de contingut dels criteris de presentació: la nota de ciències no pot dependre de la cal·ligrafia. Per a les activitats curtes (còpia breu, exercicis de completar), l'alumna pot escriure a mà amb temps addicional i llapis ergonòmic. No s'ha de reduir el contingut conceptual — l'alumna té capacitat cognitiva normativa."

  - **Nom:** Adaptació d'educació física i activitats motores
  - **Quan aplica:** Quan el docent demana orientació per a l'EF o activitats amb component motor gruixut per a un alumne amb TDC.
  - **Fonament:** L'exclusió d'EF no és una adaptació acceptable. El moviment és beneficiós per a l'alumne amb TDC; el que cal és adaptar les condicions perquè la participació sigui significativa i no humiliant (Magalhães et al., 2011).
  - **Exemple complet de raonament:** "Un docent d'EF pregunta com gestionar un alumne amb TDC que no vol participar en els esports d'equip. L'agent ha de raonar que l'evitació és una resposta d'autoprotecció davant la humiliació repetida (ser l'últim triat, no atrapar la pilota, generar errors que costen punts a l'equip). L'agent recomanaria: (1) oferir alternatives individuals dins de la sessió (caminar, exercicis de força, ioga), (2) si l'alumne vol participar en l'esport d'equip, adaptar les regles (posicions menys exposades, criteris d'èxit adaptats), (3) en l'avaluació, valorar l'esforç, la constància i la millora personal per sobre del rendiment absolut, (4) mai comparar públicament el rendiment motor amb el dels iguals. L'objectiu és que l'alumne associï el moviment amb benestar, no amb vergonya."

  - **Nom:** Dissociació competència motora–competència conceptual en l'avaluació
  - **Quan aplica:** Quan es dissenyen activitats, rúbriques o criteris d'avaluació per a alumnat amb TDC.
  - **Fonament:** Avaluar la producció motora (cal·ligrafia, presentació, velocitat d'escriptura) com a mesura de la competència conceptual invalida els resultats per a l'alumne amb TDC.
  - **Exemple complet de raonament:** "Un docent demana una rúbrica per a un examen de ciències naturals per a un alumne amb TDC moderat amb accés al teclat. L'agent ha de separar els criteris motors (presentació, cal·ligrafia, organització visual del paper) dels criteris conceptuals (comprensió de conceptes, relació causa-efecte, argumentació). Per a l'alumne amb TDC, l'examen ha de poder-se fer amb teclat o, si és en paper, amb temps addicional significatiu (mínim 30% més). Els criteris de presentació no poden restar nota. Si l'examen és de resposta llarga, l'opció oral o digital ha d'estar disponible. L'agent ha de recordar que la fatiga motora és acumulativa: un examen de dues hores escrit a mà és exponencialment més costós per a l'alumne amb TDC que per als iguals."

- **Heurístiques per a l'Agent ALUMNE:**

  - **Nom:** Estratègies d'organització i producció escrita
  - **Quan aplica:** Quan l'alumne ha de fer una redacció, informe, projecte o qualsevol tasca de producció escrita.
  - **Fonament:** Per a l'alumne amb TDC, la barrera no és saber què escriure sinó l'acte físic d'escriure. L'andamiatge ha de reduir la càrrega motora, no la cognitiva.
  - **Exemple complet de raonament:** "Un alumne amb TDC ha d'escriure un treball sobre el canvi climàtic. L'agent primer verificaria si l'alumne té accés al teclat. Si sí: proporcionar un esquema amb seccions etiquetades ('Definició / Causes / Conseqüències / Solucions') i suggerir que escrigui directament al teclat, sense esborrany manuscrit previ. Si no: proporcionar el mateix esquema amb espais generosos, limitar l'extensió de cada secció (3-5 frases per bloc), i recordar que pot completar la informació oralment amb el docent. En ambdós casos, l'objectiu és que l'alumne demostri el seu coneixement sense que la barrera motora el limiti."

  - **Nom:** Gestió de la fatiga motora durant el dia escolar
  - **Quan aplica:** Quan l'alumne mostra signes de fatiga motora (dolor a la mà, parades freqüents, disminució de la qualitat gràfica al llarg del dia).
  - **Fonament:** La fatiga motora és acumulativa i real. L'alumne amb TDC consumeix més energia que els iguals en totes les tasques amb component motor, i al final del dia escolar té menys recursos disponibles (Zwicker et al., 2012).
  - **Exemple complet de raonament:** "Un alumne amb TDC diu que li fa mal la mà i que no pot acabar l'exercici a última hora. L'agent no ha d'interpretar-ho com a excusa sinó com un senyal de fatiga motora acumulada. L'agent recomanaria: (1) completar l'exercici oralment amb el docent, (2) si és possible, canviar a teclat per a la resta de la sessió, (3) per a futures planificacions, distribuir les tasques amb major càrrega motora al matí i reservar les opcions digitals o orals per a la tarda. No suposar manca de voluntat — l'alumne ha estat escrivint a mà tot el dia amb un esforç tres vegades superior al dels seus iguals."

---

## 6. INSTRUCCIONS D'ADAPTACIÓ TEXTUAL PER A L'LLM

### Barrera nuclear
**Accés motriu**: L'alumnat amb TDC/dispraxia té com a barrera principal l'accés motriu al material (escriptura, manipulació). Les adaptacions textuals per a l'LLM són mínimes — la majoria de necessitats són CSS/frontend (navegació per teclat, mida clicable dels elements).

### Instruccions per al prompt LLM

```
PERFIL: TDC / Dispraxia
- Estructura semàntica clara per navegació per teclat/commutador
- Evitar instruccions que requereixin motricitat fina (retallar, dibuixar, escriure a mà)
- Adaptar activitats: resposta oral o selecció en lloc d'escriptura lliure
```

### Mapa barrera → instruccions (prioritzat)

| Prioritat | Instruccions activades | Justificació (barrera) |
|---|---|---|
| **1a (accés)** | I-07 (navegació per teclat/commutador) | Barrera nuclear: accés motriu |
| **2a (estructura)** | H-19 (estructura semàntica H1-H3), B-02 (blocs amb títol) | Navegació accessible |

**Nota**: La majoria d'adaptacions per a TDC/dispraxia són CSS/FE (àrees clicables grans, navegació per teclat). L'LLM ha de garantir estructura semàntica i evitar instruccions que pressuposin motricitat fina.

---

## 5. FONTS DEL CORPUS

| # | Referència | Tipus | Any |
|---|-----------|-------|-----|
| 1 | APA. *DSM-5-TR. Developmental Coordination Disorder (315.4/F82).* | Diagnòstic | 2022 |
| 2 | WHO. *ICD-11. Developmental motor coordination disorder (6A04).* | Classificació | 2022 |
| 3 | Blank, R. et al. *European Academy for Childhood Disability (EACD) recommendations on DCD.* Developmental Medicine & Child Neurology. | Consens europeu | 2012 |
| 4 | Barnhart, R.C. et al. *Developmental Coordination Disorder.* Physical Therapy, 83(8), 722-731. | Revisió | 2003 |
| 5 | Missiuna, C. et al. *Children with DCD: At home, at school, and in the community.* CanChild Centre for Childhood Disability Research. | Recurs educatiu | 2008 |
| 6 | Kirby, A. & Sugden, D. *Children with developmental coordination disorders.* Journal of the Royal Society of Medicine, 100(4), 182-186. | Revisió | 2007 |
| 7 | Magalhães, L.C. et al. *Activities and participation in children with developmental coordination disorder.* Research in Developmental Disabilities, 32(4), 1352-1357. | Recerca | 2011 |
| 8 | Zwicker, J.G. et al. *Developmental coordination disorder: A review and update.* European Journal of Paediatric Neurology, 16(6), 573-581. | Neurociència | 2012 |
| 9 | Polatajko, H.J. *A clinical trial of the process-oriented treatment approach for children with developmental co-ordination disorder.* Developmental Medicine & Child Neurology, 37(4), 310-319. | Intervenció | 1995 |
| 10 | Missiuna, C. et al. *Missed and misunderstood: Children with coordination difficulties in the school system.* International Journal of Special Education, 22(1), 12-20. | Detecció | 2007 |
| 11 | Missiuna, C. et al. *Psychological distress in children with developmental coordination disorder and attention-deficit hyperactivity disorder.* Research in Developmental Disabilities, 16(6), 485-494. | Impacte emocional | 1995 |
| 12 | Generalitat de Catalunya. *Decret 150/2017, de 17 d'octubre, de l'atenció educativa a l'alumnat en el marc d'un sistema educatiu inclusiu.* DOGC. | Normatiu | 2017 |
| 13 | Generalitat de Catalunya. *Llei 17/2020, del 22 de desembre, de modificació de la Llei 12/2009, d'educació.* DOGC. | Normatiu | 2020 |

*13 fonts referencials -- document revisat 2026-03-27*
