# Handoff ATNE → mineriaRAG — 2 instruments futurs nous

**Origen**: sessió ATNE 2026-05-25 (Fase A en curs).
**Destinatari**: sessió mineriaRAG.
**Objectiu**: comunicar dues decisions pedagògiques que **amplien el corpus FJE de 35 a 37 instruments**.

---

## Context

Durant la fusió canònica de `write-opinio` (Fase A pilot 3) han sorgit dues qüestions pedagògiques de fons que **NO es podien tancar en fals**. La sessió ATNE ha fet **recerca exhaustiva** (NotebookLM MALL + NotebookLM Marc Literacitat IA + Agents acadèmics + WebSearches) i Miquel ha pres dues decisions estratègiques.

Documents complets a:
- [parking_opinio_vs_preferencies_2026-05-25.md](parking_opinio_vs_preferencies_2026-05-25.md) — anàlisi de Q1 amb autors i postures contrastades.
- [parking_contrarelat_odi_genere_nou_2026-05-25.md](parking_contrarelat_odi_genere_nou_2026-05-25.md) — anàlisi de Q2 amb tradició ignasiana, ciutadania global i referent català.

---

## Decisió 1 — Nou instrument `expressar-preferencies` (Q1)

### El context

El gènere `write-opinio` exclou pre-A1 ("massa abstracte"). Vam detectar que:
- Si la rúbrica descriu **lectura**, un pre-A1 pot llegir un text d'opinió amb suport visual.
- Però **preferència ≠ opinió argumentativa** (BICS vs CALP, segons Cummins).
- Miquel proposa una **tríada cognitiva-discursiva** validada acadèmicament:
  - **PREFERÈNCIA**: afinitat, escollir, agradar; subjectivitat NO evidenciable.
  - **OPINIÓ**: valorar, judici intuïtiu; subjectivitat per manca d'evidència.
  - **ARGUMENTACIÓ**: defensar amb evidència; apropant-se a l'objectivitat.

Validació acadèmica: Kant *Crítica del Judici* §7, Habermas (3 pretensions de validesa), Toulmin (claim vs argument), Kuhn 1991 (desenvolupament infantil), Common Core W.K.1 literal "opinion **or** preference", Hillocks (opinion vs argument writing CCSS).

### La decisió

**Postura D (síntesi)**: crear `expressar-preferencies` com a instrument autònom per a pre-A1 (i possiblement A1), diferenciat del `write-opinio` que es manté a 5 nivells (A1-C1+).

### Característiques previstes (a validar)

```yaml
modul: M3
titol: "Expressar preferències"
tipus: instrument
categoria_principal: generes
descripcio: "Precursor cognitiu-discursiu del gènere argumentatiu. Expressió de preferència valorativa amb suport multimodal i mediació adulta. Per a pre-A1 i A1 — fase BICS prèvia al CALP argumentatiu."
mecr_range: [pre-A1, A1]
agent_roles: [adapter, generator]
genre_key: expressar-preferencies
translanguaging: true
multimodal: true  # OBLIGATORI
moduls_relacionats: [M3]
variables_configurables:
  fase_lectora: [logografica, alfabetica_emergent, alfabetica_fluida]
```

- **HCL primària**: **Valorar / Preferir** (BICS). Evolucionarà cap a **Argumentar** (CALP) a A2+ via `write-opinio`.
- **Estructura típica**: pictograma de cara emocional + paraula clau + pictograma del referent + opcional "perquè" amb raó visual/oral.
- **Pont funcional**: a A1, l'alumne pot saltar cap a `write-opinio` ("Crec que…").
- **Cas col·laboratiu pertinent**: converses literàries Infantil, "Què hauries fet tu?" del MALL MOPI/PIN, glossari col·laboratiu B1+ (paral·lel).

### Validació externa pendent

- Docents FJE Educació Infantil (P3-P5) per validar pedagògicament.
- Equip MALL FJE per confirmar coherència amb MOPI/PIN.
- Possible consulta a Olga Esteve (UPF) o Joaquim Dolz (Ginebra).

