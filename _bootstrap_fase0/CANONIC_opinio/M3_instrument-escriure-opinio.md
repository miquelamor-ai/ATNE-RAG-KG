---
modul: M3
titol: "Escriure/adaptar un article d'opinió"
tipus: genere-discursiu
categoria_principal: generes
categories_secundaries: []
descripcio: "Instrument per adaptar o generar un article d'opinió argumentatiu (tesi + arguments + evidències + connectors). No s'adapta a pre-A1 — l'argumentació requereix base lingüística A1 mínima. Rúbrica gradada 9 passos × 5 nivells MECR (A1→C1+) amb dimensions internes."
mecr_range: [A1, A2, B1, B2, C1]
agent_roles: [adapter, generator]
genre_key: opinio
translanguaging: true
multimodal: false
moduls_relacionats: [M3]
variables_configurables:
  fase_lectora: [alfabetica_emergent, alfabetica_fluida]
skill_meta: write-opinio@corpusFJE/skills/genres/write-opinio
review_status: pilot-fusio-3
version: 4.0.0-canonic
generat_at: 2026-05-25
actualitzat_at: 2026-05-25
notebooklm_review:
  data: 2026-05-25
  veredicte: si-amb-correccions-menors
  aplicades_des_d_inici: [patro-canonic-pilots-noticia-glossari, fidelitat-gradada-C2, aclariment-us-lectura-vs-produccio-C1, metadades-cella]
  aplicades_post_review: [pas4-varietat-funcional-B2plus, pas9-A2-procés-concret, metadades-tesi-A1-regex-binari]
  comentari_key: "Resol la maledicció de l'argumentació de Fase 0. Estableix estàndard alt per al CALP. Tres pilots ja validats — patró robust per a gèneres informatius (notícia), instruments de mediació (glossari) i gèneres argumentatius (opinió)."
---

# Escriure/adaptar un article d'opinió

## Descripció

L'article d'opinió és un gènere **argumentatiu** que defensa una tesi amb arguments recolzats en evidències concretes. **No s'adapta a pre-A1**: el pensament abstracte de presa de posició requereix una base lingüística mínima d'A1 i un domini bàsic del raonament causa-conseqüència.

**Tipologia MALL**: Argumentativa (convèncer).
**HCL principal**: Argumentar — defensar una tesi per convèncer l'interlocutor.
**HCL secundàries**: Justificar amb evidències (A2+) · Interpretar i reconèixer altres posicions (B2+) · Avaluar fiabilitat de les fonts (B2+).

**Connexions MALL transversals:**
- *Translanguaging / TOLC*: a A1, permet paraules de la L1 entre claudàtors `[...]` per mantenir el fil argumentatiu. A B1+, s'espera que l'argumentació sigui íntegrament en català.
- *Eix oral / escrit*: a A1-A2, el docent pot acceptar una versió oral de la tesi i arguments abans de la versió escrita (transferència oral→escrit).
- *Multimodalitat*: a A1-A2, es pot complementar amb un esquema visual de la tesi + arguments (mapa conceptual d'argumentació). A B1+, el text és autosuficient.

**Aclariment d'ús — què descriu aquesta rúbrica.**
Aquesta rúbrica descriu el **text d'opinió adaptat per a la LECTURA** de l'alumne. **No descriu la producció autònoma de l'alumne** — això es treballa amb un derivat propi (rúbrica d'avaluació formativa). El gènere argumentatiu és especialment pertinent per al **debat d'aula** com a producció col·laborativa (vegeu H1 i H3), però aquesta vista no és l'instrument adequat per avaluar aquesta producció.
**Sub-granularitat dins d'A1 i A2**: es treballa amb la variable independent `fase_lectora` del frontmatter, no amb columnes addicionals.

## Detecció

