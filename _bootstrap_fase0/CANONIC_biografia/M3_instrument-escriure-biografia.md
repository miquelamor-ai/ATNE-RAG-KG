---
modul: M3
titol: "Escriure/adaptar una biografia"
tipus: genere-discursiu
categoria_principal: generes
categories_secundaries: []
descripcio: "Instrument per adaptar o generar una biografia: narració cronològica de la vida d'una persona real, centrada en 3-5 fets rellevants i el seu llegat. HCL Narrar + Explicar (llegat B1+). No s'adapta a pre-A1. Rúbrica gradada 8 passos × 5 nivells MECR (A1→C1)."
mecr_range: [A1, A2, B1, B2, C1]
agent_roles: [adapter, generator]
genre_key: biografia
translanguaging: false
multimodal: false
moduls_relacionats: [M3]
variables_configurables:
  fase_lectora: [alfabetica_emergent, alfabetica_fluida]
skill_meta: write-biografia@corpusFJE/skills/generes/write-biografia
review_status: pilot-fusio-3
version: 4.0.0-canonic
generat_at: 2026-05-26
actualitzat_at: 2026-05-26
notebooklm_review:
  data: 2026-05-26
  veredicte: si-amb-correccions-menors
  aplicades_des_d_inici: [patro-canonic-pilots-fase-a, aclariment-us-lectura-vs-produccio-C1, fidelitat-gradada-C2, variabilitat-cardinal-passos-D3]
  aplicades_post_review: [numeracio-C1-romans-admissibles-font, especulacio-C1-inferencia-historiografica-explicita]
  comentari_key: "La biografia és l'instrument del corpus que millor resol la transició de la HCL Narrar a la HCL Explicar mitjançant la bastida estructural del llegat."
---

# Escriure/adaptar una biografia

## Descripció

La biografia és una narració cronològica de la vida d'una persona real, centrada en els fets més rellevants per entendre el seu llegat. El seu tret definitori és l'**ordre cronològic estricte** i la **separació neta entre fets i llegat**: primer es narra el que va fer, i al final s'explica per què importa.

**Tipologia MALL**: Narrativa (narrar fets reals en el temps).
**HCL principal**: Narrar — seqüenciar fets biogràfics reals en ordre cronològic.
**HCL secundàries**: Descriure context i entorn (A2+) · Explicar causes del llegat i connexió amb el present (B1+) · Argumentar des d'una perspectiva historiogràfica (C1+).
**No s'adapta a pre-A1**: la biografia requereix el temps com a categoria abstracta (cronologia, context historicogeogràfic, llegat diferit — "per què importa avui"). Cap d'aquests conceptes es pot construir per via visual i concreta sense base lingüística mínima. A diferència del conte, no hi ha mediació adulta que substitueixi la comprensió temporal abstracta. (Decisió 6 canònica Fase B.)

**Connexions MALL transversals:**
- *Narrar en el temps*: la biografia és el gènere canònic per treballar la cronologia. Els connectors temporals (primer, llavors, l'any..., quan tenia... anys, finalment) són el vocabulari estructural del gènere i la bastida principal de la comprensió.
- *Context com a ancoratge*: sense "a Alemanya, fa 150 anys", l'alumne no pot situar la figura ni construir significat. El context breu però present és imprescindible per a la comprensió, especialment per a alumnat nouvingut.
- *Llegat com a transició HCL Narrar → Explicar*: a B1+, el llegat no és una descripció ("és famosa per...") sinó una explicació ("la seva contribució és important perquè..."). Marca el pas de contar fets a explicar causes i conseqüències.

**Aclariment d'ús — què descriu aquesta rúbrica.**
Aquesta rúbrica descriu la **biografia adaptada per a la LECTURA** de l'alumne (el que el docent presenta perquè l'alumne llegeixi). **No descriu la producció autònoma de l'alumne** — la producció biogràfica de l'alumne s'avalua amb un derivat propi. Principi pedagògic MALL: l'alumne llegeix models al màxim del seu abast i en produeix els seus textos.
**Sub-granularitat dins de A1**: es treballa amb `fase_lectora: [alfabetica_emergent, alfabetica_fluida]`; no hi ha nivell logografic perquè el gènere requereix base lecto-escriptora mínima.

## Detecció

**Senyals docent** (quan adaptar a biografia):
- El text font és una biografia que cal simplificar per al nivell de l'alumne.
- La unitat de història, ciències, art, música o llengua treballa una figura rellevant.
- L'alumne ha de llegir la vida d'una persona per entendre el seu obra o impacte.
- La matèria demana comprensió del context vital d'una persona per situar el seu llegat.

**Senyals alumne** (que indica que necessita bastida biogràfica):
- Narra els fets sense ordre temporal: barreja infància i etapa adulta.
- Usa "i llavors, i llavors..." sense marcar el pas del temps amb dates o connectors.
- Inclou detalls trivials i oblida el llegat.
- Confon la vida real (biografia) amb la ficció autobiogràfica.

