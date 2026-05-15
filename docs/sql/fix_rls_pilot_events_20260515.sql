-- ============================================================================
-- FIX URGENT — taules pilot + RLS (2026-05-15, revisat)
-- ============================================================================
-- Context:
--   El 2026-05-15 descobrim que la taula `atne_pilot_events` NO existeix
--   físicament a Postgres (només quedava al schema cache de PostgREST,
--   probablement per una migració incompleta del sprint 1C). Conseqüència:
--   tots els events del pilot — incloent els suggeriments recollits durant
--   la demo als homòlegs DOP+InfPri — s'han perdut.
--
--   `atne_sessions` (759 rows) i `history` (144 rows) sí funcionen, així
--   que les adaptacions sí es desaven; només la telemetria UX granular
--   estava trencada.
--
-- Aquest SQL fa, en una sola transacció idempotent:
--   A. CREATE TABLE IF NOT EXISTS atne_pilot_events  (definició sprint 1C)
--   B. CREATE TABLE IF NOT EXISTS atne_pilot_consent (definició sprint 1C)
--   C. Habilita RLS a les dues taules
--   D. Crea les polítiques INSERT/SELECT que permeten al backend (anon key)
--      escriure-hi i al dashboard /admin/pilot llegir-les
--
-- Projecte Supabase:  qlftykfqjwaxucoeqcjv
-- Tipus de canvi:     ADDITIVE + IDEMPOTENT (IF NOT EXISTS arreu)
-- Risc:               Baix. Cap canvi destructiu.
--
-- Com executar-ho:
--   1. Supabase dashboard → projecte qlftykfqjwaxucoeqcjv → SQL Editor
--   2. Copiar el bloc "MIGRACIÓ" complet i fer Run
--   3. Verificar amb el bloc "VERIFICACIÓ"
--   4. NOTIFY pgrst, 'reload schema'; (al final ja inclòs)
-- ============================================================================


-- ─── MIGRACIÓ INICI ─────────────────────────────────────────────────────────

BEGIN;

-- A. Taula atne_pilot_events — events UX granulars del pilot
CREATE TABLE IF NOT EXISTS atne_pilot_events (
    id BIGSERIAL PRIMARY KEY,
    ts TIMESTAMPTZ NOT NULL DEFAULT now(),
    docent_id TEXT,
    docent_hash TEXT,
    session_id TEXT,
    history_id BIGINT,
    event_type TEXT NOT NULL,
    step TEXT,
    data JSONB,
    prompt_version TEXT
);

CREATE INDEX IF NOT EXISTS idx_pilot_events_ts          ON atne_pilot_events (ts DESC);
CREATE INDEX IF NOT EXISTS idx_pilot_events_docent_hash ON atne_pilot_events (docent_hash);
CREATE INDEX IF NOT EXISTS idx_pilot_events_event_type  ON atne_pilot_events (event_type);
CREATE INDEX IF NOT EXISTS idx_pilot_events_history_id  ON atne_pilot_events (history_id);
CREATE INDEX IF NOT EXISTS idx_pilot_events_session_id  ON atne_pilot_events (session_id);

COMMENT ON TABLE atne_pilot_events IS
    'Events UX granulars del pilot ATNE. Cada clic/acció rellevant pedagògicament (refines, complements, suggeriments, exports…) hi queda registrada.';

-- B. Taula atne_pilot_consent — traçabilitat del consentiment (RGPD/AI Act)
CREATE TABLE IF NOT EXISTS atne_pilot_consent (
    id BIGSERIAL PRIMARY KEY,
    ts TIMESTAMPTZ NOT NULL DEFAULT now(),
    docent_id TEXT NOT NULL,
    docent_hash TEXT,
    decision TEXT NOT NULL,
    dpia_version TEXT,
    consent_text_version TEXT,
    user_agent TEXT,
    ip_hash TEXT
);

CREATE INDEX IF NOT EXISTS idx_pilot_consent_docent ON atne_pilot_consent (docent_id);
CREATE INDEX IF NOT EXISTS idx_pilot_consent_ts     ON atne_pilot_consent (ts DESC);

COMMENT ON TABLE atne_pilot_consent IS
    'Registre de consentiments informats dels docents del pilot ATNE (RGPD art. 7 + AI Act).';

