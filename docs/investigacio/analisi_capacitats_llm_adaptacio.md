# Anàlisi de Capacitats i Límits dels LLMs per a Adaptació Textual Educativa

**Projecte**: ATNE — Adaptador de Textos a Necessitats Educatives
**Data**: 2026-03-27
**Abast**: Gemini 2.5 Flash (actual), Claude Opus/Sonnet, GPT-4.1, alternatives

---

## 1. CAPACITATS FIABLES (l'LLM ho fa bé)

### 1.1 Simplificació lèxica
**Fiabilitat: ALTA** | Depèn poc del model

La tasca més natural per als LLMs. Substituir "efectuar" per "fer", "tèrbol" per "brut", etc.

**Risc real per a ATNE**: En català, el vocabulari de freqüència dels models és menys robust que en castellà/anglès. Pot haver-hi substitucions castellanitzades.

**Recomanació**: Fiable per a producció. Considerar un petit diccionari de termes preferits en català normatiu si es detecten patrons de castellanització.

### 1.2 Simplificació sintàctica
**Fiabilitat: ALTA** | Depèn poc del model

Excel·lent a descompondre frases complexes en simples, trencar subordinades, eliminar gerundials, posar ordre SVC.

**Risc real**: En simplificar massa, pot perdre relacions causals o temporals importants ("A causa de la fotosíntesi, les plantes creixen" → "Les plantes fan fotosíntesi. Les plantes creixen." — perdent la causalitat).

**Recomanació**: Cal indicar explícitament que mantingui connectors causals i temporals quan simplifiqui.

### 1.3 Canvi de veu passiva a activa
**Fiabilitat: ALTA** | No depèn del model

**Excepció**: En textos científics, la veu passiva és convencional i convertir-la a activa pot requerir inventar un subjecte.

### 1.4 Manteniment de terminologia tècnica amb definició
**Fiabilitat: ALTA-MITJANA** | SÍ depèn del model (models grans millor)

**Risc real**:
- A vegades "sobre-simplifiquen" i substitueixen el terme tècnic per una descripció imprecisa
- Les definicions poden ser científicament imprecises en camps especialitzats
- En nivells molt baixos (pre-A1/A1), entra en conflicte entre "simplificar tot" i "mantenir terme tècnic"

### 1.5 Generació de glossaris
**Fiabilitat: ALTA** per glossaris monolingües | **MITJANA** per bilingües

| Parella lingüística | Fiabilitat |
|---|---|
| Català-Castellà/Anglès/Francès | Alta |
| Català-Àrab (estàndard) | Mitjana-Alta |
| Català-Xinès (mandarí) | Mitjana |
| Català-Urdú/Romanès | Mitjana-Baixa |
| Català-Amazic/Wòlof/Bangla | Baixa o molt baixa |

**Recomanació CRÍTICA**: Afegir disclaimer visible al frontend per als glossaris bilingües: "Les traduccions a la L1 són orientatives. Valideu-les amb un parlant natiu o mediador cultural."

### 1.6 Generació d'esquemes en text (ASCII/Unicode)
**Fiabilitat: MITJANA-ALTA** | Claude i GPT fan millor ASCII art que Gemini Flash

Limitar a 3 nivells de profunditat. Per a diagrames complexos, millor generar JSON i renderitzar al frontend.

### 1.7 Generació de preguntes de comprensió graduades
**Fiabilitat: ALTA** | Depèn poc del model

**Recomanació**: Afegir la instrucció: "Les preguntes han d'usar NOMÉS vocabulari present al text adaptat."

### 1.8 Generació de bastides (scaffolding)
**Fiabilitat: ALTA** | Models grans ho fan millor

### 1.9 Adaptació de registre
**Fiabilitat: ALTA** | Depèn poc del model

**Risc per al català**: El registre informal pot derivar cap a castellanismes col·loquials.

### 1.10 Generació d'exemples i analogies
**Fiabilitat: ALTA** | Models grans generen analogies més creatives

**Risc real**:
- Analogies culturalment inadequades per a alumnat nouvingut
- Analogies científicament imprecises que creen misconceptions

**Recomanació**: "Utilitza analogies amb objectes universals (cos humà, aigua, sol, casa) que no requereixin coneixement cultural específic."

### 1.11-1.16 Altres capacitats fiables
- **Segmentació en blocs amb títols**: ALTA
- **Connectors i senyalització discursiva**: ALTA
- **Traduccions/glossaris bilingües**: MITJANA (veure taula 1.5)
- **Coherència curricular**: MITJANA-ALTA (el RAG mitiga molt el risc)
- **Respectar un nivell MECR concret**: MITJANA (guia aproximada, no promesa precisa)
- **Mapes conceptuals en text**: MITJANA-ALTA (per a 2-3 nivells)

---

## 2. CAPACITATS LIMITADES (ho intenta però no és fiable)

### 2.1 Comptar paraules per frase amb precisió
**Fiabilitat: BAIXA**

Els LLMs basats en tokenitzadors subword **no compten paraules**. "Frases de 5-8 paraules" genera text que l'LLM "intueix" que té entre 5 i 8, però freqüentment en té 10, 12 o 4.

