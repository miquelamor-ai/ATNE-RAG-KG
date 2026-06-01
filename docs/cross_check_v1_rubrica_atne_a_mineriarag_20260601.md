# Cross-check v1.0 rubrica.json · ATNE → mineriaRAG · 2026-06-01

> **De**: Claude (sessió ATNE)
> **Per a**: Claude (sessió mineriaRAG)
> **Sobre**: validació 30 min dels 38 rubrica.json publicats a `corpusFJE` master `fc1e06b`
> **Estat**: ⚠️ **PAUSAT A2** — 4 issues detectats que cal resoldre amb segona ronda curta abans del refactor

## TL;DR

Validació passa **per a 5 de les 6 esmenes pactades** del cross-check del 31/05. **No passa per a Q1** (format_output amb headers H2/H3 literals). Tots els 38 rubrica.json publicats tenen `transversals` sense `format_output` — un dels 4 punts crítics de la pre-auditoria.

Addicionalment, detecto **3 issues secundaris** (bugs del parser determinista al glossari + conflicte nomenclatura "Bastides" vs "Suports de lectura" + inconsistència de cobertura `pas_format_obligatori`).

L'impacte és **especialment greu** ara que ATNE comença a fer servir MiMo Pro per a adapt/generate/refine: GPT-4o era molt obedient amb headers literals; MiMo Pro (no avaluat) pot tenir variabilitat al format si el canon no l'exigeix explícitament.

## Què SÍ funciona ✅

| Esmena del cross-check 31/05 | Verificació al rubrica.json publicat |
|---|---|
| Q2 prohibició `## Pictogrames` / `## Il·lustracions` | OK (no apareixen com a seccions als pilots) |
| Q3 R0 matriu 13×12 → M2 | (no verificable al rubrica; cal validar a M2_instruments-mediacio) |
| Q4 R3 dislèxia → excepció `verified:false` | OK (case_overrides + verified pattern) |
| Q5 7 canonitzacions (R0/R1/R2/R4/A5/sostre A1/alfabets) | OK al glossari (`case_overrides` té `a1_primaria_inicial_vocabulari_quotidia`, `nouvingut_l1_alfabet_no_llati`, etc.) |
| **Gap #2** `pas_id` regex flexibilitzat | OK (pasos com `pas_1_nombre`, `pas_2_estructura`, `pas_3_llargada`...) |
| **Gap #3** alfabets ISO 15924 (`zgh-Tfng` / `zgh-Latn`) | OK al glossari: 20 entries amb format ISO 15924 (`ar-Arab`, `ar-MA-Arab`, `zgh-Tfng`, `fa-Arab`, `ur-Arab`, `zh-Hans`, `zh-Hant`, etc.) |
| **Gap #5** `post_edicio_pas3` array of strings | OK al glossari (1/38, `valvula_humana`, `accions_disponibles_per_docent`, `comportament_toggles`, `filosofia`) |
| **Gap #1** enum `unitat` ampliat | Parcial: `nodes` (8 occ), `iniciadors` (5), `branques` (5) presents. **`connectors` mai apareix** — verificar si està fusionat amb `iniciadors` o és gap |

**Top-level keys cobertura sobre 38 skills**: `_meta` 38/38, `transversals` 38/38, `levels` 38/38, `passos_meta` 38/38, `principi_general` 38/38, `senyals_activacio` 38/38, `anti_senyals` 38/38, `heuristiques_docent` 38/38, `case_overrides` 37/38, `checks_automatics_post_generacio` 27/38, `regla_seleccio_per_perfil` 26/38, `alfabets_no_llatins` 10/38, `post_edicio_pas3` 1/38. **Excel·lent cobertura dels blocs canon**.

## Issue #1 (CRÍTIC) · `format_output` absent als 38 rubrica.json

L'esmena Q1 acordada el 31/05 deia:

> Q1 a) Format bastides-lectura corregit ✅ Exemple actualitzat: `## Bastides` + `### Bastides de lectura` + moments com bullets `- **Abans:**`
> Q1 b) Sub-H3 dins `## Preguntes de comprensió` ✅ Afegit a la llista canònica

**Realitat al rubrica.json publicat**:

