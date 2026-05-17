# Bootstrap Fase 0 — Benchmark V2 vs V3

**Data**: 2026-05-17 (sessió Claude Opus 4.7 + Miquel)
**Estat**: completat per a benchmark Fase 0 (180 adaptacions, 3 variants × 3 models × 4 instruments × 5)

---

## 1. Què hi ha aquí

Aquesta carpeta conté els **8 fitxers M\*.md** per al benchmark Fase 0 del consens F (vegeu `mineriaRAG/docs/sintesi_F_skills_marc_v1_3_delta.md`):

```
_bootstrap_fase0/
├── README.md                        (aquest fitxer)
├── V2_noticia/M3_instrument-escriure-noticia.md
├── V2_opinio/M3_instrument-escriure-opinio.md
├── V2_glossari/M3_instrument-generar-glossari.md
├── V2_preguntes/M3_instrument-generar-preguntes-comprensio.md
├── V3_noticia/M3_instrument-escriure-noticia.md
├── V3_opinio/M3_instrument-escriure-opinio.md
├── V3_glossari/M3_instrument-generar-glossari.md
└── V3_preguntes/M3_instrument-generar-preguntes-comprensio.md
```

**V1 (status quo)** no és aquí — són els SKILL.md actuals a `corpus/external/corpusFJE/skills/`.

---

## 2. Variants

| Variant | Format de "## Modulació per nivell" | Caracterització |
|---|---|---|
| **V1 (status quo)** | SKILL.md compacte (al submodule) | Format actual agentskills.io |
| **V2 (descriptiu)** | Paràgrafs en prosa, un per nivell MECR | M\*.md amb 3 capes complete sense rúbrica |
| **V3 (rúbrica gradada)** | Taula seqüencial: files = passos, columnes = nivells | Mateixes 3 capes amb rúbrica al nucli operatiu |

---

## 3. Cobertura per instrument

| Instrument | Categoria | Passos rúbrica V3 | Cobertura MECR | Notes |
|---|---|---|---|---|
| Notícia | generes | 9 passos | pre-A1 → C1 (6) | Inclou pre-A1 pictogramada |
| Opinió | generes | 9 passos | A1 → C1 (5) | NO pre-A1 (massa abstracte) |
| Glossari | mediacio + secundària generes | 6 passos | pre-A1 → C1 (6) | Variant bilingüe per a nouvinguts |
| Preguntes de comprensió | mediacio | 9 passos | pre-A1 → C1 (6) | Inclou Pas 8 d'acarament de llengües |

---

## 4. Correccions MALL aplicades

Tots els fitxers (V2 i V3) incorporen aquestes correccions de la validació NotebookLM MALL del 2026-05-17 (78% cites a corpus canònic):

### Correccions específiques per instrument

| # | Correcció | Aplicada a |
|---|---|---|
| 1 | Pas 2 i Pas 4 unificats a A1: "3 de 5W (Qui, Què, On)" | V2-notícia + V3-notícia |
| 2 | Pas 3 A1: admès "frase simple amb verb" (no només nominal) | V2-notícia + V3-notícia |
| 3 | Pas 5 llargada frases gradada: A1=12p / A2=15p / B1=18p / B2=22p | V2-notícia + V3-notícia |
| 4 | Piràmide invertida visible des d'A1 | V2-notícia + V3-notícia |
| 5 | Pas 7 A1 "marques d'opinió"; A2 "adjectius valoratius" | V2-notícia + V3-notícia |
| 6 | Tesi A1 "Crec que..." (no "M'agrada que...") | V2-opinió + V3-opinió |
| 7 | Connectors "tanmateix / no obstant" només a B2 | V2-opinió + V3-opinió |
| 8 | Pas 4 glossari REPLANTEJAT: explicació gradada per CALP (no fixa a A1) | V2-glossari + V3-glossari |

### Afegits MALL transversals

| # | Afegit | Aplicat a |
|---|---|---|
| A | **Descriptors en primera persona** ("He escrit...", "Verifico...") | Totes 8 rúbriques |
| B | **Pas nou: fiabilitat de fonts** | V2/V3-notícia + V2/V3-opinió |
| C | **Pas nou: acarament de llengües** (L1 ↔ català) | V2/V3-preguntes |
| D | Translanguaging/TOLC al frontmatter i text | Totes 8 rúbriques |
| E | Multimodalitat a nivells alts (B2/C1) | Totes 8 rúbriques |

---

