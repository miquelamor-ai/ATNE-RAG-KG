# ATNE Self-Improvement Agent

**Versió**: 0.1 (disseny)
**Data**: 2026-04-12
**Estat**: document de disseny — implementació pendent fins després del pilot

## Visió

ATNE no és només una eina d'adaptació de textos. És un sistema que **aprèn dels docents reals** i millora sol. Cada vegada que un docent valora una adaptació, l'app guanya informació sobre què funciona i què no. Un agent intern processa aquesta informació, detecta patrons, proposa millores al sistema, les valida sobre el dataset sintètic, i només les aplica si demostren una millora real.

L'humà sempre decideix. L'agent investiga, experimenta i proposa.

## Arquitectura

```
┌───────────────────────────────────────────────────────────┐
│  ATNE Self-Improvement Agent                              │
│                                                            │
│  ┌──────────┐    ┌────────────┐    ┌──────────────┐      │
│  │ Observa  │ →  │ Diagnostic │ →  │ Proposa      │      │
│  │ feedback │    │ patrons    │    │ hipòtesis    │      │
│  │ pilot    │    │            │    │              │      │
│  └──────────┘    └────────────┘    └──────────────┘      │
│       ↑                                       ↓           │
│  ┌──────────┐    ┌────────────┐    ┌──────────────┐      │
│  │ Aplica   │ ←  │ Humà       │ ←  │ Experimenta  │      │
│  │ canvis   │    │ aprova     │    │ + Compara    │      │
│  └──────────┘    └────────────┘    └──────────────┘      │
│                                                            │
└───────────────────────────────────────────────────────────┘
            ↓
       ATNE Core
            ↓
       Docents (pilot / producció)
            ↑
       Feedback HITL
            └────────► retorna al cicle
```

## Cicle bàsic (MVP)

### 1. Observa
Llegeix les fonts de dades:
- **Feedback dels docents**: ratings 1-3, comentaris lliures, model preferit (A vs B en pilot HITL cec)
- **Adaptacions reals**: text original, perfil configurat, adaptació generada
- **Mètriques automàtiques** (`evaluator_metrics.py`): F1-F5 forma, recall d'instruccions
- **Avaluador LLM** (`evaluator_agent.py`): rúbrica C1-C6 fons

### 2. Diagnostica
Detecta patrons en les dades. Exemples:
- "El 40% dels textos a MECR A1 encara tenen frases > 8 paraules"
- "El complement 'preguntes comprensió' té feedback 'massa llarg' en 60% dels casos"
- "Per a perfils nouvingut, l'instrucció E-07 no es respecta en el 30% dels casos"
- "Els docents prefereixen Gemma 4 en textos curts (<200 par) i Mistral en textos llargs (>500 par)"
- "El feedback baixa quan el text adaptat supera 1.5x el nombre de paraules de l'original"

### 3. Proposa hipòtesis
Genera N propostes de millora amb justificació:
- "Reforçar E-07 al system prompt amb un exemple explícit per a perfils nouvinguts"
- "Limitar 'preguntes comprensió' a màxim 3 preguntes per defecte"
- "Afegir nova instrucció: S-11 'Si MECR == A1 i frase > 8 paraules, partir-la'"
- "Reduir el ratio de paraules adaptat/original de l'actual 2.0 a 1.5 per defecte"

Cada hipòtesi inclou:
- **Diagnòstic** que la motiva
- **Canvi proposat** (a quin fitxer, quina línia)
- **Mètrica esperada** ("hauria de millorar la mètrica F2 d'un 0.65 a 0.78")
- **Risc identificat** ("podria empitjorar marginalment F4 perquè...")

### 4. Experimenta
Per cada hipòtesi:
- Aplica el canvi a una **còpia** del prompt/codi
- Re-executa els 20-30 casos més problemàtics del dataset sintètic
- Passa els nous resultats per l'avaluador i les mètriques

### 5. Compara
Genera un informe amb:
- **Mètriques abans vs després** per cada hipòtesi
- **Casos que milloren** vs **casos que empitjoren**
- **Pareto front**: visualització de les hipòtesis al pla qualitat-cost
- **Recomanació**: quina hipòtesi té millor balance

### 6. Decideix (humà)
L'humà rep l'informe i tria:
- Acceptar la hipòtesi (passa al pas 7)
- Rebutjar-la
- Demanar matís ("aplica però només per a perfils X")
- Demanar més experimentació ("prova també amb Y")

### 7. Aplica
Si s'accepta:
- El canvi va al codi real (commit + push automàtic)
- S'executa un batch de validació de 50 casos sobre el dataset sintètic
- Si la validació confirma la millora, queda definitiu
- Si no, es fa rollback automàtic i es notifica l'humà

### 8. Cicle
A partir de feedback nou (post-canvi), torna al pas 1.

