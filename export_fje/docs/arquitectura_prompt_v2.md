# Arquitectura de Prompt v2 — Triangulacio i Sintesi

**Projecte**: ATNE -- Adaptador de Textos a Necessitats Educatives
**Data**: 2026-03-27
**Fonts**: 6 documents de recerca (2 models) + audit del system prompt actual (server.py)
**Autor**: Claude Opus 4.6 amb supervisio Miquel Amor

---

## 1. Resum executiu

Despres d'analitzar i triangular els 6 documents de recerca, emergeixen 5 conclusions principals:

**1. El prompt actual fa massa coses alhora.** El `BASE_SYSTEM_PROMPT` envia ~30 instruccions simultaneament -- incloent els 5 nivells MECR quan nomes en cal 1, i totes les regles de creuament quan potser cap s'aplica. Tots els documents coincideixen que 7-12 instruccions es el rang optim per a LLMs. Aquesta es la millora de mes alt impacte i mes baix cost.

**2. Falta el "qui" i el "que".** El prompt descriu COM adaptar pero mai descriu PER A QUI (persona-audience) ni QUE tipus de text es (genere discursiu). Un nouvingut marroqui de 14 anys amb A1 i un nouvingut xines de 8 anys amb pre-A1 reben el mateix prompt. Identificar el genere discursiu (narracio, explicacio, instruccio, argumentacio) canviaria radicalment les regles aplicades.

**3. Hi ha un desert de few-shot examples.** Cap exemple complet de text original → text adaptat. Tots els documents d'analisi LLM coincideixen: 1-2 exemples redueixen la variabilitat un 40-60%. Afegir-ne es la segona millora amb mes relacio impacte/cost.

**4. Les instruccions de Lectura Facil, MECR i DUA sovint es contradiuen sense regla de resolucio.** Exemple: DUA Acces demana "suport visual maxim" pero LF diu "una idea per frase" -- que passa amb les definicions parentetiques que allarguen la frase? No hi ha jerarquia explicita.

**5. Hi ha 200+ instruccions possibles, pero el 80% de l'impacte ve de ~25.** La triangulacio dels dos bancs d'instruccions (119 + 70 variables) mostra un nucli compartit de ~25 instruccions que ambdos models consideren critiqu. La resta son condicionals per perfil o de presentacio (CSS/codi).

---

## 2. Convergencies (alta fiabilitat)

Conclusions on TOTS els documents coincideixen, organitzades per eix.

### 2.1 Sobre les variables d'adaptacio

| Convergencia | Fonts que coincideixen |
|---|---|
| Les variables linguistiques (longitud frase, complexitat sintactica, frequencia lexica, densitat terminologica) son les mes rendibles i les que l'LLM controla millor | Banc 119 (A1-A2), Taxonomia A1 (TXT_*), Analisi LLM (cap. 1.1-1.2), Modelabilitat (3.1) |
| L'estructura macro (titols, paragrafs curts, llistes, resum inicial/final) te impacte immediat en comprensio | Banc 119 (B1-B3), Taxonomia A1 (MACRO_*), Marcs teorics (Mayer) |
| Les variables de presentacio (tipografia, interlineat, contrast) NO les pot controlar l'LLM -- cal codi/CSS | Taxonomia A1 (LAY_*), Analisi LLM (cap. 3), Modelabilitat (4.2) |
| La coherencia terminologica (un terme = un concepte, no sinonimat) es critica per a tots els perfils | Banc 119 (A1.05), Taxonomia A1 (TXT_TERM_CONS), Marcs teorics (Dehaene) |
| El scaffolding decreixent per a definicions es una practica fonamentada i implementable | Marcs teorics (Vygotsky), Banc 119 (A1.02), Analisi LLM (cap. 1.4, 1.8) |

### 2.2 Sobre els marcs teorics rellevants

| Marc | Consens | Impacte per a ATNE |
|---|---|---|
| **Halliday (LSF)** | Unanimitat que es la llacuna mes important del marc actual. Cap dels 4 pilars (DUA, LF, MECR, WCAG) dona un model linguistic de COM funciona un text | Regles per genere discursiu, desnominalitzacio, cohesio |
| **Sweller (CLT)** | Ja parcialmente integrat (regla max conceptes), pero manca split-attention, pre-training, expertise reversal | Glossari previ per A1/A2, graduar suports per nivell |
| **Vygotsky (ZDP)** | Scaffolding decreixent es la millora amb millor relacio impacte/cost | Definicions que van de completa → breu → absent |
| **Mayer** | Principi de coherencia ("no afegeixis") i senyalitzacio directament aplicables | Instruccio anti-farcit i estructura de destacats |
| **Dehaene/Wolf** | Regles especifiques per dislexia (evitar compostos llargs, alta frequencia) son concretes i accionables | Capa condicional per dislexia |

### 2.3 Sobre les barreres per perfil

| Convergencia | Fonts |
|---|---|
| Cada perfil te una **barrera nuclear** diferent: TEA=inferencia, TDAH=atencio, dislexia=decodificacio, nouvingut=lexic+cultural, DI=comprensio discursiva | Mapa barreres (matriu 13x10), Banc 119 (seccio H) |
| Les comorbiditats NO sumen linealment: es multipliquen. TDAH+dislexia no es atencio+decodificacio sino un efecte combinat pitjor que la suma | Mapa barreres (16.3), Banc 119 (I2.03) |
| La doble excepcionalitat (2e) requereix doble enfocament: adaptacio + enriquiment simultanis, mai sacrificar l'un per l'altre | Mapa barreres (16.2), Banc 119 (H9) |
| Les adaptacions per disc. visual, motora i TDC son principalment de codi/CSS/frontend, no de prompt LLM | Mapa barreres (8-11), Taxonomia A1 (LAY_*, ACC_*) |

### 2.4 Sobre les capacitats/limits dels LLM

| Convergencia | Fonts |
|---|---|
| Simplificacio lexica i sintactica: capacitat ALTA en tots els models | Analisi LLM (1.1-1.2), Modelabilitat (4.1) |
| Comptar paraules per frase: capacitat BAIXA (no compten, intueixen) | Analisi LLM (2.1), Modelabilitat (4.1) |
| Gemini Flash te el pitjor seguiment d'instruccions i mes meta-text | Analisi LLM (4), Modelabilitat (3.2) |
| Claude i GPT-4 segueixen millor instruccions complexes | Analisi LLM (4), Modelabilitat (6.2) |
| 7-12 instruccions: alta fiabilitat; >20: degradacio notable | Analisi LLM (5.1), Modelabilitat (5, 7) |
| Few-shot examples redueixen variabilitat un 40-60% | Analisi LLM (5.4), Modelabilitat (7.3) |
| L'autocheck dins del mateix prompt es "majoritariament teatre" | Analisi LLM (5.5) |
| El persona-audience pattern es molt mes efectiu que nivells abstractes | Analisi LLM (6.5), Modelabilitat (7.1) |

### 2.5 Sobre l'arquitectura de prompt

