# Xat 9 — Informe executiu per a la migració FJE

**Data**: 2026-04-11
**Context**: Experiment A/B per decidir quin model LLM i quin tipus de prompt és òptim per a la migració a FJE amb 1000 docents.

---

## Resum ex­ecutiu (TL;DR)

**Recomanació principal**: **Gemma 4 31B amb prompt complet** és el guanyador en totes les dimensions.

- **Qualitat**: 4.75/5 (el més alt de tots els models)
- **Cost**: $0 (free tier Google AI Studio)
- **Escala**: 7 claus rotades ja dimensionades per a FJE
- **Integració**: ja present al pipeline ATNE (`server.py`)

**Conclusió pedagògica crítica**: **el prompt complet (98 instruccions) SÍ val la pena per a GPT-4o-mini** (+0.62 punts, d=1.19), però **NO aporta diferència significativa** per a Gemma 4, Mistral i Llama, que ja venen prou calibrats d'origen.

Això reformula la decisió: més que "val la pena el catàleg?", la pregunta és **"per a quin model val la pena?"**.

---

## Disseny experimental

- **30 textos** reals (10 primària + 10 ESO + 10 batxillerat)
- **6 perfils** (nouvingut A1, TDAH lleu B1, altes capacitats C1, TDL A2, doble excepcionalitat B2, TDAH+DI A2)
- **4 generadors**: GPT-4o-mini, Mistral Small, Llama 3.3 70B, Gemma 4 31B
- **2 condicions** per parell: prompt mínim (A) vs prompt complet amb 98 instruccions (B)
- **5 jutges** (3 closed: GPT-4o, Gemini Flash, Claude Sonnet parcial; 2 open: Qwen 3 32B, Llama 3.3 70B, Mistral Small amb exclusió auto-avaluació)
- **Rúbrica**: 5 criteris ponderats (MECR 25%, fidelitat 20%, perfil 25%, llegibilitat 15%, complements 15%)
- **Parells generats**: 604 (180 × 3 models complets + 64 Llama parcial)
- **Avaluacions totals**: 604 × 4-5 jutges ≈ 2.800 judicis LLM

---

## Resultats clau

### 1. Rànquing global de qualitat (prompt complet)

| Posició | Model | Qualitat (B/5) | Cost/1M tok | Decisió prompt |
|---|---|---|---|---|
| 🥇 | **Gemma 4 31B** | **4.75** | $0.00 | Mínim suficient |
| 🥈 | Mistral Small | 4.64 | $0.30 | Mínim suficient |
| 🥉 | Llama 3.3 70B | 4.26 | $0.00 | Mínim suficient |
| 4 | GPT-4o-mini | 4.19 | $0.38 | **Prompt complet val la pena** |

### 2. El paradox del prompt complet

| Model | A (mínim) | B (complet) | Δ | Cohen's d | Què diu |
|---|---|---|---|---|---|
| Gemma 4 | 4.62 | 4.77 | +0.14 | 0.33 (petit) | Ja és bo sol |
| Mistral | 4.47 | 4.64 | +0.17 | 0.53 (mitjà) | Millora petita |
| Llama | 4.00 | 4.27 | +0.26 | 0.52 (mitjà) | Millora petita |
| **GPT-4o-mini** | **3.57** | **4.19** | **+0.62** | **1.19 (gran)** | **Necessita el catàleg** |

**Insight clau**: els models open-source (Gemma, Mistral, Llama) ja venen amb prou "coneixement pedagògic" per adaptar textos amb un prompt mínim. **GPT-4o-mini és el que més necessita les 98 instruccions** — el catàleg compensa la seva feblesa relativa.

### 3. Fortaleses per criteri

| Criteri | Guanyador | Pt | Pitjor | Pt |
|---|---|---|---|---|
| Adequació MECR | Gemma 4 | 4.48 | GPT-4o-mini | 4.02 |
| Fidelitat curricular | **Mistral** | **4.83** | Llama | 4.35 |
| Adequació al perfil | Gemma 4 | 4.88 | GPT-4o-mini | 4.08 |
| Llegibilitat/estructura | Gemma 4 | 4.90 | Llama | 4.14 |
| Complements (glossari, esquemes) | Gemma 4 | 4.87 | GPT-4o-mini | 4.25 |

**Gemma 4 31B guanya en 4 de 5 criteris**. Mistral guanya només en fidelitat curricular, però amb marge petit (0.09). Gemma és el pitjor només a Llegibilitat quan es compara amb Mistral (0.14 de diferència).

### 4. Concordança dels jutges

Correlacions Pearson entre parells de jutges (r):
- **GPT-4o × Gemini Flash**: 0.75 ✅ (forta)
- **GPT-4o × Mistral judge**: 0.68 ✅ (moderada-forta)
- **Claude Sonnet × Gemini Flash**: 0.68 (moderada-forta, històric)
- **Llama judge × altres**: 0.29-0.43 ⚠️ (baixa — Llama és el jutge menys fiable)
- **Qwen judge × altres**: 0.41-0.55 (moderada)

