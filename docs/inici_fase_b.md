# Inici Fase B — briefing executable per Claude

**Origen**: tancament Fase A 2026-05-25 nit (validació conjunta de Miquel + 5 decisions canòniques).
**Per a**: sessió Claude amb Miquel que comenci Fase B (qualsevol moment ≥ 2026-05-26).
**Format**: aquest document és **autosuficient**. Si comences sessió amb memòria buida, llegint això tens prou per arrancar sense fricció.

---

## 1. Síntesi executiva (300 paraules)

**Què és Fase B**: consolidar **31 instruments restants** del corpus FJE (20 gèneres + 11 mediació) + **2 instruments nous** (`expressar-preferencies` + `write-contrarelat-odi`) en format `M*.md canònic`, seguint el patró validat amb els 4 pilots Fase A (notícia, glossari, opinió, bastides-lectura).

**Qui ho fa**: tu (Claude) amb Miquel. La construcció pedagògica és tasca d'ATNE. mineriaRAG dona suport arquitectònic si apareixen casos especials.

**Què produeixes**: per a cada instrument, un fitxer `_bootstrap_fase0/CANONIC_<nom>/M3_instrument-<verb>-<nom>.md` que després es puja al submodule `corpus/external/corpusFJE/skills/<categoria>/<nom>/`. La GitHub Action regenera derivats automàticament.

**Pipeline per a cada instrument**:
1. Llegir V2 + V3 a `_bootstrap_fase0/V2_<nom>/` i `V3_<nom>/`.
2. Fusionar segons patró canònic (vegeu §5 i §6).
3. Crear `_bootstrap_fase0/CANONIC_<nom>/M3_instrument-<verb>-<nom>.md`.
4. Afegir com a font al notebook NotebookLM "Fase 0 — Jutge MALL/MECR" (`5524a29e-805c-4bf8-b1f7-001a412c9cb9`).
5. Llançar query crítica (template a §8).
6. Aplicar correccions al fitxer.
7. Commit + push a `ATNE/main`.
8. Copiar al submodule `corpus/external/corpusFJE/skills/<categoria>/<nom>/M3_instrument-*.md`.
9. Commit + push del submodule a `corpusFJE/master`.
10. Bump del submodule + commit + push a `ATNE/main`.

**Validació humana**: Miquel valida **per lot, no per instrument**. Cada lot són 2-4 instruments amb parentiu pedagògic. Si un lot trenca el patró, parar i discutir.

**Calendari estimat**: 3-4 setmanes (2-15 juny), 3-4 instruments per setmana. Fase C el ~22 juny.

---

## 2. Pre-flight checklist (lectura mínima abans de començar)

Aquests fitxers han de carregar-se al context (o resumir-se):

| Fitxer | Per a què |
|---|---|
| `docs/inici_fase_b.md` | **Aquest doc** — entrada principal |
| `CLAUDE.md` | Stack tècnic + context ATNE |
| Memòria `project_validacio_conjunta_fase_a_20260525.md` | 5 decisions canòniques |
| Memòria `project_md_canonic_skills_atne.md` | Decisions arquitectòniques de fons |
| `_bootstrap_fase0/CANONIC_glossari/M3_instrument-generar-glossari.md` | **Model d'estil** per a complements |
| `_bootstrap_fase0/CANONIC_noticia/M3_instrument-escriure-noticia.md` | **Model d'estil** per a gèneres |
| `_bootstrap_fase0/CANONIC_bastides-lectura/M3_instrument-generar-bastides-lectura.md` | **Model** per cross_source intra-pipeline + absència fidelitat |

---

## 3. Inventari complet — 31 + 2 instruments

### Gèneres (20 restants + 1 nou = 21)