---

## Decisió 2 — Nou instrument `write-contrarelat-odi` (Q2)

### El context

Durant la investigació sobre la dimensió crítica del gènere argumentatiu (fal·làcies, fake news, discurs d'odi), Miquel pregunta si el **contrarelat de l'odi** pot ser un gènere propi i no només una dimensió de l'opinió.

Recerca exhaustiva sobre 6 marcs convergents:

1. **Tradició ignasiana**: CG36 (reconciliació triple), Fratelli tutti (Francesc 2020), PPI (1993), UAP 2019-2029, Sosa-Rio (2017) "ciutadans globals reconciliadors", Sosa (2019) polarització = pecat estructural, Adolfo Nicolás (2010) "globalització de la superficialitat".
2. **Referent català doctoral**: ⭐ **Albert Izquierdo Grau, UAB 2019** (tesi *Contrarelats de l'odi a l'ensenyament i aprenentatge de les Ciències Socials*, Excel·lent Cum Laude, dir. **Antoni Santisteban / GREDICS**). **Model conceptual ja existent per a l'ESO**.
3. **Institucional internacional**: Consell d'Europa (*Bookmarks* 2014/2020, *We CAN!* 2017, CM/Rec(2022)16), UNESCO (*Think Critically, Click Wisely!* MIL 2021), Decret 175/2022 (competència ciutadana).
4. **Filosòfic-acadèmic**: Walton *Argumentation Schemes* (1996, 2008), Toulmin (refutació), Susan Benesch (Dangerous Speech Project) — **taxonomia 8 estratègies**: empatia, fact-checking, humor, vergonya, advertència de conseqüències, to, identificació tribal, redirecció.
5. **Ciutadania global**: UNESCO GCED, Oxfam GCC, Henry & Lo (2020) *From deliberation to counter-narration*.
6. **NLP / tecnològic**: Fondazione Bruno Kessler (Marco Guerini, Sinem Tekiroğlu) — dataset CONAN per generació automàtica.

### La decisió

**Opció A.1 acceptada**: **gènere propi únic** `write-contrarelat-odi` (nom a confirmar) **amb modalitat configurable**:
- **Counterspeech directe** (resposta puntual a un discurs concret).
- **Counter-narrative indirecte** (canvi de marc del debat).

**NO** són dos gèneres separats. La distinció CoE entre counterspeech i alternative speech queda capturada com a **dimensió interna "Modalitat"**.

### 4 dimensions civils noves del gènere (aportació Miquel)

- **Participació democràtica**: contrarelat com a pràctica deliberativa.
- **Inclusió**: contrarelat com a desactivació de marcs excloents.
- **Diversitat**: reconeix multiplicitat de veus.
- **Universalitat**: apel·lació a drets humans universals + Fratelli tutti.

### Característiques previstes (a validar)

```yaml
modul: M3
titol: "Escriure un contrarelat de l'odi"
tipus: instrument
categoria_principal: generes  # o mediacio? a decidir
descripcio: "Gènere argumentatiu específic per construir respostes a discursos d'odi (counterspeech directe i counter-narrative indirecte). Integra discerniment ignasià, ciutadania global, dimensions de reconciliació, inclusió, diversitat i universalitat."
mecr_range: [A1, A2, B1, B2, C1]  # no aplicable a pre-A1
agent_roles: [adapter, generator]
genre_key: contrarelat-odi
translanguaging: true
multimodal: false  # contingut argumentatiu textual
moduls_relacionats: [M3, M8]  # M8 = Governança i Seguretat (ciutadania)
variables_configurables:
  modalitat: [counterspeech-directe, counter-narrative-indirecte]
  fase_lectora: [alfabetica_emergent, alfabetica_fluida]
```

### Passos proposats (8)

1. **Identificació del discurs d'odi** (Izquierdo Grau + Decret 175/2022).
2. **Discerniment** (respondre? com? quan?) — Paradigma Pedagògic Ignasià + UAP.
3. **Composició de lloc inclusiva** (empatia amb víctima i emissor) — EE 47 + Benesch + Fratelli tutti.
4. **Fact-checking / Cerca de la veritat** — Benesch + tradició ignasiana.
5. **Construcció de la resposta** segons modalitat (counterspeech directe / counter-narrative indirecte amb apel·lació a universalitat) — CoE *We CAN!* + Fratelli tutti.
6. **Crida a l'acció democràtica i comunitària** — 4 C's + Henry & Lo (2020).
7. **Criteris transversals** — Inclusió · diversitat · no-atacs personals · fonts verificades · to respectuós.
8. **Autoavaluació metacognitiva (Examen ignasià)** — He respost amb justícia? He buscat reconciliació? He estat fidel a la veritat?

### Valor diferencial FJE (únic al món)

Cap dels marcs internacionals (CoE, UNESCO, NLP, GREDICS) integra:
1. **Fonament antropològic Fratelli tutti** (no només drets humans procedimentals).
2. **Discerniment ignasià** com a metodologia.
3. **Examen ignasià** com a avaluació.
4. **4 dimensions civils** com a horitzó pedagògic transversal.

Seríem un dels primers currículums escolars del món que codifica el contrarelat com a gènere — **innovació pedagògica documentable**.

### Cautela necessària

Tractar el marc ignasià com a **arquitectura pedagògica** (PPI, examen, magis) i **NO com a contingut confessional explícit**. El gènere ha de funcionar en aules amb alumnat no creient. Les estratègies Benesch operen com a tàctiques discursives dins l'estructura PPI.

### Validació externa pendent

- ⭐ Contactar **Albert Izquierdo Grau** (UOC actualment) — té el model conceptual de referència.
- Contactar **GREDICS UAB** (continuïtat post-Santisteban).
- Possible consulta al **CAC / eduCAC** per a la part de discurs d'odi i mediàtica.

---

## Impacte arquitectònic al corpusFJE

Si mineriaRAG accepta aquests dos instruments, el corpus passa de **35 a 37 instruments**.

| Estat | Total |
|---|---|
| Inventari original handoff 2026-05-25 (matí) | 35 (22 gèneres + 12 mediació + 1 adapt-document) |
| **+ `expressar-preferencies`** (Q1) | 36 |
| **+ `write-contrarelat-odi`** (Q2) | 37 |

Aquests **no formen part de la Fase A/B/C actuals**. Són **instruments addicionals futurs** que es treballaran després de la consolidació dels 35 actuals.

---

## Preguntes a mineriaRAG

1. **Arquitectura del corpus admet créixer a 37 instruments?** Cal afegir-los a la spec `corpus-spec.md`?
2. **Categorització**:
   - `expressar-preferencies`: `categoria_principal: generes` (precursor del gènere argumentatiu)?
   - `write-contrarelat-odi`: `categoria_principal: generes` o `mediacio` (per la funció social de prevenció)?
3. **Quan els pugem al corpusFJE?** Després de Fase C (post-22 de juny)? O abans?
4. **`moduls_relacionats`**:
   - `expressar-preferencies` → `[M3]`?
   - `write-contrarelat-odi` → `[M3, M8]` (M8 = Governança i Seguretat / ciutadania)?
5. **`build_skills.py`**: poden els nous instruments fer servir el mateix pipeline sense canvis?
6. **Validació externa abans de pujar**: ho coordinem qui? ATNE contacta Izquierdo Grau o ho fa mineriaRAG?

---

## Material per consultar

- **Parking opinió/preferències complet**: `ATNE/docs/parking_opinio_vs_preferencies_2026-05-25.md` (39 referències acadèmiques integrades).
- **Parking contrarelat complet**: `ATNE/docs/parking_contrarelat_odi_genere_nou_2026-05-25.md` (recerca exhaustiva en 4 capes: filosofia + institucional + ignasià + referent català).
- **Tesi referent**: Izquierdo Grau, A. (2019). *Contrarelats de l'odi a l'ensenyament i aprenentatge de les Ciències Socials*. UAB. [TDX](https://www.tdx.cat/handle/10803/669789).
- **Manual CoE referent**: *We CAN! Taking Action against Hate Speech through Counter and Alternative Narratives*. [Council of Europe](https://rm.coe.int/wecan-eng-final-23052017-web/168071ba08).
- **Tipologia Benesch**: 8 estratègies de counterspeech (Dangerous Speech Project).

---

## Estat actual a ATNE (a la redacció original — superat per secció següent)

- Fase A en curs: pilot 3 (`write-opinio`) **completat amb validació NotebookLM**. Pilot 4 (`generate-bastides-lectura`) pendent.
- Aquests dos instruments futurs (`expressar-preferencies` + `write-contrarelat-odi`) **NO bloquegen la consolidació dels 33 actuals**.
- Decisió pedagògica de Miquel: **continuar amb Fase A i B/C amb els 35 actuals**, i tractar aquests 2 nous després.

---

## ⭐ Actualització post-resposta mineriaRAG (2026-05-25 nit)

Aquesta secció documenta tot el que ha canviat **després** de la redacció inicial del handoff, gràcies a la resposta de mineriaRAG i a la sessió ATNE nit.

### A. Resposta de mineriaRAG (rebuda i incorporada)

**A.1 Aclariment numèric** (gràcies, era ambigu a la redacció inicial):
- Total post-decisions: **35 → 37 instruments** (no 33→35). Els 35 originals + 2 nous = 37.

**A.2 Llum verda als 2 nous instruments**:
- mineriaRAG accepta procedir amb `expressar-preferencies` i `write-contrarelat-odi` **"com si validats"**, condicionat a **citar les fonts al cos del M\*.md**. La citació substitueix funcionalment el segell de l'autor.
- Fonts a citar (literal al M\*.md):
  - `expressar-preferencies` → Common Core W.K.1 + Kant *Crítica del Judici* §7 + Habermas (3 pretensions de validesa) + Toulmin 1958 + Kuhn 1991.
  - `write-contrarelat-odi` → Izquierdo Grau (UAB 2019) + GREDICS (Santisteban).
- **Desbloca**: la construcció dels 2 instruments es pot fer **abans de Fase C** (no cal esperar validació externa Izquierdo Grau + GREDICS + docents FJE Infantil + equip MALL).

**A.3 Encaix Fase B (opció d híbrida)**:
- `expressar-preferencies` → entra a Fase B com a lot propi o annexat al **lot B.6 (expressius/dialògics)**. Senzill, cobreix buit clar.
- `write-contrarelat-odi` → **últim lot pre-Fase C**. Complex, mereix concentració, permet incorporar feedback intermedi (incloent possible retorn d'Izquierdo Grau si arriba).

### B. Resposta a les "Preguntes a mineriaRAG" originals

Repreneu la secció anterior — la majoria queden resoltes:

| Pregunta original | Resposta de mineriaRAG |
|---|---|
| 1. Corpus admet 37 instruments? | ✅ Sí. Pendent: spec `corpus-spec.md` ha d'actualitzar el comptador. |
| 2. Categorització | `expressar-preferencies` → `generes`. `write-contrarelat-odi` → `generes` (amb modalitat). |
| 3. Quan els pugem? | ✅ **Abans de Fase C**: preferences a lot B.6, contrarelat com a últim lot pre-Fase C. |
| 4. `moduls_relacionats` | Confirmar amb mineriaRAG: probablement [M3] i [M3, M8]. |
| 5. `build_skills.py` admet | ✅ Sí, però veure secció C (pregunta oberta nova). |
| 6. Coordinació validació externa | Esdevé **opcional** gràcies a A.2. Si arriba, s'incorpora; no bloqueja. |

### C. Novetats arquitectòniques del Pilot 4 (per a mineriaRAG)

El pilot 4 (`generate-bastides-lectura`) s'ha construït i validat amb NotebookLM (sí-amb-correccions-menors) la mateixa nit. Han emergit **dues decisions arquitectòniques noves** que afecten el patró M\*.md canònic i `build_skills.py`:

**C.1 Patró `cross_source` intra-pipeline (NOU)**:

El pilot 4 introdueix el **primer descriptor `cross_source` que no apunta al text font** sinó a **l'output d'un altre complement del pipeline**:

```
| 4.2 No duplicar `preguntes_comprensio` | cross_source | sí (output de preguntes_comprensio si actiu) | comparar semànticament: cap pregunta de bastides ha de coincidir amb cap pregunta del complement |
```

NotebookLM qualifica això d'**"innovació arquitectònica necessària"** i recomana fixar-ho com a **patró canònic per a tots els futurs instruments de mediació amb dependències intra-pipeline**.

**Diferència amb el `cross_source` clàssic** (notícia 7.4 Fidelitat, glossari 5.5):
- Clàssic: el descriptor depèn del **text font original**.
- Nou (intra-pipeline): el descriptor depèn de **l'output d'un altre complement actiu del pipeline**.

**Implicacions per a `build_skills.py`**:
- Cal poder llegir `output[other_complement]` durant la validació, no només `source_text`.
- Cal poder marcar dependències condicionals (només actives si l'altre complement està actiu).

**C.2 Pregunta oberta nova per a mineriaRAG (decisió arquitectònica pendent)**:

Quan `bastides` i `preguntes_comprensio` estan actius simultàniament i `build_skills.py` detecta duplicitat semàntica:

> **¿`build_skills.py` ha de generar feedback condicional al docent (avís de duplicitat), o és millor que l'IA ho resolgui silenciosament per disseny?**

És una decisió de filosofia de pipeline que afectarà **tots els futurs instruments de mediació amb dependència intra-pipeline**. Demanem el criteri de mineriaRAG abans de generalitzar el patró.

**C.3 Patró d'absència de fidelitat per a instruments d'orientació**:

També validat pel pilot 4: els instruments que **orienten un procés** (bastides, en aquest cas el procés lector) **no han de tenir descriptor de fidelitat al text font** (a diferència de notícia 7.4 i glossari 5.5). NotebookLM ho qualifica de decisió "valenta i sòlida".

Aplica a tots els futurs instruments de mediació que no reformulin contingut.

### D. Estat consolidat post-sessió (substitueix l'estat redactat inicialment)

| Pilot Fase A | Estat |
|---|---|
| 1. `write-noticia` | ✅ validat + a corpusFJE |
| 2. `generate-glossari` | ✅ validat + a corpusFJE |
| 3. `write-opinio` | ✅ validat NotebookLM (sí-amb-correccions-menors) · 🔴 pendent push a corpusFJE |
| 4. `generate-bastides-lectura` | ✅ validat NotebookLM (sí-amb-correccions-menors) · 🔴 pendent push a corpusFJE |

**4 pilots Fase A a `origin/main` (ATNE)**. El patró M\*.md canònic queda consolidat amb 4 exemples diversos (gènere informatiu, mediació lèxica, gènere argumentatiu, mediació cognitiva). Es pot replicar mecànicament als 31 instruments restants de Fase B amb confiança.

### E. Coordinació pendent

| Acció | Responsable |
|---|---|
| Push de pilots 3+4 al `corpusFJE` (skills/genres/write-opinio + skills/mediacio/generate-bastides-lectura) | Miquel coordina amb mineriaRAG |
| Resolució de la pregunta C.2 (feedback `build_skills.py`) | mineriaRAG + Miquel |
| Decisió arquitectònica de generalització del patró `cross_source` intra-pipeline | mineriaRAG documenta a corpus-spec |
| Construcció dels 2 instruments nous segons encaix Fase B híbrid | Properes sessions ATNE |
