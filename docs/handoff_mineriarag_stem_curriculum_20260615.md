# Handoff a mineriaRAG — Invariant disciplinari (STEM) + Activació curricular

> **Data:** 2026-06-15
> **De:** ATNE (Miquel Amor + Claude)
> **A:** mineriaRAG (canonitzador)
> **Tipus:** Encàrrec de canonització cross-team
> **Regla aplicada:** ATNE = CONSUMIDOR, mai ORIGEN del canon
> ([[feedback_atne_consumidor_no_origen_canon]]). El coneixement nou
> neix al canon (corpusFJE); ATNE el llegeix.

---

## 0. Resum executiu (TL;DR per a mineriaRAG)

Dues millores de l'ATNE necessiten coneixement que **avui no és al canon**.
Aquest document especifica QUÈ s'ha de canonitzar perquè ATNE ho consumeixi.
**No demanem cap canvi de plataforma a ATNE en aquest document** — només font.

| # | Millora | Què demanem canonitzar | Estat del canon avui |
|---|---------|------------------------|----------------------|
| **1** | Adaptació de contingut STEM (mates/ciències/procediments) | Una secció nova **«Invariant disciplinari»** dins cada SKILL de gènere STEM | ❌ No existeix. Només `M1_discalculia.md` (perfil de l'alumne, no didàctica de la matèria) |
| **2a** | Currículum — consum bàsic (FASE 1) | **Res nou de contingut.** El JSON LOMLOE ja existeix i és complet. Demanem només **confirmació de contracte de lectura** (estabilitat de claus + manifest) | ✅ Existeix (`curriculum/<etapa>/<materia>/...json`) |
| **2b** | Currículum — pont pedagògic (FASE 2, diferit) | M*.md de **mediació curricular**: doctrina «saber/competència → instruccions per al text» | ❌ No existeix. Diferit fins validar el consum bàsic |

**Decisió d'enquadrament clau (panell d'experts — lingüística del discurs,
didàctica de mates, didàctica de ciències, DUA):** l'adaptació STEM **NO és un
subsistema nou ni un gènere nou**. L'enquadrament de gèneres discursius vigent
és correcte. El que falta és una **secció dins de cada SKILL de gènere STEM**,
amb el mateix estatus canònic que la «terminologia inviolable» que ja existeix.

---

## 1. Context: per què ara

### 1.1. El buit de mates no és arquitectònic, és de contingut

ATNE tracta tot el text com a prosa narrativa/expositiva. Quan el contingut és
matemàtic o científic, l'LLM pot «simplificar» destruint el que **és** el
contingut (no la forma): treure una condició d'un enunciat de física el fa fals,
saltar un pas d'un procediment el fa inservible, arrodonir les dades d'un
problema en canvia la lògica.

Avui l'únic tractament relacionat són instruccions de **perfil** (no de matèria):
- `H-27` / `H-28` (discalcúlia): nombres abstractes → analogies; desglossar
  procediments pas a pas.
- `A-22` (quantificadors concrets) — **suprimida** si discalcúlia activa.

Cap d'aquestes diu **què és intocable en una matèria STEM**. Aquesta és la peça
que falta.

### 1.2. El principi que ho fonamenta: eixos independents (lligam amb el 2e)

L'ADR-001 (doble excepcionalitat, bug B1) va establir que **simplicitat
lingüística** i **exigència cognitiva** són **eixos independents** — l'error era
col·lapsar-los (un AACC+dislèxia rebia text alhora cognitivament pobre).

L'invariant disciplinari és **el mateix principi en un altre pla**:

> **Eix lingüístic (ADAPTABLE) ⊥ Eix disciplinari (INVARIANT).**
> Es pot simplificar el llenguatge i el context **sense** tocar l'estructura
> matemàtica, les magnituds/condicions, ni l'ordre dels passos.

No és una analogia decorativa: és literalment la mateixa regla de no-col·lapse
d'eixos, aplicada a la dimensió del contingut disciplinari. Això dona fonament
teòric a la secció, no només utilitat pràctica. **Demanem que el canon ho
expliciti com a principi**, no només com a llista de regles.

---

## 2. MILLORA 1 — Secció «Invariant disciplinari» a les SKILLs STEM

### 2.1. Què demanem canonitzar

Una secció nova, **«## Invariant disciplinari»**, dins el cos de les SKILLs de
gènere que poden vehicular contingut STEM. Aquesta secció declara, per cada
gènere, **el parell ADAPTABLE / INVARIANT** del contingut.

