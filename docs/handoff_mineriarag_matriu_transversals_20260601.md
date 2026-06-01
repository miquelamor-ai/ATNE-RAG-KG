# Handoff R0 → mineriaRAG · Dump matriu complements + lleis operatives

> **Data**: 2026-06-01 · **De**: ATNE · **Per a**: mineriaRAG (Opció 4 — canonitzar
> la matriu al M2_instruments-mediacio-pedagogica.md + generar `matriu_cobertura.json`
> derivat). · **Estat R0**: BLOQUEJAT a ATNE fins al senyal (commit hash) de mineriaRAG.

## Resum executiu

La matriu condició→complements d'ATNE té **DUES capes**:

1. **Capa base** (taula estàtica): condició → conjunt de complements pre-marcats.
   És el que mineriaRAG ja pot llegir directament del JS. Dump determinista a §1.
2. **Capa de lleis operatives** (lògica de `defaultComplementsForProfile`): regles
   R1/R2/R3/R4/A5 que **modulen** la capa base segons MECR + curs + nouvingut+L1.
   Aquesta capa NO és visible a la taula; viu al codi. Documentada a §2.

Perquè el M2 reflecteixi **tota la realitat operativa** (no només la base), el
`matriu_cobertura.json` derivat ha de codificar **ambdues capes**. Proposta
d'esquema JSON a §3 (no vinculant — mineriaRAG decideix el contracte final).

Font canon visual paral·lela existent: `ui/saber-ne.html §7` (validada NotebookLM
2026-05-27, Opció D). El JS i el §7 han d'acabar derivant del mateix M2.

---

## §1. Capa base — dump determinista

Generat executant `complements-matriu.js` amb Node (no transcrit a mà).
Llegenda de codis a §4. `true` = complement pre-marcat per defecte per a la condició.

| Condició (codi) | Complements pre-marcats (base) |
|---|---|
| `tea`         | esquema_visual · bastides · pictogrames |
| `tdah`        | glossari · esquema_visual · preguntes_comprensio |
| `disl`        | glossari · esquema_visual · bastides |
| `di`          | esquema_visual · bastides · pictogrames |
| `tdl`         | glossari · esquema_visual · bastides |
| `ac`          | activitats_aprofundiment · mapa_mental · rubriques |
| `aud`         | glossari · preguntes_comprensio · pictogrames |
| `vis`         | glossari · preguntes_comprensio |
| `tdc`         | glossari · preguntes_comprensio |
| `cat`         | glossari · bastides · pictogrames |
| `vuln`        | glossari · esquema_visual · preguntes_comprensio |
| `emo`         | glossari · preguntes_comprensio |
| `discalculia` | glossari · esquema_visual · bastides |

**Ordre canon de les 12 columnes** (`MATRIU_KEYS`):
`glossari, esquema_visual, bastides, mapa_conceptual, preguntes_comprensio,
activitats_aprofundiment, pictogrames, mapa_mental, plantilles_genere,
resum_graduat, cartes_conversacionals, rubriques`

**Principis pedagògics ja aplicats a la base** (v2 2026-05-27, validació NotebookLM Opció D):
- BASTIDES als perfils d'aprenentatge inicial (estratègia lectora).
- PREGUNTES als perfils amb autonomia lectora (contingut del text).
- Mai BASTIDES + PREGUNTES alhora als defaults (eviten redundància plànol crític).
- Visual exclusiu per MECR: esquema (A1/A2) · mapa mental (B1) · mapa conceptual (B2+).
- AC: sense esquema, sense pictogrames (expertise reversal — infantilitza).
- "Menys és més" (MALL): defaults reduïts (mitjana 3 complements/condició, abans 5).

---

## §2. Capa de lleis operatives (la "realitat invisible")

`defaultComplementsForProfile(p, mecr)` aplica, **per sobre de la unió OR de la
base**, aquestes regles. Aquesta és la part que mineriaRAG demanava explícitament
("quines lleis aplica el JS més enllà dels case_overrides ja canonitzats").

### Mòdul A — Normalització MECR a bandes
- `low`  = pre-A1, A1
- `mid`  = A2, B1
- `high` = B2, C1, C2 **i fallback** per a MECR buit/desconegut.
  (No apliquem regles de "baix" si no sabem el nivell.)

### Mòdul B — Modulació de la unió base (només quan hi ha condicions reconegudes)
Aplica **només a banda `low`**:

- **R1 (afegir pictogrames)**: si el perfil té ALGUNA condició de
  `VISUAL_NEED_CONDITIONS` = {disl, di, tdl, cat, tea, vis, discalculia} →
  AFEGEIX `pictogrames`. *Fonament*: a nivell baix el suport visual lèxic és
  prioritari per a aquestes condicions.
