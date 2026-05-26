---
modul: M3
titol: "Escriure/adaptar una entrada de diari"
tipus: genere-discursiu
categoria_principal: generes
categories_secundaries: []
descripcio: "Instrument per adaptar o generar una entrada de diari: narració en primera persona amb tres blocs obligatoris (fets/emocions/reflexió) i separació neta entre blocs. HCL Narrar + Interpretar/Valorar. Variant acadèmica des de B1+. No s'adapta a pre-A1. Rúbrica gradada 7 passos × 5 nivells MECR (A1→C1)."
mecr_range: [A1, A2, B1, B2, C1]
agent_roles: [adapter, generator]
genre_key: diari
translanguaging: false
multimodal: false
moduls_relacionats: [M3]
variables_configurables:
  fase_lectora: [alfabetica_emergent, alfabetica_fluida]
skill_meta: write-diari@corpusFJE/skills/generes/write-diari
review_status: pilot-fusio-5
version: 4.0.0-canonic
generat_at: 2026-05-26
actualitzat_at: 2026-05-26
notebooklm_review:
  data: 2026-05-26
  veredicte: si-amb-correccions-menors
  aplicades_des_d_inici: [patro-canonic-pilots-fase-a, aclariment-us-lectura-vs-produccio-C1, fidelitat-gradada-C2, variabilitat-cardinal-passos-D3]
  aplicades_post_review: [a1-1-frase-per-bloc, b1-variant-academica-context-explicit, pas5-nosaltres-hint]
  comentari_key: "El diari és el gènere de transició BICS→CALP per excel·lència; la variant acadèmica B1+ és el pont entre l'expressió personal i el discurs acadèmic."
---

# Escriure/adaptar una entrada de diari

## Descripció

