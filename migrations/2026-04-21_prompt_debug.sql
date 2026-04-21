-- Taula per persistir les adaptacions del debug endpoint.
-- Sobreviu canvis d'instància a Cloud Run (el buffer en memòria no basta
-- quan hi ha fins a 3 instàncies concurrents).
--
-- Executar manualment a Supabase SQL Editor.

CREATE TABLE IF NOT EXISTS atne_prompt_debug (
  id           BIGSERIAL PRIMARY KEY,
  adapt_id     TEXT UNIQUE NOT NULL,
  ts_ms        BIGINT NOT NULL,
  docent_id    TEXT,
  model        TEXT,
  data         JSONB NOT NULL,
  created_at   TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_atne_prompt_debug_ts ON atne_prompt_debug (ts_ms DESC);
CREATE INDEX IF NOT EXISTS idx_atne_prompt_debug_adapt_id ON atne_prompt_debug (adapt_id);

-- Política de retenció: només mantenim les 100 últimes. Cron opcional per
-- esborrar les més antigues (no crític — si no es fa, la taula creix però
-- els índexs ho mantenen ràpid). Exemple:
--   DELETE FROM atne_prompt_debug
--   WHERE id NOT IN (SELECT id FROM atne_prompt_debug ORDER BY ts_ms DESC LIMIT 100);
