---
modul: M3
titol: "Generar activitats d'aprofundiment"
tipus: instrument
categoria_principal: mediacio
categories_secundaries: []
descripcio: "Instrument per generar 2-3 activitats d'aprofundiment cognitiu post-lectura. Principi MALL: repte igualitari (adaptar l'acces, no el repte). Pre-A1: activitats fisiques/manipulatives cognitiu-exigents. 5 tipus: connexions interdisciplinars, pensament critic, recerca guiada, debat/reflexio, dimensio plurilingue (A2+, opcional). Rubrica gradada 5 passos x 6 nivells MECR (pre-A1->C1)."
mecr_range: [pre_A1, A1, A2, B1, B2, C1]
agent_roles: [generator]
complement_key: activitats_aprofundiment
translanguaging: true
multimodal: true
moduls_relacionats: [M2, M4]
variables_configurables:
  fase_lectora: [logografica, alfabetica_emergent, alfabetica_fluida]
skill_meta: generate-activitats-aprofundiment@corpusFJE/skills/mediacio/generate-activitats-aprofundiment
review_status: pilot-fusio-8
version: 4.0.0-canonic
generat_at: 2026-05-26
actualitzat_at: 2026-05-26
notebooklm_review:
  data: 2026-05-26
  veredicte: si-amb-correccions-menors
  aplicades_des_d_inici: [patro-canonic-pilots-fase-a, aclariment-us-lectura-vs-produccio-C1, variabilitat-cardinal-passos-D3, modulacio-per-perfil-D1]
  aplicades_post_review: [b9-act-c1-pas4-qualitative-afegit, b9-act-c2-pas5-c1-format-justificacio]
  comentari_key: "C1-pas4-binary+qualitative-contrast-metalinguistic-B2C1; C2-pas5-C1-format-justificacio-afegida"
---

# Generar activitats d'aprofundiment

## Descripció

Les activitats d'aprofundiment porten l'alumne **una passa més enllà del text**: connectar, qüestionar, investigar, argumentar. Són 2-3 activitats de repte cognitiu post-lectura. No son preguntes de comprensió literal; no son producció textual del gènere (bastides-produccio, plantilles-genere): son **extensió cognitiva** que activa els plànols inferencial i crític sobre el contingut treballat.

**Tipologia MALL**: Mediació (extensió cognitiva post-lectura).
**HCL principals**: Argumentar · Valorar críticament · Crear/Imaginar.
**HCL secundàries**: Investigar · Comparar · Connectar interdisciplinarment.
**5 tipus d'activitats**: connexions interdisciplinars · pensament crític ("i si...?") · recerca guiada · debat o reflexió argumentada · dimensió plurilingüe.
**Principi rector — Repte igualitari (MALL)**: adaptar l'**accés**, no el repte. Un alumne pre-A1 que ordena imatges per seqüència causal fa pensament d'alt nivell sense escriure. La dificultat cognitiva és equivalent per a tots els nivells; canvia la forma d'accedir-hi i de produir-la.

**Translanguaging — Dimensió plurilingüe (Pas 4)**: a A2+, una de les activitats pot invitar explícitament a comparar termes o conceptes entre L1 i el català. Aquesta activitat genera contingut en L1 (translanguaging actiu). La consigna **mai exposa cap alumne**: "Si coneixes la paraula en una altra llengua, comparteix-ho si vols."

**Pre-A1 SÍ (D6)**: les activitats d'aprofundiment son compatibles amb pre-A1 si son físiques o manipulatives i cognitiu-exigents. "Ordena les imatges de la cadena alimentària de la mes gran a la mes petita" és pensament crític. Cap escriptura autònoma.

**Diferència crítica amb complements propers:**
- `preguntes_comprensio`: comprensió del text (literal, inferencial, crític). **No va més enllà del text.**
- `activitats_aprofundiment`: extensió cognitiva post-lectura. **Va més enllà del text.**
- `bastides_produccio` / `plantilles_genere`: guia o bastida per a la producció textual del gènere.
- `cartes_conversacionals`: debat estructurat amb rols explícits i cartes de rol.

