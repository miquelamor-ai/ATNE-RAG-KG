---
modul: M3
titol: "Escriure/adaptar una entrada enciclopèdica"
tipus: instrument
categoria_principal: generes
categories_secundaries: []
descripcio: "Instrument per adaptar o generar una entrada enciclopèdica: definició nuclear amb fórmula categoria+especificitat, explicació ampliada i exemple concret. HCL Descriure (definir). No s'adapta a pre-A1. Rúbrica gradada 6 passos × 5 nivells MECR (A1→C1)."
mecr_range: [A1, A2, B1, B2, C1]
agent_roles: [adapter, generator]
genre_key: enciclopedic
translanguaging: false
multimodal: false
moduls_relacionats: [M3]
variables_configurables:
  fase_lectora: [alfabetica_emergent, alfabetica_fluida]
skill_meta: write-enciclopedic@corpusFJE/skills/generes/write-enciclopedic
review_status: pilot-fusio-4
version: 4.0.0-canonic
generat_at: 2026-05-26
actualitzat_at: 2026-05-26
notebooklm_review:
  data: 2026-05-26
  veredicte: si-amb-correccions-menors
  aplicades_des_d_inici: [patro-canonic-pilots-fase-a, aclariment-us-lectura-vs-produccio-C1, fidelitat-gradada-C2, variabilitat-cardinal-passos-D3]
  aplicades_post_review: [pas2-binary-pur-matisos-al-pas5, pas62-c1-remissio-integrada, metadada-pas64-qualitative, validacio-hint-categoria-articles]
  comentari_key: "L'entrada enciclopèdica és l'instrument del corpus que millor operacionalitza la fórmula categoria+especificitat com a competència acadèmica transferible a totes les matèries."
---

# Escriure/adaptar una entrada enciclopèdica

## Descripció

L'entrada enciclopèdica defineix un terme amb la màxima precisió possible, usant la fórmula **"categoria + especificitat"** i el contextualitza amb una explicació ampliada i un exemple concret. El seu tret definitori és l'absència de circularitat: la definició no pot usar el terme ni paraules de la mateixa arrel per explicar-se.

**Tipologia MALL**: Expositiva/Descriptiva.
**HCL principal**: Descriure — definir i caracteritzar un terme amb precisió i sense circularitat.
**HCL secundàries**: Explicar — relació entre característiques del terme (B1+).
**No s'adapta a pre-A1**: l'entrada enciclopèdica requereix la comprensió del concepte abstracte **"categoria"** — ser capaç de situar un terme dins d'una classe superior ("la balena és un mamífer" implica saber que mamífer és una categoria que inclou la balena, no només que la balena és un animal). La fórmula `categoria + especificitat` és una operació de classificació abstracta inaccessible sense base lecto-escriptora mínima i sense coneixement de les categories disciplinars. (Decisió 6 canònica Fase B.)

**Connexions MALL transversals:**
- *Definició com a base del CALP*: aprendre a construir una definició precisa és aprendre la lògica del pensament científic. La fórmula "és un [categoria] que [especificitat]" és exportable a totes les matèries i és una de les competències acadèmiques més transferibles del currículum.
- *Exemple com a ancoratge ZDP*: sense un exemple concret i proper, la definició abstracta no s'integra al coneixement previ de l'alumne. L'exemple és el pont entre la definició formal i la comprensió real.
- *Absència de circularitat com a criteri de qualitat*: detectar que una definició és circular ("el fotosíntesi és el procés de fotosíntesi...") és una competència metacognitiva. El "test de la circularitat" és una eina de pensament crític exportable a totes les matèries.

**Aclariment d'ús — què descriu aquesta rúbrica.**
Aquesta rúbrica descriu l'**entrada enciclopèdica adaptada per a la LECTURA** de l'alumne. **No descriu la producció autònoma de l'alumne** — la producció és tasca d'un derivat propi. Principi pedagògic MALL: l'alumne llegeix models al màxim del seu abast.
**Sub-granularitat dins de A1**: es treballa amb `fase_lectora: [alfabetica_emergent, alfabetica_fluida]`; no hi ha nivell logogràfic perquè el gènere requereix base lecto-escriptora mínima.

## Detecció

**Senyals docent** (quan adaptar a entrada enciclopèdica):
- El text font és una entrada d'enciclopèdia, un diccionari especialitzat, un glossari curricular o una fitxa terminològica.
- La unitat de qualsevol matèria treballa terminologia nova que l'alumne ha d'interioritzar i usar amb precisió.
- L'alumne ha de llegir per aprendre a definir un terme, no per aprendre un procés o un argument.
- La matèria demana que l'alumne pugui diferenciar un terme d'altri terme proper (contraexemple).

