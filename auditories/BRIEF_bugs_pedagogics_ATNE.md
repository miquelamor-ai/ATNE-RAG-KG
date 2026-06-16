# Brief per a Claude Code — Bugs pedagògics ATNE (auditoria 12/06/2026)

**Adjunt:** `patch_bugs_pedagogics.diff` (correccions B1-B4, **ja aplicades i verificades** en un entorn d'auditoria: 17/17 smoke tests, cap regressió)
**Decisió pedagògica aprovada per Miquel (12/06):** 2e = AACC + qualsevol altra característica **constitutiva** activa. Les contextuals (nouvingut, vulnerabilitat) NO activen 2e per si soles.

## Instruccions generals
1. Branca nova: `git checkout -b fix/bugs-pedagogics-auditoria-20260612`
2. Un commit per correcció. Mostra el diff i atura't perquè el Miquel revisi abans de cada commit. No facis push sense ordre.
3. Aplica el diff adjunt: `git apply patch_bugs_pedagogics.diff` (si falla per drift del codi, aplica els canvis manualment seguint les seccions de sota).
4. Després de CADA canvi: `python -m adaptation.params_resolver` (ha de donar TOTS OK) i `python -m py_compile adaptation/params_resolver.py adaptation/prompt_builder.py`.

## B1 — 🔴 Autodetecció 2e (params_resolver.py)
- Nova constant `_CONTEXTUALS` + funció `_is_2e(chars, actives)` després de `_str_to_bool`.
- Secció 8: `not _str_to_bool(ac.get("doble_excepcionalitat"))` → `not _is_2e(chars, actives)`.
- `_resolve_dua`: `not ac_doble` → `not _is_2e(chars, actives)`.
- **Comportament verificat:** AACC+dislèxia sense flag → B1/Core (abans B2/Enriquiment ✗). AACC sol → B2/Enriquiment (intacte). Flag explícit → respectat.
- **AFEGIR un smoke test nou** al bloc `__main__` del fitxer:
```python
_check("2e AUTODETECTAT (AACC+dislèxia SENSE flag) 2n ESO",
       resolve_params({"altes_capacitats": {"actiu": True},
                       "dislexia": {"actiu": True, "grau": "moderat"}},
                      etapa="ESO", curs="2n ESO"),
       expected_mecr="B1", expected_dua="Core")
```
- Commit: `fix(pedagogia): autodetectar 2e al resolver (AACC + constitutiva activa)`

## B2 — 🟠 Adequació per etapa a preguntes de comprensió (prompt_builder.py)
`adequacio_linia` es calculava i es descartava. El diff l'afegeix al final dels DOS blocs de preguntes (branca skills ON i branca OFF) com:
```
Adequació a l'etapa:
{adequacio_linia}
```
**Verificat:** amb etapa infantil, el prompt ara conté "Evita «justifica» i «argumenta»".
Commit: `fix(pedagogia): inserir adequacio_linia per etapa a preguntes de comprensio`

## B3 — 🟡 Guard isinstance a _resolve_dua (params_resolver.py)
Helper local `_sub(key)` que retorna `{}` si el valor no és dict. **Verificat:** `resolve_params({"di": True}, ...)` ja no peta amb AttributeError.
Commit: `fix(robustesa): _resolve_dua tolera caracteristiques no-dict`

## B4 — 🟡 Avís de traça per característiques ignorades (params_resolver.py)
Després de calcular `actives`, la traça afegeix: `AVÍS: característiques presents però ignorades (sense actiu=true o format no-dict): [...]`. **Verificat.**
Commit: `fix(traçabilitat): avisar de caracteristiques de perfil ignorades`

## B6 — ⚪ Neteja cosmètica (opcional, mateix PR)
- `adaptation/orchestrator.py:483` esborrar `_all_titles_re` (no usat)
- `adaptation/prompt_builder.py` esborrar `n = len(_seccions)` (no usat)
- Esborrar els 21 imports morts de `server.py` (llista amb `python -m pyflakes server.py | grep "imported but unused"`)
- Esborrar `_mecr_from_etapa_curs()` de server.py (codi mort que duplica i contradiu el resolver canònic)

## B7 — 🟡 SSE no ha de filtrar l'error cru (server.py, ~línia 4479)
Substituir `'error': str(task_err)` per `'error': _safe_error(task_err)` (el helper ja existeix a la línia 421).
Commit: `fix(seguretat): usar _safe_error al stream SSE d'adaptacio`

## En acabat
1. `python -m adaptation.params_resolver` → TOTS OK (ara 18 casos amb el nou).
2. `node tests/test_complements_matriu.js` → sense canvis (no toquem complements).
3. Provar una adaptació real en local amb perfil AACC+dislèxia i confirmar a la traça: "AACC sense 2e" ja NO apareix; el MECR es manté al del curs.
4. Recordatori per al Miquel: comunicar al DOP la decisió 2e formalitzada (constitutives) i valorar si l'avís groc de la UI ha de dir que el backend ja ho aplica automàticament.
