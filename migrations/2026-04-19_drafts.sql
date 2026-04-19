-- Aplicar via Supabase SQL Editor o psql. Post-deploy: verificar amb SELECT count(*) FROM drafts;
-- Taula d'esborranys de text al Pas 2 (pre-adaptació).
-- Apareixen al mode 'Recuperar' del Pas 2 en una secció "Esborranys".
CREATE TABLE IF NOT EXISTS drafts (
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
CREATE INDEX IF NOT EXISTS idx_drafts_docent ON drafts(docent_id, updated_at DESC);