**Senyals docent** (quan triar opinió):
- El text font expressa un punt de vista, defensa una postura o inclou valoracions (editorial, carta al director, article d'opinió).
- Vol treballar l'argumentació estructurada i la presa de postura (HCL argumentar).
- La unitat didàctica inclou debat, pensament crític o controvèrsia sociocientífica.
- Alumnat de 4t de Primària en amunt amb MECR mínim A1.

**Senyals alumne** (que indica que necessita l'instrument):
- Quan se li demana "Justifica la teva resposta", **descriu o narra en lloc d'argumentar** — *encavalcament HCL* (MALL): l'habilitat demanada supera la competència actual.
- No pren postura: "Depèn…" o "Hi ha gent que pensa X i gent que pensa Y" sense defensar cap postura pròpia.
- La seva tesi no apareix fins al final del text (estructura invertida respecte al gènere).
- Usa "m'agrada / no m'agrada" com a argument, sense evidència.
- A B2, usa connectors A1 ("perquè", "però") en tots els arguments sense varietat.

**Context favorable**:
- Matèries de CCSS, Filosofia, Llengua o Tutoria amb debat o controvèrsia.
- Alumnat nouvingut B1-B2 que ja gestiona el català conversacional (BICS) però no el registre argumentatiu (CALP).
- Avaluació competencial que requereix argumentació escrita.

**Anti-senyals** (quan NO triar opinió):
- El text font és neutral o descriptiu → notícia o divulgatiu.
- Alumnat pre-A1: el gènere argumentatiu és massa abstracte (no s'adapta a pre-A1).
- El text font és narratiu → adaptar al gènere original.
- El docent vol treballar comprensió, no producció → preguntes de comprensió.

## Modulació per nivell

| Pas | Dimensió | A1<br>Inicial | A2<br>Funcional | B1<br>Estratègic | B2<br>Acadèmic | C1+<br>Crític |
|---|---|---|---|---|---|---|
| **1. Tesi** | Formulació | Una sola oració que comença amb "Crec que…". Sense preàmbul. | Clara i directa, en primera persona. Una oració. | Clara i directa. Pot ser de 2 oracions. Primera persona o impersonal. | Pot ser impersonal ("Cal considerar que…"). Elaborada però sense preàmbul. | Complexa. Pot matisar la pròpia postura o ser paradoxal. Sense preàmbul. |
|  | Posició al text | Primera frase del text. | Al primer paràgraf. | Al primer paràgraf. | Al primer paràgraf. | Al primer paràgraf. |
| **2. Arguments** | Nombre | Màxim 2 arguments. | 2-3 arguments. | 3 arguments. | 3-4 arguments amb estructura interna. | 3-5 arguments amb jerarquització explícita. |
| **3. Evidència per argument** | Tipus d'evidència | Exemple de la vida quotidiana de l'alumne. | Exemple concret o dada simple. | Dada, exemple concret o cita breu. | Dada estadística, cita d'expert o exemple complex. | Evidències múltiples i variades; pot incloure contrastos entre fonts. |
|  | Nombre per argument | 1 evidència per argument. | 1 evidència per argument. | 1 evidència per argument. | 1-2 evidències per argument. | Múltiples, segons la complexitat de l'argument. |
| **4. Connectors argumentatius** | Inventari per nivell | "perquè", "i", "però". | "perquè", "per tant", "però", "a més". | "en primer lloc", "a més", "per tant", "en conclusió". | "d'altra banda", "per contra", "en conseqüència", "en resum". **"Tanmateix" i "no obstant això" només a partir de B2**. | Connectors d'especialitat acadèmica propis de la disciplina. Variació rica i precisa. |
|  | Varietat funcional | N/A — només un tipus disponible. | N/A — repertori limitat. | Es recomana variar: causa (perquè) + addició (a més) + conclusió (per tant). | **Obligatori**: cada argument introduït amb un tipus diferent (causa / contrast / addició / conclusió). No repetir el mateix tipus. | Cada relació lògica marcada amb el connector funcional adequat (causal, concessiu, consecutiu, contrastiu, additiu). Sense repetició de tipus. |
| **5. Reconeixement i refutació** | Inclusió | No requerit. | No requerit. | Opcional ("Algú pot pensar que… però…"). | Obligatori: contraargument en paràgraf separat. | Obligatori: contraargument elaborat amb matís. |
|  | Refutació | No aplica. | No aplica. | Suggerida si s'inclou contraargument. | Refutació concreta amb evidència pròpia. | Refutació fonamentada, integra el contraargument al raonament. |
| **6. Conclusió** | Format i funció | Una frase: "Per això, crec que…". Reprèn la tesi. | 1-2 frases. Reprèn la tesi. No introdueix arguments nous. | 2-3 frases. Reprèn i reforça la tesi. Pot incloure una crida a l'acció. | 3-4 frases. Argumentada. Pot reformular la tesi amb matís. | Reformulació complexa de la tesi amb integració de les tensions identificades. |
| **7. Fiabilitat de les evidències** | Identificació i avaluació | No aplicable. | No aplicable. | Opcional: "D'on ve aquesta dada?". | Obligatori: el lector identifica la font de cada evidència principal. | Obligatori: el lector avalua la credibilitat i la intencionalitat de cada font. |
| **8. Criteris transversals** | Registre i persona gramatical | Primera persona singular. Registre informal tolerat. | Primera persona. Registre semiformal. | Primera persona o impersonal. Registre formal. | Impersonal preferit. Registre acadèmic. | Registre acadèmic complet; pot usar primera persona per a posicionament explícit. |
|  | Llargada de frase | Frases de fins a 12 paraules. | Frases de fins a 15 paraules. | Frases de fins a 18 paraules. | Frases de fins a 22 paraules. | Sense límit estricte; claredat com a criteri únic. |
|  | Retòrica | Cap ironia, cap pregunta retòrica, cap paral·lelisme complex. | Cap ironia, cap pregunta retòrica. | Cap ironia. Pregunta retòrica simple admissible si està marcada com a tal. | Pot incloure ironia explícita o pregunta retòrica si l'argumentació la sustenta. | Retòrica lliure si serveix l'argumentació; sense ambigüitat dels arguments. |
|  | Unicitat de tesi | Una sola tesi. | Una sola tesi. | Una sola tesi. | Una sola tesi. | Una sola tesi. |
|  | Fidelitat al text font | Fidelitat a la tesi i als arguments principals. | Fidelitat a la tesi i als arguments principals. | Fidelitat a la tesi, arguments i evidències principals. | Fidelitat a la tesi, arguments, evidències i, si hi és, contraargument. | Fidelitat al matís, als punts de vista i a la complexitat argumental originals. |
|  | No-atacs personals | Cap atac personal ni llenguatge valoratiu extrem. | Cap atac personal ni llenguatge valoratiu extrem. | Cap atac personal ni llenguatge valoratiu extrem. | Cap atac personal ni llenguatge valoratiu extrem. | Cap atac personal ni llenguatge valoratiu extrem. |
| **9. Autoavaluació metacognitiva** | Reflexió sobre el procés | "He pensat què crec abans d'escriure, i he buscat 2 raons que m'ajudin a explicar-ho." | "He comprovat que la meva tesi s'entén de seguida i que tinc un exemple per a cada raó." | "He revisat si els meus arguments es relacionen entre ells i si la conclusió tanca el que vaig anunciar a la tesi." | "He pensat què diria algú que no opina com jo, i he intentat respondre-li al text. Així he vist on era forta o feble la meva postura." | "He reflexionat sobre els límits de la meva pròpia postura: quines suposicions estic fent? Quines evidències em manquen?" |

## Metadades de cel·la (per a `build_skills.py`)

Cada dimensió té un **tipus de descriptor** que condiciona com s'ha de transformar al derivat avaluatiu i al derivat-prompt.

**Tipus de descriptor:**
- `countable` — té un llindar quantitatiu verificable mecànicament.
- `binary` — només admet "compleix / no compleix".
- `enumerable` — verificable contra una llista.
- `qualitative` — requereix judici humà o LLM-jutge.
- `structural` — requereix anàlisi sintàctica / discursiva.
- `cross_source` — requereix accés al text font per comparar.
- `metacognitive` — descriptor de procés en primera persona.

| Pas / Dimensió | Tipus | requires_source_text | validation_hint |
|---|---|---|---|
| 1.1 Tesi — Formulació | `qualitative` + `structural` | no | **A1**: regex contra fórmula d'arrencada "Crec que…" (marca binària, automatitzable sense LLM). **A2+**: LLM-jutge sobre presència de tesi explícita i adequació de la formulació al registre del nivell |
| 1.2 Tesi — Posició al text | `structural` | no | la tesi apareix al primer paràgraf (preferiblement primera frase) |
| 2 Arguments — Nombre | `countable` | no | comptar arguments separats per paràgraf o numeració |
| 3.1 Evidència — Tipus | `qualitative` + `enumerable` | no | LLM-jutge classifica l'evidència (exemple quotidià / dada / cita / estadística) i contrasta amb el nivell |
| 3.2 Evidència — Nombre per argument | `countable` | no | comptar evidències per argument |
| 4.1 Connectors — Inventari per nivell | `enumerable` | no | regex contra llistes de connectors per nivell; alerta si troba "tanmateix"/"no obstant" en text A1-B1 |
| 4.2 Connectors — Varietat funcional | `qualitative` + `enumerable` | no | A B2+: classificar connectors per tipus funcional (causa, contrast, addició, conclusió, concessió, conseqüència) i verificar que no es repeteix el mateix tipus en arguments consecutius |
| 5.1 Reconeixement — Inclusió | `binary` | no | detecció de marca discursiva ("Algú pot pensar que", "Hi ha qui defensa", "Per contra") |
| 5.2 Reconeixement — Refutació | `qualitative` | no | LLM-jutge sobre presència i qualitat de la refutació |
| 6 Conclusió | `qualitative` + `structural` | no | verificar que la conclusió reprèn la tesi i no introdueix arguments nous (LLM-jutge) |
| 7 Fiabilitat de les evidències | `qualitative` | no | LLM-jutge sobre identificació i avaluació de fonts segons nivell |
| 8.1 Registre i persona | `qualitative` | no | LLM-jutge sobre persona gramatical i registre formal/informal |
| 8.2 Llargada de frase | `countable` | no | comptar paraules per frase, verificar llindar per nivell |
| 8.3 Retòrica | `qualitative` | no | LLM-jutge detecta ironia, preguntes retòriques, paral·lelismes |
| 8.4 Unicitat de tesi | `binary` | no | LLM-jutge contra el text: hi ha una sola tesi o més d'una? |
| 8.5 Fidelitat al text font | `cross_source` | **sí** | comparació semàntica amb el text font, **gradada per nivell**: A1-A2 tesi+arguments principals; B1 +evidències; B2 +contraargument; C1 matís complet |
| 8.6 No-atacs personals | `binary` | no | LLM-jutge contra llista d'atacs personals i llenguatge valoratiu extrem |
| 9 Autoavaluació metacognitiva | `metacognitive` | no | derivat doble: autoavaluació alumne + registre docent de la qualitat |

**Notes:**
- Opinió té **molts descriptors `qualitative`** (tesi formulació, conclusió, fiabilitat, registre, retòrica). LLM-jutge serà el motor dominant — caldrà calibrar prompts específics quan s'activi.
- 4 Connectors argumentatius és **automatitzable amb regex** contra llistes per nivell (gran avantatge per cost). La regla "tanmateix/no obstant només a B2+" és estricta i mecànica.
- `cross_source` (8.5 Fidelitat) requereix text font gradat — el `validation_hint` ha de tenir prompts diferenciats per als 5 nivells A1-C1+.
- 5.2 Refutació té semàntica única (a opinió no la trobem a notícia ni glossari) — l'`audit_corpus.py` ha de validar-la al pipeline.

## Heurístiques docent

**H1 — La pregunta binària com a arrencada.**
Per a alumnat A1 o que no pren postura, la pregunta binària funciona millor que "Què en penses?": "Estàs a favor o en contra de [tema]?". El binari força la presa de postura. Un cop ha dit "a favor", li pregunto: "Per quina raó? Dona'm un exemple de la teva vida." Aquesta seqüència de 3 passos (postura → raó → exemple) és la bastida mínima per a l'article d'opinió A1.

**H2 — Detectar l'encavalcament HCL.**
Quan demano "Argumenta per què creus que [tema] és important" i l'alumne respon "Perquè és molt important i tothom ho ha de saber", sé que confon argumentar amb descriure. Li mostro la diferència amb un modelatge en veu alta (Think Aloud, MALL): "Mira com ho faig jo: 'Crec que X és important perquè [dada concreta]. Per exemple, [cas real].' Ara fes-ho tu." El modelatge és la bastida prèvia a l'escriptura autònoma.

**H3 — Nouvingut B1 amb sabers del país d'origen.**
Per a alumnat nouvingut que ja domina el català conversacional però té dificultats amb l'argumentació formal, accepto evidències de la seva cultura d'origen com a argument vàlid ("A la meva família fem X perquè…"). Aquesta estratègia té dos avantatges: l'alumne té contingut i la classe guanya diversitat de punts de vista. La bastida de connectors d'aquest instrument és especialment útil aquí perquè és explícita i gradada.

**H4 — La tesi al final (estructura invertida).**
Quan un alumne escriu 3 paràgrafs d'arguments i acaba amb "Per tot això, crec que X", la tesi és al final en lloc de ser al principi. No és un error de contingut: és un error de superestructura del gènere. Li demano que llegeixi només el primer paràgraf en veu alta i li pregunto: "Saps de seguida què defensa l'autor?". Si la resposta és "no", l'exercici és clar: mou la tesi al principi i comprova si el text guanya o perd.

**H5 — Connectors com a termòmetre del nivell.**
Reviso ràpidament els connectors que usa l'alumne: si tots els arguments comencen amb "perquè" o "però", és A1-A2 funcional. Si varia entre "en primer lloc", "a més", "per tant", és B1. Si usa "tanmateix", "no obstant", "en conseqüència", és B2. Aquesta lectura de 30 segons dels connectors em dóna el MECR real de l'alumne millor que cap test formal, i m'indica quin nivell de bastida de connectors necessita l'adaptació.

## Fonts principals

- MALL (Model d'Aprenentatge de Llengües i Literacitat): gradació MECR, connectors canònics per nivell.
- Cummins (2000): CALP i BICS — argumentació com a indicador de pensament acadèmic.
- Camps & Dolz (1995): didàctica de la seqüència argumentativa.
- Decret 175/2022 (currículum Catalunya): competències comunicatives i pensament crític.
