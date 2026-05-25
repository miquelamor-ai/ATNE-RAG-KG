---
modul: M3
titol: "Escriure/adaptar un resum"
tipus: instrument
categoria_principal: generes
categories_secundaries: []
descripcio: "Instrument per adaptar o generar un resum (gènere autònom de condensació): idea principal al primer paràgraf sense preàmbul, conservació de la veu original de l'autor, connectors lògics que reprodueixen l'estructura del text font i proporció respectada. HCL Explicar (reformulació fidel i condensada). No s'adapta a pre-A1. Rúbrica gradada 6 passos × 5 nivells MECR (A1→C1)."
mecr_range: [A1, A2, B1, B2, C1]
agent_roles: [adapter, generator]
genre_key: resum
translanguaging: false
multimodal: false
moduls_relacionats: [M3]
variables_configurables:
  fase_lectora: [alfabetica_emergent, alfabetica_fluida]
skill_meta: write-resum@corpusFJE/skills/generes/write-resum
review_status: pilot-fusio-7
version: 4.0.0-canonic
generat_at: 2026-05-26
actualitzat_at: 2026-05-26
notebooklm_review:
  data: 2026-05-26
  veredicte: si-amb-correccions-menors
  aplicades_des_d_inici: [patro-canonic-pilots-fase-a, aclariment-us-lectura-vs-produccio-C1, fidelitat-gradada-C2, variabilitat-cardinal-passos-D3]
  aplicades_post_review: [b5-resum-pas3-cross-source, b5-resum-pas52-llindar-a1]
  comentari_key: "pas3-connectors-cross-source-afegit-b1+; pas52-llindar-4-paraules-relaxat-a-a1; preambul-a1-mantingut-model-lectura-no-produccio"
---

# Escriure/adaptar un resum

## Descripció

El resum és un text secundari que condensa un text font mantenint les idees principals, la seva relació lògica i la veu original de l'autor. El seu tret definitori és la **fidelitat + reformulació**: el resum no interpreta ni afegeix opinió pròpia, però tampoc copia — reformula amb vocabulari accessible. A diferència del **resum graduat** (complement de mediació que crea un marc amb forats per omplir), el resum com a gènere és un text acabat i complet.

**Tipologia MALL**: Expositiva (text secundari).
**HCL principal**: Explicar — seleccionar la idea principal del text font, sintetitzar les idees secundàries i presentar-les de manera coherent i condensada, preservant la lògica de l'autor original.
**HCL secundàries**: Descriure (si el text font és descriptiu) · Narrar (si el text font és narratiu) — el resum adapta la seva HCL secundària al gènere del text font que condensa.
**Nota MALL**: resumir implica primer recapitular oralment ("de qué tracta?") i llavors produir el text escrit condensat. La recapitulació oral (A1-A2) és la bastida de la producció escrita.
**No s'adapta a pre-A1**: el resum escrit requereix selecció autònoma de la idea principal del text font i reformulació (no còpia). Aquesta doble operació — identificar la jerarquia informativa i parafrasear — requereix base lecto-escriptora mínima i comprensió del text font com a prerequisit. Per a pre-A1, millor recapitulació oral amb suport visual. (Decisió 6 canònica Fase B.)

**Connexions MALL transversals:**
- *HCL Explicar com a evidència de comprensió lectora*: saber escriure un resum és saber llegir. L'alumne que no sap quina és la idea principal no pot escriure un bon resum. El resum revela la comprensió lectora de manera directa i verificable: és l'instrument d'avaluació de comprensió lectora per excel·lència de totes les matèries.
- *Reformulació vs. còpia — la competència CALP clau*: la distinció entre resumir i copiar és una de les competències de més alta demanda cognitiva del CALP. Parafrasear (dir el mateix amb paraules pròpies) requereix comprensió profunda del significat, no només del text superficial. Cal treballar-la explícitament i de forma progressiva des de A1.
- *Recapitulació oral com a bastida ZDP (A1-A2)*: la seqüència pedagògica òptima és: (1) llegir el text, (2) recapitular oralment en parella ("explica de qué tracta"), (3) escriure el resum. La recapitulació oral actua com a bastida ZDP: l'alumne ancra la comprensió en el que ja pot dir oralment abans de produir-ho per escrit.

**Aclariment d'ús — què descriu aquesta rúbrica.**
Aquesta rúbrica descriu el **resum adaptat per a la LECTURA** de l'alumne. **No descriu la producció autònoma** — la producció és tasca d'un derivat propi. Principi pedagògic MALL: l'alumne llegeix models al màxim del seu abast.
**Sub-granularitat dins de A1**: es treballa amb `fase_lectora: [alfabetica_emergent, alfabetica_fluida]`; no hi ha nivell logogràfic perquè el gènere requereix base lecto-escriptora mínima.

## Detecció

