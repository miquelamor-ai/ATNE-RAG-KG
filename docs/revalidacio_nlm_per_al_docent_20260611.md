# Re-validació NotebookLM — «Per al docent» (9 categories A-I) · 2026-06-11

**Tema 2** de `project_per_al_docent_9categories_obert_20260602`: re-validar amb
NotebookLM si la taxonomia de 9 categories A-I és el format final per a la secció
«Per al docent», amb **sortida REAL** del pipeline (no només l'spec).

- **Notebook:** MALL (`c0615b8d-f57d-4444-b360-2cdb3bafc399`, 28 fonts).
- **Material avaluat:** 3 sortides reals generades amb **gpt-4o** (adapter, `adapter_only=True`)
  sobre un text de fotosíntesi (2n ESO), 3 perfils diversos (nouvingut A2 àrab DUA Accés ·
  TDAH+dislèxia B1 Core · AACC B2 Enriquiment). Script: `tests/.tmp/gen_per_al_docent_real.py`.

## Veredicte global

**El FORMAT de 9 categories ES VALIDA** (pedagògicament sòlid i coherent amb el MALL),
**PERÒ la generació actual NO és apta per a producció**: el prompt produeix una
«il·lusió de justificació» — poques categories, superficial, descriu en lloc de justificar.

→ **Tema 2 resolt**: es manté la taxonomia 9 cat A-I; el que cal millorar és el PROMPT
(no el format). Quatre millores accionables (sota).

## P1 — El format (9 cat): SÒLID amb 2 matisos

- ✅ **Punts forts:** la separació **A (Adaptació Lingüística)** vs **G (Personalització/L1)**
  és encertada (gradació MECR/Cummins vs Translanguaging/TOLC). **D (Multimodalitat)** com a
  categoria pròpia és imprescindible (MALL principi 11, visual-artístic).
- ⚠️ **Solapament C↔F:** Suport Cognitiu i Avaluació/Comprensió poden encavalcar-se (les
  preguntes de 3 moments són alhora suport cognitiu i avaluació reguladora). Vigilar.
- 🔴 **Omissió: l'ORALITAT.** Per MELVIVES Principi 1, l'oralitat és el fonament. Falta una
  categoria/subsecció de **Mediació Oral** per a pre-A1/A1 (el text com a «guió per a lectura
  mediada»). [Coincideix amb el pendent ja conegut del mapa de taxonomies — 4a transformació.]

## P2 — La qualitat REAL: superficial i incompleta

| Cas | Veredicte NLM | Categories que FALTEN (amb complement actiu) |
|---|---|---|
| Nouvingut A2 àrab | Incomplet i superficial | **G** (glossari bilingüe→TOLC/Cummins), **D** (pictogrames), **C** (bastides/Solé) |
| TDAH+dislèxia B1 | Parcial, poc rigorós | **C** (esquema visual = càrrega cognitiva), **F** (preguntes; a B1 focus inferencial). H massa genèric (lligar TDAH amb DUA Principi 8) |
| AACC B2 Enriquiment | Incoherent amb TILC | **E** (HCL superior: Justificar/Argumentar), **C** (mapa conceptual: funció epistèmica) |

Patró comú: descriu **QUÈ** s'ha fet, no el **PER QUÈ** pedagògic; omet categories amb
intervenció real; i copia els codis d'exemple del prompt («— A1+A2», «— B1+B2») fins i tot
on són incoherents (un AACC de B2 NO té simplificació A1+A2).

## P3 — Recomanacions accionables (NotebookLM)

1. **Sincronització Complement→Categoria** *(la més important; ataca la infra-generació)*:
   si hi ha un complement actiu, la seva categoria HA d'aparèixer obligatòriament.
   Ex: glossari bilingüe → categoria **G** obligatòria amb cita Cummins/TOLC.
   Mapa: glossari→G/A · pictogrames/esquema/mapes→D/C · preguntes/rúbriques/activitats→F · bastides→C.
2. **Mètriques, no descripcions:** a la categoria A, substituir «frases curtes» per xifres de
   control de llengua MALL (ex: «≤12 paraules/frase a A1»). El canon (rubrica.json) ja les té.
3. **HCL nuclear a la categoria E:** especificar quina Habilitat Cognitivolingüística
   (Descriure/Explicar/Justificar/Argumentar) es preserva — garanteix que no es rebaixa el «Què».
4. **Procés, no producte:** justificar com les bastides ajuden a l'**autoregulació** (Principi 7),
   no només com ha quedat el text.

## Implicació de codi

El bloc `_ARGUMENTACIO_9CAT_BLOCK` (`adaptation/prompt_builder.py`) necessita reforç:
- (R1) Instrucció imperativa de cobrir TOTES les categories amb complement/perfil actiu
  (derivable de `params.complements` + perfils actius — el mapa complement→categoria).
- (R2) Eliminar/neutralitzar els codis d'exemple literals («A1+A2», «B1+B2») que el model
  parrots; o fer-los placeholders explícits.
- (R3) Injectar les mètriques del canon (ja disponibles via `_sl_canon`) a la justificació A.
- (R4) Vincular cada card al «per què» (principi MALL/DUA), no al «què».

## Implementació + prova empírica (2026-06-11, opció «b» — les 4 alhora)

Aplicats els 4 reforços a `_ARGUMENTACIO_9CAT_BLOCK` + nou helper `_argumentacio_case_block`
(checklist dinàmic complement→categoria, amb mètrica del nivell). Regressió `prompt_checks`
267 PASS / 0 ERROR.

**Prova A — Call 1 bundled (adapter genera text+argumentació+notes alhora):** segueix traient
NOMÉS 2 cards (A, B). ✅ Les mètriques R2 SÍ apareixen («màxim 12/18/25 paraules»), però la
infra-generació R1 PERSISTEIX: el model de-prioritza l'argumentació dins la crida gran.

**Prova B — crida DEDICADA (mateix contingut de prompt, focalitzat només en «Per al docent»):**
🎯 **7 cards** (A, B, C, D, E, **G**, H) per al nouvingut — inclou la G (glossari bilingüe →
Cummins/TOLC) que faltava, D (pictogrames), C (bastides), E amb HCL «Descriure», i les mètriques.

→ **CONCLUSIÓ: els 4 reforços de prompt són CORRECTES i suficients, però NOMÉS rendeixen en una
crida focalitzada.** La causa arrel de la infra-generació és ARQUITECTÒNICA: «Per al docent»
no pot anar embolcallat a la Call 1 (l'adapter prioritza el text). Cal generar-lo en una crida
pròpia (anàleg a com els complements van a la Call 2).

### Recomanació arquitectònica (pendent d'OK de Miquel — afecta el pipeline + cost)
Moure la generació de «## Argumentació pedagògica» a una crida dedicada quan `adapter_only`:
- Call 1 (adapter): genera només `## Text adaptat` + `## Notes d'auditoria`.
- Crida «Per al docent» dedicada: reutilitza `_ARGUMENTACIO_9CAT_BLOCK` + `_argumentacio_case_block`
  amb el text ja adaptat com a context. Sortida = `## Argumentació pedagògica` (7-9 cards).
- ⚠️ NO plegar-ho dins la Call 2 de complements: si no hi ha complements, no hi ha Call 2 →
  l'argumentació desapareixeria. Ha de ser una crida pròpia que sempre corri (o quan adapter_only).
- Cost: +1 generació petita (~2K tokens out). Model: gpt-4o o gpt-4.1-mini.
- Re-validar amb NotebookLM la sortida real després del canvi.

## ✅ IMPLEMENTAT + RE-VALIDAT (2026-06-11) — TEMA 2 TANCAT

Implementada la crida dedicada (opció 1, decisió Miquel = coherència):
- `build_argumentacio_prompt(profile, context, params)` — crida focalitzada, reutilitza la
  font única (`_ARGUMENTACIO_9CAT_BLOCK` + `_argumentacio_case_block`).
- `build_system_prompt(..., include_argumentacio=False)` quan 2-call → la Call 1 (adapter)
  genera només text + notes; «Per al docent» va a la crida dedicada amb el TEXT ADAPTAT
  FINAL com a context (coherent amb el que el LLM retorna realment).
- orchestrator pas 6d: crida dedicada després de complements; dedup heading + normalitza
  cards `##`→`###`.
- **Bug de coherència col·lateral fixat**: la Call 1 (adapter_only) rebia el bloc
  «COMPLEMENTS A GENERAR» → generava un `## Glossari` INLINE duplicat del de la Call 2.
  Ara aquest bloc només va a la crida única.

**Prova E2E (pipeline complet, 3 perfils):**
| Perfil | Cards ABANS | Cards DESPRÉS |
|---|---|---|
| Nouvingut A2 àrab | A, B (2) | A,B,C,D,E,**G**,H (7) |
| TDAH+dislèxia B1 | A, B, H (3) | A,B,C,D,E,**F**,H,**I** (8) |
| AACC B2 Enriquiment | A, B, H (3) | A,B,C,E,**F**,H (6) |

**Re-validació NotebookLM (corpus MALL, 2a passada):** ✅ **«APTE PER A PRODUCCIÓ»**.
Confirma: completesa resolta · cita Cummins/Solé/Vygotsky · mètriques correctes (≤12 A2,
≤18 B1) · HCL nuclear (Descriure/Explicar) · enfocament procés/autoregulació. Veredicte:
«ja no informa del que s'ha fet, educa en la lògica del MALL».

**Polish opcional pendent (NO bloquejant):** a P1, card C podria dir que a A2 l'alumne ja
inicia lectura autònoma (bastides = evitar frustració descodificació); card G podria citar
que l'alfabet L1 enforteix identitat/confiança (estratègia LIT de Cummins).
