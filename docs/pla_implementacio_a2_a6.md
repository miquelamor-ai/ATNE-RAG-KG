# Pla d'implementació A2 + A6 — ATNE

> **Data**: 2026-06-01 · **Estat**: **v1.0 CONGELADA** (esquema rubrica.json freeze 01/06). Esperant publicació dels 38 rubrica.json al corpusFJE per arrencar A2 cascada.
> **Decisions finals Miquel + mineriaRAG (01/06, v1.0 100% CONGELADA)**:
> 1. Famílies canòniques = 5 valors: `mediacio`, `generes`, `adaptacio`, `bastida`, **`avaluacio`** (anticipada).
> 2. Etiquetes nivell = **només amb accent** (Estratègic / Acadèmic / Crític).
> 3. `tolc` = futur pendent (NO vista; parser preserva). `traduccio_l1` = **eliminar del parser** durant A2 (legacy confús).

## 1. Context

Després del cross-check del 31/05, mineriaRAG ha integrat les 5 esmenes tècniques d'ATNE. El **contracte tècnic** (esquema rubrica.json v1.0) és **estable**. Resten 3 micro-decisions pedagògiques de Miquel que no bloquegen la preparació.

Aquest document descriu la **seqüència d'implementació** d'A2 (refactor pipeline 37 skills) i A6 (transliteració runtime + cache Supabase) un cop els 38 JSONs estiguin publicats. Mentrestant, ATNE pot avançar amb feina **no-bloquejant**: esborrany SQL, plans, tests d'estructura.

## 2. Calendari realista

| Setmana | Què passa |
|---|---|
| 01/06 - 06/06 | mineriaRAG: parser + GitHub Action + plantilla universal. ATNE: preparació SQL + tests d'estructura. |
| 07/06 - 13/06 | mineriaRAG: publica 38 rubrica.json. ATNE: arrenca A2 (refactor pipeline) als 2 pilots (glossari + bastides-lectura). |
| 14/06 - 27/06 | ATNE: refactor 35 skills restants + A6 backend (LLM prompt amb estàndard L1 + integració cache). |
| 28/06 - 11/07 | ATNE: A6 UI (vàlvula docent Pas 3 + indicador `verified:false`) + A7 (tests integració). |
| 12/07 - 18/07 | Pilot conjunt amb docent real + rollout. |

## 3. A2 · Refactor pipeline (37 skills)

### 3.1. Pre-requisits (NO bloquejants ara)

- [ ] **Migration SQL `atne_translits`** preparat a [migrations/2026-06-01_atne_translits.sql](../migrations/2026-06-01_atne_translits.sql). Miquel l'executa al Supabase SQL Editor quan toqui.
- [ ] **Tests d'estructura ATNE actuals**: capturar el comportament d'avui (golden tests amb cas titella + nouvingut àrab + dislèxia AC) abans de tocar res. Garantia anti-regressió.

### 3.2. Refactor inicial (2 pilots)

**Quan arribi senyal mineriaRAG**:

1. Validar 30 min que els 2 rubrica.json (`generate-glossari` + `generate-bastides-lectura`) cobreixen els camps que ATNE espera (cas titella + format taula + sostres MECR + R3/R4).
2. Refactoritzar `adaptation/prompt_builder.py:build_complements_prompt` per a aquests 2 skills:
   - Llegir del `rubrica.json` (via `skills_loader.py` ja existent).
   - Substituir les directives Python hardcoded (línies ~614-650 glossari, ~1462-1495 bastides) per la lectura del JSON.
   - Format header H2/H3 literal del `transversals.format_output` (no inventar).
   - `min/max` numèrics del `levels.{MECR}.passos[].countable` (no taules hardcoded).
3. Smoke test amb 5 textos representatius:
   - 1r primària nouvingut àrab (cas A5)
   - 2n primària sense condicions (cas R4)
   - ESO dislèxia A1 (cas R3 — espera comportament excepció pactada)
   - Batx AACC B2 (cas expertise reversal)
   - ESO TDAH A2 (cas estàndard)

### 3.3. Refactor en cascada (35 skills restants)

Ordre per cost decreixent (els que tenen més directives Python actuals):

1. **Mediacio** (12 restants: preguntes-comprensio, bastides-produccio, mapa-conceptual, mapa-mental, esquema-visual, plantilles-genere, resum-graduat, cartes-conversacionals, rubriques, activitats-aprofundiment, tolc, glossari—ja fet)
2. **Generes** (24): start amb els 5 <70% normalitzats (write-conte, diari, divulgatiu, informe, generate-pictogrames) → la resta.

