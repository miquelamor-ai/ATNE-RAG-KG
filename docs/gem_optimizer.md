# GEM: ATNE Prompt Optimizer

## INSTRUCCIONS PER CREAR LA GEM

1. Ves a https://gemini.google.com
2. Menú esquerre → Gems → "Crea una Gem"
3. Nom: **ATNE Prompt Optimizer**
4. Enganxa el SYSTEM PROMPT de sota
5. Desa

---

## SYSTEM PROMPT DE LA GEM

```
Ets un expert en pedagogia inclusiva, Lectura Fàcil, DUA i adaptació de textos educatius per a Jesuïtes Educació (FJE).

La teva tasca és avaluar adaptacions de textos educatius i proposar millores al system prompt que les genera. Treballes dins d'un loop d'optimització iterativa (estil GEPA).

## CONTEXT DEL PROJECTE
ATNE (Adaptador de Textos a Necessitats Educatives) és un assistent IA que adapta textos educatius per a alumnat divers: nouvinguts, NESE (TEA, TDAH, dislèxia, DI), altes capacitats. Usa Gemini 2.5 Flash amb un system prompt de ~90 instruccions organitzades en 9 macrodirectives: Lèxic, Sintaxi, Estructura, Suport cognitiu, Rigor curricular, Multimodalitat, Avaluació, Personalització lingüística, Adaptacions per perfil.

## QUAN L'USUARI T'ENGANXI UN CAS (text original + perfil + system prompt actual)

### FASE 1 — GENERA
Genera l'adaptació completa seguint EXACTAMENT el system prompt proporcionat.
Inclou tots els complements demanats (glossari, esquema, preguntes...).

### FASE 2 — AVALUA (sigues DUR i HONEST, no complagent)
Puntua de 1 a 5 cada criteri:

**B1 — Adequació al perfil alumne**
- El text està realment adaptat al perfil concret? (nouvingut àrab pre-A1 ≠ TEA B1 ≠ altes cap B2)
- El nivell MECR és correcte? (longitud frase, vocabulari, complexitat)
- El DUA (Accés/Core/Enriquiment) es reflecteix?

**B2 — Qualitat lingüística i preservació curricular**
- S'han mantingut els termes tècnics curriculars?
- Les simplificacions NO introdueixen errors conceptuals?
- Vocabulari freqüent, veu activa, subjecte explícit?

**B3 — Format, estructura i elements de suport**
- Paràgrafs curts, títols descriptius, llistes?
- Glossari, pictogrames, esquema (si demanats)?
- Estructura deductiva, advance organizer, resum?

**C1 — Qualitat pedagògica global**
- Un docent real ho usaria a l'aula?
- L'alumne descrit al perfil podria llegir-ho i aprendre'n?

Per cada criteri, justifica en 1 línia QUÈ FALLA CONCRETAMENT.

### FASE 3 — DIAGNOSTICA
Llista els 3-5 problemes principals del SYSTEM PROMPT que causen les puntuacions baixes:
- Quina instrucció FALTA?
- Quina instrucció és AMBIGUA o CONTRADICTÒRIA?
- Quina instrucció SOBRA o genera soroll?
- Hi ha conflictes entre instruccions?

### FASE 4 — PROPOSA CANVIS AL PROMPT
Per cada problema diagnosticat:
- [NOU] Instrucció nova a afegir
- [MODIFICAT] Instrucció existent a reescriure (mostra ABANS → DESPRÉS)
- [ELIMINAT] Instrucció a treure (explica per què)
- [PRIORITZAT] Instrucció que cal moure a posició més prominent

### FASE 5 — VERSIÓ MILLORADA (NOMÉS les parts canviades)
Reescriu NOMÉS les seccions del system prompt que canvien.
No repeteixis el que ja funciona bé.

## REGLES
- Respon SEMPRE en català
- Sigues crític i específic, no genèric
- Cada suggeriment ha de ser accionable (no "millorar la claredat" sinó "a la instrucció X, canviar Y per Z")
- Recorda: el model que executa el prompt és Gemini 2.5 Flash (SLM) — les instruccions han de ser explícites i concretes
- Prioritza les millores amb més impacte pedagògic real
```

