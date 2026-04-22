-- ============================================================================
-- Sprint 1C — Events UX, versionat del prompt, consentiment informat
-- ============================================================================
-- Context:
--   Pilot FJE 20/04-08/05/2026. Arribats al dia 3 del pilot, identifiquem tres
--   gaps crítics d'avaluació:
--     (1) No sabem quina versió del prompt ha generat cada adaptació
--         → sense això, els 200+ outputs del pilot no es poden comparar
--           entre setmanes (cada refactor del prompt invalida comparacions).
--     (2) No capturem events granulars d'interacció del docent
--         (refines, edits, complements generats/esborrats, biblioteca,
--          canvis de model, exports) — només el resultat final.
--     (3) No tenim rastre del consentiment informat per a recerca (RGPD +
--         AI Act) ni del DPIA.
--
-- Aquest SQL afegeix:
--   A. Columna prompt_version a atne_sessions i history
--   B. Columna cost_estimat_eur a atne_sessions (ja existeix a history)
--   C. Taula atne_pilot_events (events UX granulars)
--   D. Taula atne_pilot_consent (traçabilitat del consentiment)
--
-- Projecte Supabase:  qlftykfqjwaxucoeqcjv
-- Tipus de canvi:     ADDITIVE (ADD COLUMN + CREATE TABLE IF NOT EXISTS)
-- Risc:               Baix. Cap canvi destructiu. Idempotent.
--
-- Com executar-ho:
--   1. Supabase dashboard → projecte qlftykfqjwaxucoeqcjv → SQL Editor
--   2. Copiar el bloc "MIGRACIÓ" complet i enganxar-lo
--   3. Executar amb Run
--   4. Verificar amb el bloc "VERIFICACIÓ"
-- ============================================================================


-- ─── MIGRACIÓ INICI ─────────────────────────────────────────────────────────

BEGIN;

-- A. prompt_version: git hash curt + data, identifica la versió del prompt
--    que ha generat cada adaptació. Imprescindible per a comparatives cegues
--    entre setmanes del pilot.
ALTER TABLE atne_sessions ADD COLUMN IF NOT EXISTS prompt_version TEXT;
ALTER TABLE history        ADD COLUMN IF NOT EXISTS prompt_version TEXT;

CREATE INDEX IF NOT EXISTS idx_atne_sessions_prompt_version
    ON atne_sessions (prompt_version);
CREATE INDEX IF NOT EXISTS idx_history_prompt_version
    ON history (prompt_version);

-- B. cost_estimat_eur a atne_sessions (història ja té aquesta columna)
ALTER TABLE atne_sessions
    ADD COLUMN IF NOT EXISTS cost_estimat_eur NUMERIC(10, 6);

-- C. Taula atne_pilot_events — events UX granulars
CREATE TABLE IF NOT EXISTS atne_pilot_events (
    id BIGSERIAL PRIMARY KEY,
    ts TIMESTAMPTZ NOT NULL DEFAULT now(),
    docent_id TEXT,                 -- email (Supabase Auth) o NULL
    docent_hash TEXT,               -- SHA256 del email per anàlisi anònima
    session_id TEXT,                -- adapt_id o UUID client, lliga amb history
    history_id BIGINT,              -- FK lògica a history.id (no constraint dur)
    event_type TEXT NOT NULL,       -- 'refine_started', 'refined', 'complement_generated',
                                    -- 'complement_deleted', 'copied', 'exported',
                                    -- 'biblioteca_opened', 'draft_loaded',
                                    -- 'model_switch', 'manual_edit', 'pas_change',
                                    -- 'consent_shown', 'rubric_submitted'
    step TEXT,                      -- 'pas1' | 'pas2' | 'pas3' | 'pas4' | NULL
    data JSONB,                     -- payload específic de l'event (preset, target, format, etc.)
    prompt_version TEXT             -- opcional, correlaciona amb atne_sessions
);

CREATE INDEX IF NOT EXISTS idx_pilot_events_ts
    ON atne_pilot_events (ts DESC);
CREATE INDEX IF NOT EXISTS idx_pilot_events_docent_hash
    ON atne_pilot_events (docent_hash);
CREATE INDEX IF NOT EXISTS idx_pilot_events_event_type
    ON atne_pilot_events (event_type);
CREATE INDEX IF NOT EXISTS idx_pilot_events_history_id
    ON atne_pilot_events (history_id);
CREATE INDEX IF NOT EXISTS idx_pilot_events_session_id
    ON atne_pilot_events (session_id);

