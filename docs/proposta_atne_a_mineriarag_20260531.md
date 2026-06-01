# Proposta ATNE → mineriaRAG · resposta consolidada 2026-05-31

> **De**: Claude (sessió ATNE) + Miquel
> **Per a**: Claude (sessió mineriaRAG)
> **Sobre**: decisions A i B del workflow d'auditoria + cobertura esquema rubrica.json + cross-check pedagògic translit
> **Estat**: llest per a la trobada de creuament d'esquema abans del freeze

---

## A · Estratègia de normalització dels M*.md

**Opció escollida**: **Opció 1 amb safety net**.

- Aplicar la plantilla universal mecànicament als 38 M*.md (lifting universal).
- Després, revisió manual ràpida (~1h) dels **5 skills <70%** de derivabilitat: `write-conte` (58%), `write-diari` (62%), `write-divulgatiu` (68%), `write-informe` (68%), `generate-pictogrames` (68%).
- **Total ~7h** en lloc de les ~6h de l'opció 1 pura — el +1h compensa el risc d'artefactes de la plantilla forçada als skills més pobres.

---

## B · Timing de revisió de l'esquema canònic rubrica.json

**Opció escollida**: **Opció 1 — extreu MD ara**.

- ATNE ja ha completat la pre-auditoria del seu pipeline (workflow `wf_18815504-a29`, 5 agents paral·lels, ~5min, 500k tokens).
- Tens els 4 punts crítics per a l'esquema a §C d'aquest document.
- Quan publiquis el MD de l'esquema → 30 min de creuament ATNE↔mineriaRAG → freeze.

**Per què no opció 3 (congelar amb la teva recomanació)**: l'esquema és el contracte. Un cop ATNE comenci A2 (refactor pipeline 37 skills), canviar l'esquema costa setmanes. La fase de revisió curta evita re-treball gros.

---

## C · Pre-auditoria pipeline ATNE — 4 punts crítics per a l'esquema

### C.1. Headers H2/H3 literals exigits a `format_output`

Sense això, el parser `parseAdaptedSections()` de `ui/atne/js/llm.js` classifica seccions a claus orfes i el Pas 3 no les renderitza. Cal definir explícitament els headers literals per a cada complement:

| Complement | Header obligatori | Sub-H3 obligatoris |
|---|---|---|
| Glossari | `## Glossari` | — |
| Esquema visual | `## Esquema visual` | — |
| Preguntes comprensió | `## Preguntes de comprensió` | `### Abans de llegir` · `### Durant la lectura` · `### Després de llegir` |
| Bastides | `## Bastides` | `### Bastides de lectura` · `### Bastides de resposta` (si producció activa) |
| Mapa conceptual | `## Mapa conceptual` | — |
| Mapa mental | `## Mapa mental` | — |
| Plantilla gènere | `## Plantilla de gènere` | — |
| Resum graduat | `## Resum graduat` | — |
| Cartes conversacionals | `## Cartes conversacionals` | — |
| Rúbriques | `## Rúbriques d'autoavaluació` | — |
| Activitats aprofundiment | `## Activitats d'aprofundiment` | — |
| Argumentació | `## Argumentació pedagògica` | format tipus card (3 estratègies de parser) |
| Notes auditoria | `## Notes d'auditoria` | — |

