# Certificació del pipeline ATNE ↔ teoria/saber-ne+ · 2026-06-12

> **Abast honest:** NO és possible firmar un «zero bugs» absolut (cap auditoria seriosa ho
> pot). Això és una certificació BASADA EN EVIDÈNCIA: verifica que el contracte (saber-ne+
> + teoria MALL/DUA + canon) arriba al prompt, que els guards passen, i declara
> explícitament què queda fora de l'abast i què no es pot garantir.

## 1. El que ES CERTIFICA (amb evidència) ✅

### 1a. El system prompt que arriba al LLM = el que defensa saber-ne+
Traça automàtica dels 3 prompts reals (Call 1 adapter · Call 2 complements · Call 3
«Per al docent»), `tests/.tmp/certify_prompt_trace.py`:

| Perfil | Cobertura del contracte al prompt |
|---|---|
| Nouvingut A2 àrab (DUA Accés) · glossari+bastides+pictogrames | **21/21** elements presents |
| TDAH+dislèxia B1 (DUA Core) · glossari+esquema+preguntes | **20/21** (l'absent = pictogrames, CORRECTE: no demanats) |

Elements verificats presents i CONDICIONALS al perfil: identitat ATNE · nivell MECR · bloc
DUA (Accés/Core/Enriquiment) · regles Lectura Fàcil · persona-audience · macrodirectives de
transformació (lèxic/sintaxi/estructura) · gènere discursiu (SKILL write-\*) + estructura
(5W/titular) · pictogrames ARASAAC (només si demanats) · TILC/TOLC plurilingüe (nouvingut) ·
glossari (bilingüe si L1) · bastides 3 moments · esquema visual · preguntes 3 moments×3
plànols · «Per al docent» 9 cat A-I (DEL CANON) · categories obligatòries del cas · mètrica de
control de llengua · HCL. → **Conclusió: el prompt reflecteix el contracte, i ho fa
condicionalment segons perfil+complements (no aboca tot sempre).**

### 1b. Guards de comportament — tots verds
- `prompt_checks.py`: **294 PASS / 0 ERROR** (27 casos × checks de contracte: UNE 153101, no
  contradicció A-02/A-30, gènere present, esquema, glossari L1, TILC, 9 cat, case-block).
- `per_al_docent_snapshot.py`: OK (comportament «Per al docent» = contracte, post consum canon).
- `per_al_docent_frontend_drift.py`: OK (pas3.html + saber-ne.html alineats amb el canon).
- `run_golden.py`: 0 ERROR (12 PASS + 15 WARN = gaps documentats, no errors).

### 1c. Arquitectura coherent amb la teoria
- 3 transformacions (VIA1) → instruction_catalog + skills, a Call 1.
- 6 complements MALL (12 eines) → skills generate-\*, a Call 2.
- «Per al docent» 9 cat → CONSUMIDES del canon `per_al_docent.json` (R0 tancat). ATNE no és origen.
- 2-call: adapter (GPT-4o) + complements (GPT-4o) + crida dedicada «Per al docent».

## 2. Validat EMPÍRICAMENT però NO garantit per execució 🟡
- **L'adherència del LLM al prompt** (que el model FACI el que el prompt diu) està validada per
  NotebookLM («apte producció») + e2e (7 cards amb G) + el llaç Verify/Retry + el pipeline de
  qualitat català. PERÒ els LLM són no-deterministes: cap auditoria garanteix la sortida
  perfecta a cada execució. El que es garanteix és que **l'instrucció correcta hi arriba**.

## 3. Caveats / oberts coneguts (transparència) ⚠️
- **Flash ≠ Taller (intencional, decisió A):** Flash és mode «lite» (1 crida, sense skills/
  2-call/Per-al-docent). NO honora el contracte complet PER DISSENY. Documentat a saber-ne+.
- **Triplicació frontend (mitigada, no eliminada):** els 9 noms de categoria viuen encara a
  pas3.html + saber-ne.html (a més del canon). Hi ha guard de drift (B-lite); la des-
  triplicació via `.data.js` queda pendent (no bloquejant).
- **snapshot_contract.py: baseline OBSOLET** (no és bug). Reporta diffs que són evolució
  legítima (rutes noves, params `adapter_only`/`include_argumentacio`/`lang`, `/api/propose`
  deprecat). Cal re-baselinar (manteniment).
- **30 WARN a prompt_checks:** soft (artefacte de finestra 3K a GENERE_specific_format +
  hints GLOSSARI_L1). No són errors.
- **Fallback hardcoded al backend:** es manté com a xarxa de seguretat (incident 02/06:
  submodule no inicialitzat → 0 skills). El canon MANA quan present.
- **Pendents pedagògics no de codi:** re-validació contínua amb NotebookLM de noves
  variants; pictogrames polisèmics (memòria prèvia).

## 4. El que NO es pot certificar
- «Zero bugs» absolut en tot el codi (cap auditoria ho pot).
- La qualitat pedagògica fina de cada sortida real (depèn del model + validació humana docent).
- Allò fora de l'abast verificat aquí (ex: auth, export PDF, dashboards) — no auditat en
  aquesta passada (es va centrar en el pipeline d'adaptació i el prompt).

## Veredicte
**Es certifica, amb l'evidència de §1, que el pipeline d'adaptació està ben construït i que el
system prompt que arriba al LLM conté el contracte que defensa saber-ne+ i la teoria MALL/DUA,
de forma condicional i coherent.** No s'han trobat bugs ni omissions en el flux verificat
(l'única «absència» trobada era comportament condicional correcte). Els punts de §2-§4 són
caveats honestos, no defectes ocults: estan documentats i, on calia, guardats per tests.

Per a una garantia adversarial màxima caldria una passada multi-agent dedicada (workflow), que
no s'ha executat aquí.