**Connexions MALL transversals:**
- *Repte igualitari*: el MALL advoca per activitats cognitivament exigents per a TOTS els alumnes, independentment del MECR. Un alumne nouvingut pre-A1 pot fer pensament de nivell superior si té accés multimodal al repte. Adaptar l'accés (llengua, format) no vol dir reduir el repte.
- *Consigna amb producte*: "Investiga sobre X" és una consigna vaga. "Busca 2 exemples de X a la teva vida quotidiana i explica per qué encaixen" és accionable. La consigna ha de dir sempre QUÈ cal fer i QUIN és el producte final (dibuix, llista, 1 frase, mapa, debat).
- *Dimensió plurilingüe com a recurs cognitiu*: la comparació entre L1 i L2 no és una concessió: és una activació de la xarxa conceptual completa de l'alumne. "Com ho anomenen en altres llengues?" obre la perspectiva conceptual i mostra la diversitat com a riquesa, no com a deficit.
- *Aprofundiment ≠ mes del mateix*: 3 preguntes literals de comprensió adicionals NO son aprofundiment. L'aprofundiment exigeix un salt qualitatiu en el nivell de pensament, no quantitatiu en el volum de preguntes.

**Aclariment d'ús — què descriu aquesta rúbrica.**
Aquesta rúbrica descriu les **activitats d'aprofundiment que ATNE genera per a l'alumne** (contingut post-lectura). **No descriu la producció autònoma de l'alumne ni l'avaluació del docent**: el docent observa si l'alumne completa l'activitat i si la seva resposta demostra aprofundiment real.
**Sub-granularitat dins de pre-A1**: `fase_lectora: logografica` → activitats totalment físiques i manipulatives (ordenar, tocar, dramatitzar). `fase_lectora: alfabetica_emergent` → activitats físiques + dibuix + 1-2 paraules escrites.

## Detecció

**Senyals docent** (quan activar el complement):
- Ha activat "Activitats d'aprofundiment" al Pas 2.
- Vol que l'alumne vagi més enllà del text: connectar, crear, qüestionar, investigar.
- La unitat treballa pensament crític o dimensió interdisciplinar.
- Hi ha alumnat amb AACC o perfil alta capacitat no diagnosticat que acaba molt aviat.

**Senyals alumne** (que indica que necessita les activitats):
- Ha comprès el text i pot fer més.
- Fa preguntes que van mes del text: "I per qué no fan...?" — curiositat que necessita canal.
- Acaba les tasques molt aviat i es distreu.
- Perfil AACC sense diagnòstic: comprensió ràpida, pensament lateral espontani.

**Context favorable**:
- Unitat TILC on el contingut disciplinar genera connexions interdisciplinars naturals.
- Text de ciències: activitats de recerca, observació, hipòtesi.
- Text literari: reflexió sobre valors, debat sobre les decisions dels personatges.
- Grup heterogeni: les activitats d'aprofundiment son l'opció per als qui acaben aviat.

**Anti-senyals** (quan NO activar):
- L'alumne no ha comprès el text → `preguntes_comprensio` primer.
- L'objectiu és produir un text del gènere → `bastides_produccio` o `plantilles_genere`.
- L'objectiu és un debat estructurat amb rols → `cartes_conversacionals`.
- El temps de sessió és molt limitat → 1 pregunta oral de pensament crític del docent basta.

## Modulació per nivell

