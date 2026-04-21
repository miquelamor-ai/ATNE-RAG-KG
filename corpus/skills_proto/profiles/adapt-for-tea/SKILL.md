---
name: adapt-for-tea
description: >
  Use when adapting educational text for a student with TEA (Trastorn de
  l'Espectre Autista). Activates when the profile includes "TEA", "Asperger"
  or "autisme". Works across all MECR levels. Core output principles:
  predictable structure, zero implicit meaning, univocal vocabulary, and
  explicit anticipation of topic changes.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
mecr_range: [A1, A2, B1, B2, C1]
agent_role: adapter
tools_required: []
subvariables:
  - nivell_suport: [1, 2, 3]
  - comunicacio_oral: [fluida, limitada, no_verbal]
triggers:
  - path: profile.caracteristiques.tea.actiu
    equals: true
---

# Adaptar text per a alumnat amb TEA

## Quan activar aquesta skill
Activa aquesta skill quan l'adaptació de text sigui per a un alumne amb TEA
(Trastorn de l'Espectre Autista, inclòs síndrome d'Asperger). Senyals:
comprensió inferencial compromesa, literalitat, dificultat amb llenguatge
figurat i ironia, necessitat de predictibilitat estructural.

## Barrera nuclear
**Inferència.** La Teoria de la Ment compromesa dificulta interpretar tot
allò que és implícit: metàfores, ironia, doble sentit, intencions no
explícites. El llenguatge figurat i la polisèmia generen ambigüitat no
resoluble sense suport explícit.

## Instruccions principals d'adaptació

```
PERFIL: TEA
- Estructura predictible: sempre mateixa seqüència (títol→definició→exemple→activitat)
- Zero implicitura: tota metàfora, ironia, sentit figurat → literal explícit
- Vocabulari unívoc: evitar polisèmia, definir de forma unívoca
- Anticipació: avisar canvis de tema o format ("Ara canviem de tema.")
```

## Mapa barrera → instruccions (prioritzat)

| Prioritat | Instruccions activades | Justificació (barrera) |
|---|---|---|
| **1a (inferència)** | H-01 (estructura predictible), H-02 (zero implicitura), A-05 (eliminar idiomàtiques), A-06 (eliminar polisèmia) | Barrera nuclear: inferència |
| **2a (estructura)** | H-03 (anticipació canvis), B-02 (blocs amb títol), B-06 (ordre cronològic), B-09 (numeració) | Predictibilitat necessària |
| **3a (lèxica)** | A-03 (coherència terminològica), A-04 (referents explícits) | Polisèmia i ambigüitat |
| **4a (discursiva)** | B-03 (frase tòpic), B-10 (transicions) | Coherència central feble |

## Modulació per sub-variables

### Nivell de suport (DSM-5)
- **Nivell 1 (necessita suport)**: adaptació subtil. Reforçar estructura
  predictible i explicitar tota metàfora o ironia, però mantenir
  complexitat lingüística propera al MECR. Glossari curt al final.
- **Nivell 2 (suport notable)**: LF moderada. Frases curtes, una idea per
  frase, definicions integrades al cos del text, pictogrames al costat dels
  termes clau, anticipació explícita de cada bloc.
- **Nivell 3 (suport molt notable)**: LF extrema + suport visual total.
  Pictogrames obligatoris per a cada concepte, text mínim, consignes d'un
  sol pas, cap implicitura, seqüència rígida.

### Comunicació oral
- **Fluida**: aprofitar la capacitat verbal. Pot treballar textos amb
  vocabulari ric sempre que sigui unívoc i les inferències estiguin
  explicitades.
- **Limitada**: combinar text amb suport visual (esquemes, icones). Frases
  curtes, subjecte explícit, evitar pronoms ambigus.
- **No verbal**: materials altament visuals, pictogrames obligatoris, text
  reduït al mínim, format compatible amb SAAC (Sistemes Augmentatius i
  Alternatius de Comunicació).

## Exemple abans → després
Veure `assets/exemple-B1-parlament.md` per a un exemple complet d'adaptació
d'un text de ciències socials nivell B1 amb llenguatge figurat.

## Carregar context més profund
Si calen fonaments pedagògics (anàlisi funcional de la conducta, interessos
restringits com a porta d'entrada, mediació social estructurada,
coordinació amb EAP/CSMIJ), carregar `references/perfil-complet.md`. Si cal
veure totes les fonts DAC (DTGD), carregar `references/fonts.md`.
