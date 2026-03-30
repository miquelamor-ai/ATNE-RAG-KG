# Briefing per a mineriaRAG — Variables configurables per característica

> Document generat des del projecte ATNE (2026-03-22).
> Destinat a l'agent que gestiona el corpus RAG de FJE.

---

## 1. Objectiu

Afegir al frontmatter de cada document `tipus: característica` de M1 un bloc `variables_configurables` que declara quines variables pot configurar el docent a la UI de l'AAU quan selecciona aquella característica per a un perfil d'alumne.

Aquestes variables **no substitueixen** el contingut narratiu del document — el complementen amb metadades estructurades que el sistema ATNE utilitza per:
1. Generar la UI de configuració del perfil
2. Parametritzar la query RAG
3. Ajustar la intensitat i el tipus d'adaptació

---

## 2. Format del bloc

Afegir al frontmatter YAML, després de `review_status`, el bloc següent:

```yaml
variables_configurables:
  - nom: nom_variable
    etiqueta: "Text que veu el docent a la UI"
    tipus: enum | boolean | text | number
    valors: [valor1, valor2, ...]   # només per a enum
    obligatori: true | false
    defecte: valor_per_defecte       # opcional
    descripcio: "Breu explicació per al docent"
    impacte: "Com afecta l'adaptació"
```

---

## 3. Variables per document

### M1_alumnat-nouvingut.md

```yaml
variables_configurables:
  - nom: L1
    etiqueta: "Llengua materna (L1)"
    tipus: text
    obligatori: true
    descripcio: "Idioma principal de l'alumne"
    impacte: "Determina la distància lingüística i els suports de traducció"

  - nom: familia_linguistica
    etiqueta: "Família lingüística"
    tipus: enum
    valors: [romanica, germanica, eslava, araboberber, sinotibetana, altra]
    obligatori: false
    defecte: null
    descripcio: "Es pot inferir automàticament de la L1. Indica la distància amb el català"
    impacte: "A més distància, més suport visual i estructural necessari"

  - nom: alfabet_llati
    etiqueta: "Alfabet llatí"
    tipus: boolean
    obligatori: true
    defecte: true
    descripcio: "L'alumne està alfabetitzat en alfabet llatí?"
    impacte: "Si no: cal suport visual reforçat, tipografia més gran, evitar text dens"

  - nom: escolaritzacio_previa
    etiqueta: "Escolarització prèvia"
    tipus: enum
    valors: [si, parcial, no]
    obligatori: true
    defecte: si
    descripcio: "Ha estat escolaritzat regularment al país d'origen?"
    impacte: "Sense escolarització: cal bastida cognitiva bàsica, no només lingüística"

  - nom: mecr
    etiqueta: "Nivell de català (MECR)"
    tipus: enum
    valors: [pre-A1, A1, A2, B1, B2]
    obligatori: true
    defecte: A1
    descripcio: "Nivell de competència en català segons el Marc Europeu"
    impacte: "Determina la complexitat lingüística màxima del text de sortida"

  - nom: calp
    etiqueta: "Llengua acadèmica (CALP)"
    tipus: enum
    valors: [inicial, emergent, consolidat]
    obligatori: false
    defecte: inicial
    descripcio: "Competència en llenguatge acadèmic (diferent del conversacional)"
    impacte: "Inicial: vocabulari acadèmic amb definicions integrades. Consolidat: termes tècnics sense bastida"
```

### M1_alumnat-TEA.md

```yaml
variables_configurables:
  - nom: nivell_suport
    etiqueta: "Nivell de suport (DSM-5)"
    tipus: enum
    valors: [1, 2, 3]
    obligatori: true
    defecte: 1
    descripcio: "Nivell 1: necessita suport. Nivell 2: suport notable. Nivell 3: suport molt notable"
    impacte: "Nivell 1: adaptació subtil (estructura, literalitat). Nivell 3: LF extrema + suport visual total"

  - nom: comunicacio_oral
    etiqueta: "Comunicació oral"
    tipus: enum
    valors: [fluida, limitada, no_verbal]
    obligatori: true
    defecte: fluida
    descripcio: "Capacitat de comunicació verbal de l'alumne"
    impacte: "No verbal: materials altament visuals, pictogrames obligatoris"
```

### M1_TDAH.md

```yaml
variables_configurables: []
# Justificació: les adaptacions per TDAH (estructura, brevetat, suports atencionals)
# són consistents dins l'espectre. La variació individual es gestiona
# millor via els complements (bastides, esquemes) que via sub-variables.
```

### M1_dislexia-dificultats-lectores.md

```yaml
variables_configurables: []
# Justificació: les adaptacions de format (tipografia, espaiat, frases curtes,
# suport visual) s'apliquen de manera universal. La variabilitat es cobreix
# amb la intensitat de LF, que es calcula des del perfil global.
```

### M1_altes-capacitats.md

```yaml
variables_configurables:
  - nom: tipus_capacitat
    etiqueta: "Tipus de capacitat"
    tipus: enum
    valors: [global, talent_especific]
    obligatori: true
    defecte: global
    descripcio: "Superdotació global o talent en àrea concreta (verbal, matemàtic, artístic...)"
    impacte: "Global: enriquiment transversal. Talent específic: aprofundiment en l'àrea de talent"

  - nom: doble_excepcionalitat
    etiqueta: "Doble excepcionalitat"
    tipus: boolean
    obligatori: false
    defecte: false
    descripcio: "Coexisteix amb alguna dificultat d'aprenentatge (TDAH, dislèxia, TEA...)?"
    impacte: "Si sí: cal equilibrar repte cognitiu amb suports per a la dificultat associada"
```

