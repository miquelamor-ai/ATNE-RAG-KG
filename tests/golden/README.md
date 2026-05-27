# Golden Harness — Fase A

Aquesta carpeta conté el **harness de qualitat offline** d'ATNE.

## Què fa

Validar, sense cridar el LLM (zero cost, segons), que el sistema **fa el que ha
de fer** per a cada combinació canònica de:

- **12 condicions** (TEA, TDAH, dislèxia, DI, TDL, AC, aud, vis, tdc, cat, vuln, emo)
- **MECRs** (pre-A1 → C2) i **DUA** (Accés / Core / Enriquiment)
- **Gèneres discursius** (24 SKILLs `write-*`)
- **Complements** (12 a la matriu canònica de saber-ne+ §7)

Comprova 3 coses per cada cas:

1. **Skills activades** = expected_skills · diff +/-
2. **Defaults UI alineats amb la matriu canònica** · `pas2.html:MATRIU_CONDICIONS`
3. **`instruction_filter.get_instructions()` no peta** i activa macrodirectives

## Com s'executa

```bash
python tests/golden/run_golden.py                       # tots els casos
python tests/golden/run_golden.py --case C01_tea_b1_noticia
python tests/golden/run_golden.py --json                # JSON, no markdown
python tests/golden/run_golden.py --no-write            # no escriu _report.md
```

Genera `tests/golden/_report.md` amb el resum + heatmap + detall.

## Estructura

| Fitxer | Què és |
|---|---|
| [`matrix.yaml`](matrix.yaml) | **Canon executable**. Mapping condicions→backend keys, complements→SKILL, matriu defaults per condició, gèneres canònics, MECRs. Font: `saber-ne+ §7` + `pas2.html:MATRIU_CONDICIONS`. |
| [`cases.yaml`](cases.yaml) | **15 casos golden** (12 condicions individuals + 3 multi-condició). Cadascun amb `expected_skills`. |
| [`run_golden.py`](run_golden.py) | **Runner offline**. Crida `skills_loader.select_active` i `instruction_filter.get_instructions`. Genera report MD. |
| `_report.md` | Output de l'última execució (no commiteig recomanat — afegir a `.gitignore` si vols). |

## Què detecta (al primer cop)

Mentre escrivíem el harness ja n'hem trobat un parell:

- **`MATRIU_CONDICIONS` (pas2.html) inclou `tdc`, `vuln`, `emo`** com a
  condicions canòniques, però **`ALL_CHAR_KEYS` (llm.js:46)** NO les reconeix.
  Conclusió: defaults i instruccions PERFIL no s'activen mai per a aquestes
  3 condicions. Capturat com a `chars_key: null` a `matrix.yaml` i marcat
  `gap_known` als casos C09/C11/C12.
- **`discalculia`** apareix a `ALL_CHAR_KEYS` però NO a la matriu §7. Marcat
  `fora_matriu: true`.

Aquestes són troballes diagnòstiques del propi exercici de muntar el harness.

## Què NO fa la Fase A (Fase B en endavant)

- ❌ No crida `/api/adapt` ni cap LLM (cost zero, però no valida output real).
- ❌ No avalua qualitat pedagògica del text adaptat (això és Fase B — LLM-as-Judge).
- ❌ No mesura mida del prompt en tokens (futur — budget).
- ❌ No genera dashboard `/admin/health` (futur — Capa 5).

## Fase B — LLM-as-Judge (cost monetari)

Disponible a [run_phase_b.py](run_phase_b.py). Per cada cas del Golden Suite:

1. Crida `/api/adapt` real per generar text adaptat + complements.
2. Demana al judge LLM (Gemini Flash per defecte) que apliqui [judge_rubric.yaml](judge_rubric.yaml) sobre l'output.
3. Aggrega tots els judgments en un report ([_phase_b_report.md](_phase_b_report.md)).

**Pre-requisits**:
- Servidor ATNE up a `http://localhost:8000` (o passar `--server URL`).
- `.env` amb `GEMINI_API_KEY`.

**Comandes**:

```bash
python tests/golden/run_phase_b.py --plan         # mostra pla, NO executa (cost zero)
python tests/golden/run_phase_b.py --full         # generate + judge + aggregate
python tests/golden/run_phase_b.py --generate     # només genera adaptacions
python tests/golden/run_phase_b.py --judge        # només judge sobre outputs ja generats
python tests/golden/run_phase_b.py --aggregate    # només refà el report (sense crides LLM)
python tests/golden/run_phase_b.py --case C01_tea_b1_noticia --full   # un sol cas
```

**Cost primera passada**: ~0.03 € (15 casos × 1 text × 2 crides LLM amb Gemini Flash). Negligible. Si s'escala a 24 gèneres × 12 condicions × 3 textos = ~0.6 €.

**Rúbrica**: 6 criteris (adequació MECR, perfil aplicat, complements coherents, fidelitat semàntica, estructura gènere, llegibilitat LF) amb escala 0-5 i pautes explícites perquè el judge sigui consistent.

**Output schema**: JSON per cada judgment a [judgments/](judgments/) (gitignorat). Aggregator genera un score global ponderat per cas + flags d'alertes greus.

## Quan executar-lo

- **Abans de cada commit que toca**: `instruction_catalog.py`, `instruction_filter.py`,
  `prompt_builder.py`, `skills_loader.py`, qualsevol SKILL.md, o `MATRIU_CONDICIONS`
  a `pas2.html`.
- **Després d'afegir una condició o un complement nou** — primer
  el cas a `cases.yaml`, després el runner ha de quedar PASS.
- **Setmanalment** durant pilots, com a baseline.

## Codis d'estat

| | Significat |
|---|---|
| ✅ PASS | Skills actives = esperades · filter OK |
| ⚠️ WARN | Diferència esperada (gap conegut documentat) o SKILLs extra |
| ❌ FAIL | SKILLs esperades absents (sense gap documentat) |
| 💥 ERROR | `instruction_filter` peta o excepció no controlada |
