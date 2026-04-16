# Guió de demo ATNE — 16/04/2026

**Durada**: 30 min
**Audiència**: 8 direccions pedagògiques + 8 DOPs + 3 àrea pedagogia FJE (total ~19 persones)
**Objectiu**: obtenir compromís per al pilot (NO demo exhaustiva ni presentació tècnica)
**Ask concret**: 2 docents × 8 escoles = 16 docents, pilot 20/04-08/05, ~5 textos per docent
**Ponent**: Miquel Amor (sol)

---

## Estructura (30 min)

| Min | Secció | Què es fa |
|---|---|---|
| 0-3 | Obertura i propòsit | Qui, què, per què |
| 3-7 | El marc: no és rebaixar, és acompanyar | Framing ignasianer + ZPD |
| 7-15 | Demo cas 1 — Primària (Fotosíntesi) | Generar + adaptar A2 nouvingut |
| 15-22 | Demo cas 2 — ESO (Revolució Industrial) | Via observable + multinivell + pictogrames |
| 22-25 | El control de qualitat | Semàfor + LanguageTool + disclaimer |
| 25-28 | L'ask del pilot | Calendari, compromís, feedback |
| 28-30 | Preguntes obertes | Respondre 1-2 preguntes clau |

---

## 0-3 min · Obertura

> "Bon dia. Soc Miquel Amor, de l'àrea de pedagogia de FJE. Us presento ATNE — Adaptador de Textos a Necessitats Educatives. Són 30 minuts: vull ensenyar-vos què fa, com ho fa, i demanar-vos una cosa molt concreta al final."

**Frases clau a dir literalment:**
- "ATNE no és un corrector. No és un generador de continguts. És un assistent pedagògic que ajuda el docent a adaptar un text a la realitat concreta del seu alumnat."
- "I sobretot: no substitueix la vostra mirada. L'amplifica."

**NO fer**:
- ❌ Parlar d'LLMs, Gemma, GPT, Mistral, Supabase, embeddings
- ❌ Explicar l'arquitectura tècnica
- ❌ Ensenyar codi

---

## 3-7 min · El marc pedagògic

> "Abans d'ensenyar-vos el producte, vull que entenguem el mateix per 'adaptar'. Perquè la paraula està gastada."

**Missatge central** (dir literalment):

> "Adaptar **no és rebaixar**. Adaptar no és treure fricció. Adaptar és **apropar-se allà on és l'alumne i oferir-li els ajuts perquè progressi**. L'objectiu final no és la simplificació — és l'aprenentatge."

**Marc ignasianer** (sense ser confessional, ho poden escoltar les DOPs):
- Cura personalis — cada alumne és únic, no un diagnòstic
- Acompanyament — caminar al costat, no davant ni darrere
- "Adaptar a temps, llocs i persones" (Exercicis, principi clàssic)
- Bastida decreixent: el suport es retira quan l'alumne ja no el necessita

**Anchor visual** (si tens slide): la frase al centre:

> **"Quins ajuts oferim perquè l'alumne progressi cap a més autonomia?"**

**Why això primer**: direccions i DOPs necessiten saber que no estem venent "una IA que fa textos fàcils". Estem venent **una eina de cura personalis amplificada**. Si aquest marc no és clar, la resta es malinterpreta.

---

## 7-15 min · Demo cas 1 — Primària (Fotosíntesi)

**Objectiu pedagògic del cas**: ensenyar que el docent configura una vegada el perfil de l'aula i ATNE produeix un text adequat sense haver-lo d'escriure des de zero.

### Script click-by-click

**1. Pas 1 — Context i perfil** (~1 min)
- Etapa: **Primària**, Curs: **5è**, Matèria: **Coneixement del medi natural**
- Perfil alumnat: **Nouvingut A2** (selecciona perfil ja guardat o crea ràpid)
- Observacions: "alumne arribat fa 4 mesos, alfabetització llatina, llengua inicial: àrab"
- Frase a dir: *"Configuro el perfil una vegada. Per a aquest alumne. No per a 'nouvinguts' en abstracte."*