**Marcadors inline obligatoris** (NO secció ##): `[PICTO: terme_arasaac|terme_visible]` i `[IMATGE: <concepte_curt>]`. **Prohibir explícitament** `## Pictogrames` i `## Il·lustracions` com a secció separada — si el LLM les genera, el frontend les marca com a "inline confús" i les mou al final del text.

**Gaps UI detectats**: `tolc` i `traduccio_l1` són parsejats al backend però **NO tenen vista al frontend**. Decisió pendent: o (a) afegir vista UI o (b) eliminar-los del parser. ATNE proposa (a) post-pilot.

### C.2. `regex_check` per a taules markdown obligatòries

3 complements requereixen estructura tabular MD que el parser depèn:

- **Glossari**: pipes `| ... |` + separador `|---|---|`. Sense això, els toggles UX (CA · Pictograma · L1 · Translit) implementats com a part d'A3 queden inhàbils.
- **Rúbriques**: taula 3 o 4 nivells segons MECR (pre-A1 → checklist `- [ ]`; A1 → 3 nivells "Encara no | Sí | Sí, i alguna cosa més"; A2+ → escala FJE 4 nivells NA/AS/AN/AE).
- **Notes auditoria**: taula `| Aspecte | Original | Adaptat | Motiu |` o columnes similars. Parser custom a `pas3.html:3603-3642` depèn de pipes.

### C.3. `min/max numèrics` per MECR

Sense això, sobre-simplificació C1 i regressió cas titella. Camps necessaris:

- **MECR_MAX_WORDS** (paraules/frase): graduat per banda MECR. A B1+ s'emet **terra + sostre** alhora per evitar fragmentació A1/A2.
- **Glossari**: nombre per nivell (pre-A1: 3-5 termes · A1: 5-8 · A2: 8-10 · B1: 10-12 · B2: 12-15 · C1+: 15-18). **Sostre estricte A1**: max 2 termes + exclusió lèxic quotidià (mitja/botó/agulla/fil/retolador/llapis/paper/plat/got/casa/taula/porta). Si cap terme nou: nota "Aquest text no necessita glossari nou per al teu nivell" sense taula.
- **Esquema visual**: nombre de nodes (Emergent 2-3 · Inicial 3-4 · Funcional 4-6 · Estratègic 6-8).
- **Bastides resposta** — connectors permesos per MECR + iniciadors per MECR + paraules clau per MECR (taules ja documentades a M2_instruments-mediacio i M2_bastides-lectura-produccio).

### C.4. `case_overrides` per a 8 regles client-side ATNE

Aquestes regles viuen al codi ATNE (`complements-matriu.js`, `instruction_filter.py`, `prompt_builder.py`) sense contrapartida al M*.md. Cal **o pujar-les al canon** o **marcar-les com excepció pactada**:

1. **R1**: si MECR low (pre-A1/A1) + perfil amb VISUAL_NEED (disl/di/tdl/cat/tea/vis/discalculia) → afegeix pictogrames al default. **Recomanació**: pujar al canon M3 com a taula "condicions visuals × MECR". Justificat per M2_instruments-mediacio §230-236 ("1 complement visual fort a low + etapa inicial").
2. **R2**: si MECR low → treu mapa_conceptual + mapa_mental dels defaults. **Recomanació**: canonitzar a `case_overrides`. Ja coherent amb SKILL canon (mapa conceptual NO apropiat emergent/inicial).
3. **R3**: si dislèxia pura (NOT cat, NOT tdl) + MECR low → treu glossari. **Recomanació**: excepció pactada `verified:false`. Justificat per expertise reversal (M2_carrega-cognitiva §53-58) — però la composició concreta `disl AND NOT(cat) AND NOT(tdl)` és massa específica per al canon.
4. **R4**: si fallback (sense condicions) + MECR low + curs ∈ {1r Primària, 2n Primària} → defaults = `['preguntes_comprensio']` (glossari NO per defecte). **Recomanació**: canonitzar el llindar exacte (1r-2n) a M3_glossari §74. ATNE codi ja alineat (commit 31/05).
5. **A5**: si nouvingut detectat via `profile.conditions[key=nouvingut]` o `subvariables.nouvingut/l2` (NO només chip `cat` legacy) + L1 declarada → R4 NO aplica. **Recomanació**: pujar al canon la **lògica de detecció triple** (chips legacy + conditions modernes + subvariables). Justificat per Cummins/MALL (prioritat #1 nouvingut = accés a L2, no a contingut).
6. **R0 matriu 13 condicions × 12 complements**: la "matriu condició→complements" és font canon ATNE però viu a `ui/saber-ne.html §7` (UI, no canon). **Recomanació**: pujar al M2_instruments-mediacio com a taula canon explícita. `saber-ne.html` ha de ser mirall del canon, no la font.
7. **Sostre A1 glossari + exclusió quotidians** (cas titella): la nota "max 2 termes si text majoritàriament quotidià" + llista d'exclusions concretes (mitja/botó/agulla...) viu a `prompt_builder.py:1575-1626`. **Recomanació**: canonitzar a M3_glossari §Nombre amb la regla i la llista.
8. **Detecció alfabet no llatí per L1**: actualment a `instruction_filter.py:120-131` com a llista hardcoded `_NON_LATIN`. **Recomanació**: substituir per la taula canon que publicaràs al document de transliteració (16 L1s + GAPS amazic/mandinga/fula/soninké).

---

## D · Cross-check pedagògic transliteració (NotebookLM perfil `fje`)

Notebook consultat: **L'aula d'acollida a l'aula ordinària: transició** (12 fonts FJE incloent actes d'acollida 26.02.2025 dels centres Poble Sec, Sagrat Cor-Vic, Casp, Educar-me Primària).

### D.1. Les 4 decisions discutibles: TOTES VALIDADES

| Decisió | Veredicte | Raonament canon FJE |
|---|---|---|
| D-1 Àrab → ALA-LC simplificat | ✅ OK | Manté vàlua acadèmica; el docent ha de poder fer de model de llengua + vincle afectiu pronunciant el nom de l'alumne. Arabizi (números) seria críptic. |
| D-2 Xinès → Pinyin amb tons | ✅ OK (els tons són essencials) | Cura personalis = no desvirtuar la L1. Els alumnes xinesos assisteixen a escola de xinès els dissabtes (5h, confirmat a actes FJE); sense tons el glossari pot induir errors de significat. |
| D-3 Urdú → Roman Urdu informal | ✅ OK (tria encertada) | La relació amb la família és central al Pla d'Acollida FJE. WhatsApp/SMS de les famílies usa Roman Urdu — és pont real, no estàndard acadèmic aliè. |
| D-4 Hebreu → fonètica simplificada | ✅ OK | Oralitat prioritària + baix volum FJE → pragmatisme. |

### D.2. GAPS COBERTURA L1 confirmats pedagògicament

Les actes d'acollida FJE confirmen que **la teva taula de 16 L1s deixa fora L1s pedagògicament molt rellevants als centres FJE**:

- 🔴 **Amazic / Tamazight** (`zgh`): famílies marroquines amb L1 amazic, no àrab estàndard. Pedagogicament és **error tractar-les com a "àrab"** — fa invisible la identitat lingüística real. Alfabet variable: Tifinagh necessita translit; variant llatina pan-amaziga no.
- 🔴 **Mandinga** (`mnk`), **Fula** (`ff`), **Soninké/Sarahule** (`snk`): Àfrica Occidental, "pes pedagògic molt elevat" a centres FJE (Gàmbia, Senegal, Mali). Alfabet llatí → no necessiten translit, però cal entrada al perfil per al **reconeixement simbòlic**.
- 🟡 **Darija marroquí**: NO entrada separada — **variant** dialectal d'àrab (`ar-MA`). La translit segueix l'estàndard àrab.
- 🟡 **Persa / Farsi** (`fa`): entrada emergent. Probable ALA-LC simplificat.

### D.3. Política open-list (acordada)

Si arriba L1 NO llistada → marcar `unknown_L1` + LLM transliteri amb sistema "més proper" a la família lingüística + `verified:false` prioritat alta per a revisió docent. mineriaRAG afegeix la L1 a la taula canon **quan se'n detectin ≥3 casos reals** a la BD ATNE. Així la taula creix per **evidència real**, no per teoria.

### D.4. Termes científics moderns sense equivalent L1

Política acordada: deixar el **terme català** + nota "(sense equivalent directe)" com a default; el docent pot sobreescriure amb perífrasi. Raonament: **honestedat lingüística** — transliterar pseudo-fonèticament "fotosíntesi" en àrab és inútil i confús. Si la perífrasi és necessària, el docent (que coneix l'alumne) decideix.

---

## E · Cache de transliteracions: Supabase BD

**Decisió ATNE**: taula `atne_translits` a Supabase. **Esquema SQL preparat**:

```sql
CREATE TABLE IF NOT EXISTS atne_translits (
  id BIGSERIAL PRIMARY KEY,
  terme TEXT NOT NULL,                          -- terme en llengua de sortida (CA per defecte)
  l1 TEXT NOT NULL,                             -- 'àrab','xinès','urdú','ucraïnès'...
  transliteracio TEXT NOT NULL,
  verified BOOLEAN NOT NULL DEFAULT false,
  verified_by TEXT,                             -- email docent @fje.edu
  verified_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(terme, l1)
);
CREATE INDEX idx_atne_translits_lookup ON atne_translits(terme, l1);
ALTER TABLE atne_translits ENABLE ROW LEVEL SECURITY;
CREATE POLICY "atne_translits_anon_r" ON atne_translits FOR SELECT TO anon USING (true);
CREATE POLICY "atne_translits_anon_w" ON atne_translits FOR ALL TO anon USING (true) WITH CHECK (true);
```

**Raonament**: separació canon/operatiu.
- **corpusFJE = canon estable**: regles per L1 (ALA-LC àrab, Pinyin xinès, etc.).
- **BD = dada operativa acumulativa**: cache de termes verificats per docents.

Posar el cache al corpusFJE convertiria cada validació docent en un flux PR — no escala. La separació actual ja segueix el patró `atne_*` existent (drafts, history, pilot_events).

---

## F · Estat ATNE working tree post-sessió 31/05

Arxius modificats aquesta sessió:

- `ui/atne/js/complements-matriu.js`: A5 (excepció R4 nouvingut amb L1) + R4 corregit a 1r-2n (alineat M3_glossari §74). 4 tests Node passen.
- `ui/atne/pas3.html`: A3 complet (4 toggles glossari Pas 3) + heurística NON_LATIN_L1 alineada amb les 16 L1s mineriaRAG.
- `ui/saber-ne.html`: §Plurilingüisme ampliada amb taula d'estàndards translit + vàlvula docent verified:false→true + esment dels 4 toggles del Pas 3.
- `corpus/M3_translit_canon_proposta_20260531.md`: NOU — esborrany M3 per a ingesta canon (vegeu §D.3 i §C.4.8).

---

## G · Calendari proposat (recordatori)

| Setmana | mineriaRAG | ATNE |
|---|---|---|
| 31/05 - 06/06 | Esquema rubrica.json + plantilla universal + normalització M*.md | (esperar esquema; A3+A4+A5 ja fets) |
| 07/06 - 13/06 | Publicar 38 JSONs a corpusFJE | Creuament esquema (30 min) + ajustos finals abans freeze |
| 14/06 - 20/06 | Suport ATNE durant refactor | A2 inicial: refactor 2 pilots (glossari + bastides-lectura) + A6 (translit runtime) |
| 21/06 - 04/07 | Suport + iteració esquema si cal | A2 complet: refactor 35 skills restants |
| 05/07 - 11/07 | — | A7 (tests integració) |
| 12/07 - 18/07 | — | Pilot conjunt amb docent real + rollout |

---

## H · Decisions resoltes (resum executiu)

1. **Estratègia normalització**: opció 1 + safety net 5 skills <70% (~7h).
2. **Timing esquema**: opció 1 (extreu MD ara) + creuament 30 min.
3. **Cobertura L1**: open-list + ≥3 casos per ingestar L1 nova. Ampliar amb amazic/mandinga/fula/soninké/persa/darija pendent ratificació mineriaRAG.
4. **Termes científics sense equivalent L1**: default = català + nota "(sense equivalent directe)" + perífrasi opcional docent.
5. **4 decisions translit (D-1 a D-4)**: validades per NotebookLM ignasià.
6. **Cache translit**: Supabase BD (taula `atne_translits`), esquema preparat.
7. **PRIMARIA_INICIAL_CURSOS**: 1r-2n (no 1r-3r). Codi alineat.
8. **R4 + A5**: implementats + tests passen.
9. **A3 (4 toggles glossari)**: implementat.

---

*Document generat 2026-05-31 nit. Compila tota la feina ATNE de la sessió per a la trobada de creuament d'esquema amb mineriaRAG.*
