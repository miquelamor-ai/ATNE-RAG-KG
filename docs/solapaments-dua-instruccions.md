# Estudi de solapaments: blocs DUA vs catàleg d'instruccions

Data: 2026-04-19
Autor: Claude (agent analític), sota encàrrec del Miquel Amor (FJE)
Abast: detectar duplicacions, similituds i contradiccions entre dos senyals que
arriben al prompt de l'LLM a `build_system_prompt()`:

1. El bloc DUA (Accés / Core / Enriquiment) llegit del corpus.
2. El catàleg de 84 instruccions efectives a `instruction_catalog.py`.

## 1. Resum executiu

- **12 directrius DUA analitzades** (3 blocs × 4-5 bullets cada un).
- Solapaments detectats: **9 SIMILARS o IDÈNTICS**, **2 COMPLEMENTARIS**, **1 ÚNIC DUA**. Zero CONTRADICTORIS.
- **Veredicte: duplicació PARCIAL però significativa al bloc Accés** (5 de 5 bullets ja coberts pel catàleg, amb gradació MECR més fina); **baixa al Core** (4 de 4 coberts, però la formulació és prou breu per funcionar com a resum útil); **residual a Enriquiment** (1 contingut únic real: "fronteres del coneixement, debats oberts", que ja és a H-12).
- **Recomanació global**: el bloc DUA actua avui com a **etiqueta de registre** ("Lectura Fàcil extrema" / "Llenguatge Clar" / "Màxima complexitat") més que no pas com a font d'instruccions operatives noves. Les directrius operatives ja són al catàleg amb gradació MECR. Es pot:
  - (a) Reduir el bloc DUA al sol titular de registre i eliminar els bullets redundants, o
  - (b) Deixar-lo com a reforç conscient —reconeixent que repeteix— si es valida empíricament que millora la consistència del LLM.
  - Decisió no prescriptiva: cal experiment A/B abans de retallar.

## 2. Font de dades

