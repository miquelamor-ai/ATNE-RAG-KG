# Modelabilitat de LLM per a adaptació de materials didàctics

## 1. Propòsit

Aquest document sintetitza informació sobre diversos models de llenguatge disponibles via API i la seva capacitat de ser modelats mitjançant indicacions (prompts) per a tasques d'adaptació de textos i materials didàctics.

L'objectiu és enllaçar la taxonomia de variables d'adaptació (A1/A2) amb la sensibilitat real dels models a les instruccions i oferir criteris per escollir el model més adequat segons el tipus d'adaptació.

## 2. Models considerats

Es consideren els següents models servits via API:

- GPT-4o / GPT-4.x (OpenAI o compatibles).
- Claude 3 (Opus, Sonnet, Haiku) d'Anthropic.
- Gemini 2.x (Flash, Pro, variants similars) de Google.
- Mistral (Large, Mixtral / Nemo, Agents API).
- Llama 3.x Instruct (p. ex. 3.3 70B Instruct) servits via APIs compatibles.

## 3. Resum de capacitats de modelatge via indicacions

### 3.1 Eixos generals de "promptability"

Per a l'adaptació de materials, es consideren aquests eixos de sensibilitat a les indicacions:

- Control d'estil lingüístic: frases curtes, lèxic freqüent, evitació de metàfores, registre, veu activa.
- Control d'estructura: paràgrafs curts, títols/subtítols, llistes, resum inicial/final, glossari.
- Control semàntic: explicitar allò implícit, explicar referents culturals, mantenir totes les idees clau.
- Control de format: produir JSON estricte, markdown estructurat, seccions fixes i esquemes de sortida.
- Control de multimodalitat textual: afegir glossaris, suggerir imatges funcionals, incloure preguntes guia o activitats.
- Control de càrrega cognitiva: simplificar sense eliminar conceptes, ajustar quantitat d'informació i repte.
- Control de límits pedagògics i de seguretat: no inventar contingut, no inferir diagnòstics, no rebaixar objectius sense permís docent.

### 3.2 Taula comparativa alta

| Model | Punts forts de modelatge via prompts | Limitacions rellevants |
| --- | --- | --- |
| GPT-4o / GPT-4.x | Molt bona adherència a formats estructurats (JSON, esquemes) i control de sortida amb paràmetres d'API quan són disponibles. Bona sensibilitat a canvis d'estil i rol si s'expliciten indicacions i exemples. | Pot relaxar algunes restriccions fines (p. ex. longitud exacta de frase) en textos llargs si no es combinen prompts amb validacions externes. |
| Claude 3 (Opus/Sonnet) | Molt fort en seguiment de system prompts extensos amb instruccions jeràrquiques; bones pràctiques d'Anthropic orientades a estructurar rol, objectius i regles. Molt sensible a matisos d'estil i to. | Quan hi ha massa regles simultànies, pot introduir redundància o ser massa literal; continua requerint validació externa per a formats estrictes. |
| Gemini 2.x | Bon control d'estil i to via prompts, amb documentació específica sobre control de la parla i l'estil de resposta. Fort en escenaris multimodals (text + imatge). | Compliment de formats molt rígids pot ser menys estable que models més centrats en text si no s'aporten exemples i validació posterior. |
| Mistral (Large/Agents) | Models instruct eficients amb bona resposta a prompts compactes i clars; Agents API facilita orquestració i memòria. | Adherència a formats estrictes i a regles fines d'estil menys consistent que GPT/Claude si no es reforça amb validació i cicles de postprocés. |
| Llama 3.x Instruct (via API) | Bona base per a tasques d'explicació, simplificació i resum; adequada per entorns self-hosted o APIs genèriques amb control d'infraestructura. | Compliment de micro-regles (p. ex. límit precís de paraules per frase, evitar completament idiomatismes) més variable i depenent de la implementació. |

## 4. Relació entre variables A1/A2 i capacitat de control per model

### 4.1 Variables A1 (llengua i estructura)

