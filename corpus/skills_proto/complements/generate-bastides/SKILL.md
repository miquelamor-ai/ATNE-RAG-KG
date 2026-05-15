---
name: generate-bastides
description: >
  Use when the teacher has activated the "bastides" complement. Generates
  scaffolding supports for the student that cover the full reading process
  (pre-reading, during, post-reading) and, when production tasks exist
  (preguntes_comprensio or activitats_aprofundiment), also production
  scaffolds (connectors + sentence frames + key vocabulary). Language
  adapts to the student's MECR level: simple/visual for A1-A2, more
  technical for B1+. L1 support (translation/transliteration) is delegated
  to the Glossari complement, not duplicated here. Visual layout
  suggestions for the teacher go to "Notes d'auditoria", not to the
  student-facing output.
author: FJE — Fundació Jesuïtes Educació
version: 2.0.0-proto
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
---

# Generar bastides (scaffolding) — v2

## Què són les bastides en aquest context

**Bastides = ajudes perquè l'alumne realitzi una tasca** que sense suport no
podria fer. Segueix el principi de Vygotsky (Zona de Desenvolupament Pròxim)
i el model DUA/Cummins/MALL-TILC.

ATNE distingeix **dos tipus de bastides** dins d'aquest complement:

1. **Bastides de LECTURA** — sempre activades quan el complement està actiu.
   Ajuden l'alumne a llegir el text amb estratègia, no només a desxifrar.

2. **Bastides de RESPOSTA** — només si hi ha tasca de producció activada
   (preguntes_comprensio o activitats_aprofundiment). Ajuden l'alumne a
   formular respostes orals o escrites amb estructura.

> **Nota important sobre nomenclatura**: pedagògicament *tots* els
> complements d'ATNE (glossari, esquemes, mapes, preguntes, pictogrames,
> etc.) són **bastides** en sentit ampli (Vygotsky/Bruner). Aquest
> complement específic les anomena «bastides» com a abreviació històrica de
> «bastides lingüístiques i lectores», ja que és el que aporta al sistema
> en lloc del que ja cobreixen els altres complements. Es preveu una
> renominació al post-pilot.

## Dependència amb altres complements

| Complement | Relació amb bastides |
|---|---|
| **Preguntes de comprensió** | Si actiu → s'inclouen bastides de resposta (connectors, frases model). Si no → només bastides de lectura. |
| **Activitats d'aprofundiment** | Mateixa relació que preguntes. |
| **Glossari** | Si l'alumne és nouvingut, el glossari ja inclou traducció L1 i transliteració. Per això les bastides NO repeteixen aquesta info. |

## Llenguatge segons MECR

El llenguatge dels títols i etiquetes ha de ser **comprensible per l'alumne**,
no per al docent. Adaptació obligatòria:

| MECR | Tractament |
|---|---|
| pre-A1, A1, A2 | Títol "**Eines per llegir i respondre**". Emojis i visuals. Frases molt curtes (<10 paraules). EVITAR termes tècnics: «scaffolding», «connectors lògics», «patró lingüístic», «MALL/TILC». |
| B1, B2 | Títol "**Bastides (ajudes per llegir i respondre)**". Llenguatge clar però pot contenir terminologia bàsica. |
| C1, C2 | Termes tècnics permesos (l'alumne ja té vocabulari metalingüístic). |

## Estructura de sortida

### Sempre presents (bastides de LECTURA)

```markdown
## [Eines per llegir i respondre | Bastides (ajudes per llegir i respondre)]

### CONTEXT
- Matèria: [matèria]
- Etapa: [etapa] · MECR: [nivell]

### 📖 Abans de llegir
- Pregunta d'activació de coneixements previs
- Predicció a partir del títol
- Propòsit clar de la lectura

### 🔍 Durant la lectura
- Què subratllar (1-2 tipus d'informació clau)
- Com prendre nota al marge (ex: ✓ entès / ? dubte / ! important)
- Idea principal per paràgraf en 1 paraula

### 📝 Després de llegir
- Resum en 1 frase amb buit per completar
- Idea principal vs detalls
- Connexió amb la vida pròpia
```

### Condicionals (bastides de RESPOSTA, només si preguntes o activitats)

```markdown
### 🔗 Connectors per respondre
[Taula adaptada al MECR amb 5 funcions: causa, conseqüència, contrast, exemple, conclusió]

### ✏️ Frases per començar la resposta
[4-5 inicis de frase amb forats per completar]

### 🗂️ Paraules clau del text
[6-10 paraules del text, marcant amb (T) les tècniques]
```

### Si no hi ha tasca de producció

Substituir bastides de resposta per missatge:
> **Recomanació**: No hi ha preguntes ni activitats actives. Per generar
> bastides de resposta (connectors + frases model), activa també el
> complement «Preguntes de comprensió» o «Activitats d'aprofundiment».

## Què s'elimina respecte a la v1

| Bloc v1 | Acció v2 | Motiu |
|---|---|---|
| 6. Suport L1 (traducció a llengua materna) | **Eliminat** | Duplicat amb el complement Glossari (que ja inclou L1) |
| 4. Suport visual recomanat (icones al docent) | **Mogut** a Notes d'auditoria | És info pel docent, no per a l'alumne |
| Etiquetes tècniques sense modulació MECR | **Adaptades** segons nivell | Inintel·ligible per a A1-A2 |

## Adequació per etapa educativa

Modula el contingut segons l'etapa (no només el MECR):

- **Infantil / Cicle Inicial**: pre-lectura amb dibuixos, durant amb símbols
  visuals (✓ ?), després amb dibuix a mà.
- **Cicle Mitjà / Superior / ESO**: estratègies procedimentals (esquemes,
  taules, plantilles de resposta).
- **Batxillerat / FP**: síntesi, anàlisi crítica de múltiples fonts,
  argumentació amb tesi/antítesi.

## Regles estrictes

- **SEMPRE** generar les 3 fases de lectura (abans/durant/després).
- **CONDICIONAL** les bastides de resposta segons preguntes/activitats.
- **MAI** repetir suport L1 (ja és al glossari).
- **MAI** posar suggeriments visuals al docent dins de les bastides (van
  a Notes d'auditoria).
- **NO** donar respostes: l'alumne ha de completar tot.
- Modular complexitat lingüística segons MECR (especialment a A1-A2).

## Exemple

Veure `assets/exemple-ciencies-B1.md` (text informatiu, ESO 3r, MECR B1).
*Nota: l'exemple v1 cal actualitzar a v2 (post-pilot).*
