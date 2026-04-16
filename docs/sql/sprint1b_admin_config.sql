-- ============================================================================
-- Sprint 1B — Capa administrador + captura implícita ampliada
-- ============================================================================
-- Context:
--   El cap ha donat llum verda a comparar LLMs superiors (GPT-4o-mini vs GPT-4o
--   vs Mistral Large vs Gemma 4). Necessitem:
--   (a) persistència del selector de model per fase (generate/adapt/refine/auditor/complements)
--   (b) captura de senyals implícits del pilot: copy, time_on_step4, rúbrica lleugera
--
--   Aquest SQL complementa docs/sql/sprint1a_alter_history.sql. Tots dos són
--   additive i idempotents. Es poden executar en ordre cronològic sense risc.
--
-- Projecte Supabase:  qlftykfqjwaxucoeqcjv  (el vell, on viu `history`)
-- Tipus de canvi:     ADDITIVE (ADD COLUMN IF NOT EXISTS + CREATE TABLE IF NOT EXISTS)
-- Risc:               Baix. Cap canvi destructiu.
--
-- Com executar-ho:
--   1. Supabase dashboard → projecte qlftykfqjwaxucoeqcjv → SQL Editor
--   2. Copiar el bloc "MIGRACIÓ" complet i enganxar-lo
--   3. Executar amb Run
--   4. Verificar amb el bloc "VERIFICACIÓ"
-- ============================================================================


-- ─── MIGRACIÓ INICI ─────────────────────────────────────────────────────────

BEGIN;

-- A. Columnes addicionals a `history` per a senyals implícits del pilot
ALTER TABLE history ADD COLUMN IF NOT EXISTS copied BOOLEAN NOT NULL DEFAULT false;
ALTER TABLE history ADD COLUMN IF NOT EXISTS time_on_step4_ms INT;
ALTER TABLE history ADD COLUMN IF NOT EXISTS review_items JSONB;
ALTER TABLE history ADD COLUMN IF NOT EXISTS cost_estimat_eur NUMERIC(10, 6);

-- `review_items` desarà els 6 checkboxes de la rúbrica lleugera com a JSONB:
--   {
--     "nivell_inadequat": bool,          -- Nivell lingüístic massa alt/baix
--     "contingut_perdut": bool,          -- Ha perdut contingut curricular important
--     "errors_catala": bool,             -- Errors o frases estranyes en català
--     "format_inadequat": bool,          -- Format o estructura no adequats
--     "complements_poc_utils": bool,     -- Complements poc útils
--     "altres_text": "text opcional"     -- Camp lliure (1 línia)
--   }
-- NULL si el docent no ha clicat "Alguna cosa no quadra". Fora d'aquest cas,
-- almenys una clau és true o `altres_text` no és buit.

-- B. Model usat per fase (un row de history pot involucrar múltiples crides LLM)
-- `model_used` d'sprint 1A guardava UN model. Ara separem per fase per
-- a poder comparar A/B amb granularitat.
ALTER TABLE history ADD COLUMN IF NOT EXISTS models_per_phase JSONB;

-- `models_per_phase` exemple:
--   {
--     "generate": "gpt-4o-mini",     -- si s'ha generat text nou
--     "adapt": "gemma-4-31b-it",     -- model que ha adaptat el text
--     "refine": ["gemma-4-31b-it", "gemma-4-31b-it"],  -- array si múltiples refines
--     "auditor": null,               -- null si auditor desactivat
--     "complements": "gpt-4o"        -- model per als complements
--   }
-- Els camps `model_used` i `auditor_used` d'sprint 1A queden com a fallback
-- legacy per compatibilitat. `models_per_phase` és el que usarà el dashboard.

-- C. Índexs addicionals per filtres del dashboard
CREATE INDEX IF NOT EXISTS idx_history_copied ON history (copied) WHERE copied = true;
CREATE INDEX IF NOT EXISTS idx_history_review_items ON history USING GIN (review_items);
CREATE INDEX IF NOT EXISTS idx_history_models_per_phase ON history USING GIN (models_per_phase);


