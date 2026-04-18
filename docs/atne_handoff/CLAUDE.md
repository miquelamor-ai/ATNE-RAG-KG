# CLAUDE.md — Instruccions per a Claude Code (handoff ATNE)

> La **font de veritat del projecte** és el `CLAUDE.md` de l'**arrel** del repositori
> (`c:\Users\miquel.amor\Documents\GitHub\ATNE\CLAUDE.md`). En cas de conflicte amb
> aquest document, mana l'arrel. Aquest fitxer només concreta com aplicar el paquet
> de disseny del handoff (tokens + base + spec del Pas 3) al codi del projecte.

## Stack (confirmat 2026-04-18)

- **HTML + JavaScript pur + CSS**. Zero frameworks. Res de React / Vue / Next / Svelte.
- **Icones**: SVG inline (a `ui/atne/icons.js` o inline a l'HTML). **Res de llibreries d'icones** (no `lucide-react` etc.). Els noms dels icones segueixen la nomenclatura Lucide com a referència, però el marcatge és SVG pla.
- **Servidor**: FastAPI a `server.py` (ja existent). El frontend s'hi serveix com a estàtics.
- **LLM**: el frontend consumeix un **stub** (`ui/atne/js/llm-stub.js`) amb `setTimeout` i text de mostra. Quan la UI estigui validada, s'endolla als endpoints de `server.py` que ja fa servir `ui/workspace.html`. **El frontend no ha de saber quin model LLM hi ha darrere.**

## Integració amb l'app existent

- L'app ATNE actual viu a `ui/` (`ui/workspace.html`, `ui/app.js`, etc.).
- El nou Pas 3 es construeix **en paral·lel** a `ui/atne/`. **No reemplacem** `workspace.html` fins que el nou flux estigui validat amb Miquel.
- La migració serà un pas posterior, separat.

## Què hi ha en aquest directori

| Fitxer | Propòsit |
|---|---|
| `README.md` | Context del producte, convencions, mapa dels prototips. **Llegeix-lo primer.** |
| `tokens.css` | Variables CSS (colors, tipografia, espaiat, radis, ombres). **Cal copiar** a `ui/styles/tokens.css`. |
| `base.css` | Reset + tipografia + primitives (`.btn`, `.chip`, `.doc-read` + variants). **Cal copiar** a `ui/styles/base.css`. |
| `spec-pas3.md` | Guia detallada del Pas 3 (selection toolbar, paràmetres, regeneració, undo/redo). |
| `prototypes/` | 4 prototips HTML — **font de veritat visual**. |

## Estructura de fitxers al projecte

```
ui/
├── styles/
│   ├── tokens.css          ← còpia literal de docs/atne_handoff/tokens.css
│   ├── base.css            ← còpia literal de docs/atne_handoff/base.css
│   ├── shell.css           ← comú 4 passos: .wrap, .rail, .topbar, .steps, .icon-btn
│   └── pas3.css            ← doc-pane, sel-tb, paramenu, regen, lside (pas3)
├── atne/
│   ├── index.html          ← entrada al nou flux (carrega Pas 1)
│   ├── pas1.html           ← selecció de perfil/grup
│   ├── pas2.html           ← document original
│   ├── pas3.html           ← adaptació (individual + grup a la mateixa pàgina)
│   ├── pas4.html           ← entrega
│   ├── icons.js            ← SVG inline amb nomenclatura Lucide
│   └── js/
│       ├── shell.js        ← stepper, rail, navegació entre passos
│       ├── state.js        ← estat global (pas, grup, doc, versions, undo-stack)
│       ├── pas3-selection.js   ← selection toolbar (mouseup + getBoundingClientRect)
│       ├── pas3-paramenu.js    ← popover paràmetres per versió
│       ├── pas3-regen.js       ← overlay regeneració (parcial + sencera)
│       ├── pas3-undo.js        ← pila de snapshots + atalls de teclat
│       └── llm-stub.js         ← stub amb setTimeout; s'endollarà després a server.py
```

**Ordre de càrrega dels estils** (a totes les pàgines de `ui/atne/`):
1. Google Fonts (Inter, Fraunces, JetBrains Mono)
2. `/ui/styles/tokens.css` ← **primer sempre**
3. `/ui/styles/base.css`
4. `/ui/styles/shell.css`
5. `/ui/styles/pas3.css` (només a `pas3.html`)
6. CSS específic de la pàgina (inline dins del `<style>` si cal)

## Pla d'execució

### Fase 0 — Lectura (feta)

### Fase 1 — Proposta d'arquitectura (feta i confirmada)

### Fase 2 — Base visual + smoke test Pas 1

1. Copiar `tokens.css` i `base.css` a `ui/styles/`.
2. Crear `ui/styles/shell.css` amb la capa comuna (.wrap, .rail, .topbar, .steps, .icon-btn).
3. Crear `ui/styles/pas3.css` (pot començar buit, s'omple a la Fase 4).
4. Construir `ui/atne/pas1.html` reproduint el prototip **ATNE Pas1 V3.html** fidelment.
5. **Parar i ensenyar-ho a Miquel** abans de continuar.

### Fase 3 — Passos 2 i 4

Implementar `pas2.html` i `pas4.html` seguint els prototips. Passos simples.

### Fase 4 — Pas 3 (el complex)

Seguir el checklist final de `spec-pas3.md`. Ordre:
1. Estructura (rail esquerre + àrea central) — individual + grup.
2. 4 variants de `.doc-read` amb text de mostra.
3. **Selection toolbar** (flotant, ancorada a selecció de text).
4. **Popover de paràmetres** (un per versió, contingut dinàmic).
5. **Overlay de regeneració** (parcial + sencera).
6. **Undo/Redo** (pila de snapshots + atalls de teclat).

### Fase 5 — Connexió al backend

Reemplaçar `llm-stub.js` per crides als endpoints existents de `server.py` (els mateixos que fa servir `ui/workspace.html`). El frontend no s'ha de modificar més enllà del mòdul de client LLM.

### Fase 6 — Verificació

- Contrast WCAG AA de qualsevol combinació nova.
- Focus visible a tots els elements interactius (suggeriment al `README.md`).
- Responsiu: comportament a `<1440px` descrit a `spec-pas3.md` §6.

## Convencions

- **No inventar patrons visuals nous.** Si una cosa no és òbvia del prototip, preguntar a Miquel.
- **No canviar la paleta ni els radis.** Si cal un valor que no és als tokens, proposar afegir-lo a `tokens.css` primer.
- **SVG inline sempre**, amb nomenclatura Lucide als noms de referència.
- **No usar blanc pur** per als fons (excepte on el prototip ho marqui explícitament). Els fons per defecte són `var(--cream)` i les targetes són blanques sobre cream.
- **Mantén les tres famílies tipogràfiques** (Inter / Fraunces / JetBrains Mono). No n'afegeixis.
- **Encoding UTF-8** sempre (coherent amb la convenció del projecte).

## Comunicació amb Miquel

- Sempre en **català**.
- Miquel és expert en pedagogia, **no programador**. Explicacions clares i pràctiques, res de jerga innecessària.
- Per a qualsevol detall visual ambigu, preguntar abans d'improvisar.

## Preguntes freqüents

**Q: Puc fer servir Tailwind o un preprocessador CSS?**
No. CSS pla amb les variables de `tokens.css`. Zero frameworks.

**Q: Puc migrar els SVG a `lucide-react` o similar?**
No. SVG inline, sense llibreries. Els noms Lucide són només referència semàntica.

**Q: Què passa amb els tests?**
No estan dissenyats. Preguntar a Miquel el nivell de cobertura que vol.

**Q: Com gestiono els errors del LLM?**
Preguntar a Miquel. Suggeriment: un toast a la topbar + desbloqueig de l'overlay de regeneració amb un botó "Tornar a provar".

**Q: El Pas 1 del prototip té el rail `#fff` però els Pas 2/3 el tenen `var(--cream-2)`. Què faig?**
Seguir el prototip de cada pas tal com està. Flag a Miquel si la divergència molesta; no la "normalitzis" unilateralment.
