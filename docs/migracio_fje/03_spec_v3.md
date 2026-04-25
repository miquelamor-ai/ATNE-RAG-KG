# ATNE — Especificació de migració al stack FJE

**Versió**: 3.0
**Data**: 2026-04-23
**Origen**: migració del prototip ATNE (Python/FastAPI/Supabase/GCP) al stack institucional FJE
**Destí**: repo `FundacioJesuitesEducacio/ATNE`, branca `main`

> Aquest document substitueix el [SPEC_MVP_AZURE.md](../../SPEC_MVP_AZURE.md) v2.1 del 2026-03-24 (quedava obsolet: només cobria 4 característiques i 3 variables, sense SSE, skills, auth, il·lustracions, instrumentació pilot, etc.).

## 0. TL;DR

| Punt | Valor |
|---|---|
| Repo destí | `FundacioJesuitesEducacio/ATNE` branca `main` |
| Frontend | HTML + JavaScript pur + CSS (0 frameworks) — còpia 1:1 de `ui/atne/` |
| Backend | **PHP 8.2 + Slim 4** |
| BD | **MSSQL Server on-premises FJE** (NO Azure SQL) |
| Auth | **Microsoft Entra ID** via include PHP institucional |
| Runtime | **Azure Web App (App Service for Containers) — Linux + nginx + php-fpm** |
| CI/CD | GitHub Actions → Azure Container Registry → App Service |
| DNS | Institucional (p. ex. `atne.fje.edu`), configurat per FJE |
| Endpoints | **86** (vegeu [01_inventari_endpoints.md](01_inventari_endpoints.md)) |
| Taules BD | **9 actives** + prefix `atne_` (vegeu [02_mapping_postgres_mssql.md](02_mapping_postgres_mssql.md)) |
| Estimació | **12-18 sessions** (~2-4 setmanes) |
| Pilot | Tancat fins a fi de migració. Cutover net, sense dos stacks en paral·lel |

## 1. Arquitectura de destí

```
                         ┌──────────────────────────────────────┐
                         │  Client (navegador docent @fje.edu)   │
                         │  HTML + JS + CSS (còpia 1:1 ui/atne/) │
                         └───────────────┬──────────────────────┘
                                         │ HTTPS
                                         ▼
                 ┌─────────────────────────────────────────────┐
                 │  Azure Web App (App Service for Containers) │
                 │  Custom container: nginx + php-fpm 8.2       │
                 │  ┌────────────────────────────────────────┐ │
                 │  │ Slim 4 (public/index.php bootstrap)     │ │
                 │  │  ├── Middleware: EntraIdAuth (include)  │ │
                 │  │  ├── Middleware: AdminHmac              │ │
                 │  │  ├── Middleware: CORS + ErrorHandler    │ │
                 │  │  └── Routes (86)                        │ │
                 │  │                                         │ │
                 │  │  src/Domain/                            │ │
                 │  │   ├── CorpusReader                      │ │
                 │  │   ├── InstructionCatalog (~45KB port)   │ │
                 │  │   ├── InstructionFilter                 │ │
                 │  │   └── PromptBuilder                     │ │
                 │  │                                         │ │
                 │  │  src/Services/                          │ │
                 │  │   ├── LLMClient (OpenAI, Gemini, Gemma) │ │
                 │  │   ├── Orchestrator (pipeline adapt)     │ │
                 │  │   ├── PostProcess (LT, typos, LaTeX)    │ │
                 │  │   ├── IllustrationResolver              │ │
                 │  │   ├── Export (PDF/DOCX/TXT)             │ │
                 │  │   └── CostEstimator                     │ │
                 │  │                                         │ │
                 │  │  src/Repositories/ (PDO sqlsrv)         │ │
                 │  │   ├── HistoryRepo                       │ │
                 │  │   ├── DraftsRepo                        │ │
                 │  │   ├── AdaptationsRepo                   │ │
                 │  │   ├── DocentsRepo                       │ │
                 │  │   ├── ProfilesRepo                      │ │
                 │  │   ├── PilotEventsRepo                   │ │
                 │  │   └── SystemConfigRepo                  │ │
                 │  └────────────────────────────────────────┘ │
                 └──────────┬──────────────────┬───────────────┘
                            │                  │
               ┌────────────▼───────┐    ┌─────▼────────────────┐
               │  MSSQL FJE         │    │  APIs externes       │
               │  (Windows Server)  │    │  · OpenAI            │
               │  · atne_docents    │    │  · Google Gemini     │
               │  · atne_drafts     │    │  · Gemma (Gemini)    │
               │  · atne_adaptations│    │  · LanguageTool      │
               │  · atne_custom_prof│    │  · Wikimedia Commons │
               │  · atne_pilot_*    │    │  · Pexels            │
               │  · history         │    │  · FLUX (BFL)        │
               │  · system_config   │    │  · Entra ID (OIDC)   │
               │  · atne_prompt_deb │    └──────────────────────┘
               │  · atne_sessions   │
               └────────────────────┘
```

