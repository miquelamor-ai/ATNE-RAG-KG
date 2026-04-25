---
version: alpha
name: ATNE
description: >
  Adaptador de Textos a Necessitats Educatives — Jesuïtes Educació (FJE).
  Eina pedagògica per adaptar materials curriculars a la diversitat de l'aula:
  nouvinguts, NESE, DUA, altes capacitats. L'estètica és editorial i càlida,
  com paper de qualitat, no una interfície d'aplicació freda.

colors:
  # Marca
  primary:        "#3337a6"
  primary-hover:  "#3f45c4"
  primary-light:  "#e1e4ff"
  primary-subtle: "#eef0ff"

  # Fons editorial "paper" — el tret d'identitat de l'app
  cream:   "#f4f1e8"
  cream-2: "#ece8db"
  cream-3: "#e6e2d3"

  # Escala de text (ink)
  ink-900: "#121a2b"
  ink-800: "#1b2440"
  ink-700: "#2d3655"
  ink-600: "#464f6d"
  ink-500: "#6a7392"
  ink-400: "#8a93b0"
  ink-300: "#b5bdd4"
  ink-200: "#d7dce9"
  ink-150: "#e4e8f2"
  ink-100: "#eef1f8"
  ink-75:  "#f4f6fb"
  ink-50:  "#f9fafd"

  # Estats semàntics
  ok:         "#188a5a"
  ok-bg:      "#e6f5ee"
  warn:       "#a16207"
  warn-bg:    "#fcf4dc"
  danger:     "#b43d3d"
  danger-bg:  "#fce9e9"

  # Colors de condició educativa (NEE) — NO intercanviables, veure secció Colors
  tdah:        "#c64a4a"
  tdah-bg:     "#fce7d5"
  dyslexia:    "#b77400"
  dyslexia-bg: "#fbe9c2"
  language:    "#0f7a7a"
  language-bg: "#d3ece9"
  gifted:      "#6d3aa3"
  gifted-bg:   "#e7dcf4"

typography:
  display:
    fontFamily: "Fraunces"
    fontWeight: 700
    fontSize: "40px"
    lineHeight: 1.1
    letterSpacing: "-0.02em"
  heading:
    fontFamily: "Fraunces"
    fontWeight: 700
    fontSize: "28px"
    lineHeight: 1.2
    letterSpacing: "-0.01em"
  subheading:
    fontFamily: "Fraunces"
    fontWeight: 700
    fontSize: "22px"
    lineHeight: 1.3
  document:
    fontFamily: "Fraunces"
    fontSize: "18px"
    fontWeight: 400
    lineHeight: 1.75
  body:
    fontFamily: "Inter"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.5
  ui-sm:
    fontFamily: "Inter"
    fontSize: "13px"
    fontWeight: 400
    lineHeight: 1.4
  label:
    fontFamily: "JetBrains Mono"
    fontSize: "11px"
    fontWeight: 500
    letterSpacing: "0.12em"
  caption:
    fontFamily: "JetBrains Mono"
    fontSize: "11px"
    fontWeight: 400
    letterSpacing: "0.08em"

rounded:
  xs:   "4px"
  sm:   "6px"
  md:   "8px"
  lg:   "10px"
  xl:   "12px"
  2xl:  "16px"
  pill: "9999px"

spacing:
  1: "4px"
  2: "8px"
  3: "12px"
  4: "16px"
  5: "20px"
  6: "24px"
  7: "32px"
  8: "40px"
  9: "48px"

components:
  topbar:
    backgroundColor: "{colors.cream}"
    height: "52px"
    padding: "10px 20px"
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "#ffffff"
    rounded: "{rounded.md}"
    padding: "12px 20px"
    typography: "{typography.body}"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.ink-700}"
    rounded: "{rounded.md}"
    padding: "8px 12px"
  avatar:
    size: "32px"
    rounded: "50%"
    typography: "{typography.label}"
  chip:
    backgroundColor: "{colors.ink-75}"
    textColor: "{colors.ink-700}"
    rounded: "{rounded.pill}"
    padding: "5px 12px"
    typography: "{typography.ui-sm}"
  chip-active:
    backgroundColor: "{colors.primary}"
    textColor: "#ffffff"
    rounded: "{rounded.pill}"
  card:
    backgroundColor: "#ffffff"
    rounded: "{rounded.xl}"
    padding: "20px 24px"
  step-toggle:
    backgroundColor: "{colors.ink-75}"
    rounded: "{rounded.pill}"
    padding: "3px"
  step-active:
    backgroundColor: "{colors.ink-900}"
    textColor: "#ffffff"
    rounded: "{rounded.pill}"
---

# ATNE — Sistema de Disseny

## Implementation

**Stack**: HTML + CSS + JavaScript vanilla. Cap framework (no React, no Vue, no Tailwind, no TypeScript).

