# Missatge breu per a equip mineriaRAG

(Per a copy-paste a Slack/correu/canal habitual)

---

Hola equip,

Aquesta setmana al pilot d'ATNE hem trobat 5 famílies de bugs detectades per docents reals (cas titella, 30/05) i hem descobert una baula desconnectada al pipeline: **ATNE consumia `SKILL.md` sencer en lloc de `prompt_adapter.md`**, tot i que `build_skills.py` ja produïa ambdós artefactes des del switch coordinat del 26 maig.

L'hem connectada avui (commit `b065b96`). El prompt baixa 44-57% sense pèrdua de canon (els preàmbuls condicionals dels SKILL.md es preserven). Tots els tests regressors verds amb el slicing actiu.

També hem fet un experiment intencionat: **eliminar les directives Python defensives una a una** per veure si el slicing pur del canon ja era suficient. Resultat: **cap directiva eliminable**. Cada una indica un forat real al canon o a l'arquitectura de SKILLs:

- `glossari` (0/3 sense): manca al M3 §5 d'A1 sostre numèric + exemples concrets de quotidians + anti-castellanismes específics.
- `bastides` (8/10 sense): el §A1 no cobreix el cas-frontera disl·A1·text curt.
- `pictogrames` call 1 (0/8 sense): la SKILL té `agent_role: complements`, no es carrega al call 1. Gap arquitectònic.
- `esquema_visual` (0/2 sense): NO existeix `generate-esquema-visual/M3_*.md` al corpusFJE. Gap canon total.

El document complet amb diagnòstic, mesures, evidència del cas titella i 4 demandes concretes està al repo d'ATNE: `docs/proposta_post_fase0_2026_05_31.md`.

**Demandes per a vosaltres** (en ordre d'impacte):

1. **Crear `M3_instrument-generar-esquema-visual.md`** al corpusFJE. Avui no existeix.
2. **Decidir l'`agent_role` correcte per a pictogrames** (adapter vs complements). Avui és `complements` però s'utilitzen al call 1 (text adaptat) inline.
3. **Reforçar M3_glossari §5 d'A1** amb sostre numèric + exemples concrets de quotidians + anti-castellanismes específics.
4. **Pujar "Menys és més (MALL)" a M2_instruments-mediacio** com a principi transversal de la matriu auto-suggestió.

Si feu aquests canvis, ATNE pot eliminar les directives Python defensives i tancar el deute tècnic.

També: en la sessió hem confirmat que **mantenim 2-call** (gpt-4o adapter + gpt-4.1-mini complements). Estudi comparatiu de 9 criteris: 2-call guanya 6, perd a latència, empat en 2. No és només cost.

Per al 8 juny (o asíncron): la confirmació final de la decisió 17/05 (SKILL.md=V2 prosa + rubrica.json) hauria de mencionar explícitament `prompt_adapter.md` com a via productiva per a ATNE — és el que realment consumim ara.

Salut,
Miquel

---

**Enllaços al repo ATNE:**
- Doc complet: `docs/proposta_post_fase0_2026_05_31.md`
- Commit clau: `b065b96` (connexió prompt_adapter)
- Audits empírics: `tests/audit_skill_preamble.py`, `tests/audit_prompt_size.py`
