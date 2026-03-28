---
modul: M1
titol: "Alumnat amb discapacitat auditiva"
tipus: caracteristica
subtipus: constitutiva
descripcio: "Discapacitat auditiva (hipoacúsia i sordesa): classificació audiomètrica, CREDA, MALL/SIAL, implant coclear, LSC, marc normatiu D150/2017 i Llei 17/2010"
review_status: revisat
locked: true
generat_at: 2026-03-18T12:59:19
actualitzat_at: 2026-03-27T23:00:00
variables_configurables:
  - nom: comunicacio
    etiqueta: "Mode de comunicació"
    tipus: enum
    valors: [oral, LSC, bimodal]
    obligatori: true
    defecte: oral
    descripcio: "Oral: amb pròtesi/implant. LSC: Llengua de Signes Catalana com a L1. Bimodal: oral + signes simultàniament"
    impacte: "LSC: contingut visual/escrit, intèrpret, LSC com a L1; Oral: subtítols, FM, verbalització clara; Bimodal: combinació"
  - nom: implant_coclear
    etiqueta: "Implant coclear"
    tipus: boolean
    obligatori: false
    defecte: false
    descripcio: "Porta implant coclear actiu?"
    impacte: "Amb implant: pot beneficiar-se de contingut oral amb suport visual; sense implant amb DA severa/pregona: comunicació principalment visual"
---

# 1. CONTINGUT ESPECÍFIC

## Definició i classificació

La **discapacitat auditiva** comprèn qualsevol pèrdua total o parcial de la capacitat auditiva que, un cop considerada la millor amplificació possible, afecta significativament la comunicació, el desenvolupament del llenguatge i l'aprenentatge. L'OMS estableix el llindar de discapacitat auditiva a partir d'una pèrdua superior a **25 dB** en l'orella amb millor audició.

S'avalua principalment a través de l'**audiometria tonal** a les freqüències de la parla: 500 Hz, 1.000 Hz, 2.000 Hz i 3.000 Hz.

### Classificació audiomètrica XTEC / CREDA

| Categoria | Abrev. | Pèrdua (dB) | Implicació funcional i comunicativa |
|:---|:---|:---|:---|
| **Audició normal** | — | ≤ 20 dB | Sense restriccions. |
| **Deficiència Auditiva Lleugera** | DAL | 21–40 dB | Dificultats en entorns sorollosos; pot passar desapercebuda; risc de retard articulatori. |
| **Deficiència Auditiva Mitjana 1r grau** | DAM1 | 41–55 dB | Alta dificultat per entendre la parla a volum normal; retard de llenguatge probable. |
| **Deficiència Auditiva Mitjana 2n grau** | DAM2 | 56–70 dB | Comprensió molt limitada sense pròtesi; amplificació constant necessària. |
| **Deficiència Auditiva Severa 1r grau** | DAS1 | 71–80 dB | Sols percep veus molt intenses; risc elevat de no adquisició del llenguatge oral sense intervenció primerenca. |
| **Deficiència Auditiva Severa 2n grau** | DAS2 | 81–90 dB | Percepció molt reduïda; depèn de pròtesi i suport logopèdic intensiu. |
| **Deficiència Auditiva Pregona 1r grau** | DAP1 | 91–100 dB | Sols percep sons molt forts; implant coclear freqüentment indicat. |
| **Deficiència Auditiva Pregona 2n grau** | DAP2 | 101–110 dB | Restes auditives molt limitades. |
| **Deficiència Auditiva Pregona 3r grau** | DAP3 | 111–119 dB | Restes auditives mínimes. |
| **Cofosi (sordesa total)** | — | ≥ 120 dB | Absència de percepció auditiva; comunicació visual/tàctil; LSC. |

> **Criteri de derivació al CREDA:** qualsevol alumne amb pèrdua auditiva confirmada, des de DAL, és susceptible de derivació per valoració. La intensitat del suport s'ajusta al grau de pèrdua i a l'impacte funcional real.

### Codis diagnòstics ICD-11

| Sistema | Codi | Denominació |
|:---|:---|:---|
| **ICD-11** (OMS, 2019) | **AB50** | Deficiència auditiva congènita |
| **ICD-11** | **AB51** | Deficiència auditiva adquirida |
| **ICD-11** | **AB52** | Sordesa no especificada |
| **ICD-10** (antic) | H90–H91 | Sordesa conductiva, neurosensorial i mixta |

