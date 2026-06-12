# ATNE-RAG-KG — Resum de sessió (2026-03-27, actualitzat)

---

## Sessió 2026-06-12 — Auditoria creuada + bugs pedagògics + R0 «Per al docent»

### ✅ DEPLOY 2026-06-12 12:15
- Merge a main: `f1d0f28`. Cloud Build `a6f02221` **SUCCESS** → Cloud Run revisió
  `atne-00623-vt6` (servint des de 12:15). URL: `https://atne-1050342211642.europe-west1.run.app`.
- **Verificat (codi desplegat f1d0f28):** AACC+dislèxia 2n ESO → **B1/Core**; traça SENSE
  «AACC sense 2e». Bug B1 mort a prod. (Traça calenta via UI/auth pendent — endpoint auth-gated.)

### Fet (branca `fix/bugs-pedagogics-auditoria-20260612`, mergejada a main `f1d0f28`)
- **B1 🔴 (viu en producció): 2e rebia text MÉS difícil.** El resolver depenia d'un flag
  que cap UI establia → AACC+dislèxia donava B2/Enriquiment. Fix: autodetecció `_is_2e`
  (AACC + constitutiva). Veure `docs/adr/ADR-001-2e-doble-excepcionalitat.md`.
- B2 (adequació preguntes per etapa), B3 (guard bool resolver), B4 (avís malformats),
  B6 (codi mort: `_mecr_from_etapa_curs`, `_all_titles_re`, `n`), B7 (`_safe_error` SSE).
- **R0 «Per al docent» tancat**: ATNE consumeix `corpusFJE/.tooling/per_al_docent.json`
  (era hardcoded; cicle R0 com la matriu). Submodule bumpejat a cb9918a.
- CI determinista mínim a `.github/workflows/ci.yml`.

### ⚠️ Seguiment post-deploy
- **Avís pilot:** si algun docent havia generat adaptacions per a alumnes 2e abans del fix,
  les noves sortiran DIFERENTS (millors). Que no el sorprengui.
- (Opcional) traça calenta de `/api/derive-params` amb sessió @fje.edu per confirmar a la UI.

### 📋 Backlog
- **30 WARN de `prompt_checks`** (294 PASS, 0 ERROR — no bloquegen): un dia de calma,
  mirar què avisen (artefacte finestra 3K a GENERE_specific_format + hints GLOSSARI_L1).
- **21 imports morts a server.py** (cosmètic, pyflakes `imported but unused`).
- **Ratificació DOP** de la definició 2e (ADR-001) — no bloquejant.
- Des-triplicació frontend «Per al docent» via `.data.js` (opcional; ara guard de drift).

---

## Sessió 2026-03-27 (tarda) — Historial de textos anteriors

### Problema resolt
- Servidor antic (PID 42656, iniciat el 24-03) continuava corrent amb codi obsolet
- Calia matar-lo manualment (PowerShell `Stop-Process`) per carregar el codi nou

### Canvis implementats

#### 5. Historial de textos anteriors (GET /api/history + UI)
- **Nou endpoint** `GET /api/history` → llista les 30 últimes adaptacions de Supabase
- **Panell desplegable** al pas 2 (sota el textarea):
  - Badge amb nom del perfil + data + previsualització 200 caràcters
  - "Carrega text" → omple textarea (manté perfil actual)
  - "Carrega text + perfil" → restaura text + característiques + context (etapa, curs, etc.) i va al pas 1
  - Notificació blava 6s en restaurar perfil complet
- **Cache invalidada** automàticament en desar nova adaptació
- Pre-càrrega silenciosa en obrir l'app

#### 6. Fixes SSE/Gemini (inclosos al mateix commit)
- `timeout=180_000` al client Gemini (generacions llargues)
- `max_output_tokens=16384` (era 8000)
- `thinking_config=ThinkingConfig(thinking_budget=0)` per evitar tokens thinking
- Keepalive SSE (`: keepalive\n\n`) cada 0.5s per evitar QUIC_NETWORK_IDLE_TIMEOUT
- Dedup event `done` (flag `_doneHandled`)
- Avís si Gemini trunca per MAX_TOKENS

### Push
- `miquelamor-ai/ATNE-RAG-KG` (origin) ✓
- `FundacioJesuitesEducacio/ATNE` (fje) ✓ — remote afegit i push confirmat

