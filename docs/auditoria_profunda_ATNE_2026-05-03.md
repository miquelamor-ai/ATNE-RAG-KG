# Auditoria profunda i consultoria ATNE

Data: 2026-05-03  
Abast: revisio de codi local, prompts, pipeline LLM, harness d'avaluacio, fonamentacio pedagogica, UIX, seguretat, sostenibilitat i alineacio amb practiques actuals.

## 1. Veredicte executiu

ATNE te una base ambiciosa i poc habitual per a una app educativa amb IA: no es limita a un xat, sino que defineix perfils, context docent, MECR, DUA, generes discursius, complements, justificacio pedagogica, historial, exportacio i avaluacio. El projecte ja conte una cultura d'avaluacio i documentacio que molts productes d'IA educativa no tenen.

El problema principal no es la idea, sino la concentracio de complexitat. La logica critica viu massa en fitxers grans, el prompt intenta resoldre massa tasques en una sola generacio, el harness no es prou fiable per actuar com a porta de qualitat i hi ha riscos de seguretat/privacitat que s'han de tancar abans d'escalar un pilot real.

La meva lectura clara:

1. **Producte**: la direccio es bona. ATNE ha de continuar sent un "espai de treball docent" i no un chatbot generic.
2. **Arquitectura**: ara mateix es funcional pero fragil. Cal separar domini, serveis, routers, LLM, persistencia, postprocessat i avaluacio.
3. **Prompt**: esta ben pensat i pedagogicament carregat, pero esta sobrecarregat. Per a models barats/gratuits, menys prompt i mes pipeline guanyara.
4. **Pedagogia**: els fonaments son raonables, pero encara no equivalen a validacio experta. Cal una capa de govern pedagogic, no nomes instruccions.
5. **Harness**: no es inutil. Es prometedor, pero avui no es prou efectiu com a control de qualitat de produccio.
6. **Seguretat**: hi ha dos punts prioritaris: ownership dels drafts i sanititzacio de sortides LLM/HTML.
7. **Sostenibilitat**: l'estrategia guanyadora no es "mes agents", sino workflows simples, routing, validacio determinista, evals continus i human-in-the-loop.

## 2. Evidencies locals principals

### Arquitectura i mida

- `server.py` arriba a unes 5.755 linies segons `rg`, amb rutes, integracions, auth, persistencia, PDF/PPTX, adaptacio, metrics i utilitats al mateix modul.
- `ui/atne/pas3.html` arriba a unes 4.941 linies. Fa de renderer, editor, SSE client, exportador, historial, complements, biblioteca, feedback, il·lustracions i autosave.
- `ui/styles.css` passa de 6.400 linies i `ui/app.js` passa de 4.500 linies.
- Hi ha una extraccio parcial encertada a `adaptation/` i `routes/`, pero encara no defineix una arquitectura suficientment neta.

Fitxers clau:

- `adaptation/prompt_builder.py:223` construeix el system prompt.
- `adaptation/orchestrator.py:52` defineix el verificador LLM rapid.
- `adaptation/llm_clients.py:59` concentra aliases i resolucio de models.
- `server.py:3861` exposa `/api/adapt` amb streaming i execucio concurrent.
- `routes/drafts.py:43` i seguents gestionen drafts.
- `routes/adaptations.py:111` mostra un patro millor d'ownership autenticat.
- `ui/atne/js/llm.js:704` reconeix que el `docent_id` local no es auth real.
- `ui/atne/pas3.html:1876`, `3146`, `3235`, `3341`, `3410` mostren injeccions `innerHTML` amb contingut original, adaptat o emmagatzemat.

## 3. Arquitectura de codi

### Diagnosi

El sistema funciona com una aplicacio "organica": s'ha anat resolent necessitat rere necessitat dins de fitxers cada vegada mes grans. Aixo es normal en un pilot, pero ja es el principal fre per fer-lo fiable, rapid i sostenible.

Punts forts:

- FastAPI es una bona tria per aquest tipus de producte.
- Ja hi ha separacio parcial de prompts, clients LLM, orchestrator, postprocess i routers.
- Hi ha documentacio tecnica i pedagogica abundant.
- L'app no depen d'un framework frontend pesat, cosa que pot fer-la lleugera si es modularitza.

