---
modul: M3
titol: "Escriure/adaptar un text instructiu"
tipus: genere-discursiu
categoria_principal: generes
categories_secundaries: []
descripcio: "Instrument per adaptar o generar un text instructiu: guia pas a pas per realitzar una acció amb materials en llista prèvia, verb imperatiu per pas, ordre cronològic estricte i resultat esperat. HCL Narrar processal + Descriure (materials). No s'adapta a pre-A1. Rúbrica gradada 7 passos × 5 nivells MECR (A1→C1)."
mecr_range: [A1, A2, B1, B2, C1]
agent_roles: [adapter, generator]
genre_key: instructiu
translanguaging: false
multimodal: false
moduls_relacionats: [M3]
variables_configurables:
  fase_lectora: [alfabetica_emergent, alfabetica_fluida]
skill_meta: write-instructiu@corpusFJE/skills/generes/write-instructiu
review_status: pilot-fusio-6
version: 4.0.0-canonic
generat_at: 2026-05-26
actualitzat_at: 2026-05-26
notebooklm_review:
  data: 2026-05-26
  veredicte: si
  aplicades_des_d_inici: [patro-canonic-pilots-fase-a, aclariment-us-lectura-vs-produccio-C1, fidelitat-gradada-C2, variabilitat-cardinal-passos-D3]
  aplicades_post_review: []
  comentari_key: "translanguaging-false-correcte-H4-estrategia-gramatical-no-L1"
---

# Escriure/adaptar un text instructiu

## Descripció

El text instructiu guia el lector pas a pas per realitzar una acció amb **ordre cronològic processal estricte**. El seu tret definitori és la doble estructura invariant: la **llista de materials** (sempre prèvia als passos) i els **passos numerats** (un verb imperatiu + un objecte per pas). A diferència del text divulgatiu (que explica per qué funciona un procés), l'instructiu no explica: prescriu accions.

**Tipologia MALL**: Instructiva/Prescriptiva.
**HCL principal**: Narrar — variant processal: on el conte narra fets que han passat, l'instructiu narra fets que han de passar; la seqüenciació és la mateixa, el temps verbal canvia (imperatiu present).
**HCL secundàries**: Descriure — llistar i quantificar els materials (A1-B1).
**No s'adapta a pre-A1**: l'instructiu requereix la interpretació del **verb imperatiu com a ordre adreçada al lector** — "Barreja la farina i l'água" prescriu una acció futura per a l'executor, no descriu un event ni explica un fenomen. Aquesta funció pragmàtica directiva del verb imperatiu (acte de parla prescriptiu) requereix base lecto-escriptora mínima i la comprensió del "tu" implícit com a executor. (Decisió 6 canònica Fase B.)

**Connexions MALL transversals:**
- *Narrar processal com a variant de HCL Narrar*: el text instructiu és la variant processal de la HCL Narrar. La seqüenciació temporal és la mateixa que en el conte o la crònica, però el temps verbal canvia (imperatiu o futur) i el punt de vista passa de "narrador" a "instructor". Treballar l'instructiu és treballar la seqüenciació en mode actiu.
- *Verb d'acció com a ancoratge cognitiu*: el verb imperatiu ("agafa", "barreja", "posa") és la paraula amb màxima càrrega informativa. Per a alumnat nouvingut o amb dificultats de comprensió lectora, identificar el verb és identificar l'acció. Destacar els verbs és una bastida de lectura vàlida i transferible a altres gèneres prescriptius.
- *L'instructiu com a avaluació autèntica*: fer que l'alumne executi l'instructiu que ha escrit un company és avaluació autèntica. Si els passos no son independents o l'ordre no és clar, el resultat fallarà de forma visible i immediata. L'error és un feedback objectiu.

**Aclariment d'ús — què descriu aquesta rúbrica.**
Aquesta rúbrica descriu el **text instructiu adaptat per a la LECTURA** de l'alumne. **No descriu la producció autònoma de l'alumne** — la producció és tasca d'un derivat propi. Principi pedagògic MALL: l'alumne llegeix models al màxim del seu abast.
**Sub-granularitat dins de A1**: es treballa amb `fase_lectora: [alfabetica_emergent, alfabetica_fluida]`; no hi ha nivell logogràfic perquè el gènere requereix base lecto-escriptora mínima.

## Detecció

