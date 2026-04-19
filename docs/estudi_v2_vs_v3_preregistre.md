# Pre-registre — Estudi V2 vs V3 del system prompt ATNE

**Data**: 2026-04-19
**Autor**: Miquel Amor (FJE) + assistent IA (Claude Opus 4.7)
**Estat**: pre-registrat abans d'executar cap generació ni avaluació.

## 1. Context

Després de dos smoke tests (36 casos, 2026-04-19 matí; 120 casos, 2026-04-19 tarda), la dada preliminar suggereix que **la variant V2** (identitat + catàleg filtrat per MECR + gènere, **sense** DUA ni persona-audience) produeix adaptacions no pitjors que la variant V3 (baseline complet amb tot).

Volem una validació més rigorosa per decidir si el prompt es pot reduir a V2 en producció (menys tokens, més ràpid, menys cost) sense pèrdua visible de qualitat pedagògica.

## 2. Hipòtesis

- **H0 (nul·la)**: V2 = V3 en qualitat pedagògica mitjana (mesurada per rúbrica 5 dimensions).
- **H1 (alternativa)**: V2 ≠ V3 (test bilateral; permetem que V3 guanyi, V2 guanyi, o hi hagi interacció per perfil/model).

## 3. Variants comparades

| Variant | Composició |
|---|---|
| **V2** | identitat + instruccions filtrades per MECR + bloc gènere |
| **V3** | identitat + instruccions filtrades per MECR + DUA + bloc gènere + persona-audience |

V1 (sense catàleg) **no entra** a aquest estudi — els smoke tests previs ja van mostrar que degrada qualitat.

## 4. Mostra

**Factorial complet**: 5 perfils × 6 textos × 2 variants × 2 models × 3 rèpliques = **360 generacions**.

### 4.1 Perfils (cap repetit de les proves anteriors)

| Id | Perfil | Etapa / MECR |
|---|---|---|
| P1 | Ibrahima Ndiaye — nouvingut L1 wolof, 6 mesos | 2n ESO / A2 |
| P2 | Júlia Roig — TEA sense DI | 3r ESO / B1 |
| P3 | Èric Vives — TDL | 5è primària / B1 |
| P4 | Clara Font — AACC | 5è primària / B2+ |
| P5 | Nil Torras — 2e (TDAH + AACC) | 4t ESO / B2 |

### 4.2 Textos (6 matèries, cap repetit)

| Id | Text | Matèria |
|---|---|---|
| T1 | Teorema de Pitàgores i aplicacions | Matemàtiques |
| T2 | Formació dels Pirineus: tectònica de plaques | Geografia física |
| T3 | Àtoms, enllaços iònics i covalents | Química |
| T4 | Sistema immunitari: línies de defensa | Biologia humana |
| T5 | L'Odissea d'Homer: el viatge d'Ulisses | Literatura clàssica |
| T6 | El dilema del tramvia: utilitarisme vs deontologia | Filosofia / ètica |

Tots ~200-250 paraules, registre pedagògic estàndard.

### 4.3 Models

- **Gemma 3 27B** (via `GEMMA4_API_KEY`, free tier)
- **GPT-4.1-mini** (via `OPENAI_API_KEY`)

### 4.4 Rèpliques

3 per cel·la amb `temperature=0.7` per capturar variabilitat natural del model.

## 5. Avaluació

### 5.1 Jutge LLM

Claude Opus 4.7 (Claude Code, subscripció Max), distribuït en **9 sub-agents paral·lels** amb context net. Cada sub-agent avalua ~20 parells V2/V3 aparellats.

### 5.2 Rúbrica (5 dimensions, 1-5 cadascuna)

| Dim | Criteri |
|---|---|
| **Q** | Qualitat textual: coherència, correcció gramatical, llegibilitat |
| **P** | Adequació al perfil: ajust a les necessitats cognitives/lingüístiques declarades |
| **C** | Rigor curricular: preservació del contingut i terminologia |
| **A** | Adequació a MECR: el text respecta el nivell de sortida declarat |
| **E** | Valor pedagògic: ajuda efectiva a aprendre (andamiatge, claredat, motivació) |

Cada dimensió requereix **justificació breu** (1-2 frases) obligatòria.

### 5.3 Cegament