## Tipologies

### Per localització anatòmica

| Tipus | Causa habitual | Característiques |
|:---|:---|:---|
| **Conductiva** | Otitis, tapó de cerumen, malformació oïda externa/mitjana | Sovint reversible amb tractament; amplificació molt efectiva |
| **Neurosensorial** | Dany a la còclea o al nervi auditiu (genètica, prematuritat, meningitis, ototòxics) | Generalment permanent; pròtesi auditiva o implant coclear |
| **Mixta** | Combinació de les dues anteriors | Tractament combinat |
| **Trastorn del Processament Auditiu Central (TPAC)** | Disfunció de les vies auditives centrals | AV normal a l'audiometria; falles en discriminació i comprensió en soroll; sovint infradiagnosticat; freqüent comorbiditat amb TDAH i TDL |

### Per moment d'adquisició

| Tipus | Descripció | Implicació educativa clau |
|:---|:---|:---|
| **Prelingual** | Apareix abans de l'adquisició del llenguatge (0–2 anys) | Risc de no adquisició del llenguatge oral sense intervenció primerenca; LSC pot ser L1 |
| **Perilingual** | Apareix durant l'adquisició (2–5 anys) | Intervenció logopèdica primerenca crítica; pronòstic variable |
| **Postlingual** | Apareix un cop el llenguatge oral és adquirit | Base lingüística consolidada; menys impacte en la lectoescriptura |

## Manifestacions a l'escola

### Senyals d'alerta per etapes

| Etapa | Senyals d'alerta |
|:---|:---|
| **Ed. Infantil (0–6)** | No es gira en sentir el seu nom; no localitza sons; retard en les primeres paraules; parla poc clara; no entén consignes senzilles; veu molt alta o indiferenciada |
| **Ed. Primària (6–12)** | Demana freqüentment que li repeteixin; distracció en entorns sorollosos; ortografia i articulació pobres sense altra causa; fatiga en escolta prolongada; se situa prop del professor/a |
| **ESO (12–16)** | Dificultats en exposicions orals; problemes en idiomes estrangers (comprensió oral); baixa participació oral; aïllament social; fatiga acumulada al final del dia |

### Per àmbits funcionals

| Àmbit | Alumnat hipoacúsic (DAL–DAS) | Alumnat sord (DAP–Cofosi) |
|:---|:---|:---|
| **Comunicació oral** | Dificultats en soroll; benefici de la lectura labial | Comunicació oral limitada; LSC com a llengua principal en molts casos |
| **Lectoescriptura** | Ortografia fonètica alterada; comprensió lectora afectada | Metodologia visual específica; el català/castellà pot ser L2 |
| **Matemàtiques** | Dificultats en explicacions orals llargues | Representació visual sistemàtica de totes les instruccions |
| **Idiomes estrangers** | Discriminació fonètica estrangera molt difícil | Adaptació curricular significativa necessària |
| **Educació Física** | No percep xiulets; dificultats amb instruccions en moviment | Senyals visuals (gestos, llum, contacte) en lloc d'acústics |
| **Entorn digital** | Subtítols en tots els vídeos; sistema FM; altaveus personals | Contingut en LSC sempre que sigui possible; subtítols activats |

## Barreres d'aprenentatge

- **Accés a la informació oral:** La major part de la comunicació escolar és oral (explicacions, debats, consignes, feedback). L'alumnat amb DA té un accés reduït o nul a aquest canal.
- **Soroll ambiental:** Les aules convencionals tenen nivells de soroll que degraden greument la relació senyal/soroll per a qui porta pròtesi o implant.
- **Fatiga auditiva:** L'esforç d'escolta compensatòria (lectura labial, atenció sostinguda) genera fatiga acumulativa al llarg del dia.
- **Llengua escrita com a L2:** Per a l'alumnat sord signant, el català/castellà escrit és una segona llengua; la comprensió lectora i l'expressió escrita requereixen metodologia específica.
- **Idiomes estrangers:** La discriminació fonètica en una llengua estrangera és especialment difícil; la part oral de l'anglès, francès, etc. pot ser inaccessible.
- **Comunicació no verbal perduda:** Tons de veu, ironies, dobles sentits, sorolls de fons significatius (riures, xiuxiuejos) que donen context social.
- **Aïllament social:** La dificultat per seguir converses ràpides entre iguals pot generar exclusió no intencionada però real.

