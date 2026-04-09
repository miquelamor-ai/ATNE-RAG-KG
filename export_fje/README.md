# ATNE — Paquet de migració per al stack FJE

Contingut complet per migrar la lògica d'adaptació de textos al stack PHP + OpenAI + Neo4j.

## Estructura

```
export_fje/
├── corpus/                     ← 17 fitxers MD (el contingut pedagògic)
│   ├── M1_alumnat-nouvingut.md
│   ├── M1_alumnat-TEA.md
│   ├── M1_TDAH.md
│   ├── M1_dislexia-dificultats-lectores.md
│   ├── M1_discapacitat-intel·lectual.md
│   ├── M1_discapacitat-visual.md
│   ├── M1_discapacitat-auditiva.md
│   ├── M1_TDL-trastorn-llenguatge.md
│   ├── M1_trastorn-coordinacio-dispraxia.md
│   ├── M1_trastorns-emocionals-conducta.md
│   ├── M1_vulnerabilitat-socioeducativa.md
│   ├── M1_altes-capacitats.md
│   ├── M1_acollida-marc-conceptual.md
│   ├── M1_creuament-variables-dependencies.md
│   ├── M2_DUA-principis-pautes.md
│   ├── M3_lectura-facil-comunicacio-clara.md
│   └── M3_generes-discursius.md
│
├── logica/                     ← La lògica de construcció del prompt (Python → migrar a PHP)
│   ├── instruction_catalog.py      ← Les 88 instruccions amb regles d'activació
│   ├── instruction_filter.py       ← Filtre: perfil + MECR + sub-vars → instruccions actives
│   ├── corpus_reader.py            ← Llegeix blocs dels MD: identitat, DUA, MECR, gèneres, few-shot
│   ├── prompt_builder.py           ← Orquestrador: munta el prompt final en 4 capes
│   └── prompt_blocks_referencia.py ← Versió "tot en un" hardcoded (referència, no per producció)
│
├── docs/                       ← Documentació de disseny
│   ├── arquitectura_prompt_v2.md       ← El plànol: 4 capes, macrodirectives, com encaixen
│   └── mapa_variables_instruccions.md  ← Quines sub-variables activen quines instruccions
│
└── README.md                   ← Aquest fitxer
```

## Com funciona el prompt (resum executiu)

El sistema munta un **system prompt** de 1.000-3.000 paraules en **4 capes**:

### Capa 1: IDENTITAT (fixa)
"Ets ATNE de Jesuïtes Educació, especialista en adaptació de textos educatius..."
- Sempre igual, no canvia mai
- Origen: `corpus_reader.py` → text fix al corpus

### Capa 2: INSTRUCCIONS D'ADAPTACIÓ (variable)
Les regles concretes que l'LLM ha de seguir. Exemple: "Màxim 8 paraules per frase", "Estructura predictible per TEA".
- 88 instruccions possibles al catàleg (`instruction_catalog.py`)
- El filtre (`instruction_filter.py`) selecciona 15-30 segons el cas
- S'agrupen en 6-8 blocs temàtics (LÈXIC, SINTAXI, ESTRUCTURA, COGNITIU, QUALITAT, PERSONALITZACIÓ, PERFIL)
- L'LLM no veu IDs (A-01, H-04...) — només prosa agrupada

**4 criteris d'activació:**
| Criteri | Quantes | Quan s'activen |
|---------|---------|----------------|
| SEMPRE | 12 | Bones pràctiques universals |
| NIVELL | 31 | Depenen del MECR de sortida (pre-A1 a B2) |
| PERFIL | 38 | Depenen de les característiques actives (TEA, TDAH, dislèxia...) |
| COMPLEMENT | 3 | Si el docent activa pictogrames, esquema, mapa... |

