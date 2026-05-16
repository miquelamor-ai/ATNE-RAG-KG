---
name: generate-bastides-lectura
description: >
  Use when the teacher has activated the "bastides" complement. Generates
  reading scaffolds for the 3 moments (Abans / Durant / Després) and 3 planes
  (literal / inferencial / crític). Always active when bastides complement is on,
  regardless of whether production complements are active. At Emergent/pre-A1:
  physical and gestural activities only — zero written production. Modulated by
  MECR level.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
complement_key: bastides
agent_role: complements
tools_required: []
triggers:
  - path: params.complements.bastides
    equals: true
---

# Generar bastides de lectura

## Funció d'aquest instrument

Les bastides de lectura guien l'alumne als **tres moments** del procés lector
i als **tres plànols** de comprensió. Són sempre actives quan el complement
"bastides" és activat — independentment de si hi ha producció.

Es diferencien del complement `preguntes_comprensio`: les bastides de lectura
proporcionen el **procediment** (com llegir), no les preguntes (què cal respondre).

## Gradació per nivell MALL

| Nivell | Abans | Durant | Després |
|---|---|---|---|
| **Emergent (pre-A1)** | Assenyalar imatges, predicció oral amb adult | L'adult llegeix en veu alta; infant assenyala | Dibuixar el que ha après; dictat a l'adult |
| **Inicial (A1)** | 1 pregunta d'activació + predicció pel títol | Subratlla 1 mot clau per paràgraf | Frase marc: «El text parla de ___» |
| **Funcional (A2)** | 2 preguntes + propòsit de lectura explícit | Marca ✓/? /! al marge | Resum 2-3 frases + 1 pregunta inferencial |
| **Estratègic (B1)** | Activació + predicció + hipòtesi pròpia | Notes marginals + hipòtesi en curs | Resum + inferència + valoració |
| **Acadèmic (B2)** | + identificació del gènere i l'autor | + detecció de posicionament | + avaluació de fiabilitat |
| **Crític (C1)** | + formulació de preguntes pròpies | + contrast amb coneixements previs | + autoregulació: «He entès el que calia?» |

## Format de sortida

```markdown
## Suports de lectura

### Abans de llegir
- **Activa els previs**: «Què saps de [tema del text]?»
- **Predicció**: «Mira el títol [i la imatge]. Què creus que explicarà?»
- **Propòsit**: «Llegeix per saber [una cosa concreta i rellevant del text].»

### Durant la lectura
- Subratlla [1-2 tipus d'informació clau específics del text]
- Marca al marge: **✓** entès · **?** dubte · **!** important

### Després de llegir
- *Literal*: «[Frase marc incompleta sobre la idea principal del text]»
- *Inferencial*: «[Pregunta que obliga a relacionar o interpretar, no a copiar]»
- *Valoració*: «[Pregunta de posicionament o transferència]»
```

## Regles estrictes de sortida

- Comença **sempre** amb `## Suports de lectura`.
- **Pre-A1**: substitueix tota escriptura autònoma per accions físiques (assenyalar, dibuixar, dramatitzar, dictar a l'adult). La bastida pre-lectura és ORAL.
- Les preguntes "Després de llegir" han de cobrir els 3 plànols (literal / inferencial / crític) en proporció al MECR (veure taula gradació M2).
- El propòsit de lectura ("Llegeix per saber...") ha de ser **específic del text**, no genèric.
- NO generis les mateixes preguntes que el complement `preguntes_comprensio` — les bastides de lectura donen el MARC, les preguntes comprensió fan el treball de comprensió detallat.
- Màxim 3 ítems per moment. Menys és més.
- La frase marc del Resum ha de tenir **un sol buit** i ser completable en 1-2 línies.