Punts febles:

- `server.py` continua sent un monolit. Aixo augmenta regressions i fa dificil provar unitariament.
- Hi ha moltes crides `requests.*` dins de rutes async o fluxos que poden bloquejar l'event loop.
- `/api/adapt` usa una llista compartida `events` entre threads (`server.py:3894`, `3925`). En concurrencia real, es millor una `queue.Queue` o `asyncio.Queue` amb `loop.call_soon_threadsafe`.
- Es crea un `ThreadPoolExecutor` per request (`server.py:3905`). Si molts docents fan adaptacions multinivell, pot multiplicar crides LLM i topar amb quotes o latencia.
- Els indexs globals de rotacio de claus a `adaptation/llm_clients.py:34`, `39`, `44` no son thread-safe.
- La configuracio de models, preus i aliases esta massa codificada en Python. Els preus i disponibilitat de models canvien sovint.

### Arquitectura recomanada

Separacio proposada:

```text
app/
  main.py                     # app factory, middleware, routers
  core/
    config.py                 # env, feature flags, model registry
    security.py               # auth, ownership, cookies, CSP
    logging.py                # structured logs, request ids
  domain/
    profiles.py               # perfil, condicions, subvariables
    adaptation_contracts.py   # seccions, schemas, complements
    pedagogy_rules.py         # decisions pedagogiques versionades
  services/
    adaptation_service.py     # cas d'us: adaptar
    complement_service.py     # generar complements
    feedback_service.py       # rubriques i telemetry
    export_service.py         # PDF/PPTX
  llm/
    registry.py               # models, costos, limits, capacitats
    clients.py                # OpenAI, Gemini, OpenRouter...
    router.py                 # seleccio model per tasca
    validators.py             # validacio determinista
  persistence/
    supabase_client.py        # wrapper async/sync consistent
    repositories.py           # drafts, adaptations, pilot events
  api/
    routes_adapt.py
    routes_drafts.py
    routes_auth.py
    routes_exports.py
```

Principis:

- Un router no hauria de saber com es construeix el prompt.
- Un prompt no hauria de saber com es desa una adaptacio.
- Un client LLM no hauria de decidir politica pedagogica.
- Un postprocess no hauria de tapar sistematicament errors que haurien de fallar l'eval.
- Les decisions de model/cost han de ser configuracio, no codi dur.

## 4. Prompt i qualitat LLM

### El system prompt te sentit?

Si. La proposta te sentit i es mes madura que un prompt generic. El constructor a `adaptation/prompt_builder.py:223` incorpora identitat, llengua, rol, MECR, cataleg d'instruccions, DUA, genere, creuaments de perfil, audiencia i complements. Aixo es bo.

Pero ara el prompt te un problema de "massa responsabilitats":

- adapta el text;
- genera glossari;
- genera esquema visual;
- genera mapa conceptual;
- genera preguntes;
- genera bastides;
- genera activitats;
- genera argumentacio pedagogica;
- genera notes d'auditoria;
- preserva format;
- compleix MECR;
- compleix perfil;
- evita inventar;
- segueix seccions markdown estrictes.

A `adaptation/prompt_builder.py:617` i `626`, l'argumentacio pedagogica i les notes d'auditoria son part del mateix contracte de sortida. Aixo afegeix soroll al producte final i penalitza models petits.

### Recomanacio central

Canviar d'un "gran prompt unic" a un workflow curt i verificable:

1. **Adaptacio base**
   - Entrada: text original, perfil, MECR, genere, instruccions minimes.
   - Sortida: nomes `text_adaptat`.
   - Validacio: longitud, seccions, fidelitat, llengua, artefactes prohibits.

2. **Complements**
   - Entrada: text adaptat, perfil i complements seleccionats.
   - Sortida: JSON o seccions separades per complement.
   - Retry parcial si falla un complement.

3. **Capa docent**
   - Entrada: original, adaptat, perfil, diffs o decisions.
   - Sortida: argumentacio pedagogica, alertes, notes d'auditoria.
   - Aquesta capa no hauria d'apareixer dins del material de l'alumne tret que el docent ho exporti expressament.

