# ADR-004 — Suport de fórmules matemàtiques i químiques (juny 2026)

- **Estat:** Esborrany · pendent aprovació Miquel Amor
- **Data:** 2026-06-25
- **Decisió de:** Miquel Amor · recomanació arquitectònica Claude Code
- **Context relacionat:** `adaptation/post_process.py` · `ui/atne/js/fonts.js` · `ui/fonts/fonts.css` ·
  `docs/handoff_mineriarag_stem_curriculum_20260615.md` · skills STEAM (`write-poster-cientific`,
  `write-diari-camp`, `write-practica-laboratori`) · corpusFJE invariant disciplinari

---

## Context i problema

ATNE s'usa a matèries STEAM (Ciències, Tecnologia, Matemàtiques, Física, Química, Biologia)
a totes les etapes. Els textos d'aquestes matèries contenen **fórmules matemàtiques i químiques**
que han de sobreviure intactes el pipeline d'adaptació (invariant disciplinari) i ser llegibles
per l'alumne al text adaptat.

**Tres punts d'entrada on apareixen fórmules:**

| Punt | Situació actual | Problema |
|---|---|---|
| **A — Entrada (text font)** | El docent enganxa text amb fórmules (LaTeX, Unicode, text pla) | `post_process.py` _elimina_ artefactes LaTeX → destrueix fórmules vàlides |
| **B — Sortida (text adaptat)** | ATNE genera text amb fórmules | Símbols simples (H₂O, F=m·a) funcionen via Noto Sans Math; equacions complexes (fraccions, integrals, matrius) no es renderitzen |
| **C — Generador (Pas 2)** | El docent escriu o insereix fórmules al panell Generar | No hi ha cap mecanisme d'entrada de fórmules: camp de text pla sense suport matemàtic |

**Abast per etapa:**
- Primària / ESO baix (Ciències Naturals, Tecnologia): símbols simples suficients (H₂O, x², ∑).
- ESO alt / Batxillerat (Física, Química, Matemàtiques): equacions complexes imprescindibles
  (fraccions, arrels compostes, integrals, derivades, matrius).

**Estat actual de la infraestructura:**
- ✅ **Noto Sans Math** — font Unicode matemàtica carregada (cobreix ∑ ∫ √ π ≤ ≥ ≠ ∞ Δ ∇, alfabet grec, lletres dobles matemàtiques). Suficient per a símbol simple.
- ✅ **`post_process.py` / `_strip_latex_artifacts()`** — elimina marques LaTeX injectades pel LLM. Lògica correcta per a artefactes, però **no distingeix artefacte de fórmula vàlida**.
- ❌ **Cap renderitzador d'equacions** (ni KaTeX, ni MathJax) al frontend.
- ❌ **Cap editor de fórmules** al panell Generar.

---

## Decisions

### D1 — Format intern de les fórmules: LaTeX delimitat

**Decisió:** Les fórmules viuen en format **LaTeX delimitat** dins el flux d'ATNE:
- Inline: `$...$` (ex: `$F = m \cdot a$`, `$\mathrm{H_2O}$`)
- Display (bloc): `$$...$$` (ex: equació en línia pròpia)

**Raonament:**
- LaTeX és l'estàndard acadèmic universal i el que genera el LLM de manera natural.
- KaTeX (D2) consumeix LaTeX directament → no cal cap conversió intermèdia.
- Delimitar amb `$...$` permet distingir fórmules vàlides d'artefactes LaTeX en prosa
  (ex: `$\rightarrow$` sense context matemàtic → artefacte; `$F=ma$` → fórmula vàlida).
- Alternativa descartada: MathML — verbós, no el genera cap LLM de manera fiable.
- Alternativa descartada: Unicode pla — suficient per a símbols simples però no escalable
  a equacions complexes de Batxillerat.

### D2 — Renderitzador frontend: KaTeX

