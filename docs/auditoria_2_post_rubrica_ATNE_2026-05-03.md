# Auditoria 2 ATNE post-rubrica

Data: 2026-05-03  
Relacio amb l'auditoria anterior: aquesta auditoria no substitueix `docs/auditoria_profunda_ATNE_2026-05-03.md`; la rellegeix amb la rubrica de decisio del projecte i en treu una prioritzacio mes estricta.  
Objectiu: decidir que cal fer ara, que cal validar post-pilot, que cal portar a migracio/sprint dedicat i que cal aparcar.

## 1. Veredicte executiu

La primera auditoria era correcta com a mapa de riscos i arquitectura objectiu, pero era massa ampla per al moment del projecte. Despres d'aplicar la rubrica ATNE, el criteri canvia:

- **No tot el que es tecnicament correcte s'ha de fer ara.**
- **No tot el que millora qualitat justifica tocar el flux principal durant el pilot.**
- **No tota abstraccio bona es bona abans de la migracio FJE.**
- **La prioritat no es fer ATNE mes sofisticat, sino mes fiable sense perdre el marc rector.**

La decisio central d'aquesta auditoria 2 es:

1. Ara nomes entren **riscos de seguretat, privacitat, compliment, dades o bugs que puguin degradar el pilot**.
2. Les millores de prompt, harness, UI modular i arquitectura passen a **post-pilot o sprint dedicat**, excepte microcanvis que no alterin el flux.
3. Les propostes d'agents, auto-millora, GEPA, plataforma i grans refactors passen a **roadmap**, no al cicle actual.
4. Qualsevol proposta ha de demostrar que ajuda a **apropar, bastir i acompanyar**, no a rebaixar.

## 2. Rubrica que faria servir

Faria servir la rubrica del projecte com a marc principal, amb una versio operativa per auditar propostes. No canviaria el fons de la rubrica; hi afegiria portes de decisio per evitar que l'auditoria generi backlog indiscriminat.

### 2.1 Rubrica ATNE-R2 de decisio de millores

La rubrica que faria servir es:

```text
ATNE-R2 = Rubrica ATNE original + porta C0 + escala d'evidencia + classificacio temporal + veredicte obligatori.
```

### 2.2 Jerarquia d'objectius

Mantindria els 7 objectius jerarquitzats:

1. **Marc rector ignasia + visio inclusiva**  
   Cura personalis, acompanyament, dignificacio, magis, adaptar a temps/llocs/persones. Rebutjar tot el que porti a rebaixar, etiquetar o fer "facil" sense bastida.

2. **Qualitat pedagogica del text adaptat**  
   Rigor curricular, genere discursiu, multinivell coherent, complements ben formats, fidelitat del contingut.

3. **Inclusivitat conceptual i terminologica**  
   Condicions, situacions, barreres, necessitats; perfil com a combinacio, no diagnostic. Via observable per al docent.

4. **Usabilitat per al docent FJE real**  
   Tres passos, text dominant, accions minimes, perfil visible, funcionament a mobil docent.

5. **Transparencia pedagogica i confianca**  
   El docent ha d'entendre per que s'ha adaptat aixi. "Saber-ne+", traçabilitat i criteri docent.

6. **Coherencia amb la plataforma futura**  
   Perfils, corpus, KG i regles han de poder ser serveis transversals, no hardcode d'una pantalla.

7. **Sostenibilitat tecnica i de costos**  
   Python + JS pur, LLMs barats/gratuits quan sigui viable, evitar deute abans de migracio, cost operacional assumible per Miquel.

### 2.3 Porta C0: risc abans de pilot first

Afegiria una porta previa:

```text
C0. Seguretat, privacitat, compliment i confiança institucional.
Si una proposta corregeix exposicio de dades, ownership, XSS, consentiment, risc legal,
traçabilitat minima o confiança institucional, pot entrar abans del final del pilot,
sempre amb canvi minim viable.
```

Aixo matisa "pilot first". Pilot first no pot bloquejar una correccio de privacitat.

### 2.4 Escala d'evidencia

