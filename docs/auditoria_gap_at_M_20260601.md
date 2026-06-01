# Auditoria gap_at_M — dedup directives Python (tasca 3 A2)

> **Data**: 2026-06-01 · **Mètode**: workflow d'auditoria (62 agents, fan-out per
> lots + verificació adversarial). · **Conclusió**: **0 directives segures
> d'eliminar amb el canon actual.** No es toca `instruction_catalog.py`.

## Pregunta de la tasca

El pla A2 §3.4.d demana eliminar d'`instruction_catalog.py` les directives amb
`gap_at_M=false` (les que dupliquen contingut JA consumit del canon), mantenint
les `gap_at_M=true` (que requereixen pujada prèvia al M*.md per mineriaRAG).

**Problema previ**: l'auditoria `gap_at_M` no existia com a dades al repo — el
pla la referenciava ("segons l'auditoria del workflow") però no s'havia fet mai.
Aquesta auditoria la produeix.

## Mètode

Workflow `audit-gap-at-m` (background, ~20 min, 62 agents):
1. **Classificar** (fan-out per lots de 13): per cada directiva, decidir
   `gap_at_M` amb cita del canon (`covered_by`) i confiança.
2. **Verificar** (adversarial): cada directiva marcada `gap_at_M=false`
   (candidata a eliminar) passa per un verificador escèptic que intenta REFUTAR
   que sigui segura eliminar, anant a la skill/corpus citada i comprovant si el
   pipeline ATNE la consumeix REALMENT en runtime.

Criteri conservador: davant el dubte, NO eliminar (perdre una directiva
pedagògica és pitjor que mantenir-ne una de duplicada).

## Resultat

| Mètrica | Valor |
|---|---|
| Directives classificades | 121 (de 122; `H-20b`, `H-41` fora del lotatge → classificades a part com a PERFIL/true) |
| `gap_at_M=true` (no eliminar, esperen mineriaRAG) | 71 |
| `gap_at_M=false` (candidates a eliminar) | 51 |
| **Candidates confirmades segures d'eliminar** | **0** |
| Candidates REFUTADES pel verificador | 51 (100%) |

**Totes les candidates a eliminar van ser refutades.** `confirma_eliminar`: 0.

## Per què 0 — el patró (verificat amb codi, no només LLM)

Les refutacions convergeixen en tres raons, totes vàlides:

1. **Corpus = referència estàtica, NO consumida en runtime.** La pauta existeix
   al M*.md (típicament `M3_lectura-facil-comunicacio-clara.md §1.2` o les taules
   "barrera→instruccions" dels M1), però `corpus_reader.py` **no carrega aquestes
   seccions**. Verificat deterministicament: `corpus_reader.load_corpus` no
   extreu ni la secció 1.2 (Ortotipografia/Sintaxi) ni les taules de prioritats
   M1 — només seccions MECR/càrrega-cognitiva/exemples. Per tant, eliminar la
   directiva Python deixaria la regla SENSE cap via d'arribar al prompt.