**Context favorable**:
- Història, Ciències Naturals, Música, Art, Llengua: qualsevol unitat centrada en una figura.
- Alumnat nouvingut A1-A2: l'estructura cronològica és universal i accessible sense conèixer la tradició cultural específica.

**Anti-senyals** (quan NO adaptar a biografia):
- El text font és narratiu de ficció → conte.
- El text no tracta d'una persona real sinó d'un personatge arquetípic o simbòlic → fàbula.
- Pre-A1: la comprensió del temps com a categoria abstracta no és accessible sense base lingüística.

## Modulació per nivell

| Pas | Dimensió | A1<br>Inicial | A2<br>Funcional | B1<br>Estratègic | B2<br>Acadèmic | C1+<br>Crític |
|---|---|---|---|---|---|---|
| **1. Ordre cronològic** | Seqüència i coherència | Fets ordenats en el temps, del més antic al més recent. Sense flashbacks. | Fets ordenats cronològicament amb connectors temporals simples. | Cronologia estricta respectada al llarg de tot el text. | Cronologia precisa amb relació causa-efecte entre fets. | Cronologia completa. Pot incloure una retrospectiva crítica del llegat al final. |
| **2. Dates** | Format i precisió | Dates relatives: "fa molts anys", "quan era jove", "l'any passat dels seus besavis". | Dates completes o any exacte: "el 1879", "el 15 de març de 1879". | Dates completes: "el 15 de març de 1879". Context temporal breu integrat. | Dates completes amb context historicogeogràfic integrat als paràgrafs. | Dates amb referència al context historiogràfic quan és rellevant per al llegat. |
| **3. Context (lloc i època)** | Situació espai-temps | Context d'1 frase: "a Alemanya, fa molt de temps". | Context de 2 frases: país, època, context familiar breu. | Context breu però present: lloc + any + 1 frase sobre el context social. | Context historicogeogràfic integrat als paràgrafs de fets. | Context historiogràfic crític: la figura en relació amb el seu temps i amb el nostre. |
| **4. Selecció de fets principals** | Nombre i rellevància | 2-3 fets simples, un per frase. Ordenats cronològicament. | 3 fets principals, un per paràgraf o dues frases cadascun. | 3-4 fets seleccionats per rellevància per al llegat. Jerarquització implícita. | 4-5 fets amb context causal. Selecció justificada implícitament per la seva relació amb el llegat. | 5 fets amb perspectiva historiogràfica. Pot incloure reflexió sobre la selecció mateixa (quins fets es recorden i per qué). |
| **5. Connectors temporals** | Varietat i precisió | "Primer", "després", "al final". | "L'any...", "quan tenia... anys", "més tard". | "En aquell moment", "com a conseqüència", "a partir d'aleshores". | Connectors causals i temporals variats i precisos. | Connectors elaborats amb matís cronològic o causal complex. |
| **6. Llegat** | Extensió i profunditat | 1 frase: "Per això, aquesta persona és important." | 1-2 frases amb connector: "per això, avui... és recordada per..." | 2-3 frases. Distinció clara entre fets i llegat. Connector explicatiu ("la seva contribució és important perquè..."). | Llegat argumentat (3-4 frases). Connexió explícita entre el context de la figura i el context actual. | Llegat crític (4-5 frases): pot incloure controvèrsies, revisions historiogràfiques o perspectives múltiples. |
| **7. Criteris transversals** | Especulació | Cap especulació sobre motivacions íntimes ("potser pensava que...", "probablement sentia..."). Només fets verificables. | Idem. | Idem. Les motivacions s'expliciten per fonts (cites documentades), no per inferència. | Idem. | La inferència historiogràfica és admissible si s'explicita ("Segons els historiadors...", "Els indicis suggereixen que..."). L'especulació íntima sense evidència segueix prohibida. |
|  | Numeració | Sense números romans per a segles. Usar "al segle XX" o "fa cent anys". | Idem. Dates en xifres aràbigues. | Idem. | Idem. | Números romans admissibles si el text font els conté i el context historiogràfic ho requereix. |
|  | Fidelitat al text font | Fidelitat als fets nuclears: qui és la persona, quins fets principals, quin llegat. | Fidelitat als fets i al llegat essencial. | Fidelitat als fets, al llegat i al to factual del text original. | Fidelitat als fets, al llegat, al context historiogràfic i al to. | Fidelitat a la complexitat crítica del text original, incloent matisos i controvèrsies. |
| **8. Autoavaluació metacognitiva** | Reflexió sobre el procés | "He escrit qui és la persona, 2 coses que va fer i per qué és important." | "He explicat la seva vida en ordre cronològic i he inclòs dates." | "He inclòs 3-4 fets principals amb context. He separat els fets del llegat." | "He argumentat el llegat amb referència al context actual. He revisat que tots els fets estiguin ordenats cronològicament." | "He presentat la figura amb perspectiva crítica i he contextualitzat el llegat en el debat historiogràfic. He revisat que no hi hagi especulació sense evidència." |

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
| 1 Ordre cronològic — Seqüència | `structural` + `binary` | no | detectar flashbacks (connectos retrospectius: "però tornem a..."); verificar que la seqüència és cronològica |
| 2 Dates — Format i precisió | `binary` + `qualitative` | no | binary: presència de dates (any o data completa A2+); qualitative: format correcte per nivell (relatiu A1, absolut A2+) |
| 3 Context — Situació espai-temps | `qualitative` + `countable` | no | LLM-jutge: presència i suficiència del context (lloc + època); comptar frases de context per paràgraf |
| 4 Selecció de fets — Nombre i rellevància | `countable` + `qualitative` | no | comptar fets principals (verificar entre 2 i 5); LLM-jutge: rellevància dels fets per al llegat |
| 5 Connectors temporals — Varietat | `enumerable` + `qualitative` | no | detectar i classificar connectors temporals per tipus (simple/causal/elaborat); verificar coherència amb el nivell |
| 6 Llegat — Extensió i profunditat | `qualitative` + `countable` | no | binary: llegat present/absent; qualitative: LLM-jutge sobre la distinció fets/llegat i la profunditat argumentativa per nivell |
| 7.1 Criteris — Especulació | `binary` + `qualitative` | no | detectar patrons especulatius ("potser pensava", "probablement sentia", "devia creure"); LLM-jutge per a casos ambigus |
| 7.2 Criteris — Numeració | `binary` | no | regex: detectar números romans en context de segle (I, II, III, IV... precedits de "segle") |
| 7.3 Criteris — Fidelitat al text font | `cross_source` | **sí** (si adaptació) | comparació fets nuclears originals vs adaptats; verificació que el llegat es conserva; gradació per nivell: A1 fets+llegat basic; B1+ context+to; C1 complexitat crítica |
| 8 Autoavaluació metacognitiva | `metacognitive` | no | derivar a vista d'autoavaluació alumne + registre docent |

