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
version: 3.1.0-proto
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

# Generar bastides (scaffolding) — v3.1

## 1. Què cobreix el complement

El complement «Bastides» actua com a **mediador per a la construcció de
significats i la producció de textos de qualitat**. Segueix el model
**MALL/TIL/TILC** de Jesuïtes Educació.

### Els tres plànols de la lectura

L'assistent interroga el text en tres nivells progressius:

1. **Llegir "les línies" (literal)** — recuperar informació explícita
   (dades, fets).
2. **Llegir "entre línies" (inferencial)** — deduir el que no es diu,
   fer hipòtesis, establir relacions causa-efecte.
3. **Llegir "rere les línies" (crític)** — comprendre la ideologia, la
   intenció de l'autor i emetre judicis valoratius.

Les bastides de lectura cobreixen aquests tres plànols progressivament.

### Resposta condicional (mediació a la ZDP)

L'IA actua segons el principi de la **Zona de Desenvolupament Proper**:

- **No dóna la resposta** — ofereix pistes, no solucions.
- **Detecta bloquejos** — ofereix l'**ajuda mínima necessària** per
  reactivar el procés.
- **Activa Habilitats Cognitivolingüístiques (HCL)** segons la demanda
  de la tasca: descriure, explicar, justificar, argumentar, demostrar.

### Funció epistèmica de la llengua

La llengua no només comunica, sinó que **fa pensar la matèria**. Les
bastides ajuden a estructurar el raonament disciplinari, no només a
formular respostes.

## 2. Dependència amb altres complements

Aquesta skill no funciona aïllada. Sota el model TILC (la llengua i la
matèria formen una unitat indestriable, com una infusió), depèn dels
elements següents:

| Element | Què aporta | D'on ve |
|---|---|---|
| **Patró Temàtic** (contingut disciplinari) | Xarxa de conceptes i models teòrics de la disciplina (el "te" de la infusió). Sense això no es pot generar una bastida per *justificar* en Ciències sense els models científics de referència. | `materia` + corpus M4 (curricular) |
| **Patró Lingüístic i Gèneres Textuals** | Lèxic especialitzat, sintaxi pròpia, i estructura del gènere textual. Cada gènere és una "esfera d'activitat humana" que determina el lèxic, la formalitat i l'estructura. | corpus M3 + `params.genere_discursiu` (22 gèneres) |
| **Habilitats Cognitivolingüístiques (HCL)** | La bastida ha d'estar "sincronitzada" amb l'habilitat que la tasca reclama. | Detecció a partir de l'encàrrec de treball / preguntes |
| **Criteris d'Avaluació i Indicadors d'Assoliment** | Per oferir feedback regulador, l'assistent ha de conèixer els criteris compartits (el "GPS" de l'alumne). Sense aquests, la bastida no pot orientar cap a l'èxit. | corpus M6 (avaluació) + `params` |
| **Complements Multimodals (DUA)** | Suports visuals (imatges, gràfics, mapes conceptuals) que reforcen el text i el procés. | Complements `pictogrames`, `esquema_visual`, `mapa_conceptual`, `illustracions` |

I dependències directes amb altres complements activats:

| Complement | Relació amb bastides |
|---|---|
| **Preguntes de comprensió** | Si actiu → s'inclouen bastides de RESPOSTA (connectors, frases model, checklists). Si no → només bastides de lectura. |
| **Activitats d'aprofundiment** | Mateixa relació que preguntes. |
| **Glossari** | Si l'alumne és nouvingut, el glossari ja inclou traducció L1 i transliteració. Per això les bastides NO repeteixen aquesta info. |

## 3. Llenguatge segons MECR

L'assistent modula el seu discurs per garantir un *input comprensible*
(Krashen) i un repte assequible:

### A1 (Inicial — propi de l'etapa MOPI/PIN)

- **Focus**: descodificació i identificació bàsica.
- **Bastides**: suports visuals i multimodals predominants (imatges,
  dibuixos, objectes). Iniciadors de frase molt simples. Lèxic funcional
  i quotidià.
- **Exemple (animals)**: per a la **descripció** — "Aquest animal és un…
  [imatge]", "Té… [dibuix de potes]".

### A2 (Bàsic — inicis ESO)

- **Focus**: comprensió literal i estructures oracionals senzilles.
- **Bastides**: iniciadors per ordenar seqüències temporals ("Primer…",
  "Després…"). Llistes de vocabulari específic de la matèria com a
  "crossa".
- **Exemple (Ciències 1r ESO — explicar un experiment)**: "Primer hem
  posat l'aigua…", "A causa de la calor, l'aigua ha…".

### B1 (Llindar — objectiu per a 2n d'ESO)

