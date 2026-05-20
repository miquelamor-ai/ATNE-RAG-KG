---
name: generar-bastides
description: Instrument per generar bastides de lectura (3 moments × 3 plànols, sempre actives) i bastides de producció (base d'orientació + connectors + HCL iniciadors + checklist, condicionals). Pre-A1 gestual/oral. Correccions MALL 2026-05-17 aplicades.
type: instrument
categoria_principal: mediacio
categories_secundaries: []
mecr_range: [pre-A1, A1, A2, B1, B2, C1]
agent_roles: [adapter, generator]
translanguaging: false
multimodal: true
skill_meta: generate-bastides@corpusFJE/skills/mediacio/generate-bastides-lectura
version: 2.0.0-bootstrap
---

# Generar bastides (lectura i producció) — V2 Descriptiu

## Descripció

Les bastides (scaffolding) són suports temporals i retirables que guien l'alumne mentre no té automatitzats els processos de lectura o producció. En ATNE, hi ha **dos tipus**:

- **Bastides de LECTURA** (sempre actives quan s'activa el complement bastides): guien els 3 moments del procés lector (Abans / Durant / Després) i els 3 plànols (literal / inferencial / crític/valoratiu).
- **Bastides de PRODUCCIÓ** (condicionals — únicament si hi ha preguntes obertes o activitats d'aprofundiment actives): GPS del gènere + recursos lingüístics + checklist.

**Tipologia MALL**: Mediació cognitiva (doble — lectura + producció)
**Distinció clau**: les bastides de lectura proporcionen el **procediment** (com llegir), no les preguntes (el complement preguntes_comprensio fa el treball de comprensió detallat). No duplicar.
**Principi rector**: "Menys és més" — màxim 3 ítems per moment. Una bastida ben triada aporta més que deu ítems genèrics.

## Estructura canònica

### Bastides de lectura (sempre)

| Moment | Funció | Estratègia MALL |
|---|---|---|
| **Abans de llegir** | Activar coneixements previs, predicció, propòsit | Formular hipòtesis |
| **Durant la lectura** | Monitorar la comprensió, marcar dubtes | Visualitzar / fer inferències en curs |
| **Després de llegir** | Processar als 3 plànols: literal → inferencial → valoratiu | Recapitular → resumir |

### Bastides de producció (condicionals, A1+)

- **Bloc A — Base d'orientació**: GPS del gènere i la matèria, amb passos disciplinars específics.
- **Bloc B — Catàleg de recursos**: connectors MECR exactes + iniciadors per HCL rellevants.
- **Bloc C — Pauta d'interrogació**: checklist d'autoavaluació específic de la tasca (A2+).

## Modulació per nivell MECR

### Pre-A1 — Emergent

**Bastides de lectura**: totes físiques i gestuals. Assenyalar imatges, predicció oral amb adult, l'adult llegeix en veu alta, l'infant assenyala o dramatitza. Després: dibuixar el que ha après, dictat a l'adult.
**Bastides de producció**: **cap.** Zero escriptura autònoma a pre-A1.

### A1 — Inicial

**Lectura**: 1 pregunta d'activació + predicció pel títol. Subratlla 1 mot clau per paràgraf. Frase marc simple: "El text parla de ___."
**Producció** (si escau): 2-3 passos molt concrets del gènere. 1 iniciador per HCL principal. Connectors: *i, però, perquè*. Sense checklist.

### A2 — Funcional

**Lectura**: 2 preguntes + propòsit de lectura explícit. Marca ✓/? /! al marge. Resum de 2-3 frases + 1 pregunta inferencial.
**Producció**: 3-4 passos + terminologia disciplinar. 2-3 iniciadors per HCL. Connectors: + *primer, llavors, per tant*. Checklist de 2-3 ítems simples.

### B1 — Estratègic

**Lectura**: Activació + predicció + hipòtesi pròpia. Notes marginals + hipòtesi en curs. Resum + inferència + valoració.
**Producció**: Raonament disciplinar (hipòtesi, evidència, causa). Iniciadors inferencials i causals. Connectors: + *ja que, en canvi, tot i que*. Checklist de 4-5 ítems.

### B2 — Acadèmic

**Lectura**: + identificació del gènere i l'autor. + detecció de posicionament. + avaluació de fiabilitat de les dades.
**Producció**: Superestructura del gènere + lèxic CALP. Iniciadors argumentals. Connectors: + *no obstant, atès que, en conseqüència* (**"tanmateix" i "no obstant" NOMÉS a B2+**). Checklist amb criteris d'avaluació.

### C1 — Crític

**Lectura**: + formulació de preguntes pròpies abans de llegir. + contrast amb coneixements previs. + autoregulació: "He entès el que calia?"
**Producció**: Contrast de fonts, biaix, intertextualitat. Recursos dialectics i retòrics. Checklist sobre fiabilitat i intenció de l'autor.

## Regles crítiques

**FER:**
- Bastides de lectura: comença sempre amb `## Suports de lectura`.
- Bastides de producció: comença la base d'orientació amb `### Per escriure [gènere], segueix aquest ordre:`.
- La base d'orientació (Bloc A) SEMPRE té passos disciplinars específics del gènere + matèria: no és mai "introducció/cos/conclusió".
- Connectors: usar EXACTAMENT els del nivell MECR, no la llista completa de tots els nivells.
- Màxim 3 ítems per moment de lectura.

**NO FER:**
- ❌ Pre-A1: cap escriptura autònoma, ni bastides de producció.
- ❌ Base d'orientació genèrica ("escriu la introducció, el desenvolupament i la conclusió").
- ❌ "Tanmateix" / "no obstant" a A1-B1.
- ❌ Repetir el suport L1/L2 aquí: va al complement Glossari.
- ❌ Donar les respostes: l'alumne omple els buits.
- ❌ Duplicar les preguntes del complement preguntes_comprensio.

## Connexions MALL

- **3 moments × 3 plànols**: les bastides de lectura implementen directament el model MALL de 3 moments (Abans/Durant/Després) i els 3 plànols cognitius (literal/inferencial/crític).
- **Base d'orientació = GPS disciplinar**: concepte MALL que distingeix el raonament disciplinar de la redacció genèrica. El docent el presenta com a model, l'alumne el consulta mentre produeix.
- **Multimodalitat**: a pre-A1, les accions físiques i gestuals substitueixen les bastides escrites.
- **"Menys és més"**: 3 ítems ben triats superen una llista de 10 genèrics.

## Detecció

**Senyals docent** (quan activar bastides):
- L'alumnat llegeix passivament sense estratègia: llegeix les paraules però no construeix sentit.
- Cal guiar la producció escrita d'una tasca complexa (informe, argumentació, experiment).
- La unitat és TILC i el contingut disciplinar és nou per a l'alumnat.
- Grup amb diversitat de nivells on es necessita una bastida universal que cada alumne usa al seu ritme.

**Senyals alumne** (que indica que necessita bastides):
- Comença a llegir sense propòsit: s'atura al mig sense saber on tornar.
- A la pregunta "De qué has llegit?", respon "No sé" o "Parla de coses".
- En producció: l'alumne mira el full en blanc durant molt de temps.
- Escriu tot de seguida sense planificar i el resultat és un text desordenat.
- Usa "perquè és molt important" com a única justificació.

**Context favorable**:
- Unitat TILC amb text dens (>200 paraules) on la comprensió és prerequisit per a l'activitat.
- Alumnat nouvingut A1-B1: necessita el GPS del gènere perquè no el té internalitzat en català.
- Primer cicle de treball d'un gènere nou (bastides es retiren progressivament al llarg de la SD).

**Anti-senyals** (quan NO activar):
- Text molt curt i comprensió immediata → discussió oral directa.
- L'alumne ja ha internalitzat l'estructura del gènere → retirar les bastides.
- Temps molt limitat → millor una o dues preguntes de comprensió potents.

## Heurístiques docent

**H1 — La bastida que es retira**
Les bastides no són permanents. Introdueixo les bastides de lectura les primeres 2-3 sessions i progressivament elimino els ítems que l'alumne ja fa sol. Una bastida que no es retira deixa de ser bastida i es converteix en dependència.

**H2 — La base d'orientació com a model, no com a recepta**
Presento la base d'orientació en veu alta, pensant en veu alta ("Primer faig X perquè..."). L'alumne veu el procés, no només el resultat. Quan l'alumne intenta fer-ho sol i s'equivoca, li pregunto: "Mira el pas 2. Qué diu que has de fer?" La bastida és l'adult accessible a qualsevol moment.

**H3 — Connectors com a termòmetre del nivell**
Reviso ràpidament els connectors que usa l'alumne: si tots els arguments comencen amb "perquè" o "però" → A1-A2. Si varia entre "en primer lloc", "per tant" → B1. Si usa "tanmateix", "no obstant" → B2. Els connectors de les bastides de producció reflecteixen exactament aquest termòmetre.

**H4 — "Subratlla el que no entens" abans de marcar el que entens**
A A2-B1, dono primer la instrucció inversa: "Marca amb ? les paraules o frases que no entens." Quan l'alumne ho ha fet, li dic: "El que queda sense marcar, ho has entès. Ara subratllem les idees importants d'allò que has entès." Evita la paralisi davant un text parcialment opac.

**H5 — La bastida mínima viable**
Quan tinc poc temps, tria la bastida mínima: propòsit de lectura ("Llegeix per saber [X concret]") + un buit al final per al resum. Dos ítems ben triats activen la comprensió activa millor que 10 ítems mal triats.

## Autoavaluació (descriptors en primera persona)

- *Pre-A1*: "He assenyalat el que m'ha demanat el mestre." (oral/gestual)
- *A1*: "He marcat una paraula important a cada part. He completat la frase del resum."
- *A2*: "He marcat ✓/? /! mentre llegia. He escrit de qué tracta el text."
- *B1*: "He fet una hipòtesi abans de llegir. He comprovat si era correcta."
- *B2*: "He identificat la postura de l'autor. He avaluat si les dades eren fiables."
- *C1*: "He formulat les meves pròpies preguntes abans de llegir i he comprovat si el text les responia."

## Fonts principals

- MALL (Model d'Aprenentatge de Llengües i Literacitat): 3 moments × 3 plànols, base d'orientació, GPS disciplinar.
- Vygotsky (1978): zone of proximal development — el scaffolding com a suport temporal.
- Wood, Bruner & Ross (1976): concepte de scaffolding en educació.
- Gibbons (2002): scaffolding language, scaffolding learning — bastides per a alumnat EAL.
- Decret 175/2022 (currículum Catalunya): metodologies actives i plurilingüisme.