L'entrada de diari és una narració en primera persona on l'escriptor processa una experiència viscuda des de tres dimensions obligatòries: els **fets** (qué ha passat), les **emocions** (com m'he sentit) i la **reflexió** (qué he après o qué en penso). El seu tret definitori és la **separació neta entre blocs**: fets, emocions i reflexió han d'aparèixer en espais discursius diferenciats i no barrejats.

**Tipologia MALL**: Narrativa/Reflexiva (personal) · Expositiva/Justificativa (diari acadèmic, B1+).
**HCL principal**: Narrar — seqüenciar l'experiència en primera persona · Interpretar/Valorar — reflexió orientada a l'aprenentatge.
**HCL secundàries**: Expressar emocions (A1-B1) · Explicar — relació entre fets i aprenentatge (B1+) · Justificar — diari acadèmic (B1+) · Argumentar — reflexió crítica sobre l'experiència (C1).
**No s'adapta a pre-A1**: el diari requereix la producció autònoma en primera persona de **tres blocs metacognitius simultanis** — la separació conscient entre "el que ha passat", "el que he sentit" i "el que he après" és una operació metacognitiva que no és accessible sense base lecto-escriptora mínima i sense el concepte del "jo" com a subjecte narratiu explícit. (Decisió 6 canònica Fase B.)

**Connexions MALL transversals:**
- *Emoció nomenada com a competència*: nomenar emocions amb precisió és una competència sociolingüística i emocional. El diari és el gènere on s'entrena explícitament: "estava bé" no és informació, "estava nerviós però content" és una observació accionable. El vocabulari d'emocions és tan acadèmic com el vocabulari disciplinar.
- *Diari acadèmic com a pont BICS→CALP*: la mateixa estructura (fets/emocions/reflexió) s'omple amb HCL progressivament més acadèmiques (Narrar → Explicar → Justificar). A B1+, el bloc fets es transforma en "observació o resultats", les emocions en "valoració del procés" i la reflexió en "conclusions". La transició BICS→CALP és visible i gradual en el mateix gènere.
- *Metacognició com a competència d'aprenentatge*: la reflexió orientada a l'aprenentatge ("qué he après" i "com ho he après") és la porta d'entrada a la metacognició. A B1+, el diari deixa de ser memorialístic i es converteix en una eina de regulació de l'aprenentatge transferible a totes les matèries.

**Aclariment d'ús — què descriu aquesta rúbrica.**
Aquesta rúbrica descriu l'**entrada de diari adaptada per a la LECTURA** de l'alumne. **No descriu la producció autònoma de l'alumne** — la producció és tasca d'un derivat propi. Principi pedagògic MALL: l'alumne llegeix models al màxim del seu abast.
**Sub-granularitat dins de A1**: es treballa amb `fase_lectora: [alfabetica_emergent, alfabetica_fluida]`; no hi ha nivell logogràfic perquè el gènere requereix base lecto-escriptora mínima.

## Detecció

**Senyals docent** (quan adaptar a diari):
- El text font és una entrada de diari (personal, acadèmic, de viatge, de projecte).
- La unitat inclou una experiència (visita, experiment, projecte, debat) que cal processar per escrit des de la perspectiva personal de l'alumne.
- L'activitat vol desenvolupar la competència metacognitiva o emocional de l'alumne.
- L'activitat preveu un diari de lectura, de laboratori, de recerca o de projecte (diari acadèmic, B1+).

**Senyals alumne** (que indica que necessita bastida):
- Escriu els fets però no les emocions, o les emocions sense situar-les en fets concrets.
- Barreja fets, emocions i reflexions en la mateixa frase o paràgraf.
- Escriu en tercera persona ("l'alumne va anar") en lloc de primera persona.
- La reflexió és absent o és una frase aïllada sense connexió amb l'experiència narrada.

**Context favorable**:
- Tutoria: diari de classe, benestar emocional, cohesió de grup.
- Llengua i Literatura: diari de lectura, diari d'escriptor.
- Ciències: diari d'experiments, diari de sortida de camp.
- Qualsevol matèria: diari de projecte, diari d'aprenentatge (B1+).
- Alumnat nouvingut A1-A2: l'estructura simple (fets/emocions/reflexió) permet l'expressió autèntica sense la pressió del gènere acadèmic formal.

**Anti-senyals** (quan NO adaptar a diari):
- El text és purament informatiu i objectiu, sense perspectiva personal → informe.
- El text narra una experiència per comunicar-la a un lector extern → crònica.
- El text és íntim però no processa fets concrets (reflexió lliure sense ancoratge) → journal/dietari lliure.
- Pre-A1: la producció autònoma en primera persona de tres blocs metacognitius simultanis no és accessible sense base lecto-escriptora.

## Modulació per nivell

| Pas | Dimensió | A1<br>Inicial | A2<br>Funcional | B1<br>Estratègic | B2<br>Acadèmic | C1<br>Crític |
|---|---|---|---|---|---|---|
| **1. Data i encapçalament** | Format i precisió | Data en format simple: "Dilluns" / "12/05". | Data completa: "Dilluns, 12 de maig de 2026". | Data completa + context breu si escau ("Primer dia de campaments"). | Data completa integrada naturalment a l'entrada. | Data completa. Pot incloure el context situacional si és rellevant per a la comprensió. |
| **2. Bloc fets** | Seqüència i rellevància | 1-2 frases de fets en passat simple. Ordre cronològic estricte. | 3-4 frases de fets ordenats cronològicament. Connectors simples. | Fets narrats amb causa explícita. Connectors temporals variats. Selecció dels moments clau. | Fets en relació amb el context. Selecció conscient dels fets més rellevants per a la reflexió. | Fets narrats amb perspectiva sobre la seva significació. Pot incloure contrast entre expectativa i realitat. |
| **3. Bloc emocions** | Precisió i ancoratge | 1 emoció nomenada: "Estava content." / "Tenia por." | 2 emocions amb matís lleu: "Estava una mica nerviós però content." | 2-3 emocions variades i situades en el moment: "Quan vaig veure X, em vaig sentir Y." | Emocions analitzades: no només nomenades, sinó explicades en relació als fets. | Emocions complexes o contradictòries amb reflexió sobre el seu origen i significat. |
| **4. Bloc reflexió** | Profunditat i orientació | 1 frase de reflexió orientada a l'aprenentatge: "He après que..." | Reflexió de 2 frases amb connector causal: "Per això crec que..." | Conclusió clara de 2-3 frases. Diari acadèmic (B1+): "Els resultats mostren que..." | Reflexió que connecta l'experiència amb coneixements previs o futurs. | Reflexió metacognitiva: "com he après" i "qué m'ha sorprès", no només "qué he après". |
| **5. Primera persona** | Consistència i naturalitat | Primera persona consistent: "he", "em", "vaig". | Primera persona en tots els verbs principals. Cap canvi a tercera persona. | Primera persona consistent i variada. Veu pròpia recognoscible. | Primera persona natural, no forçada. Veu personal diferenciada. | Primera persona reflexiva: "m'he adonat que", "he reconsiderat", "em pregunto si". |
| **6. Criteris transversals** | Separació dels blocs | Tres seccions clarament separades, 1 frase per bloc. Cap barreja fets/emocions. | Tres blocs diferenciats per paràgraf o línia en blanc. | Tres paràgrafs clarament diferenciats amb transicions naturals entre blocs. | Blocs integrats amb transicions elaborades que mantenen la distinció fets/emocions/reflexió. | Blocs fluïts però clarament discernibles per al lector. La integració no amaga la distinció. |
|  | Variant acadèmica (B1+) | No s'aplica. | No s'aplica. | Quan el context és acadèmic (diari de laboratori, projecte): bloc fets → "Observació"; bloc reflexió → "Conclusions" ("Els resultats mostren que..."). El to és acadèmic, no memorialístic. | Tots tres blocs amb vocabulari acadèmic. Fets → Observació o resultats. Emocions → Valoració del procés. Reflexió → Conclusions. | Reflexió crítica sobre el procés d'aprenentatge, incloent limitacions i reptes. |
|  | Fidelitat al text font | Fidelitat als fets principals i a la veu en primera persona. | Fidelitat als fets, a les emocions i a la reflexió essencial. | Fidelitat als fets, a les emocions, a la reflexió i al to personal. | Fidelitat a la complexitat emocional i reflexiva del text original. | Fidelitat a la complexitat, als matisos i a les contradiccions si les hi ha. |
| **7. Autoavaluació metacognitiva** | Reflexió sobre el procés | "He dit qué ha passat, com m'he sentit i qué he après." | "He separat els fets de les emocions. He nomenat com em vaig sentir." | "He escrit una conclusió que explica qué he après i per qué." | "He analitzat les meves emocions i les he relacionat amb el context." | "He reflexionat sobre com he après, no només sobre qué he après." |

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
| 1 Data — Format i precisió | `structural` + `binary` | no | binary: data present; verificar format per nivell (simple A1 vs completa A2+); detectar absència de data |
| 2 Bloc fets — Seqüència | `countable` + `structural` | no | comptar frases de fets; verificar ordre cronològic; detectar fets barrejats amb emocions al mateix paràgraf |
| 3 Bloc emocions — Precisió | `binary` + `qualitative` | no | binary: emoció present i nomenada explícitament (no "estava bé" com a única emoció a A2+); qualitative: LLM-jutge sobre ancoratge al moment concret (B1+) |
| 4 Bloc reflexió — Profunditat | `binary` + `qualitative` | no | binary: reflexió present a A1+ (mínima 1 frase orientada a l'aprenentatge); qualitative: LLM-jutge sobre orientació a l'aprenentatge vs. opinió genèrica |
| 5 Primera persona — Consistència | `binary` + `structural` | no | binary: primera persona consistent; detectar canvis a tercera persona o veu impersonal; el "nosaltres" acadèmic (primera plural en treball col·lectiu) no es penalitza (vegeu Notes) |
| 6.1 Criteris — Separació blocs | `structural` + `binary` | no | binary: tres blocs discernibles; detectar barreja fets+emocions al mateix paràgraf; verificar separació gràfica (paràgraf o línia en blanc) |
| 6.2 Criteris — Variant acadèmica | `binary` + `qualitative` | no | binary: present a B1+ si el context és acadèmic; qualitative: LLM-jutge sobre vocabulari acadèmic (observació/resultats/conclusions) vs. memorialístic |
| 6.3 Criteris — Fidelitat al text font | `cross_source` + `qualitative` | **sí** (si adaptació) | comparar fets principals, to emocional i reflexió original vs adaptats; LLM-jutge sobre preservació de la veu personal |
| 7 Autoavaluació metacognitiva | `metacognitive` | no | derivar a vista d'autoavaluació alumne + registre docent |

**Notes:**
- Separació dels blocs (Pas 6.1): és el descriptor de qualitat més crític del diari. La barreja fets+emocions és el principal error dels alumnes i és detectable per posició (emoció dins del paràgraf de fets o viceversa) i per marcadors ("vaig veure X i em vaig sentir Y" en una sola frase en lloc de dos blocs separats).
- Primera persona (Pas 5): detectable per presència de pronoms de primera persona (jo, em, me, m', vaig, he, havia) de manera consistent. Cas especial: el diari acadèmic usa "nosaltres" si és un treball col·lectiu — no es penalitza.
- Variant acadèmica (Pas 6.2): verificable per vocabulari clau (observació, resultat, conclusió, mostra, indica, suggereix) i per absència de marcadors memorialístics ("ahir", "em vaig sentir").

## Heurístiques docent

**H1 — Les tres preguntes com a guió.**
Proposo que les tres preguntes vagin a la pissarra SEMPRE: (1) "Qué ha passat avui?", (2) "Com t'has sentit?", (3) "Qué has après?" A A1, l'alumne les copia i escriu una frase per pregunta. Amb les tres preguntes resoltes, l'entrada de diari està feta. Evita el bloqueig de "no sé qué escriure" i garanteix l'estructura de blocs.

**H2 — El vocabulari d'emocions al marge.**
Cartell a l'aula amb 10-15 emocions graduades (de la més bàsica a la més matisada). Quan l'alumne escriu "estava bé", li demano que triï una emoció del cartell. Funciona com a bastida lèxica per a A1-A2 i com a model per a B1+. El vocabulari d'emocions no és un complement: és la competència central del gènere.

**H3 — El temps verbal com a ancoratge.**
El pretèrit perfet o indefinit per als fets ("hem anat", "vam veure"), l'imperfet per a les emocions de fons ("estava nerviós", "sentia una mica de por"), i el present per a la reflexió ("crec que", "ara entenc que"). Distingir els temps verbals és una bastida gramatical que reforça la distinció entre blocs. Funciona des de A2.

**H4 — El diari acadèmic com a transformació del diari personal.**
A B1+, proposo que el docent i l'alumne renomegin els blocs: fets → "Observació o resultats", emocions → "Valoració del procés", reflexió → "Conclusions". La mateixa estructura física es reutilitza amb vocabulari acadèmic. L'alumne no aprèn un gènere nou: aprèn a fer servir el gènere que ja coneix en un context acadèmic. La transició BICS→CALP és visible i gradual.

## Fonts principals

- MALL (Model d'Aprenentatge de Llengües i Literacitat): HCL Narrar + Interpretar/Valorar, diari acadèmic com a gènere de transició BICS→CALP.
- Moon, J. (1999): *Learning Journals* — el diari com a eina de reflexió i metacognició; els tres blocs (fets/emocions/reflexió) com a estructura de processament de l'experiència.
- Vygotsky, L.S. (1978): *Mind in Society* — la zona de desenvolupament proper i la metacognició com a funció psicològica superior.
- Decret 175/2022 (currículum Catalunya): competència en comunicació lingüística i competència d'aprendre a aprendre.
