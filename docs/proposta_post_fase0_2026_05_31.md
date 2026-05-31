# Proposta post-Fase 0 — Diagnòstic ATNE + demandes a mineriaRAG

**Data:** 2026-05-31
**Autors:** Miquel Amor (ATNE) + assistència Claude
**Destinatari:** equip mineriaRAG / FJE (reunió 8 juny o asíncron)
**Status:** evidència empírica de Fase 0; canvis ATNE ja desplegats; demandes concretes per a coordinació

---

## 1. Resum executiu

Durant la setmana del 25-31 maig 2026, el pilot d'ATNE ha generat 5 commits que han resolt 5 famílies de bugs detectats per docents reals (cas titella, 30/05). Mentre s'aplicaven aquests fixes, hem descobert que el pipeline canònic de SKILLs **no estava plenament connectat**: ATNE consumia `SKILL.md` sencer (rúbrica vertical de 7 nivells) en lloc de `prompt_adapter.md` (parametritzat per nivell), tot i que **build_skills.py** ja produïa ambdós artefactes a producció des del switch coordinat del 26 maig.

La connexió s'ha completat avui (commit `b065b96`). El resultat: reducció del 44–57% del prompt per cas real, sense pèrdua de canon (els preàmbuls condicionals dels SKILL.md es preserven).

**Però** alguns guards observed-failure detectats pels fixes d'aquesta setmana **no estan al canon actual** i, al provar d'eliminar les capes Python defensives, els regressors fallen. Aquesta proposta documenta exactament quins guards cal pujar al canon (M3 dels instruments corresponents) i quines decisions de format demanen alineació amb mineriaRAG.

---

## 2. La baula que faltava — prompt_adapter desconnectat

### 2.1 Estat trobat (auditoria 31 maig)

| Component | Estat de la baula |
|---|---|
| `build_skills.py` (corpusFJE/.tooling) | ✅ Genera 37/40 SKILLs amb `SKILL.md` + `prompt_adapter.md` |
| `prompt_adapter.md` (per SKILL) | ✅ Compilat amb placeholders `{{NIVELL}}`, `{{LLISTA_DESCRIPTORS_DEL_NIVELL}}`, etc. |
| `skills_loader.py` (ATNE) | ❌ Llegia NOMÉS `SKILL.md` (rúbrica completa de 7 nivells) |
| Conseqüència | LLM rebia tots els nivells alhora, havia d'extreure mentalment el nivell A1 sota pressió multi-complement |

`prompt_adapter.md` no es referenciava en cap fitxer de codi d'ATNE. Verificat amb grep recursiu.

### 2.2 Connexió completada (commit `b065b96`)

- `skills_loader.py`: ara carrega també `prompt_adapter.md` sibling, parseja la secció "## Llistes per nivell (per a substitució)" en un dict `{nivell: descriptors_text}`, i extreu el preàmbul del SKILL.md (tot el que va abans de `## Modulació per nivell`).
- `render_skill_block(skills, mecr)`: si MECR donat i slicing actiu, envia preàmbul + llesca del nivell actiu. Fallback al body sencer si qualsevol condició falla.
- `ATNE_USE_PROMPT_ADAPTER` env var (default ON) — rollback ràpid sense canvi de codi.

### 2.3 Mesura objectiva (audits a `tests/audit_*.py`)

| Cas | Prompt actual (sencer) | Amb slicing | Reducció |
|---|---|---|---|
| titella (4 complements) | 39.2 KB | 16.8 KB | **-57%** |
| ex_pri (6 complements) | 56.5 KB | 27.0 KB | **-52%** |
| pol AC B2 (4 complements) | 29.3 KB | 16.4 KB | **-44%** |

37/40 SKILLs tenen preàmbul substantiu (>500 chars o marcadors crítics `⚠️/FORMAT/PROHIBIT/CONDICIONAL`). El preàmbul es preserva sempre. SKILLs amb canon preàmbul rellevant: `generate-glossari` (FORMAT BILINGÜE), `generate-bastides-lectura` (múltiples PROHIBIT/MAI), `generate-preguntes-comprensio`.

---

## 3. Patró observat — capes Python = guards no canònics

ATNE ha acumulat aquesta setmana 5 directives Python al `prompt_builder.py`:

| Directiva | Origen del bug | Què aporta sobre canon |
|---|---|---|
| `bastides` (commit `10b8bd0`) | clean_gemini_output §5c relocava cos a `## Preguntes` fantasma | Format imperatiu 3 moments, anti-pictogrames, desambiguació amb preguntes |
| `pictogrames` call 1 (`ac90566`) | adapter_only=True saltava la instrucció de pictogrames | Format `[PICTO:]`, exemples, anti-emojis Unicode |
| `matriu MECR-aware` (`fe1dd0c`) | Matriu Pas 2 mapejava perfil sense graduació per MECR | Pictogrames a A1+visual; mapes fora a A1; glossari fora a A1+dislèxia |
| `glossari` (`8dd9a9a`) | Glossari ple de quotidians (mitja/botó/agulla/fil) | Sostre estricte 2 termes A1, exemples quotidians, anti-castellanismes específics |
| `typography` (`4ed81e3`) | Auto-cache de font sobreescrivia el manual | Separar `font_manual_key` vs `font_key` |

**Cadascuna és, conceptualment, una simulació manual d'una regla del canon que el model no segueix sota pressió.**

### 3.1 Experiment Phase 2 (executat 31 maig)

Després de connectar el slicing, hem provat d'eliminar les directives Python una a una per veure si la capa canon (preàmbul + slicing) ja era suficient.

| Directiva | Sense directiva | Diagnòstic |
|---|---|---|
| **glossari** | **0/3 ❌** | Canon §5 d'A1 té la regla genèrica "cap quotidiana òbvia" però NO inclou exemples concrets ni sostre numèric. Sense la directiva, el model genera 8 termes amb 4 quotidians (mitja/botó/agulla/fil). **Gap canon.** |
| **bastides** | **8/10 ⚠️** | El slicing cobreix la majoria. Però ex_ci (1r primària·disl·A1·descripcio) falla 2/2. **Gap canon parcial**: el §A1 del SKILL no és prou robust per a aquest cas-específic. |
| **pictogrames call 1** | **0/8 ❌** | La SKILL té `agent_role: complements` → no es carrega al call 1. El slicing no té res a aplicar. **Gap arquitectònic**: pictogrames hauria de tenir versió amb `agent_role: adapter` per call 1. |
| **esquema_visual** | **0/2 ❌** | NO existeix `generate-esquema-visual/` al corpusFJE. Sense directiva, l'arrel cau a "Mitja vella" (el bug original del titella). **Gap canon total**: cal crear el SKILL al corpusFJE. |

### 3.2 Phase 2 retry (post canvis canon corpusFJE 981d9a0)

Després d'aplicar els 4 canvis canon proposats al corpusFJE (commit 981d9a0), hem repetit l'experiment d'eliminar les directives Python. **Resultats consolidats**:

| Directiva | Pre-canon (slicing sol) | Post-canon (slicing + canon reforçat) | Decisió |
|---|---|---|---|
| **esquema_visual** | 0/2 ❌ | **2/2 ✅** | **ELIMINADA** (commit pendent) |
| **glossari** | 0/3 ❌ | 0/3 ❌ | Mantinguda — tensió §Nombre vs §Selecció pertinent |
| **bastides** | 8/10 ⚠️ | **4/10 ⬇️** | Mantinguda — efecte cross-SKILL del nou esquema-visual al call 2 |
| **pictogrames** | 0/8 ❌ | 0/8 ❌ | Mantinguda — canvi agent_role NO és suficient; canon descriptiu, no imperatiu |

**Aprenentatges:**
1. Crear un SKILL nou complet amb regles imperatives explícites (com el nostre `generate-esquema-visual` amb "node central = producte") **SÍ** permet eliminar la directiva Python correspondent. Aquest és el camí més robust.
2. **Afegir exemples concrets al §A1** (com vam fer al glossari) **no és suficient** si hi ha tensions amb altres seccions del mateix M3 (cas §Nombre 5-8 vs §Selecció pertinent). Cal resoldre les tensions amb regles d'ordre clar.
3. **Canviar `agent_role`** d'un SKILL existent (cas pictogrames) **no és suficient** si el cos descriptiu del SKILL no inclou format imperatiu + exemples concrets. Cal complementar amb reescriptura del M3.
4. **Efecte cross-SKILL** detectat: afegir un SKILL nou (esquema-visual a complements-role) ha degradat el rendiment de bastides (8/10 → 4/10) per competència per atenció al prompt. **Cal monitoritzar tipus i quantitat de SKILLs simultanis carregats al call 2**.