- [x] B.1.1 — `write-conte` (v4.0.0-canonic, NLM si-amb-correccions-menors, 2026-05-26)
- [x] B.1.2 — `write-fabula` (v4.0.0-canonic, NLM si-amb-correccions-menors, 2026-05-26)
- [x] B.1.3 — `write-biografia` (v4.0.0-canonic, NLM si-amb-correccions-menors, 2026-05-26)
- [x] B.2.1 — `write-descripcio` (v4.0.0-canonic, NLM si-amb-correccions-menors, 2026-05-26)
- [x] B.2.2 — `write-divulgatiu` (v4.0.0-canonic, NLM si-amb-correccions-menors, 2026-05-26)
- [x] B.2.3 — `write-enciclopedic` (v4.0.0-canonic, NLM si-amb-correccions-menors, 2026-05-26)
- [x] B.2.4 — `write-informe` (v4.0.0-canonic, NLM si-amb-correccions-menors, 2026-05-26)
- [x] B.3.1 — `write-cronica` (v4.0.0-canonic, NLM si-amb-correccions-menors, 2026-05-26)
- [x] B.3.2 — `write-entrevista` (v4.0.0-canonic, NLM si-amb-correccions-menors, 2026-05-26)
- [x] B.3.3 — `write-diari` (v4.0.0-canonic, NLM si-amb-correccions-menors, 2026-05-26)
- [x] B.3.4 — `write-carta` (v4.0.0-canonic, NLM si-amb-correccions-menors, 2026-05-26)
- [x] B.4.1 — `write-instructiu` (v4.0.0-canonic, NLM si, 2026-05-26)
- [x] B.4.2 — `write-manual` (v4.0.0-canonic, NLM si, 2026-05-26)
- [x] B.4.3 — `write-receptari` (v4.0.0-canonic, NLM si-amb-correccions, 2026-05-26)
- [x] B.4.4 — `write-reglament` (v4.0.0-canonic, NLM si-amb-correccions-menors, 2026-05-26)
- [x] B.5.1 — `write-assaig` (v4.0.0-canonic, NLM si-amb-correccions-menors, 2026-05-26)
- [x] B.5.2 — `write-ressenya` (v4.0.0-canonic, NLM si-amb-correccions-menors, 2026-05-26)
- [x] B.5.3 — `write-resum` (v4.0.0-canonic, NLM si-amb-correccions-menors, 2026-05-26)
- [x] B.6.1 — `write-poema` (v4.0.0-canonic, NLM si-amb-correccions-menors, 2026-05-26)
- [x] B.6.2 — `write-dialeg` (v4.0.0-canonic, NLM si-amb-correccions-menors, 2026-05-26)
- [x] B.6.3 — `expressar-preferencies` (v4.0.0-canonic, NLM si-amb-correccions-menors, 2026-05-26) **(NOU)**
- [ ] **FINAL** — `write-contrarelat-odi` **(NOU)** — *últim lot pre-Fase C, vegeu §10*

### Mediació (11 restants)

- [x] B.7.1 — `generate-pictogrames` (v4.0.0-canonic, NLM si-amb-correccions-menors, 2026-05-26)
- [x] B.7.2 — `generate-illustracions` (v4.0.0-canonic, NLM si-amb-correccions-menors, 2026-05-26)
- [ ] B.8.1 — `generate-bastides-produccio` *(cas especial — vegeu §9)*
- [ ] B.8.2 — `generate-plantilles-genere`
- [ ] B.9.1 — `generate-preguntes-comprensio` *(cross_source intra-pipeline amb bastides-lectura)*
- [ ] B.9.2 — `generate-activitats-aprofundiment`
- [ ] B.9.3 — `generate-resum-graduat` *(cas especial — vegeu §9)*
- [ ] B.10.1 — `generate-mapa-conceptual`
- [ ] B.10.2 — `generate-cartes-conversacionals`
- [ ] B.10.3 — `generate-tolc`
- [ ] B.10.4 — `generate-rubriques`

**NO consolidar**: `generate-bastides` (sense -lectura/-produccio) — deprecada al SKILL.md actual.

---

## 4. Organització en 10 lots

