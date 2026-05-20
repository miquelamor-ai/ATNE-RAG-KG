---
name: generar-mapa-conceptual
description: Instrument per generar un mapa conceptual o esquema visual adaptat al MECR. Pre-A1/A1 esquema visual (2-4 nodes). A2+ mapa jeràrquic en markdown estructurat (no ASCII-art). Pot copiar-se a Canva/XMind/MindMeister. Correccions MALL 2026-05-17 aplicades.
type: instrument
categoria_principal: mediacio
categories_secundaries: []
mecr_range: [pre-A1, A1, A2, B1, B2, C1]
agent_roles: [adapter, generator]
translanguaging: false
multimodal: true
skill_meta: generate-mapa-conceptual@corpusFJE/skills/mediacio/generate-mapa-conceptual
version: 2.0.0-bootstrap
---

# Generar mapa conceptual / esquema visual — V2 Descriptiu

## Descripció

El mapa conceptual és un organitzador visual que representa les relacions jeràrquiques entre conceptes d'un text. El MALL distingeix dos instruments amb funcions diferents:

- **Esquema visual** (funció instrumental): seqüències temporals, parts d'un tot, ordenació de fets. Adequat des de pre-A1.
- **Mapa conceptual jeràrquic** (funció epistèmica — "llegir per aprendre"): reorganitza el coneixement en categories i relacions lògiques. Comença a A2.

**Tipologia MALL**: Mediació cognitiva (organització i síntesi del coneixement)
**HCL principal**: Descriure — organitzar i jerarquitzar conceptes amb precisió creixent
**Principi rector**: text jeràrquic útil, no ASCII-art. El mapa ha de poder copiar-se a Canva, MindMeister o XMind amb mínima edició.

## Estructura canònica

### Esquema visual (pre-A1/A1)

- 2-4 nodes màxim.
- Representació d'un procés (seqüència), parts d'un tot, o qualitats simples d'un objecte.
- Pot usar fletxes simples (→) com a connectors, no estructures ASCII.

### Mapa conceptual jeràrquic (A2+)

- **Concepte central**: 1 terme nuclear del text, en negreta.
- **Branques principals**: 3-5 categories que organitzen el contingut (causes, tipus, processos, característiques...).
- **Sub-elements**: conceptes o entitats curtes, no frases explicatives llargues.
- Branques etiquetades: el nom de la branca indica la relació ("Causes", "Conseqüències", "Tipus", "Processos").

## Modulació per nivell MECR

### Pre-A1 — Emergent

Esquema visual de 2-3 nodes. Imatge → paraula o seqüència "abans/després". Màxima concreció visual: objectes reals, accions físiques. El docent pot complementar amb imatges reals enganxades.

### A1 — Inicial

Esquema visual de 3-4 nodes. Parts d'un tot o qualitats simples d'un objecte. Molt guiat: el LLM omple gairebé tot l'esquema i deixa 1-2 buits perquè l'alumne completi.

### A2 — Funcional

Primera introducció al mapa conceptual jeràrquic. 2 nivells de jerarquia (concepte central → idees principals literals). Branques etiquetades amb vocabulari del text. 3-4 branques màxim. Connexió directa amb el text: tots els termes apareixen al text adaptat.

### B1 — Estratègic

Mapa conceptual de 3 nivells (concepte → categories → detalls inferits). Connectors lògics a les branques ("Causa", "Efecte", "Tipus"). Lèxic lleugerament tècnic si s'acompanya dels termes del text. L'alumne pot completar 2-3 sub-elements buits.

### B2 — Acadèmic

Mapa de 4+ nivells. Superestructura del gènere (per a textos argumentatius: tesi → arguments → evidències). Lèxic CALP. Relacions abstractes (causa remota, consecució, contrast). Pot incloure referència creuada entre branques.

### C1 — Crític

Mapa de contrast: 2 columnes (postura A vs. postura B) o comparació de fonts/ideologies. L'alumne situa cada concepte "rere les línies" i detecta el biaix o la intenció de l'autor. Eina epistèmica de pensament crític, no de síntesi de contingut.

## Regles crítiques

**FER:**
- Pre-A1/A1: comença amb `## Esquema visual`.
- A2+: comença amb `## Mapa conceptual`.
- Branques principals sempre en **negreta**.
- Termes exclusivament del text adaptat: no inventar conceptes aliens al text.
- Etiquetar les branques per la relació que expressen, no per "Informació" o "Dades".

**NO FER:**
- ❌ Fletxes ASCII (├─, └─, │) o caixes ASCII — incompatibles amb editors visuals.
- ❌ Emojis decoratius.
- ❌ Sub-elements com a frases llargues (frases explicatives → al glossari).
- ❌ Repetir el mateix concepte a múltiples branques.
- ❌ Superar 3 nivells de sagnia (excés de profunditat).
- ❌ Conceptes no presents al text adaptat.

