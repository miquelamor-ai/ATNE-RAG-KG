# ATNE — Paquet d'entrega a enginyeria

Aquest directori conté els materials necessaris perquè l'equip d'enginyeria implementi ATNE a partir dels prototips de disseny. No és codi de producció: són **tokens**, **primitives CSS** i **especificacions d'interacció** derivats dels prototips HTML d'aquest projecte.

## Què hi ha

| Fitxer | Per a què serveix |
|---|---|
| `tokens.css` | Variables CSS: colors, tipografia, espaiat, radis, ombres. **Font única de veritat** per al look & feel. |
| `base.css` | Reset mínim + tipografia base + algunes primitives reutilitzables (`.btn`, `.chip`, `.doc-read` amb les seves variants). |
| `spec-pas3.md` | Guia d'implementació del Pas 3 (Adaptació), el pas més complex: eines flotants, regeneració parcial, menú de paràmetres, undo/redo. |
| `README.md` | Aquest fitxer. |

## Context: què és ATNE

ATNE és una eina per a docents que permet **adaptar materials educatius** als perfils NEE dels alumnes (TDAH, dislèxia, alumnes amb llengua materna diferent al català, altes capacitats). El flux té 4 passos:

1. **Grup** — el docent selecciona el grup classe (els perfils d'alumne ja estan a la base de dades).
2. **Document** — puja o crea el document original.
3. **Adaptació** — *(el pas complex)* genera versions adaptades; el docent pot editar, regenerar fragments i ajustar paràmetres.
4. **Entrega** — el docent distribueix les versions finals (imprimir, compartir, etc.).

La vista compartida per a Pas 3 i Pas 4 és el **canvas de documents**: un rail esquerre amb perfils/versions, un àrea central amb el document, i eines contextuals.

## Convencions

### Estructura de pantalles
Totes les pantalles principals tenen la mateixa estructura:

```
.wrap  (grid 52px | 1fr, height: 100vh)
 ├── .rail       (barra lateral esquerra, icones verticals)
 └── .canvas     (columna principal)
      ├── .topbar   (títol + stepper + botons)
      └── .main     (àrea de treball, específica de cada pas)
```

### Tipografia
- **UI** (`var(--ui)` = Inter) — botons, menús, text d'interfície.
- **Serif** (`var(--serif)` = Fraunces) — títols de document, títols de pas, logo.
- **Mono** (`var(--mono)` = JetBrains Mono) — metadades, labels, números de pas, xips.

No hi ha "Display" ni altres famílies; mantingueu aquestes tres.

### Paleta
- **Primari** `#3337a6` — accions primàries, estat "seleccionat", insercions (`.ins`).
- **Ink** (escala de gris blavós) — text i divisions.
- **Cream** — fons "paper" de tota l'app. **No useu blanc pur** per al fons; les targetes són blanques sobre cream, i això dóna la sensació editorial.
- **Colors de perfil** (`--tdah`, `--disl`, `--cat`, `--ac`) — identifiquen cada perfil NEE de forma consistent a tot l'app. Es fan servir en xips, vores de targeta i overlays, mai com a color de text llarg.

### Radis i ombres
Escales en `tokens.css`. Les targetes principals usen `--r-xl` (12px) + `--sh-sm`. Els popovers i menús contextuals `--r-lg` (10px) + `--sh-lg`.

### Accessibilitat
- Contrast: tot el text sobre `--cream` compleix WCAG AA. El color primari `#3337a6` sobre blanc també. Verifiqueu qualsevol combinació nova.
- Targets tàctils: mínim 32×32px per a icon-buttons. Els botons principals són més grans.
- Focus visible: no està dissenyat als prototips. **Cal afegir-lo** a la implementació (suggeriment: `outline: 2px solid var(--primary); outline-offset: 2px`).

## Què **no** hi ha en aquest paquet

- **Components React/Vue** — els prototips estan en HTML vanilla. L'equip d'enginyeria pot triar el framework i estructurar components lliurement, sempre que el resultat visual coincideixi amb els prototips.
- **Sistema d'icones** — els prototips usen SVG inline (Lucide style). L'equip pot adoptar Lucide directament (`lucide-react`, `lucide-vue`, etc.) o fer una llibreria pròpia. Els noms a `spec-pas3.md` segueixen la nomenclatura Lucide.
- **Contractes d'API** — fora d'abast d'aquest paquet; veieu els documents de product/backend.
- **Estats d'error** genèrics (404, 500, loading initial) — dissenyats per separat si cal.

## Llista de prototips de referència

Els fitxers HTML a l'arrel del projecte són la **font de veritat visual**. Per a qualsevol dubte d'implementació, obriu el prototip corresponent i inspeccioneu l'HTML.

| Prototip | Rellevant per a |
|---|---|
| `ATNE Pas1 V3.html` | Pas 1 — selecció de grup |
| `ATNE Pas2 V2.html` | Pas 2 — document original |
| `ATNE Pas3 V1.html` | Pas 3 — adaptació individual **amb** eines d'edició ← punt de partida |
| `ATNE Pas3 Grup.html` | Pas 3 — adaptació grupal amb eines d'edició ← punt de partida |

**Per a enginyeria, el punt de partida és `ATNE Pas3 V1.html` i `ATNE Pas3 Grup.html`**, que són les dues vistes del Pas 3 i contenen totes les eines d'edició (selection toolbar, paràmetres, regeneració, undo/redo).

## Suport

Qualsevol dubte sobre intenció de disseny o comportaments ambigus: pregunteu al dissenyador abans d'improvisar. Les micro-interaccions i jerarquies visuals estan pensades amb cura i una desviació petita a cada lloc acumula un resultat final molt diferent.