- **R2 (treure mapes fora de rang)**: a banda `low`, ELIMINA `mapa_conceptual` i
  `mapa_mental`. *Fonament*: SKILL canon situa mapa_conceptual a A2+ i
  mapa_mental a B1+. A `low` queden fora de rang → es treuen encara que la base
  els marqués.
- **R3 (dislèxia: treure glossari textual)**: si `disl` present I NO `cat`
  (nouvingut) I NO `tdl` → ELIMINA `glossari`. *Fonament*: el glossari textual
  afegeix càrrega lectora a la dislèxia; R1 ja hi posa pictogrames com a
  substitut visual. Excepcions explícites: nouvinguts mantenen glossari (bilingüe
  és central per a L2); TDL manté glossari (el gap lèxic és el seu nucli).

### Mòdul C — Fallback sense condicions reconegudes
Quan el perfil NO té cap condició de la matriu (`anyKnown=false`):

- **Defecte general**: `['glossari', 'preguntes_comprensio']`.
- **R4 (primària inicial low sense condició)**: si banda `low` I curs ∈
  {`1r Primària`, `2n Primària`} → NOMÉS `['preguntes_comprensio']`.
  *Fonament* (decisió Miquel 2026-05-31, post-pilot opció E): a primària inicial
  el text sol ser BICS quotidià; el glossari per defecte afegeix càrrega lectora
  innecessària si no hi ha condició que el justifiqui. El docent el pot activar
  manualment al Pas 2. Alineat amb `M3_instrument-generar-glossari.md §74`.
- **A5 (excepció a R4 per nouvingut amb L1)**: si es compleix R4 PERÒ el perfil és
  nouvingut amb L1 declarada → `['glossari', 'preguntes_comprensio']` (el glossari
  BICS quotidià + L1 + pictograma és precisament el que toca per a adquisició L2).
  *Detecció de nouvingut+L1*: chip `cat`, o `p.conditions[key=nouvingut]`, o
  `p.subvariables.nouvingut/l2`, amb una L1 a `nouCond.l1 || subvar.l1 || p.l1`.
  *Fonament*: resposta mineriaRAG 2026-05-31.

### Notes d'interacció (per evitar sorpreses al canonitzar)
- Les lleis R1/R2/R3 **només** s'apliquen quan `anyKnown=true` (hi ha condició).
- R4/A5 **només** quan `anyKnown=false` (cap condició) → són mútuament exclusives
  amb R1/R2/R3 dins una mateixa execució.
- La base és **unió OR** entre condicions: un perfil amb 2 condicions rep la unió
  dels seus dos conjunts base, i DESPRÉS s'hi apliquen R1/R2/R3.

---

## §3. Proposta d'esquema `matriu_cobertura.json` (no vinculant)

Perquè ATNE pugui consumir-lo SENSE perdre cap llei, l'esquema hauria de portar
les dues capes. Suggeriment (mineriaRAG decideix el contracte):

```json
{
  "version": "1.0",
  "source": "M2_instruments-mediacio-pedagogica.md §perfils-complements",
  "complement_keys": ["glossari", "esquema_visual", "bastides", "..."],
  "base": {
    "tea": ["esquema_visual", "bastides", "pictogrames"],
    "tdah": ["glossari", "esquema_visual", "preguntes_comprensio"]
  },
  "visual_need_conditions": ["disl", "di", "tdl", "cat", "tea", "vis", "discalculia"],
  "rules": {
    "mecr_bands": { "low": ["pre-A1", "A1"], "mid": ["A2", "B1"], "high": ["B2", "C1", "C2"] },
    "R1_add_pictos_low_visual": true,
    "R2_drop_maps_low": ["mapa_conceptual", "mapa_mental"],
    "R3_drop_glossari_disl": { "if": "disl", "unless": ["cat", "tdl"] },
    "R4_primaria_inicial": { "cursos": ["1r Primària", "2n Primària"], "only": ["preguntes_comprensio"] },
    "A5_nouvingut_l1_exception": ["glossari", "preguntes_comprensio"]
  }
}
```

Si mineriaRAG prefereix codificar les regles com a `case_overrides` per condició
(com a `rubrica.json`) en lloc d'un bloc `rules` global, ATNE s'hi pot adaptar:
el que importa és que **cap llei es perdi** en passar de JS → JSON.

---

## §4. Llegenda codis condició → nom canon

