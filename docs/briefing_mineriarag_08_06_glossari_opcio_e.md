# Briefing reunió mineriaRAG · 8 de juny 2026

> **Per a**: Joan (mineriaRAG)
> **De**: Miquel (ATNE)
> **Tema**: Decisió arquitectònica oberta del 31/05 (glossari A/B/C) — proposem opció **E** validada empíricament

---

## TL;DR

La decisió oberta del 31/05 (A reescriure 37 M3 imperatiu / B compilador / C rúbrica JSON amb llistes) **queda tancada** a favor d'una nova **opció E**: rúbrica JSON simplificada al backend + **vàlvula humana al Pas 3 d'ATNE** (botó esborrar entries + toggles columnes). Validat amb **39 crides reals** la nit del 31/05.

Per al 8/06: **4 decisions arquitectòniques** + **2 decisions pedagògiques** per consensuar.

---

## Per què opció E (no A, B ni C)

| Opció | Què | Per què no |
|---|---|---|
| A | Reescriure 37 M3 en imperatiu | Lligat a OpenAI; sobreengineering si canviem model |
| B | Compilador descriptiu→imperatiu | Bona, però depèn de regles de transformació complexes |
| C | Rúbrica JSON amb `case_overrides` + llistes finites (mitja, botó, agulla, fil...) | **Bloqueig pedagògic**: impossible enumerar exhaustivament les paraules quotidianes |
| **E** | **Auto al backend (rúbrica simple) + post-edició docent al Pas 3** | **ATNE proposa, docent decideix**. Resol el cas titella sense necessitat d'enumerar res |

Pilot empíric (39 crides, GPT-4o + Gemma 4):
- Opció C amb llistes: **0/4 PASS** al cas titella (mitja/agulla/fil tornaven a sortir)
- Opció E + R4 al Pas 2: **resol arquitectònicament** (no oferint glossari quan no toca per a 1r-3r primària sense condicions)
- Bastides amb JSON estructural: **12/12 PASS** + 3 bugs pedagògics del baseline detectats (L1 inventada, format heterogeni, castellanismes)

---

## 4 decisions arquitectòniques (cal alineament)

### D1 · Com es genera `rubrica_*.json` per a cada SKILL?
- **Opció A**: pipeline mineriaRAG ho deriva automàticament del M3 v4.0.0 (extensió del `build_skills.py`)
- **Opció B**: ATNE manté els JSONs manualment al repo
- **Recomanació**: A — preserva el principi "M3 = font canònica única", JSON = derivat

### D2 · El M3 actual del glossari s'ha de modificar?
El M3 actual té cel·les qualitatives en prosa ("paraules quotidianes òbvies"). Amb opció E (vàlvula humana), la complexitat queda a la UI.
- **Opció A**: M3 queda igual; el JSON v2 és una simplificació derivada (només camps tipats)
- **Opció B**: M3 es simplifica per coherència amb el JSON
- **Recomanació**: A — M3 segueix sent canon humà; JSON v2 és la versió operativa per al LLM

### D3 · El patró JSON s'estén a les 37 SKILLs?
Bastides validat 12/12. Glossari validat. Resten 35.
- **Opció A**: aplicar a totes 37 (un sol cop, batch)
- **Opció B**: només a les que tenen bugs coneguts (glossari, bastides, pictogrames + 3-4 més detectats)
- **Opció C**: només a glossari per ara; resta després del pilot
- **Recomanació pendent** — depèn capacitat mineriaRAG

### D4 · Pictogrames: dins el pipeline JSON o aparcat?
Pictogrames té `agent_role=adapter` (no `complements`) → s'insereix INLINE al text adaptat, no és una crida separada.
- **Opció A**: refactor del pipeline ATNE per testar adapters amb JSON (cost mig)
- **Opció B**: aparcar pictogrames per a una fase posterior; mantenir directiva Python actual
- **Recomanació**: B — pictogrames té un problema diferent (densitat per nivell, ARASAAC vs emoji) que no és lèxic-qualitatiu. No bloqueja la resta

---

## 2 decisions pedagògiques (validar amb mineriaRAG)

### P1 · Format "només L1 + transliteració" per a nouvingut emergent
Pedagògicament defensable per MALL/translanguaging (Cummins & Early 2011, ja citat al M3 línia 152). El M3 línia 87 diu "*la traducció directa és el pont*". Proposta:
- **pre-A1 nouvingut**: Terme + Pictograma + L1 + Translit. **Sense explicació CA** (no la pot llegir)
- **A1 nouvingut**: opcional toggle al Pas 3 (default amb explicació)
- **A2+ nouvingut**: estàndard amb explicació CA

**Pregunta a Joan**: confirma que aquesta lectura és canon MALL?

### P2 · Regla R4 al Pas 2 (1r-3r primària sense condicions → sense glossari per defecte)
Implementada a `ui/atne/js/complements-matriu.js` (commit `452fe3a`). 5/5 tests passen.

**Pregunta a Joan**: l'abast (només 1r-3r primària) és el correcte? Possibles alternatives:
- Restringir més: només 1r-2n primària
- Ampliar: tota primària sense condicions
- Ampliar: pre-A1/A1 totes etapes sense condicions

---

## Material de suport (al repo, commit `452fe3a`)

| Artefacte | Què conté |
|---|---|
| `tests/pilot_glossari_2026_05_31/rubrica_glossari_v2.json` | Rúbrica simplificada definitiva (Nivell 1 sense `case_overrides`) |
| `tests/pilot_glossari_2026_05_31/rubrica_bastides_lectura.json` | Patró JSON estès a bastides (validat 12/12) |
| `tests/pilot_glossari_2026_05_31/pilot.py` + `pilot_v2.py` + `pilot_bastides.py` | Harnesses reproduïbles |
| `tests/pilot_glossari_2026_05_31/resultats_*.json` | Dumps de les 39 crides reals per a inspecció |
| `ui/atne/js/complements-matriu.js` | Regla R4 implementada |

Per a reproduir el pilot:
```bash
python tests/pilot_glossari_2026_05_31/pilot.py --reps 3        # opció C inicial
python tests/pilot_glossari_2026_05_31/pilot_v2.py --reps 2     # opció E (v2)
python tests/pilot_glossari_2026_05_31/pilot_bastides.py        # extensió bastides
```

---

## Calendari proposat (depenent de la conversa)

| Setmana | Què |
|---|---|
| **8/06** | Reunió: validar D1-D4 + P1-P2 |
| 9-13/06 | mineriaRAG: genera `rubrica_*.json` derivats automàtics (depenent D1+D3) |
| 9-13/06 | ATNE: implementa 4 controls UX al Pas 3 (X esborrar + 3 toggles) — ~6-8h |
| 14-20/06 | ATNE: integra rúbriques v2 al pipeline, elimina directives Python lean |
| 21-27/06 | Pilot conjunt amb docent real (cas titella + 2-3 altres) per validar UX |

---

## Resum executiu

**Què ja està fet**: la decisió arquitectònica oberta està tancada amb evidència empírica. El cas titella resolt sense necessitat d'enumerar paraules quotidianes. R4 ja al codi.

**Què ens demana mineriaRAG**:
1. Confirmar la direcció (opció E vs alternativa)
2. Decidir si genera els derivats `rubrica_*.json` automàticament
3. Decidir l'abast (37 SKILLs / 3-4 / només glossari)
4. Validar pedagògicament P1 i P2

**Sortida desitjada de la reunió**: pla d'implementació clar per a la setmana 9-13/06.
