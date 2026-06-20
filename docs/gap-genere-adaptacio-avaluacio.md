# Gap del gènere discursiu a l'adaptació i l'avaluació

**Data:** 2026-06-20
**Estat:** diagnòstic tancat · Gap 2 (bug) fixat · Gap 1 i Gap d'avaluació OBERTS (briefing per al xat que ho abordi)

## Context

Durant l'experiment A/B "skills ON vs OFF" (Peça 4, `tests/experiment_ab/`) es va
detectar que el harness assignava `genere_discursiu` explícitament a cada cas. Això
mesurava el **camí feliç** (gènere conegut), però va fer evident que el cas real més
freqüent —un docent que adapta un text propi pujat/enganxat— no passa per aquí.

Verificació al codi (2026-06-20):

- Les 23 skills de gènere `write-*` (corpusFJE/skills/generes/) tenen totes
  `agent_role: adapter` i un trigger `path: params.genere_discursiu · equals: <X>`.
- `genere_discursiu` només s'estableix a la via de **generació IA** del Pas 2
  (`ui/atne/pas2.html`, dins el bloc "Generar text"). Quan el docent **puja o enganxa**
  un text propi, NO s'estableix.
- L'avaluador no consumeix cap skill de gènere: **no existeix cap skill amb
  `agent_role: evaluator` a tot el corpus** (cerca recursiva: 0 resultats).

## Mapa dels gaps

|                                   | Adaptador                              | Avaluador                              |
|-----------------------------------|----------------------------------------|----------------------------------------|
| Text generat per ATNE             | ✅ skill de gènere s'activa            | ❌ no consumeix skills de gènere       |
| Text pujat/enganxat (net)         | ❌ gènere buit → cap skill (**Gap 1**) | ❌ mai consumeix skills de gènere      |
| Text pujat després de generar     | ⚠️ gènere heretat incorrecte (**Gap 2**) | ❌ mai consumeix skills de gènere      |

## Gap 2 — gènere heretat (BUG) — ✅ FIXAT 2026-06-20

`atne.genere_discursiu` era una clau de localStorage persistent i òrfena: s'escrivia
a la generació IA i no es netejava en cap reset. Un docent que primer generava un
text (ex: "notícia") i després pujava/enganxava un text propi (ex: un poema)
arrossegava `genere_discursiu = noticia`, i l'adaptador activava `write-noticia`
sobre el poema. El localStorage persisteix entre sessions del navegador, així que
podia arrossegar-se de dies anteriors.

**Fix:** s'afegeix `localStorage.removeItem('atne.genere_discursiu')` als tres punts
de reset de `pas2.html` (nova adaptació `?new=1`, "Comença de nou", "Buidar editor"),
on ja es netejava `doc_draft`. Branca `fix/genere-localstorage-cleanup`.

## Gap 1 — text propi sense gènere (OBERT)

Quan el docent puja/enganxa un text net, `genere_discursiu` queda buit i l'adaptador
no activa cap skill de gènere: cau al comportament genèric. Tres opcions sobre la taula:

1. **Detecció automàtica de gènere** (classificador lleuger): una crida ràpida a l'LLM
   infereix el gènere del text pujat abans d'adaptar, i omple `genere_discursiu`.
   Tanca el gap de debò; cost = 1 crida extra + risc de classificació errònia.
2. **Selector de gènere també a la via d'upload/enganxat**: el docent tria el gènere
   manualment quan puja text propi (com ja fa quan genera). Simple; depèn que el docent
   sàpiga/vulgui triar-lo.
3. **No fer res**: l'adaptació de text propi va sense skill de gènere (estat actual).

## Gap d'avaluació — estructural (OBERT)

L'avaluador no té cap mecanisme per conèixer el gènere del text: no consumeix skills
de gènere (totes són `adapter`) i no existeix cap skill `evaluator`. Aquest gap és
**total**, no condicional: no depèn que `genere_discursiu` estigui ple o buit.

Tancar-ho no és un fix de neteja — requereix **decidir si l'avaluador ha de ser
conscient del gènere** i, si sí, com:

- Crear skills `agent_role: evaluator` per gènere (rúbrica d'avaluació específica del
  gènere), o
- Passar el `genere_discursiu` a l'avaluador per un altre canal (sense skill), o
- Un classificador compartit amb el Gap 1 que alimenti adaptador i avaluador alhora.

## Pendent de decisió

Gap 1 i Gap d'avaluació queden oberts. Quan s'abordin, val la pena considerar-los
junts: una possible detecció/assignació de gènere podria alimentar adaptador i
avaluador a la vegada, tancant els dos gaps amb un sol mecanisme.
