---
modul: M3
titol: "Generar il·lustracions"
tipus: instrument
categoria_principal: mediacio
categories_secundaries: []
descripcio: "Instrument per inserir marcadors d'il·lustracions IA al text adaptat. Format: [IMATGE: concepte curt en catala]. Backend: Wikimedia (llicencia lliure) → FLUX (generativa) → skip. 7 presets d'estil. Pre-A1/A1 davant del concepte com a anticipacio; A2+ al costat o dins del paragraf. Principi 'menys és mes': maxim 3-4 per document. Rubrica gradada 5 passos × 6 nivells MECR (pre-A1→C1)."
mecr_range: [pre_A1, A1, A2, B1, B2, C1]
agent_roles: [generator]
complement_key: illustracions
translanguaging: false
multimodal: true
moduls_relacionats: [M2, M3]
variables_configurables:
  fase_lectora: [logografica, alfabetica_emergent, alfabetica_fluida]
skill_meta: generate-illustracions@corpusFJE/skills/mediacio/generate-illustracions
review_status: pilot-fusio-8
version: 4.0.0-canonic
generat_at: 2026-05-26
actualitzat_at: 2026-05-26
notebooklm_review:
  data: 2026-05-26
  veredicte: si-amb-correccions-menors
  aplicades_des_d_inici: [patro-canonic-pilots-fase-a, aclariment-us-lectura-vs-produccio-C1, variabilitat-cardinal-passos-D3, modulacio-per-perfil-D1]
  aplicades_post_review: [b7-illustr-pas3-requires-source, b7-illustr-pas5-c1-na, b7-illustr-antisenyal-polisemics]
  comentari_key: "pas3-requires-source-text-si-especificitat-vs-font; pas5-c1-marcat-na; anti-senyals-conceptes-polisemics-afegit"
---

# Generar il·lustracions

## Descripció

El complement d'il·lustracions insereix marcadors `[IMATGE: concepte curt en catala]` al text adaptat perque el backend els resolgui en imatges. El backend prova tres vies en ordre: Wikimedia Commons (imatges reals amb llicencia lliure), FLUX.1-schnell (generacio IA), skip (si el concepte no és visualitzable). La il·lustració no decora — ancla conceptes que son difícils de descriure verbalment.

**Tipologia MALL**: Mediacio (suport multimodal cognitiu).
**HCL associada**: cap HCL productiva — el complement suporta l'acces i l'ancoratge conceptual del text.
**Principi rector**: menys és mes. Cada il·lustració afegeix carrega cognitiva de processament visual. A B2-C1, una il·lustració sense valor informatiu addicional distreu en lloc d'ancorar.
**Feature BETA**: qualitat no garantida; demora de 1-3 minuts per imatge; el docent sempre pot substituir o regenerar.

**Format del marcador:**
```
[IMATGE: concepte curt en catala]
```
- Delimitadors obligatoris: `[IMATGE:` a l'inici, `]` al final.
- Idioma: catala. El backend tradueix si cal.
- En linia propia, DAVANT del paragraf on s'introdueix el concepte (pre-A1/A1) o al costat (A2+).
- Longitud: 3-8 paraules. Concepte nuclear, no descripcio d'escena.
- Mai dins de llistes, taules, bastides, glossaris, pictogrames o altres complements.
- Mai incloure estil, paleta, viewpoint o enquadrament (el backend ho afegeix automaticament).

**Els 7 presets d'estil** (el docent tria al Pas 2; si no, el backend aplica el default per MECR + assignatura):

| Preset | Per a qui / quan |
|---|---|
| Aquarel·la storybook | Primaria, LF, nouvinguts, literatura, A1-A2 |
| Vectorial editorial pla | ESO+, humanitats, conceptes abstractes, B1+ |
| Isometric infografic | STEM, processos, sistemes, diagrames, A2+ |
| Icona minimalista | DUA Acces, vocabulari abstracte, glossari visual |
| Claymation plastilina | Primaria STEM ludic, infantil, A1-B1 |
| Escala de grisos (carbonet) | Historia, filosofia, impressio B/N, baixa visio |
| Fotografia documental | Natura, arquitectura, geografia, ciencia actual |

**Diferencia clau amb pictogrames:**
- **Pictogrames**: sistema AAC (emojis o ARASAAC), vocabulari, referencia lexica, TEA/CAA.
- **Il·lustracions**: ancoratge conceptual de processos, sistemes, llocs, escenes; no és AAC.

**Connexions MALL transversals:**
- *Imatge com a bastida d'acces (pre-A1/A1)*: l'alumne nouvingut que no coneix "fotosintesi" pot aprendre el concepte si veu la imatge PRIMER. La sequencia imatge → paraula és la logica de l'aprenentatge, no la del text.
- *Imatge com a ampliacio cognitiva (B1+)*: als nivells alts, la il·lustració no simplifica — complexifica. Un diagrama pot donar en un cop d'ull la informacio que requereix 3 paragraf de text. L'ampliacio és el valor afegit, no la simplificacio.
- *Preset com a coherencia de registre*: triar el preset adequat al context (aquarel·la per a primaria, vectorial per a ESO) és una decisio pedagogica sobre el registre visual. Un poema il·lustrat amb infografic isometric envia un missatge contradictori.