Per no tractar igual una opinio, una dada de codi i un resultat del pilot, faria servir aquesta escala:

```text
E5 - Evidencia directa reproduible de codi, seguretat o bug.
E4 - Dades del pilot amb us real docent.
E3 - Batch/eval ATNE existent.
E2 - Literatura, practica externa o patró consolidat.
E1 - Judici expert raonat, pendent de validar.
E0 - Preferencia o intuicio sense evidencia.
```

Regla:

- E5 + C0 pot entrar ara.
- E4/E3 serveix per prioritzar post-pilot.
- E2/E1 va a experiment o roadmap.
- E0 no entra.

### 2.5 Classificacio obligatoria

Cada proposta ha de tenir una classe:

```text
Bug pilot
Risc seguretat/privacitat/compliment
Millora de qualitat pedagogica
Millora UX
Refactor tecnic
Experiment post-pilot
Estrategic/roadmap
```

I un moment:

```text
Ara pilot
Post-pilot immediat
Sprint dedicat
Migracio FJE
Roadmap
Rebutjar
```

### 2.6 Veredicte obligatori

Cada proposta ha d'acabar en un dels veredictes:

```text
Acceptar ara amb canvi minim
Acceptar post-pilot
Fer A/B post-pilot
Aparcar a migracio
Aparcar a roadmap
Rebutjar
Reobrir decisio previa amb justificacio explicita
```

## 3. Que refaig de l'auditoria 1 despres de la rubrica

### 3.1 El canvi mes important

La primera auditoria prioritzava massa per severitat tecnica. L'auditoria 2 prioritza per:

1. risc per al pilot;
2. alineacio amb marc rector;
3. evidencia;
4. cost de manteniment;
5. moment adequat.

Per tant, moltes recomanacions continuen sent bones, pero canvien de moment.

### 3.2 El que mantinc

Mantinc aquests diagnòstics:

- `routes/drafts.py` confia massa en `docent_id` client-side, mentre `routes/adaptations.py` te un patro millor d'ownership autenticat.
- `ui/atne/pas3.html` usa molt `innerHTML` amb contingut generat, guardat o derivat de l'usuari.
- El consent gate esta desactivat a les tres pantalles, mentre la DPIA descriu consentiment.
- El prompt fa massa coses en una sola generacio.
- El verificador LLM usa el mateix model que genera, cosa que limita el valor d'auditoria.
- El harness actual no pot ser porta de qualitat si `pytest` pot trencar-se en collection per scripts amb xarxa.
- Els grans fitxers son un risc real de manteniment.

### 3.3 El que rectifico

Rectifico tres coses de la primera auditoria:

1. **No faria entrar tots els P0 proposats.**  
   En pilot nomes faria canvis minims de risc. El refactor de concurrencia, prompt split o harness complet no entren si no hi ha incidencia real.

2. **No presentaria l'arquitectura objectiu com a feina immediata.**  
   La deixaria com a nord de migracio/sprint dedicat, no com a backlog urgent.

3. **Posaria el marc ignasia al davant.**  
   L'auditoria 1 parlava massa en llenguatge d'arquitectura LLM i massa poc en llenguatge ATNE: apropar, bastir, acompanyar, dignificar i mantenir exigencia.

## 4. Auditoria 2: matriu de decisions

### A2-01. Ownership dels drafts

**Troballa**  
`routes/drafts.py` accepta `docent_id` de query/body; `ui/atne/js/llm.js` reconeix que el `docent_id` localStorage no es auth real. En canvi, `routes/adaptations.py` calcula ownership a partir de l'usuari autenticat.

**Rubrica**  
C0, objectius 4, 5 i 7.  
Evidencia: E5, codi local.  
Tipus: risc seguretat/privacitat.

**Veredicte**  
Acceptar ara amb canvi minim.

**Accio recomanada**  
Portar el patro de `routes/adaptations.py` a drafts. No redissenyar auth; nomes impedir que el client decideixi la identitat efectiva.

**Per que passa la rubrica**  
No es una optimitzacio. Es proteccio de dades i confiança institucional.

### A2-02. Sanititzacio de sortides LLM/HTML

