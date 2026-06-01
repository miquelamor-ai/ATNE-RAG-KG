-- ATNE · Cache de transliteracions verificades (taula `atne_translits`)
-- Decisió 2026-05-31: separació canon (regles per L1 al corpusFJE) / operativa (cache verificat aquí).
-- Acordat amb mineriaRAG; document de referència: docs/transliteracio_standards_l1_2026-05-31.md
--
-- Aplicar via Supabase SQL Editor:
--   https://supabase.com/dashboard/project/qlftykfqjwaxucoeqcjv/sql/new
--
-- Verificar:
--   SELECT count(*) FROM atne_translits;
--   SELECT terme, l1, transliteracio, verified FROM atne_translits ORDER BY created_at DESC LIMIT 10;

CREATE TABLE IF NOT EXISTS atne_translits (
  id              BIGSERIAL PRIMARY KEY,
  terme           TEXT NOT NULL,              -- terme en llengua de sortida (CA per defecte)
  l1              TEXT NOT NULL,              -- codi ISO + variant si cal (ex: 'ar', 'zh', 'ar-MA', 'zgh-Tfng')
  transliteracio  TEXT NOT NULL,              -- transliteració segons l'estàndard canon per L1
  estandard       TEXT,                       -- nom de l'estàndard usat (ex: 'ALA-LC simplificat', 'Pinyin amb tons')
  verified        BOOLEAN NOT NULL DEFAULT false,
  verified_by     TEXT,                       -- email docent FJE (auth.jwt()->>'email')
  verified_at     TIMESTAMPTZ,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT atne_translits_unique_terme_l1 UNIQUE (terme, l1)
);

-- Index per a lookup ràpid abans de cridar el LLM.
CREATE INDEX IF NOT EXISTS idx_atne_translits_lookup
  ON atne_translits (terme, l1)
  WHERE verified = true;

-- Index per a panel admin (entrades pendents revisió).
CREATE INDEX IF NOT EXISTS idx_atne_translits_pending
  ON atne_translits (verified, created_at DESC)
  WHERE verified = false;

-- RLS: lectura oberta (qualsevol pipeline ATNE pot fer lookup), escriptura via backend amb anon key.
-- Quan s'afegeixi auth real amb JWT FJE, restringir UPDATE/INSERT a auth.jwt()->>'email' LIKE '%@fje.edu'.
ALTER TABLE atne_translits ENABLE ROW LEVEL SECURITY;

CREATE POLICY "atne_translits_anon_select"
  ON atne_translits FOR SELECT TO anon
  USING (true);

CREATE POLICY "atne_translits_anon_write"
  ON atne_translits FOR ALL TO anon
  USING (true) WITH CHECK (true);

-- Trigger per actualitzar updated_at automàticament.
CREATE OR REPLACE FUNCTION atne_translits_touch_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS atne_translits_updated_at_trigger ON atne_translits;
CREATE TRIGGER atne_translits_updated_at_trigger
  BEFORE UPDATE ON atne_translits
  FOR EACH ROW EXECUTE FUNCTION atne_translits_touch_updated_at();