**Aclariment d'us — que descriu aquesta rubrica.**
Aquesta rubrica descriu el **complement d'il·lustracions generat per al text adaptat**. **No descriu la produccio autonoma de l'alumne**: el marcador el genera el LLM, la imatge la resol el backend. El registre d'us és del docent (observacio de si l'alumne usa el suport visual durant la lectura).

## Detecció

**Senyals docent** (quan activar el complement):
- Ha activat "Il·lustracions" al Pas 2.
- El text adaptat conte conceptes visuals que l'alumne pot no conèixer o que son difícils de representar verbalment.
- La materia és visual per naturalesa (ciencies naturals, historia, geografia, educacio artistica).

**Senyals alumne** (que indica que necessita el suport):
- Llegeix paraules sense imatge mental del concepte (mai ha vist un volca, una balena, una fabrica del s. XIX).
- El vocabulari esta desconnectat del significat referencial.

**Context favorable**:
- Ciencies naturals (ecosistemes, organs, processos biologics).
- Historia (monuments, escenes historiques, artefactes culturals).
- Politiques STEM: diagrames, infografies, mapes de conceptes visuals.
- Educacio artistica (tecniques visuals, estils, artistes).

**Anti-senyals** (quan NO activar):
- El text és abstracte i purament verbal (matematiques de calcul, filosofia) → cap il·lustració.
- El concepte és tècnic-microscopic (cel·lula, atom, enzim) → formular a escala macro o ometre.
- El concepte no te representacio visual clara → no posar el marcador.
- El concepte és polisemic sense context suficient al marcador → especificar el context al marcador (ex.: "banc" → `[IMATGE: banc de peixos]` o `[IMATGE: banc de fusta al parc]`; mai `[IMATGE: banc]`).
- Suport lexic sistematic → complement `pictogrames`.
- Esquema visual del contingut → complement `mapa-conceptual`.

## Modulació per nivell