**Recomanació**:
1. Mantenir els rangs al prompt (guien la tendència)
2. Afegir post-processament amb codi Python que mesuri la longitud real
3. NO intentar que el codi "arregli" frases automàticament

### 2.2 Garantir nombre exacte de conceptes per paràgraf
**Fiabilitat: BAIXA** | Difícilment mitigable

"Màxim 2 conceptes nous per paràgraf" — l'LLM no té definició operacional consistent de "concepte".

### 2.3 Pictogrames/icones
**Fiabilitat: ALTA per emojis, BAIXA per pictogrames reals**

**Recomanació a llarg termini**: L'LLM genera etiquetes (`[PICTO:fotosíntesi]`), el codi les substitueix per pictogrames reals (ARASAAC API, gratuïta).

### 2.4 Controlar longitud exacta del text de sortida
**Fiabilitat: BAIXA** | "200 paraules" pot donar 150 o 300

### 2.5 Evitar al 100% determinades paraules
**Fiabilitat: MITJANA** (no 100%, però la llista negra redueix molt la freqüència)

Mantenir al prompt (cost zero) + implementar detecció post-generació amb regex.

### 2.6 Consistència perfecta entre seccions llargues
**Fiabilitat: MITJANA-BAIXA** per textos > 2000 paraules

L'atenció dels transformers es degrada amb la distància. Instruccions del system prompt "pesen menys" quan la sortida s'allarga.

### 2.7 Adaptar a un nivell Flesch/readability precís
**Fiabilitat: BAIXA** | L'LLM no calcula mètriques durant la generació

---

## 3. COSES QUE L'LLM NO POT FER (cal codi/CSS/frontend)

| Tasca | On fer-ho | Estat a ATNE |
|---|---|---|
| **Canviar tipografia** (OpenDyslexic) | CSS frontend | Parking lot |
| **Espaiat entre línies** | CSS frontend | No implementat |
| **Pictogrames reals** | API ARASAAC + frontend | Emojis com a substitut |
| **Maquetació** (columnes, posició imatges) | CSS/HTML frontend | Pendent |
| **Àudio** (TTS) | Web Speech API o Google Cloud TTS | No implementat |
| **Detectar nivell de dificultat** del text d'entrada | Codi Python (mètriques) | No implementat |
| **Verificar precisió científica** | Revisió humana (docent) — IRRENUNCIABLE | Auditoria comparativa |

---

## 4. DIFERÈNCIES ENTRE MODELS

| Criteri | Gemini 2.5 Flash | Gemini 2.5 Pro | Claude Sonnet 4.6 | Claude Opus 4.6 | GPT-4.1 | GPT-4.1-mini |
|---|---|---|---|---|---|---|
| **Seguiment instruccions** | 7/10 | 8.5/10 | 9/10 | 9.5/10 | 9/10 | 7.5/10 |
| **Qualitat català** | 6.5/10 | 7.5/10 | 8/10 | 8.5/10 | 7.5/10 | 6.5/10 |
| **Consistència format** | 6/10 | 8/10 | 9/10 | 9.5/10 | 8.5/10 | 7/10 |
| **Context window** | 1M | 1M | 200K | 200K | 1M | 1M |
| **Max output tokens** | 65K | 65K | 64K | 64K | 32K | 16K |
| **Velocitat** | Molt ràpid | Mitjà | Ràpid | Lent | Ràpid | Molt ràpid |
| **Cost (~4K in, ~4K out)** | Gratuït* | ~$0.02 | ~$0.02 | ~$0.08 | ~$0.02 | ~$0.003 |
| **Meta-text indesitjat** | ALT (el pitjor) | Mitjà | Baix | Baix | Baix | Mitjà |

*Flash gratuït: 15 RPM, 1M TPM, 1500 RPD. Suficient per prototip, insuficient per producció.

### Per què Gemini Flash és problemàtic per a ATNE

La funció `clean_gemini_output()` (40+ línies) que elimina meta-text, arregla headings duplicats i converteix sub-headings malformats **és prova directa** que el model actual no segueix instruccions de format consistentment. Amb Claude Sonnet o GPT-4.1, la major part seria innecessària.

### Recomanació de model per escenari

| Escenari | Model | Motiu |
|---|---|---|
| Prototip/demo (ara) | Gemini 2.5 Flash | Gratuït |
| Producció FJE (1r desplegament) | Claude Sonnet 4.6 o Gemini 2.5 Pro | Qualitat/cost |
| Adaptacions complexes (pre-A1, 2e, TEA+nouvingut) | Claude Opus 4.6 o GPT-4.1 | Qualitat màxima |
| Ús massiu (centenars/dia) | GPT-4.1-mini (simple) + GPT-4.1 (complex) | Routing per complexitat |
| Millor català possible | Claude Opus 4.6 | Superior en registre normatiu |

---

## 5. RECOMANACIONS PRÀCTIQUES

### 5.1 Quantes instruccions simultànies?

**7-12 instruccions**: alta fiabilitat
**15-20**: fiabilitat acceptable
**>20**: degradació notable

