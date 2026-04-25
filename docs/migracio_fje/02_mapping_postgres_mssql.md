# Mapping PostgreSQL (Supabase) → Microsoft SQL Server

## Resum Executiu

- **Total taules actives: 9**
- **Taules amb JSONB/JSON**: 6
- **Taules amb IDENTITY**: 6

## Incompatibilitats principals

| PostgreSQL | MSSQL | Solució |
|-----------|-------|---------|
| JSONB | NVARCHAR(MAX) + CHECK ISJSON | Validació a taula |
| SERIAL/BIGSERIAL | INT/BIGINT IDENTITY(1,1) | Autoincrement |
| TIMESTAMPTZ | DATETIMEOFFSET(3) | Preserva timezone offset |
| BOOLEAN | BIT | 0/1 |
| NOW() | SYSUTCDATETIME() | DEFAULT |
| ON CONFLICT DO UPDATE | MERGE | Upsert |
| RETURNING * | OUTPUT inserted.* | Result set |
| LIMIT N OFFSET M | OFFSET M ROWS FETCH NEXT N | Paginació |

## Encoding

```sql
CREATE DATABASE ATNE_FJE COLLATE Latin1_General_100_CI_AI_SC_UTF8;
```

## Taules (ordre de creació)

### 1. atne_docents
- id (NVARCHAR 255 PRIMARY KEY)
- email, alias (NVARCHAR MAX)
- is_admin (BIT DEFAULT 0)
- created_at (DATETIMEOFFSET DEFAULT SYSDATETIMEOFFSET())

### 2. history (CORE)
- id (BIGINT IDENTITY)
- profile_json, context_json, params_json (NVARCHAR MAX + CHECK ISJSON)
- refine_count, edit_manual, exported (INT/BIT)
- [Sprint 1A] model_used, endpoint, duration_ms, n_words_in, n_words_out, docent_hash, quality_summary, auditor_used, feedback booleans
- [Sprint 1B] copied, time_on_step4_ms, review_items, cost_estimat_eur, models_per_phase
- [Sprint B] source
- [Sprint 1C] prompt_version
- created_at, updated_at (DATETIMEOFFSET)

### 3. atne_drafts
- id (BIGINT IDENTITY)
- docent_id (NVARCHAR MAX)
- text (NVARCHAR MAX NOT NULL)
- created_at, updated_at (DATETIMEOFFSET)

### 4. atne_adaptations
- id (BIGINT IDENTITY)
- docent_id (NVARCHAR MAX)
- adapted_html (NVARCHAR MAX NOT NULL)
- profile_snapshot, context_snapshot, complements_snapshot (JSONB → NVARCHAR MAX)

### 5. atne_custom_profiles
- id (BIGINT IDENTITY)
- docent_id (NVARCHAR MAX)
- profile_data (NVARCHAR MAX + CHECK ISJSON)

### 6. system_config
- key (NVARCHAR 255 PRIMARY KEY)
- value (NVARCHAR MAX + CHECK ISJSON)

### 7. atne_prompt_debug
- id (BIGINT IDENTITY)
- adapt_id (NVARCHAR 255 UNIQUE)
- ts_ms (BIGINT)
- data (NVARCHAR MAX + CHECK ISJSON)

### 8. atne_sessions
- id (BIGINT IDENTITY)
- conditions (NVARCHAR MAX - JSON array)
- latency_ms, n_instructions (INT)
- verify_score (NUMERIC)

### 9. atne_pilot_events
- id (BIGINT IDENTITY)
- event_type (NVARCHAR MAX NOT NULL)
- data (NVARCHAR MAX + CHECK ISJSON)
- history_id (BIGINT - FK lògica)

### 10. atne_pilot_consent
- id (BIGINT IDENTITY)
- docent_id (NVARCHAR 255 NOT NULL)
- decision (NVARCHAR 255 - accepted/declined/revoked)

## Reescriptures Python

### RETURNING → OUTPUT
```
INSERT INTO history (...) OUTPUT inserted.id, inserted.updated_at VALUES (...)
```

### ON CONFLICT → MERGE
```
MERGE INTO system_config t
USING (SELECT ... AS key, ... AS value) s
ON t.key = s.key
WHEN MATCHED THEN UPDATE SET value = s.value
WHEN NOT MATCHED THEN INSERT (key, value) VALUES (s.key, s.value);
```

### LIMIT → OFFSET FETCH
```
SELECT ... FROM history OFFSET 0 ROWS FETCH NEXT {limit} ROWS ONLY
```

## Taules NO a migrar

- rag_fje (Dead code, RAG desactivat)
- kg_nodes (Dead code, KG desactivat)
- kg_edges (Dead code, KG desactivat)

## Checklist de migració

- [ ] CREATE DATABASE ATNE_FJE amb collation UTF-8
- [ ] CREATE TABLE per a 10 taules (ordre: docents, history, drafts, adaptations, custom_profiles, system_config, prompt_debug, sessions, pilot_events, pilot_consent)
- [ ] INSERT inicial de system_config
- [ ] CREATE INDEXES a totes les taules
- [ ] Verificar IDENTITY sequences (no começar a 0)
- [ ] BACKUP inicial de database
- [ ] Update backend .env (MSSQL connection string)
- [ ] Reescriure queries Python (RETURNING→OUTPUT, ON CONFLICT→MERGE, LIMIT→OFFSET FETCH)
- [ ] Test endpoints: POST /api/history, GET /api/history, PATCH /api/history, DELETE
- [ ] Test endpoints drafts i adaptations
- [ ] Verificar CHECK ISJSON en totes les columnes JSON
- [ ] Verificar autorització docent_id (backend filters, no RLS)

## Recursos
- MS SQL Server JSON: https://docs.microsoft.com/en-us/sql/relational-databases/json/
- PostgreSQL to MSSQL: https://learn.microsoft.com/en-us/sql/ssma/sql-server-migration-assistant
- DATETIMEOFFSET: https://docs.microsoft.com/en-us/sql/t-sql/data-types/datetimeoffset-transact-sql
- Collation: https://docs.microsoft.com/en-us/sql/t-sql/statements/create-database-transact-sql

---

**Document**: Mapping PostgreSQL → Microsoft SQL Server (ATNE)
**Data**: 2026-04-23
**Versió**: 1.0
**Status**: Llistat per a DBA FJE
