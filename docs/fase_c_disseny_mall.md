# Disseny de Fase C — Gradacions del catàleg + Modalitat lectora MALL

**Data**: 2026-05-15
**Estat**: Disseny tancat pedagògicament (consultes a NotebookLM MALL).
Pendent d'implementar.

Aquest document recull les troballes pedagògiques de la sessió 2026-05-15
que han de guiar la implementació de Fase C. **No s'ha codificat res
encara**. La implementació es farà quan Fase B (refactor estructural de
MECR) estigui validada en producció.

---

## 1. Distinció arquitectònica clau: MECR ≠ Modalitat lectora

ATNE avui té UNA dimensió de "nivell": el MECR (pre-A1 → C2). El MALL
demostra que això **és insuficient**: la "lectura emergent" no és un
nivell lingüístic, és una **modalitat de relació amb el text**, i té
DOS perfils pedagògicament molt diferents:

### Tipus 1 — Lectura emergent per edat (MOPI/PIN inferior)

L'infant està **construint el concepte mateix** de lectura.

- **Foc del MALL**: comportament lector, no descodificació.
- **Qui descodifica**: l'adult, sempre. L'infant construeix significat.
- **Bastides**: pistes paratextuals (imatge, títol, format), lectura
  logogràfica de paraules familiars (el seu nom, el de la classe).
- **Exemple operatiu**: a P5 amb un àlbum il·lustrat, la pregunta NO és
  *"llegeix aquesta frase"*, sinó *"mirant el dibuix i el títol, qui
  creus que serà el protagonista?"*.

### Tipus 2 — Lectura emergent per llengua (TILC/L2)

L'alumne ja és lector en L1. Té **CUP** (Competència Subjacent Comuna):
sap què és un text, què és un paràgraf, llegeix d'esquerra a dreta.

- **Foc del MALL**: transferència interlingüística, pas de BICS a CALP.
- **Qui descodifica**: l'alumne mateix.
- **Bastides**: intercomprensió (semblances L1-català), traducció
  pedagògica (TOLC), glossari bilingüe, iniciadors de frase comparats.
- **Exemple operatiu**: a 1r ESO de Ciències, un nouvingut pot
  descodificar *"La cèl·lula és la unitat bàsica"*. La instrucció NO és
  explicar-li sons; és demanar-li *"Com es diu 'cèl·lula' en la teva
  llengua? Fixa't que l'estructura de la definició és igual en català
  que en la teva L1"*.

### Conseqüència per al disseny

L'instrucció **G-08** actual (lectura compartida) està activada per
`mecr_levels=["pre-A1"]`. Això la fa caure sobre **tot pre-A1**, però
en realitat només aplica a Tipus 1. Un nouvingut de 1r ESO amb MECR
pre-A1 **NO necessita lectura compartida** — necessita transferència L1.

**Cal una nova dimensió** al catàleg: `modalitat_lectora`.

---

## 2. Quan deixa de ser "Emergent": consulta MALL detallada

El MALL no dóna un curs fix per al pas a lectura autònoma. La fita és
**evolutiva**:

| Etapa | Curs | Estat lector típic |
|---|---|---|
| MOPI | P3-P5 | Lectura emergent (logogràfica/paratextual) |
| PIN | 1r-2n Primària | Trànsit logogràfica → alfabètica. Zona crítica |
| CM | 3r-4t Primària | Autonomia alfabètica + transició cap a *"llegir per aprendre"* (CALP) |

**Forquilla normal de consolidació de l'autonomia: entre els 4 i els 7 anys.**

Marcador real del MALL: trànsit **Fase Logogràfica → Fase Alfabètica**:

- Logogràfica: reconeix configuracions globals, pregunta *"què posa?"*
- Alfabètica: comprèn el codi, consciència fonològica, pregunta *"quina és?"*

A Cicle Mitjà el focus canvia:
- Es deixa d'emfasitzar *"aprendre a llegir"* (descodificació)
- S'aposta pel *"llegir per aprendre"* (competència epistèmica i CALP)

**Operativa a 1r Primària**:
- Lector emergent → instrucció *"llegir a través de l'adult"*
- Lector inicial autònom → *"lectura compartida (ara tu, ara jo)"*

### Conseqüència per al disseny

No es pot derivar la modalitat només per etapa. Cal una **subvariable al
perfil** que el docent omple (amb default segons curs):

```
fase_lectora: "logografica" | "alfabetica_emergent" | "alfabetica_fluida"
```

