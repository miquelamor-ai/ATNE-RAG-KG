# Pas 3 · Adaptació — Guia d'implementació

Aquest document descriu el comportament del **Pas 3**, la pantalla més complexa d'ATNE. Per a la resta de passos, el prototip HTML és suficient. Aquí explicitem comportaments que no són obvis de llegir el codi del prototip.

**Prototips de referència:**
- `ATNE Pas3 V1.html` — vista d'adaptació individual amb eines d'edició
- `ATNE Pas3 Grup.html` — vista d'adaptació grupal amb eines d'edició

Totes dues comparteixen la mateixa barra d'eines, menú de paràmetres i lògica d'undo.

---

## 1. Estructura de la pantalla

```
.main (grid 240px | 1fr)
 ├── .lside    — rail esquerre amb Perfils (individual) o Versions (grup)
 └── .rside    — àrea principal
      ├── (individual) 2 columnes: .doc-pane (original) + .doc-pane (adaptat)
      └── (grup)       4 columnes en grid: 1 per versió
```

### Diferència individual vs. grup

| | Individual | Grup |
|---|---|---|
| Rail esquerre | Llista d'**alumnes** (amb xips de perfil NEE) | Llista de **versions** (A2, TDAH, Dislèxia, AC) |
| Àrea central | **Original** a l'esquerra, **Adaptat** a la dreta | Grid de 4 versions, totes a la vegada |
| Focus actual | Alumne seleccionat (1 a la vegada) | Versió seleccionada (1 a la vegada, ressaltada amb vora) |

---

## 2. Tres eines d'edició (compartides entre individual i grup)

El docent pot intervenir en el document adaptat de tres formes. Totes tres s'activen des del mateix document adaptat (o, al grup, des de la versió seleccionada).

### 2.1 Selection toolbar (`.sel-tb`)

**Què fa:** apareix quan el docent selecciona text dins del document adaptat. Permet aplicar una acció ràpida sobre el text seleccionat.

**Com apareix:**
- Event: `mouseup` sobre un `.doc-read` editable.
- Si la selecció és no-buida → calcular el `getBoundingClientRect()` de la selecció, posicionar el toolbar **a sobre del centre de la selecció**, amb offset de ~8px.
- Si la selecció és buida → ocultar.

**Posicionament:** `position: fixed`, amb `left` i `top` calculats via JS. Té una fletxeta cap avall (`::after` pseudo-element, CSS-only).

**Botons (per ordre):**
1. **Regenerar** (icona `refresh-cw`) — llança regeneració parcial *només sobre la selecció*. Veure §3.
2. **Simplificar** (icona `type`) — redueix vocabulari/complexitat del fragment.
3. **Expandir** (icona `maximize-2`) — afegeix explicació o exemple al fragment.
4. Separador vertical.
5. **Marcar com a clau** (icona `highlighter`) — aplica la marca visual de "paraula/frase clau" segons la versió (groc per TDAH, subratllat per dislèxia, etc.).
6. **Afegir nota** (icona `message-square`) — afegeix un comentari del docent, visible en mode revisió.

Tots els botons són `icon-only`, 28×28px, amb tooltip (atribut `title`).

**Estil:**
```css
background: var(--ink-900);
color: #fff;
border-radius: var(--r-md);
box-shadow: var(--sh-lg);
padding: 4px;
display: flex; gap: 2px;
```

Botons: `color: #fff; opacity: .75;` → `opacity: 1` en hover.

**Comportament d'ocultació:**
- Si el docent clica fora de la selecció → amagar.
- Si clica un botó → executar l'acció i amagar (excepte "Marcar com a clau" que només aplica la classe i deixa el toolbar obert perquè el docent pugui afegir nota seguidament).

---

### 2.2 Paràmetres (`.paramenu`)

