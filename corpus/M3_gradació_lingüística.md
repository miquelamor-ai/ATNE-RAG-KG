---
titol: "Gradació Lingüística per Nivell MECR: Generació i Enriquiment de Textos"
modul: M3
tipus: estrategia
paraules_clau: [gradació, MECR, MALL, generació-textos, enriquiment, vocabulari, sintaxi, connectors, HCL]
descripcio: "Característiques lingüístiques operatives de cada nivell MECR (pre-A1 → C1) per a la generació i l'enriquiment de textos educatius. Vocabulari, longitud de frase, estructures sintàctiques, connectors, temps verbals, registre i habilitats cognitivolingüístiques per nivell. Marc rector: MALL (FJE) — paradigma adequació > correcció, gènere discursiu obligatori, bastides en lloc de simplificar."
review_status: esborrany
generat_at: 2026-05-16T00:00:00
---

# Gradació Lingüística per Nivell MECR: Generació i Enriquiment de Textos

---

### 1.1 Propòsit i àmbit

Aquest document descriu **les característiques lingüístiques operatives** de cada nivell MECR
(pre-A1 → C1) perquè els assistents IA puguin:

- **Generar** textos calibrats al nivell lingüístic de l'alumnat
- **Enriquir** un text un graó per sobre del seu nivell actual (sense fer salt de registre)
- **Avaluar** si un text és coherent amb el nivell declarat

A diferència del M3_lectura-facil (centrat en l'**adaptació** d'un text existent), aquest M3
mira en l'altra direcció: com **crear** un text al nivell adequat o com **enriquir-lo**
proporcionalment al seu punt de partida.

### 1.2 Paradigma rector MALL

MALL (FJE) estableix un paradigma de **adequació > correcció**: cap estructura lingüística
no és "prohibida" en absolut, sinó **adequada o inadequada al nivell, al gènere i a la
situació comunicativa**. Aquest document llista per a cada nivell:

- Estructures **adequades** (les esperables al nivell)
- Estructures **inadequades** (les que dificulten la llegibilitat al nivell)
- Bastides recomanades (per pujar el nivell mantenint estructures complexes)

### 1.3 Principis transversals (sempre, no per nivell)

Independentment del nivell, qualsevol text generat ha de respectar:

- **Gènere discursiu obligatori**: tot text es genera dins d'un gènere real (notícia,
  informe, conte, recepta), no com a "tipologia abstracta"
- **Multimodalitat**: text + imatge/gràfic/esquema com a garantia d'accessibilitat
- **TILC** (Tractament Integrat de Llengua i Continguts): patró temàtic + patró lingüístic
  planificats alhora, no separats
- **Bastides en lloc de reduir**: un text de nivell B1 amb bastida pot tenir estructura
  més complexa del que sembla. **Es prefereix mantenir el text i afegir bastida** abans
  que escurçar o trencar contingut
- **Càrrega cognitiva**: la longitud de frase per paraules és un proxy. El criteri real
  és la càrrega cognitiva (densitat informativa, dependències sintàctiques, abstracció)

### 1.4 Habilitats Cognitivolingüístiques (HCL)

MALL identifica **5 HCL oficials** que progressen amb el nivell:

1. **Descriure** — adequada a tots els nivells
2. **Definir** — emergeix a A2
3. **Explicar** — emergeix a A1 (bàsic) i es consolida a A2-B1
4. **Justificar** — emergeix a B1
5. **Argumentar** — emergeix a B1 (bàsic) i es consolida a B2
6. **Demostrar** — esperable a B2-C1 (raonament formal)

A ciències i matemàtiques, **definir** i **interpretar** s'afegeixen com a HCL freqüents.

---

## 3. Connexions amb altres documents del corpus

- **M3_lectura-facil-comunicacio-clara.md**: descriu el comportament lector per nivell
  MALL i les pautes d'adaptació. Aquest document és complementari: cobreix la direcció
  inversa (generar/enriquir)
- **M3_MECR-descriptors-llengua.md**: descriptors oficials del Consell d'Europa per nivell
- **M3_generes-discursius.md**: catàleg de 22 gèneres. Vinculació obligatòria amb la
  gradació (cada gènere té connectors i estructures pròpies)
- **M3_TILC-llengua-i-continguts.md**: principis de TILC, criteri rector per a contingut
  curricular en L2