Per cada parell (text × perfil × model × rèplica), les sortides V2 i V3 es presenten al jutge etiquetades "A" i "B" en ordre aleatoritzat. El jutge no sap quina és V2 ni V3.

### 5.4 Independència del jutge

El jutge (Claude Opus 4.7) és de família diferent dels generadors (Gemma 3 27B i GPT-4.1-mini). No hi ha autoavaluació.

### 5.5 Validació humana complementària (post-pilot)

Després del pilot, Miquel farà validació cega de 30 parells aleatoris via interfície HTML local. No entra al veredicte primari d'aquest estudi però servirà per comparar concordança humà↔jutge LLM.

## 6. Pla d'anàlisi estadística

### 6.1 Test primari

**Wilcoxon signed-rank** (test no-paramètric per parells) sobre la diferència V3-V2 per cada dimensió de la rúbrica.

### 6.2 Correcció per múltiples comparacions

**Bonferroni**: α' = 0.05 / (5 dimensions × 5 perfils × 2 models) = 0.05 / 50 = **0.001**.

### 6.3 Mida d'efecte

**Cohen's d** per cada comparació:
- d < 0.2 → trivial
- 0.2 ≤ d < 0.5 → petit
- 0.5 ≤ d < 0.8 → moderat
- d ≥ 0.8 → gran

### 6.4 Anàlisi subgrup

Estratificació per:
- Perfil extrem (P1 nouvingut A2, P4 AACC primària) vs intermedi (P2 TEA, P3 TDL, P5 2e)
- Model generador (Gemma vs GPT)
- Interacció model × variant (ANOVA de rangs)

## 7. Criteri de decisió

**V2 s'adopta com a prompt de producció si**:

1. Wilcoxon **no significatiu** (p > 0.001) en ≥ 80% dels subgrups (perfil × model × dimensió), **AND**
2. Mediana de Cohen's d ≤ 0.2 (trivial) en cada dimensió, **AND**
3. Cap regressió categòrica a perfils extrems (definida com a Cohen's d > 0.5 a favor de V3 en alguna dimensió).

**V3 es manté com a prompt de producció si**:

- Wilcoxon significatiu a favor de V3 en ≥ 50% dels subgrups, **OR**
- Alguna regressió categòrica a favor de V3 (Cohen's d > 0.5) en perfils crítics (P1, P4).

**Resultat intermedi (sense canvi actual però amb modificació parcial)**:

- Wilcoxon no significatiu global però efecte a favor de V3 concentrat en un subgrup específic → proposar V3 condicional a aquell subgrup i V2 per a la resta.

## 8. Riscos i limitacions acceptades

- **Sol català**: no generalitzable a altres llengües.
- **5 perfils, 6 textos**: cobertura representativa però no exhaustiva.
- **2 models**: Gemma i GPT són diferents però no cobreixen Claude, Gemini Pro, etc.
- **Rúbrica Likert**: el jutge LLM pot inflar puntuacions (efecte conegut amb GPT-4o; menys documentat amb Opus 4.7 però possible).
- **Validació humana limitada**: 30 parells és mostra petita per a test humà-jutge LLM.

## 9. Canvis post-registre

Si es necessita canviar qualsevol element d'aquest pre-registre després d'executar (p.ex. afegir una dimensió, excloure casos amb errors), el canvi es documentarà explícitament a l'informe final amb justificació.

## 10. Fitxers de sortida compromesos

- `docs/estudi_v2_vs_v3_preregistre.md` (aquest document)
- `tests/rigor_v2_v3_generacio.py` (script Fase A)
- `tests/rigor_v2_v3_dades.jsonl` (360 generacions brutes)
- `tests/rigor_v2_v3_avaluacions.jsonl` (360 avaluacions del jutge LLM)
- `tests/rigor_v2_v3_humana.jsonl` (30 avaluacions humanes cegues, post-pilot)
- `docs/estudi_v2_vs_v3_informe.md` (informe final amb estadística)
- `tests/humana_blind_eval.html` (interfície validació humana)

## 11. Temps i cost estimats

| Fase | Temps | Cost |
|---|---|---|
| Fase A (generació 360) | 60-90 min | ~$0.25 API Gemma + GPT |
| Fase B (avaluació 9 agents Opus) | 20-40 min | quota Max (0 € addicional) |
| Fase C (agregació estadística) | <5 min | 0 € |
| Fase D humana post-pilot | 90 min humans | 0 € |
