---
name: generar-cartes-conversacionals
description: Instrument per generar cartes conversacionals amb rols per a debat o conversa estructurada. 4 rols (Proposador, Objector, Mediador, Sintetitzador) amb iniciadors calibrats al MECR. A2 parelles simplificades. Pre-A1/A1 no generar. Correccions MALL 2026-05-17 aplicades.
type: instrument
categoria_principal: mediacio
categories_secundaries: []
mecr_range: [A2, B1, B2, C1]
agent_roles: [adapter, generator]
translanguaging: false
multimodal: false
skill_meta: generate-cartes-conversacionals@corpusFJE/skills/mediacio/generate-cartes-conversacionals
version: 2.0.0-bootstrap
---

# Generar cartes conversacionals — V2 Descriptiu

## Descripció

Les cartes conversacionals bastiden la participació oral (o escrita en format debat) donant a cada alumne un repertori d'iniciadors associats al seu **rol** dins la conversa. No són una llista de connectors genèrics: cada carta té un rol i uns iniciadors específics per a aquella funció comunicativa en el context del text treballat.

**Tipologia MALL**: Mediació comunicativa (bastides per a la interacció oral estructurada)
**HCL principals**: Argumentar · Justificar · Avaluar (progressió per rol i nivell)
**Dos tipus de conversa (MALL)**:
- **Conversa exploratòria** (A2-B1): raonament visible, posicions obertes, errors tolerats. "Pensar en veu alta junts."
- **Conversa disputativa** (B2+): posicions definides, argumentació formal, citació d'evidències.

**No generar a pre-A1/A1**: la interacció oral requereix suport docent directe en temps real; les cartes escrites no substitueixen la mediació adulta.

## Estructura canònica

### 4 rols estàndard

| Rol | Funció comunicativa |
|---|---|
| **Proposador/a** | Presenta una idea o posició i la justifica |
| **Objector/a** | Qüestiona, contraposa o afegeix un punt de vista diferent |
| **Mediador/a** | Dona la paraula, resumeix el que s'ha dit, busca consens |
| **Sintetitzador/a** | Al final, resumeix les idees principals i treu una conclusió |

*(A A2: només 2 rols en parelles: Proposador / Objector.)*

### Instrument companion: taulell de debat (B1+)

El MALL recomana un taulell de debat com a complement de les cartes a B1+: una superfície compartida (cartolina o pantalla) on el grup anota en temps real arguments a favor, arguments en contra, punts d'acord i preguntes obertes. Externalitza el raonament col·lectiu i fa visible l'evolució del debat.

## Modulació per nivell MECR

### Pre-A1 / A1 — NO generar

La interacció oral requereix bastides en temps real del docent: no hi ha iniciadors escrits que puguin substituir la mediació adulta directa. Retornar una nota per al docent indicant que la conversa estructurada és oral i mediada.

### A2 — Funcional

2 rols en parelles (Proposador / Objector). Iniciadors molt curts (màxim 8 paraules). Conversa exploratòria. Una sola pregunta de debat molt concreta i propera a l'experiència de l'alumne. Sense taulell de debat.

### B1 — Estratègic

3-4 rols. Frases completes per a cada HCL principal. Iniciadors per argumentar, justificar i reformular. Conversa exploratòria amb inici de disputativa. Taulell de debat recomanat. La pregunta de debat deriva del text adaptat (no genèrica).

### B2 — Acadèmic

4 rols. Registre formal. Iniciadors de debat acadèmic: contrastius, causals, hipotètics. Rol Objector inclou iniciadors de citació ("Segons el text...", "D'acord amb [autor]..."). Conversa disputativa. Taulell de debat obligatori.

### C1 — Crític

4 rols + metacognició del debat. Iniciadors de retòrica i detecció de biaix. Rol Sintetitzador inclou element de reflexió sobre el procés del debat ("El que hem dit sense evidència suficient és..."). Intertextualitat i contrast de fonts com a recursos dels rols avançats.

## Regles crítiques

**FER:**
- Comença sempre amb `## Cartes per al debat`.
- Usa colors o emojis per distingir els rols (millora el reconeixement visual, especialment A2-B1).
- Màxim 3 iniciadors per rol: menys és més.
- Els iniciadors han de ser específics de la pregunta de debat del text, no genèrics.
- Rol Sintetitzador: sempre incloure un element obert ("El que no hem resolt és...").
- B2+: rol Objector inclou iniciador de citació o evidència.

**NO FER:**
- ❌ Pre-A1/A1: no generar cartes escrites.
- ❌ Iniciadors genèrics aplicables a qualsevol debat (han de reflectir el text).
- ❌ Més de 3 iniciadors per rol.
- ❌ "Tanmateix" / "no obstant" a A2-B1.
- ❌ Cartes sense rol definit: cada carta = un rol = una funció.

## Connexions MALL

