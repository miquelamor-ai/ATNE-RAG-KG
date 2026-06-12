# Baseline `a5f7981` — constància dels 3 canvis acumulats

> Constància **versionada**. La mateixa nota va a la descripció del PR de
> `feat/mapa-conceptual-novak-fallback`; es deixa també aquí perquè el registre
> quedi al repo encara que el PR es creï tard.

El commit `a5f7981` («test(baseline): regenera baseline_prompts amb el bloc
"Per al docent" 9-cat») regenera `tests/baseline_prompts/` — **cap canvi de codi,
només el snapshot**. Les fotos del prompt estaven **congelades des de l'1/06**
(`8a312d4`), així que el diff captura **TRES** evolucions acumulades del
`prompt_builder`, **no només el bloc 9-cat**. Totes tres ja estaven **fusionades
a `main`**:

1. **Bloc «Per al docent» → 9 categories A-I** — substitueix els 5 punts genèrics
   antics.
2. **Format de gènere delegat a la SKILL activa** — el bloc llarg hardcoded
   (titular/lead/piràmide…) → versió curta «tal com la defineix la SKILL ACTIVA,
   NO la reinterpretis» (commit `ae80831`).
3. **Instrucció de títol** — la 1a línia de `## Text adaptat` ha de ser `# Títol`
   al camí 2-call (commit `358a317`).

A més, **1 línia** a `aacc…complements` (`generate-rubriques`: «4-5» → «5-6
criteris», descriptor del canon ja vigent abans d'aquesta branca).

## Per què aquesta nota i no una reescriptura del commit

El **missatge** d'`a5f7981` només menciona el 9-cat, així que **infravalora el
diff**. Es va decidir **NO reescriure'l**: és història **ja publicada** a origin i
la branca `feat/editor-diagrames-novak` hi penja a sobre. Reescriure-la voldria
dir un *force-push* de la base d'una branca activa d'un altre context — el cost no
paga el defecte d'un missatge incomplet. Aquesta nota completa el registre sense
tocar res publicat.

Rastreig de confirmació: gènere `ae80831` i títol `358a317` són **ancestres de
`origin/main`** (evolucions legítimes ja fusionades, res colat).
