# Arxiu de reforços hardcoded — pre-reducció A2 cascada (2026-06-01)

> Aquests reforços de prompt s'han RETIRAT del prompt_builder.py durant la cascada A2
> ("el JSON mana"): el canon (SKILL.md + rubrica.json del corpusFJE) ja cobreix
> l'estructura de cada gènere. Es guarden aquí LITERALS per reaplicar-los si reapareixen
> els bugs que van motivar-los (LLM ignorant la SKILL del gènere).

## Per què es retiren

Aquests blocs es van afegir al `adaptation/prompt_builder.py` (entre 2026-04-20 i
2026-05-31) com a pegats imperatius per forçar el LLM a respectar l'estructura del
gènere quan ignorava la SKILL `write-*` carregada al mig del system prompt.

Amb el refactor "el JSON mana", els gèneres discursius (write-noticia, write-conte…)
ja s'injecten SENCERS al prompt des del canon
(`corpus/external/corpusFJE/skills/generes/*/`) via `skills_loader.render_skill_block`.
Per tant aquests reforços:

- **Dupliquen el canon**: repeteixen (sovint amb redacció lleugerament divergent)
  l'estructura que ja descriu la SKILL.md + rubrica.json de cada gènere. Mantenir-los
  obliga a editar dos llocs (canon + Python) quan canvia un gènere → font de
  desincronització.
- **Contaminen la prova del canon**: en l'arquitectura nova volem verificar si el
  canon SOL és prou imperatiu perquè el LLM respecti l'estructura. Si deixem els
  reforços Python actius, no podem saber si el bon resultat ve del canon o del pegat;
  emmascaren regressions del canon.

## Com reaplicar

Si reapareixen els bugs (LLM aplana poemes a prosa, notícia sense titular/lead 5W,
gènere ignorat, pictogrames absents…):

1. Obre `adaptation/prompt_builder.py`.
2. Torna a enganxar l'string/codi literal d'aquest arxiu a la variable corresponent,
   a la posició original indicada a cada bloc (o equivalent si el fitxer ha canviat).
3. Assegura't que la variable es continua injectant a la f-string / llista que
   s'indica al camp «Com s'injecta».

Les referències externes (tests, snapshots) NO existeixen: cap altre fitxer del repo
referencia `_noticia_block`, `_genere_block`, `_form_genres`, `_PICTO_BANDS` ni
«PRESERVA LA FORMA» (Grep 2026-06-01, 0 coincidències fora de prompt_builder.py).

---

## Bloc A — Reforç NOTÍCIA (`_noticia_block`)

- **Ubicació original**: `adaptation/prompt_builder.py` L.486-517 (variable inicialitzada
  a `""` a L.486; assignació dins `if _is_noticia:` a L.487-517).
- **Bug que arreglava** (comentari del codi, L.480-483): «Fix 2026-05-27 (Bug 3): reforç
  específic per a "notícia" — sense aquest reforç, el LLM ignorava l'estructura
  periodística canònica (titular + lead 5W + cos en piràmide invertida + cita) i
  generava prosa expositiva amb preguntes. Vegeu cas mireia C5_estructura_genere=1/5.»
- **Detecció del gènere** (L.484-485):
  ```python
  _genere_lower = _genere_param.lower()
  _is_noticia = "notic" in _genere_lower or "notíc" in _genere_lower
  ```
- **Com s'injecta**: la variable `_noticia_block` s'interpola DINS de l'f-string de
  `_genere_block` (Bloc B), a la línia `{_noticia_block}` (L.532).

```literal

### 🗞️ FORMAT OBLIGATORI per a NOTÍCIA (piràmide invertida)
El text adaptat HA DE SEGUIR aquesta estructura, NO és opcional:

1. **TITULAR** (1a línia, format `# Titular`):
   - Frase informativa amb subjecte + verb d'acció + complement.
   - NO és el tema genèric ("La fotosíntesi"), sinó el FET noticiable
     ("Els científics descobreixen com les plantes generen oxigen").
   - Sense adjectius valoratius. Llargada segons MECR.

2. **LEAD** (1r paràgraf, sense títol propi):
   - Respon a les 5W en una sola frase o dues curtes:
     QUI · QUÈ · QUAN · ON · PER QUÈ (cobertura segons MECR: A1=2W, A2=4W, B1+=5W).
   - És el resum complet del fet més important. Si el lector només llegís el lead,
     ja sabria l'essencial.

3. **COS** (paràgrafs següents, piràmide invertida):
   - Detalls per ordre DECREIXENT de rellevància (el més important PRIMER).
   - Cada paràgraf afegeix un detall menys central que l'anterior.
   - Pot incloure 1 cita directa atribuïda ("Segons [persona], '…'") a partir d'A2.