Defaults:
- Infantil → `logografica` (sempre)
- 1r-2n Primària → `alfabetica_emergent` (el docent pot baixar a `logografica`)
- 3r+ → `alfabetica_fluida` (el docent pot baixar excepcionalment)

I la **modalitat lectora** la dispara aquesta subvar + perfil nouvingut + MECR:

| Condició | Modalitat lectora |
|---|---|
| `fase_lectora == "logografica"` | **compartida** |
| `fase_lectora == "alfabetica_emergent"` | **progressiva** (ara tu, ara jo) |
| `nouvingut + mecr_low + fase_lectora != "logografica"` | **transferència** |
| Resta | **autònoma** |

---

## 3. Gradació operativa per nivell MALL (per implementar al catàleg)

### 3.1 Connectors per nivell (substitueix taula plana actual)

| Nivell | Inventari operatiu |
|---|---|
| Emergent (pre-A1) | **Cap** abstracte. Suport visual/oral. Si textuals: `i`, `després` |
| Inicial (A1) | + `però`, `perquè` |
| Funcional (A2) | + `primer`, `llavors`, `per tant` |
| Estratègic (B1) | + `ja que`, `en canvi`, `a més a més`, `tot i que` |
| Acadèmic (B2) | + `així mateix`, `no obstant això`, `atès que`, `en conseqüència`, `per contra` |
| Crític (C1) | Idèntic B2 + matisadors |