**Funcionalitats avançades:**
- Supressió intel·ligent (si dislèxia activa, no enviar A-01 perquè H-08 ja ho cobreix)
- Intensificació per sub-variables (tdah.baixa_memoria_treball → chunking 3 elements en lloc de 5)
- Creuaments entre perfils (nouvingut+TEA: instruccions específiques del corpus)

### Capa 3: CONTEXT (variable, no són ordres)
Informació perquè l'LLM entengui el cas:
- **Context educatiu**: etapa, curs, àmbit, matèria
- **Persona-audience**: narrativa natural de l'alumne ("Alumne nouvingut arabòfon, CALP inicial, TEA nivell 2...")
- **Coneixement pedagògic (RAG)**: 8-12 fragments del corpus FJE cercats per similitud vectorial + Knowledge Graph
- **Complements activats**: glossari, esquema, preguntes...

### Capa 4: FORMAT DE SORTIDA (variable)
Indica exactament quines seccions ha de generar l'LLM:
- `## Text adaptat` (sempre)
- `## Glossari` (si activat — taula bilingüe amb traducció a L1)
- `## Esquema visual` (si activat)
- `## Preguntes de comprensió` (si activat — 3 nivells graduats)
- `## Argumentació pedagògica` (sempre)
- `## Notes d'auditoria` (sempre — taula comparativa)

## Com migrar a PHP

### 1. El corpus (corpus/)
Són fitxers markdown amb seccions estàndard. `corpus_reader.py` els llegeix i n'extreu blocs per secció. A PHP cal replicar la mateixa lògica: obrir el fitxer, buscar la secció "6. INSTRUCCIONS D'ADAPTACIÓ TEXTUAL PER A L'LLM", extreure-la.

Per al vector store d'OpenAI: indexar els 17 fitxers tal com estan.
Per a Neo4j: el graf actual té 952 nodes i 2.294 arestes (a Supabase, taules `kg_nodes` i `kg_edges`). Cal exportar i importar a Neo4j.

### 2. Les instruccions (logica/)
`instruction_catalog.py` és un diccionari Python amb 88 entrades. Cada entrada té:
- `text`: la instrucció en prosa
- `activation`: SEMPRE / NIVELL / PERFIL / COMPLEMENT
- `profiles`: llista de perfils que l'activen (si PERFIL)
- `mecr_levels`: llista de nivells MECR (si NIVELL)
- `suppress_if`: perfils que la desactiven
- `subvar_conditions`: condicions de sub-variables

`instruction_filter.py` implementa la lògica de selecció. La funció clau és `get_instructions(profile, params)` → retorna la llista filtrada.

A PHP: convertir el diccionari a un array associatiu o JSON, i reimplementar `get_instructions()`.

### 3. El prompt builder (logica/prompt_builder.py)
Conté dues funcions clau:
- `build_persona_audience()`: genera la narrativa de l'alumne a partir de les sub-variables
- `build_system_prompt()`: orquestra les 4 capes

A PHP: reimplementar amb la mateixa estructura. El text generat és idèntic independentment del llenguatge de programació.

## Resultats d'avaluació (6 models)

200 casos × 6 models, avaluats amb rúbrica de 8 criteris per 4 jutges independents:

| Model | Puntuació mitjana |
|-------|-------------------|
| GPT-4o-mini | 4.44 / 5 |
| Gemma 4 31B | 4.23 / 5 |
| Mistral Small | 4.19 / 5 |
| Gemini 2.5 Flash | 3.93 / 5 |

GPT-4o-mini és el model recomanat si FJE té clau OpenAI institucional.

## Perfils d'alumnat suportats (13)

Nouvingut (6 sub-vars) · TEA (2) · TDAH (4) · Dislèxia (4) · TDL (8) · DI (1) · Altes capacitats (1) · Disc. visual · Disc. auditiva · Disc. motora/TDC · Vulnerabilitat · Trastorn emocional · 2e (doble excepcionalitat, detecció automàtica)

36 sub-variables en total. Combinables entre ells.
