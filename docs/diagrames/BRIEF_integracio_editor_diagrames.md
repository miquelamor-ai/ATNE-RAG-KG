# Brief d'integració — Editor de diagrames Novak (ATNE)
**Data:** 12 juny 2026 · **Origen:** prototip validat amb Miquel (v0.10) + auditoria del renderitzador
**Executor:** Claude Code sobre el repo local · **Revisor:** Miquel (aprovació per blocs)

Aquest brief té DOS blocs independents:
- **(A) Correccions de producció** del renderitzador `mermaid-converter.js` — bugs latents que afecten mapes que el sistema ja pot generar avui. Es poden aplicar i desplegar sols.
- **(B) Funcionalitat nova** — el subsistema d'edició Novak complet (afegir/editar/eliminar nodes i connexions sobre el diagrama). Depèn de (A).

**Adjunts:** `patch_renderer_diagrames.diff` (bloc A) · `diagram-editor-core.js` (bloc B, nucli)

## Instruccions generals
1. Branca nova: `git checkout -b feat/editor-diagrames-novak`
2. Aplica primer (A), verifica, commit. Després (B). Un commit per bloc com a mínim.
3. Mostra diffs i atura't per revisió. No push sense ordre.
4. Tot és vanilla JS pur (zero dependències noves) — coherent amb l'stack ATNE.

---

# BLOC A — Correccions de producció del renderitzador

Aplica `patch_renderer_diagrames.diff` a `ui/atne/js/mermaid-converter.js`:
```
git apply patch_renderer_diagrames.diff
```
(Verificat: el diff aplica net sobre la versió actual del repo i el resultat passa els tests funcionals.)

Conté **quatre fixos**, tots a `buildConceptMap`, tots amb compatibilitat enrere demostrada (un mapa sense aquestes característiques renderitza geometria **idèntica byte a byte** a l'actual):

### A1 — Layout de profunditat arbitrària (bug latent)
El layout actual col·loca només 2 nivells per columna; els nodes de 4t nivell o més quedaven **sense coordenades i es descartaven en silenci**. Afecta mapes B2 ("4+ nivells, jerarquització complexa") i C1 (multi-font) que el propi prompt demana. Ara el layout és recursiu.

### A2 — Fork horitzontal de proposicions germanes
Quan un concepte (o l'arrel) té 2+ proposicions, ara es despleguen **en paral·lel** (costat a costat, pare centrat a sobre) en lloc d'apilar-se en vertical (que les feia semblar una cadena encadenada falsa).

### A3 — Routing d'arestes sense travessies enganyoses
Una aresta entre nodes de la mateixa columna que tenia un subarbre aliè pel mig dibuixava una recta que **mentia sobre la jerarquia**. Ara fa bypass lateral.

### A4 — z-order i viewBox dels enllaços creuats
(Aquesta part del diff dona suport al bloc B, però és inofensiva sense ell: si no hi ha bloc "Enllaços creuats" al markdown, no fa res.) Les arestes creuades es dibuixen DESPRÉS dels nodes (z-order) i el viewBox s'eixampla per encabir-les; routing multi-carril perquè múltiples enllaços no se solapin.

### Verificació del bloc A
- Generar (o enganxar a un mapa de test) una cadena de 4+ nivells i confirmar que TOTS els nodes es dibuixen.
- Un mapa de 3 nivells existent ha de renderitzar EXACTAMENT igual que abans.
- **Test de regressió recomanat** (cablejar al CI determinista): un test node que, amb DOM stub, comprovi que `buildConceptMap` d'una cadena profunda produeix tants nodes amb `data-line` com ítems al markdown (cap descartat). Patró al final d'aquest brief.

### Nota sobre tipografia (decisió pendent de Miquel)
Al prototip vam apujar la mida de les proposicions (PFS 11→13) i l'alçada (PH 22→26) perquè es llegien petites. **El diff NO inclou aquest canvi** (l'he revertit a producció) perquè la decisió correcta és **modular-ho per perfil**: un alumne amb baixa visió o dislèxia hauria de rebre el diagrama amb tipografia més gran, com ja preveu el backlog `tipografia_adaptada`. Recomanació: fer `PFS`/`PH` funció del perfil quan s'implementi aquell camp, no hardcodejar 13.

---

# BLOC B — Subsistema d'edició Novak

Permet, sobre el diagrama renderitzat: afegir conceptes/proposicions amb `+` contextual, eliminar amb `×`, crear connexions creuades amb `↝`, i editar/eliminar connexions clicant-les. Tot sobre **font única** (el markdown) amb undo/redo.

### B1 — Nucli (fitxer nou): `ui/atne/js/diagram-editor-core.js`
Copia l'adjunt `diagram-editor-core.js` tal qual a `ui/atne/js/`. Exposa `window.ATNE_EDIT_CORE` amb mutacions PURES de markdown (sense DOM), totes testejades:
- `classify(md, lineIdx)` → 'root' | 'prop' | 'concept'
- `addChild` / `addSibling` / `deleteSubtree` / `descendantCount` / `nodeCount`
- `shiftLines` / `wrapSelection` (toolbar: Tab, negreta/cursiva amb toggle)
- `splitCross` / `addCross` / `removeCross` / `updateCrossLink` / `renameInCross` (enllaços creuats)

Inclou-lo a la pàgina del pas 4 (o on es renderitzin els complements) ABANS de `mermaid-converter.js`.

### B2 — Petit canvi al renderitzador per a la interactivitat
A `buildConceptMap`, les etiquetes dels enllaços creuats ja porten `data-cross-idx` (ve amb el diff del bloc A). El bloc B s'hi enganxa.

### B3 — Capa d'UI (codi nou)
La lògica d'UI del prototip està a `/home/claude/editor/extension.js` (no és un adjunt directe perquè conté codi d'arrencada del banc de proves que NO va a producció). Adapta-la així:
- **Reutilitza**: `injectButtons` (botons +/×/↝ al popup de node existent), `startConnect`/mode connexió, `showCrossPopup` (editar/eliminar connexió), undo/redo, toolbar de l'editor de font, vista prèvia en viu.
- **NO copiïs**: el bloc `DOMContentLoaded` que llegeix `#seed`/`#diagram`/`#src` (és del banc de proves). En producció, `state.cont` és el contenidor real del diagrama i `md()` ve del flux d'adaptació, no d'un `<textarea>` seed.
- **Punt d'enganx**: el renderitzador ja té `addEditListeners` que obre el popup d'edició de node. La capa B afegeix botons a aquest popup i un listener nou per als clics sobre `data-cross-idx`.