| Lot | Instruments | Parentiu pedagògic | Estimat |
|---|---|---|---|
| **B.1** | conte, fabula, biografia | Narratius literaris | 1 setmana |
| **B.2** | descripcio, divulgatiu, enciclopedic, informe | Expositius | 1 setmana |
| **B.3** | cronica, entrevista, diari, carta | Narratius testimonials | 1 setmana |
| **B.4** | instructiu, manual, receptari, reglament | Instructius | 1 setmana |
| **B.5** | assaig, ressenya, resum | Argumentatius/sintètics | 1 setmana |
| **B.6** | poema, dialeg, **expressar-preferencies** | Expressius/dialògics | 1 setmana |
| **B.7** | pictogrames, illustracions | Multimodals visuals | 0.5 setmana |
| **B.8** | bastides-produccio, plantilles-genere | Bastides de producció | 0.5 setmana |
| **B.9** | preguntes-comprensio, activitats-aprofundiment, resum-graduat | Suports comprensió | 1 setmana |
| **B.10** | mapa-conceptual, cartes-conversacionals, tolc, rubriques | Resta mediació | 1 setmana |
| **FINAL** | **write-contrarelat-odi** | Pre-Fase C, complex | 1 setmana |

**Validació Miquel = per lot**. Quan un lot està complet i NotebookLM-validat, Miquel revisa el lot abans de continuar.

---

## 5. Patró M\*.md canònic (estructura obligatòria)

Cada fitxer ha de tenir **exactament** aquesta estructura (referent: pilots Fase A):

```
---
modul: M3
titol: "<Verb> <nom>"
tipus: instrument
categoria_principal: generes | mediacio
categories_secundaries: []
descripcio: "<resum d'una frase amb estructura, mecr_range i passos>"
mecr_range: [pre-A1, A1, A2, B1, B2, C1]   # exclou pre-A1 si pertoca
agent_roles: [adapter, generator]            # complements: només [generator]
genre_key: <nom>                              # només si categoria = generes
complement_key: <nom>                         # només si categoria = mediacio
translanguaging: true | false
multimodal: true | false
moduls_relacionats: [M3]                      # vegeu §7 per regles
variables_configurables:
  fase_lectora: [logografica, alfabetica_emergent, alfabetica_fluida]
skill_meta: <skill_name>@corpusFJE/skills/<categoria>/<nom>
review_status: pilot-fusio-<N>
version: 4.0.0-canonic
generat_at: YYYY-MM-DD
actualitzat_at: YYYY-MM-DD
notebooklm_review:
  data: <pendent fins query>
  veredicte: <pendent>
  aplicades_des_d_inici: [patro-canonic-pilots-fase-a, ...]
  aplicades_post_review: [...]
  comentari_key: "..."
---

# <Verb> <nom>

## Descripció
<Tipologia MALL · HCL primària · HCL secundàries · Principi rector>
<Connexions MALL transversals: translanguaging/TOLC, multimodalitat, eix oral/escrit>

**Aclariment d'ús — què descriu aquesta rúbrica.**
<Aplicar C1: rúbrica = LECTURA, no producció autònoma. Sub-pre-A1 via fase_lectora.>

## Detecció
<Senyals docent · Senyals alumne · Context favorable · Anti-senyals>

## Modulació per nivell
<Taula | Pas | Dimensió | Pre-A1 | A1 | A2 | B1 | B2 | C1+ |>
<Variable nombre de passos. Sempre acaba amb Pas N-1 transversal + Pas N autoavaluació.>

## Metadades de cel·la (per a `build_skills.py`)
<Definir tipus de descriptor + taula amb requires_source_text + validation_hint>

## Heurístiques docent
<5 H pràctiques, numerades H1-H5>

## Fonts principals
<MALL + autors específics + Decret 175/2022>
```

---

## 6. 6 decisions canòniques (regiren tots els pilots Fase B)

### Decisió 1 — Asimetria `agent_roles`
Gèneres: `[adapter, generator]`. **Complements: `[generator]`** (no `adapter`).

