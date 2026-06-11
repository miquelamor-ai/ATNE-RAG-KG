# Auditoria pipeline ↔ saber-ne+ (contracte didàctic) — 2026-06-09

**Objectiu:** verificar que el motor d'ATNE (el codi) fa el que saber-ne+ PROMET
(el contracte didàctic per a docents), tant al flux **Taller** com al **Flash**.

**Mètode:** mapeig estàtic del codi (no LLM) + tests golden offline + 1 fix
test-first. NO s'ha tocat `ui/saber-ne.html` (s'audita en paral·lel).

---

## 1. El contracte (saber-ne+ / mapa de taxonomies canonitzat 06/06)

Una adaptació ATNE té **tres taxonomies** que s'han de reflectir al pipeline:

| # | Promesa | Què és | Qui ho fa al codi |
|---|---------|--------|-------------------|
| VIA 1 | **3 transformacions** (lingüístiques · estructurals · contingut curricular) | toquen el TEXT | adapter (Call 1) — macrodirectives `instruction_catalog` + skills `write-*` |
| VIA 2 | **complements** (12 eines en 6 categories MALL) | s'AFEGEIXEN al costat | Call 2 (`build_complements_prompt`) + skills `generate-*` |
| Factura | **Per al docent** (9 categories A–I) | explica QUÈ s'ha transformat + afegit | secció `## Argumentació pedagògica` |

> Ajuts (docent en directe) i Crossa (alumne) són les 2 categories MALL que ATNE
> **NO** genera — correctament absents de `COMPLEMENT_DEFS`.

---

## 2. Veredicte per promesa