**Troballa**  
Hi ha multiples assignacions `innerHTML` a `pas3.html` amb text original, adaptat, complements, HTML guardat i contingut generat.

**Rubrica**  
C0, objectius 4, 5 i 7.  
Evidencia: E5, codi local.  
Tipus: risc seguretat/privacitat.

**Veredicte**  
Acceptar ara amb canvi minim si es pot fer sense alterar UX; si no, aplicar mitigacio minima i completar post-pilot.

**Accio recomanada**  
Afegir una funcio unica de sanititzacio per al render de contingut LLM/guardat i usar-la en els punts mes exposats de `pas3`. Evitar una reescriptura completa del renderer durant el pilot.

**Per que passa la rubrica**  
Protegeix el docent i la institució sense canviar la proposta pedagogica.

### A2-03. Incoherencia consent gate / DPIA

**Troballa**  
Els fitxers `pas1`, `pas2` i `pas3` tenen el consent gate comentat/desactivat, mentre la DPIA descriu un flux amb consentiment.

**Rubrica**  
C0, objectiu 5.  
Evidencia: E5, codi/documentacio local.  
Tipus: compliment/confiança.

**Veredicte**  
Acceptar ara amb canvi minim documental o operatiu.

**Accio recomanada**  
Decidir una de dues opcions i alinear-ho:

- reactivar consentiment si el pilot ho exigeix;
- o ajustar la DPIA i el text legal si la base operativa no es consentiment explicit.

No faria una solucio legal sofisticada a mig pilot sense criteri institucional.

### A2-04. Prompt unic massa carregat

**Troballa**  
El prompt genera text adaptat, complements, argumentacio pedagogica i notes d'auditoria en el mateix output.

**Rubrica**  
Objectius 2, 5 i 7.  
Evidencia: E3/E2, codi + resultats d'avaluacio + practica LLM.  
Tipus: millora de qualitat pedagogica / experiment post-pilot.

**Veredicte**  
Fer A/B post-pilot, no tocar el flux principal ara.

**Accio recomanada**  
Preparar un experiment:

- branca A: prompt actual;
- branca B: text adaptat separat de capa docent;
- mesurar fidelitat, qualitat, format, temps, cost, satisfaccio docent i edicio posterior.

**Per que no entra ara**  
Toca el cor del producte i podria alterar resultats del pilot. La rubrica diu pilot first.

### A2-05. Separar material alumne i capa docent

**Troballa**  
`Argumentació pedagògica` i `Notes d'auditoria` formen part del contracte de sortida. Conceptualment, aixo pot barrejar material per alumne amb justificacio per docent.

**Rubrica**  
Objectius 2 i 5.  
Evidencia: E2/E1; coherent pedagogicament, pero falta dada pilot.  
Tipus: millora UX/pedagogica.

**Veredicte**  
Acceptar post-pilot, amb A/B si afecta la pantalla de resultat.

**Accio recomanada**  
No eliminar la transparencia; moure-la a una capa docent clara. El docent ha de poder veure el perque, pero el document de l'alumne ha de quedar net.

### A2-06. Verificador amb el mateix model generador

**Troballa**  
L'orchestrator fa verificacio rapida amb el mateix `active_model`.

**Rubrica**  
Objectius 2, 5 i 7.  
Evidencia: E3/E2, informes interns + practica LLM-as-judge.  
Tipus: millora de harness.

**Veredicte**  
Acceptar post-pilot.

**Accio recomanada**  
Canviar a jutge extern o validadors deterministes primer. No fer-ho ara si incrementa cost o latencia del pilot sense necessitat.

### A2-07. Harness trencable en collection

**Troballa**  
Un script de prova OpenRouter fa xarxa i `sys.exit` en import, cosa que pot trencar `pytest --collect-only`.

**Rubrica**  
Objectiu 7.  
Evidencia: E5, execucio local.  
Tipus: bug de desenvolupament.

**Veredicte**  
Acceptar ara nomes si bloqueja desenvolupament o deploy; si no, post-pilot immediat.

**Accio recomanada**  
Microcanvi:

