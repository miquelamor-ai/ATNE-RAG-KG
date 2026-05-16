---
name: generate-mapa-conceptual
description: >
  Use when the teacher has activated the "mapa_conceptual" complement.
  Generates a visual organiser adapted to MECR level: at pre-A1/A1 a simple
  visual schema (2-4 nodes, image→word or parts of a whole); from A2 a
  hierarchical concept map in structured markdown (central concept + branches
  + sub-elements). Output is NOT ASCII-art. Can be copy-pasted into Canva,
  MindMeister, XMind, Word SmartArt.
author: FJE — Fundació Jesuïtes Educació
version: 2.0.0-proto
complement_key: mapa_conceptual
agent_role: complements
tools_required: []
triggers:
  - path: params.complements.mapa_conceptual
    equals: true
---

# Generar mapa conceptual / esquema visual

## Distinció fonamental (MALL)

El MALL distingeix dues eines amb funcions diferents:

- **Esquema visual** (funció instrumental/executiva): seqüències temporals,
  parts d'un tot, ordenació. Adequat des de pre-A1.
- **Mapa conceptual jeràrquic** (funció epistèmica — «llegir per aprendre»):
  reorganitza el coneixement en categories i relacions lògiques. Comença a **A2**.

Aquesta skill genera l'eina adequada per al MECR de l'alumne.

## Gradació per nivell MALL

| Nivell | Eina | Nodes / Nivells | Característiques |
|---|---|---|---|
| **Emergent (pre-A1)** | Esquema visual | 2-3 nodes | Imatge → paraula, o seqüència antes/després. Màxim concreció visual |
| **Inicial (A1)** | Esquema visual | 3-4 nodes | Parts d'un tot o qualitats simples d'un objecte. Molt guiat |
| **Funcional (A2)** | Mapa conceptual | **2 nivells** | Concepte central → idees principals literals. Primera introducció guiada |
| **Estratègic (B1)** | Mapa conceptual | **3 nivells** | Concepte → categories → detalls inferits. Connectors lògics a les fletxes |
| **Acadèmic (B2)** | Mapa conceptual | **4+ nivells** | Superestructura del gènere. Lèxic CALP. Relacions abstractes |
| **Crític (C1)** | Mapa de contrast | 2 columnes | Comparació de fonts o ideologies. «Rere les línies» |

## Principi: text jeràrquic útil, no ASCII-art

**L'objectiu NO és dibuixar** un diagrama amb fletxes ASCII, caixes o emojis.
**L'objectiu SÍ és** una **jerarquia estructurada en markdown** que:
- Es llegeix directament com a guia d'estudi.
- Es copia a Canva, MindMeister, XMind, Word SmartArt amb mínima edició.
- S'exporta a PDF sense renderitzadors especials.

## Regles per construir el mapa

- **Concepte central**: 1 terme nuclear del text, en negreta.
- **Branques principals**: 3-5 categories (causes, conseqüències, tipus, processos...).
- **Sub-elements**: conceptes o entitats curtes, no frases explicatives.
- **Branques = relacions clares** («Causes», no «Informació»).
- Termes del **text adaptat**, no inventats.
- **No repetir** el mateix concepte a múltiples branques.

## Format de sortida — OBLIGATORI

**Esquema visual (pre-A1/A1):**
```markdown
## Esquema visual

**[concepte o personatge central]**

- [element 1] → [element 2]
- [part/qualitat 1]
- [part/qualitat 2]
- [part/qualitat 3]
```

**Mapa conceptual (A2+):**
```markdown
## Mapa conceptual

**Concepte central**: [terme nuclear del text]

- **[Branca 1 — relació/categoria]**
  - [Sub-element 1.1]
  - [Sub-element 1.2]
- **[Branca 2 — relació/categoria]**
  - [Sub-element 2.1]
  - [Sub-element 2.2]
- **[Branca 3 — relació/categoria]**
  - [Sub-element 3.1]
  - [Sub-element 3.2]
```

**Opcional** al final (A2+):
```markdown
> Aquest mapa es pot enganxar a MindMeister, Canva o XMind per convertir-lo en diagrama visual.
```

## Regles estrictes de sortida

- Pre-A1/A1: comença amb `## Esquema visual`.
- A2+: comença amb `## Mapa conceptual`.
- **Sempre** etiquetar les branques en negreta.
- **NO** fletxes ASCII (→ és acceptable com a connector, no com a estructura).
- **NO** caixes ASCII (│├└), no emojis decoratius.
- **NO** sub-elements com a frases llargues.
- **NO** conceptes no presents al text adaptat.
- **NO** superar 3 nivells de sagnia (profunditat limitada).

## Casos especials

### Text narratiu (conte, relat)
- Concepte central: tema o idea nuclear (no «El conte»).
- Branques: personatges, espai-temps, conflicte, resolució, missatge.

### Text poètic
- Concepte central: tema nuclear.
- Branques: camps semàntics, imatges, emocions, recursos recurrents.

### Si el docent ha activat «esquema visual» i «mapa conceptual» alhora
Genera una sola secció (`## Mapa conceptual` a A2+, `## Esquema visual` a A1).

## Exemple
Veure `assets/exemple-historia-B1.md` (Revolució Industrial, ESO 3r) i
`assets/exemple-ciencies-A2.md` (fotosíntesi, Primària Superior).
