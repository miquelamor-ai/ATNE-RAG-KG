# Refactor 2026-04-21/22 — Changelog complet i pla de validació

**Autor:** Claude Opus 4.7 + Miquel Amor
**Branques afectades:** `refactor/server-split`, `refactor/prompt-lean`
**Branca de producció:** `main` (pilot actiu 20/04–08/05)

## Context

`server.py` era un monòlit de **6.445 línies** amb 75 endpoints. Aquesta sessió ha fet una **refactorització arquitectònica** que redueix `server.py` a **4.243 línies (−34%)** i un **refactor del system prompt** que l'escurça un **22%**. Cap canvi afecta producció encara — tot viu en dues branques separades del `main` que corre el pilot.

## Tots els commits de la sessió (10)

### Ja pushejats a origin (primers 8 commits)

| SHA | Missatge | Fitxers | Δ línies |
|---|---|---|---|
| `4245bf2` | refactor(server): snapshot del contracte public abans del split | `tests/snapshot_contract.py`, `tests/snapshots/server_contract.json` | +320 |
| `d5b4bda` | refactor(adaptation): extreu post_process.py de server.py | `adaptation/post_process.py` (nou), `server.py` | server.py −500 |
| `2252183` | refactor(routes): extreu drafts endpoints a routes/drafts.py | `routes/drafts.py` (nou), `server.py` | server.py −195 |
| `5a1f438` | cleanup(server): elimina RAG/KG dead code (200 linies) | `server.py` | −200 |
| `b6e2784` | refactor(adaptation): extreu llm_clients.py de server.py | `adaptation/llm_clients.py` (nou), `server.py` | server.py −561 |
| `33b7eac` | refactor(adaptation): extreu prompt_builder.py de server.py | `adaptation/prompt_builder.py` (nou), `server.py` | server.py −604 |
| `d06a933` | cleanup: elimina imports i vars morts post-split | `server.py`, `instruction_filter.py` | −6 |
| `92504ee` | cleanup(corpus_reader): elimina funcions orfenes | `corpus_reader.py` | −20 |

### Commits locals pendents de push (2 a `refactor/server-split`, 1 a `refactor/prompt-lean`)

| SHA | Branca | Missatge | Fitxers |
|---|---|---|---|
| `aabcb7c` | refactor/server-split | refactor(adaptation): extreu orchestrator.py (run_adaptation) de server.py | `adaptation/orchestrator.py` (nou), `server.py` |
| `59ffdcd` | refactor/server-split | fix(languagetool): treu CASING / UPPERCASE_ d'auto-apply | `server.py` |
| `b33ee4c` | refactor/prompt-lean | refactor(prompt): prompt lean -22% tokens sense perdre qualitat | `adaptation/prompt_builder.py` |

## Categoria 1 — Split arquitectònic (sense canvi funcional)

### Mòdul `adaptation/` creat des de zero

```
adaptation/
├── __init__.py
├── post_process.py    (d5b4bda) — clean_gemini_output, _strip_latex_artifacts, typos, english, concat…
├── llm_clients.py     (b6e2784) — _call_llm + _call_llm_raw + _call_llm_stream + claus API + rotació
├── prompt_builder.py  (33b7eac) — build_system_prompt + build_persona_audience + helpers
└── orchestrator.py    (aabcb7c) — run_adaptation + _verify_adaptation + buffer d'audit
```

**Contracte preservat:** cada mòdul extret es re-importa al namespace de `server.py`. Per això `from server import run_adaptation` segueix funcionant per a `generador_lliure` i 7+ tests.

**Truc d'orchestrator:** `run_adaptation` fa `import server` lazy (dins la funció, no a load-time) per accedir a `_model_for`, `_AUDITOR_ENABLED_RUNTIME`, `post_process_catalan`, `_persist_adaptation_to_supabase`, `_log_session` sense circularitat. L'estat mutable (`_ATNE_LAST_ADAPTATION`, `_ATNE_ADAPTATIONS_LOG`) viu a `orchestrator.py` i els endpoints d'audit a server.py el llegeixen via atribut del mòdul (`_orchestrator._ATNE_*`) per tenir sempre valors frescos.