4. **Verificacio externa**
   - Un model/jutge diferent o un validador determinista avalua.
   - Si falla, el retry ha d'incloure feedback concret, no nomes regenerar.

### Sortida estructurada

On el proveidor ho permeti, usar JSON Schema o structured outputs. La documentacio d'OpenAI descriu Structured Outputs com una manera de fer que les respostes segueixin un JSON Schema i redueixin claus omeses o enums inventats: <https://platform.openai.com/docs/guides/structured-outputs>.

Per a proveidors que no ho suportin:

- usar tags sentinella estables;
- parser estricte;
- validacio de contracte;
- retry amb error concret;
- mai confiar que Markdown lliure sigui el contracte intern.

## 5. Models barats o gratuïts

La manera de treure el millor partit de models barats no es donar-los un prompt gegant. Es donar-los menys tasques, millors exemples i una xarxa de validacio al voltant.

Estratègia recomanada:

- **Model router per tasca**:
  - adaptacio simple: model gratuit/barat;
  - text llarg o perfil complex: model mes fort;
  - verificacio de fidelitat: model extern al generador;
  - complements senzills: model petit;
  - capa docent/auditoria: model petit o mitja, segons exigencia.

- **Prompt profiles per model**:
  - Gemma/Gemini/OpenRouter: instruccions curtes, exemples positius, contracte simple.
  - GPT o models mes obedients a schema: sortida estructurada i validacio mes estricta.

- **Validacio determinista abans de jutge LLM**:
  - llengua;
  - longitud de frases;
  - max paraules;
  - seccions requerides;
  - complements activats/desactivats;
  - absencia de "com a IA";
  - absencia de preguntes si no tocava;
  - sanititzacio HTML;
  - preservacio de llistes/titols.

- **Retry amb feedback**:
  - el retry ha de rebre "has fallat X, corregeix nomes X".
  - Ara l'orchestrator verifica, pero el segon intent no sembla incorporar feedback concret del jutge.

- **Cache i deduplicacio**:
  - cache per hash de text+perfil+MECR+model+prompt_version;
  - cache de complements separada;
  - cache de verificacio;
  - invalidacio quan canvia `prompt_version`.

- **No apostar cegament per self-hosting**:
  - nomes te sentit si hi ha requisit fort de sobirania, privacitat o volum sostingut.
  - per qualitat/cost, un portfolio de proveidors sol ser millor en fase pilot.

Els preus a `adaptation/pricing.py` han d'anar a una configuracio versionada i revisable, amb "last_checked" i alertes. No recomanaria prendre decisions de model a llarg termini amb preus codificats al codi.

## 6. Harness, evals i recerca actual

### Estat actual

ATNE te un inici d'harness mes serios que la mitjana:

- rubriques LLM (`evaluator_rubrics.py`);
- informes A/B;
- experiments multi-model;
- estadistica amb Bonferroni, alpha de Cronbach i analisi factorial;
- snapshot de contracte de rutes;
- documentacio de biaixos de jutges.

Aixo es molt positiu.

Pero avui el harness no pot ser considerat una porta de qualitat robusta:

- `pytest --collect-only` va quedar bloquejat per un script `scripts/test_openrouter.py` que fa crides de xarxa i `sys.exit` en import.
- `tests/test_instruction_filter.py` sembla mes un script de prints que un test amb asserts, i esta desalineat amb les claus actuals de stats.
- `tests/snapshot_contract.py --check` falla per drift de rutes i signatures. Pot ser que el canvi sigui legitim, pero si el baseline no s'actualitza de manera governada, el test deixa de ser senyal.
- El verificador de `adaptation/orchestrator.py:52` usa el mateix `active_model` que genera. Aixo introdueix biaix de self-evaluation i errors correlacionats.

### Que diu la practica actual?

OpenAI recomana evals continus sobre canvis, datasets amb casos tipics, limit, adversarials i labels humans experts. Tambe assenyala que els LLMs son millors discriminant entre opcions que generant judicis oberts, de manera que comparacions parellades, classificacio i scoring per criteris solen ser mes fiables: <https://platform.openai.com/docs/guides/evaluation-best-practices>.

Anthropic recomana començar per workflows simples i composables, i augmentar complexitat nomes quan cal. Tambe descriu routing com a patró util quan hi ha categories distintes i models petits/grans segons dificultat: <https://www.anthropic.com/engineering/building-effective-agents>.

