# Interpretacio estadistica — Avaluacio multi_v2 RAG-v2

**Data**: 5 abril 2026
**Dades**: 4.200 avaluacions externes (sense self-eval)
**Eina**: `tests/stats_analysis.py` (scipy 1.17)

---

## 1. Mitjanes amb intervals de confiança 95%

Agregacio per generador (tots els jutges externs):

| Generador | N | Mitjana | IC95% |
|-----------|---|---------|-------|
| **gpt** | 538 | **4.443** | [4.401, 4.485] |
| **gemma4** | 287 | **4.232** | [4.166, 4.297] |
| **mistral** | 198 | **4.192** | [4.153, 4.231] |
| gemini | 341 | 3.932 | [3.820, 4.044] |

**Interpretacio**: els intervals de confiança no se superposen entre:
- GPT i Gemma 4 (diferencia real)
- GPT i Mistral (diferencia real)
- GPT i Gemini (diferencia real)

Els IC de **Gemma 4 i Mistral si se superposen** lleugerament ([4.166, 4.297] vs [4.153, 4.231]), cosa que confirma l'empat tecnic.

---

## 2. Kruskal-Wallis: diferencies globals

**H = 81.28, p = 1.63e-17** (p < 0.001)

**CONCLUSIO: Les diferencies entre generadors son ALTAMENT significatives.** No son soroll aleatori.

---

## 3. Comparacions parellades (Mann-Whitney + Bonferroni)

Alpha corregit: 0.0083 (6 parelles, alpha = 0.05 / 6)

| Parella | p-value | Significatiu? |
|---------|---------|---------------|
| **GPT vs Gemini** | 2.60e-13 | ⭐⭐ SI (altament) |
| **GPT vs Gemma 4** | 2.47e-08 | ⭐⭐ SI (altament) |
| **GPT vs Mistral** | 1.37e-11 | ⭐⭐ SI (altament) |
| Gemma 4 vs Mistral | 1.37e-02 | ⭐ SI (sense Bonferroni) |
| Gemini vs Gemma 4 | 6.06e-02 | **NO** |
| Gemini vs Mistral | 9.50e-01 | **NO** |

### Troballes importants

1. **GPT es significativament superior a tots els altres** (p < 0.0083 en totes les comparacions)
2. **Gemini i Mistral son estadisticament EQUIVALENTS** (p = 0.95)
3. **Gemini i Gemma 4 son estadisticament equivalents** (p = 0.06, per sobre alpha Bonferroni)
4. **Gemma 4 i Mistral**: diferencia marginal (p = 0.014), **NO resisteix Bonferroni**

### Conclusio revisada

El rànquing real, amb rigor estadistic, es:
- **Grup 1**: GPT (clarament millor)
- **Grup 2**: Gemma 4, Mistral, Gemini (empat tecnic — diferencies no significatives amb Bonferroni)

**La diferencia Gemma 4 vs Mistral que reportavem (0.04 punts) NO es estadisticament significativa.** Son equivalents.

---

## 4. Cronbach's alpha (consistencia interna rubrica v2)

**Alpha = 0.886** (N = 4.200, K = 8 items)

**CONCLUSIO: Consistencia interna BONA (α >= 0.8).** La rubrica v2 es fiable: els 8 criteris mesuren el mateix constructe subjacent.

### Alpha si eliminem cada item:

| Item | Alpha si eliminem |
|------|-------------------|
| A1 Coherencia | 0.867 |
| A2 Gramatica | 0.882 |
| A3 Llegibilitat | 0.860 |
| **B1 Fidelitat** | **0.899** ← eliminar milloraria |
| B2 Perfil | 0.859 |
| B3 Scaffolding | 0.877 |
| B4 Cultura | 0.873 |
| C1 Aprenentatge | 0.853 |

**Observacio**: eliminant B1 (Fidelitat curricular) l'alpha pujaria a 0.899. Aixo suggereix que **B1 mesura quelcom diferent** de la resta de criteris. Te sentit: la fidelitat al contingut original es conceptualment independent de la coherencia textual o el perfil de l'alumne.

**Recomanacio per rubrica v3**: considerar B1 com una dimensio independent o separada de la resta.

---

## 5. Correlacio longitud ↔ puntuacio (biaix de verbositat)

| Jutge | N | Spearman r | p | Biaix |
|-------|---|-----------|---|-------|
| Gemini | 200 | 0.066 | 0.352 | **Cap** |
| GPT-4o-mini | 787 | -0.009 | 0.794 | **Cap** |
| Mistral | 377 | **0.296** | 4.73e-09 | **Petit** |