**Què fa:** popover ancorat a cada **targeta de versió** (al capçal de la versió adaptada, a l'esquerra del botó de regenerar). Permet ajustar paràmetres específics de la versió *abans* de regenerar, i torna a generar la versió sencera amb els nous paràmetres.

**Com s'activa:** clic sobre el botó `.param-btn` (icona `sliders-horizontal`) al capçal de la versió.

**Posicionament:** popover flotant, ancorat al botó. `position: absolute` sobre un contenidor `position: relative` que és el capçal de la versió. Típicament `top: calc(100% + 6px); right: 0`.

**Tancament:**
- Clic fora del popover → tanca.
- Clic al botó "Aplicar" → aplica i tanca (i llança regeneració sencera).
- Tecla Esc → tanca sense aplicar.

**Contingut del popover (varia segons la versió):**

Cada paràmetre és una fila (`.paramenu-row`) amb:
- **Label** (`.paramenu-lbl`) — nom curt
- **Control** — slider, select o toggle
- **Valor actual** (`.paramenu-val`) — a la dreta, en mono, mostra el valor seleccionat

#### Paràmetres per versió (mínim)

| Versió | Paràmetres |
|---|---|
| **A2 (idioma)** | Nivell CEFR (select: A1/A2/B1), Vocabulari tècnic (slider 0–100%: "tot traduït" ↔ "intacte"), Glossari al marge (toggle) |
| **TDAH** | Longitud de frase (slider curt/mitjana/llarga), Marques clau (toggle), Pauses actives (select: cap / cada 2 paràgrafs / cada paràgraf), Icones (toggle) |
| **Dislèxia** | Mida tipogràfica (slider 15–20px), Interlineat (slider 1.6–2.2), Espaiat entre caràcters (slider 0–4%), Subratllar paraules clau (toggle) |
| **Altes capacitats (AC)** | Nivell de profunditat (select: repte / extensió / investigació), Preguntes obertes (toggle), Referències externes (slider 0–5) |

Els valors per defecte han de coincidir amb el que es mostra al prototip. Els valors seleccionats es guarden **per alumne** (individual) o **per versió** (grup).

**Botó "Aplicar"** (a la part inferior del popover):
- Estil `btn-primary`, full-width dins del popover.
- En clicar: tanca el popover i llança l'**overlay de regeneració** (§3) sobre la versió sencera, no sobre una selecció.

**Botó "Restablir"** (opcional, secundari):
- Reverteix als valors per defecte.

---

### 2.3 Regeneració (overlay `.regen`)

**Què fa:** quan hi ha una operació asíncrona de regeneració (parcial o sencera), apareix un overlay sobre el contenidor afectat que bloqueja la interacció i mostra el progrés.

**Trigger:**
- Selection toolbar → "Regenerar / Simplificar / Expandir" → overlay **només sobre el rang seleccionat**.
- Paràmetres → "Aplicar" → overlay sobre la **versió sencera** (`.doc-pane` o la targeta de versió al grup).

**Comportament visual:**
- `position: absolute` dins d'un contenidor `position: relative`.
- Cobreix el 100% del contenidor, amb un fons semi-translúcid: `background: rgba(244, 241, 232, .85)` (cream amb alfa).
- Backdrop-filter `blur(2px)` si el navegador ho suporta.
- Centrat: un petit "card" blanc amb l'estat.

**Contingut del card d'overlay:**
- Spinner (SVG animat o `border` rotant).
- Text: "Regenerant amb GPT-4..." (o model que correspongui), font `var(--mono)`, `--fs-xs`.
- Línia de progrés opcional (determinista si el backend ho proporciona, si no omès).
- Botó "Cancel·lar" (text link, sota el text).

**Regeneració parcial vs. sencera:**
- **Parcial:** l'overlay es limita al rang del fragment afectat. Es pot implementar col·locant l'overlay dins d'un wrapper que envolta només el fragment, o mesurant les línies amb `Range.getClientRects()` i dibuixant l'overlay sobre aquelles coordenades.
- **Sencera:** l'overlay cobreix tota la targeta `.doc-pane` de la versió.

**Duració:**
- Típicament 1.5–3s en prototip (`setTimeout`). En producció, depèn del temps real de crida a LLM.
- **Mínim 600ms** d'overlay encara que la resposta arribi abans, per evitar el *flash* visual.

**En completar:**
- El fragment (o la versió sencera) es substitueix amb el nou text.
- L'overlay fa un fade-out de 200ms.
- Si hi havia una selecció prèvia a la selection toolbar, es manté seleccionada sobre el nou text (per permetre encadenar accions).

---

## 3. Undo / Redo

Tota acció d'edició que modifiqui el document adaptat ha d'anar al historial d'undo.

**Accions rastrejades:**
- Regenerar (parcial o sencera)
- Simplificar / Expandir fragment
- Marcar com a clau / treure marca
- Afegir / eliminar nota del docent
- Canviar paràmetres (un sol undo per "Aplicar", no per cada slider mogut)
- Edició manual de text (si s'habilita `contenteditable`)

**Controls:**
- Botons a la topbar: **Undo** (`undo-2`) i **Redo** (`redo-2`).
- Atalls de teclat: `Cmd/Ctrl+Z` i `Cmd/Ctrl+Shift+Z`.
- Estat deshabilitat (`opacity: .4; pointer-events: none`) quan no hi ha res per desfer/refer.

**Granularitat:**
- Cada "Aplicar" de paràmetres = 1 entrada.
- Cada acció de selection toolbar = 1 entrada.
- Edició manual a `contenteditable` → agrupar per "burst" de 1s d'inactivitat abans de crear una nova entrada (patró estàndard d'editors).

**Implementació suggerida:**
Pila de snapshots del document adaptat (un per versió si estem en vista grup). No cal operar a nivell de diffs.

---

## 4. Estats buits i de càrrega

### Generació inicial del Pas 3
En entrar al Pas 3 per primera vegada, les versions adaptades **encara no existeixen**. Comportament:

- Cada `.doc-pane` (individual) o targeta de versió (grup) mostra un estat "generant" que és el mateix overlay de regeneració sencera (§3).
- Es generen en paral·lel. A mesura que cada una acaba, l'overlay desapareix i apareix el contingut.
- La topbar mostra un comptador discret: "Generant 3 de 4..." a l'esquerra dels botons d'acció.

### Entrada del Pas 2 al Pas 3
El stepper de la topbar ha de mostrar el Pas 2 amb `.done` (check) i el Pas 3 amb `.on`. Si el docent torna al Pas 2, el Pas 3 **no es regenera automàticament** llevat que canviï el document original; en aquest cas, avisar amb un toast: "El document original ha canviat. Vols regenerar les adaptacions?" amb botons "Regenerar" / "Mantenir".

---

## 5. Keyboard shortcuts (resum)

| Tecla | Acció |
|---|---|
| `Cmd/Ctrl+Z` | Undo |
| `Cmd/Ctrl+Shift+Z` | Redo |
| `Esc` | Tancar popover de paràmetres / amagar selection toolbar |
| `Cmd/Ctrl+Enter` | Aplicar paràmetres (quan el popover és obert) |
| `Cmd/Ctrl+→` | Pas següent |
| `Cmd/Ctrl+←` | Pas anterior |

---

## 6. Responsiu

Els prototips estan dissenyats a **1440px de width**. Comportament a altres mides:

- **≥1440px:** igual que prototip.
- **1200–1440px:** rail esquerre es redueix a 200px; grid de versions al Pas 3 Grup passa de 4 col a 2×2.
- **<1200px:** vista "mobile-first" fora d'abast d'aquest entregable; avisar amb un banner "ATNE està optimitzat per a escriptori".

---

## 7. Checklist d'implementació

- [ ] Tokens i base.css aplicats globalment
- [ ] Estructura `.wrap > .rail + .canvas` comuna a tots els passos
- [ ] Stepper reutilitzable amb estats `on` / `done`
- [ ] Rail esquerre amb llista d'alumnes (individual) i llista de versions (grup)
- [ ] `.doc-read` amb variants `.v-a2 / .v-tdah / .v-disl / .v-ac`
- [ ] Selection toolbar flotant, ancorada a selecció de text
- [ ] Popover de paràmetres amb contingut dinàmic per versió
- [ ] Overlay de regeneració, parcial i sencera
- [ ] Pila d'undo/redo amb atalls de teclat
- [ ] Estat de "generació inicial" del Pas 3
- [ ] Warning en tornar al Pas 2 i modificar el document original
- [ ] Focus visible accessible a tots els elements interactius
- [ ] Verificació de contrast WCAG AA per a qualsevol nova combinació