Variables A1 típiques: longitud de frase (TXT_SENT_LEN), complexitat sintàctica (TXT_SENT_COMPLEX), freqüència lèxica (TXT_LEX_FREQ), densitat terminològica (TXT_TERM_DENS), idiomatismes (TXT_IDIOM), jerarquia de títols (MACRO_HEAD), longitud de paràgraf (MACRO_PARA), llistes (MACRO_LIST), resums (MACRO_SUM_PRE/POST).

- GPT-4o i Claude 3 responen bé a indicacions com "fes frases curtes, una idea per frase, evita metàfores, defineix tecnicismes" quan aquestes es donen de manera explícita i amb 1-2 exemples.
- Gemini 2.x també controla bé l'estil i el registre, especialment si es defineix clarament el públic objectiu i es proporcionen prompts d'exemple.
- Mistral i Llama 3.x responen a la simplificació i al canvi d'estil, però el grau de control fi pot ser inferior; convé acompanyar l'ús amb validació automàtica (p. ex. calcular longitud mitjana de frase sobre la sortida i re-iterar si cal).

En general, les indicacions de tipus **"estil i microestructura"** són bastant "promptables" a tots els models, amb adherència més consistent en Claude 3 i GPT-4o.

### 4.2 Variables A1 de format i layout

Variables com longitud de línia (LAY_LINE_LEN), tipografia, contrast, compatibilitat amb lector de pantalla o navegació per teclat (ACC_SCREEN, ACC_KEYB, LAY_CONTRAST, LAY_FONT_SIZE) depenen més del codi, CSS i plantilles que no pas del model.

- Els models poden generar HTML/markdown amb jerarquia semàntica correcta (títols, llistes, seccions), però **no poden garantir** contrast real, comportament de focus, zoom, etc.
- Per tant, val la pena demanar-los estructura semàntica clara, però la comprovació d'accessibilitat tècnica ha de recaure en eines i pipelines de desenvolupament (linters, validadores, CSS).

### 4.3 Variables A2 (càrrega cognitiva, tasca, principis de marcs addicionals)

Variables com càrrega cognitiva de la tasca (TASK_COG_LOAD), exigència inferencial (SEM_INFER), càrrega cultural (SEM_CULT), claredat de tasca (COGA-like), funció ambiental dels materials (ICF), representativitat i diversitat (Index for Inclusion) són més **conceptuals**.

- Claude 3 i GPT-4o són més competents a respondre a instruccions del tipus "simplifica el llenguatge però manté totes les idees clau i un cert repte cognitiu", o "explica referents culturals i fes explícites inferències importants".
- Gemini 2.x pot ser útil quan es volen suggeriments multimodals (afegir imatges explicatives o vídeos curts relacionats) en funció del contingut.
- Per Mistral i Llama, aquest tipus d'instruccions conceptuals funcionen, però pot ser necessari guiar més la sortida amb exemples i checks automàtics (p. ex. comparar nombre de conceptes clau abans/després).

## 5. Té sentit passar totes les indicacions A1/A2 al prompt?

Les guies de bons prompts per Claude, GPT i altres models desaconsellen prompts massa llargs i llistes enormes de regles; recomanen agrupar les regles en blocs i prioritzar les més importants per a la tasca.

En aquest context:

