# Estrategia de costos i escalat ATNE

**Data**: 4 abril 2026
**Autor**: Miquel Amor (amb suport Claude)
**Per a**: Direccio FJE

---

## 1. Context

L'assistent ATNE adapta textos educatius a les necessitats de l'alumnat (nouvinguts, NESE, altes capacitats, DUA). Utilitza models d'intel.ligencia artificial (LLM) per transformar textos originals en versions adaptades segons el perfil de cada alumne.

La pregunta clau: **quin es el cost real d'operar aquest assistent a escala?**

---

## 2. Resultats de l'avaluacio (marc 2026)

S'han avaluat 1.800 textos adaptats amb 3 generadors, 3 arquitectures de prompt i 2 jutges automatitzats.

### Qualitat obtinguda (escala 1-5, RAG-v2, sense self-eval)

| Rang | Model | Puntuacio global | Cost per adaptacio | Notes |
|------|-------|-----------------|-------------------|-------|
| 1 | **GPT-4o-mini** (OpenAI) | **4.44** | ~0.003€ | Millor qualitat absoluta |
| 2 | **Gemma 4 31B** (Google) | **4.23** | **0€ (free tier)** | Open-source, Apache 2.0 |
| 3 | **Mistral Small** (Mistral) | **4.19** | **0€ (free tier)** | Europeu, mes rapid |
| 4 | Gemini 2.5 Flash | 3.93 | 0€ (free tier) | Sense thinking tokens |
| 5 | Claude Sonnet 3.5 | 2.04 | 0€ (CLI) | Bug RAG-v2 (invalid) |

### Conclusio qualitat

**Els 3 models gratuits arriben al 94-95% de la qualitat del millor model de pagament (GPT).**

- Diferencia GPT vs Gemma 4: **0.21 punts** (nomes un 4.7%)
- Diferencia GPT vs Mistral: **0.25 punts** (un 5.6%)
- Gemma 4 vs Mistral: **0.04 punts** (diferencia despreciable)

**Tots els models guanyadors superen el 4.0/5.0**, que significa que un docent els podria usar directament a l'aula amb revisions minimes.

### Eleccio per escenari

- **Maxima qualitat (~0.005€/cas)**: GPT-4o-mini
- **Cost zero + velocitat**: Mistral Small (~9s/cas)
- **Cost zero + open-source**: Gemma 4 31B
- **Producte final**: es pot oferir al docent tria entre Mistral/Gemma 4 segons preferencia

---

## 3. Escenaris de cost

### Escenari A: Pilot FJE (1.000 docents, 10% actius)

**500 adaptacions/dia**

| Opcio | Model | Cost/mes | Cost/any |
|-------|-------|----------|----------|
| Free tier | Gemma 4 (Google AI Studio) | **0€** | **0€** |
| Free tier | Gemini Flash (Google AI Studio) | **0€** | **0€** |
| API barata | DeepSeek V3.2 | 8€ | 96€ |
| API Google | Gemini Flash (pagament) | 15€ | 180€ |

**Veredicte**: El pilot es pot fer amb cost zero usant la capa gratuita de Google AI Studio.

### Escenari B: FJE complet + escalat moderat (5.000 docents)

**2.500 adaptacions/dia**

| Opcio | Model | Cost/mes | Cost/any |
|-------|-------|----------|----------|
| API barata | DeepSeek V3.2 | ~40€ | ~480€ |
| API Google | Gemini Flash | ~75€ | ~900€ |
| API open-source | Gemma 4 via OpenRouter | ~50€ | ~600€ |

### Escenari C: Espanya sencera (15.000 docents)

**7.500 adaptacions/dia**

| Opcio | Model | Cost/mes | Cost/any |
|-------|-------|----------|----------|
| API barata | DeepSeek V3.2 | ~190€ | ~2.280€ |
| API Google | Gemini 3 Flash | ~225€ | ~2.700€ |
| API open-source | Gemma 4 via OpenRouter | ~150€ | ~1.800€ |
| Servidor propi | Gemma 4 self-hosted | ~2.000€ | ~24.000€ |

---

## 4. Comparativa servidor propi vs API cloud

### Cost d'un servidor propi

| Component | Cost |
|-----------|------|
| 2x GPU NVIDIA RTX 5090 (32 GB) | 3.600€ |
| CPU + placa + RAM 64 GB | 800€ |
| Font 1500W + caixa | 200€ |
| SSD 1 TB | 80€ |
| **Total hardware** | **~4.700€** |
| Electricitat (~300W 24/7) | ~100€/mes |
| Manteniment tecnic | ~1.500€/mes (enginyer parcial) |
| **Cost operatiu mensual** | **~1.600€/mes** |

### Amortitzacio

| Escenari | Cost API/mes | Cost servidor/mes | Amortitzacio hardware |
|----------|-------------|-------------------|----------------------|
| FJE pilot (1.000 doc) | 0-15€ | 1.600€ | **Mai** |
| FJE complet (5.000 doc) | 40-75€ | 1.600€ | **Mai** |
| Espanya (15.000 doc) | 150-225€ | 2.000€ | **Mai** |

**Conclusio**: El servidor propi NO surt a compte per a cap escenari previst. Les APIs han baixat un 80% de preu en un any i segueixen baixant. L'unic cas on te sentit es si hi ha un requisit legal de sobirania de dades que impedeixi enviar dades fora de la infraestructura propia.

---

## 5. Models disponibles (abril 2026)

### Models recomanats per ATNE

