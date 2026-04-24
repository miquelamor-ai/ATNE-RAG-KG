-- ATNE · Afegir columna `mode` per a l'experiment Flash vs Taller
--
-- Registra quin mode va usar el docent a cada adaptació.
-- Valors: 'flash' | 'taller'
-- Default 'taller' per compatibilitat amb les files existents.
--
-- Aplicar via Supabase SQL Editor:
-- https://supabase.com/dashboard/project/qlftykfqjwaxucoeqcjv/sql/new

-- 1. Taula history (adaptacions completades del pilot)
ALTER TABLE history
  ADD COLUMN IF NOT EXISTS mode TEXT NOT NULL DEFAULT 'taller';

CREATE INDEX IF NOT EXISTS idx_history_mode
  ON history (mode);

-- 2. Taula atne_adaptations (biblioteca desada)
ALTER TABLE atne_adaptations
  ADD COLUMN IF NOT EXISTS mode TEXT NOT NULL DEFAULT 'taller';

CREATE INDEX IF NOT EXISTS idx_atne_adaptations_mode
  ON atne_adaptations (mode);

-- ── Verificació ──────────────────────────────────────────────────────────────
-- Executa això per confirmar que les columnes s'han creat correctament:
--
-- SELECT column_name, data_type, column_default
-- FROM information_schema.columns
-- WHERE table_schema = 'public'
--   AND table_name IN ('history', 'atne_adaptations')
--   AND column_name = 'mode';

-- ── Rollback ─────────────────────────────────────────────────────────────────
-- DROP INDEX IF EXISTS idx_history_mode;
-- DROP INDEX IF EXISTS idx_atne_adaptations_mode;
-- ALTER TABLE history DROP COLUMN IF EXISTS mode;
-- ALTER TABLE atne_adaptations DROP COLUMN IF EXISTS mode;
