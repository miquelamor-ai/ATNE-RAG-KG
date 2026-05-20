---
name: generar-illustracions
description: Instrument per afegir il·lustracions IA (FLUX) al text adaptat. Marcadors inline [IMATGE: concepte curt], 7 presets d'estil, màxim 3-4 per document. Backend Wikimedia+FLUX. Pre-A1/A1 preferir pictogrames. MECR pre-A1-C1. Correccions MALL 2026-05-17 aplicades.
type: instrument
categoria_principal: mediacio
categories_secundaries: []
mecr_range: [pre-A1, A1, A2, B1, B2, C1]
agent_roles: [generator]
translanguaging: false
multimodal: true
skill_meta: generate-illustracions@corpusFJE/skills/mediacio/generate-illustracions
version: 2.0.0-bootstrap
---

# Generar il·lustracions IA — V2 Descriptiu

## Descripció

El complement d'il·lustracions insereix imatges generades per IA al text adaptat per reforçar la comprensió de conceptes clau difícils de descriure verbalment. El LLM afegeix marcadors `[IMATGE: concepte curt en català]` en línia pròpia al text; el backend resol cada marcador en tres passos: Wikimedia Commons (cerca primer), FLUX.1-schnell (fallback), skip (si no és visualitzable).

**Feature BETA**: qualitat no garantida; demora de 1-3 minuts per imatge; el docent sempre pot substituir o regenerar.
**Principi MALL "menys és més"**: màxim 3-4 marcadors per document. Cada marcador afegeix càrrega cognitiva i demora de generació.
**Pre-A1/A1**: preferir pictogrames (emoji) que son instantanis. Les il·lustracions IA aporten valor quan el concepte és visual i complex (un procés, un sistema, un lloc).

## Els 7 presets d'estil

| Preset | Per a qui/quan |
|---|---|
| Aquarel·la storybook | Primària, LF, nouvinguts, literatura, A1-A2 |
| Vectorial editorial pla | ESO+, humanitats, conceptes abstractes, B1+ |
| Isomètric infogràfic | STEM, processos, sistemes, diagrames, A2+ |
| Icona minimalista | DUA Accés, vocabulari abstracte, glossari visual |
| Claymation plastilina | Primària STEM lúdic, infantil, A1-B1 |
| Escala de grisos (carbonet) | História, filosofia, impressió B/N, baixa visió |
| Fotografia documental | Natura, arquitectura, geografia, ciència actual |

El docent tria el preset al Pas 2; si no, el backend aplica el default per MECR + assignatura.

## Gradació per nivell MECR

### Pre-A1 — Emergent

1-2 marcadors màxim. Conceptes físics i observables: animals, persones, objectes quotidians. Mai conceptes abstractes. Coloca el marcador DAVANT del paràgraf que introdueix el concepte. Format: `[IMATGE: nena llegint un llibre]`.

### A1 — Inicial

2-3 marcadors màxim. Conceptes físics observables o processos simples (pluja, creixement). Un marcador per secció principal. Preset recomanat: aquarel·la storybook.

### A2 — Funcional

2-3 marcadors. Processos físics observables o elements d'un sistema. El concepte ha de ser difícil de descriure verbalment. Preset: aquarel·la o isomètric.

### B1 — Estratègic

2-4 marcadors. Pot incloure sistemes, mapes, línies de temps, relacions causa-efecte visibles. Mai conceptes purament verbals o abstractes. Preset: vectorial o isomètric.

### B2 — Acadèmic

1-3 marcadors, molt selectius. Il·lustrar processos o sistemes quan aporten valor real. No usar si el concepte és millor explicat verbalment. Preset: vectorial o fotografia documental.

### C1 — Crític

0-2 marcadors, opcionals. Imatge com a argument visual, no com a suport. Preset: vectorial editorial o fotografia documental.

## Format del marcador

```
[IMATGE: <concepte curt en català>]
```

- Delimitadors obligatoris: `[IMATGE:` a l'inici, `]` al final.
- Idioma: català. El backend tradueix si cal.
- En línia pròpia, DAVANT del paràgraf on s'introdueix el concepte.
- Longitud: 3-8 paraules. Concepte nuclear, no descripció d'escena.
- Mai dins de llistes, taules, bastides, glossaris o altres complements.
- Mai incloure estil, paleta, viewpoint o enquadrament (el backend ho afegeix).

