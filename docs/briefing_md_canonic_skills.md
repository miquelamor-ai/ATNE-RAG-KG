# Briefing per a ATNE — M*.md canònic dels skills (gèneres + mediació)

**Origen:** sessió Claude Code a mineriaRAG, 2026-05-22, amb Miquel.
**Destinatari:** ATNE (agent o sessió Claude treballant al repo ATNE).
**Objectiu:** consolidar els 35 skills (22 gèneres + 13 mediació + adapt-document) en un sol M*.md canònic per instrument, llest per ser publicat al corpusFJE i alimentar `build_skills.py`.

---

## 1. Context i decisió arquitectònica

Fins ara hem treballat amb tres versions paral·leles per cada skill:
- **V1** — SKILL.md a `corpusFJE/skills/<nom>/SKILL.md` (format Agent Skills per a LLM).
- **V2** — `ATNE/_bootstrap_fase0/V2_*/M3_instrument-*.md` (prosa descriptiva per a humans).
- **V3** — `ATNE/_bootstrap_fase0/V3_*/M3_instrument-*.md` (prosa + rúbrica taula gradada).

**Decisió 2026-05-22:** abandonem aquesta triple versió i consolidem en **una sola font M*.md canònica** amb una **taula narrativa única**. Les antigues V1/V2/V3 esdevenen materials d'origen per a la fusió o, en el cas de V1, derivat autogenerat futur.

**Per què una sola taula i no taula + prosa separades:** si conviuen taula i prosa, l'editor pot canviar-ne una i oblidar l'altra, i l'LLM consumeix una versió diferent de la que llegeix el docent. Risc silenciós inacceptable. Una sola font garanteix coherència automàtica.

---

## 2. Estructura canònica del M*.md

### Frontmatter

Camps obligatoris segons `corpus-spec.md` v2.4+:
```yaml
---
modul: M3  # o el que correspongui
titol: "Escriure/adaptar una notícia"
tipus: instrument
categoria_principal: generes  # | mediacio | avaluacio
categories_secundaries: []
descripcio: "..."
mecr_range: [pre-A1, A1, A2, B1, B2, C1]
agent_roles: [adapter, generator]  # segons l'skill
genre_key: noticia          # només per gèneres
complement_key: glossari    # només per mediació
translanguaging: true
multimodal: true
moduls_relacionats: [M3]    # per al filtratge contextual (vegeu §5)
review_status: revisat
generat_at: ...
actualitzat_at: ...
---
```

### Cos del fitxer

```markdown
# [Títol de l'skill]

## Descripció

[Paràgraf curt: què és l'instrument, per què s'usa, tipologia MALL, HCL principal/secundàries.]

## Detecció

[Senyals docent, senyals alumne, context favorable, anti-senyals.]

## Modulació per nivell

[LA TAULA — vegeu §3]

## Heurístiques docent

[3-5 heurístiques de detecció en prosa narrativa.]

## Fonts principals

[Llista bibliogràfica.]
```

---

## 3. La taula — l'element central

```markdown
| Pas              | Dimensió             | Pre-A1<br>Emergent | A1<br>Inicial | A2<br>Funcional | B1<br>Estratègic | B2<br>Acadèmic | C1+<br>Crític |
|---|---|---|---|---|---|---|---|
| **1. [Nom]**     | [Dimensió 1.1]       | [descriptor]       | [descriptor] | [descriptor]    | [descriptor]     | [descriptor]   | [descriptor]  |
|                  | [Dimensió 1.2]       | [descriptor]       | ...          | ...             | ...              | ...            | ...           |
| **2. [Nom]**     | [Dimensió 2.1]       | ...                | ...          | ...             | ...              | ...            | ...           |
| ...              | ...                  | ...                | ...          | ...             | ...              | ...            | ...           |
| **N-1. Criteris transversals** | [Crit 1] | ...    | ...          | ...             | ...              | ...            | ...           |
|                  | [Crit 2]             | ...                | ...          | ...             | ...              | ...            | ...           |
| **N. Autoavaluació** | (descriptor primera persona) | "He..." | "He..."     | "He..."         | "He..."          | "He..."        | "He..."       |
```

### Regles d'estructura

- **Columna 1 (Pas)**: procediment seqüencial. Cardinal per instrument (notícia 9, glossari menys). Format: `**N. Nom curt**`.
- **Columna 2 (Dimensió)**: aspectes a contemplar dins el pas. **1-N dimensions per pas** (no totes igual; algun pas en pot tenir 1, un altre 3).
- **Columnes 3-8 (Nivells)**: sempre 6, sempre amb etiqueta dual MECR + MALL. No afegir ni treure columnes per instrument.
- **Cel·les descriptor**: frases curtes autocontingudes (una microdescripció per cel·la, no etiquetes telegràfiques tipus "≤10 par.").

