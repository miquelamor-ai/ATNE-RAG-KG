---
modul: M3
titol: "Generar bastides de producció"
tipus: instrument
categoria_principal: mediacio
categories_secundaries: []
descripcio: "Instrument de mediació cognitiva per guiar la producció textual de l'alumne en 3 blocs: (A) base d'orientació disciplinar GPS del gènere, (B) catàleg de recursos lingüístics connectors MECR + iniciadors HCL, (C) pauta d'interrogació checklist autoavaluació. S'activa nomes si hi ha producció activa (preguntes-comprensio o activitats-aprofundiment). No s'adapta a pre-A1 (zero escriptura autonoma). Rúbrica gradada 4 passos × 5 nivells MECR (A1→C1)."
mecr_range: [A1, A2, B1, B2, C1]
agent_roles: [generator]
complement_key: bastides
translanguaging: false
multimodal: false
moduls_relacionats: [M2, M3]
variables_configurables:
  fase_lectora: [alfabetica_emergent, alfabetica_fluida]
skill_meta: generate-bastides-produccio@corpusFJE/skills/mediacio/generate-bastides-produccio
review_status: pilot-fusio-8
version: 4.0.0-canonic
generat_at: 2026-05-26
actualitzat_at: 2026-05-26
notebooklm_review:
  data: 2026-05-26
  veredicte: si-amb-correccions-menors
  aplicades_des_d_inici: [patro-canonic-pilots-fase-a, aclariment-us-lectura-vs-produccio-C1, variabilitat-cardinal-passos-D3, modulacio-per-perfil-D1]
  aplicades_post_review: [b8-bastides-prod-pas3-a2-exemple-destinatari, b8-bastides-prod-pas2-hint-millorat]
  comentari_key: "C1-translanguaging-false-rebutjat-correcte; pas3-A2-exemple-destinatari-afegit; pas2-hint-llista-tancada-connectors-MECR"
---

# Generar bastides de producció

## Descripció

Les bastides de producció guien el procés d'escriptura de l'alumne en tres blocs complementaris: **(A) base d'orientació**, **(B) catàleg de recursos** i **(C) pauta d'interrogació**. Constitueixen el GPS de la producció textual: mostren a l'alumne el camí per construir el text del gènere treballat, pas a pas i amb els recursos lingüístics del seu nivell MECR.

**Tipologia MALL**: Mediació cognitiva (bastida de producció).
**HCL associada**: cap HCL pròpia — el complement suporta la HCL productiva del gènere actiu (Narrar, Argumentar, Descriure, Explicar, etc.). El Bloc B adapta els iniciadors a la HCL del gènere.
**Activació condicional**: ÚNICAMENT si hi ha producció activa al Pas 2. Si el docent activa "bastides" sense activar `preguntes_comprensio` o `activitats_aprofundiment`, aquest complement NO genera res. La senyera: "Sense producció no hi ha bastida de producció."
**Principi rector**: el Bloc A SEMPRE és disciplinar i específic del gènere i la matèria. Mai "introduccio / cos / conclusio". Una base d'orientació genèrica és pitjor que cap: desorientació disfressada d'estructura.

**No s'adapta a pre-A1 (D6)**: zero escriptura autònoma a fase logografica i alfabetica emergent primerenca. La producció requereix tenir la mecànica de la frase interioritzada com a mínim en la seva forma rudimentaria. A pre-A1 no hi ha cap bloc generat; si el docent activa el complement, el backend el salta silenciosament.

**Diferència crítica amb bastides-lectura:**
- `bastides-lectura`: sempre actiu quan el docent activa "bastides"; guia el PROCÉS LECTOR.
- `bastides-produccio`: condicional (requereix producció activa); guia el PROCÉS D'ESCRIPTURA.
- Els dos complements son ortogonals i complementaris: mai duplicar contingut entre ells.

**Connexions MALL transversals:**
- *Base d'orientació com a GPS disciplinar*: el Bloc A no és un índex de seccions sinó el procediment mental expert per a aquell gènere i aquella matèria. Per a una crònica de ciències: "1. Quan, on i qui. 2. Quin fenomen. 3. Quines causes. 4. Quines conseqüències." Per a un assaig de filosofia: "1. Tesi pròpia. 2. Evidència 1 i refutació. 3. Evidència 2. 4. Conclusió-implicació." El gènere i la matèria determinen els passos.
- *Catàleg de recursos com a vocabulari actiu*: els iniciadors del Bloc B no son per llegir — son per usar mentre s'escriu. Menys iniciadors (2-3 per HCL) és millor que una llista inabastable. L'alumne ha de triar, no copiar mecànicament.
- *Pauta d'interrogació com a metaregulació*: el Bloc C desplaça la regulació externa del docent cap a la regulació interna de l'alumne. La pregunta "He justificat amb exemples del text?" activa el monitoratge metacognitiu que és el preludi de l'escriptura autònoma.
- *Bastida retirable (ZDP)*: el Bloc A es retira quan l'alumne ha internalitzat l'estructura del gènere. El Bloc B es retira quan l'alumne usa els connectors sense necessitat de consulta. El Bloc C es retira quan l'alumne s'autoavaluà espontàniament. La bastida té vocació d'extingir-se.

