# ATNE — SESSION LOG i ESTAT DEL PROJECTE
> **Instrucció d'ús:** executa `bash log.sh` per actualitzar la secció d'estat.
> La part objectiva (branques, commits) s'omple automàticament.
> La part de coordinació (xats actius, decisions) l'actualitzes tu a mà sota.

---

## 🗂️ ESTAT ACTUAL — 2026-06-16 08:39

### Repositori
- **Branca activa:** `main`
- **Working tree:** ⚠️ 0 fitxers modificats · 1 untracked
- **main vs origin:** ✅ sincronitzats (`2ffeb54`)

**Últims commits a main:**
-` `2ffeb54 Merge pull request #11 from miquelamor-ai/feat/tests-avaluacio-v2
-` `8bdad3e feat(tests): harnesses d'avaluació (titella e2e + multimodel eval/test)
-` `d9bc21f Merge pull request #10 from miquelamor-ai/docs/handoff-stem-curriculum-v2

**Branques obertes (ahead de main):**
- `spec/mvp-migracio-php` — 1 ahead · 771 behind

### 🔴 Espera decisió meva
<!-- Actualitza manualment: push/merge/decisions pendents -->
- **mineriaRAG ha de respondre el handoff STEM+currículum** (`docs/handoff_mineriarag_stem_curriculum_20260615.md`, a main) abans que ATNE pugui implementar.
- **Firmar ADR-003** → pendent resposta DPO FJE (B1 base jurídica + B2 k-anonimat). ADR-003 segueix untracked (no versionat fins firma).
- *(ronda de merges de documentació TANCADA — PRs #8-#11 a main, branques esborrades)*

### 🟡 En marxa (xats actius)
<!-- Actualitza manualment: qui treballa què i a quina branca -->
- (cap xat actiu)

### 📋 Backlog
- RAG/KG desactivat des del 9/04 — decidir reactivar o retirar
- Neteja branques velles a origin (~15 punters antics)
- Bucle de millora (ADR-003) — bloquejat fins al DPO FJE
- Tercer jutge Claude per al framework d'avaluació
- SVG diagrames a l'export PDF/DOCX
- Multi-agent (Adaptador→Auditor→Corrector→Traductor)
- Memòria triàdica (StudentMemory/ClassMemory/SubjectProfile)
- Decisió motor institucional FJE
- Gemma 4 com a motor sobirà

---

---

---

---

---

---

## ⚙️ INFRAESTRUCTURA (referència fixa)
- **Repos:** `origin` = `miquelamor-ai/ATNE-RAG-KG` · `fje` = `FundacioJesuitesEducacio/ATNE`
- **Deploy:** Cloud Run `europe-west1` → `https://atne-1050342211642.europe-west1.run.app`
- **Working tree local:** `C:\Users\miquel.amor\Documents\GitHub\ATNE\` ⚠️ compartit entre xats
- **CI:** `.github/workflows/ci.yml` · Node 24 · secret `CORPUSFJE_PAT` · 8/8 jobs
- **Regla de governança:** cap push/merge sense ordre de Miquel · verificar amb `bash log.sh`

---

## 📋 HISTORIAL DE SESSIONS

### Sessió 2026-06-15 — Disseny STEM + currículum (handoff a mineriaRAG)

- **Handoff a mineriaRAG redactat** (`docs/handoff_mineriarag_stem_curriculum_20260615.md`).
- **Decisions:**
  - STEM = secció **invariant disciplinari** dins les SKILLs de gènere (NO subsistema nou), graduada per MECR, format taula **ADAPTABLE | INVARIANT** auditable, fonamentada en el principi del 2e (eix lingüístic ⊥ eix disciplinari, ADR-001).
  - Currículum en **2 fases**: F1 = selector cascada determinista + injecció mecànica del text del saber (canon ja complet); F2 = pont pedagògic saber→text (diferit).
- **Risc detectat:** divergència entre `schema_lomloe.json` i el JSON real de mates (`sabers_basics`/`cursos.<curs>` vs `sabers_items` pla) — mineriaRAG ha de confirmar la **forma canònica** abans que ATNE construeixi el parser.

### Sessió 2026-06-13/15 — Release + Editor de diagrames + Decisió de models

#### ✅ A main, CI verd
- **Mapa conceptual Novak graduat per MECR** (`ac7729e`): proposicions verbals B1+, categories nominals A2, fallback graduat al `prompt_builder`, canon v4.1.1
- **CI determinista instal·lat** (`c82d4a3`): `.github/workflows/ci.yml`, secret `CORPUSFJE_PAT` configurat, Node 24, 8/8 jobs verds
- **Bugs pedagògics B1-B7** (`a123b28`): bug 2e (resolver autodetecta doble excepcionalitat), B2-B7 (seguretat SSE, guards, codi mort)
- **Bloc A editor diagrames** (`041c791`): correccions renderitzador A1-A4 (layout recursiu, fork horitzontal, routing, z-order creuats)
- **Node 24** (`e08fe44`): PR #1, deprecació GitHub 16/06 coberta
- **J2 cross-judge + ADR-002 firmat** (`544a625`): jutge gemini-2.5-flash homogeni 21/21, artefacte self-judging corregit, decisió: empat dins variància → mana compliance
- **Bloc B editor Novak** (PR #2): subsistema d'edició interactiu (+/×/↝/Ctrl+Z), modulació profunditat per MECR
- **Mapa mental + Esquema visual** (PRs #4-#7): dos nous tipus de diagrama, routing creuats millorat
- **Fix header offset** (`a0b7695`): +/×/germana operaven a la branca equivocada (capçalera ## desplaçava índexs +2)

#### Decisions clau
- **ADR-002**: gemini-2.5-flash per al prototip (free tier + compliance UE, NO per qualitat — empatat amb gpt-4o dins variància del jutge)
- **ADR-003 (ESBORRANY)**: bucle de millora via few-shot (`get_fewshot_example()`), gate compliance multicapa, `observacions` exclòs de l'exemplar per defecte. Pendent DPO.
- **RAG/KG desactivat** des del 9/04 — troballa de l'auditoria del bucle: codi mort, zero crides reals

#### Eines de govern creades
- `log.sh` (aquest script) — actualitza l'estat del SESSION_LOG automàticament
- `estat.sh` — taulell ràpid de branques i commits
- `docs/ESTAT_DEL_DIA_plantilla.md` — plantilla de taulell manual

---

### Sessió 2026-06-12 — Auditoria creuada + bugs pedagògics + R0 «Per al docent»

#### ✅ DEPLOY 2026-06-12 12:15
- Merge a main: `f1d0f28`. Cloud Build `a6f02221` **SUCCESS** → Cloud Run revisió `atne-00623-vt6`
- **Verificat:** AACC+dislèxia 2n ESO → **B1/Core**; traça SENSE «AACC sense 2e». Bug B1 mort a prod.

#### Fet (branca `fix/bugs-pedagogics-auditoria-20260612`, mergejada a main `f1d0f28`)
- **B1 🔴 (viu en producció): 2e rebia text MÉS difícil.** El resolver depenia d'un flag que cap UI establia → AACC+dislèxia donava B2/Enriquiment. Fix: autodetecció `_is_2e`. Veure `docs/adr/ADR-001-2e-doble-excepcionalitat.md`.
- B2-B7: adequació preguntes per etapa, guards bool resolver, codi mort, `_safe_error` SSE
- **R0 «Per al docent» tancat**: ATNE consumeix `corpusFJE/.tooling/per_al_docent.json` (era hardcoded)
- CI determinista mínim afegit

---

### Sessió 2026-03-27 (tarda) — Historial de textos anteriors

- Nou endpoint `GET /api/history` + panell desplegable al pas 2
- Fixes SSE/Gemini: timeout, max_output_tokens, keepalive
- Doble excepcionalitat (2e): detecció automàtica + alerta UI
- Ampliació variables: 13 característiques, 40 variables configurables (TDAH, dislèxia, TDL, TDC/dispraxia, disc. visual, disc. auditiva)

---

### Sessions 2026-03-23/26 — Base del sistema

- App completa: backend FastAPI, frontend vanilla HTML/JS/CSS, export PDF/DOCX/TXT, Cloud Run
- Historial d'adaptacions amb feedback docent (Supabase)
- Spec MVP migració PHP/OpenAI + corpus 7 MDs
- Creuament variables, càrrega cognitiva, camps perfil nous

---

## Estructura de carpetes

```
Documents/GitHub/
├── ATNE/              ← AQUEST PROJECTE (Python + RAG-KG)
│   origin: miquelamor-ai/ATNE-RAG-KG.git
│   Deploy: Cloud Run → https://atne-1050342211642.europe-west1.run.app
│
└── mineriaRAG/        ← Gestió corpus i canon
    origin: miquelamor-ai/mineriaRAG
```

---

## 📖 GUIA DE MÈTODE (secció estable — el `log.sh` NO la regenera)
> Migrada de l'antic `ESTAT_DEL_DIA.md` (unificat 2026-06-16). El `log.sh`
> només toca la capçalera 🗂️ de dalt; tot el que va sota el bloc d'historial
> és estable.

### Com l'uso (3 moments)
1. **Obro un xat nou** → primera línia: "Vinc de [tasca], branca [X]; aquí vull [Z]". Enganxo context del taulell.
2. **Canvio de tasca o tanco un xat** → actualitzo les seccions 🔴🟡 (30 segons).
3. **Torno a un xat després d'estona** → llegeixo el taulell abans de res. En 10 segons sé on soc.

### Quan val la pena un worktree
Si DOS xats han de tocar CODI alhora en branques diferents → `git worktree add ../ATNE-[tasca] [branca]`.
Un directori per tasca = cap xat mou el terra a un altre.
