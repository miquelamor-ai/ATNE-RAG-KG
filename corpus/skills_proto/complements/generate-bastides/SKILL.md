---
name: generate-bastides
description: >
  Use when the teacher has activated the "bastides" complement. Generates
  scaffolding supports following MALL/TIL/TILC: helps students access the
  three planes of reading (literal, inferential, critical) and produce
  quality texts by activating cognitive-linguistic abilities (describe,
  explain, justify, argue, demonstrate). Language adapts to MECR. L1
  support is delegated to the Glossari complement. Visual layout
  suggestions for the teacher go to "Notes d'auditoria".
author: FJE — Fundació Jesuïtes Educació
version: 3.0.0-proto
complement_key: bastides
agent_role: complements
tools_required: []
triggers:
  - path: params.complements.bastides
    equals: true
depends_on:
  - path: params.complements.preguntes_comprensio
    relation: enriches  # bastides de RESPOSTA només si preguntes o activitats
  - path: params.complements.activitats_aprofundiment
    relation: enriches
related:
  - skill: generate-glossari
    note: El suport L1 (traducció + transliteració) es genera al Glossari, no aquí.
fonts_internes: NotebookLM MALL/TIL/TILC (FJE)
---

# Generar bastides (scaffolding) — v3

## Què cobreix aquest complement

El complement «Bastides» actua com a **mediador per a la construcció de
significats i la producció de textos de qualitat**. Segueix el model
**MALL/TIL/TILC** de Jesuïtes Educació.

### Els tres plànols de la lectura

Guia l'alumne a través de tres nivells de comprensió:

1. **Les línies** — comprensió literal del text (què diu).
2. **Entre línies** — inferències i hipòtesis (què vol dir).
3. **Rere les línies** — valoració crítica i ideologia (qui ho diu i
   per què).

Les bastides de lectura cobreixen aquests tres plànols progressivament.

### Habilitats cognitivolingüístiques

Quan hi ha tasca de producció, l'IA activa una o més de les **5 habilitats
cognitivolingüístiques** (Jorba/Gómez/Prat):

| Habilitat | Què fa l'alumne |
|---|---|
| Descriure | Identificar característiques, classificar |
| Explicar | Establir relacions causa-efecte, processos |
| Justificar | Aportar evidències, arguments validats |
| Argumentar | Defensar una tesi, refutar contraarguments |
| Demostrar | Provar amb dades, casos o procediments |

### Funció epistèmica de la llengua

La llengua no només comunica, sinó que **fa pensar la matèria**: les
bastides ajuden a estructurar el raonament disciplinari, no només a
formular respostes.

## Marc TILC: dependències amb el corpus

Aquest complement no funciona aïllat. Necessita el context del Tractament
Integrat de Llengua i Contingut (TILC):

| Element | Què aporta | D'on ve |
|---|---|---|
| **Patró Temàtic** | Conceptes, models i lèxic disciplinari (el "te") | `materia` + corpus M4 (curricular) |
| **Patró Lingüístic** | Estructures sintàctiques pròpies de l'àrea (l'"aigua") | corpus M3 + nivell MECR |
| **Gèneres Textuals** | Estructura del gènere (informe, crònica, debat...) | `params.genere` + corpus M3 (22 gèneres) |

## Dependència amb altres complements

| Complement | Relació amb bastides |
|---|---|
| **Preguntes de comprensió** | Si actiu → s'inclouen bastides de RESPOSTA (connectors, frases model, checklists). Si no → només bastides de lectura. |
| **Activitats d'aprofundiment** | Mateixa relació que preguntes. |
| **Glossari** | Si l'alumne és nouvingut, el glossari ja inclou traducció L1 i transliteració. Per això les bastides NO repeteixen aquesta info. |
| **Mapa conceptual** | Complementari: el mapa visualitza relacions; les bastides ajuden a verbalitzar-les. |

## Llenguatge segons MECR

L'assistent ha d'ajustar la seva complexitat al nivell de l'alumne per
garantir un **input comprensible** (Krashen):

| MECR | Tractament | Èmfasi |
|---|---|---|
| pre-A1, A1, A2 | Frases curtes, suports visuals i multimodals, emojis | Descodificació, vocabulari funcional, BICS |
| B1, B2 | Terminologia específica de l'àrea, connectors lògics complexos | Foment de l'autonomia i la reflexió metacognitiva |
| C1, C2 | Terminologia metalingüística, sofisticació argumentativa | CALP avançat, contraargumentació |

> **Nota**: a A1-A2 mai s'usen termes tècnics pedagògics (*scaffolding*,
> *patró lingüístic*, *MALL/TILC*). El títol passa de «Bastides» a
> «Eines per llegir i respondre». Els 5 elements del MALL es generen
> igualment però amb llenguatge accessible.

## Estructura de sortida v3

### Bastides de LECTURA (sempre, quan el complement està actiu)

```markdown
## [Eines per llegir i respondre | Bastides (ajudes per llegir i respondre)]

### CONTEXT
- Matèria: [matèria]
- Etapa: [etapa] · MECR: [nivell]
- Gènere textual: [gènere]

### 📖 Abans de llegir — preparar (pla de les línies)
- Activació de coneixements previs: «Què saps de [tema]?»
- Predicció: «Què creus que diu el text? Mira el títol.»
- Propòsit clar: «Llegeix per saber [una cosa concreta].»

### 🔍 Durant la lectura — comprendre (pla entre línies)
- Què subratllar (1-2 tipus d'informació clau)
- Notes al marge (✓ entès / ? dubte / ! important)
- Idea principal per paràgraf en 1 paraula

### 📝 Després de llegir — valorar (pla rere les línies)
- Resum literal en 1 frase amb buit per completar
- Inferència: «Què deu pensar l'autor sobre…?»
- Valoració crítica: «Estàs d'acord? Per què?»
```

