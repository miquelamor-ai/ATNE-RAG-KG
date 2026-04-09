# Matriu de traçabilitat: instruccions ATNE ↔ marcs teòrics

**Actualitzat**: 2026-04-09
**Instruccions al catàleg**: 98 (20 SEMPRE, 31 NIVELL, 43 PERFIL, 3 COMPLEMENT, 1 absorbit)
**Instruccions amb gradació MECR** (`mecr_detail`): 22
**Macrodirectives**: 10 (LÈXIC, SINTAXI, ESTRUCTURA, COGNITIU, QUALITAT, MULTIMODAL, AVALUACIÓ, PERSONALITZACIÓ, PERFIL, ENRIQUIMENT)

Cada instrucció del catàleg ATNE amb la seva correspondència als marcs de referència, activació, gradació i supressió.

## Llegenda marcs

| Codi | Marc | Font |
|------|------|------|
| **UNE** | UNE 153101:2018 EX — Lectura Fàcil | AENOR, 2018 |
| **IFLA** | Guidelines for Easy-to-Read Materials | IFLA Professional Report 120, 2010 |
| **MECR** | Marc Europeu Comú de Referència (CEFR) | Consell d'Europa, 2001/2020 |
| **CC** | Comunicació Clara / Plain Language | "Siguem clars" Ajuntament BCN, 2022; ISO 24495-1:2023 |
| **DUA** | Disseny Universal per a l'Aprenentatge | CAST UDL Guidelines 3.0, 2024 |
| **CLT** | Cognitive Load Theory | Sweller, 1988; Mayer, 2009 |
| **ZPD** | Zona de Desenvolupament Pròxim | Vygotsky, 1978 |
| **NE** | Neuroeducació / Neurociència lectora | Dehaene, 2009; Wolf, 2018 |
| **DSM** | DSM-5 / literatura clínica per perfil | APA, 2013 + literatura específica |
| **M1-M3** | Corpus FJE (documents ATNE) | Producció pròpia basada en fonts |

## Llegenda activació

| Tipus | Significat | Quantes |
|-------|-----------|---------|
| **SEMPRE** | Tota adaptació | 20 |
| **NIVELL** | Segons MECR sortida (amb o sense gradació) | 31 |
| **NIVELL GRADUAT** | NIVELL amb `mecr_detail` — text diferent per nivell | 22 de 31 |
| **PERFIL** | Segons característiques alumne + sub-variables | 43 |
| **COMPLEMENT** | Segons complements activats | 3 |

## Llegenda columnes traçabilitat

| Columna | Significat |
|---------|-----------|
| **Activ.** | SEMPRE / NIVELL / NIVELL GRADUAT / PERFIL / COMPLEMENT |
| **Macro** | Macrodirectiva on s'agrupa al prompt |
| **Perfils** | Perfils que l'activen (si PERFIL) |
| **Nivells** | Nivells MECR que l'activen (si NIVELL) |
| **Suprimida per** | Perfils que la desactiven |
| **Intensificada per** | Sub-variables que en modifiquen el text |

---

## A. ADAPTACIÓ LINGÜÍSTICA — LÈXIC (Macro: LÈXIC)