- **Focus**: comprensió inferencial i relacions lògiques entre idees.
- **Bastides**: taules de connectors lògics (causals, consecutius) per
  jerarquitzar la informació. Pautes d'interrogació per a l'autoregulació.
- **Exemple (Història 2n ESO — justificar un fet)**: "Aquest fet es
  relaciona amb… [model històric]", "Això va passar perquè…, ja que…".

### B2 (Avançat — final d'ESO)

- **Focus**: lectura crítica, domini del **llenguatge acadèmic (CALP)**
  i discurs genuí.
- **Bastides**: bases d'orientació per a gèneres complexos (assaig,
  debat, informe tècnic). Reflexió sobre l'ús estètic o ideològic de la
  llengua.
- **Exemple (Llengua catalana — ressenya literària)**: "La intenció de
  l'autor és…", "En conclusió, aquest text és persuasiu perquè utilitza
  connectors de contrast com ara…".

### C1+ (post-batxillerat / FP)

- **Focus**: contraargumentació, síntesi multifont, anàlisi crítica.
- **Bastides**: metalingüística sofisticada, argumentació tesi/antítesi.

> **Nota crítica**: a A1-A2 mai s'usen termes tècnics pedagògics
> (*scaffolding*, *patró lingüístic*, *MALL/TILC*). El títol passa de
> «Bastides» a **«Eines per llegir i respondre»**. Els elements del MALL
> es generen igualment però amb llenguatge accessible.

## 4. Estructura de sortida v3

L'estructura no és un text acabat, sinó una combinació d'instruments que
ajuden l'alumne a construir-lo.

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

### Bastides de RESPOSTA — 4 blocs (només si preguntes_comprensio o activitats_aprofundiment)

**Bloc A — Base d'orientació (l'esquema del gènere)**

L'IA proporciona el "mapa" del gènere textual demanat.

*Exemple Història — Crònica històrica:* "Per escriure la teva crònica,
recorda seguir aquest ordre:
1. Títol suggeridor
2. Introducció (què, qui, on, quan)
3. Fets ordenats cronològicament
4. Conclusió (conseqüències del fet)."

**Bloc B — Bastides lingüístiques (iniciadors de frase per HCL)**

Estructures per activar les habilitats cognitivolingüístiques. Adapta
els iniciadors a l'habilitat demanada:

| Habilitat | Iniciadors |
|---|---|
| Definir | "X és un/a…", "S'anomena X a…", "Es caracteritza per…" |
| Descriure | "Es caracteritza per…", "Té…", "Està format per…" |
| Explicar | "Això passa perquè…", "Com a conseqüència…", "El mecanisme és…" |
| Justificar | "Això passa perquè…", "Seguint el model de…, podem dir que…", "Aquest fenomen es deu a…" |
| Argumentar | "Penso que… perquè…", "En canvi…", "Malgrat que…" |
| Demostrar | "Es pot comprovar que…", "L'exemple de… ho prova" |

**Bloc C — Taula de connectors lògics**

Tria selecta segons la funció necessària. Modula per MECR:

| Funció | Connectors (modula segons MECR) |
|---|---|
| Causa | perquè, com que, ja que (A1-A2: només «perquè») |
| Conseqüència | per tant, així doncs, en conseqüència |
| Oposició / contrast | però, en canvi, no obstant això, per contra |
| Exemplificació | per exemple, com ara, així mateix |
| Conclusió | en resum, per acabar, en definitiva |

**Bloc D — Pauta d'interrogació (checklist co-construïble)**

2-5 preguntes clau perquè l'alumne revisi la seva pròpia producció:

- Has utilitzat el lèxic precís de la matèria?
- Has connectat les idees amb connectors clars?
- Has justificat amb evidències del text?
- El meu text té introducció, desenvolupament i conclusió?
- Algú que no hagi llegit el text entendria la meva resposta?

### Exemple d'aplicació combinada (Ciències 1r ESO)

Si l'alumne diu *"No sé com explicar per què la planta s'ha mort"*,
l'IA respon:

1. **Iniciador (Bloc B)**: "Pots començar dient: *La planta s'ha mort a
   causa de…* o *Si ens fixem en el reg, veiem que…*"
2. **Connector (Bloc C)**: "Per connectar amb la teva hipòtesi inicial,
   usa: *per tant* o *en conseqüència*."
3. **Pregunta de revisió (Bloc D)**: "Has fet servir paraules
   científiques com *fotosíntesi* o *nutrients*?"

### Si no hi ha tasca de producció

```markdown
> **Recomanació**: No hi ha preguntes ni activitats actives en aquesta
> adaptació. Per això NO s'inclouen bastides de resposta. Si vols que
> l'alumne respongui, activa també el complement «Preguntes de
> comprensió» o «Activitats d'aprofundiment».
```

