---
name: adapt-for-disc-auditiva
description: >
  Use when adapting educational text for a student with hearing
  impairment (hipoacúsia DAL-DAS o sordesa DAP / cofosi, ICD-11
  AB50-AB52). Activates when the profile includes "discapacitat
  auditiva". Works across all MECR levels. Core principle: for deaf
  students with prelocutive signing profile, written Catalan is
  effectively an L2 — lexical and syntactic simplification similar to
  newly-arrived students. For hypoacusia and postlocutive deafness
  with good reading competence, textual adaptation is minimal; most
  needs are frontend (subtitles, FM, magnetic loop, LSC interpreter).
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
mecr_range: [A1, A2, B1, B2, C1]
agent_role: adapter
tools_required: []
subvariables:
  - comunicacio: [oral, LSC, bimodal]
  - implant_coclear: bool
triggers:
  - path: profile.caracteristiques.disc_auditiva.actiu
    equals: true
---

# Adaptar text per a alumnat amb discapacitat auditiva

## Quan activar aquesta skill
Activa aquesta skill quan l'adaptació de text sigui per a un alumne
amb pèrdua auditiva — des de deficiència auditiva lleugera (DAL,
21-40 dB) fins a sordesa pregona o cofosi (≥ 91 dB). Senyals: demana
que li repeteixin, distracció en entorns sorollosos, ús d'audiòfon o
implant coclear, comunicació amb LSC (Llengua de Signes Catalana) o
bimodal, ortografia fonètica alterada, dificultats marcades en
idiomes estrangers orals, fatiga auditiva acumulativa.

## Barrera nuclear
**Lèxica i sintàctica (en sordesa prelocutiva).** L'alumnat amb
discapacitat auditiva prelocutiva signant té com a barrera principal
la comprensió del text escrit — la llengua escrita és efectivament una
L2 (el català/castellà no és la seva L1, que és la LSC). La
simplificació lingüística és similar a la d'un alumne nouvingut. En
canvi, per a hipoacúsia lleu-moderada i sordesa postlocutiva amb bona
competència lectora, l'adaptació textual és mínima: les necessitats
són principalment de frontend (subtítols, sistema FM, bucle magnètic,
intèrpret de LSC, ubicació a l'aula, reducció del soroll).

## Instruccions principals d'adaptació

```
PERFIL: Discapacitat Auditiva
- Tractar com L2 en sordesa prelocutiva signant
- Simplificació lingüística similar a nouvingut
- Suport visual com a compensació
```

## Mapa barrera → instruccions (prioritzat)

| Prioritat | Instruccions activades | Justificació (barrera) |
|---|---|---|
| **1a (lèxica/sintàctica)** | H-20 (simplificació com L2), A-01 (vocab freqüent), A-07 (una idea per frase), A-12 (longitud frase), A-13 (eliminació subordinades) | Barrera lèxica i sintàctica en sordesa prelocutiva |
| **2a (visual)** | D-01 (emojis suport), D-02 (esquema procés) | Suport visual com a compensació |
| **3a (pragmàtica)** | A-05 (eliminar idiomàtiques), A-06 (eliminar polisèmia) | L2 + pèrdua de context auditiu |

**Nota**: La gravetat de la barrera depèn del tipus de sordesa. En
sordesa postlocutiva amb bona competència lectora, l'adaptació
textual és mínima — les necessitats són principalment de frontend
(subtítols en tot material audiovisual, bucle magnètic, FM, intèrpret
de LSC, ubicació preferent, reducció del soroll).

## Modulació per sub-variables

### Mode de comunicació
- **Oral** (amb pròtesi o implant): l'adaptació textual és moderada.
  El text ha d'anar acompanyat sistemàticament de suport visual
  (esquemes, imatges, mapes conceptuals). Evitar instruccions que
  només s'hagin donat oralment. Tot vídeo o àudio ha de tenir
  subtítols activats.
- **LSC** (Llengua de Signes Catalana com a L1): tractar el text
  escrit com L2 completa. Simplificació lèxica i sintàctica
  intensa — vocabulari d'alta freqüència, estructura SVO simple,
  zero subordinades, definicions integrades. Glossari bilingüe
  català–LSC si és possible. La LSC no és una traducció del català
  sinó una llengua plena amb gramàtica pròpia (Llei 17/2010).
- **Bimodal** (oral + signes simultàniament): combinació d'ambdues
  estratègies — text escrit simplificat com a L2 moderada i suport
  visual sistemàtic. Pot beneficiar-se de marques visuals que
  facilitin la interpretació simultània.

### Implant coclear
- **Sí**: pot beneficiar-se de contingut oral amb suport visual.
  **Important**: l'implant coclear NO fa que l'alumne "senti
  normal". Segueix necessitant totes les mesures (FM, subtítols,
  suport visual, ubicació preferent). L'adaptació textual és similar
  al mode oral però amb més marge segons l'edat d'implantació i la
  rehabilitació.
- **No**: si la DA és severa o pregona sense implant, la
  comunicació és principalment visual i la llengua escrita és L2.
  Aplicar la simplificació com LSC si el mode de comunicació és
  signant.

## Exemple abans → després
Veure `assets/exemple-B1-democracia.md` per a un exemple complet
d'adaptació d'un text de ciències socials nivell B1 per a alumne
sord prelocutiu signant (LSC com a L1).

## Carregar context més profund
Si calen fonaments pedagògics (classificació audiomètrica XTEC/CREDA,
codis ICD-11, tipologies per localització i moment d'adquisició,
implant coclear i LSC, rol del CREDA i del MALL/SIAL, marc normatiu
D150/2017 i Llei 17/2010 de la LSC, mesures universals/addicionals/
intensives, tecnologia de suport (FM, bucle magnètic, subtitulació
automàtica), diagnòstic diferencial amb TDL i TDAH, comunitat sorda
i identitat cultural), carregar `references/perfil-complet.md`. Si
cal veure totes les fonts (OMS, CREDA, DOGC, FESOCA, Marschark,
Humphries), carregar `references/fonts.md`.