Els estudis de LLM-as-judge mostren que jutges forts poden aproximar preferencies humanes, pero tenen biaixos de posicio, verbositat i autoavaluacio: <https://huggingface.co/papers/2306.05685>.

Per RAG i groundedness, RAGAS i ARES convergeixen en dimensions com faithfulness, context relevance/precision i answer relevance. RAGAS defineix faithfulness com claims suportats pel context, i ARES avalua context relevance, answer faithfulness i answer relevance amb una petita base humana per calibrar: <https://docs.ragas.io/en/v0.3.9/concepts/metrics/available_metrics/faithfulness/> i <https://aclanthology.org/2024.naacl-long.20/>.

### Harness v3 recomanat

Crear un sistema d'avaluacio amb quatre capes:

1. **Tests de contracte**
   - cap crida de xarxa en import;
   - `pytest.ini` amb `testpaths = tests`;
   - marks `unit`, `integration`, `network`, `llm_live`;
   - fixtures amb respostes LLM congelades;
   - snapshot update explicit i revisat.

2. **Validators deterministes**
   - contracte de sortida;
   - seccions obligatories/prohibides;
   - max paraules/frase;
   - no HTML perillos;
   - complements exactes;
   - llengua;
   - estructura de genere;
   - preservacio de dades curriculars critiques.

3. **LLM-as-judge calibrat**
   - jutge diferent del generador;
   - ordre A/B randomitzat;
   - criteris independents;
   - justificacio curta amb evidencies;
   - deteccio de biaix de longitud;
   - intervals de confianca;
   - comparacio amb humans.

4. **Gold set pedagogic**
   - 60-100 casos inicials;
   - estratificats per perfil, etapa, MECR, materia, genere i longitud;
   - etiquetats per docents/experts;
   - ampliats amb casos reals anonimitzats del pilot.

Rubrica v3:

- Separar **fidelitat curricular** com a criteri porta. Si suspèn fidelitat, l'adaptacio no pot aprovar encara que sigui clara.
- Mantenir qualitat pedagogica com a segon bloc.
- Mantenir usabilitat docent com a tercer bloc.
- No barrejar fidelitat amb "adequacio pedagogica" si l'analisi factorial ja indica que B1 mesura una dimensio diferent (`docs/estadistica/interpretacio_estadistica.md:86`).

## 7. Agents i auto-millora

No recomano convertir ATNE en una arquitectura multiagent autonoma per defecte. La millor versio d'ATNE hauria de ser un workflow controlat amb passos petits, observables i recuperables.

Agents si:

- hi ha tasques obertes amb nombre de passos desconegut;
- hi ha eines externes;
- hi ha sandbox;
- hi ha human approval;
- hi ha evals i traçabilitat.

Workflows si:

- adaptar text;
- generar complements;
- verificar sortida;
- exportar;
- registrar feedback;
- optimitzar prompt offline.

El document `docs/AGENT_DESIGN.md` va en bona direccio quan parla d'auto-millora post-pilot amb aprovacio humana. La linia correcta es:

- cap canvi automatic a produccio;
- proposta d'hipotesis;
- execucio sobre gold set;
- comparativa amb baseline;
- revisio humana;
- merge versionat.

GEPA i prompt optimization per reflexio son prometedors, pero nomes tenen sentit si ATNE disposa abans d'un eval set fiable. GEPA no arreglara un harness feble; l'amplificara.

## 8. Pedagogia

### Fortaleses

ATNE esta ben orientat pedagogicament:

- DUA/UDL;
- Lectura Facil;
- MECR;
- genere discursiu;
- carrega cognitiva;
- bastides;
- perfils i creuaments;
- argumentacio pedagogica;
- feedback docent.

CAST UDL 3.0 posa mes pes en barreres, biaixos i sistemes d'exclusio, no nomes en deficits individuals. ATNE hauria d'alinear-se explicitament amb aquest enfocament: <https://udlguidelines.cast.org/more/downloads/>.

UNESCO insisteix en un enfocament human-centered, segur, equitatiu i significatiu per a GenAI en educacio: <https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research>.