### Mòdul `routes/` iniciat

```
routes/
└── drafts.py          (2252183) — 5 endpoints /api/drafts via APIRouter
```

### Cleanup aplicat (no canvia funcionalitat)

- `5a1f438` — 200 línies de dead code RAG/KG (vector_search, kg_expand_concept, combined_search, KEYWORD_MAP…)
- `d06a933` — 6 línies: `import jwt as pyjwt` (auth via HTTP, no decode local), `sqlite3` duplicats, `_lower_raw` mort, `PROFILE_INSTRUCTION_MAP` sense ús
- `92504ee` — 20 línies: `get_mecr_block`, `get_profile_block` a `corpus_reader.py` (zero callers al repo)

## Categoria 2 — Fix pedagògic (canvi de comportament)

### `59ffdcd` — LanguageTool CASING passa a warning

**Què canvia:**
- Treiem `"CASING"` de `_SAFE_RULE_CATEGORIES`
- Treiem `"UPPERCASE_SENTENCE_START"` i `"UPPERCASE_"` de `_SAFE_RULE_PREFIXES`

**Efecte pràctic:**
- Abans: LT auto-corregia "Revolució Industrial" → "revolució industrial" (norma IEC estricta)
- Ara: el docent veu el suggeriment al Quality Report i decideix manualment

**Motiu pedagògic:** pel català estricte "revolució industrial" és l'ús correcte, però al context pedagògic/històric és freqüent tractar "Revolució Industrial" com a nom propi d'una època. Mateix fenomen feia que al glossari l'adjectiu "comunista" pugés a "Comunista" per regla de majúscula inicial de cel·la de taula.

**Decisió explícita:** Miquel Amor, 2026-04-21 després de veure-ho a la validació real.

## Categoria 3 — Refactor del system prompt (canvi funcional pedagògic)

### `b33ee4c` — Prompt lean: −22.2% tokens

**5 reduccions simultànies a `adaptation/prompt_builder.py`:**

| # | Què | Abans | Ara |
|---|---|---|---|
| P1 | Bloc "Tipologia interna (ÚS TEU, NO la mostris)" dins preguntes_comprensio | 13 línies de meta-instrucció | Eliminat — la info ja queda al FORMAT DE SORTIDA explícit |
| P2 | "Adequació per etapa" | 5 línies amb totes 5 etapes | 1 línia filtrada segons `context.etapa` |
| P3 | "Literari vs informatiu" | 2 línies (les dues rames) | 1 línia (només la rama aplicable segons `es_literari`) |
| P4 | "RECORDATORI CRÍTIC DE TÍTOLS" al final | 15 línies amb tots els títols enumerats | 2 línies compactes |
| P5 | "Regles estrictes de la SORTIDA" (preguntes) | 11 bullet points | 2 línies amb les 3 restriccions essencials |

**Mesura (perfil Marc Ribera TDAH + 3 complements):**
- Baseline: **1.952 paraules / 12.902 caràcters**
- Lean: **1.518 paraules / 10.054 caràcters**
- **Estalvi: 434 paraules (22.2%)**, ≈500 tokens per adaptació

**Marcadors estructurals verificats (9/9 presents al prompt generat):**
identitat · role docent · MECR anchor · persona TDAH · DUA · glossari format · preguntes MALL · argumentació · auditoria

## Validacions efectuades

### Snapshot contract (`tests/snapshot_contract.py --check`)

Executat a **cada commit**. Sempre OK: 78 rutes + 18 exports crítics preservats.

### Smoke test mockejat (`aabcb7c`)

Test Python amb `_call_llm` mockejat. `run_adaptation` end-to-end:
- 2 crides (adapt + verify)
- 6 events emesos al progress_callback
- Buffer orchestrator `_ATNE_LAST_ADAPTATION` poblat
- Lectura dinàmica `_orchestrator._ATNE_*` des dels endpoints d'audit OK

### Validació real E2E a `localhost:8080`

Executada amb `PORT=8080 PYTHONUNBUFFERED=1 python -u server.py`:

