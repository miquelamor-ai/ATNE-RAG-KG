# Arrancada propera sessió ATNE — continuació consolidació 35 instruments

**Origen**: tancament sessió ATNE 2026-05-25 (vespre+nit, dues onades).
**Per a**: propera sessió ATNE amb memòria fresca (qualsevol moment a partir de 2026-05-26).
**Actualitzat**: 2026-05-25 nit (segona onada — pilot 4 fet i validat).

---

## Lectura mínima per orientar-se

1. **Memòria principal**: `MEMORY.md` — totes les entrades del projecte.
2. **Memòria operativa**:
   - `project_handoff_mineriarag_20260525.md` — pipeline operatiu + 33 instruments + 4 casos especials V2/V3.
   - `project_parking_opinio_preferencies_contrarelat.md` — 2 instruments futurs decidits.
3. **Docs clau a `docs/`**:
   - `handoff_mineriaRAG_consolidacio_33_2026-05-25.md` — el handoff originari de mineriaRAG.
   - `handoff_a_mineriaRAG_nous_instruments_2026-05-25.md` — el handoff de tornada per a mineriaRAG (a passar quan Miquel vulgui).
   - `parking_opinio_vs_preferencies_2026-05-25.md` — anàlisi Q1.
   - `parking_contrarelat_odi_genere_nou_2026-05-25.md` — anàlisi Q2.

## Estat consolidat a 2026-05-25

| Element | Estat |
|---|---|
| Pipeline mineriaRAG ↔ corpusFJE | ✅ Operatiu (GitHub Action regenera derivats) |
| Pilot 1 — `write-noticia` | ✅ Validat + ja al corpusFJE |
| Pilot 2 — `generate-glossari` | ✅ Validat + ja al corpusFJE |
| **Pilot 3 — `write-opinio`** | ✅ **Validat localment (NotebookLM SÍ amb correccions menors) — PENDENT PUSH al corpusFJE** |
| **Pilot 4 — `generate-bastides-lectura`** | ✅ **Validat NotebookLM (SÍ amb correccions menors, aplicades) — PENDENT PUSH al corpusFJE** |
| Q1 — pre-A1 vs `expressar-preferencies` | ✅ Decisió Miquel: postura D (instrument futur nou) |
| Q2 — contrarelat de l'odi | ✅ Decisió Miquel: opció A.1 (gènere propi únic) |
| mineriaRAG llum verda 2 nous instruments | ✅ Procedir com si validats, citant fonts al cos M\*.md |
| Encaix Fase B 2 nous | ✅ Híbrid: `expressar-preferencies` a lot B.6 · `write-contrarelat-odi` últim lot pre-Fase C |
| Corpus FJE | 35 → **37 instruments** (35 originals + 2 nous) |

## Què cal fer a la propera sessió

### Tasca 0 (5 min) — Recuperar context

Llegir aquesta arrancada + memòria mestra. Mirar el M\*.md d'opinió per veure el resultat de la sessió 2026-05-25.

### Tasca 1 (10 min) — Push de pilot 3 (write-opinio) al corpusFJE

El fitxer canònic ja és a `_bootstrap_fase0/CANONIC_opinio/M3_instrument-escriure-opinio.md`.

Cal:
1. Verificar que el contingut és el final (post-correccions NotebookLM: ordre alfabètic NO aplica, Pas 4 connectors amb 2 dimensions, Pas 9 A2 metacognició polit, metadades 1.1 amb nota regex per A1).
2. Coordinar amb Miquel el push manual al corpusFJE: `skills/generes/write-opinio/M3_instrument-escriure-opinio.md`.
3. Esperar el commit-bot de la GitHub Action.
4. Validar `_derivats_v2/SKILL.md` i `_derivats_v2/prompt_adapter.md` regenerats.

### Tasca 2 — ✅ FETA 2026-05-25 nit — Fase A pilot 4: `generate-bastides-lectura`

**Estat**: completada. M\*.md canònic a `_bootstrap_fase0/CANONIC_bastides-lectura/`, validat NotebookLM (sí-amb-correccions-menors), correccions C1 (terminologia "Frase-buit") + C2 (pausa obligatòria explícita a hipòtesi en curs) aplicades. Commits `65cf8e9` + `b668888` ja a `origin/main`.

**Cas especial confirmat operatiu**: la fusió V2 compartit + V3 dedicat funciona retenint només la dimensió lectura. Patró aplicable a `generate-bastides-produccio` quan toqui (Fase B).