- moure scripts live fora de discovery;
- afegir `if __name__ == "__main__"`;
- crear `pytest.ini` amb `testpaths = tests`.

No crear encara un harness complet si el pilot esta en marxa.

### A2-08. Monolit `server.py`

**Troballa**  
`server.py` concentra massa responsabilitats.

**Rubrica**  
Objectius 6 i 7.  
Evidencia: E5, codi local.  
Tipus: refactor tecnic.

**Veredicte**  
Aparcar a sprint dedicat o migracio FJE.

**Accio recomanada**  
No fer un gran split ara. Crear un pla de migracio i, mentrestant, nomes extreure funcions si cal tocar-les per un bug.

**Per que no entra ara**  
El criteri F rebutja abstraccions prematures, especialment amb migracio a l'horitzo.

### A2-09. `pas3.html` massa gran

**Troballa**  
`pas3.html` concentra editor, render, streaming, exportacio, feedback, biblioteca, historial i il·lustracions.

**Rubrica**  
Objectius 4, 6 i 7.  
Evidencia: E5.  
Tipus: refactor UI.

**Veredicte**  
Aparcar a sprint dedicat, amb excepcio de fixes de seguretat.

**Accio recomanada**  
Ara: tocar nomes sanititzacio o bugs del pilot.  
Post-pilot: split progressiu per moduls, començant per `sanitize/render`, `sse`, `editor-history`, `export`.

### A2-10. Massa estat en `localStorage`

**Troballa**  
El flux usa `localStorage` per perfils, text original, adaptacio, drafts, complements, ids i docent.

**Rubrica**  
Objectius 4, 5 i 7; C0 quan afecta identitat/dades.  
Evidencia: E5.  
Tipus: mixt: risc + refactor.

**Veredicte**  
Dividir:

- identitat/ownership: acceptar ara amb canvi minim;
- estat UX no sensible: post-pilot;
- arquitectura d'estat: migracio/sprint.

**Accio recomanada**  
No demonitzar `localStorage`: es pragmatic per pilot. Pero no pot ser font d'autoritat d'identitat ni ownership.

### A2-11. Concurrencia de `/api/adapt`

**Troballa**  
`/api/adapt` usa `ThreadPoolExecutor` per request i una llista compartida d'events entre threads.

**Rubrica**  
Objectiu 7.  
Evidencia: E5 codi; impacte real pendent.  
Tipus: bug potencial / robustesa.

**Veredicte**  
Post-pilot, excepte si el pilot mostra errors de streaming, bloquejos o perdua d'events.

**Accio recomanada**  
Si hi ha incidencies, fer patch minim amb `queue.Queue`. Si no, deixar-ho com a refactor controlat.

### A2-12. Estrategia LLM barats/gratuits

**Troballa**  
Hi ha configuracio de models i preus en codi, i una estrategia que depen de free tiers i rotacio.

**Rubrica**  
Objectiu 7, i objectiu 2 si afecta qualitat.  
Evidencia: E3 interna + dades pilot pendents.  
Tipus: optimitzacio post-pilot.

**Veredicte**  
Acceptar post-pilot.

**Accio recomanada**  
No canviar model principal durant el pilot si no hi ha fallada. Despres:

- registry de models amb data de revisio;
- metriques reals de qualitat/cost/latencia;
- routing per tasca;
- alertes de cost.

### A2-13. Rubrica pedagogica v3

**Troballa**  
La rubrica v2 interna te bona consistencia, pero la fidelitat curricular sembla una dimensio independent.

**Rubrica**  
Objectius 2 i 5.  
Evidencia: E3, analisi estadistica interna.  
Tipus: millora de qualitat pedagogica.

**Veredicte**  
Acceptar post-pilot.

**Accio recomanada**  
Reformular la rubrica d'avaluacio de sortides:

- fidelitat curricular com a porta;
- qualitat pedagogica com a dimensio separada;
- usabilitat docent com a dimensio separada;
- justificacio curta amb evidencia del text.

### A2-14. Terminologia de perfils

**Troballa**  
El projecte ja sap que cal distingir condicions, situacions, barreres, necessitats i perfils combinats.

