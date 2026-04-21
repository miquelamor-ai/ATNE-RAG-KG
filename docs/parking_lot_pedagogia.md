# Parking Lot — Decisions pedagògiques pendents

**Propietari**: equip de pedagogia FJE.
**Mantenedor tècnic actual**: Miquel Amor.

## Què és aquest document

Un registre dels temes que **requereixen judici pedagògic** (no decisió tècnica
pura) per resoldre's. L'equip tècnic ha fet una proposta provisional o ha deixat
el comportament actual, però la decisió final depèn de l'equip de pedagogia.

## Què NO és

- No és una llista de bugs tècnics (això va a GitHub Issues).
- No és un changelog ni un roadmap.
- No és per anotar suggerències menors: cada entrada hauria de tenir impacte en
  la interpretació pedagògica d'ATNE o del corpusFJE.

## Com entrar un tema nou

Afegiu un bloc nou sota la categoria corresponent seguint aquest template:

```markdown
### Títol curt i concret

- **Context**: per què ha sorgit aquest tema.
- **On impacta**: codi / corpus / UI / prompt / diverses.
- **Situació actual**: què fa ATNE ara mateix (sense judici).
- **Dubte obert**: la pregunta que cal que l'equip de pedagogia resolgui.
- **Proposta provisional** (opcional): una primera direcció, rebatible.
- **Estat**: `obert` | `en discussió` | `resolt` | `ajornat`.
- **Obert per**: nom + data (format AAAA-MM-DD).
- **Acord**: si es resol, resum de la decisió + data.
```

Quan un tema es resolgui, es **manté al document** amb estat `resolt` i un camp
`Acord`. No esborrar l'històric — el raonament és valuós.

---

## 1. Gèneres i tipologies textuals

### 1.1 Gèneres híbrids (email, entrada de blog, post xarxes socials…)

- **Context**: el Pas 2 d'ATNE ofereix una llista de 22 gèneres discursius
  classificats per tipologia (narratiu, expositiu, argumentatiu, descriptiu,
  instructiu, dialogat). Alguns gèneres reals combinen diverses tipologies: un
  email pot ser expositiu al cos + argumentatiu a la petició + fàtic a
  l'obertura/tancament.
- **On impacta**: UI (Pas 2 selector de gènere), corpus (`M3_generes-22.md`),
  prompt (via `corpus_reader.get_genre_block()`), skills (`skills_proto/genres/`).
- **Situació actual**: ATNE obliga a triar **un sol** gènere per adaptació. El
  docent ha d'escollir el dominant.
- **Dubte obert**: voleu permetre múltiples tipologies per a un mateix text?
  Voleu afegir gèneres híbrids explícits (ex: "email formal argumentatiu")?
  Voleu que l'agent detecti automàticament la tipologia mixta?
- **Proposta provisional**: mantenir un sol gènere per adaptació; documentar a
  la skill de cada gènere les combinacions vàlides quan un text té trets
  híbrids.
- **Estat**: `obert`.
- **Obert per**: Miquel Amor, 2026-04-21.

### 1.2 Gèneres no previstos

- **Context**: docents reals porten textos que no encaixen clarament en cap
  dels 22 gèneres (textos legals, cartells, infografies, apunts…).
- **On impacta**: UI del Pas 2.
- **Situació actual**: el docent tria "el que més s'assembla" o no tria res
  (veure 1.3).
- **Dubte obert**: voleu ampliar els 22 fins a cobrir gèneres més moderns?
  Voleu una opció "altres" amb text lliure?
- **Estat**: `obert`.

### 1.3 Comportament quan el docent NO tria gènere