| Convergencia | Fonts |
|---|---|
| Cal enviar NOMES les instruccions rellevants per al cas concret | Analisi LLM (5.1, 7), Modelabilitat (5, 7) |
| Cal enviar NOMES el nivell MECR de sortida (no tots 5) | Analisi LLM (7, taula #2) |
| El pipeline en 2 passos (adaptar → complements) milloraria la qualitat | Analisi LLM (5.2), Modelabilitat (5) |
| Cal post-processament amb codi Python per verificar el que l'LLM no pot garantir | Analisi LLM (2.1, 2.4, 5.5), Modelabilitat (5, 7.5) |

---

## 3. Divergencies significatives

### 3.1 Quantitat d'instruccions per prompt

| Font | Posicio |
|---|---|
| Analisi LLM (Claude Opus) | "7-12 instruccions alta fiabilitat, 15-20 acceptable, >20 degradacio" |
| Modelabilitat (altre model) | "5-8 regles claus per crida" |
| Banc 119 instruccions | Llista 119 instruccions, suggerint que totes son implementables |

**Recomanacio**: Adoptar el criteri mes conservador (5-8 instruccions fixes + 3-5 condicionals per perfil = max 13 al prompt). Les 119 instruccions son un REPOSITORI del qual seleccionar, no un llistat per enviar sencer.

### 3.2 Necessitat de canvi de model

| Font | Posicio |
|---|---|
| Analisi LLM | Molt critic amb Gemini Flash: "la funcio clean_gemini_output() de 40+ linies es prova directa que el model no segueix instruccions". Recomana canvi a produccia |
| Modelabilitat | Mes neutra: "Gemini 2.x competent en control d'estil i to", pero reconeix que "compliment de formats rigids menys estable" |

**Recomanacio**: Mantenir Gemini Flash per prototip (gratuit), pero planificar migracio a Claude Sonnet o Gemini Pro per a produccia FJE. La funcio `clean_gemini_output()` es evidencia objectiva del problema.

### 3.3 Utilitat de l'autocheck

| Font | Posicio |
|---|---|
| Analisi LLM | "Majoritariament teatre dins del mateix prompt" |
| Banc 119 | Inclou I1.01 (autocheck terminologic) com a instruccio obligatoria |
| Modelabilitat | No aborda directament, pero recomana "mini-checklist de comprovacio" |

**Recomanacio**: Mantenir l'autocheck (cost zero, petita millora marginal) pero NO comptar-hi com a verificacio real. Implementar verificacio amb codi Python com a pas obligatori.

### 3.4 Taxonomia de variables: estructura plana vs jerarquica

| Font | Posicio |
|---|---|
| Banc 119 | Organitzacio jerarquica: 9 categories (A-I), 119 instruccions amb ID, font, graduabilitat, exemples |
| Taxonomia A1 | Organitzacio per dominis funcionals: 8 dominis amb codis (TXT_, MACRO_, SEM_, LAY_, MOD_, TASK_, ACC_, LR_) |

**Recomanacio**: Fusionar en un catàleg unic amb l'estructura del Banc 119 (mes detallada i amb exemples) pero incorporant els codis de la Taxonomia A1 (mes aptes per a metadades i JSON). Veure seccio 7.

---

## 4. Buits identificats

| # | Buit | Que falta | On caldria cobrir-ho |
|---|---|---|---|
| 1 | **Genere textual** | Cap document defineix regles operatives per genere (narracio, explicacio, instruccio, argumentacio) mes enlla de la mencio de Halliday. Falten exemples concrets per a cada genere | Prompt + few-shot |
| 2 | **Validacio en catala** | No existeixen metriques de llegibilitat validades per al catala. L'LLM no te dades de frequencia lexica en catala | Backend Python |
| 3 | **Evidencia empirica d'impacte** | Cap document mesura l'impacte REAL de les adaptacions sobre la comprensio de l'alumnat. Tot es teoric | Pilot amb docents FJE |
| 4 | **Adaptacio per etapa** | Les regles actuals son generiques. Un text de P5 i un de 2n Batxillerat reben essencialment les mateixes instruccions amb diferent MECR | Capa condicional per etapa |
| 5 | **Materia i camp disciplinar** | La variable "materia" (cientific/humanistic/linguistic) es massa grossa. Un text de matematiques i un de biologia necessiten regles molt diferents | Ampliar tipologia de materia |
| 6 | **FP i formacio professional** | Cap document aborda les particularitats de FP (vocabulari tecnic sectorial, procediments, normativa) | Extensio futura |
| 7 | **Adaptacio d'activitats vs text** | Gairebe totes les instruccions es centren en adaptar TEXT. L'adaptacio d'ACTIVITATS i AVALUACIO te regles propies poc desenvolupades | Banc 119 (F) inicia, pero falta profunditat |
| 8 | **Pictogrames reals** | Tots els documents mencionen pictogrames com a element clau, pero l'unica implementacio actual son emojis Unicode | Integracio ARASAAC |
| 9 | **Feedback al docent** | Cap document aborda com informar el docent de QUE s'ha canviat i PER QUE, d'una manera util | Millora de l'auditoria comparativa |
| 10 | **Multilingue real** | El glossari bilingue depen de la fiabilitat de l'LLM, que es baixa per a llengues com amazic, wolof o bangla | Diccionari extern o disclaimer |

---

## 5. Auditoria de l'estat actual vs. ideal

### Comparacio server.py actual vs. recomanacions de la recerca

| Area | Estat actual (server.py) | Estat ideal (recerca) | Gap | Prioritat |
|---|---|---|---|---|
| **Nombre d'instruccions** | ~30 instruccions al BASE_SYSTEM_PROMPT | 7-12 fixes + 3-5 condicionals | Alt: 2-3x massa instruccions | **P0** |
| **Nivells MECR** | S'envien els 5 nivells sempre | Enviar NOMES el nivell de sortida | Alt: 4 nivells de soroll | **P0** |
| **Regles de creuament** | S'envien TOTES (8 regles) sempre | Enviar nomes les que s'apliquen al perfil | Mitja-alt | **P0** |
| **Genere textual** | No es detecta ni s'usa | Regles per narracio, explicacio, instruccio, argumentacio | Alt: dimensio absent | **P1** |
| **Few-shot examples** | Zero exemples | 1-2 exemples per nivell MECR i genere | Alt: 40-60% menys variabilitat | **P1** |
| **Persona-audience** | Abstracte ("nouvingut amb A1") | Narrativa concreta ("alumne de 14 anys que...") | Mitja | **P1** |
| **Scaffolding decreixent** | Definicio identica totes les aparicions | 1a=completa, 2a=breu, 3a=sol | Mitja | **P1** |
| **Desnominalitzacio** | No existeix | Convertir noms abstractes en verbs | Mitja | **P1** |
| **Pre-training (glossari previ)** | No existeix | Mini-glossari ABANS del text per A1/A2 | Mitja | **P1** |
| **Principi coherencia (Mayer)** | Implicit ("no invents contingut") | Explicit: "NO afegeixis res no original" | Baixa (parcialment cobert) | **P1** |
| **To per nivell** | Generic | pre-A1/A2=conversacional, B1=proper, B2=academic | Baixa | **P1** |
| **Pipeline 2 passos** | Tot en 1 crida | Pas 1: text adaptat / Pas 2: complements | Mitja-alt | **P2** |
| **Post-processament codi** | clean_gemini_output() (format) | + verificar longitud frase, paraules prohibides, estructura | Alt | **P2** |
| **Thinking adaptatiu** | thinking_budget=0 sempre | Activar per perfils complexos (2e, pre-A1, multi-comorbiditat) | Baixa | **P2** |
| **Verificacio 2n prompt** | No existeix | Segon prompt amb rubrica que revisa la sortida | Mitja | **P3** |
| **Routing de models** | Gemini Flash sempre | Model simple per adaptacions basiques, model potent per complexes | Mitja | **P3** |
| **Pictogrames reals** | Emojis Unicode | ARASAAC API | Alt (impacte alumnat) | **P3** |
| **Metriques llegibilitat** | No existeix | Verificador post-generacio (longitud frase, freq lexica) | Mitja | **P3** |
| **Disclaimer traduccions** | No existeix | Avis visible per glossaris bilingues en llengues poc suportades | Baixa | **P1** |

---

## 6. Arquitectura de prompt v2 -- Proposta

### 6.1 Estructura en 4 capes

```
CAPA 1: IDENTITAT (fixa, ~100 tokens)
  Rol, objectiu, restriccions absolutes

CAPA 2: INSTRUCCIONS UNIVERSALS (fixa, ~200 tokens)
  12-15 regles que SEMPRE s'apliquen

CAPA 3: INSTRUCCIONS CONDICIONALS (variable, ~200-400 tokens)
  Seleccionades per codi segun perfil + MECR + genere

CAPA 4: CONTEXT (variable, ~500-1500 tokens)
  Persona-audience + RAG + text original
```

### 6.2 Capa 1 -- Identitat (FIXA, sempre s'envia)

```
Ets l'assistent ATNE (Adaptador de Textos a Necessitats Educatives) de Jesuites Educacio.

OBJECTIU: Transformar textos educatius perque siguin accessibles a l'alumnat
descrit, seguint principis de DUA, Lectura Facil i MECR.

RESTRICCIONS ABSOLUTES:
- Comenca DIRECTAMENT amb "## Text adaptat". ZERO meta-text.
- Escriu en catala (o la llengua vehicular indicada).
- Mantingues el rigor curricular: MAI substitueixis un terme tecnic
  per un de colloquial ("cosa", "allo", "el que fa que" = PROHIBITS).
- ADAPTA, no CREES: cada element del text adaptat ha de tenir
  correspondencia amb l'original (principi de coherencia de Mayer).
```

### 6.3 Capa 2 -- Instruccions universals (FIXA, sempre s'envia)

Aquestes 15 instruccions s'envien SEMPRE perque son aplicables a qualsevol adaptacio:

```
REGLES UNIVERSALS D'ADAPTACIO:

LEXIC:
1. Usa vocabulari frequent. Termes tecnics en **negreta** amb definicio.
2. Un terme = un concepte. No variis per elegancia (no sinonims).
3. Referents pronominals explicits: si ambigu, repeteix el nom.
4. Elimina expressions idiomatiques i sentit figurat.

SINTAXI:
5. Una idea per frase. Veu activa. Subjecte explicit.
6. Puntuacio simple: punts i dos punts. Evita punt i coma.
7. Ordre canonic: Subjecte + Verb + Complement.

ESTRUCTURA:
8. Paragrafs curts (3-5 frases max). Un tema per paragraf.
9. Titols descriptius en format pregunta quan sigui possible.
10. Frase topic al principi de cada paragraf.

COHESIO (Halliday):
11. Connectors explicits entre frases (per tant, a mes, en canvi).
12. Desnominalitza: noms abstractes → verbs ("l'evaporacio" → "quan s'evapora").
13. Transicions entre seccions ("Ja hem vist X. Ara veurem Y").

QUALITAT:
14. Scaffolding decreixent (Vygotsky): 1a aparicio=terme+definicio completa,
    2a=terme+definicio breu, 3a en endavant=terme sol.
15. AUTOCHECK: revisa que no hi aparegui cap paraula prohibida.
```

### 6.4 Capa 3 -- Instruccions condicionals (VARIABLE, seleccionades per codi)

El codi `build_system_prompt()` selecciona NOMES els blocs rellevants:

#### 6.4.1 Bloc MECR (enviar NOMES el nivell de sortida)

```python
MECR_BLOCKS = {
    "pre-A1": """
NIVELL MECR DE SORTIDA: pre-A1 (Alfabetitzacio)
- Frases de 3-5 paraules maxim
- Vocabulari quotidiana basic (menjar, casa, escola)
- Verbs en present, formes regulars
- Cada idea amb suport visual (emoji/pictograma)
- To: molt conversacional i directe ("Mira! Les plantes...")
""",
    "A1": """
NIVELL MECR DE SORTIDA: A1 (Acces)
- Frases de 5-8 paraules maxim
- Vocabulari quotidiana i escolar basic
- Present indicatiu, frases SVO simples
- Max 3-4 termes tecnics, amb definicio molt curta
- To: conversacional i directe ("Ara aprendras...")
- GLOSSARI PREVI: comenca amb "## Paraules clau" (3-5 termes)
""",
    # ... A2, B1, B2
}
```

#### 6.4.2 Bloc per genere discursiu (detectat pel codi o indicat pel docent)

```python
GENRE_BLOCKS = {
    "explicacio": """
GENERE DISCURSIU: Explicacio
- Progressio del simple al complex
- Causa → efecte explicita
- Desnominalitza processos
- Estructura: que es → com funciona → per que importa
""",
    "narracio": """
GENERE DISCURSIU: Narracio
- Mante personatges principals, simplifica secundaris
- Explicita motivacions i emocions
- Cronologia lineal (evitar flashbacks)
- Estructura: qui → que passa → per que → com acaba
""",
    "instruccio": """
GENERE DISCURSIU: Instruccio
- Numera els passos
- Un verb d'accio per pas, subjecte "tu" explicit
- Ordre cronologic estricte
- Estructura: que necessites → passos → resultat esperat
""",
    "argumentacio": """
GENERE DISCURSIU: Argumentacio
- Tesi al primer paragraf
- Cada argument numerat amb evidencia
- Conclusio explicita
- Estructura: que defensa → arguments → conclusio
""",
}
```

#### 6.4.3 Blocs per perfil (enviar NOMES els que s'apliquen)

```python
PROFILE_BLOCKS = {
    "nouvingut": """
PERFIL: Nouvingut
- Referents culturals: substitueix locals per universals o explica
- Glossari bilingue amb traduccio a L1
- Suport visual: imatges, esquemes (la comprensio visual no depen de L2)
- Redundancia modal: text + imatge + esquema
""",
    "tea": """
PERFIL: TEA
- Estructura predictible: sempre mateixa sequencia (titol→definicio→exemple→activitat)
- Zero implicitura: tota metafora, ironia, sentit figurat → literal
- Vocabulari univoc: evitar polisemia, definir de forma univoca
- Anticipacio: avisar canvis de tema o format
""",
    "tdah": """
PERFIL: TDAH
- Micro-blocs de 3-5 frases amb objectiu explicit per bloc
- Senyalitzacio visual intensa: negretes, requadres, icones
- Variacio: alternar lectura, esquema, pregunta
- Indicadors de progres: [Seccio 2 de 4]
""",
    "dislexia": """
PERFIL: Dislexia (Dehaene/Wolf)
- Evita paraules compostes llargues: divideix o reformula
- Prefereix paraules d'alta frequencia lexica
- Repeteix termes clau en lloc d'usar sinonims
- Frases 2-3 paraules mes curtes que el maxim MECR
- Evita encadenar prefixos i sufixos
""",
    "tdl": """
PERFIL: TDL
- Reduccio maxima de densitat lexica
- Cada terme tecnic apareix en 2-3 contextos diferents (modelatge)
- Zero subordinades i pronoms febles (li, els, en, hi)
- Definicions integrades just al costat del terme (no al final)
""",
    "di": """
PERFIL: Discapacitat Intellectural
- UN sol concepte nou per bloc
- Concreccio radical: cada concepte abstracte → exemple tangible
- Repeticio sistematica en formats diversos
- Generalitzacio guiada: connectar amb vida quotidiana
""",
    "altes_capacitats": """
PERFIL: Altes Capacitats
- NO simplifiquis: mante complexitat linguistica i conceptual
- Afegeix profunditat: excepcions, fronteres del coneixement, debats oberts
- Connexions interdisciplinars
- Preguntes de pensament critic (analitzar, avaluar, crear)
""",
    "2e": """
PERFIL: Doble Excepcionalitat (2e)
- EQUILIBRI: mante repte cognitiu ALT amb suports d'accessibilitat
- Mai sacrificar enriquiment per accessibilitat ni a l'inreves
- Adapta el FORMAT (visual, oral, segmentat) pero no el CONTINGUT intel·lectual
""",
}
```

#### 6.4.4 Blocs de creuament (enviar NOMES si 2+ perfils actius)

```python
CROSSING_BLOCKS = {
    ("nouvingut", "dislexia"): "Nouvingut+Dislexia: densitat visual baixa + suport no-textual + simplificacio linguistica simultanea.",
    ("nouvingut", "escolaritzacio_parcial"): "Nouvingut+Esc.parcial: NO pressuposar familiaritat amb generes escolars. Explicita que s'espera.",
    ("tea", "narracio"): "TEA+Narracio: explicitar TOTES les inferencies. Zero implicitura.",
    ("di", "abstracte"): "DI+Abstracte: concretar amb exemples quotidians. 1 concepte per bloc.",
    ("tdah", "text_llarg"): "TDAH+Text llarg: micro-blocs, objectiu per bloc, progres visual.",
    ("tdl", "vocabulari"): "TDL+Vocabulari dens: reduir densitat lexica, repetir, modelar us.",
    # ...
}
```

### 6.5 Capa 4 -- Context (VARIABLE)

```
PERSONA-AUDIENCE:
Escrius per a [narrativa generada pel codi a partir del perfil]:
"Un alumne de 14 anys que va arribar del Marroc fa 3 mesos.
Enten catala oral basic pero llegeix amb dificultat.
Ha estat escolaritzat regularment al seu pais.
Nivell MECR: A1. Barrera nuclear: lexica i cultural."

CONEIXEMENT PEDAGOGIC (RAG):
[Context recuperat del corpus FJE, truncat a 800-1000 chars per doc obligatori]

TEXT ORIGINAL A ADAPTAR:
[Text complet del docent]
```

### 6.6 Resolucio del conflicte DUA - MECR - LF

Quan DUA, MECR i LF entren en conflicte, la jerarquia de resolucio es:

```
1. MECR (PRIORITAT MAXIMA): El nivell linguistic de sortida es el limit dur.
   Si el MECR diu "max 8 paraules per frase" (A1), cap altra regla ho pot superar.

2. DUA (SEGON): El nivell DUA (Acces/Core/Enriquiment) determina la INTENSITAT
   de l'adaptacio dins dels limits del MECR.
   - Acces = LF extrema dins del MECR indicat
   - Core = Llenguatge Clar (ISO 24495) dins del MECR indicat
   - Enriquiment = maxima complexitat permesa pel MECR

3. LF (TERCER): Les regles de Lectura Facil s'apliquen com a INTENSIFICADOR
   del nivell DUA Acces, no com a sistema independent.
   - DUA Acces + LF alta = maxima simplificacio (dins MECR)
   - DUA Core + LF baixa = llenguatge clar estandard (dins MECR)

REGLA DE CONFLICTE CONCRETA:
Si una definicio parentetica fa superar el maxim de paraules MECR:
→ Per A1/pre-A1: treure el parentesi, posar la definicio com a frase independent
→ Per A2/B1: permetre excepcio de +3 paraules si conte definicio
→ Per B2: no hi ha conflicte (limits amplis)
```

### 6.7 Few-shot examples

Cal incloure 1 mini-exemple (~100 tokens) per combinacio MECR + genere mes frequent. Minims:

| Nivell MECR | Genere | Exemple a incloure |
|---|---|---|
| A1 | Explicacio | Text de ciencies naturals, 3-4 frases adaptades |
| A2 | Explicacio | Text de ciencies socials, 5-6 frases adaptades |
| B1 | Argumentacio | Text d'humanitats, 1 paragraf adaptat |
| B2 | Qualsevol | Adaptacio minima (clarificar i estructurar) |

Format suggerit:

```
EXEMPLE NIVELL A1 (explicacio):
Original: "La fotosintesi es el proces bioquimic pel qual els organismes
  fotosinteics converteixen l'energia lluminosa en energia quimica."
Adaptat:
## Paraules clau
- **Fotosintesi**: les plantes fan menjar amb llum.
## Text adaptat
Les plantes fan el seu menjar.
Les plantes utilitzen la llum del sol.
Aquest proces es diu **fotosintesi**.
```

### 6.8 Pipeline en 2 passos (Fase 2)

Quan implementar-lo:
- **Pas 1** (sempre): Prompt d'adaptacio (~10 instruccions) → genera NOMES el text adaptat
- **Pas 2** (si hi ha complements activats): Prompt de complements (rep el text adaptat com a input) → genera glossari, preguntes, bastides, esquema

Avantatges:
- Cada prompt te menys instruccions → millor seguiment
- El text adaptat es estable; els complements s'hi basen
- Es pot usar un model diferent per cada pas (Flash per pas 2, Pro per pas 1)

### 6.9 Recomanacio de model per escenari

| Escenari | Model recomanat | Motiu |
|---|---|---|
| Prototip/demo (ara) | Gemini 2.5 Flash | Gratuit, suficient per demo |
| Produccio FJE (desplegament) | Claude Sonnet 4 o Gemini 2.5 Pro | Millor adherencia a instruccions, menys meta-text |
| Perfils complexos (pre-A1, 2e, multi-comorbiditat) | Claude Opus 4 o GPT-4.1 | Maxima qualitat, thinking adaptatiu |
| Us massiu (centenars/dia) | Routing: GPT-4.1-mini (B1/B2 simples) + Claude Sonnet (A1/A2 complexos) | Equilibri cost-qualitat |
| Millor catala possible | Claude Opus 4 | Superior en registre normatiu catala |

---

## 7. Cataleg consolidat d'instruccions

Fusio dels dos bancs (119 instruccions del Banc Exhaustiu + 70 variables de la Taxonomia A1) en un cataleg desduplicat.

### Llegenda

- **Executor**: LLM = l'LLM ho fa al prompt | CODI = el backend Python ho fa | FE = CSS/frontend ho fa
- **Activacio**: SEMPRE = tota adaptacio | PERFIL = segons perfil alumne | NIVELL = segons MECR | COMPLEMENT = si s'activa el complement
- **Prioritat**: P0 = ja implementat | P1 = fer immediatament | P2 = fase seguent | P3 = futur

### A. Adaptacio linguistica

| ID | Instruccio | Executor | Activacio | Prioritat |
|---|---|---|---|---|
| A-01 | Substitucio per vocabulari frequent (TXT_LEX_FREQ) | LLM | SEMPRE | P0 |
| A-02 | Termes tecnics en negreta amb definicio (TXT_TERM_DENS) | LLM | SEMPRE | P0 |
| A-03 | Repeticio lexica coherent, no sinonims (TXT_TERM_CONS) | LLM | SEMPRE | P0 |
| A-04 | Referents pronominals explicits (TXT_REF_CLEAR) | LLM | SEMPRE | P0 |
| A-05 | Eliminar expressions idiomatiques (TXT_IDIOM) | LLM | SEMPRE | P0 |
| A-06 | Eliminar polisemia (TXT_POLYSEMY) | LLM | SEMPRE | P0 |
| A-07 | Una idea per frase (TXT_SENT_COMPLEX) | LLM | SEMPRE | P0 |
| A-08 | Veu activa obligatoria | LLM | SEMPRE | P0 |
| A-09 | Subjecte explicit a cada frase | LLM | SEMPRE | P0 |
| A-10 | Ordre canonic SVO | LLM | SEMPRE | P0 |
| A-11 | Puntuacio simplificada (punts i dos punts) | LLM | SEMPRE | P0 |
| A-12 | Limitacio longitud de frase (per MECR) (TXT_SENT_LEN) | LLM | NIVELL | P0 |
| A-13 | Eliminacio/reduccio de subordinades | LLM | NIVELL | P0 |
| A-14 | Connectors explicits (TXT_CONNECT) | LLM | SEMPRE | P0 |
| A-15 | Scaffolding decreixent de definicions (Vygotsky) | LLM | SEMPRE | **P1** |
| A-16 | Desnominalitzacio (Halliday) | LLM | SEMPRE | **P1** |
| A-17 | Evitar negacions multiples | LLM | SEMPRE | P0 |
| A-18 | Dates i xifres en format complet | LLM | SEMPRE | P0 |
| A-19 | Sigles i abreviatures explicades (TXT_ACRONYM) | LLM | SEMPRE | P0 |
| A-20 | Control densitat lexica | LLM | NIVELL | **P1** |
| A-21 | Descomposicio paraules compostes | LLM | PERFIL (dislexia, nouvingut) | **P1** |
| A-22 | Concreccio de quantificadors (TXT_ABSTRACT) | LLM | NIVELL (A1/A2) | P2 |
| A-23 | Evitar cultismes i llatinismes | LLM | NIVELL (pre-A1-A2) | P2 |
| A-24 | Present d'indicatiu preferent | LLM | NIVELL (pre-A1-A2) | P0 |
| A-25 | Formes verbals simples | LLM | NIVELL (pre-A1-A2) | P0 |
| A-26 | Evitar incisos parentetics llargs | LLM | NIVELL (pre-A1-B1) | P0 |

### B. Estructura i organitzacio

| ID | Instruccio | Executor | Activacio | Prioritat |
|---|---|---|---|---|
| B-01 | Paragrafs curts (3-5 frases) (MACRO_PARA) | LLM | SEMPRE | P0 |
| B-02 | Blocs tematics amb titol descriptiu (MACRO_HEAD) | LLM | SEMPRE | P0 |
| B-03 | Frase topic al principi de cada paragraf | LLM | SEMPRE | P0 |
| B-04 | Llistes en lloc d'enumeracions (MACRO_LIST) | LLM | SEMPRE | P0 |
| B-05 | Estructura deductiva (general → particular) | LLM | SEMPRE | P0 |
| B-06 | Ordre cronologic per a processos (MACRO_STEP) | LLM | SEMPRE | P0 |
| B-07 | Resum anticipatiu (advance organizer) (MACRO_SUM_PRE) | LLM | NIVELL (pre-A1-A2) | **P1** |
| B-08 | Resum final recapitulatiu (MACRO_SUM_POST) | LLM | NIVELL (pre-A1-B1) | **P1** |
| B-09 | Numeracio de passos i sequencies | LLM | SEMPRE | P0 |
| B-10 | Transicions entre seccions | LLM | SEMPRE | **P1** |
| B-11 | Salt de linia entre idees | LLM | SEMPRE | P0 |
| B-12 | Senyalitzacio nucli vs complement (MACRO_SIGNAL) | LLM | COMPLEMENT | P2 |
| B-13 | Indicadors de progres [Seccio X de Y] | LLM | PERFIL (TDAH) | P2 |
| B-14 | Taules per informacio comparativa | LLM | SEMPRE | P0 |

### C. Suport cognitiu

| ID | Instruccio | Executor | Activacio | Prioritat |
|---|---|---|---|---|
| C-01 | Limit de conceptes nous per bloc (SEM_CONCEPT_LOAD) | LLM | NIVELL | P0 |
| C-02 | Reforc immediat de cada concepte nou | LLM | NIVELL | P0 |
| C-03 | Eliminacio redundancia decorativa (Mayer) | LLM | SEMPRE | **P1** |
| C-04 | Chunking (agrupacio 3-5 elements) (TASK_MEM) | LLM | SEMPRE | P0 |
| C-05 | Glossari previ (pre-training Sweller) | LLM | NIVELL (pre-A1-A2) | **P1** |
| C-06 | Analogies amb experiencies quotidianes (SEM_BACKGROUND) | LLM | NIVELL | P0 |
| C-07 | Connexio amb aprenentatges anteriors | LLM | COMPLEMENT | P2 |
| C-08 | Anticipacio de vocabulari | LLM | NIVELL (pre-A1-A2) | **P1** |
| C-09 | Espaiament de la dificultat (TASK_COG_LOAD) | LLM | NIVELL | P2 |

### D. Multimodalitat

| ID | Instruccio | Executor | Activacio | Prioritat |
|---|---|---|---|---|
| D-01 | Emojis de suport per conceptes clau | LLM | COMPLEMENT | P0 |
| D-02 | Esquema de proces (flowchart textual) | LLM | COMPLEMENT | P0 |
| D-03 | Mapa conceptual jerarquic | LLM | COMPLEMENT | P0 |
| D-04 | Taula comparativa | LLM | COMPLEMENT | P0 |
| D-05 | Linia del temps textual | LLM | COMPLEMENT | P0 |
| D-06 | Text preparat per lectura en veu alta | LLM | PERFIL (dislexia, DI, disc_visual) | P2 |
| D-07 | Indicacions de tipus d'imatge (pictograma vs diagrama) (MOD_IMG_REL) | LLM | PERFIL | P2 |
| D-08 | Pictogrames reals (ARASAAC) | CODI+FE | COMPLEMENT | P3 |
| D-09 | Audio TTS | CODI+FE | COMPLEMENT | P3 |

### E. Contingut curricular

| ID | Instruccio | Executor | Activacio | Prioritat |
|---|---|---|---|---|
| E-01 | Nucli terminologic intocable | LLM | SEMPRE | P0 |
| E-02 | Graduacio definicio tecnica per MECR | LLM | NIVELL | P0 |
| E-03 | Glossari final complet | LLM | COMPLEMENT | P0 |
| E-04 | Glossari bilingue (L1-L2) | LLM | PERFIL (nouvingut) | P0 |
| E-05 | Manteniment exactitud cientifica | LLM | SEMPRE | P0 |
| E-06 | Simplificacio processos mantenint causalitat (SEM_CAUSE) | LLM | SEMPRE | P0 |
| E-07 | Exemple concret per concepte abstracte | LLM | NIVELL | P0 |
| E-08 | Referents culturalment diversos (SEM_CULT) | LLM | PERFIL (nouvingut) | P0 |
| E-09 | Evitar suposits culturals implicits | LLM | PERFIL (nouvingut) | P0 |
| E-10 | Sensibilitat a temes traumatics (SEM_EMO) | LLM | PERFIL (trauma, vulnerabilitat) | P0 |
| E-11 | Pistes etimologiques translingues | LLM | PERFIL (nouvingut, L1 romanica) | P2 |
| E-12 | Contra-exemples per delimitar conceptes | LLM | NIVELL (B1-B2) | P2 |

### F. Avaluacio i comprensio

| ID | Instruccio | Executor | Activacio | Prioritat |
|---|---|---|---|---|
| F-01 | Preguntes de reconeixement (literal) | LLM | COMPLEMENT | P0 |
| F-02 | Preguntes V/F | LLM | COMPLEMENT | P0 |
| F-03 | Preguntes d'inferencia | LLM | COMPLEMENT | P0 |
| F-04 | Preguntes de transferencia | LLM | COMPLEMENT | P0 |
| F-05 | Gradacio format resposta (seleccio→oberta) | LLM | COMPLEMENT | P0 |
| F-06 | Preguntes comprensio intercalades (C4.01) | LLM | PERFIL (TDAH) | P2 |
| F-07 | Objectius d'aprenentatge explicits | LLM | COMPLEMENT | **P1** |
| F-08 | Activitats d'aprofundiment | LLM | COMPLEMENT | P0 |
| F-09 | Pensament critic (per que? i si...?) | LLM | PERFIL (altes_cap) | P0 |
| F-10 | Connexions interdisciplinars | LLM | PERFIL (altes_cap) | P0 |

### G. Personalitzacio linguistica

| ID | Instruccio | Executor | Activacio | Prioritat |
|---|---|---|---|---|
| G-01 | Glossari bilingue complet | LLM | PERFIL (nouvingut) | P0 |
| G-02 | Traduccio parcial de consignes | LLM | PERFIL (nouvingut, pre-A1/A1) | P2 |
| G-03 | Transliteracio fonetica | LLM | PERFIL (nouvingut, alfabet no llati) | P2 |
| G-04 | Disclaimer traduccions L1 no fiables | CODI+FE | PERFIL (nouvingut, L1 poc suportada) | **P1** |
| G-05 | Substitucio referents culturals | LLM | PERFIL (nouvingut) | P0 |
| G-06 | To per nivell MECR (Mayer) | LLM | NIVELL | **P1** |

### H. Adaptacions especifiques per perfil

| ID | Instruccio | Executor | Activacio | Prioritat |
|---|---|---|---|---|
| H-01 | TEA: estructura predictible i fixa | LLM | PERFIL | P0 |
| H-02 | TEA: zero implicitura | LLM | PERFIL | P0 |
| H-03 | TEA: anticipacio canvis i transicions | LLM | PERFIL | P0 |
| H-04 | TDAH: micro-blocs amb objectiu | LLM | PERFIL | P0 |
| H-05 | TDAH: retroalimentacio visual progres | LLM | PERFIL | P2 |
| H-06 | TDAH: variacio activitat dins text | LLM | PERFIL | P2 |
| H-07 | Dislexia: evitar compostos llargs (Dehaene) | LLM | PERFIL | **P1** |
| H-08 | Dislexia: alta frequencia, no sinonims | LLM | PERFIL | **P1** |
| H-09 | DI: 1 concepte per bloc | LLM | PERFIL | P0 |
| H-10 | DI: concreccio radical | LLM | PERFIL | P0 |
| H-11 | DI: repeticio sistematica | LLM | PERFIL | P0 |
| H-12 | AC: profunditzacio conceptual | LLM | PERFIL | P0 |
| H-13 | AC: connexions interdisciplinars | LLM | PERFIL | P0 |
| H-14 | AC: manteniment complexitat linguistica | LLM | PERFIL | P0 |
| H-15 | 2e: equilibri repte/accessibilitat | LLM | PERFIL (2e) | P0 |
| H-16 | TDL: reduccio densitat lexica | LLM | PERFIL | P0 |
| H-17 | TDL: modelatge us en context | LLM | PERFIL | **P1** |
| H-18 | Disc.visual: alt-text per imatges | CODI+FE | PERFIL | P2 |
| H-19 | Disc.visual: estructura semantica (H1-H3) | LLM | PERFIL | P0 |
| H-20 | Disc.auditiva: simplificacio com L2 | LLM | PERFIL | P0 |

### I. Presentacio i layout

| ID | Instruccio | Executor | Activacio | Prioritat |
|---|---|---|---|---|
| I-01 | Tipografia sans-serif, mida 14pt (LAY_FONT_SIZE) | FE | PERFIL (dislexia) | P3 |
| I-02 | Interlineat 1.5 (LAY_SPACING) | FE | PERFIL (dislexia) | P3 |
| I-03 | Columna estreta 60-70 chars (LAY_LINE_LEN) | FE | PERFIL (dislexia) | P3 |
| I-04 | Fons suau (crema/blau clar) (LAY_CONTRAST) | FE | PERFIL (dislexia) | P3 |
| I-05 | Text alineat esquerra (no justificat) | FE | PERFIL (dislexia) | P3 |
| I-06 | Contrast alt negre/blanc (LAY_CONTRAST) | FE | PERFIL (disc_visual) | P3 |
| I-07 | Document digital navegable per teclat (ACC_KEYB) | FE | PERFIL (disc_motora) | P3 |
| I-08 | Reescalat i zoom (ACC_RESIZE) | FE | PERFIL (disc_visual) | P3 |

### J. Verificacio i post-processament

| ID | Instruccio | Executor | Activacio | Prioritat |
|---|---|---|---|---|
| J-01 | Verificar longitud de frases (max per MECR) | CODI | SEMPRE | **P1** |
| J-02 | Detectar paraules prohibides (regex) | CODI | SEMPRE | **P1** |
| J-03 | Verificar presencia d'encapcalaments | CODI | SEMPRE | P2 |
| J-04 | Verificar presencia de termes en negreta | CODI | SEMPRE | P2 |
| J-05 | Metriques de llegibilitat basiques | CODI | SEMPRE | P3 |
| J-06 | Segon prompt de verificacio amb rubrica | LLM | PERFIL (complex) | P3 |
| J-07 | Comptar conceptes nous per paragraf | CODI | SEMPRE | P3 |

**Resum del cataleg**:
- Total instruccions: 95
- Per LLM: 72
- Per CODI: 12
- Per FE (CSS/frontend): 11
- Ja implementades (P0): 52
- A implementar ja (P1): 22
- Fase seguent (P2): 14
- Futur (P3): 17

---

## 8. Mapa perfil → instruccions

Per a cada un dels 13 perfils principals: quines instruccions del cataleg s'activen, en quin ordre de prioritat.

### 8.1 Nouvingut

| Prioritat | Instruccions activades | Justificacio (barrera nuclear) |
|---|---|---|
| **1a (lexica)** | A-01, A-02, A-04, A-05, A-06, A-20, A-21 | Barrera nuclear: comprensio lexica (2-4) |
| **2a (cultural)** | E-08, E-09, E-10, G-01, G-05 | Barrera cultural (3-4) |
| **3a (sintactica)** | A-07, A-09, A-12, A-13, A-24, A-25 | Barrera sintactica (2-4) |
| **4a (estructura)** | B-01, B-02, B-07, C-05, C-08 | Suport discursiu (glossari previ) |

### 8.2 TEA

| Prioritat | Instruccions activades | Justificacio |
|---|---|---|
| **1a (inferencia)** | H-01, H-02, A-05, A-06 | Barrera nuclear: inferencia (3-4) |
| **2a (estructura)** | H-03, B-02, B-06, B-09 | Predictibilitat necessaria |
| **3a (lexica)** | A-03, A-04 | Polisemia i ambiguitat |
| **4a (discursiva)** | B-03, B-10 | Coherencia central feble |

### 8.3 TDAH

| Prioritat | Instruccions activades | Justificacio |
|---|---|---|
| **1a (atencio)** | H-04, B-13, H-06 | Barrera nuclear: atencio (3-4) |
| **2a (memoria treball)** | C-04, C-01, B-01 | Barrera memoria treball (2-4) |
| **3a (motivacio)** | H-05, F-06 | Feedback i variacio per mantenir motivacio |

### 8.4 Dislexia

| Prioritat | Instruccions activades | Justificacio |
|---|---|---|
| **1a (decodificacio)** | H-07, H-08, A-21 | Barrera nuclear: decodificacio (3-4) |
| **2a (fatiga)** | I-01, I-02, I-03, I-04, I-05 | Reduir fatiga visual (CSS/FE) |
| **3a (compensacio)** | D-06, A-03 | Canal oral com a complement |

### 8.5 TDL

| Prioritat | Instruccions activades | Justificacio |
|---|---|---|
| **1a (lexica)** | H-16, A-01, A-02, A-20 | Barrera nuclear: comprensio lexica (2-4) |
| **2a (sintactica)** | H-17, A-07, A-13, A-26 | Barrera nuclear: comprensio sintactica (2-4) |
| **3a (memoria)** | C-04, C-05 | Memoria fonologica compromesa |

### 8.6 Discapacitat intellectual

| Prioritat | Instruccions activades | Justificacio |
|---|---|---|
| **1a (discursiva)** | H-09, H-10, H-11 | Barrera nuclear: comprensio discursiva (3-4) |
| **2a (inferencia)** | C-01, C-06 | Barrera inferencia (3-4) |
| **3a (lexica)** | A-01, A-12, A-22 | Vocabulari limitat |
| **4a (visual)** | D-01, D-08 | Suport pictografic intens |

### 8.7 Discapacitat visual

| Prioritat | Instruccions activades | Justificacio |
|---|---|---|
| **1a (percepcio)** | H-18, H-19, I-06, I-08 | Barrera nuclear: percepcio (2-4) |
| **2a (estructura)** | B-02, B-14 | Navegacio amb lector de pantalla |

Nota: Gairebe totes les adaptacions son CSS/FE, no LLM.

### 8.8 Discapacitat auditiva

| Prioritat | Instruccions activades | Justificacio |
|---|---|---|
| **1a (lexica/sintactica)** | H-20, A-01, A-07, A-12, A-13 | Barrera lexica i sintactica (2-4) en sordesa prelocutiva |
| **2a (visual)** | D-01, D-02 | Suport visual com a compensacio |

Nota: Tractar com L2 en sordesa prelocutiva signant.

### 8.9 Discapacitat motora

| Prioritat | Instruccions activades | Justificacio |
|---|---|---|
| **1a (acces)** | I-07 | Navegacio per teclat/commutador |

Nota: Gairebe totes les adaptacions son CSS/FE. L'LLM nomes ha de garantir estructura semantica.

### 8.10 TDC / Dispraxia

| Prioritat | Instruccions activades | Justificacio |
|---|---|---|
| **1a (acces)** | I-07 | Resposta alternativa (no escriptura manual) |

Nota: Similar a disc. motora. L'adaptacio es principalment de frontend.

### 8.11 Altes Capacitats

| Prioritat | Instruccions activades | Justificacio |
|---|---|---|
| **1a (motivacio)** | H-12, H-13, H-14 | Barrera nuclear: avorriment/motivacio (1-3) |
| **2a (repte)** | F-09, F-10 | Pensament critic i connexions |

Nota: NO simplificar. Enriquir.

### 8.12 Vulnerabilitat socioeducativa

| Prioritat | Instruccions activades | Justificacio |
|---|---|---|
| **1a (motivacio)** | E-10, A-01 | Barrera nuclear: motivacio (2-4) |
| **2a (cultural)** | E-08, E-09 | Capital cultural limitat (1-3) |
| **3a (estructura)** | B-01, B-02, C-06 | Compensar manca familiaritat amb generes academics |

### 8.13 Trastorn emocional/conductual

| Prioritat | Instruccions activades | Justificacio |
|---|---|---|
| **1a (emocional)** | E-10 | Barrera nuclear: motivacio/emocional (3-4) |
| **2a (atencio)** | H-04, B-01 | Barrera atencio (2-4) per ansietat/hipervigilancia |
| **3a (seguretat)** | B-07 | Anticipacio, predictibilitat, estructura |

---

## 9. Pla d'implementacio

### Fase 0: Quick wins (canvis al prompt actual sense tocar arquitectura)

**Temps estimat**: 2-4 hores
**Impacte**: Alt

| # | Canvi | Que fer concretament | Fitxer |
|---|---|---|---|
| 0.1 | Enviar NOMES 1 nivell MECR | A `build_system_prompt()`, substituir els 5 blocs MECR per un `if/elif` que envii nomes el nivell de `params['mecr_sortida']` | server.py L428-471 |
| 0.2 | Condicionar regles de creuament | Enviar nomes les regles de creuament que s'apliquen als perfils actius del `profile` | server.py L473-481 |
| 0.3 | Afegir scaffolding decreixent | Afegir al BASE_SYSTEM_PROMPT la instruccio de Vygotsky: "1a aparicio=definicio completa, 2a=breu, 3a=sol" | server.py L406 |
| 0.4 | Afegir principi coherencia Mayer | Canviar "No invents contingut" per "NO afegeixis informacio, exemples, dades o curiositats que no estiguin al text original. ADAPTA, no AMPLIA." | server.py L402 |
| 0.5 | Afegir desnominalitzacio Halliday | Afegir regla: "Desnominalitza: converteix noms abstractes en verbs ('l'evaporacio' → 'quan s'evapora')" | server.py L406 |
| 0.6 | Afegir to per nivell | Afegir al bloc MECR: pre-A1/A2=conversacional, B1=proper, B2=academic | server.py L432-471 |
| 0.7 | Disclaimer traduccions L1 | Afegir al frontend un avis per glossaris bilingues: "Traduccions orientatives. Valideu amb parlant natiu." | ui/app.js |

**Resultat esperat**: Reduccio ~40% del soroll al prompt, millor seguiment d'instruccions.

### Fase 1: Reestructuracio del prompt (condicionalitat, few-shot, persona-audience)

**Temps estimat**: 1-2 setmanes
**Impacte**: Molt alt

| # | Canvi | Que fer | Fitxer |
|---|---|---|---|
| 1.1 | Reestructurar en 4 capes | Reescriure `build_system_prompt()` per montar el prompt amb les 4 capes descrites a la seccio 6 | server.py |
| 1.2 | Blocs condicionals per perfil | Crear diccionari `PROFILE_BLOCKS` amb instruccions especifiques per perfil | server.py (o fitxer separat prompt_blocks.py) |
| 1.3 | Blocs per genere discursiu | Afegir deteccio de genere (via LLM ratic o heuristica simple) + blocs condicionals | server.py |
| 1.4 | Few-shot examples | Crear 4 mini-exemples (A1+explicacio, A2+explicacio, B1+argumentacio, B2+qualsevol) de ~100 tokens cadascun | prompt_blocks.py |
| 1.5 | Persona-audience | A `build_system_prompt()`, generar narrativa de l'alumne a partir del perfil: edat, origen, L1, mesos a Catalunya, escolaritzacio | server.py |
| 1.6 | Glossari previ per A1/A2 | Afegir instruccio "Comenca amb ## Paraules clau" quan MECR es pre-A1, A1 o A2 | prompt_blocks.py |
| 1.7 | Post-processament basic | Afegir funcions Python: verificar longitud frases, detectar paraules prohibides, verificar estructura | server.py |
| 1.8 | Regles dislexia (Dehaene) | Afegir bloc condicional per dislexia amb les 5 regles de Dehaene/Wolf | prompt_blocks.py |
| 1.9 | Regles Halliday per genere | Afegir 4 blocs (explicacio, narracio, instruccio, argumentacio) | prompt_blocks.py |

**Resultat esperat**: Prompt 50% mes curt per adaptacio simple (B1 generic), 30% millor qualitat per perfils complexos.

### Fase 2: Pipeline en 2 passos + verificacio

**Temps estimat**: 2-4 setmanes
**Impacte**: Alt

| # | Canvi | Que fer |
|---|---|---|
| 2.1 | Pipeline 2 passos | Separar adaptacio (pas 1) i complements (pas 2). Pas 2 rep el text adaptat com a input |
| 2.2 | Thinking adaptatiu | Activar thinking_budget=2000-4000 per perfils complexos (2e, pre-A1, 2+ comorbiditats) |
| 2.3 | Post-processament avancat | Verificar metriques: longitud frase, densitat lexica, presencia termes tecnics, estructura encapcalaments |
| 2.4 | SRE (Graves) | Seccions opcionals "Abans de llegir" i "Despres de llegir" al frontend |
| 2.5 | Preguntes metacognitives | Opcio de preguntes intercalades al text (TDAH, DI) |
| 2.6 | Gradacio Bloom per DUA | Explicitar: Acces=Recordar/Comprendre, Core=Comprendre/Aplicar, Enriquiment=Analitzar/Avaluar/Crear |

### Fase 3: Model routing + metriques + pictogrames

**Temps estimat**: 1-3 mesos
**Impacte**: Mitja-alt

| # | Canvi | Que fer |
|---|---|---|
| 3.1 | Routing de models | Classificar adaptacio per complexitat. Model simple (Flash/mini) per B1/B2 generics, model potent (Sonnet/Pro) per A1/pre-A1 i perfils complexos |
| 3.2 | Segon prompt de verificacio | Prompt de revisio amb rubrica que rep text original + adaptat + perfil i avalua qualitat |
| 3.3 | Pictogrames ARASAAC | L'LLM genera etiquetes [PICTO:concepte], el codi les substitueix per imatges ARASAAC via API |
| 3.4 | Corpus frequencia catala | Integrar llistes de frequencia lexica per validar vocabulari post-generacio |
| 3.5 | TTS | Integrar Text-to-Speech per crear versio audio del text adaptat |
| 3.6 | CSS adaptatiu per dislexia | Tipografia OpenDyslexic, interlineat, fons, alineacio -- toggle al frontend |
| 3.7 | Metriques i dashboard | Recollir dades d'us, metriques de qualitat, feedback docent |

---

## 10. Actualitzacio 2026-03-30: Macrodirectives i connexio de sub-variables

Aquesta seccio documenta els canvis arquitectonics fets el 2026-03-30, que transformen el cataleg de 95 instruccions atomiques (seccio 7) en un sistema de macrodirectives compactes i connecten les sub-variables del perfil alumne amb les instruccions corresponents.

### 10.1 Macrodirectives implementades

Les 9 macrodirectives substitueixen les llistes atomiques d'instruccions com a unitat d'enviament a l'LLM. Cada macrodirectiva agrupa instruccions relacionades en un bloc coherent i autocontingut:

| Macrodirectiva | Abast | Instruccions que agrupa |
|---|---|---|
| **LEXIC** | Vocabulari, terminologia, referents | A-01 a A-06, A-19 a A-23 |
| **SINTAXI** | Frases, veu, ordre, puntuacio | A-07 a A-13, A-17, A-24 a A-26 |
| **ESTRUCTURA** | Paragrafs, titols, llistes, transicions | B-01 a B-14 |
| **COGNITIU** | Carrega cognitiva, scaffolding, glossari previ | C-01 a C-09 |
| **QUALITAT** | Coherencia Mayer, exactitud, autocheck | E-01, E-05, E-06, C-03 |
| **MULTIMODAL** | Emojis, esquemes, taules, TTS | D-01 a D-09 |
| **AVALUACIO** | Preguntes, activitats, pensament critic | F-01 a F-10 |
| **PERSONALITZACIO** | Glossari bilingue, referents culturals, to | G-01 a G-06, E-08 a E-11 |
| **PERFIL** | Bloc especific per perfil actiu (TEA, TDAH, dislexia, etc.) | H-01 a H-22 |

L'avantatge principal es que l'LLM rep blocs narratius amb coherencia interna, en lloc de llistes numerades d'instruccions desconnectades. Aixo millora el seguiment d'instruccions, especialment amb Gemini Flash.

### 10.2 Instruccions SEMPRE reduides de 24 a 12

De les 24 instruccions que tenien activacio SEMPRE al cataleg original (seccio 7), 12 es mantenen com a SEMPRE i 12 passen a activacio NIVELL (condicionals per MECR).

**12 instruccions que es mantenen SEMPRE:**

| ID | Instruccio |
|---|---|
| A-01 | Substitucio per vocabulari frequent |
| A-02 | Termes tecnics en negreta amb definicio |
| A-03 | Repeticio lexica coherent, no sinonims |
| A-04 | Referents pronominals explicits |
| A-05 | Eliminar expressions idiomatiques |
| A-07 | Una idea per frase |
| A-14 | Connectors explicits |
| A-18 | Dates i xifres en format complet |
| A-19 | Sigles i abreviatures explicades |
| B-01 | Paragrafs curts (3-5 frases) |
| B-02 | Blocs tematics amb titol descriptiu |
| B-03 | Frase topic al principi de cada paragraf |

**12 instruccions que passen a NIVELL (condicionals):**

| ID | Nova activacio | Motiu |
|---|---|---|
| A-06 | NIVELL (<=B1) | Eliminar polisemia nomes necessari per sota B2 |
| A-08 | NIVELL (<=B1) | Veu activa obligatoria es restrictiu per B2 |
| A-09 | NIVELL (<=B1) | Subjecte explicit a cada frase nomes cal per sota B2 |
| A-10 | NIVELL (<=B1) | Ordre canonic SVO innecessari per B2 |
| A-11 | NIVELL (<=B1) | Puntuacio simplificada innecessaria per B2 |
| A-17 | NIVELL (<=B1) | Evitar negacions multiples nomes crític per sota B2 |
| B-04 | NIVELL (<=B1) | Llistes en lloc d'enumeracions nomes per sota B2 |
| B-05 | NIVELL (<=B1) | Estructura deductiva nomes obligatoria per sota B2 |
| B-06 | NIVELL (<=B1) | Ordre cronologic per a processos nomes obligatori per sota B2 |
| B-09 | NIVELL (<=B1) | Numeracio de passos nomes obligatoria per sota B2 |
| B-11 | NIVELL (<=A2) | Salt de linia entre idees nomes obligatori per nivells baixos |
| B-14 | NIVELL (<=B1) | Taules per informacio comparativa nomes obligatories per sota B2 |

Aquesta reduccio fa que un cas B2 generic rebi 12 instruccions fixes (dins rang optim 7-12) en lloc de 24.

### 10.3 Cinc duplicats resolts

El cataleg original contenia redundancies que s'han eliminat:

| Duplicat | Resolucio |
|---|---|
| E-04 (glossari bilingue L1-L2) = G-01 (glossari bilingue complet) | E-04 eliminat, G-01 es la canonica |
| H-13 (AC: connexions interdisciplinars) = F-10 (connexions interdisciplinars) | H-13 eliminat, F-10 es la canonica |
| E-08 (referents culturalment diversos) + G-05 (substitucio referents culturals) | Fusionats: una sola instruccio que cobreix ambdos aspectes |
| H-14 (AC: manteniment complexitat) + H-14b (si existia duplicat intern) | Fusionats en una sola entrada |
| A-01/A-03 vs H-08 i A-05 vs H-02 | Resolts amb suppress_if_profile: les instruccions generiques (A-01, A-03, A-05) es suprimeixen quan el perfil especific (dislexia per H-08, TEA per H-02) ja les cobreix amb mes detall |

### 10.4 Tres noves instruccions

| ID | Instruccio | Activacio | Justificacio |
|---|---|---|---|
| A-27 | Retall per fatiga: si el text supera X paraules (llindar per MECR), dividir en parts amb indicador [Part N de M] | NIVELL (<=A2) | Textos llargs causen abandonament en nivells baixos. Complementa H-04 (TDAH micro-blocs) pero per motiu diferent (fatiga lectora vs atencio) |
| H-21 | Descripcio visual per ceguesa: generar descripcions textuals detallades de qualsevol element visual del text original (grafics, taules, mapes) | PERFIL (disc_visual) | Omplia un buit important: H-18 (alt-text) era per FE/CODI, pero l'LLM pot generar descripcions narratives dels visuals del text original |
| H-22 | Dislexia fonologica: evitar clusters consonantics (bl, pr, tr a inici de paraula), preferir paraules amb estructura CV-CV, evitar paraules amb doble consonant | PERFIL (dislexia) | Regla especifica per dislexia fonologica basada en Dehaene, mes granular que H-07 (compostos llargs) |

### 10.5 Vint-i-una sub-variables connectades

S'ha creat un mapa sistematic que connecta les 21 sub-variables del perfil alumne (configurables per UI) amb les instruccions del cataleg que activen o desactiven. El mapa complet es a `docs/decisions/mapa_variables_instruccions.md`.

Aquesta connexio permet que el codi `build_system_prompt()` seleccioni instruccions automaticament a partir de la configuracio del docent, sense logica ad hoc.

### 10.6 Simulacio d'eficiencia

Per validar l'impacte dels canvis, s'ha simulat un cas real:

**Cas**: nouvingut amb nivell A1, text explicatiu de ciencies naturals.

| Metrica | Abans (cataleg atomic) | Despres (macrodirectives) |
|---|---|---|
| Instruccions enviades | ~49 instruccions atomiques | 7 macrodirectives |
| Tokens estimats al prompt | ~2.500 tokens d'instruccions | ~800 tokens d'instruccions |
| Dins rang optim LLM (7-12) | No (4x per sobre) | Si |

Les 7 macrodirectives del cas nouvingut A1 son: LEXIC, SINTAXI, ESTRUCTURA, COGNITIU, QUALITAT, PERSONALITZACIO i PERFIL(nouvingut). MULTIMODAL i AVALUACIO nomes s'afegeixen si el docent activa complements.

---

## Annex A: Implementacio de referencia per a `build_system_prompt()` v2

Pseudocodi que il-lustra com quedaria la funcio reestructurada:

```python
def build_system_prompt_v2(profile, context, params, rag_context):
    parts = []

    # CAPA 1: Identitat (fixa)
    parts.append(IDENTITY_BLOCK)

    # CAPA 2: Instruccions universals (fixa)
    parts.append(UNIVERSAL_RULES_BLOCK)

    # CAPA 3a: Bloc MECR (nomes el nivell de sortida)
    mecr = params.get("mecr_sortida", "B2")
    parts.append(MECR_BLOCKS[mecr])

    # CAPA 3b: Bloc DUA
    dua = params.get("dua", "Core")
    parts.append(DUA_BLOCKS[dua])

    # CAPA 3c: Bloc genere discursiu (si detectat)
    genre = detect_genre(context)  # o indicat pel docent
    if genre in GENRE_BLOCKS:
        parts.append(GENRE_BLOCKS[genre])

    # CAPA 3d: Blocs per perfil (nomes els actius)
    active_profiles = get_active_profiles(profile)
    for p in active_profiles:
        if p in PROFILE_BLOCKS:
            parts.append(PROFILE_BLOCKS[p])

    # CAPA 3e: Blocs de creuament (nomes si apliquen)
    for combo, block in CROSSING_BLOCKS.items():
        if all(p in active_profiles for p in combo):
            parts.append(block)

    # CAPA 3f: Few-shot example (1 per al nivell MECR)
    if mecr in FEWSHOT_EXAMPLES:
        parts.append(FEWSHOT_EXAMPLES[mecr])

    # CAPA 4a: Persona-audience
    parts.append(build_persona_audience(profile, context))

    # CAPA 4b: Context RAG
    if rag_context:
        parts.append(f"CONEIXEMENT PEDAGOGIC (FJE):\n{rag_context}")

    # CAPA 4c: Format de sortida
    parts.append(build_output_format(params))

    return "\n\n".join(parts)


def build_persona_audience(profile, context):
    """Genera narrativa concreta de l'alumne."""
    chars = profile.get("caracteristiques", {})
    etapa = context.get("etapa", "ESO")
    narrativa = f"Escrius per a un alumne de {etapa}"

    if chars.get("nouvingut", {}).get("actiu"):
        l1 = chars["nouvingut"].get("L1", "desconeguda")
        mecr = chars["nouvingut"].get("mecr", "A1")
        narrativa += f" nouvingut (L1: {l1}, MECR: {mecr})"

    # ... altres perfils

    return f"PERSONA-AUDIENCE:\n{narrativa}"
```

---

## Annex B: Metriques d'exit per fase

| Fase | Metrica | Objectiu |
|---|---|---|
| Fase 0 | Longitud del prompt enviat | Reduir de ~4000 tokens a ~2500 |
| Fase 0 | Frequencia de meta-text indesitjat | Reduir >50% |
| Fase 1 | Variabilitat entre adaptacions del mateix text | Reduir 40-60% (gracies a few-shot) |
| Fase 1 | Satisfaccio docent (pilot 5 docents FJE) | >4/5 en utilitat |
| Fase 2 | Longitud mitjana de frase per nivell MECR | Dins rang (A1: 5-8, A2: 8-12, B1: 12-18) |
| Fase 2 | Paraules prohibides a la sortida | <1% dels textos |
| Fase 3 | Temps de resposta amb routing | <8s per adaptacio basica, <15s per complexa |
| Fase 3 | Cobertura pictogrames | >80% conceptes clau amb ARASAAC |

---

## Annex C: Referències bibliografiques principals

Pels marcs teorics integrats a l'arquitectura:

- Sweller, J. (2011). *Cognitive Load Theory*. Springer.
- Mayer, R.E. (2021). *Multimedia Learning* (3rd ed.). Cambridge University Press.
- Halliday, M.A.K. & Matthiessen, C. (2014). *Halliday's Introduction to Functional Grammar* (4th ed.). Routledge.
- Vygotsky, L.S. (1978). *Mind in Society*. Harvard University Press.
- Dehaene, S. (2009). *Reading in the Brain*. Viking.
- Wolf, M. (2018). *Reader, Come Home*. Harper.
- ISO 24495-1:2023. *Plain language -- Part 1: Governing principles and guidelines*.
- Anderson, L.W. & Krathwohl, D.R. (2001). *A Taxonomy for Learning, Teaching, and Assessing*. Pearson.
- Graves, M.F. & Graves, B.B. (2003). *Scaffolded Reading Experiences* (2nd ed.). Christopher-Gordon.
- Hattie, J. (2023). *Visible Learning: The Sequel*. Routledge.