**Decisió:** Afegir **KaTeX** (https://katex.org) com a renderitzador d'equacions al frontend.

**Raonament:**
- KaTeX renderitza LaTeX a HTML+CSS sense dependre de JavaScript asíncron (a diferència de MathJax v3).
- Lleuger (~300 KB minificat+gzip vs ~1 MB de MathJax).
- Renderitza síncronament → compatible amb el flux SSE d'ATNE (streaming token a token).
- Pot operar en mode auto-render: detecta `$...$` i `$$...$$` al DOM i els renderitza automàticament.
- Subconjunt LaTeX ampli: cobreix tot el currículum STEAM de secundària i batxillerat.
- Llicència MIT, sense dependències de servidor.

**Integració prevista:**
```html
<!-- CDN (o bundle local) -->
<link rel="stylesheet" href="katex.min.css">
<script defer src="katex.min.js"></script>
<script defer src="contrib/auto-render.min.js"
  onload="renderMathInElement(document.body, {delimiters: [
    {left: '$$', right: '$$', display: true},
    {left: '$', right: '$', display: false}
  ]})"></script>
```

### D3 — `post_process.py`: preservar fórmules, eliminar artefactes

**Decisió:** Modificar `_strip_latex_artifacts()` per distingir:
- **Fórmula vàlida** (`$...$` o `$$...$$` amb contingut matemàtic): **PRESERVAR intacta**.
- **Artefacte LaTeX en prosa** (marques LaTeX fora de delimitadors, o delimitadors buits/malformats): **ELIMINAR** com ara.

**Regla operativa:**
```
Si el token és de la forma $<expr>$ o $$<expr>$$
  i <expr> conté caràcters matemàtics (lletres, números, operadors, comandes LaTeX),
  → preservar el token sencer (el KaTeX el renderitzarà al frontend).
Altrament (artefacte: \rightarrow$ sense $, \text{} sense delimitador, etc.):
  → aplicar la lògica actual d'eliminació.
```

**Implicació:** el LLM ha de generar fórmules sempre dins `$...$`. El prompt del sistema
(skills STEAM) ha d'explicitar aquesta convenció.

### D4 — Editor docent al panell Generar: input LaTeX amb preview

**Decisió:** Afegir al panell Generar un **camp de text amb preview LaTeX en viu** per a fórmules,
en lloc d'un editor visual d'equacions complet.

**Raonament:**
- Un editor visual d'equacions (tipus MathType o GeoGebra) és costós de mantenir i innecessari
  si el docent coneix LaTeX mínim o pot copiar-enganxar des d'un editor extern.
- La majoria de docents STEAM de secundària coneixen la notació LaTeX bàsica o la poden obtenir
  fàcilment (copiant des de Wolfram Alpha, Wikipedia, etc.).
- Un camp de text + preview en viu (KaTeX renderitza en temps real) dona feedback immediat sense
  complexitat d'implementació.
- Alternativa per a docents sense LaTeX: botó d'inserció de fórmules freqüents (plantilles
  de les fórmules més comunes del currículum: equació de moviment, llei de Coulomb, etc.).
  Diferit a Fase 2 d'aquesta feature.

**Format d'entrada:** el docent escriu LaTeX dins `$...$` al camp de text. Preview renderitzada
per KaTeX en temps real a sota del camp.

### D5 — Prompt del sistema (skills STEAM): convenció de fórmules

**Decisió:** Afegir a cada skill STEAM (`write-poster-cientific`, `write-diari-camp`,
`write-practica-laboratori`) i a la **meta-regla transversal d'invariant notació** la convenció:

> "Totes les fórmules matemàtiques i químiques s'escriuen en format LaTeX delimitat: `$...$`
> per a inline i `$$...$$` per a display. Els símbols i fórmules de l'invariant disciplinari
> es preserven exactament en aquest format. No verbalitzis mai una fórmula en prosa."

**Implicació per al corpus:** les skills STEAM del corpusFJE han d'incloure exemples de
format correcte a la secció `## Format de sortida`.

---

## Impacte i feina prevista

| Component | Canvi | Complexitat |
|---|---|---|
| `ui/atne/index.html` (o equivalent) | Afegir KaTeX CDN + auto-render | Baixa |
| `adaptation/post_process.py` | Modificar `_strip_latex_artifacts()` per preservar `$...$` | Baixa-Mitjana |
| `ui/atne/js/` (panell Generar) | Camp LaTeX + preview KaTeX | Mitjana |
| Skills STEAM corpusFJE | Afegir convenció `$...$` a `## Format de sortida` | Baixa |
| Prompt del sistema (`instruction_catalog.py` o `skills_loader.py`) | Meta-regla transversal d'invariant notació | Baixa |
| Tests (`tests/test_strip_latex_quick.py`) | Ampliar casos per a fórmules preservades | Baixa |

**Ordre d'implementació recomanat:**
1. KaTeX al frontend (D2) — visible i verificable immediatament.
2. `post_process.py` (D3) — evita que el pipeline destrueixi fórmules.
3. Tests (validar D3).
4. Skills STEAM + meta-regla (D5) — el LLM comença a generar `$...$`.
5. Editor docent (D4) — últim, depèn que tot l'anterior funcioni.

---

## Alternatives descartades

- **MathJax**: més complet que KaTeX però 3× més pesat i renderització asíncrona
  incompatible amb SSE. Descartada.
- **Unicode pla per a tot**: suficient per a Primària/ESO baix però no escalable.
  Descartada per a Batxillerat.
- **Editor visual d'equacions integrat**: massa complex per a la Fase 1. Diferit.
- **Imatges de fórmules (SVG/PNG generades)**: no accessibles (lectora de pantalla),
  no editables, no exportables. Descartada.

---

## Risc residual

- **LLM inconsistent amb `$...$`**: el LLM pot generar fórmules sense delimitadors o amb
  delimitadors dobles incorrectes. Mitigació: instrucció explícita al prompt + tests de regressió.
- **KaTeX no cobreix tot LaTeX**: KaTeX no suporta `\begin{align}` complet ni alguns paquets
  avançats. Per al currículum de Batxillerat, el subconjunt suportat és suficient; per a
  universitat (fora d'abast), no.
- **Docents sense LaTeX**: el camp de text + preview pot ser intimidant. Mitigació:
  plantilles de fórmules freqüents (Fase 2).