- **Blocs DUA**: llegits per [corpus_reader.py:227](../corpus_reader.py#L227) via `get_dua_block(level)`, que retorna l'entrada de `_cache["dua"][level]` carregada a [corpus_reader.py:163-176](../corpus_reader.py#L163). La càrrega extreu blocs de codi sota els encapçalaments `### DUA Accés`, `### DUA Core`, `### DUA Enriquiment` de la secció `## 6. INSTRUCCIONS DUA PER NIVELL` del fitxer [corpus/M2_DUA-principis-pautes.md](../corpus/M2_DUA-principis-pautes.md) (línies 172-202 del MD). Longitud: ~420 caràcters per bloc (Accés), ~320 (Core), ~320 (Enriquiment).
- **Catàleg**: dict `CATALOG` a [instruction_catalog.py:115-870](../instruction_catalog.py#L115). 84 instruccions efectives (12 SEMPRE, 31 NIVELL graduades per MECR, 38 PERFIL, 3 COMPLEMENT), agrupades en 10 macrodirectives.
- **Punt d'injecció al prompt**: [server.py:1213-1220](../server.py#L1213). Primer s'afegeixen les instruccions filtrades, després el bloc DUA com a "complement". Aquest ordre fa que qualsevol solapament sigui un reforç posterior, no un primer contacte.

## 3. Contingut literal dels 3 blocs DUA

Transcripció directa de [corpus/M2_DUA-principis-pautes.md:176-202](../corpus/M2_DUA-principis-pautes.md#L176):

### 3.1 DUA Accés — Lectura Fàcil extrema

```
NIVELL DUA: Accés — Lectura Fàcil extrema dins del límit MECR
- Suport visual màxim a cada idea
- Vocabulari molt bàsic, definicions integrades a CADA aparició
- Estructura molt explícita i predictible
- Redundància modal: text + imatge + esquema
- Eliminació total de farcit: cada frase té funció pedagògica clara
```

### 3.2 DUA Core — Llenguatge Clar

```
NIVELL DUA: Core — Llenguatge Clar (ISO 24495) dins del límit MECR
- Adaptació estàndard mantenint rigor curricular
- Frases curtes, vocabulari freqüent
- Definicions per termes tècnics (la primera vegada)
- Estructura clara amb connectors
```

### 3.3 DUA Enriquiment — Màxima complexitat

```
NIVELL DUA: Enriquiment — Màxima complexitat dins del MECR
- NO simplifiquis: mantén complexitat lingüística i conceptual
- Afegeix profunditat: excepcions, fronteres del coneixement, debats oberts
- Connexions interdisciplinars
- Preguntes de pensament crític (analitzar, avaluar, crear)
```

## 4. Taula de solapaments

Cada fila és una directriu DUA. Els IDs d'instrucció referencien el `CATALOG` a [instruction_catalog.py:115](../instruction_catalog.py#L115).

| # | Text DUA (resumit) | Nivell | Instruccions catàleg | Tipus | Comentari |
|---|---|---|---|---|---|
| 1 | Suport visual màxim a cada idea | Accés | D-01, D-02, D-03, C-02 (graduat pre-A1) | SIMILAR | DUA és etiqueta; D-0x només activa si hi ha complement; C-02 en pre-A1 ja exigeix "exemple visual a cada concepte" |
| 2 | Vocabulari molt bàsic, definicions integrades CADA aparició | Accés | A-01, A-02, A-15 (graduat pre-A1) | IDÈNTIC | A-15 pre-A1 diu exactament "1a aparició = terme + definició completa + exemple visual; 2a = terme + definició; 3a = terme sol amb recordatori". DUA diu "CADA aparició", cosa lleugerament més agressiva que A-15 però coberta |
| 3 | Estructura molt explícita i predictible | Accés | B-02, B-03, B-07 (graduat pre-A1), H-01 (TEA), G-07 (nouvingut sense CALP) | SIMILAR | L'"explicitació estructural" és el cor de la macro ESTRUCTURA. DUA no aporta regla operativa nova |
| 4 | Redundància modal: text + imatge + esquema | Accés | D-01, D-02, D-03, H-11 (DI) | COMPLEMENTARI | D-0x són COMPLEMENT (s'han d'activar); H-11 només DI. DUA ho generalitza per a tot perfil Accés. Aporta marc conceptual útil |
| 5 | Eliminació total de farcit: cada frase té funció pedagògica | Accés | C-03 (idèntic textual) | IDÈNTIC | C-03 diu: "Eliminació de redundància decorativa (principi de coherència, Mayer): cada element ha de tenir funció pedagògica clara". Duplicació clara |
| 6 | Adaptació estàndard mantenint rigor curricular | Core | E-01, E-05, E-06 (QUALITAT) | SIMILAR | Cobert per macro QUALITAT. DUA ho diu com a paraigua |
| 7 | Frases curtes, vocabulari freqüent | Core | A-01, A-07, A-12 (graduat per MECR) | IDÈNTIC | Repetició directa dels principis de simplificació. A-12 dona xifres concretes per MECR, DUA no |
| 8 | Definicions per termes tècnics (la primera vegada) | Core | A-02, A-15, E-02 (graduat) | IDÈNTIC | A-02: "Termes tècnics en negreta amb definició entre parèntesis la primera vegada". Literal |
| 9 | Estructura clara amb connectors | Core | A-14, B-02, B-03, B-10 | SIMILAR | A-14: "Connectors explícits entre frases..." |
| 10 | NO simplifiquis: mantén complexitat lingüística i conceptual | Enriquiment | H-14 (idèntic, però més contundent) | IDÈNTIC | H-14 és el text més fort del catàleg ("PROHIBIT SIMPLIFICAR..."). DUA diu el mateix més suau |
| 11 | Excepcions, fronteres del coneixement, debats oberts | Enriquiment | H-12 (literal) | IDÈNTIC | H-12: "Altes capacitats: profundització conceptual — excepcions, fronteres del coneixement, debats oberts." Còpia literal |
| 12 | Connexions interdisciplinars | Enriquiment | F-10 (PERFIL altes_capacitats) | IDÈNTIC | F-10: "Connexions interdisciplinars: relaciona el contingut amb altres matèries..." |
| 13 | Preguntes de pensament crític (analitzar, avaluar, crear) | Enriquiment | F-09 (literal) | IDÈNTIC | F-09: "Preguntes de pensament crític: per què? i si...? quines alternatives? quines limitacions?" |

Nota sobre la fila 4 (COMPLEMENTARI): és l'única entrada del bloc Accés que afegeix senyal real — generalitza la redundància modal a tot Accés, no només quan l'usuari ha activat un complement visual. Si es decideix retallar DUA, aquesta directriu val la pena re-ubicar.

Nota sobre el bloc Enriquiment: 4 de 4 directrius són cobertes pel catàleg (H-12, H-14, F-09, F-10). Però el catàleg les activa només amb `profiles: ["altes_capacitats"]`. Si l'usuari selecciona DUA=Enriquiment **sense** marcar perfil d'altes capacitats, el bloc DUA és l'**únic canal** que envia aquestes directrius. Això és un detall rellevant: eliminar DUA trencaria aquest camí.

## 5. Casos crítics

### Cas A — IDÈNTIC: DUA Accés "eliminació de farcit" vs C-03

- **Text DUA**: "Eliminació total de farcit: cada frase té funció pedagògica clara"
- **Text C-03**: "Eliminació de redundància decorativa (principi de coherència, Mayer): cada element ha de tenir funció pedagògica clara."
- **Problema**: pràcticament la mateixa frase. C-03 s'activa SEMPRE; en una adaptació DUA Accés, l'LLM rep el principi dues vegades.
- **Proposta**: eliminar el bullet del bloc DUA; C-03 ja ho cobreix. Si es vol reforç per a Accés, es pot afegir `intensified_if_dua_acces` a C-03 més que repetir-ho al bloc DUA.

### Cas B — IDÈNTIC: DUA Enriquiment "excepcions, fronteres del coneixement, debats oberts" vs H-12

- **Text DUA**: "Afegeix profunditat: excepcions, fronteres del coneixement, debats oberts"
- **Text H-12**: "Altes capacitats: profundització conceptual — excepcions, fronteres del coneixement, debats oberts."
- **Problema**: còpia textual de la cua de la frase.
- **Proposta**: deixar només DUA (i desactivar H-12 quan DUA=Enriquiment), o a l'inrevés. La decisió depèn de si l'enriquiment s'ha d'aplicar **sempre que DUA=Enriquiment** (via DUA) o **només si perfil=altes_capacitats** (via H-12). Avui es disparen les dues, cosa que pot ser desitjada (doble senyal) o redundant (soroll).

### Cas C — IDÈNTIC: DUA Enriquiment "preguntes pensament crític" vs F-09

- **Text DUA**: "Preguntes de pensament crític (analitzar, avaluar, crear)"
- **Text F-09**: "Preguntes de pensament crític: per què? i si...? quines alternatives? quines limitacions?"
- **Problema**: la formulació DUA fa servir el vocabulari de Bloom (analitzar/avaluar/crear); F-09 dona preguntes operatives exemple. Els dos textos són **complementaris tècnicament** (marc + exemples), però al prompt diuen el mateix al LLM.
- **Proposta**: fusionar al catàleg — ampliar F-09 amb els verbs de Bloom — i eliminar el bullet de DUA.

### Cas D — IDÈNTIC: DUA Core "definicions per termes tècnics (primera vegada)" vs A-02 + A-15

- **Text DUA**: "Definicions per termes tècnics (la primera vegada)"
- **Text A-02**: "Termes tècnics en **negreta** amb definició entre parèntesis la primera vegada."
- **Text A-15** (pre-A1..B1, graduat): "Scaffolding decreixent: 1a aparició = terme + definició completa; 2a = terme + definició breu; 3a en endavant = terme sol."
- **Problema**: A-02 i A-15 ja són activades SEMPRE i donen la regla amb més precisió (negreta, format, gradació). El bullet DUA és estrictament un subconjunt pobre.
- **Proposta**: eliminar-lo del bloc DUA.

### Cas E — IDÈNTIC: DUA Enriquiment "NO simplifiquis" vs H-14

- **Text DUA**: "NO simplifiquis: mantén complexitat lingüística i conceptual"
- **Text H-14**: "Altes capacitats: PROHIBIT SIMPLIFICAR. Mantén la complexitat lingüística i conceptual original o augmenta-la. NO facis servir vocabulari freqüent, NO eliminis subordinades, NO escurcis frases, NO desnominalitzis, NO eliminis sentit figurat. Les regles universals de simplificació NO s'apliquen a aquest perfil."
- **Problema**: H-14 és molt més fort i operatiu. DUA diu el mateix en versió resumida. Repetir el missatge en dos punts del prompt pot ser estratègia deliberada (ancoratge) o redundància. H-14 s'activa només si perfil=altes_capacitats; DUA s'activa si l'usuari tria Enriquiment. Coexisteixen **només quan coincideixen**.
- **Proposta**: observar empíricament si el doble senyal millora la fidelitat al "no simplificar" o genera soroll. Aquest és un candidat a experiment A/B abans de decidir.

## 6. Casos valuosos (coexistència justificada)

- **DUA com a etiqueta de registre**. La primera línia de cada bloc ("NIVELL DUA: Accés — Lectura Fàcil extrema dins del límit MECR") és un **marc identitari** que el catàleg no dona. Orienta el LLM abans d'entrar en regles. Valor: mantenir.
- **DUA Accés bullet 4 "redundància modal"**. Generalitza una regla que al catàleg només existeix fragmentada (D-01/02/03 són COMPLEMENT, H-11 és DI). DUA la torna principi general per a tot Accés. Valor real afegit.
- **DUA Enriquiment com a canal alternatiu a altes_capacitats**. Si el docent tria DUA=Enriquiment **sense** marcar perfil d'altes capacitats (per ex., per a un grup mixt), el bloc DUA és l'únic vehicle de les directrius H-12/H-14/F-09/F-10. Eliminar-lo trencaria aquest cas d'ús.
- **DUA Core com a recordatori de rigor curricular**. El bullet "Adaptació estàndard mantenint rigor curricular" no afegeix regla nova (E-01/E-05/E-06 hi són), però és un resum útil que actua com a àncora.

## 7. Preguntes obertes (cal experiment empíric)

1. Amb DUA Accés, el LLM **consolida** el missatge en rebre el mateix en dos formats (catàleg + DUA) o **satura**? Batch A/B amb i sense bloc DUA, mateix perfil i MECR.
2. Quan DUA i una instrucció del catàleg són textualment gairebé iguals (casos A, B, C, D, E), l'LLM **prioritza** l'una sobre l'altra? Es podria observar via logs d'atenció o proves amb un dels dos senyals modificat.
3. El bloc DUA pesa més per **posició** al prompt? Avui va després del bloc d'instruccions filtrades ([server.py:1218-1220](../server.py#L1218)). Si es mou al principi, canvia el comportament?
4. La repetició ajuda quan el missatge és delicat (H-14 "NO SIMPLIFIQUIS" + DUA "NO simplifiquis")? Concretament en Enriquiment, on el risc de regressió a la mitjana és alt.
5. El bloc DUA es podria substituir per una sola línia de "registre" ("Ara escrius en registre Lectura Fàcil extrema") i deixar la resta al catàleg? Cal empíria.

## 8. Annex: matriu completa

Matriu instrucció × nivell DUA. "X" = coincideix amb almenys una directriu d'aquell bloc DUA. "p" = parcial (només una part del text). "·" = no coincideix. Només es mostren les instruccions amb alguna coincidència; les restants (73 de 84) no tenen solapament amb cap bloc DUA.

| Instrucció | Accés | Core | Enriq | Nota |
|---|---|---|---|---|
| A-01 (vocabulari freqüent) | X | X | · | Subjacent a "vocabulari bàsic/freqüent" |
| A-02 (termes tècnics + negreta + def) | X | X | · | Idèntic a "definicions termes tècnics" |
| A-07 (una idea per frase) | p | X | · | Subjacent a "frases curtes" |
| A-12 (longitud frase) | p | X | · | Precisa frases curtes |
| A-14 (connectors) | · | X | · | Idèntic a "estructura amb connectors" |
| A-15 (scaffolding definicions) | X | X | · | Idèntic a "def integrades CADA aparició" |
| B-02 (blocs amb títol) | X | p | · | Estructura explícita |
| B-03 (frase tòpic) | X | · | · | Estructura predictible |
| B-07 (advance organizer) | X | · | · | Estructura predictible |
| C-02 (reforç immediat concepte) | X | · | · | "Suport visual a cada idea" (pre-A1) |
| C-03 (eliminació redundància) | X | · | · | Idèntic (Cas A) |
| D-01/02/03 (pictogrames/esquema/mapa) | p | · | · | "Redundància modal", però són COMPLEMENT |
| E-01 (nucli terminològic intocable) | · | X | · | "Rigor curricular" |
| E-05 (exactitud científica) | · | X | · | "Rigor curricular" |
| E-06 (causalitat) | · | X | · | "Rigor curricular" |
| E-02 (graduar definició) | X | X | · | Definicions primera aparició |
| F-09 (preguntes pensament crític) | · | · | X | Idèntic (Cas C) |
| F-10 (connexions interdisciplinars) | · | · | X | Idèntic |
| G-07 (nouvingut sense CALP) | p | · | · | Estructura explícita per casos específics |
| H-01 (TEA estructura predictible) | p | · | · | Coincideix per casos TEA |
| H-11 (DI repetició formats diversos) | X | · | · | Redundància modal per DI |
| H-12 (altes cap: fronteres coneixement) | · | · | X | Idèntic (Cas B) |
| H-14 (altes cap: PROHIBIT simplificar) | · | · | X | Idèntic (Cas E) |
| H-15 (2e equilibri) | · | · | p | Coincideix parcialment amb Enriquiment |

Total: 24 instruccions amb solapament (de 84). Les altres 60 tracten matèries no cobertes per cap bloc DUA (puntuació, veu activa, negacions, perfils específics com TDAH/dislèxia/TDL/disc. sensorials/vulnerabilitat, personalització L1, etc.).

---

## Fonts no llegides o absents

Cap. Tots els fitxers citats han estat llegits directament:
- [corpus/M2_DUA-principis-pautes.md](../corpus/M2_DUA-principis-pautes.md) (líns. 172-202)
- [corpus_reader.py](../corpus_reader.py) (líns. 163-176, 227-230)
- [instruction_catalog.py](../instruction_catalog.py) (líns. 115-870)
- [server.py](../server.py) (líns. 1202-1250)
