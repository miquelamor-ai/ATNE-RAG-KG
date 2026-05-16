# M3 — Gradació Lingüística per Nivell MECR

**Mòdul**: M3 Llengua
**Versió**: 1.0 (2026-05-16)
**Àmbit**: Generació i enriquiment de textos educatius per a ATNE i futurs assistents FJE
**Font**: MALL FJE + Decret 175/2022 + MECR (Consell d'Europa) + HCL (Habilitats Cognitivolingüístiques)

---

## 1. Propòsit

Aquest mòdul descriu **les característiques lingüístiques operatives** de cada nivell MECR
(pre-A1 → C1) perquè els assistents IA puguin:

- **Generar** textos calibrats al nivell de l'alumnat
- **Enriquir** un text un graó per sobre del seu nivell actual
- **Avaluar** si un text és coherent amb el nivell declarat

Les instruccions estan pensades per ser **prescriptives i comprovables**: connectors concrets,
rangs de longitud de frase, estructures permeses i prohibides. No descripcions abstractes.

---

## 2. Mapa de nivells

| Codi MECR | Etiqueta MALL | Etapa típica | Descripció lectora |
|---|---|---|---|
| pre-A1 | Emergent | Infantil I3-I5, 1r-2n CI | Fase loogràfica o alfabètica emergent. Lectura compartida adult/infant. |
| A1 | Inicial | 3r-4t CI, nouvingut recent | Descodifica amb suport. Comprèn textos molt senzills. |
| A2 | Funcional | 5è-6è CP, 1r-2n ESO baix | Lector autònom per a textos quotidians. Comprèn textos breus. |
| B1 | Estratègic | 2n-3r ESO, batx. inicial | Lector estratègic. Comprèn textos curriculars estàndard. |
| B2 | Acadèmic | 4t ESO, batxillerat | Lector acadèmic. Comprèn textos disciplinaris. |
| C1 | Expert | Batxillerat superior, FP | Lector expert. Domina registres especialitzats. |

---

## 3. Taula de gradació per dimensions lingüístiques

| Dimensió | pre-A1 | A1 | A2 | B1 | B2 | C1 |
|---|---|---|---|---|---|---|
| **Vocabulari** | Concret visual, món immediat | Freqüent quotidià (≤500 paraules) | Temàtic general curricular | Temàtic específic | Acadèmic-disciplinar | Especialitzat metadiscursiu |
| **Longitud frase** | 3-6 paraules | 6-10 paraules | 8-14 paraules | 12-20 paraules | 15-25 paraules | Variable 5-30+ |
| **Sintaxi** | Frase simple S+V+C | Simple + coordinació (i/però/o) | Coordinació + subord. causal/temporal bàsica | Subord. adverbials completes | Subord. complexa + passiva + nominalitz. | Hipotaxi, incisos, retòrica |
| **Connectors** | i, i llavors | i, però, perquè, o, també | primer, després, per tant, és a dir | tot i que, en canvi, ja que, d'una banda | en conseqüència, atès que, tanmateix | tots + metadiscursius |
| **Temps verbals** | Present indicatiu | Present + passat perifràstic + futur | Tots els bàsics + condicional | Tots + subjuntiu present | Tots + subjuntiu passat + perífrasis | Tots + modalitat epistèmica |
| **HCL** | Descriure | Descriure, explicar | Descriure, explicar, justificar | + argumentar bàsic | Tots | Tots, complexos |
| **Estructura** | Repetitiva i rítmica | Lineal senzilla | Lineal amb alguna ruptura | Paragrafada temàtica | Estructura argumentativa | Variació deliberada |

---

## 4. Regla de l'enriquiment gradual

Quan s'enriqueix un text, s'apliquen les característiques del nivell N+1 al text de nivell N.
**No es fa un salt de registre** sinó un ajust incremental:

| Nivell actual | Nivell a aplicar en enriquir |
|---|---|
| pre-A1 | A1 |
| A1 | A2 |
| A2 | B1 |
| B1 | B2 |
| B2 | C1 |
| C1 / C2 | C1 (enriquiment d'estil, no de nivell) |

---

## 5. Blocs per a l'LLM

Cada bloc és una instrucció operativa que l'assistent IA pot injectar directament al prompt.
Format parseable: `### <nivell>` + bloc de codi.

### pre-A1

```
NIVELL pre-A1 — Emergent (MOPI / lectura loogràfica o alfabètica emergent)
Vocabulari: exclusivament concret i visual. Paraules del món immediat (cos, casa, família, animals, colors, accions bàsiques). Cap terme abstracte.
Sintaxi: ÚNICAMENT frase simple (Subjecte + Verb + Complement). PROHIBIT qualsevol subordinació i coordinació adversativa.
Connectors permesos: "i", "i llavors". CAP ALTRE.
Longitud de frase: 3 a 6 paraules. Màxim total del text: 40 paraules.
Temps verbals: present d'indicatiu ÚNICAMENT.
Estructura: repetitiva i rítmica per facilitar l'anticipació lectora (patró: «La Maria té un gat. El gat és taronja. El gat menja.»).
HCL: descriure (pur). Cap altra habilitat cognitivolingüística.
Marcadors visuals: afegeix [IMATGE: concepte curt] al final de cada frase.
```

### A1

```
NIVELL A1 — Inicial
Vocabulari: freqüent quotidià (les ~500 paraules més freqüents del català). Termes nous SEMPRE amb definició curta o imatge adjacent.
Sintaxi: frase simple + coordinació senzilla (i, però, o, també). Cap subordinació.
Connectors permesos: i, però, perquè (causal simple), o, també, llavors, de vegades.
Longitud de frase: 6 a 10 paraules.
Temps verbals: present d'indicatiu, passat perifràstic (va fer, va anar), futur immediat (anirà, ho farà).
HCL: descriure, explicar bàsic.
Marcadors visuals: [IMATGE:] cada 2-3 frases si el tema ho permet.
```

### A2

```
NIVELL A2 — Funcional
Vocabulari: temàtic general del currículum. Termes especialitzats en negreta amb definició inline o al glossari.
Sintaxi: coordinació completa + subordinades causals (perquè, ja que) i temporals (quan, mentre, després que). Màxim 1 subordinada per frase.
Connectors permesos: primer, després, finalment, per tant, per exemple, tot i que (amb mesura), és a dir, a més.
Longitud de frase: 8 a 14 paraules.
Temps verbals: present, passat (perifràstic + imperfet), futur, condicional simple.
HCL: descriure, explicar, justificar senzill.
```

### B1

```
NIVELL B1 — Estratègic
Vocabulari: temàtic específic de la disciplina. Termes tècnics definits la primera vegada que apareixen.
Sintaxi: subordinades adverbials completes (causal, temporal, condicional, concessiva). Fins a 2 subordinades per frase.
Connectors permesos: tot i que, en canvi, ja que, per tant, d'una banda / de l'altra, és a dir, a diferència de, a causa de, per consegüent.
Longitud de frase: 12 a 20 paraules.
Temps verbals: tots els temps indicatiu + subjuntiu present + imperfetuós.
HCL: descriure, explicar, justificar, argumentar bàsic.
```

### B2

```
NIVELL B2 — Acadèmic
Vocabulari: acadèmic-disciplinar. Termes especialitzats sense definició sistemàtica (es pressuposa competència lectora bàsica en la matèria).
Sintaxi: subordinació complexa, veu passiva ocasional, nominalitzacions (la realització de, l'aplicació del mètode). Fins a 3 clàusules per frase. Variació de longitud de frase.
Connectors permesos: en conseqüència, atès que, cal subratllar que, en aquest sentit, d'acord amb, malgrat que, tot i que, tanmateix, amb tot.
Longitud de frase: 15 a 25 paraules.
Temps verbals: tots + subjuntiu passat + perífrasis (haver de, poder, deure, caldre).
HCL: tots (descriure, explicar, justificar, argumentar, demostrar, definir, interpretar).
```

### C1

```
NIVELL C1 — Expert
Vocabulari: especialitzat i metadiscursiu. Camp semàntic ampli, variació lèxica deliberada per evitar repeticions.
Sintaxi: hipotaxi complexa, incisos, aposicions, estructures retòriques (anàfora, comparació). Variació intencional de longitud de frase per efecte estilístic.
Connectors permesos: tots, incloent dit d'una altra manera, cal remarcar que, en el marc de, a tall d'il·lustració, en definitiva, com a corol·lari, per acabar.
Longitud de frase: variable (de 5 a 30+ paraules), amb diversitat deliberada.
Temps verbals: tots, amb modalitat epistèmica (sembla que, és probable que + subj., cal que + subj.).
HCL: tots, amb argumentació i demostració sofisticades. Capacitat de discussió crítica.
```

---

## 6. Instrucció d'enriquiment per a l'LLM

### Enriquir-amb-nivell

```
Enriqueix el text UN GRAÓ respecte al nivell indicat. Aplica EXACTAMENT les característiques del nivell {NIVELL_SUPERIOR}: el vocabulari, la longitud de frase, els connectors permesos i les estructures sintàctiques d'aquell nivell. NO canviïs el gènere, el to ni la longitud total del text. NO facis un salt de dos nivells. OBJECTIU: una versió lleugerament més exigent del mateix text, reconeixible com el mateix document.
Característiques a aplicar (nivell {NIVELL_SUPERIOR}):
{BLOC_NIVELL_SUPERIOR}
```

### Enriquir-auto-avaluació

```
Enriqueix el text un graó respecte al seu nivell actual. PRIMER avalua internament el nivell MECR del text original (pre-A1 / A1 / A2 / B1 / B2 / C1) observant: longitud de frase, tipus de connectors, complexitat sintàctica i registre de vocabulari. LLAVORS aplica les característiques del nivell immediatament superior al que has detectat: ajusta vocabulari, longitud de frase, connectors i estructures sintàctiques de manera proporcional. NO facis un salt de dos nivells. NO canviïs el gènere, el to ni la longitud total. Si el text és ja C1, enriqueix l'estil (variació lèxica, precisió) sense canviar el nivell sintàctic. OBJECTIU: una versió lleugerament més exigent del mateix text, reconeixible com el mateix document.
```