2. **Cobertura parcial.** El corpus diu QUÈ evitar (ex: "no majúscules", "no punt
   i coma") però NO l'alternativa positiva que la directiva prescriu (ex: "usa
   negreta", "si cita, introdueix amb 'L'autor diu:'"). L'LLM necessita el QUÈ
   FER, no només el QUÈ PROHIBIR.

3. **Gradació MECR / especialització per perfil absent al corpus.** La directiva
   Python gradua per nivell (pre-A1→B1) o s'activa només per a perfils concrets
   (nouvingut, TDL, TEA, discalcúlia…). El corpus dóna la pauta genèrica, sense
   gradació ni condicionalitat → el pipeline perdria la capacitat de diferenciar.

Aquest tercer punt és **coherent amb CLAUDE.md**: «editar un M1_*.md NO canvia el
prompt per a perfils — les instruccions de perfil venen del Python hardcoded». De
fet, **39/39 directives PERFIL** queden com a `gap_at_M=true`.

## Implicació pràctica

- **ATNE no elimina cap directiva ara.** `instruction_catalog.py` queda intacte.
- La dedup NO és impossible: és **bloquejada pel mateix motiu que R0 i T1/T2** —
  el canon encara no conté aquestes regles en forma **consumible en runtime**.
- **Camí per desbloquejar-la** (acció mineriaRAG, futura): per a una directiva
  passi a ser realment eliminable, el seu contingut (amb la gradació MECR i la
  condicionalitat per perfil) ha d'estar en una SKILL/rubrica.json que el
  pipeline JA carregui — no només al cos descriptiu d'un M*.md. Llavors es
  reaudita i s'elimina la duplicada.

## Distribució `gap_at_M=true` (71) per activació

- **PERFIL (39)**: A-21, A-27, B-13, D-06, D-06b, E-08, E-09, E-10, E-11, F-06,
  F-09, F-10, G-02, G-03, H-08..H-20, H-20b, H-29..H-41 (instruccions per
  condició — nucli hardcoded segons CLAUDE.md).
- **NIVELL (20)**: A-06..A-13, A-15, A-17, A-20, A-22..A-26, C-05, E-12, G-05, G-06.
- **SEMPRE (12)**: A-01..A-05, A-14, A-16, A-18, A-19, E-01, E-05, E-13.

## Candidates `gap_at_M=false` REFUTADES (51) — registre de traçabilitat

Cada fila: la cita del canon que semblava cobrir-la + el motiu pel qual NO és
segura d'eliminar. Quan mineriaRAG canonitzi alguna d'aquestes en forma
consumible, es podrà reauditar i eliminar.

<!-- taula generada des de docs/_audit_gap_result.json -->
| ID | Activació | covered_by (cita) | Per què NO s'elimina (refutació) |
|---|---|---|---|
| A-28 | NIVELL | corpus/external/corpusFJE/M3_lectura-facil-comunicacio-clara.md:141 — pauta 1.2  | La pauta UNE al corpus M3 (línea 141: 'Evitar oracions impersonals amb "cal", "convé", "s'ha de"...') és una REFERÈNCIA ESTÀTICA dins la documentació pedagògica |
| A-29 | NIVELL | corpus/external/corpusFJE/M3_lectura-facil-comunicacio-clara.md:126 — pauta 1.2  | M3_lectura-facil-comunicacio-clara.md:126 cobreix NOMÉS la substitució 'adverbis -ment' per 'molt + adjectiu' ('clarament'→'molt clar'). A-29 demanda reformulac |
| A-30 | PERFIL | corpus/external/corpusFJE/M3_lectura-facil-comunicacio-clara.md:128 — pauta 1.2  | M3_lectura-facil-comunicacio-clara.md:128 diu "Evitar paraules d'altres idiomes si no són d'ús comú en el context de l'usuari final" com a PAUTA GENERAL de Lect |
| A-31 | SEMPRE | corpus/external/corpusFJE/M3_lectura-facil-comunicacio-clara.md:110 — pauta Orto | M3_lectura-facil-comunicacio-clara.md:110 proposa només la prohibició de majúscules ("No escriure paraules ni frases en majúscules"), però MANCA la prescripció  |
| A-32 | SEMPRE | corpus/external/corpusFJE/M3_lectura-facil-comunicacio-clara.md:112-115 — pautes | M3_lectura-facil-comunicacio-clara.md (línies 112-115) cobreix les PROHIBICIONS ('No usar punt i coma', 'Evitar punts suspensius', 'No usar cometes'), però FALT |
| A-33 | SEMPRE | corpus/external/corpusFJE/M3_lectura-facil-comunicacio-clara.md:139 — pauta 'Evi | M3_lectura-facil-comunicacio-clara.md:139 cobreix la regla pedagògica bàsica ("Evitar la veu passiva... sempre és preferible la veu activa"), però: (1) no és ex |
| A-34 | SEMPRE | corpus/external/corpusFJE/M3_lectura-facil-comunicacio-clara.md:143 — pauta 'Evi | A-34 és una regla operativa específica a "DUA Accés" que diu: "una idea per frase, subjecte explícit sempre... REPETEIX el nom (no pronoms ambigus)". El canon M |
| A-35 | SEMPRE | corpus/external/corpusFJE/M3_lectura-facil-comunicacio-clara.md:113 + corpus/ext | La cita proposta menciona M3_lectura-facil-comunicacio-clara.md:113 que diu NO usar parèntesi, i M3_instrument-generar-glossari.md:68-70 que parla de criteris d |
| B-01 | SEMPRE | corpus/external/corpusFJE/M3_lectura-facil-comunicacio-clara.md:111-112 — pauta  | M3_lectura-facil-comunicacio-clara.md línies 111-112 i 152 cobreixen principis generals (separar idees per paràgrafs, agrupar temes), però NO especifiquen la gr |
| B-02 | SEMPRE | corpus/external/corpusFJE/M3_lectura-facil-comunicacio-clara.md:151 — pauta 'Tít | M3 (línies 151-152) especifica "Títols que anticipen el contingut" + "Agrupar informació en blocs", però: (1) NO cobreix l'especificació "Format pregunta" que B |
| B-03 | SEMPRE | corpus/external/corpusFJE/M3_lectura-facil-comunicacio-clara.md:151 — pauta 'Tít | M3:151 diu ÚNICAMENT «Títols que anticipen el contingut» (nivell de secció). B-03 demanda «Frase tòpic al principi de cada paràgraf». Aquestes són dues coses di |
| B-04 | NIVELL | corpus/external/corpusFJE/M3_lectura-facil-comunicacio-clara.md:153 — pauta 'Usa | La corpus M3_lectura-facil-comunicacio-clara.md (línea 153 + heurística H6, línies 407-436) estableix la pauta UNE genèrica: "Usar llistes si hi ha més de tres  |
| B-05 | NIVELL | corpus/external/corpusFJE/M3_lectura-facil-comunicacio-clara.md (linies 145-151) | CRÍTICA FALLIDA DE COBERTURA: La cita afirma que B-05 (Estructura deductiva: general→particular) está cubierta a corpus/external/corpusFJE/M3_lectura-facil-comu |
| B-06 | NIVELL | corpus/external/corpusFJE/M3_lectura-facil-comunicacio-clara.md (linies 149-150) | B-06 al pipeline ATNE diu 'Ordre cronològic per a processos i seqüències' sense especificar connectors temporals explícits. M3 (corpus/external/corpusFJE/M3_lec |
| B-07 | NIVELL | corpus/external/corpusFJE/skills/mediacio/generate-bastides-lectura/SKILL.md (li | B-07 és una instrucció de GENERACIÓ (inserir un resum anticipatiu com a paràgraf introductori del text adaptat). La skill generate-bastides-lectura (M3_instrume |
| B-08 | NIVELL | corpus/external/corpusFJE/skills/mediacio/generate-bastides-lectura/SKILL.md: Mo | B-08 instrueix l'LLM que insereixi resums finals **dins el text adaptat** al tanca cada secció. Les skills citades (generate-bastides-lectura linia 59/109/133,  |
| B-09 | NIVELL | corpus/external/corpusFJE/M3_lectura-facil-comunicacio-clara.md (linies 152-153) | Línia 153 de M3_lectura-facil-comunicacio-clara.md diu "Usar llistes si hi ha més de tres elements", però B-09 exigeix "Numera els passos i seqüències. Cada pas |
| B-10 | SEMPRE | corpus/external/corpusFJE/M3_lectura-facil-comunicacio-clara.md (linies 148-149) | corpus/external/corpusFJE/M3_lectura-facil-comunicacio-clara.md (línies 149-150) menciona "Cohesió i coherència" i "connectors temporals explícits: primer, desp |
| B-11 | NIVELL | corpus/external/corpusFJE/M3_lectura-facil-comunicacio-clara.md (linies 110-114) | M3 (línies 110-114) cobreix 'Punt i apart per separar idees. Cada idea nova comença en paràgraf nou' com a recomanació ortotipogràfica general de Lectura Fàcil. |
| B-14 | NIVELL | corpus/external/corpusFJE/M3_lectura-facil-comunicacio-clara.md (linies 152): Ll | M3 menciona taules com a recurs visual genèric dins del Pas 5 de Comunicació Clara (línies 79, 236: 'Incorpora taules, llistes, gràfics i elements visuals quan  |
| C-01 | NIVELL | corpus/external/corpusFJE/M2_carrega-cognitiva-adaptacio-textos.md + M2_factors- | M2_carrega-cognitiva-adaptacio-textos.md (línies 30-38) ofereix la teoria de Sweller + Miller sobre densitat conceptual (pre-A1/A1: 1-2 conceptes, A2: 2-3, B1:  |
| C-02 | NIVELL | corpus/external/corpusFJE/skills/mediacio/generate-bastides-lectura/SKILL.md + M | C-02 defineix "reforç immediat de cada concepte nou" com afegir DINS del text "exemple concret, connexió quotidiana, o suport visual" (banc_exhaustiu_instruccio |
| C-03 | SEMPRE | corpus/external/corpusFJE/M2_carrega-friccio-cognitiva.md + M3_lectura-facil-com | La cita a corpus/external/corpusFJE/M2_carrega-friccio-cognitiva.md + M3_lectura-facil-comunicacio-clara.md NO cobreix adequadament el contingut pedagogic de C- |
| C-04 | SEMPRE | corpus/external/corpusFJE/M2_carrega-cognitiva-adaptacio-textos.md (chunking, lí | M2_carrega-cognitiva-adaptacio-textos.md documenta teoria de Sweller i Miller sobre memòria de treball (línies 20-26, 32) però NO cobreix la REGLA OPERATIVA de  |
| C-06 | NIVELL | corpus/external/corpusFJE/skills/mediacio/generate-glossari/rubrica.json, M3_ins | C-06 al pipeline ATNE (matriu_tracabilitat.md línia 114): 'Analogies amb experiències quotidianes. NIVELL GRADUAT pre-A1→B1'. Definició: 'Analogia amb concepte  |
| C-08 | NIVELL | corpus/external/corpusFJE/skills/mediacio/generate-glossari/M3_instrument-genera | C-08 especifica 'els termes clau apareixen primer al glossari, després al text' — una directiva de SEQÜENCIACIÓ pedagògica basada en CLT pre-training (Sweller). |
| D-01 | COMPLEMENT | corpus/external/corpusFJE/skills/mediacio/generate-pictogrames/SKILL.md: '[PICTO | SKILL.md de generate-pictogrames (corpus/external/corpusFJE/skills/mediacio/generate-pictogrames/SKILL.md, linia 14) té agent_role: complements, cosa que **NO e |
| D-02 | COMPLEMENT | corpus/external/corpusFJE/skills/mediacio/generate-esquema-visual/SKILL.md: 'Lli | D-02 especifica: "Esquema de procés com a llista markdown amb sagnia (compatible amb renderer Mermaid SVG del frontend); NO fletxes Unicode ni ASCII-art." (inst |
| D-03 | COMPLEMENT | corpus/external/corpusFJE/skills/mediacio/generate-mapa-conceptual/SKILL.md: 'Ma | La cita és parcial i crea confusió. La SKILL `corpus/external/corpusFJE/skills/mediacio/generate-mapa-conceptual/SKILL.md` sí cobreix la tipologia MALL completa |
| E-02 | NIVELL | corpus/external/corpusFJE/skills/mediacio/generate-glossari/M3_instrument-genera | E-02 "Gradua la definició tècnica segons MECR" (instruction_catalog.py, lín. 645-655) és una instrucció INDEPENDENT que prescriu definicions integrades dins del |
| E-06 | SEMPRE | corpus/external/corpusFJE/skills/generes/write-conte/M3_genere-escriure-conte.md | E-06 és una instrucció SEMPRE (universal, s'aplica a TOTS els texts de TOTS els gèneres). La citació cobreix NOMÉS la causalitat narrativa dins el M3 del conte  |
| E-07 | NIVELL | corpus/external/corpusFJE/skills/mediacio/generate-glossari/M3_instrument-genera | E-07 ('Un exemple concret per concepte abstracte', NIVELL GRADUAT pre-A1→B1) és una INSTRUCCIÓ DEL PIPELINE ATNE que s'aplica al cos del TEXT ADAPTAT, mentre qu |
| G-01 | PERFIL | corpus/external/corpusFJE/skills/mediacio/generate-glossari/SKILL.md — 'Inclou u | La skill 'generate-glossari' (SKILL.md línies 62-64 i 91-94) descriu CÓMO GENERAR glossaris bilingües amb L1 en alfabet original — és una rúbrica de QUALITAT pe |
| G-07 | PERFIL | M1_alumnat-nouvingut.md (sec. 4, barreres lingüístiques, inferència); M3_TILC-ll | M1_alumnat-nouvingut.md secció 4 (Heurístiques) parla de context BICS/CALP però no conté instruccions operatives sobre marcar estructures discursives. M3_TILC-l |
| G-08 | NIVELL | M3_lectura-facil-comunicacio-clara.md, secció 6 "pre-A1 Emergent" (linies 493-50 | G-08 és una instrucció ACTIVA del pipeline ATNE (instruction_catalog.py, línies 789-795) que es transmet a l'LLM via instruction_filter.get_instructions(). El M |
| G-09 | NIVELL | M3_lectura-facil-comunicacio-clara.md, secció 6 "pre-A1 Emergent" (linies 498-49 | M3_lectura-facil-comunicacio-clara.md secció 6 "pre-A1 Emergent" (línies 493-508) cobreix descriptivament el nivell MECR pre-A1 (frases 3-5 paraules, vocabulari |
| G-10 | PERFIL | M3_TILC-llengua-i-continguts.md (paragrafs sobre TILC i CALP, línies 13-15, 59): | M3_TILC-llengua-i-continguts.md (linies 13, 59-62, 97) menciona TILC, CALP/BICS, bastides i glossaris bilingües, però NO prescriu explícitament 'NO reduir llarg |
| H-01 | PERFIL | M1_alumnat-TEA.md (taula prioritats línies 279-284): 'H-01 (estructura predictib | M1_alumnat-TEA.md (línies 271 i 281) cita H-01 com a descriptiu al corpus, però corpus_reader.py (línea 107) busca secció "## 6. INSTRUCCIONS D'ADAPTACIÓ TEXTUA |
| H-02 | PERFIL | M1_alumnat-TEA.md (taula prioritats línies 281): 'H-02 (zero implicitura)' citat | M1_alumnat-TEA.md cita H-02 (zero implicitura) a la taula prioritats (línia 281) i ofereix l'exemple ABANS→DESPRÉS (línies 289-300) amb expressions figurades tr |
| H-03 | PERFIL | M1_alumnat-TEA.md (taula prioritats línies 282): 'H-03 (anticipació canvis)' cit | La taula de M1_alumnat-TEA.md (línea 282) cita "H-03 (anticipació canvis)" com a instrucció prioritat 2a, però és només una REFERÈNCIA al catàleg de `instructio |
| H-04 | PERFIL | M1_TDAH.md (taula prioritats línies 218): 'H-04 (micro-blocs amb objectiu)' cita | M1_TDAH.md (línies 204-229) cita H-04 i proporciona exemple pedagògic ABANS→DESPRÉS que il·lustra micro-blocs amb objectiu ('Secció X de Y'). Però M1_TDAH.md NO |
| H-05 | PERFIL | M1_TDAH.md (taula prioritats línies 220): 'H-05 (retroalimentació visual)' citat | **CRÍTICA TROUVADA DE DUPLICACIÓ PARCIAL, NO TOTAL:**  M1_TDAH.md (línies 204-206) diferencia clarament: - **Prioritat 1a (ATENCIÓ):** B-13 = "Indicadors de pro |
| H-06 | PERFIL | M1_TDAH.md (taula prioritats línies 218): 'H-06 (variació dins text)' citat expl | M1_TDAH.md (línea 218) cita H-06 a la taula barrera→instruccions, però aquesta cita és DOCUMENTACIÓ INTERNA, no cobertura funcional. El pipeline ATNE no consume |
| H-07 | PERFIL | M1_dislexia-dificultats-lectores.md (taula prioritats línies 281): 'H-07 (evitar | M1_dislexia.md (línea 281) cita H-07 dins la taula "Mapa barrera → instruccions" com a prioritat 1a (descodificació). PERÒ aquesta taula és només documentació i |
| H-21 | PERFIL | corpus/external/corpusFJE/M1_discapacitat-visual.md — Secció 'Barreres d'aprenen | M1_discapacitat-visual.md COBREIX PEDAGÒGICA però NO GENERATIVA. 1) «Verbalització sistemàtica» (§ Necessitats prioritàries, línea 6): «El docent ha de verbalit |
| H-22 | PERFIL | corpus/external/corpusFJE/M1_dislexia-dificultats-lectores.md — Secció 'Barrera  | La cita al M1_dislexia (línies 264-274, secció "Barrera nuclear") diu textualment "Evita encadenar prefixos i sufixos", però aquesta és METADA DE CORPUS (text d |
| H-23 | PERFIL | corpus/external/corpusFJE/M1_TDL-trastorn-llenguatge.md — Variables configurable | M1_TDL-trastorn-llenguatge.md (línes 11-18) DECLARA la variable `modalitat: [comprensiu, expressiu, mixt]` però NO CONSUM a través de cap instrucció explícita d |
| H-24 | PERFIL | corpus/external/corpusFJE/M1_TDL-trastorn-llenguatge.md — Variables configurable | H-24 (TDL semàntica: vocabulari mínim funcional) NO està suficientment cobert per M1_TDL-trastorn-llenguatge.md. (1) M1 especifica 'Vocabulari d'alta freqüència |
| H-25 | PERFIL | corpus/external/corpusFJE/M1_TDL-trastorn-llenguatge.md — Variables 'morfosintax | El corpus M1_TDL-trastorn-llenguatge.md (lines 297-303) cita només H-16, H-17, H-13, H-26 al mapa barrera, però NO H-25. La variable `morfosintaxi=true` al corp |
| H-26 | PERFIL | corpus/external/corpusFJE/M1_TDL-trastorn-llenguatge.md — Variables 'pragmatica= | M1_TDL-trastorn-llenguatge.md línies 33-39 cobreix parcialment: 'pragmatica=true' → 'Evitar consignes amb llenguatge figurat o ambigu, explicitar el context com |
| H-27 | PERFIL | corpus/external/corpusFJE/M1_discalculia.md — Secció 'Manifestacions per etapa'  | M1_discalculia.md (corpus/external/corpusFJE/) documenta els PRINCIPIS teòrics: Secció "Necessitats prioritàries" (línies 124-131) descriu 'Instrucció basada en |
| H-28 | PERFIL | corpus/external/corpusFJE/M1_discalculia.md — Secció 'Progressió CPA': 'no s'ha  | H-28 és una instrucció de RUNTIME de format textual: 'desglossa qualsevol seqüència numèrica o procediment pas a pas, sense saltar-ne cap' (instruction_catalog. |

## Artefactes

- `docs/_audit_gap_result.json` — resultat estructurat complet del workflow
  (classificació + veredictes per a les 121 directives).
- `docs/_catalog_dump_a2.json` — dump del catàleg auditat (input del workflow).
- Workflow runId: `wf_0ccc6c28-cf7`.
