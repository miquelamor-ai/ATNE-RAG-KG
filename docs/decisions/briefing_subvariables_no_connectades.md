# Briefing: 21 sub-variables declarades pero no connectades al prompt

**Data**: 2026-03-30
**Origen**: auditoria a la pagina /cuina (sessio de cuina ATNE)

## El problema

De les 36 sub-variables declarades a la UI (app.js CHARACTERISTICS), nomes 15 (42%) fan alguna cosa al sistema. Les altres 21 (58%) es recullen del docent pero no arriben al prompt ni afecten cap instruccio.

## Xifres

| Destí | Quantes | % |
|---|---|---|
| Activen instruccions (ORDRES al prompt) | 3 | 8% |
| Afecten proposta (DUA/LF/MECR) | 5 | 14% |
| Van a context (narrativa persona-audience) | 5 | 14% |
| Son de frontend (CSS/UI) | 6 | 17% |
| **Fan alguna cosa** | **15** | **42%** |
| **No fan res** | **21** | **58%** |

## Les 3 que SÍ activen instruccions condicionals

Totes del nouvingut:
- `nouvingut.L1` → activa G-01 (glossari bilingue), E-11 (pistes etimologiques si L1 romanica)
- `nouvingut.alfabet_llati` → activa G-03 (transliteracio fonetica si alfabet no llati)
- `nouvingut.mecr` → determina MECR sortida → activa TOTES les instruccions amb activation="NIVELL"

## Les 21 que NO fan res

### TDL (8 sub-variables — 0 connectades)
- `tdl.modalitat` (comprensiu/expressiu/mixt)
- `tdl.morfosintaxi` (afectada si/no)
- `tdl.semantica` (afectada si/no)
- `tdl.pragmatica` (afectada si/no)
- `tdl.discurs_narrativa` (afectat si/no)
- `tdl.comprensio_lectora` (afectada si/no)
- `tdl.grau` (lleu/moderat/sever)
- `tdl.bilingue` (si/no)

**Impacte potencial**: el TDL te nomes 2 instruccions fixes (H-16, H-17). Les sub-variables podrien condicionar instruccions molt diferents: si morfosintaxi afectada → reforcar A-13 (reduir subordinades), A-10 (ordre canonic); si semantica afectada → reforcar A-01 (vocab frequent), A-20 (densitat lexica); si pragmatica → reforcar B-03 (frase topic), B-10 (transicions).

### TDAH (2 sub-variables)
- `tdah.grau` (lleu/moderat/sever)
- `tdah.baixa_memoria_treball` (si/no)
- `tdah.fatiga_cognitiva` (si/no)

**Impacte potencial**: grau sever podria intensificar LF o activar mes micro-blocs. Baixa memoria treball → reforcar C-04 (chunking), C-01 (limitar conceptes). Fatiga cognitiva → textos mes curts, mes pauses visuals.

### Dislexia (2 sub-variables)
- `dislexia.tipus_dislexia` (fonologica/superficial/mixta)
- `dislexia.grau` (lleu/moderat/sever)

**Impacte potencial**: tipus fonologica → prioritzar descomposicio de compostes; superficial → prioritzar alta frequencia; grau sever → activar mes suports visuals.

### Disc. auditiva (2 sub-variables)
- `disc_auditiva.comunicacio` (oral/LSC/bimodal)
- `disc_auditiva.implant_coclear` (si/no)

**Impacte potencial**: LSC → simplificacio com L2 (ja a H-20 pero podria intensificar-se); implant coclear → menys simplificacio necessaria.

### Altres (7 sub-variables)
- `altes_capacitats.tipus_capacitat` (global/talent) — podria condicionar tipus de profunditzacio
- `nouvingut.calp` (inicial/emergent/consolidat) — podria modular intensitat adaptacio
- `nouvingut.familia_linguistica` — podria activar pistes etimologiques (ara nomes es mira L1_romanica)
- `vulnerabilitat.sensibilitat_tematica` — hauria d'activar E-10 (sensibilitat temes traumatics)
- `trastorn_emocional.sensibilitat_tematica` — idem
- `tdc.grau` — podria afectar LF/proposta

## Documents de referencia per a la investigacio

1. **Banc exhaustiu**: `docs/investigacio/banc_exhaustiu_instruccions_adaptacio.md` (119 instruccions, 1.691 linies)
   - Conte instruccions candidates per a cada barrera i perfil

2. **Mapa de barreres**: `docs/investigacio/mapa_barreres_perfil.md` (15 perfils × 10 dimensions, 1.397 linies)
   - Descriu amb detall com cada sub-variable modula la severitat de les barreres

3. **Sensibilitat LLM**: `docs/investigacio/analisi_capacitats_llm_adaptacio.md` (291 linies)
   - Indica quines instruccions el model pot seguir de forma fiable

4. **Arquitectura prompt v2**: `docs/decisions/arquitectura_prompt_v2.md` (651 linies)
   - La taxonomia consolidada de 95 instruccions amb classificacio LLM/codi/frontend

5. **Cataleg actual**: `instruction_catalog.py` — 89 instruccions amb `subvar_conditions` (nomes 3 instruccions en tenen)

6. **Filtre actual**: `instruction_filter.py` — `_check_subvar_conditions()` nomes comprova: `alfabet_llati`, `mecr_low`, `L1_romanica`

## Feina a fer

Per cada sub-variable no connectada:
1. Consultar el mapa de barreres per entendre com modula la severitat
2. Consultar el banc exhaustiu per trobar instruccions candidates
3. Decidir si l'efecte es: activar instruccio, condicionar instruccio existent, afectar proposta (DUA/LF/MECR), o anar a context (narrativa)
4. Verificar sensibilitat LLM: pot el model seguir la instruccio de forma fiable?
5. Implementar al cataleg + filtre

## Prioritzacio suggerida

| Prioritat | Sub-variables | Motiu |
|---|---|---|
| P1 | vulnerabilitat.sensibilitat, trastorn_emocional.sensibilitat | Bug: E-10 s'activa pel perfil pero la sub-variable no es consulta |
| P1 | tdl.morfosintaxi, tdl.semantica | 8 vars sense cap efecte, alt impacte pedagogic |
| P1 | tdah.baixa_memoria_treball, tdah.fatiga_cognitiva | Afecten directament carrega cognitiva |
| P2 | dislexia.tipus, dislexia.grau | Modulen tipus d'adaptacio |
| P2 | tdah.grau, tdc.grau | Podrien afectar LF/proposta |
| P2 | disc_auditiva.comunicacio | LSC vs oral canvia adaptacio |
| P3 | nouvingut.calp, nouvingut.familia_linguistica | Refinament, no critic |
| P3 | altes_capacitats.tipus_capacitat | Poc impacte |