Per cada skill:
- Validar rubrica.json present + cobreix casos d'ús
- Substituir directiva Python al `prompt_builder.py` per lectura JSON
- 1 smoke test
- Marcar com `migrated` a un check intern

### 3.4. Tasques transversals d'A2

a) **R0 matriu canon**: refactor `ui/atne/js/complements-matriu.js` per consumir `matriu_cobertura.json` del corpusFJE (no hardcoded).
   - Mantenir la mateixa API pública (`defaultComplementsForProfile`, `MATRIU_CONDICIONS`).
   - Test de regressió: la matriu carregada del JSON ha de coincidir byte-a-byte amb la hardcoded actual.
   - Quan coincideix → eliminar hardcoded.

b) **`tolc` = futur pendent** (decisió Q3a final — matís mineriaRAG 01/06):
   - **NO tocar** el parser orchestrator backend ni el TITLE_MAP de llm.js (segueix preservant si LLM genera `## TOLC` o `## Transllenguatge`).
   - **NO afegir** a `COMP_META` ara (sense vista al Pas 3).
   - **Revisió post-pilot (juliol)**: si docents en demanen vista pròpia → entra a v1.1 com a complement plenament integrat amb chip + vista.

c) **`traduccio_l1` = eliminar del parser** (decisió Q3b final — matís mineriaRAG 01/06):
   - **Treure** `'traduccio_l1'` (i `'traduccio l1'`, `'traduccio_de_l1'`) del `TITLE_MAP` de [ui/atne/js/llm.js](../ui/atne/js/llm.js).
   - **Treure** del `_section_aliases` del orchestrator backend (adaptation/orchestrator.py).
   - **Verificar** que no hi ha codi orfe (cerca `traduccio_l1` a tot el repo) que en depèn.
   - **Test de regressió**: text d'input simulat amb secció `## Traducció L1` ha de quedar absorbit al `_main` (fallback) o filtrat, NO a una clau orfa.

d) **Eliminar directives Python duplicades amb SKILLs**:
   - Després del refactor, les directives a `instruction_catalog.py` que ara dupliquen contingut SKILL.md poden eliminar-se.
   - **Atenció**: només eliminar les que tenen `gap_at_M=false` segons l'auditoria del workflow. Les 20 directives `gap_at_M=true` requereixen pujada al M*.md primer (responsabilitat mineriaRAG durant la normalització Pla B).

## 4. A6 · Transliteració runtime + cache Supabase

### 4.1. Pre-requisits

- [ ] **Migration SQL executada** (`atne_translits`). Manual a Supabase Editor.
- [ ] **A2 complet o suficient als 2 pilots** (perquè el flux glossari ja consumeix rubrica.json).
- [ ] **Taula d'estàndards canon publicada al corpusFJE** (la del document `transliteracio_standards_l1_2026-05-31.md`).

### 4.2. Components

#### a) Cache lookup (backend, Python)

```python
# adaptation/translit_cache.py (NOU)

def lookup_translit(terme: str, l1: str) -> str | None:
    """Retorna translit verified=true si existeix; None altrament."""
    # Query a Supabase atne_translits via supabase-py o REST
    ...

def store_translit(terme: str, l1: str, translit: str, estandard: str,
                   verified: bool = False, verified_by: str | None = None) -> None:
    """Desa o actualitza una entrada (UPSERT per UNIQUE(terme, l1))."""
    ...
```

#### b) Integració al LLM prompt (backend)

Al `prompt_builder.py` quan es genera glossari amb columna translit:
1. Per cada `(terme, L1)` ja al glossari intermedi → `lookup_translit()` primer.
2. Si troba `verified=true` → usar directament.
3. Si NO troba → demanar al LLM (amb directiva: "estàndard X per a la L1 Y, format Z") → desar `verified=false`.

Estalvi esperat: 30-60% de crides LLM post-fase d'estabilització (un cop els termes habituals estan verificats).

#### c) Vàlvula docent (UI Pas 3)

A `ui/atne/pas3.html`:
- Cada cel·la de la columna translit del glossari porta un **indicador discret** `verified:false` (badge "?" + tooltip "Pendent de revisió").
- En **editar inline** la cel·la (ja és comportament existent), s'envia un POST al backend amb `terme + l1 + nova_translit + verified=true + verified_by={email}`.
- El backend crida `store_translit(..., verified=True, verified_by=...)`.

#### d) Indicador visual `verified:false`

CSS petit: les cel·les `.gl-translit-pending` amb un punt o subtil background-color, sense ser invasives. Aprovat pel docent quan calgui amb un sol clic.