## 5. Fitxes pedagògiques pendents (no bloquegen Fase 0)

Cada M\*.md té dues seccions amb `> ⚠️ ESBORRANY` que **no impedeixen el benchmark** però que caldria completar abans del pilot real (post-Fase 0):

1. **Detecció**: senyals docent (7), alumne (5), context (5), anti-senyals (5). Esborrany inicial fet; cal validació pedagògica humana.
2. **Heurístiques narratives** (H1-H5 docent + H6-H8 alumne) amb cas concret en primera persona 80+ paraules. **No automatitzables amb LLM** — cal captura via entrevistes a docents FJE o memòries del projecte ATNE.

---

## 6. Calendari Fase 0 (recordatori)

| Dia | Activitat | Responsable |
|---|---|---|
| Dijous-divendres (22-23 maig) | Miquel revisa pedagògicament els 8 M\*.md d'aquesta carpeta | Miquel (~3h) |
| Dissabte 23 maig | Migració nominal coordinada (corpusFJE + mineriaRAG + ATNE + scriptorium) | mineriaRAG + Miquel supervisa |
| Dilluns 26 maig | Inici Fase 0 | mineriaRAG generació 180 adaptacions |
| 27 maig - 4 juny | Avaluació híbrida Capa 1 (codi) + Capa 2 (3 jutges LLM) | mineriaRAG |
| 5 juny | Calibration humana Miquel (15 adaptacions) | Miquel (~2-3h) |
| 8 juny | Anàlisi ANOVA + reunió de decisió arquitectònica | mineriaRAG + Miquel |

---

## 7. Validació NotebookLM MALL (resum)

| Instrument V3 | Veredicte | Suport documental MALL |
|---|---|---|
| Notícia | (b) Adoptable amb canvis menors | ✅ Fort (nivells comprensió, HCL, 5W) |
| Opinió | (b) Adoptable amb canvis menors | ✅ Fort (inscripció lector, connectors canònics) |
| Glossari | (c) Replantejament Pas 4 — aplicat | ✅ Fort (CALP de Cummins) |
| Preguntes | (a) Adoptable directament | ✅ Fort (plànols cognitius, tres nivells) |

**Suport empíric global**: 78% de cites a corpus MALL canònic (no autoreferent).

---

## 8. Tasques per a tu (Miquel)

Abans del dissabte 23 maig (migració nominal):

1. **Llegir cada M\*.md V3** (≤30 min cada un = 2h totals)
2. **Anotar dubtes pedagògics** o errors detectats
3. **Revisar les seccions de Detecció i Heurístiques** marcades com a esborrany — no és bloquejant per a Fase 0
4. **Revisar el patch corpus-spec v2.4** de mineriaRAG (~30 min)
5. **Començar generació dels 20 textos font** al Pas 2 d'ATNE (no urgent fins al 4 juny)

---

## 9. Reservas honestes sobre les correccions MALL

Algunes correccions tenen **suport MALL canònic directe**; altres són **proposta pedagògica de NotebookLM sense cita literal**. Les principals reserves:

| Correcció | Suport documental | Comentari |
|---|---|---|
| Llargada frases A2/B1/B2 (xifres exactes 15/18/22 paraules) | ⚠️ Parcial | Principi MALL sí (control de llengua); xifres concretes són opinió pedagògica |
| Piràmide invertida visible des d'A1 | ⚠️ Parcial | Coherent amb gènere, sense cita MALL literal |

Si vols validació empírica d'aquestes xifres concretes abans del benchmark, podem fer una segona consulta a NotebookLM amb pregunta específica.

---

## 10. Què passa si Fase 0 dóna negatiu (es revoca F)?

**Es manté** independent del benchmark:
- Marc terminològic KA/Skill/Tool al corpus-spec v2.4
- Migració nominal `tipus: eina` → `tipus: instrument`
- Taxonomia tríplica `generes / mediacio / avaluacio`
- Renombrament filesystem (`skills/generes/`, `skills/mediacio/`)

**Es revoca** (depèn del benchmark):
- M\*.md amb CAPA 1+2 completes per cada instrument
- Rúbrica seqüencial gradada com a estàndard
- `build_skills.py` i autogeneració de SKILL.md

Aquesta carpeta `_bootstrap_fase0/` quedaria com a material per a parking lot post-pilot. No es perd.

---

*Document elaborat el 2026-05-17. Bootstrap Fase 0 a punt per a revisió Miquel + migració nominal dissabte 23 maig.*
