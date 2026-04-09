# Refactorització system prompt — 2026-04-09

**Autor**: Claude Opus 4.6 amb supervisió Miquel Amor
**Abast**: server.py, corpus_reader.py, instruction_catalog.py, instruction_filter.py

---

## Resum executiu

Anàlisi profunda dels 12 components del system prompt. Diagnòstic: ~35% soroll (redundància, contradiccions, components inerts). Aplicats canvis amb bisturí: el prompt passa de ~12.900 chars a ~8.200-10.500 chars segons perfil, amb més precisió i zero pèrdua de qualitat (verificat amb generacions comparatives Mistral + GPT).

---

## 1. Canvis al catàleg d'instruccions (instruction_catalog.py)

### 1.1 Gradació MECR a 22 instruccions NIVELL
Abans: pre-A1, A1 i A2 activaven les mateixes 25 instruccions NIVELL (idèntiques).
Ara: cada nivell rep text diferent via `mecr_detail`.

**Instruccions graduades** (22 de 31 NIVELL):
- Ja existien: A-12, A-13, C-01, E-02, G-06
- Noves: A-06, A-08, A-09, A-10, A-11, A-15, A-17, A-20, A-24, A-25, A-26, B-04, B-07, B-08, C-02, C-05, C-06, E-07

**Instruccions binàries** (9, no admeten gradació): A-22, A-23, B-05, B-06, B-09, B-11, B-14, C-08, E-12

**Resultat mesurable**:
| MECR | Instruccions actives | To del text |
|------|---------------------|-------------|
| pre-A1 | 50 | "SEMPRE/ZERO/NOMÉS" — restricció màxima |
| A1 | 50 | "obligatori/mai" — estricte |
| A2 | 50 | "preferent/permet si..." — flexible amb condicions |
| B1 | 42 | "per defecte/permet" — obert |
| B2 | 26 | Gairebé sense restriccions |
| C1 | 20 | Nou, per altes capacitats |

### 1.2 A-15 scaffolding: de SEMPRE → NIVELL ≤B1
Abans s'enviava a B2/C1 on no cal. Ara amb gradació (pre-A1: màxim + exemple visual, B1: lleuger).

### 1.3 Fusió chunking
- **C-04b** absorbit dins C-04 via `_get_intensified_text` (TDAH+baixa_memoria → "2-3 elements")
- **H-04b** absorbit dins H-04 via `_get_intensified_text` (TDAH sever → "2-3 frases")
- Catàleg passa de 97 a 98 instruccions (3 noves - 2 absorbides + ajustos)

### 1.4 Macro ENRIQUIMENT (ordre 0)
H-12, H-14, H-15 separats de la macro PERFIL a una macro pròpia:
`⚠️ ENRIQUIMENT — NO SIMPLIFIQUIS`
Posició 0 = primer bloc del prompt. Garanteix que "no simplifiquis" sona FORT.

### 1.5 Fixes
- **A-14** (connectors explícits): era orfe, no pertanyia a cap macro → afegida a LEXIC
- **G-05**: phantom a macro PERSONALITZACIO (no existia al catàleg) → eliminada de la macro
- **H-02** (TEA): ampliada amb "No generis ironia, sarcasme ni inferències socials"

