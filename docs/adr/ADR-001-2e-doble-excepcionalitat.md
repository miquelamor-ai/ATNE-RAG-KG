# ADR-001 — Definició i detecció de la doble excepcionalitat (2e)

- **Estat:** Acceptat (criteri per defecte) · ⏳ pendent ratificació formal del DOP
- **Data:** 2026-06-12
- **Decisió de:** Miquel Amor · recomanació auditoria (Fable) + verificació codi (Claude Code)
- **Context relacionat:** bug B1 (auditoria 12/06), `adaptation/params_resolver.py`

## Context i problema

L'alumnat de **doble excepcionalitat (2e)** = altes capacitats (AACC) + una altra
condició. Pedagògicament, un alumne 2e NO ha de rebre el **+1 de nivell MECR** ni un
**DUA d'Enriquiment pur** que reben els AACC: necessita mantenir el repte cognitiu *al
nivell del curs* però amb la **via d'accés** que la seva altra condició demana.

**El bug (B1, viu en producció):** el resolver decidia el 2e a partir d'un flag
`doble_excepcionalitat` que **cap fitxer de la UI activa establia mai**. Resultat: un
alumne AACC + dislèxia rebia text **MÉS difícil** (B2/Enriquiment) — el contrari del que
la UI prometia al docent. La detecció vivia a la presentació; la decisió, al backend; i el
contracte entre ells (el flag) no existia.

## Decisió

1. **Autodetectar el 2e al backend** (font única), sense dependre de cap flag de client.
   Implementat com `_is_2e(chars, actives)` a `params_resolver.py`.
2. **Definició de 2e:** AACC + **una altra característica CONSTITUTIVA** activa.
   - **CONSTITUTIVA** (excepcionalitat: discapacitat o trastorn diagnosticat) → SÍ activa 2e.
     Ex: dislèxia, TEA, TDAH, DI, TDL, discalcúlia, dispràxia, discapacitat auditiva/visual,
     **`trastorn_emocional`** (trastorn diagnosticat).
   - **CONTEXTUAL** (situacional, no és una excepcionalitat) → NO activa 2e per si sola.
     Ex: `nouvingut`, `vulnerabilitat` (socioeconòmica), `vulnerabilitat_emocional`
     (situacional: dol, crisi puntual).
3. El flag explícit `doble_excepcionalitat` (si arriba) **es continua respectant**.

`_CONTEXTUALS = {"nouvingut", "vulnerabilitat", "vulnerabilitat_emocional"}`
(`vulnerabilitat_emocional` s'hi inclou per forward-compat de la taxonomia documentada; el
resolver actual rep la grafia `vulnerabilitat`).

## Conseqüències

- **Comportament nou (correcte):** AACC + dislèxia (sense flag) → B1/Core (abans
  B2/Enriquiment). AACC sola → B2/Enriquiment (intacte). AACC + `vulnerabilitat`
  situacional → NO 2e: s'aplica el +1 (les dues forces es compensen: base B1 → −1
  vulnerabilitat → A2 → +1 AACC → B1, amb Enriquiment). AACC + `trastorn_emocional` → 2e.
- **Blindat amb smoke tests** a `params_resolver.py` (`__main__`): fixen la distinció
  situacional/diagnosticat per sempre.
- **Pilot:** si algun docent havia generat adaptacions per a alumnes 2e abans del fix, les
  noves sortiran **diferents (millors)**. Anotar-ho al canal del pilot.

## Punt obert (no bloquejant)

La frontera exacta constitutiva/contextual (especialment `trastorn_emocional` vs
`vulnerabilitat_emocional`, i `comprensio_lectora`) ha de ser **ratificada pel DOP**.
Mentre el DOP no digui el contrari, **mana aquesta taxonomia documentada**. Un refinament
posterior és un canvi d'una línia a `_CONTEXTUALS` + actualitzar el smoke test — barat i
traçable. Quan el DOP respongui, tancar-ho en aquest mateix ADR.