4. **CONTEXT FINAL** (opcional, últim paràgraf):
   - Antecedents o conseqüències. La part més prescindible.

PROHIBIT:
- Generar el text com a prosa expositiva tipus llibre de text ("La fotosíntesi és...").
- Estructurar el cos amb preguntes ("**On passa aquest procés?**", "**Què necessita la planta?**").
  Això és gènere DIVULGATIU/EXPOSITIU, NO notícia.
- Ometre el titular o el lead 5W.
```

---

## Bloc B — Bloc genèric de gènere (`_genere_block`)

- **Ubicació original**: `adaptation/prompt_builder.py` L.518-535 (variable inicialitzada
  a `""` a L.477; assignació de l'f-string dins `if _genere_param:` a L.518-535).
- **Bug que arreglava** (comentari del codi, L.470-475): «Recordatori del gènere demanat
  al FINAL del prompt (recency bias): detectat 2026-05-27 amb harness Fase B + Sonnet
  judge — quan el gènere no és divulgatiu/expositiu (ex: entrevista, opinió, conte,
  poema), el LLM ignorava la SKILL WRITE-* del mig del prompt i generava sempre text
  didàctic expositiu (la directiva del final guanyava). C5 Estructura: 0.86/5.»
- **Variables prèvies relacionades** (L.476-479):
  ```python
  _genere_param = (params.get("genere_discursiu") or "").strip()
  _genere_block = ""
  if _genere_param:
      _genere_label = _genere_param.replace("_", " ").replace("-", " ").upper()
  ```
- **Com s'injecta**: la variable `_genere_block` s'interpola a la línia `{_genere_block}`
  (L.608) dins de l'f-string final que es fa `parts.append(...)` (L.600-617). Conté al
  seu torn el «menú» de gèneres (entrevista/opinió/conte/instructiu/diàleg/notícia/
  divulgatiu) i incrusta `{_noticia_block}` (Bloc A).

```literal

## ⚠️ GÈNERE DISCURSIU OBLIGATORI: {_genere_label}
El text adaptat HA DE SEGUIR l'estructura canònica del gènere "{_genere_param}",
tal com es defineix a la SKILL ACTIVA de més amunt al system prompt.
- Si el gènere és entrevista: format de torns Pregunta/Resposta entre entrevistador i entrevistat.
- Si el gènere és opinió: tesi clara + arguments + conclusió.
- Si el gènere és conte/fàbula/poema: narrativa amb personatges i estructura literària.
- Si el gènere és instructiu/receptari/manual: materials + passos numerats + bloc final
  `### Per acabar` (A1-A2) o `### Resultat esperat` (A2+) amb 1-2 frases que diuen
  què s'ha obtingut. PROHIBIT deixar la frase de tancament com a paràgraf solt fora
  d'estructura: ha d'anar dins un encapçalament propi.
