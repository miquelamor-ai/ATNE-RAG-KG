-- ATNE · Biblioteca d'adaptacions desades al núvol
-- Prefix 'atne_' al nom de la taula per identificar-la dins el Supabase compartit.
--
-- Diferencia respecte atne_drafts:
--  - atne_drafts → text ORIGINAL del Pas 2 (abans d'adaptar)
--  - atne_adaptations → resultat FINAL del Pas 3 (HTML adaptat + imatges + edicions)
--
-- Aplicar via Supabase SQL Editor:
-- https://supabase.com/dashboard/project/qlftykfqjwaxucoeqcjv/sql/new
-- Verificar: SELECT count(*) FROM atne_adaptations;

CREATE TABLE IF NOT EXISTS atne_adaptations (
  id BIGSERIAL PRIMARY KEY,
  docent_id TEXT NOT NULL,                 -- UUID auto-generat al navegador
  title TEXT,                              -- títol visible a la biblioteca
  original_text TEXT,                      -- text original (referència)
  adapted_html TEXT NOT NULL,              -- HTML del #adapted-text, inclou <figure>
  profile_snapshot JSONB,                  -- perfil sencer al moment del desat
  context_snapshot JSONB,                  -- matèria, gènere, nivell
  complements_snapshot JSONB,              -- complements actius
  multinivell_versions JSONB,              -- versions si era grup multinivell
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index per a la llista "la meva biblioteca" (ordre descendent per data)
CREATE INDEX IF NOT EXISTS idx_atne_adaptations_docent
  ON atne_adaptations(docent_id, updated_at DESC);

-- RLS ON + policy allow-all per al rol 'anon'. Mateix patró que atne_drafts.
-- Quan s'afegeixi auth real, canviar la policy per restringir per JWT claim.
ALTER TABLE atne_adaptations ENABLE ROW LEVEL SECURITY;
CREATE POLICY "atne_adaptations_anon_rw"
  ON atne_adaptations FOR ALL TO anon
  USING (true) WITH CHECK (true);