| Model | Desenvolupador | Llicencia | Preu API (/M tokens) | Qualitat | Catala | UE |
|-------|---------------|-----------|---------------------|---------|--------|-----|
| **Gemma 4 31B** | Google | Apache 2.0 | $0.14/$0.40 | #3 open | 140+ llengues | OK |
| **Gemma 4 26B MoE** | Google | Apache 2.0 | $0.13/$0.40 | #6 open | 140+ llengues | OK |
| **DeepSeek V3.2** | DeepSeek | MIT | $0.14/$0.28 | ~GPT-5 | Bo | OK |
| **Qwen 3.5** | Alibaba | Apache 2.0 | ~$0.30/$0.90 | #1 open | 201 llengues | OK |
| **Gemini Flash** | Google | Propietaria | $0.15/$0.60 | Molt alt | Excellent | OK |
| **GLM-5** | Zhipu AI | MIT | ~$0.20/$0.50 | Competitiu | Bo | OK |

### Models descartats

| Model | Motiu |
|-------|-------|
| **Llama 4** (Meta) | **Prohibit a la UE** — la llicencia exclou explicitement la Unio Europea per als models multimodals |
| **GPT-5** (OpenAI) | Massa car ($1.25/$10 per M tokens) per al volum previst |
| **Claude Opus** (Anthropic) | Massa car ($15/$75 per M tokens) |

---

## 6. Arquitectura recomanada

### Fase actual: Pilot personal (cost zero)

```
Gemma 4 31B (free tier, 14.400 peticions/dia)
     |
     v
Text adaptat → Autoavaluacio (Gemma 4 jutge) → Si OK → Docent
                                              → Si NO → Regenera (max 2 intents)
```

- Cost: **0€/mes**
- Limit: ~4.800 adaptacions/dia (suficient fins a 1.000 docents)

### Fase 2: Institucional FJE (1.000-5.000 docents)

```
Gemini Flash o Gemma 4 (free tier o API barata)
     |
     v
Text adaptat → Autoavaluacio → Retry si cal
```

- Cost: **0-75€/mes**
- Infraestructura: servidor web barat (Cloud Run ~20€/mes)
- Total: **20-95€/mes**

### Fase 3: Escalat nacional (15.000 docents)

```
DeepSeek V3.2 o Gemma 4 (API)
     |
     v
Text adaptat → Autoavaluacio → Retry si cal
```

- Cost LLM: **150-225€/mes**
- Infraestructura: Cloud Run escalat (~100€/mes)
- Total: **250-325€/mes**

---

## 7. Arquitectura multiagent: analisi

S'ha investigat si usar multiples models en cascada (un fa el borrador, un altre el revisa) milloraria la qualitat.

### Conclusions

| Patro | Guany qualitat | Cost extra | Recomanacio |
|-------|---------------|------------|-------------|
| Draft + Refine (2 models) | +5-15% | 2x crides | NO — guany marginal |
| Cascade/Routing (model petit → gran) | 0% (ambdos free) | Cap | NO — no estalvia res |
| **Generate + Verify + Retry** | +10-20% en casos dificils | 2-3x crides | **SI** — millora fiabilitat |

L'unica arquitectura multiagent que te sentit es la d'**autoavaluacio amb retry**: generar, avaluar automaticament, i regenerar si la qualitat es baixa. Amb els limits generosos del free tier (14.400 peticions/dia), hi ha marge de sobra.

La recerca academica (ICLR 2025) confirma que els sistemes multi-agent de debat "no superen consistentment estrategies amb un sol agent" per a tasques de generacio de text.

---

## 8. Riscos i mitigacions

| Risc | Probabilitat | Impacte | Mitigacio |
|------|-------------|---------|-----------|
| Google elimina free tier | Mitjana | Alt | Tenir DeepSeek/Qwen com a backup (canvi de 2 linies de codi) |
| Qualitat insuficient per a catala | Baixa | Alt | Avaluacio continua amb rubrica v2 + feedback docents |
| Problemes GDPR amb dades alumnes | Mitjana | Alt | No enviar dades personals al model (nomes text academic) |
| Model genera contingut inadequat | Baixa | Alt | Autoavaluacio + filtres de seguretat |
| Preu APIs puja | Baixa | Baix | Tendencia es a la baixa (80% reduccio en un any) |

---

## 9. Comparativa amb alternatives al mercat

| Solucio | Cost/docent/mes | Adaptacio personalitzada | Ecosistema segur | Memoria alumne |
|---------|----------------|------------------------|------------------|----------------|
| ChatGPT (obert) | 0-20€ | NO (prompt manual) | NO | NO |
| Gemini (obert) | 0€ | NO (prompt manual) | NO | NO |
| ATNE (nostre) | **0-0.02€** | **SI** (10 perfils, DUA, MECR) | **SI** | **SI** (futur) |
| Plataformes EdTech | 5-15€ | Parcial | Variable | Variable |

**L'avantatge d'ATNE no es el cost (tots son barats), sino l'especificitat pedagogica**: adapta per perfil, nivell MECR, DUA, amb memoria de l'alumne i del grup, dins un ecosistema segur i normatiu.

---

## 10. Resum executiu

1. **El cost de l'LLM ja no es un problema.** Fins per a 15.000 docents, parlem de 150-225€/mes — menys que una llicencia de Zoom.

2. **El pilot es pot fer a cost zero** amb la capa gratuita de Google AI Studio (Gemma 4: 14.400 peticions/dia).

3. **No cal comprar servidor.** Les APIs cloud son 10x mes barates que el hardware propi per al nostre volum.

4. **Llama 4 (Meta) esta prohibit a la UE.** Alternatives viables: Gemma 4 (Google, Apache 2.0), DeepSeek (MIT), Qwen 3.5 (Apache 2.0).

5. **L'arquitectura multiagent no aporta valor significatiu.** Un sol model ben promptejat + autoavaluacio amb retry es la millor opcio.

6. **El cost real d'escalar no es l'LLM, sino la infraestructura, el suport i el manteniment.** El model d'IA es la part mes barata del projecte.