**Principi pedagògic**: els complements **no s'adapten — es generen segons les característiques del perfil**. El mateix complement pot ser **diferent segons perfil** (glossari TEA ≠ glossari AACC; bastides dislèxia ≠ bastides nouvingut).

**Implicació al M\*.md**: a complements de Fase B, documentar (almenys a Heurístiques o Detecció) exemples de **modulació per perfil específic**, no només per MECR/fase_lectora/nouvingut.

### Decisió 2 — Variabilitat cardinal de passos
**No s'estandarditza** el nombre de passos. Cada instrument té la seva lògica natural. Però la consistència es manté en el **patró meta** (estructura comuna de §5).

### Decisió 3 — C1 (aclariment lectura vs producció) obligatori
Cada M\*.md ha de tenir explícitament:
> "Aquesta rúbrica descriu el text/instrument adaptat per a la LECTURA de l'alumne. **No descriu la producció autònoma**."

### Decisió 4 — C2 (fidelitat gradada) si aplica
Si l'instrument reformula contingut d'un text font (gèneres), incloure descriptor de fidelitat gradat per nivell (nuclear pre-A1→A2 · fet+context B1 · matís B2-C1+).

Si l'instrument **orienta** un procés (bastides, preguntes-comprensio), **no incloure** descriptor de fidelitat al text font. Patró validat per NotebookLM com a "absència de fidelitat per a instruments d'orientació".

### Decisió 5 — Validació NotebookLM obligatòria
**Tots els pilots Fase B passen per NotebookLM**. No replicació mecànica sense validació. Notebook: `5524a29e-805c-4bf8-b1f7-001a412c9cb9`.

### Decisió 6 — Pre-A1: criteri del concret vs l'abstracte
**Emergida del lot B.1 (2026-05-26)**. Un instrument admet `pre-A1` si i només si el significat es pot construir per via visual i concreta, mediat per l'adult, sense inferència simbòlica ni abstracció temporal.

**Filtre en dues preguntes**:
1. Pot l'adult mediar el significat amb imatges i gest, sense que l'alumne hagi d'inferir res? → Si sí, pre-A1 possible.
2. El gènere requereix comprendre dos plans simultanis (simbòlic, temporal, causal diferit)? → Si sí, NO pre-A1.

**Casos del lot B.1**:
- `write-conte` → **pre-A1 SÍ**: personatge + acció + imatge, significat concret i visual.
- `write-fabula` → **pre-A1 NO**: relació historia↔moral requereix abstracció de 2n nivell (símbol).
- `write-biografia` → **pre-A1 NO**: cronologia i llegat diferit requereixen temps com a categoria abstracta.

**Implicació per als lots restants**: aplicar el filtre per a cada nou instrument. Documentar la justificació al camp `No s'adapta a pre-A1:` de la Descripció.

---

## 7. Regles de frontmatter

### `moduls_relacionats`
- Gèneres: `[M3]`
- Mediació general: `[M2, M3]`
- `generate-rubriques`: `[M2, M6]` (M6 = Avaluació)
- `generate-activitats-aprofundiment`: `[M2, M4]` (M4 = Contingut Curricular)
- `write-contrarelat-odi`: `[M3, M8]` (M8 = Governança / ciutadania)

### `variables_configurables`
- Si admet pre-A1: `fase_lectora: [logografica, alfabetica_emergent, alfabetica_fluida]`
- Si no admet pre-A1: `fase_lectora: [alfabetica_emergent, alfabetica_fluida]`
- Casos especials (com `write-contrarelat-odi`): `modalitat: [counterspeech-directe, counter-narrative-indirecte]`

### `translanguaging` i `multimodal`
- Decidir segons naturalesa pedagògica de l'instrument.
- Bastides en general: `translanguaging: false` (orienten en català, no tradueixen).
- Poema, diàleg: `multimodal: false` (textuals).
- Pictogrames, illustracions: `multimodal: true` obligatori.

---

## 8. Plantilla de query NotebookLM

