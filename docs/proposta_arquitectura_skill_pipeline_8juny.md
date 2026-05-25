# Proposta arquitectònica per a la reunió del 8 de juny — pipeline `build_skills.py`

> ⚠️ **ESTAT 2026-05-25**: aquest document és **parcialment obsolet**. mineriaRAG ha avançat sense esperar la reunió i ha implementat el pipeline. Vegeu [handoff_mineriaRAG_consolidacio_33_2026-05-25.md](handoff_mineriaRAG_consolidacio_33_2026-05-25.md) per a l'estat real. Resum dels canvis:
> - ✅ `build_skills.py` ja existeix a `corpusFJE/.tooling/`.
> - ✅ GitHub Action operativa: cada push de `M3_instrument-*.md` regenera `_derivats_v2/SKILL.md` + `_derivats_v2/prompt_adapter.md`.
> - ✅ Corpus-spec v2.6 publicada amb metadades de cel·la.
> - ✅ `audit_corpus.py` valida M\*.md amb regles K-INST-01..07.
> - ⏸️ `rubrica_avaluacio_<niv>.md` **aparcat** — sense consumidor avui; s'activarà quan scriptorium o ATNE el necessitin.
> - ⏸️ Calibratge LLM-jutge i 1.050 textos d'ancoratge **aparcat** amb la rúbrica.
>
> Aquesta proposta queda com a **document arxivat** per traçabilitat de les decisions arquitectòniques inicials. El nou material de referència és el handoff de mineriaRAG.

**Origen**: sessió ATNE amb Claude, 2026-05-22 / 2026-05-23.
**Destinatari**: equip mineriaRAG + Miquel + qui calgui de l'equip docent.
**Objectiu**: arribar a la reunió del 8 de juny amb una proposta concreta sobre com han de viure els skills (gèneres + mediació) i quin pipeline els genera, perquè la discussió sigui sobre opcions concretes i no en abstracte.

---

## 1. Resum executiu (3 línies)

1. **El M\*.md canònic no és prosa; és un model de dades.** Cada cel·la de la rúbrica té un tipus (`countable`, `binary`, `qualitative`, etc.) que condiciona com es deriva.
2. **D'un sol M\*.md surten tres derivats automàtics**: SKILL.md (prompt LLM), rubrica_avaluacio.md (graella docent), prompt_adapter.md (encàrrec d'adaptació).
3. **mineriaRAG implementa `build_skills.py` + GitHub Action**; ATNE consumeix els derivats com a fonts de veritat un cop el corpusFJE estigui actualitzat.

---

## 2. Decisió arquitectònica de fons

### Què és un M\*.md canònic d'instrument

Una **sola font de veritat** descriptiva per skill, amb:
- Frontmatter amb metadades del skill (modul, mecr_range, agent_roles, moduls_relacionats, variables_configurables).
- Cos amb seccions estables: Descripció · Detecció · Modulació per nivell (taula gradada) · Metadades de cel·la · Heurístiques docent · Fonts principals.
- Una **taula central** Pas × Dimensió × 6 nivells MECR+MALL, amb cel·les descriptores autocontingudes.

### El que la sessió d'avui ha demostrat

Validació empírica feta amb el pilot **notícia**:

- ✅ Un sol M\*.md pot servir simultàniament al docent (referent pedagògic) i a derivats automàtics.
- ✅ NotebookLM (28 fonts MALL) confirma la posició majoritària: **una rúbrica, múltiples veus**.
- ✅ Literatura internacional (CEFR Companion Volume 2018, Sadler 1989, Black & Wiliam 2018, Andrade/Brookhart/Panadero) coincideix: same rubric, multiple uses.
- ⚠️ **Però** el M\*.md actual encara és massa narratiu per a script automàtic — calen metadades estructurals per cel·la. Ja afegides al pilot notícia (vegeu §4).

---

## 3. Pipeline proposat

```
                    corpusFJE/M3_instruments/{noticia,conte,...}.md
                              (font canònica, una per instrument)
                                          │
                                          ▼
                              build_skills.py (mineriaRAG)
                                          │
                ┌─────────────────────────┼─────────────────────────┐
                ▼                         ▼                         ▼
        corpusFJE/skills/        corpusFJE/rubriques/      corpusFJE/prompts/
        <nom>/SKILL.md          avaluacio/<nom>_<niv>.md   adapter/<nom>.md
        (LLM operador)          (docent avaluador)         (LLM adapter/generator)
                │                         │                         │
                ▼                         ▼                         ▼
              ATNE                    docents                   ATNE
        (consum runtime)          (consum aula)            (consum runtime)
```

### Tres derivats per skill

| Derivat | Veu | Format | Consumidor |
|---|---|---|---|
| **SKILL.md** | Imperativa | Markdown amb instructions + examples | LLM via Agent Skills (carrega quan és rellevant) |
| **rubrica_avaluacio_<niv>.md** | Criterial observable | Graella per nivell amb 3 bandes (Encara no / En procés / Aconseguit) + feedback orientatiu | Docent al moment de valorar producció d'alumnat |
| **prompt_adapter.md** | Instructiva amb gradació | Text per al prompt de l'LLM adaptador, parametritzat per nivell objectiu | ATNE quan rep tasca d'adaptació |

