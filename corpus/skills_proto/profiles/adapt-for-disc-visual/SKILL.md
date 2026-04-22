---
name: adapt-for-disc-visual
description: >
  Use when adapting educational text for a student with visual
  impairment (baixa visió moderada/greu o ceguesa, ICD-11 9D90).
  Activates when the profile includes "discapacitat visual". Works
  across all MECR levels. Core principle: format adaptation, NOT
  content simplification. For the prompt LLM, guarantee semantic
  structure (H1-H3), descriptive alt-text for any mentioned visual
  element, and never depend on colour or position to convey meaning.
  Most adaptations are CSS/frontend (font size, contrast, zoom).
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
mecr_range: [A1, A2, B1, B2, C1]
agent_role: adapter
tools_required: []
subvariables:
  - grau: [baixa_visio_moderada, baixa_visio_greu, ceguesa]
triggers:
  - path: profile.caracteristiques.disc_visual.actiu
    equals: true
---

# Adaptar text per a alumnat amb discapacitat visual

## Quan activar aquesta skill
Activa aquesta skill quan l'adaptació de text sigui per a un alumne
amb discapacitat visual — baixa visió moderada (AV < 0,3), baixa visió
greu (AV < 0,12) o ceguesa (AV < 0,02 o sense percepció de llum).
Senyals: l'alumne s'acosta molt al material, fatiga visual en lectures
llargues, ús de lupa o ajudes òptiques, ús de Braille, necessitat de
lector de pantalla (JAWS/NVDA) o magnificador (ZoomText).

## Barrera nuclear
**Percepció visual.** L'alumnat amb discapacitat visual té com a
barrera principal l'accés a la informació presentada visualment. El
80-90% de la informació escolar es transmet per via visual (pissarra,
llibres, projeccions, gràfics). L'adaptació NO és de contingut: el
nivell d'exigència curricular no canvia. El que canvia és COM arriba
la informació. Les adaptacions per a l'LLM se centren en l'estructura
semàntica del text (encapçalaments, alt-text), ja que la majoria
d'adaptacions són CSS/frontend (contrast, mida, zoom).

## Instruccions principals d'adaptació

```
PERFIL: Discapacitat Visual
- Estructura semàntica amb encapçalaments (H1-H3) per lector de pantalla
- Alt-text descriptiu per a cada element visual mencionat
- NO dependre d'elements visuals (colors, posicions) per transmetre informació
```

## Mapa barrera → instruccions (prioritzat)

| Prioritat | Instruccions activades | Justificació (barrera) |
|---|---|---|
| **1a (percepció)** | H-18 (alt-text imatges), H-19 (estructura semàntica H1-H3), I-06 (contrast alt), I-08 (reescalat) | Barrera nuclear: percepció |
| **2a (estructura)** | B-02 (blocs amb títol), B-14 (taules per comparació) | Navegació amb lector de pantalla |
| **3a (referents)** | A-04 (referents explícits; evitar díctics "aquí", "això", "com veieu") | Invisibilitat de díctics i gestos |

**Nota**: La majoria d'adaptacions per a discapacitat visual són
CSS/FE (contrast, mida tipografia, zoom, suport a lector de pantalla),
no de prompt LLM. L'LLM ha de garantir: estructura semàntica,
descripcions textuals d'elements visuals, i no dependre de color o
posició per transmetre significat.

## Modulació per sub-variables

### Grau de discapacitat visual
- **Baixa visió moderada** (AV < 0,3): el text pot ser llegit
  directament amb ampliació (font 18-22pt, Arial o equivalent,
  contrast alt). L'estructura amb encapçalaments facilita la
  navegació amb magnificador. Alt-text concís per a cada element
  visual. Evitar paràgrafs densos (pausa visual freqüent).
- **Baixa visió greu** (AV < 0,12): estructura semàntica
  especialment rigorosa per a magnificador i/o lector de pantalla
  alternatius. Alt-text descriptiu complet — no "imatge d'una
  plana" sinó "fotografia d'una plana verda amb cinc glops
  d'aigua sobre les fulles". Preveure que la lectura és ~2x més
  lenta.
- **Ceguesa** (sense percepció de llum o AV < 0,02): el text es
  llegeix via Braille o lector de pantalla (JAWS, NVDA). TOTES les
  imatges, gràfics, taules i fórmules han de tenir equivalent
  textual descriptiu complet. Les taules han d'estar marcades
  semànticament (capçaleres, files). No usar "com es veu a la
  imatge" — substituir per "segons la descripció següent".
  Preveure que la lectura és ~3x més lenta (temps addicional).

## Exemple abans → després
Veure `assets/exemple-B1-celula.md` per a un exemple complet
d'adaptació d'un text de ciències naturals nivell B1 amb descripció
alternativa d'un esquema cel·lular.

## Carregar context més profund
Si calen fonaments pedagògics (classificació OMS/ICD-11, criteris
ONCE d'afiliació, tipologies i etiologies, rol del CREDV-ONCE i
protocol d'accés, tiflotecnologia (línia Braille, JAWS/NVDA,
ZoomText, anotador parlant), marc normatiu D150/2017 i Llei 17/2020,
verbalització sistemàtica a l'aula, autoadvocacia, distinció entre
DV i dificultats de comprensió lectora), carregar
`references/perfil-complet.md`. Si cal veure totes les fonts (OMS,
ONCE, CREDV, Decret 150/2017, Llei 17/2020, WCAG 2.1), carregar
`references/fonts.md`.