## Necessitats prioritàries

1. **Accés a la comunicació:** Garantir que tota la informació arribi a l'alumne pel seu canal preferent (oral amplificat, LSC, bimodal, escrit).
2. **Sistema FM / Roger:** Micròfon del docent + receptor de l'alumne; millora decisivament la relació senyal/soroll. El CREDA el pot facilitar en préstec.
3. **Suport CREDA + MALL:** Intervenció logopèdica, assessorament al tutor/a, seguiment audiològic, orientació comunicativa.
4. **Subtítols en TOT material audiovisual:** Vídeos, podcasts, presentacions amb àudio. Sense excepció.
5. **Reducció del soroll:** Suro a potes de cadires, portes ben tancades, aula allunyada de fonts de soroll, panells acústics si és possible.
6. **Ubicació a l'aula:** Primera fila, de cara al docent, amb visió dels companys (lectura labial). Llum al rostre del docent, mai a contrallum.
7. **Temps addicional:** En avaluacions amb component oral o de comprensió lectora. Mínim +25%.
8. **Suport visual sistemàtic:** Esquemes, mapes conceptuals, instruccions escrites, pissarra digital — tot el que és oral ha de tenir un suport visual.
9. **Intèrpret de LSC:** Si la modalitat comunicativa és LSC, l'alumne té dret a intèrpret a l'aula (Llei 17/2010).

## Fortaleses a aprofitar

L'alumnat amb discapacitat auditiva desenvolupa capacitats compensatòries que són un actiu:
- **Agudesa visual:** Capacitat d'observació visual superior; detecten detalls visuals que altres no perceben.
- **Memòria visual:** Retenció superior d'informació presentada visualment (esquemes, gràfics, mapes).
- **Comunicació no verbal:** Domini de l'expressió corporal, gestual i facial; capacitat per llegir microexpressions.
- **Concentració en tasques visuals:** Capacitat de treball sostingut en tasques que no depenen del canal auditiu.
- **Identitat cultural rica (comunitat sorda):** Per a l'alumnat signant, la pertinença a la comunitat sorda és una font d'identitat, cultura i resiliència.
- **Bilingüisme LSC-català/castellà:** L'alumnat bilingüe en LSC i llengua oral té avantatges cognitius associats al bilingüisme.

## Perfils associats i comorbiditats

| Perfil associat | Prevalença | Implicació |
|:---|:---|:---|
| **TDL (Trastorn del Llenguatge)** | Freqüent confusió diagnòstica | Cal descartar DA abans de diagnosticar TDL; audiometria obligatòria en tot cas de retard de llenguatge |
| **TDAH** | Comorbiditat moderada, esp. amb TPAC | La fatiga auditiva pot semblar inatentió; avaluació diferencial necessària |
| **Discapacitat visual (sordceguesa)** | Poc freqüent però molt greu | Comunicació tàctil (dactilobraille); suport CREDV + CREDA |
| **TEA** | Minoritari | La DA pot emmascarar senyals de TEA o viceversa; avaluació especialitzada |
| **Discapacitat intel·lectual** | En algunes etiologies congènites | Adaptació curricular significativa + adaptació comunicativa |
| **TPAC** | Sovint infradiagnosticat | Audiometria normal però comprensió en soroll alterada; derivar a CREDA per valoració específica |

> **Alerta:** No confondre mai el retard de llenguatge per manca d'accés auditiu amb una discapacitat intel·lectual o un trastorn del llenguatge. Un alumne sord sense intervenció primerenca pot semblar tenir un retard cognitiu que NO existeix.

## L'implant coclear

L'**implant coclear (IC)** és un dispositiu electrònic que estimula directament el nervi auditiu, bypassing la còclea danyada. Està indicat en sordeses severes-pregones neurosensorials bilaterals.

### Implicacions educatives

