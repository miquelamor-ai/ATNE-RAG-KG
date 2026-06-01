# Senyal T1/T2 → ATNE · forma_sobre_mecr al canon; no_contingut_no_demanat es queda a ATNE

> **Data**: 2026-06-01 · **De**: mineriaRAG · **Per a**: ATNE
> **Resposta a**: `handoff_mineriarag_matriu_transversals_20260601.md` §6 (deute T1/T2)
> **Estat**: ✅ Decisions preses. T1 canonitzat, T2 confirmat com a regla vostra.

## Commit del senyal

**corpusFJE master: `de53387`**
(complet `de533877c6cf0cb4e6d8cb148b782213088e1218`)

## T1 — `forma_sobre_mecr` → AL CANON ✅

Decisió de Miquel: T1 és coneixement pedagògic genuí (preservar l'estructura del
gènere, no aplanar-la per nivell) → puja al canon com a **transversal**.

**Què s'ha fet:**
- `build_rubrica.py` reconeix `forma_sobre_mecr` (type `structural`).
- Els 6 M3 de gènere-forma tenen secció `## Regles transversals` amb el bullet
  **"Forma sobre MECR"**. El text és **idèntic** al vostre bloc `_is_form_genre` →
  **sense canvi de comportament**.
- Els 6 `rubrica.json` ja porten `transversals.forma_sobre_mecr`:

```
write-poema · write-dialeg · write-receptari · write-reglament · write-instructiu · write-manual
```

**Abast**: exactament els 6 que mapegen amb la vostra llista `_form_genres` (poema,
teatre/diàleg/monòleg, recepta, reglament/norma, instructiu, manual, fitxa tècnica).
"Fitxa tècnica" no té skill propi → quedarà cobert si algun dia es crea. **No he
ampliat** l'abast a altres gèneres per no introduir divergència amb el vostre
comportament viu (vegeu pendent sota).

**Acció per a vosaltres:**
1. Bump del submodule corpusFJE a `de53387` (o HEAD posterior; T1 no el toca cap
   altre workflow).
2. Llegir `forma_sobre_mecr` via `skills_loader` (anàleg a `get_format_output` —
   `rubrica["transversals"]["forma_sobre_mecr"]["rule"]`).
3. Retirar el bloc Python `if _is_form_genre:` de `prompt_builder.py` i substituir-lo
   per la lectura del canon. Test: el prompt resultant per a un gènere-forma ha de
   seguir contenint la regla (mateix text).

> Com sabeu quins gèneres són "de forma"? El canon ho marca **per presència del
> transversal**: si `rubrica["transversals"]` conté `forma_sobre_mecr`, és gènere-forma.
> Així no cal mantenir la llista `_form_genres` hardcoded — la deriveu del canon.

## T2 — `no_contingut_no_demanat` → ES QUEDA A ATNE ✅

Decisió de Miquel (coincideix amb la vostra hipòtesi): T2 governa el **format de
sortida del vostre pipeline 2-call** (què va dins `## Text adaptat` vs `## Notes
d'auditoria`), no el marc pedagògic MALL. **No puja al canon.**

**Acció per a vosaltres:** deixar el bloc "REGLA CRÍTICA — NO INVENTIS CONTINGUT NO
DEMANAT" a `prompt_builder.py` tal com està, i **actualitzar el comentari** que avui
el marca com a "TRANSVERSAL-EN-TRÀNSIT T2 / pendent decidir amb mineriaRAG":
ara és **regla de plataforma ATNE confirmada**, ja no està en-trànsit.

## Pendent (no bloqueja)

- **Revisar post-pilot** si algun altre gènere amb estructura forta (carta,
  entrevista, enciclopèdic...) també necessita `forma_sobre_mecr`. Si el pilot docent
  ho evidencia: s'afegeix el transversal a aquell M3 + ampliem la detecció. Decisió amb
  evidència al davant, no a priori.

Amb T1/T2 tancats, el deute del handoff §6 queda saldat. Gràcies!
