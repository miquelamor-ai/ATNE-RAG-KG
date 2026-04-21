# ATNE — Adaptador de Textos a Necessitats Educatives

## Projecte
Assistent IA per adaptar textos educatius a les diverses necessitats de l'alumnat
(nouvinguts, NESE, DUA, altes capacitats). Jesuites Educacio (FJE).

## Usuari
Miquel Amor — expert en pedagogia, NO programador. Comunica't SEMPRE en catala.
Explicacions clares i practiques.

## Stack tecnic
- **Backend**: Python 3.12 + FastAPI + uvicorn
- **Frontend**: HTML + JavaScript pur + CSS (ZERO frameworks)
- **LLM**: Gemma 4 31B + rotacio GPT-4o / GPT-4.1-mini / Gemma 3 27B (decidit 2026-04-16)
  - Gemini 2.5-flash disponible al codi pero no es el model per defecte des de 2026-04-12
- **Auth**: Supabase Auth + Google OAuth restringit a `@fje.edu` (desplegat 2026-04-20)
- **Dades**: Supabase (PostgreSQL)
  - Perfils docents: `atne_docents`, `atne_custom_profiles`, `atne_drafts`
  - Historial i analytics: `history`, `pilot_events`, `system_config`
  - Vector store i KG: `rag_fje`, `kg_nodes`, `kg_edges` — **INFRAESTRUCTURA DESACTIVADA** (veure seccio seguent)
- **NO usar**: React, Vue, Next.js, Tailwind, Prisma, TypeScript

## Credencials (fitxer .env, NO al git)
```
GEMINI_API_KEY=...
SUPABASE_URL=https://qlftykfqjwaxucoeqcjv.supabase.co
SUPABASE_ANON_KEY=...
```

## Arquitectura del prompt (RAG-KG DESACTIVAT — 2026-04-09)

**IMPORTANT**: ATNE NO usa RAG-KG dinamic. L'auditoria 2026-04-21 confirma
que `vector_search()`, `kg_expand_concept()`, `combined_search()` son dead
code: zero crides reals. El prompt s'omple via:

1. **`instruction_catalog.py` (Python hardcoded)** — 107 instruccions amb
   text literal. Filtre via `instruction_filter.py` segons:
   - `SEMPRE` (nucli, sempre actiu)
   - `NIVELL` (segons MECR)
   - `PERFIL` (segons condicions: tdah, dislexia, nouvingut, etc.)
   - `COMPLEMENT` (segons complements triats)
2. **`corpus_reader.py` (legeix MD)** — SOMENTS aquests blocs:
   - `get_identity()` — identitat fixa de l'assistent
   - `get_dua_block(dua)` — blocs DUA Acces/Core/Enriquiment
   - `get_genre_block(genre)` — gèneres discursius (22)
   - `get_crossing_blocks(active_profiles)` — creuaments entre condicions
   - `get_fewshot_example(mecr)` — exemple abans/despres
   - **NO usats**: `get_profile_block()`, `get_mecr_block()` — funcions orfes.
3. **Corpus MD local** (`ATNE/corpus/`) — 18 fitxers locals, font duplicada.
   Font de veritat real: `github.com/miquelamor-ai/corpusFJE` (93 fitxers).
   Fase D pendent post-pilot: substituir corpus local per submodule del corpusFJE.

**Implicacio practica**: editar un M1_*.md NO canvia el prompt per a perfils
(TDAH, dislexia, etc.) — les instruccions de perfil venen del Python hardcoded.
Si edites M1, ha de ser tambe a `instruction_catalog.py` per tenir efecte.

## Pipeline de l'assistent
1. **Pas 1**: docent tria perfil (persona o grup) amb curs + MECR + condicions
2. **Pas 2**: enganxa/puja/genera text + configura materia, genere, complements
3. **Pas 3**: LLM adapta amb streaming SSE, mostra complements, permet refinar
4. **Export**: PDF client-side (html2pdf.js), copia al porta-papers, impressio

Tot el flux passa per `/api/adapt` (SSE). Auth obligatori via Supabase JWT
amb email `@fje.edu`.

## Regles de Lectura Facil (LF)
- Puntuacio: nomes punts i dos punts (no ; ni ...)
- Veu activa sempre, subjecte explicit
- Vocabulari frequent, termes tecnics en negreta amb explicacio
- Una idea per frase
- Imatges/pictogrames a l'esquerra del text
- Dates completes, no numeros romans

## Nivells DUA (multinivell)
- **Acces**: LF extrema + suport visual + definicions integrades
- **Core**: adaptacio estandard mantenint rigor curricular
- **Enriquiment**: profunditzacio + pensament critic + connexio interdisciplinar

## Memoria triadica (context per a l'LLM)
1. **Alumne**: origen, L1, MECR, alfabetitzacio llatina, necessitats
2. **Classe**: configuracio multinivell, estil suport preferit
3. **Materia**: assignatura, estil redaccio, termes intocables

## Repo anterior (arxivat)
El prototip anterior esta a `.gemini/antigravity/scratch/ATNE/app/`
amb repo GitHub `miquelamor-ai/ATNE`. Usava Next.js + Prisma (descartat).
Les especificacions (SYSTEM_PROMPT.md, AAU_SPECIFICATION.md, CONFIG_VARIABLES.md)
son a `[GEMINI] ATNE_sources/` i son referencia valida.

## Projecte germa
El pipeline de mineria/indexacio esta a `C:\Users\miquel.amor\Documents\mineriaRAG\`
(repo `miquelamor-ai/mineriaRAG`). Alli es gestiona:
- Scraping + classificacio + ingesta del corpus
- Indexacio al vector store (index_rag.py)
- Extraccio del KG (build_kg.py)

## Moduls del corpus (M0-M9)
- M0: Identitat i Missio
- M1: Subjecte (perfils alumnat)
- M2: Metode (metodologies)
- M3: Llengua
- M4: Contingut Curricular
- M5: Tecnopedagogia
- M6: Avaluacio
- M7: Entorn, Convivencia i Familia
- M8: Governanca i Seguretat
- M9: Marc Legal i Normatiu

## Convencions de codi
- Python 3.12, FastAPI + uvicorn, google-genai, python-dotenv, requests
- Encoding UTF-8 sempre
- SSE per streaming de progres (no websockets)