**Senyals docent** (quan adaptar a instructiu):
- El text font és un text instructiu (protocol d'experiment, guia d'ús, instruccions d'assemblatge, recepta simplificada).
- La unitat treballa un procés seqüencial (taller, experiment de laboratori, procediment de seguretat, algoritme matemàtic).
- L'alumne ha de llegir per comprendre com es fa alguna cosa, no per saber per qué funciona.
- L'activitat preveu que l'alumne produeixi un instructiu (explicar un joc, documentar un procés, crear un protocol).

**Senyals alumne** (que indica que necessita bastida):
- Mescla materials i passos dins d'un mateix paràgraf.
- Els passos no son independents: per executar el pas 4 cal saber el pas 3.
- Usa instruccions en passiva ("s'afegirà la farina" en lloc de "Afegeix la farina").
- Ordena els passos per lògica narrativa en lloc de per ordre d'execució.
- Dona passos per suposats o implícits perquè els considera obvis.

**Context favorable**:
- Ciències i Tecnologia: protocols d'experiment, instruccions d'assemblatge, procediments de seguretat.
- Educació Física: explicar les regles d'un joc o la seqüència d'un escalfament.
- Arts plàstiques: tècniques de pintura, escultura o collage.
- Matemàtiques: algoritmes i procediments de càlcul.
- Alumnat nouvingut A1-A2: l'estructura verbo-objecte simple és accessible i ofereix context comunicatiu real.

**Anti-senyals** (quan NO adaptar a instructiu):
- El text explica per qué funciona un procés → divulgatiu o informe.
- El text descriu l'aspecte o les propietats d'un objecte → descripció.
- El text narra una experiència → crònica o diari.
- El text regula conductes socials → reglament.
- Pre-A1: la interpretació del verb imperatiu com a ordre directiva no és accessible sense base lecto-escriptora.

## Modulació per nivell

| Pas | Dimensió | A1<br>Inicial | A2<br>Funcional | B1<br>Estratègic | B2<br>Acadèmic | C1<br>Crític |
|---|---|---|---|---|---|---|
| **1. Materials (llista prèvia)** | Completitud i ordre | Llista de 3-5 materials. Sense quantitats. 1 material per línia. | Llista de 4-6 materials amb quantitats bàsiques ("1 tassa", "2 ous"). | Llista completa amb quantitats i especificitats bàsiques. Materials en ordre d'ús. | Materials amb quantitats, tipus i condicions si escau. Llista exhaustiva. | Materials completament especificats. Alternatives si n'hi ha. Ordenats per fases si el procés és complex. |
| **2. Format dels passos** | Claredat i precisió | Passos numerats. 1 verb + 1 objecte. ≤5 paraules per pas. | Passos numerats. 1 verb + 1 objecte concret. ≤8 paraules per pas. | Passos numerats. 1 verb precís + 1 objecte + context breu si cal. | Passos numerats. 1-2 accions estretament relacionades per pas. Pot incloure condicions simples. | Passos numerats. Completament autònoms. Precisió tècnica màxima. Pot incloure notes tècniques en cursiva. |
| **3. Autonomia del pas** | Independència operativa | Cada pas s'executa sense mirar el pas següent. Cap referència implícita. | Cada pas independent. Sense "després de fer el pas anterior". | Passos estrictament independents. Test: puc fer el pas 3 sense saber el pas 4? | Independència total. Cap referència implícita a un pas anterior ni posterior. | Passos absolutament autònoms i complets en si mateixos. Cap sobreentès. |
| **4. Ordre cronològic** | Rigor processal | Ordre d'execució respectat. No reordenar per legibilitat. | Ordre processal estricte. L'ordre és estructuralment obligatori. | Ordre cronològic respectat sense excepcions. Cap inversió per "lògica narrativa". | Ordre processal pur. Qualsevol reordenació trencaria el resultat final. | Ordre processal rigorós. Pot incloure passos previs de preparació clarament separats. |
| **5. Resultat esperat** | Verificabilitat | 1 frase: qué s'ha aconseguit. Com es nota que ha sortit bé. | Resultat de 1-2 frases: qué s'obté i com es nota que és correcte. | Resultat amb les característiques esperades del producte o procés acabat. | Resultat amb criteris de qualitat o avaluació del producte. | Resultat amb criteris precisos i possibles variacions acceptables. |
| **6. Criteris transversals** | No instruccions en passiva | Cap instrucció en passiva. "Afegeix l'agua" (no "S'afegirà l'agua"). Imperatiu consistent. | Idem. Cap construcció passiva ni impersonal ("s'ha d'afegir"). | Idem. El subjecte "tu" (implícit) és sempre l'executor. | Idem. Pot incloure l'imperatiu de primera plural ("Barregem") si el context és col·lectiu. | Idem. Precisió tècnica màxima amb l'imperatiu adequat al registre professional. |
|  | No condicionals niats | Cap condicional ("si X, fes Y"). Linealitat estricta. | Idem. Condicionals simples admesos en nota al final, no dins dels passos. | Idem. Alternatives opcionals en nota al final del pas, entre parèntesis. | Idem. Pot incloure bifurcacions simples en paràgraf separat. | Condicionals simples admesos si el context professional ho requereix, però sempre en pas separat. |
|  | Fidelitat al text font | Fidelitat al procés principal i a l'ordre dels passos. | Fidelitat al procés, a l'ordre i als materials essencials. | Fidelitat al procés, a l'ordre, als materials i als indicadors de qualitat. | Fidelitat a la complexitat tècnica del procés original. | Fidelitat a la complexitat, a la precisió tècnica i a les variacions del text original. |
| **7. Autoavaluació metacognitiva** | Reflexió sobre el procés | "He escrit la llista de materials. He escrit 3-5 passos numerats amb una acció cadascun." | "Cada pas té un verb i un objecte. He posat el resultat al final." | "Puc executar cada pas sense llegir el següent. He posat tots els materials a la llista." | "L'instructiu té totes les quantitats i especificitats necessàries. El resultat descriu com ha de quedar." | "L'instructiu és complet i professional. Qualsevol persona podria fer el procés seguint els meus passos." |

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
| 1 Materials — Completitud | `binary` + `countable` | no | binary: llista de materials present i anterior als passos; countable: comptar materials; verificar quantitats per nivell (absent A1, present A2+) |
| 2 Format dels passos — Claredat | `binary` + `countable` | no | binary: passos numerats (números arabs, no lletres ni vinyetes); comptar paraules per pas (≤5 A1, ≤8 A2); detectar absència de verb imperatiu |
| 3 Autonomia del pas — Independència | `binary` + `qualitative` | no | binary: detectar referències a passos anteriors ("com hem fet al pas 3", "usant el que has preparat"); qualitative: LLM-jutge sobre passos implícits o donats per suposats |
| 4 Ordre cronològic — Rigor | `structural` + `binary` | no | binary: detectar inversió d'ordre ("ara torna al pas 2", "abans de fer el pas 4 caldrà"); qualitative: LLM-jutge sobre si l'ordre d'execució és l'ordre del text |
| 5 Resultat esperat — Verificabilitat | `binary` + `qualitative` | no | binary: resultat present al final del text; qualitative: LLM-jutge sobre verificabilitat (com es nota que ha sortit bé) |
| 6.1 Criteris — No passiva | `binary` | no | regex: detectar passiva en els passos ("s'afegirà", "s'ha de barrejar", "ha de posar-se"); binary: absent compleix, present no compleix |
| 6.2 Criteris — No condicionals niats | `binary` | no | regex: detectar condicionals dins dels passos ("si X, fes Y"; "en cas que"); binary: absent compleix; condicionals en nota final admesos |
| 6.3 Criteris — Fidelitat al text font | `cross_source` + `qualitative` | **sí** (si adaptació) | comparar ordre dels passos, materials i resultat original vs adaptat; LLM-jutge sobre completitud i fidelitat tècnica |
| 7 Autoavaluació metacognitiva | `metacognitive` | no | derivar a vista d'autoavaluació alumne + registre docent |

**Notes:**
- Passiva en els passos (Pas 6.1): és el descriptor de qualitat lingüística més automatitzable de l'instructiu. Detectable per regex sobre "s'ha de + infinitiu", "s'afegirà", "ha de + infinitiu" referits als passos de l'executor.
- Numeració dels passos (Pas 2): verificable per regex sobre números arabs seguits de punt. L'absència de numeració és el segon error més freqüent dels alumnes.
- Autonomia (Pas 3): parcialmente automatitzable per detecció de pronoms anafòrics ("el que has preparat", "com hem vist") i connectors retrospectius.

## Heurístiques docent

**H1 — La bastida del verb + objecte.**
Proposo que l'alumne escrigui primer una llista de "Verb + objecte" per a cada pas, sense preocupar-se de cap altra cosa: "Agafar / la farina", "Barrejar / farina i aigua", "Posar / al forn". Amb la llista feta, completar cada pas és senzill. Funciona molt bé a A1-A2 i per a alumnat amb bloqueig d'escriptura.

**H2 — Provar l'instructiu amb un company.**
Per avaluar si l'instructiu és clar, un company l'executa seguint exactament el que hi ha escrit, sense cap aclariment verbal. Els errors d'execució indiquen passos poc clars, implícits o desordenats. L'alumne veu immediatament l'impacte de la claredat i el fa visible.

**H3 — La llista de materials com a planificació.**
Proposo que escriure la llista de materials es faci ABANS de redactar els passos: "Qué necessito per fer X?" La llista força l'alumne a planificar el procés complet i evita el problema dels materials que apareixen a mig text perquè "se m'havia oblidat posar-los".

**H4 — El subjecte "tu" com a eliminació de la passiva.**
Quan un pas és en passiva ("s'afegirà l'agua"), proposo substituir-la afegint "tu" o "vosaltres": "Afegeix tu l'agua" en lloc de "S'afegirà l'agua". El subjecte explícit elimina la passiva i posa la responsabilitat de l'acció en l'executor. Funciona especialment per a alumnat nou en català.

## Fonts principals

- MALL (Model d'Aprenentatge de Llengües i Literacitat): HCL Narrar processal, seqüenciació prescriptiva, gènere instructiu.
- Halliday, M.A.K. (1994): *An Introduction to Functional Grammar* — funció ideativa de la llengua; el text instructiu com a regulació de l'acció (metafunció interpersonal directiva).
- Decret 175/2022 (currículum Catalunya): competència en comunicació lingüística, gèneres instructius i procedimentals.