**Rubrica**  
Objectius 1 i 3.  
Evidencia: E3/E1, documents interns i coherencia pedagogica.  
Tipus: millora conceptual/UX copy.

**Veredicte**  
Acceptar post-pilot; microcopy ara nomes si no altera flux.

**Accio recomanada**  
Crear guia terminologica i revisar copies de UI. Prioritzar llenguatge observable: "barreres detectades", "suports que necessita", "situacio linguistica", "condicions conegudes si el docent les vol indicar".

### A2-15. Matriu de traçabilitat pedagogica

**Troballa**  
Les instruccions i perfils necessiten millor traçabilitat entre regla, evidencia, risc i etapa.

**Rubrica**  
Objectius 1, 2, 3 i 5.  
Evidencia: E1/E2; molt coherent, pero no bloquejant.  
Tipus: estrategic post-pilot.

**Veredicte**  
Acceptar post-pilot com a document viu.

**Accio recomanada**  
No crear una eina complexa. Començar amb una taula Markdown/CSV:

```text
id_regla | perfil/barrera | objectiu | evidencia | risc | exemple bo | exemple dolent | estat
```

### A2-16. Agents, auto-millora i GEPA

**Troballa**  
L'auto-millora de prompts i agents pot ser potent, pero nomes si hi ha harness fiable i aprovacio humana.

**Rubrica**  
Objectius 5, 6 i 7.  
Evidencia: E2/E1.  
Tipus: estrategic/roadmap.

**Veredicte**  
Aparcar a roadmap.

**Accio recomanada**  
No implementar ara. Condicions previes:

- gold set;
- rubrica v3;
- eval reproduible;
- logs de pilot;
- human approval;
- rollback.

## 5. Que faria ara, exactament

Durant el pilot, faria nomes aquests blocs:

### Ara 1. Ownership de drafts

Canvi minim:

- calcular docent autenticat al backend;
- rebutjar mismatch;
- no confiar en `docent_id` localStorage.

### Ara 2. Sanititzacio minima de sortides

Canvi minim:

- introduir sanititzador;
- aplicar-lo als punts de render de contingut adaptat/guardat;
- no reescriure tot el renderer.

### Ara 3. Consentiment/DPIA

Canvi minim:

- decisio institucional;
- coherencia entre documentacio i UI;
- si no es reactiva consent gate, ajustar la DPIA.

### Ara 4. Guardrail de no regressio

Canvi minim:

- si `pytest` o scripts trenquen desenvolupament, protegir scripts live;
- no construir encara harness v3 complet.

## 6. Que no faria ara

No faria ara:

- split gran de `server.py`;
- modularitzacio completa de `pas3.html`;
- canvi de model principal;
- prompt split en produccio;
- nou sistema d'agents;
- GEPA;
- RAG-KG;
- migracio d'arquitectura;
- redisseny de UI;
- nova taxonomia completa de perfils dins del flux.

No perquè siguin males idees, sino perquè la rubrica diu que no toca ara sense dades del pilot o sense necessitat de seguretat.

## 7. Experiments post-pilot prioritaris

Quan acabi el pilot, faria aquests experiments en ordre:

### EXP-1. Prompt actual vs sortida alumne/docent separada

Pregunta pilot vinculada: qualitat, transparencia, usabilitat.  
Mesures: qualitat docent, edicio posterior, errors de format, temps, cost, satisfaccio.

### EXP-2. Verificador mateix model vs jutge extern vs validators deterministes

Pregunta pilot vinculada: qualitat i confiança.  
Mesures: correlacio amb docent, falsos positius/negatius, cost, latencia.

### EXP-3. Rubrica v2 vs rubrica v3

Pregunta pilot vinculada: qualitat.  
Mesures: fidelitat curricular com a porta, coherencia entre jutges, utilitat de l'informe.

### EXP-4. UI amb capa docent separada

Pregunta pilot vinculada: transparencia i usabilitat.  
Mesures: si el docent entén millor l'adaptacio, si exporta mes, si edita menys, si confia mes.

### EXP-5. Routing de models

