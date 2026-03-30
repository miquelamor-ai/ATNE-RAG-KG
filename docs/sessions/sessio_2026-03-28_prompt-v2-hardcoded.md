# Sessio 2026-03-28 — Prompt v2 Hardcoded

## Context
Continuacio de la recerca prompt v2 (sessio 2026-03-27 nit).
Decisio presa: crear dues branques per comparar hardcoded vs RAG-KG.
Avui comencem la branca `prompt-v2-hardcoded`.

## Decisio clau
Les instruccions d'adaptacio viuen al codi Python (no al corpus RAG).
El RAG aporta context pedagogic complementari, no instruccions.

## Que s'ha fet

### 1. Creacio branca git
```
git checkout -b prompt-v2-hardcoded  (des de main, commit 5624f62)
```

### 2. Nou fitxer: prompt_blocks.py
Tots els blocs constants de l'arquitectura 4 capes:

| Bloc | Descripcio | Quantitat |
|------|-----------|-----------|
| IDENTITY_BLOCK | Rol, objectiu, restriccions absolutes | 1 fix |
| UNIVERSAL_RULES_BLOCK | 15 regles que SEMPRE s'apliquen (lexic, sintaxi, estructura, cohesio, qualitat) | 1 fix |
| MECR_BLOCKS | 1 bloc per nivell (pre-A1, A1, A2, B1, B2) — s'envia NOMES el de sortida | 5 (1 seleccionat) |
| DUA_BLOCKS | Acces / Core / Enriquiment | 3 (1 seleccionat) |
| GENRE_BLOCKS | Explicacio, narracio, instruccio, argumentacio | 4 (0-1 seleccionat) |
| PROFILE_BLOCKS | 12 perfils (nouvingut, TEA, TDAH, dislexia, TDL, DI, visual, auditiva, AC, 2e, vulnerabilitat, emocional) | 12 (0-N seleccionats) |
| CROSSING_BLOCKS | 8 creuaments entre perfils/condicions | 8 (0-N seleccionats) |
| FEWSHOT_EXAMPLES | 1 mini-exemple per nivell MECR | 5 (1 seleccionat) |
| COGNITIVE_LOAD_BLOCK | Regles de carrega cognitiva per nivell | 3 (1 seleccionat) |
| CONFLICT_RESOLUTION_BLOCK | Jerarquia MECR > DUA > LF per resoldre conflictes | 1 (condicional) |

### 3. Refactoritzacio server.py
La funcio `build_system_prompt()` passa de monolitica (~30 instruccions sempre) a 4 capes condicionals:

**Capa 1 — Identitat (fixa)**
Rol ATNE, objectiu, restriccions absolutes, paraules prohibides.

**Capa 2 — Instruccions universals (fixa)**
15 regles que SEMPRE s'apliquen: lexic (4), sintaxi (3), estructura (3), cohesio Halliday (3), qualitat Vygotsky (2).

**Capa 3 — Instruccions condicionals (variable)**
Seleccionades pel codi Python segons el cas:
- MECR: nomes 1 dels 5 nivells (abans s'enviaven tots 5)
- DUA: Acces/Core/Enriquiment
- Genere discursiu: si indicat
- Perfils: nomes els actius
- Creuaments: nomes si 2+ perfils coincideixen
- Carrega cognitiva: segons MECR
- Resolucio conflictes: nomes si nivell baix o DUA Acces
- Few-shot: 1 exemple per MECR

**Capa 4 — Context (variable)**
- Context educatiu (etapa, curs, materia)
- Persona-audience: narrativa concreta de l'alumne (nou! abans era abstracte)
- RAG pedagogic del corpus FJE
- Format de sortida (complements activats)

### 4. Noves funcions afegides a server.py
- `build_persona_audience()` — genera narrativa concreta ("alumne de ESO nouvingut, L1 arab, 3 mesos a Catalunya...")
- `build_output_format()` — format de sortida condicional segons complements
- `post_process_adaptation()` — verificacio post-LLM amb Python:
  - Longitud de frases (max per MECR)
  - Paraules prohibides ("cosa", "coses"...)
  - Presencia d'encapcalaments
  - Presencia de negretes
  - Metriques basiques (paraules, frases, termes en negreta)
- `_get_active_profiles()`, `_detect_crossing_signals()`, `_get_cognitive_load_level()` — funcions auxiliars

### 5. Resultats mesurats

**Mida del prompt:**
| Cas | Abans (v1) | Despres (v2) | Reduccio |
|-----|-----------|-------------|----------|
| B2 generic, sense complements | ~2500 tokens | ~820 tokens | -67% |
| A1 nouvingut+dislexia, DUA Acces, glossari | ~2500 tokens | ~1340 tokens | -46% |

**Prova real amb Gemini 2.5 Flash:**
- Text: fotosintesi (ciencies naturals)
- Perfil: nouvingut maroqui, A1, DUA Acces, glossari + pictogrames
- Resultat: excel-lent
  - Frases curtes (5-8 paraules)
  - Termes tecnics en negreta amb definicio
  - Pictogrames integrats
  - Glossari bilingue catala-arab amb alfabet original
  - Zero meta-text, zero "coses"
  - Comenca directe amb ## Text adaptat

### 6. Commit
```
5cd92ac feat: prompt v2 hardcoded — arquitectura 4 capes condicional
```
Branca: `prompt-v2-hardcoded` (NO pushed)

## Millores respecte v1 (resum)

| Millora | Referencia arquitectura |
|---------|----------------------|
| Enviar NOMES 1 nivell MECR (no tots 5) | Fase 0.1 |
| Creuaments condicionals (no tots 8 sempre) | Fase 0.2 |
| Scaffolding decreixent Vygotsky | Fase 0.3 |
| Principi coherencia Mayer explicit | Fase 0.4 |
| Desnominalitzacio Halliday | Fase 0.5 |
| To per nivell MECR | Fase 0.6 |
| Blocs condicionals per perfil | Fase 1.2 |
| Few-shot examples per MECR | Fase 1.4 |
| Persona-audience narratiu | Fase 1.5 |
| Glossari previ per A1/A2 | Fase 1.6 |
| Post-processament Python | Fase 1.7 |
| Blocs dislexia Dehaene/Wolf | Fase 1.8 |
| Resolucio conflictes DUA-MECR-LF | Seccio 6.6 |

## Pendent (proper pas)
- [ ] Crear branca `prompt-v2-rag` per comparar
- [ ] Proves amb mes perfils (TEA, TDAH, altes capacitats)
- [ ] Proves amb mes textos (narracio, instruccio, argumentacio)
- [ ] Deteccio automatica de genere discursiu
- [ ] Push de la branca (pactat amb Miquel)
