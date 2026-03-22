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
- **LLM**: Gemini 2.5-flash (google.genai SDK, capa gratuita)
- **Dades**: Supabase (PostgreSQL + pgvector)
  - Vector store: taula `rag_fje` (1.443 chunks, embeddings 768d)
  - Knowledge Graph: taules `kg_nodes` (952) + `kg_edges` (2.294)
  - Funcio SQL: `match_rag_fje` (cerca vectorial) + `kg_expand` (graf)
- **NO usar**: React, Vue, Next.js, Tailwind, Prisma, TypeScript

## Credencials (fitxer .env, NO al git)
```
GEMINI_API_KEY=...
SUPABASE_URL=https://qlftykfqjwaxucoeqcjv.supabase.co
SUPABASE_ANON_KEY=...
```

## Arquitectura de cerca (RAG + KG)
La cerca combina dos senyals:
1. **Vector search**: embedding de la query → match_rag_fje (Supabase)
2. **KG expansion**: conceptes de la query → kg_expand (1-2 salts)
3. **Fusio**: bonus per senyal dual (vector + KG > nomes un)

Documents obligatoris per regles de negoci (sempre inclosos segons context):
- Adaptar text → M3_lectura-facil-comunicacio-clara.md + M2_DUA-principis-pautes.md
- Nouvingut → M1_alumnat-nouvingut.md + M1_acollida-marc-conceptual.md
- Avaluacio → M6_avaluacio-formativa-formadora.md

## Pipeline de l'assistent
1. **Input**: docent puja o enganxa un text
2. **Configuracio** (parametres, NO xat obert):
   - Perfil alumnat: nouvingut | NESE | altes capacitats | generic
   - Etapa: infantil | primaria | ESO | batxillerat | FP
   - Nivell linguistic (MECR): pre-A1 | A1 | A2 | B1 | B2
   - Tipus adaptacio: lectura facil | multinivell (Acces/Core/Enriquiment) | ambdos
   - Materia: cientific | humanistic | linguistic
   - Ajuts: definicions | exemples | esquema | pictogrames
3. **Adaptacio**: Gemini transforma el text usant RAG+KG com a context
4. **Auditoria**: taula comparativa original vs adaptat
5. **Producte**: visualitzacio + descarrega (PDF/DOCX/TXT)

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
- .env exclosa del git