**Senyals docent** (quan adaptar a resum):
- L'alumne ha de demostrar que ha comprès un text llegit a classe produint un resum escrit.
- El text font és un article, un capítol, un text divulgatiu o acadèmic.
- La unitat avalua la comprensió lectora a través de la producció escrita condensada.
- L'activitat preveu que l'alumne produeixi un resum com a tasca de síntesi transversal (totes les matèries).

**Senyals alumne** (que indica que necessita bastida):
- Comença el resum amb "En aquest text parla de..." o "L'autor explica que..." (preàmbul meta-comentari).
- Copia frases literals del text font sense reformulació.
- Inclou la seva opinió sobre el text ("A mi m'ha semblat que...", "Crec que l'autor té raó").
- Omit la idea principal i desenvolupa exemples secundaris.
- Fa una llista d'idees sense connectors lògics entre elles.

**Context favorable**:
- Totes les matèries. El resum és el gènere de comprensió lectora per excel·lència.
- Especialment útil a Ciències Socials, Ciències, Llengua i Filosofia per a textos expositius i argumentatius.

**Anti-senyals** (quan NO adaptar a resum):
- El text vol afegir una valoració personal → ressenya.
- El text vol argumentar una tesi → assaig.
- El text condensa amb forats per omplir → resum graduat (complement de mediació).
- El text analitza i interpreta → comentari crític.
- Pre-A1: la selecció autònoma de la idea principal i la reformulació no son accessibles sense base lecto-escriptora.

## Modulació per nivell

| Pas | Dimensió | A1<br>Inicial | A2<br>Funcional | B1<br>Estratègic | B2<br>Acadèmic | C1<br>Crític |
|---|---|---|---|---|---|---|
| **1. Idea principal al 1r paràgraf** | Claredat i directesa | 1 frase que diu de qué tracta el text. Directa. Al principi. | Idea principal en 1-2 frases. Primer paràgraf. Directa i sense preàmbul. | Idea principal condensada amb precisió. Primera frase densa i informativa. | Idea principal amb el matís necessari. Primera frase que capta el nucli del text font. | Idea principal amb tots els matisos que el text font implica, sense sobrecarregar. |
| **2. Conservació de la veu original** | Fidelitat i imparcialitat | No afegir opinions pròpies: sense "crec que", "m'agrada", "és interessant". | Sense afegir informació nova ni opinions. Veu neutra i impersonal. | Reformulació que manté el punt de vista de l'autor original sense adoptar-lo. | Veu de l'autor preservada. Distinció clara entre el que diu l'autor i qui resumeix. | Veu de l'autor preservada amb precisió. Atribució explícita si cal ("Segons l'autor..."). |
| **3. Connectors lògics** | Coherència i estructura | "I", "però", "perquè". Pocs però presents. | "Per tant", "d'altra banda", "però". Variats i usats per connectar les idees. | Connectors que reflecteixen la relació real entre idees del text font (causa, contrast, conseqüència). | Connectors precisos que reprodueixen l'estructura lògica del text font. | Connectors sofisticats que capturen la lògica argumentativa o expositiva de l'autor. |
| **4. Proporció i llargada** | Síntesi i selecció | 3-4 frases. Màxim 1/3 del text font. | 4-6 frases (o ~1/4 del text font). Proporcional a la complexitat del font. | ~1/4 o 1/5 del text font. Preservar estructura lògica per davant de la llargada mecànica. | Proporció conscient: la llargada reflecteix la importància relativa de cada idea del font. | Condensació rigorosa: cada frase del resum aporta informació nova i necessària del font. |
| **5. Criteris transversals** | Síntesi sense preàmbul | Cap "En aquest text…", "L'autor diu que…" com a primera frase. La primera paraula del resum és ja contingut. | Idem. Sense meta-comentaris sobre el text o l'autor. | Idem. Cap frase buida de contingut al resum. | Idem. Densitat informativa alta. | Idem. Màxima densitat: cada frase és contingut del font, no comentari sobre el font. |
|  | No còpia literal | Cap frase copiada del text font. Reformulació sempre. | Idem. Cap fragment de més de 4 paraules consecutives idèntiques al font. | Idem. La reformulació captura el sentit, no el text superficial. | Idem. La reformulació preserva els matisos semàntics rellevants del font. | Idem. La reformulació pot conservar termes tècnics si no existeix paràfrasi adequada. |
|  | Fidelitat al text font | Fidelitat a la idea principal i a les 2-3 idees secundàries del text font. | Fidelitat a la idea principal, a les idees secundàries i a l'ordre del font. | Fidelitat a la idea principal, a les idees secundàries, als connectors i a la relació lògica del font. | Fidelitat a la complexitat informativa i al registre del text font. | Fidelitat total: idea principal, idees secundàries, relació lògica i matisos del font. |
| **6. Autoavaluació metacognitiva** | Reflexió sobre el procés | "He escrit la idea principal en la primera frase. No he escrit la meva opinió." | "He connectat les idees amb connectors. No he afegit informació nova." | "El meu resum té les idees en el mateix ordre que el text original. He eliminat exemples però no idees." | "He mantingut la veu de l'autor. La llargada és proporcional al text font." | "El meu resum és dens, fidel i complet. Qualsevol persona pot entendre el text font llegint el meu resum." |

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
| 1 Idea principal — Claredat | `binary` + `qualitative` | **sí** | binary: idea principal present a la primera frase; qualitative: LLM-jutge sobre si la primera frase captura la idea central del text font (cross_source) |
| 2 Veu original — Fidelitat | `binary` + `qualitative` | no | binary: detectar opinions pròpies ("crec que", "m'agrada", "és interessant", "estic d'acord"); qualitative: LLM-jutge sobre si el resum adopta el punt de vista de l'autor o del resumidor |
| 3 Connectors lògics — Coherència | `structural` + `qualitative` + `cross_source` | **sí** (B1+) | detectar i comptar connectors; qualitative: LLM-jutge sobre si el connector reflecteix la relació real entre les idees (causa, contrast, conseqüència) o si és merament additiu ("i"); cross_source (B1+): verificar si la relació lògica del connector coincideix amb la del text font |
| 4 Proporció — Síntesi | `countable` + `qualitative` | **sí** | comptar paraules/frases del resum vs. text font; qualitative: LLM-jutge sobre si la proporció respecta la importància relativa de les idees o fa retallada mecànica |
| 5.1 Criteris — Sense preàmbul | `binary` | no | regex: detectar "En aquest text", "L'autor diu que", "Aquest article", "En aquest resum" com a primera frase; binary: absent compleix |
| 5.2 Criteris — No còpia literal | `binary` + `qualitative` | **sí** | binary: A1 detectar frases senceres copiades; A2+: detectar fragments de 4+ paraules consecutives idèntiques al text font; qualitative: LLM-jutge sobre si la reformulació captura el sentit o és paràfrasi superficial |
| 5.3 Criteris — Fidelitat al text font | `cross_source` + `qualitative` | **sí** | comparar idea principal, idees secundàries i relació lògica del font vs. resum; LLM-jutge sobre si les omissions son justificades (exemples) o problemàtiques (idees principals) |
| 6 Autoavaluació metacognitiva | `metacognitive` | no | derivar a vista d'autoavaluació alumne + registre docent |