### Trigger del pipeline

GitHub Action al **corpusFJE**:
- On push a `M3_instruments/*.md`: regenera tots els derivats afectats.
- Validacions: linter de frontmatter, schema de metadades de cel·la, presència dels 6 nivells, integritat referencial entre passos.
- Output: PR automàtic al corpusFJE amb els derivats actualitzats per a revisió humana.

---

## 4. Schema de metadades de cel·la (validat amb pilot notícia)

Ja implementat a `_bootstrap_fase0/CANONIC_noticia/M3_instrument-escriure-noticia.md` (secció "Metadades de cel·la").

### Tipus de descriptor

| Tipus | Significat | Derivació automàtica |
|---|---|---|
| `countable` | Llindar quantitatiu verificable | regex + comptatge |
| `binary` | Compleix / no compleix | regex + presència/absència |
| `enumerable` | Verificable contra llista (ex: 5W) | comptatge per ítem de la llista |
| `qualitative` | Requereix judici | LLM-jutge amb prompt específic |
| `structural` | Requereix anàlisi sintàctica/discursiva | parser sintàctic o LLM amb regla |
| `cross_source` | Requereix text font per comparar | comparació semàntica (LLM o embeddings) |
| `metacognitive` | Descriptor de procés primera persona | derivat doble: alumne + registre docent |

### Camps obligatoris per cel·la

```yaml
metadades_dimensions:
  "<pas>.<dim>_<slug>":
    type: countable | binary | enumerable | qualitative | structural | cross_source | metacognitive
    requires_source_text: true | false | partial
    validation_hint: "<descripció operativa>"
```

### Implicacions per al pipeline

- Els tipus `countable`, `binary`, `enumerable`, `structural` són **automatitzables sense LLM** (regex + parser). Cost zero, deterministes.
- Els tipus `qualitative` requereixen **LLM-jutge**. Punt de variància entre execucions. Caldrà calibrar consistència.
- `cross_source` **bloqueja** la derivació si ATNE no conserva el text font al pipeline. ⚠️ Auditar arquitectura de dades de la sessió ATNE: actualment es conserva el font?
- `metacognitive` (Pas 8) requereix **dues sortides** al derivat avaluatiu (autoavaluació alumne + registre docent de la qualitat).

---

## 5. Registre de riscos i mitigacions

| Risc | Probabilitat | Impacte | Mitigació proposada |
|---|---|---|---|
| **Variància de l'LLM-jutge** entre execucions per descriptors `qualitative` | Alta | Alt | Calibrar amb 30 textos d'ancoratge per nivell; congelar prompts de jutge; conservar versionat |
| **Drift entre derivats i font** si algú edita un derivat manualment | Mitjana | Alt | Generats com a read-only amb header de warning; només es modifica la font |
| **`cross_source` no funcional** si ATNE no conserva el text font | ~~Alta~~ **RESOLT 2026-05-23** | ~~Alt~~ | ✅ **Auditoria feta**: text font preservat a 3 taules (`atne_drafts.text`, `atne_adaptations.original_text`, `history.original_text`). Font canònica recomanada per al pipeline: `history.original_text` (estable, permanent). Vegeu §9. |
| **Multilingüe** (post-pilot, castellà/francès/àrab): descriptors fixats al català | Mitjana | Alt | Schema preveu camp `language` i fitxer paral·lel `M3_instrument-noticia.es.md`; build_skills emet derivats per llengua |
| **Reedició del M\*.md trenca derivats existents** | Mitjana | Mitjà | Versionat semàntic (4.0.0-canonic actual); breaking changes a `major`; checksums al frontmatter dels derivats |
| **Tipus de descriptor no exhaustiu** (apareixen casos nous) | Mitjana | Baix | Llista de tipus oberta; revisió cada 6 mesos |

---

## 6. Decisió necessària a la reunió del 8 de juny

### Punts oberts a debatre

1. **On viu `build_skills.py`?**
   - Opció A: dins de `mineriaRAG/`, executat per GitHub Action al corpusFJE via dispatch.
   - Opció A': dins del **corpusFJE** mateix com a tooling local + GitHub Action.
   - Opció B: dins d'ATNE (no recomanat — acobla el productor amb un consumidor).
   - **Recomanació tècnica**: A' (autocontingut al corpusFJE, més simple operativament).

2. **Format del rubrica_avaluacio**: Markdown (com el pilot) o **JSON estructurat** parsejable per UI?
   - Recomanació: emetre **tots dos** (.md per humans + .json per UI futura).
   - Schema JSON pendent (vegeu memòria `parking-rubrica-json-pipeline`).