---

## 5 CASOS DE TEST

Enganxa un cas a la vegada. Primer enganxa el system prompt actual, i després el cas.

### CAS 1: Nouvingut àrab — Cèl·lula eucariota (ESO, explicació, pre-A1, Accés)

**PERFIL:**
- Nouvingut del Marroc, L1 àrab, 3 mesos d'immersió
- Alfabet llatí: NO
- MECR sortida: pre-A1
- DUA: Accés (lectura fàcil extrema)
- Etapa: 1r ESO, matèria científica
- Gènere: explicació
- Ajuts: glossari bilingüe, pictogrames, esquema

**TEXT ORIGINAL:**
La cèl·lula és la unitat fonamental de la matèria vivent. Funciona com a unitat anatòmica i fisiològica: és el sistema organitzat més simple capaç de portar a terme les funcions vitals. Existeixen dos grans tipus de cèl·lules: les procariòtiques, sense membrana nuclear, pròpies dels bacteris, i les eucariòtiques, que contenen múltiples orgànuls i material genètic dins de cromosomes, pròpies dels animals i dels vegetals.

La cèl·lula eucariota consta de tres estructures principals. En primer lloc, la membrana cel·lular, formada per fosfolípids disposats en doble capa amb proteïnes incrustades, que funciona com a barrera selectiva i determina i manté les diferències entre el líquid de l'interior i l'exterior de la cèl·lula. En segon lloc, el citoplasma, que conté diversos orgànuls especialitzats.

---

### CAS 2: TEA nivell 2 — Guerra Civil (ESO, narració, B1, Core)

**PERFIL:**
- TEA nivell de suport 2, comunicació oral fluida
- MECR sortida: B1
- DUA: Core (adaptació estàndard)
- Etapa: 3r ESO, matèria humanística
- Gènere: narració
- Ajuts: definicions, esquema

**TEXT ORIGINAL:**
La Guerra Civil espanyola fou un conflicte armat iniciat el 18 i 19 de juliol de 1936 i acabat l'1 d'abril de 1939. El conflicte es provocà per un cop d'estat planejat pel general Emilio Mola, que comptà amb el suport de sectors de les forces armades, partits de dreta i la Falange Española. Fou una resposta a la revolució d'octubre de 1934 i reflectia el fracàs de la convivència política durant la Segona República.

La insurrecció tingué èxit parcial. A les zones republicanes — Barcelona, Madrid, Bilbao, Menorca — es mantingué la lleialtat al govern central. Als territoris que caigueren sota control rebel, el poder fou assumit pels militars. A la zona republicana, els partits polítics del Front Popular i les organitzacions sindicals constituïren un poder paral·lel que desenvolupà reformes socials.

---

### CAS 3: Altes capacitats — Ètica de la IA (Batxillerat, argumentació, B2, Enriquiment)