**Aclariment d'ús — què descriu aquesta rúbrica.**
Aquesta rúbrica descriu les **bastides que ATNE genera per orientar la producció escrita de l'alumne** (PRODUCCIÓ). **No descriu la producció autònoma de l'alumne ni l'avaluació del docent**: el docent observa si l'alumne usa la bastida com a suport i si la seva producció millorat amb ella.
**Sub-granularitat dins de A1**: es treballa amb `fase_lectora: alfabetica_emergent` (frases simples, bastida mínima) i `alfabetica_fluida` (frases completes, bastida plena).

## Detecció

**Senyals docent** (quan activar el complement):
- Ha activat "Bastides" al Pas 2 i ha activat almenys un complement de producció.
- L'alumnat escriu sense saber per on començar (full en blanc).
- La producció és correcta en contingut però desorganitzada estructuralment.
- Primera exposició a un gènere nou en el context TILC.

**Senyals alumne** (que indica que necessita el suport):
- Mira el full en blanc durant molt de temps sense escriure.
- Comença a escriure i el resultat és un caos de frases sense estructura.
- Usa "perquè és molt important" com a única justificació de tot.
- No usa vocabulari disciplinar tot i haver-lo treballat.

**Context favorable**:
- Unitat TILC: alumnat nouvingut que coneix el contingut però no sap com estructurar-lo en català.
- Primer cicle de treball d'un gènere nou (retira les bastides al 3r cicle).
- Alumnat amb TDAH o dificultats executives que necessita l'estructura explícita com a punt de partida.

**Anti-senyals** (quan NO activar):
- No hi ha producció activa al Pas 2 → el complement salta silenciosament.
- L'alumne ja domina l'estructura del gènere → la bastida pot limitar la creativitat i la fluència.
- Tasca de producció lliure o creativa sense restriccions de gènere → `plantilles-genere` amb forats mínims.
- Rúbrica avaluativa per al docent → `rubriques`.
- El text és molt curt i la producció és trivial → un parell de preguntes guia orals del docent basten.

## Modulació per nivell

| Pas | Dimensió | A1 Inicial | A2 Funcional | B1 Estratègic | B2 Acadèmic | C1 Crític |
|---|---|---|---|---|---|---|
| **1. Bloc A — Base d'orientació** | GPS disciplinar | 2-3 passos molt concrets amb terminologia disciplinar de la matèria. Cada pas = 1 frase imperativa breu. | 3-4 passos + terminologia disciplinar específica. Cada pas indica QUÈ fer i AMB QUÈ. | Raonament disciplinar explícit: hipòtesi, evidència, causa, efecte. Vocabulari CALP del camp. | Superestructura completa del gènere amb lèxic CALP i indicadors de qualitat per secció. | Contrast de fonts, biaix autorial, intertextualitat. El GPS inclou indicadors de rigor crític. |
| **2. Bloc B — Catàleg de recursos** | Connectors + iniciadors HCL | 1 iniciador per HCL principal del gènere. Connectors: *i, però, perquè*. Llista curta (max 5 ítems). | 2-3 iniciadors per HCL. Connectors: + *primer, llavors, per tant*. Connectors de causa-efecte. | Iniciadors inferencials i causals. Connectors: + *ja que, en canvi, tot i que*. Iniciadors de contrast. | Iniciadors CALP argumentals. Connectors: + *no obstant, atès que, en conseqüència* (NOMES a B2+). | Iniciadors dialèctics i retòrics. Connectors de concessió i contrast complexos. |
| **3. Bloc C — Pauta d'interrogació** | Checklist d'autoavaluació | Cap pauta a A1: la bastida és el Bloc A i B. | 2-3 ítems simples vinculats al gènere i la tasca concreta. Com a mínim un ítem sobre el destinatari o el propòsit (ex.: "A qui escric? He posat el nom del personatge?"). | 4-5 ítems específics del gènere. Vinculats als criteris d'avaluació si estan disponibles. | Criteris d'avaluació específics amb indicadors observables. Inclou criteris de rigor disciplinar. | Reflexió metacognitiva sobre fiabilitat de les fonts, biaix i coherència interna de l'argument. |
| **4. Autoavaluació mediada** | Metacognició | "He seguit els passos de la bastida per escriure el meu text." | "He usat la bastida per estructurar el meu text. He completat el checklist." | "He seguit la base d'orientació i he usat els iniciadors per construir el meu argument." | "He usat la pauta d'interrogació per revisar que el meu text compleix els criteris del gènere." | "He comprovat que les meves fonts son fiables i que el meu argument és coherent i honest." |

## Metadades de cel·la (per a `build_skills.py`)