## 5. Tests d'integració (A7 — després d'A2+A6)

Bateria mínima:

| Test | Espera | Cobreix |
|---|---|---|
| Glossari nouvingut àrab pre-A1 1r prim | 3-5 termes + L1 + translit `verified:false` | A5 + cache miss + format taula 4 cols |
| Glossari nouvingut àrab pre-A1 1r prim (segona crida) | Mateix output amb les translits validades = cache hit | Cache lookup |
| Glossari sense condicions 1r prim | NO glossari per defecte | R4 |
| Glossari dislèxia A1 sense L1 | NO glossari per defecte (R3 verified:false) | R3 excepció pactada |
| Adaptació AACC B2 | NO pictogrames, NO esquema, mapes a B2 OK | expertise reversal |
| Esquema visual emergent pre-A1 | 2-3 nodes | min/max nodes per MECR |
| Bastides amb preguntes_comprensio | Sense duplicat redundant | Opció D mineriaRAG |

## 5.bis Troballa pre-A2 · no-determinisme `build_complements_prompt`

Detectat 01/06 mentre generàvem els baselines de [tests/capture_baseline_prompts.py](../tests/capture_baseline_prompts.py): execucions consecutives del mateix input generen sortides del **Call 2 (complements)** lleugerament diferents — ordre d'algunes seccions inestable, probablement per iteració sobre `set` no ordenat (`comp_actius = {k for k,v in comp.items() if v}` a `adaptation/prompt_builder.py:1353`, i possible iteració de `select_active()` sense `sorted()`).

**Impacte avui**: l'LLM rep prompts que canvien d'una crida a l'altra → els tests A/B amb temperatura 0 NO són reproduïbles. Cost de cache (Anthropic, OpenAI) augmentat per cache miss innecessari.

**Acció proposada durant A2**: ordenar deterministament les seccions del prompt:
- Ordenar `comp_actius` per ordre canon (definit a `_COMP_HEADERS` o llista explícita).
- Aplicar `sorted(active_skills, key=lambda s: s.name)` abans d'iterar.
- Test de regressió: 3 execucions consecutives han de donar prompt idèntic byte-a-byte.

**Mitigació mentre no es fixa**: el `--diff` del script de baselines marca els `.adapter.txt` (deterministes) com a referència sòlida; els `.complements.txt` són referència aproximada (canvi d'ordre tolerable, canvi de contingut = regressió real).

## 6. Riscos i mitigacions

| Risc | Mitigació |
|---|---|
| Esquema rubrica.json no cobreix algun cas viu del pipeline | Validació 30 min als 2 pilots ABANS d'arrencar refactor cascada. Si falla → segona ronda amb mineriaRAG. |
| Refactor de matriu canon trenca defaults actuals | Test de regressió byte-a-byte abans d'eliminar hardcoded. Rollback fàcil (mantenir hardcoded comentat 1 sprint). |
| Cache Supabase amb traduccions errònies dels primers docents | UI clara `verified:false` + permetre **invalidar** verified:true (botó "marcar com a no verificada"). Auditoria mensual primers 3 mesos. |
| Pacted_exceptions del rubrica.json (R3, post_edicio_pas3, alfabets) divergeixen entre canon i codi | Test CI anti-drift: el codi ATNE consumeix les pacted_exceptions del rubrica.json corresponent (no hardcoded). |

## 7. Què NO fem en aquest pla

- **No fem refactor `instruction_catalog.py` complet** ara — la majoria de les 107 instruccions són `gap_at_M=true` i requereixen pujada al M*.md primer (responsabilitat mineriaRAG, Pla B normalització). ATNE espera.
- **No tocarem `case_overrides` complexos d'esquema rubrica.json (Q3 R3 dislèxia pura, etc.) com a regles canon** — queden com excepcions pactades al codi ATNE amb `verified:false`, revisió post-pilot juliol.
- **No implementem complement TOLC amb vista pròpia** ara (Q3a opció c). Pendent post-pilot si docents en demanen.

## 8. Senyal d'arrencada

mineriaRAG envia: **"v1.0 final · commit `{hash}` corpusFJE · 38 rubrica.json publicats"** amb la senyal explícita acordada.

A partir d'aquest moment:
1. ATNE valida 30 min als 2 pilots.
2. Si validat → arrencada A2 en cascada + preparació A6.
3. Si NO validat → segona ronda amb mineriaRAG (esperem que no calgui).

---

*Document pre-freeze. Es congela versió v1.0 quan mineriaRAG enviï la senyal explícita. Mentrestant, és roadmap intern ATNE per coordinar feina interna sense bloquejar res.*
