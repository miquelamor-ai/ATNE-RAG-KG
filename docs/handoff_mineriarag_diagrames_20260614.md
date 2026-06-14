# Handoff a mineriaRAG — necessitats de canon per a l'editor de diagrames (ATNE)

**Data:** 14 juny 2026 · **De:** ATNE (editor de diagrames bloc B) · **Per a:** mineriaRAG (canon corpusFJE)

## Context

ATNE ha afegit **edició interactiva** als diagrames (mapa conceptual Novak), **graduada per MECR consumint el canon** (`rubrica.json` de cada skill, via build-script → derivat `.data.js` → consum al frontend, amb drift-guard). Ara s'estén l'edició a **mapa mental** i **esquema visual**. Calen 2 coses al canon perquè ATNE les pugui consumir (ATNE = consumidor, mai origen).

## Petició 1 — `generate-mapa-mental`: falta el `rubrica.json`

La skill `skills/mediacio/generate-mapa-mental/` **existeix** però **no té `rubrica.json`**, a diferència de `generate-mapa-conceptual` i `generate-esquema-visual`, que sí en tenen.

ATNE necessita el derivat amb la **graduació per MECR** (profunditat / total de nodes / nombre de branques per nivell) per graduar l'editor de mapa mental. Sense això, l'editor de mapa mental va **sense límit MECR** (estat actual: és el que ATNE ha desplegat ara — `capsObj()` retorna `null` per a `mapa_mental` → profunditat lliure).

**Bona notícia: la graduació JA EXISTEIX a la prosa del `SKILL.md`** (`generate-mapa-mental/SKILL.md`, secció «Graduació per nivell MECR»). Només cal **canonitzar-la** a `rubrica.json` (la prosa del SKILL.md no és font consumible per ATNE — ATNE només llegeix el derivat de `rubrica.json`). La taula literal del SKILL.md:

| Nivell | Nombre branques | Profunditat |
|---|---|---|
| Pre-A1 / A1 | 2-3 branques | 1 nivell |
| A2 | 3-4 branques | 1-2 nivells |
| B1 | 4-5 branques | 2 nivells |
| B2 | 5-7 branques | 2-3 nivells |
| C1+ | 5-8 branques | 3 nivells |

→ **Si us plau, canonitzar `generate-mapa-mental`** (M3_instrument + `rubrica.json`) amb la mateixa estructura de `levels`/`passos` que les altres skills de diagrama. Per al consum d'ATNE n'hi ha prou amb **2 senyals comptables** (com l'esquema): **profunditat** (nivells de l'arbre) i **densitat/total de nodes** o **nombre de branques** per MECR. Quan existeixi el `rubrica.json`, ATNE només haurà d'afegir l'extracció al build-script i una clau `mapa_mental` al derivat (canvi mecànic, ja previst a `capsObj()`).

## Petició 2 — Nombre recomanat d'enllaços creuats (cross-links)

El canon de `generate-mapa-conceptual` **no especifica** quants enllaços creuats (cross-links Novak) són recomanables en un mapa. ATNE usa ara un **valor temporal de plataforma** (`CROSS_REC = 3`, hardcoded a `diagram-editor-ui.js`) per **avisar** (no blocar) quan n'hi ha massa.

→ **Si us plau, definir al canon** el nombre recomanat d'enllaços creuats (segons Novak/CmapTools en són **pocs**, 1-2; per MECR o valor únic?) perquè ATNE el consumeixi en lloc del hardcoded.

## Nota — esquema visual ja està OK (CONSUMIT per ATNE)

`generate-esquema-visual/rubrica.json` ja existeix amb `pas_2_profunditat_de_l` + `pas_2_total_nodes` (estructura de passos DIFERENT de mapa-conceptual). ATNE **ja el consumeix**: el build-script en deriva la clau `esquema` (`levels` de `pas_2_profunditat_de_l`, `densitat_max` de `pas_2_total_nodes.countable.max`) a `diagram-mecr-depth.data.js`, amb drift-guard propi. **No cal res de mineriaRAG** per a l'esquema.

---

*Referència ATNE: [[project_handoff_editor_mm_esquema_20260614]] (memòria) · branca `feat/editor-diagrames-mm-esquema` (stacked sobre `feat/editor-diagrames-blocB`).*