Per a cada pilot, enganxa el M\*.md com a font al notebook `5524a29e-805c-4bf8-b1f7-001a412c9cb9` i llança:

```
Validació crítica del **Pilot Fase B — `M3_instrument-<verb>-<nom>.md`**.

Context: és un dels 31+2 instruments de Fase B (consolidació corpus FJE).
Els 4 pilots Fase A (notícia, glossari, opinió, bastides-lectura) ja són
fonts d'aquest notebook i han estat validats com a patró canònic.

Avalua els 6 punts següents i dóna veredicte global al final:

1. Coherència amb el patró canònic Fase A (estructura, decisions C1-C4).
2. Rigor pedagògic MALL (3 moments × 3 plànols, gradació MECR coherent).
3. Pas N-1 transversal i Pas N autoavaluació adequats.
4. Metadades de cel·la (tipus, requires_source_text, validation_hint) correctes.
5. Decisions arquitectòniques pròpies de l'instrument (modulació per perfil,
   cas especial si aplica).
6. Heurístiques (5 H, complementàries, pràctiques) i fonts (pertinents).

Veredicte: sí / sí-amb-correccions / sí-amb-correccions-menors / no.
Correccions: codi (C1, C2, ...) + localització (pas/dimensió/nivell) + què canviar.
Comentari clau: una frase.
Pregunta oberta a Miquel (si en tens): un punt on cal judici humà.
```

---

## 9. Casos especials coneguts

### 9.1 — `generate-bastides-produccio` (sense V2 dedicat)
Mateix patró que `generate-bastides-lectura` Fase A: V2 compartit (`V2_bastides`) + V3 dedicat (`V3_bastides-produccio`). La fusió canònica reté **només la dimensió producció** del V2.

Diferència crítica respecte a lectura: bastides-produccio aplica **només a A1+** (zero escriptura autònoma a pre-A1).

