# Fitxes de gèneres discursius — v1

Document de referència per al corpus FJE. Defineix, per a cada un dels 22 gèneres
discursius reconeguts al sistema ATNE, les regles de composició i adaptació a
Lectura Fàcil (LF) / Comunicació Clara (CC).

**Estat:** v1 — primera versió. Les regles per als 4 macro-gèneres (Explicació,
Narració, Instrucció, Argumentació) es basen en fonts normatives (UNE 153101:2018 EX,
IFLA, Inclusion Europe). Les regles dels sub-gèneres són **inferides** de principis
generals LF + teoria del gènere + estàndards específics quan existeixen. Requereixen
validació empírica amb docents i alumnes.

**Data:** 2026-04-19 · **Autoria:** Miquel Amor (FJE) + assistent ATNE

---

## Visió a llarg termini

Aquest catàleg s'ha dissenyat amb **XML semàntic agnòstic al format de sortida**.
Cada element (`<pas>`, `<vers>`, `<definicio>`...) representa contingut, no
presentació. Això permet que, amb la mateixa font semàntica, es puguin generar
en el futur:

- **Text adaptat** (MVP actual): PDF, DOCX, TXT.
- **Presentacions** (slides): un `<apartat>` → una diapositiva, un `<pas>` → un bullet.
- **Àudio** (TTS amb entonació LF): cada `<torn>` amb la veu corresponent,
  `<estrofa>` amb pausa marcada.
- **Pictogrames seqüencials**: cada `<pas>` → un pictograma AAC/SAAC.
- **Exercicis interactius**: `<pregunta>`/`<resposta>` → formulari; `<definicio>`
  → flashcard.
- **Vídeo** amb subtítols LF: cada `<vers>` com a línia de subtítol.
- **Material imprès** tradicional: fitxes, murals, quaderns.

El mateix principi val per a **altres assistents germans** de l'ecosistema
(Dissenyador d'activitats, Generador de seqüències didàctiques, Productor de
recursos multimodals): podrien consumir aquest catàleg d'elements i compondre
gèneres nous (unitat didàctica, seqüència, projecte) amb les mateixes peces.

---

## Índex