-- C. RLS habilitada explícitament
ALTER TABLE atne_pilot_events  ENABLE ROW LEVEL SECURITY;
ALTER TABLE atne_pilot_consent ENABLE ROW LEVEL SECURITY;

-- D. Polítiques d'INSERT (backend escriu via clau anon) i SELECT (dashboard
--    llegeix via clau anon). Les escriptures sempre venen del backend ATNE
--    amb event_type validat contra whitelist; no cal validació a la DB.
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_policies
    WHERE schemaname = 'public' AND tablename = 'atne_pilot_events'
      AND policyname = 'atne_pilot_events_insert_backend'
  ) THEN
    CREATE POLICY atne_pilot_events_insert_backend
      ON atne_pilot_events FOR INSERT
      TO anon, authenticated
      WITH CHECK (true);
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM pg_policies
    WHERE schemaname = 'public' AND tablename = 'atne_pilot_events'
      AND policyname = 'atne_pilot_events_select_all'
  ) THEN
    CREATE POLICY atne_pilot_events_select_all
      ON atne_pilot_events FOR SELECT
      TO anon, authenticated
      USING (true);
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM pg_policies
    WHERE schemaname = 'public' AND tablename = 'atne_pilot_consent'
      AND policyname = 'atne_pilot_consent_insert_backend'
  ) THEN
    CREATE POLICY atne_pilot_consent_insert_backend
      ON atne_pilot_consent FOR INSERT
      TO anon, authenticated
      WITH CHECK (true);
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM pg_policies
    WHERE schemaname = 'public' AND tablename = 'atne_pilot_consent'
      AND policyname = 'atne_pilot_consent_select_all'
  ) THEN
    CREATE POLICY atne_pilot_consent_select_all
      ON atne_pilot_consent FOR SELECT
      TO anon, authenticated
      USING (true);
  END IF;
END $$;

COMMIT;

-- Força refresc del schema cache de PostgREST perquè vegi les taules noves
NOTIFY pgrst, 'reload schema';

-- ─── MIGRACIÓ FI ────────────────────────────────────────────────────────────


-- ============================================================================
-- VERIFICACIÓ (read-only)
-- ============================================================================

-- 1. Taules creades
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN ('atne_pilot_events', 'atne_pilot_consent')
ORDER BY table_name;
-- Esperat: 2 files.

-- 2. RLS habilitada
SELECT relname, relrowsecurity
FROM pg_class
WHERE relname IN ('atne_pilot_events', 'atne_pilot_consent');
-- Esperat: relrowsecurity = true a les dues.

-- 3. Polítiques actives
SELECT tablename, policyname, cmd, roles
FROM pg_policies
WHERE schemaname = 'public'
  AND tablename IN ('atne_pilot_events', 'atne_pilot_consent')
ORDER BY tablename, cmd, policyname;
-- Esperat: 4 files (INSERT + SELECT × 2 taules).

-- 4. Self-test d'insert i lectura (executar com a service_role des del
--    SQL editor — això NO valida la RLS per anon, però sí l'existència
--    física i les columnes):
--    INSERT INTO atne_pilot_events (event_type, step, data)
--    VALUES ('client_error', 'pas3', '{"_selftest":true}'::jsonb)
--    RETURNING id, ts;
--    SELECT id, ts, event_type, data
--    FROM atne_pilot_events
--    WHERE data->>'_selftest' = 'true'
--    ORDER BY ts DESC LIMIT 1;
--    DELETE FROM atne_pilot_events WHERE data->>'_selftest' = 'true';


-- ============================================================================
-- ROLLBACK (NO executar llevat que calgui desfer)
-- ============================================================================
/*
BEGIN;

DROP POLICY IF EXISTS atne_pilot_events_insert_backend  ON atne_pilot_events;
DROP POLICY IF EXISTS atne_pilot_events_select_all      ON atne_pilot_events;
DROP POLICY IF EXISTS atne_pilot_consent_insert_backend ON atne_pilot_consent;
DROP POLICY IF EXISTS atne_pilot_consent_select_all     ON atne_pilot_consent;

-- Atenció: DROP TABLE destruirà tots els events. Només si saps el que fas:
-- DROP TABLE IF EXISTS atne_pilot_events;
-- DROP TABLE IF EXISTS atne_pilot_consent;

COMMIT;
*/