### Els dos darrers passos sempre

**Pas N-1 — Criteris transversals.** Qualitats globals del producte final. Sovint la mateixa cel·la repetida a totes les columnes (criteri purament binari); pot tenir matís per nivell quan correspongui. Exemples per a notícia:
- Adjectius valoratius: cap (a tots els nivells).
- Acrònims desplegats: matís per nivell.
- Fidelitat al text font: total (a tots els nivells).
- Registre: pot variar per nivell.

**Pas N — Autoavaluació metacognitiva.** Autoregulació del **procés**, en primera persona, gradat per nivell, **SENSE repetir passos anteriors**.
- ✅ "He revisat el meu text abans de donar-lo per acabat."
- ✅ "He pensat en el meu lector i en si entendrà les paraules tècniques."
- ✅ "He demanat ajuda quan no entenia alguna paraula del text font."
- ❌ "He escrit les 5W" (això repeteix el Pas 3, no és metacognició).

### Distinció pedagògica clau

- **Criteris transversals** = qualitats del **producte final** (què té el text al final).
- **Autoavaluació** = autoregulació del **procés** (com he treballat).

Si vols fer una "checklist de qualitat", va a transversals. Si vols fer una pregunta sobre el procés ("com he treballat?"), va a autoavaluació.

---

## 4. Gradació de nivells

**Per ara, sis columnes MECR amb etiqueta MALL:**

| Codi MECR | Etiqueta MALL |
|---|---|
| pre-A1 | Emergent |
| A1 | Inicial |
| A2 | Funcional |
| B1 | Estratègic |
| B2 | Acadèmic |
| C1+ | Crític |

**Variables independents al frontmatter, NO a la taula:**
- `fase_lectora: logografica | alfabetica_emergent | alfabetica_fluida`
- Altres variables configurables específiques de l'instrument.

Aquestes variables condicionen **descriptors interns de les cel·les** o activen **files condicionals** marcades amb `[només si X]`. No són noves columnes.

> ⚠️ **Parking lot:** la gradació per nivell s'ha de seguir investigant. En particular, com es comporta `fase_lectora` a través de tots els nivells MECR. Per ara fem amb aquesta estructura; potser caldrà refinar després.

---

## 5. Camp nou al frontmatter: `moduls_relacionats`

Els skills són transversals (no encaixen nets en un sol mòdul). Per permetre el filtratge contextual a scriptorium, cada skill ha d'incloure `moduls_relacionats` al frontmatter amb el lligam fort als mòduls FJE.

Proposta validada amb Miquel:

| Tipus skill | moduls_relacionats |
|---|---|
| Gèneres (22): write-* | `[M3]` |
| Mediació general (bastides, glossari, pictogrames, etc.) | `[M2, M3]` |
| generate-rubriques | `[M2, M6]` |
| generate-activitats-aprofundiment | `[M2, M4]` |
| adapt-document | `[M2, M3]` |

Detall complet a la conversa Claude Code mineriaRAG 2026-05-22.

---

## 6. Què passa amb V1/V2/V3 existents

| Versió | Què hem de fer |
|---|---|
| **V1** (SKILL.md a corpusFJE/skills/) | **Derivat futur autogenerat** per `build_skills.py` a partir del M*.md canònic. Per ara els actuals es conserven com a versió estable de producció fins que el nou pipeline estigui en marxa. |
| **V2** (`ATNE/_bootstrap_fase0/V2_*/`) | **Font primària** per al pas "Descripció" + prosa narrativa per a Detecció i Heurístiques docent. |
| **V3** (`ATNE/_bootstrap_fase0/V3_*/`) | **Font primària** per a la rúbrica gradada. Els passos i descriptors de la taula V3 són la base de la nova taula canònica. **Cal corregir errors detectats** (per exemple, V3_noticia té duplicació de secció "Detecció" a línies 54-69 — cal revisió neta abans de migrar). |

**No copiar mecànicament V3.** Cal una passada de revisió pedagògica per cada instrument: alguns passos potser cal fusionar, algunes dimensions potser cal extreure de cel·les massa carregades, els criteris transversals s'han d'agrupar al pas N-1, l'autoavaluació s'ha de reescriure perquè no repeteixi passos.

---

## 7. Què esperem d'ATNE — pla d'acció

### Pas 0 — Validar el briefing
Llegir aquest document. Si alguna cosa no quadra o és ambigua, fer-ho saber abans de començar.

### Pas 1 — Pilot amb un instrument
**Notícia** és la candidata natural (és la més madura, té V2 i V3 ben desenvolupats). Fusionar V2_noticia + V3_noticia en un sol M*.md canònic seguint l'estructura definida.

Resultat esperat: `ATNE/_bootstrap_fase0/CANONIC_noticia/M3_instrument-escriure-noticia.md` (o ubicació equivalent).

