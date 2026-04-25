# Inventari d'endpoints ATNE (FastAPI → Slim4)

**Data**: 2026-04-23
**Font**: `server.py` (77 rutes) + `routes/drafts.py` (5) + `routes/adaptations.py` (4)
**Total**: **86 endpoints**
**Destí de migració**: `FundacioJesuitesEducacio/ATNE` (PHP Slim4 + MSSQL + Azure Web App Linux/nginx)

## Convencions d'autenticació

| Flag | Descripció | Mecanisme origen | Mecanisme destí (Slim4) |
|---|---|---|---|
| `public` | Sense auth | — | — |
| `docent` | Usuari docent FJE autenticat | JWT Supabase validat via `/auth/v1/user` (middleware `_AtneAuthMiddleware`) | **Entra ID** via include PHP institucional |
| `admin` | Admin del sistema | Cookie HMAC-SHA256 pròpia, 8h TTL (`_require_admin`) | Middleware PSR-15 PHP equivalent |

Rutes públiques actuals (sense auth): `/api/health`, `/api/runtime-config`, tot `/api/admin/*`, `/favicon.ico`, `/`, `/ui/*`, `/legacy`, i totes les pàgines HTML (`/admin`, `/cuina`, etc.). Vegeu `_atne_is_public_path()` a [server.py:364](../../server.py#L364).

## Taula resum

| Categoria | Comptador | SSE | Auth docent | Auth admin | Crítics pilot |
|---|---:|---:|---:|---:|---:|
| Static/HTML | 16 | 0 | 0 | 0¹ | 0 |
| Health + runtime | 2 | 0 | 0 | 0 | 1 |
| Admin auth/config | 5 | 0 | 0 | 4 | 0 |
| Admin analytics + wipe | 3 | 0 | 0 | 3 | 0 |
| Audit (last, list, detail, map) | 4 | 0 | 0 | 4 | 0 |
| Pilot instrumentation | 4 | 0 | 0 | 1 | 1 |
| Profiles (legacy) | 4 | 0 | 0 | 0 | 0 |
| History (list/save/beacon/patch) | 4 | 0 | 0 | 0 | 1 |
| Docent (login + profiles CRUD) | 6 | 0 | 3 | 1 | 1 |
| Adaptation pipeline | 7 | 2 | 5 | 0 | 2 |
| Illustrations | 2 | 0 | 2 | 0 | 0 |
| Export | 1 | 0 | 1 | 0 | 1 |
| Drafts (routes/) | 5 | 0 | 5 | 0 | 1 |
| Adaptations (routes/) | 4 | 0 | 4 | 0 | 1 |
| Corpus + catalog + preview | 5 | 0 | 0 | 0 | 0 |
| Validacio | 3 | 0 | 0 | 0 | 0 |
| Eval dashboard + APIs | 11 | 0 | 0 | 0 | 0 |
| **TOTAL** | **86** | **2** | **20** | **13** | **8** |

¹ Les rutes HTML d'admin (`/admin`, `/admin/pilot`) serveixen el HTML però fan la comprovació d'admin client-side. Considerar enforcament server-side a la migració.

---

## 1. Static / HTML routes

| # | Mètode + path | Línia | Handler | Auth | Notes |
|---|---|---|---|---|---|
| 1 | `GET /favicon.ico` | [557](../../server.py#L557) | `favicon` | public | FileResponse |
| 2 | `GET /` | [563](../../server.py#L563) | `index` | public | HTML principal (ui/atne/index.html) |
| 3 | `GET /legacy` | [571](../../server.py#L571) | `index_legacy` | public | HTML legacy (ui/index.html) |
| 4 | `GET /ui/{path:path}` | [580](../../server.py#L580) | `serve_static` | public | Serveix ui/ amb MIME correcte |
| 5 | `GET /admin` | [3911](../../server.py#L3911) | `admin_page` | public¹ | HTML admin |
| 6 | `GET /admin/pilot` | [3925](../../server.py#L3925) | `admin_pilot_page` | public¹ | HTML dashboard pilot |
| 7 | `GET /cuina` | [3941](../../server.py#L3941) | `cuina_page` | public | HTML flux prompt |
| 8 | `GET /pipeline` | [3953](../../server.py#L3953) | `pipeline_page` | public | HTML arquitectura |
| 9 | `GET /saber-ne` | [3965](../../server.py#L3965) | `saber_ne_page` | public | HTML ajuda |
| 10 | `GET /avaluacio` | [3977](../../server.py#L3977) | `avaluacio_page` | public | HTML avaluació |
| 11 | `GET /demo` | [3989](../../server.py#L3989) | `demo_v7_page` | public | HTML demo V7 Stitch |
| 12 | `GET /dashboard` | [4001](../../server.py#L4001) | `dashboard_xat9_page` | public | HTML dashboard xat9 |
| 13 | `GET /dashboard_complements` | [4013](../../server.py#L4013) | `dashboard_complements_page` | public | |
| 14 | `GET /dashboard_questions` | [4024](../../server.py#L4024) | `dashboard_questions_page` | public | |
| 15 | `GET /informe_fje` | [4035](../../server.py#L4035) | `informe_fje_md` | public | Serveix MD |
| 16 | `GET /informe_tecnic` | [4048](../../server.py#L4048) | `informe_tecnic_md` | public | Serveix MD |

**Migració**: a Slim4, rutes HTML amb `Slim\Views\PhpRenderer` o serve static + template engine si cal. Les 4 pàgines de l'eval dashboard (`/eval`, `/eval/progress`, `/eval/results`, `/eval/cases`) es comptabilitzen a secció 17.

## 2. Health + runtime config

| # | Mètode + path | Línia | Handler | Resposta | Auth | BD |
|---|---|---|---|---|---|---|
| 17 | `GET /api/health` | [843](../../server.py#L843) | `health` | JSON | public | — |
| 18 | `GET /api/runtime-config` | [998](../../server.py#L998) | `runtime_config` | JSON | public | `system_config` (R) |

- **#17 crític**: probe per al `az webapp` health check.
- **#18** retorna model aliases + prompt_version perquè el frontend sàpiga quin model fa servir.

## 3. Admin (auth + config)

| # | Mètode + path | Línia | Handler | Body | Auth | BD |
|---|---|---|---|---|---|---|
| 19 | `POST /api/admin/login` | [958](../../server.py#L958) | `admin_login` | `{password}` | public | — |
| 20 | `POST /api/admin/logout` | [980](../../server.py#L980) | `admin_logout` | — | public | — |
| 21 | `GET /api/admin/whoami` | [987](../../server.py#L987) | `admin_whoami` | — | public (retorna is_admin bool) | — |
| 22 | `GET /api/admin/config` | [1014](../../server.py#L1014) | `admin_get_config` | — | **admin** | `system_config` (R) |
| 23 | `PUT /api/admin/config` | [1028](../../server.py#L1028) | `admin_put_config` | model config JSON | **admin** | `system_config` (W) |

**Patró HMAC cookie** ([server.py:294-361](../../server.py#L294)) — a PHP, equivalent amb `hash_hmac('sha256', ...)` + `Set-Cookie` `HttpOnly` `Secure` `SameSite=Strict`. A la versió FJE considerar si aquest admin ha d'anar també via Entra ID (amb claim de grup) o manté login separat.

## 4. Admin analytics + wipe

| # | Mètode + path | Línia | Handler | Auth | BD |
|---|---|---|---|---|---|
| 24 | `DELETE /api/admin/history` | [1168](../../server.py#L1168) | `admin_wipe_history` | admin | `history` (D) |
| 25 | `GET /api/admin/analytics` | [1237](../../server.py#L1237) | `admin_analytics` | admin | `history` (R) + aggregations |
| 26 | `GET /api/admin/pilot-metrics` | [1457](../../server.py#L1457) | `admin_pilot_metrics` | admin | `atne_pilot_events`, `history` (R) |

## 5. Audit

| # | Mètode + path | Línia | Handler | Auth | BD |
|---|---|---|---|---|---|
| 27 | `GET /api/audit/last-adaptation` | [1669](../../server.py#L1669) | `audit_last_adaptation` | admin | in-memory buffer |
| 28 | `GET /api/audit/adaptations` | [1736](../../server.py#L1736) | `audit_adaptations_list` | admin | `atne_prompt_debug` (R) |
| 29 | `GET /api/audit/adaptations/{adapt_id}` | [1767](../../server.py#L1767) | `audit_adaptation_detail` | admin | `atne_prompt_debug` (R) |
| 30 | `POST /api/audit/instruction-map` | [1779](../../server.py#L1779) | `audit_instruction_map` | admin | — (calcula catàleg) |

**#27 important**: usa un buffer en memòria de la darrera adaptació. A PHP amb múltiples workers FPM no té sentit — substituir per taula amb TTL o `atne_prompt_debug` amb `ORDER BY ts_ms DESC LIMIT 1`.

## 6. Pilot instrumentation

| # | Mètode + path | Línia | Handler | Auth | BD |
|---|---|---|---|---|---|
| 31 | `POST /api/pilot/event` | [1345](../../server.py#L1345) | `pilot_event` | docent (per `data.docent_id`) | `atne_pilot_events` (W) |
| 32 | `POST /api/pilot/consent` | [1387](../../server.py#L1387) | `pilot_consent` | docent | `atne_pilot_consent` (W) |
| 33 | `GET /api/pilot/consent/{docent_id}` | [1435](../../server.py#L1435) | `pilot_consent_status` | docent | `atne_pilot_consent` (R) |
| (ja comptat a #26) | `GET /api/admin/pilot-metrics` | 1457 | | admin | |

**#31 crític**: és el canal únic d'instrumentació de l'experiència docent al pilot. Cal garantir que sempre respon ràpid (no bloquejar UI). Considerar batch endpoint + `navigator.sendBeacon()` al frontend.

## 7. Profiles (legacy, in-memory)

| # | Mètode + path | Línia | Handler | Auth | Storage |
|---|---|---|---|---|---|
| 34 | `GET /api/profiles` | [1225](../../server.py#L1225) | `list_profiles` | public | `profiles/*.json` (FS) |
| 35 | `POST /api/profiles` | [1875](../../server.py#L1875) | `save_profile` | public | FS |
| 36 | `GET /api/profiles/{nom}` | [1887](../../server.py#L1887) | `load_profile` | public | FS |
| 37 | `DELETE /api/profiles/{nom}` | [1895](../../server.py#L1895) | `delete_profile` | public | FS |

**Nota**: són perfils globals JSON al disc (no per docent). Els perfils per docent viuen al grup 9 (docent/profiles). Decidir a la migració si aquest grup es manté o es deprecia.

## 8. History

| # | Mètode + path | Línia | Handler | Auth | BD |
|---|---|---|---|---|---|
| 38 | `GET /api/history` | [1905](../../server.py#L1905) | `list_history` | public² | `history` (R, filtrat per docent_hash) |
| 39 | `POST /api/history` | [1990](../../server.py#L1990) | `save_history` | public² | `history` (I) |
| 40 | `POST /api/history/{history_id}/beacon` | [2057](../../server.py#L2057) | `history_beacon` | public² | `history` (U) |
| 41 | `PATCH /api/history/{history_id}` | [2085](../../server.py#L2085) | `update_history_feedback` | public² | `history` (U) |

² Actualment no auth docent a middleware, però filtra per `_get_current_docent_hash()`. A FJE: protegir amb auth docent efectiva.

**#40 crític**: endpoint de `navigator.sendBeacon()` per mesurar temps al pas 4 quan l'usuari tanca la pestanya. Ha de ser ultraràpid (≤50ms).

## 9. Docent (auth + profiles CRUD)

| # | Mètode + path | Línia | Handler | Auth | BD |
|---|---|---|---|---|---|
| 42 | `POST /api/docent/login` | [4729](../../server.py#L4729) | `docent_login` | docent | `atne_docents` (upsert) |
| 43 | `GET /api/docent/profiles` | [4762](../../server.py#L4762) | `get_docent_profiles` | docent | `atne_custom_profiles` (R) |
| 44 | `POST /api/docent/profiles` | [4780](../../server.py#L4780) | `save_docent_profile` | docent | `atne_custom_profiles` (I/U) |
| 45 | `PATCH /api/docent/profiles/{profile_id}` | [4807](../../server.py#L4807) | `update_docent_profile` | docent | `atne_custom_profiles` (U) |
| 46 | `DELETE /api/docent/profiles/{profile_id}` | [4824](../../server.py#L4824) | `delete_docent_profile` | docent | `atne_custom_profiles` (D) |
| 47 | `GET /api/docent/is-admin` | [4838](../../server.py#L4838) | `check_is_admin` | docent | `atne_docents` (R) |
| 48 | `POST /api/docent/set-admin` | [4853](../../server.py#L4853) | `set_admin` | admin | `atne_docents` (U) |

**#42 crític**: és el punt d'entrada autenticat del pilot. A FJE: passar a Entra ID + upsert a `atne_docents` amb claim `email`. L'`id` del docent es deriva de l'email via hash — mantenir o canviar a UUID?

## 10. Adaptation pipeline

| # | Mètode + path | Línia | Handler | Resposta | Auth | LLM | Body clau |
|---|---|---|---|---|---|---|---|
| 49 | `POST /api/propose` | [2120](../../server.py#L2120) | `propose` | JSON | docent | — (regles) | `characteristics`, `context` |
| 50 | `POST /api/extract-text` | [2132](../../server.py#L2132) | `extract_text_from_file` | JSON | docent | — | multipart `file` (PDF/DOCX/TXT/MD/EPUB, 50MB) |
| 51 | `POST /api/generate-text` | [2308](../../server.py#L2308) | `generate_text` | JSON | docent | Gemma 3 27B | `tema`, `mecr`, `etapa`, `paraules_objectiu` |
| 52 | `POST /api/generate-text-stream` | [2352](../../server.py#L2352) | `generate_text_stream` | **SSE** | docent | Gemma 3 27B | idem |
| 53 | `POST /api/refine-text` | [3241](../../server.py#L3241) | `refine_text` | JSON | docent | Gemma 3 27B | `text`, `instruction`, `context` |
| 54 | `POST /api/adapt` | [3380](../../server.py#L3380) | `adapt_stream` | **SSE** | docent | rotate (Gemma3/Gemma4/GPT-4o/GPT-4.1-mini) | text + profile + dua + genre + complements |
| 55 | `POST /api/export` | [3527](../../server.py#L3527) | `export_doc` | FileResponse PDF/DOCX/TXT | docent | — | HTML adaptat + options |

**#54 el més crític**: pipeline principal. SSE events: `phase_update`, `chunk`, `image_found`, `refine_progress`, `audit_feedback`, `done`. Timeout 120s+. Al runtime nginx+php-fpm:
- `proxy_buffering off`
- `fastcgi_buffering off`
- `fastcgi_read_timeout 180s`
- `add_header X-Accel-Buffering no;`
- Al PHP: `ini_set('output_buffering', '0')`, `@ob_end_flush()`, `flush()` després de cada event.

**#52 també SSE**: generació de text nou (pas 2 de l'app).

**#50** usa `pypdf`, `python-docx`, `python-multipart`. En PHP: `smalot/pdfparser` per PDF, `phpoffice/phpword` per DOCX, natiu per TXT/MD, `smichaelsen/php-epub-reader` o `kiwilan/php-ebook` per EPUB.

## 11. Illustrations

| # | Mètode + path | Línia | Handler | Auth | Externs |
|---|---|---|---|---|---|
| 56 | `POST /api/illustration` | [3468](../../server.py#L3468) | `resolve_illustration` | docent | Wikimedia, Pexels, Gemma 3 (query), FLUX (opt) |
| 57 | `POST /api/illustrations/batch` | [3496](../../server.py#L3496) | `resolve_illustrations_batch` | docent | idem |

## 12. Drafts (routes/drafts.py)

| # | Mètode + path | Línia | Handler | Auth | BD |
|---|---|---|---|---|---|
| 58 | `POST /api/drafts` | [39](../../routes/drafts.py#L39) | `save_draft` | docent | `atne_drafts` (I/U) |
| 59 | `GET /api/drafts` | [108](../../routes/drafts.py#L108) | `list_drafts` | docent | `atne_drafts` (R) |
| 60 | `GET /api/drafts/{draft_id}` | [155](../../routes/drafts.py#L155) | `get_draft` | docent | `atne_drafts` (R) |
| 61 | `DELETE /api/drafts/{draft_id}` | [187](../../routes/drafts.py#L187) | `delete_draft` | docent | `atne_drafts` (D) |
| 62 | `PATCH /api/drafts/{draft_id}` | [209](../../routes/drafts.py#L209) | `patch_draft` | docent | `atne_drafts` (U) |

## 13. Adaptations (routes/adaptations.py)

| # | Mètode + path | Línia | Handler | Auth | BD |
|---|---|---|---|---|---|
| 63 | `POST /api/adaptations` | [37](../../routes/adaptations.py#L37) | `save_adaptation` | docent | `atne_adaptations` (I/U) |
| 64 | `GET /api/adaptations` | [110](../../routes/adaptations.py#L110) | `list_adaptations` | docent | `atne_adaptations` (R) |
| 65 | `GET /api/adaptations/{adaptation_id}` | [162](../../routes/adaptations.py#L162) | `get_adaptation` | docent | `atne_adaptations` (R) |
| 66 | `DELETE /api/adaptations/{adaptation_id}` | [189](../../routes/adaptations.py#L189) | `delete_adaptation` | docent | `atne_adaptations` (D) |

## 14. Corpus + catalog + prompt preview

| # | Mètode + path | Línia | Handler | Auth | Font |
|---|---|---|---|---|---|
| 67 | `GET /api/catalog` | [4125](../../server.py#L4125) | `api_catalog` | public | `instruction_catalog.py` |
| 68 | `GET /api/corpus` | [4175](../../server.py#L4175) | `api_corpus_list` | public | `corpus/*.md` |
| 69 | `GET /api/corpus/{filename}` | [4198](../../server.py#L4198) | `api_corpus_file` | public | `corpus/*.md` |
| 70 | `POST /api/prompt-preview` | [4228](../../server.py#L4228) | `api_prompt_preview` | public | genera prompt de previsualització |
| 71 | `GET /api/stats-instruccions` | [4288](../../server.py#L4288) | `api_stats_instruccions` | public | catàleg |

## 15. Validacio

| # | Mètode + path | Línia | Handler | Auth | Font |
|---|---|---|---|---|---|
| 72 | `GET /validacio` | [4061](../../server.py#L4061) | `validacio_page` | public | HTML |
| 73 | `GET /validacio_data.json` | [4071](../../server.py#L4071) | `validacio_data` | public | JSON fix |
| 74 | `GET /api/validacio/{tanda}` | [4080](../../server.py#L4080) | `api_validacio_tanda` | public | dades per tanda |

## 16. Eval dashboard pages

| # | Mètode + path | Línia | Handler | Auth | Notes |
|---|---|---|---|---|---|
| 75 | `GET /eval` | [4300](../../server.py#L4300) | `eval_dashboard` | public | HTML |
| 76 | `GET /eval/progress` | [4309](../../server.py#L4309) | `eval_progress_page` | public | HTML |
| 77 | `GET /eval/results` | [4318](../../server.py#L4318) | `eval_results_page` | public | HTML |
| 78 | `GET /eval/cases` | [4327](../../server.py#L4327) | `eval_cases_page` | public | HTML |

## 17. Eval APIs

| # | Mètode + path | Línia | Handler | Auth | Font |
|---|---|---|---|---|---|
| 79 | `GET /api/eval/cases/{run_id}` | [4336](../../server.py#L4336) | `eval_cases_detail` | public | SQLite eval_db |
| 80 | `GET /api/eval/originals` | [4422](../../server.py#L4422) | `eval_originals` | public | eval_db |
| 81 | `GET /api/eval/comparative` | [4432](../../server.py#L4432) | `eval_comparative` | public | eval_db |
| 82 | `GET /api/eval/runs` | [4495](../../server.py#L4495) | `eval_runs` | public | eval_db |
| 83 | `GET /api/eval/run/{run_id}` | [4508](../../server.py#L4508) | `eval_run_detail` | public | eval_db |
| 84 | `GET /api/eval/progress` | [4521](../../server.py#L4521) | `eval_progress` | public | eval_db |
| 85 | `GET /api/eval/v2debug` | [4687](../../server.py#L4687) | `eval_v2debug` | public | eval_db |

**Nota sobre eval/*****: són pàgines i APIs per al dashboard d'avaluació intern (cuina). No són crítiques per al pilot docent. Migrar en última fase, o mantenir el Python en paral·lel només per a ús intern (decisió pendent).

---

## Endpoints crítics per al pilot (8)

Els 8 que cal garantir amb **paritat 100%** abans de reobrir el pilot:

1. **POST `/api/adapt`** (SSE) — pipeline d'adaptació, cor funcional
2. **POST `/api/generate-text-stream`** (SSE) — generació de text
3. **POST `/api/refine-text`** — refinament de l'output
4. **POST `/api/export`** — exportació PDF/DOCX/TXT (amb complements)
5. **POST `/api/docent/login`** — punt d'entrada autenticat
6. **POST `/api/drafts`** (+ GET + PATCH) — persistència del pas 2
7. **POST `/api/adaptations`** (+ GET + PATCH) — biblioteca de l'adaptació
8. **POST `/api/pilot/event`** — instrumentació UX (perd-ho → cec al pilot)

## Dependències externes (HTTP/SDK)

Cal reimplementar o mantenir:

| Servei | Origen | Proposta PHP |
|---|---|---|
| OpenAI (GPT-4o, GPT-4.1-mini) | `openai-python` SDK | `openai-php/client` |
| Google Gemini | `google-genai` SDK | REST directe amb Guzzle/Symfony HTTP |
| Google Gemma (3-27b-it, 4-31b-it) | `google-genai` SDK | REST directe amb Guzzle/Symfony HTTP |
| LanguageTool | `requests` POST | Guzzle POST |
| Supabase REST | `requests` | **ELIMINAT** (substituït per PDO MSSQL) |
| Supabase Auth | `requests` | **ELIMINAT** (substituït per Entra ID include) |
| Wikimedia Commons | `requests` | Guzzle |
| Pexels | `requests` | Guzzle |
| FLUX (Black Forest Labs) | `requests` | Guzzle |

## Patrons a preservar

1. **SSE streaming**: 2 endpoints (`/api/adapt`, `/api/generate-text-stream`). Cal nginx correctament configurat (vegeu #54).
2. **Rotate LLM per fase**: mode `fixed` o `rotate` per cada fase (generate/adapt/complements/refine/auditor), config llegida de `system_config`. Vegeu `_model_for()` a [server.py:111](../../server.py#L111).
3. **Estimació de cost EUR**: `_estimate_cost_eur()` a [server.py:171](../../server.py#L171) — cal port a PHP per mantenir la taula `history.cost_estimat_eur`.
4. **Post-procés català**: `post_process_catalan()` a [server.py:3146](../../server.py#L3146) — orquestra LT + typos + LaTeX + english + concat. És complex; Port a `PostProcess.php` a F3.
5. **Audit buffer en memòria**: incompatible amb múltiples workers PHP-FPM. Substituir per `atne_prompt_debug` amb `ORDER BY ts_ms DESC LIMIT 1`.
6. **Docent hash**: `_docent_hash_from_id()` a [server.py:823](../../server.py#L823) — usa SHA-256 d'email per anonimitzar a la BD. Port directe a PHP (`hash('sha256', ...)`).

---

**Document**: Inventari d'endpoints ATNE per a migració PHP Slim4
**Data**: 2026-04-23
**Versió**: 1.0
**Font**: grep de `@app.(get|post|put|delete|patch)` a `server.py` + `routes/*.py`