**Novetat arquitectònica validada per NotebookLM**: descriptor `cross_source` **intra-pipeline** (no contra text font, sinó contra output d'altres complements del pipeline). Qualificat com a "**innovació arquitectònica necessària**" → quedar com a **patró canònic per a tots els instruments de mediació amb dependències intra-pipeline**.

**Pendent operatiu**: push del fitxer canònic al corpusFJE: `skills/mediacio/generate-bastides-lectura/M3_instrument-generar-bastides-lectura.md` (coordinació Miquel).

### Tasca 2 bis — Pregunta oberta arquitectònica per a Miquel + mineriaRAG

NotebookLM ha plantejat una pregunta de disseny que cal resoldre abans que es generalitzi el patró `cross_source` intra-pipeline:

> **Pas 4.2** (no duplicar `preguntes_comprensio`): quan `bastides` i `preguntes_comprensio` estan actius simultàniament i `build_skills.py` detecta duplicitat — ha de **generar feedback condicional al docent** (avís de duplicitat) o ha de **resoldre-ho silenciosament l'IA per disseny**?

Afecta: tots els futurs instruments de mediació amb dependència intra-pipeline. **Decisió pendent** — passar a mineriaRAG perquè és la seva àrea (validation runtime).

### Tasca 3 — ✅ FETA 2026-05-25 nit — Validació conjunta Fase A per part de Miquel

**Estat**: Fase A **VALIDADA CONJUNTAMENT**. Veredicte: el patró M\*.md canònic és estable i replicable mecànicament a Fase B.

**5 decisions canòniques** (regiran Fase B) — vegeu memòria [[validacio-conjunta-fase-a-20260525]]:

1. **Asimetria `agent_roles`**: complements `[generator]` (no `adapter`). PRINCIPI NOU: complements es generen segons perfil — el mateix complement pot ser **diferent segons perfil** (glossari TEA ≠ glossari AACC; bastides dislèxia ≠ bastides nouvingut). Documentar modulació per perfil als M\*.md de Fase B.
2. Opinió sense pre-A1 — confirmat. Revisar més endavant amb `expressar-preferencies`.
3. **Variabilitat cardinal de passos** — confirmat com a principi. No s'estandarditza.
4. Bastides-lectura `translanguaging: false` — confirmat. Separació de funcions amb glossari.
5. **Validació NotebookLM obligatòria** per tots els pilots Fase B. No replicació mecànica sense validació.

### Tasca 3 anterior (ja completada) — Validació conjunta

Quan tinguem pilots 3 i 4 al corpusFJE, Miquel valida la Fase A completa abans d'entrar a Fase B.

### Tasca 4 (3-4 setmanes) — Fase B (10 lots temàtics)

Inventari complet i lots a `docs/handoff_mineriaRAG_consolidacio_33_2026-05-25.md`. Recordatori dels casos especials:
- `write-opinio` (V3 ESBORRANY) — ja fet a Fase A.
- `generate-bastides-lectura` (sense V2 dedicat) — Fase A pilot 4.
- `generate-bastides-produccio` (sense V2 dedicat) — Fase B.
- `write-resum` vs `generate-resum-graduat` — **mapatge ambigu**: cal aclarir amb mineriaRAG abans del lot que toqui (probablement B.5 o B.9).

### Tasca 5 — Fase C (switch coordinat, ~22 juny)

mineriaRAG fa el commit únic substituint SKILL.md actuals per `_derivats_v2/SKILL.md`. ATNE actualitza submodule + test 5-10 adaptacions reals.

### Tasca 6 — Post Fase C: 2 instruments nous

Treballar `expressar-preferencies` (Q1) i `write-contrarelat-odi` (Q2). Pendent:
- Coordinació amb mineriaRAG (Miquel ha de passar `handoff_a_mineriaRAG_nous_instruments_2026-05-25.md`).
- Validació externa: Albert Izquierdo Grau (UOC) + GREDICS UAB per al contrarelat.
- Consulta a docents FJE Infantil + equip MALL FJE per a `expressar-preferencies`.

## Patró canònic validat (recordatori)

Cada M\*.md canònic ha de tenir:

1. **Frontmatter** amb `modul`, `titol`, `tipus`, `categoria_principal`, `mecr_range`, `agent_roles`, `moduls_relacionats`, `variables_configurables.fase_lectora`, etc.
2. **Descripció** amb HCL primària/secundàries + connexions MALL + **aclariment d'ús lectura vs producció** (C1).
3. **Detecció** (senyals docent + senyals alumne + context favorable + anti-senyals).
4. **Modulació per nivell** — taula Pas × Dimensió × 6 nivells MECR (5 si exclou pre-A1 com opinió).
5. **Metadades de cel·la** per a `build_skills.py` amb tipus (`countable`, `binary`, `enumerable`, `qualitative`, `structural`, `cross_source`, `metacognitive`) + `requires_source_text` + `validation_hint`.
6. **Heurístiques docent** (3-5 H pràctiques).
7. **Fonts principals**.

**Estructura passos:**
- Variable per instrument (notícia 8, glossari 6, opinió 9...).
- **Pas N-1 = Criteris transversals** sempre.
- **Pas N = Autoavaluació metacognitiva** sempre (reflexió de procés, no producte).

**Decisions pedagògiques aplicades des de l'inici:**
- **C1** — rúbrica descriu text per a LECTURA (no producció autònoma). Sub-pre-A1 via `fase_lectora`, no columnes noves.
- **C2** — Fidelitat al text font gradada per nivell (no "total" a tots).
- **C3** — Pas N (Autoavaluació) reescrit com a metacognició pura, no repetició de passos anteriors.
- **C4-soft** — restriccions retòriques suaus al nivell més alt (C1+).

## Validació recomanada

NotebookLM "Fase 0 — Jutge MALL/MECR" (id `5524a29e-805c-4bf8-b1f7-001a412c9cb9`) — el notebook ja té els 3 pilots anteriors com a fonts. Cada nou pilot puja-l'hi com a source i pregunta-li la mateixa bateria de crítica.

## Compte amb saturació API

A la sessió 2026-05-25 els Agents acadèmics van caure 4 cops amb error 529. Si torna a passar, usa WebSearch directe + NotebookLM com a substitut.

## Memòria viva a actualitzar

Després de cada pilot validat, actualitzar la memòria projecte amb:
- Estat post-pilot.
- Correccions aplicades.
- Aprenentatges nous (si el patró revela un cas no previst).

## Recordatori sobre 2 instruments futurs

`expressar-preferencies` i `write-contrarelat-odi` **NO formen part de Fase A/B/C** dels 33 actuals. Són **instruments addicionals** post-Fase C. No els barregis amb la consolidació en curs.