| Pas | Dimensió | Pre-A1 Emergent | A1 Inicial | A2 Funcional | B1 Estratègic | B2 Acadèmic | C1 Crític |
|---|---|---|---|---|---|---|---|
| **1. Nombre d'il·lustracions** | Densitat | Maxim 4-5. Una per idea principal. Alta densitat justificada (text ≈ imatge). | 3-4 il·lustracions. Una per paragraf o per concepte clau. | 2-3 il·lustracions. Als punts de maxim ancoratge conceptual. | 1-2 il·lustracions als conceptes abstractes o processos clau. | 1-2 il·lustracions molt selectives (diagrama, proces, dada visual clau). | 0-1 il·lustració. Reservada per a diagrames o infografies que condensin dades. |
| **2. Posicio al text** | Anticipacio vs ancoratge | Imatge DAVANT de la paraula/frase que il·lustra. L'alumne veu la imatge PRIMER. Anticipacio visual. | Imatge immediatament DAVANT o AL COSTAT del concepte clau. | Imatge al costat del concepte que ancora, dins del paragraf. | Imatge al concepte abstracte o al proces que beneficia d'ancoratge visual. | Imatge estrategica: diagrama d'un proces, taula de dades, mapa conceptual visual. | Imatge de suport a l'argument: infografia, grafic, mapa. |
| **3. Especificitat del marcador** | Concretesa del concepte | Concepte molt concret i universal: "gat", "arbre", "pluja". 1-2 paraules. | Concepte concret: "cel·lula animal", "volca en erupcio". 1-3 paraules. | Concepte concret + context: "fotosintesi a fulla verda". 2-4 paraules. | Concepte especific del contingut: "cadena trofica marina", "cambra del parlament". | Concepte disciplinar: "diagrama de l'aparell respiratori", "mapa de la Revolucio Francesa". | Concepte complex: "infografia comparativa de sistemes politics", "grafic evolucio PIB". |
| **4. Preset d'estil** | Registre visual | Pictograma o il·lustració clara i simple. Sense elements distractors. | Il·lustracò o foto realista. Molt clara, sense text a la imatge. | Foto realista o il·lustracó educativa. Pot tenir etiquetes simples. | Diagrama o foto cientifica/geografica. Etiquetes disciplinars. | Diagrama, mapa, grafic. Llegenda si cal. | Infografia, grafic estadistic, mapa tematic. |
| **5. Autoavaluacio mediada** | Metacognicao | "He vist la imatge i he dit el que era." (oral, mediat per adult) | "He mirat la imatge i m'ha ajudat a entendre la paraula difícil." | "La imatge m'ha ajudat a entendre el proces o el concepte." | "He identificat quins conceptes necessitaven imatge i quins no." | "He usat les il·lustracions com a suport visual per a conceptes que no s'expliquen facilment amb paraules." | — (N/A: a C1 rarament es genera il·lustracó; si es genera, l'autoavaluacio és igual que B2) |

## Metadades de cel·la (per a `build_skills.py`)

**Tipus de descriptor:**
- `binary` — "compleix / no compleix".
- `qualitative` — requereix judici huma o LLM-jutge.
- `countable` — llindar quantitatiu verificable mecanicament.
- `structural` — requereix analisi sintatica o discursiva.
- `metacognitive` — descriptor de proces en primera persona.

| Pas / Dimensió | Tipus | requires_source_text | validation_hint |
|---|---|---|---|
| 1 Nombre d'il·lustracions | `countable` | no | comptar marcadors `[IMATGE:]` al text; verificar que esta dins del rang per nivell (pre-A1: ≤5; A1: ≤4; A2: ≤3; B1: ≤2; B2: ≤2; C1: ≤1) |
| 2 Posicio al text | `structural` | no | pre-A1/A1: verificar que el marcador precedeix el paragraf (linia propia DAVANT); A2+: verificar que no hi ha marcadors en linia propia aillats (han d'anar dins del context del paragraf) |
| 3 Especificitat del marcador | `qualitative` | **si** | LLM-jutge sobre si el concepte del marcador és concret i visualitzable (positiu) o vague i abstracte (negatiu); detectar marcadors massa genèrics ("[IMATGE: ciencies]"); cross_source: verificar que el concepte del marcador esta present i és central al text font |
| 4 Preset d'estil | `binary` | no | binary: el preset seleccionat és coherent amb el MECR i la materia (aquarel·la per primaria, vectorial per ESO+); si no s'especifica, el backend aplica el default adequat |
| 5 Autoavaluacio mediada | `metacognitive` | no | pre-A1: registre docent d'observacio; A1+: derivar a vista d'autoavaluacio alumne |

**Notes:**
- Format del marcador: `[IMATGE: concepte curt]`. L'absencia del delimitador de tancament `]` o un marcador dins d'una llista/taula son errors detectables per regex.
- Conceptes micro/abstractes: detectables per LLM-jutge. Si el marcador conté "cel·lula", "atom", "molecula", "justicia", "infinit" → alertar el docent per si vol ometre o reformular.
- Diferencia `[IMATGE:]` vs `[PICTO:]`: el backend processa separadament. Mai barrejar els dos sistemes en el mateix fragment per al mateix concepte.
- Pre-A1: si el text no te conceptes visualitzables, millor usar `pictogrames` que il·lustracions (mes ràpid i sense demora de generacio).

## Heurístiques docent

**H1 — "Pots imaginar-ho?" (seleccio del concepte).**
Per a cada concepte del text, pregunto: "Pots imaginar una imatge clara d'aquest concepte?" Si la resposta és si facilment (gat, arbre, volca), potser no cal il·lustrar — l'alumne ja te la imatge mental. Si la resposta és no (fotosintesi, revolucio industrial, democracia), la il·lustració pot ajudar. Si no hi ha cap imatge possible clara, no posar el marcador.

**H2 — Pre-A1: imatge DAVANT, sempre.**
L'ordre natural del text posa la imatge al costat o darrere del concepte. Per a pre-A1, cal invertir-ho: la imatge anticipa la paraula. L'alumne veu la imatge → el docent diu la paraula → l'alumne llegeix la paraula al text. Aquesta inversio és pedagogica, no estetica.

**H3 — El preset com a decisio pedagogica explicita.**
Quan el docent tria el preset, ho fa com a decisio conscious. Explicar a la classe per que s'ha triat aquarel·la per a un conte i vectorial per a un article de ciencies és una llico de multimodalitat i de registre visual: cada context te el seu codi visual.

**H4 — Menys és mes (A2+).**
Cada il·lustró afegeix carrega cognitiva. A B2-C1, una il·lustració sense valor informatiu addicional distreu en lloc d'ancorar. Proposo la regla: si puc explicar el concepte en dues frases sense la imatge i l'alumne ho entendra igualment, no posar el marcador.

**H5 — Il·lustracio vs pictograma: la pregunta de la funcio.**
Quan dubto entre usar pictograma o il·lustració, em pregunto: "Necessite suport lexic (aprendre la paraula) o suport conceptual (entendre el concepte)?" Suport lexic → pictograma. Suport conceptual (proces, sistema, lloc, escena) → il·lustracó.

## Fonts principals

- MALL (Model d'Aprenentatge de Llengues i Literacitat): multimodalitat, principi "imatge a l'esquerra", ancoratge visual ZDP.
- Mayer, R.E. (2009): *Multimedia Learning* — principi de contigüitat imatge-text; principi de redundancia; principi de coherencia (eliminar elements visuals sense valor informatiu).
- Regles de Lectura Facil ATNE: imatge davant del text, un element visual per concepte clau.
- Decret 175/2022 (curriculum Catalunya): competencia digital i multimodalitat com a dimensio de la comunicacio lingüística.