### ✅ Arquitectura 2-call — CORRECTE
- Trigger a [orchestrator.py:147-167](../adaptation/orchestrator.py#L147): `_two_call = is_skills_enabled() AND any(complements)`. Coincideix amb el contracte.
- Call 1 = adapter (`_model_for("adapt")` → gpt-4o), Call 2 = complements (`_model_for("complements")` → gpt-4.1-mini). ✅
- Complements INLINE (pictogrames, il·lustracions, activitats) van a Call 1; complements SECCIÓ (glossari, bastides…) a Call 2. Documentat i coherent.
- Fallbacks (Call 1 buida → no Call 2; Call 2 falla → text preservat + warning SSE; retry de seccions absents). ✅

### ✅ 3 transformacions (VIA 1) — REFLECTIDES
- `instruction_catalog.py` (84 instruccions) amb macrodirectives LÈXIC/SINTAXI/ESTRUCTURA/COGNITIU/QUALITAT/MULTIMODAL/AVALUACIO/PERSONALITZACIO/PERFIL → cobreixen lingüístiques + estructurals + contingut.
- `instruction_filter.get_instructions()` filtra per perfil + sub-variables + MECR + DUA.
- Skills `write-*` aporten l'estructura de gènere. La regla "adaptar el COM, mai el QUÈ" viu al prompt. ✅

### ✅ 6 complements MALL (VIA 2) — REFLECTITS
- Els 12 complements UI mapegen a skills via `COMP_TO_SKILL` ([skills_loader.py:456](../skills_loader.py#L456)).
- Matriu condició→complements consumida del canon (`matriu_cobertura.json` → `complements-matriu.data.js`), amb test anti-drift deep-equal + golden snapshot 711 combinacions. ✅

### 🔴→✅ "Per al docent" 9 categories A–I — BUG TROBAT I FIXAT (test-first)
**Símptoma:** el camí 2-call (`adapter_only=True`, el que s'usa amb skills+complements
actius) generava l'estructura **ANTIGA de 5 punts** ("adaptació lingüística, atenció
a la diversitat, suport multimodal, gradació cognitiva, rigor curricular"), NO les 9
categories A–I que el frontend (`pas3.html` dimMap) espera i que la crida única ja
generava. Mateix patró que el bug històric del `# Títol`.

**Causa arrel:** el bloc de 9 cat estava **duplicat** — només a la crida única
([prompt_builder.py], bloc de ~80 línies). El camí adapter_only en tenia una còpia
antiga divergent.

**Fix (2026-06-09):**
1. Test-first: nou check `PER_AL_DOCENT_9_categories` (ERROR) a
   [prompt_checks.py](../tests/golden/prompt_checks.py) que assereix les 9 cat al
   prompt adapter_only i prohibeix l'estructura antiga de 5 punts. Va FALLAR (3/9
   categories absents + legacy present), capturant el bug.
2. Extret el bloc a una **constant única** `_ARGUMENTACIO_9CAT_BLOCK` a dalt de
   [prompt_builder.py](../adaptation/prompt_builder.py), usada pels DOS camins
   (adapter_only + crida única). Elimina la duplicació que causa el drift.
3. Verificat: check PASSA, 0 errors als 27 casos, exactament 1 bloc de 9 cat per
   camí, sense legacy. `GENERE_present_at_end` (recency del gènere) segueix 27/27.

> **Tema PEDAGÒGIC encara obert (no de codi):** re-validació NotebookLM de la
> sortida real post-A–I — si les 9 cat són el format final o cal ajustar-les. Veure
> `project_per_al_docent_9categories_obert_20260602`. El fix de codi NOMÉS
> sincronitza; no decideix la pedagogia.

### ✅ Drift canon ↔ codi — NET (ATNE = consumidor, no origen)
- ATNE LLEGEIX el canon (rubrica.json, matriu_cobertura.json, skills, M*.md);
  cap escriptura de JSON canon. Fallbacks segurs ("" / None).
- Derivat incrustat `complements-matriu.data.js` amb guard anti-drift + golden snapshot.
- `_forma_sobre_mecr_canon` i pictogrames llegeixen del canon (hardcoded arxivat).

---

## 3. ⚠️ DIVERGÈNCIA ESTRUCTURAL: Flash ≠ Taller (decisió pendent de Miquel)

**Flash i Taller són dos motors diferents:**

| | **Taller** (`/api/adapt`) | **Flash** (`/api/adapt-flash`) |
|---|---|---|
| Entry point | `run_adaptation` (orchestrator) | `adapt_flash` (server.py:4730) |
| Prompt | `build_system_prompt` (catàleg + skills + DUA) | `_build_flash_system_prompt` (MVP propi) |
| Arquitectura | 2-call (adapter + complements) | **1 sola crida** |
| Skills / canon | SÍ | **NO** (perfils via `_FLASH_PERFIL_MAP` simplificat) |
| Verify/Retry + quality CA | SÍ | **NO** |
| Complements | 12 | **3** (glossari, preguntes, resum) |
| **Per al docent (9 cat)** | SÍ (ara fixat) | **NO existeix** |
| 3 transformacions | catàleg complet | versió condensada |

**Implicació:** saber-ne+ descriu el contracte COMPLET. Flash, per disseny, n'implementa
una fracció reduïda (mode ràpid).

**✅ DECISIÓ Miquel 2026-06-11 — OPCIÓ A:** Flash es manté com a **mode ràpid "lite"**
i saber-ne+ ho explicita. NO convergeix cap al contracte complet. Acció de codi feta:
banner intencional al docstring de `adapt_flash` (server.py) perquè ningú "arregli"
Flash afegint-hi skills/2-call/Per-al-docent. Acció de text PENDENT a saber-ne+ (altre
xat): dir explícitament que Flash = mode ràpid amb subconjunt del contracte.

---

## 3-bis. Reconciliacions codi → saber-ne+ (ground truth per a l'altre xat)

Verificat al codi 2026-06-11. saber-ne+ té text desactualitzat en aquests punts:

### #7 Models — DISCREPÀNCIA REAL (cal actualitzar saber-ne+)
`server._MODEL_CONFIG` (defaults runtime):

| Tasca | Model real |
|---|---|
| adapt (Taller adapter, Call 1) | **gpt-4o** |
| complements (Taller Call 2) | **gpt-4.1-mini** |
| adapt_flash (Flash) | **gpt-4o** (1 crida) |
| auditor | gpt-4.1-mini |
| refine / generate | gpt-4o |

- saber-ne+ §09 (≈línia 2495) diu *"El model per defecte és **Gemma 4 31B**, amb rotació
  opcional a GPT-4o i GPT-4.1-mini"* → **FALS** al runtime. Gemma NO és per defecte des de
  2026-04-12; decisió GPT-4o/GPT-4.1-mini el 27/05.
- saber-ne+ §11 (≈línia 2674) destaca "Gemma 4 31B" com a card principal → desactualitzat.

### #6 Nombre d'instruccions — DESACTUALITZAT
`len(instruction_catalog.CATALOG)` = **122** (SEMPRE 24 · NIVELL 37 · PERFIL 58 · COMPLEMENT 3),
en 10 macrodirectives.
- saber-ne+ §10 (≈línia 2523) diu *"Més de 90 instruccions"* i §09 (≈línia 2488) *"unes 40
  de 90+"* → el **40 actives típiques** és plausible (denominador APLICABLE per perfil), però
  el **total "90+" hauria de ser ~122**.

### §09 pipeline 1-call ↔ 2-call — A COMPLETAR (desbloquejat per Opció A)
saber-ne+ §09 descriu el pipeline com una sola crida (3 passos). Ara que Flash=A:
- **Taller** = **2-call**: adapter (gpt-4o) genera text + «Per al docent» (9 cat); després
  complements (gpt-4.1-mini) generen glossari/bastides/… El trigger és skills + complements.
- **Flash** = **1-call** "lite" (gpt-4o), 3 complements, sense «Per al docent».

---

## 4. Punts menors / observacions

- `pas3.html` dimMap manté 5 fallbacks legacy (estructura antiga) com a xarxa
  defensiva. Amb el fix, ja no s'haurien d'activar mai al 2-call; es poden retirar
  en una neteja futura (no urgent — són inofensius).
- `GENERE_specific_format` (check WARN) va de 7→11 avisos perquè el bloc de 9 cat
  (~3KB) empeny algunes keywords de format fora de la finestra dels últims 3000 chars
  del check. Artefacte del test, no del prompt (el detall de format viu a la SKILL i
  `GENERE_present_at_end` ERROR passa 27/27). No-acció.
- `Diagrama 0` de `docs/mapa_taxonomies_visual.md` (Mermaid) manté l'estructura
  ANTIGA del diagrama vs el nou HTML natiu de saber-ne+ §05b — drift menor de docs.

---

## 5. Fitxers tocats en aquesta auditoria
- `adaptation/prompt_builder.py` — constant `_ARGUMENTACIO_9CAT_BLOCK` + ús als 2 camins.
- `tests/golden/prompt_checks.py` — nou check `PER_AL_DOCENT_9_categories`.
- `docs/auditoria_pipeline_saber-ne_20260609.md` — aquest informe.
