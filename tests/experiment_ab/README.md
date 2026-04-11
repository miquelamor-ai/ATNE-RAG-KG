# Xat 9 — Experiment A/B: Prompt mínim vs complet

## Estat: SCRIPTS LLESTOS, GENERACIÓ EN CURS

### Fitxers creats

| Fitxer | Descripció | Estat |
|--------|-----------|-------|
| `textos.json` | 30 textos (10 primària + 10 ESO + 10 batxillerat) | ✅ Complet |
| `perfils.json` | 6 perfils (3 simples + 3 complexos) | ✅ Complet |
| `rubrica.json` | 5 criteris amb descriptors 1-5 | ✅ Complet |
| `experiment_ab.py` | Generació 180 parells A/B amb Gemini | ✅ Complet |
| `eval_experiment.py` | Avaluació dual GPT-4o + Claude Sonnet | ✅ Complet |
| `stats_experiment.py` | Wilcoxon + Cohen's d + informe | ✅ Complet |
| `run_all.py` | Orquestrador (tot en seqüència) | ✅ Complet |

### Com executar

```bash
# Opció 1: Tot en seqüència
cd c:\Users\miquel.amor\Documents\GitHub\ATNE
python tests/experiment_ab/run_all.py

# Opció 2: Pas a pas
python tests/experiment_ab/experiment_ab.py     # Generació 180 parells
python tests/experiment_ab/eval_experiment.py   # Avaluació dual
python tests/experiment_ab/stats_experiment.py  # Anàlisi + informe

# Opció 3: Saltar generació (si ja tens resultats_generacio.json)
python tests/experiment_ab/run_all.py --skip-gen

# Opció 4: Només estadístiques
python tests/experiment_ab/run_all.py --only-stats
```

### Nota sobre quota Gemini
Les claus gratuïtes tenen límit de 15 req/min i 1500 req/dia.
Amb 180 parells × 2 condicions = 360 crides, cal esperar entre crides.
L'script té recuperació automàtica (guarda cada 5 parells).
Si falla, simplement relança i continuarà des d'on s'havia quedat.

### Disseny de l'experiment

**30 textos** × **6 perfils** = **180 parells A/B**

Condició A (mínim): "Adapta per a [perfil], [etapa], MECR [X]"
Condició B (complet): Pipeline sencer (98 instruccions + identitat + DUA + persona)

**Jutges**: GPT-4o + Claude Sonnet (via OpenRouter)
**Rúbrica**: 5 criteris (adequació lingüística, fidelitat, perfil, llegibilitat, complements)
**Anàlisi**: Wilcoxon parells aparellats + Cohen's d + concordança inter-jutge

**Llindar decisió**:
- Diferència > 0.5 punts → prompt complet val la pena
- Diferència < 0.3 → prompt mínim suficient
- Entremig → cal més dades
