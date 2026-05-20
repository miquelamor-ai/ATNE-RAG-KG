---
name: generar-rubriques
description: Instrument per generar una rúbrica d'assoliment (alumne-facing). Escala FJE NA/AS/AN/AE, primera persona, descriptors observables. Pre-A1/A1 checklist d'icones. Criteri AE = salt qualitatiu real. MECR pre-A1-C1. Correccions MALL 2026-05-17 aplicades.
type: instrument
categoria_principal: mediacio
categories_secundaries: []
mecr_range: [pre-A1, A1, A2, B1, B2, C1]
agent_roles: [generator]
translanguaging: false
multimodal: false
skill_meta: generate-rubriques@corpusFJE/skills/mediacio/generate-rubriques
version: 2.0.0-bootstrap
---

# Generar rúbrica d'assoliment — V2 Descriptiu

## Descripció

La rúbrica d'assoliment és un instrument d'avaluació per a l'**alumne**: permet l'autoavaluació i la coavaluació d'una producció. S'orienta a la tasca de producció derivada del text adaptat. El seu tret definitori és la **primera persona i l'observabilitat**: cada descriptor diu exactament el que l'alumne ha fet o no ha fet, en termes que ell pot reconèixer en la seva pròpia producció.

**Distinció fonamental**:
- **Rúbrica d'assoliment** → s'usa AL FINAL de la producció, per avaluar el resultat.
- **Pauta d'interrogació** (Bloc C de bastides) → s'usa DURANT la producció, com a checklist d'autoregulació.

**Escala FJE**: NA (No Assolit) / AS (Assolit Satisfactòriament) / AN (Assolit Notablement) / AE (Assolit Excel·lentment).
**Pre-A1/A1**: checklist d'icones (✅/⬜) en lloc de taula.

## L'escala FJE

| Codi | Significat | Descripció en primera persona |
|---|---|---|
| **NA** | No Assolit | "No ho he fet / no apareix a la meva producció" |
| **AS** | Assolit Satisfactòriament | "Ho he fet de forma bàsica, amb suport o de manera incompleta" |
| **AN** | Assolit Notablement | "Ho he fet de forma clara, autònoma i completa" |
| **AE** | Assolit Excel·lentment | "Ho he fet amb creativitat, profunditat o autonomia destacada" |

La columna **AE** implica un salt qualitatiu real, no simplement "fer-ne més". AE = creativitat, profunditat o connexió no esperada.

## El doble esmicolament MALL

Dissenyar una rúbrica requereix dos passos:
1. **Primer esmicolament** → identificar els **criteris** (dimensions de la qualitat): contingut, llengua, estructura, rigor, reflexió.
2. **Segon esmicolament** → definir els **indicadors** per a cada nivell: comportaments observables i concrets en primera persona.

Sense el segon esmicolament, els descriptors queden abstractes ("fa bé", "és adequat") i l'alumne no sap on se situa ni com millorar.

## Criteris per nivell i matèria

**Contingut** (sempre):
- He dit el que se'm demanava.
- He usat el lèxic de la matèria.
- He justificat amb exemples o evidències.

**Llengua** (A2+):
- He connectat les idees amb connectors.
- He escrit frases clares amb subjecte i verb explícit.
- He usat el vocabulari del text.

