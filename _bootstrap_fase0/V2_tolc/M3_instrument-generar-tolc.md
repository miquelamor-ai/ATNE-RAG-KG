---
name: generar-tolc
description: Instrument per generar un bloc de Transllenguatge/TOLC. Usa la L1 de l'alumne nouvingut com a pont cognitiu cap al català. Taula bilingüe L1↔català + observació estructural + consigna de transferència. PBCS per a alternança estratègica de codis. Pre-A1 oral. Correccions MALL 2026-05-17 aplicades.
type: instrument
categoria_principal: mediacio
categories_secundaries: []
mecr_range: [pre-A1, A1, A2, B1, B2, C1]
agent_roles: [adapter, generator]
translanguaging: true
multimodal: true
skill_meta: generate-tolc@corpusFJE/skills/mediacio/generate-tolc
version: 2.0.0-bootstrap
---

# Generar Transllenguatge / TOLC — V2 Descriptiu

## Descripció

El TOLC (Transllenguatge per a Altres Contextos d'Aprenentatge) usa la **traducció activa** com a eina pedagògica: no és un glossari, és una comparació que fa visible com dues llengües codifiquen el mateix concepte. L'objectiu és activar el coneixement previ de l'alumne en L1 i construir un pont cap al català, reduint la càrrega cognitiva doble (aprendre el concepte i la paraula simultàniament).

**Tipologia MALL**: Mediació metalingüística (pont cognitiu L1 → L2)
**Condició necessària**: perfil nouvingut actiu amb L1 coneguda. Si la L1 no és coneguda, generar únicament el bloc PBCS genèric.
**Dos instruments integrats**:
- **TOLC** (Translation for Other Learning Contexts): compara activament L1 i català, fa visible la semblança i la diferència.
- **PBCS** (Pedagogically-Based Code Switching): alternança estratègica de codis dissenyada; el material indica explícitament quan canviar de llengua i per a quina funció. No és espontani.

**Diferència clau**: TOLC **tradueix i compara**; PBCS **alterna per consciència metalingüística**.

## Estructura canònica — 3 moments

Tot bloc TOLC té **3 moments encadenats**:

1. **Activació** — ancorar el concepte clau en L1 (pregunta comparativa).
2. **Acarament** — requadre de contrast L1 ↔ català (estructura visible).
3. **Transferència** — consigna de producció (oral o escrita, segons MECR).

## Formats validats (MALL)

| Format | Quan usar |
|---|---|
| **Taula bilingüe** (A1+) | Comparació parell a parell L1↔català. Format base. |
| **Dictat bilingüe** | L'alumne dicta en L1 el que ha entès; el docent o company escriu en català. |
| **Col·lage lingüístic** | Text que integra expressions en L1 i català de forma planificada. |
| **Language Identity Texts (LIT)** | L'alumne crea un text (poema, relat, presentació) que integra L1 i L2 alhora. Especialment potent a Primària i ESO. |

## Modulació per nivell MECR

### Pre-A1 — Emergent

**Cap escriptura autònoma.** El TOLC és oral i gestual: "Com es diu [paraula clau] en la teva llengua? Dibuixa o assenyala la imatge mentre ho dius." El docent fa el recast en català. El bloc generat és una instrucció per al docent, no per a l'alumne.

### A1 — Inicial

Taula de 3-5 parells L1 ↔ català (paraula en alfabet original de la L1). Observació estructural d'1 frase molt senzilla sobre semblances. Consigna de transferència: dictat a l'adult o assenyalar.

### A2 — Funcional

Taula bilingüe + 1 frase de contrast estructural (p.ex. ordre subjecte-verb si difereix). Consigna de transferència: 1 frase curta en L1 → traduir al català usant connectors del text. Pot incloure una observació sobre falsos amics si n'hi ha.

### B1 — Estratègic

Contrast de connectors i construccions causals entre L1 i català. PBCS: consigna de mediació epistèmica (resumir en una llengua un text de l'altra). Consigna de transferència: paràgraf breu. Pot incloure diferències en l'estructura de la frase o l'ús de la passiva.

### B2 / C1 — Acadèmic / Crític

Contrast de gèneres entre L1 i català (com s'argumenta en cada cultura escrita, diferències discursives). Mediació complexa: text complet de síntesi que integra les dues llengües. Reflexió metalingüística explícita: "Per qué creus que en [L1] s'usa [construcció] on en català s'usa [construcció]?"

## Regles crítiques

**FER:**
- Usar sempre l'**alfabet original** de la L1: àrab الكتاب, xinès 书, urdú کتاب, ciríl·lic книга, armeni գիրք.
- Comença sempre amb `## Connexió amb la teva llengua`.
- L'observació estructural ha de ser **positiva**: semblances primer, diferències com a curiositat.
- La consigna de transferència ha de ser voluntària ("si vols", "si pots"): no exposar l'alumne.
- Màxim 3-5 parells a la taula: no sobrecarregar.
- Si L1 sense equivalència exacta: paraula més propera + "(semblant)" entre parèntesis.

**NO FER:**
- ❌ Pre-A1: cap escriptura autònoma. El bloc és per al docent.
- ❌ Generar si `nouvingut.actiu = false`: retornar advertència al docent.
- ❌ Exposar l'alumne: no forçar-lo a parlar de la seva L1 davant la classe.
- ❌ Observació negativa ("en àrab l'ordre és l'invers i per això us equivoqueu...").
- ❌ Confondre TOLC (comparació activa) amb glossari bilingüe (llista sense comparació).

## Connexions MALL

- **Translanguaging (Cummins)**: el TOLC implementa el TOLC (Transfer of Literacy and Cognition) de Cummins. La hipòtesi de la interdependència: si la competència en L1 és alta, el transfer a L2 és més ràpid i profund.
- **BICS → CALP**: el pont L1 permet que l'alumne accedeixi al CALP en L2 sense perdre el fil conceptual. El concepte ja existeix en L1; el TOLC dona la paraula en L2.
- **Identitat lingüística**: els Language Identity Texts (LIT) van més enllà de la bastida: reconeixen la L1 com a recurs cultural i identitari, no com a obstacle.
- **Multimodalitat**: a pre-A1, el gest i el dibuix substitueixen l'escriptura. La L1 oral és el punt d'ancoratge.

## Detecció

**Senyals docent** (quan activar TOLC):
- Hi ha alumnat nouvingut a l'aula amb L1 coneguda i nivell MECR A1-B1.
- El text conté conceptes que l'alumne probablement coneix en L1 però no en català.
- L'alumne mostra confusió de conceptes (no de paraules): el TOLC aclareix si el concepte és nou o si és familiar en una altra llengua.
- La matèria és de contingut (TILC): l'alumne ha d'aprendre simultàniament concepte i paraula.

**Senyals alumne** (que indica que necessita TOLC):
- Diu "no sé" però quan li preguntes en L1 demostra que sí sap el concepte.
- Barreja paraules de L1 i L2 en la mateixa frase (code-switching espontani no estratègic).
- Tradueix literalment de L1 i la traducció és incorrecta en català (interferència).
- S'atura davant un terme tècnic que molt probablement coneix en L1.
- Nouvingut recent (menys de 6 mesos): tota la càrrega cognitiva és doble.

**Context favorable**:
- Aula d'acollida o grup amb nouvinguts recents.
- Text de ciències, matemàtiques o socials (TILC) amb conceptes curriculars.
- Primers 3 mesos d'escolarització: el TOLC és quasi obligatori per evitar la càrrega cognitiva doble.
- L'alumne té alta competència en L1 (alfabetitzat, CALP en L1 consolidat): el transfer és molt ràpid.

**Anti-senyals** (quan NO activar):
- L1 desconeguda: generar únicament PBCS genèric sense taula bilingüe.
- Alumne no nouvingut (català com a L1 o L2 molt consolidad): el TOLC no aporta valor.
- Text molt curt on el vocabulari es pot explicar oralment en 2 minuts.

## Heurístiques docent

**H1 — "Saps com es diu això en la teva llengua?" com a diagnòstic**
Quan un alumne nouvingut diu "no sé" davant un concepte, li pregunto en la seva llengua (o li demano que escrigui la paraula). Si respon sense dubtar, el problema NO és conceptual sinó lèxic en L2. El TOLC resol exactament això: dóna la paraula en català per a un concepte que l'alumne ja té.

**H2 — L'alfabet original com a respecte**
Escriure el terme en àrab, xinès o urdú amb el seu alfabet original no és decoració: és un missatge de reconeixement. L'alumne veu que la seva llengua cap a la pissarra, al material, a l'escola. L'efecte sobre la motivació i la percepció d'inclusió és mesurable i consistent a la literatura.

**H3 — El transfer cap a B1**
A B1, el TOLC passa de comparar paraules a comparar estructures: "En àrab, la frase causal es fa diferent..." Aquesta reflexió metalingüística accelera la adquisició perquè l'alumne entén per qué ha de canviar, no només qué ha de canviar. És la diferència entre aprendre una regla i entendre-la.

**H4 — LIT per a alumnes AACC nouvinguts**
Per a alumnat nouvingut d'altes capacitats, els Language Identity Texts (LIT) son especialment potents: creen un producte complex (poema bilingüe, relat en dues veus) que demostra el nivell cognitiu real per sobre del nivell lingüístic en L2. Evita la subestimació de l'alumne i el frustrant "ha de passar per A1 primer".

**H5 — La consigna voluntària, sempre**
Mai "Digues-nos com es diu en la teva llengua": és una exposició no consentida. Sempre "si vols i pots, pots compartir com es diu en la teva llengua." La diferència entre les dues consignes és la diferència entre inclusió i tokenisme. L'alumne nouvingut no és el representant de la seva cultura lingüística.

## Autoavaluació (descriptors en primera persona)

- *Pre-A1*: "He dit com es diu [paraula] en la meva llengua." (oral)
- *A1*: "He vist les paraules en la meva llengua i en català. Les reconec."
- *A2*: "He escrit una frase en la meva llengua i l'he traduïda al català."
- *B1*: "He explicat una part del text en la meva llengua i llavors en català."
- *B2*: "He reflexionat sobre com les dues llengües organitzen les idees de manera diferent."
- *C1*: "He analitzat les diferències discursives entre la meva L1 i el català en aquest gènere."

## Fonts principals

- Cummins (2000): TOLC (Transfer of Literacy and Cognition) i hipòtesi de la interdependència.
- Cummins & Early (2011): Identity Texts — Language Identity Texts com a eina d'inclusió.
- García & Wei (2014): Translanguaging: language, bilingualism and education.
- MALL (Model d'Aprenentatge de Llengües i Literacitat): PBCS, mediació epistèmica, pont L1-L2.
- Decret 175/2022 (currículum Catalunya): plurilingüisme i translanguaging com a competència.