### 9.2 — `write-resum` vs `generate-resum-graduat`
**Mapatge ambigu** entre el gènere `write-resum` i el complement `generate-resum-graduat`. Aclarir amb Miquel + mineriaRAG abans de B.5/B.9:
- ¿Són el mateix instrument categoritzat de dues maneres?
- ¿Són funcions diferents (resum com a gènere autònom vs resum com a complement d'altre text)?
- Possible decisió: deprecar un dels dos o redefinir-los.

### 9.3 — `generate-preguntes-comprensio` (cross_source amb bastides-lectura)
Aquest complement és l'altre extrem de la dependència intra-pipeline establerta al pilot 4. Pel patró C.2 mineriaRAG:
- **Prevenció per disseny**: si bastides-lectura està actiu, preguntes-comprensio NO ha de duplicar la seva funció (i a la inversa).
- **Fallback dedup amb prioritat**: `preguntes_comprensio` **guanya** sobre `bastides`.

Documentar aquesta interacció al M\*.md.

---

## 10. 2 instruments nous (fonts a citar al cos)

### 10.1 — `expressar-preferencies` (a lot B.6)

**Fonts a citar literalment al cos del M\*.md** (decisió mineriaRAG: la citació substitueix funcionalment el segell d'autor):
- Common Core W.K.1 (literal: "state an opinion or preference")
- Kant, *Crítica del Judici* §7 (distinció preferència vs judici)
- Habermas (3 pretensions de validesa: Wahrhaftigkeit/Richtigkeit/Wahrheit)
- Toulmin 1958 (claim vs argument)
- Kuhn 1991 (desenvolupament infantil del raonament)

**mecr_range**: `[pre-A1, A1]`
**`multimodal: true` obligatori** (pictograma de cara emocional + paraula clau + referent).
**HCL primària**: Valorar/Preferir (BICS). Evoluciona cap a Argumentar (CALP) a A2+ via `write-opinio`.

### 10.2 — `write-contrarelat-odi` (últim lot pre-Fase C)

**Fonts a citar literalment**:
- Izquierdo Grau (UAB 2019) — tesi *Contrarelats de l'odi a l'ensenyament i aprenentatge de les Ciències Socials*
- GREDICS UAB (Santisteban)
- Susan Benesch / Dangerous Speech Project (taxonomia 8 estratègies de counterspeech)
- Council of Europe (*Bookmarks*, *We CAN!*, CM/Rec(2022)16)
- UNESCO (*Think Critically, Click Wisely!* MIL 2021)
- Walton, *Argumentation Schemes* (1996, 2008)
- Decret 175/2022 (competència ciutadana)

**mecr_range**: `[A1, A2, B1, B2, C1]` (no pre-A1)
**`multimodal: false`** (argumentatiu textual)
**`moduls_relacionats: [M3, M8]`**
**`variables_configurables`** ha d'incloure `modalitat: [counterspeech-directe, counter-narrative-indirecte]`
**8 passos** (proposta validada al parking): identificació discurs d'odi · discerniment ignasià · composició de lloc · fact-checking · construcció resposta segons modalitat · crida a acció democràtica · criteris transversals · examen ignasià.

**Cautela**: tractar marc ignasià com a **arquitectura pedagògica** (no contingut confessional explícit). Funcional en aules amb alumnat no creient.

---

## 11. Pipeline de Fase C (referència — no executar fins ~22 juny)

Quan els 31+2 estiguin consolidats i validats:
1. **Commit únic al corpusFJE** per part de mineriaRAG: `mv _derivats_v2/SKILL.md SKILL.md` per a cada `skills/<categoria>/<nom>/`.
2. **ATNE actualitza submodule** + commit/push del bump a `ATNE/main`.
3. **Test ATNE amb 5-10 adaptacions reals** per detectar regressions.

ATNE no executa l'1, només l'2 i l'3. mineriaRAG coordina.

---

## 12. Glossari de paths útils

| Path | Què hi ha |
|---|---|
| `_bootstrap_fase0/V2_<nom>/` | Fonts V2 descriptives (entrada per fusió) |
| `_bootstrap_fase0/V3_<nom>/` | Fonts V3 rúbrica gradada (entrada per fusió) |
| `_bootstrap_fase0/CANONIC_<nom>/` | Sortida M\*.md canònic (treball ATNE) |
| `corpus/external/corpusFJE/skills/<categoria>/<nom>/` | Destí canon FJE (push de submodule) |
| `corpus/external/corpusFJE/skills/<categoria>/<nom>/_derivats_v2/` | Regenerat per GitHub Action (no tocar) |

---

## 13. Compte amb saturació API

A sessions anteriors (2026-05-25 tarda), els Agents acadèmics van caure 4 cops amb error 529 (overload Anthropic). Si torna a passar a Fase B:
- Usar **WebSearch directe** + **NotebookLM** com a substituts.
- No retry agressiu — espera 5-10 min entre intents.

---

## 14. Memòria viva a actualitzar

Després de cada **lot** validat (no per instrument):
- Actualitzar `MEMORY.md` amb entrada nova de la sessió.
- Si emergeix un aprenentatge nou o cas especial inesperat, registrar com a memòria de projecte separada.
- Si una decisió canònica de §6 trenca, **parar** i discutir amb Miquel + mineriaRAG abans de continuar.

---

## 15. Inici de sessió Claude Fase B — checklist

Quan comencis sessió Claude per a Fase B:

1. [ ] Llegir aquest doc (`docs/inici_fase_b.md`).
2. [ ] Carregar les memòries de §2 (pre-flight).
3. [ ] Confirmar amb Miquel: quin lot comencem (B.1 per defecte).
4. [ ] Verificar `git status` net + `origin/main` sincronitzat.
5. [ ] Llançar pipeline per al primer instrument del lot (§1 passos 1-10).
6. [ ] Continuar fins completar el lot.
7. [ ] Demanar validació Miquel del lot complet.
8. [ ] Si OK → següent lot. Si KO → parar + discutir.

**Bona feina. La Fase A ha demostrat que el patró escala. La Fase B és replicació mecànica amb validació crítica.**
