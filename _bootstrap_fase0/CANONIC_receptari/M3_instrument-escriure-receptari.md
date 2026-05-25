---
modul: M3
titol: "Escriure/adaptar una recepta"
tipus: instrument
categoria_principal: generes
categories_secundaries: []
descripcio: "Instrument per adaptar o generar una recepta: text instructiu culinari amb llista d'ingredients ordenada per ús, passos numerats amb verb imperatiu, indicadors sensorials per pas i resultat esperat. HCL Narrar processal + Descriure (ingredients, textures). No s'adapta a pre-A1. Rúbrica gradada 8 passos × 5 nivells MECR (A1→C1)."
mecr_range: [A1, A2, B1, B2, C1]
agent_roles: [adapter, generator]
genre_key: receptari
translanguaging: false
multimodal: false
moduls_relacionats: [M3]
variables_configurables:
  fase_lectora: [alfabetica_emergent, alfabetica_fluida]
skill_meta: write-receptari@corpusFJE/skills/generes/write-receptari
review_status: pilot-fusio-6
version: 4.0.0-canonic
generat_at: 2026-05-26
actualitzat_at: 2026-05-26
notebooklm_review:
  data: 2026-05-26
  veredicte: si-amb-correccions
  aplicades_des_d_inici: [patro-canonic-pilots-fase-a, aclariment-us-lectura-vs-produccio-C1, fidelitat-gradada-C2, variabilitat-cardinal-passos-D3]
  aplicades_post_review: [a25-receptari-autoavaluacio-a1-quantitats]
  comentari_key: "pas8-a1-eliminada-referencia-quantitats-contradiccio-amb-pas1-a1-sense-quantitats"
---

# Escriure/adaptar una recepta

## Descripció

La recepta és un text instructiu especialitzat en processos culinaris. El seu tret definitori doble és la **llista d'ingredients ordenada per l'ordre en qué s'usen** i els **indicadors sensorials** ("fins que sigui daurat", "fins que l'escuma desaparegui") com a criteris d'avaluació autèntics dels passos clau. A diferència de l'instructiu genèric, la recepta porta inherentment la dimensió cultural: els plats son portadors d'identitat.

**Tipologia MALL**: Instructiva/Prescriptiva (culinària).
**HCL principal**: Narrar — seqüència processal culinària: la recepta ordena accions en el temps amb verb imperatiu com a vehicle.
**HCL secundàries**: Descriure — llistar i quantificar ingredients; descriure textures, colors i olors com a indicadors sensorials (A1-B1+).
**No s'adapta a pre-A1**: la recepta requereix la **lectura simultània de dos sistemes**: la llista d'ingredients (amb quantitats) i la seqüència de passos imperatius, amb la comprensió que els ingredients de la llista s'usen als passos en l'ordre en qué apareixen. Aquesta doble planificació i la comprensió de les mesures com a quantitats exactes ("200 g", "2 cullerades") no és accessible sense base lecto-escriptora mínima. (Decisió 6 canònica Fase B.)

**Connexions MALL transversals:**
- *Recepta com a pont BICS→CALP*: el context culinari (BICS) és familiar i concret per a quasi tot l'alumnat. Les mesures, els temps i els indicadors sensorials son vocabulari CALP (termes tècnics precisos) en un entorn de seguretat cognitiva. La recepta és el gènere instructiu amb menor barrera d'entrada.
- *Indicador sensorial com a competència d'observació científica*: "fins que sigui daurat", "quan l'escuma desaparegui", "quan el tacte sigui elàstic" son instruccions d'autoavaluació en acció. L'alumne aprèn a observar i decidir, no només a seguir. Aquesta competència és transferible a la ciència (observació d'experiments) i a la tecnologia.
- *Recepta com a vehicle d'identitat cultural (TOLC)*: els plats son portadors d'identitat. Treballar receptes de les cultures familiars de l'alumnat és un acte de reconeixement identitari. En producció, la recepta en L1 traduïda al català és un acte de TOLC natural i motivador.

