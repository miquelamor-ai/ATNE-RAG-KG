---
name: generate-pictogrames
description: >
  Use when the teacher has activated the "pictogrames" complement. Adds
  emoji/icon visual supports to the adapted text. At Emergent/pre-A1: inline
  above/beside each key noun and verb (1-2 per sentence) + lateral paratext
  for anticipation. At A1: 1 pictogram per sentence or technical term. At
  A2+: visual glossary only (icons beside terms in a side list, NOT inline
  in running text). Modulated strictly by MECR level.
author: FJE — Fundació Jesuïtes Educació
version: 2.0.0-proto
complement_key: pictogrames
agent_role: complements
tools_required: []
triggers:
  - path: params.complements.pictogrames
    equals: true
---

# Afegir pictogrames al text adaptat

## Distinció fonamental (MALL)

La funció i la col·locació dels pictogrames canvien radicalment per nivell:

| Nivell | Densitat | Col·locació | Paratext lateral |
|---|---|---|---|
| **Emergent (pre-A1)** | 1-2 per frase (noms + verbs clau) | **Inline** (damunt o al costat de cada paraula clau) | ✅ Paratext d'anticipació al marge esquerre (dona context ABANS de llegir) |
| **Inicial (A1)** | 1 per frase o per tecnicisme | Inline, discret | Opcional |
| **Funcional (A2)+** | Mínims | **Glossari visual** al peu o marge — NO inline al text corrent | ❌ |

A Emergent el pictograma és el suport principal de descodificació.
A A2+ el pictograma és una referència de glossari; el text corrent no s'interromp.

## Comportament per nivell

**Emergent (pre-A1):**
Cada nom i verb clau porta el seu emoji **immediatament damunt o al costat** dins
de la frase. El lector visual no ha de buscar: el pictograma i la paraula van junts.
A més, es genera un **paratext lateral d'anticipació** (columna esquerra o capçalera
visual) que mostra els conceptes clau del text ABANS de llegir-lo.

**Inicial (A1):**
Un pictograma per frase, preferentment al costat dels termes tècnics o nous.
Evitar sobrecàrrega: si una frase curta ja és comprensible, no forçar pictograma.

**Funcional (A2) i superior:**
Cap pictograma inline al text corrent. En canvi, si el text té termes complexos,
es pot afegir un **glossari visual** al peu (2 columnes: emoji + terme), a l'estil
del complement Glossari.

## Format de sortida — Emergent (pre-A1)

```markdown
### Vocabulari del text (mira primer!)
☀️ sol · 💧 aigua · 🌳 arbre · 🦋 papallona

---

El sol ☀️ dona llum i escalfor. Les plantes 🌱 necessiten
l'aigua 💧 i el sol ☀️ per créixer.
```

## Format de sortida — Inicial (A1)

```markdown
El sol ☀️ dona llum i escalfor a la Terra. Les plantes necessiten
l'aigua 💧 per viure. El cicle de l'aigua és molt important.
```

## Format de sortida — Funcional (A2+)

El text corrent NO porta emojis. Si hi ha termes complexos, s'afegeix:

```markdown
[text adaptat sense emojis inline]

---
**Vocabulari visual**
☀️ radiació solar · 🌡️ temperatura · 🌊 evaporació
```

## Criteris de selecció d'emojis

Prioritzar, per ordre:
1. **Emojis universals i reconeguts** (Unicode estàndard): ☀️ 💧 🌱 🔬 📚 🏛️ 🌍 ⚡ 🔥 ❄️ 🌡️ 🦋 ⏰ 📅 🧮 ✏️ 📖 🗺️
2. **Emojis concrets** abans que abstractes.
3. **Coherència**: el mateix concepte sempre amb el mateix emoji.

Evitar:
- Emojis amb càrrega cultural ambigua (banderes, gestos de mans).
- Emojis decoratius que no aporten significat.
- Si un concepte no té emoji clar, millor no posar-ne cap.

## Regles estrictes de sortida

- A2+: **MAI** emojis inline al text corrent. Glossari visual al peu si cal.
- Si el pictograma apareix 5 vegades, mostrar-lo com a molt les primeres 1-2.
- **NO** generis una secció `### Pictogrames usats`. No cal llistat separat.
- **NO** posis emojis a les bastides, glossari, preguntes o altres seccions.
- **Preserva** íntegrament el contingut del text adaptat; l'única addició és visual.

## Exemple
Veure `assets/exemple-emergent-infantil.md` (pre-A1, Infantil, paràgraf amb
paratext d'anticipació + inline) i `assets/exemple-a2-ciencies.md` (A2,
glossari visual al peu, sense inline).
