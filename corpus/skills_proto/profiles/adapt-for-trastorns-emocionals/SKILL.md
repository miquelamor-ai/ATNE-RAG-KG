---
name: adapt-for-trastorns-emocionals
description: >
  Use when adapting educational text for a student with emotional or
  behavioural difficulties (ansietat, depressió, trastorns de conducta,
  desregulació emocional, baixa autoestima). Activates when the profile
  includes "trastorns emocionals / conducta". Works across all MECR
  levels. Core output principles: avoid sensitive topics when the
  profile indicates so, predictable structure with explicit anticipation
  of changes, micro-blocks to keep attention and reduce frustration.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
mecr_range: [A1, A2, B1, B2, C1]
agent_role: adapter
tools_required: []
subvariables: []
triggers:
  - path: profile.caracteristiques.trastorns_emocionals.actiu
    equals: true
---

# Adaptar text per a alumnat amb trastorns emocionals i de conducta

## Quan activar aquesta skill
Activa aquesta skill quan l'adaptació de text sigui per a un alumne
que presenta necessitats afectives greus i/o desregulació emocional o
conductual: ansietat, depressió, baixa autoestima, trastorns de
conducta, conductes inhibides, irritabilitat, reactivitat davant de
temes sensibles, historial de vulnerabilitat emocional. **Important**:
la funció docent no és diagnosticar — és identificar barreres
d'aprenentatge i participació i ajustar el material per reduir-les.

## Barrera nuclear
**Regulació emocional.** L'alumnat amb trastorns emocionals o
conductuals pot tenir baixa tolerància a la frustració, ansietat
davant tasques llargues o complexes, i sensibilitat a temes que
activen experiències traumàtiques. La barrera no és cognitiva sinó
emocional — la capacitat d'aprendre està preservada, però l'estat
afectiu condiciona la disponibilitat per entrar en la tasca i
mantenir-s'hi. La prioritat és que el text NO generi desbordament
emocional innecessari.

## Instruccions principals d'adaptació

```
PERFIL: Trastorn Emocional/Conductual
- Evitar temes sensibles (violència, guerra, separació, mort) si el perfil ho indica
- Estructura predictible i anticipació de canvis
- Micro-blocs curts per mantenir atenció i reduir frustració
```

## Mapa barrera → instruccions (prioritzat)

| Prioritat | Instruccions activades | Justificació (barrera) |
|---|---|---|
| **1a (emocional)** | E-10 (sensibilitat temes traumàtics), H-03 (anticipació canvis) | Barrera nuclear: regulació emocional |
| **2a (estructura)** | H-01 (estructura predictible), B-01 (paràgrafs curts), H-04 (micro-blocs) | Reduir ansietat per imprevisibilitat |
| **3a (atenció)** | C-04 (chunking), B-13 (indicadors progrés) | Mantenir atenció i reduir frustració |

## Modulació per sub-variables
Aquesta skill no té sub-variables configurables al frontmatter. La
variabilitat interna del perfil (des de conductes inhibides fins a
trastorns de conducta explícits, passant per ansietat, depressió o
baixa autoestima) és massa gran per parametritzar amb camps fixos.
El docent aporta context específic per cada cas al camp lliure del
perfil de l'alumne.

Criteris d'ajust pragmàtic recomanats:

- **Si hi ha ansietat o pànic davant l'avaluació**: oferir
  indicadors de progrés explícits ("[Secció X de Y]"), eliminar
  consignes que siguin una trampa o que generin pressió temporal
  innecessària. Les tasques llargues es fragmenten en sub-tasques
  amb punts d'aturada clars.
- **Si hi ha historial de trauma o vulnerabilitat**: revisar el
  contingut perquè no inclogui referències a violència, guerra,
  separació, mort, assetjament o altres temes potencialment
  reactivadors. Si el currículum requereix tractar aquests temes,
  anunciar-ho explícitament al principi del text perquè l'alumne
  pugui preparar-se o demanar alternativa.
- **Si hi ha trastorn de conducta o baixa tolerància a la
  frustració**: micro-blocs amb objectiu clar, feedback visual de
  progrés entre blocs, evitar tasques que s'allarguin sense punts
  de tancament.
- **Si hi ha baixa autoestima**: evitar fórmules de consigna que
  pressuposin fracàs ("segur que no ho sabràs, però intenta-ho...").
  Reconèixer l'esforç al text ("ja has arribat al pas 3, molt bé").
  Donar opcions perquè l'alumne pugui trobar èxit sense dependre
  d'una resposta única.
- **Si hi ha inhibició o evitació**: estructura molt predictible
  perquè l'alumne sàpiga a cada moment què es demana. Sense
  sorpreses ni canvis de format dins la mateixa activitat.

## Exemple abans → després
Veure `assets/exemple-B1-historia.md` per a un exemple complet
d'adaptació d'un text de ciències socials nivell B1 amb sensibilitat
a temes traumàtics i estructura predictible.

## Carregar context més profund
Si calen fonaments pedagògics (observació activa i empàtica,
intervenció inclusiva dins l'aula ordinària vs. segregació,
coordinació amb EAP / EAIA / CDIAP, protocol de derivació, foment
de l'autoestima i l'autoconcepte positiu, cohesió grupal davant
dinàmiques negatives, suport afectiu continuat, línia vermella de
no etiquetar ni diagnosticar a l'aula, distinció amb altres perfils
que tenen component emocional), carregar
`references/perfil-complet.md`. Si cal veure totes les fonts DEIC
(Formació del professorat), carregar `references/fonts.md`.
