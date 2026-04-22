---
name: adapt-for-nouvingut
description: >
  Use when adapting educational text for a newly arrived student (alumnat
  nouvingut) acquiring Catalan as L2. Activates when the profile includes
  "nouvingut" or recent incorporation to the Catalan school system. Works
  mainly at pre-A1, A1, A2, B1. Core output principles: frequent
  vocabulary, cultural scaffolding, bilingual glossary, visual redundancy.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
mecr_range: [A1, A2, B1, B2]
agent_role: adapter
tools_required: []
subvariables:
  - L1: [text lliure]
  - familia_linguistica: [romanica, germanica, eslava, araboberber, sinotibetana, altra]
  - alfabet_llati: bool
  - escolaritzacio_previa: [si, parcial, no]
  - mecr: [pre-A1, A1, A2, B1, B2]
  - calp: [inicial, emergent, consolidat]
triggers:
  - path: profile.caracteristiques.nouvingut.actiu
    equals: true
---

# Adaptar text per a alumnat nouvingut

## Quan activar aquesta skill
Activa aquesta skill quan l'adaptació de text sigui per a un alumne
nouvingut que s'ha incorporat recentment al sistema educatiu català (en
els darrers 24-36 mesos) i està adquirint el català com a L2. Senyals:
competència lingüística en català limitada, llacunes en referents
culturals locals, dificultat amb textos acadèmics malgrat fluïdesa
conversacional.

## Barrera nuclear
**Lèxica i cultural.** La comprensió lèxica en L2 (vocabulari en català) i
els referents culturals locals que l'alumne desconeix són la doble barrera
principal. La distància lingüística entre L1 i català amplifica la
dificultat: no és el mateix adaptar un text per a un alumne amb L1
romànica que per a un amb L1 sino-tibetana o araboberber.

## Instruccions principals d'adaptació

```
PERFIL: Nouvingut
- Referents culturals: substitueix locals per universals o explica breument
- Glossari bilingüe amb traducció a L1 (al final)
- Suport visual: la comprensió visual no depèn de L2
- Redundància modal: text + imatge + esquema
- NO pressuposar coneixement cultural local
```

## Mapa barrera → instruccions (prioritzat)

| Prioritat | Instruccions activades | Justificació (barrera) |
|---|---|---|
| **1a (lèxica)** | A-01 (vocab freqüent), A-02 (termes en negreta), A-04 (referents explícits), A-05 (eliminar idiomàtiques), A-06 (eliminar polisèmia), A-20 (control densitat lèxica), A-21 (descomposició compostos) | Barrera nuclear: comprensió lèxica |
| **2a (cultural)** | E-08 (referents culturalment diversos), E-09 (evitar suposits culturals), E-10 (sensibilitat temes), G-01 (glossari bilingüe), G-05 (substitució referents) | Barrera cultural |
| **3a (sintàctica)** | A-07 (una idea per frase), A-09 (subjecte explícit), A-12 (limitació longitud frase), A-13 (eliminació subordinades), A-24 (present indicatiu), A-25 (formes verbals simples) | Barrera sintàctica |
| **4a (estructura)** | B-01 (paràgrafs curts), B-02 (blocs amb títol), B-07 (resum anticipatiu), C-05 (glossari previ Sweller), C-08 (anticipació vocabulari) | Suport discursiu |

## Modulació per sub-variables

### L1 (llengua materna) i família lingüística
- **Romànica** (castellà, francès, italià, romanès, portuguès): alta
  transferència lèxica positiva. Es pot confiar en cognats amb moderació
  i advertir dels "falsos amics".
- **Germànica** (anglès, alemany): transferència moderada, sobretot en
  vocabulari acadèmic (mots cultes llatins compartits).
- **Eslava** (rus, ucraïnès, polonès): distància lèxica alta, però
  alfabet llatí si l'alumne el té adquirit. Suport visual reforçat.
- **Araboberber** (àrab, amazic): distància lèxica i d'alfabet. Glossari
  bilingüe obligatori. Direcció de lectura a considerar si hi ha
  activitats bidireccionals.
- **Sinotibetana** (xinès, tibetà): màxima distància estructural (tons,
  morfologia, escriptura logogràfica). Glossari bilingüe obligatori,
  suport visual màxim, text mínim.
- **Altra**: aplicar criteri conservador (màxim suport).

### Alfabet llatí
- **Sí**: es pot treballar amb text ordinari respectant el MECR.
- **No**: cal suport visual reforçat, tipografia més gran, evitar text
  dens, combinació sistemàtica de text + pictograma. Considerar
  transliteració fonètica per a termes clau.

### Escolarització prèvia
- **Sí (regular)**: la dificultat és purament lingüística i cultural.
- **Parcial**: cal bastida cognitiva complementària (hàbits d'estudi,
  convencions acadèmiques).
- **No**: cal bastida cognitiva bàsica, no només lingüística. El text
  ha d'acompanyar-se d'explicitació de rutines i convencions (com es
  fa una activitat, què és un esquema, etc.).

### Nivell MECR
- **pre-A1, A1**: DUA Accés. LF extrema, glossari bilingüe ampli,
  pictogrames, frases nominals o present simple.
- **A2**: LF intensa amb glossari bilingüe dels termes clau.
- **B1**: LF moderada, glossari només per a termes acadèmics o
  culturalment marcats.
- **B2**: suport cultural més que lingüístic. Explicitar referents
  locals (festes, institucions, literatura catalana).

### CALP (Llengua acadèmica)
- **Inicial**: vocabulari acadèmic amb definicions integrades al cos
  del text, no només al glossari.
- **Emergent**: termes acadèmics en negreta + definició breu.
- **Consolidat**: termes tècnics sense bastida, com un company natiu.

## Exemple abans → després
Veure `assets/exemple-A1-fotosintesi.md` per a un exemple complet
d'adaptació d'un text de ciències naturals nivell A1 amb glossari
bilingüe català-àrab.

## Carregar context més profund
Si calen fonaments pedagògics (dol migratori, identitat de múltiples
pertinences, paper de l'aula d'acollida, CALP vs. BICS, etnomatemàtica,
coordinació amb LIC i mediació intercultural), carregar
`references/perfil-complet.md`. Si cal veure totes les fonts del DEIC
(Departament d'Ensenyament — acollida), carregar `references/fonts.md`.