| ID | Instrucció | Activ. | Perfils | Nivells | Suprimida per | Intensificada per | Marcs |
|---|---|---|---|---|---|---|---|
| A-01 | Vocabulari freqüent. Substitueix termes poc habituals. | SEMPRE | — | — | altes_capacitats, dislèxia | — | UNE §Voc, IFLA N1-N2, MECR A1-B1, CC Pas 2, DUA P1.3, CLT intrínseca |
| A-02 | Termes tècnics en **negreta** amb definició entre parèntesis. | SEMPRE | — | — | — | — | UNE §Voc, IFLA N2, CC Pas 4, DUA P1.3, ZPD scaffolding |
| A-03 | Repetició lèxica: un terme = un concepte. No sinònims. | SEMPRE | — | — | altes_capacitats, dislèxia | — | UNE §Voc, IFLA N1-N2, CLT extrínseca |
| A-04 | Referents pronominals explícits: si ambigu, repeteix nom. | SEMPRE | — | — | — | — | UNE §Frases, MECR A1-A2, CC Pas 2, CLT extrínseca |
| A-05 | Elimina expressions idiomàtiques, metàfores, figurat. Tot literal. | SEMPRE | — | — | altes_capacitats, tea | — | UNE §Voc, IFLA N1, MECR A1, CLT intrínseca, DSM TEA |
| A-06 | Elimina polisèmia: cada paraula en un sol sentit. | **NIVELL GRADUAT** | — | pre-A1→B1 | — | — | UNE §Voc, MECR A1-A2 unívoc, CLT intrínseca |
| A-14 | Connectors explícits: per tant, a més, en canvi. | SEMPRE | — | — | — | — | UNE §Org, MECR A2+ cohesió, CC Pas 1, CLT germana |
| A-15 | Scaffolding decreixent (Vygotsky): 1a=def completa, 2a=breu, 3a=sol. | **NIVELL GRADUAT** | — | pre-A1→B1 | — | — | DUA P1.3, ZPD, CLT scaffolding |
| A-16 | Desnominalitza: noms abstractes → verbs. | SEMPRE | — | — | altes_capacitats | — | MECR A1-A2, CC Pas 2, CLT intrínseca, NE Dehaene |
| A-17 | Evita negacions múltiples. Reformula en positiu. | **NIVELL GRADUAT** | — | pre-A1→B1 | — | — | UNE §Frases, MECR A1-B1, CC Pas 2, CLT intrínseca |
| A-18 | Dates en format complet (12 de març de 2026). | SEMPRE | — | — | — | — | UNE §Ortotip, IFLA N1, CC Pas 2, M3 corpus FJE |
| A-19 | Sigles: forma completa la 1a vegada. | SEMPRE | — | — | — | — | UNE §Voc, CC Pas 2, CLT intrínseca |
| A-20 | Controla densitat lèxica: redueix paraules contingut/frase. | **NIVELL GRADUAT** | — | pre-A1→A2 | tdl | — | MECR A1-A2, CLT intrínseca |
| A-21 | Descompón paraules compostes llargues. | PERFIL | dislèxia, nouvingut | — | — | — | UNE §Voc, NE Wolf 2018 |
| A-22 | Concreta quantificadors: 'molts' → 'més de 50'. | NIVELL | — | pre-A1→A2 | — | — | MECR A1 concret, CLT intrínseca |
| A-23 | Evita cultismes i llatinismes. Equivalents patrimonials. | NIVELL | — | pre-A1→A2 | — | — | UNE §Voc, MECR A1-A2 quotidià |
| A-29 | **NOU** Evita adverbis acabats en -ment. Reformula. | **NIVELL GRADUAT** | — | pre-A1→A2 | — | — | UNE §Voc, CLT intrínseca |
| A-30 | **NOU** Evita anglicismes. Equivalents habituals en català. | PERFIL | nouvingut, tdl | — | — | — | UNE §Voc, CC |

## A. ADAPTACIÓ LINGÜÍSTICA — SINTAXI (Macro: SINTAXI)