### 2.2. Granularitat acordada (decisió de Miquel, 2026-06-15)

**Per gènere, amb sub-blocs per disciplina.** Un mateix gènere (p.ex.
`write-divulgatiu`) pot vehicular mates O ciències amb invariants diferents.
Per tant la secció es subdivideix:

```
## Invariant disciplinari
### Matemàtiques
   (taula ADAPTABLE | INVARIANT)
### Ciències experimentals (física, química, biologia, geologia)
   (taula ADAPTABLE | INVARIANT)
### Procedimental (algorismes, protocols pas a pas)
   (taula ADAPTABLE | INVARIANT)
```

ATNE activarà el sub-bloc segons la **matèria** del Pas 2 (camp `materia` /
`codi_area` del currículum — veure §3). Si la matèria no és STEM, la secció
sencera queda inactiva (no s'injecta).

> **Nota per a mineriaRAG:** ATNE només especifica QUÈ ha de poder consumir.
> Si en canonitzar trobeu que una estructura de **creuament gènere × matèria**
> (a l'estil dels `get_crossing_blocks` de perfils) és més neta que sub-blocs
> dins la SKILL, és decisió vostra — el contracte de consum d'ATNE és el mateix
> mentre el resultat sigui injectable per gènere+matèria+MECR. Recomanació
> d'ATNE: sub-blocs dins la SKILL (menys entrades a mantenir, una font per
> gènere).

### 2.3. Format obligatori: taula de dues columnes

L'invariant **no pot ser una declaració abstracta** («l'estructura matemàtica és
intocable»): això no és accionable per un LLM en streaming ni verificable per un
test/jutge. Cal el **parell explícit**:

| ADAPTABLE (eix lingüístic) | INVARIANT (eix disciplinari) |
|----------------------------|------------------------------|
| Vocabulari, registre, longitud de frase, context narratiu de l'enunciat, exemples il·lustratius | L'estructura del problema: dades, relacions entre dades, incògnita, nombre de passos lògics |

Raó del format de dues columnes:
1. És **injectable** al prompt tal qual.
2. És **comprovable**: un test/jutge pot auditar si una adaptació ha tocat la
   columna INVARIANT (regressió disciplinària) — i també l'error oposat: que
   l'LLM **no simplifiqui res** «per si de cas» (la columna ADAPTABLE explícita
   l'autoritza a simplificar el que toca).

### 2.4. ⚠️ L'invariant GRADUA per MECR (no és una constant fixa)

Aquest és el matís més important i el que evita un xoc amb DUA-Accés.

«Nombre de passos intocable» és cert a **Core/Enriquiment**. Però a
**Accés / pre-A1 / A1**, un problema de 4 passos sovint s'ha de **descompondre**
en sub-problemes encadenats — *sense saltar lògica, però re-segmentant*. Igual
que la terminologia inviolable ja gradua (a A1 el terme hi és, però amb glossari).

Per tant:
- **El QUÈ es preserva** (la columna INVARIANT) és estable.
- **El COM es preserva** gradua per MECR.

La secció ha d'usar **la mateixa estructura `mecr_detail` gradada** que ja tenen
les instruccions del catàleg i la modulació per nivell que ja tenen les SKILLs
(veure `write-instructiu/SKILL.md`, blocs pre-A1 → C1+). Exemple del que volem
evitar: una taula plana que digui «4 passos intocables» i que a Accés
contradigui la pauta DUA de descomposició.

Esbós de gradació (a refinar pel panell):

| MECR | Tractament de l'invariant «nombre de passos» |
|------|----------------------------------------------|
| pre-A1 / A1 | Es **descompon** en sub-passos atòmics encadenats. Cap pas lògic desapareix; se'n fan més de més petits. |
| A2 / B1 | Es manté el nombre de passos; s'explica millor cada pas. |
| B2 / C1+ | Estructura íntegra; es pot afegir justificació del raonament. |

### 2.5. Els tres patrons d'invariant (del panell)

A canonitzar amb rigor didàctic. Esbós de partida:

**a) Enunciat de problema (matemàtiques)**
- INVARIANT: estructura matemàtica — dades, relacions, incògnita, nombre de
  passos lògics.
- ADAPTABLE: el llenguatge i el context narratiu de l'enunciat.