| Pas | Dimensió | Pre-A1 Emergent | A1 Inicial | A2 Funcional | B1 Estratègic | B2 Acadèmic | C1 Crític |
|---|---|---|---|---|---|---|---|
| **1. Nombre i tipologia** | Quantitat i varietat | 1-2 activitats físiques o manipulatives. Una sola consigna visual. | 2 activitats concretes i visuals. Evitar debats abstractes. | 2-3 activitats. Combinació de connexió i "i si...?". | 2-3 activitats. Combinació de debat, connexió interdisciplinar i recerca guiada. | 2-3 activitats. Connexió entre matèries, contrast de fonts, intertextualitat. | 2-3 activitats. Reflexió crítica, hipòtesis contrafactuals, fonts contradictòries. |
| **2. Nivell cognitiu (Bloom)** | Profunditat de pensament | Manipulatiu: ordenar, tocar, moure, dramatitzar, dibuixar. No requereix abstracció lingüística. | Concret i visual. Màxim ancoratge en objectes o experiències familiars. Comparació simple. | Comparable i imaginatiu. "Com és X aquí vs. allà?" · "Qué passaria si...?". | Argumentatiu. Pren posicions i les justifica. Discrimina evidència de creença o opinió. | Analític. Contrastiu. Cerca relacions no evidents entre idees o camps disciplinars. | Crític. Metacognitiu. Detecta biaixos, dilemes ètics, limitacions del coneixement i de les fonts. |
| **3. Format de consigna** | Producte esperat explícit | Indicació física i visual: "Ordena les imatges de [X] a [Y]." Producte: dibuix, ordenació, dramatització. Cap escriptura autònoma. | Consigna molt concreta. Producte clar i assolible: 1 dibuix, 1 frase, 1 llista de 3 ítems. | Consigna accionable. Producte concret i delimitat: 1 fitxa, 1 mapa, 1 comparació de 3 elements. | Consigna accionable amb producte i temps estimat (15-30 min): 1 argument escrit, 1 recerca a 2 fonts. | Consigna amb producte complex: argumentació de 2-3 paràgrafs, recerca comparada, informe breu. | Consigna oberta amb criteris de qualitat del producte. L'alumne decideix el format i justifica la tria. |
| **4. Dimensió plurilingüe** | Ús de L1 com a recurs | No generar. | No generar. | Opcional: "Com es diu [terme clau] en altres llengues de l'aula? Comparteix-ho si vols." Cap exposició. | Opcional: comparació d'expressions o conceptes entre L1s dels alumnes si el text ho permet. | Opcional: contrast d'equivalents culturals o termes tècnics entre les llengues que coneixes. | Opcional: contrast metalingüístic i discursiu entre sistemes lingüístics i culturals. |
| **5. Autoavaluació mediada** | Metacognició | "He ordenat les imatges / he dibuixat." (oral, mediat per adult) | "He fet l'activitat. He escrit [producte]." | "He pensat més enllà del text. He fet la connexió o el 'i si...?'." | "He argumentat la meva postura i he usat evidència del text o d'una altra font." | "He analitzat les relacions entre matèries i he contrastat informació de fonts diverses." | "He detectat biaixos i limitacions del text. He qüestionat les afirmacions de l'autor amb arguments propis. He justificat la tria del format del meu producte segons l'objectiu de l'activitat." |

## Metadades de cel·la (per a `build_skills.py`)

**Tipus de descriptor:**
- `binary` — "compleix / no compleix".
- `qualitative` — requereix judici huma o LLM-jutge.
- `countable` — llindar quantitatiu verificable mecanicament.
- `structural` — requereix analisi sintatica o discursiva.
- `metacognitive` — descriptor de proces en primera persona.

