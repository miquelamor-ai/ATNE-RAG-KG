# RESPOSTA ATNE → mineriaRAG (accions sobre taxonomies)

**Data:** 2026-06-06
**De:** ATNE (Miquel + Claude)
**Per a:** mineriaRAG
**Re:** `resposta_mineriaRAG_a_handoff_taxonomies_2026-06-06.md` (commit corpusFJE `a7b3df9`)

---

## Estat de les 4 accions demanades

### (1) Submòdul actualitzat ✅
- `corpus/external/corpusFJE/` actualitzat a `master`.
- HEAD del submòdul: `2fe2ea3` (inclou `a7b3df9` com a ancestre + regeneració de derivats SKILL/rubrica/manifest).
- Verificat: `M2_marc-teoric-mediacio.md` existeix (17.672 bytes). `a7b3df9` confirmat com a ancestre de HEAD.
- Pendent de fer el commit del bump del submòdul al repo ATNE (`git add corpus/external/corpusFJE`).

### (2) Sweller tret com a FONT ✅ (amb 1 decisió oberta per a vosaltres)
Escombrat de tot el codi/prompts/frontend d'ATNE. Trobats i corregits els casos on Sweller
es presentava com a **fonament** (atribució indeguda al MALL):

| Fitxer | Abans | Després |
|---|---|---|
| `instruction_catalog.py:576` (C-05, instrucció injectada al prompt) | "Glossari previ (pre-training, **Sweller**)" | "Glossari previ (organitzador previ, **principi MALL**)" |
| `export_fje/logica/instruction_catalog.py:404` (paquet migració FJE, mateixa C-05) | "(pre-training, **Sweller**)" | "(organitzador previ, **principi MALL**)" |
| `ui/saber-ne.html:1960` (secció §05b, text que llegeix el docent) | "menys és més — no sobre-mediar (**Sweller**, Vygotsky)" | "menys és més — **principi propi del MALL**; convergeix amb la càrrega cognitiva de Sweller" |
| `docs/mapa_taxonomies_visual.md` (paraigua MALL + regla complements) | "MALL integra ... **Sweller** ..." / "menys és més (Sweller + Vygotsky)" | tret Sweller del paraigua; "menys és més = principi PROPI del MALL, Sweller = convergència externa" |

Confirmat: el motor d'adaptació (`adaptation/prompt_builder.py`) ja atribuïa correctament el
"menys és més" al MALL (línies 712, 951, 955, 1001: "regla MALL «menys és més»"). NO calia tocar-lo.

**🟡 DECISIÓ OBERTA PER A VOSALTRES — `evaluator_rubrics.py`:**
Sweller apareix a la rúbrica del JUTGE LLM (l'avaluador que puntua adaptacions), NO al
"Per al docent" ni al motor d'adaptació:
- Línia 48: "rúbrica fonamentada en 6 marcs teòrics (Halliday, **Sweller**, Mayer, CAST/UDL, Vygotsky, TSAR)"
- Línia 97: criteri B3 "SUPORTS COGNITIUS I SCAFFOLDING (**Sweller** CLT, Vygotsky ZPD)"

Aquí Sweller NO es presenta com a fonament del MALL, sinó com a marc propi de la rúbrica
d'avaluació d'ATNE (un avaluador pot triar els seus marcs lliurement; Sweller és un autor
real de càrrega cognitiva). Per això ho hem **deixat com està**, perquè queda fora de
l'abast literal de la petició ("Per al docent"/motor d'adaptació).
**Pregunta a mineriaRAG:** voleu que també hi marquem Sweller com a "convergència externa"
a la rúbrica del jutge, o el deixem com a marc propi de l'avaluador? Miquel no ho té clar
i prefereix que decidiu vosaltres, ja que la regla és vostra.

### (3) Anidament de bastides — NO APLICA al codi ✅
Revisat `adaptation/prompt_builder.py` i `instruction_catalog.py`. ATNE NO té les bastides
codificades amb la taxonomia de famílies (lèxiques/sintàctiques/etc.). El que hi ha és
**estructura de SORTIDA del complement**: "## Bastides" amb sub-blocs "### Bastides de
lectura" + "### Bastides de resposta" (això són els moments de lectura, no les famílies).
La taxonomia de 3 famílies viu només al corpus (que ja heu corregit). **Res a reorganitzar
al codi d'ATNE.** El model canònic d'anidament queda registrat per a quan es derivi a JSON.

### (4) Gibbons → Bajtín/Adam — NO APLICA al codi ✅
Escombrat complet: **Gibbons no apareix a cap fitxer de codi (.py) ni frontend (ui/) d'ATNE.**
Les úniques apariciones eren al submòdul corpusFJE (ja corregit per vosaltres), al bootstrap
arxivat (`_bootstrap_fase0/`, no productiu) i als docs de la sessió anterior. **Res a corregir.**

---

## Resum

| Acció | Estat |
|---|---|
| (1) Submòdul actualitzat | ✅ (`2fe2ea3`, conté `a7b3df9`) |
| (2) Sweller tret com a font | ✅ 4 punts corregits · 🟡 1 decisió oberta (avaluador) |
| (3) Anidament bastides | ✅ no aplica (no codificat al motor) |
| (4) Gibbons → Bajtín/Adam | ✅ no aplica (absent del codi) |

## Pendents ATNE (no urgents)
- Derivar a JSON des de `M2_marc-teoric-mediacio.md` quan el "Per al docent" hagi de citar
  l'origen teòric de cada decisió (usant la columna "Estatus al MALL" per no sobreatribuir).
- Regla recordada: ATNE consumeix el canon derivat, no escriu al corpus.
- Una única decisió us torna la pilota: Sweller a la rúbrica del jutge (§2).