COMMENT ON TABLE atne_pilot_events IS
    'Events UX granulars del pilot ATNE (2026-04-20 a 2026-05-08). Cada clic/acció rellevant pedagògicament es registra aquí. Complementa `history` (1 row per adaptació finalitzada) amb el detall del procés.';


-- D. Taula atne_pilot_consent — traçabilitat del consentiment (RGPD/AI Act)
CREATE TABLE IF NOT EXISTS atne_pilot_consent (
    id BIGSERIAL PRIMARY KEY,
    ts TIMESTAMPTZ NOT NULL DEFAULT now(),
    docent_id TEXT NOT NULL,        -- email @fje.edu
    docent_hash TEXT,               -- hash SHA256 per anàlisi anònima
    decision TEXT NOT NULL,         -- 'accepted' | 'declined' | 'revoked'
    dpia_version TEXT,              -- referència al document DPIA vigent (ex: '2026-04-22')
    consent_text_version TEXT,      -- versió del text de consentiment mostrat
    user_agent TEXT,                -- navegador que va donar el consentiment
    ip_hash TEXT                    -- SHA256 de la IP (traçabilitat mínima, no PII)
);

CREATE INDEX IF NOT EXISTS idx_pilot_consent_docent
    ON atne_pilot_consent (docent_id);
CREATE INDEX IF NOT EXISTS idx_pilot_consent_ts
    ON atne_pilot_consent (ts DESC);

COMMENT ON TABLE atne_pilot_consent IS
    'Registre de consentiments informats dels docents participants al pilot ATNE. Cal per a RGPD art. 7 (demostrabilitat del consentiment) i AI Act Annex III. El docent pot revocar en qualsevol moment — es crea un nou row amb decision=revoked.';


-- E. Configuració del pilot i del DPIA vigent
INSERT INTO system_config (key, value, updated_by) VALUES
    ('pilot_dpia_version', '"2026-04-22"', 'system'),
    ('pilot_consent_text_version', '"v1.0"', 'system'),
    ('pilot_start_date', '"2026-04-20"', 'system'),
    ('pilot_end_date', '"2026-05-08"', 'system')
ON CONFLICT (key) DO NOTHING;

COMMIT;

-- ─── MIGRACIÓ FI ────────────────────────────────────────────────────────────


-- ============================================================================
-- VERIFICACIÓ (read-only)
-- ============================================================================

-- 1. Columnes noves
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public'
  AND ((table_name = 'atne_sessions' AND column_name IN ('prompt_version', 'cost_estimat_eur'))
       OR (table_name = 'history' AND column_name = 'prompt_version'))
ORDER BY table_name, column_name;

-- Esperat: 3 files.

-- 2. Taules noves
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN ('atne_pilot_events', 'atne_pilot_consent')
ORDER BY table_name;

-- Esperat: 2 files.

-- 3. Configuració del pilot
SELECT key, value
FROM system_config
WHERE key LIKE 'pilot_%'
ORDER BY key;

-- Esperat: almenys 5 files (les del sprint 1B + les 4 d'aquí).


-- ============================================================================
-- ROLLBACK (no executar llevat que calgui desfer)
-- ============================================================================
/*
BEGIN;

DELETE FROM system_config WHERE key IN (
    'pilot_dpia_version', 'pilot_consent_text_version',
    'pilot_start_date', 'pilot_end_date'
);

DROP INDEX IF EXISTS idx_pilot_consent_ts;
DROP INDEX IF EXISTS idx_pilot_consent_docent;
DROP TABLE IF EXISTS atne_pilot_consent;

DROP INDEX IF EXISTS idx_pilot_events_session_id;
DROP INDEX IF EXISTS idx_pilot_events_history_id;
DROP INDEX IF EXISTS idx_pilot_events_event_type;
DROP INDEX IF EXISTS idx_pilot_events_docent_hash;
DROP INDEX IF EXISTS idx_pilot_events_ts;
DROP TABLE IF EXISTS atne_pilot_events;

ALTER TABLE atne_sessions DROP COLUMN IF EXISTS cost_estimat_eur;

DROP INDEX IF EXISTS idx_history_prompt_version;
DROP INDEX IF EXISTS idx_atne_sessions_prompt_version;
ALTER TABLE history DROP COLUMN IF EXISTS prompt_version;
ALTER TABLE atne_sessions DROP COLUMN IF EXISTS prompt_version;

COMMIT;
*/