### Riscos pedagogics

- Els perfils poden llegir-se com etiquetes diagnostics fixes. Cal passar de "alumne TEA/TDAH/dislexia" a "barreres, necessitats, suports i objectiu didactic".
- Els documents locals reconeixen que els perfils son il·lustratius i no validats externament. Aixo s'ha de mantenir visible fins que hi hagi validacio.
- L'adaptacio pot rebaixar massa contingut. Per AACC/enriquiment, aixo es especialment greu: adaptar no vol dir simplificar.
- Traduccions/glossaris per nouvinguts poden ser falsos o culturalment inadequats si el model no domina la L1.
- Les decisions de MECR poden confondre competència linguistica amb nivell curricular.
- Grups multinivell necessiten una modelitzacio propia, no nomes fer diverses versions en paral·lel.

### Millora pedagogica prioritaria

Crear una **matriu de traçabilitat pedagogica**:

```text
Regla / instruccio
  perfil o barrera
  etapa i materia on aplica
  objectiu pedagogic
  evidencia o font
  risc si s'aplica malament
  exemple bo
  exemple dolent
  validador determinista possible
  estat: pilot / validada / retirada
```

I un comite curt de validacio:

- 1 expert DUA/inclusio;
- 1 especialista llengua/lectura facil;
- 1 docent de primaria;
- 1 docent de secundaria;
- 1 orientador/a o psicopedagog/a;
- revisio externa puntual per perfils concrets.

## 9. UIX

### Que funciona

La UIX te una decisio encertada: ATNE no es un xat. Es un flux docent:

1. triar o crear perfil;
2. introduir/generar text;
3. adaptar, revisar, comparar, complementar, exportar i desar.

Aixo encaixa amb la feina real del docent. Tambe es bo que l'app guardi context, mostri biblioteca, permeti refinament i exportacio.

### Que cal millorar

- `pas3.html` ha esdevingut massa gran per mantenir qualitat.
- Massa estat viu a `localStorage`: text original, perfil, adaptacio, cache, draft, docent_id, complements, id d'adaptacio.
- El material de l'alumne i la capa docent no estan prou separats conceptualment.
- El risc XSS es real si contingut LLM o guardat entra a `innerHTML` sense sanititzacio.
- La dependencia CDN `html2pdf.js` continua carregada a `pas3.html:31` tot i comentaris posteriors que diuen que s'ha abandonat. Aixo es soroll tecnic i risc de supply chain/CSP.

### UIX recomanada

Separar `pas3` en moduls:

```text
pas3/
  state.js
  render-markdown.js
  sanitize.js
  sse-adaptation.js
  editor-history.js
  complements.js
  feedback.js
  export.js
  library.js
  illustrations.js
```

Separar vistes:

- **Text de l'alumne**: net, exportable, sense notes internes.
- **Vista docent**: justificacio, advertiments, criteris, canvis, feedback.
- **Vista qualitat**: contracte, alertes, puntuacions, traça de model/prompt.

UX de qualitat:

- mostrar "necessita revisio" quan falla fidelitat o hi ha baixa confiança;
- permetre "acceptar amb canvis" i capturar edit distance;
- no demanar massa ratings manuals si es poden inferir senyals d'ús: exportat, copiat, editat, descartat, regenerat.

## 10. Seguretat, privacitat i compliment

### Risc 1: ownership de drafts

`routes/adaptations.py` calcula un `docent_id` esperat a partir de l'usuari autenticat i verifica ownership (`routes/adaptations.py:111-119`). Aquest es el patro correcte.

`routes/drafts.py`, en canvi, confia en `docent_id` de query/body. Aixo es especialment preocupant perquè `ui/atne/js/llm.js:704-705` diu explicitament que el `docent_id` localStorage no es auth real. Per tant:

- un usuari podria manipular `docent_id`;
- si coneix o endevina ids, podria accedir/modificar drafts d'un altre docent;
- encara que Supabase tingui filtres, l'API esta exposant un patró insegur.

Prioritat: alta.

Correccio:

- totes les rutes de drafts han de rebre `Request`;
- calcular `expected_docent_id(request)`;
- ignorar o validar estrictament qualsevol `docent_id` client-side;
- aplicar el mateix patró que `routes/adaptations.py`;
- idealment activar RLS a Supabase amb subject autenticat, no nomes filtre REST.

