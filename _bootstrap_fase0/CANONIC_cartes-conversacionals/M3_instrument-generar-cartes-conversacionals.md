---
modul: M3
titol: "Generar cartes conversacionals"
tipus: instrument
categoria_principal: mediacio
categories_secundaries: []
descripcio: "Instrument per generar cartes conversacionals: rols + iniciadors per a debat estructurat (oral o escrit). No s'aplica a pre-A1/A1 (interaccio oral requereix suport docent directe). 2 tipus de conversa: exploratoria (A2-B1) i disputativa (B2+). 4 rols: Proposador/a, Objector/a, Mediador/a, Sintetitzador/a. Maxim 3 iniciadors per rol. Sintetitzador sempre amb element obert. Rubrica gradada 5 passos x 4 nivells MECR (A2->C1)."
mecr_range: [A2, B1, B2, C1]
agent_roles: [generator]
complement_key: cartes_conversacionals
translanguaging: false
multimodal: false
moduls_relacionats: [M2, M3]
variables_configurables: {}
skill_meta: generate-cartes-conversacionals@corpusFJE/skills/mediacio/generate-cartes-conversacionals
review_status: pilot-fusio-8
version: 4.0.0-canonic
generat_at: 2026-05-26
actualitzat_at: 2026-05-26
notebooklm_review:
  data: 2026-05-26
  veredicte: si-amb-correccions-menors
  aplicades_des_d_inici: [patro-canonic-pilots-fase-a, aclariment-us-lectura-vs-produccio-C1, variabilitat-cardinal-passos-D3, modulacio-per-perfil-D1]
  aplicades_post_review: [b10-cartes-c3-a2-element-obert-proposador-aclariment]
  comentari_key: "C1-pas6-7-rebutjat-categoria-instruments-5-passos; C2-c1-vs-b2-rebutjat-ja-diferenciat-pas3"
---

# Generar cartes conversacionals

## Descripció

Les cartes conversacionals bastiden la **participació oral** (o escrita en format debat) donant a cada alumne un **repertori d'iniciadors** associats al seu rol dins la conversa. Cada carta = 1 rol + descripció de la funció comunicativa + màxim 3 iniciadors. El rol allibera l'alumne de la por a "dir el que penso" — és el personatge qui argumenta, no ell. Especialment rellevant per a alumnat nouvingut o NESE amb baixa seguretat oral.

**Tipologia MALL**: Mediació (bastida de producció oral/dialogada).
**HCL principals**: Argumentar · Contrargumentar · Sintetitzar · Mediar.
**Principi rector**: Els iniciadors han de ser **específics de la pregunta de debat** del text. Si els iniciadors serveixen per a qualsevol debat de qualsevol tema, cal tornar a escriure'ls. La connexió amb el text font és la garantia de pertinença.

**2 tipus de conversa:**
- **Exploratòria** (A2-B1): posicions obertes, errors tolerats, raonament visible. L'objectiu és explorar conjuntament, no guanyar. Estil: "Jo penso que... però potser..." "I si...?".
- **Disputativa** (B2+): posicions definides, argumentació formal, citació d'evidències. L'objectiu és defensar una postura amb evidències. Estil: "Segons el text...", "D'acord amb...", "Però si observem que...".

**4 rols estàndard (B1+):**
- **Proposador/a**: formula la tesi i els arguments principals. Inicia la conversa.
- **Objector/a**: qüestiona la tesi. Planteja contraarguments i punts febles.
- **Mediador/a**: equilibra les posicions. Busca acord parcial i formula preguntes.
- **Sintetitzador/a**: tanca la ronda. Resumeix el que s'ha dit i formula l'element obert.

**Pre-A1/A1: NO generar.** La interacció oral a aquests nivells requereix suport docent directe en temps real (mediació de torn, reformulació, andamiatge). Les cartes conversacionals presuposen l'autonomia d'inici comunicatiu que s'assoleix a A2.