**El prompt actual d'ATNE té ~30 instruccions.** Això és massa, especialment per a Gemini Flash. L'efecte "primacy-recency" fa que les regles de creuament (posició intermèdia) siguin les més ignorades.

**Solució clau**: Enviar NOMÉS les instruccions rellevants per al cas concret.

### 5.2 Prompt llarg vs prompts encadenats?

**Millora (dos prompts encadenats)**:
1. **Prompt d'adaptació** (~10 instruccions): genera NOMÉS el text adaptat
2. **Prompt de complements** (rep text adaptat com a input): glossari, preguntes, bastides, etc.

### 5.3 Chain-of-thought en adaptació textual?

Mantenir `thinking_budget=0` per defecte. Activar (budget 2000-4000) per a perfils complexos (2+ característiques, DUA Accés, MECR pre-A1/A1).

### 5.4 Cal few-shot examples?

**Sí, significativament**. Amb 1-2 exemples, la variabilitat es redueix un 40-60%.

El prompt d'ATNE NO conté cap exemple complet. Afegir 1 mini-exemple per nivell MECR (~100 tokens).

### 5.5 Autocheck: funciona o és teatre?

**Majoritàriament teatre** dins del mateix prompt. L'LLM NO revisa realment el seu output token per token.

**Recomanació**:
1. Mantenir AUTOCHECK (cost zero, ajuda una mica)
2. Implementar verificació real amb codi Python (regex, comptatge, parsing)
3. Opcionalment futur: segon prompt de verificació

---

## 6. PATRONS DE PROMPT ENGINEERING

### 6.1 Role prompting — Ja s'usa. Millora: ser més específic sobre marcs concrets.

### 6.2 Constraint-based
**Punt crític**: Les restriccions negatives ("NO") són menys efectives que les positives ("FES"). Reformular:
```
En lloc de "cosa/coses" → usa el nom específic del concepte
En lloc de "allò/això" → repeteix el nom o usa un sinònim precís
En lloc de "el que fa que" → usa "provoca", "causa", "permet"
```

### 6.3 Template-based — Punt més fort actual. Millora: esquelet complet amb placeholders.

### 6.4 Rubric-based — Per a segon prompt de revisió optatiu.

### 6.5 Persona-audience pattern (NO usat, RECOMANAT)

Molt més efectiu que nivells abstractes:
```
Escrius per a un alumne de 14 anys que acaba d'arribar de Marroc fa 3 mesos.
Entén el català oral bàsic però llegeix amb dificultat.
Ha estat escolaritzat regularment al seu país.
```
L'LLM "entén" millor una persona que un nivell abstracte. El `build_system_prompt()` podria generar aquesta narrativa a partir del perfil.

---

## 7. AUDITORIA DEL PROMPT ACTUAL

### Punts forts (mantenir)
1. Regla de terminologia amb exemples correctes/incorrectes — excel·lent
2. Nivells MECR amb especificacions detallades
3. Regles de creuament de variables — innovador
4. Activació condicional de seccions de sortida
5. Format amb headings ## per parsing

### Punts a millorar (per ordre d'impacte)

| # | Problema | Gravetat | Solució |
|---|---|---|---|
| 1 | Prompt massa llarg (~30 instruccions) | **Alta** | Condicionar: no enviar regles que no s'apliquin |
| 2 | S'envien TOTS els nivells MECR (5) quan només en cal 1 | **Alta** | Enviar NOMÉS el nivell de sortida |
| 3 | Meta-text persistent de Gemini | **Alta** | Canvi de model o prefilling |
| 4 | Manca de few-shot examples | **Mitjana** | Afegir 1-2 exemples per nivell |
| 5 | Regles negatives > positives | **Mitjana** | Reformular "NO" com "FES en lloc de" |
| 6 | Sense persona-audience | **Mitjana** | Generar narrativa de l'alumne des del perfil |
| 7 | AUTOCHECK dubtosament efectiu | **Baixa** | Mantenir + verificació real amb codi |
| 8 | Thinking desactivat sempre | **Baixa** | Activar per perfils complexos |
| 9 | RAG truncat a 500 chars/doc | **Mitjana** | Augmentar a 800-1000 per docs obligatoris |

---

## 8. PLA D'ACCIÓ CONCRET

### Impacte Alt, Esforç Baix (fer ja)
1. Enviar NOMÉS el nivell MECR de sortida (no tots 5)
2. Condicionar regles de creuament — enviar NOMÉS les aplicables
3. Afegir 1 few-shot example per nivell MECR
4. Post-processament: detectar paraules prohibides (regex)
5. Post-processament: verificar longitud de frases

### Impacte Alt, Esforç Mitjà (fase següent)
6. Persona-audience al prompt
7. Reformular restriccions negatives a positives
8. Thinking adaptatiu per perfils complexos
9. Disclaimer traduccions L1 al frontend
10. Routing de models

### Impacte Mitjà, Esforç Alt (futur)
11. Pipeline en 2 passos (adaptar + complements separats)
12. Segon prompt de verificació amb rúbrica
13. Integració pictogrames ARASAAC
14. Mètriques de llegibilitat post-generació
15. Detecció automàtica de nivell del text d'entrada