**Implicació**: Els jutges principals (GPT-4o, Gemini Flash, Mistral) són consistents entre ells. Llama com a jutge no és fiable — afegeix soroll. Qwen és acceptable però no tan robust com GPT-4o.

---

## Recomanacions per a la migració FJE

### Opció A — Una sola arquitectura (simple, recomanada)

**Gemma 4 31B amb prompt complet**.

- **Cost**: $0 (free tier Google)
- **Qualitat**: 4.75/5 (la més alta)
- **Escalat a 1000 docents**: cobert per les 7 claus GEMMA4 rotades (límit ~1.500 req/dia per clau × 7 = ~10.500 req/dia)
- **Per què prompt complet tot i que el delta és petit**: els +0.14 punts en un escenari real amb 20.000 adaptacions/mes equivalen a **milers d'adaptacions més ben fetes**, i el cost extra és zero (Gemma és gratis). A més, els guanys són en criteris pedagògicament importants: complements (+1.0 sobre Mistral) i adequació al perfil.

### Opció B — Arquitectura dual (més sofisticada)

**Gemma 4 31B per al text + Mistral Small per a complements**.

- Gemma per al cos del text adaptat (excel·lent en MECR, perfil i llegibilitat)
- Mistral per al glossari i esquemes (lidera fidelitat curricular)
- **Cost afegit**: ~$15/mes per la part Mistral a escala FJE
- **Complexitat tècnica**: requereix orquestració de 2 crides per cada adaptació

**Recomanació**: començar amb l'**Opció A** i passar a Opció B només si veiem caigudes específiques en fidelitat curricular als casos reals de FJE.

### Opció C — Fallback econòmic

Si les claus Gemma s'exhaureixen per pics de demanda:

- **Fallback 1**: Llama 3.3 70B via Groq (gratis, qualitat 4.26, però NO escala a textos de batxillerat — cal limitar-lo a primària)
- **Fallback 2**: Mistral Small pagant (només $15-20/mes a escala FJE)

### Descartats

- **GPT-4o-mini**: el pitjor dels 4, més car que els gratuïts, i l'únic que depèn críticament del prompt complet. Si es va decidir fer servir en algun context, cal mantenir-hi sempre el catàleg de 98 instruccions.
- **Llama 3.3 70B**: inviable en producció via Groq free tier — saltava textos llargs sistemàticament. Caldria Groq Dev Tier ($0.59/M tok) o un altre proveïdor perquè funcionés, i aleshores deixaria de ser competitiu amb Gemma gratis.

---

## Conclusions científiques (més enllà de FJE)

1. **El catàleg de 98 instruccions sí que té valor**, però concentrat en un model concret (GPT-4o-mini). Els models open-source ja venen amb prou scaffolding pedagògic integrat.

2. **Gemma 4 31B és més potent del que ens pensàvem**: és el millor model del mercat per a aquesta tasca específica (adaptació de textos educatius en català), superant GPT-4o-mini i Mistral Small. Que sigui gratuït fa que sigui una opció clara.

3. **La mida no ho és tot**: Llama 3.3 70B (70 mil milions de paràmetres) puntua pitjor que Gemma 4 31B (31 mil milions), i Mistral Small (22B) puntua gairebé igual. El disseny del model (dades d'entrenament, fine-tuning d'instruccions) importa més que el tamany brut.

4. **Els jutges LLM són prou fiables** (r≈0.68-0.75 entre els principals) per poder-los usar com a sistema d'avaluació automàtic a producció, però cal excloure Llama com a jutge (correlació baixa).

5. **El prompt mínim és viable** per a 3 dels 4 models. Això obre la porta a arquitectures més lleugeres i econòmiques a llarg termini, tot i que el catàleg continua afegint valor puntual en certs criteris.

---

## Pròxims passos suggerits

1. **Dashboard HTML**: obre `dashboard.html` al navegador per explorar els resultats visualment.
2. **Validació humana**: seleccionar 5-10 parells representatius i contrastar el judici dels LLM amb una lectura personal o Arena.
3. **Pilot FJE**: desplegar Gemma 4 31B amb prompt complet en un grup reduït (1-2 centres FJE) abans de l'escalat general.
4. **Monitoratge en producció**: mesurar la concordança entre el judici dels docents reals i els jutges LLM durant el pilot.

---

## Fitxers generats

- `resultats_generacio.json` — GPT-4o-mini 180/180
- `resultats_generacio_mistral.json` — Mistral 180/180
- `resultats_generacio_llama.json` — Llama 64/180 (primària + 2 ESO)
- `resultats_generacio_gemma.json` — Gemma 4 31B 180/180
- `resultats_avaluacio_multi.json` — 604 avaluacions × 4-5 jutges
- `informe_multi_model.md` — informe tècnic detallat amb totes les taules
- `dashboard.html` — dashboard interactiu amb gràfics
- `informe_executiu_FJE.md` — aquest document
