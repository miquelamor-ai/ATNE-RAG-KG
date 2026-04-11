# Informe Xat 9 — Experiment A/B: Prompt mínim vs complet

**Data**: C:\Users\miquel.amor\Documents\GitHub\ATNE\tests\experiment_ab\resultats_avaluacio.json

**Parells avaluats**: 180


## Resultats — Jutge: GPT-4o

| Criteri | Mitjana A | Mitjana B | Diff (B-A) | Wilcoxon p | Cohen's d | Interpretació |
|---|---|---|---|---|---|---|
| adequacio_linguistica | 4.11 | 4.06 | -0.05 | 0.3535 | -0.15 (negligible) | DIFERÈNCIA NEGLIGIBLE — prompt mínim suficient |
| fidelitat_curricular | 4.22 | 4.40 | +0.18 | 0.0018** | +0.32 (petit) | DIFERÈNCIA NEGLIGIBLE — prompt mínim suficient |
| adequacio_perfil | 3.63 | 4.35 | +0.72 | 0.0000** | +0.80 (mitjà) | PROMPT COMPLET VAL LA PENA |
| llegibilitat_estructura | 4.34 | 4.45 | +0.12 | 0.0793 | +0.21 (petit) | DIFERÈNCIA NEGLIGIBLE — prompt mínim suficient |
| complements | 2.54 | 4.51 | +1.97 | 0.0000** | +2.06 (gran) | PROMPT COMPLET VAL LA PENA |

**Puntuació global ponderada**: A=3.81, B=4.33, Diff=+0.52, p=0.0000, d=+1.16

**Decisió**: PROMPT COMPLET VAL LA PENA


## Resultats — Jutge: Claude Sonnet

| Criteri | Mitjana A | Mitjana B | Diff (B-A) | Wilcoxon p | Cohen's d | Interpretació |
|---|---|---|---|---|---|---|
| adequacio_linguistica | 3.57 | 3.62 | +0.04 | 1.0000 | +0.06 (negligible) | DIFERÈNCIA NEGLIGIBLE — prompt mínim suficient |
| fidelitat_curricular | 3.74 | 4.28 | +0.53 | 0.0001** | +0.81 (gran) | PROMPT COMPLET VAL LA PENA |
| adequacio_perfil | 2.57 | 3.21 | +0.64 | 0.0254** | +0.42 (petit) | PROMPT COMPLET VAL LA PENA |
| llegibilitat_estructura | 3.98 | 3.89 | -0.09 | 1.0000 | -0.12 (negligible) | DIFERÈNCIA NEGLIGIBLE — prompt mínim suficient |
| complements | 1.66 | 4.09 | +2.43 | 0.0000** | +2.55 (gran) | PROMPT COMPLET VAL LA PENA |

**Puntuació global ponderada**: A=3.13, B=3.76, Diff=+0.63, p=0.0000, d=+0.96

**Decisió**: PROMPT COMPLET VAL LA PENA


## Concordança inter-jutge (GPT-4o vs Claude Sonnet)

- **adequacio_linguistica** (A): Kappa=0.70, r=-0.77, n=47
- **adequacio_linguistica** (B): Kappa=0.79, r=-0.05, n=47
- **fidelitat_curricular** (A): Kappa=1.00, r=0.62, n=47
- **fidelitat_curricular** (B): Kappa=1.00, r=0.17, n=47
- **adequacio_perfil** (A): Kappa=0.57, r=0.50, n=47
- **adequacio_perfil** (B): Kappa=0.36, r=0.53, n=47
- **llegibilitat_estructura** (A): Kappa=0.91, r=0.19, n=47
- **llegibilitat_estructura** (B): Kappa=0.87, r=0.16, n=47
- **complements** (A): Kappa=0.74, r=0.38, n=47
- **complements** (B): Kappa=0.87, r=0.31, n=47

## Diferències per etapa

- primaria / adequacio_linguistica: diff=-0.03 (n=60)
- primaria / fidelitat_curricular: diff=+0.13 (n=60)
- primaria / adequacio_perfil: diff=+0.72 (n=60)
- primaria / llegibilitat_estructura: diff=+0.22 (n=60)
- primaria / complements: diff=+1.95 (n=60)
- ESO / adequacio_linguistica: diff=-0.08 (n=59)
- ESO / fidelitat_curricular: diff=+0.14 (n=59)
- ESO / adequacio_perfil: diff=+0.71 (n=59)
- ESO / llegibilitat_estructura: diff=+0.07 (n=59)
- ESO / complements: diff=+1.92 (n=59)
- batxillerat / adequacio_linguistica: diff=+0.00 (n=19)
- batxillerat / fidelitat_curricular: diff=+0.47 (n=19)
- batxillerat / adequacio_perfil: diff=+0.74 (n=19)
- batxillerat / llegibilitat_estructura: diff=-0.11 (n=19)
- batxillerat / complements: diff=+2.21 (n=19)