- No és eficient carregar cada crida amb la taxonomia completa A1/A2; és millor tenir **plantilles per perfil d'adaptació** amb 5-8 regles claus i exemples de transformació.
- Dimensions molt tècniques d'accessibilitat (contrast, navegació per teclat, tipografia) s'han de resoldre a nivell d'implementació, mentre que els models s'han de centrar en llengua, estructura i suport semàntic.
- Algunes dimensions conceptuals (participació, representativitat, nivell d'intervenció adaptació vs accommodació vs modificació) poden aparèixer com a "principis de política" que condicionen què se li permet fer al model (p. ex. no eliminar contingut curricular sense instruccions específiques).

## 6. Orientació per a l'elecció de model segons adaptació

### 6.1 Taula orientativa per tipus d'adaptació

| Tipus d'adaptació | Exemple de requeriments A1/A2 | Models recomanats | Notes |
| --- | --- | --- | --- |
| Simplificació lingüística + lectura fàcil | TXT_SENT_LEN curt, TXT_LEX_FREQ alta, TXT_IDIOM baix, explicació de tecnicismes, glossari bàsic. | Claude 3 (Opus/Sonnet), GPT-4o | Millor adherència a regles d'estil combinades, especialment amb system prompt estructurat i exemples. |
| Reestructuració macro (títols, llistes, resums) | MACRO_HEAD clar, MACRO_PARA curt, MACRO_LIST, MACRO_SUM_PRE/POST. | GPT-4o, Claude 3 | Bona capacitat per generar estructures marcades i seguir plantilles de seccions. |
| Adaptació amb focus en accessibilitat cognitiva (COGA) | Claredat de tasca, passos numerats, suport a memòria de treball, reducció de distraccions. | Claude 3, GPT-4o | System prompts extensos amb passos i checklists; Claude 3 especialment robust per a rols complexos. |
| Adaptació multimodal (text + suggeriments visuals) | MOD_IMG_REL, MOD_GLOSS_VIS, suggeriments d'àudio/vídeo. | Gemini 2.x | Fort en multimodalitat i control estilístic; útil per suggeriments d'imatges i vídeos educatius. |
| Adaptacions cost-eficients amb validació externa | Simplificació bàsica, resum, reestructuració parcial, sota pipelines de validació. | Mistral Large, Llama 3.x Instruct | Més econòmics; es recomana afegir validadors automàtics de format, longitud i estructura. |

### 6.2 Ranking general per adaptació textual educativa

Assumint accés als models de gamma alta i sense considerar el cost com a limitació principal:

1. **Claude 3 (Opus/Sonnet)** — millor adherència global a prompts complexos i rols d'adaptador de materials amb regles múltiples; recomanat com a primera opció per adaptar textos amb criteris A1/A2 sofisticats.
2. **GPT-4o / GPT-4.x** — molt fort en generació estructurada i en equilibri entre control de format i qualitat de contingut; excel·lent segon candidat o complement en un sistema híbrid.
3. **Gemini 2.x** — especialment recomanable quan el projecte requereix multimodalitat i integració estreta amb ecosistema Google; molt competent en control d'estil i to.
4. **Mistral Large / Agents** — bona relació cost-rendiment i integració amb agents; ideal per sistemes amb fort control d'orquestració i validació de sortida.
5. **Llama 3.x Instruct via API** — bona base per infraestructures pròpies i per escenaris on el control de dades i hosting és crític; fiable per adaptacions bàsiques, menys per complir micro-regles sense capes de control addicionals.

## 7. Recomanacions pràctiques de disseny de prompts per A1/A2

Les millors pràctiques en prompting per Claude, GPT i altres models coincideixen en alguns punts clau:

1. **Separar rols, objectius i regles**.
   - Definir clarament el rol de l'agent (p. ex. "adaptador de materials per alumnat X"), l'objectiu (p. ex. "maximitzar comprensió mantenint idees clau") i les regles d'estil i estructura.

2. **Prioritzar 5-8 regles per crida**.
   - A partir de la taxonomia A1/A2, seleccionar només les variables clau per al perfil i la tasca, en lloc de llistar-les totes.

3. **Incloure exemples d'abans/després**.
   - Mostrar al model 1-2 fragments originals amb la corresponent adaptació, incorporant les regles A1/A2 desitjades.

4. **Afegir mini-checklist de comprovació**.
   - Demanar explícitament que el model confirmi, abans de respondre, que ha aplicat determinades regles (frases curtes, glossari, resums, etc.).

5. **Complementar amb validació automàtica**.
   - Implementar, fora del model, verificacions de longitud de frase, presència de títols, format JSON, etc., i re-iterar si cal.

Aquestes pràctiques maximitzen l'efecte de les variables A1/A2 sobre la sortida dels models i permeten aprofitar millor la seva capacitat de ser modelats amb indicacions, especialment en el cas de Claude 3, GPT-4o i Gemini 2.x.