**Conclusió de Phase 2:** una de quatre directives eliminada. Tres mantingudes amb diagnòstic empíric clar del que cal pujar al canon en cicles posteriors:
- Glossari §Nombre A1: afegir nota "max 2 si text és majoritàriament quotidià".
- Bastides: investigar interaccions cross-SKILL al call 2.
- Pictogrames M3: reescriure §A1 amb estil imperatiu i exemples (format `[PICTO:]`, anti-emojis).

---

## 4. Demandes concretes a mineriaRAG

### A) Pujar guards observed-failure al canon

Cada directiva Python ha estat provada empíricament a Phase 2. Cap és eliminable. Proposem:

| M3 / Acció | Reforç a pujar al canon | Justificació empírica |
|---|---|---|
| `M3_instrument-generar-glossari.md` §5 (A1) | • Sostre numèric: "MÀXIM 2 termes a A1+etapa inicial."<br>• Exemples concrets de QUOTIDIANS a excloure: mitja/botó/agulla/fil/retolador/llapis/paper/casa/taula/parts del cos/verbs bàsics.<br>• Anti-castellanismes específics: NO Muñeco, calcetín, aguja, hilo. | 0/3 sense directiva. El "cap quotidiana òbvia" genèric no es segueix; el model necessita exemples explícits. |
| `M3_instrument-generar-bastides-lectura.md` §A1 | • Format imperatiu dels 3 moments amb verbs d'acció (no preguntes).<br>• Regla anti-`## Preguntes`: les 3 fases viuen sota `## Bastides`, no com a secció pròpia.<br>• Anti-pictogrames a la secció bastides. | 2/10 fallades, totes a casos disl·A1·descripcio·text curt. El §A1 actual no contempla aquest cas-frontera. |
| **CREAR** `M3_instrument-generar-esquema-visual.md` | El SKILL no existeix al corpusFJE. Cal crear-lo amb gradació per nivell (PRE-A1: 2-3 nodes, A1: 3-4, A2: 4-6, B1: 6-8) i regla específica per a gèneres procedimentals (instructiu/receptari): "Node central = PRODUCTE/OBJECTIU final, no el primer apartat (Materials, Ingredients)." | 0/2 sense directiva. Arrel cau a "Mitja vella" en lloc de "Titella" — bug original del cas titella. |
| **CREAR o REFORÇAR** `generate-pictogrames` per a call 1 (adapter) | Opcions:<br>(a) Crear `generate-pictogrames-adapter` amb `agent_role: adapter` que contingui les regles del call 1.<br>(b) Canviar `generate-pictogrames` actual a `agent_role: adapter` (els pictogrames s'insereixen al text adaptat, no com a complement separat).<br>(c) Crear un instrument nou específic per multimodalitat-inline. | 0/8 sense directiva. La SKILL actual no es carrega al call 1 perquè és `complements`-role. El catàleg D-01 menciona [PICTO:] però el model l'ignora. |
| `M2_instruments-mediacio-pedagogica.md` | Pujar **"Menys és més (MALL)"** com a principi transversal de la matriu auto-suggestió Pas 2 (no només dins instruments específics com `preguntes_comprensio` o `bastides-lectura`). Justificar per què la matriu proposa 2-3 complements per perfil i no 12. | Audit Q3 de la sessió: principi MALL ja existeix al canon però aplicat dins instruments específics. La matriu transversal no té justificació canon explícita. |

Si aquests reforços es pugen al canon, **les directives Python passaran a ser redundants** i ATNE les podrà eliminar — tancant el deute tècnic. Mentrestant, ATNE manté la doble capa (slicing + directives) com a defense-in-depth conscient.

### B) Refinar la decisió 17/05 (SKILL.md = V2 prosa)

La memòria `parking_rubrica_json_post_fase0` (mineriaRAG) documenta:
> "SKILL.md productiu = V2 descriptiu (prosa); rubrica.json autogenerada des de JSON-font. Confirmació final pendent 8 juny."

Aquesta decisió **no menciona `prompt_adapter.md`**. La realitat observada el 31 maig:
- ATNE consumeix `prompt_adapter.md` (no `SKILL.md` sencer) com a via productiva.
- `SKILL.md` queda com a referència humana i fallback.
- `rubrica.json` (encara no produït per build_skills.py) seria una via complementària per a UI/calibratge si es decideix activar.

**Proposta:** refinar la decisió 17/05 explicitant els tres artefactes amb el seu rol: `prompt_adapter.md` (productiu LLM), `SKILL.md` (referència humana + fallback), `rubrica.json` (UI/Capa 1, si s'activa).

### C) Cas titella com a evidència Fase 0

Cas real del docent (30/05): perfil 1r primària + dislèxia + A1 + receptari. Bugs detectats abans dels fixes:
1. Glossari amb 4 termes quotidians + castellanisme ("titella → Muñeco")
2. Esquema visual centrat a "Materials" en lloc de "Titella"
3. Bastides amb verbs A2 ("Distingir", "Escriu al marge") inadequats per A1
4. Tipografia friendly-dislèxia (Lexend) no aplicada automàticament
5. Text adaptat amb prou feines diferent de l'original

Els 5 commits d'aquesta setmana resolen 1–4. El punt 5 es desbloca pel slicing (text receptari ja simple a A1 no admet més simplificació textual; el guany és multimodal: pictogrames + tipografia + bastides graduades).

**Aquesta evidència confirma que el sistema dissenyat funciona** — només calia connectar el `prompt_adapter.md`. Les decisions de Fase 1 (pilot 1000 docents) es poden fer amb base empírica sòlida.

### D) "Menys és més" al canon transversal

Detectat avui (Q3 audit): el principi MALL "Menys és més" està documentat **dins instruments específics** (bastides max 3 ítems/moment, preguntes max 10), però la matriu d'auto-suggestió Pas 2 d'ATNE l'aplica de manera transversal (mitjana 3 complements/perfil vs 12 possibles) **sense referència canon explícita**.

Proposta: pujar el principi a `M2_instruments-mediacio-pedagogica.md` com a regla transversal, citant-lo a `saber-ne.html` §7 al costat de la matriu. ATNE referenciarà aquest M2 al comentari del codi.

---

## 5. Decisions ATNE preses sense esperar al 8 juny

| Decisió | Motivació |
|---|---|
| Mantenir 2-call (gpt-4o adapter + gpt-4.1-mini complements) | Estudi comparatiu: 2-call guanya 6 criteris de 9 (cost, UX streaming, robustesa, debugging, compositionalitat, retry granular). Cost és UN motiu, no l'únic. |
| Connectar prompt_adapter (Phase 1, commit `b065b96`) | Auditoria empírica: slicing redueix prompt 50% sense pèrdua canon. |
| Defense-in-depth temporal | Mantenir directives Python active mentre el slicing es valida en producció. Phase 2 (eliminació gradual) en curs aquesta setmana. |

---

## 6. Pendents post-reunió

Si mineriaRAG aprova:
- Pujar guards al M3 (3-4 SKILLs) → ATNE elimina directives Python redundants.
- Definir `rubrica.json` per a un instrument pilot (preguntes?) si es decideix activar.
- Calibratge amb textos d'ancoratge (estratègia incremental, agenda 8/6 punt 4).

Si manté el status quo:
- ATNE conserva la doble capa (slicing + directives) com a belt-and-braces.
- Acumulació de deute tècnic continuada, però gestionable.

---

## 7. Annex: commits ATNE 25-31 maig

| Commit | Tema | Impacte |
|---|---|---|
| `10b8bd0` | fix(complements): bastides buides — §5c clean_gemini_output | Bastides apareixen al output |
| `ac90566` | fix(complements): pictogrames absents en 2-call (call 1 sense instrucció) | Pictogrames inline ARASAAC |
| `fe1dd0c` | feat(pas2): auto-suggestió de complements MECR-aware | Matriu Pas 2 gradua per MECR |
| `8dd9a9a` | fix(complements): glossari amb paraules quotidianes | Sostre 2 termes A1, anti-castellanismes |
| `4ed81e3` | fix(typography): auto-switch per perfil ignorat pel pseudo-manual cache | Lexend per dislèxia |
| `b065b96` | feat(skills): connectar prompt_adapter.md (slicing per nivell MECR) | **Tancament de la baula** |

---

**Per al 8 juny (o asíncron):** confirmar demanes 4A, 4B, 4D. Decidir sobre 4C (calendari Fase 1).