### Interpretacio

- **GPT-4o-mini i Gemini jutgen amb objectivitat**: no hi ha correlacio entre longitud i puntuacio
- **Mistral te un biaix petit-moderat** cap a textos mes llargs (r = 0.30)

**Implicacio**: Quan Mistral jutja, tendeix a puntuar mes alt els textos mes llargs. Aixo podria explicar per que:
- Mistral puntua Gemma 4 = 4.66 (Gemma genera 552 paraules/cas)
- Mistral puntua Mistral = 4.73 (520 paraules/cas)
- Mistral puntua GPT = 4.61 (323 paraules/cas)

Tot i el biaix, GPT guanya igualment → la seva superioritat es real, no artefacte.

### Recomanacio

Usar **GPT-4o-mini** com a jutge de referencia en futurs benchmarks. Gemini tambe es fiable (sense biaix de verbositat).

---

## 6. Analisi factorial (validacio estructural de la rubrica)

### Resultats

- **PC1 captura el 58.2% de la variança**
- PC2 captura el 15.2% addicional (total 73.4%)
- **Nomes 2 components tenen eigen > 1** (Kaiser)

### Loadings (com carreguen els items a cada component)

| Item | PC1 | PC2 | Interpretacio |
|------|-----|-----|---------------|
| A1 Coherencia | -0.78 | 0.28 | PC1 |
| A2 Gramatica | -0.63 | 0.48 | PC1 + PC2 |
| A3 Llegibilitat | -0.86 | -0.24 | PC1 |
| B1 Fidelitat | -0.47 | **0.74** | **PC2** |
| B2 Perfil | -0.86 | -0.30 | PC1 |
| B3 Scaffolding | -0.76 | -0.43 | PC1 |
| B4 Cultura | -0.73 | 0.10 | PC1 |
| C1 Aprenentatge | -0.91 | -0.16 | PC1 |

### Interpretacio critica

**La rubrica v2 NO te les 3 dimensions (A, B, C) que pretenem.** En realitat, te **2 dimensions latents**:

1. **Factor 1 (58% variança): Qualitat pedagogica general** (tot menys B1)
   - Inclou: A1 A2 A3 B2 B3 B4 C1
   - Els criteris tendeixen a pujar o baixar junts
2. **Factor 2 (15% variança): Fidelitat al contingut curricular** (B1 sol)
   - Mesura una cosa diferent: si el text es ajusta al contingut original

### Implicacions

- Les "dimensions" A/B/C que vas postular **no estan empiricament validades**
- La rubrica v2 mesura 2 coses: **qualitat pedagogica** + **fidelitat curricular**
- Per al proper benchmark, **simplificar a 2 dimensions** seria mes honest
- O be, **refer la rubrica v3** amb items mes independents per a cada dimensio

---

## Conclusions generals

### Que es sosté estadisticament
✅ **GPT es significativament superior als altres** (p < 0.001 en totes les comparacions amb Bonferroni)
✅ **La rubrica v2 te bona consistencia interna** (alpha = 0.886)
✅ **Gemini i GPT no tenen biaix de verbositat**
✅ **Les diferencies globals entre generadors son reals** (Kruskal-Wallis p < 0.001)

### Que s'ha de revisar
⚠️ **Gemma 4, Mistral i Gemini son estadisticament equivalents** (contrari al rànquing ingenu)
⚠️ **Mistral te biaix petit de verbositat** com a jutge (r = 0.30)
⚠️ **La rubrica v2 no te 3 dimensions sino 2** (qualitat + fidelitat)
⚠️ **B1 (Fidelitat) es conceptualment independent** dels altres criteris

### Que cal fer per publicacio academica
- Encara falta **validacio humana** (gold standard)
- Encara falta **test-retest reliability**
- Rubrica v3 reformulada amb 2 dimensions empiriques

---

## Rànquing revisat (amb rigor estadistic)

| Grup | Models | Qualitat | Nota |
|------|--------|----------|------|
| **1r** | **GPT-4o-mini** | 4.44 | Significativament superior |
| **2n** | **Gemma 4, Mistral, Gemini** | 3.93-4.23 | Empat tecnic (diferencies no sig. amb Bonferroni) |
| **3r** | **Sonnet** | 2.04 | Bug RAG-v2, pendent regenerar |

**Per al pilot FJE**: oferir al docent triar entre **Gemma 4 / Mistral / Gemini** (tots free tier, tots al mateix nivell estadistic).