- **M1_alumnat-nouvingut.md**: el nivell MECR del nouvingut es deriva del CALP, no del
  curs (Cummins, hipòtesi de la interdependència)

---

## 4. Aplicacions

### Generació de textos (ATNE Pas 2, futur assistent de material didàctic)
Quan el sistema coneix el nivell MECR del destinatari (via perfil actiu), injecta el
bloc operatiu del nivell al prompt de generació.

### Enriquiment proporcional (preset "enriquir" del refinador)
Si el MECR és conegut → s'aplica el bloc del nivell N+1.
Si no es coneix → l'LLM fa auto-avaluació interna i eleva un graó.

### Avaluació de coherència de nivell
Un text declarat com a A2 amb subordinades concessives massives no és coherent. El bloc
operatiu permet contrastar.

---

## 5. Fonts

- **MALL (FJE)** — Marc d'Aprenentatge de Llengües, Notebook `c0615b8d-f57d-4444-b360-2cdb3bafc399`
- **Decret 175/2022** (Catalunya) — Currículum educació bàsica
- **MECR / CEFR** — Marc Europeu Comú de Referència per a les Llengües (Consell d'Europa, 2001/2020)
- **Cummins, J. (1984)** — Hipòtesi de la interdependència, CALP/BICS
- **CEFR Companion Volume (2020)** — Descriptors actualitzats incloent mediació

---

## 6. INSTRUCCIONS PER NIVELL MECR — BLOCS PER A L'LLM

Cada generació o enriquiment usa **UN ÚNIC** nivell MECR. El sistema selecciona el bloc
corresponent i l'injecta al prompt.

### pre-A1 · Emergent (Logogràfic, MOPI, lectura compartida)
```
NIVELL MECR DE GENERACIÓ: pre-A1 · Emergent (MALL)
Destinatari real: lectura compartida adult/infant. L'adult llegeix en veu alta i l'infant anticipa el significat per les imatges.
Vocabulari ADEQUAT: concret i visual del món immediat (cos, casa, família, animals, colors, accions bàsiques).
Vocabulari INADEQUAT al nivell: abstraccions, termes acadèmics, conceptes no visualitzables.
Longitud de frase: 3 a 6 paraules. Màxim total del text: 40 paraules.
Sintaxi ADEQUADA: frase simple (Subjecte + Verb + Complement). Ritme oral natural.
Sintaxi INADEQUADA al nivell: subordinació de qualsevol tipus, coordinació adversativa (però), passiva, pronoms febles complexos.
Connectors ADEQUATS: i, llavors.
Temps verbals: present d'indicatiu (formes regulars).
Registre: col·loquial directe, conversacional ("Mira! Les plantes…").
HCL: descriure (pura). Cap altra HCL.
Estructura: repetitiva i rítmica per afavorir l'anticipació (patró: «La Maria té un gat. El gat és taronja. El gat menja.»).
Multimodalitat: cada frase amb suport visual obligatori. Afegeix marcadors [IMATGE: concepte curt] al final de cada frase.
Bastides: nom propi de l'infant com a protagonista (Textos d'Identitat, Cummins), gèneres tipus rondalla quan escaigui.
```

### A1 · Inicial (Funció executiva, descodificació alfabètica)
```
NIVELL MECR DE GENERACIÓ: A1 · Inicial (MALL)
Destinatari real: lector emergent que comença a llegir sol amb suport.
Vocabulari ADEQUAT: freqüent quotidià (les ~500 paraules més freqüents del català) + lèxic d'entorn immediat.
Vocabulari INADEQUAT al nivell: termes acadèmics no definits, abstraccions, sinònims rebuscats.
Longitud de frase: 5 a 10 paraules.
Sintaxi ADEQUADA: frase simple SVO + coordinació senzilla. Inici de coordinació adversativa amb «però».
Sintaxi INADEQUADA al nivell: subordinació, passiva, nominalitzacions, pronoms febles encadenats.
Connectors ADEQUATS: i, però, o, també, llavors, perquè (només causal simple, una vegada per text màxim).
Temps verbals: present d'indicatiu, passat perifràstic (va fer, va anar), futur immediat (anirà, ho farà).
Registre: col·loquial-funcional, directe ("Ara aprendràs a…").
HCL: descriure, explicar (bàsic).
Estructura: lineal senzilla, una idea per frase.
Multimodalitat: marcador [IMATGE:] cada 2-3 frases si el tema ho permet.
Termes tècnics: màxim 3-4 per text, amb definició curta i imatge.
```

### A2 · Funcional (Lectura "de les línies", significat literal)
```
NIVELL MECR DE GENERACIÓ: A2 · Funcional (MALL)
Destinatari real: lector autònom per a textos quotidians i escolars senzills.
Vocabulari ADEQUAT: freqüent + temàtic general del currículum. Termes especialitzats sempre amb definició inline o al glossari.
Vocabulari INADEQUAT al nivell: lèxic abstracte sense referent concret, terminologia disciplinar sense bastida.
Longitud de frase: 8 a 14 paraules.
Sintaxi ADEQUADA: coordinació completa + subordinades causals (perquè, ja que) i temporals (quan, mentre, després que). Màxim 1 subordinada per frase.
Sintaxi INADEQUADA al nivell: subordinació concessiva (tot i que), passiva reflexiva sistemàtica, nominalitzacions.
Connectors ADEQUATS: primer, després, finalment, per exemple, és a dir, a més, també, perquè.
Temps verbals: present, passat (perifràstic + imperfet), futur, condicional simple.
Registre: funcional-social, conversacional acadèmic ("En aquesta secció veurem…").
HCL: descriure, definir, explicar.
Estructura: lineal amb alguna ruptura temàtica (paràgrafs).
Termes tècnics: 5-6 per text, amb definició breu inline.
```

### B1 · Estratègic (Lectura "entre línies", inferències)
```
NIVELL MECR DE GENERACIÓ: B1 · Estratègic (MALL)
Destinatari real: lector estratègic que infereix, estableix relacions causa-efecte, formula hipòtesis.
Vocabulari ADEQUAT: temàtic específic de la disciplina, lèxic acadèmic bàsic. Termes tècnics definits la primera vegada.
Vocabulari INADEQUAT al nivell: lèxic culte, metadiscurs especialitzat, terminologia sense definició.
Longitud de frase: 12 a 20 paraules.
Sintaxi ADEQUADA: subordinades adverbials completes (causal, temporal, condicional, concessiva). Fins a 2 clàusules subordinades per frase. Inici de nominalització («la realització de», «l'aplicació de»).
Sintaxi INADEQUADA al nivell: nominalitzacions complexes encadenades, hipotaxi de 3+ nivells, el·lipsi avançada.
Connectors ADEQUATS: tot i que, en canvi, ja que, per tant, d'una banda / de l'altra, a diferència de, a causa de, per consegüent, és a dir, a més.
Temps verbals: tots els temps d'indicatiu + subjuntiu present.
Registre: formal bàsic, acadèmic inicial.
HCL: descriure, definir, explicar, justificar, argumentar (bàsic).
Estructura: paragrafada per blocs temàtics, amb introducció-desenvolupament-conclusió.
Bastides: explicació del terme tècnic la primera vegada que apareix. Connectors marcats en negreta opcionalment.
```

### B2 · Acadèmic (Funció epistèmica, CALP)
```
NIVELL MECR DE GENERACIÓ: B2 · Acadèmic (MALL)
Destinatari real: lector que llegeix per aprendre (CALP) — domina gèneres disciplinars.
Vocabulari ADEQUAT: acadèmic-disciplinar. Terminologia especialitzada (s'assumeix competència lectora bàsica en la matèria).
Vocabulari INADEQUAT al nivell: argot, col·loquialismes a textos formals (excepte recursos estilístics).
Longitud de frase: variable, fins a 25 paraules.
Sintaxi ADEQUADA: subordinació complexa, passiva reflexiva («es col·loca», «s'observa»), nominalitzacions («la realització de», «l'aplicació del mètode»). Fins a 3 clàusules per frase. Variació deliberada de longitud.
Sintaxi INADEQUADA al nivell: estructures retòriques sofisticades (anacolut, hipèrbaton marcat), incisos múltiples.
Connectors ADEQUATS: en conseqüència, atès que, cal subratllar que, en aquest sentit, d'acord amb, malgrat que, tot i que, tanmateix, amb tot, no obstant.
Temps verbals: tots + subjuntiu passat + perífrasis modals (haver de, poder, deure, caldre).
Registre: formal acadèmic complet.
HCL: tots (descriure, definir, explicar, justificar, argumentar, demostrar, interpretar).
Estructura: argumentativa o expositiva amb tesi, desenvolupament i conclusió. Connectors lògics integrats.
Bastides: ja no es defineix sistemàticament cada terme. Es manté glossari final si cal.
```

### C1 · Crític (Lectura "rere les línies", ideologia i fiabilitat)
```
NIVELL MECR DE GENERACIÓ: C1 · Crític (MALL)
Destinatari real: lector crític que valora intenció autorial, ideologia, fiabilitat. Emet judicis fonamentats.
Vocabulari ADEQUAT: especialitzat, metadiscursiu, registre culte. Variació lèxica deliberada per evitar repeticions. Sinònims, hiperònims, hipònims.
Vocabulari INADEQUAT al nivell: cap restricció pedagògica; només l'adequació al gènere.
Longitud de frase: variable, sense límit fix (5 a 30+ paraules), amb diversitat deliberada per efecte estilístic.
Sintaxi ADEQUADA: hipotaxi complexa, incisos, aposicions, nominalitzacions complexes, passiva, el·lipsi, hipèrbaton controlat. Estructures retòriques (anàfora, paral·lelisme, comparació).
Connectors ADEQUATS: no obstant, nogensmenys, per contra, en darrer terme, en definitiva, dit d'una altra manera, com a corol·lari, en el marc de + tots els anteriors.
Temps verbals: tots + modalitat epistèmica (sembla que, és probable que + subj., cal que + subj., és pertinent que + subj.). Aspecte verbal i valors modals plenament desenvolupats.
Registre: culte, retòric, especialitzat.
HCL: tots, amb argumentació crítica i demostració sofisticada.
Estructura: lliure però coherent al gènere. Ambigüitat i subtilesa permeses (no s'eliminen).
Nota MALL: NO simplificar argumentació ni eliminar ambigüitat intencional — la subtilesa és part del contingut.
```

---

## 7. ENRIQUIMENT GRADUAL — INSTRUCCIONS PER A L'LLM

L'enriquiment **eleva el text un sol graó** respecte al nivell actual, **no fa un salt
de registre**. Manté gènere, to i longitud total.

**Mapping de nivells**:

| Nivell actual | Nivell aplicat en enriquir |
|---|---|
| pre-A1 | A1 |
| A1 | A2 |
| A2 | B1 |
| B1 | B2 |
| B2 | C1 |
| C1 / C2 | C1 (enriquiment d'estil, no de nivell) |

### Enriquir-amb-nivell
```
Enriqueix el text UN GRAÓ respecte al nivell indicat. Aplica EXACTAMENT les característiques del nivell {NIVELL_SUPERIOR}: vocabulari, longitud de frase, connectors ADEQUATS i estructures sintàctiques ADEQUADES d'aquell nivell. NO canviïs el gènere, el to ni la longitud total del text. NO facis un salt de dos nivells. NO incorporis estructures marcades com a INADEQUADES al nivell objectiu.

OBJECTIU: una versió lleugerament més exigent del mateix text, reconeixible com el mateix document. El lector ha de reconèixer-lo com una versió "una mica més rica" del text original, no com un text diferent.

Característiques a aplicar (nivell {NIVELL_SUPERIOR}):
{BLOC_NIVELL_SUPERIOR}
```

### Enriquir-auto-avaluació
```
Enriqueix el text un graó respecte al seu nivell actual.

PAS 1 — Avalua internament el nivell MECR del text original (pre-A1 / A1 / A2 / B1 / B2 / C1) observant:
- Longitud mitjana de frase
- Connectors emprats
- Complexitat sintàctica (presència o absència de subordinació, nominalitzacions, passiva)
- Registre del vocabulari
- Gènere discursiu

PAS 2 — Aplica les característiques del nivell IMMEDIATAMENT SUPERIOR al que has detectat. Ajusta proporcionalment vocabulari, longitud de frase, connectors i estructures sintàctiques.

REGLES:
- NO facis un salt de dos nivells
- NO canviïs el gènere, el to ni la longitud total
- Si el text és ja C1, enriqueix l'estil (variació lèxica, precisió, recursos retòrics) sense canviar el nivell sintàctic
- Respecta SEMPRE el paradigma MALL d'adequació > correcció: cap estructura no és "prohibida", però sí inadequada al nivell objectiu

OBJECTIU: una versió lleugerament més exigent del mateix text, reconeixible com el mateix document.
```