### Pas 2 — Validació humana
Miquel revisa el pilot. Iteració fins que el patró estigui validat.

### Pas 3 — Escalat als 34 instruments restants
Replicar el patró validat als 34 instruments restants. Notar que **caldrà revisió pedagògica per cada instrument**, no és una operació mecànica.

### Pas 4 — Publicació
mineriaRAG empaqueta els 35 M*.md i els puja a `corpusFJE/skills/<nom>/M3_instrument-<nom>.md`. ATNE NO necessita pujar res directament al corpusFJE — la pujada coordinada la fa mineriaRAG.

### Pas 5 — Pipeline derivat
mineriaRAG implementa `build_skills.py` per regenerar SKILL.md + rubrica.json des dels M*.md canònics. GitHub Action al corpusFJE dispara la regeneració automàtica a cada canvi de M*.md.

---

## 8. Format del SKILL.md derivat (per al LLM)

`build_skills.py` (que escriurà mineriaRAG) extreu **una columna** de la taula per nivell i la presenta verticalment al SKILL.md:

```
A1 — Inicial:

1. Identificació del fet
   - Punt clau: Respon "Qui?" i "Què?" en 1-2 paraules.

2. Titular
   - Punt clau: ≤10 paraules. Verb concret. Sense metàfores.

3. Lead
   - Cobertura 5W: 3W (Qui, Què, On).
   - Llargada frase: ≤12 paraules.
   - Estructura: Frase simple S+V+C.

...

N-1. Criteris transversals
   - Adjectius valoratius: cap.
   - Acrònims desplegats: sí, sempre.
   - Fidelitat al text font: total.

N. Autoavaluació
   - "He llegit el text un cop i, quan no entenia una paraula, l'he buscat o he demanat ajuda."
```

**Implicació crítica per a la redacció dels descriptors**: cada descriptor s'ha de poder llegir junt amb el nom de la dimensió i amb sentit propi. Una cel·la com "12" no funcionarà; una cel·la com "≤12 paraules per frase" sí. **Cada descriptor és una frase autocontinguda** amb verb o estat clar.

---

## 9. Errades conegudes a corregir durant la fusió

Detectades durant la sessió 2026-05-22:

1. **V3_noticia secció "Detecció" duplicada** (línies 54-69). Cal mantenir només una versió neta.
2. **Pot ser sistèmic.** ATNE hauria de fer una passada de revisió per detectar duplicacions o esborranys deixats a tots els V3 abans de migrar.

Si es troben més errors, anotar-los i comunicar-los abans de la fase d'escalat.

---

## 10. Parking lot / Decisions encara obertes

1. **Gradació de nivells** (vegeu §4): caldrà aprofundir en com `fase_lectora` interacciona amb MECR a la pràctica. Consultar NotebookLM MALL FJE pot ajudar.
2. **On viu `build_skills.py`**: pendent de la reunió 8 de juny. Proposta actual: Python a mineriaRAG + GitHub Action al corpusFJE (Opció A' del parking lot).
3. **Editor d'aquestes taules a scriptorium**: la lògica d'edició (capçaleres readonly, files de pas/dimensió readonly, cel·les editables) és tasca de scriptorium per a una sessió pròpia. No bloqueja la consolidació pedagògica.

---

## 11. Referències

- Memòria Claude Code mineriaRAG: `project_md_canonic_skills.md` (decisions consolidades).
- Memòria Claude Code mineriaRAG: `parking_rubrica_json_post_fase0.md` (decisió V2+JSON refinada).
- Memòria Claude Code mineriaRAG: `project_decisio_F_skills_marc.md` (calendari i context Fase 0).
- Memòria Claude Code mineriaRAG: `project_mall_mediacio.md` (MALL com a marc dels instruments de mediació; DUA = 1 de 6 categories MALL).
- Corpus: `corpusFJE/M2_instruments-mediacio-pedagogica.md` (taxonomia MALL canònica).
- Corpus: `corpusFJE/M2_bastides-lectura-produccio.md` (gradació MALL per a bastides; modalitat lectora dual).

---

## 12. Resum executiu en 5 línies

1. **Una sola font:** un M*.md canònic per instrument substitueix V1/V2/V3.
2. **Taula central:** Pas | Dimensió | 6 nivells MECR+MALL. Cel·les amb frases descriptives autocontingudes.
3. **Dos darrers passos sempre:** N-1 Criteris transversals (producte), N Autoavaluació metacognitiva (procés).
4. **Variables fora de la taula:** `fase_lectora` i d'altres viuen al frontmatter, no com a columnes.
5. **Pilot primer (notícia), validació humana de Miquel, després escalat als 34 restants. mineriaRAG s'encarrega de publicació i del pipeline derivat (SKILL.md + rubrica.json autogenerats).**