3. **Versionat de derivats**: heretat de la font o propi?
   - Recomanació: heretar `version:` + afegir `built_at:` + checksum SHA256 del M\*.md font.

4. **Calibratge de l'LLM-jutge per `qualitative`**: qui aporta els textos d'ancoratge?
   - Proposta: 5 textos per nivell MECR × 6 nivells = 30 textos per skill. Cap a 35 skills = 1.050 textos. **Inversió pedagògica significativa**. Cal pla.

5. **Schema dels camps de cel·la**: el meu pilot proposa `type`, `requires_source_text`, `validation_hint`. **Falten camps?**
   - Candidats: `feedback_pattern_<encara_no|en_proces|aconseguit>`, `pictogram_set` (per a pre-A1 i A1), `language`.

6. **Cas multilingüe**: la decisió pot esperar post-pilot o cal preveure-la al schema des d'avui?
   - Recomanació: preveure-la al schema (cost zero ara, cost alt després).

### Decisions ja preses (no a debatre)

- ✅ Una sola font canònica M\*.md per skill (no V1/V2/V3).
- ✅ Taula Pas × Dimensió × 6 nivells MECR+MALL com a estructura central.
- ✅ Pas N-1 = Criteris transversals (producte) · Pas N = Autoavaluació metacognitiva (procés).
- ✅ ATNE consumeix els derivats; no els genera. mineriaRAG gestiona la pujada coordinada al corpusFJE.
- ✅ Validat amb pilot **notícia** (vegeu `_bootstrap_fase0/CANONIC_noticia/`).

---

## 7. Material que ATNE porta a la reunió

A `_bootstrap_fase0/CANONIC_noticia/`:
- `M3_instrument-escriure-noticia.md` (font canònica v4.0.0 amb metadades de cel·la).
- `derivat_avaluacio_alumne_A1.md` (simulació manual del derivat avaluatiu per nivell A1, validat per NotebookLM).

A `docs/`:
- `briefing_md_canonic_skills.md` (briefing originari de mineriaRAG, autocontingut).
- `proposta_arquitectura_skill_pipeline_8juny.md` (aquest fitxer).

Material previst per portar (si es valida en sessió posterior):
- Derivat **prompt_adapter** simulat per a notícia A1 (vista C: ATNE adaptant).
- Esquema JSON-schema del format `rubrica_avaluacio.json`.

---

## 8. Auditoria preservació text font a ATNE (2026-05-23)

**Pregunta auditada**: ATNE preserva el text font (text original que el docent enganxa o adapta) de manera accessible al pipeline?

**Resultat**: ✅ **SÍ, en 3 taules paral·leles**.

| Taula | Camp | Quan s'escriu | Font de codi |
|---|---|---|---|
| `atne_drafts` | `text` | Quan el docent guarda esborrany Pas 2 | [routes/drafts.py:64,76](../routes/drafts.py) |
| `atne_adaptations` | `original_text` | Quan finalitza una adaptació amb biblioteca | [routes/adaptations.py:65](../routes/adaptations.py) |
| `history` | `original_text` | Registre permanent a l'historial (cada `/api/adapt`) | [server.py:2697,4788](../server.py) |

**Font canònica recomanada per a `build_skills.py`**: `history.original_text` (registre permanent, estable, indexat per `id` + `created_at`).

**Implicacions per al pipeline**:

1. ✅ `cross_source` (Fidelitat al text font 7.4) és **derivable**.
2. ✅ Es pot fer JOIN `atne_pilot_events.history_id` ↔ `history.id` per recuperar el text font des d'events granulars.
3. ⚠️ **3 fonts paral·leles** poden divergir si l'usuari edita el draft entre Pas 2 i Pas 3. Recomanació: usar **`history.original_text`** com a font de veritat per al pipeline d'avaluació (perquè reflecteix l'estat real en el moment de l'adaptació).
4. ⚠️ **Privacitat**: el text font pot contenir noms d'alumnes o dades sensibles. RLS (Row Level Security) ja aplicat a Supabase; el script `build_skills.py` ha d'usar `service_role_key` o respectar RLS. **No exportar textos fora de `@fje.edu` sense pseudonimització.**
5. ⚠️ **Mida**: textos llargs poden ser cars per a LLM-jutge. Caldrà tokenitzar o resumir abans de comparar. Decisió tècnica per a mineriaRAG.

**Risc cross_source: RESOLT.**

---

## 9. Resum executiu en 5 línies

1. **Una sola font M\*.md** per skill amb metadades de cel·la tipades.
2. **Tres derivats automàtics** per skill (SKILL.md, rubrica_avaluacio.md, prompt_adapter.md), un per consumidor.
3. **mineriaRAG implementa `build_skills.py` + GitHub Action al corpusFJE**; ATNE només consumeix.
4. **Variància LLM-jutge** i **`cross_source` sense text font** són els riscos principals — mitigacions proposades.
5. **6 punts oberts** per a la reunió del 8 de juny (vegeu §6); la majoria de decisions arquitectòniques ja són tancades pel pilot notícia.
