---
name: generar-pictogrames
description: Instrument per afegir pictogrames (emojis) al text adaptat. Pre-A1 inline + paratext lateral. A1 inline discret. A2+ glossari visual al peu (NO inline). Emojis universals, coherents, sense càrrega cultural ambigua. MECR pre-A1-C1. Correccions MALL 2026-05-17 aplicades.
type: instrument
categoria_principal: mediacio
categories_secundaries: []
mecr_range: [pre-A1, A1, A2, B1, B2, C1]
agent_roles: [generator]
translanguaging: false
multimodal: true
skill_meta: generate-pictogrames@corpusFJE/skills/mediacio/generate-pictogrames
version: 2.0.0-bootstrap
---

# Generar pictogrames — V2 Descriptiu

## Descripció

El complement de pictogrames afegeix suport visual emoji al text adaptat per facilitar la descodificació. La funció i la ubicació canvien radicalment per nivell: a pre-A1, els emojis van **inline** (damunt o al costat de cada paraula clau) i es genera un **paratext d'anticipació** amb el vocabulari visual; a A2+, els emojis van **al peu com a glossari visual** i mai inline al text corrent.

**Principi clau**: el pictograma és una bastida de descodificació a pre-A1/A1, i un glossari visual de referència a A2+. La mateixa forma serveix funcions completament diferents.

## La diferència fonamental per nivell

| Nivell | Densitat | Col·locació | Paratext lateral |
|---|---|---|---|
| **Emergent (pre-A1)** | 1-2 per frase (noms + verbs clau) | Inline, damunt/costat de la paraula | Sí: paratext d'anticipació esquerre |
| **Inicial (A1)** | 1 per frase o per terme tècnic | Inline, discret | Opcional |
| **Funcional (A2)+** | Mínims | Glossari visual al peu/marge — NO inline | No |

## Modulació per nivell MECR

### Pre-A1 — Emergent

Cada nom i verb clau porta el seu emoji immediatament al costat dins de la frase. El lector visual no ha de buscar: pictograma i paraula van junts. A més, es genera un **paratext d'anticipació** al principi: vocabulari visual que mostra els conceptes clau ABANS de llegir el text.

Format pre-A1:
```
### Vocabulari del text (mira primer!)
☀️ sol · 💧 aigua · 🌳 arbre

---

El sol ☀️ dona llum. Les plantes 🌱 necessiten l'aigua 💧 per créixer.
```

### A1 — Inicial

Un pictograma per frase, preferentment al costat dels termes tècnics o nous. Si una frase curta ja és comprensible sense pictograma, no forçar-ne cap. Evitar sobrecàrrega.

Format A1:
```
El sol ☀️ dona llum i escalfor a la Terra. Les plantes necessiten
l'aigua 💧 per viure.
```

### A2 — Funcional

Cap pictograma inline al text corrent. Si el text té termes complexos, s'afegeix un **glossari visual** al peu (2 columnes: emoji + terme).

Format A2+:
```
[text adaptat sense emojis inline]

---
**Vocabulari visual**
☀️ radiació solar · 🌡️ temperatura · 🌊 evaporació
```

### B1, B2, C1

Glossari visual al peu si el text té terminologia específica que es beneficia del suport icònic. Si els termes son abstractes sense emoji obvi, millor no posar glossari.

## Criteris de selecció d'emojis

**Prioritzar per ordre:**
1. Emojis universals i reconeguts (Unicode estàndard): ☀️ 💧 🌱 🔬 📚 🏛️ 🌍 ⚡ 🔥 ❄️ 🌡️ 🦋 ⏰ 📅 🧮 ✏️ 📖 🗺️
2. Emojis concrets abans que abstractes.
3. Coherència: el mateix concepte sempre amb el mateix emoji en tot el document.

**Evitar:**
- Emojis amb càrrega cultural ambigua (banderes de països específics, gestos de mans).
- Emojis decoratius que no aporten significat ("✨", "💫").
- Si un concepte no té emoji clar i universal, millor no posar-ne cap.

## Regles crítiques