**b) Text de ciències experimentals**
- INVARIANT: magnituds, condicions i relacions causals. *Treure «a pressió
  atmosfèrica» fa la frase falsa.*
- ADAPTABLE: el vocabulari, no la precisió condicional.

**c) Procediment / algorisme**
- INVARIANT: ordre i completesa dels passos. No se'n salta cap.
- ADAPTABLE: l'explicació de cada pas (es pot enriquir, no ometre).

### 2.6. On enganxa amb el que JA existeix al canon

Les SKILLs de gènere ja tenen, als «Criteris transversals», la línia
**«Fidelitat al text font»** (veure `write-instructiu/SKILL.md` L.74, 100, 126…).
Això és **fidelitat de forma**. L'invariant disciplinari n'és el **complement de
contingut**: el mateix estatus canònic, estès de «lèxic/forma intocable» a
«estructura disciplinària intocable». Recomanem situar la secció a prop o com a
ampliació d'aquest criteri, no com a apèndix desconnectat.

### 2.7. Quins gèneres reben la secció (a confirmar pel panell)

Candidats segons les 24 SKILLs de `skills/generes/`:
- `write-instructiu`, `write-manual` → sub-bloc **Procedimental** (clar).
- `write-divulgatiu`, `write-enciclopedic`, `write-informe` → sub-blocs
  **Matemàtiques** i **Ciències** (segons matèria).