**Taulell de debat companion** (B1+): el MALL recomana combinar les cartes amb un taulell compartit (Arguments a favor / Arguments en contra / Punts d'acord / Preguntes obertes). Externalitza el raonament col·lectiu del grup.

**Connexions MALL transversals:**
- *Rol com a identitat comunicativa provisional*: el rol és una màscara pedagògica que permet a l'alumne experimentar posicions comunicatives que no necessàriament comparteix. L'Objector/a aprèn a contrargumentar; el Mediador/a aprèn a equilibrar. Aquesta experimentació de rols és la base del pensament dialèctic.
- *Iniciador com a frase de posada en marxa*: la por al silenci o al "no sé com dir-ho" és la barrera principal de la participació oral. Un iniciador concret ("Jo crec que... perquè...") desbloqueja el primer torn. Un cop l'alumne ha dit la primera frase, la conversa flueix.
- *Sintetitzador com a metacognició col·lectiva*: el rol del Sintetitzador és l'única funció metacognitiva del grup. "El que no hem resolt és ___" externalitza la consciència dels límits del coneixement col·lectiu. A C1, inclou la dimensió de fiabilitat de les fonts.

**Aclariment d'ús — què descriu aquesta rúbrica.**
Aquesta rúbrica descriu les **cartes conversacionals que es generen per bastir el debat** (MEDIACIÓ DE LA PRODUCCIÓ ORAL). **No descriu l'avaluació del debat ni la qualitat de la participació de l'alumne**: el docent observa si l'alumne usa les cartes i si la conversa avança amb estructura.

## Detecció

**Senyals docent** (quan activar el complement):
- Ha activat "Cartes conversacionals" al Pas 2.
- Vol estructurar un debat, una discussió o una activitat de producció oral argumentada.
- Treballa la HCL Argumentar amb suport estructural per a alumnes que no saben "com dir que no estan d'acord".

**Senyals alumne** (que indica que necessita el suport):
- Es bloqueja a l'hora de prendre la paraula: silenci llarg, mirada al terra.
- No sap com discrepar respectuosament ("no és que no estigui d'acord, però...").
- Les discussions deriven sense producte: tothom parla però ningú avança.
- Usa sempre la mateixa estructura de frase per a tot (solo "perquè sí").

**Context favorable**:
- Unitat TILC on el text genera debat (textos d'opinió, textos científics amb controvèrsia, dilemes ètics).
- Activitat prèvia a una producció escrita argumentativa: el debat oral bastit amb cartes prepara la producció.
- Grup multicultural: les cartes equiparen la participació eliminant la norma social de "el qui parla molt domina".

**Anti-senyals** (quan NO activar):
- Pre-A1/A1: NO generar (interacció oral requereix suport docent en temps real).
- Objectiu és preguntes de comprensió → `preguntes_comprensio`.
- Objectiu és aprofundiment cognitiu post-lectura → `activitats_aprofundiment`.
- El debat és totalment lliure sense estructura de rols → discussió docent directa.

## Modulació per nivell

| Pas | Dimensió | Pre-A1/A1 — No aplicable | A2 Funcional | B1 Estratègic | B2 Acadèmic | C1 Crític |
|---|---|---|---|---|---|---|
| **1. Rols actius** | Nombre i complexitat | NO generar. | 2 rols: Proposador/a + Objector/a. Format simplificat per parelles. | 3-4 rols: Proposador + Objector + Mediador + Sintetitzador. | 4 rols complets amb registre formal i terminologia de debat. | 4 rols + capa metacognitiva al Sintetitzador (detecció de biaixos i punts cecs). |
| **2. Nombre d'iniciadors per rol** | Repertori lingüístic | NO generar. | 2 iniciadors per rol. Frases curtes i segures (Jo penso que ___ / Jo crec que no ___). | 3 iniciadors per rol. Frases completes adaptades a la HCL del rol (Argumentar, Contrargumentar, Mediar). | 3 iniciadors amb vocabulari CALP i connectors argumentals (Malgrat que..., Tenint en compte que...). | 3 iniciadors dialèctics o retòrics que qüestionen la postura contrària (Si fos cert que X, llavors...). |
| **3. Tipus de conversa** | Registre i objectiu | NO generar. | Exploratòria: posicions obertes, errors tolerats, raonament visible. "I si...?" "Potser...". | Exploratòria o disputativa: comença explorant, pot formalitzar-se si el grup avança. | Disputativa: posicions definides, argumentació formal, citació d'evidències del text. | Disputativa amb metacognició: detecció de biaixos, qüestionament de la fiabilitat de les fonts. |
| **4. Especificitat dels iniciadors** | Connexió amb el text | NO generar. | Iniciadors genèrics ("Jo penso que ___"). Curts i segurs. Fàcils de dir. | Iniciadors específics de la pregunta de debat del text. Causals i justificatius ("El text diu que... i per això crec que..."). | Iniciadors que inclouen citació del text ("Segons el text...", "D'acord amb..."). Registre formal. | Iniciadors que qüestionen, matisen i detecten biaixos ("Però si pensem que X, el text podria estar ignorant..."). |
| **5. Element obert al Sintetitzador** | Metareflexió del grup | NO generar. | "Hem dit ___. Algú vol afegir alguna cosa?" (Element obert simple). | "La conclusió del grup és ___. El que no hem resolt és ___." (Tancament + obertura). | "El que no hem resolt és ___. Per resoldre-ho caldria saber ___." (Apertura epistemica). | "El que queda obert és ___. Per respondre-ho, caldria contrastar amb ___ i revisar si els nostres arguments son fiables." |

## Metadades de cel·la (per a `build_skills.py`)

**Tipus de descriptor:**
- `binary` — "compleix / no compleix".
- `qualitative` — requereix judici huma o LLM-jutge.
- `countable` — llindar quantitatiu verificable mecanicament.
- `structural` — requereix analisi sintatica o discursiva.
- `metacognitive` — descriptor de proces en primera persona.

| Pas / Dimensió | Tipus | requires_source_text | validation_hint |
|---|---|---|---|
| 1 Rols actius | `binary` + `countable` | no | binary: presencia del Sintetitzador des de B1+; countable: A2 = 2 rols; B1 = 3-4 rols; B2-C1 = 4 rols; error crític: generar cartes per a pre-A1/A1 |
| 2 Nombre d'iniciadors per rol | `countable` | no | countable: ≤3 iniciadors per rol en tots els nivells; error: 4 o mes iniciadors per rol (sobrecàrrega) |
| 3 Tipus de conversa | `binary` | no | binary: A2-B1 = exploratòria (detectar indicadors: "potser", "i si", "penso que"); B2-C1 = disputativa (detectar: "Segons el text", "D'acord amb", "citació", "evidència") |
| 4 Especificitat dels iniciadors | `qualitative` | **si** | LLM-jutge: iniciadors específics de la pregunta de debat del text (positiu) o genèrics que serveixen per a qualsevol debat (negatiu — error crític); cross_source: verificar que els iniciadors fan referència al contingut o pregunta del text font |
| 5 Element obert al Sintetitzador | `binary` + `qualitative` | no | binary: B1+: presencia d'element obert al rol Sintetitzador; A2: presencia d'invitació a afegir integrada al tancament del Proposador/a (no hi ha rol Sintetitzador a A2 — la funció és informal); qualitative: LLM-jutge sobre si l'element obert obre genuïnament la reflexió o és una frase de tancament disfressada |

**Notes:**
- Error crític: generar per a pre-A1/A1. Detectar per MECR declarat al perfil.
- Error frequent: iniciadors genèrics. Detectar per LLM-jutge: si l'iniciador funciona per a qualsevol debat independentment del text → error.
- Màxim 3 iniciadors per rol: si n'hi ha 4 o més, l'alumne es perd. Detectar per countable.
- Sintetitzador sense element obert: error pedagògic significatiu (talla la metacognició col·lectiva). Detectar per binary.

## Heurístiques docent

**H1 — La pregunta de debat és el centre.**
Els iniciadors han de ser específics de la pregunta de debat que surt del text. Si els iniciadors serveixen per a qualsevol debat de qualsevol tema ("Jo crec que sí" / "Jo crec que no"), cal tornar a escriure'ls. La prova: "Podria un alumne usar aquest iniciador en un debat sobre un tema completament diferent?" Si la resposta és sí, l'iniciador és massa genèric.

**H2 — Proposador + Objector és suficient per a A2.**
No cal els 4 rols des del principi. Dues parelles (Proposa / Respon) ja estructuren la conversa exploratòria sense sobrecarregar l'alumne amb múltiples funcions simultànies. La complexitat de rols creix amb el MECR i amb la pràctica prèvia del format.

**H3 — El Sintetitzador no tanca: obre.**
Quan formo el grup, explico explícitament que la funció del Sintetitzador no és "acabar" el debat sinó "veure fins on hem arribat i on no". "El que no hem resolt és..." és la frase més valuosa del debat: demostra que el grup ha pensat prou com per saber que no ho sap tot.

**H4 — Rol com a màscara pedagògica.**
Quan un alumne tímid o nouvingut agafa la carta de Proposador/a, no és "ell" qui argumenta — és el Proposador/a. Aquesta distància permet prendre riscos comunicatius que d'altra manera serien inhibits per la por al judici social. Assegura't que els rols rotin entre sessions perquè tots els alumnes practiquin totes les funcions comunicatives.

**H5 — Taulell de debat companion (B1+).**
Per a B1+, combina les cartes amb un taulell compartit de paper (Arguments a favor / Arguments en contra / Punts d'acord / Preguntes obertes). A mesura que el debat avança, un alumne designat anota les idees al taulell. Aquesta externalització del raonament col·lectiu fa visible el procés d'argumentació i permet al Sintetitzador fer la seva feina amb millor informació.

## Fonts principals

- MALL (Model d'Aprenentatge de Llengues i Literacitat): HCL Argumentar, cartes amb etiquetes lingüístiques, conversa exploratòria vs. disputativa.
- Sacks, H., Schegloff, E.A. & Jefferson, G. (1974): "A simplest systematics for the organization of turn-taking for conversation" — seqüències d'adjacència i torns de paraula.
- Mercer, N. (2000): *Words and Minds* — conversa exploratòria com a eines cognitives col·lectives.
- Decret 175/2022 (curriculum Catalunya): competencia en comunicacio oral, participacio democratica i pensament critic.