-- D. Taula nova `system_config` per persistir el selector runtime dels motors
CREATE TABLE IF NOT EXISTS system_config (
    key TEXT PRIMARY KEY,
    value JSONB NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_by TEXT  -- hash del docent/admin que ha fet el canvi, NULL per system
);

COMMENT ON TABLE system_config IS
    'Configuració runtime de l''app ATNE. Key-value. El backend llegeix aquesta taula al startup i a cada PUT /api/admin/config. Sobrevisca a restarts de Cloud Run.';

COMMENT ON COLUMN system_config.key IS
    'Clau de configuració. Exemples: atne_model_generate, atne_model_adapt, atne_model_refine, atne_model_auditor, atne_model_complements, atne_auditor_enabled, languagetool_url, admin_budget_eur_max, pilot_active';

COMMENT ON COLUMN system_config.value IS
    'Valor JSONB. Per a models: {"model_id": "gpt-4o-mini", "cost_per_call_eur": 0.002, "set_by": "admin"}. Per a booleans: true/false. Per a strings: "value".';

-- Valors inicials per al pilot (es poden modificar via /admin un cop viu).
-- Només inserim si no existeixen — idempotent.
INSERT INTO system_config (key, value, updated_by) VALUES
    ('atne_model_generate', '{"model_id": "gemma-4-31b-it", "cost_per_call_eur": 0, "set_by": "system"}', 'system'),
    ('atne_model_adapt',    '{"model_id": "gemma-4-31b-it", "cost_per_call_eur": 0, "set_by": "system"}', 'system'),
    ('atne_model_refine',   '{"model_id": "gemma-4-31b-it", "cost_per_call_eur": 0, "set_by": "system"}', 'system'),
    ('atne_model_auditor',  '{"model_id": "gpt-4o-mini",    "cost_per_call_eur": 0.002, "set_by": "system"}', 'system'),
    ('atne_model_complements', '{"model_id": "gemma-4-31b-it", "cost_per_call_eur": 0, "set_by": "system"}', 'system'),
    ('atne_auditor_enabled', 'false', 'system'),
    ('admin_budget_eur_max', '30', 'system'),
    ('pilot_active', 'true', 'system')
ON CONFLICT (key) DO NOTHING;

COMMIT;

-- ─── MIGRACIÓ FI ────────────────────────────────────────────────────────────


-- ============================================================================
-- VERIFICACIÓ (read-only)
-- ============================================================================

-- 1. Columnes noves a history
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public' AND table_name = 'history'
  AND column_name IN ('copied', 'time_on_step4_ms', 'review_items', 'cost_estimat_eur', 'models_per_phase')
ORDER BY column_name;

-- Esperat: 5 files.

-- 2. Taula system_config
SELECT key, value, updated_at
FROM system_config
ORDER BY key;

-- Esperat: 8 files (els valors inicials del INSERT).

-- 3. Verificar que un row de history nou pot inserir els nous camps
-- (només per test, no afegeix cap row — RAISE exception al final)
-- BEGIN;
-- INSERT INTO history (profile_name, original_text, adapted_text, copied, models_per_phase)
-- VALUES ('test', 'original', 'adaptat', true, '{"adapt": "gpt-4o"}'::jsonb)
-- RETURNING id, copied, models_per_phase;
-- ROLLBACK;


-- ============================================================================
-- ROLLBACK (no executar llevat que calgui desfer)
-- ============================================================================
/*
BEGIN;

DROP INDEX IF EXISTS idx_history_models_per_phase;
DROP INDEX IF EXISTS idx_history_review_items;
DROP INDEX IF EXISTS idx_history_copied;

ALTER TABLE history DROP COLUMN IF EXISTS models_per_phase;
ALTER TABLE history DROP COLUMN IF EXISTS cost_estimat_eur;
ALTER TABLE history DROP COLUMN IF EXISTS review_items;
ALTER TABLE history DROP COLUMN IF EXISTS time_on_step4_ms;
ALTER TABLE history DROP COLUMN IF EXISTS copied;

DROP TABLE IF EXISTS system_config;

COMMIT;
*/