### B4 — Modulació per MECR (regla del canon, no hardcoded)
Al prototip, el botó `+ proposició` dels conceptes permet profunditat il·limitada. En producció, **graduar per MECR** com la resta: A2 fins a 2 nivells, B1 fins a 3, B2+ lliure. Llegir el límit del canon (rubrica.json, `pas_3` profunditat) — NO escriure'l al codi. Mateix patró que la resta de complements: el codi consumeix, el canon mana.

### Verificació del bloc B
- Crear concepte, proposició germana (ha de quedar en paral·lel), eliminar amb confirmació si té fills.
- Crear connexió amb ↝ (dos clics + paraula d'enllaç), clicar-la per editar el verb, eliminar-la.
- Undo/redo (Ctrl+Z / Ctrl+Y) revertint cadascuna de les operacions anteriors.
- Confirmar que tot s'escriu al markdown font (és l'única font de veritat).

---

# Test de regressió per al CI (afegir a tests/)

`tests/test_diagram_layout.js` — determinista, sense LLM, cablejar al ci.yml:
```javascript
// Carrega mermaid-converter.js amb DOM stub i ATNE_EDIT_CORE.
// Verifica per a mostres de markdown:
//  1. Cadena de 4+ nivells -> nº nodes amb data-line === nº ítems del markdown (A1)
//  2. Concepte amb 2 proposicions -> tenen la mateixa y i x diferents (A2, fork)
//  3. Mapa de 3 nivells -> geometria byte-a-byte estable (snapshot, evita regressions)
//  4. Bloc "Enllaços creuats" -> splitCross el separa; parseTree de l'arbre el ignora
```

---

# Resum d'execució recomanat
1. **Bloc A** (aplica diff → verifica regressió → commit). Es pot desplegar sol: corregeix bugs de producció.
2. **Bloc B** (nucli → capa UI adaptada → modulació MECR → verifica). Funcionalitat nova.
3. Test de regressió al CI.
4. Quan Miquel ho aprovi: merge + deploy. Verificació visual final amb una adaptació B1 real (mapa amb proposicions verbals + 1-2 enllaços creuats) — material ideal per ensenyar al DOP què fa l'eina.
