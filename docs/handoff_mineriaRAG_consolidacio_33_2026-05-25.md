# Handoff a ATNE — consolidació dels 33 instruments restants

**Origen:** sessió mineriaRAG ↔ Miquel, 2026-05-25.
**Destinatari:** sessió ATNE (agent o sessió Claude treballant al repo ATNE).
**Objectiu:** consolidar els 33 instruments restants en M*.md canònic per al corpusFJE, perquè els derivats es generin automàticament i poguem fer el switch d'ATNE.

---

## Estat actual (què ja està fet)

El **pipeline mineriaRAG ↔ corpusFJE està operatiu**:

- **Corpus-spec v2.6** publicada — `mineriaRAG/docs/corpus-spec.md` §4.X.4 i §4.X.5 (estructura M*.md + metadades de cel·la).
- **2 pilots ja al corpusFJE** (validats per tu i committejats):
  - `corpusFJE/skills/generes/write-noticia/M3_instrument-escriure-noticia.md`
  - `corpusFJE/skills/mediacio/generate-glossari/M3_instrument-generar-glossari.md`
- **GitHub Action "Build skills derivats"** al corpusFJE: cada push d'un `M3_instrument-*.md` regenera automàticament `_derivats_v2/SKILL.md` i `_derivats_v2/prompt_adapter.md` per a aquell instrument. **Validat en producció** (commit-bot `393a9a4`).
- **`build_skills.py`** és determinista, viu a `corpusFJE/.tooling/build_skills.py`. **No actua a runtime per a ATNE**, només al moment de commit dels M*.md.
- **`audit_corpus.py`** té 7 regles noves K-INST-01..07 que validen l'estructura del M*.md d'instrument.

## Què queda fora d'abast

- **rubrica_avaluacio_<niv>.md**: APARCAT (decisió 2026-05-24). No té consumidor avui. S'activarà quan scriptorium tingui mòdul d'avaluació o ATNE entri en mode avaluador.
- **LLM-jutge per a feedback per banda**: aparcat amb la rubrica.
- **Calibratge amb 1.050 textos d'ancoratge**: aparcat amb el LLM-jutge.

## Què espera mineriaRAG (i Miquel) de tu, ATNE

### Tasca

Consolidar els 33 instruments restants en M*.md canònics seguint **exactament** el patró validat amb notícia + glossari. **No facis derivats** — els fa l'Action automàticament. Tu només crees el M*.md font.

### Inventari de pendents

**Gèneres (21 restants):**
1. write-assaig
2. write-biografia
3. write-carta
4. write-conte
5. write-cronica
6. write-descripcio
7. write-dialeg
8. write-diari
9. write-divulgatiu
10. write-enciclopedic
11. write-entrevista
12. write-fabula
13. write-informe
14. write-instructiu
15. write-manual
16. write-opinio
17. write-poema
18. write-receptari
19. write-reglament
20. write-ressenya
21. write-resum

**Mediació (12 restants):**
1. generate-activitats-aprofundiment
2. generate-bastides-lectura
3. generate-bastides-produccio
4. generate-cartes-conversacionals
5. generate-illustracions
6. generate-mapa-conceptual
7. generate-pictogrames
8. generate-plantilles-genere
9. generate-preguntes-comprensio
10. generate-resum-graduat
11. generate-rubriques
12. generate-tolc

**Excepció**: `generate-bastides` (sense -lectura/-produccio) està marcada com a `deprecated` al SKILL.md actual. **No la consolidis**; en lloc seu hi van bastides-lectura i bastides-produccio.

### Material que tens

- **Bootstrap V2/V3 d'ATNE** (`_bootstrap_fase0/V2_*/` i `_bootstrap_fase0/V3_*/`) — font primària per a la fusió pedagògica.
- **Els 2 pilots ja consolidats** com a model d'estil (notícia per a gèneres, glossari per a mediació).
- **Briefing complet** a `mineriaRAG/docs/briefing_md_canonic_skills.md` (estructura M*.md, taula, dos darrers passos, etc.).
- **Plantilla buida** a `mineriaRAG/docs/template_instrument.md` (esquelet amb tots els blocs).

### Estratègia recomanada (per fases, amb validació de Miquel)

**Fase A — 2 pilots addicionals per validar generalització (1 setmana)**

Triar dos instruments **conceptualment diferents** dels pilots per confirmar que el patró escala més enllà del gènere informatiu i la mediació lèxica:

- **Un gènere argumentatiu**: recomanat **`write-opinio`** (és el que va donar més problemes a Fase 0, val la pena tenir-lo aviat).
- **Una bastida no-lèxica**: recomanat **`generate-bastides-lectura`** (és la més complexa i serveix de model per a les altres bastides).

Procés:
1. Fusionar V2 + V3 d'aquell instrument → M*.md canònic.
2. Validar amb NotebookLM MALL (com vas fer amb els pilots).
3. Push a `corpusFJE/skills/<categoria>/<nom>/M3_instrument-<verb>-<nom>.md`.
4. **Esperar el commit-bot** (gestionat per la GitHub Action) que regenera `_derivats_v2/`.
5. Validació de Miquel + qualsevol docent disponible.
6. Si tot OK → endavant Fase B. Si calen ajustos al patró → comunica-ho i revisem la spec.

**Fase B — Resta en lots temàtics (3-4 setmanes)**

Recomano agrupar per parentiu pedagògic, no fer-ho alfabèticament. Per exemple:

