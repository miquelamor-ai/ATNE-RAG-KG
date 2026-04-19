-- ATNE · esborranys desats al servidor (Opció B)
-- Prefix 'atne_' al nom de la taula per identificar-la dins el Supabase compartit.
--
-- Aplicar via Supabase SQL Editor: https://supabase.com/dashboard/project/qlftykfqjwaxucoeqcjv/sql/new
-- Verificar: SELECT count(*) FROM atne_drafts;
--
-- SI JA HAVIES EXECUTAT LA VERSIÓ ANTERIOR (sense prefix), executa PRIMER:
--   ALTER TABLE IF EXISTS drafts RENAME TO atne_drafts;
--   ALTER INDEX IF EXISTS idx_drafts_docent RENAME TO idx_atne_drafts_docent;
-- i NO executis el CREATE de sota.

CREATE TABLE IF NOT EXISTS atne_drafts (
  id BIGSERIAL PRIMARY KEY,
  docent_id TEXT NOT NULL,          -- UUID auto-generat al navegador (atne.docent_id)
  profile_id TEXT,                   -- id del perfil seleccionat quan es va desar
  title TEXT,
  text TEXT NOT NULL,
  materia TEXT,
  nivell TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_atne_drafts_docent ON atne_drafts(docent_id, updated_at DESC);