**Notes:**
- El resum és l'únic gènere del lot B.5 on `requires_source_text: sí` per a múltiples descriptors (Pas 1, 4, 5.2, 5.3). Per definició, el resum és un text secundari i la seva validació requereix comparació amb el font.
- Preàmbul (Pas 5.1): altament automatitzable. Les frases d'obertura del tipus "En aquest text...", "L'autor explica...", "Aquest article parla de..." son el error més freqüent i el més fàcil de detectar per regex.
- Còpia literal (Pas 5.2): parcialment automatitzable per n-grames. Fragments de 4+ paraules consecutives idèntiques al font son candidats a còpia.
- Resum graduat (mediació) vs. resum (gènere): l'instrument `generate-resum-graduat` és un complement de mediació que crea una estructura amb forats per omplir. Aquest instrument descriu el resum com a text complet i autònom. Son dos instruments distints amb lògica pedagògica diferent.

## Heurístiques docent

**H1 — La pregunta de la idea principal.**
Proposo que l'alumne llegeixi el text sencer i llavors, sense mirar-lo, respongui en una frase: "De qué tracta aquest text?" La resposta és la idea principal. Amb la idea principal escrita, la resta del resum s'organitza com a desenvolupament d'aquesta frase inicial.

**H2 — El marcador de paràgrafs (B1+).**
Per a textos llargs, proposo que l'alumne marqui la idea central de cada paràgraf al marge. Amb les idees centrals llistades, el resum és una síntesi de les marques. La tècnica entrena la identificació de la jerarquia informativa del text.

**H3 — El test del parafraseo.**
Llegeixo una frase del resum de l'alumne i demano: "Pots dir el mateix sense usar cap paraula de la frase original?" Si pot, ha parafraseat correctament. Si no pot, ha copiat. El test es fa en parelles: A llegeix la frase del resum de B, B la reformula sense mirar l'original.

**H4 — Recapitulació oral primer (A1-A2).**
Abans d'escriure, proposo 2 minuts de recapitulació oral en parelles: "Explica a ton company de qué tractava el text." Qui explica oralment construeix la comprensió col·lectiva necessària per escriure el resum individual. La recapitulació oral és la bastida ZDP del resum escrit.

## Fonts principals

- MALL (Model d'Aprenentatge de Llengües i Literacitat): HCL Explicar, text secundari com a evidència de comprensió, recapitulació oral com a bastida.
- Kintsch, W. & van Dijk, T.A. (1978): macroregles de condensació (supressió, generalització, construcció) — el model cognitiu del resum.
- Cassany, D. (1993): *Ensenyar llengua* — parafrasear com a estratègia de comprensió lectora; distinció resum vs. còpia.
- Decret 175/2022 (currículum Catalunya): competència en comunicació lingüística, comprensió i producció de textos expositius.