## 2. Stack decidit

### 2.1 Frontend (sense canvis)

- **Font**: `ui/atne/` (actual al repo ATNE-RAG-KG)
- **Cal fer**: còpia 1:1 a `public/` o `ui/` al repo FJE. Només ajustos:
  - `auth.js`: substituir el flux Supabase per el que expose l'Entra ID include (veure §5)
  - Si la base URL canvia (subdomini `*.azurewebsites.net` temporalment → `atne.fje.edu` després), assegurar paths relatius
- **Lliuraments**: pàgines `pas1.html`, `pas2.html`, `pas3.html`, `index.html`, `admin.html`, `admin-pilot.html`, `biblioteca.html`, etc.
- **Dependències client**: `html2pdf.js` (client-side PDF), `driver.js` (onboarding), cap altre framework

### 2.2 Backend PHP Slim 4

**composer.json** (nou, ampliat respecte l'MVP v1):

```json
{
  "name": "fje/atne",
  "require": {
    "php": "^8.2",
    "ext-pdo_sqlsrv": "*",
    "ext-sqlsrv": "*",
    "ext-mbstring": "*",
    "ext-json": "*",
    "ext-intl": "*",
    "slim/slim": "^4.12",
    "slim/psr7": "^1.6",
    "php-di/php-di": "^7.0",
    "vlucas/phpdotenv": "^5.6",
    "guzzlehttp/guzzle": "^7.8",
    "openai-php/client": "^0.10",
    "monolog/monolog": "^3.5",
    "symfony/http-client": "^7.0",
    "firebase/php-jwt": "^6.10",
    "smalot/pdfparser": "^2.9",
    "phpoffice/phpword": "^1.2",
    "tecnickcom/tcpdf": "^6.7",
    "kiwilan/php-ebook": "^2.0"
  },
  "autoload": {
    "psr-4": { "Atne\\": "src/" }
  }
}
```

**Estructura de directoris**:

```
FundacioJesuitesEducacio/ATNE/
├── public/
│   ├── index.php                # bootstrap Slim4
│   ├── ui/                      # còpia de ui/atne/
│   └── legacy_include_entra.php # include institucional FJE (vegeu §5)
├── src/
│   ├── Controllers/             # un per grup d'endpoints
│   ├── Middleware/
│   │   ├── EntraIdAuth.php
│   │   ├── AdminHmac.php
│   │   └── CorsErrorHandler.php
│   ├── Domain/
│   │   ├── CorpusReader.php
│   │   ├── InstructionCatalog.php
│   │   ├── InstructionFilter.php
│   │   └── PromptBuilder.php
│   ├── Services/
│   │   ├── LLMClient/
│   │   │   ├── OpenAIClient.php
│   │   │   ├── GeminiClient.php
│   │   │   └── GemmaClient.php
│   │   ├── Orchestrator.php
│   │   ├── PostProcess/
│   │   │   ├── LanguageToolClient.php
│   │   │   ├── TypoFixer.php
│   │   │   ├── LatexCleaner.php
│   │   │   └── PostProcess.php (façana)
│   │   ├── IllustrationResolver.php
│   │   ├── ExportService.php
│   │   └── CostEstimator.php
│   ├── Repositories/            # PDO sqlsrv per taula
│   └── Support/
├── corpus/                      # submodule corpusFJE
├── db/
│   ├── migrations/              # T-SQL per a MSSQL
│   └── seed/
├── docker/
│   ├── Dockerfile               # nginx + php-fpm 8.2
│   ├── nginx.conf
│   └── php-fpm.conf
├── tests/
├── .env.example
├── composer.json
└── README.md
```

### 2.3 Base de dades MSSQL

Veure document sencer a [02_mapping_postgres_mssql.md](02_mapping_postgres_mssql.md). Resum:

| Taula | Propòsit | Claus especials |
|---|---|---|
| `atne_docents` | Usuari docent autenticat | PK id (hash email), `is_admin BIT` |
| `atne_custom_profiles` | Perfils de suport creats pel docent | `docent_id`, `profile_data NVARCHAR(MAX) + CHECK ISJSON` |
| `atne_drafts` | Esborranys text original (Pas 2) | `docent_id`, `text NVARCHAR(MAX)` |
| `atne_adaptations` | Adaptacions finals amb HTML (Pas 3, biblioteca) | `adapted_html`, 3 JSONs de snapshot |
| `history` | Historial + analytics + instrumentació Sprint 1A/1B/1C | ~35 columnes, `cost_estimat_eur`, `prompt_version` |
| `atne_pilot_events` | Events UX granulars | `event_type`, `data JSON` |
| `atne_pilot_consent` | RGPD | `decision` ∈ {accepted, declined, revoked} |
| `system_config` | Config runtime (models per fase) | PK `key NVARCHAR(255)`, `value JSON` |
| `atne_prompt_debug` | Debugging audit (darrera adaptació) | `adapt_id UNIQUE`, `data JSON` |

**Collation**: `Latin1_General_100_CI_AI_SC_UTF8` (UTF-8 case/accent insensitive).

**Taules NO migrades** (dead code): `rag_fje`, `kg_nodes`, `kg_edges`.

### 2.4 Runtime — Azure Web App Linux + nginx

- **SKU**: P1v3 o superior (per tenir almenys 2 GB RAM per suportar 4 workers php-fpm + buffer LT).
- **Deployment**: App Service for Containers (Custom Container) via Azure Container Registry.
- **Dockerfile** (al repo): `FROM php:8.2-fpm-alpine` + instal·lar `pdo_sqlsrv`, `sqlsrv`, `mbstring`, `intl`, `opcache` + nginx + supervisord.
- **nginx.conf** clau per SSE:
  ```nginx
  location ~ \.php$ {
      fastcgi_pass 127.0.0.1:9000;
      fastcgi_buffering off;
      fastcgi_read_timeout 300s;
      proxy_buffering off;
      add_header X-Accel-Buffering no;
  }
  ```
- **CORS**: configurar origins acceptats (`atne.fje.edu`, `*.azurewebsites.net` per a dev).
- **Headers de seguretat**: CSP, X-Content-Type-Options, Strict-Transport-Security, Referrer-Policy.
- **Scale-out**: arrencar amb 1 instància, autoscale a 3 si es pugen docents ≥ 50 concurrents.

## 3. Pipeline de l'app (flux pas a pas, idèntic al Python)

Sense canvis funcionals — port 1:1. Es manté:

1. **Pas 1** (`pas1.html`): tria de perfil docent (persona o grup) amb curs + MECR + condicions
2. **Pas 2** (`pas2.html`): text original — enganxa / puja / genera (SSE stream preview)
3. **Pas 3** (`pas3.html`): adaptació — `/api/adapt` SSE amb `phase_update`, `chunk`, `image_found`, `refine_progress`, `audit_feedback`, `done`
4. **Exportació**: client-side `html2pdf.js` + servidor `/api/export` (DOCX/PDF/TXT amb complements)

Tot el flux passa per `/api/adapt`. Auth obligatori via Entra ID amb email `@fje.edu`.

## 4. Regles pedagògiques (sense canvis)

- **Lectura fàcil**, **DUA** (Accés/Core/Enriquiment), **memòria triàdica** (Alumne + Classe + Matèria), **107 instruccions del catàleg**, **22 gèneres discursius**, **complements** (glossari, definicions integrades, esquema visual, bastides, preguntes graduades, mapa conceptual, etc.).
- **Font de veritat** del corpus: submodule `corpusFJE` (93 fitxers MD). A F3 s'integra via `git submodule`.
- **Instrucció catàleg** (`instruction_catalog.py` → `InstructionCatalog.php`): 45KB de text literal + metadades de filtre (SEMPRE/NIVELL/PERFIL/COMPLEMENT). Port mecànic amb array PHP.

## 5. Autenticació — Entra ID via include PHP

**Decisió Miquel 2026-04-23**: FJE disposa d'un fitxer PHP institucional (p. ex. `legacy_include_entra.php`) que es fa `require` al bootstrap Slim4 i valida el token Entra ID. Aquest fitxer el proveirà l'equip d'infra FJE.

**Integració proposada**:

```php
// public/index.php
require __DIR__ . '/legacy_include_entra.php'; // FJE-provided
// després del require, $entra_user conté email, groups, etc.

$app = \Slim\Factory\AppFactory::create();
$app->add(\Atne\Middleware\EntraIdAuth::class);  // propaga $entra_user al request
$app->add(\Atne\Middleware\AdminHmac::class);
```

**Middleware `EntraIdAuth`**:
- Llegeix `$entra_user` que l'include FJE ha inflat.
- Valida domini `@fje.edu`.
- Injecta `docent_email`, `docent_id` (hash email), `docent_alias` a l'atribut del request PSR-7.
- Rutes públiques (§1 de [01_inventari_endpoints.md](01_inventari_endpoints.md)) salten aquesta validació.

**Migració de dades**: els docents existents a Supabase `atne_docents` es migren per email (la `id` = hash de l'email manté la mateixa fórmula).

**Pendent**: obtenir de FJE el skeleton exacte del include (claims retornats, format de l'objecte, errors, mode logout).

## 6. Integracions externes

| Servei | Mode | Notes |
|---|---|---|
| OpenAI (GPT-4o, 4.1-mini, 4o-mini) | `openai-php/client` | Variables: `OPENAI_API_KEY` |
| Gemini 2.5-flash | REST directe amb `symfony/http-client` | `GEMINI_API_KEY`. Mantenir `thinking_budget=0` ([memòria](../../../.claude/projects/c--Users-miquel-amor-Documents-GitHub-ATNE/memory/project_gemini_thinking_cost.md)). |
| Gemma 3 27B / Gemma 4 31B | REST via Gemini API | `GEMMA4_API_KEY`, `GEMMA_API_KEY`. Sense `system_instruction` separat ([memòria](../../../.claude/projects/c--Users-miquel-amor-Documents-GitHub-ATNE/memory/project_gemma_system_instruction_empiric.md)). |
| LanguageTool | REST Guzzle | Públic o self-hosted |
| Wikimedia Commons | REST Guzzle | Sense clau |
| Pexels | REST Guzzle | `PEXELS_API_KEY` |
| FLUX (BFL) | REST Guzzle | `BFL_API_KEY` (opcional) |

**Claus al `.env`** (no al repo). Al runtime Azure: usar App Service > Configuration > Application Settings.

## 7. Post-procés català

Pipeline actual a `server.py:_languagetool_correct` + `post_process_catalan`:
1. Neteja LaTeX (`\text{}`, `\frac{}{}`, etc.)
2. Typo fixes (_TYPO_FIXES dict, 16+ entrades)
3. Eliminació d'interrogants/admiracions castellans (`¿¡`)
4. LanguageTool (configurable: CASING/UPPERCASE només warning, no auto-apply)
5. Concatenació + validació final

Port a `src/Services/PostProcess/` amb 4 classes i una façana. **I18n**: el post-procés actual és CAT-only ([memòria](../../../.claude/projects/c--Users-miquel-amor-Documents-GitHub-ATNE/memory/project_i18n_postprocess.md)) — a F3 deixar refactor ja pensat per a CAST/FR/ES/EN futurs (fitxers per idioma a `src/Services/PostProcess/lang/`).

## 8. Instrumentació pilot (sense canvis funcionals)

Port mecànic:
- `POST /api/pilot/event`: rep events UX, desa a `atne_pilot_events`.
- `POST /api/pilot/consent`: RGPD, desa a `atne_pilot_consent`.
- Camp `history.prompt_version` (Sprint 1C) per comparar A/B de prompts post-pilot.
- Dashboard `/admin/pilot` es copia 1:1 del HTML actual.

## 9. Fases d'execució

Les 7 fases (detall a memòria [project_migracio_stack_decisions](../../../.claude/projects/c--Users-miquel-amor-Documents-GitHub-ATNE/memory/project_migracio_stack_decisions.md)):

| Fase | Entregable | Sessions | Depèn de |
|---|---|---|---|
| F0 | Spec v3 + mapping BD + inventari endpoints | 1 (gairebé feta) | — |
| F1 | Scaffolding PHP Slim4 + Dockerfile + ACR + primer deploy | 2 | accés Azure, accés MSSQL |
| F2 | BD MSSQL + repositories PDO + migracions T-SQL | 2 | F1 |
| F3 | Port domini (CorpusReader, InstructionCatalog, PromptBuilder, PostProcess, LLMClient, Orchestrator) | 3-4 | F1 |
| F4 | Port endpoints (86, començant pels 8 crítics) | 3-4 | F2+F3 |
| F5 | Frontend (còpia + ajust auth.js) | 1 | F4 |
| F6 | Auth Entra ID (include) + claus externes | 1 | skeleton include FJE |
| F7 | Paritat funcional E2E + cutover | 1-2 | totes |
| **Total** | | **14-16** | |

## 10. Criteris de go/no-go per a reobrir el pilot

1. ✅ 8 endpoints crítics funcionant (amb SSE validat via nginx al runtime real Azure)
2. ✅ 10 perfils E2E validats (TDAH, dislèxia, nouvingut A1, nouvingut A2, TEA, AC, doble excepcionalitat, grup multinivell ACC/STD/EXIG, grup sense etiquetes)
3. ✅ Paritat output a ≥95% (diff textual ajustat per diferències acceptables) entre Python prod i PHP FJE
4. ✅ Auth Entra ID operatiu amb almenys 5 comptes `@fje.edu` de prova
5. ✅ Instrumentació pilot (event + consent) escrivint correctament a MSSQL
6. ✅ Exportació PDF/DOCX/TXT funcionant amb complements
7. ✅ Llatència de `/api/adapt` ≤ 1.5× la del Python (acceptable: nginx+fpm és més lleuger que uvicorn però tenim PDO sqlsrv més costós que PostgREST)
8. ✅ Cost estimat validat: `_estimate_cost_eur` retorna mateixos valors per a un mateix conjunt `models_per_phase`

## 11. Punts oberts / pendents

- **Entra ID include skeleton**: pendent obtenir de FJE. Bloqueja F6.
- **MSSQL connectivity**: des d'Azure Web App Linux cap a MSSQL Windows on-prem — decidir VPN / private endpoint / IP pública + firewall. Bloqueja F2 testing real.
- **ACR existent**: reutilitzar o crear. Bloqueja F1 CI/CD.
- **Admin**: decidir si l'admin (HMAC cookie) es manté o també passa per Entra ID + claim de grup.
- **Eval dashboard**: decidir si es migra o es deixa al Python congelat (ús intern només).
- **`/api/export` PDF**: la versió Python usa `fpdf2` + `tcpdf` + client-side `html2pdf.js`. Decidir si a PHP mantenim client-side (recomanable) + només endpoint `/api/export` per DOCX/TXT.

---

**Document**: Especificació migració ATNE → FJE v3.0
**Data**: 2026-04-23
**Versió**: 3.0
**Replaça**: SPEC_MVP_AZURE.md v2.1 (2026-03-24)