**Senyals alumne** (que indica que necessita bastida enciclopèdica):
- No distingeix terme de definició ("fotosíntesi és quan les plantes...").
- Usa el terme per definir-se ("la democràcia és un sistema democràtic...").
- Dona exemples en lloc de definir ("l'osmosi és com quan el sucre es dissol...").
- La definició és tan general que no exclou res ("l'animal és un ésser viu").

**Context favorable**:
- Totes les matèries en unitats d'introducció de terminologia nova.
- Ciències Naturals: termes biològics, químics, físics.
- Ciències Socials: termes geogràfics, econòmics, històrics i polítics.
- Llengua i Literatura: termes retòrics, gramaticals i literaris.

**Anti-senyals** (quan NO adaptar a entrada enciclopèdica):
- El text presenta les característiques generals d'un objecte en ordre espacial → descripció.
- El text explica com funciona un fenomen → divulgatiu.
- El text narra la vida d'una persona → biografia.
- Pre-A1: la comprensió de la categoria com a classe abstracta no és accessible sense base lingüística.

## Modulació per nivell

| Pas | Dimensió | A1<br>Inicial | A2<br>Funcional | B1<br>Estratègic | B2<br>Acadèmic | C1<br>Crític |
|---|---|---|---|---|---|---|
| **1. Definició nuclear** | Precisió i estructura | 1 frase ≤10 paraules. Estructura: "X és un Y que Z." | 1 frase clara. Categoria + especificitat. Sense circularitat. | 1 frase precisa amb terminologia adequada. Sense circularitat ni sinònim com a definició. | 1 frase completa amb terminologia específica de la matèria. Pot delimitar el terme respecte a termes propers. | Definició nuclear rigorosa amb matisos terminològics i referència al debat si és rellevant. |
| **2. Absència de circularitat** | Coherència lògica | Test: la definició no usa el terme per definir-se. Criteri bàsic. | Definició que no usa el terme ni paraules de la mateixa arrel. | Definició sense circularitat i sense sinònim com a definició ("la democràcia és un govern popular" és circular si no s'explica "popular"). | Idem. La delimitació respecte a termes propers s'explicita a l'Explicació ampliada (Pas 5), no a la definició nuclear. | Idem. Si hi ha debat terminològic, es recull a l'Explicació ampliada (Pas 5). La definició nuclear segueix sent binary: no usa el terme ni arrels. |
| **3. Categoria primer** | Estructura lògica | Categoria explícita a la primera paraula de la definició: "és un animal / un lloc / un procés...". | Categoria clara: [Terme] és un [categoria] que [especificitat]. | Categoria i especificitat ben diferenciades. La categoria situa el terme dins d'una classe superordinal. | Categoria dins del camp lèxic de la matèria amb precisió disciplinar. | Categoria amb precisió i referència a la taxonomia disciplinar si escau. |
| **4. Exemple concret** | Accessibilitat i ancoratge | 1 exemple molt visual i quotidià. 1 frase. | 1 exemple concret pres del context immediat de l'alumne. Immediat a la definició. | Exemple concret + contraexemple si és útil per delimitar el concepte. | 1-2 exemples elaborats amb connexió explícita amb la definició. | Exemples variats. Pot incloure un exemple límit o de frontera que posi a prova la definició. |
| **5. Explicació ampliada** | Profunditat i coherència | 2-3 frases simples amb detalls addicionals del terme. Una característica per frase. | 3 frases amb detalls rellevants. Vocabulari accessible. | 3-4 frases amb relació entre característiques. 1 terme tècnic nou introduït. | Explicació amb múltiples característiques. Comparació amb termes propers. | Explicació completa amb matisos, variants i possibles debats sobre la delimitació del terme. |
| **6. Criteris transversals** | Llargada | Definició (1 frase) + 2-3 frases d'explicació + 1 exemple. | Definició (1 frase) + 3 frases + 1 exemple. | Definició + 3-4 frases + exemple + contraexemple si escau. | Definició + explicació (4-5 frases) + 1-2 exemples. | Text complet amb tots els matisos necessaris. |
|  | Sense remissions | Cap remissió a altres entrades ("vegeu també..."). | Idem. | Idem. | Idem. | Idem. La referència a termes relacionats, si escau, s'integra al cos de l'explicació sense remissió formal. |
|  | Sense etimologia inicial | L'etimologia no substitueix la definició. Si apareix, va darrere de la definició. | Idem. | Idem. | Idem. | L'etimologia pot aparèixer si aporta matisos al significat, però mai com a única definició. |
|  | Fidelitat al text font | Fidelitat a la categoria i al tret diferencial principals del terme. | Fidelitat a la categoria, al tret diferencial i a l'exemple. | Fidelitat a la categoria, al tret diferencial, a l'exemple i al to factual. | Fidelitat a la complexitat conceptual i al context disciplinar. | Fidelitat a la complexitat, als matisos i als debats si els hi ha. |
| **7. Autoavaluació metacognitiva** | Reflexió sobre el procés | "He escrit una frase que diu qué és el terme. He posat un exemple." | "He dit a quina categoria pertany el terme i qué el fa diferent. He posat un exemple." | "La meva definició no usa el terme per definir-se. He explicat 2-3 característiques." | "He delimitat el terme respecte a termes propers. He usat vocabulari específic de la matèria." | "He presentat el terme amb matisos, variants i possibles debats sobre la seva definició." |

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
| 1 Definició nuclear — Precisió i estructura | `structural` + `qualitative` | no | verificar estructura [Terme] és un [categoria] que [especificitat]; LLM-jutge sobre precisió i adequació al nivell |
| 2 Absència de circularitat — Coherència lògica | `binary` | no | detectar el terme o arrel del terme dins de la definició; regex sobre la primera frase |
| 3 Categoria primer — Estructura lògica | `binary` + `qualitative` | no | binary: categoria present a la primera frase (articles o determinants admissibles: "és un animal", "és una substància"); qualitative: categoria correcta i precisa per al nivell |
| 4 Exemple concret — Accessibilitat | `qualitative` + `binary` | no | binary: presència d'exemple; qualitative: LLM-jutge sobre concreció i accessibilitat |
| 5 Explicació ampliada — Profunditat | `countable` + `qualitative` | no | comptar frases d'explicació; LLM-jutge sobre relació entre característiques (B1+) |
| 6.1 Criteris — Llargada | `countable` | no | comptar frases totals per bloc (definició + explicació + exemple); verificar llindar per nivell |
| 6.2 Criteris — Sense remissions | `binary` | no | regex: detectar "vegeu", "vegeu també", "veure" com a remissions a altres entrades |
| 6.3 Criteris — Sense etimologia inicial | `structural` + `binary` | no | detectar si la primera frase és etimologia en lloc de definició; patrons: "prové del llatí", "del grec" |
| 6.4 Criteris — Fidelitat al text font | `cross_source` + `qualitative` | **sí** (si adaptació) | comparar categoria, tret diferencial i exemple original vs adaptat; LLM-jutge sobre fidelitat del to factual (B1+) |
| 7 Autoavaluació metacognitiva | `metacognitive` | no | derivar a vista d'autoavaluació alumne + registre docent |

**Notes:**
- Absència de circularitat (Pas 2) és el descriptor més automatitzable del corpus: és un binary pur per regex sobre la primera frase de la definició.
- Categoria primer (Pas 3): verificable estructuralment fins a A2 (la categoria apareix a la primera frase). A B1+ la qualitat de la categoria requereix LLM-jutge.
- Exemple concret (Pas 4): a A1-A2, la concreció és verificable (exemple quotidià vs exemple abstracte); a B1+ la connexió explícita amb la definició requereix LLM-jutge.

## Heurístiques docent

**H1 — La fórmula màgica.**
"El/La ___ és un/una [categoria] que [característica diferencial]." Dos passos: (1) identificar la categoria (quin tipus de cosa és?); (2) dir qué el fa diferent d'altres coses de la mateixa categoria. A A1 proposo que l'alumne triï la categoria d'una llista de 4-5 opcions que jo preparo per a la matèria.

**H2 — El test de la circularitat.**
"Si no coneixies aquesta paraula i llegeixes la teva definició, l'entendries?" Si la resposta és "no" o "potser", cal tornar a escriure. Una variant més explícita per a A1-A2: "Tapa el terme amb el dit. Llegeix la definició. Podries endevinar el terme? Si sí, la definició és bona."

**H3 — El contraexemple com a eina de precisió.**
A B1+, proposo: "Posa un exemple de [terme] i un exemple de [terme proper que NO és el terme]." El contraexemple força la precisió de la definició: si l'alumne no pot posar un contraexemple, la definició és massa àmplia. Exemple: "la balena és un mamífer (exemple) / el tauró no és un mamífer (contraexemple), per tant la definició de mamífer ha d'excloure el tauró".

## Fonts principals

- MALL (Model d'Aprenentatge de Llengües i Literacitat): HCL Descriure, definició com a competència acadèmica central del CALP.
- Vygotsky, L.S. (1978): *Mind in Society* — zona de desenvolupament proper; l'exemple concret com a ancoratge del concepte abstracte.
- Cassany, D. (1993): *La cuina de l'escriptura* — criteris de precisió i claredat en la definició de termes; la circularitat com a error de coherència.
- Decret 175/2022 (currículum Catalunya): competència en comunicació lingüística i competència científica.
