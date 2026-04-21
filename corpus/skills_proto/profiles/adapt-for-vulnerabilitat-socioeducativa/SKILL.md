---
name: adapt-for-vulnerabilitat-socioeducativa
description: >
  Use when adapting educational text for a student in a socio-educational
  vulnerability situation (risc d'exclusió, entorn desfavorit, lack of
  familiarity with academic codes and cultural referents expected by
  school). Activates when the profile includes "vulnerabilitat
  socioeducativa". Works across all MECR levels. Core output principles:
  avoid assumptions about cultural capital, use universal referents and
  everyday experiences, very clear structure to compensate for
  unfamiliarity with academic genres.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
mecr_range: [A1, A2, B1, B2, C1]
agent_role: adapter
tools_required: []
subvariables: []
triggers:
  - path: profile.caracteristiques.vulnerabilitat_socioeducativa.actiu
    equals: true
---

# Adaptar text per a alumnat en situació de vulnerabilitat socioeducativa

## Quan activar aquesta skill
Activa aquesta skill quan l'adaptació de text sigui per a un alumne
en situació de vulnerabilitat socioeducativa — risc d'exclusió,
entorn desfavorit, llacunes en coneixements previs per factors
socials o culturals, manca de familiaritat amb rutines i gèneres
acadèmics del sistema educatiu. Senyals: baix rendiment en àrees
amb alt contingut cultural local (història, geografia) que no es
correspon amb el rendiment general; desconeixement de rutines
d'aula o procediments didàctics habituals; dificultat per
participar en dinàmiques que pressuposen capital cultural (debats,
comentari de textos literaris locals); frustració o desmotivació
davant de referents desconeguts; risc d'abandonament escolar.

## Barrera nuclear
**Capital cultural i familiaritat acadèmica.** L'alumnat en situació
de vulnerabilitat socioeducativa pot tenir manca de familiaritat amb
gèneres acadèmics, vocabulari culte i referents culturals que
l'escola pressuposa. La barrera NO és cognitiva sinó d'accés al codi
acadèmic. L'alumne té la capacitat per aprendre; el que li falta és
la xarxa de referents previs que el sistema dóna per suposada.
L'objectiu és explicitar el que és implícit, no rebaixar l'exigència.

## Instruccions principals d'adaptació

```
PERFIL: Vulnerabilitat Socioeducativa
- Evitar suposits sobre capital cultural
- Referents universals i experiències quotidianes
- Estructura molt clara (compensar manca familiaritat amb gèneres acadèmics)
```

## Mapa barrera → instruccions (prioritzat)

| Prioritat | Instruccions activades | Justificació (barrera) |
|---|---|---|
| **1a (capital cultural)** | E-09 (evitar suposits culturals), C-06 (analogies quotidianes), A-01 (vocab freqüent) | Manca familiaritat amb codi acadèmic |
| **2a (estructura)** | B-01 (paràgrafs curts), B-02 (blocs amb títol), B-05 (estructura deductiva) | Compensar manca familiaritat amb gèneres acadèmics |
| **3a (motivació)** | E-10 (sensibilitat temes), A-05 (eliminar idiomàtiques) | Evitar exclusió per referents |

## Modulació per sub-variables
Aquesta skill no té sub-variables configurables al frontmatter. La
vulnerabilitat socioeducativa és massa heterogènia per parametritzar
amb camps fixos (cada situació combina factors diferents: migració,
pobresa, aïllament territorial, família monoparental sobrecarregada,
absentisme, etc.). El docent aporta el context específic al camp
lliure del perfil de l'alumne.

Criteris d'ajust pragmàtic recomanats:

- **Explicitar les rutines acadèmiques**: si el text demana "fer un
  comentari de text", "treballar en grup" o "fer un esquema",
  incloure breument què vol dir exactament (com es fa, què
  s'espera). No suposar que l'alumne coneix el gènere acadèmic.
- **Referents universals, no locals**: substituir exemples que
  pressuposin coneixement local (festes catalanes específiques,
  figures històriques locals, obres literàries canòniques) per
  referents de vida quotidiana universal (menjar, família, escola,
  transport) quan el referent concret no sigui el contingut
  curricular nuclear.
- **Vocabulari culte explicat**: cada terme culte apareix amb
  definició integrada, no al glossari final. No pressuposar que
  l'alumne tingui accés a diccionaris ni a un entorn on les
  paraules s'aprenen per immersió.
- **Estructura deductiva amb títol anunciador**: cada bloc comença
  amb una frase tòpic que diu de què va. No deixar que l'alumne
  hagi d'inferir l'estructura del text (els gèneres acadèmics
  s'aprenen, no són universals).
- **Pont cultural amb el bagatge de l'alumne**: si el text parla
  de festes, menjars, jocs o tradicions, obrir explícitament una
  via perquè l'alumne pugui connectar amb el seu propi bagatge
  ("i tu, coneixes alguna festa semblant?"). La diversitat no
  és un inconvenient, és un recurs.
- **Sensibilitat a temes** (E-10): evitar referències que puguin
  generar vergonya o exclusió (dar per suposat viatges a l'estranger,
  activitats extraescolars de pagament, aparells tecnològics cars).

## Exemple abans → després
Veure `assets/exemple-A2-llibre.md` per a un exemple complet
d'adaptació d'un text de llengua nivell A2 amb substitució de
referents culturals i explicitació de rutines acadèmiques.

## Carregar context més profund
Si calen fonaments pedagògics (marc d'educació inclusiva, pla
d'acollida integral, llengua comunicativa vs. llengua acadèmica
(CALP vs. BICS, Cummins), pont cultural i bagatge de l'alumne com
a recurs, coordinació amb EAP / EAIA / serveis socials,
col·laboració amb famílies des del respecte a les expectatives
culturals, prevenció de l'abandonament escolar, distinció amb el
perfil nouvingut (que té el component lingüístic com a barrera
principal) i amb altres condicions constitutives), carregar
`references/perfil-complet.md`. Si cal veure totes les fonts DEIC
i ANSU (acollida), carregar `references/fonts.md`.