**Tipus de descriptor:**
- `binary` — "compleix / no compleix".
- `qualitative` — requereix judici huma o LLM-jutge.
- `countable` — llindar quantitatiu verificable mecanicament.
- `structural` — requereix analisi sintatica o discursiva.
- `metacognitive` — descriptor de proces en primera persona.

| Pas / Dimensió | Tipus | requires_source_text | validation_hint |
|---|---|---|---|
| 1 Bloc A — Base d'orientació | `qualitative` | **si** | LLM-jutge: la base d'orientació és específica del gènere i la matèria (positiu) o genèrica "introduccio/cos/conclusio" (negatiu); cross_source: verificar que els passos son coherents amb el gènere declarat al text font |
| 2 Bloc B — Catàleg de recursos | `binary` + `qualitative` | no | binary: connectors del nivell MECR exacte presents (detectar per regex connectors d'un nivell superior contra la llista tancada per nivell: A1={i,però,perquè}, A2+={primer,llavors,per tant}, B1+={ja que,en canvi,tot i que}, B2+={no obstant,atès que,tanmateix}); qualitative: LLM-jutge sobre pertinença dels iniciadors HCL al gènere actiu |
| 3 Bloc C — Pauta d'interrogació | `binary` + `qualitative` | **si** | binary: presencia de checklist a A2+ i absencia a A1; qualitative: LLM-jutge sobre especificitat de la pauta (vinculada al gènere i la tasca concreta vs genèrica); cross_source: ítems de la pauta coherents amb el gènere del text |
| 4 Autoavaluació mediada | `metacognitive` | no | A1: registre docent d'observació; A2+: derivar a vista d'autoavaluació de l'alumne |

**Notes:**
- Activació condicional: el backend SALT el complement si no hi ha producció activa. Documentar al log de generació.
- Bloc A genèric: detectar "introduccio / cos / conclusio" per regex + LLM-jutge. És l'error mes freqüent i el de major impacte pedagògic.
- Connectors de nivell superior: `no obstant`, `atès que`, `tanmateix` son NOMES B2+. Detectar per regex si apareixen a A1-B1.
- Interacció intra-pipeline: si `bastides` i `preguntes_comprensio` son actius simultàniament, les bastides de producció llegeixen l'output de preguntes_comprensio i generen ítems ortogonals (no duplicats). Patró cross_source intra-pipeline confirmat al corpus-spec v2.7 (mineriaRAG).

## Heurístiques docent

**H1 — El test de la matèria (Bloc A).**
Llegeixo la base d'orientació i em pregunto: "Podria servir per a qualsevol text de qualsevol matèria?" Si la resposta és sí, cal tornar a escriure-la. Ha de ser específica del gènere i la matèria: "Per a una crònica de biologia: 1. Quan i on va passar el fenomen. 2. Quin organisme/procés. 3. Quines causes concretes. 4. Quines conseqüències observades." Això no val per a una crònica de historia.

**H2 — El Bloc B com a termòmetre del nivell.**
Reviso ràpidament els connectors que usa l'alumne: si tots els arguments comencen amb "perquè" o "però" → A1-A2. Si varia entre "en primer lloc", "per tant" → B1. Si usa "tanmateix", "no obstant" → B2. Si el Bloc B dona connectors del nivell correcte, l'alumne té un termòmetre lingüístic de la seva ZDP.

**H3 — El Bloc C com a conversa interior.**
Proposo que l'alumne completi el Bloc C EN VEU ALTA en parella ABANS de lliurar el text. El company és el "lector intern": "Has posat quins personatges? Sí. Has posat per que passa el conflicte? No, torna-hi." L'externalitzar la pauta converteix un exercici solitari en una conversa metacognitiva.

**H4 — Bastida que es retira progressivament.**
Introdueixo les bastides les primeres 2-3 sessions del gènere i progressivament elimino ítems que l'alumne ja fa sol. Semana 1: Bloc A complet + Bloc B. Semana 3: Bloc B + Bloc C (l'alumne ja recorda l'estructura). Semana 5: Bloc C sol (l'alumne ja usa connectors autònomament). Una bastida que no es retira es converteix en dependència.

**H5 — "Sense producció, sense bastida".**
Quan el docent activa "bastides" però oblida activar preguntes o activitats, el complement salta. Li explico explícitament: la bastida de producció nomes existeix si hi ha alguna cosa a produir. Si el text no té tasca de producció associada, la bastida es limita a les bastides de lectura.

## Fonts principals

- MALL (Model d'Aprenentatge de Llengues i Literacitat): base d'orientació, GPS disciplinar, HCL, connectors per nivell.
- Vygotsky, L.S. (1978): *Mind in Society* — zona de desenvolupament proper; bastida com a suport temporal que es retira progressivament.
- Wood, D., Bruner, J.S. & Ross, G. (1976): "The role of tutoring in problem solving" — concepte de scaffolding educatiu.
- Gibbons, P. (2002): *Scaffolding Language, Scaffolding Learning* — bastides per a alumnat EAL; GPS disciplinar.
- Decret 175/2022 (curriculum Catalunya): competencia en comunicacio lingüística i produccio de textos.
