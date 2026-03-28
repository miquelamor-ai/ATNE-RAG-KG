# Investigació de marcs teòrics addicionals per a ATNE

## Context i objectiu

ATNE ja integra quatre pilars teòrics: **DUA/CAST**, **Lectura Fàcil (UNE 153101)**, **MECR** i **WCAG**. Aquesta investigació avalua si hi ha referents addicionals que aportin valor real — és a dir, que es tradueixin en instruccions concretes per a l'LLM o en millores de la UI, i que no siguin redundants amb el que ja tenim.

**Criteri de filtratge**: Un marc és rellevant per a ATNE només si:
1. Afecta directament la **transformació de text** (no la pedagogia general d'aula)
2. És **operativitzable** en regles per a un LLM (no requereix observació directa de l'alumne)
3. Aporta algo **no cobert** per DUA+LF+MECR

---

## 1. NEUROCIÈNCIA DE L'APRENENTATGE

### 1.1 Teoria de la Càrrega Cognitiva (Sweller, 1988-2024)

**Què diu**: La memòria de treball té capacitat limitada (~4 elements per a informació nova). L'aprenentatge falla quan la càrrega cognitiva total (intrínseca + extrínseca + germana) supera aquesta capacitat. Tres tipus:
- **Intrínseca**: complexitat inherent del contingut (interactivitat entre elements)
- **Extrínseca**: càrrega innecessària per mal disseny (redundància, split-attention, informació irrelevant)
- **Germana**: càrrega útil per construir esquemes mentals

**Rellevància per a ATNE**: **ALTA**

**Què aporta que no tinguem**: Ja teniu una "REGLA DE CÀRREGA COGNITIVA" al system prompt (max 2 conceptes nous per paràgraf a pre-A1/A1/A2, etc.). Però només apliqueu la versió més bàsica. Sweller aporta principis molt més precisos:

| Principi CLT | Ja implementat a ATNE? | Què falta |
|---|---|---|
| Limitar elements nous | Sí (regla max conceptes) | Correcte, però manca gradació per complexitat del contingut (un text de biologia cel·lular té més interactivitat d'elements que un de geografia) |
| Efecte split-attention | No | Quan poseu definicions entre parèntesis, forceu l'alumne a integrar dos fluxos. Per nivells baixos, seria millor glossari lateral o definició ABANS del terme |
| Efecte redundància | Parcialment | "Evitar redundància decorativa" ja ho dieu, però no hi ha regla sobre quan text+imatge és redundant vs complementari |
| Efecte worked-example | No | Per textos procedimentals (mates, ciències), un exemple resolt pas a pas redueix càrrega cognitiva més que una explicació abstracta |
| Efecte isolation / pre-training | No | Ensenyar els termes clau ABANS del text complet (glossari previ). Especialment útil per nouvinguts |
| Efecte expertise reversal | No | Suports que ajuden a novells MOLESTEN a experts. Les ajudes per nivell B2 haurien de ser mínimes; el nivell ja ho indica però no és explícit |

**Accionable per a l'LLM**: Sí, molt.
- Afegir al prompt: "Per a textos amb alta interactivitat d'elements (processos en cadena, relacions causa-efecte múltiples), reduir en 1 el màxim de conceptes nous per paràgraf"
- Afegir: "Per nivells pre-A1/A1, presentar un mini-glossari dels 3-5 termes clau ABANS del text adaptat (pre-training/isolation effect)"
- Afegir: "Per nivells B2, minimitzar suports explícits — l'excés de suport perjudica aprenents avançats (expertise reversal effect)"

**Prioritat**: **Incorporar ara (fase 1)** — És una millora directa al system prompt amb alt impacte i baix cost.

---

### 1.2 Teoria del Doble Codificació (Paivio, 1971-1991)

**Què diu**: El cervell processa informació verbal i informació visual per canals separats. Quan un concepte es codifica per ambdós canals (paraula + imatge), la retenció i comprensió milloren significativament.

**Rellevància per a ATNE**: **ALTA** (però amb matís)

**Què aporta**: Ja teniu suport per pictogrames i canal visual al sistema. El que Paivio aporta és el fonament teòric per a decisions que ja preneu intuïtivament, i afegeix precisió:
- No qualsevol combinació text+imatge funciona. La imatge ha de ser **referencial** (representar el concepte) no **decorativa**
- Per continguts abstractes (justícia, democràcia, energia), cal usar **analogies visuals** o **diagrames relacionals**, no pictogrames literals
- L'efecte és més fort per a alumnat amb baix nivell lingüístic (nouvinguts, DI) i menys impactant per a lectors competents

**Accionable per a l'LLM**: Parcialment. L'LLM genera text, no imatges. Però pot:
- Indicar on caldria suport visual i de quin tipus: `[IMATGE: diagrama del cicle de l'aigua amb fletxes]` vs `[PICTOGRAMA: sol]`
- Distingir entre suggeriment de pictograma (concret) i diagrama (relacional)
- Usar analogies visuals en el text: "L'energia és com l'aigua d'un riu: flueix d'un lloc a un altre"

**Prioritat**: **Fase 2** — L'impacte principal vindria de generació d'imatges, que ara no teniu. Les indicacions textuals de tipus d'imatge són una millora menor.

---

### 1.3 Principis d'Aprenentatge Multimèdia de Mayer (2001-2024)

**Què diu**: Richard Mayer ha identificat 15+ principis empíricament validats sobre com combinar text, imatge, àudio i vídeo per maximitzar l'aprenentatge. Els més rellevants per a text educatiu:

| Principi | Descripció | Aplica a ATNE? |
|---|---|---|
| **Coherència** | Eliminar material interessant però irrelevant | **SÍ** — l'LLM tendeix a afegir "farcit" |
| **Senyalització (Signaling)** | Ressaltar informació clau (negreta, encapçalaments, marcadors) | **SÍ** — ja ho feu parcialment |
| **Redundància** | Text + narració + imatge pot ser perjudicial; millor imatge + narració O text + imatge | Parcialment (context multimèdia) |
| **Contigüitat espacial** | Text i imatge referida han d'estar junts | **SÍ** — implicacions per layout |
| **Segmentació** | Dividir contingut complex en segments manejables | **SÍ** — ja ho feu |
| **Pre-training** | Ensenyar termes/conceptes clau abans del contingut principal | **SÍ** — alineat amb CLT |
| **Personalització** | Estil conversacional > estil formal per a aprenentatge | **SÍ** — implicacions per to |

**Rellevància per a ATNE**: **ALTA** (els 6 principis marcats amb SÍ)

**Què aporta de nou**:
1. **Principi de coherència**: L'LLM Gemini pot afegir informació "extra" que sembla útil però augmenta la càrrega cognitiva. Cal instrucció explícita: "NO afegeixis informació que no sigui a l'original, per molt interessant que sigui"
2. **Principi de senyalització**: Podeu ser més sistemàtic — no només negreta per termes tècnics, sinó també encapçalaments jeràrquics, numeració, i marcadors visuals d'estructura
3. **Principi de pre-training**: Reforçar el glossari previ (convergeix amb CLT)
4. **Principi de personalització**: Per nivells baixos (pre-A1 a A2), un to més conversacional ("Tu llegiràs...", "Ara veurem...") millora la comprensió més que un to impersonal

**Accionable per a l'LLM**: Sí, directament.

**Prioritat**: **Incorporar ara (fase 1)** — Coherència i senyalització són millores immediates al prompt.

---

### 1.4 Neurociència de la lectura (Dehaene, 2009; Wolf, 2007-2018)

**Què diu**: Stanislas Dehaene (*Reading in the Brain*) i Maryanne Wolf (*Proust and the Squid*, *Reader Come Home*) han cartografiat com el cervell processa la lectura:
- La lectura "recicla" l'àrea de la forma visual de les paraules (VWFA) al gir fusiforme esquerre
- La ruta lèxica (paraules conegudes, accés directe) i la ruta fonològica (descodificació lletra-so) són dos vies complementàries
- En dislèxia fonològica, la ruta fonològica està compromesa; en dislèxia superficial, la ruta lèxica
- La fluència lectora (automatisme en descodificació) allibera recursos cognitius per a la comprensió

**Rellevància per a ATNE**: **MITJANA-ALTA** (molt rellevant per dislèxia; menys per a la resta)

**Què aporta de nou**: Ja teniu subvars de dislèxia amb "tipografia_adaptada" i "columna_ampla". El que manca és portar-ho al TEXT generat:
1. Evitar paraules molt llargues (compostos, prefixos encadenats) — dificulten la ruta fonològica
2. Evitar paraules de forma similar (homògrafs, paraules amb lletres mirall: b/d, p/q)
3. Preferir paraules d'alta freqüència lèxica (ruta lèxica més automàtica)
4. Per alumnat amb baixa fluència (no només dislèxia — també nouvinguts, DI): cada frase ha de ser auto-continguda, sense dependre de la memòria de la frase anterior

**Accionable per a l'LLM**: Sí.
- Per dislèxia: "Evita paraules compostes llargues — divideix-les o reformula. Evita encadenar prefixos (ex: 'descontextualització' → 'treure del context'). Usa paraules d'alta freqüència sempre que sigui possible sense perdre rigor."
- Per baixa fluència: "Cada frase ha de ser comprensible per si mateixa. Repeteix el subjecte en lloc d'usar pronoms quan hi hagi risc d'ambigüitat."

**Prioritat**: **Fase 1 per a les regles de dislèxia** (són concretes i accionables). Fase 2 per a deep reading.

---

### 1.5 Memòria de treball — Baddeley (1974-2012)

**Què diu**: Model amb bucle fonològic, agenda visuoespacial, executiu central i buffer episòdic. En TDAH, l'executiu central està compromès. En DI, la capacitat general és reduïda.

**Rellevància per a ATNE**: **MITJANA**

**Què aporta**: És el fonament teòric DE la teoria de càrrega cognitiva. No aporta regles addicionals a les que ja surten de Sweller i Mayer. L'únic afegit concret:
- Per DI: màxim 1 concepte nou per paràgraf (vs 2 per a perfils sense DI a nivells baixos)

**Prioritat**: **Incorporar ara** (és una línia al prompt) però l'impacte marginal és baix perquè CLT ja cobreix el gruix. **Subsumit per Sweller.**

---

## 2. FACTORS D'APRENENTATGE

### 2.1 Hattie — Visible Learning (2009-2023)

**Què diu**: John Hattie ha sintetitzat 1.800+ meta-anàlisis per calcular la mida d'efecte de 300+ factors sobre l'aprenentatge. Factors amb alta mida d'efecte rellevants per a ATNE:

| Factor | Mida efecte (d) | Rellevant per ATNE? |
|---|---|---|
| Claredat del docent | 0.75 | **SÍ** — text clar = docent clar |
| Feedback | 0.70 | Parcialment (feedback al docent) |
| Estratègies metacognitives | 0.60 | **SÍ** — scaffolding metacognitiu |
| Organitzadors previs (Ausubel) | 0.41 | **SÍ** — glossaris previs |
| Vocabulari | 0.67 | **SÍ** — control de vocabulari |
| Repetició/pràctica espaçada | 0.58 | **SÍ** — repetir termes clau |

**Rellevància per a ATNE**: **MITJANA**

**Què aporta**: Hattie no dona regles de disseny de text — dona evidència sobre QUÈ funciona. Valor per a ATNE:
1. **Validació empírica** del que ja feu: vocabulari (d=0.67), claredat (d=0.75) i organitzadors previs (d=0.41)
2. **Estratègies metacognitives**: Afegir preguntes de comprensió intercalades. Per nivells B1-B2
3. **Repetició amb variació**: Termes clau han d'aparèixer mínim 3 vegades, cada vegada en context diferent

**Prioritat**: **Fase 2** — Les preguntes metacognitives requereixen disseny de UI. La repetició amb variació es pot afegir al prompt ara.

---

### 2.2 Vygotsky — Zona de Desenvolupament Pròxim (ZDP, 1934)

**Què diu**: L'aprenentatge òptim es dona entre el que l'alumne pot fer sol i el que pot fer amb ajuda (scaffolding). L'ensenyament ha de situar-se en aquesta franja.

**Rellevància per a ATNE**: **ALTA** (conceptualment fonamental)

**Què aporta de concret**:

1. **El nivell MECR ja és una operativització de la ZDP lingüística**. Però la ZDP no és només lingüística — també és conceptual. Un alumne pot tenir MECR B2 però estar en ZDP bàsica per a química. Implicació: el MECR hauria d'interactuar amb la familiaritat amb el contingut.

2. **Scaffolding decreixent**: Les definicions entre parèntesis haurien de seguir un patró decreixent al llarg del text:
   - 1a aparició: `**fotosíntesi** (el procés que fan les plantes per fabricar el seu aliment amb la llum del Sol)`
   - 2a aparició: `**fotosíntesi** (aliment + llum)`
   - 3a aparició i posteriors: `**fotosíntesi**` sol

3. **Mediació semiòtica**: Les eines (text, imatges, esquemes) no són accessoris, són constitutives del procés cognitiu.

**Accionable per a l'LLM**: Sí, molt.
- Scaffolding decreixent: instrucció directa al prompt sobre com graduar les definicions
- Interacció MECR x contingut: "Si el text original conté conceptes molt especialitzats, rebaixa un nivell addicional la complexitat conceptual"

**Prioritat**: **Incorporar ara (fase 1)** — El scaffolding decreixent és la millora amb millor relació impacte/cost de tot el document. És elegant, té base teòrica sòlida, i és una instrucció concreta per a l'LLM.

---

### 2.3 Bloom — Taxonomia revisada (Anderson & Krathwohl, 2001)

**Què diu**: 6 nivells de complexitat cognitiva: Recordar, Comprendre, Aplicar, Analitzar, Avaluar, Crear.

**Rellevància per a ATNE**: **MITJANA**

**Què aporta**: No dona regles de simplificació, però sí gradació per als nivells DUA:
- Accés: text al nivell Recordar/Comprendre
- Core: text al nivell Comprendre/Aplicar
- Enriquiment: text al nivell Analitzar/Avaluar/Crear

El que manca: fer EXPLÍCITA aquesta gradació al prompt d'Enriquiment.

**Prioritat**: **Fase 2** — Útil per refinar l'enriquiment. L'enriquiment DUA ja cobreix la idea general.

---

## 3. MARCS D'INCLUSIÓ EDUCATIVA

### 3.1 Index for Inclusion (Booth & Ainscow, 2002-2011)

**Rellevància**: **BAIXA** — Marc de transformació escolar, no d'adaptació de textos. No genera regles per a un LLM.

**Prioritat**: **Descartar** per a ATNE.

### 3.2 Model social de la discapacitat (OMS/CIF, 2001-2024)

**Rellevància**: **MITJANA** (conceptualment important, operativament limitada)

**Què aporta**: Ja l'apliqueu implícitament: ATNE modifica el TEXT (entorn), no l'alumne. Implicació pràctica: revisar que el llenguatge de la UI parli de "barreres d'accés al text" i no de "dèficits de l'alumne".

**Prioritat**: **Fase 2** — Revisar llenguatge UI. El prompt ja és prou neutre.

### 3.3 Decret 150/2017 Catalunya (escola inclusiva)

**Rellevància**: **MITJANA-ALTA** (marc legal del vostre context)

**Què aporta**: Terminologia legal (mesures universals/addicionals/intensives) i possible esborrany de justificació d'adaptació alineat amb la normativa. Útil per a l'auditoria/comparativa (pas 4 del pipeline).

**Prioritat**: **Fase 2** — Incorporar terminologia a l'auditoria.

### 3.4 European Agency for Special Needs and Inclusive Education

**Rellevància**: **BAIXA** — Política educativa, no d'adaptació de textos.

**Prioritat**: **Descartar** per a ATNE.

---

## 4. MARCS LINGÜÍSTICS

### 4.1 Lingüística Funcional Sistèmica — Halliday (1978-2014)

**Rellevància per a ATNE**: **ALTA** — **Aquesta és probablement la llacuna més important del vostre marc actual.**

**Què diu**: La llengua s'organitza en tres metafuncions (ideacional, interpersonal, textual). Distingeix registre (camp, to, mode) i gènere (tipus de text amb estructura predictible).

**Què aporta que NO teniu amb DUA+LF+MECR**: DUA i LF diuen QUÈ adaptar però no donen un model lingüístic precís de COM funciona un text. Halliday sí:

**1. Regles per gènere discursiu**: ATNE té la variable "matèria" (científic/humanístic/lingüístic) però NO gestiona el gènere discursiu (explicació, instrucció, narració, argumentació, descripció). Adaptar una narració és molt diferent d'adaptar una instrucció de laboratori:
- **Narració**: simplificar trama, explicitar relacions causals, reduir personatges
- **Instrucció**: numerar passos, un verb per pas, subjecte explícit
- **Explicació**: causalitat explícita, progressió del simple al complex
- **Argumentació**: tesi explícita, evidències numerades, conclusió

**2. Cohesió textual**: LF diu "una idea per frase" però no parla de com CONNECTAR frases. Per a textos adaptats:
- Evitar el·lipsi (que l'alumne hagi de reconstruir informació omesa)
- Usar referència explícita (repetir "les plantes" en lloc d'usar "elles")
- Connectors explícits ("per aquest motiu" en lloc d'assumir relació causal)

**3. Densitat lèxica i desnominalització**: Textos acadèmics tenen alta densitat lèxica i nominalització elevada. Per adaptar:
- **Desnominalitzar**: "la contaminació de l'aigua" → "l'aigua està contaminada" (verb en lloc de nom)
- **Reduir densitat lèxica**: afegir paraules gramaticals que expliciten relacions
- **Desempaquetar** metàfores gramaticals: "l'augment de temperatura causa evaporació" → "quan fa més calor, l'aigua s'evapora"

**Accionable per a l'LLM**: Sí, molt directament.

**Prioritat**: **Incorporar ara (fase 1)** — Les regles per gènere discursiu i la desnominalització són les millores més substancials que podeu fer al system prompt. Cap dels marcs actuals cobreix aquesta dimensió.

---

### 4.2 Fórmules de llegibilitat (Flesch, Dale-Chall, etc.)

**Rellevància per a ATNE**: **BAIXA**

**Per què**:
1. **No existeixen validades per al català**. Hi ha adaptacions per a castellà (Fernández-Huerta, Inflesz) però per al català no hi ha fórmules consolidades.
2. Són mètriques, no prescripcions: diuen "dificultat X" però no QUÈ canviar.
3. Ignoren coherència i estructura.
4. El MECR ja cobreix la gradació amb límits de paraules per frase.

**Prioritat**: **Parking lot** — Investigar mètriques per al català quan es plantegi validació automàtica.

---

### 4.3 Corpus lingüístics de freqüència per al català

**Rellevància per a ATNE**: **ALTA**

**Què aporta**: Ara ATNE demana "vocabulari freqüent" a l'LLM, però Gemini no té accés a dades de freqüència lèxica en català. Un corpus permetria:
1. Validació automàtica post-generació: comprovar paraules dins de les N mil més freqüents
2. Suggeriments de substitució
3. Detecció de vocabulari problemàtic al text original

Recursos existents: CTILC (IEC), Corpus DUCME, llistes de vocabulari per nivells MECR.

**Accionable per a l'LLM**: No directament. Sí com a eina de post-processament al backend Python.

**Prioritat**: **Fase 2** — Implementar verificador de freqüència lèxica.

---

## 5. ALTRES MARCS

### 5.1 TPACK (Mishra & Koehler, 2006)

**Rellevància**: **BAIXA** — Marc sobre competències docents, no sobre disseny de text. **Descartar.**

### 5.2 What Works Clearinghouse (WWC)

**Rellevància**: **MITJANA** com a font de validació, no com a marc. Les recomanacions ja estan capturades per DUA+CLT+Mayer. **Descartar** com a marc separat.

### 5.3 Social Stories (Carol Gray, 1991-2024)

**Rellevància**: **BAIXA-MITJANA** — Només rellevant quan perfil = TEA + text amb contingut social.

**Accionable**: "Per alumnat TEA, quan el text descriu situacions socials: reformula les normes implícites en frases explícites. Descriu QUÈ passa, PER QUÈ passa, i QUÈ es pot fer."

**Prioritat**: **Fase 2** — Regla de creuament específica TEA + contingut social.

---

## 6. MARCS ADDICIONALS NO SOL·LICITATS PERÒ RELLEVANTS

### 6.1 Scaffolded Reading Experience — SRE (Graves & Graves, 2003)

**Què diu**: Estructura l'experiència de lectura en tres fases: pre-lectura (activar coneixements, vocabulari, objectiu), durant-lectura (guiar, segmentar), post-lectura (resumir, connectar, aplicar).

**Rellevància**: **ALTA**

**Què aporta**: ATNE genera un TEXT ADAPTAT (fase "durant"). Però ignora pre-lectura i post-lectura:
- **Pre-lectura**: Glossari previ (ja alineat amb CLT) + "Objectiu de lectura: després de llegir, sabràs X" + "Coneixement previ: per entendre això, has de saber Y"
- **Post-lectura**: Preguntes de comprensió, activitat de consolidació

**Prioritat**: **Fase 2** — Requereix UI nova (seccions opcionals), però és la millora estructural més important a mitjà termini.

### 6.2 Llenguatge Clar / Plain Language (ISO 24495-1:2023)

**Què diu**: Norma ISO amb quatre principis: rellevant, localitzable, comprensible, usable. Diferent de LF: LF és per a dificultats cognitives; Llenguatge Clar és per a TOTHOM.

**Rellevància**: **MITJANA-ALTA**

**Què aporta**: Cobreix el nivell **Core DUA**, que ara no té referent normatiu propi:
- Accés → LF (UNE 153101)
- **Core → Llenguatge Clar (ISO 24495-1)**
- Enriquiment → Text acadèmic estàndard

**Prioritat**: **Fase 1** — Reforçar el nivell Core amb directrius de Llenguatge Clar. Ara el Core és massa vague al prompt.

---

## RESUM EXECUTIU

### Incorporar ARA (Fase 1) — Alt impacte, baix cost

| Marc | Què afegir | On |
|---|---|---|
| **Halliday (LSF)** | Regles per gènere discursiu + desnominalització + cohesió explícita | System prompt |
| **Vygotsky (ZDP)** | Scaffolding decreixent per a definicions (1a=completa, 2a=breu, 3a=terme sol) | System prompt |
| **Sweller (CLT)** | Pre-training (glossari previ), expertise reversal, split-attention | System prompt |
| **Mayer** | Principi de coherència ("no afegeixis res no original"), personalització per nivells baixos | System prompt |
| **Dehaene/Wolf** | Regles dislèxia: evitar compostos llargs, desnominalitzar, alta freqüència | System prompt |
| **ISO 24495 (Lleng. Clar)** | Reforçar definició del nivell Core DUA | System prompt |

### Incorporar en FASE 2 — Requereix desenvolupament

| Marc | Què afegir | On |
|---|---|---|
| **SRE (Graves)** | Seccions "Abans de llegir" i "Després de llegir" | UI + prompt |
| **Hattie** | Preguntes metacognitives intercalades | UI + prompt |
| **Bloom** | Gradació de complexitat cognitiva per nivell DUA | System prompt |
| **Paivio** | Indicacions de tipus d'imatge (pictograma vs diagrama) | System prompt |
| **Decret 150** | Terminologia legal a l'auditoria | Auditoria |
| **Social Stories** | Regla creuament TEA + contingut social | System prompt |
| **Corpus freq. català** | Validació automàtica de vocabulari | Backend Python |

### DESCARTAR per a ATNE

| Marc | Per què |
|---|---|
| Index for Inclusion | Marc institucional, no d'adaptació de text |
| European Agency SNEI | Política educativa, no eina |
| TPACK | Competències docents, no disseny de text |
| Fórmules llegibilitat | No validades per català, el MECR ja cobreix la funció |
| WWC | Font de validació, no marc independent |
| Baddeley | Subsumit per CLT (Sweller) |

---

## PROPOSTA CONCRETA: ADDICIONS AL SYSTEM PROMPT (FASE 1)

Text que caldria afegir al `BASE_SYSTEM_PROMPT` de `server.py`:

```
REGLES PER GÈNERE TEXTUAL (Halliday):
Identifica el gènere del text original i aplica regles específiques:
- NARRACIÓ: manté els personatges principals, explicita motivacions i emocions, simplifica trames secundàries, fes cronologia lineal.
- EXPLICACIÓ: progressió del simple al complex, causa→efecte explícita, desnominalitza processos (ex: "l'evaporació" → "quan l'aigua s'evapora").
- INSTRUCCIÓ: numera els passos, un verb d'acció per pas, subjecte "tu" explícit, ordre cronològic estricte.
- ARGUMENTACIÓ: tesi al primer paràgraf, cada argument numerat amb evidència, conclusió explícita.
- DESCRIPCIÓ: organitza espacialment o per categories, del general al particular.

COHESIÓ TEXTUAL (Halliday):
- Evita pronoms ambigus: si el referent no és a la mateixa frase, repeteix el nom complet.
- Usa connectors explícits entre frases (per tant, per aquest motiu, a més, en canvi, en primer lloc).
- Cada paràgraf comença amb una frase temàtica que anticipa el contingut.
- Desnominalitza: converteix noms abstractes en verbs quan sigui possible sense perdre rigor.

SCAFFOLDING DECREIXENT (Vygotsky):
Les definicions de termes tècnics segueixen un patró decreixent al llarg del text:
- 1a aparició: terme en negreta + definició completa
- 2a aparició: terme en negreta + definició abreujada (2-3 paraules)
- 3a aparició i posteriors: terme en negreta sol
Així l'alumne construeix progressivament l'autonomia lèxica.

PRE-TRAINING (Sweller/Mayer):
Per nivells pre-A1 a A2, comença el text adaptat amb un mini-glossari:
"## Paraules clau" amb els 3-5 termes tècnics essencials i la seva definició, ABANS del text principal.
Això redueix la càrrega cognitiva durant la lectura.

PRINCIPI DE COHERÈNCIA (Mayer):
NO afegeixis informació, exemples, dades o curiositats que no estiguin al text original.
La teva feina és ADAPTAR, no AMPLIAR. Cada element del text adaptat ha de tenir correspondència amb l'original.

PERSONALITZACIÓ PER NIVELL (Mayer):
- Pre-A1 a A2: to conversacional i directe ("Ara aprendràs...", "Mira aquest exemple...").
- B1: to clar i proper, sense ser infantil.
- B2: to acadèmic estàndard.

NIVELL CORE DUA — LLENGUATGE CLAR (ISO 24495):
Per al nivell Core, aplica principis de Llenguatge Clar:
- Cada secció té un objectiu comunicatiu clar expressat a l'encapçalament
- La informació més important va primer (piràmide invertida)
- Les enumeracions dins de frases es converteixen en llistes amb vinyetes
- Les frases passives es converteixen en actives
- El subjecte i el verb van a prop (evitar incisos llargs entre subjecte i verb)

REGLES ADDICIONALS PER DISLÈXIA (Dehaene/Wolf):
Quan el perfil inclou dislèxia:
- Evita paraules compostes llargues: divideix-les o reformula
- Prefereix paraules d'alta freqüència lèxica
- Evita encadenar prefixos i sufixos
- Frases més curtes que el màxim del nivell MECR (resta 2-3 paraules al límit)
- Repeteix termes clau en lloc d'usar sinònims (la variació lèxica dificulta el reconeixement per ruta lèxica)
```

---

## REFERÈNCIES BIBLIOGRÀFIQUES

- Sweller, J. (2011). *Cognitive Load Theory*. Springer.
- Mayer, R.E. (2021). *Multimedia Learning* (3rd ed.). Cambridge University Press.
- Paivio, A. (1991). *Dual Coding Theory*. In: Imagery and Cognition.
- Dehaene, S. (2009). *Reading in the Brain*. Viking.
- Wolf, M. (2018). *Reader, Come Home*. Harper.
- Hattie, J. (2023). *Visible Learning: The Sequel*. Routledge.
- Halliday, M.A.K. & Matthiessen, C. (2014). *Halliday's Introduction to Functional Grammar* (4th ed.). Routledge.
- Anderson, L.W. & Krathwohl, D.R. (2001). *A Taxonomy for Learning, Teaching, and Assessing*. Pearson.
- Graves, M.F. & Graves, B.B. (2003). *Scaffolded Reading Experiences* (2nd ed.). Christopher-Gordon.
- ISO 24495-1:2023. *Plain language — Part 1: Governing principles and guidelines*.
- Booth, T. & Ainscow, M. (2011). *Index for Inclusion* (3rd ed.). CSIE.
- Decret 150/2017, de 17 d'octubre, DOGC.
- Gray, C. (2015). *The New Social Story Book* (15th ed.). Future Horizons.
- Vygotsky, L.S. (1978). *Mind in Society*. Harvard University Press.