### Risc 2: sortides LLM com HTML

OWASP LLM05:2025 "Improper Output Handling" avisa que sortides LLM sense validacio/sanititzacio poden acabar en XSS, CSRF, SSRF, escalada o execucio remota: <https://genai.owasp.org/llmrisk/llm05-supply-chain-vulnerabilities/>.

ATNE renderitza contingut original, adaptat, complements i guardats amb `innerHTML` en molts punts. Encara que hi hagi `escapeHtml` i conversio Markdown, cal una politica unica:

- DOMPurify o sanititzador equivalent al client;
- sanititzacio server-side abans de persistir HTML;
- CSP estricta;
- no permetre `<script>`, event handlers, `javascript:`, iframes no autoritzats;
- diferenciar Markdown intern de HTML exportable.

### Risc 3: consentiment i DPIA

Els fitxers `pas1`, `pas2` i `pas3` indiquen que el consent gate esta desactivat per revisio legal (`ui/atne/pas1.html:12`, `pas2.html:12`, `pas3.html:12`). Pero la DPIA descriu un flux amb consentiment. Aixo no vol dir que el pilot sigui il·legal, pero si que hi ha una inconsistencia documental i operativa.

Correccio:

- decidir si el pilot exigeix consentiment explicit o base alternativa;
- alinear DPIA, UI i backend;
- registrar estat de consentiment de manera verificable si s'usa;
- minimitzar dades personals i evitar noms d'alumnes en prompts.

### AI Act

L'AI Act considera d'alt risc sistemes educatius que determinen acces/admissio, avaluen resultats d'aprenentatge, determinen nivell educatiu o monitoritzen conductes d'examen: <https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3>.

ATNE pot mantenir-se fora d'aquesta categoria si queda clar que:

- no avalua alumnes;
- no decideix nivell educatiu;
- no assigna itineraris;
- no substitueix criteri docent;
- nomes assisteix el docent en generar materials.

Tot i aixi, per excel·lencia i confiança, ATNE hauria d'adoptar controls voluntaris d'alt risc: logs, traçabilitat, validacio, humans al centre, gestio de riscos i documentacio.

## 11. Pla d'accio prioritzat

### P0 - Aquesta setmana

1. **Tancar ownership de drafts**
   - portar `_expected_docent_id` i `_check_ownership` a un modul compartit;
   - aplicar-ho a totes les rutes de drafts;
   - deixar de confiar en `localStorage` com a identitat.

2. **Sanititzar HTML**
   - afegir DOMPurify o equivalent;
   - sanititzar tot LLM Markdown/HTML abans d'`innerHTML`;
   - sanititzar abans de persistir `adapted_html`.

3. **Fer que pytest torni a ser fiable**
   - moure `scripts/test_openrouter.py` fora del patró de test o protegir amb `if __name__ == "__main__"`;
   - afegir `pytest.ini`;
   - prohibir network en tests unitaris;
   - convertir `tests/test_instruction_filter.py` en asserts reals.

4. **Corregir streaming concurrent**
   - substituir `events` compartit per `queue.Queue`;
   - capturar excepcions de futures;
   - limitar concurrencia global LLM.

5. **Separar sortida alumne/docent**
   - no fer obligatories `Argumentació pedagògica` i `Notes d'auditoria` dins del document de l'alumne.

### P1 - 2 a 4 setmanes

1. Refactoritzar `server.py` cap a app factory, routers i serveis.
2. Crear `llm/registry.py` amb capacitats, costos, limits, structured-output support i data `last_checked`.
3. Implementar pipeline en 3 fases: adaptacio, complements, auditoria.
4. Crear validators deterministes.
5. Fer jutge extern al generador i retry amb feedback concret.
6. Modularitzar `pas3.html`.
7. Crear gold set inicial amb 60-100 casos.
8. Reformular rubrica v3 amb fidelitat curricular com a porta.

### P2 - 1 trimestre

