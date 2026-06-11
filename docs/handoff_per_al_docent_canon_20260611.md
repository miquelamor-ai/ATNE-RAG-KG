# HANDOFF a mineriaRAG — canonitzar la taxonomia «Per al docent» · 2026-06-11

## Per què aquest handoff

**Principi (Opció 4, 01/06):** ATNE = CONSUMIDOR del canon, mai ORIGEN. Quan ATNE té
coneixement pedagògic implícit hardcoded, la solució NO és que ATNE generi el JSON canon,
sinó que **mineriaRAG el canonitzi al M\*.md i el generi com a derivat**; ATNE el llegeix.

**El problema concret:** la secció **«Per al docent»** (la justificació pedagògica per al
docent després de cada adaptació) usa una **taxonomia de 9 categories A-I** + un **mapeig
complement→categoria** + unes **lleis** que avui viuen **hardcoded a ATNE** i NO al canon.
Verificat 2026-06-11: cap dels 9 noms de categoria apareix a `corpusFJE`.

**Pitjor: està TRIPLICADA** (3 fonts que poden divergir):
1. `ATNE/adaptation/prompt_builder.py` (`_ARGUMENTACIO_9CAT_BLOCK`, `_COMP_TO_DOCENT_CAT`)
2. `ATNE/ui/atne/pas3.html` (dimMap A-I que renderitza la sortida)
3. `ATNE/ui/saber-ne.html` («Categories d'adaptació» per al docent)

És el mateix patró que la **matriu condició→complement** abans de la canonització R0
(01/06). La solució ha de seguir el cicle R0 validat:
**handoff ATNE → mineriaRAG canonitza al M\*.md + genera derivat JSON → ATNE consumeix +
valida vs snapshot + elimina hardcoded (×3) → corpus = font única.**

---

## 1. El DUMP determinista (què s'ha de canonitzar)

Font màquina-llegible: [`tests/golden/per_al_docent_snapshot.json`](../tests/golden/per_al_docent_snapshot.json)
(regenerable amb `python tests/golden/per_al_docent_snapshot.py --update`).

### 1a. Taxonomia 9 categories A-I
| Codi | Nom | Sub-àrees | Naturalesa (mapa taxonomies, Diagrama 4) |
|---|---|---|---|
| A | Adaptació Lingüística | A1 Lèxic · A2 Sintaxi · A3 Cohesió · A4 Registre | Transformació |
| B | Estructura i Organització | B1 Segmentació · B2 Jerarquia · B3 Ordre · B4 Senyalització | Transformació |
| C | Suport Cognitiu | C1 Càrrega cognitiva · C2 Scaffolding · C3 Coneixements previs · C4 Metacognició | Complement |
| D | Multimodalitat | D1 Suport visual · D2 Organitzadors gràfics · D3 Redundància canals | Complement |
| E | Contingut Curricular | E1 Terminologia · E2 Rigor · E3 Exemples · E4 Contextualització | Transformació |
| F | Avaluació i Comprensió | F1 Preguntes · F2 Activitats · F3 Autoavaluació | Complement |
| G | Personalització Lingüística | G1 Suport L1 · G2 Adaptació cultural | Les dues |
| H | Adaptacions per Perfil | (per condició: TEA, TDAH, dislèxia, DI, TDL, AACC, 2e, disc.aud/vis, discalcúlia, vulnerabilitat, dispraxia) | Les dues |
| I | Meta-regles Transversals | I1 Qualitat · I2 Integració de perfils | Transversal |

> El text descriptiu complet de cada categoria (guia per a la card que genera el LLM) és a
> `_ARGUMENTACIO_9CAT_BLOCK` (≈5,2 KB). Inclou: «què cobreix», format de card, exemples
> correcte/incorrecte, i els matisos validats per NotebookLM (HCL a E; LIT/Cummins a G;
> lectura autònoma A2+ a C).

### 1b. Mapeig complement → categoria/es que la seva presència fa OBLIGATÒRIES
```
glossari → A   (+ G si L1)        bastides → C
pictogrames → D                    preguntes_comprensio → F
illustracions → D                  activitats_aprofundiment → F, E
esquema_visual → C, D              rubriques → F
mapa_conceptual → C                resum_graduat → C
mapa_mental → C                    cartes_conversacionals → F
plantilles_genere → B
```

### 1c. Les LLEIS invisibles del case-block (lògica que NO és a la taula)
- **A, B, E** són SEMPRE obligatòries (són les 3 transformacions del text).
- **H** és obligatòria si hi ha ≥1 perfil/condició actiu (una sub-card per condició real).
- **I** és obligatòria si hi ha ≥2 condicions (combinació de regles).
- **G** és obligatòria si el perfil nouvingut té L1 declarada (glossari bilingüe / TOLC).
- **Mètrica de la categoria A**: frases ≤ N paraules segons MECR
  (`pre-A1:5 · A1:8 · A2:12 · B1:18 · B2:25` — avui a `post_process.MECR_MAX_WORDS`;
  ⚠️ solapa amb els límits per gènere/nivell del `rubrica.json` → unificar al canonitzar).

### 1d. Contracte de comportament (snapshot, deep-equal)
El snapshot congela QUINES categories són obligatòries per a 5 perfils golden (ex: nouvingut
A2 àrab → `A,B,C,D,E,G,H`). És el contracte que ha de seguir verd després del refactor de consum.

---

## 2. Proposta per a mineriaRAG (canon → derivat)

1. **Canonitzar al M\*.md**: candidat natural `M2_instruments-mediacio-pedagogica.md` (ja conté
   la matriu condició→complement) o un nou `M6_argumentacio-per-al-docent.md` (és avaluació/
   metacognició docent). Decidiu vosaltres l'encaix.
2. **Generar derivat** `.tooling/per_al_docent.json` (build determinista, sense IA), amb:
   `categories[]` (codi, nom, sub-àrees, descripció/guia), `complement_to_categoria{}`, `lleis{}`
   (sempre, H/I/G, mètrica_per_mecr). Anàleg a `matriu_cobertura.json`.
3. **Senyalar amb commit hash** quan estigui → ATNE bumpeja submodule, refactoritza el consum,
   valida 5/5 vs snapshot i elimina el hardcoded (×3, incloent un `.data.js` per a pas3.html/
   saber-ne.html si cal consum síncron al browser, amb guard deep-equal com a la matriu).

## 3. Què fa ATNE MENTRESTANT (ja fet en aquest handoff)
- ✅ Dump determinista: `tests/golden/per_al_docent_snapshot.json`.
- ✅ Lleis documentades (§1c) — la part que NO és a cap taula.
- ✅ Golden snapshot + guard anti-regressió: `tests/golden/per_al_docent_snapshot.py`.
- ✅ Test de prompt: `PER_AL_DOCENT_9_categories` + `PER_AL_DOCENT_dedicated_mandatory`.
- ⏳ ATNE NO genera el JSON canon ni puja res a corpusFJE (respecta el principi). Espera senyal.

## 4. Nota de mètode
Mentre la taxonomia visqui a 3 llocs d'ATNE, qualsevol canvi s'ha de fer als 3 alhora
(commit atòmic) fins que el canon sigui la font única. El snapshot detecta drift de
comportament; el guard de pas3/saber-ne (futur `.data.js`) detectaria frescor derivat↔canon.