**Estructura** (B1+):
- He seguit els passos del gènere (base d'orientació).
- He organitzat les idees de forma coherent.

**Rigor** (B2+):
- He aportat evidències, no només opinions.
- He detectat si les fonts que cito son fiables.

**Reflexió** (C1):
- He identificat la meva posició i l'he justificada.
- He tingut en compte punts de vista alternatius.

## Modulació per nivell MECR

### Pre-A1 — Emergent

Checklist d'icones. Zero lèxic abstracte. Zero escriptura autònoma. 2-3 ítems molt concrets i visuals.

```markdown
## Comprovo el meu treball

- ⬜ He assenyalat la imatge correcta
- ⬜ He dit el nom en veu alta
- ⬜ He dibuixat el que he après
```

### A1 — Inicial

Checklist de 3 ítems. Frases de 5-8 paraules en primera persona. Escala ✅/⬜ o Sí/No.

```markdown
## Comprovo el meu treball

- ⬜ He dit de qué tracta el text
- ⬜ He usat paraules del text
- ⬜ He connectat les idees amb *i*, *però*, *perquè*
```

### A2 — Funcional

Taula 3 criteris × 3 nivells (AS/AN/AE, sense NA). Descriptors curts i concrets.

### B1 — Estratègic

Taula 3-4 criteris × 4 nivells (NA/AS/AN/AE). Criteris de contingut + llengua + estructura.

```markdown
## Rúbrica d'assoliment

| Criteri | NA | AS | AN | AE |
|---|---|---|---|---|
| **Contingut** | No ho he fet | Ho he fet de forma bàsica | Ho he fet de forma clara | Ho he fet amb detalls i exemples propis |
| **Lèxic** | No n'he usat | N'he usat poc | N'he usat els principals | N'he usat tots i els he explicat |
| **Estructura** | No l'he seguit | N'he seguit alguns passos | L'he seguit gairebé tot | L'he seguit completament i l'he adaptat |
```

### B2 — Acadèmic

Taula 4 criteris × 4 nivells. Afegeix criteri de rigor acadèmic i evidències.

### C1 — Crític

Taula 4-5 criteris × 4 nivells. Afegeix criteri d'intencionalitat i contrast de fonts.

## Regles crítiques

**FER:**
- Descriptors en primera persona: "He fet...", "He usat...", "He explicat...".
- Descriptors observables i accionables: l'alumne sap exactament on se situa.
- AE = salt qualitatiu real (creativitat, autonomia, profunditat), no "fer-ne més".
- Nombre de criteris proporcional al MECR: 2-3 per A1-A2, màxim 5 per C1.
- Els descriptors han de fer referència al gènere i la tasca concrets.

**NO FER:**
- ❌ Descriptors abstractes: "qualitat", "adequat", "correcte" sense concretar qué significa.
- ❌ AE = "ha fet molt" o "ha fet tot" — AE és un salt qualitatiu, no quantitatiu.
- ❌ Generar rúbrica si no hi ha tasca de producció al context.
- ❌ Pre-A1/A1: taula de rúbrica — sempre checklist d'icones.
- ❌ Criteris que avaluïn el docent o el text, no la producció de l'alumne.

## Connexions MALL

- **Primera persona com a responsabilitat**: escriure la rúbrica en primera persona és un acte pedagògic. L'alumne no és avaluat "des de fora" sinó que s'autoavalua. La responsabilitat de la producció és seva.
- **Doble esmicolament com a competència de pensament**: dissenyar una rúbrica (identificar criteris + indicadors) és una competència metacognitiva d'alt ordre. Quan l'alumne co-dissenya la rúbrica (B1+), interioritza els criteris de qualitat del gènere.
- **AE com a model d'excel·lència**: la columna AE no és "fer-ne molt", és "fer-ne d'una manera que sorprèn positivament". Definir l'excel·lència clarament és donar a l'alumne un horitzó de qualitat aspiracional, no un estàndard de quantitat.

## Detecció

**Senyals docent**: ha activat el complement "Rúbrica d'assoliment" al Pas 2. Hi ha una tasca de producció derivada del text adaptat (escriure un text del gènere, respondre una pregunta oberta, fer una activitat d'aprofundiment).

**Senyals alumne**: no sap com sap si ho ha fet bé; no sap qué millorar; la coavaluació entre iguals no té criteris clars.

**Context favorable**: qualsevol tasca de producció escrita o oral on l'alumne necessiti autoavaluar-se. Especialment útil per a tasques de gènere (informe, crònica, ressenya) i per a activitats d'aprofundiment.

**Anti-senyals**: no hi ha tasca de producció → la rúbrica no té objecte; la tasca és un exercici tancat (completar buits, respondre preguntes de comprensió tancades) → preferir pauta d'interrogació.

## Heurístiques docent

**H1 — "Com sé que ho has fet?"**
Per a cada criteri, em faig la pregunta: "Com sé que l'alumne ha fet X?" La resposta és el descriptor observable. Si no puc respondre la pregunta, el criteri és massa abstracte i cal concretar.

**H2 — Co-dissenyar la rúbrica amb l'alumnat (B1+)**
Proposo que l'alumnat co-dissenyi els criteris: "Qué creieu que fa que un bon informe sigui un bon informe?" Les respostes dels alumnes son els criteris en primera persona. L'alumne que ha participat en definir la rúbrica la interioritza molt millor.

**H3 — La rúbrica com a guia de producció prèvia**
Proposo que l'alumne llegeixi la rúbrica ABANS d'escriure (no només al final). La rúbrica com a guia de producció és una bastida d'autoregulació. A B1+, l'alumne pot usar la rúbrica per planificar el seu text.

**H4 — AE: el cas excepcional**
Presento exemples concrets de produccions AE i AN a la classe. L'alumne ha de poder veure la diferència. Un informe AN explica els fets clarament. Un informe AE connecta els fets amb el context actual i aporta una perspectiva nova. Mostrar el contrast és ensenyar l'excel·lència.

## Autoavaluació (descriptors en primera persona)

*(Nota: la rúbrica és ella mateixa un instrument d'autoavaluació. Aquí es presenta l'autoavaluació de l'ús del complement, no de la producció.)*

- *Pre-A1/A1*: "He marcat les caselles del meu treball."
- *A2*: "He mirat la rúbrica i he vist en quin nivell estic."
- *B1*: "He llegit els descriptors i he identificat qué he de millorar."
- *B2*: "He usat la rúbrica per planificar la meva producció i per autoavaluar-la al final."
- *C1*: "He co-dissenyat els criteris i he usat la rúbrica per autoregular el meu procés d'escriptura."

## Fonts principals

- MALL (Model d'Aprenentatge de Llengües i Literacitat): metacognició, avaluació formativa integrada.
- Andrade, H. (2005): *Teaching with Rubrics* — descriptors en primera persona i autoavaluació.
- Black & Wiliam (1998): *Assessment for Learning* — feedback formatiu com a motor d'aprenentatge.
- FJE — Fundació Jesuïtes Educació: escala NA/AS/AN/AE, criteris de qualitat per etapa.
- Decret 175/2022 (currículum Catalunya): competència en comunicació lingüística, avaluació formativa.