| Codi JS | Condició | M1 de referència |
|---|---|---|
| `tea`         | TEA (espectre autista)            | M1_alumnat-TEA.md |
| `tdah`        | TDAH                              | M1_TDAH.md |
| `disl`        | Dislèxia / dificultats lectores   | M1_dislexia-dificultats-lectores.md |
| `di`          | Discapacitat intel·lectual        | M1_discapacitat-intel·lectual.md |
| `tdl`         | Trastorn del llenguatge (TDL)     | M1_TDL-trastorn-llenguatge.md |
| `ac`          | Altes capacitats                  | M1_altes-capacitats.md |
| `aud`         | Discapacitat auditiva             | M1_discapacitat-auditiva.md |
| `vis`         | Discapacitat visual               | M1_discapacitat-visual.md |
| `tdc`         | Trastorn de la coordinació (dispràxia) | M1_trastorn-coordinacio-dispraxia.md |
| `cat`         | Nouvingut (català L2)             | M1_alumnat-nouvingut.md |
| `vuln`        | Vulnerabilitat socioeducativa     | M1_vulnerabilitat-socioeducativa.md |
| `emo`         | Trastorns emocionals/conducta     | M1_trastorns-emocionals-conducta.md |
| `discalculia` | Discalcúlia                       | M1_discalculia.md |

---

## §5. Què necessita ATNE de tornada

1. `matriu_cobertura.json` publicat al corpusFJE (derivat del M2), amb les dues
   capes (§1 base + §2 lleis) perquè el refactor JS no perdi comportament.
2. El **commit hash** del senyal (per fer el refactor + test byte-a-byte contra
   el dump d'aquest document).
3. Confirmació de si les lleis R1-R4/A5 es canonitzen com a `rules` globals o com
   a `case_overrides` per condició (afecta com ATNE les llegirà).

**Test d'acceptació a ATNE** (quan arribi el JSON): per a TOTS els perfils de §1 ×
{low, mid, high} × {1r Primària, altres cursos} × {nouvingut+L1, sense}, la
sortida de `defaultComplementsForProfile` llegint del JSON ha de coincidir
**byte-a-byte** amb la implementació hardcoded actual. Només llavors s'elimina el
hardcoded.

**Golden snapshot ja capturat**: `tests/golden/matriu_complements_snapshot.json`
(711 entrades, generat deterministicament des del JS actual amb Node). És el
contracte anti-regressió: el refactor R0 llegirà del JSON i haurà de reproduir
aquest snapshot exacte. Cobreix les 13 condicions × 9 MECR × 5 cursos + fallbacks
(NONE, NOUV_L1) + 4 parelles de condicions (R1/R2/R3/R4/A5 exercitades).

---

## §6. Deute paral·lel — transversals T1/T2 (mateixa decisió que R0)

Aprofitant aquest canal: T1 i T2 estan en el MATEIX estat que R0 (bloquejats
esperant decisió mineriaRAG). Detall complet a
`docs/reforcos_generes_arxiu_20260601.md` §Regles transversals. Resum + cita
literal del que ATNE té actiu i que caldria canonitzar (o confirmar com a ATNE):

**T1 — "la forma del gènere guanya sobre el MECR"** (ACTIVA, reduïda al mínim).
Ubicació: `prompt_builder.py` bloc `if _is_form_genre:`. Text literal actual:

> REGLA TRANSVERSAL — La FORMA del gènere «{genre}» guanya sobre el nivell MECR:
> si hi ha conflicte entre simplificar al MECR i preservar l'estructura formal del
> gènere (versos, torns, passos numerats, camps), GUANYA LA FORMA. Pots simplificar
> VOCABULARI, però segueix l'estructura canònica que defineix la SKILL del gènere.

- Aplica a gèneres-forma: poema, poesia, vers, cançó, teatre/diàleg, recepta,
  instructiu, manual, reglament, fitxa tècnica.
- **Demanem**: ¿entra com a transversal del canon (proposta de nom
  `forma_sobre_mecr`) als rubrica.json dels gèneres-forma? Si sí, ATNE el llegirà
  via `skills_loader` (anàleg a `get_format_output`) i retirarà el bloc Python.

**T2 — "no inventar contingut no demanat"** (ACTIVA, intacta). Salvaguarda del
format de sortida del pipeline 2-call (no afegir preguntes/marcadors/meta-comentaris
dins «## Text adaptat»). Text literal a `prompt_builder.py` (bloc "REGLA CRÍTICA
— NO INVENTIS CONTINGUT NO DEMANAT").

- **Demanem**: ¿és transversal de canon (`no_contingut_no_demanat`) o és
  legítimament una regla de plataforma ATNE? La nostra hipòtesi: T2 és més
  runtime-ATNE que canon-MALL (governa el nostre format 2-call, no el marc
  pedagògic). Si mineriaRAG hi coincideix, T2 NO puja al canon i es queda a ATNE
  documentada com a regla de plataforma (deixa de ser "en-trànsit").

Quan tinguem la vostra decisió sobre T1/T2 (igual que sobre R0), ATNE tanca el
deute: llegeix del canon el que pugi i retira el Python equivalent, amb test
anti-regressió que el prompt resultant conté la mateixa regla.