Els tokens del frontmatter YAML es corresponen directament a **CSS custom properties** definides a `tokens.css`:

```css
/* tokens.css */
:root {
  --primary: #3337a6;
  --r-xl: 12px;
  --fs-base: 14px;
}
```

Quan generis components o pantalles per a ATNE:
- Usa `var(--primary)` en lloc de `#3337a6` o `text-blue-700`
- Usa `var(--r-xl)` en lloc de `border-radius: 12px` o `rounded-xl`
- Usa `var(--fs-base)` en lloc de `font-size: 14px` o `text-sm`
- Genera HTML semàntic amb classes CSS kebab-case (`.btn-primary`, `.mode-card`, `.topbar`)
- El CSS va en un bloc `<style>` dins del fitxer HTML o en un fitxer `.css` extern
- El JS va en un bloc `<script>` o fitxer `.js` extern, sense bundlers ni build tools

## Overview

ATNE és una eina pedagògica per a docents de Jesuïtes Educació (FJE). L'estètica és deliberadament **editorial i càlida**: el fons cream (`#f4f1e8`) evoca paper de qualitat i redueix la fatiga visual durant sessions llargues de treball. No és una app tecnològica freda — és un espai de treball per a professionals de l'educació.

La personalitat visual combina:
- **Seriosa i professional** (tipografia Fraunces, gamma de blaus foscos)
- **Accessible i acollidora** (fons cream, molt d'espai en blanc, ombres subtils)
- **Pedagògicament conscient** (el sistema de colors NEE té significat educatiu real)

El públic és **docents**, no estudiants ni programadors. Les decisions de disseny prioritzen claredat, llegibilitat i confiança institucional per sobre de modernitat o impacte visual.

## Colors

### Fons editorial

El tret d'identitat d'ATNE és el fons **cream** (`#f4f1e8`). **No substituïr per blanc** — el contrast pur blanc/negre és més fatigós i trenca el to editorial. Les tres variants de cream defineixen la jerarquia de superfícies:

- `cream` — fons principal de tota l'app
- `cream-2` — rail lateral, formularis, superfícies de segon pla
- `cream-3` — hover sobre cream-2

### Escala ink

L'escala ink (900→50) substitueix els gris genèrics. Tots els textos, icones i línies divisòries usen ink. **Mai usar negre pur (`#000`) ni gris genèric.**

- `ink-900` — text principal, overlays foscos
- `ink-800` — títols
- `ink-500` — captions, metadades
- `ink-300` — icones desactivades, placeholders

### Colors de condició educativa (NEE)

Aquests quatre colors identifiquen condicions d'aprenentatge específiques. Tenen significat pedagògic precís i **no s'han d'intercanviar ni usar decorativament**:

| Token | Color | Condició |
|---|---|---|
| `tdah` / `tdah-bg` | Vermell-taronja | TDAH, dèficit d'atenció |
| `dyslexia` / `dyslexia-bg` | Ambre/ocre | Dislèxia, dificultats lectores |
| `language` / `language-bg` | Verd fosc | Nouvinguts, aprenents de català |
| `gifted` / `gifted-bg` | Porpra | Altes capacitats (AC) |

Cada condició usa el color fosc per a text/borde i el clar (`-bg`) per a fons. L'avatar de cada perfil d'alumne usa la combinació de la seva condició principal.

### Color primari

El blau `#3337a6` és el color d'acció: botons principals, elements actius, links. És fosc i institucional, adequat per a context educatiu.

## Typography

ATNE usa **tres famílies** amb rols diferenciats:

### Fraunces (serif) — Identitat i contingut
La font editorial de l'app. S'usa per a:
- Títols i headings de totes les pàgines
- El nom "ATNE" al topbar
- Textos adaptats (la sortida del LLM que llegirà el docent)
- Noms de perfils d'alumnes

**Fraunces dona caràcter editorial i distingeix ATNE d'eines tecnològiques genèriques.**

### Inter (sans-serif) — Interfície
La font funcional. S'usa per a:
- Tot el text de formularis, etiquetes, botons, descripcions
- Body text de la interfície
- Textos secundaris i captions llargues

### JetBrains Mono (monospace) — Metadades
S'usa exclusivament per a:
- Labels de formulari (uppercase, letter-spacing ample)
- Indicadors de nivell MECR, codi de versió, timestamps
- Qualsevol informació de sistema que no sigui text llegible

### Fonts d'accessibilitat (opt-in)
A les pàgines Flash i Pas3, el docent pot canviar la font del text adaptat:
- **Atkinson Hyperlegible** — baixa visió
- **Lexend** — dificultats de lectura
- **OpenDyslexic** — dislèxia

Aquestes fonts **mai s'usen per a la interfície** — són eines d'accessibilitat per al contingut generat.

## Layout

### Patró principal (Taller: Pas1, Pas2, Pas3)
```
[Rail 52px] [Canvas principal]
```
- Rail esquerre: 52px, icones de navegació, fons cream-2
- Canvas: columna flex, topbar fixe + zona de contingut scrollable

Algunes pàgines afegeixen un segon panel lateral per al perfil de l'alumne (240px).

### Patró centrat (Home)
Columna centrada, max-width 680px, padding generós. No hi ha rail.

### Patró editorial (Saber-ne+)
Topbar fixe + sidebar de navegació de document (256px, oculta en mòbil) + contingut ample.

### Topbar
Consistent a totes les pàgines:
```
[Logo FJE + "ATNE"] — [Toggle Flash/Taller] — [Avatar docent]
```
El toggle Flash/Taller usa l'estil `.steps` (pill amb fons ink-75, opció activa ink-900 sobre blanc).

## Elevation & Depth

Les ombres són deliberadament subtils — l'app no competeix per atenció visual.

| Nivell | Ús |
|---|---|
| `sh-xs` | Cards bàsiques sobre cream |
| `sh-sm` | Cards en hover, panells laterals |
| `sh-md` | Botons flotants (FABs) |
| `sh-lg` | Menús desplegables, popovers |
| `sh-xl` | Modals, drawer mòbil |

**Regla**: mai usar ombres de colors (primari, etc.) excepte al hover del botó primari.

## Shapes

El sistema de radis és consistent i progressiu:
- `xs` (4px) — badges de text molt petits, indicadors de color
- `sm` (6px) — inputs, botons compactes
- `md` (8px) — botons principals, icon-buttons, inputs estàndard
- `lg` (10px) — contenidors de llista
- `xl` (12px) — cards estàndard, panells laterals
- `2xl` (16px) — cards grans (home), mode-cards
- `pill` — chips, step toggles, badges de nivell

**Regla**: com més gran és el component, més gran el radi. Les cards principals de la home usen 2xl; els chips de nivell usen pill.

## Components

### Topbar
Fons cream amb transparència i blur quan és fixe. Alçada 52px. Sempre conté: logo + brand text (Fraunces 700, 18px) a l'esquerra, step toggle al centre, avatar docent a la dreta.

### Step Toggle (Flash / Taller)
Pill amb fons ink-75, border paper-line. Cada opció té padding 6px 14px (mono, xs, med). Opció activa: fons ink-900, text blanc. Opció completada: text primary amb prefix "✓".

### Avatar docent
Cercle 32px. Color de fons i text determinat per la condició principal del docent/alumne. Usa la família Fraunces 700, 13.5px. Sempre té border d'1px del color de la condició.

### Cards de mode (Home)
Fons blanc, radius 2xl, padding 28px 24px, ombra sh-xs. Hover: border primary, ombra blava subtil, translateY(-2px).

### Chips de complement
Pill, fons ink-75/blanc, border paper-line. Actiu: fons primary, text blanc. S'usen per seleccionar complements pedagògics (bastides, preguntes, mapa conceptual...).

### Floating Action Bar (Flash, Pas3)
Barra fixe bottom-right, fons ink-900, radius pill. Botons interns amb text rgba(255,255,255,.75), hover fons rgba(255,255,255,.12).

## Do's and Don'ts

### Colors
- ✅ Usar cream com a fons base, mai blanc pur
- ✅ Usar els colors NEE únicament per als seus perfils corresponents
- ✅ Usar ink-500 per a text secundari i metadades
- ❌ Intercanviar els colors de condicions NEE (tdah, dyslexia, language, gifted)
- ❌ Usar negre pur (#000) per a text
- ❌ Usar el color primary de fons en zones grans

### Tipografia
- ✅ Fraunces per a títols i text adaptat (sortida del LLM)
- ✅ JetBrains Mono per a labels en uppercase amb letter-spacing
- ✅ Inter per a tot el text d'interfície
- ❌ Usar Atkinson/Lexend/OpenDyslexic per a la interfície (són eines d'accessibilitat de contingut)
- ❌ Mesclar Fraunces i Inter en el mateix nivell jeràrquic

### Layout
- ✅ Mantenir el topbar consistent: logo + toggle + avatar
- ✅ Usar el patró rail (52px) per a les pàgines de flux de treball (Pas1-3)
- ❌ Afegir navegació secundària al topbar (ja és al rail o sidebar)
- ❌ Usar fons blancs per a pàgines senceres (sempre cream)

### Components
- ✅ Chips en pill per a seleccions múltiples (complements, nivells)
- ✅ Cards amb radius xl/2xl per a contingut principal
- ❌ Usar botons primaris (primary) per a accions destructives o secundàries
- ❌ Crear ombres de colors (reservades per a hover del botó principal)