## 5. Què s'elimina respecte v1

Per garantir un aprenentatge més profund i una comunicació de qualitat,
v3 elimina els enfocaments següents:

- **Avaluació de resultats aïllada** — s'elimina el focus en la
  qualificació final del producte. Es passa a una **avaluació de
  procés**, on l'IA actua com a reguladora durant tota la tasca.
- **Correcció sistemàtica de l'error** — en una primera versió es
  prioritza que el missatge s'entengui i que el **patró temàtic** sigui
  correcte. La revisió formal és per a fases posteriors. *Exemple*:
  enlloc de "T'has oblidat l'accent a *econòmica*", v3 diu: "Has
  utilitzat bé el connector *per tant*, però revisa si el lèxic
  especialitzat (*economia feudal*) és el més precís per a aquesta
  crònica."
- **Llistes de preguntes literals** — s'eliminen bateries on la resposta
  es troba "copiant les línies". V3 prioritza preguntes de **comprensió
  inferencial** (entre línies) i **comprensió crítica** (rere les línies).
- **Gramàtica descontextualitzada** — s'eliminen les explicacions
  gramaticals sense funció directa en la tasca comunicativa. V3 només
  proporciona recursos lingüístics útils per al **gènere textual** que
  es treballa.
- **Plantilles "talla única"** — s'eliminen les bastides rígides i
  uniformes. V3 detecta el nivell **MECR** i les dificultats específiques
  per oferir ajuda personalitzada ajustada a la **ZDP**.
- **Excessiva intervenció (sobreintervenció)** — s'elimina l'ajuda
  permanent que genera inseguretat o dependència. V3 planifica la
  **retirada de la bastida** (fading) a mesura que l'alumne guanya
  autonomia.
- **Simplificació excessiva (baixar el nivell)** — l'objectiu no és
  rebaixar el contingut, sinó oferir bastides per accedir al **CALP**
  (Cummins).
- **Models únics (talla-única)** — plantilles rígides que impedeixen el
  discurs genuí de l'alumne.
- **Repetir suport L1** dins de les bastides — ja és al complement
  Glossari.
- **Suggeriments visuals al docent** dins de les bastides — van a
  «Notes d'auditoria».

## 6. Adequació per etapa educativa

| Etapa | Tipus de bastides prioritzades |
|---|---|
| Infantil / Cicle Inicial | Físiques i visuals (imatges, gestos, colors). Evita abstracció. |
| Cicle Mitjà / Superior / ESO | Procedimentals (estratègies, taules, plantilles). |
| Batxillerat / FP | Síntesi i anàlisi crítica multifont, argumentació sofisticada. |

## 7. Regles estrictes

- **SEMPRE** generar les 3 fases de lectura (abans/durant/després).
- **CONDICIONAL** generar bastides de resposta segons preguntes/activitats.
- **CONDICIONAL** activar els 4 blocs de resposta (A/B/C/D) si hi ha
  producció. Si no, no inserir-los.
- **MAI** repetir suport L1 (ja és al glossari).
- **MAI** posar suggeriments visuals al docent dins de les bastides (van
  a «Notes d'auditoria»).
- **MAI** donar respostes: l'alumne ha de completar tot.
- **SEMPRE** modular complexitat lingüística segons MECR, especialment
  el TÍTOL (a A1-A2 és «Eines per llegir i respondre», no «Bastides
  (scaffolding)»).
- **SEMPRE** connectar les bastides al gènere textual i a la matèria
  (no genèriques).
- **SEMPRE** vincular la pauta d'interrogació (Bloc D) als criteris
  d'avaluació compartits amb l'alumne (transparència).

## 8. Referències

- `corpus/M2_bastides-scaffolding.md` — marc teòric complet (autors,
  exemples, errors comuns, fonts).
- `corpus/external/corpusFJE/M3_TILC-llengua-i-continguts.md` — model
  TILC (patró temàtic + lingüístic + gèneres).
- `corpus/external/corpusFJE/M1_desenvolupament-cognitiu-social.md` —
  ZDP de Vygotski.
- Jorba, J., Gómez, I., Prat, À. — *Parlar i escriure per aprendre*.
- Material MALL FJE (ESO, MOPI, PIN).

## 9. Exemple

Veure `assets/exemple-ciencies-B1.md` (text informatiu, ESO 3r, MECR B1).
*Nota: l'exemple v1 cal actualitzar a v3.1 amb els 3 plànols de lectura,
els 4 blocs MALL i la modulació MECR refinada. Pendent quan es despleguin
les skills.*