**Acció Fase C**: afegir `mecr_detail` a A-14 amb aquesta gradació.
Reemplaçar la taula plana del bloc bastides a [prompt_builder.py:628-635](adaptation/prompt_builder.py#L628-L635).

### 3.2 Iniciadors de resposta per nivell (mida del forat)

| Nivell | Iniciador exemple |
|---|---|
| Emergent | *"A la imatge veig un ___."* (suport visual) |
| Inicial | *"El personatge es diu ___ i vol ___."* (designació) |
| Funcional | *"Segons el text, ___ va passar perquè ___."* (literal) |
| Estratègic | *"Jo crec que ___ perquè el text diu ___."* (raonament propi) |
| Acadèmic | *"Aquest fenomen s'explica mitjançant ___, ja que ___."* (model teòric) |
| Crític | *"L'autor intenta convèncer el lector de ___ fent servir ___."* (intencionalitat) |

**Acció Fase C**: afegir `mecr_detail` al bloc *"Frases per començar la resposta"* del bastides.

### 3.3 Paraules clau / rescat lèxic

| Nivell | Quantitat i tipus |
|---|---|
| Emergent | 3-5 paraules + **pictograma**. Objectes reals del tema. NO tecnicismes |
| Inicial-Funcional | 5-8 paraules. Noms + verbs d'acció bàsics |
| Estratègic | ~10 paraules. Inclou habilitats: `hipòtesi`, `causa`, `conseqüència` |
| Acadèmic-Crític | Lèxic d'especialitat pur (CALP). Sense equivalent col·loquial |

**Acció Fase C**: afegir `mecr_detail` al bloc *"Paraules clau del text"* del bastides.

### 3.4 Pictogrames i suport visual (consulta MALL E1)

| Nivell | Densitat | Col·locació |
|---|---|---|
| Emergent | **1-2 per frase** (noms + verbs) | **Inline o sobre la paraula** (associació directa grafia-significat). Paratext lateral per anticipar sentit. |
| Inicial | **1 per frase** o només tecnicismes | **Glossari visual** (dreta o peu del text). L'alumne descodifica primer. |
| Funcional+ | Decidir docent | Glossari visual (no inline) — el suport visual no ha de competir amb el text |

**Justificació MALL**: el suport visual no és ornament, és **bastida
cognitiva** que fa l'input comprensible. La cobertura es gradua segons
l'estratègia lectora activada.

**Acció Fase C**: gradació al bloc del prompt per al complement
`pictogrames` (avui sense gradació).

### 3.5 Glossari L1 nouvingut (consulta MALL E2) — **RECTIFICAT**

Memòria 2026-05-15 `project_lectura_compartida_infantil.md` deia que els
ajuts L1 *"són per a la família, no per a l'infant"*. **És una mitja
veritat**. MALL ho rectifica: el glossari L1 + transliteració és
**per a TOTS DOS** (alumne + família):

- **Per a l'alumne**: veure la seva llengua escrita valida la identitat
  i activa la CUP. Són *"Textos d'Identitat"* que enforteixen la
  confiança.
- **Per a la família**: permet acompanyar la comprensió a casa
  (literacitat familiar).

**Patró concret** per a Emergent + nouvingut L1 no-llatí:

```
[Imatge del concepte] + [paraula L1 en alfabet origen] + [PARAULA EN CATALÀ]
```

La imatge és la **"llengua franca visual"** que connecta dos sistemes
gràfics diferents.

**Acció Fase C**:
- Reformular text de G-08 i de la capçalera del glossari: ja NO
  *"Per llegir junts a casa amb la família"* sinó alguna cosa com
  *"Per llegir junts: pictograma + L1 + català"* o *"Textos d'identitat"*
- Forçar el triplet pictograma+L1+català al glossari quan
  modalitat=compartida + alfabet_llati=False
- Actualitzar la memòria `project_lectura_compartida_infantil.md`

---

## 4. Preguntes de comprensió per nivell (substitueix lògica plana actual)

### 4.1 Marc pedagògic — Tres plànols

Qualsevol bateria de preguntes ha d'interrogar el text en **tres nivells
de profunditat de forma equilibrada**:

- **Literal** (llegir les línies): info explícita, dades, seqüències
- **Inferencial** (llegir entre línies): deducció, causa-efecte, hipòtesi
- **Crític** (llegir rere les línies): intencionalitat, ideologia, judici

### 4.2 Format apropiat per nivell

| Nivell | Formats apropiats |
|---|---|
| Emergent | **NO escriptura autònoma**. Assenyalar/Dibuixar/Dramatització/Dictat a l'adult |
| Inicial | V/F textual (sobre paraules clau), omplir buits amb opcions visuals |
| Funcional | Relacionar amb fletxes, elecció múltiple de títols, ordenació de seqüències |
| Estratègic | Idem A2 + preguntes inferencials (per què? i si...?) |
| Acadèmic | Argumentació oberta, transferència al jo, contrast de fonts |
| Crític | Argumentació + valoració d'intencionalitat + judicis fonamentats |

**Crític**: a Emergent, **prohibit** V/F textual, omplir buits textuals,
relaciona-amb-línies, *"per què..."*, comparacions abstractes, metacognició.

### 4.3 Quantitat per moment

- **Abans de llegir** (Predicció): **2-3 preguntes**. Activar previs + objectiu de lectura
- **Durant la lectura** (Monitorització): **1-2 aturades**. Dubtes lèxics + hipòtesi + resum parcial
- **Després de llegir** (Avaluació + Resum): **3-5 preguntes**. Cobrir els 3 plànols

**Regla MALL**: *"menys és més"*. No fatigar; mantenir compromís lector.

### 4.4 Operacions cognitives per nivell (pes de cada operació)

| Nivell | Pes literal | Pes inferencial | Pes crític |
|---|---|---|---|
| Emergent | Tot via adult | Propedèutic | Propedèutic |
| Inicial | Predominant | Inici | Mínim |
| Funcional | Domina | Apareix | Inicial |
| Estratègic | Base | **Motor** | Creixent |
| Acadèmic | Base | Base | Sòlid |
| Crític | Base | Base | **Motor** |

### 4.5 Modalitat discursiva

L'assistent ha de **canviar el "xip" segons si el text és literari o
informatiu**:

| Modalitat | Tipus de preguntes |
|---|---|
| Literari ("Porta Oberta") | Afectives (emocions), creatives (què hauria passat si...?), crítiques |
| Informatiu ("Porta Tancada") | Metacognitives (preveure pel títol), qüestionar info, resumir idees principals |

### 4.6 Modelatge ("Think Aloud")

L'assistent ha d'incloure, **de tant en tant**, comentaris on verbalitzi
el procés d'un lector expert. Exemple: *"Com a lector, quan veig aquest
títol en negreta em pregunto si és la idea més important. I tu, què en
penses?"*. Funciona com a ZDP de Vigotski.

**Acció Fase C**: refactoritzar tot el bloc `## Preguntes de comprensió`
de [prompt_builder.py](adaptation/prompt_builder.py#L523-L554) amb
gradació explícita per nivell MALL + ramificació literari/informatiu +
mòduls Think Aloud.

---

## 5. Regla rectora de mida del text adaptat

Decisió de Miquel 2026-05-15: la regla de longitud NO és un tope numèric,
és un principi **de no-expansió fidel**:

> *Una idea = una frase. L'adaptació preserva les idees essencials i en
> pot eliminar les secundàries. NO pot multiplicar frases. NO pot
> expandir el text. Si el contingut original té 1 frase per idea,
> l'adaptat tindrà ≤1 frase per la mateixa idea.*

Diferència amb la regla d'expansió que jo havia proposat inicialment:
- ❌ *Pre-A1 ≤ 70% de l'original* (no, és massa rígid)
- ✅ Preservació de nucli curricular + compressió fidel (no expansió)

Conseqüència: una adaptació a pre-A1 d'un text amb 6 elements
curriculars (Castanyada, Reis, Carnaval, Sant Jordi, Sant Joan, gegants)
manté els 6, però cada un en 1 frase curta + emoji + glossari L1 per
nouvingut (NO en 3 frases cadascú).

**Acció Fase C**: nova instrucció `C-12` SEMPRE amb la regla *"NO
expandeixis. Una idea = una frase. Si l'original té 1 frase, l'adaptat
té ≤1 frase per la mateixa idea."*.

---

## 6. Constraint arquitectònic: qualitat del text font

> *Adaptació a pre-A1 d'un text B2 sempre serà pitjor que un text ja
> escrit per a pre-A1. ATNE té un sostre de qualitat lligat a la qualitat
> de l'input.* — Miquel Amor 2026-05-15

Implicació: el botó **"Generar"** al Pas 2 és **el camí més robust per a
pre-A1**, no l'adaptació d'un text d'institut. Quan dissenyem el catàleg
pre-A1 per a Fase C, ha de tenir dos modes:

1. **Adapta des de text existent** → fes el que puguis. Si el text font
   és inadequat (massa complex per al nivell objectiu), **avisa el
   docent** que ha agafat un text incompatible.
2. **Genera des de zero** → qualitat molt millor, sense les restriccions
   de fidelitat estructural a l'original.

**Acció Fase C**: a `Argumentació pedagògica`, afegir un avís quan
detectem desajust entre la complexitat del text font i el MECR de sortida
(p.ex. text amb >40 paraules/frase quan MECR és pre-A1).

---

## 6.5 Esquemes visuals i mapes conceptuals (consulta MALL F1+F2)

Avui ATNE té els complements `esquema_visual` i `mapa_conceptual` sense
gradació per nivell. El MALL els distingeix clarament com a **bastides
cognitives** per fer trànsit cap al CALP.

### Esquema visual (diagrama de fletxes)

Treballa funció executiva i instrumental (seqüenciar, analitzar processos).

| Nivell | Apropiat per a | N nodes |
|---|---|---|
| Emergent | Seqüències temporals bàsiques (abans/després), relacions imatge→paraula | **2-3 nodes** |
| Inicial | Enumerar qualitats o parts d'un objecte (descripció simple) | **3-4 nodes** |
| Funcional | Seqüenciar passos d'instrucció / esdeveniments cronològics | **4-6 nodes** |
| Estratègic | Causa-efecte, hipòtesis | **6-8 nodes** |
| Acadèmic+ | Modelització de processos complexos | Decisió docent |

### Mapa conceptual jeràrquic

Eina de funció epistèmica (escriure i organitzar per pensar). **NO
treballable abans de A2 final**.

| Nivell | Treballable? | Profunditat |
|---|---|---|
| Emergent/Inicial | ❌ Inapropiat (encara descodificació) | — |
| Funcional (A2) | Introducció guiada | **2 nivells** (concepte → idees principals literals) |
| Estratègic (B1) | Eina fonamental | **3 nivells** (concepte → categories → exemples/detalls inferits). **Connectors lògics a les fletxes** |
| Acadèmic (B2) | Dominar superestructura del gènere | **4+ nivells**. Jerarquització complexa abstracta (CALP) |
| Crític (C1) | **Mapa de contrast** (no només contingut) | Multi-font / multi-ideologia, mostrant fiabilitat/posicionament |

### Bastides com a **temporals**

Principi rector MALL: les bastides visuals s'han d'anar **retirant** quan
l'alumne pot representar-se mentalment l'estructura. ATNE hauria
d'apuntar a l'**Argumentació pedagògica** quan un mapa és bastida
puntual vs quan és contingut estable.

### Acció Fase C

- Afegir `mecr_detail` al bloc del prompt per a `esquema_visual` amb
  cobertures de nodes per nivell
- **Suprimir** el complement `mapa_conceptual` automàticament per a
  Emergent/Inicial (vegeu `suppress_if_low_mecr`)
- Afegir nota d'argumentació pedagògica sobre bastides temporals

### Habilitats cognitivolingüístiques i format apropiat (MALL)

| Habilitat | Format | Nivell típic |
|---|---|---|
| Descriure | Esquema radial (objecte al centre + adjectius) | Inicial |
| Explicar | Diagrama de flux amb connectors "perquè"/"per tant" | Funcional/Estratègic |
| Justificar | Mapa conceptual jeràrquic (tesi + evidències + models) | Acadèmic |

---

## 7. Majúscules per a infantil — **RECTIFICAT 2026-05-15 (consulta MALL)**

**Proposta inicial de Miquel**: tot el text en majúscules per a I3-I5.

**Consulta MALL ho reformula**: el MALL NO recomana convertir tot el
text a majúscules. Tres principis:

1. **Materials reals des d'I3**: lletra d'impremta MAJÚSCULA + minúscula.
   No s'han d'"amagar" les minúscules — l'infant les troba a etiquetes,
   cartells i contes del seu entorn real.
2. **Majúscules són per ESCRIURE, no per LLEGIR**: la lletra de pal és
   motriument menys complexa per al traç (producció), no per a la
   percepció lectora.
3. **Transició natural a mixta/lligada** quan l'infant arriba a fase
   alfabètica de l'escriptura, no de la lectura.

**Acció Fase C reformulada**:
- ❌ NO conversió automàtica de tot el text a CAPS per a infantil
- ✅ Default: text en mixta normal (com els materials reals)
- ✅ Toggle manual al Pas 2: *"Noms de personatges en majúscules"* per a
  tasques d'identificació (rètols, llistes, descodificació logogràfica
  del propi nom)
- ✅ Toggle manual al Pas 2: *"Tot el text en majúscules"* per a casos
  específics que el docent jutgi (no com a default infantil)
- Preservar accents catalans: À/È/É/Í/Ò/Ó/Ú/Ï/Ü, ç→Ç, ñ→Ñ

---

## 8. Conseqüències per a la UI (chip del perfil, dropdowns)

Quan implementem Fase C, la card del perfil al Pas 1 i Pas 3 haurà de
mostrar 3 senyals coherents:

```
[Avatar] Nom Cognom
12 anys · 1r ESO
Català L2
A2 · Funcional
🤝 Lectura compartida (si modalitat=compartida)
```

O similar. La modalitat lectora és nova i visible.

També al dropdown de creació de perfil (Pas 1), quan curs és 1r-2n
Primària, oferir una opció *"Encara lectura emergent? (Sí/No)"* que
modifica `fase_lectora` per defecte.

---

## 9. Estat d'implementació

- **Fase A** (etapa+curs al backend, eliminar default ESO): ✅ Commit `adfd7f3`
- **Fase B** (MECR canònic):
  - B.1 ✅ `40f6e46` — `params_resolver.py`
  - B.2 ✅ `007e424` — endpoint `/api/derive-params` + clamp infantil
  - B.3 ✅ `1cf9c55` — pas3 consumeix endpoint
  - B.4 ❌ Diferit a Fase C (chip del perfil necessitarà refactor junt amb modalitat lectora)
  - B.5 ✅ `a8b2319` — eliminat default `materia='Història'`
- **Fase C** (gradacions catàleg + modalitat lectora): pendent.
  **Aquest document és el disseny pedagògic.**
- **Fase D** (autosave perfils): pendent
- **Fase E** (neteja codi mort): pendent

---

## 10. Referències

Consultes a NotebookLM MALL (corpus FJE) 2026-05-15:
- Distinció Tipus 1 vs Tipus 2 (lectura emergent dual)
- Forquilla evolutiva 4-7 anys (consolidació autonomia)
- Marc dels 3 plànols de lectura
- Modulació de preguntes per nivell MALL
- Quantitat de preguntes per moment
- Operacions cognitives per nivell
- Formats apropiats per nivell

Decisions pedagògiques Miquel Amor:
- Etapa infantil → pre-A1 sempre (clamp rectora)
- Una idea = una frase, no expansió
- Sostre de qualitat lligat al text font
- Majúscules I3-I5 (opt-in fora d'infantil)

Corpus de referència:
- `corpus/M3_lectura-facil-comunicacio-clara.md` (MALL + descodificació)
- `corpus/M3_generes-22.md` (22 gèneres canònics)
- `corpus/M2_DUA-principis-pautes.md` (DUA Acces/Core/Enriquiment)