### Bastides de RESPOSTA (només si preguntes_comprensio o activitats_aprofundiment)

L'estructura conté **4 elements MALL**:

**1. Bases d'orientació**
Guia pas a pas per realitzar la tasca de producció (segons el gènere
textual i l'habilitat cognitivolingüística demanada). Per exemple,
per «justificar un fet històric»: pas 1 enunciar el fet → pas 2 buscar
evidències al text → pas 3 connectar amb causa → pas 4 concloure.

**2. Iniciadors de frase (sentence starters)**
4-5 estructures perquè l'alumne arrenqui la producció. Adaptades a
l'habilitat cognitivolingüística:

| Habilitat | Iniciadors |
|---|---|
| Descriure | «Es caracteritza per…», «Té…», «Està format per…» |
| Explicar | «Això passa perquè…», «Com a conseqüència…» |
| Justificar | «Les dades mostren que…», «Si analitzem…, veiem que…» |
| Argumentar | «Penso que… perquè…», «En canvi…», «Malgrat que…» |
| Demostrar | «Es pot comprovar que…», «L'exemple de… ho prova» |

**3. Taula de connectors per funció discursiva**
Modulació per MECR:

| Funció | Connectors (modula segons MECR) |
|---|---|
| Causa | perquè, com que, ja que (A1-A2: només «perquè») |
| Conseqüència | per tant, així doncs, en conseqüència |
| Oposició / contrast | però, en canvi, malgrat que |
| Exemplificació | per exemple, com ara, en concret |
| Conclusió | en resum, per acabar, en definitiva |

**4. Pautes d'interrogació (checklist co-construïble)**
Llista de preguntes per a l'autoregulació, idealment co-construïdes amb
l'alumnat:
- He fet servir el lèxic precís de la matèria?
- He connectat les idees amb connectors clars?
- He justificat amb evidències del text?
- El meu text té introducció, desenvolupament i conclusió?
- Algú que no hagi llegit el text entendria la meva resposta?

### Si no hi ha tasca de producció

```markdown
> **Recomanació**: No hi ha preguntes ni activitats actives en aquesta
> adaptació. Per això NO s'inclouen bastides de resposta. Si vols que
> l'alumne respongui, activa també el complement «Preguntes de
> comprensió» o «Activitats d'aprofundiment».
```

## Errors comuns — què NO fer (v3)

Errors específics del MALL que aquesta skill evita:

- **Anàlisis gramaticals descontextualitzades** — no posar regles
  gramaticals que no serveixin per a la tasca comunicativa.
- **Simplificació excessiva (baixar nivell vs donar bastides)** —
  l'objectiu és accedir al **CALP** (llenguatge acadèmic), no
  substituir-lo per llenguatge col·loquial.
- **Correcció sistemàtica de l'error** — en una primera versió, prioritzar
  sentit i comunicació; la correcció ortogràfica és per fases posteriors.
- **Models únics (talla-única)** — no donar plantilles rígides que
  impedeixin el discurs genuí de l'alumne.
- **Sobreintervenció** — intervenir en tot moment genera dependència;
  cal deixar espai per l'autonomia.
- **Bastides permanents** — sense fading no hi ha aprenentatge real
  (només resultat).
- **Donar la resposta** — la bastida facilita el procés, no el substitueix.
- **Ocultar els criteris** — l'alumne ha de saber què s'espera d'ell
  des del principi (per això la checklist és valuosa).
- **Repetir suport L1** — ja és al complement Glossari.
- **Suggeriments visuals dins de les bastides** — són info pel docent;
  van a «Notes d'auditoria».

## Adequació per etapa educativa

| Etapa | Tipus de bastides prioritzades |
|---|---|
| Infantil / Cicle Inicial | Físiques i visuals (imatges, gestos, colors). Evita abstracció. |
| Cicle Mitjà / Superior / ESO | Procedimentals (estratègies, taules, plantilles). |
| Batxillerat / FP | Síntesi i anàlisi crítica multifont, argumentació sofisticada. |

## Regles estrictes

- **SEMPRE** generar les 3 fases de lectura (abans/durant/després).
- **CONDICIONAL** generar bastides de resposta segons preguntes/activitats.
- **CONDICIONAL** activar els 4 elements del MALL (bases, iniciadors,
  connectors, checklist) si hi ha producció. Si no, no inserir-los.
- **MAI** repetir suport L1 (ja és al glossari).
- **MAI** posar suggeriments visuals al docent dins de les bastides (van
  a «Notes d'auditoria»).
- **MAI** donar respostes: l'alumne ha de completar tot.
- **SEMPRE** modular complexitat lingüística segons MECR, especialment
  el TÍTOL (a A1-A2 és «Eines per llegir i respondre», no «Bastides
  (scaffolding)»).
- **SEMPRE** connectar les bastides al gènere textual i a la matèria
  (no genèriques).

## Referències

- `corpus/M2_bastides-scaffolding.md` — marc teòric complet (autors,
  exemples, errors comuns, fonts).
- `corpus/external/corpusFJE/M3_TILC-llengua-i-continguts.md` — model
  TILC (patró temàtic + lingüístic + gèneres).
- `corpus/external/corpusFJE/M1_desenvolupament-cognitiu-social.md` —
  ZDP de Vygotski.
- Jorba, J., Gómez, I., Prat, À. — *Parlar i escriure per aprendre*.
- Material MALL FJE (ESO, MOPI, PIN).

## Exemple

Veure `assets/exemple-ciencies-B1.md` (text informatiu, ESO 3r, MECR B1).
*Nota: l'exemple v1 cal actualitzar a v3 amb els 3 plànols de lectura i
els 4 elements MALL — pendent quan es despleguin les skills.*