- **Cartes amb etiquetes lingüístiques**: denominació MALL de les cartes conversacionals. El nom "etiquetes" recorda que els iniciadors no son frases màgiques, sinó etiquetes que l'alumne omple amb el seu contingut.
- **Conversa exploratòria vs. disputativa**: distinció MALL fonamental. L'exploratòria és el pas previ; no és un fracàs, és el format correcte per a A2-B1. No forçar la disputativa fins que l'alumne tingui prou vocabulari argumentatiu.
- **Taulell de debat**: instrument companion que fa el raonament col·lectiu visible. Evita que el debat es redueixi a un intercanvi d'opinions sense memòria.

## Detecció

**Senyals docent** (quan activar cartes conversacionals):
- La unitat inclou un debat, una posada en comú o una discussió filosòfica/científica.
- L'alumnat participa en debats però uns pocs alumnes dominen i la resta calla.
- Cal estructurar la conversa perquè tothom tingui un rol i una funció.
- La llengua de la interacció oral (català) necessita bastida lèxica per fer-la accessible.
- S'ha activat el complement activitats_aprofundiment amb debat o reflexió argumentada.

**Senyals alumne** (que indica que necessita les cartes):
- Participa al debat amb "Sí / No / Depèn" sense elaborar.
- Usa "perquè és molt important" com a única justificació.
- No sap com cedlar la paraula o interrompre de forma cortesa.
- Nouvingut B1: té les idees però no el vocabulari d'interacció oral acadèmica en català.
- No sap com resumir el que s'ha dit fins ara en el debat.

**Context favorable**:
- Filosofia per a Nens (FpN) i discussió filosòfica: les cartes estructuren el diàleg socrètic.
- Ciències i Socials amb controvèrsies sociocientífiques: energia nuclear, canvi climàtic, IA.
- Llengua i Tutoria: debats sobre temes de convivència, valors, diversitat.
- Alumnat nouvingut B1+: les cartes fan accessible la participació en català sense improvisació.

**Anti-senyals** (quan NO activar):
- Pre-A1/A1: la interacció requereix mediació docent directa.
- Temps molt limitat: les cartes necessiten un mínim de 15-20 minuts per ser útils.
- Text molt curt sense contingut debatable → discussió oral directa sense estructura.
- L'alumnat ja participa fluidament: les cartes serien una restricció innecessària.

## Heurístiques docent

**H1 — El rol com a llibertat, no com a restricció**
Presento les cartes com "el teu superpower per avui": si tens la carta de Mediador/a, ningú et pot interrompre quan dones la paraula. Els alumnes tímids sovint s'alliberen quan tenen un rol clar: saben exactament qué se'ls demana i no han d'improvisar. El rol és una bastida d'identitat comunicativa.

**H2 — Rotar els rols cada debat**
Si el mateix alumne sempre és el Proposador, no aprèn a objectar ni a sintetitzar. Roto els rols cada sessió de debat, de forma aleatòria o estratègica (dono el rol Objector a qui normalment proposaria i viceversa). Efecte doble: aprèn totes les funcions i evita rols fixos que reprodueixin jerarquies de classe.

**H3 — Els iniciadors com a trampolí, no com a guió**
Els iniciadors no s'han de recitar: son el punt de partida. Quan un alumne llegeix "Jo crec que ___ perquè ___" i omple els buits amb el seu contingut, l'iniciador ha fet la seva feina. Si un alumne avançat vol abandonar l'iniciador, l'animo: significa que ja ha internalitzat l'estructura.

**H4 — El taulell com a memòria col·lectiva**
Sense taulell, els debats sovint giren en cercle: els mateixos arguments apareixen tres vegades sense que ningú s'adoni. El taulell (una cartolina dividida en 4 zones: A favor / En contra / Acords / Preguntes obertes) evita la repetició i fa visible el progrés. A B1+, el Sintetitzador és el "escrivà" del taulell.

**H5 — La pregunta de debat com a prerequisit**
Les cartes conversacionals son inútils sense una bona pregunta de debat. Una bona pregunta: (1) no té resposta única, (2) connecta amb el text treballat, (3) té rellevància per a l'alumne. Evitar: "Esteu d'acord amb el text?" (massa vaga) → millor: "Creus que [postura concreta del text] és justa? Per qué?" El LLM ha d'inferir la pregunta del text, no generar-ne una de genèrica.

## Autoavaluació (descriptors en primera persona)

- *A2*: "He dit la meva opinió i he escoltat la del company."
- *B1*: "He usat frases del meu rol per participar al debat. He escoltat i he respost a les idees dels altres."
- *B2*: "He citat el text per justificar la meva postura. He reconegut un argument de l'altre bàndol."
- *C1*: "He detectat si algú ha dit alguna cosa sense evidència suficient. He contribuït a la síntesi final."

## Fonts principals

- MALL (Model d'Aprenentatge de Llengües i Literacitat): cartes amb etiquetes lingüístiques, conversa exploratòria/disputativa.
- Mercer (2000): "Thinking together" — la conversa exploratòria com a eina de pensament col·lectiu.
- Gibbons (2002): scaffolding language, scaffolding learning — bastides per a la interacció oral acadèmica.
- Lipman (1988): Philosophy for Children — el diàleg filosòfic com a pràctica educativa.
- Decret 175/2022 (currículum Catalunya): comunicació oral, argumentació i pensament crític.