### 1.6 Instruccions noves
- **A-28**: Evita impersonals (cal, s'ha de) → directe (tu has de, fes). NIVELL ≤A2 amb gradació.
- **A-29**: Evita adverbis -ment → reformula. NIVELL ≤A2 amb gradació.
- **A-30**: Evita anglicismes. PERFIL nouvingut + TDL.

### 1.7 Format prompt (instruction_filter.py)
De prosa concatenada a bullets:
```
Abans: **LÈXIC**: Regla1. Regla2. Regla3. Regla4...
Ara:   **LÈXIC**:
       - Regla1
       - Regla2
       - Regla3
```

---

## 2. Canvis al MECR (server.py, propose_adaptation)

### 2.1 Arquitectura: candidats en lloc d'if/elif/else
Cada perfil amb barrera lingüística proposa un MECR candidat. El més restrictiu guanya. Permet multi-perfil correcte (nouvingut A2 + TDL sever → A1).

### 2.2 Nous mappings
| Perfil | Mapping | Font |
|--------|---------|------|
| TDL | sever→A1, moderat→A2, lleu→B1 | Bishop 2017, mapa_barreres_perfil.md |
| Disc. auditiva LSC | →A1 fix | Català escrit = L2 per sords prelocutius |
| Vulnerabilitat | -1 nivell vs etapa | Retard lector per manca d'estimulació |
| Altes capacitats (sense 2e) | +1 nivell vs etapa | Necessita complexitat, no simplificació |

### 2.3 Perfils SENSE ajust MECR (barrera no lingüística)
TEA, TDAH, dislèxia, disc_visual, TDC, trastorn_emocional → mantenen default d'etapa.

---

## 3. Identitat v2 (corpus_reader.py)

### 3.1 Eliminat
- **universal_rules** (15 regles): duplicaven A-01 a B-10 del catàleg
- Incoherència: universal_rules deia "veu activa SEMPRE" però A-08 al catàleg diu "NIVELL ≤B1"

### 3.2 Afegit
- **TO**: Acadèmic neutre, respectar registre original
- **FIDELITAT**: 2 modes (adaptació vs complements), preparat per futur mode creació
- **SEGURETAT**: privacitat, contingut sensible, no inventar dades

### 3.3 Redissenyat
- "ADAPTA no CREES" → principi de FIDELITAT (els complements SÍ es creen)
- Paraules prohibides: de llista tancada (7 mots) → principi ("MAI parafrasis buides") + exemples

---

## 4. Components ELIMINATS del prompt

### 4.1 RAG-KG (combined_search + mandatory docs)
**Evidència**: generació amb/sense RAG indistingible. RAG recuperava docs irrellevants (M0 filosofia, perfils equivocats). Afegia ~4.300 chars de soroll.
**Decisió**: eliminar del pipeline d'adaptació. Infraestructura Supabase (vectors + KG) es manté per futur ús.

### 4.2 Context educatiu (etapa, curs, àmbit, matèria)
**Motiu**: cap instrucció del catàleg el consulta. L'etapa s'usa al Python per calcular MECR, no necessita ser visible per l'LLM.

### 4.3 Resolució de conflictes
**Motiu**: 100% redundant amb A-26 graduada per MECR (que ja diu "ZERO incisos" a pre-A1, "permet incisos curts" a A2).

### 4.4 Few-shot example
**Motiu**: un sol domini (fotosíntesi), risc de sobreajust. Parking lot per afegir 3-4 dominis.

---

## 5. Components MANTINGUTS

| Component | Motiu |
|-----------|-------|
| Identitat v2 | Immutable, curta, neta |
| Instruccions filtrades (98) | Motor principal |
| Bloc DUA | CRÍTIC: únic senyal que diferencia Accés de Core (58 instruccions idèntiques) |
| Gènere discursiu | Únic component no cobert per instruccions (s'activa si indicat) |
| Creuaments | Semànticament valuosos per multi-perfil (s'activen si 2+ perfils) |
| Persona-audience | Condensat, dóna orientació general |
| Complements sortida | Funcional, indica format per complement |

---

## 6. Impacte en documents existents

Els documents següents contenen referències a components canviats. Es mantenen com a **històric** — aquesta decisió és la referència vigent:

- `docs/decisions/arquitectura_prompt_v2.md` — referencia 95 instruccions, RAG, few-shot, universal_rules
- `docs/decisions/mapa_variables_instruccions.md` — referencia 89 instruccions, C-04b, H-04b
- `docs/decisions/matriu_tracabilitat_instruccions.md` — referencia RAG, few-shot, context educatiu, C-04b, H-04b
- `docs/research/informe_arquitectura_instruccions_v2.md` — referencia RAG-KG, universal_rules, few-shot
- `docs/research/informe_avaluacio_AB_v1.md` — referencia RAG vs Hardcoded

**Xifra actual correcta**: 98 instruccions al catàleg (no 72, 84, 89 ni 95).

---

## 7. Pendent

### Alta prioritat
1. Resoldre 6 contradiccions al catàleg (terme tècnic vs vocabulari freqüent, H-04 doble activació, TEA estructura vs títols pregunta, supressió multi-perfil, connectors vs una idea/frase)
2. Condensar persona-audience
3. Estudiar bloc DUA: crear instruccions condicionals per DUA al catàleg (ara Accés i Core activen les mateixes 58 instruccions)

### Parking lot
- Few-shot: afegir 3-4 dominis (humanitats, matemàtiques, socials)
- Gènere discursiu: més exemples i disambiguation
- Creuaments: convertir prosa a bullets accionables
- Reagrupar macros per acció (Tria paraules / Construeix frases / etc.)
- Mode creació a la identitat