## Regles crítiques

**FER:**
- Marcador en línia pròpia, davant del paràgraf corresponent.
- Concepte visualitzable i concret: lloc, objecte, escena, procés físic observable.
- Màxim 1 marcador per secció major (H2/H3).
- Preservar íntegrament el text adaptat; el marcador s'afegeix, no substitueix.
- En cas de dubte sobre si val la pena il·lustrar: NO posar el marcador.

**NO FER:**
- ❌ Conceptes purament abstractes: "la democràcia", "la justícia", "l'amor".
- ❌ Conceptes tècnic-microscòpics (cèl·lula, àtom, enzim) → formular a nivell macroscòpic ("fulla verda sota el sol").
- ❌ Marcadors en anglès o amb descripció d'estil.
- ❌ Més de 3-4 marcadors per document.
- ❌ Secció final amb llista de il·lustracions: els marcadors van inline.

## Connexions MALL

- **Imatge com a text a pre-A1/A1**: a nivells emergents, la il·lustració no decora el text, en fa les funcions. El principi "imatge a l'esquerra del text" (regla LF) és una bastida de descodificació: l'alumne veu el concepte abans de llegir la paraula.
- **Menys és més**: cada il·lustració afegeix càrrega cognitiva de processament visual. A B2-C1, una il·lustració sense valor informatiu addicional distrau en lloc d'ancorar.
- **Preset com a coherència de registre**: triar el preset adequat al context (aquarel·la per a primària, vectorial per a ESO) és una decisió pedagògica sobre el registre visual. Un poema il·lustrat amb infogràfic isomètric envia un missatge contradictori.

## Detecció

**Senyals docent**: ha activat el complement "Il·lustracions" al Pas 2. El text adaptat conté conceptes visuals que l'alumne pot no conèixer o que son difícils de representar verbalment.

**Senyals alumne**: no pot imaginar el referent d'un terme (mai ha vist un volcà, una balena, una fàbrica del s. XIX); la il·lustració facilitaria l'ancoratge del concepte.

**Context favorable**: ciències naturals (ecosistemes, òrgans), história (monuments, scenes histórics), geografía (paisatges, mapes de conceptes), educació artística (tècniques visuals).

**Anti-senyals**: el text és abstracte i verbal (filosofia, matemàtiques de càlcul) → pictograma o sense il·lustració; el concepte és tècnic-microscòpic → formular a escala macro o ometre.

## Heurístiques docent

**H1 — "Pots imaginar-ho?"**
Per a cada concepte del text, pregunto: "Pots imaginar una imatge d'aquest concepte?" Si la resposta és no, el marcador pot ajudar. Si és sí fàcilment, potser la il·lustració no afegeix valor.

**H2 — La il·lustració com a anticipació**
A pre-A1/A1, la il·lustració ha de venir DAVANT del text, no al darrere. L'alumne veu la imatge primer, activa el coneixement previ i llavors llegeix. L'ordre importa.

**H3 — El preset com a decisió pedagògica explícita**
Quan el docent tria el preset, ho fa com a decisió pedagògica. Explicar a la classe per qué s'ha triat aquarel·la per a un conte i vectorial per a un article de ciències és una lliçó de multimodalitat i de registre visual.

## Autoavaluació (descriptors en primera persona)

- *Pre-A1*: "He vist la imatge i he dit el que era." (oral)
- *A1*: "He mirat la imatge i m'ha ajudat a entendre la paraula difícil."
- *A2*: "La imatge m'ha ajudat a entendre el procés o el concepte."
- *B1*: "He identificat quins conceptes necessitaven imatge i quins no."
- *B2+*: "He usat les il·lustracions com a suport visual per a conceptes que no es poden explicar fàcilment amb paraules."

## Fonts principals

- MALL (Model d'Aprenentatge de Llengües i Literacitat): multimodalitat, principi "imatge a l'esquerra".
- Mayer, R.E. (2009): *Multimedia Learning* — principi de contiguïtat temporal i espacial imatge-text.
- Regles de Lectura Fàcil ATNE: imatge davant del text, un element visual per concepte clau.
- Decret 175/2022 (currículum Catalunya): competència en comunicació lingüística, dimensió multimodal.