1. [Principis generals](#principis-generals)
2. [Catàleg d'elements atòmics](#cataleg-delements-atomics)
3. [Estructura de cada fitxa](#estructura-de-cada-fitxa)
4. [Tipologia Expositiva](#tipologia-expositiva) — 6 gèneres
5. [Tipologia Narrativa](#tipologia-narrativa) — 7 gèneres
6. [Tipologia Argumentativa](#tipologia-argumentativa) — 4 gèneres
7. [Tipologia Instructiva](#tipologia-instructiva) — 3 gèneres
8. [Tipologia Dialogada](#tipologia-dialogada) — 2 gèneres
9. [Referències](#referencies)

---

## Principis generals

Les regles específiques per gènere **complementen** — no substitueixen — els
principis universals LF del corpus `M3_lectura-facil-comunicacio-clara.md`:

- **Frase curta** (15-20 paraules màx. en general; gradació per MECR).
- **Una idea per paràgraf**, 3-5 frases màx.
- **Veu activa**, subjecte explícit.
- **Vocabulari freqüent**; termes tècnics definits a la primera aparició.
- **Sense** punt i coma, parèntesis, cometes no explicades, punts suspensius,
  "etcètera", abreviatures sense explicar.
- **Sense** temps compostos, condicionals, subjuntiu, passiva, gerundi.
- **Tipografia:** sans-serif 14pt mín., interlineat 1.5-2, alineació esquerra.
- **Imatges** informatives, no decoratives.

**Jerarquia de conflictes** (M3_lectura-facil-comunicacio-clara.md):
`MECR > DUA > LF específica`. El nivell lingüístic és sempre el límit dur.

---

## Catàleg d'elements atòmics

25 elements semàntics que componen qualsevol gènere. XML-ready.

### Estructurals

| Element | XML | Funció | Regla LF |
|---------|-----|--------|----------|
| Títol del text | `<titol>` | Obertura (1 per text) | Concret, sense metàfores |
| Apartat | `<apartat>` | Secció dins del text | Una frase anticipa contingut |
| Subapartat | `<subapartat>` | Només dins complements | Evitar al text principal |
| Paràgraf | `<p>` | Bloc de prosa | 1 idea, 3-5 frases |
| Frase destacada | `<destacat>` | Tesi, moral, conclusió | Una sola frase prominent |

### Llistes

| Element | XML | Funció | Regla LF |
|---------|-----|--------|----------|
| Llista | `<llista tipus="bullet\|numerada">` | Grup d'ítems | Usar per a 3+ elements |
| Ítem | `<item>` | Element de llista | Una idea per ítem |
| Pas | `<pas n="1">` | Acció seqüencial | 1 verb d'acció + objecte concret |

### Diàleg

| Element | XML | Funció | Regla LF |
|---------|-----|--------|----------|
| Torn de diàleg | `<torn parlant="X">` | Intervenció | Atribuir parlant sempre |
| Pregunta | `<pregunta>` | Q en entrevista/guia | Directa, sense subordinades |
| Resposta | `<resposta>` | R en entrevista | Simplificar preservant veu |
| Acotació | `<acotacio>` | Didascàlia teatral | Present, 3a persona |

### Poesia

| Element | XML | Funció | Regla LF |
|---------|-----|--------|----------|
| Estrofa | `<estrofa>` | Grup de versos | Preservar separació |
| Vers | `<vers>` | Línia de poesia | No aplanar en prosa |

### Lèxic

| Element | XML | Funció | Regla LF |
|---------|-----|--------|----------|
| Definició | `<definicio terme="X">` | Entrada terme+def | Evitar circularitat |
| Citació | `<cita font="X">` | Cita directa | Curta, amb atribució |

### Temporals i referencials

| Element | XML | Funció | Regla LF |
|---------|-----|--------|----------|
| Data | `<data>` | Marcador temporal | Format complet, no xifres romanes |
| Referència | `<referent>` | Font bibliogràfica | Autor + any mínim |

### Visuals

| Element | XML | Funció | Regla LF |
|---------|-----|--------|----------|
| Imatge | `<imatge>` amb `<peu>` | Suport visual | Informativa, no decorativa |
| Taula | `<taula>` | Dades estructurades | Màx 3 columnes, sense cel·les fusionades |
| Caixa destacada | `<caixa>` | Info complementària | Separada del flux principal |
| Text paral·lel | `<paral·lel>` amb `<col>` × 2 | Comparació línia a línia | Màx 2 columnes |

### Epistolars

| Element | XML | Funció | Regla LF |
|---------|-----|--------|----------|
| Capçalera | `<capcalera>` | Destinatari + data | Format estàndard |
| Salutació | `<salutacio>` | Fórmula inicial | Ajustada al registre |
| Comiat | `<comiat>` | Fórmula final | Breu |
| Signatura | `<signatura>` | Remitent | Nom complet |

---

## Estructura de cada fitxa

Cada gènere segueix un format de 7 seccions:

1. **Propòsit pedagògic** — Què desenvolupa (competència).
2. **Etapa i context curricular** — Etapes educatives, connexió curricular si és clara.
3. **Composició estructural** — Taula d'elements (ordre, XML, obligatori/opcional, notes).
4. **Gradació MECR** — Què canvia de la composició segons el nivell de sortida.
5. **Regles crítiques LF** — 3-5 normes específiques del gènere.
6. **Contraindicacions** — 3-5 coses que el gènere NO ha de tenir.
7. **Exemple XML** — Mostra canònica adaptada.

---

# Tipologia Expositiva

Funció: **fer entendre** un fenomen, procés o concepte.
Estructura canònica: Què és → Com funciona → Per què importa.

## 1. Manual / capítol escolar

### Propòsit pedagògic
Construir coneixement disciplinari de manera progressiva. Desenvolupa la
**competència comprensió lectora acadèmica** i la **capacitat d'estudi autònom**.

### Etapa i context curricular
Totes les etapes (primària → FP). Present a totes les matèries. Font principal
d'estudi a l'ESO i batxillerat.

### Composició estructural

| Ordre | Element | Obligatori? | Notes |
|-------|---------|-------------|-------|
| 1 | `<titol>` | ✅ | Tema del capítol |
| 2 | `<entradeta>` | ⬜ | Avança el contingut (1-2 frases) |
| 3 | `<apartat>` + `<p>` | ✅ | N seccions del capítol |
| 4 | `<definicio>` | ⬜ | Termes clau integrats |
| 5 | `<imatge>` amb `<peu>` | ⬜ | Suport visual informatiu |
| 6 | `<taula>` o `<llista>` | ⬜ | Dades sistematitzades |
| 7 | `<caixa>` | ⬜ | Saber curiós, recordatori |
| 8 | `<destacat>` | ⬜ | Idea clau per recordar |

### Gradació MECR

| Nivell | Canvis |
|--------|--------|
| A1 | Màx 3 apartats. Definicions obligatòries amb exemples. Imatge per cada apartat. |
| A2 | Màx 4-5 apartats. Definicions al primer ús. Taules amb màx 2 columnes. |
| B1 | Apartats lliures. Definicions opcionals. |
| B2 | Densitat conceptual estàndard. |

### Regles crítiques LF
- **Progressió simple → complex**: cada apartat es recolza en l'anterior.
- **Desnominalitzar processos**: "l'oxidació" → "quan s'oxida".
- **Connectors causals explícits**: "perquè", "per tant", "així doncs".
- **Exemples concrets** abans de l'abstracció.
- **Termes tècnics** sempre definits a la primera aparició, en negreta.

### Contraindicacions
- NO apartats niats de més d'un nivell (no subapartats).
- NO notes al peu (distreuen el flux).
- NO referències a capítols posteriors ("ho veurem més endavant").
- NO apel·lacions al lector adult ("pensaràs que...").

### Exemple XML

```xml
<manual>
  <titol>La fotosíntesi</titol>
  <entradeta>Les plantes fan el seu propi aliment amb la llum del sol.</entradeta>

  <apartat>Què és la fotosíntesi</apartat>
  <p>La fotosíntesi és el procés que fan les plantes per produir aliment.
  Fan servir la <destacat>llum del sol</destacat>.</p>

  <apartat>Com funciona</apartat>
  <p>La planta necessita tres coses:</p>
  <llista tipus="bullet">
    <item>Aigua de la terra.</item>
    <item>Diòxid de carboni de l'aire.</item>
    <item>Llum del sol.</item>
  </llista>
</manual>
```

---

## 2. Article divulgatiu

### Propòsit pedagògic
Apropar coneixement científic o cultural a un públic no especialitzat.
Desenvolupa **alfabetització científica** i **curiositat intel·lectual**.

### Etapa i context curricular
ESO i batxillerat principalment. Ciències, socials, humanitats.

### Composició estructural

| Ordre | Element | Obligatori? | Notes |
|-------|---------|-------------|-------|
| 1 | `<titol>` | ✅ | Suggeridor però clar |
| 2 | `<entradeta>` | ✅ | Gancho + idea principal |
| 3 | `<p>` | ✅ | Desenvolupament narrativitzat |
| 4 | `<cita>` | ⬜ | Veu d'expert |
| 5 | `<imatge>` amb `<peu>` | ⬜ | Dades visualitzades |
| 6 | `<caixa>` | ⬜ | "Saps que..." |

### Gradació MECR

| Nivell | Canvis |
|--------|--------|
| A1-A2 | Entradeta molt simple. Una idea per paràgraf. Sense cites. |
| B1 | Cites curtes admeses. Estructura narrativa simple. |
| B2 | Complexitat estàndard. |

### Regles crítiques LF
- **Entradeta captadora** però sense metàfores obscures.
- **Narrativitzar** el contingut científic (explicar com una història).
- **Cites breus** amb atribució clara ("diu X, expert en Y").
- **Evitar xifres llargues**: arrodonir ("més de 2 milions" en lloc de "2.347.812").

### Contraindicacions
- NO tecnicismes sense explicar.
- NO referències culturals implícites (cultura general no universal).
- NO humor irònic (pot confondre).
- NO frases incompletes o suspensives.

### Exemple XML

```xml
<article_divulgatiu>
  <titol>Els elefants parlen amb els peus</titol>
  <entradeta>Els elefants envien missatges a quilòmetres de distància.
  Ho fan amb vibracions que surten de les seves potes.</entradeta>

  <p>Els científics han descobert una cosa increïble. Els elefants poden
  sentir altres elefants des de molt lluny. No els senten amb les orelles.
  Els senten amb els peus.</p>

  <cita font="Caitlin O'Connell, bióloga de Stanford">
    Els elefants usen el terra com un telèfon.
  </cita>
</article_divulgatiu>
```

---

## 3. Informe / memòria

### Propòsit pedagògic
Comunicar resultats, observacions o conclusions d'una activitat o investigació.
Desenvolupa **rigor metodològic** i **organització del pensament**.

### Etapa i context curricular
ESO (informes de pràctiques, treballs de recerca) i batxillerat (treball de
recerca). FP (memòries tècniques).

### Composició estructural

| Ordre | Element | Obligatori? | Notes |
|-------|---------|-------------|-------|
| 1 | `<titol>` | ✅ | Tema + tipus d'informe |
| 2 | `<entradeta>` | ✅ | Resum executiu (3-5 línies) |
| 3 | `<apartat>` "Objectiu" + `<p>` | ✅ | Què es buscava |
| 4 | `<apartat>` "Mètode" + `<p>` o `<llista>` | ✅ | Com s'ha fet |
| 5 | `<apartat>` "Resultats" + `<p>` + `<taula>` | ✅ | Què s'ha trobat |
| 6 | `<apartat>` "Conclusions" + `<destacat>` | ✅ | Què significa |
| 7 | `<referent>` | ⬜ | Fonts consultades |

### Gradació MECR

| Nivell | Canvis |
|--------|--------|
| A1-A2 | Només 3 apartats: Què volíem / Què hem fet / Què hem trobat. |
| B1 | 4 apartats. Taules simples. |
| B2 | Estructura completa amb referents. |

### Regles crítiques LF
- **Resum executiu** al principi (què s'ha fet i què s'ha trobat).
- **Dades presentades visualment** (taules, gràfics) abans de la prosa.
- **Conclusió destacada** com a frase final prominent.
- **Verbs en passat** per a accions fetes; present per a conclusions.

### Contraindicacions
- NO opinions personals barrejades amb fets.
- NO conclusions que no derivin dels resultats.
- NO tecnicismes sense glossari.
- NO referències a lectura futura.

### Exemple XML

```xml
<informe>
  <titol>Informe de l'experiment del pèndol</titol>
  <entradeta>Hem mesurat el temps d'oscil·lació d'un pèndol amb diferents
  longituds. Hem trobat que com més llarg és, més triga a oscil·lar.</entradeta>

  <apartat>Què volíem trobar</apartat>
  <p>Volíem saber si la longitud del pèndol canvia el temps d'oscil·lació.</p>

  <apartat>Com ho hem fet</apartat>
  <llista tipus="numerada">
    <item>Vam preparar 3 pèndols de 20 cm, 40 cm i 60 cm.</item>
    <item>Vam mesurar 10 oscil·lacions amb un cronòmetre.</item>
    <item>Vam repetir l'experiment 3 vegades.</item>
  </llista>

  <apartat>Conclusions</apartat>
  <destacat>Com més llarg és el pèndol, més temps triga a oscil·lar.</destacat>
</informe>
```

---

## 4. Definició enciclopèdica

### Propòsit pedagògic
Fixar un concepte amb precisió referencial. Desenvolupa **vocabulari
disciplinari** i **accés a coneixement sistematitzat**.

### Etapa i context curricular
ESO i batxillerat. Totes les matèries (glossaris, entrades enciclopèdiques).

### Composició estructural

| Ordre | Element | Obligatori? | Notes |
|-------|---------|-------------|-------|
| 1 | `<titol>` | ✅ | Terme definit |
| 2 | `<definicio>` | ✅ | Definició nuclear (1 frase) |
| 3 | `<p>` | ⬜ | Explicació ampliada |
| 4 | `<imatge>` amb `<peu>` | ⬜ | Exemple visual |
| 5 | `<llista>` | ⬜ | Exemples o variants |
| 6 | `<referent>` | ⬜ | Font de la definició |

### Gradació MECR

| Nivell | Canvis |
|--------|--------|
| A1-A2 | Només definició + 1 exemple visual. Vocabulari concret. |
| B1 | Definició + explicació + exemples. |
| B2 | Definició + variants + context disciplinari. |

### Regles crítiques LF
- **Definició nuclear** en una sola frase, sense subordinades.
- **Evitar circularitat**: no definir X usant X o paraules de la mateixa arrel.
- **Exemple concret** immediatament després de la definició.
- **Categoria primer, especificitat després**: "La balena és un mamífer gran
  que viu al mar" (categoria: mamífer; especificitat: gran, marí).

### Contraindicacions
- NO definicions per negació ("no és X") com a primera línia.
- NO sinònims com a definició ("llibre: obra literària").
- NO etimologia abans del significat.
- NO referències a entrades anteriors/posteriors.

### Exemple XML

```xml
<enciclopedia>
  <titol>Fotosíntesi</titol>
  <definicio terme="fotosíntesi">
    La fotosíntesi és el procés pel qual les plantes fan menjar
    amb la llum del sol.
  </definicio>
  <p>Les plantes agafen aigua, aire i llum. Amb aquestes tres coses fan
  sucre. El sucre és el seu aliment.</p>
  <imatge>
    <peu>Una planta amb fulles verdes rep la llum del sol.</peu>
  </imatge>
</enciclopedia>
```

---

## 5. Descripció

### Propòsit pedagògic
Representar amb paraules un objecte, persona, lloc o procés. Desenvolupa
**observació sistemàtica** i **vocabulari precís**.

### Etapa i context curricular
Totes les etapes. Especialment primària (descripció de persones, llocs) i
ciències (descripció de processos, espècies).

### Composició estructural

| Ordre | Element | Obligatori? | Notes |
|-------|---------|-------------|-------|
| 1 | `<titol>` | ✅ | Què/qui es descriu |
| 2 | `<p>` | ✅ | Descripció general (1-2 frases) |
| 3 | `<apartat>` + `<p>` | ⬜ | Aspectes (aparença, funció, etc.) |
| 4 | `<llista>` | ⬜ | Característiques |
| 5 | `<imatge>` amb `<peu>` | ⬜ | Suport visual |

### Gradació MECR

| Nivell | Canvis |
|--------|--------|
| A1-A2 | 3-5 característiques en llista. Molt visual. |
| B1 | Descripció en prosa, aspectes agrupats. |
| B2 | Descripció integrada amb matís. |

### Regles crítiques LF
- **Ordre espacial explícit**: de dalt a baix, de l'exterior a l'interior, etc.
- **Comparacions concretes** per a mides ("com una pilota de futbol").
- **Evitar superlatius sintètics**: "molt gran" > "grandíssim".
- **Una característica per frase** en nivells baixos.

### Contraindicacions
- NO adjectius subjectius sense concretar ("molt bonic", "impressionant").
- NO descripcions poètiques amb metàfores.
- NO ordre aleatori de característiques.
- NO barreja de descripció física i emocional.

### Exemple XML

```xml
<descripcio>
  <titol>L'elefant africà</titol>
  <p>L'elefant africà és l'animal terrestre més gran del món.</p>

  <apartat>Com és</apartat>
  <llista tipus="bullet">
    <item>Té la pell grisa i rugosa.</item>
    <item>Pot mesurar 4 metres d'alçada.</item>
    <item>Pesa fins a 6.000 quilos.</item>
    <item>Té dues orelles molt grans, com ventalls.</item>
    <item>Té una trompa llarga que fa servir de mà.</item>
  </llista>
</descripcio>
```

---

## 6. Resum / síntesi

### Propòsit pedagògic
Extreure l'essencial d'un text (resum) o combinar múltiples fonts (síntesi).
Desenvolupa **comprensió profunda** i **jerarquització d'idees**.

### Etapa i context curricular
Primària cicle superior, ESO, batxillerat. Totes les matèries. Competència
transversal d'estudi.

### Composició estructural

| Ordre | Element | Obligatori? | Notes |
|-------|---------|-------------|-------|
| 1 | `<titol>` | ✅ | Títol del text resumit |
| 2 | `<referent>` | ✅ | Font original |
| 3 | `<p>` | ✅ | Idea principal |
| 4 | `<p>` | ⬜ | Idees secundàries (1-3 paràgrafs) |
| 5 | `<destacat>` | ⬜ | Conclusió o tesi |

### Gradació MECR

| Nivell | Canvis |
|--------|--------|
| A1-A2 | Només idea principal + 1 idea secundària. Màx 50 paraules. |
| B1 | 1 idea principal + 2-3 secundàries. Màx 100 paraules. |
| B2 | Síntesi completa amb connectors. Màx 150 paraules. |

### Regles crítiques LF
- **Idea principal al primer paràgraf**, sense preàmbul.
- **Conservar la veu del text original** (no interpretar).
- **Connectors d'ordre lògic** entre idees ("primer... després... finalment").
- **No citar** literalment — reformular amb vocabulari accessible.

### Contraindicacions
- NO opinions del redactor.
- NO cites textuals llargues.
- NO repeticions del contingut original.
- NO exemples no presents a l'original.

### Exemple XML

```xml
<resum>
  <titol>Resum: "Les abelles i la pol·linització"</titol>
  <referent>Text de J. Martí, revista Ciència Avui, 2024.</referent>

  <p>Les abelles són molt importants per la natura. Porten el pol·len
  de flor a flor. Sense abelles, moltes plantes no podrien tenir fruits.</p>

  <destacat>Si les abelles desapareixen, la natura se'n ressent molt.</destacat>
</resum>
```

---

# Tipologia Narrativa

Funció: **explicar fets o històries** amb personatges, acció i final.
Estructura canònica: Qui → Què passa → Per què → Com acaba.

## 7. Conte / relat

### Propòsit pedagògic
Construir sentit a partir d'una seqüència d'esdeveniments. Desenvolupa
**comprensió narrativa**, **empatia** i **imaginació controlada**.

### Etapa i context curricular
Totes les etapes, especialment infantil i primària. Llengua, literatura,
educació en valors.

### Composició estructural

| Ordre | Element | Obligatori? | Notes |
|-------|---------|-------------|-------|
| 1 | `<titol>` | ✅ | Evocador però clar |
| 2 | `<p>` | ✅ | Situació inicial (personatges + lloc) |
| 3 | `<p>` | ✅ | Nus (problema, conflicte) |
| 4 | `<torn parlant="X">` | ⬜ | Diàleg si hi ha |
| 5 | `<p>` | ✅ | Resolució |
| 6 | `<imatge>` amb `<peu>` | ⬜ | Clau visual per moment |

### Gradació MECR

| Nivell | Canvis |
|--------|--------|
| A1-A2 | Màx 2 personatges. 3 escenes. Una imatge per escena. |
| B1 | 3-4 personatges. Diàleg curt admès. |
| B2 | Complexitat narrativa estàndard. |

### Regles crítiques LF
- **Cronologia lineal**: no flashbacks, no salts temporals.
- **Motivacions explícites**: "Lluc tenia por perquè estava sol" (no inferibles).
- **Emocions nomenades**: "estava trist", "es va enfadar".
- **Personatges principals persistents**: usar els mateixos noms, no pronoms.
- **Diàleg atribuït sempre**: "va dir la Marta", "va preguntar en Pau".

### Contraindicacions
- NO narrador no fiable o ambigu.
- NO temps narratius barrejats (passat amb present històric).
- NO referències culturals implícites.
- NO finals oberts o ambigus.
- NO ironia o sarcasme.

### Exemple XML

```xml
<conte>
  <titol>La tortuga i la llebre</titol>

  <p>En un bosc, hi vivien una tortuga i una llebre. La llebre corria
  molt de pressa. La tortuga caminava molt a poc a poc.</p>

  <p>Un dia, la llebre va riure de la tortuga. La tortuga es va enfadar
  i va proposar una cursa.</p>

  <torn parlant="tortuga">Correm fins a l'arbre gran!</torn>
  <torn parlant="llebre">D'acord. Guanyaré segur.</torn>

  <p>La llebre va córrer molt, però es va aturar a descansar. Es va
  adormir. La tortuga va caminar sense parar. Va arribar primera a
  l'arbre gran.</p>
</conte>
```

---

## 8. Fàbula / llegenda

### Propòsit pedagògic
Transmetre una ensenyança moral (fàbula) o cultural (llegenda). Desenvolupa
**pensament ètic** i **identitat cultural**.

### Etapa i context curricular
Primària i ESO. Llengua, literatura, socials, educació en valors.

### Composició estructural

| Ordre | Element | Obligatori? | Notes |
|-------|---------|-------------|-------|
| 1 | `<titol>` | ✅ | Nom (sovint amb protagonistes) |
| 2 | `<p>` | ✅ | Situació inicial |
| 3 | `<p>` | ✅ | Acció/conflicte |
| 4 | `<torn parlant="X">` | ⬜ | Diàleg arquetípic |
| 5 | `<p>` | ✅ | Desenllaç |
| 6 | `<destacat>` | ✅ | Moral (fàbula) o lliçó cultural (llegenda) |

### Gradació MECR

| Nivell | Canvis |
|--------|--------|
| A1-A2 | 2 personatges. Moral en una frase molt simple. |
| B1 | 3 personatges. Moral concisa. |
| B2 | Complexitat estàndard. |

### Regles crítiques LF
- **Moral explícita al final**, no subentesa.
- **Personatges arquetípics amb trets únics** (la llebre ràpida, la tortuga
  lenta) — sense matisos psicològics.
- **Caràcters mantinguts**: si un personatge és llest al principi, ho és fins al final.
- **Llegendes**: situar en temps i lloc reals tot i ser ficció.

### Contraindicacions
- NO morals ambigües o debatables.
- NO evolució psicològica dels personatges.
- NO referències històriques no explicades (llegendes).
- NO llenguatge arcaic.

### Exemple XML

```xml
<fabula>
  <titol>El corb i la guineu</titol>
  <p>Un corb va trobar un tros de formatge. Es va posar dalt d'un arbre
  per menjar-lo tranquil.</p>

  <p>Una guineu passava per allà. Va veure el formatge i el va voler.</p>

  <torn parlant="guineu">Quina veu tan bonica deus tenir, corb. Canta una cançó!</torn>

  <p>El corb, content, va obrir el bec per cantar. El formatge va caure a
  terra. La guineu el va agafar i va marxar corrent.</p>

  <destacat>Moral: no et creguis els afalacs dels qui volen alguna cosa de tu.</destacat>
</fabula>
```

---

## 9. Poema / vers

### Propòsit pedagògic
Experimentar el llenguatge com a art. Desenvolupa **sensibilitat estètica**,
**ritme** i **ús expressiu de la paraula**.

### Etapa i context curricular
Totes les etapes. Llengua, literatura, educació artística.

### Composició estructural

| Ordre | Element | Obligatori? | Notes |
|-------|---------|-------------|-------|
| 1 | `<titol>` | ✅ | Concret o evocador |
| 2 | `<referent>` | ⬜ | Autor i data si es coneix |
| 3 | `<estrofa>` amb `<vers>` | ✅ | Estructura estròfica preservada |
| 4 | `<imatge>` amb `<peu>` | ⬜ | Només si és funcional |

### Gradació MECR

| Nivell | Canvis |
|--------|--------|
| A1-A2 | Versos curts (3-5 paraules). Rima simple. Sense metàfores. |
| B1 | Versos estàndard. Metàfores concretes admeses. |
| B2 | Poesia en la seva forma original si és accessible. |

### Regles crítiques LF
- **Preservar estructura estròfica**: no fusionar estrofes ni aplanar versos.
- **No reescriure en prosa**: seria un altre gènere.
- **Simplificar vocabulari mantenint el ritme** quan sigui possible.
- **Metàfores concretes**: "el sol és una taronja" > "l'astre flamíger".
- **Rima:** conservar-la si es pot; si no, prioritzar la claredat.

### Contraindicacions
- NO convertir en narrativa.
- NO eliminar la divisió en estrofes.
- NO explicar la metàfora dins del poema (trencaria la forma).
- NO afegir comentaris o notes entre versos.

### Exemple XML

```xml
<poema>
  <titol>La lluna</titol>
  <referent>Anònim, tradicional.</referent>

  <estrofa>
    <vers>La lluna, la pruna,</vers>
    <vers>vestida de dol,</vers>
    <vers>son pare la crida,</vers>
    <vers>sa mare no ho vol.</vers>
  </estrofa>
</poema>
```

**Nota específica poema LF:** No hi ha estàndard publicat. La recomanació és
conservar la forma i només simplificar el lèxic quan sigui imprescindible per
comprensió. Si el poema és massa complex, oferir-ne una versió narrativa
**al costat** (no substituint), amb l'original sempre visible.

---

## 10. Biografia

### Propòsit pedagògic
Conèixer una persona a través dels seus fets vitals. Desenvolupa **pensament
històric** i **comprensió de causalitat biogràfica**.

### Etapa i context curricular
Primària cicle superior i ESO. Socials, història, llengua, educació física
(esportistes), arts (artistes).

### Composició estructural

| Ordre | Element | Obligatori? | Notes |
|-------|---------|-------------|-------|
| 1 | `<titol>` | ✅ | Nom de la persona |
| 2 | `<entradeta>` | ✅ | Qui va ser i per què és important |
| 3 | `<data>` + `<p>` | ✅ | Naixement + infància |
| 4 | `<data>` + `<p>` | ✅ | Fets principals (ordre cronològic) |
| 5 | `<data>` + `<p>` | ⬜ | Mort (si escau) |
| 6 | `<destacat>` | ⬜ | Llegat principal |
| 7 | `<imatge>` amb `<peu>` | ⬜ | Fotografia |

### Gradació MECR

| Nivell | Canvis |
|--------|--------|
| A1-A2 | 3-4 fets principals. Dates completes. Imatge obligatòria. |
| B1 | 5-6 fets. Context històric breu. |
| B2 | Biografia completa amb matís. |

### Regles crítiques LF
- **Ordre cronològic estricte**: naixement → infància → fets → mort/llegat.
- **3-5 fets principals** màxim; no llista exhaustiva.
- **Dates completes**: "el 15 de març de 1879", no "1879" ni "s. XIX".
- **Contextualitzar** el lloc i l'època breument ("a Alemanya, fa 150 anys").
- **Separar fets de llegat**: primer què va fer, després per què importa.

### Contraindicacions
- NO flashbacks ("però tornem als seus inicis...").
- NO especulació ("potser pensava que...").
- NO detalls íntims sense rellevància.
- NO xifres romanes per a segles.

### Exemple XML

```xml
<biografia>
  <titol>Albert Einstein</titol>
  <entradeta>Albert Einstein va ser un científic molt famós.
  Va canviar la manera com entenem l'univers.</entradeta>

  <data>14 de març de 1879</data>
  <p>Va néixer a Ulm, una ciutat d'Alemanya. De petit, li agradaven les
  matemàtiques i la música.</p>

  <data>1905</data>
  <p>Va publicar la teoria de la relativitat. Aquesta teoria explica com
  funciona el temps i l'espai.</p>

  <data>1921</data>
  <p>Va guanyar el premi Nobel de Física.</p>

  <data>18 d'abril de 1955</data>
  <p>Va morir als Estats Units.</p>

  <destacat>Einstein és una de les ments més brillants de la història.</destacat>
</biografia>
```

---

## 11. Notícia de premsa

### Propòsit pedagògic
Informar d'un fet rellevant i recent. Desenvolupa **alfabetització mediàtica**
i **comprensió de l'actualitat**.

### Etapa i context curricular
ESO i batxillerat. Llengua, socials, projecte de centre.

### Composició estructural

| Ordre | Element | Obligatori? | Notes |
|-------|---------|-------------|-------|
| 1 | `<titol>` | ✅ | Titular: fet principal |
| 2 | `<entradeta>` | ✅ | Lead: 5W (qui, què, quan, on, per què) |
| 3 | `<p>` | ✅ | Cos: desenvolupament en piràmide invertida |
| 4 | `<cita>` | ⬜ | Veu de protagonista/expert |
| 5 | `<imatge>` amb `<peu>` | ⬜ | Il·lustració del fet |
| 6 | `<data>` | ✅ | Data de publicació |

### Gradació MECR

| Nivell | Canvis |
|--------|--------|
| A1-A2 | Titular + 5W + 1 paràgraf. Màx 80 paraules. |
| B1 | Titular + lead + 2-3 paràgrafs. Cita curta admesa. |
| B2 | Notícia completa. |

### Regles crítiques LF (Reuters Institute, 2024)
- **Piràmide invertida**: el més important al principi.
- **5W al lead**: qui, què, quan, on, per què — tots explicitats.
- **Context explicat**, no assumit (els lectors LF no sempre segueixen l'actualitat).
- **Cites curtes amb atribució clara**.
- **Vocabulari no periodístic**: "va morir" > "va perdre la vida", "es va reunir"
  > "va mantenir una trobada".

### Contraindicacions
- NO titulars metafòrics o amb jocs de paraules.
- NO acrònims sense explicar (UE → Unió Europea).
- NO referències a notícies anteriors sense context.
- NO adjectius valoratius ("escandalós", "vergonyós").

### Exemple XML

```xml
<noticia>
  <data>18 d'abril de 2026</data>
  <titol>Un tren d'alta velocitat connectarà Barcelona i Girona en 30 minuts</titol>
  <entradeta>Avui ha començat el servei del nou tren d'alta velocitat.
  Permet anar de Barcelona a Girona en mitja hora.</entradeta>

  <p>El nou tren funciona des de les 6 del matí. El viatge dura 30 minuts.
  Abans, el trajecte durava una hora i mitja. El preu del bitllet és de 15 euros.</p>

  <cita font="Maria López, directora de Renfe Catalunya">
    Aquesta línia millorarà la vida de milers de persones.
  </cita>
</noticia>
```

---

## 12. Crònica

### Propòsit pedagògic
Relatar un esdeveniment viscut amb perspectiva personal i temporal.
Desenvolupa **observació** i **narració testimonial**.

### Etapa i context curricular
ESO i batxillerat. Llengua, socials, viatges d'estudi, esports.

### Composició estructural

| Ordre | Element | Obligatori? | Notes |
|-------|---------|-------------|-------|
| 1 | `<titol>` | ✅ | Esdeveniment + lloc/data |
| 2 | `<entradeta>` | ⬜ | Context del cronista |
| 3 | `<data>` + `<p>` | ✅ | Moments en ordre cronològic |
| 4 | `<cita>` | ⬜ | Testimoni |
| 5 | `<imatge>` amb `<peu>` | ⬜ | Documentació visual |
| 6 | `<destacat>` | ⬜ | Impressió final |

### Gradació MECR

| Nivell | Canvis |
|--------|--------|
| A1-A2 | 3-4 moments. Cronologia simple. |
| B1 | Més detall, perspectiva personal admesa. |
| B2 | Crònica completa. |

### Regles crítiques LF
- **Cronologia explícita** amb marcadors ("A les 9 del matí...").
- **Perspectiva del cronista sempre visible**: "vaig veure", "vam anar".
- **Descripcions sensorials concretes** (què es veu, què se sent).
- **Separar fet de valoració**: primer què va passar, després què va semblar.

### Contraindicacions
- NO salts temporals (no flashback, no flash-forward).
- NO opinions barrejades amb els fets.
- NO especulació sobre el que altres pensaven.
- NO jocs estilístics (metàfora estesa, ironia).

### Exemple XML

```xml
<cronica>
  <titol>La nostra visita al Museu de la Ciència (Barcelona, 15 d'abril)</titol>

  <data>9:00 del matí</data>
  <p>Vam arribar al museu amb autobús. Feia sol i no hi havia gaire gent.</p>

  <data>10:30</data>
  <p>Vam fer un taller de robots. Vam construir un petit robot que es movia sol.</p>

  <data>13:00</data>
  <p>Vam dinar a la cafeteria del museu. El menjar estava bo.</p>

  <destacat>Va ser un dia molt divertit. Volem tornar-hi.</destacat>
</cronica>
```

---

## 13. Diari / blog

### Propòsit pedagògic
Registrar i reflexionar sobre la pròpia experiència. Desenvolupa
**metacognició**, **consciència emocional** i **escriptura reflexiva**.

### Etapa i context curricular
Totes les etapes. Llengua, tutoria, projectes personals.

### Composició estructural

| Ordre | Element | Obligatori? | Notes |
|-------|---------|-------------|-------|
| 1 | `<data>` | ✅ | Data d'entrada |
| 2 | `<titol>` | ⬜ | Títol de l'entrada (opcional) |
| 3 | `<p>` | ✅ | Què ha passat |
| 4 | `<p>` | ⬜ | Com m'he sentit |
| 5 | `<p>` | ⬜ | Què penso / he après |

### Gradació MECR

| Nivell | Canvis |
|--------|--------|
| A1-A2 | Només el "què ha passat" + 1 emoció. Frases curtes. |
| B1 | Fet + emoció + reflexió breu. |
| B2 | Entrada completa amb matís. |

### Regles crítiques LF
- **Primera persona sempre**: "he vist", "he pensat".
- **Separar fets d'emocions** en paràgrafs distints.
- **Nomenar les emocions explícitament**: "estava content", "em vaig avergonyir".
- **Conclusió orientada a l'aprenentatge**: "el que he après és...".

### Contraindicacions
- NO reflexions filosòfiques abstractes.
- NO dobles sentits o ironia.
- NO crítiques a persones sense anonimitzar (qüestió ètica).
- NO exageració dramàtica.

### Exemple XML

```xml
<diari>
  <data>18 d'abril de 2026</data>
  <titol>El dia que vaig aprendre a nedar</titol>

  <p>Avui he anat a la piscina amb el meu pare. He fet 5 metres jo sol,
  sense surodors. És la primera vegada.</p>

  <p>Al principi tenia por. Després m'he sentit molt content.</p>

  <p>He après que si proves les coses, moltes vegades surten bé.</p>
</diari>
```

---

# Tipologia Argumentativa

Funció: **defensar una posició** amb raons i evidència.
Estructura canònica: Tesi → Arguments (amb evidència) → Conclusió.

## 14. Article d'opinió

### Propòsit pedagògic
Expressar i defensar un punt de vista amb raons. Desenvolupa **pensament
crític** i **argumentació raonada**.

### Etapa i context curricular
ESO (segon cicle) i batxillerat. Llengua, ètica, projecte de centre.

### Composició estructural

| Ordre | Element | Obligatori? | Notes |
|-------|---------|-------------|-------|
| 1 | `<titol>` | ✅ | Suggereix la tesi |
| 2 | `<destacat>` | ✅ | Tesi al primer paràgraf |
| 3 | `<p>` | ✅ | Argument 1 + evidència |
| 4 | `<p>` | ✅ | Argument 2 + evidència |
| 5 | `<p>` | ⬜ | Argument 3 + evidència |
| 6 | `<destacat>` | ✅ | Conclusió que reprèn la tesi |

### Gradació MECR

| Nivell | Canvis |
|--------|--------|
| A1-A2 | Tesi + 1 argument + conclusió. Sense contraargument. |
| B1 | Tesi + 2 arguments + conclusió. |
| B2 | Tesi + 3 arguments + contraargument breu + conclusió. |

### Regles crítiques LF
- **Tesi al primer paràgraf**, sense preàmbul.
- **Arguments numerats o clarament separats** (1 per paràgraf).
- **Cada argument amb evidència concreta** (dada, exemple, cita).
- **Conclusió que reprèn la tesi**, no n'introdueix cap d'altra.
- **Connectors argumentatius explícits**: "per tant", "en canvi", "a més".

### Contraindicacions
- NO retorica complexa (preguntes retòriques niades, paral·lelismes).
- NO ironia (pot ser entesa literalment).
- NO atacs personals.
- NO tesis múltiples.

### Exemple XML

```xml
<opinio>
  <titol>Hem de cuidar millor els boscos</titol>
  <destacat>Cal protegir els boscos. Els necessitem per a viure.</destacat>

  <p>Els boscos donen oxigen. Sense oxigen no podem respirar.
  Un arbre gran dona oxigen per a 10 persones cada any.</p>

  <p>Els boscos també són casa de molts animals. Si tallem els boscos,
  els animals perden la seva casa.</p>

  <destacat>Per tot això, hem de cuidar i plantar més arbres.</destacat>
</opinio>
```

---

## 15. Ressenya / crítica

### Propòsit pedagògic
Valorar una obra (llibre, pel·lícula, esdeveniment) amb criteri. Desenvolupa
**judici estètic** i **argumentació valorativa**.

### Etapa i context curricular
ESO i batxillerat. Llengua, literatura, arts, educació visual.

### Composició estructural

| Ordre | Element | Obligatori? | Notes |
|-------|---------|-------------|-------|
| 1 | `<titol>` | ✅ | Títol de la ressenya |
| 2 | `<referent>` | ✅ | Obra ressenyada (títol, autor, any) |
| 3 | `<p>` | ✅ | Descripció: de què tracta |
| 4 | `<p>` | ✅ | Valoració: què està bé / què no |
| 5 | `<destacat>` | ✅ | Recomanació (per a qui) |

### Gradació MECR

| Nivell | Canvis |
|--------|--------|
| A1-A2 | Descripció + una valoració + recomanació sí/no. |
| B1 | Descripció + 2 valoracions (positiva i negativa) + recomanació. |
| B2 | Ressenya completa amb matís. |

### Regles crítiques LF
- **Descripció abans de valoració**: primer què és, després què en pensem.
- **Separar fets de judicis**: "la pel·lícula dura 2 hores" (fet) vs "és massa
  llarga" (judici).
- **Recomanació concreta**: "bona per a nens de 8 a 10 anys" (no "recomanable").
- **Evitar spoilers**: no revelar el final.

### Contraindicacions
- NO sarcasme o ironia.
- NO comparacions amb obres no conegudes pel lector.
- NO llenguatge crític especialitzat sense explicar.
- NO valoracions sense argument.

### Exemple XML

```xml
<ressenya>
  <titol>Ressenya de "El petit príncep"</titol>
  <referent>"El petit príncep", d'Antoine de Saint-Exupéry (1943).</referent>

  <p>Aquest llibre explica la història d'un príncep que viu en un petit
  planeta. Viatja per l'espai i coneix gent diferent.</p>

  <p>És un llibre bonic i fàcil de llegir. Les il·lustracions són molt boniques.
  Algunes idees són difícils d'entendre del tot.</p>

  <destacat>És un llibre recomanable per a nens i adults.</destacat>
</ressenya>
```

---

## 16. Assaig

### Propòsit pedagògic
Explorar una idea o pregunta amb profunditat reflexiva. Desenvolupa
**pensament complex** i **escriptura acadèmica**.

### Etapa i context curricular
Batxillerat principalment. Humanitats, filosofia, llengua, treball de recerca.

### Composició estructural

| Ordre | Element | Obligatori? | Notes |
|-------|---------|-------------|-------|
| 1 | `<titol>` | ✅ | Pregunta o tesi central |
| 2 | `<p>` | ✅ | Introducció: context + tesi |
| 3 | `<apartat>` + `<p>` | ✅ | Desenvolupament (2-4 apartats) |
| 4 | `<cita>` | ⬜ | Veus d'autors rellevants |
| 5 | `<p>` | ✅ | Conclusió |
| 6 | `<referent>` | ⬜ | Bibliografia mínima |

### Gradació MECR

| Nivell | Canvis |
|--------|--------|
| A1-A2 | **No aplicable**: l'assaig és inherentment complex. Si cal, convertir en article d'opinió. |
| B1 | Introducció + 1 apartat de desenvolupament + conclusió. Sense cites. |
| B2 | Estructura completa amb cites. |

### Regles crítiques LF
- **Tesi clara a la introducció** (no al final).
- **Cada apartat desenvolupa una idea** del paraigua tesi.
- **Cites integrades, no decoratives**: explicar per què importa la cita.
- **Vocabulari acadèmic definit** a la primera aparició.

### Contraindicacions
- NO tesi implícita o ambigua.
- NO digressions sense connexió amb la tesi.
- NO llenguatge barroc o circumlocucions.
- NO conclusions obertes ("cadascú que en pensi el que vulgui").

### Exemple XML

```xml
<assaig>
  <titol>Per què llegim literatura?</titol>

  <p>Llegim literatura per moltes raons. Aquest text defensa que la raó
  més important és que la literatura ens ajuda a entendre els altres.</p>

  <apartat>La literatura com a mirall</apartat>
  <p>Quan llegim una novel·la, veiem la vida d'altres persones. Això ens
  permet saber com pensen i com senten.</p>

  <apartat>La literatura com a escola</apartat>
  <p>Les històries ens ensenyen coses sense sermonejar. Ens fan pensar
  sobre què és just i què no.</p>

  <p>Per tant, la literatura no és només entreteniment. És una eina per
  créixer com a persones.</p>
</assaig>
```

---

## 17. Carta / correu

### Propòsit pedagògic
Comunicar-se per escrit amb un destinatari concret, adaptant el registre.
Desenvolupa **pragmàtica** i **consciència del receptor**.

### Etapa i context curricular
Totes les etapes. Llengua, tutoria, projecte de centre (cartes formals).

### Composició estructural

| Ordre | Element | Obligatori? | Notes |
|-------|---------|-------------|-------|
| 1 | `<capcalera>` | ✅ | Destinatari, data, lloc |
| 2 | `<salutacio>` | ✅ | "Benvolgut/da X,..." |
| 3 | `<p>` | ✅ | Introducció: motiu de la carta |
| 4 | `<p>` | ✅ | Cos: contingut |
| 5 | `<p>` | ⬜ | Petició/acció concreta |
| 6 | `<comiat>` | ✅ | "Cordialment,..." |
| 7 | `<signatura>` | ✅ | Nom del remitent |

### Gradació MECR

| Nivell | Canvis |
|--------|--------|
| A1-A2 | Carta molt breu. Salutació i comiat senzills. 1 paràgraf de cos. |
| B1 | 2-3 paràgrafs. Fórmules més variades. |
| B2 | Carta formal completa amb registre elaborat. |

### Regles crítiques LF (Federal Plain Language Act, 2010)
- **Motiu al primer paràgraf**: per què escrius.
- **Petició concreta i única**: què vols que faci el destinatari.
- **Una acció per carta**: no barrejar demandes.
- **Registre ajustat al destinatari**: formal (institució) o informal (amic).
- **Frases 15-20 paraules màx**, veu activa.

### Contraindicacions
- NO fórmules arcaiques ("En prego acceptació de les més distingides salutacions").
- NO introduccions llargues abans del motiu.
- NO múltiples peticions barrejades.
- NO abreviatures sense explicar.

### Exemple XML

```xml
<carta>
  <capcalera>
    Destinatari: Director de l'escola
    Lloc: Barcelona
    Data: 18 d'abril de 2026
  </capcalera>

  <salutacio>Benvolgut director,</salutacio>

  <p>Li escric per demanar un canvi d'horari per a l'excursió del divendres.</p>

  <p>Alguns alumnes no poden venir a les 8 del matí per problemes de transport.
  Proposem començar a les 9.</p>

  <p>Agrairia que em confirmés si és possible.</p>

  <comiat>Cordialment,</comiat>
  <signatura>Maria Ribas, tutora de 2n d'ESO</signatura>
</carta>
```

---

# Tipologia Instructiva

Funció: **guiar l'execució** d'una tasca, procés o procediment.
Estructura canònica: Materials → Passos → Resultat esperat.

## 18. Procediment / protocol

### Propòsit pedagògic
Executar una seqüència d'accions per assolir un objectiu concret. Desenvolupa
**raonament seqüencial** i **rigor procedimental**.

### Etapa i context curricular
Totes les etapes. Ciències (pràctiques de laboratori), tecnologia, educació
física, arts plàstiques.

### Composició estructural

| Ordre | Element | Obligatori? | Notes |
|-------|---------|-------------|-------|
| 1 | `<titol>` | ✅ | Nom del procediment |
| 2 | `<entradeta>` | ⬜ | Objectiu del procediment |
| 3 | `<apartat>` "Materials" + `<llista>` | ✅ | Què necessites |
| 4 | `<apartat>` "Passos" + `<llista numerada>` amb `<pas>` | ✅ | Seqüència |
| 5 | `<apartat>` "Resultat" + `<p>` | ⬜ | Què has d'obtenir |
| 6 | `<caixa>` "Atenció" | ⬜ | Seguretat, precaucions |

### Gradació MECR (W3C Cognitive Accessibility)

| Nivell | Canvis |
|--------|--------|
| A1 | Màx 4 passos. 1 verb per pas. Pictograma obligatori per pas. |
| A2 | 5-6 passos. Pictograma recomanat. |
| B1 | Passos lliures. Indicacions amb connectors. |
| B2 | Procediment complet. |

### Regles crítiques LF (UNE 153101 + W3C)
- **Materials en llista abans dels passos**.
- **Cada `<pas>`** = 1 verb d'acció + 1 objecte concret.
- **Ordre cronològic estricte**: mai reordenar per legibilitat.
- **Passos independents**: cada pas s'ha de poder executar sense mirar el següent.
- **Subjecte "tu" explícit** quan calgui claredat.

### Contraindicacions
- NO passos condicionals niats ("si X, fes Y; si no, fes Z").
- NO passos implícits o omesos.
- NO instruccions en passiva ("s'afegirà l'aigua").
- NO observacions digressives al mig dels passos.

### Exemple XML

```xml
<procediment>
  <titol>Com plantar una llavor</titol>
  <entradeta>Aprendràs a plantar una llavor i veure-la créixer.</entradeta>

  <apartat>Materials</apartat>
  <llista tipus="bullet">
    <item>Un got de plàstic.</item>
    <item>Terra.</item>
    <item>Una llavor de mongeta.</item>
    <item>Aigua.</item>
  </llista>

  <apartat>Passos</apartat>
  <llista tipus="numerada">
    <pas n="1">Posa terra al got fins a mitja alçada.</pas>
    <pas n="2">Fes un forat petit al centre amb el dit.</pas>
    <pas n="3">Posa la llavor dins del forat.</pas>
    <pas n="4">Tapa la llavor amb una mica de terra.</pas>
    <pas n="5">Rega amb aigua fins que la terra estigui humida.</pas>
  </llista>

  <apartat>Resultat</apartat>
  <p>En uns dies, veuràs una petita planta verda sortint de la terra.</p>
</procediment>
```

---

## 19. Receptari

### Propòsit pedagògic
Elaborar un plat seguint una seqüència d'accions culinàries. Desenvolupa
**autonomia pràctica** i **vocabulari funcional**.

### Etapa i context curricular
Primària (tallers), ESO (tecnologia, tutoria, projecte cuina saludable), FP
(cuina, hostaleria).

### Composició estructural

| Ordre | Element | Obligatori? | Notes |
|-------|---------|-------------|-------|
| 1 | `<titol>` | ✅ | Nom del plat |
| 2 | `<entradeta>` | ⬜ | Descripció breu (1 frase) |
| 3 | `<caixa>` | ⬜ | Temps, racions, dificultat |
| 4 | `<apartat>` "Ingredients" + `<llista>` | ✅ | Amb quantitats |
| 5 | `<apartat>` "Preparació" + `<pas>` | ✅ | Numerats |
| 6 | `<apartat>` "Resultat" | ⬜ | Què obtindràs |
| 7 | `<imatge>` amb `<peu>` | ⬜ | Del plat acabat |

### Gradació MECR

| Nivell | Canvis |
|--------|--------|
| A1 | Màx 4 ingredients. 3-4 passos. Pictograma per pas. |
| A2 | 5-6 ingredients. 5 passos. Pictograma per ingredient. |
| B1 | Recepta estàndard. |
| B2 | Recepta completa amb variants. |

### Regles crítiques LF
- **Ingredients en ordre d'ús**, no alfabètic.
- **Cada `<pas>`** = 1 verb d'acció + 1 objecte concret.
- **No fusionar passos** ("Barreja i deixa reposar" → 2 passos).
- **Indicacions sensorials preferibles al temps** ("fins que sigui daurat" > "5 minuts").
- **Quantitats sempre explícites amb unitat** (2 ous, 200 g farina).

### Contraindicacions
- NO passatges narratius ("La meva àvia sempre deia...").
- NO condicionals opcionals ("Si vols, pots afegir...").
- NO valoracions subjectives ("Quedarà molt bo").
- NO referències culturals implícites.

### Exemple XML

```xml
<recepta>
  <titol>Coca de sucre</titol>
  <entradeta>Una coca dolça fàcil de fer a casa.</entradeta>

  <caixa>
    <item>Temps: 30 minuts</item>
    <item>Racions: 6 persones</item>
    <item>Dificultat: fàcil</item>
  </caixa>

  <apartat>Ingredients</apartat>
  <llista tipus="bullet">
    <item>200 grams de farina</item>
    <item>100 grams de sucre</item>
    <item>2 ous</item>
    <item>1 got de llet</item>
  </llista>

  <apartat>Preparació</apartat>
  <llista tipus="numerada">
    <pas n="1">Bat els ous en un bol gran.</pas>
    <pas n="2">Afegeix el sucre. Remena fins que es dissolgui.</pas>
    <pas n="3">Aboca la llet. Barreja suaument.</pas>
    <pas n="4">Incorpora la farina a poc a poc.</pas>
    <pas n="5">Coc al forn a 180°C fins que sigui daurat.</pas>
  </llista>
</recepta>
```

---

## 20. Reglament / normes

### Propòsit pedagògic
Formalitzar regles que regulen una activitat o convivència. Desenvolupa
**consciència normativa** i **convivència cívica**.

### Etapa i context curricular
Totes les etapes. Tutoria, projecte de centre, ciutadania, educació física
(reglaments esportius).

### Composició estructural

| Ordre | Element | Obligatori? | Notes |
|-------|---------|-------------|-------|
| 1 | `<titol>` | ✅ | Nom del reglament |
| 2 | `<entradeta>` | ⬜ | Finalitat del reglament |
| 3 | `<apartat>` temàtic + `<llista>` | ✅ | Agrupació de normes |
| 4 | `<item>` | ✅ | Una norma per ítem |
| 5 | `<caixa>` | ⬜ | Conseqüències si no es compleix |

### Gradació MECR

| Nivell | Canvis |
|--------|--------|
| A1 | Màx 5 normes totals. Pictograma per norma. |
| A2 | 6-8 normes agrupades en 2 apartats. |
| B1 | Reglament estàndard amb excepcions simples. |
| B2 | Reglament complet amb jerarquia de normes. |

### Regles crítiques LF
- **Una norma per ítem**, sense conjuncions ni comes complexes.
- **Veu imperativa directa**: "Respecta el torn", no "S'ha de respectar el torn".
- **Agrupar per tema**, no per ordre d'importància.
- **Conseqüències separades de les normes**, en caixa específica.
- **Positiu abans que negatiu**: "Escolta els altres" > "No interrompis".

### Contraindicacions
- NO normes condicionals complexes ("Si X, llavors Y, excepte quan Z").
- NO justificacions dins de la norma.
- NO excepcions niades.
- NO llenguatge legal tècnic sense explicar.

### Exemple XML

```xml
<reglament>
  <titol>Normes de la classe</titol>
  <entradeta>Aquestes normes ens ajuden a aprendre millor tots junts.</entradeta>

  <apartat>Per estudiar bé</apartat>
  <llista tipus="numerada">
    <item>Arriba puntual a classe.</item>
    <item>Porta el material cada dia.</item>
    <item>Aixeca la mà per parlar.</item>
    <item>Escolta quan parla algú.</item>
  </llista>

  <apartat>Per conviure bé</apartat>
  <llista tipus="numerada">
    <item>Tracta els companys amb respecte.</item>
    <item>Cuida el material comú.</item>
    <item>Tira els papers a la paperera.</item>
  </llista>

  <caixa>
    Si no compleixes una norma, la professora et recordarà el que has
    de fer. Si passa diverses vegades, ho parlarem amb la família.
  </caixa>
</reglament>
```

---

# Tipologia Dialogada

Funció: **representar un intercanvi verbal** entre dos o més participants.

## 21. Entrevista

### Propòsit pedagògic
Recollir informació a través d'un intercanvi de preguntes i respostes.
Desenvolupa **competència mediàtica** i **pragmàtica del diàleg asimètric**.

### Etapa i context curricular
ESO i batxillerat. Llengua, socials, projectes de recerca.

### Composició estructural

| Ordre | Element | Obligatori? | Notes |
|-------|---------|-------------|-------|
| 1 | `<titol>` | ✅ | "Entrevista amb X" |
| 2 | `<entradeta>` | ✅ | Qui és l'entrevistat + context |
| 3 | `<imatge>` amb `<peu>` | ⬜ | Foto de l'entrevistat |
| 4 | `<pregunta>` | ✅ | Pregunta de l'entrevistador |
| 5 | `<resposta>` | ✅ | Resposta de l'entrevistat |
| 6 | (repetir 4-5) | ✅ | 4-8 parells pregunta/resposta |

### Gradació MECR

| Nivell | Canvis |
|--------|--------|
| A1-A2 | 3-4 parells pregunta/resposta. Respostes curtes. |
| B1 | 5-6 parells. Respostes d'1-2 frases. |
| B2 | Entrevista completa. |

### Regles crítiques LF
- **Preguntes directes, sense subordinades**: "Què fas quan estàs trist?" >
  "Em podries explicar, si no et sap greu, què sols fer quan et trobes trist?".
- **Respostes simplificades preservant la veu original** (no re-escriure-les
  en tercera persona).
- **Marcar clarament qui parla** amb etiquetes visibles.
- **No linearitzar**: mantenir el format pregunta/resposta, no convertir en prosa.
- **Explicar termes propis de l'entrevistat** (si és expert, definir el seu vocabulari).

### Contraindicacions
- NO preguntes múltiples en una ("Com et dius i què fas?").
- NO preguntes retòriques.
- NO intervencions intermèdies ("i llavors, vostè què va pensar...").
- NO respostes sense pregunta anterior.

### Exemple XML

```xml
<entrevista>
  <titol>Entrevista amb Joan Mas, pagès</titol>
  <entradeta>El Joan Mas té una granja al Vallès. Cultiva tomàquets
  ecològics des de fa 20 anys.</entradeta>

  <pregunta>Per què va decidir ser pagès ecològic?</pregunta>
  <resposta>Vaig començar perquè volia cuidar la terra. L'agricultura
  normal fa servir productes que contaminen.</resposta>

  <pregunta>Què és el més difícil del seu treball?</pregunta>
  <resposta>Aixecar-me molt d'hora. A les 5 del matí ja estic al camp.</resposta>

  <pregunta>Què recomanaria als nens que volen ser pagesos?</pregunta>
  <resposta>Que estudiïn bé i que aprenguin a estimar les plantes.</resposta>
</entrevista>
```

---

## 22. Diàleg / guió teatral

### Propòsit pedagògic
Representar una interacció verbal amb intenció escènica. Desenvolupa
**oralitat**, **expressió corporal** i **comprensió del subtext**.

### Etapa i context curricular
Totes les etapes. Llengua, literatura, educació artística, projecte de centre.

### Composició estructural

| Ordre | Element | Obligatori? | Notes |
|-------|---------|-------------|-------|
| 1 | `<titol>` | ✅ | Títol de l'obra o escena |
| 2 | `<apartat>` "Personatges" + `<llista>` | ✅ | Qui surt |
| 3 | `<acotacio>` inicial | ⬜ | Lloc i situació |
| 4 | `<torn parlant="X">` | ✅ | Intervencions |
| 5 | `<acotacio>` | ⬜ | Què fa el personatge |
| 6 | (repetir 4-5) | ✅ | Desenvolupament de l'escena |

### Gradació MECR

| Nivell | Canvis |
|--------|--------|
| A1-A2 | 2 personatges. 4-6 torns. Acotacions molt curtes. |
| B1 | 3 personatges. Acotacions descriptives. |
| B2 | Guió estàndard. |

### Regles crítiques LF
- **Llistar personatges a l'inici** amb descripció breu (1 línia).
- **Atribuir cada torn** amb el nom del personatge (no amb lletres/inicials).
- **Acotacions al present i 3a persona**: "En Joan entra a l'habitació".
- **Subtext explícit**: si un personatge està enfadat, nomenar-ho a l'acotació
  (les inferències emocionals són difícils en LF).
- **Una acció per acotació**, sense subordinades.

### Contraindicacions
- NO acotacions amb ironia o judicis ("Diu amb un to evidentment fals").
- NO canvis d'escena implícits (marcar-los amb apartat).
- NO llenguatge teatral arcaic o elevat.
- NO monòlegs interns llargs (el teatre és acció externa).

### Exemple XML

```xml
<teatre>
  <titol>La sorpresa</titol>

  <apartat>Personatges</apartat>
  <llista tipus="bullet">
    <item>Marta: una nena de 10 anys.</item>
    <item>Àvia: l'àvia de la Marta.</item>
  </llista>

  <acotacio>La Marta entra a la cuina. L'àvia cuina a la cassola.</acotacio>

  <torn parlant="Marta">Hola, àvia! Què cuines?</torn>
  <torn parlant="Àvia">Estic fent el teu pastís preferit.</torn>

  <acotacio>La Marta somriu i s'acosta a l'àvia.</acotacio>

  <torn parlant="Marta">Gràcies, àvia! Ets la millor.</torn>
</teatre>
```

---

## Referències

### Normatives

1. AENOR. (2018). *UNE 153101:2018 EX — Lectura Fácil. Pautas y recomendaciones
   para la elaboración de documentos*. Madrid: AENOR.
2. AENOR. (2018). *UNE 153102:2018 EX — Guía en Lectura Fácil para validadores
   de documentos*. Madrid: AENOR.
3. IFLA. (2010). *Guidelines for Easy-to-Read Materials* (Professional Report 120).
   The Hague: IFLA.
4. Inclusion Europe. (2010). *Information for all: European standards for making
   information easy to read and understand*. Brussels.
5. W3C. (2018). *Web Content Accessibility Guidelines (WCAG) 2.1*.
6. IEC/IEEE. (2019). *IEC/IEEE 82079-1:2019 — Preparation of information for use*.
7. Ajuntament de Barcelona. (2022). *Siguem clars. Guia de comunicació clara per
   a administracions*.
8. U.S. Office of Management and Budget. (2010). *Federal Plain Language Guidelines*.

### Recerca

9. Xu, W., Callison-Burch, C., & Daumé III, H. (2016). "Optimizing Statistical
   Machine Translation for Text Simplification". *TACL*, 4, 401-415.
10. Scarton, C., Specia, L., & Pianta, E. (2021). "The (Un)Suitability of Automatic
    Evaluation Metrics for Text Simplification". *Computational Linguistics*, 47(4).
11. Reuters Institute. (2024). *Creating news for (and with) people with learning
    disabilities*. University of Oxford.
12. Proceedings of the Third Workshop on Text Simplification, Accessibility and
    Readability (TSAR 2024). Miami, FL: ACL.

### Catalans

13. Associació Lectura Fàcil. *Pautes de Lectura Fàcil*. Barcelona: ALF.
    https://www.lecturafacil.net
14. Consell Superior d'Avaluació del Sistema Educatiu. *Currículum per competències
    de Catalunya*. Generalitat de Catalunya.
15. Institut d'Estudis Catalans. *Lectura fàcil per a nouvinguts: una eina
    possible*. https://publicacions.iec.cat/

### Marcs

16. Halliday, M. A. K. (1994). *An Introduction to Functional Grammar* (2nd ed.).
    London: Edward Arnold. [Base teòrica SFL per a la classificació per tipologies.]
17. Council of Europe. (2001, 2020). *Common European Framework of Reference for
    Languages (CEFR)*. [Gradació per nivells MECR.]

---

## Nota metodològica

Aquest document barreja **regles derivades de fonts normatives** (per als 4
macro-gèneres SFL i per a notícies/procediments/cartes) amb **regles inferides**
(per als sub-gèneres sense estàndard publicat).

Cada fitxa hauria de ser **validada empíricament** amb:
- Adaptacions reals de docents FJE
- Feedback d'alumnes amb perfils diversos (NESE, nouvinguts, etc.)
- Comparació A/B entre adaptacions amb/sense regles específiques

Post-pilot 2026-04-20 a 2026-05-08, revisar quines regles han demostrat valor
i quines són innecessàries o contraproduents.
