---
name: write-enciclopedic
description: >
  Use when adapting or generating an enciclopèdic entry for students.
  Activates when genre_discursiu == "enciclopedic". Applies single-sentence
  nuclear definition, category-first structure, and immediate concrete
  example. Output: enciclopèdic entry in markdown with term, definition,
  expanded explanation, and example.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
genre_key: enciclopedic
tipologia: Expositiva
mecr_range: [A1, A2, B1, B2, C1]
agent_role: adapter
tools_required: []
triggers:
  - path: params.genere_discursiu
    equals: enciclopedic
---

# Escriure/adaptar una entrada enciclopèdica

## Quan activar aquesta skill
Activar quan el docent ha seleccionat el gènere "enciclopedic" al Pas 2
de l'adaptador. L'entrada enciclopèdica defineix un terme amb precisió
i el contextualitza amb un exemple concret.

## Estructura canònica
Tota entrada enciclopèdica adaptada ha de tenir **aquestes parts, en
aquest ordre**:

1. **Terme** — la paraula o concepte definit.
2. **Definició nuclear** — una sola frase, sense subordinades.
3. **Explicació ampliada** — desenvolupament amb detalls addicionals.
4. **Exemple** — un cas concret que il·lustra la definició.

## Regles crítiques (FER)
- **Definició nuclear en una sola frase**, sense subordinades.
- **Evitar circularitat**: no definir X usant X o paraules de la
  mateixa arrel.
- **Exemple concret immediatament** després de la definició.
- **Categoria primer, especificitat després** ("La balena és un
  mamífer gran que viu al mar").

## Contraindicacions (NO FER)
- ❌ Definicions per negació ("no és X") com a primera línia.
- ❌ Sinònims com a definició ("llibre: obra literària").
- ❌ Etimologia abans del significat.
- ❌ Referències a entrades anteriors/posteriors.

## Modulació per MECR
- **A1-A2**: definició d'una frase curta (màx 10 paraules).
  Explicació ampliada de 2-3 frases. Un exemple visual i quotidià.
- **B1-B2**: definició precisa. Explicació ampliada amb 2-3 detalls.
  Exemple concret.
- **C1**: definició completa. Explicació amb matisos i múltiples
  exemples si cal.

## Format de sortida
```markdown
# [Terme]

[Definició nuclear: una frase amb estructura "És un [categoria]
que [especificitat]".]

[Explicació ampliada: 2-3 frases amb detalls.]

**Exemple:** [Cas concret que il·lustra la definició.]
```

## Exemple
Veure `assets/exemple-basic-A2.md` per a una entrada enciclopèdica nivell A2.