| Pas / Dimensió | Tipus | requires_source_text | validation_hint |
|---|---|---|---|
| 1 Nombre i tipologia | `countable` + `qualitative` | no | countable: 1-2 activitats pre-A1/A1; 2-3 activitats A2+; qualitative: LLM-jutge sobre si les activitats son extensió cognitiva post-lectura (positiu) o preguntes de comprensió literal disfressades (negatiu — error crític) |
| 2 Nivell cognitiu (Bloom) | `qualitative` | **si** | LLM-jutge sobre si el nivell cognitiu demanat correspon al MECR declarat (ordenar/manipular pre-A1; argumentar B1+; detectar biaix C1); cross_source: verificar que el repte és sobre el contingut del text font (no sobre coneixements aliens) |
| 3 Format de consigna | `binary` + `qualitative` | no | binary: presencia de producte esperat explícit a la consigna (QUÈ cal fer + QUIN és el producte); qualitative: LLM-jutge sobre si la consigna és accionable o vaga ("investiga sobre X" sense producte = negatiu) |
| 4 Dimensió plurilingüe | `binary` + `qualitative` | no | binary: si present, verificar que la consigna inclou clàusula de voluntarietat ("si vols", "si en coneixes") detectada per regex; qualitative: LLM-jutge sobre la profunditat del contrast metalingüístic a B2-C1 (contrast d'equivalents culturals vs. simple traducció); si perfil nouvingut actiu i MECR A2+, marcar com a gap si absent (no error crític) |
| 5 Autoavaluació mediada | `metacognitive` | no | pre-A1: registre docent d'observació oral; A1+: derivar a vista d'autoavaluació de l'alumne |

**Notes:**
- Error crític mes freqüent: activitats d'aprofundiment = preguntes de comprensió literal addicionals. Detectar per LLM-jutge: si la resposta pot trobar-se directament al text sense extensió cognitiva → error.
- Consigna vaga: detectar "investiga sobre X" o "busca informació de X" sense producte explícit → alerta.
- Dimensió plurilingüe: la consigna ha de tenir la clàusula de voluntarietat ("si vols", "si en coneixes"). Detectar per regex.
- Pre-A1 + multimodal: les activitats han d'incloure una acció física visible (ordenar, dibuixar, dramatitzar). Si la consigna pre-A1 demana "escriu" o "explica" sense mediació oral → error.

## Heurístiques docent

**H1 — La prova del "mes del mateix".**
Llegeixo les activitats i em pregunto: "Son preguntes de comprensió formulades diferent?" Si la resposta pot trobar-se copiada del text, no son activitats d'aprofundiment. Les activitats d'aprofundiment requereixen que l'alumne generi nova informació, connexions o arguments que no estan al text.

**H2 — La consigna amb producte (l'antídot a la vaguetat).**
Una consigna bona té dos components: QUÈ cal fer ("compara", "argumenta", "busca", "ordena") i QUIN és el producte ("escriu 1 frase", "dibuixa un mapa", "prepara 2 arguments"). "Investiga sobre X" falla perquè no diu el producte. "Busca 2 exemples de X al teu entorn i explica en 1 frase per qué encaixen" és accionable.

**H3 — El repte cognitiu per a pre-A1 (Repte igualitari).**
La pregunta "Qué li passarà a [personatge] si fa X?" és pensament crític. L'alumne pre-A1 pot respondre assenyalant la imatge correcta, dramatitzant o dibuixant el resultat. El repte cognitiu no depèn de la producció escrita. Davant de pre-A1, em pregunto: "Quin producte físic o visual demostra que ha pensat?"

**H4 — La dimensió plurilingüe com a pont, no com a expositor.**
Quan proposo la dimensió plurilingüe, uso sempre la clàusula de voluntarietat: "Si coneixes la paraula en una altra llengua, comparteix-ho si vols." Mai "Com es diu en X?" (assumpció de llengua) ni "Qui sap com es diu en X?" (exposició pública). La voluntarietat no és opcional: és la condició per a un espai segur.

**H5 — 2-3 activitats, no 5-6.**
El principi MALL de "menys és mes" s'aplica també a les activitats d'aprofundiment. Prefereixo 2 activitats de qualitat cognitiva alta (que l'alumne ha de pensar de debò) que 5 activitats mecàniques. Si l'activitat pot completar-se en menys d'1 minut sense pensar, cal replantejar-la.

## Fonts principals

- MALL (Model d'Aprenentatge de Llengues i Literacitat): HCL Argumentar, extensió cognitiva, repte igualitari.
- Bloom, B.S. (1956, rev. Anderson & Krathwohl, 2001): *A Taxonomy for Learning, Teaching, and Assessing* — nivells superiors (analitzar, avaluar, crear).
- Cummins, J. (2000): *Language, Power and Pedagogy* — CALP, BICS, TOLC; multilingüisme com a recurs cognitiu.
- Decret 175/2022 (curriculum Catalunya): competencia personal i social, pensament crític, plurilingüisme.
