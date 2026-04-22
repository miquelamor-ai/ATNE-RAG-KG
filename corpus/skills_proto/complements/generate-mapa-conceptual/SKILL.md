---
name: generate-mapa-conceptual
description: >
  Use when the teacher has activated the "mapa_conceptual" complement.
  Generates a hierarchical concept map in structured markdown (central concept
  + branches + sub-elements) that is directly useful as a study guide and can
  be copy-pasted into any external diagramming tool (Canva, MindMeister,
  XMind, Word SmartArt). Output is NOT ASCII-art; it's a purposeful
  pedagogical document.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
complement_key: mapa_conceptual
agent_role: complements
tools_required: []
triggers:
  - path: params.complements.mapa_conceptual
    equals: true
---

# Generar mapa conceptual

## Quan activar aquesta skill
Activar quan el docent ha marcat el complement **"Mapa conceptual"** al Pas 2.

## Principi: text jeràrquic útil, no ASCII-art

**L'objectiu NO és dibuixar** un diagrama amb fletxes ASCII, caixes de text o
emojis. Aquest format és soroll visual per a alumnat amb TEA/dislèxia i
inutilitzable per al docent.

**L'objectiu SÍ és** generar una **jerarquia estructurada en markdown** que:

1. **Es pot llegir com a guia d'estudi** directament (sense cap eina extra).
2. **Es pot projectar o imprimir** tal qual.
3. **Es pot copiar-enganxar** a qualsevol eina de mapes mentals/conceptuals
   (Canva, MindMeister, XMind, SimpleMind, Coggle, Word SmartArt) i el diagrama
   es fa automàticament o amb mínima edició.
4. **Es pot exportar a PDF** sense renderitzadors especials.

## Regles per construir el mapa

### Estructura obligatòria

- **Concepte central**: 1 concepte clau del text, amb èmfasi (**negreta**).
- **Branques principals**: 3-5 categories que relacionen conceptes amb el
  central (ex. causes, conseqüències, tipus, exemples, processos).
- **Sub-elements**: 2-4 per branca, termes o frases curtes.

Profunditat màxima: **2 nivells de sub-elements** (no més de 3 nivells de
sagnia). Un mapa amb 5 nivells és un esquema, no un mapa.

### Qualitat pedagògica

- **Els sub-elements han de ser conceptes o entitats**, no frases explicatives
  llargues. Un mapa conceptual **és de conceptes**, no un resum en viñetes.
- **Les branques han de representar RELACIONS clares** (p.ex. "Causes", no
  "Informació"; "Conseqüències socials", no "Altres dades").
- Els termes han de provenir del **text adaptat**, no inventar-los.
- **No repetir** el mateix concepte a múltiples branques.

### Modulació per MECR i etapa

| Nivell | Profunditat | Nombre branques | Sub-elements per branca |
|---|---|---|---|
| A1 | 1 nivell | 2-3 | 2 |
| A2 | 1-2 nivells | 3-4 | 2-3 |
| B1 | 2 nivells | 3-4 | 3-4 |
| B2-C1 | 2 nivells | 4-5 | 3-4 |

A etapes inicials (Infantil, Cicle Inicial): 2-3 branques màxim, termes
concrets i propers. A Batxillerat: més branques i relacions conceptuals
abstractes.

## Format de sortida — OBLIGATORI

La secció comença SEMPRE amb `## Mapa conceptual` i segueix aquesta
estructura:

```markdown
## Mapa conceptual

**Concepte central**: [terme nuclear del text]

- **[Branca 1 — relació/categoria]**
  - [Sub-element 1.1]
  - [Sub-element 1.2]
  - [Sub-element 1.3]
- **[Branca 2 — relació/categoria]**
  - [Sub-element 2.1]
  - [Sub-element 2.2]
- **[Branca 3 — relació/categoria]**
  - [Sub-element 3.1]
  - [Sub-element 3.2]
```

**Opcional, al final**, afegir una línia que indiqui com usar-lo:

```markdown
> Aquest mapa es pot enganxar directament a una eina de diagrames
> (MindMeister, Canva, XMind…) per convertir-lo en un mapa visual.
```

## Regles estrictes de la sortida

- **SEMPRE** començar amb `## Mapa conceptual` (secció top-level del parser).
- **SEMPRE** etiquetar les branques amb **negreta** (`- **Branca**`).
- **NO** usar fletxes (→, ↓), no usar caixes ASCII (│├└), no usar emojis
  decoratius. Pots usar emojis si aporten (p.ex. ☀️ al costat de "llum
  solar"), però com a reforç del concepte, no com a decoració.
- **NO** escriure explicacions llargues als sub-elements; han de ser
  conceptes/entitats curtes.
- **NO** inventar conceptes que no siguin al text adaptat.
- **NO** superar 3 nivells de sagnia en cap cas.

## Casos especials

### Si el text és narratiu (conte, relat)
Els mapes conceptuals no sempre tenen sentit per narrativa pura. En aquest cas:
- Concepte central: el tema o la idea nuclear del relat (no "El conte").
- Branques: personatges, espai-temps, conflicte, resolució, tema/missatge.
- Sub-elements: conceptes concrets (no "passos de la trama").

### Si el text és poètic
Genera un mapa **temàtic**, no narratiu:
- Concepte central: el tema nuclear.
- Branques: camps semàntics, imatges, emocions, recursos recurrents.

### Si el docent també ha activat "mapa mental" o "esquema visual"
Pots generar una sola secció `## Mapa conceptual` — aquests 3 complements
tenen el mateix output en el MVP actual. No duplicar seccions.

## Exemple
Veure `assets/exemple-historia-B1.md` (Revolució Industrial, ESO 3r) i
`assets/exemple-ciencies-A2.md` (fotosíntesi, Primària Superior).