### M1_TDL-trastorn-llenguatge.md

```yaml
variables_configurables: []
# Justificació: les adaptacions (simplificació sintàctica, suport visual,
# temps extra) són consistents. Es pot afegir severitat en fase 2.
```

### M1_discapacitat-intel·lectual.md

```yaml
variables_configurables:
  - nom: grau
    etiqueta: "Grau de discapacitat intel·lectual"
    tipus: enum
    valors: [lleu, moderat, sever]
    obligatori: true
    defecte: lleu
    descripcio: "Nivell de suport cognitiu necessari"
    impacte: "Lleu: LF moderada, vocabulari simplificat. Sever: LF extrema, pictogrames obligatoris, frases mínimes"
```

### M1_discapacitat-visual.md

```yaml
variables_configurables:
  - nom: grau
    etiqueta: "Grau de discapacitat visual"
    tipus: enum
    valors: [baixa_visio, ceguesa]
    obligatori: true
    defecte: baixa_visio
    descripcio: "Baixa visió: pot llegir amb adaptació de format. Ceguesa: necessita format alternatiu"
    impacte: "Baixa visió: tipografia gran, alt contrast, evitar gràfics complexos. Ceguesa: text pla, descripcions d'imatges, estructura lineal"
```

### M1_discapacitat-auditiva.md

```yaml
variables_configurables:
  - nom: comunicacio
    etiqueta: "Mode de comunicació"
    tipus: enum
    valors: [oral, LSC, mixta]
    obligatori: true
    defecte: oral
    descripcio: "Llengua de Signes Catalana, oral, o mixta"
    impacte: "LSC: prioritzar suport visual, estructura simple. Oral amb implant: adaptació similar a oient amb suport"

  - nom: implant_coclear
    etiqueta: "Implant coclear"
    tipus: boolean
    obligatori: false
    defecte: false
    descripcio: "Porta implant coclear o audiòfon?"
    impacte: "Amb implant: pot beneficiar-se de contingut oral/audiovisual amb subtítols"
```

### M1_discapacitat-motora.md

```yaml
variables_configurables:
  - nom: acces_teclat
    etiqueta: "Accés al teclat/pantalla"
    tipus: boolean
    obligatori: false
    defecte: true
    descripcio: "L'alumne pot interactuar amb teclat o pantalla tàctil?"
    impacte: "Si no: evitar exercicis interactius que requereixin input manual, prioritzar formats de resposta oral o selecció simple"
```

### M1_vulnerabilitat-socioeducativa.md

```yaml
variables_configurables: []
# Justificació: la vulnerabilitat socioeducativa és massa heterogènia per
# parametritzar amb camps fixos. El docent pot afegir context via camp lliure
# al perfil de l'alumne a l'AAU.
```

### M1_trastorns-emocionals-conducta.md

```yaml
variables_configurables: []
# Justificació: ídem. La variabilitat interna és massa gran.
# El docent aporta context específic per cada cas.
```

---

## 4. Camp lliure al perfil

A banda de les variables estructurades, la UI de l'AAU oferirà un **camp de text lliure** al perfil:

```
Observacions del docent: [____________________________]
```

Aquest camp s'injecta al prompt del LLM com a context addicional. Serveix per a:
- Matisos que no encaixen en cap variable (ex: "l'alumne té molta ansietat amb els exàmens")
- Context de característiques sense sub-variables (vulnerabilitat, trastorns emocionals)
- Informació que el docent considera rellevant i que no té camp específic

---

## 5. Resum de canvis per fitxer

| Fitxer | Variables | Canvi |
|---|---|---|
| `M1_alumnat-nouvingut.md` | 6 variables | Afegir bloc `variables_configurables` al frontmatter |
| `M1_alumnat-TEA.md` | 2 variables | Ídem |
| `M1_TDAH.md` | 0 (array buit) | Afegir bloc buit amb justificació en comentari |
| `M1_dislexia-dificultats-lectores.md` | 0 | Ídem |
| `M1_altes-capacitats.md` | 2 variables | Afegir bloc |
| `M1_TDL-trastorn-llenguatge.md` | 0 | Bloc buit |
| `M1_discapacitat-intel·lectual.md` | 1 variable | Afegir bloc |
| `M1_discapacitat-visual.md` | 1 variable | Afegir bloc |
| `M1_discapacitat-auditiva.md` | 2 variables | Afegir bloc |
| `M1_discapacitat-motora.md` | 1 variable | Afegir bloc |
| `M1_vulnerabilitat-socioeducativa.md` | 0 | Bloc buit |
| `M1_trastorns-emocionals-conducta.md` | 0 | Bloc buit |

**Total: 15 variables configurables repartides en 7 característiques.**

---

## 6. Nota per a l'agent mineriaRAG

- Aquests canvis són **només al frontmatter** — no cal modificar el contingut narratiu del document.
- El bloc `variables_configurables` és metadada per a la UI de l'AAU, no altera la cerca vectorial.
- Els comentaris YAML (#) dins del bloc serveixen com a documentació interna i no s'indexen.
- Si durant la implementació es detecta que cal una variable addicional, el projecte ATNE la proposarà via un briefing actualitzat.
