# Senyal a mineriaRAG — canonitzar la taxonomia «Per al docent»

> Missatge per al repo/equip mineriaRAG. Context + petició + on són els artefactes.
> Repo origen: `ATNE` (miquelamor-ai/ATNE-RAG-KG), branca `main`.

---

**Hola mineriaRAG,**

Us passem un **handoff** perquè canonitzeu una peça de coneixement pedagògic que ara mateix
viu hardcoded a ATNE i n'hauríeu de ser vosaltres la font (corpus = font única). Seguim el
**cicle R0** que ja vam validar amb la matriu condició→complement.

## Context

ATNE, després de cada adaptació de text, genera una secció **«Per al docent»** que justifica
les decisions pedagògiques classificades en una **taxonomia de 9 categories A-I**
(A. Adaptació Lingüística … I. Meta-regles Transversals). Aquesta setmana l'hem reconstruïda
end-to-end (crida dedicada, validada per NotebookLM com a «apte per a producció»: cita
Cummins/Solé/Vygotsky, mètriques de control de llengua, HCL nuclear, enfocament en
l'autoregulació).

**El problema arquitectònic:** aquesta taxonomia + el **mapeig complement→categoria** + les
**lleis** de quines categories són obligatòries per cada cas viuen **hardcoded a ATNE i
TRIPLICATS** (`prompt_builder.py` + `pas3.html` + `saber-ne.html`). Hem verificat que **cap
dels 9 noms apareix al `corpusFJE`** → ATNE n'és, de facto, l'ORIGEN. Això trenca el principi
«ATNE = consumidor, mai origen» i és exactament el patró que la matriu tenia abans de la R0.

## Què us demanem (cicle R0)

1. **Canonitzar al M\*.md**: candidat natural `M2_instruments-mediacio-pedagogica.md` (ja conté
   la matriu) o un nou `M6_argumentacio-per-al-docent.md` (és metacognició/avaluació docent).
   Decidiu vosaltres l'encaix conceptual.
2. **Generar el derivat** `.tooling/per_al_docent.json` (build determinista, sense IA),
   anàleg a `matriu_cobertura.json`, amb: `categories[]` (codi, nom, sub-àrees, descripció/guia),
   `complement_to_categoria{}`, i `lleis{}` (sempre A/B/E · H si perfil · I si multi-condició ·
   G si L1 · mètrica_paraules_per_mecr).
3. **Senyalar-nos amb el commit hash** quan estigui. Llavors ATNE bumpeja el submodule,
   refactoritza per consumir el derivat, valida 5/5 contra el snapshot, i **elimina la
   triplicació** (els 3 llocs passen a llegir una sola font; per al browser, via `.data.js`
   amb guard deep-equal com a la matriu).

## On són els artefactes (al repo ATNE, branca main)

- **Handoff complet** (lleis invisibles + proposta de canon + schema del derivat + pla de
  consum): `docs/handoff_per_al_docent_canon_20260611.md`
- **Dump determinista** (màquina-llegible: taxonomia + mapeig + lleis + contracte per 5
  perfils golden): `tests/golden/per_al_docent_snapshot.json`
- **Guard anti-regressió**: `tests/golden/per_al_docent_snapshot.py`

> Commit d'entrega ATNE: **{{COMMIT_HASH}}**

## Detall que us estalvia feina (les lleis NO són a cap taula)

- **A, B, E** són SEMPRE obligatòries (les 3 transformacions del text).
- **H** obligatòria si ≥1 perfil/condició actiu; **I** si ≥2 condicions; **G** si nouvingut amb L1.
- **Mapeig**: glossari→A (+G si L1) · pictogrames/illustracions→D · esquema→C,D ·
  mapes→C · bastides→C · preguntes/rúbriques/cartes→F · activitats→F,E · plantilles→B.
- **Mètrica categoria A** (frases ≤ N paraules): pre-A1:5 · A1:8 · A2:12 · B1:18 · B2:25.
  ⚠️ Avui a `post_process.MECR_MAX_WORDS` d'ATNE i SOLAPA amb els límits per gènere/nivell del
  `rubrica.json`. En canonitzar, unifiqueu-ho (una sola font per a la llargada de frase).

ATNE NO genera cap JSON canon ni puja res al corpus: esperem el vostre senyal. Gràcies!