**2. Pas 2 — Generar text original** (~2 min)
- Tab **"Generar amb IA"** → prompt: *"Text expositiu sobre la fotosíntesi per a 5è de primària, estàndard curricular"*
- **Selector de model**: mantenir **GPT-4o-mini** (descobriment 14/04: és el que millor s'adequa a primària, 14.6 wps dins de B1)
- Clica generar → el text apareix (~3-5s)
- Frase a dir: *"Aquest és un text curricular estàndard. Encara no l'hem adaptat. Això és el que un llibre de text us donaria."*

**3. Pas 3 — Configurar complements** (~1.5 min)
- Mostrar la **columna esquerra fixa** amb el perfil: *"Des de qualsevol punt del procés, veieu per a qui estem adaptant."*
- Activar **Ajuts lèxics** (definicions integrades + glossari)
- Activar **Ajuts visuals** (pictogrames)
- Activar **Ajuts de comprensió** (preguntes + bastides)
- Frase a dir: *"Aquests són els suports que acompanyaran el text. Cada família té un sentit pedagògic: lèxics, visuals, de síntesi, de comprensió, d'ampliació. No són accessoris — són la bastida."*

**4. Pas 4 — Resultat adaptat** (~2.5 min)
- Esperar que aparegui el text adaptat (~8-15s amb SSE mostrant progrés)
- **Activar toggle "Comparar amb original"** per ensenyar abans/després
- Scroll per ensenyar:
  - Frases curtes, una idea per frase
  - Negretes amb definicions integrades
  - Pictogrames al costat (si el text els accepta)
  - Preguntes de comprensió sota
- **Obrir el Quality Report** (ensenyar el semàfor verd + la fila de llegibilitat dins A2)
- Frase a dir: *"Mateix contingut curricular. Mateixa idea. Però ara aquest alumne concret pot accedir-hi amb dignitat."*

**Fallback si alguna cosa falla**:
- Si el Pas 2 falla (API timeout): tenir preparat un text original copiat al clipboard com a backup.
- Si el Pas 4 falla: tenir el resultat esperat en una captura de pantalla de fallback.
- Si res funciona: saltar directament a l'ask i ensenyar captures estàtiques. Acceptar que falla.

---

## 15-22 min · Demo cas 2 — ESO (Revolució Industrial)

**Objectiu pedagògic del cas**: ensenyar la **via observable** (doble columna) i el **multinivell** (DUA: Accés / Core / Enriquiment).

### Script click-by-click

**1. Pas 1 — Via observable** (~2 min)
- Etapa: **ESO**, Curs: **3r**, Matèria: **Ciències socials**
- **Canviar a via observable** (el toggle al Pas 1)
- Frase a dir crítica: *"Aquí està la part que més m'importa que veieu. Moltes vegades el docent no té diagnòstic de l'alumne. Té observacions. ATNE parla el llenguatge de l'observació."*
- Marcar 3 de les 6 conductes:
  1. *"Li costa mantenir l'atenció en textos llargs"*
  2. *"Té un vocabulari més reduït del que necessita per al curs"*
  3. *"Capta la idea general però li costa retenir els detalls concrets"*
- **Mostrar la doble columna**: a la dreta apareixen automàticament els ajuts que es recomanarien per a aquestes observacions
- Frase a dir: *"El docent no ha de diagnosticar. Observa i ATNE proposa. I si el docent vol ajustar els ajuts, pot fer-ho: és transparent."*

**2. Pas 2 — Pujar text** (~1 min)
- Tab **"Pujar fitxer"** → pujar un PDF de text de llibre sobre Revolució Industrial (tenir-lo preparat al desktop)
- O alternativa: copiar el text d'un cas ja preparat als "Textos anteriors"
- Frase a dir: *"El docent porta el seu propi text. Del llibre, del dossier, del que sigui. No li fem canviar de material."*

**3. Pas 3 — Complements + multinivell** (~1.5 min)
- Ensenyar el catàleg de 7 famílies d'ajuts "Ajuts X"
- Activar: **Pictogrames**, **Definicions integrades**, **Bastides**, **Preguntes de comprensió**
- Frase a dir sobre bastides: *"Les bastides són ajuts de comprensió — són l'exemple més clar de 'acompanyament que es retira'. Comencen amb molta estructura i el docent les va retirant a mesura que l'alumne avança."*

**4. Pas 4 — Multinivell (tres pestanyes)** (~2.5 min)
- Mostrar les 3 versions: **Accés** / **Estàndard (Core)** / **Enriquiment**
- **Obrir el DUA Accés** i ensenyar el text amb pictogrames estil exemple del Saber-ne+:
  ```
  🛠️ Abans la gent fa les coses a mà.
  🏭 Després la gent treballa a la fàbrica.
  ⚙️ A la fàbrica hi ha màquines.
  🚂 La màquina de vapor és molt important.
  💡 Això és la Revolució Industrial.
  ```
- Frase a dir: *"Això no és un text simplificat. És el mateix contingut curricular: un fenomen històric, causes, conseqüències, rellevància. Però amb ancoratges visuals. L'alumne pot parlar de la Revolució Industrial amb els seus companys."*
- **Obrir l'Enriquiment** i ensenyar que per a altes capacitats ATNE **no simplifica** sinó que **aprofundeix**: connexions interdisciplinàries, pensament crític, més rigor.
- Frase a dir: *"Aquí és on ATNE respon al vostre principi de 'no rebaixar mai'. Els alumnes d'alta capacitat reben més, no menys. Això és magis."*

---

## 22-25 min · Control de qualitat i transparència

**Missatge**: no es vol vendre màgia, es vol vendre un sistema supervisable.

- **Obrir el Quality Report** en pantalla
- Ensenyar les files:
  - ✅ **Caràcters exòtics**: 0 detectats
  - ✅ **LanguageTool**: N correccions aplicades automàticament
  - ⚠️ **Paraules sospitoses**: si n'hi ha, com es visualitzen
  - ✅ **Llegibilitat**: paraules/frase dins del nivell MECR
  - ℹ️ **Avisos d'estil**: no crítics
- Frase a dir: *"Tota la generació passa per un pipeline de qualitat determinista: ortografia catalana via LanguageTool de Softcatalà, filtre de caràcters estranys, càlcul de llegibilitat. El docent veu el que passa amb el text. Res ocult."*

- **Ensenyar el banner ambre al peu**:

  > *"Aquest assistent ajuda, però NO substitueix la revisió humana. Revisa sempre el text final abans d'usar-lo amb els alumnes."*

- Frase a dir crítica: *"Aquest missatge apareix sempre. És la nostra posició: **ATNE és un amplificador de la mirada docent, no un substitut**. La decisió final és del docent que coneix l'alumne."*

---

## 25-28 min · L'ask del pilot

**L'ask en una frase:**

> *"Us demano 2 docents per escola que vulguin provar ATNE amb textos reals durant 3 setmanes. El pilot comença el 20 d'abril i acaba el 8 de maig. Cada docent adaptarà aproximadament 5 textos i em farà arribar feedback."*

**El calendari** (mostrar en slide o pizarra):
- **16-19/04** (aquesta setmana) — enllaç al pilot + vídeo de 5 min + formulari d'inscripció
- **20/04-08/05** (3 setmanes) — el pilot viu
- **11-15/05** — informe de resultats i retorn a direccions
- **Juny** — marge per iterar amb el feedback rebut

**Què necessito de vosaltres**:
1. **Avui**: un "sí, hi confiem" com a direcció pedagògica
2. **Aquesta setmana**: identificar 2 docents voluntaris a la vostra escola
3. **Durant el pilot**: permetre'ls fer servir ATNE amb textos reals de classe
4. **Després**: 1 hora de feedback estructurat amb mi

**Què rebreu**:
- Informe individual per escola (agregat, sense PII dels alumnes)
- Informe global amb aprenentatges
- Accés continu a ATNE si decidiu seguir-lo

**Frase a dir per tancar**:

> *"Si dieu que sí, el 9 de maig tindrem dades reals de si ATNE ajuda o no. Si no funciona, ho veurem junts i ho retirarem. Si funciona, tenim eina FJE per al curs vinent."*

---

## 28-30 min · Preguntes

**Preguntes esperades i respostes preparades**:

**P1: "Què passa amb les dades dels alumnes?"**
> "Cap dada personal de l'alumne entra al sistema. El docent descriu el perfil amb etapa, curs, necessitats observades — mai nom, mai informació sensible. Els textos generats queden a una base de dades per avaluar qualitat, però sense vincular a cap alumne. Més detall al document de privacitat que us faré arribar."

**P2: "I si s'equivoca? I si inventa coses?"**
> "Pot passar — per això hi ha el pipeline de qualitat i el disclaimer. Hem detectat i documentat exemples reals d'errors: paraules llatines, caràcters exòtics, llegibilitat fora de nivell. El Quality Report els marca. La regla és sempre: el docent revisa abans de portar-ho a classe. I durant el pilot recollirem tots aquests casos per millorar-ho."

**P3: "Quant costa?"**
> "Durant el pilot: 0€. Post-pilot per tota FJE: uns 15€/mes en infraestructura. Els detalls de costos estan al document d'estratègia que compartiré. Volem una eina sostenible, no dependre d'una subscripció cara."

**P4: "Hi ha altres escoles que ja ho usin?"**
> "No. Sou els primers. Per això és un pilot — volem validar amb vosaltres abans d'obrir-ho a més contextos. El compromís amb vosaltres és bidireccional: vosaltres ens doneu la realitat, nosaltres us donem el control."

**P5: "Quina IA usa?"**
> "Usem diversos motors per a diferents tasques. Per a primària, GPT-4o-mini; per a ESO i batxillerat, Gemma 4 (un model obert). La decisió no és ideològica — és empírica. Hem testat 5 models amb 200 casos cadascun i triat els que millor adapten al català i al nivell dels alumnes. Detalls tècnics al final del dossier."

**P6: "I si un docent vol usar-ho amb castellà?"**
> "ATNE està pensat per al català. El pipeline de qualitat (LanguageTool) és específic català. Per al castellà, tindríem una segona versió — no és trivial, però tampoc impossible. Si ho voleu explorar, ho parlem post-pilot."

---

## Checklist pre-demo (15/04 al vespre)

- [ ] Tot això verificat: `/api/health` retorna tot verd (vegeu secció paral·lela de verificació Cloud Run)
- [ ] Tenir 2 perfils ja guardats: "Nouvingut A2 primària 5è" i "ESO 3r amb observacions"
- [ ] Tenir un PDF de Revolució Industrial al desktop com a backup
- [ ] Tenir captures de pantalla de fallback dels 2 casos adaptats, per si cau la xarxa
- [ ] Provar en mode incògnit del navegador per assegurar zero caché d'estat previ
- [ ] Wifi de la sala verificat abans de la reunió
- [ ] Navegador en fullscreen + zoom 125% per visibilitat
- [ ] Notebook carregat + cable per si de cas
- [ ] Cronòmetre (mòbil) per controlar els 30 min estricte

## Què NO dir al demo

- ❌ "Aquesta tecnologia..." → dir "aquesta eina"
- ❌ "L'LLM" / "el model" → dir "ATNE" o "l'assistent"
- ❌ "Prompt engineering" / "embeddings" → no sortir del llenguatge pedagògic
- ❌ "Encara no està del tot llest" → dir "és la versió del pilot, en construcció"
- ❌ "És gratis perquè la IA és gratis" → dir "és sostenible gràcies a models oberts"
- ❌ Qualsevol comparació amb ChatGPT

## Missatges que han d'arribar (els 3 crítics)

1. **ATNE no rebaixa — acompanya i apropa.** (framing ignasianer)
2. **El docent decideix, ATNE proposa.** (disclaimer i transparència)
3. **Sense vosaltres no hi ha pilot. Us necessitem 16 docents durant 3 setmanes.** (ask concret)