| ID | Instrucció | Activ. | Perfils | Nivells | Suprimida per | Intensificada per | Marcs |
|---|---|---|---|---|---|---|---|
| A-07 | Una idea per frase. Divideix frases llargues. | SEMPRE | — | — | altes_capacitats | — | UNE §Frases, IFLA N1, MECR A1, CC Pas 2, CLT extrínseca |
| A-08 | Veu activa obligatòria. Transforma passives. | **NIVELL GRADUAT** | — | pre-A1→B1 | — | — | UNE §Frases, MECR A1-A2, CC Pas 2 |
| A-09 | Subjecte explícit a cada frase. No elideixis. | **NIVELL GRADUAT** | — | pre-A1→B1 | — | — | UNE §Frases, MECR A1 SVO, CLT extrínseca |
| A-10 | Ordre canònic: SVO. Evita inversions. | **NIVELL GRADUAT** | — | pre-A1→B1 | — | — | UNE §Frases, MECR A1-A2, Lingüística: ordre no marcat |
| A-11 | Puntuació simplificada. | **NIVELL GRADUAT** | — | pre-A1→B1 | — | — | UNE §Ortotip, CLT extrínseca |
| A-12 | Longitud frase per MECR: pre-A1=3-5, A1=5-8, A2=8-12, B1=12-18, B2=25. | **NIVELL GRADUAT** | — | tots | — | — | UNE §Frases, MECR descriptors, CLT |
| A-13 | Subordinades per MECR: pre-A1=zero, A1=coordinades, A2=simples. | **NIVELL GRADUAT** | — | tots | — | — | UNE §Frases, MECR descriptors gramaticals |
| A-24 | Present indicatiu preferent. Evita subjuntiu/condicional. | **NIVELL GRADUAT** | — | pre-A1→A2 | — | — | UNE §Frases, MECR A1 present simple |
| A-25 | Formes verbals simples. Evita perífrasis. No gerundis. | **NIVELL GRADUAT** | — | pre-A1→A2 | — | — | UNE §Frases, MECR A1-A2 formes simples |
| A-26 | Evita incisos parentètics llargs. Frase independent. | **NIVELL GRADUAT** | — | pre-A1→B1 | — | — | UNE §Ortotip, CLT extrínseca |
| A-27 | Retalla text al 60-70%. Elimina exemples secundaris. | PERFIL | tdah, di | — | — | — | CC Pas 3, CLT redueix volum, DSM TDAH fatiga |
| A-28 | **NOU** Evita impersonals (cal, s'ha de). Dirigeix-te al lector. | **NIVELL GRADUAT** | — | pre-A1→A2 | — | — | UNE §Frases, CC centrat receptor |

## B. ESTRUCTURA I ORGANITZACIÓ (Macro: ESTRUCTURA)

| ID | Instrucció | Activ. | Perfils | Nivells | Suprimida per | Intensificada per | Marcs |
|---|---|---|---|---|---|---|---|
| B-01 | Paràgrafs curts: 3-5 frases. Un tema per paràgraf. | SEMPRE | — | — | — | — | UNE §Org, IFLA N1-N2, CC Pas 1, DUA P1.3, CLT chunking Miller |
| B-02 | Blocs temàtics amb títol descriptiu. Format pregunta. | SEMPRE | — | — | — | — | UNE §Org, IFLA N2-N3, CC Pas 1, DUA P1.3, Advance organizer Ausubel |
| B-03 | Frase tòpic al principi de cada paràgraf. | SEMPRE | — | — | — | — | UNE §Org, CC Pas 1, Advance organizer |
| B-04 | Llistes en lloc d'enumeracions dins del text. | **NIVELL GRADUAT** | — | pre-A1→B1 | — | — | UNE §Org, CC Pas 5, DUA P1.3, CLT extrínseca |
| B-05 | Estructura deductiva: general → particular. | NIVELL | — | pre-A1→B1 | — | — | CC Pas 1, CLT esquemes mentals |
| B-06 | Ordre cronològic per processos i seqüències. | NIVELL | — | pre-A1→B1 | — | — | UNE §Org, CC Pas 1 |
| B-07 | Resum anticipatiu (advance organizer). | **NIVELL GRADUAT** | — | pre-A1→A2 | — | — | DUA P1.3, Advance organizer Ausubel 1968 |
| B-08 | Resum final recapitulatiu. | **NIVELL GRADUAT** | — | pre-A1→B1 | — | — | DUA P1.3 |
| B-09 | Numera passos i seqüències. Cada pas en línia separada. | NIVELL | — | pre-A1→B1 | — | — | UNE §Org, CC Pas 5 |
| B-10 | Transicions entre seccions: 'Ja hem vist X. Ara veurem Y.' | SEMPRE | — | — | — | — | UNE §Org, CC Pas 1, Senyalització Mayer |
| B-11 | Salt de línia entre idees. Cada idea independent. | NIVELL | — | pre-A1→A2 | — | — | UNE §Ortotip, IFLA N1, DUA P1.3 |
| B-13 | Indicadors progrés: [Secció X de Y]. | PERFIL | tdah | — | — | — | DUA P3 autoregulació, DSM TDAH |
| B-14 | Taules per informació comparativa. Markdown. | NIVELL | — | pre-A1→B1 | — | — | CC Pas 5, DUA P1.1 múltiples representacions |

## C. SUPORT COGNITIU (Macro: COGNITIU)

| ID | Instrucció | Activ. | Perfils | Nivells | Suprimida per | Intensificada per | Marcs |
|---|---|---|---|---|---|---|---|
| C-01 | Limita conceptes nous/paràgraf per MECR. | **NIVELL GRADUAT** | — | tots | — | tdah.baixa_memoria_treball → -1 nivell | DUA P1.3, CLT intrínseca Sweller, Límit memòria treball |
| C-02 | Reforç immediat de cada concepte nou. | **NIVELL GRADUAT** | — | pre-A1→B1 | — | — | CC Pas 4, DUA P1.3, CLT elaboració |
| C-04 | Chunking: blocs de 3-5 elements. | SEMPRE | — | — | — | tdah.baixa_memoria → "2-3 elements" | CLT Miller 1956 7±2, Cowan 2001 4±1 |
| C-05 | Glossari previ (pre-training). | **NIVELL GRADUAT** | — | pre-A1→A2 | — | — | UNE §Voc glossari, CC Pas 4, DUA P1.3, CLT pre-training Sweller |
| C-06 | Analogies amb experiències quotidianes. | **NIVELL GRADUAT** | — | pre-A1→B1 | — | — | MECR A1-A2 concrets, CC Pas 4, DUA P3.1, CLT esquemes previs |
| C-08 | Anticipació vocabulari: glossari → text. | NIVELL | — | pre-A1→A2 | — | — | DUA P1.3, CLT pre-training Sweller |

**Nota**: C-03 (eliminació redundància decorativa, Mayer) ara pertany a macro QUALITAT. C-04b absorbit dins C-04 via intensificació (2026-04-09).

## D. MULTIMODALITAT (Macro: MULTIMODAL)

| ID | Instrucció | Activ. | Perfils | Nivells | Suprimida per | Intensificada per | Marcs |
|---|---|---|---|---|---|---|---|
| D-01 | Emojis/icones al costat de conceptes clau. | COMPLEMENT | — | — | — | — | UNE §Disseny, IFLA N1, CC Pas 5, DUA P1.1, CLT dual coding Paivio |
| D-02 | Esquema de procés en text (fletxes, símbols). | COMPLEMENT | — | — | — | — | CC Pas 5, DUA P1.1, CLT senyalització |
| D-03 | Mapa conceptual jeràrquic en text. | COMPLEMENT | — | — | — | — | DUA P1.1, Organitzadors gràfics Novak |
| D-06 | Text preparat per lectura en veu alta. | PERFIL | di, disc_visual | — | — | — | DUA P1.1 auditiu+visual, CLT dual coding, DSM DI/disc_visual |
| D-06b | Dislèxia: text per veu alta com a canal principal. | PERFIL | dislèxia | — | — | dislèxia.grau ∈ {moderat, sever} | DUA P1.1, NE Wolf 2018, Dehaene 2009 |

## E. CONTINGUT CURRICULAR / QUALITAT (Macro: QUALITAT)

| ID | Instrucció | Activ. | Perfils | Nivells | Suprimida per | Intensificada per | Marcs |
|---|---|---|---|---|---|---|---|
| C-03 | Eliminació redundància decorativa (Mayer coherence). | SEMPRE | — | — | — | — | CC Pas 3, CLT principi coherència Mayer 2009 |
| E-01 | Nucli terminològic intocable: MAI substituir terme curricular. | SEMPRE | — | — | — | — | UNE §Voc terme oficial, Pedagogia rigor curricular |
| E-02 | Definició tècnica graduada per MECR. | **NIVELL GRADUAT** | — | tots | — | — | MECR competència lèxica per nivell, DUA P1.3, ZPD |
| E-05 | Exactitud científica: simplificació ≠ error conceptual. | SEMPRE | — | — | — | — | UNE respectar sentit original, Pedagogia |
| E-06 | Simplifica processos mantenint causalitat. | SEMPRE | — | — | — | — | Pedagogia: cadena causal |
| E-07 | Un exemple concret per concepte abstracte. | **NIVELL GRADUAT** | — | pre-A1→B1 | — | — | MECR A1-A2 concrets, CC Pas 4, DUA P1.3, CLT concreció |
| E-08 | Referents culturalment diversos. Explica referents locals. | PERFIL | nouvingut, vulnerabilitat | — | — | — | DUA P3.1 rellevància cultural |
| E-09 | Evita supòsits culturals implícits. | PERFIL | nouvingut | — | — | — | DUA P3.1, Educació intercultural |
| E-10 | Sensibilitat temes traumàtics. | PERFIL | trastorn_emocional, vulnerabilitat | — | — | sensibilitat_tematica=true | DUA P3 clima segur, DSM trastorn emocional |
| E-11 | Pistes etimològiques translingües (L1 romànica). | PERFIL | nouvingut | — | — | L1 ∈ llengües romàniques | DUA P1.3, Lingüística contrastiva |
| E-12 | Contra-exemples per delimitar conceptes. | NIVELL | — | B1→B2 | — | — | MECR B1+ argumentar, Bloom anàlisi |

## F. AVALUACIÓ I COMPRENSIÓ (Macro: AVALUACIÓ)

| ID | Instrucció | Activ. | Perfils | Nivells | Suprimida per | Intensificada per | Marcs |
|---|---|---|---|---|---|---|---|
| F-06 | Preguntes comprensió intercalades cada 2-3 paràgrafs. | PERFIL | tdah | — | — | — | DUA P2.1, DSM TDAH, Bloom nivell 1-2 |
| F-09 | Preguntes pensament crític: per què? i si...? | PERFIL | altes_capacitats | — | — | — | MECR B2 argumentar, DUA P3.3, Bloom avaluar/crear |
| F-10 | Connexions interdisciplinars. | PERFIL | altes_capacitats | — | — | — | MECR B2, DUA P3, Bloom crear |

## G. PERSONALITZACIÓ LINGÜÍSTICA (Macro: PERSONALITZACIÓ)

| ID | Instrucció | Activ. | Perfils | Nivells | Suprimida per | Intensificada per | Marcs |
|---|---|---|---|---|---|---|---|
| G-01 | Glossari bilingüe complet amb traducció a L1. | PERFIL | nouvingut | — | — | — | UNE §Voc glossari, DUA P1.2, Educació plurilingüe |
| G-02 | Traducció parcial consignes bàsiques a L1. | PERFIL | nouvingut | — | — | mecr ∈ {pre-A1, A1} | DUA P1.2, Acollida lingüística |
| G-03 | Transliteració fonètica obligatòria (alfabet no llatí). | PERFIL | nouvingut | — | — | alfabet_llati=false | DUA P1.2, M1 corpus FJE |
| G-06 | Ajusta to segons MECR (conversacional→acadèmic). | **NIVELL GRADUAT** | — | tots | — | — | MECR descriptors pragmàtics, Sociolingüística registres |
| G-07 | CALP inicial: estructura discursiva molt explícita. | PERFIL | nouvingut | — | — | calp=inicial | DUA P1.3, Cummins 1979 BICS vs CALP |

## H. ADAPTACIONS PER PERFIL (Macros: PERFIL + ENRIQUIMENT)

### TEA (Macro: PERFIL)

| ID | Instrucció | Activ. | Condició subvar | Intensificada per | Marcs |
|---|---|---|---|---|---|
| H-01 | TEA: estructura predictible (títol→def→exemple→activitat). | PERFIL tea | — | — | DSM-5 TEA, DUA P1.3 patrons, TEACCH, M1 corpus |
| H-02 | TEA: zero implicitura. Tot literal. No ironia, sarcasme ni inferències socials. | PERFIL tea | — | — | DSM-5 dèficit pragmàtica |
| H-03 | TEA: anticipació de canvis ('Ara canviem de tema'). | PERFIL tea | — | — | DSM-5, DUA P1.3 predictibilitat |

### TDAH (Macro: PERFIL)

| ID | Instrucció | Activ. | Condició subvar | Intensificada per | Marcs |
|---|---|---|---|---|---|
| H-04 | Micro-blocs 3-5 frases amb objectiu explícit. | PERFIL tdah, trastorn_emocional | — | tdah.grau=sever → "2-3 frases" | DSM-5 TDAH, DUA P3.2, CLT chunking |
| H-05 | Retroalimentació visual de progrés (barres, %). | PERFIL tdah | — | — | DSM-5, DUA P3.2 retroalimentació |
| H-06 | Variació dins text (lectura, esquema, pregunta). | PERFIL tdah | — | — | DSM-5, DUA P3 atenció |

**Nota**: H-04b absorbit dins H-04 via intensificació `_get_intensified_text` (2026-04-09).

### Dislèxia (Macro: PERFIL)

| ID | Instrucció | Activ. | Condició subvar | Intensificada per | Marcs |
|---|---|---|---|---|---|
| H-07 | Evita paraules compostes llargues. Divideix o reformula. | PERFIL dislèxia | — | — | UNE §Voc, NE Wolf 2018, Dehaene 2009 |
| H-08 | Paraules alta freqüència. Repeteix termes, no sinònims. | PERFIL dislèxia | — | — | UNE §Voc, NE decodificació |
| H-22 | Dislèxia fonològica: evita prefixos+sufixos encadenats. | PERFIL dislèxia | tipus_dislexia=fonologica | — | NE Dehaene ruta fonològica |

### Discapacitat intel·lectual (Macro: PERFIL)

| ID | Instrucció | Activ. | Condició subvar | Intensificada per | Marcs |
|---|---|---|---|---|---|
| H-09 | UN sol concepte nou per bloc. No barrejar idees. | PERFIL di | — | — | DUA P1.3, CLT intrínseca, DSM-5 DI |
| H-10 | Concreció radical: cada concepte abstracte amb exemple tangible. | PERFIL di | — | — | DUA P1.3, CLT, DSM-5 |
| H-11 | Repetició sistemàtica en formats diversos (text, esquema, exemple). | PERFIL di | — | — | DUA P1.1 múltiples representacions, DSM-5 |

### Altes capacitats i 2e (Macro: ENRIQUIMENT — ordre 0, primer al prompt)

| ID | Instrucció | Activ. | Condició subvar | Intensificada per | Marcs |
|---|---|---|---|---|---|
| H-12 | Profundització conceptual: excepcions, fronteres, debats oberts. | PERFIL altes_capacitats | — | — | MECR B2+ argumentar, DUA P3.3, Renzulli 1978 enriquiment |
| H-14 | PROHIBIT SIMPLIFICAR. Mantenir/augmentar complexitat. | PERFIL altes_capacitats | — | — | Renzulli, Bloom avaluar/crear |
| H-15 | 2e: equilibri repte ALT + suports accessibilitat. Format sí, contingut no. | PERFIL 2e | — | — | DUA multinivell, Baum 2004 2e |

### TDL (Macro: PERFIL)

| ID | Instrucció | Activ. | Condició subvar | Intensificada per | Marcs |
|---|---|---|---|---|---|
| H-16 | Reducció màxima densitat lèxica. | PERFIL tdl | — | — | CLT, DSM-5 TDL, M1 corpus |
| H-17 | Modelatge ús en context: terme en 2-3 contextos. | PERFIL tdl | — | — | Logopèdia modelatge |
| H-23 | TDL receptiu: simplificació reforçada en TOT el text. | PERFIL tdl | tdl.modalitat=receptiu | — | DSM-5 TDL receptiu |
| H-24 | TDL semàntica: vocabulari mínim funcional. | PERFIL tdl | tdl.semantica=true | — | DSM-5, CLT |
| H-25 | TDL morfosintaxi: SVO estricte, zero passives/subordinades. | PERFIL tdl | tdl.morfosintaxi=true | — | DSM-5 |
| H-26 | TDL pragmàtica: intenció comunicativa explícita. | PERFIL tdl | tdl.pragmatica=true | — | DSM-5 |

### Discapacitat sensorial i motora (Macro: PERFIL)

| ID | Instrucció | Activ. | Condició subvar | Intensificada per | Marcs |
|---|---|---|---|---|---|
| H-19 | Disc. visual: encapçalaments semàntics per lector pantalla. | PERFIL disc_visual | — | — | UNE §Disseny, DUA P1.1, WCAG 2.1 |
| H-20 | Disc. auditiva: simplificació com L2 en sordesa prelocutiva. | PERFIL disc_auditiva | — | comunicacio=LSC → H-20b | DSM-5, Lingüística LSC |
| H-20b | Disc. auditiva LSC: català escrit = L2 estricte. | PERFIL disc_auditiva | comunicacio=LSC | — | DSM-5, DUA P1.2 |
| H-21 | Disc. visual ceguesa: descriu textualment elements visuals. | PERFIL disc_visual | grau=ceguesa | — | UNE §Disseny, DUA P1.1, WCAG 2.1 alt text |

---

## Components del system prompt (no instruccions)

| Element | Estat 2026-04-09 | Origen |
|---|---|---|
| Identitat v2 (TO, Fidelitat, Rigor, Format, Llengua, Seguretat) | ✅ Actiu | corpus_reader.get_identity() |
| Instruccions filtrades (98, agrupades per macrodirectiva, format bullets) | ✅ Actiu — motor principal | instruction_filter → format_instructions_for_prompt() |
| Bloc DUA (Accés/Core/Enriquiment) | ✅ Actiu — únic diferenciador Accés vs Core | corpus_reader.get_dua_block() |
| Gènere discursiu | ✅ Actiu (si indicat) | corpus_reader.get_genre_block() |
| Creuaments (2+ perfils) | ✅ Actiu (si 2+ perfils) | corpus_reader.get_crossing_blocks() |
| Persona-audience | ✅ Actiu — orientació general per l'LLM | build_persona_audience() |
| Complements + format sortida | ✅ Actiu | build_system_prompt() secció output |
| ~~RAG-KG~~ | ❌ Eliminat (2026-04-09) | Indistingible amb/sense, docs irrellevants |
| ~~Context educatiu~~ | ❌ Eliminat del prompt (2026-04-09) | Etapa/curs s'usen al Python per MECR, no al prompt |
| ~~Resolució conflictes~~ | ❌ Eliminat (2026-04-09) | Redundant amb A-26 graduada |
| ~~Few-shot example~~ | ❌ Eliminat (2026-04-09) | Un sol domini (fotosíntesi), parking lot |
| ~~universal_rules~~ | ❌ Eliminat (2026-04-09) | 15 regles duplicaven catàleg |

---

## MECR mappings per perfil (server.py, propose_adaptation)

Sistema de candidats: cada perfil amb barrera lingüística proposa un MECR. El més restrictiu guanya.

| Perfil | Mapping | Font | Barrera |
|--------|---------|------|--------|
| Nouvingut | Docent tria explícitament | MECR-CV | Lingüística (L2) |
| DI | sever→A1, moderat→A2, lleu→B1 | DSM-5, mapa_barreres | Cognitiva→lingüística |
| TDL | sever→A1, moderat→A2, lleu→B1 | Bishop 2017, mapa_barreres | Lingüística directa |
| Disc. auditiva LSC | →A1 fix | mapa_barreres | Català escrit = L2 |
| Vulnerabilitat | -1 nivell vs etapa | mapa_barreres | Retard lector |
| Altes capacitats (sense 2e) | +1 nivell vs etapa | mapa_barreres | Cap (necessita complexitat) |
| TEA | Default etapa | mapa_barreres | No lingüística (coherència central) |
| TDAH | Default etapa | mapa_barreres | No lingüística (atenció) |
| Dislèxia | Default etapa | mapa_barreres | No lingüística (decodificació) |
| Disc. visual | Default etapa | mapa_barreres | No lingüística (accés) |
| TDC | Default etapa | mapa_barreres | No lingüística (motricitat) |
| Trastorn emocional | Default etapa | mapa_barreres | No lingüística (emocional) |

Defaults per etapa: infantil→A1, primària→B1, ESO→B2, batxillerat→B2, FP→B2.

---

## Resum quantitatiu per nivell MECR

| MECR | Instruccions NIVELL | + SEMPRE | Total (sense PERFIL) |
|------|--------------------|---------|--------------------|
| pre-A1 | 25 | +18 | **43** |
| A1 | 25 | +18 | **43** |
| A2 | 25 | +18 | **43** |
| B1 | 17 | +18 | **35** |
| B2 | 1 | +18 | **19** |
| C1 | 0 | +18 | **18** |

**Nota**: SEMPRE ara són 18 (no 20) perquè A-15 ha passat a NIVELL i 2 instruccions s'han suprimit per altes_capacitats a C1.

---

## Cobertura per marc teòric

| Marc | Instruccions que hi mapegen | % del total (98) |
|---|---|---|
| **UNE 153101** (LF) | A-01 a A-11, A-17, A-19, A-21, A-23 a A-26, A-29, B-01, B-04, B-06, B-11, C-05, E-01, E-05, H-07, H-08, H-19, H-21 | **~27 (28%)** |
| **CLT** (Sweller/Mayer) | C-01 a C-08, A-12, A-20, A-27, A-29, B-01, C-03, H-04, H-09, H-16, H-24 | **~18 (18%)** |
| **DUA/CAST** | B-02, B-07, B-13, D-01 a D-06b, E-08, E-09, F-06, F-09, G-01 a G-03, H-01, H-03, H-05, H-06, H-11, H-15, H-19 | **~22 (22%)** |
| **MECR** | A-06 a A-13, A-17, A-20, A-22 a A-26, A-28, B-04 a B-11, B-14, C-01, C-02, C-05, C-06, C-08, E-02, E-07, E-12, G-06 | **~33 (34%)** — eix principal |
| **DSM-5 / clínic** | Totes les H-xx, F-06, D-06b, A-27 | **~30 (31%)** |
| **CC / ISO** | A-01, A-04, A-07, A-14, A-16, A-28 a A-30, B-01 a B-06, B-09, B-14, C-02, C-03, C-05, C-06, E-07 | **~18 (18%)** |
| **NE** (Dehaene/Wolf) | A-16, A-21, D-06b, H-07, H-08, H-22 | **~6 (6%)** |
| **ZPD** (Vygotsky) | A-15, E-02 | **~2 (2%)** |
