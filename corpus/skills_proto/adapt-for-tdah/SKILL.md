---
name: adapt-for-tdah
description: >
  Use when adapting educational text for a student with TDAH (Trastorn per Dèficit
  d'Atenció i Hiperactivitat). Activates when the student profile includes "TDAH"
  or "atenció sostinguda baixa" or "memòria de treball limitada". Works across
  all MECR levels but is especially critical for A1-B1. Output format: markdown
  with micro-blocks, progress indicators, and visual signaling.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
mecr_range: [A1, A2, B1, B2, C1]
subvariables:
  - presentacio: [inatent, hiperactiu, combinat]
  - grau: [lleu, moderat, sever]
  - baixa_memoria_treball: bool
  - fatiga_cognitiva: bool
---

# Adaptar text per a alumnat amb TDAH

## Quan activar aquesta skill
Activa aquesta skill quan l'adaptació de text sigui per a un alumne amb TDAH
(Trastorn per Dèficit d'Atenció i Hiperactivitat). Senyals: baixa atenció
sostinguda, memòria de treball limitada, necessitat de variació i
retroalimentació constant.

## Barrera nuclear
**Atenció sostinguda limitada.** La memòria de treball compromesa dificulta
retenir informació entre frases llargues o paràgrafs densos.

## Instruccions principals d'adaptació

```
PERFIL: TDAH
- Micro-blocs de 3-5 frases amb objectiu explícit per bloc
- Senyalització visual intensa: negretes, requadres, icones
- Variació: alternar lectura, esquema, pregunta
- Indicadors de progrés: [Secció X de Y]
```

## Mapa barrera → instruccions (prioritzat)

| Prioritat | Instruccions activades | Justificació (barrera) |
|---|---|---|
| **1a (atenció)** | H-04 (micro-blocs amb objectiu), B-13 (indicadors progrés), H-06 (variació activitat) | Barrera nuclear: atenció |
| **2a (memòria treball)** | C-04 (chunking 3-5 elements), C-01 (límit conceptes nous), B-01 (paràgrafs curts) | Barrera memòria de treball |
| **3a (motivació)** | H-05 (retroalimentació visual), F-06 (preguntes intercalades) | Feedback per mantenir motivació |

## Modulació per sub-variables

### Presentació clínica (DSM-5)
- **Predomini inatent**: chunking molt intens, negretes per paraules clau, títols intermedis cada 3-4 línies
- **Predomini hiperactiu-impulsiu**: frases curtes i directes, verbs d'acció, consignes d'un sol pas, ritme dinàmic
- **Presentació combinada**: combinació d'ambdues estratègies (la més freqüent en edat escolar)

### Grau de suport
- **Lleu**: estructura clara, frases curtes; contingut intact
- **Moderat**: reducció de text, suport visual explícit, llistes sobre paràgrafs
- **Sever**: text mínim, consignes d'un sol pas, vocabulari molt controlat

### Si baixa memòria de treball
Repetir concepte principal al final de cada bloc. No assumir informació prèvia.
Instruccions numerades i seqüencials (mai simultànies). Evitar subordinades
complexes que sobrecarreguen el bucle fonològic.

### Si fatiga cognitiva
Fragmentar text en blocs amb marcadors de progrés. Sessions òptimes 10-15
minuts. Feedback immediat entre blocs.

## Exemple abans → després
Veure `assets/exemple-A2-digestive.md` per a un exemple complet d'adaptació de
text de ciències naturals nivell A2.

## Carregar context més profund
Si calen fonaments pedagògics (neurociència, comorbiditats, marc DUA), carregar
`references/perfil-complet.md`. Si cal veure totes les fonts, carregar
`references/fonts.md`.