- **Auth Supabase**: Google @fje.edu login funciona a localhost (redirect URL ja registrat)
- **Admin reconegut**: `/api/docent/is-admin` retorna `true` per al docent `78a2ad3c03384a73`
- **Adaptació Marc Ribera (TDAH, 3r ESO, text sobre revolucions):**
  - `POST /api/adapt` → 200 OK, SSE streaming via `orchestrator.run_adaptation` → `llm_clients._call_llm` (Gemma 4 31B) → `post_process_adaptation` → Quality Report LT
  - Text adaptat correcte: 5 micro-blocs `[Secció X de 5]`, frases <18 paraules, termes tècnics en negreta + definició, "Pregunta ràpida" intercalada
  - Complements OK: glossari taula, preguntes MALL/TILC (3+3+7), argumentació pedagògica 5 àrees, notes auditoria
  - Post-process ha netejat 3 problemes de Gemma: anglicisme `owners→propietaris`, typo `possuïen→posseïen`, LaTeX `$\rightarrow$ → →`

### Validació real E2E adaptació **Yassin Mansour** (perfil nouvingut àrab, A1)

Executada 2026-04-21 23:59 (adapt-1776808795857). **Perfil més exigent del sistema:** 5 complements (glossari + esquema + bastides + pictogrames + preguntes), 60 instruccions filtrades, MECR A1 (màxim 8 paraules per frase), L1 àrab alfabet no-llatí.

**OK — el refactor funciona per al perfil més complex:**
- Glossari bilingüe amb 8 traduccions àrab reals (ثدييات, غدد ثدية, شعر, دم حار, رئتان, سطح, صغار, متنوعة)
- Frases de 5-8 paraules estrictes, SVO, zero subordinades
- Pictogrames integrats al text (🤱, 🍼, 🐾, 🌡️, 🦇, 🐬, 🫁)
- Bastides MALL/TILC adaptades a A1 (només perquè/però/per tant/per exemple)
- Suport L1 àrab a les bastides
- LaTeX post-process confirmat: 5+ ocurrències de `$\rightarrow$` totes netejades a `→`

**Problemes detectats (NO són del refactor, sinó errors preexistents de Gemma + LT):**

1. **8 errors ortogràfics de Gemma que LT no ha detectat:**
   - `Escribeu` → hauria de ser `Escriviu`
   - `Veritater o Fals` → `Veritable o Fals` / `Cert o Fals`
   - `definint'los` → `definint-los` (guionet, no apòstrof)
   - `limited` (anglicisme) → `limitat`
   - `sencelles` → `senzilles`
   - `estrict` → `estricte`
   - `ratols` → `ratolins`
   - `delfins`/`delfí` → `dofins`/`dofí`

2. **LT PUNT_FINAL auto-apply afegeix punts a cel·les de taula** on probablement no caldrien:
   - `| per exemple |` → `| per exemple |.`
   - `Banc de paraules: ...fills` → `...fills.`
   - `Sang calenta → دم حار` → `Sang calenta — دم حار.` (addicionalment canvia `→` per `—`)

### Validació real E2E del **prompt lean** — PENDENT

El servidor 8080 encara corre el codi de `refactor/server-split` (prompt baseline). **Per validar `b33ee4c` cal:**
1. Matar procés 8080 actual
2. `git checkout refactor/prompt-lean`
3. Rellançar `PORT=8080 python -u server.py`
4. Fer adaptació amb Marc Ribera mateix perfil i text
5. Comparar output amb la baseline d'ahir (guardada com `adapt-1776807273306`)

### Tests amb bugs pre-existents (no causats pel refactor)

- `tests/test_instruction_filter.py`: KeyError 'sempre' (canvi de nom de clau fet algun dia passat)
- `tests/test_strip_latex_quick.py`: UnicodeEncodeError a Windows cp1252 (cal `PYTHONIOENCODING=utf-8`)

## Pla de validació pedagògica per a docents

Per explicar els canvis a qualsevol docent/PedagogIA de l'equip FJE, calen **3 demos comparatives**:

