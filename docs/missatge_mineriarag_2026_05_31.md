# Missatge breu per a equip mineriaRAG

(Per a copy-paste a Slack/correu/canal habitual)

---

Hola equip,

Aquesta setmana al pilot d'ATNE hem trobat 5 famílies de bugs detectades per docents reals (cas titella, 30/05) i hem descobert una baula desconnectada al pipeline: **ATNE consumia `SKILL.md` sencer en lloc de `prompt_adapter.md`**, tot i que `build_skills.py` ja produïa ambdós artefactes des del switch coordinat del 26 maig.

L'hem connectada (commit ATNE `b065b96`). El prompt baixa 44-57% sense pèrdua de canon (els preàmbuls condicionals dels SKILL.md es preserven). Tots els tests regressors verds amb el slicing actiu.

**A continuació** hem fet 4 reforços canon al corpusFJE (commit corpusFJE `981d9a0`) per cobrir els forats que la setmana havia identificat:

1. **M3_glossari §5**: afegits exemples concrets de quotidians a excloure a A1+primària inicial (mitja/botó/agulla/fil/...). Llengua de definició generalitzada a multi-idioma (anti-castellanismes només si sortida = català; mateix patró per a altres llengües).
2. **M3_instrument-generar-esquema-visual NOU** (~150 línies): aquest instrument no existia al canon. Inclou regla canon "node central = PRODUCTE/OBJECTIU per a gèneres procedimentals (instructiu/receptari/manual)" — la regla del titella.
3. **Pictogrames**: `agent_role: complements → adapter` (al M3 i al SKILL.md). Es carregarà al call 1.
4. **M2_instruments-mediacio**: nova subsecció §Principis "Principi de proporcionalitat — 'Menys és més' transversal (MALL)". Justifica per què la matriu auto-suggestió proposa 2-3 complements/perfil (no 12).

**Phase 2 retry**: després dels reforços, hem provat d'eliminar les directives Python defensives. **Resultat**:

| Directiva | Pre-canon | Post-canon | Decisió |
|---|---|---|---|
| esquema_visual | 0/2 | **2/2 ✅** | **ELIMINADA** |
| glossari | 0/3 | 0/3 | Mantinguda — tensió §Nombre vs §Selecció |
| bastides | 8/10 | 4/10 ⬇️ | Mantinguda — efecte cross-SKILL del nou esquema-visual |
| pictogrames | 0/8 | 0/8 | Mantinguda — canvi agent_role NO és suficient |

**1 de 4 directives eliminada gràcies al canon reforçat.** Les altres tres mantingudes per motius diferenciats. Aprenentatge clau: **crear un SKILL nou complet amb regles imperatives explícites SÍ funciona** (cas esquema_visual). Reforçar §5 amb exemples NO és suficient si hi ha tensions intra-M3 (cas glossari). Canviar `agent_role` no n'hi ha prou si el cos descriptiu no inclou format imperatiu (cas pictogrames).

**Demandes residuals per a vosaltres** (ja heu cobert 3 de 4 forats — gràcies; queden ajustos):

1. **M3_glossari §Nombre A1**: afegir nota "max 2 termes si el text és majoritàriament quotidià" (sostre dur que sobreescriu el rang 5-8). Resol la tensió detectada.
2. **M3_pictogrames §A1**: reescriure amb estil més imperatiu i exemples concrets de format `[PICTO: terme|terme_castellà]` + anti-emojis Unicode. El cos descriptiu actual no és prou per a gpt-4o.
3. **Efecte cross-SKILL**: investigar per què afegir generate-esquema-visual al call 2 (complements role) degrada bastides (8/10 → 4/10). Hipòtesi: competència per atenció. Possible solució: marcar esquema_visual amb prioritat o moure'l a un call separat.
4. **Documentar el principi de proporcionalitat** a saber-ne.html §7 al costat de la matriu condició→complements per visibilitat docent.

També: en la sessió hem confirmat que **mantenim 2-call** (gpt-4o adapter + gpt-4.1-mini complements). Estudi comparatiu de 9 criteris: 2-call guanya 6, perd a latència, empat en 2. No és només cost.

Per al 8 juny (o asíncron): la confirmació final de la decisió 17/05 (SKILL.md=V2 prosa + rubrica.json) hauria de mencionar explícitament `prompt_adapter.md` com a via productiva per a ATNE — és el que realment consumim ara.

Salut,
Miquel

---

**Enllaços al repo ATNE:**
- Doc complet: `docs/proposta_post_fase0_2026_05_31.md`
- Commit clau: `b065b96` (connexió prompt_adapter)
- Audits empírics: `tests/audit_skill_preamble.py`, `tests/audit_prompt_size.py`
