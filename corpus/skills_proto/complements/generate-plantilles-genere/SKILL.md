---
name: generate-plantilles-genere
description: >
  Use when the teacher has activated the "plantilles_genere" complement. Generates
  a partially completed text model of the target genre — a concrete example that
  shows the student what the finished product looks like, with some sections
  filled in and others left as guided blanks. Distinct from base d'orientació
  (which is a procedure/GPS): a plantilla is a CONCRETE PARTIAL TEXT to imitate.
  Modulated by MECR, genre, and subject.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
complement_key: plantilles_genere
agent_role: complements
tools_required: []
triggers:
  - path: params.complements.plantilles_genere
    equals: true
---

# Generar plantilla de gènere

## Distinció fonamental

| Instrument | Naturalesa | Exemple |
|---|---|---|
| **Base d'orientació** | Procediment (GPS): passos a seguir | "1. Escriu la pregunta. 2. Hipòtesi..." |
| **Plantilla de gènere** | Texto model parcial: mostra com queda | Un informe amb seccions completes i buits per omplir |
| **Textos model** | Text complet d'autor/a per analitzar | Un article real de divulgació científica |

La plantilla no és una base d'orientació en forma de taula: és un **text quasi complet**
on les seccions estructurals ja estan posades i alguns continguts clau es deixen oberts.
L'alumne veu la forma acabada i l'imita amb el contingut del text que ha llegit.

## Quan és útil

- Gèneres que l'alumne no ha treballat mai (primera exposició al gènere).
- Alumnat nouvingut o amb dificultats d'expressió que necessita un model concret.
- Qualsevol MECR: la plantilla canvia de densitat de forats, no de format.

## Principi cognitiu: descarregar la textualització

La plantilla actua a la **Fase 4 (Textualització)** de la SD. En aquest moment, l'alumne
ha d'activar simultàniament tres processos cognitius:

1. Recuperar el contingut (el que ha après del text)
2. Organitzar les idees (estructura del gènere)
3. Codificar en llengua nova (L2 o NESE)

La plantilla elimina la càrrega del pas (2) — l'estructura ja és donada — perquè l'alumne
pugui centrar-se en (1) i (3). **No és una drecera: és una bastida temporal** que es retira
quan l'alumne interioritza el gènere.

## Gradació per nivell MALL

| Nivell | Forats | Estructura |
|---|---|---|
| **Emergent (pre-A1)** | Cap text; plantilla visual (icones + línies puntejades per dibuixar) | 3-4 requadres amb icones que l'alumne pot dibuixar/enganxar |
| **Inicial (A1)** | 1-2 paraules per frase | Frases gairebé completes, només 1-2 buits per frase |
| **Funcional (A2)** | 3-5 buits per secció (paraules i frases curtes) | Seccions marcades amb títols, buits moderats |
| **Estratègic (B1)** | Paràgrafs amb l'inici donat i continuació oberta | L'estructura és donada; el contingut és propi |
| **Acadèmic (B2)** | Plantilla minimalista: encapçalaments + 1 frase d'exemple per secció | Model de referència, no de còpia |
| **Crític (C1)** | Criteris de gènere i estil sense text de suport | Rúbrica de gènere per autoregulació |

## Format de sortida (exemple: crònica, B1)

```markdown
## Plantilla: Crònica històrica

**Títol**: [Escriu aquí un títol que indiqui el fet i el moment]

**Situació inicial** *(Qui? Quan? On?)*
L'any ___________, a ___________, ___________ [personatge o grup] es trobava...

**Desenvolupament** *(Què va passar? En quin ordre?)*
En primer lloc, ___________________________________________.
Després, _______________________________________________.
Finalment, _____________________________________________.

**Causes** *(Per què va passar?)*
Això va ocórrer perquè ___________________________________.

**Conseqüències** *(Quin impacte va tenir?)*
Com a resultat, _________________________________________.

**Valoració** *(Per què és important recordar-ho?)*
Aquest fet és rellevant perquè ___________________________.
```

## Format Emergent (pre-A1)

```markdown
## El meu text amb imatges

[Requadre 1 🖼️] El text parla de: *(dibuixa o enganxa)*
[Requadre 2 🖼️] El més important és: *(dibuixa o enganxa)*
[Requadre 3 🖼️] Al final passa: *(dibuixa o enganxa)*
```

## Regles estrictes de sortida

- Comença **sempre** amb `## Plantilla: [nom del gènere]`.
- Infereix el gènere del text original. Si no és explícit, dedueix-lo del contingut.
- Els buits han de ser **específics del text** (no genèrics): fan referència als personatges, fets, conceptes o arguments reals del text adaptat.
- **NO** és un text model complet — ha de tenir forats. Un text model sense forats no és una bastida.
- **NO** repeteixis la base d'orientació en forma de taula: la plantilla és TEXT, no passos.
- Pre-A1: cap lletra manuscrita. Icones, requadres per dibuixar, o opcions per enganxar.
- La plantilla ha de ser **completable en 15-20 minuts** com a màxim.
- Adapta el registre al gènere (formal per a informe/article; narratiu per a conte/crònica).
