-- ATNE Sprint B (2026-04-16) — Mem\u00f2ria pilot an\u00f2nima
--
-- Afegeix la columna `source` a la taula `history` per distingir l'origen
-- del text original de cada adaptaci\u00f3:
--
--   'paste'      → el docent ha enganxat manualment el text al Pas 2
--   'upload'     → el docent ha pujat un fitxer (PDF/DOCX/TXT)
--   'generated'  → el text ha estat generat per l'LLM via /api/generate-text
--   (qualsevol altre valor = llegit com 'paste' al frontend)
--
-- Aix\u00f2 serveix al frontend per pintar un badge \"Origen\" a cada card de
-- l'historial, per\u00f2 no condiciona cap l\u00f2gica del backend.
--
-- Execuci\u00f3: copia-enganxa aquestes 2 l\u00ednies al SQL Editor de Supabase.

ALTER TABLE history ADD COLUMN IF NOT EXISTS source TEXT DEFAULT 'paste';
CREATE INDEX IF NOT EXISTS idx_history_source ON history(source);