**Aclariment d'ús — què descriu aquesta rúbrica.**
Aquesta rúbrica descriu la **recepta adaptada per a la LECTURA** de l'alumne. **No descriu la producció autònoma de l'alumne** — la producció és tasca d'un derivat propi. Principi pedagògic MALL: l'alumne llegeix models al màxim del seu abast.
**Sub-granularitat dins de A1**: es treballa amb `fase_lectora: [alfabetica_emergent, alfabetica_fluida]`; no hi ha nivell logogràfic perquè el gènere requereix base lecto-escriptora mínima.

## Detecció

**Senyals docent** (quan adaptar a recepta):
- El text font és una recepta (culinària, de laboratori simplificada o de taller d'arts).
- La unitat treballa el text instructiu en un context culinari, cultural o de salut i alimentació.
- L'alumne ha de llegir per comprendre un procés culinari i poder-lo reproduir.
- L'activitat preveu un receptari de classe, un projecte d'educació alimentària o un taller intercultural.

**Senyals alumne** (que indica que necessita bastida):
- Barreja ingredients i passos dins d'un mateix paràgraf.
- No posa quantitats als ingredients.
- Usa la passiva ("s'ha de barrejar" en lloc de "Barreja").
- Omit passos que considera obvis (pelar, tallar, esbandir).
- Usa indicadors temporals vagues en lloc de sensorials ("cou 10 minuts" en lloc de "fins que sigui daurat").

**Context favorable**:
- Ciències Naturals: nutrició, química culinària (reaccions de cuina), biotecnologia alimentària.
- Ciències Socials: gastronomia i cultura, alimentació al món.
- Llengua i Literatura: recull de receptes de les famílies de la classe, traducció intercultural.
- Tutoria: projecte multicultural, mercat solidari, cuina inclusiva.
- Alumnat nouvingut A1-A2: la recepta familiar és un text real i proper que pot portar de casa.

**Anti-senyals** (quan NO adaptar a recepta):
- El text explica el procés químic de la cocció o el valor nutricional → divulgatiu.
- El text descriu el plat acabat sense instruccions → descripció.
- El text narra un àpat o una experiència culinària → crònica o diari.
- Pre-A1: la doble planificació (llista d'ingredients + passos) no és accessible sense base lecto-escriptora.

## Modulació per nivell

| Pas | Dimensió | A1<br>Inicial | A2<br>Funcional | B1<br>Estratègic | B2<br>Acadèmic | C1<br>Crític |
|---|---|---|---|---|---|---|
| **1. Llista d'ingredients** | Completitud i format | Llista de 3-5 ingredients. Sense quantitats. 1 ingredient per línia. | Llista de 4-6 ingredients amb quantitats bàsiques ("1 tassa", "2 ous"). | Ingredients amb quantitats i unitats de mesura estàndard. Llista completa. | Ingredients completament especificats (graus, temps de repòs si cal). | Ingredients amb quantitats precises, variants i possibles substitucions explicitades. |
| **2. Ordre dels ingredients** | Seqüència d'ús | Ingredients en qualsevol ordre (llista simple). | Ingredients ordenats aproximadament per l'ordre en qué s'usen. | Ingredients ordenats estrictament per l'ordre d'ús. Separació per fases si cal. | Agrupació per fases de preparació si la recepta és complexa. | Organització professional per fases i subfases si cal. Cada fase amb subtítol. |
| **3. Format dels passos** | Claredat i precisió | Passos numerats. 1 verb + 1 objecte. ≤6 paraules per pas. | Passos numerats. 1 acció culinària + context breu. ≤10 paraules per pas. | Passos numerats amb indicador sensorial o temporal si cal. 1-2 accions relacionades. | Passos numerats complets i autònoms. Pot incloure condicions simples ("si bull, baixa el foc"). | Passos tècnicament precisos. Temperatures, temps i textures especificats sempre. |
| **4. Indicadors sensorials** | Observació i verificació | 1 indicador per pas crític: "fins que sigui daurat". | 1-2 indicadors sensorials per pas crític (color, textura, olor). | Indicadors sensorials als passos clau. Permeten saber si el pas s'ha executat correctament. | Indicadors sensorials precisos i variats (color, so, tacte, olor). Sempre preferits al temps. | Indicadors sensorials complets que permeten reproduir la recepta sense ajuda externa. |
| **5. Temps de cocció** | Precisió temporal | Temps global aproximat: "uns 20 minuts". | Temps per a les fases principals: "fregir 5 minuts / coure 20 minuts". | Temps específic per a cada pas que en requereix. Indicador sensorial alternatiu. | Temps amb marge ("10-12 minuts") i indicador sensorial com a confirmació. | Temps i temperatures precisos. Alternatives per a equipaments o altituds diferents. |
| **6. Resultat esperat** | Verificabilitat final | 1 frase: com ha de quedar (color o textura principals). | 1-2 frases que descriuen el resultat en termes sensorials concrets. | Resultat descrit amb 2-3 indicadors sensorials. Com saber que ha sortit bé. | Resultat complet: aspecte, textura, olor i gust. Criteris de qualitat. Racions o quantitat final. | Resultat professional: criteris precisos + variacions acceptables + errors comuns amb solució. |
| **7. Criteris transversals** | No passiva en els passos | Cap instrucció en passiva. "Barreja la farina" (no "S'ha de barrejar la farina"). Imperatiu consistent. | Idem. | Idem. | Idem. | Idem. Imperatiu o infinitiu normatiu consistent. |
|  | No ingredients a mig text | Cap ingredient nou als passos que no hagi estat a la llista prèvia. | Idem. | Idem. | Idem. | Idem. Variants opcionals en nota final, no intercalades als passos. |
|  | Fidelitat al text font | Fidelitat als ingredients principals i a l'ordre dels passos. | Fidelitat als ingredients, a l'ordre, als temps bàsics i al resultat. | Fidelitat als ingredients, als passos, als indicadors sensorials i al resultat. | Fidelitat a la complexitat culinària i als indicadors de qualitat del text original. | Fidelitat a la complexitat, a les variants i als errors comuns del text original. |
| **8. Autoavaluació metacognitiva** | Reflexió sobre el procés | "He escrit la llista d'ingredients i els passos numerats." | "Cada pas té un verb i un objecte. He posat indicadors ('fins que...') a alguns passos." | "Els ingredients estan en l'ordre d'ús. Puc executar cada pas sense llegir el següent." | "La recepta té totes les quantitats i especificitats. El resultat indica les racions." | "La recepta és completa i professional. Qualsevol persona podria cuinar el plat seguint els meus passos." |

## Metadades de cel·la (per a `build_skills.py`)

**Tipus de descriptor:**
- `countable` — llindar quantitatiu verificable mecànicament.
- `binary` — "compleix / no compleix".
- `qualitative` — requereix judici humà o LLM-jutge.
- `structural` — requereix anàlisi sintàctica o discursiva.
- `cross_source` — requereix accés al text font per comparar.
- `metacognitive` — descriptor de procés en primera persona.

| Pas / Dimensió | Tipus | requires_source_text | validation_hint |
|---|---|---|---|
| 1 Llista d'ingredients — Completitud | `binary` + `countable` | no | binary: llista d'ingredients present i anterior als passos; countable: comptar ingredients; verificar quantitats per nivell (absent A1, present A2+) |
| 2 Ordre dels ingredients — Seqüència | `structural` + `qualitative` | no | qualitative: LLM-jutge sobre si els ingredients apareixen en l'ordre en qué s'usen als passos; A1 exempt |
| 3 Format dels passos — Claredat | `binary` + `countable` | no | binary: passos numerats; comptar paraules per pas (≤6 A1, ≤10 A2); detectar absència de verb imperatiu |
| 4 Indicadors sensorials — Observació | `binary` + `countable` | no | binary: indicadors sensorials presents als passos clau; countable: comptar indicadors (mínim 1 a A1, als passos clau a A2+); detectar indicadors temporals sense sensorial alternatiu (B1+) |
| 5 Temps de cocció — Precisió | `binary` + `qualitative` | no | binary: temps present als passos que el requereixen; qualitative: LLM-jutge sobre si l'indicador sensorial és preferit al temps com a criteri de qualitat (B1+) |
| 6 Resultat esperat — Verificabilitat | `binary` + `qualitative` | no | binary: resultat present al final; qualitative: LLM-jutge sobre verificabilitat sensorial (no sols "fins que estigui fet") |
| 7.1 Criteris — No passiva | `binary` | no | regex: detectar passiva als passos ("s'ha de", "s'afegirà", "s'ha de barrejar"); binary: absent compleix |
| 7.2 Criteris — No ingredients a mig text | `binary` + `cross_source` | **sí** (si adaptació) | binary: detectar ingredients als passos que no estan a la llista prèvia; cross_source: verificar completitud de la llista respecte al text font |
| 7.3 Criteris — Fidelitat al text font | `cross_source` + `qualitative` | **sí** (si adaptació) | comparar ingredients, passos, indicadors i resultat original vs adaptat; LLM-jutge sobre fidelitat culinària |
| 8 Autoavaluació metacognitiva | `metacognitive` | no | derivar a vista d'autoavaluació alumne + registre docent |

**Notes:**
- Indicadors sensorials (Pas 4): detectable per patrons lingüístics específics: "fins que + [adjectiu o sintagma sensorial]", "quan + [verb d'estat sensorial]", "si [color/textura]". Altament automatitzable.
- Passiva als passos (Pas 7.1): igual que l'instructiu, detectable per regex sobre construccions passives a l'interior dels passos numerats.
- Ingredients a mig text (Pas 7.2): verificable comparant el lèxic de la llista prèvia amb els substantius de la llista de passos. Ingredients que apareixen als passos i no a la llista prèvia son errors detectables per diferència de sets.

## Heurístiques docent

**H1 — Primer la llista, després els passos.**
Proposo que l'alumne escrigui primer tots els ingredients que usarà, i LLAVORS escrigui els passos. Molts alumnes obliden ingredients perquè comencen pels passos. La llista prèvia força la planificació completa del procés culinari.

**H2 — L'indicador sensorial com a exercici d'observació.**
Per a cada pas que acaba amb un temps ("cou 10 minuts"), demano: "Com saps que ja està?" La resposta és l'indicador sensorial ("quan sigui daurat", "quan l'escuma desaparegui"). Transformar el temps en sensació és un exercici d'observació científica integrat a la llengua.

**H3 — La recepta familiar com a pont identitari (TOLC).**
Proposo que cada alumne porti la recepta d'un plat típic de la seva família o cultura. La classe recull les receptes i crea un receptari col·lectiu. L'alumne nouvingut pot escriure la recepta en la seva L1 i treballem junts la versió catalana: és un acte de TOLC natural, motivador i de reconeixement identitari.

**H4 — Cuinar per verificar.**
La millor prova d'una recepta és executar-la. Si la unitat ho permet, proposo cuinar el plat seguint exactament la recepta escrita per un company. Els errors de claredat (ingredient no llistat, pas fusionat, indicador temporal en lloc de sensorial) es fan visibles i corregibles immediatament.

## Fonts principals

- MALL (Model d'Aprenentatge de Llengües i Literacitat): HCL Narrar processal, gènere instructiu culinari, transició BICS→CALP.
- Cummins, J. (2001): *Negotiating identities: Education for empowerment in a diverse society* — la recepta com a vehicle d'identitat cultural i TOLC.
- Halliday, M.A.K. (1994): *An Introduction to Functional Grammar* — funció ideativa; el text instructiu com a regulació de l'acció en un context cultural.
- Decret 175/2022 (currículum Catalunya): competència en comunicació lingüística i educació per al desenvolupament sostenible.