Pregunta pilot vinculada: qualitat, sostenibilitat i funcionalitats.  
Mesures: cost per adaptacio util, latencia, taxa de retry, qualitat per perfil.

## 8. Lectura pedagogica post-rubrica

La pregunta no es "com fem ATNE mes potent?". La pregunta es:

```text
Com fem que ATNE ajudi el docent a acompanyar millor cada alumne,
mantenint exigencia, dignitat, rigor curricular i criteri professional,
amb el minim de complexitat operativa?
```

Aixo canvia el filtre:

- Si una proposta fa el text mes facil pero menys rigoros, es rebutja.
- Si una proposta augmenta funcionalitat pero fa la UI menys docent, s'aparca.
- Si una proposta millora un 5% la qualitat pero duplica complexitat, s'aparca.
- Si una proposta protegeix dades o confiança institucional, entra ara.
- Si una proposta ajuda el docent a entendre per que, passa millor la rubrica.

## 9. Revisio de la primera auditoria per blocs

### Arquitectura

Diagnosi valida, moment corregit.  
El refactor gran no es P0. S'ha de convertir en pla de migracio/sprint, amb canvis petits quan un bug obligui a tocar una zona.

### Prompt

Diagnosi valida, moment corregit.  
El prompt split es una hipotesi forta, no un canvi immediat. Cal A/B post-pilot.

### Harness

Diagnosi valida, moment corregit.  
Arreglar collection si bloqueja; harness v3 post-pilot.

### Pedagogia

Cal reforçar mes el marc ignasia.  
La primera auditoria va parlar be de DUA i inclusio, pero el marc rector ha de manar: no simplificar per rebaixar, sino bastir per fer possible el magis.

### UIX

Diagnosi valida, moment corregit.  
La separacio alumne/docent es bona, pero s'ha de validar. Ara nomes tocar seguretat o bugs.

### Seguretat

La primera auditoria queda confirmada i reforçada.  
Ownership, sanititzacio i coherencia DPIA son els tres punts que poden trencar confiança del pilot.

## 10. Backlog filtrat per rubrica

| Prioritat | Proposta | Tipus | Evidencia | Moment | Veredicte |
|---|---|---|---|---|---|
| P0 | Ownership drafts | Risc privacitat | E5 | Ara | Acceptar canvi minim |
| P0 | Sanititzacio LLM/HTML | Risc seguretat | E5 | Ara | Acceptar canvi minim |
| P0 | Coherencia consentiment/DPIA | Compliment/confiança | E5 | Ara | Decidir i alinear |
| P0/P1 | Protegir scripts live de pytest | Bug dev | E5 | Ara si bloqueja | Microfix |
| P1 | Prompt alumne/docent separat | Qualitat/UX | E3/E2 | Post-pilot | A/B |
| P1 | Jutge extern/validators | Harness | E3/E2 | Post-pilot | Acceptar |
| P1 | Rubrica sortides v3 | Qualitat pedagogica | E3 | Post-pilot | Acceptar |
| P1 | Guia terminologica | Inclusio | E3/E1 | Post-pilot | Acceptar |
| P2 | Split `pas3.html` | Refactor UI | E5 | Sprint dedicat | Aparcar |
| P2 | Split `server.py` | Refactor backend | E5 | Sprint/migracio | Aparcar |
| P2 | Registry models/costos | Sostenibilitat | E3 | Post-pilot | Acceptar |
| R | Agents/GEPA | Estrategic | E2/E1 | Roadmap | Aparcar |

## 11. Conclusio

La primera auditoria deia: ATNE ha de ser mes robusta, modular, segura, verificable i pedagogicament validada.

L'auditoria 2 diu: si apliquem la rubrica, **no hem de convertir aquesta llista en feina immediata**. Hem de protegir el pilot i la confiança, recollir dades, i despres fer millores amb evidencia.

El proper pas correcte no es "fer-ho tot". Es:

1. tancar riscos de dades i confiança;
2. no desestabilitzar el flux principal;
3. acabar el pilot;
4. convertir resultats reals en experiments post-pilot;
5. llavors si, refactoritzar i optimitzar amb criteri.