**PERFIL:**
- Altes capacitats
- MECR sortida: B2
- DUA: Enriquiment (profundització + pensament crític)
- Etapa: 1r Batxillerat, matèria científica
- Gènere: argumentació
- Ajuts: cap (l'alumne no necessita suports)

**TEXT ORIGINAL:**
La intel·ligència artificial ha deixat de ser un concepte de ciència-ficció per convertir-se en una tecnologia transversal que impregna tots els àmbits de la vida quotidiana. Com afirma Karina Gibert, catedràtica i directora de l'IDEAI-UPC: "La IA és transversal. No hi ha cap camp on no es pugui utilitzar." Ara bé, aquesta omnipresència planteja interrogants ètics que la societat no pot eludir. La tesi d'aquest text és que el desenvolupament de la intel·ligència artificial requereix un marc ètic i regulador sòlid que garanteixi que els seus beneficis superin els riscos.

En primer lloc, cal assenyalar el problema dels biaixos algorítmics. La IA es basa en les dades que han generat i generen els humans i, per tant, reprodueix els biaixos de gènere, edat o etnicitat que contenen aquestes dades.

---

### CAS 4: TDAH combinat — Volcà bicarbonat (Primària, instrucció, A2, Core)

**PERFIL:**
- TDAH subtipus combinat
- MECR sortida: A2
- DUA: Core
- Etapa: primària, matèria científica
- Gènere: instrucció
- Ajuts: esquema, exemples

**TEXT ORIGINAL:**
Objectiu: Simular una erupció volcànica mitjançant una reacció química entre un àcid i una base.

Materials necessaris: 1 got de vidre o ampolla petita de plàstic, 2 cullerades de bicarbonat sòdic, 150 ml de vinagre de vi, 1 cullerada de detergent de rentaplats, 4 gotes de colorant alimentari vermell, 1 safata de forn, argila o plastilina per construir el volcà.

Procediment:
Pas 1. Construeix el volcà. Col·loca el got de vidre al centre de la safata i modela la plastilina o l'argila al voltant per donar-li forma de muntanya. Deixa l'obertura del got lliure a la part superior: serà el cràter del volcà.
Pas 2. Prepara la barreja. Dins del got, posa la cullerada de detergent de rentaplats i afegeix-hi les 4 gotes de colorant alimentari vermell. Remena bé.
Pas 3. Afegeix el vinagre. Aboca els 150 ml de vinagre dins del got.

---

### CAS 5: Nouvingut + Dislèxia — La Castanyada (Primària, narració, A1, Accés)

**PERFIL:**
- Doble perfil: Nouvingut (Senegal, L1 wòlof, 5 mesos immersió, alfabet llatí: SÍ) + Dislèxia
- MECR sortida: A1
- DUA: Accés (lectura fàcil extrema)
- Etapa: 5è Primària, matèria humanística
- Gènere: narració
- Ajuts: glossari bilingüe, pictogrames, esquema

**TEXT ORIGINAL:**
Cada any, quan arriba la tardor i les fulles dels arbres es tornen grogues i vermelles, a Catalunya se celebra la Castanyada. És la nit del 31 d'octubre, la vigília de Tots Sants, i les famílies es reuneixen per menjar castanyes torrades, moniatos al forn i panellets, uns dolços petits fets amb massapà i pinyons.

La castanyera és el personatge més conegut d'aquesta festa. És una dona gran, vestida amb roba de pagesa, que seu al costat d'un fogó on torra les castanyes. Als mercats i a les escoles, es munten parades de castanyes i els nens i nenes es disfressen de castanyeres i castanyers.

Diuen que antigament, la nit de Tots Sants era una nit màgica en què les ànimes dels difunts tornaven a visitar les seves famílies. Per això, les famílies deixaven castanyes i panellets a la taula, perquè les ànimes poguessin menjar.

---

## COM USAR LA GEM

### Iteració 1 (baseline):
1. Enganxa: "SYSTEM PROMPT ACTUAL:" + [el prompt sencer de server.py]
2. Enganxa: "CAS 1:" + [text + perfil del cas 1]
3. La Gem farà les 5 fases automàticament
4. Apunta els canvis proposats

### Iteració 2 (millora):
1. Aplica els canvis proposats al system prompt
2. Enganxa: "SYSTEM PROMPT V2:" + [prompt actualitzat]
3. Enganxa el MATEIX cas 1
4. Compara puntuacions: han millorat?

### Iteració 3-5:
Repeteix amb els altres 4 casos per trobar patrons transversals.

### Consolidació:
Quan tinguis canvis validats en 3+ casos, actualitza:
- `instruction_catalog.py` (instruccions noves/modificades)
- `macrodirectives.py` (si cal reordenar)
- `server.py` → `build_system_prompt()` (si canvia l'estructura)
