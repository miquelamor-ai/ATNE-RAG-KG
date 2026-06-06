# RESPOSTA mineriaRAG → handoff "Mapa de taxonomies"

**Data:** 2026-06-06
**De:** mineriaRAG (Miquel + Claude)
**Per a:** ATNE
**Re:** `handoff_mineriarag_mapa_taxonomies.md`

---

## Resum executiu

El handoff era **sòlid**. S'ha canonitzat al corpusFJE després de triangular 4 veus:
ATNE + **NotebookLM (notebook MALL, 28 fonts)** + recerca acadèmica externa + revisió
mineriaRAG. El consens **confirma l'essencial i corregeix 3 punts**.

**Commit corpusFJE:** `a7b3df9`.

Canvis:
1. **NOU `M2_marc-teoric-mediacio.md`** (`tipus: marc`) — genealogia teòrica integrada:
   transformacions→marcs, complements→teòrics, creuament de les 3 taxonomies, llinatge complet.
2. **`M2_instruments-mediacio-pedagogica.md`** — resolta la incoherència 3 vs 7-8 famílies.

---

## Resposta a les 5 demandes

### 1. Canonitzar el mapa? On?
**SÍ.** Doc nou `M2_marc-teoric-mediacio.md` (separa *fonament teòric* de *catàleg operatiu*,
que es queda a `M2_instruments`). El catàleg no s'ha de duplicar; el marc nou n'és el fonament.

### 2. Pilar de l'oralitat
**No és una transformació futura: JA és fonament canònic del MALL.** NotebookLM ho demostra
amb fonts: lectura mediada per l'adult, *information talk*, dictat a l'adult, consignes d'acció
oral a pre-A1. Canonitzat com a **eix oral/escrit transversal** de tota transformació, no com a
4a transformació separada. ATNE pot, si vol, implementar "text → guió oral" per a pre-A1/A1
amb base canònica sòlida.

### 3. Incoherència 3 vs 7-8 famílies
**RESOLTA**, i la teva proposta era correcta. NotebookLM confirma: **3 mares estructurals**
(per funció: lingüístiques/cognitives/metacognitives) ⊃ **desplegament operatiu** (per naturalesa
del recurs). PERÒ atenció a l'anidament exacte (el catàleg actual no el feia bé):
- **Lingüístiques** ⊃ lèxiques · sintàctiques · discursives
- **Cognitives** ⊃ visuals/multimodals · de lectura · de producció
- **Metacognitives** ⊃ procedimentals/checklists · d'autoavaluació

S'ha afegit frase-pont a §Taxonomia i nota d'anidament al §Catàleg.

### 4. Els 5 teòrics absents
**CONFIRMATS els 5** (Halliday, Camps/Zayas, Bajtín, J.M. Adam, Solé) — tots citats
nominalment pel MALL. **A més, NotebookLM en va detectar 6 més** que també falten i s'han
afegit: **Mercer** (aula dialògica), **Sanmartí** (avaluació reguladora), **Jorba-Gómez-Prat**
(HCL), **Fons** (alfabetització inicial), **González-Davies/Corcoll** (TOLC/PBCS), **MELVIVES 2015**.

### 5. Consum per ATNE
Un cop derivat a JSON, ATNE pot citar l'origen teòric de cada decisió al "Per al docent".
El marc nou té la columna **Estatus al MALL** (fonament intern vs convergència externa) — útil
per no sobreatribuir.

---

## ⚠️ 3 CORRECCIONS al teu mapeig (validades per NotebookLM)

1. **Gèneres = Bajtín/Adam, NO Gibbons.** Ja ho deies bé al handoff; reforçat. Però el M2
   tenia Gibbons mal posat com a origen de gèneres → corregit. Gibbons queda com a referent
   extern de *scaffolding* en CLIL, no de gèneres.

2. **🔴 Sweller DESMARCAT.** Atribuïes "menys és més" i la segmentació a Sweller. **NotebookLM:
   Sweller NO apareix a cap de les 28 fonts del MALL.** El "menys és més" és **principi propi
   del MALL**. Sweller queda com a *convergència externa*, mai com a fonament. (La recerca
   externa confirma que el concepte de Sweller és real, però el MALL no se'n reclama.)
   → **Acció suggerida a ATNE:** revisar qualsevol lloc on el "Per al docent" citi Sweller com
   a font del límit de preguntes; substituir per "principi MALL (menys és més)".

3. **Ausubel/Mayer/Novak/Buzan** = convergència externa, no MALL. Tal com ja marcaves amb
   asterisc; consolidat com a regla al doc nou.

---

## Estat

- ✅ corpusFJE actualitzat i pushat (`a7b3df9`).
- ✅ Auditoria passada (`audit_corpus.py`): doc nou sense issues.
- ⏭️ Pendent ATNE: derivar a JSON quan calgui; revisar atribucions a Sweller al "Per al docent".
