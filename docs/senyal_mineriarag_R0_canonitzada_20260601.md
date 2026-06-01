# Senyal R0 → ATNE · Matriu canonitzada + matriu_cobertura.json publicat

> **Data**: 2026-06-01 · **De**: mineriaRAG · **Per a**: ATNE
> **Resposta a**: `handoff_mineriarag_matriu_transversals_20260601.md`
> **Estat**: ✅ R0 DESBLOQUEJAT. Podeu retirar el hardcoded.

## Commit hash del senyal

**corpusFJE master: `2109c91`** (el commit que introdueix la matriu)
(complet `2109c918e1e19d797163a2b119a2b05ec5041d7a`)

> El HEAD actual de master és `d612502` (commit posterior del corpus-bot que només
> regenera `_manifest.json`; **NO toca** `matriu_cobertura.json` — verificat idèntic).
> Feu el bump del submodule a `d612502` (HEAD) per no quedar enrere; el JSON és el
> mateix que a `2109c91`.
>
> `git submodule update --remote corpus/external/corpusFJE` i committegeu el bump.

## Què s'ha fet (Opció 4)

1. **Font canon única**: nova secció `## Matriu de cobertura perfil × complement` al
   `M2_instruments-mediacio-pedagogica.md`. Conté:
   - Matriu base R0 (13 condicions × 12 complements) — §1 del vostre handoff.
   - `complement_keys` (ordre canon), bandes MECR, `visual_need_conditions`,
     `primaria_inicial_cursos`.
   - Lleis operatives R1/R2/**R3**/fallback/R4/A5 amb fonament pedagògic — §2 del handoff.
2. **Derivat mecànic**: `.tooling/matriu_cobertura.json`, generat per
   `.tooling/build_matriu_cobertura.py` (determinista, sense LLM). El consumiu via
   **path fix**: `corpus/external/corpusFJE/.tooling/matriu_cobertura.json`
   (NO és per-skill, no el trobareu amb rglob de rubrica.json).
3. **GitHub Action**: `build-skills.yml` regenera el JSON automàticament en cada canvi
   del M2. Idempotent (el JSON committejat == el que genera l'Action).

## Decisions preses (respostes a les vostres 3 preguntes de §5)

| Pregunta vostra | Decisió mineriaRAG |
|---|---|
| Ubicació del JSON | `.tooling/matriu_cobertura.json` (path fix, no rglob). Coherent amb `format_outputs.yaml`. |
| Lleis com a `rules` globals o `case_overrides`? | **`rules` globals** (com proposàveu a §3). R1–R3 operen sobre la unió i R4/A5 sobre el fallback → són lleis d'algoritme, no overrides per condició. |
| R3 (`verified:false`) | **Canonitzada al M2** amb fonament (decisió de Miquel). El canon és 100% complet; no queda cap llei al codi tret de la *detecció* d'A5 (vegeu sota). |

## Contracte del JSON (esquema final)

Blocs: `version`, `_meta`, `complement_keys`, `base`, `visual_need_conditions`,
`primaria_inicial_cursos`, `rules` (`mecr_bands`, `R1_add_pictos`, `R2_drop_maps`,
`R3_drop_glossari_disl`, `fallback`, `R4_primaria_inicial`, `A5_nouvingut_l1`),
`algoritme` (string amb l'ordre d'aplicació, perquè no l'hàgiu d'endevinar).

### Una sola excepció pactada que queda al vostre codi

La **detecció** de "nouvingut amb L1 declarada" (per disparar A5) depèn de l'estructura
del perfil al frontend (chip `cat` / `conditions[key=nouvingut]` / `subvariables` /
`p.l1`). Això **no és pedagogia** sinó implementació, per tant resta a
`complements-matriu.js` documentada com a excepció pactada. El que SÍ és canon és
l'**efecte** d'A5 (`rules.A5_nouvingut_l1.result`). La resta de la funció
`defaultComplementsForProfile` ja és derivable 100% del JSON.

## Validació anti-regressió ja feta al nostre costat

He corregut un **round-trip 711/711** contra el vostre golden snapshot
(`tests/golden/matriu_complements_snapshot.json`): reimplementant l'algoritme
**aplicant només el JSON**, reprodueix exactament les 711 entrades del snapshot
(13 condicions × 9 MECR × 5 cursos + NONE + NOUV_L1 + 4 parelles).

→ Test: `corpusFJE/.tooling/test_matriu_cobertura.py` (llegeix el vostre snapshot per
ruta local). Quan feu el refactor, el vostre test d'acceptació de §5 hauria de passar
idènticament.

## Acció recomanada per a vosaltres

1. Bump del submodule corpusFJE a `2109c91`.
2. Refactoritzar `complements-matriu.js`: carregar `.tooling/matriu_cobertura.json` i
   aplicar `rules` segons `algoritme`. Mantenir només la *detecció* nouvingut+L1.
3. Córrer el vostre test byte-a-byte vs snapshot. Si passa → eliminar
   `MATRIU_CONDICIONS` i la lògica hardcoded.
4. Senyalar-me quan estigui (commit ATNE) per tancar el cicle R0.

## Notes / pendents (no bloquegen)

- **`tests/golden/matrix.yaml`** (v1.0.0, 26/05): conté un `defaults_per_condicio`
  **obsolet** (matriu antiga `pas2.html:2814`, ja substituïda per `complements-matriu.js`).
  No l'he canonitzat. Recomano que l'esborreu o el regenereu des del JSON per no
  confondre futurs lectors — el contracte viu és `complements-matriu.js` + el snapshot.
- **T1/T2 (handoff §6)**: deute paral·lel, decisió separada de Miquel (pendent). La meva
  hipòtesi coincideix amb la vostra: T1 (`forma_sobre_mecr`) → sí al canon dels
  gèneres-forma; T2 (`no_contingut_no_demanat`) → regla de plataforma ATNE, no puja al
  canon. Ho tractem en sessió pròpia.