1. Validacio pedagogica externa per perfil i per instruccio.
2. Pilot amb metrics d'us real: edit distance, exportacio, descart, regeneracio, temps fins a resultat util.
3. Mesura d'impacte educatiu limitada pero real: comprensio abans/despres o tasques breus amb consentiment.
4. Observabilitat de cost/latencia/qualitat per model.
5. Playwright visual smoke tests per desktop/tablet/mobil.
6. CSP, SRI o assets locals per dependències frontend.
7. Govern de prompt: versionat, changelog, eval abans de merge.

## 12. Arquitectura objectiu de qualitat

Per convertir ATNE en una app de referencia, la unitat de qualitat no ha de ser "la resposta sembla bona". Ha de ser:

```text
Entrada docent
  -> normalitzacio i deteccio de risc
  -> seleccio de perfil/regles
  -> adaptacio base
  -> validacio determinista
  -> verificacio pedagogica/fidelitat
  -> retry parcial si cal
  -> complements separats
  -> sanititzacio
  -> vista alumne
  -> vista docent
  -> feedback i telemetry
  -> eval continu
```

ATNE hauria de mostrar internament per cada adaptacio:

- model;
- prompt_version;
- rules_version;
- validators pass/fail;
- retry count;
- cost estimat real;
- latencia;
- confidence/fidelitat;
- avisos per al docent;
- si el docent ha editat/exportat/descartat.

## 13. Resposta directa a les preguntes

### L'estructura i arquitectura son fiables, robustes i lleugeres?

Encara no. Son potents pero massa acoblades. El sistema es funcional per pilot, no per escala robusta. La solucio no es reescriure-ho tot, sino extreure serveis i contractes a partir dels punts ja existents.

### La qualitat amb LLMs barats/gratuits es pot millorar?

Si, molt. No amb prompts mes llargs, sino amb pipeline, routing, validators, retry amb feedback, complements separats, cache i gold set.

### El system prompt esta ben dissenyat?

La base es bona. El problema es que fa massa coses. Cal dividir-lo i reduir la carrega cognitiva per al model. Especialment, separar material alumne de justificacio docent.

### Pedagogicament es coherent?

Te coherencia i fonaments, pero necessita validacio externa i una matriu de traçabilitat. El risc mes gran es convertir perfils en etiquetes o simplificar massa el contingut.

### La UIX es rigorosa amb l'objectiu?

La decisio de flux docent es molt bona. La implementacio necessita modularitzacio, sanititzacio i separacio mes clara entre alumne/docent/qualitat. Ara mateix la UI pot funcionar, pero es fragil de mantenir.

### El harness es actual, avançat i efectiu?

Conceptualment, esta per sobre de molts projectes. Operativament, encara no. Amb tests que fallen en collection, snapshots desactualitzats i jutge igual al generador, no pot actuar com a garantia. Convertit a harness v3, pot ser un avantatge competitiu real.

## 14. Fonts externes consultades

- OpenAI, Evaluation best practices: <https://platform.openai.com/docs/guides/evaluation-best-practices>
- OpenAI, Structured Outputs: <https://platform.openai.com/docs/guides/structured-outputs>
- Anthropic, Building effective agents: <https://www.anthropic.com/engineering/building-effective-agents>
- CAST, UDL Guidelines 3.0: <https://udlguidelines.cast.org/more/downloads/>
- UNESCO, Guidance for generative AI in education and research: <https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research>
- EU AI Act Annex III, Education and vocational training: <https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3>
- OWASP GenAI, LLM01 Prompt Injection: <https://genai.owasp.org/llmrisk/llm01-prompt-injection/>
- OWASP GenAI, LLM05 Improper Output Handling: <https://genai.owasp.org/llmrisk/llm05-supply-chain-vulnerabilities/>
- RAGAS, Faithfulness metric: <https://docs.ragas.io/en/v0.3.9/concepts/metrics/available_metrics/faithfulness/>
- RAGAS, Response Relevancy metric: <https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/answer_relevance/>
- ARES, Automated RAG Evaluation System, ACL Anthology: <https://aclanthology.org/2024.naacl-long.20/>
- Zheng et al., Judging LLM-as-a-judge with MT-Bench and Chatbot Arena: <https://huggingface.co/papers/2306.05685>
- GEPA, Reflective Prompt Evolution Can Outperform Reinforcement Learning: <https://huggingface.co/papers/2507.19457>
