-- ============================================================================
-- Sprint 1A.1 — Ampliar taula `history` per instrumentació del pilot
-- ============================================================================
-- Context:
--   Pilot FJE 20/04-08/05/2026 amb ~16 docents. Ampliem la taula `history`
--   existent del Supabase vell (projecte qlftykfqjwaxucoeqcjv) amb metadades
--   addicionals per capturar: model usat, durada, quality report, interacció
--   docent (refines, edits, feedback ampliat), hash anonimitzat del docent.
--
-- Projecte Supabase:  qlftykfqjwaxucoeqcjv  (el vell, NO el nou corpusFJE)
-- Taula:              public.history
-- Tipus de canvi:     ADDITIVE (només ADD COLUMN, cap DROP/ALTER existent)
-- Rollback possible:  Sí (DROP COLUMN al final d'aquest fitxer, comentat)
-- Risc:               Baix. Rows antics queden amb NULL als camps nous.
--                     Cap codi actual depèn d'aquests camps.
--
-- Com executar-ho:
--   1. Supabase dashboard → projecte qlftykfqjwaxucoeqcjv → SQL Editor
--   2. Copiar TOT el bloc "MIGRACIÓ" (de línia --- MIGRACIÓ INICI --- fins
--      --- MIGRACIÓ FI ---) i enganxar-lo
--   3. Executar amb Run
--   4. Verificar amb el bloc "VERIFICACIÓ" (queries SELECT, només lectura)
--
-- Després d'executar aquest SQL:
--   - Codi actual segueix funcionant igual (NULL als camps nous)
--   - Sprint 1A.2 instrumenta els endpoints per escriure-hi
--   - Sprint 1B.1 (/admin) llegeix aquests camps al dashboard
-- ============================================================================


-- ─── MIGRACIÓ INICI ─────────────────────────────────────────────────────────

BEGIN;

-- A. Metadades de la crida LLM
ALTER TABLE history ADD COLUMN IF NOT EXISTS model_used TEXT;
ALTER TABLE history ADD COLUMN IF NOT EXISTS endpoint TEXT;
ALTER TABLE history ADD COLUMN IF NOT EXISTS duration_ms INT;

-- B. Interacció del docent (refines + edició manual + exportació)
ALTER TABLE history ADD COLUMN IF NOT EXISTS refine_count INT NOT NULL DEFAULT 0;
ALTER TABLE history ADD COLUMN IF NOT EXISTS edit_manual BOOLEAN NOT NULL DEFAULT false;
ALTER TABLE history ADD COLUMN IF NOT EXISTS exported BOOLEAN NOT NULL DEFAULT false;

-- C. Context educatiu desnormalitzat (per filtrar al dashboard sense parsejar JSON)
ALTER TABLE history ADD COLUMN IF NOT EXISTS etapa TEXT;
ALTER TABLE history ADD COLUMN IF NOT EXISTS curs TEXT;
ALTER TABLE history ADD COLUMN IF NOT EXISTS perfil_kind TEXT;   -- 'observable' | 'nese' | 'generic'
ALTER TABLE history ADD COLUMN IF NOT EXISTS via TEXT;           -- 'observable' | 'nese' (pot ser NULL)

-- D. Mètriques de text
ALTER TABLE history ADD COLUMN IF NOT EXISTS n_words_in INT;
ALTER TABLE history ADD COLUMN IF NOT EXISTS n_words_out INT;

-- E. Identitat del docent (hash anonimitzat, preparat per tokenNet)
ALTER TABLE history ADD COLUMN IF NOT EXISTS docent_hash TEXT;

-- F. Pipeline de qualitat (resum condensat, no el report sencer)
ALTER TABLE history ADD COLUMN IF NOT EXISTS quality_summary JSONB;
ALTER TABLE history ADD COLUMN IF NOT EXISTS auditor_used BOOLEAN NOT NULL DEFAULT false;

-- G. Feedback docent ampliat (checkboxes nous del Pas 4)
ALTER TABLE history ADD COLUMN IF NOT EXISTS fb_used_in_class BOOLEAN;    -- "l'he usat a classe"
ALTER TABLE history ADD COLUMN IF NOT EXISTS fb_needs_redo BOOLEAN;       -- "caldria refer-ho"
ALTER TABLE history ADD COLUMN IF NOT EXISTS fb_level_ok BOOLEAN;         -- "s'ha adequat al nivell"

-- Índexs útils per al dashboard /admin (Sprint 1B)
-- (No són imprescindibles pel MVP però el dashboard filtra molt per aquests camps)
CREATE INDEX IF NOT EXISTS idx_history_created_at ON history (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_history_docent_hash ON history (docent_hash);
CREATE INDEX IF NOT EXISTS idx_history_etapa ON history (etapa);
CREATE INDEX IF NOT EXISTS idx_history_endpoint ON history (endpoint);

COMMIT;

-- ─── MIGRACIÓ FI ────────────────────────────────────────────────────────────


-- ============================================================================
-- VERIFICACIÓ (read-only, pots executar-ho per comprovar que tot ha anat bé)
-- ============================================================================

-- 1. Llistar totes les columnes de history després de la migració
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_schema = 'public' AND table_name = 'history'
ORDER BY ordinal_position;

-- Esperat: veure les columnes antigues + totes les noves (model_used, endpoint,
-- duration_ms, refine_count, edit_manual, exported, etapa, curs, perfil_kind,
-- via, n_words_in, n_words_out, docent_hash, quality_summary, auditor_used,
-- fb_used_in_class, fb_needs_redo, fb_level_ok)

-- 2. Verificar que els índexs s'han creat
SELECT indexname, indexdef
FROM pg_indexes
WHERE schemaname = 'public' AND tablename = 'history';

-- 3. Comprovar que els rows antics no s'han trencat (NULL als camps nous)
SELECT COUNT(*) AS total_rows,
       COUNT(model_used) AS rows_amb_model,
       COUNT(docent_hash) AS rows_amb_hash
FROM history;

-- Esperat: total_rows > 0, rows_amb_model = 0, rows_amb_hash = 0
-- (tots els rows antics queden amb NULL fins que l'instrumentació nova comenci a escriure)


-- ============================================================================
-- ROLLBACK (NO EXECUTAR LLEVAT QUE CALGUI DESFER LA MIGRACIÓ)
-- ============================================================================
-- Descomentar només si cal tornar enrere. Es perden les dades d'aquests camps.
/*
BEGIN;

DROP INDEX IF EXISTS idx_history_endpoint;
DROP INDEX IF EXISTS idx_history_etapa;
DROP INDEX IF EXISTS idx_history_docent_hash;
DROP INDEX IF EXISTS idx_history_created_at;

ALTER TABLE history DROP COLUMN IF EXISTS fb_level_ok;
ALTER TABLE history DROP COLUMN IF EXISTS fb_needs_redo;
ALTER TABLE history DROP COLUMN IF EXISTS fb_used_in_class;
ALTER TABLE history DROP COLUMN IF EXISTS auditor_used;
ALTER TABLE history DROP COLUMN IF EXISTS quality_summary;
ALTER TABLE history DROP COLUMN IF EXISTS docent_hash;
ALTER TABLE history DROP COLUMN IF EXISTS n_words_out;
ALTER TABLE history DROP COLUMN IF EXISTS n_words_in;
ALTER TABLE history DROP COLUMN IF EXISTS via;
ALTER TABLE history DROP COLUMN IF EXISTS perfil_kind;
ALTER TABLE history DROP COLUMN IF EXISTS curs;
ALTER TABLE history DROP COLUMN IF EXISTS etapa;
ALTER TABLE history DROP COLUMN IF EXISTS exported;
ALTER TABLE history DROP COLUMN IF EXISTS edit_manual;
ALTER TABLE history DROP COLUMN IF EXISTS refine_count;
ALTER TABLE history DROP COLUMN IF EXISTS duration_ms;
ALTER TABLE history DROP COLUMN IF EXISTS endpoint;
ALTER TABLE history DROP COLUMN IF EXISTS model_used;

COMMIT;
*/