| Lot | Instruments | Per què junts |
|---|---|---|
| B.1 | write-conte, write-fabula, write-biografia | Narratius literaris |
| B.2 | write-descripcio, write-divulgatiu, write-enciclopedic, write-informe | Expositius |
| B.3 | write-cronica, write-entrevista, write-diari, write-carta | Narratius testimonials |
| B.4 | write-instructiu, write-manual, write-receptari, write-reglament | Instructius |
| B.5 | write-assaig, write-ressenya, write-resum | Argumentatius/sintètics |
| B.6 | write-poema, write-dialeg | Expressius/dialògics |
| B.7 | generate-pictogrames, generate-illustracions | Multimodals visuals |
| B.8 | generate-bastides-produccio, generate-plantilles-genere | Bastides de producció |
| B.9 | generate-preguntes-comprensio, generate-activitats-aprofundiment, generate-resum-graduat | Suports comprensió/aprofundiment |
| B.10 | generate-mapa-conceptual, generate-cartes-conversacionals, generate-tolc, generate-rubriques | Resta de mediació |

Validació per lot, no per instrument. Si un lot dóna problemes, parem i discutim abans de continuar.

**Fase C — Switch ATNE coordinat (1 dia)**

Quan els 33 estiguin consolidats i validats:
1. Commit únic al corpusFJE: per cada `skills/<nom>/`, `mv _derivats_v2/SKILL.md SKILL.md` (sobreescriu).
2. ATNE actualitza submodule → consumeix els nous SKILL.md.
3. Test ATNE amb 5-10 adaptacions reals per detectar regressions.

## Punts crítics que NO has d'oblidar

1. **Cada M*.md ha de portar el bloc `## Metadades de cel·la (per a build_skills.py)`** amb el contracte tipat. Sense això, `audit_corpus.py` (K-INST-04, K-INST-05, K-INST-06) marca fail i la generació de derivats és menys útil.

2. **Els 2 darrers passos sempre**: `Pas N-1: Criteris transversals` (qualitats del producte, sovint mateix descriptor a tots els nivells) + `Pas N: Autoavaluació metacognitiva` (autoregulació del **procés**, no repetir passos).

3. **Frontmatter sempre amb `moduls_relacionats`**. Els 37 SKILL.md actuals ja en tenen. Per als M*.md nous:
   - Gèneres: `[M3]`
   - Mediació general: `[M2, M3]`
   - generate-rubriques: `[M2, M6]`
   - generate-activitats-aprofundiment: `[M2, M4]`

4. **No toquis els SKILL.md actuals**. Són la producció d'ATNE avui. Els nous derivats viuen a `_derivats_v2/` sense interferir.

5. **No regeneris derivats a mà**. La GitHub Action ho fa. Tu només pugues `M3_instrument-*.md`.

## Verificació automàtica

Cada cop que pugis un M*.md, la GitHub Action et farà:
- ✅ Si tot va bé: apareix un commit `chore(skills): regenera _derivats_v2/ [skip ci]` del corpus-bot al cap d'uns segons. Els `_derivats_v2/` actualitzats apareixen al repo.
- ❌ Si hi ha error: el workflow surt en vermell a [github.com/miquelamor-ai/corpusFJE/actions](https://github.com/miquelamor-ai/corpusFJE/actions). Mira el log del pas en vermell i corregeix.

Pots també validar localment abans de pujar:
```bash
python audit_corpus.py <path-al-M*.md>
# (regles K-INST-01..07)
```

## Calendari estimat

| Setmana | Activitat |
|---|---|
| 26 maig | Fase A (2 pilots addicionals: opinió + bastides-lectura) + validació Miquel |
| 2-15 juny | Fase B (10 lots, 3-4 instruments per setmana segons disponibilitat) |
| ~22 juny | Fase C (switch ATNE) |

És orientatiu — la disponibilitat de Miquel per validar és el factor limitant, no la teva capacitat d'escriure.

## Què fa mineriaRAG en paral·lel

- Manteniment del pipeline si trobes algun cas que trenca el parser (improbable; el parser és determinista i tolerant).
- Suport puntual si cal afegir tipus de descriptor nous (els 7 actuals estan estabilitzats, però oberts a ampliació documentada).
- Quan estiguis a Fase C (switch), coordinarà el commit únic de reemplaçament.

## Què NO ha de fer mineriaRAG

- Escriure contingut pedagògic dels M*.md (tu tens el context MALL, no jo).
- Validar pedagògicament (això és tasca de Miquel i d'altres docents si vol involucrar-los).

## Pregunta directa per a ATNE

Quan llegeixis aquest handoff, confirma a Miquel:
1. Acceptes el repartiment (tu pedagogia, jo pipeline)?
2. Comences per la Fase A (write-opinio + generate-bastides-lectura)?
3. Hi ha algun bloqueig que veiem que no he previst?

---

## Referències al repo

- Corpus-spec v2.6: [mineriaRAG/docs/corpus-spec.md](../corpus-spec.md)
- Briefing original: [mineriaRAG/docs/briefing_md_canonic_skills.md](./briefing_md_canonic_skills.md)
- Plantilla M*.md: [mineriaRAG/docs/template_instrument.md](./template_instrument.md)
- Pilots de referència:
  - [corpusFJE/skills/generes/write-noticia/M3_instrument-escriure-noticia.md](https://github.com/miquelamor-ai/corpusFJE/blob/master/skills/generes/write-noticia/M3_instrument-escriure-noticia.md)
  - [corpusFJE/skills/mediacio/generate-glossari/M3_instrument-generar-glossari.md](https://github.com/miquelamor-ai/corpusFJE/blob/master/skills/mediacio/generate-glossari/M3_instrument-generar-glossari.md)