## Connexions MALL

- **Funció instrumental vs. epistèmica**: el MALL distingeix els dos usos del mapa. L'esquema visual organitza seqüències (procedimental); el mapa conceptual reorganitza el coneixement (epistèmic). Usar la distinció per triar el tipus correcte.
- **Multimodalitat**: a pre-A1 i A1, el mapa es complementa amb imatges reals. El suport visual és la bastida de la jerarquia conceptual.
- **Portabilitat**: el format markdown jeràrquic és dissenyat per ser copiat a eines visuals (Canva, XMind, MindMeister, Word SmartArt) amb mínima edició.

## Detecció

**Senyals docent** (quan activar mapa conceptual):
- El text té estructura jeràrquica clara: un tema central amb categories i subcategories.
- L'alumnat confon la idea principal amb els detalls: necessita veure la jerarquia.
- La unitat requereix que l'alumne organitzi el coneixement per a un estudi posterior.
- Text TILC amb conceptes relacionats entre si (ciències, història, geografia).

**Senyals alumne** (que indica que necessita el mapa):
- No pot explicar l'estructura del text: "Parla de moltes coses."
- Estudia subratllant gairebé tot el text: no jerarquitza.
- No detecta les categories que organitzen el contingut.
- En un examen, respon els detalls però oblida la idea central.
- Nouvingut B1: comprèn els termes aïllats però no veu les relacions entre ells.

**Context favorable**:
- Ciències Naturals, Socials o Geografia: textos amb categories taxonòmiques clares.
- Preparació d'un examen o exposició oral: el mapa com a eina d'estudi.
- Text amb estructura argumentativa: el mapa revela la tesi i els arguments.

**Anti-senyals** (quan NO activar):
- Text narratiu (conte, relat): l'estructura temporal és millor amb la línia del temps o l'esquema 3 parts.
- Text molt curt (<100 paraules): la jerarquia és evident sense mapa.
- Alumnat que ja usa mapes conceptuals de forma autònoma: la bastida no afegeix valor.

## Heurístiques docent

**H1 — El concepte central com a diagnòstic**
Demano a l'alumne: "Digues el text en una sola paraula o sintagma." Si no pot (o diu "tot"), el concepte central no li és clar. Fem el mapa des d'aquí: primer acordem la paraula central i llavors busquem les categories que l'organitzen. Sense concepte central, el mapa és una llista disfressada.

**H2 — Les branques com a preguntes**
Per construir les branques, ensenyo a l'alumne a fer-se preguntes sobre el concepte central: "Quins tipus hi ha?", "Quines causes té?", "Quines conseqüències?", "Com funciona?". Cada resposta és una branca. Funciona especialment bé amb textos de ciències on les branques solen ser: Definició / Tipus / Processos / Aplicacions.

**H3 — El mapa incomplet com a bastida**
En lloc de donar el mapa complet, dono el mapa amb les branques ja etiquetades i 2-3 sub-elements buits per nivell. L'alumne omple els buits consultant el text. Efecte triple: comprensió activa, jerarquització guiada i autoavaluació implícita (si no troba el sub-element, rellegeix).

**H4 — Mapa col·laboratiu per a textos complexos**
A B1+, proposo que parelles facin el mapa del mateix text i el comparin. Les diferències (una parella ha posat "causes" on l'altra ha posat "problemes") generen la discussió sobre la jerarquia del text i el significat dels termes. El docent arbitrà i aclareix.

**H5 — "El mapa es pot enganxar a Canva?"**
Crit de qualitat ràpid: si l'alumne o el LLM ha produït caixes ASCII o fletxes decoratives, el mapa no és exportable. La prova de Canva força el format correcte: jerarquia de punts amb sagnies, sense art ASCII.

## Autoavaluació (descriptors en primera persona)

- *Pre-A1*: "He vist el dibuix i puc dir de qué tracta." (oral)
- *A1*: "He vist les parts principals de [objecte/procés] a l'esquema."
- *A2*: "He identificat el tema principal i les idees principals del text."
- *B1*: "He organitzat les idees del text en categories amb les seves subcategories."
- *B2*: "He representat les relacions entre idees abstractes del text."
- *C1*: "He comparat dues postures o fonts i he identificat les diferències clau."

## Fonts principals

- MALL (Model d'Aprenentatge de Llengües i Literacitat): esquema visual vs. mapa epistèmic.
- Novak & Gowin (1984): concept mapping com a eina d'aprenentatge significatiu.
- Ausubel (1968): aprenentatge significatiu — el mapa com a pont entre el nou i el conegut.
- Cummins (2000): CALP — la jerarquització conceptual com a competència acadèmica.
- Decret 175/2022 (currículum Catalunya): competència digital i tractament de la informació.