## Implementació MVP (post-pilot)

### Inputs
- `tests/test_data.json` — 200 casos × 10 perfils = 2000 cas-perfil
- `tests/results/evaluations.db` (SQLite) — històric d'avaluacions
- Feedback de Supabase `history` table — feedback real dels docents
- `instruction_catalog.py` — el prompt actual a optimitzar

### Components
- **`agent/observer.py`** — llegeix totes les fonts i normalitza
- **`agent/diagnostician.py`** — detecta patrons amb consultes SQL + LLM analytic
- **`agent/proposer.py`** — genera hipòtesis amb LLM (prompt: "donat aquest patró, què canviaries i per què?")
- **`agent/experimenter.py`** — aplica el canvi a una còpia, re-executa el subset, mesura
- **`agent/comparator.py`** — informe abans/després per a humà
- **`agent/applier.py`** — aplica el canvi al codi real (amb commit Git)
- **`agent/cli.py`** — interfície per a l'humà: `python agent.py run` → veu informe interactiu

### Stack
- Python 3.12 (mateix que ATNE)
- `google-genai` o `claude-agent-sdk` per al LLM analític
- SQLite per a l'estat del cicle
- Git per a versionat dels canvis del prompt

### Stack alternatiu (nivell 2)
Integració amb **GEPA** (Genetic-Pareto):
- Repo: github.com/gepa-ai/gepa
- Avantatge: optimització de múltiples objectius alhora (no només una mètrica)
- Trade-off: més complexitat, més temps d'execució

## Què milloraria

L'agent pot proposar canvis en aquestes capes:

| Capa | Què pot canviar | Exemple |
|---|---|---|
| **Catàleg d'instruccions** | Reforçar, reformular, afegir, eliminar regles | "L'instrucció E-07 s'ignora — afegeixo un exemple" |
| **Filtre de perfils** | Regles d'activació, intensificacions per sub-variables | "Quan TDAH + memòria baixa, intensificar C-01 més que ara" |
| **Mapping conducta → ajut** | Quines conductes activen quins ajuts | "La conducta b3 hauria d'activar també el complement X" |
| **Catàleg de complements** | Quins complements existeixen i com es generen | "El complement 'mapa mental' té poc ús — eliminar?" |
| **Taula MECR** | Nivell de referència per etapa+curs | "Els docents de 5è primària sempre baixen el MECR — ajustar referència de A2 a A1?" |
| **Prompts de complements** | Cada complement té el seu mini-prompt | "El prompt de bastides és massa llarg — escurçar" |

## Salvaguardes

L'agent **mai modifica res sense aprovació humana** (cicle bàsic). Per al cicle avançat (futur, automàtic) caldria:

1. **Test suite**: bateria de casos crítics que han de continuar funcionant. Si un canvi els trenca, rollback automàtic.
2. **Mètriques de no-regressió**: cap canvi que empitjori una mètrica per sota d'un llindar es considera vàlid.
3. **Rate limit**: màxim 1 canvi automàtic per setmana per evitar drift acumulat.
4. **Audit log**: tot canvi té traçabilitat (què, per què, dades que el van motivar, qui ho va aprovar).
5. **Kill switch**: l'humà pot desactivar l'agent en qualsevol moment.

## Roadmap

| Fase | Quan | Què |
|---|---|---|
| **0** | 2026-04-12 | Document de disseny (aquest fitxer) |
| **1** | Després del pilot (post 08/05) | MVP cicle bàsic — observador + diagnosticador + proposer + comparator + CLI |
| **2** | Q3 2026 | Experimenter automàtic + comparador visual |
| **3** | Q4 2026 | Aplicador automàtic amb salvaguardes |
| **4** | 2027+ | Integració GEPA per optimització multi-objectiu |

## Connexió amb el pilot HITL

El pilot 20/04 - 08/05 és la **primera font de dades reals HITL** que tindrem. Les decisions per al disseny de l'agent depenen d'aquestes dades:

- **Quins patrons són detectables?** (calibrar el diagnosticador)
- **Quines mètriques són rellevants per als docents?** (saber què optimitzar)
- **Quin volum de feedback genera un cicle?** (calibrar la freqüència del cicle)

L'agent NO ha de ser actiu durant el pilot. El pilot recull dades; l'agent treballa post-pilot amb les dades acumulades.

## Decisions pendents

- [ ] Stack: usar `claude-agent-sdk` o construir l'agent amb `google-genai`?
- [ ] On viu l'agent: fitxers `agent/` dins ATNE, o repo separat?
- [ ] CLI o web UI per a l'humà aprovador?
- [ ] Estratègia de rollback (Git revert? Branch? Snapshot?)
- [ ] Quants casos del dataset sintètic per al subset experimental? (proposta: 30 casos representatius)