- Si el gènere és diàleg: dos parlants identificats amb torns clars.
- Si el gènere és notícia: titular + lead 5W + cos en piràmide invertida + cita opcional.
- Si el gènere és divulgatiu/expositiu: prosa estructurada amb idees jerarquitzades.
{_noticia_block}
PROHIBIT generar prosa expositiva genèrica si el gènere és un altre. La forma del
gènere és tan important com el contingut adaptat.
```

---

## Bloc C — Reforç gèneres-forma (`_form_genres` + `if _is_form_genre:` — PRESERVA LA FORMA)

- **Ubicació original**: `adaptation/prompt_builder.py` L.1439-1462 (set `_form_genres`
  L.1439-1445; detecció L.1446-1447; bloc `if _is_form_genre:` amb l'`output_sections.append(...)`
  L.1448-1462).
- **Bug que arreglava** (comentari del codi, L.1434-1438): «Reforç crític per a gèneres
  on la FORMA és contingut (poema, teatre, recepta…). Sense això, smoke tests 2026-04-20
  mostraven que el LLM aplanava poemes a prosa quan MECR era baix, contradient la regla
  del gènere (parking lot #59). El reforç va al final perquè els LLMs respecten més les
  normes properes a la generació.»
- **Com s'injecta**: quan `_is_form_genre` és cert, s'afegeix l'f-string a la llista
  `output_sections` (L.1449); aquesta llista es fa `"\n".join(output_sections)` i
  s'afegeix a `parts` a L.1478 (`parts.append("\n".join(output_sections))`).

Codi literal complet (set + detecció + bloc):

```literal
    _form_genres = {
        "poema", "poesia", "vers", "cançó", "canço", "song",
        "teatre", "guió teatral", "guio teatral", "monòleg", "monoleg", "diàleg", "dialeg",
        "recepta", "receptari",
        "reglament", "norma", "instructiu", "manual",
        "fitxa tècnica", "fitxa tecnica",
    }
    _genre_lower = (genre or "").lower()
    _is_form_genre = any(g in _genre_lower for g in _form_genres)
    if _is_form_genre:
        output_sections.append(f"""
REGLA CRÍTICA — PRESERVA LA FORMA DEL GÈNERE «{genre}»:
La forma estructural d'aquest gènere ÉS contingut, no només envoltori.
Si hi ha conflicte entre la simplificació MECR i la preservació de la forma,
GUANYA LA FORMA. Pots simplificar VOCABULARI però NO:
- Convertir versos a prosa (poema, cançó): MAI uneixis dos versos amb una coma o un connector. Cada vers a la seva línia.
- Eliminar acotacions o canvis de personatge (teatre, diàleg): preserva «PERSONATGE:» i les acotacions entre parèntesis o cursiva.
- Reformular llistes numerades a prosa (recepta, instructiu, reglament): manté el «1. 2. 3.» i els passos discrets.
- Treure separadors gràfics significatius (fitxa tècnica): respecta la presentació en taula o llista de camps.

Si simplificar-ho et porta a destruir l'estructura, deixa el text en una versió
mínimament adaptada però FORMALMENT íntegra. La integritat formal és més
important que arribar al MECR exacte en aquests gèneres.
""")
```

---

## Bloc D — Segon bloc de PICTOGRAMES (`_picto_block` + `_PICTO_BANDS`) — DUPLICACIÓ del de Call1

- **Ubicació original**: `adaptation/prompt_builder.py` L.543-598 (variable `_picto_block`
  inicialitzada a `""` a L.543; tot el cos dins `if comp.get("pictogrames"):` a L.544-598,
  que inclou el dict `_PICTO_BANDS` L.554-572, el càlcul de `_picto_rule` L.573-581 i
  l'f-string del bloc L.582-598).
- **Duplicació**: aquest és el SEGON bloc de pictogrames. El bloc de Call1 ja migrat
  viu a L.731-787 (dins el seu propi `if comp.get("pictogrames"):`, amb `_picto_canon`
  des de `generate-pictogrames` del canon). Aquest Bloc D és la duplicació hardcoded
  que el refactor "el JSON mana" elimina.
- **Bug que arreglava** (comentari del codi, L.537-542): «Phase 2 retry 2026-05-31:
  provat sense aquesta directiva amb el nou canon (pictogrames ara agent_role:adapter,
  carregat al call 1). Resultat: 0/8 — el SKILL es carrega però el seu cos descriptiu
  no és prou imperatiu per a gpt-4o. Cal el format estricte i exemples de la directiva
  Python. Pendent (mineriaRAG): reescriure el M3 amb estil més directiu per al §A1.»
- **Càlcul del nivell** (L.545): `_mecr_pic = (mecr or "B1").upper().replace("Ç", "C")`
- **Com s'injecta**: la variable `_picto_block` s'interpola a la línia `{_picto_block}`
  (L.609) dins de l'f-string final que es fa `parts.append(...)` (L.600-617), just
  després de `{_genere_block}`.

Codi literal complet (dict `_PICTO_BANDS` + `_picto_rule` + f-string):

```literal
        _PICTO_BANDS = {
                "PRE-A1": (
                    "1-2 marcadors per frase davant noms i verbs clau (8-10 max per text). "
                    "POSICIÓ: SEMPRE abans de la paraula (`[PICTO: gat|gato] el gat dorm`, "
                    "MAI després). Afegeix també una capçalera `### Vocabulari del text "
                    "(mira primer!)` al començament amb la llista pictograma·paraula per "
                    "anticipació visual (UNE 153101)."
                ),
                "A1": (
                    "4-6 marcadors per text, 1 per paraula nova o concepte clau. "
                    "POSICIÓ: INLINE DAVANT del terme (`[PICTO: mitja|calcetin] una mitja "
                    "vella`, MAI després)."
                ),
                "A2": (
                    "4-6 marcadors INLINE DAVANT dels termes tècnics o conceptes clau del text "
                    "(`[PICTO: planta|planta] la planta verda`). Opcionalment, també pots "
                    "afegir un `### Glossari visual` al final amb la llista pictograma·terme."
                ),
            }
        _picto_rule = _PICTO_BANDS.get(
                _mecr_pic,
                (
                    "4-5 marcadors INLINE DAVANT dels termes tècnics o conceptes clau del text "
                    "(`[PICTO: clorofil·la|clorofila] la clorofil·la`). Només per a termes "
                    "tècnics o conceptes clau, no per a vocabulari quotidià. Opcionalment, "
                    "també pots afegir un `### Glossari visual` al final."
                ),
            )
        _picto_block = f"""
## ⚠️ PICTOGRAMES ARASAAC — OBLIGATORI a {_mecr_pic}
ACTIVAT — Insereix marcadors `[PICTO: terme]` reals (NO emojis Unicode 🌞🌊🌱).
Gradació per a {_mecr_pic}: {_picto_rule}

Format OBLIGATORI del marcador: `[PICTO: terme_idioma_doc|terme_castellà]`
- Esquerra del `|`: terme en l'idioma del document (català, castellà…).
- Dreta del `|`: equivalent en castellà per a la cerca ARASAAC.
- Terme curt (1-3 paraules), minúscules, concret i visualitzable (objecte, acció, ésser viu).
- Exemples (text català): `[PICTO: sol|sol]` `[PICTO: aigua|agua]` `[PICTO: planta|planta]` `[PICTO: córrer|correr]` `[PICTO: clorofil·la|clorofila]`.
- NO inventis emojis Unicode (🌞 🌊 🌱 ✨…): usa SEMPRE el marcador `[PICTO: …]`.
- NO posis text ni puntuació dins del marcador, només els termes separats per `|`.
- El backend els substitueix per imatges reals ARASAAC (CC BY-NC-SA 4.0).

PROHIBIT generar una secció `## Pictogrames` separada: els marcadors viuen DINS de `## Text adaptat`.
PROHIBIT deixar la sortida sense cap marcador `[PICTO:]` quan pictogrames és ACTIVAT.
"""
```

> Nota d'indentació: al codi original el dict `_PICTO_BANDS`, `_picto_rule` i
> `_picto_block` viuen dins `if comp.get("pictogrames"):` (12 espais de sagnat base).
> Aquí s'ha conservat el contingut literal; en reaplicar, respecta el sagnat del bloc
> on l'enganxis.

---

# Regles TRANSVERSALS pendents de pujar al canon (decisió Miquel 2026-06-01)

> **Distinció important** (Miquel): aquests blocs NO són reforços-duplicats d'un
> `rubrica.json` concret. Són **regles transversals** que apliquen a TOTS els
> instruments/gèneres alhora. Per tant NO s'han de retirar com els reforços ni
> deixar com a "excepció" silenciosa: **s'han de pujar a la secció `transversals`
> del canon** (responsabilitat mineriaRAG). Mentre el canon no les reculli, ATNE
> les manté ACTIVES al prompt, però registrades aquí com a **transversal-en-trànsit**.

Estat actual del canon (auditat 2026-06-01): la secció `transversals` dels 37
rubrica.json conté `format_output` (38×), `fidelitat_text_font` (22×) i 4 puntuals
(`no_circularitat`, `no_recursivitat`, `llengua_definicio`, `seleccio_pertinent`).
**NO existeix cap transversal de "forma > MECR" ni de "no inventar contingut".**

## T1 — Preserva la forma del gènere sobre el MECR (ACTIVA, reduïda)
- Ubicació: prompt_builder.py, bloc `if _is_form_genre:` (~L.1382).
- Estat: REDUÏDA a la versió mínima (principi transversal); el detall per gènere
  s'ha tret perquè el canon write-* ja el descriu.
- **Acció mineriaRAG**: afegir un transversal (proposta de nom: `forma_sobre_mecr`)
  als rubrica.json dels gèneres-forma (poema, teatre, recepta, instructiu, manual,
  reglament, fitxa tècnica) → "Si hi ha conflicte entre simplificar al MECR i
  preservar l'estructura formal del gènere, guanya la forma."
- Quan hi sigui: ATNE el llegirà del canon i retirarà el bloc Python.

## T2 — No inventar contingut no demanat (ACTIVA, intacta)
- Ubicació: prompt_builder.py, bloc "REGLA CRÍTICA — NO INVENTIS CONTINGUT NO DEMANAT"
  (dins l'output_sections final) i "Omet les seccions NO activades".
- Estat: INTACTA (no tocada en aquesta cascada — és salvaguarda transversal viva).
- **Acció mineriaRAG**: avaluar si entra com a transversal global del canon
  (proposta de nom: `no_contingut_no_demanat`) o si es queda com a regla de
  plataforma ATNE (pot ser que sigui més runtime-ATNE que canon-pedagògic).
- Decisió oberta: aquesta potser SÍ és legítimament d'ATNE (és sobre el format de
  sortida del nostre pipeline 2-call), no del marc MALL. Confirmar amb mineriaRAG.

## Com es tanca aquest deute
1. mineriaRAG decideix si T1/T2 són transversals de canon i, si ho són, les afegeix
   a `transversals` dels rubrica.json afectats (amb el nom de camp que esculli).
2. ATNE afegeix la lectura d'aquest transversal a `skills_loader` (anàleg a
   `get_format_output`) i retira el bloc Python corresponent.
3. Test anti-regressió: el prompt amb el transversal del canon ha de contenir la
   mateixa regla que el bloc Python retirat.
