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

-- RLS ON + policy allow-all per al rol 'anon'. Equivalent funcional a
-- DISABLE RLS per a la clau SUPABASE_ANON_KEY (backend pot fer CRUD), però
-- deixa RLS activat per:
--   (a) quan s'afegeixi auth real (JWT del docent amb docent_id), només cal
--       canviar la policy per restringir (USING docent_id = auth.jwt()->>'docent_id').
--   (b) el dashboard de Supabase respecta RLS si es consulta sense la anon key.
-- L'autorització actual per docent_id es fa via el filtre del backend al query.
ALTER TABLE atne_drafts ENABLE ROW LEVEL SECURITY;
CREATE POLICY "atne_drafts_anon_rw"
  ON atne_drafts FOR ALL TO anon
  USING (true) WITH CHECK (true);