**FER:**
- Pre-A1: paratext d'anticipació PRIMER, llavors text amb emojis inline.
- A1: un emoji per frase, al costat del terme més difícil.
- A2+: glossari visual al peu, text corrent sense emojis.
- Coherència: el mateix emoji per al mateix concepte en tot el document.
- Emojis universals i sense ambigüitat cultural.

**NO FER:**
- ❌ A2+: emojis inline al text corrent.
- ❌ Mostrar el mateix emoji més de 2 vegades si apareix 5+ vegades.
- ❌ Emojis a bastides, glossari verbal, preguntes o altres complements.
- ❌ Secció "Pictogrames usats" al final: no cal llistat separat.
- ❌ Emojis per a conceptes abstractes sense representació visual clara.

## Connexions MALL

- **Descodificació visual com a competència lectora emergent**: a pre-A1, l'emoji és el text per a lectors logogràfics o amb alfabet diferent. L'emoji i la paraula van junts perquè el lector associa forma visual amb so/significat. És el pont entre la lletra i el concepte.
- **Paratext d'anticipació com a activació de coneixement previ**: mostrar el vocabulari visual ABANS de llegir activa els coneixements previs de l'alumne i redueix la càrrega cognitiva de la lectura. Es tracta d'aplicar el principi de "context before text".
- **Glossari visual A2+ com a referència, no com a bastida**: a A2+, l'alumne ja pot llegir sense suport visual inline. El glossari al peu és un recurs de referència (com un diccionari visual), no una bastida de descodificació. Mantenir-los inline a A2+ introduiria noise visual i distracció.

## Detecció

**Senyals docent**: ha activat el complement "Pictogrames" al Pas 2. L'alumnat destinatari és pre-A1, A1 o alumnat amb DUA Accés que necessita suport visual de descodificació.

**Senyals alumne**: no reconeix les paraules escrites però pot reconèixer el referent visual; es "perd" en el text per no saber per on seguir; necessita suport de descodificació per mantenir el fil del text.

**Context favorable**: primària inicial i infantil, alumnat nouvingut pre-A1/A1, alumnat amb TEA o dificultats de lectura, alumnat amb DUA Accés.

**Anti-senyals**: el text és per a B1+ amb lectors funcionals → prescindir d'emojis inline; el text és molt abstracte (matemàtiques, filosofia) → sense pictogrames o glossari visual mínim.

## Heurístiques docent

**H1 — El test de l'emoji: "Quin emoji li posaries?"**
Per a cada terme clau del text, demano als alumnes: "Quin emoji li posaries?" Treballen en parelles i decideixen. L'exercici entrena la consciència semàntica i la capacitat de trobar representació visual per als conceptes.

**H2 — El paratext com a pre-lectura (pre-A1/A1)**
Proposo que l'alumne vegi el paratext d'anticipació (vocabulari visual) abans de llegir el text. Assenyala cada emoji i diu el nom en veu alta. Quan llegeix el text i troba l'emoji, el reconeix. La lectura s'accelera perquè el vocabulari ja és conegut.

**H3 — Coherència de l'emoji com a norma de classe**
Per a textos llargs o projectes multi-sessió, estableixo un "diccionari d'emojis" de classe: els mateixos emojis per als mateixos conceptes en tots els textos del trimestre. La coherència entre textos reforça la memòria semàntica.

## Autoavaluació (descriptors en primera persona)

- *Pre-A1*: "He vist els emojis i he dit el nom de cada objecte." (oral)
- *A1*: "He usat els emojis per entendre les paraules difícils."
- *A2*: "He usat el glossari visual al peu per recordar el significat dels termes."
- *B1+*: "He identificat quins termes necessitaven un pictograma de referència."

## Fonts principals

- MALL (Model d'Aprenentatge de Llengües i Literacitat): multimodalitat, paratext d'anticipació.
- Mayer, R.E. (2009): *Multimedia Learning* — redundàcia codis visual+verbal per a memoritzar.
- ARASAAC: sistema de pictogrames per a Comunicació Augmentativa i Alternativa (referent per a pre-A1/TEA).
- Decret 175/2022 (currículum Catalunya): competència en comunicació lingüística, dimensió multimodal.
