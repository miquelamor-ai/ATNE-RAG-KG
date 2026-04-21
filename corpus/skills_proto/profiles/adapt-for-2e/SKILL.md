---
name: adapt-for-2e
description: >
  Use when adapting educational text for a twice-exceptional student
  (2e — doble excepcionalitat): altes capacitats combinades amb una
  altra condició (TDAH, dislèxia, TEA, TDL, TDC, ansietat, etc.).
  Activates when the profile has "2e" or combines "altes_capacitats"
  with any other active condition. Works across all MECR levels.
  Core principle: DO NOT reduce cognitive expectations because of the
  associated difficulty; combine enrichment with specific support
  for the other condition. NEVER a single simplification — always a
  dual profile.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
mecr_range: [A1, A2, B1, B2, C1]
agent_role: adapter
tools_required: []
subvariables:
  - condicio_associada: [tdah, dislexia, tea, tdl, tdc, trastorns_emocionals, altres]
triggers:
  - path: profile.caracteristiques.2e.actiu
    equals: true
---

# Adaptar text per a alumnat amb doble excepcionalitat (2e)

## Quan activar aquesta skill
Activa aquesta skill quan l'adaptació de text sigui per a un alumne
amb **doble excepcionalitat**: coexistència d'**altes capacitats**
amb una altra condició (TDAH, dislèxia, TEA, TDL, TDC, trastorns
emocionals, etc.). Senyals: l'alumne mostra indicadors clars d'AC
(preguntes profundes, producció original, comprensió ràpida en
àrees d'interès) però també dificultats persistents en una altra
dimensió (atenció, descodificació, pragmàtica, coordinació motora,
regulació emocional). Molt sovint, les dues condicions
**s'emmascaren mútuament** — les AC compensen les dificultats i les
dificultats amaguen les AC — i per això la detecció és tardana.

## Barrera nuclear
**Doble demanda simultània.** L'alumnat 2e té una doble demanda
educativa: necessita **repte cognitiu** (propi de les AC) i
**bastida específica** per a la condició associada. La barrera
nuclear NO és la "mitjana" entre ambdues — és saber mantenir al
mateix temps l'exigència conceptual elevada i els suports
operatius per accedir-hi. Reduir una dimensió (simplificar perquè
té TDAH, o no donar suport perquè té AC) és l'error més comú i té
conseqüències devastadores: avorriment, desmotivació, baixa
autoestima, fracàs escolar malgrat el potencial.

## Instruccions principals d'adaptació

```
PERFIL: Doble Excepcionalitat (2e)
- Mantenir complexitat conceptual i lingüística pròpia d'AC
- Afegir bastida específica segons la condició associada (NO simplificar per ella)
- Profunditat + suport operatiu (mai l'un sense l'altre)
- Alternatives de canal de sortida sense rebaixar exigència
```

## Mapa barrera → instruccions (prioritzat)

| Prioritat | Instruccions activades | Justificació |
|---|---|---|
| **1a (AC mantingudes)** | H-12 (profundització), H-13 (connexions interdisciplinars), H-14 (mantenir complexitat), F-09 (pensament crític) | Evitar infraexpectativa |
| **2a (bastida condició associada)** | Segons perfil: micro-blocs (TDAH), vocabulari freqüent i no sinònims (dislèxia), zero implicitura (TEA), simplificació sintàctica (TDL), canal no motor (TDC), sensibilitat temes (trastorns emocionals) | Garantir accés |
| **3a (integració)** | Combinació explícita: "profund però en format X" — mai "profund o X" | Les dues dimensions alhora |

## Modulació per sub-variables

### Condició associada (quina és l'altra excepcionalitat)

- **AC + TDAH** (la combinació més freqüent): contingut profund amb
  excepcions i fronteres del coneixement, PERÒ en **micro-blocs**
  amb indicadors de progrés. Pensar divergent està encoratjat, però
  amb marcs de referència clars per no perdre el fil. Preguntes de
  pensament crític intercalades per mantenir l'atenció activa.
  Combinar aquesta skill amb `adapt-for-tdah`.

- **AC + dislèxia**: contingut conceptual exigent però amb lèxica
  controlada (paraules d'alta freqüència, evitar sinònims,
  descomposició de compostos llargs). Donar opcions de canal
  d'entrada (text-to-speech) sense rebaixar la complexitat del que
  es llegeix. Les connexions interdisciplinars s'expressen amb
  vocabulari controlat, no simplificat. Combinar aquesta skill amb
  `adapt-for-dislexia`.

- **AC + TEA**: contingut complex i obert al pensament crític, PERÒ
  amb **estructura predictible i zero implicitura**. Les metàfores
  i les ironies s'expliciten en lloc de rebaixar el repte
  conceptual. Les preguntes obertes ("i si...?") venen acompanyades
  d'exemples concrets per ancorar la inferència. Combinar aquesta
  skill amb `adapt-for-tea`.

- **AC + TDL**: contingut conceptual de nivell alt però amb
  **simplificació sintàctica i lèxica**. Els conceptes complexos
  s'expressen amb estructures SVO simples; els termes tècnics
  apareixen en 2-3 contextos per modelatge. L'andamiatge lingüístic
  (plantilles, bancs de paraules) permet que l'alumne demostri el
  seu potencial cognitiu sense que la barrera lingüística ho
  bloquegi. Combinar aquesta skill amb `adapt-for-tdl`.

- **AC + TDC/dispraxia**: repte cognitiu íntegre però amb
  **alternatives de canal de sortida** (teclat, resposta oral,
  selecció). La profunditat del contingut es manté; el que s'adapta
  és COM l'alumne demostra el coneixement. L'avaluació separa
  estrictament el component motor del cognitiu. Combinar aquesta
  skill amb `adapt-for-tdc`.

- **AC + trastorns emocionals**: contingut exigent i ric, PERÒ amb
  **sensibilitat a temes reactivadors** i estructura predictible
  que redueixi l'ansietat. Les preguntes de pensament crític han
  de tenir espai de pausa i opcions de resposta flexibles. No
  rebaixar l'exigència — oferir vies d'accés. Combinar aquesta
  skill amb `adapt-for-trastorns-emocionals`.

- **Altres combinacions**: aplicar el principi general (profunditat
  AC + bastida específica) adaptat a la condició concreta indicada
  al perfil de l'alumne. En cap cas reduir simultàniament les dues
  dimensions.

## Exemple abans → després
Veure `assets/exemple-B2-revolucio-industrial.md` per a un exemple
complet d'adaptació d'un text de ciències socials nivell B2 per a
un alumne AC + TDAH (la combinació més freqüent).

## Carregar context més profund
Si calen fonaments pedagògics (doble excepcionalitat: emmascarament
mutu entre AC i dificultat associada, detecció tardana, risc
d'infraexpectativa, línia vermella de no assumir que les AC
compensen altres dificultats, estratègies d'enriquiment compatible
amb adaptació, col·laboració amb EAP, avaluació de funció executiva
en AC+TDAH, distinció entre "simplificar" i "donar bastida"),
carregar `references/perfil-complet.md`. Si cal veure totes les
fonts (Guia DAC Altes Capacitats, bibliografia sobre 2e),
carregar `references/fonts.md`.