### Remote FJE
El repo `FundacioJesuitesEducacio/ATNE` (branca main) és el mateix codi que ATNE-RAG-KG.
Ara té dos remots configurats: `origin` (personal) i `fje` (institucional).

---

# ATNE-RAG-KG — Resum de sessió (2026-03-27)

## Repo
- **Local**: `C:\Users\miquel.amor\Documents\GitHub\ATNE\`
- **Remote origin**: `https://github.com/miquelamor-ai/ATNE-RAG-KG.git`
- **Branca**: `main`
- **Deploy**: Cloud Run `atne-00011-rqn` → `https://atne-1050342211642.europe-west1.run.app`
- **Projecte GCP**: `dreseraios-drive`

## Stack
Python 3.12 + FastAPI + Gemini 2.5-flash + Supabase (RAG-KG) + Cloud Run

## Canvis fets (2026-03-25 → 2026-03-27)

### 1. Reorganització de repos (2026-03-25)
- Repo `miquelamor-ai/ATNE` traspassat a `FundacioJesuitesEducacio/ATNE`
- Nou repo personal `miquelamor-ai/ATNE-RAG-KG` per la versió Python
- Creada carpeta local ATNE-FJE per la versió institucional PHP

### 2. Cursos i àmbits dinàmics per etapa (2026-03-25)
- FP: 1r/2n CGM, 1r/2n CGS + 25 famílies professionals
- Cada etapa amb cursos propis

### 3. Doble excepcionalitat — 2e (2026-03-25)
- Detecció automàtica: quan AC + qualsevol altra → alerta groga al pas 1
- Bloc informatiu al pas 3 Proposta amb combinació específica
- Eliminada sub-variable manual `doble_excepcionalitat` (redundant)
- CSS: `.alert-2e`, `.proposal-2e` (colors ambre/groc)
- Briefing per mineriaRAG: `briefing_2e_mineriaRAG.md`

### 4. Ampliació variables configurables (2026-03-27)
Sincronització amb briefing mineriaRAG `briefing_variables_ATNE_2026-03-27.md`:
- **TDAH**: 4 subvars noves (presentació DSM-5, grau, memòria treball, fatiga)
- **Dislèxia**: 4 subvars noves (tipus ruta, grau, tipografia adaptada, columnes estretes)
- **TDL**: 8 subvars noves (modalitat, 5 components, grau, bilingüe)
- **TDC/Dispraxia**: nova característica + 4 subvars (grau, motricitat fina/grossa, accés teclat)
- **Disc. visual**: grau ampliat 2→3 (baixa_visio_moderada, baixa_visio_greu, ceguesa)
- **Disc. auditiva**: `mixta` → `bimodal`
- Total: 13 característiques, 40 variables configurables

## Qüestions pendents

### Per fer
- [ ] Renombrar carpeta local `ATNE` → `ATNE-RAG-KG` (cal tancar VSCode primer)
- [ ] Actualitzar corpus mineriaRAG amb briefing 2e
- [ ] Actualitzar corpus mineriaRAG amb noves variables (briefing a mineriaRAG/output/)
- [ ] Implementar CSS tipografia dislèxia (subvar `tipografia_adaptada`)
- [ ] Implementar CSS columnes estretes (subvar `columnes_estretes`)
- [ ] Pujar fitxer PDF/DOCX al pas 2

### Notes
- Sensibilitat temàtica (trauma) a vulnerabilitat i trastorns emocionals: camp manual, no al corpus
- La detecció 2e funciona amb qualsevol combinació AC + altra (inclou noves: TDC, TDL, etc.)

## Estructura de carpetes

```
Documents/GitHub/
├── ATNE/              ← AQUEST PROJECTE (Python + RAG-KG) — renombrar a ATNE-RAG-KG
│   origin: miquelamor-ai/ATNE-RAG-KG.git
│   Deploy: Cloud Run (atne) — https://atne-1050342211642.europe-west1.run.app
│
└── ATNE-FJE/          ← Versió institucional (PHP + OpenAI)
    origin: FundacioJesuitesEducacio/ATNE.git (branca spec/mvp-migracio-php)
    Deploy: Cloud Run (atne-fje) — https://atne-fje-1050342211642.europe-west1.run.app
```