**Notes:**
- Ordre cronològic (Pas 1) és parcialment automatitzable: detecció de flashbacks per connectors retrospectius.
- Especulació (Pas 7.1) és detectable per patrons lingüístics però requereix LLM-jutge per a casos ambigus (l'alumne pot usar el condicional per a fets no verificats sense specular).
- Llegat (Pas 6) és el descriptor de major càrrega qualitativa: distinció fets/llegat és una competència de HCL que requereix judici.

## Heurístiques docent

**H1 — La línia de temps com a bastida.**
Abans d'escriure, proposo a l'alumne que faci una línia de temps amb 3-5 dates clau en un full en blanc. Un cop la línia és feta, la biografia gairebé s'escriu sola: cada punt de la línia és un paràgraf. Funciona especialment bé a A2-B1: externalitza la cronologia perquè l'alumne pugui centrar-se en la redacció sense perdre l'ordre.

**H2 — "Per qué importa avui?" com a brúixola del llegat.**
El llegat és la part que més costa als alumnes, que tendeixen a sumar fets sense reflexionar sobre la seva importància. La pregunta clau és: "Si aquesta persona no hagués existit, qué seria diferent avui?" La resposta és el llegat. A A1 és una frase. A B2+ és un paràgraf argumentat amb referència al context actual.

**H3 — Selecció de fets: la regla dels 5.**
Per a textos biogràfics complexos, demano a l'alumne que subratlli els 5 fets que li semblen més importants. Llavors en triem 3 junts, discutint quins es queden fora i per qué. El procés de selecció és un exercici de jerarquització que prepara la comprensió del llegat: si un fet no aporta res al llegat, no hi va.

**H4 — Context mínim, no màxim.**
L'error més freqüent és posar massa context i pocs fets. La regla és: 1 frase de context per paràgraf, la resta de fets. El context és el marc; els fets són el quadre. Si el context ocupa més que els fets, cal podar.

**H5 — Dates completes vs. dates relatives.**
A A1-A2, les dates completes poden intimidar o bloquejar l'alumne nouvingut. L'alternativa: dates relatives ("fa 150 anys", "quan l'avi dels vostres avis era nen"). A B1+, les dates completes són necessàries per a la precisió historiogràfica. La gradació és clara: de relatiu a absolut amb el nivell.

## Fonts principals

- MALL (Model d'Aprenentatge de Llengües i Literacitat): HCL Narrar + Explicar, seqüenciació temporal, connectors.
- Labov, W. i Waletzky, J. (1967): estructura narrativa canònica aplicada a textos biogràfics; seqüenciació i avaluació del relat.
- Decret 175/2022 (currículum Catalunya): competència en comunicació lingüística (dimensió literària i cultural) i competència en consciència i expressions culturals.