| Aspecte | Detall |
|:---|:---|
| **Edat d'implantació** | Més primerenca = millor pronòstic en adquisició de llenguatge oral. Implantació < 2 anys: resultats excel·lents en molts casos. |
| **Rehabilitació** | Requereix logopèdia intensiva durant anys; el procés no és immediat. |
| **Expectatives** | L'IC no "cura" la sordesa; dóna accés a sons, però la comprensió requereix aprenentatge. El rendiment auditiu varia enormement entre persones. |
| **A l'aula** | L'alumne amb IC necessita igualment: sistema FM, ubicació preferent, subtítols, suport visual. No tractar com a "oient". |
| **Manteniment** | El processador extern necessita càrrega diària, recanvi de piles/bateries, i cal evitar cops i aigua. |
| **Decisió familiar** | L'IC és una decisió de la família; el centre NO pot pressionar. Respectar la modalitat comunicativa escollida (oral, LSC, bimodal). |

## La Llengua de Signes Catalana (LSC)

La **Llengua de Signes Catalana (LSC)** està reconeguda per la Llei 17/2010 del 3 de juny com a **llengua pròpia de la comunitat sorda de Catalunya**. No és una traducció del català sinó una llengua amb gramàtica, sintaxi i pragmàtica pròpies.

### Implicacions educatives

- L'alumnat sord signant té dret a rebre ensenyament en LSC o amb intèrpret de LSC.
- El català/castellà escrit és per a ells una **L2**: cal metodologia d'ensenyament de segones llengües, no d'alfabetització en L1.
- La LSC és un canal complet de comunicació: no és un "suport" ni un "recurs"; és una llengua plena.
- El respecte a la identitat sorda i a la LSC és un principi normatiu, no una opció del centre.
- El professorat pot aprendre LSC bàsica per facilitar la comunicació directa (cursos CREDA, FESOCA).

## Principis d'actuació

1. **Accés comunicatiu primer:** Abans de pensar en continguts, assegurar que l'alumne rep la informació pel seu canal preferent. Sense accés comunicatiu, no hi ha aprenentatge.
2. **Modalitat comunicativa respectada:** Oral, LSC o bimodal — és una decisió de la família i l'alumne, no del centre. El centre s'adapta, no al revés.
3. **Verbalització visual:** Parlar sempre de cara, amb bona il·luminació al rostre, sense objectes davant de la boca. No parlar mentre s'escriu a la pissarra.
4. **Suport visual sistemàtic:** Tot el que es diu oralment ha de tenir un equivalent visual disponible.
5. **Reducció del soroll:** Intervenir activament sobre l'acústica de l'aula; és una mesura de primera línia, no un luxe.
6. **Coordinació CREDA–MALL:** El CREDA és l'aliat principal; la comunicació ha de ser fluida, regular i bidireccional.
7. **Normalització:** L'alumne participa en totes les activitats amb les adaptacions necessàries. No excloure.

## Línies vermelles

- **No treure l'audiòfon o l'IC com a càstig:** Retirar l'accés auditiu és equivalent a tapar els ulls a un alumne vident. **Per què?** És una aggressió a la integritat funcional de la persona i vulnera els seus drets.
- **No parlar des de l'esquena o en moviment:** L'alumne que fa lectura labial necessita veure la cara. **Per què?** Cada vegada que es parla d'esquena, l'alumne perd tota la informació i queda exclòs.
- **No assumir que l'IC fa que l'alumne "senti normal":** L'alumne amb IC segueix necessitant totes les mesures de suport. **Per què?** L'IC dóna accés a sons, no comprensió automàtica; el rendiment varia enormement.
- **No excloure la LSC:** Si la família ha triat LSC, no intentar "normalitzar" l'alumne forçant l'oralisme. **Per què?** La Llei 17/2010 garanteix el dret a la LSC; negar-la atempta contra la identitat lingüística.
- **No excloure d'activitats per "raons pràctiques":** No treure l'alumne d'Ed. Física, sortides o debats. **Per què?** El D150/2017 garanteix la participació; l'exclusió empobreix l'experiència educativa.
- **No confondre sordesa amb discapacitat intel·lectual:** El retard de llenguatge per manca d'accés auditiu NO és un retard cognitiu. **Per què?** Confondre-ho porta a rebaixar expectatives i a un currículum empobrit.

## Marc normatiu català