- `write-receptari` → procedimental (cas no-STEM però mateixa lògica d'ordre).

**🔑 Pregunta oberta per al panell:** ¿falta un gènere `write-problema`
(enunciat matemàtic) que avui no existeix? Cap SKILL actual cobreix
específicament l'enunciat de problema com a tipus textual. Decisió de
mineriaRAG: ampliar gèneres existents o crear-ne un de nou.

---

## 3. MILLORA 2a — Activació curricular (FASE 1: consum bàsic)

### 3.1. Bona notícia: el canon JA hi és i és determinista

`corpus/external/corpusFJE/curriculum/` conté JSON per etapa × matèria,
extrets dels decrets oficials (175/2022 P+ESO, 221/2022 BAT) amb
**`pdfplumber + regex, 0 IA generativa, 100% verificat`** (camp `_validacio`).

Exemple real (`eso/matematiques/matematiques_eso.json`, 80 KB):
- 9 competències específiques (CE1…CE9) amb text literal.
- Criteris d'avaluació (CA1.1…) amb 4 descriptors d'assoliment NA/AS/AN/AE.
- **133 sabers bàsics** amb `nivell` (1r_3r…), `bloc` (Sentit numèric…),
  `subapartat`, `text`.
- Competències transversals a `competencies_transversals/*.json`.

Estructura d'etapes disponibles: `infantil`, `primaria`, `eso`,
`batxillerat`, `fp` + `schemas/` + `competencies_transversals/`.

### 3.2. Què demanem (NOMÉS contracte, cap contingut nou)

ATNE vol consumir aquests JSON via un **selector cascada determinista**
(decisió de Miquel): `etapa → curs → àmbit/matèria → competències → sabers`,
**sense LLM al selector** (filtratge pur del JSON), amb **selecció múltiple
inter-matèries** per a projectes interdisciplinaris.

Perquè ATNE ho consumeixi sense fragilitat, demanem a mineriaRAG:

1. **Estabilitat de claus confirmada.** Hem detectat que la forma real divergeix
   del `schema_lomloe.json` base: el JSON de mates usa `competencies_especifiques`
   (top-level) + `sabers_items` (llista plana amb `nivell`/`bloc`/`subapartat`),
   mentre el schema descriu `cursos.<curs>.competencies_especifiques` +
   `sabers_basics` (per bloc). **Quina és la forma canònica vigent?** ATNE
   necessita UNA forma estable per parsejar. Si hi ha dues versions (v1.0 vs
   v1.1), digueu-nos quina pinjar.
2. **Un manifest/índex** `curriculum/manifest.json` (o equivalent) que llisti
   etapa → matèries disponibles → cursos/nivells, perquè el selector cascada
   d'ATNE no hagi de fer `ls` del submodule ni endevinar quins fitxers existeixen.
   Avui hauríem d'escanejar directoris; preferim un índex declaratiu.
3. **Mapeig `materia` ↔ `codi_area`** (p.ex. `Matemàtiques`↔`MAT`) com a taula al
   canon, perquè ATNE pugui (a) lligar el camp `materia` del Pas 2 amb el JSON
   curricular correcte i (b) activar el sub-bloc STEM correcte de la Millora 1.
   Avui `materia` a ATNE és **text lliure** sense normalitzar → cal una llista
   tancada canònica de matèries amb codi.
4. **Versió i pin.** Com sempre: digueu-nos el commit/tag a pinjar i quins
   derivats es regeneren sols via GitHub Action.

> **El que NO demanem en FASE 1:** cap interpretació pedagògica. ATNE injectarà
> el **text literal** del saber/competència seleccionats com a context de fons
> del prompt («El text ha de treballar aquest saber del currículum: <text>»).
> L'LLM decideix com. Això és **injecció mecànica**, no doctrina — i per tant no
> requereix canon nou, només contracte de lectura estable.

---

## 4. MILLORA 2b — Pont pedagògic «saber → text» (FASE 2, DIFERIT)

**Decisió de Miquel (2026-06-15): diferit a fase 2**, després de validar que el
consum bàsic (§3) funciona.

Quan s'activi, demanarem canonitzar un **M*.md de mediació curricular** amb la
doctrina «de saber/competència a instruccions per al text»: què implica
**treballar** una competència específica o un saber concret en el text generat i
en els complements (p.ex. «treballar el saber S2.3 de Sentit numèric implica que
el text ha de…, i les preguntes de comprensió han de…»). Això SÍ és doctrina
nova i ha de néixer al canon, no a ATNE.

**No cal fer res ara.** Ho registrem perquè quedi traçat l'origen i no es
construeixi mai a ATNE per drecera.

---

## 5. Prioritat i seqüència

Sense precedència forta entre les dues millores. Recomanació d'ATNE per a la
planificació de mineriaRAG:

1. **§3 (contracte curricular)** primer — és el més barat (només confirmar
   forma + 3 artefactes petits: manifest, mapeig matèria↔codi, pin). Desbloqueja
   valor immediat (pertinença curricular) i ATNE pot validar el consum ràpid.
2. **§2 (invariant disciplinari STEM)** en paral·lel — és el gruix de feina
   pedagògica (panell d'experts), el buit més gros i el més arriscat. Comença
   pels 3 patrons del §2.5 i la gradació MECR del §2.4.
3. **§4 (pont pedagògic)** diferit fins que §3 estigui consumit i validat.

---

## 6. Resum del que ATNE espera rebre del canon

- [ ] **§2** Secció `## Invariant disciplinari` (sub-blocs Matemàtiques /
  Ciències / Procedimental) a les SKILLs de gènere STEM, **gradada per MECR**,
  format **taula ADAPTABLE | INVARIANT**, fonamentada en el principi
  d'eixos independents (lligam ADR-001/2e).
- [ ] **§2.7** Decisió: quins gèneres la reben + ¿cal `write-problema`?
- [ ] **§3.2.1** Confirmació de la forma canònica del JSON curricular (claus
  estables).
- [ ] **§3.2.2** `manifest.json` curricular (índex etapa→matèria→curs).
- [ ] **§3.2.3** Taula canònica `materia ↔ codi_area` (llista tancada de
  matèries).
- [ ] **§3.2.4** Pin (commit/tag) + confirmació de regeneració de derivats.
- [ ] **§4** (diferit) Reconeixement que el pont pedagògic saber→text es
  canonitzarà a fase 2.

---

## 7. Decisions d'ATNE ja preses (no cal validar, només informatives)

- Enquadrament: STEM = secció dins SKILLs de gènere, **no** subsistema/gènere nou.
- Granularitat invariant: **per gènere amb sub-blocs per disciplina**.
- Abast STEM: enunciats + procediments + fórmules/notació + gràfics
  (tot tractat com a invariant disciplinari, no com a problema tècnic de format).
- UX currículum: **selector cascada determinista**, sense LLM, multi-matèria.
- Currículum fase 1 = **injecció mecànica** del text del saber; pont pedagògic
  = fase 2.
- Origen de tot el coneixement nou: **canon (mineriaRAG)**. ATNE consumeix.

---

*Document generat en sessió de disseny SDD ATNE 2026-06-15. Cap canvi de codi
fet a ATNE; aquest és un encàrrec de canonització. Quan mineriaRAG respongui,
ATNE obrirà el cicle R0 de consum (com a `per_al_docent.json` i el mapa
conceptual canon).*
