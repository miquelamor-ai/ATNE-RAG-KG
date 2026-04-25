# ATNE - Esquema Real de Taules

**Versio**: 1.0  
**Data**: 2026-04-23

## Reconstruccio completada

### Taules investigades: 10/10

1. atne_docents - Usuaris docents autenticats
2. atne_custom_profiles - Perfils personalitzats per docent
3. atne_drafts - Esborranys Pas 2 (text original)
4. atne_adaptations - Adaptacions Pas 3 (HTML final + biblioteca)
5. history - Historial + analytics (~35 camps, ~6 sprints)
6. atne_pilot_events - Events UX granulars
7. atne_pilot_consent - Consentiment RGPD/AI Act
8. system_config - Configuracio runtime (models, budgets)
9. atne_prompt_debug - Debug de prompts
10. atne_sessions - Telemetria de sessions

## Font de la reconstruccio

### Codis Python fonts

- **server.py** (principal)
  - atne_docents: INSERT (4754), SELECT (4744), UPDATE (4863)
  - atne_custom_profiles: INSERT (4799), SELECT (4769), UPDATE (4818)
  - history: INSERT (2044), SELECT (1924), UPDATE (2075), DELETE (1206)
  - atne_pilot_events: INSERT (813)
  - atne_pilot_consent: INSERT (1423), SELECT (1443)
  - system_config: INSERT (1149), SELECT (221)
  - atne_prompt_debug: INSERT (1683)

- **routes/drafts.py** (completament documentat)
  - atne_drafts: INSERT (60), SELECT (126), UPDATE (71), DELETE (196)

- **routes/adaptations.py** (completament documentat)
  - atne_adaptations: INSERT (60), SELECT (128), UPDATE (75), DELETE (197)

- **adaptation/orchestrator.py** (telemetria)
  - atne_sessions: INSERT (365)

### Migracions SQL

- migrations/2026-04-19_drafts.sql - atne_drafts CREATE TABLE
- migrations/2026-04-22_adaptations.sql - atne_adaptations CREATE TABLE
- migrations/2026-04-21_prompt_debug.sql - atne_prompt_debug CREATE TABLE
- docs/sql/sprint1a_alter_history.sql - history ALTER (16 columnes)
- docs/sql/sprint1b_admin_config.sql - history ALTER (5 columnes) + system_config CREATE
- docs/sql/sprint1c_pilot_events.sql - atne_pilot_events, atne_pilot_consent CREATE + ALTER history/sessions
- docs/sql/sprint_b_source_column.sql - history ALTER (1 columna)

## Resum de camps per taula

### atne_docents (5 camps)
id (PK), email (UNIQUE), alias, is_admin, created_at

### atne_custom_profiles (4 camps)
id (PK), docent_id, profile_data (JSON), created_at

### atne_drafts (9 camps)
id (PK), docent_id, profile_id, title, text, materia, nivell, created_at, updated_at

### atne_adaptations (11 camps)
id (PK), docent_id, title, original_text, adapted_html, profile_snapshot, context_snapshot, complements_snapshot, multinivell_versions, created_at, updated_at

### history (~35 camps)
Legacy (10): id, profile_name, profile_json, context_json, params_json, original_text, adapted_text, rating, comment, created_at, updated_at
Sprint 1A (8): model_used, endpoint, duration_ms, refine_count, edit_manual, exported, etapa, curs, perfil_kind, via, n_words_in, n_words_out, docent_hash, quality_summary, auditor_used, fb_used_in_class, fb_needs_redo, fb_level_ok
Sprint 1B (5): models_per_phase, cost_estimat_eur, copied, time_on_step4_ms, review_items
Sprint B (1): source
Sprint 1C (2): prompt_version, rated_at
TOTAL: ~35 camps

### atne_pilot_events (10 camps)
id (PK), ts, docent_id, docent_hash, session_id, history_id, event_type, step, data (JSON), prompt_version

### atne_pilot_consent (9 camps)
id (PK), ts, docent_id, docent_hash, decision, dpia_version, consent_text_version, user_agent, ip_hash

### system_config (4 camps)
key (PK), value (JSON), updated_at, updated_by

### atne_prompt_debug (7 camps)
id (PK), adapt_id (UNIQUE), ts_ms, docent_id, model, data (JSON), created_at

### atne_sessions (16 camps)
id (PK), profile_type, conditions (JSON), etapa, mecr_entrada, mecr_sortida, model, instruction_ids (JSON), n_instructions, latency_ms, input_chars, output_chars, verify_score, docent_id, prompt_version, cost_estimat_eur, created_at

## Tipus de dades MSSQL

### Regles generals
- TEXT -> NVARCHAR(MAX)
- TIMESTAMPTZ -> DATETIMEOFFSET(3)
- BOOLEAN -> BIT
- SERIAL/BIGSERIAL -> BIGINT IDENTITY(1,1)
- JSONB -> NVARCHAR(MAX) + CHECK(ISJSON(...))
- NOW() -> SYSUTCDATETIME()

### Collation
Latin1_General_100_CI_AI_SC_UTF8 (UTF-8 case insensitive, accent insensitive)

## Conclusio

Esquema complet reconstruït a partir del codi Python + migracions SQL.
Cap columna inventada - totes proven de:
- INSERT/UPDATE/SELECT al codi Python
- Declaracions CREATE/ALTER TABLE al SQL

Llest per a F2 (CREATE TABLE T-SQL MSSQL).

---
Document creat: 2026-04-23
Versio: 1.0