| Norma | Aplicació |
|:---|:---|
| **Decret 150/2017, art. 3.2.a** | Sordesa pregona i severa amb alt impacte funcional → **NEE** → **PI obligatori** (art. 18). Hipoacúsia lleugera/moderada → **NESE** → mesures addicionals (art. 7). |
| **D150/2017, art. 7** | Mesures addicionals: suport MALL, sistema FM, adaptació de materials, temps addicional. |
| **D150/2017, art. 9** | Mesures intensives: atenció directa CREDA; SIAL; MALL de centre o SIAL. |
| **D150/2017, art. 14** | L'EAP coordina l'avaluació psicopedagògica i la derivació al CREDA. |
| **DOIGC 2025-2026** | Protocols de coordinació CREDA–EAP–centre. |
| **Llei 17/2010, del 3 de juny, de la LSC** | Reconeix la **Llengua de Signes Catalana** com a llengua pròpia de la comunitat sorda de Catalunya i garanteix el dret al seu ús en l'educació. |
| **Llei 17/2020** | Accessibilitat universal; obligació de subtitulació i recursos d'accés auditiu en entorns educatius. |

## El CREDA: servei de referència

Els **Centres de Recursos Educatius per a Deficients Auditius (CREDA)** són serveis educatius específics del Departament d'Educació de Catalunya per a l'alumnat amb pèrdua auditiva i/o trastorns greus del llenguatge i la comunicació.

### Destinataris

- Infants i joves amb pèrdua auditiva (0–18 anys) i llurs famílies.
- Alumnat amb greus trastorns del llenguatge i/o la comunicació (3–12 anys).
- Centres i professorat que atenen aquest alumnat.
- Professorat especialitzat MALL de la zona educativa.

### Funcions principals

- Valoració i seguiment del procés evolutiu audiològic, comunicatiu i lingüístic.
- Intervenció logopèdica específica complementària a les mesures del centre.
- Assessorament i formació al professorat i equips directius.
- Orientació a les famílies sobre modalitat comunicativa (oralisme, LSC, bilingüisme).
- Préstec de material especialitzat (sistemes FM, material logopèdic, etc.).
- Atenció primerenca (0–3 anys) en col·laboració amb CDIAP i serveis de salut.

### Seus territorials

