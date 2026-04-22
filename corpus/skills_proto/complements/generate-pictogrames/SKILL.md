---
name: generate-pictogrames
description: >
  Use when the teacher has activated the "pictogrames" complement. Adds
  supporting icons/emojis next to the key concepts DIRECTLY INSIDE the adapted
  text (not as a separate section). Typically useful for students with ASD,
  newcomers or intellectual disability, where visual anchors reinforce
  comprehension of abstract or technical vocabulary.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
complement_key: pictogrames
agent_role: complements
tools_required: []
triggers:
  - path: params.complements.pictogrames
    equals: true
---

# Afegir pictogrames al text adaptat

## Quan activar aquesta skill
Activar quan el docent ha marcat el complement **"Pictogrames"** al Pas 2.
Els pictogrames són **icones o emojis** que s'afegeixen **al costat dels
conceptes clau del text adaptat** com a ancoratge visual. Són especialment
útils per a:

- **Alumnat amb TEA** (Trastorn de l'Espectre Autista): l'ancoratge visual
  facilita la comprensió literal i redueix l'ambigüitat.
- **Alumnat nouvingut** (MECR baix): reforcen el significat quan el lèxic
  encara no és estable en català.
- **Alumnat amb DI** (Discapacitat Intel·lectual): els suports visuals són
  un principi bàsic de Lectura Fàcil.
- **Infantil i Cicle Inicial** en general.

## IMPORTANT — On s'integren els pictogrames

**Els pictogrames s'afegeixen DIRECTAMENT al text adaptat, inline, al costat
del concepte que representen. NO es genera una secció separada
`## Pictogrames`.**

Format inline: emoji immediatament **després** del concepte (abans també és
acceptable si millora la llegibilitat), separat per un espai:

```
El sol ☀️ dona llum i escalfor a la Terra 🌍. Les plantes 🌱 necessiten
l'aigua 💧 i el sol ☀️ per viure.
```

Això és diferent dels altres complements (glossari, preguntes, bastides,
activitats): pictogrames **modifica el text adaptat mateix**, no afegeix una
nova secció al final.

## Què fa aquesta skill

1. Identifica els **conceptes clau** del text adaptat: noms tècnics,
   elements curriculars, paraules abstractes que poden ser difícils.
2. Per a cada concepte, tria un **emoji universal** que el representi
   visualment.
3. **Insereix l'emoji inline** al text adaptat, immediatament després del
   concepte, separat per un espai.
4. Si un mateix concepte apareix moltes vegades al text, **només** afegir
   l'emoji les primeres 1-2 aparicions (evitar sobrecàrrega visual).

## Criteris de selecció d'emojis

Prioritzar, per aquest ordre:

1. **Emojis universals i reconeguts** (Unicode estàndard): ☀️ 💧 🌱 🔬 📚
   🏛️ 🌍 ⚡ 🔥 ❄️ 🌡️ 🐚 🦋 🐦 ⏰ 📅 🧮 ✏️ 📖 🗺️ 🎨 🎵 🏃 💭 ❤️ ⚖️.
2. **Emojis concrets** abans que abstractes (p.ex. 🌍 per «Terra» millor que
   un emoji ambigu per «planeta»).
3. **Coherència**: el mateix concepte sempre amb el mateix emoji al llarg
   del text.

Evitar:

- Emojis amb **càrrega cultural ambigua** (p.ex. banderes, gestos de mans
  que varien de significat entre cultures).
- Emojis de persones amb trets físics específics si no són rellevants.
- **Sobrecàrrega**: com a màxim 1 pictograma per frase curta, 2-3 per
  paràgraf. Si poses pictograma a cada paraula, perd la funció.
- Emojis decoratius que no aporten significat (no posar 🎉 a una frase sobre
  volcans «perquè quedi bonic»).

## Quan un concepte NO necessita pictograma

- Paraules quotidianes òbvies per al MECR de l'alumne.
- Connectors, preposicions, articles.
- Paraules que l'emoji no representa bé (millor deixar-ho sense que posar-ne
  un de confús).
- Noms propis, excepte si són icònics (p.ex. 🗽 per Estàtua de la Llibertat).

## Format de sortida

A diferència dels altres complements, aquesta skill **NO afegeix una secció
nova**. La sortida és el **text adaptat ja modificat** amb els emojis
inline.

Exemple — text adaptat original:

```markdown
### El cicle de l'aigua
L'aigua és molt important per a la vida. El sol escalfa l'aigua dels mars
i dels rius. L'aigua es converteix en vapor i puja cap al cel. Allà forma
els núvols. Després, l'aigua cau en forma de pluja.
```

Exemple — text adaptat amb pictogrames integrats:

```markdown
### El cicle de l'aigua 💧
L'aigua 💧 és molt important per a la vida. El sol ☀️ escalfa l'aigua dels
mars 🌊 i dels rius. L'aigua es converteix en vapor i puja cap al cel ☁️.
Allà forma els núvols ☁️. Després, l'aigua cau en forma de pluja 🌧️.
```

## Regles estrictes de la sortida

- **NO** generis una secció `### Pictogrames` ni `## Pictogrames` al final
  del text. Els pictogrames viuen dins del text adaptat.
- **NO** facis una llista a part del tipus «pictogrames usats». No cal.
- **Preserva** íntegrament el contingut i l'ordre del text adaptat; l'única
  cosa que canvia és l'addició d'emojis inline als conceptes clau.
- **No** posis emojis a les instruccions, bastides, glossari o altres
  seccions de sortida — només al cos del text adaptat.
- Si un concepte surt 5 vegades al text, l'emoji només apareix les primeres
  1-2 vegades.

## Exemple
Veure `assets/exemple-primaria-ciencies.md` (Cicle Mitjà, Ciències Naturals,
MECR A2) per veure un paràgraf abans i després amb els emojis integrats i
el raonament de cada tria.