- **Context**: el camp `genere_discursiu` pot arribar buit al servidor.
- **On impacta**: prompt (no s'injecta cap `get_genre_block()`), skills (cap
  `write-*` s'activa).
- **Situació actual**: el model actua amb instruccions genèriques sense regles
  específiques de gènere. Sortides menys estructurades.
- **Dubte obert**: volem forçar la tria al Pas 2? Volem que el sistema
  intenti detectar el gènere a partir del text? Volem una skill
  `write-genre-unknown` amb regles de mínims?
- **Estat**: `obert`.

### 1.4 Conservació del registre literari en adaptar

- **Context**: quan s'adapta un poema o un conte per a MECR A1/A2, el nivell
  de frase imposa restriccions que poden trair el registre literari. Es
  prioritza el contingut o l'emoció?
- **On impacta**: skills de gènere (`write-conte`, `write-fabula`,
  `write-poema`).
- **Situació actual**: ATNE aplica lectura fàcil també als textos literaris.
  El registre literari pot quedar reduït.
- **Dubte obert**: s'hauria de permetre un "mode literari" que relaxés algunes
  regles de LF per mantenir la musicalitat, les metàfores suaus, el ritme?
- **Estat**: `obert`.

---

## 2. MECR, nivells i suports

### 2.1 "Nivell bàsic" — rebaixa MECR o només afegeix suports?

- **Context**: al Pas 1 o Pas 2, quan el docent classifica un alumne com a
  "nivell bàsic" (terme informal, no MECR), no està clar què fa ATNE.
- **On impacta**: càlcul de MECR (`propose_adaptation`), prompt, skills de
  perfil, complements.
- **Situació actual**: cal auditar què fa avui. Sembla que en alguns casos
  rebaixa un MECR (pex: si l'alumne era B1, baixa a A2) i en altres manté el
  MECR però intensifica LF.
- **Dubte obert**: volem una regla clara — p.ex. "rebaixar MECR només si
  nouvingut o AACC (constitutiu); per a la resta, mantenir MECR i afegir
  ajuts/LF"? Això ja està a la memòria del projecte però cal fer-ho explícit.
- **Proposta provisional**: respectar la regla de la [feedback memory
  `mecr_ajust_perfil`]: MECR es modifica només per condicions constitutives
  rellevants (nouvingut, AACC); la resta de perfils modifiquen DINS del MECR
  via catàleg/skills.
- **Estat**: `en discussió`.

### 2.2 Grups multinivell

- **Context**: ATNE permet adaptar per a una persona o per a un grup-classe.
  En grups reals, el MECR no és uniforme (p.ex. 3 alumnes A2 + 15 B1 + 2 B2).
- **On impacta**: UI Pas 1, càlcul de MECR representatiu, sortida
  (multinivell?).
- **Situació actual**: el docent tria un MECR representatiu manualment. Els
  alumnes fora d'aquest nivell queden sub o sobre-atesos.
- **Dubte obert**: volem una funcionalitat de sortida multinivell (tres
  versions del mateix text a tres MECR)? O preferim que el docent adapti
  individualment? O una versió única amb "bastides internes" per a nivells
  alts?
- **Estat**: `obert`.

---

## 3. Marc conceptual i terminologia

### 3.1 Terminologia dels perfils

- **Context**: al codi i la documentació es barregen els termes "perfil",
  "característica", "condició", "situació". La memòria
  [`project_terme_perfil_pendent.md`] té una proposta de regulació.
- **On impacta**: codi (`profile.caracteristiques`), UI, documentació,
  corpus, skills.
- **Situació actual**:
  - Perfil = combinació de condicions + situacions que té un alumne.
  - Condició = tret constitutiu (TDAH, TEA, discapacitat).
  - Situació = context transitori (nouvingut, vulnerabilitat socioeducativa).
- **Dubte obert**: s'ha formalitzat aquesta distinció? Cal unificar el codi
  (hi ha `profile.caracteristiques` — el nom "característiques" no és del tot
  precís pedagògicament)?
- **Estat**: `en discussió` — hi ha nota de memòria prèvia del Miquel.

### 3.2 DUA com a marc arquitectònic vs marc ignasià com a marc rector

- **Context**: decisions pedagògiques d'ATNE es prenen alhora des del marc DUA
  (principis + pautes) i des de la tradició ignasiana (cura personalis,
  acompanyament, adaptar a la persona). Històricament s'ha debatut quin és el
  marc primer.
- **On impacta**: corpus (identitat ATNE, marc general), prompt, decisions
  futures del sistema.
- **Situació actual (acord previ)**: el marc ignasià és el marc rector (per
  què adaptem: cura de la persona concreta); el DUA és l'eina arquitectònica
  (com ho estructurem: accés/core/enriquiment).
- **Estat**: `resolt` (memòria
  [`project_marc_rector_ignasianer.md`] i
  [`project_dua_marc_referent_pendent.md`]).
- **Acord**: tradició ignasiana per sobre del DUA per a decisions de principi.
  DUA com a eina. Data aproximada: abril 2026.

### 3.3 "Adaptar" ≠ "rebaixar"

- **Context**: risc que l'usuari entengui l'adaptador com una "màquina de
  simplificar". L'adaptació inclusiva FJE vol apropar-se a la ZDP i oferir
  ajuts, no evitar la fricció cognitiva.
- **On impacta**: to del producte, UI, exemples, skills, comunicació interna.
- **Situació actual (acord)**: s'ha establert com a principi rector a la
  memòria [`project_visio_inclusiva_fje.md`]. Falta que aquest principi es
  reflecteixi de forma explícita al corpus i a la documentació pública.
- **Dubte obert**: hi hauria d'haver un document de "Principis ATNE" visible
  al projecte, no només a memòries internes?
- **Estat**: `resolt` (principi) + `obert` (plasmació al corpus).

---

## 4. Corpus i fidelitat

### 4.1 Contradicció interna a `M1_dislexia-dificultats-lectores.md`

- **Context**: detectat el 2026-04-21 pel subagent que va convertir els 4
  perfils a skills. La secció 1 del document (descripció) parla gairebé
  exclusivament d'alumnat nouvingut/L2, dient explícitament que les
  "dificultats lectores" NO es refereixen a dislèxia de base neurobiològica.
  La secció 6 (instruccions per a l'LLM) sí que està escrita des del marc
  dislèxia real (Dehaene/Wolf, descodificació fonològica).
- **On impacta**: corpus (font de veritat), skill `adapt-for-dislexia`,
  interpretació del clic UI `dislexia.actiu`.
- **Situació actual**: la skill derivada s'ha basat en la secció 6 (que és la
  que mapa al clic UI). La secció 1 queda inconsistent.
- **Dubte obert**: s'ha de reescriure la secció 1 per alinear-la amb la secció
  6? O la secció 1 reflectia un altre perfil (nouvingut amb dificultats
  lectores no-dislèxia) que mereix una entrada pròpia al corpus?
- **Estat**: `obert`.

### 4.2 Revisió pedagògica dels SKILL.md

- **Context**: el 2026-04-21 s'ha creat una biblioteca de 26+ skills a
  `corpus/skills_proto/` (22 gèneres + perfils + complements) a partir del
  corpus M1/M3. Els skills són MVP — el contingut és "prou bé" per validar la
  infraestructura, però no està revisat pedagògicament.
- **On impacta**: qualitat de les adaptacions quan la feature flag
  `ATNE_USE_SKILLS=true` s'activi.
- **Situació actual**: feature flag OFF per defecte a producció. Els skills
  només s'activen en tests locals.
- **Dubte obert**: quan l'equip de pedagogia té temps, cal revisar
  skill per skill: les regles són correctes? Els exemples són útils?
  Els matisos per MECR són ben calibrats?
- **Proposta provisional**: començar per les skills més crítiques
  pedagògicament (perfils amb impacte alt: TDAH, TEA, dislèxia, nouvingut) i
  per gèneres més usats a l'aula FJE.
- **Estat**: `obert`.

---

## 5. Complements

### 5.1 Complement "Preguntes graduades" no es genera sempre

- **Context**: històricament (memòria
  [`project_complement_preguntes_graduades.md`]) s'ha observat que aquest
  complement de vegades no apareix a la sortida.
- **On impacta**: `server.py parseAdaptedSections`, format del prompt.
- **Situació actual**: depèn de la fiabilitat del model. No està garantit.
- **Dubte obert**: més enllà de la investigació tècnica, cal definir
  pedagògicament: quan falla, volem retry automàtic? Volem que el docent ho
  vegi i decideixi si torna a provar?
- **Estat**: `en discussió`.

### 5.2 Valor real dels complements "mapes/esquemes" en text pla

- **Context**: els complements `esquema_visual`, `mapa_conceptual` i
  `mapa_mental` generen actualment ASCII-art amb fletxes, bullets i emojis
  (p.ex. `ELEMENT ☀️ → RESULTAT`). Per a alumnat amb TEA o dislèxia, aquesta
  sortida pot ser **soroll visual** més que ajuda. Per al docent, no és
  utilitzable: no es pot imprimir ni projectar de forma professional, hauria
  de refer el diagrama a una eina externa (Canva, SmartArt, MindMeister…).
- **On impacta**: prompt (`FORMAT SORTIDA` servidor), complements,
  experiència docent, cost de tokens.
- **Situació actual**: si el docent activa qualsevol d'aquests 3 complements,
  l'LLM genera la seva aproximació en text pla + emojis. Sortida de qualitat
  pedagògica discutible.
- **Dubte obert**: què volem fer amb aquests 3 complements?
- **Proposta provisional — 3 opcions**:
  - **A. Eliminar-los del MVP**. Netament. El docent usarà eines externes.
  - **B. Reconvertir-los a "guió per crear el mapa"**: en comptes d'ASCII-art,
    l'LLM genera una jerarquia de concepte central + branques ben
    estructurada, pensada perquè el docent la copiï i enganxi a la seva eina
    de diagrames. Això sí aporta valor.
  - **C. Generar codi [Mermaid](https://mermaid.js.org/)**: text que una
    llibreria JS del frontend pot renderitzar com a diagrama real. Amb
    `mermaid.js` afegit a la UI i als exports PDF, el mateix output serviria
    tant per a visualització com per a impressió. Requereix ~un dia de feina
    al frontend.
- **Estat**: `obert` — decisió prioritària: **no s'ha creat cap SKILL.md**
  per a aquests 3 complements fins que l'equip decideixi la direcció.
- **Obert per**: Miquel Amor, 2026-04-21.

### 5.3 Modalitat de les preguntes per textos literaris vs informatius

- **Context**: la skill `generate-preguntes-comprensio` (creada el
  2026-04-21) detecta automàticament si un text és literari o informatiu a
  partir del gènere discursiu triat (heurística amb paraules clau: `conte`,
  `poema`, `fantàstic`…).
- **On impacta**: skill `generate-preguntes-comprensio`, prompt dels
  complements.
- **Situació actual**: heurística basada en nom del gènere. Pot errar en
  casos fronterers (una crònica sobre art pot ser literària).
- **Dubte obert**: volem una casella explícita al Pas 2 ("tractament literari"
  vs "tractament informatiu")? Confiem en l'heurística?
- **Estat**: `obert`.

---

## 6. Altres temes oberts

(Sense categoria encara; migrar a sobre quan en sorgeixin més d'un per
tema.)

### 6.1 [Afegeix aquí el teu tema]