| Seu | Zona d'influència |
|:---|:---|
| **CREDA Pere Barnils** | Barcelona ciutat (Consorci d'Educació de Barcelona) |
| **CREDA Catalunya Central** | Osona, Bages, Berguedà, Anoia |
| **CREDA Lleida** | Lleida i comarques |
| **CREDA Tarragona** | Tarragona i comarques |
| **CREDA Girona** | Girona i comarques |
| **CREDA Maresme–Vallès Oriental** | Maresme, Vallès Oriental |

### Protocol d'accés

**Via EAP (cas general):**
Centre detecta → Tutor/a informa CAD → CAD sol·licita valoració EAP → EAP deriva al CREDA amb full protocolitzat de demanda

**Via directa (0–3 anys):**
Família, CDIAP o pediatra → accés directe al CREDA (diagnòstic ORL previ recomanat però no imprescindible)

## Professionals especialitzats: MALL i SIAL

| Professional | Nom complet | Funcions principals |
|:---|:---|:---|
| **MALL** | Mestre/a d'Audició i Llenguatge | Intervenció logopèdica directa; suport a l'aula ordinària; coordinació CREDA–família–tutoria; orientació al professorat |
| **MESI** | Mestre/a Especialista en Suport Intensiu | Suport intensiu a alumnat amb NEE severes a l'aula ordinària |
| **MALL de SIAL** | MALL adscrit al Suport Intensiu a l'Audició i el Llenguatge | Projectes específics d'audició i llenguatge per a tot el centre; col·labora amb l'equip directiu en la inclusió |

> El **SIAL** és un recurs per a centres amb concentració significativa d'alumnat amb pèrdua auditiva que requereix intervenció d'alta intensitat de manera estable.

## Mesures educatives per nivell (D150/2017)

### Mesures universals (tot el grup classe)

- Reduir el soroll de fons a l'aula (suro a les potes de les cadires, portes ben tancades, evitar aules prop de fonts de soroll).
- Parlar sempre de cara a l'alumne; no parlar mentre s'escriu a la pissarra.
- Suport visual sistemàtic: esquemes, imatges, subtítols activats en tots els vídeos.
- Ubicar l'alumne a la primera fila, allunyat de fonts de soroll extern (finestra al carrer, porta).
- Confirmar la comprensió de consignes de manera individualitzada (no preguntar «ho heu entès?» al grup).
- Verbalitzar clarament el que es posa a la pissarra digital.

### Mesures addicionals (hipoacúsia DAL–DAS — NESE)

- **Sistema FM / Roger:** Micròfon del/la mestre/a + receptor de l'alumne; millora decisivament la relació senyal/soroll; el CREDA el pot facilitar en préstec.
- Temps addicional en proves (+25% com a mínim).
- Materials escrits com a suport de totes les explicacions orals.
- Adaptació de les proves d'idiomes estrangers: substitució de la part oral per format escrit o supressió justificada.
- Suport logopèdic del MALL (sessions individuals o en petit grup, dins o fora de l'aula).
- Subtítols en tots els materials audiovisuals; plataformes digitals del centre amb subtitulat obligatori.
- Avaluació alternativa en continguts amb alta càrrega oral (exposicions → presentació escrita + visual).

### Mesures intensives (sordesa DAS2–Cofosi — NEE, PI obligatori)

- Atenció directa del CREDA: sessions setmanals de logopèdia especialitzada.
- Intèrpret de LSC a l'aula si la modalitat comunicativa és signant (Llei 17/2010).
- MALL assignat al centre o SIAL si hi ha concentració d'alumnat.
- PI amb objectius comunicatius, lingüístics i acadèmics; revisió trimestral amb CREDA–EAP–família.
- Adaptació curricular significativa en idiomes estrangers si l'impacte funcional ho justifica.
- Coordinació CREDA–EAP–centre–família amb periodicitat mínima trimestral.

## Tecnologia de suport

| Eina | Funció | Quan |
|:---|:---|:---|
| **Audiòfon** | Amplificació del so | DA lleugera a severa; ús constant |
| **Implant coclear** | Estimulació directa del nervi auditiu | DA severa-pregona; decisió mèdica i familiar |
| **Sistema FM / Roger** | Transmissió directa de la veu del docent a l'audiòfon/IC | Aula; millora relació senyal/soroll |
| **Bucle magnètic** | Camp magnètic que transmet l'àudio a audiòfons amb posició T | Sales grans, auditoris |
| **Subtitulació automàtica** | Transcripció en temps real de la parla | Totes les activitats amb àudio |
| **Línia Braille + lector pantalla** | Per a sordceguesa | Combinació DA + DV |
| **Aplicacions de transcripció** | Google Live Transcribe, Ava, Microsoft Teams subtítols | Classes, tutories, reunions |

# 2. CONNEXIONS AMB ALTRES DOCUMENTS DEL CORPUS

- **M1_model-caracteritzacio-diversitat.md** → Marc de 3 nivells; discapacitat auditiva = característica constitutiva
- **M1_neurodiversitat-NESE.md** → Sordesa severa/pregona = NEE dins D150/2017
- **M1_plans-individuals-PAD-PI.md** → PI obligatori per a NEE; el CREDA participa en l'elaboració
- **M1_discapacitat-visual.md** → Perfil associat: sordceguesa (co-ocurrència)
- **M1_TDL-trastorn-llenguatge.md** → Diagnòstic diferencial: cal descartar DA abans de diagnosticar TDL
- **M1_TDAH.md** → Diagnòstic diferencial: la fatiga auditiva pot semblar inatentió
- **M2_mesures-suports-inclusius.md** → Escala de mesures: universals → addicionals → intensives
- **M2_carrega-cognitiva-adaptacio-textos.md** → Adaptació de textos: suport visual, estructura clara
- **M3_comunicacio-augmentativa.md** → LSC, sistemes augmentatius i alternatius
- **M3_llengua-diversitat.md** → LSC com a llengua pròpia; bilingüisme LSC-català
- **M5_accessibilitat-digital.md** → Subtitulació, WCAG 2.1, accessibilitat auditiva digital
- **M9_normativa-inclusio.md** → D150/2017, Llei 17/2010 (LSC), Llei 17/2020 (accessibilitat)

# 3. DETECCIÓ (Variables de Context)

**Senyals del docent:**
- "Tinc un alumne que no es gira quan el crido i demana que li repeteixin tot."
- "L'alumne es distreu molt en entorns sorollosos però en silenci funciona bé."
- "Necessito saber com configurar el sistema FM que ens ha portat el CREDA."
- "Tinc un alumne sord amb intèrpret de LSC; com coordino les explicacions?"
- "L'alumne amb implant coclear segueix tenint dificultats; pensava que ja sentia bé."
- "Com adapto els exàmens d'anglès per a un alumne amb hipoacúsia severa?"

**Senyals de l'alumne:**
- "No entenc el profe quan parla d'esquena a la pissarra."
- "Em canso molt a les tardes i em perdo coses."
- "Els vídeos sense subtítols no els puc seguir."
- "No sento bé el profe quan els companys fan soroll."
- "Necessito que em miris quan em parles."

**Senyals de context:**
- Aula amb reverberació alta, finestres al carrer, soroll ambiental.
- Activitat amb component oral predominant (debat, dictàt, listening d'anglès).
- Vídeo o podcast sense subtítols.
- Canvi de professorat (el nou no coneix les mesures de l'alumne).
- Sortida escolar a espai sorollós (museu interactiu, fàbrica).
- Examen oral o exposició davant del grup.

**Anti-senyals:**
- L'alumne segueix explicacions orals sense dificultat en tots els contextos (DA descartada o compensada).
- Les dificultats són exclusivament de comprensió lectora sense component auditiu (considerar dislèxia, TDL).
- L'alumne "no escolta" selectivament segons l'interès (explorar component conductual/motivacional).
- Les dificultats apareixen només en una matèria concreta (pot ser curricular, no auditiu).

# 4. HEURÍSTIQUES I RAONAMENT PER A L'AGENT

**Principi general:** L'adaptació per a l'alumnat amb DA és fonamentalment d'accés comunicatiu. El canal canvia; el contingut i l'exigència NO. Si l'alumne no accedeix a la informació, el problema és de l'entorn, no de l'alumne.

## Heurístiques per a l'Agent DOCENT

### H1: Canal comunicatiu primer, contingut després
- **Quan aplica:** Quan un docent prepara una activitat i té un alumne amb DA al grup.
- **Raonament:** Abans de pensar en el contingut, s'ha de garantir l'accés comunicatiu. Si l'alumne no rep la informació, no pot aprendre. L'ordre és: 1) canal accessible, 2) contingut, 3) avaluació.
- **Resposta tipus:** "Comprova que l'alumne rep la informació: FM activat? Subtítols als vídeos? Instruccions escrites disponibles? Si l'alumne usa LSC, l'intèrpret està informat del tema? Un cop el canal està assegurat, la planificació de l'activitat és la mateixa que per a la resta."

### H2: Soroll = barrera invisible
- **Quan aplica:** Quan un docent reporta que l'alumne "no presta atenció" o "es distreu".
- **Raonament:** En un alumne amb DA, la distracció aparent sovint és fatiga auditiva per excés de soroll. Cal intervenir sobre l'acústica ABANS de qüestionar l'atenció.
- **Resposta tipus:** "Pregunta't: l'aula és sorollosa? Hi ha reverberació? L'alumne porta el FM? Les cadires tenen protectors de suro? En la majoria de casos, millorant l'acústica es resol la 'inatentió'. Si persisteix, considera fatiga acumulativa: proporciona pauses breus o alterna activitats orals amb visuals."

### H3: L'implant coclear no és una solució màgica
- **Quan aplica:** Quan un docent o família expressa frustració perquè l'alumne "ja porta implant i hauria de sentir bé".
- **Raonament:** L'IC dóna accés a sons, no comprensió automàtica. El rendiment varia enormement segons l'edat d'implantació, la rehabilitació, el context acústic i la complexitat lingüística.
- **Resposta tipus:** "L'alumne amb IC necessita TOTES les mesures: FM, subtítols, ubicació preferent, suport visual. L'IC ajuda, però no elimina la necessitat d'adaptació. Compara-ho amb unes ulleres: milloren la visió, però si la lletra és massa petita, no serveixen."

## Heurístiques per a l'Agent ALUMNE

### H1: Gestió de la fatiga auditiva
- **Quan aplica:** Quan l'alumne reporta cansament, dificultat per concentrar-se a les últimes hores, mal de cap.
- **Raonament:** La fatiga auditiva és acumulativa i real. No és mandra; és un límit fisiològic de l'esforç d'escolta compensatòria.
- **Resposta tipus:** "La fatiga que sents és normal i no és culpa teva. Pots demanar pauses breus, alternar entre escolta i lectura, o demanar al professor que et doni les instruccions per escrit les últimes hores del dia."

### H2: Autoadvocacia comunicativa
- **Quan aplica:** Quan l'alumne no entén alguna cosa, no rep el suport que necessita, o es troba en un entorn no adaptat.
- **Raonament:** L'alumne ha d'aprendre a demanar el que necessita sense sentir-se una càrrega. Saber comunicar les pròpies necessitats és una competència clau.
- **Resposta tipus:** "Tens dret a entendre tot el que es diu a classe. Si no sents bé, pots dir: 'Professor/a, podeu parlar-me de cara?' o 'Podeu activar els subtítols del vídeo?'. No és una molèstia; és el teu dret."

# 5. FONTS

| # | Referència | Rellevància |
|---|-----------|-------------|
| 1 | OMS (2019). *ICD-11: International Classification of Diseases, 11th Revision.* Codis AB50–AB52. | Classificació diagnòstica de referència |
| 2 | CREDA (2024). *Guia de serveis educatius per a alumnat amb pèrdua auditiva a Catalunya.* Departament d'Educació. | Grups, funcions, protocol d'accés |
| 3 | Decret 150/2017, de 17 d'octubre, de l'atenció educativa a l'alumnat en el marc d'un sistema educatiu inclusiu. DOGC 7477. | NEE, PI obligatori, mesures |
| 4 | Llei 17/2010, del 3 de juny, de la Llengua de Signes Catalana. DOGC 5647. | Reconeixement LSC; dret a l'educació en LSC |
| 5 | Llei 17/2020, de 22 de desembre, d'accessibilitat. DOGC 8303. | Accessibilitat universal; subtitulació |
| 6 | DOIGC 2025-2026. Departament d'Educació. *Educació inclusiva: protocols de derivació.* | Coordinació CREDA–EAP–centre |
| 7 | XTEC (2024). *Classificació de la pèrdua auditiva: taula de referència CREDA.* | Classificació audiomètrica catalana |
| 8 | Marschark, M. & Spencer, P. E. (2010). *The Oxford Handbook of Deaf Studies, Language, and Education.* Oxford University Press. | Marc teòric de l'educació de l'alumnat sord |
| 9 | Humphries, T. et al. (2012). "Language acquisition for deaf children: Reducing the harms of zero tolerance to the use of alternative approaches." *Harm Reduction Journal*, 9(1), 16. | Evidència sobre accés primerenc a la llengua de signes |
| 10 | FESOCA (2023). *La Llengua de Signes Catalana: guia per a centres educatius.* Federació de Persones Sordes de Catalunya. | Guia pràctica LSC en centres |
| 11 | Anderson, K. L. & Goldstein, H. (2004). "Speech perception benefits of FM and infrared devices to children with hearing aids in a typical classroom." *Language, Speech, and Hearing Services in Schools*, 35(2), 169–184. | Evidència sobre eficàcia del sistema FM |
| 12 | Moeller, M. P. (2000). "Early intervention and language development in children who are deaf and hard of hearing." *Pediatrics*, 106(3), e43. | Evidència sobre intervenció primerenca |

*12 fonts · document revisat manualment amb contingut clínic i normatiu*

---

## 6. INSTRUCCIONS D'ADAPTACIÓ TEXTUAL PER A L'LLM

### Barrera nuclear
**Lèxica i sintàctica (en sordesa prelocutiva)**: L'alumnat amb discapacitat auditiva prelocutiva signant té com a barrera principal la comprensió del text escrit — la llengua escrita és efectivament una L2. La simplificació lingüística és similar a la d'un nouvingut.

### Instruccions per al prompt LLM

```
PERFIL: Discapacitat Auditiva
- Tractar com L2 en sordesa prelocutiva signant
- Simplificació lingüística similar a nouvingut
- Suport visual com a compensació
```

### Mapa barrera → instruccions (prioritzat)

| Prioritat | Instruccions activades | Justificació (barrera) |
|---|---|---|
| **1a (lèxica/sintàctica)** | H-20 (simplificació com L2), A-01 (vocab freqüent), A-07 (una idea per frase), A-12 (longitud frase), A-13 (eliminació subordinades) | Barrera lèxica i sintàctica en sordesa prelocutiva |
| **2a (visual)** | D-01 (emojis suport), D-02 (esquema procés) | Suport visual com a compensació |

**Nota**: La gravetat de la barrera depèn del tipus de sordesa. En sordesa postlocutiva amb bona competència lectora, l'adaptació textual és mínima — les necessitats són principalment de frontend (subtítols, bucle magnètic).