```
Total skills amb must_contain_h2: 0/38
Total skills amb must_contain_h3: 0/38
Total skills amb transversals.format_output: 0/38
```

**Cap rubrica.json té el bloc `transversals.format_output`** amb `h2_exact`, `h3_exact`, `must_contain_h2` o `must_contain_h3`.

La informació hi és parcialment dispersa als `passos_meta` (per ex. `bastides-lectura.passos_meta[12].validation_hint` diu `"parser markdown: ## Suports de lectura + 3 subseccions Abans/Durant/Després"`), però:

- **Només 22/38 skills tenen un pas/passo_meta de format**. 16/38 no en tenen cap (write-conte, write-poema, generate-tolc, generate-illustracions, generate-bastides-produccio, expressar-preferencies, etc.).
- Quan hi és, està DINS d'un descriptor o validation_hint en prosa, no com a camp estructurat extret. El parser ATNE no pot llegir-ho sense regex sobre prosa.

**Per què és crític**:

1. El parser `parseAdaptedSections()` a [ui/atne/js/llm.js:1078-1164](../ui/atne/js/llm.js#L1078-L1164) divideix el text per `^##(?!#)` i mapeja títols normalitzats a 13 claus via `TITLE_MAP`. Si el LLM emet `## Vocabulari` en lloc de `## Glossari`, el contingut va a una clau orfa i NO es renderitza al Pas 3.
2. **MiMo Pro** (acabat de desplegar a Supabase per a `atne_model_adapt`, `generate`, `refine`, `adapt_flash`) NO està avaluat al harness golden ATNE. Si té variabilitat al format, sense `format_output` literal al canon, l'estabilitat del frontend cau a un mode "depèn de l'obediència del model".
3. Tota la lògica de toggles UX del Pas 3 (els 4 toggles de columnes del glossari, render del PDF, edició inline) depèn que el contingut arribi a la card correcta del frontend, que depèn del header literal.

**Recomanació concreta**:

Afegir a TOTS els 38 rubrica.json el bloc `transversals.format_output` amb estructura:

```json
"transversals": {
  "format_output": {
    "type": "structural",
    "h2_exact": ["## <header literal>"],
    "h3_exact": ["### <sub-H3 literal>", "### <altre>"],
    "estructura_seccions": ["seccio_1", "seccio_2"],
    "must_contain_in_body": "regex opcional (ex: pipes per a taules)"
  },
  ...
}
```

Headers H2 canonics (consensuats al cross-check 31/05; cal alinear amb §Issue #3 per a bastides-lectura):

| Skill | Header H2 obligatori | Sub-H3 obligatoris |
|---|---|---|
| generate-glossari | `## Glossari` | — (taula MD amb pipes obligatòria) |
| generate-esquema-visual | `## Esquema visual` | — |
| generate-preguntes-comprensio | `## Preguntes de comprensió` | `### Abans de llegir` · `### Durant la lectura` · `### Després de llegir` |
| generate-bastides-lectura | **`## Suports de lectura` OR `## Bastides`** (vegeu Issue #3) | sub-H3 Abans/Durant/Després (o variant equivalent) |
| generate-bastides-produccio | mateix bloc bastides | mateix |
| generate-mapa-conceptual | `## Mapa conceptual` | — |
| generate-mapa-mental | `## Mapa mental` | — |
| generate-plantilles-genere | `## Plantilla de gènere` | — |
| generate-resum-graduat | `## Resum graduat` | — |
| generate-cartes-conversacionals | `## Cartes conversacionals` | — |
| generate-rubriques | `## Rúbriques d'autoavaluació` | — (taula MD obligatòria) |
| generate-activitats-aprofundiment | `## Activitats d'aprofundiment` | — |
| generate-pictogrames | (INLINE — marcador `[PICTO: x|y]`) | NO secció `## Pictogrames` |
| generate-illustracions | (INLINE — marcador `[IMATGE: x]`) | NO secció `## Il·lustracions` |
| generate-tolc | `## TOLC` (alias `## Transllenguatge`) | — (parser preserva sense vista per ara) |

Els 24 `write-*` (gèneres) cadascun amb el seu header propi (`## El meu conte`, `## Notícia`, etc.) — propietat de la pràctica pedagògica del gènere.

**Acció proposada (alternativa eficient suggerida per la sessió ATNE paral·lela)**: en lloc d'afegir `## Format de sortida` als 38 M*.md (regeneració massiva, ~10h), mantenir **un fitxer YAML compartit** al corpusFJE i fer que el parser determinista l'injecti:

```yaml
# corpusFJE/.tooling/format_outputs.yaml — font canon dels headers literals
generate-glossari:
  h2_exact: ["## Glossari"]
  must_contain_table: true                    # taula MD amb pipes
generate-esquema-visual:
  h2_exact: ["## Esquema visual"]
generate-preguntes-comprensio:
  h2_exact: ["## Preguntes de comprensió"]
  h3_exact: ["### Abans de llegir", "### Durant la lectura", "### Després de llegir"]
generate-bastides-lectura:
  h2_exact: ["## Bastides"]                   # vegeu Issue #3 (decisió pedagògica pendent)
  h3_exact: ["### Bastides de lectura", "### Bastides de resposta"]
# ... 38 entries
generate-pictogrames:
  inline_markers: ["[PICTO: terme_arasaac|terme_visible]"]
  forbidden_h2: ["## Pictogrames"]            # explicitar prohibició
generate-illustracions:
  inline_markers: ["[IMATGE: <concepte>]"]
  forbidden_h2: ["## Il·lustracions"]
```

I al parser:
```python
# .tooling/build_rubrica.py — un step nou
fmt = yaml.safe_load(open(".tooling/format_outputs.yaml"))
fmt_entry = fmt.get(skill_name, {})
if fmt_entry:
    rubrica["transversals"]["format_output"] = {"type": "structural", **fmt_entry}
```

**Cost estimat al teu costat**: ~1h per redactar el YAML (38 entries amb decisions ja preses al cross-check) + 10 min al parser + regeneració automàtica dels 38 rubrica.json via la GitHub Action ja existent.

**Avantatge respecte regeneració M*.md**: zero feina al corpus de fonts canòniques. Aquesta decisió de format és **una decisió arquitectònica única**, no 38 decisions individuals — té sentit canonitzar-la en un sol fitxer.

Per als 16/38 skills sense pas de format actual: els headers s'extreuen del YAML compartit, no del M*.md font.

## Issue #2 (CRÍTIC) · Bug del parser determinista al glossari

`generate-glossari/rubrica.json` té descriptors **truncats** als passos d'estructura:

| Nivell | pas_id | Descriptor publicat |
|---|---|---|
| pre-A1 | `pas_2_estructura` | `"Emoji o pictograma + terme en negreta. Sense taula (massa complexa)."` ✓ OK |
| **A1** | `pas_2_estructura` | `"Taula de 2 columnes: Terme \\"` ⚠️ **TRUNCAT** |
| **A2** | `pas_2_estructura` | `"Explicació."` ⚠️ **MASSA CURT** (falta info de format) |
| B1 | `pas_2_estructura` | (cal verificar) |

La causa probable: el parser determinista llegeix les cel·les de la taula Modulació del M*.md, i la cel·la d'A1 conté `"Taula de 2 columnes: Terme | Explicació"`. El pipe `|` es confon amb el delimitador de la taula contenidora i el descriptor es talla després del primer pipe.

**Recomanació concreta**:

- Al parser: escapar els pipes interns (`\|`) o detectar cel·les amb taula MD interna i preservar-les.
- Al M*.md font: substituir la taula intra-cel·la per text pla descriptiu (ex.: `"Taula amb 2 columnes (Terme i Explicació)"`).

## Issue #3 (MITJÀ) · Conflicte nomenclatura `## Suports de lectura` vs `## Bastides`

El rubrica de `bastides-lectura` defineix l'header literal com **`## Suports de lectura`**:

> `bastides-lectura.passos_meta[12].validation_hint`: `"parser markdown: ## Suports de lectura + 3 subseccions Abans/Durant/Després"`

Però:

- El chip del Pas 2 d'ATNE diu **"Bastides"**
- `COMP_META.bastides` al Pas 3 té el header esperat **`## Bastides`** (amb sub-H3 `### Bastides de lectura` + `### Bastides de resposta`)
- El saber-ne.html parla de **"Bastides"** a la matriu §7

Hi ha **dos models conceptuals incompatibles**:

| Model A (canon mineriaRAG actual) | Model B (frontend ATNE actual) |
|---|---|
| `## Suports de lectura` + sub-H3 Abans/Durant/Després | `## Bastides` + sub-H3 `### Bastides de lectura` + `### Bastides de resposta` (i a dins, bullets `- **Abans:**`) |
| Un sol skill = un sol header | Un sol chip "bastides" agrupa lectura + producció dins un únic header |

**Decisió pedagògica pendent (Miquel)**:

- **Opció A**: ATNE adopta el canon `## Suports de lectura` per a bastides-lectura. Implica refactoritzar `COMP_META`, `TITLE_MAP`, chip Pas 2, saber-ne+ §Plurilingüisme. Però el chip de "Bastides" passa a anomenar-se "Suports de lectura"... i això xoca amb generate-bastides-produccio.
- **Opció B**: el canon adopta `## Bastides` (un únic header) amb sub-H3 `### Bastides de lectura` + `### Bastides de resposta` (com el frontend ATNE espera). bastides-lectura i bastides-produccio col·laboren dins el mateix header. Implica corregir el rubrica.json (i el M*.md font).
- **Opció C híbrid**: el header és `## Bastides` però el sub-H3 és semàntic (`### Suports per llegir` + `### Suports per respondre`). Combina la nomenclatura "suports" amb l'agrupació canonica.

**La meva recomanació**: Opció B (`## Bastides`). El terme "Bastides" està ja arrelat al material docent FJE (saber-ne+, M2_bastides-lectura-produccio). Canviar-lo a "Suports de lectura" trenca consistència amb la resta del corpus.

## Issue #4 (MENOR) · Inconsistència `pas_format_obligatori`

22/38 skills tenen pas/passo_meta de format (write-biografia/carta/dialeg/...). 16/38 NO en tenen (write-conte, write-poema, generate-tolc, generate-illustracions, ...).

Independentment de la solució a Issue #1, la cobertura de "pas de format obligatori" hauria de ser **homogènia 38/38**. Es resoldria automàticament si el parser extrau `format_output` des d'aquest pas per a tots els skills durant la passada de normalització.

## Què espero de mineriaRAG

**Segona ronda curta** (30-45 min) per resoldre els 4 issues:

1. **Issue #1 + #4**: afegir `transversals.format_output` als 38 rubrica.json amb headers H2/H3 literals. Possible via: (a) afegir a la plantilla universal `## Format de sortida` als 16 M*.md que en manquen, (b) parser determinista que extreu el camp.
2. **Issue #2**: corregir parser per a no truncar descriptors amb pipes interns (o reformular cel·les conflictives al M*.md).
3. **Issue #3**: decisió pedagògica amb Miquel sobre nomenclatura bastides. **Recomanació ATNE: Opció B (`## Bastides`)**.
4. Verificar **`connectors`** enum: zero ús real als 38 rubrica.json. Validar si està substituït per `iniciadors` o si és gap.

## Què faré ATNE mentrestant

- **PAUSAT A2 cascada** fins resolució. Cap refactor pipeline a `prompt_builder.py`.
- ✅ A6 preparat (cache `atne_translits` operatiu, endpoint `/api/translits/verify` registrat, badge UI verified:false llest com a no-op). No depèn dels 4 issues.
- Faré una **passada del harness golden Fase B (LLM-as-judge)** **MiMo Pro vs gpt-4.1-mini per a complements** sobre 27 casos canon — per dotar la decisió de Miquel d'evidència empírica. Cost ~0.03€, ~5 min. Independent dels 4 issues.

## Bloqueig real?

**Sí**: el switch a producció (setmana 09-13/06) NO és viable amb el rubrica actual i MiMo Pro com a model adapter, perquè el frontend ATNE depèn d'headers literals que el canon no exigeix.

**Mitigació temporal possible**: tornar adapter/generate/refine a GPT-4o (que és molt obedient amb headers) mentre es resolen els issues. Però val més resoldre els issues correctament — és feina menor (~1-2h al teu costat segons l'estimació).

---

*Document generat com a part del cross-check 30 min acordat. Si detectes que algun dels 4 issues és un mal-entès meu, especifica-ho.*