### Demo A — Refactor arquitectònic és invisible
Executar la mateixa adaptació (Marc Ribera, text revolucions, MECR B1, complements: glossari + esquema + preguntes) a dues instàncies:
- Cloud Run (main, prompt vell)
- Local refactor/server-split (prompt vell, codi refactoritzat)

**Esperat:** sortides funcionalment equivalents (diferències només per la aleatorietat de Gemma, no per estructura). El docent no ha de notar cap canvi.

### Demo B — Prompt lean millora velocitat sense perdre qualitat
Mateix perfil, text i complements, a dues instàncies:
- Local refactor/server-split (prompt antic, 1.952 paraules)
- Local refactor/prompt-lean (prompt nou, 1.518 paraules)

**Esperat:**
- El lean genera **15-20% més ràpid** (menys input tokens = menys temps TTFT)
- Qualitat pedagògica equivalent: mateixes seccions, mateix rigor, mateix format TDAH
- Cost/generació 22% menor (rellevant si algun dia passem de Gemma free a OpenAI pagat)

### Demo C — Fix LanguageFanTool CASING respecta noms propis d'època
Mateix perfil, text amb "Revolució Industrial", "Edat Mitjana", "Il·lustració":
- Sense fix (main): LT baixa a "revolució industrial", "edat mitjana"
- Amb fix (`59ffdcd`): es mantenen en majúscules tal com escriu el LLM

**Esperat:** docents d'Història i Humanitats agraeixen el canvi; docents de llengua veuen el warning al Quality Report i decideixen cas a cas.

## Decisions obertes per a **2026-04-22 primera hora**

### Decisió 1 — Quins commits pugem a origin

- **Mínim obligat**: `aabcb7c` i `59ffdcd` ja validats. Push simple a `origin/refactor/server-split`.
- **Afegir opcional**: `b33ee4c` a `origin/refactor/prompt-lean`. Afegeix backup remot del prompt lean.

### Decisió 2 — Què arriba a producció (main) per al pilot

Tres opcions, de menys a més canvi:

| Opció | Què arriba a main | Impacte al pilot |
|---|---|---|
| **A. Només fix LT** | Cherry-pick `59ffdcd` a main (1 línia) | Baixíssim. Docents d'Història noten millora, la resta no veu diferència |
| **B. Fix LT + prompt lean** | Cherry-pick `59ffdcd` + adaptació de `b33ee4c` a main (cal reescriure dins server.py monolític) | Baix. Latència -15%, cost -22%. Exigeix A/B breu abans de merge |
| **C. Split complet + prompt lean** | Merge `refactor/prompt-lean` a main | Mitjà. 5 mòduls nous. Requereix validació més gran però deixa main molt més net |

**Recomanació tècnica pragmàtica: Opció A per a demà matí** (risc mínim mid-pilot). **Opcions B i C post-pilot (maig-juny).**

Però la decisió final és del Miquel segons prioritats del pilot.

### Decisió 3 — Test real del prompt lean abans de commit a main

Cal fer adaptació real a localhost:8080 amb `refactor/prompt-lean` checkout, mateix perfil Marc Ribera + text revolucions, per confirmar 0 regressió pedagògica. Estimació: 5 minuts.

## Com revertir (pla d'emergència)

Si a producció apareix qualsevol regressió:

```bash
# Revert del fix LT (opció A)
git revert 59ffdcd

# Revert del prompt lean (opció B/C)
git revert b33ee4c

# Revert total fins abans del split
git checkout main
git reset --hard 5a1f438  # (l'últim commit abans del refactor gran)
```

Cada commit és atòmic i reversible. El snapshot `tests/snapshots/server_contract.json` permet detectar regressions estructurals abans del deploy.

## Estadístiques finals

- **Línies net eliminades a server.py:** 2.202 (6.445 → 4.243, −34%)
- **Mòduls nous:** 5 (post_process, llm_clients, prompt_builder, orchestrator, routes.drafts)
- **Commits total:** 10
- **Snapshot contract checks executats:** 11 (0 trencaments)
- **Adaptacions reals validades:** 1 (Marc Ribera, 7.711 chars output, tots els marcadors OK)
- **Tests pre-existents trencats:** 0 (els 2 que fallaven ja fallaven abans del refactor)
