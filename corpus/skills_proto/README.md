# Skills per a ATNE — prototip

**Estat:** prototip (2026-04-21). Activació per feature flag `ATNE_USE_SKILLS=true`.
**Per defecte OFF** — el comportament d'ATNE no canvia fins que s'activi.

Aquest directori conté la biblioteca de **Skills** compliant amb
[agentskills.io](https://agentskills.io), el format obert per a capacitats
especialitzades d'agents IA.

---

## 1. Per a què serveixen

Una **Skill** és una carpeta amb un `SKILL.md` que encapsula un coneixement
procedimental específic (com adaptar un text per a TDAH, com estructurar una
notícia, com generar un glossari bilingüe). Quan el perfil de l'alumne o els
paràmetres d'adaptació encaixen amb els triggers d'una skill, aquesta s'injecta
al system prompt del LLM.

**Beneficis vs catàleg Python actual:**
- **Editable per docents**: un pedagog pot refinar una skill sense programar.
- **Debuggable**: veus quina skill s'ha activat i què ha dit.
- **Compartible**: destinat a viure a `corpusFJE/skills/` compartit per altres
  assistents FJE futurs.
- **Portable**: el loader és 3 funcions reimplementables en qualsevol llengua
  (Python avui, PHP Slim4 demà).

---

## 2. Estructura del directori

```
skills_proto/
├── README.md                          ← aquest fitxer
├── adapt-for-tdah/                    ← skill de perfil
│   ├── SKILL.md
│   ├── assets/
│   │   └── exemple-A2-digestive.md
│   └── references/
│       └── README.md
├── genres/                            ← skills de gèneres discursius
│   ├── write-noticia/
│   ├── write-conte/
│   └── ... (22 gèneres)
└── complements/                       ← skills de complements
    └── generate-glossari/
```

---

## 3. Format d'una SKILL.md

### Estructura obligatòria

```yaml
---
name: write-noticia              # identificador únic, en kebab-case
description: >                   # una frase per Tier 1 (descripció curta)
  Use when adapting or generating a news article for students.
  Activates when genre_discursiu == "noticia".
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto             # semver; major = canvi incompatible
agent_role: adapter              # adapter | complements | evaluator | multimodal
tools_required: []               # llista de tools externes (buida per ara)
mecr_range: [A1, A2, B1, B2, C1] # informatiu, no funcional
triggers:                        # OR entre ells; la skill s'activa si algun matcha
  - path: params.genere_discursiu
    equals: noticia
---

# Títol llegible de la skill

## Quan activar aquesta skill
[una frase curta explicant quan]

## [Altres seccions pedagògiques lliures]

## Format de sortida
[blocodi markdown mostrant l'estructura esperada]

## Exemple
Veure `assets/exemple-basic-{nivell}.md` per un exemple complet.
```

### Triggers disponibles

Cada entrada a `triggers:` és un objecte amb `path` + operador:

| Operador | Sintaxi | Exemple |
|---|---|---|
| `equals` | `equals: <valor>` | `equals: noticia` |
| `not_equals` | `not_equals: <valor>` | `not_equals: "core"` |
| `in` | `in: [<v1>, <v2>, ...]` | `in: [A1, A2]` |
| `exists` | `exists: true/false` | `exists: true` |
| `truthy` | `truthy: true/false` | `truthy: true` |

El `path` és una ruta dins del context `{profile, params}` separada per `.`:

- `params.genere_discursiu`
- `params.mecr_sortida`
- `params.complements.glossari`
- `profile.caracteristiques.tdah.actiu`
- `profile.caracteristiques.nouvingut.L1`

### Semàntica

- **OR entre triggers**: la skill s'activa si **qualsevol** trigger matcha.
- Si vols AND, crea dues skills o usa un únic trigger amb una condició
  combinada (no suportat avui; evitar).
- Si falta `path` o `path` retorna `None`, el trigger no matcha.

---

## 4. Contracte del loader (per al portador a PHP Slim4)

Interfície mínima. Reimplementa aquestes 3+1 funcions en PHP i la biblioteca
funciona igual.

### `load_skills(skills_root: Path) -> list[Skill]`

Escaneja `skills_root` recursivament, troba tots els `SKILL.md`, parseja el
frontmatter YAML i el body markdown. Ignora silenciosament fitxers mal formats
(amb log).

**Estructura d'un Skill:**
```
{
  name: str,
  description: str,
  agent_role: str,
  triggers: list[dict],
  tools_required: list[dict],
  frontmatter: dict,   # tot el YAML cru
  body: str,           # markdown sense frontmatter
  path: Path,          # carpeta del SKILL.md
}
```

### `select_active(skills, profile, params, agent_role='adapter') -> list[Skill]`

Filtra pels skills amb `agent_role` coincident i evalua els triggers contra
`context = {profile, params}`. Retorna les skills on algun trigger matcha.

### `render_skill_block(skills) -> str`

Concatena els bodies de les skills com a un únic bloc per injectar al prompt:

```
=== SKILL ACTIVA: WRITE-NOTICIA ===
[body de la skill]

=== SKILL ACTIVA: ADAPT-FOR-TDAH ===
[body de la skill]
```

### `is_skills_enabled() -> bool`

Llegeix variable d'entorn `ATNE_USE_SKILLS`. Torna `true` si val `1`, `true`,
`yes` o `on`. Qualsevol altre valor (o absència) retorna `false`.

### Integració al servidor

Al `build_system_prompt()` (o equivalent PHP), afegir després de la
persona-audience:

```
if is_skills_enabled():
    skills = load_skills(SKILLS_ROOT)
    active = []
    for role in ("adapter", "complements"):
        active.extend(select_active(skills, profile, params, agent_role=role))
    if active:
        prompt_parts.append(render_skill_block(active))
```

---

## 5. Guia per a docents / editors pedagògics

### Com crear una skill nova

1. Trieu la carpeta adequada (`genres/`, `complements/`, `profiles/`, etc.).
2. Creeu una subcarpeta amb el nom de la skill (ex: `write-post-xarxes/`).
3. Creeu `SKILL.md` copiant el frontmatter d'una skill existent del mateix tipus.
4. Ompliu el body amb les instruccions pedagògiques (regles, contraindicacions,
   modulació per MECR, format de sortida).
5. Opcionalment, creeu `assets/exemple-basic-{nivell}.md` amb un abans-després
   pedagògic.
6. Llanceu el validador: `python skills_loader.py` (hauria de llistar la nova
   skill sense errors).

### Com editar una skill existent

Simplement editeu el `SKILL.md` corresponent. Els canvis són efectius immediatament:
el loader rellegeix els fitxers a cada crida a `build_system_prompt()`.

### Bones pràctiques

- **Sigueu concisos**: una skill és un "bitllet" operatiu, no un manual. ~50-100
  línies de body.
- **Regles concretes > descripcions vagues**: "frases de màxim 10 paraules" val
  més que "frases curtes".
- **Format de sortida explícit**: blocodi markdown amb l'estructura exacta.
- **Triggers específics, no amplis**: millor 2 triggers clars que un trigger que
  agafa massa casos.
- **Versió**: cada canvi incompatible puja major (1.0.0 → 2.0.0); canvis
  compatibles puja minor; correccions menors puja patch.

---

## 6. Inventari actual (2026-04-21)

### adapter (23 skills)

- **Perfils**: `adapt-for-tdah`
- **Gèneres** (22): write-manual, write-divulgatiu, write-informe, write-enciclopedic,
  write-descripcio, write-resum, write-conte, write-fabula, write-poema,
  write-biografia, write-noticia, write-cronica, write-diari, write-opinio,
  write-ressenya, write-assaig, write-carta, write-instructiu, write-receptari,
  write-reglament, write-entrevista, write-dialeg

### complements (1 skill)

- `generate-glossari` (variants monolingüe + bilingüe)

### Pendents (futur)

- Altres perfils: TEA, dislèxia, nouvingut, altes capacitats, discapacitats...
- Altres complements: preguntes-comprensio, bastides, mapa-conceptual,
  esquema-visual, pictogrames, activitats-aprofundiment...
- Skills multimodals (amb `tools_required`): descripció d'imatge, OCR, pictogrames
- Skills d'avaluador (jutge pedagògic per Verify 2.0)

---

## 7. Proves i debugging

### Llistar totes les skills i veure quines s'activen

```bash
python skills_loader.py
```

### Comparar prompt OFF vs ON

```bash
python tests/.tmp/e2e_skills_ab.py      # si aquest fitxer existeix
```

### Afegir un test nou

Copiar `tests/.tmp/e2e_skills_ab.py` com a base, canviar perfil/params.

---

## 8. Limitacions conegudes

- **Additiu en MVP**: les skills s'afegeixen al prompt actual sense substituir
  res del catàleg Python. Hi pot haver redundància (pex: la skill `write-noticia`
  i el bloc del corpus `get_genre_block("noticia")` diuen coses similars). Això
  s'optimitzarà en una fase posterior.
- **Orre en paral·lel**: en mode single-call (avui), totes les skills es barregen
  en un sol prompt. Pot saturar. En multiagent (futur), cada agent rebrà només
  les seves skills.
- **Sense `scripts/` executables encara**: les skills d'avui només porten text.
  Quan calgui multimodal (OCR, pictogrames), s'afegirà un registre de tools
  paral·lel (veure conversa del 2026-04-21).

---

## 9. Referències

- [agentskills.io](https://agentskills.io) — estàndard obert
- `docs/decisions/arquitectura_prompt_v2.md` — context històric del prompt
- `docs/decisions/refactoritzacio_prompt_20260409.md` — decisions prèvies
- `C:/Users/miquel.amor/.claude/plans/snoopy-crunching-wind.md` — pla de Sprint
  que va originar aquest treball (2026-04-21)
