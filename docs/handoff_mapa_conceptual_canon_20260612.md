# Handoff a mineriaRAG — format de les branques del mapa conceptual · 2026-06-12

> Per a l'equip/xat mineriaRAG. Decisió PEDAGÒGICA a canonitzar a la SKILL
> `generate-mapa-conceptual`. ATNE n'és consumidor; no toca el format pel seu compte.

## (a) Context

Auditoria ATNE 12/06 (consultoria Fable + verificació codi). El renderitzador de diagrames
d'ATNE (`ui/atne/js/mermaid-converter.js`, SVG pur) pinta com a **node-proposició** (oval en
cursiva, estil Novak) qualsevol node **en negreta que no sigui l'arrel**. La pregunta: quin
ha de ser el format de les branques del mapa conceptual?

## (b) Estat actual + EVIDÈNCIA

**El canon `generate-mapa-conceptual` ja demana "branques en negreta amb noms de CATEGORIA
relacional"** (Causes, Conseqüències, Tipus de, Processos). Bé. PERÒ una verificació real
(gpt-4o, camí de producció 2-call, cas B1 Revolució Industrial) mostra **dos problemes de
compliment de prompt**:

```
## Mapa conceptual
### **La Revolució Industrial**     ← H3 (el canon diu "Cap H3")
- **Inici**                          ← branca en negreta, però a COLUMNA 0 (no sagnada)
  - Va començar a Gran Bretanya
- **Innovacions tecnològiques**
  - Màquina de vapor
...
```

1. El LLM posa el **concepte central com a `###`** (encapçalament), tot i que el canon ho
   prohibeix. El parser del renderitzador **filtra les línies `#`** → **el concepte central
   es PERD** i la 1a branca («Inici») es promociona malament a arrel → mapa trencat.
2. Les branques surten **en negreta amb noms de categoria** (correcte segons el canon
   ACTUAL), però a columna 0 en lloc de sagnades sota l'arrel.

→ **Problema de compliment**, rellevant decidiu el format que decidiu: caldria **reforçar al
canon** que el concepte central és l'ÚNICA arrel de LLISTA en negreta (mai `###`) i que les
branques pengen per sagnia. (ATNE ja ho ha reforçat al seu fallback de crida única per
no divergir; el camí de producció depèn de la SKILL.)

## (c) Proposta a valorar (decisió pedagògica)

Quin contingut han de tenir les branques en negreta (= els nodes-proposició)?

- **Opció 1 — mantenir NOMS DE CATEGORIA** (actual): Causes, Conseqüències, Tipus de.
  Bastida classificatòria; senzilla.
- **Opció 2 — PARAULES D'ENLLAÇ VERBALS** (Novak pur): «necessita», «provoca», «es produeix
  a». Formen una PROPOSICIÓ llegible (concepte + enllaç + concepte): *«La fotosíntesi
  NECESSITA llum»*. És on viu la comprensió relacional; més exigent.
- **Opció 3 — GRADUAR PER MECR** (proposta ATNE, coherent amb el MALL):
  - **A2**: noms de categoria (bastida classificatòria — l'alumne aprèn a agrupar).
  - **B1+**: paraules d'enllaç verbals (mapa proposicional — l'alumne explicita la relació).
  Segueix la lògica de gradació del canon (la profunditat ja es gradua per MECR).

## (d) Nota tècnica (no condiciona la decisió)

**El renderitzador d'ATNE pinta els DOS formats sense cap canvi de codi**: tota negreta
no-arrel és un node-proposició, contingui un nom de categoria o un verb. Per tant la decisió
és **purament pedagògica** i es canonitza a la SKILL `generate-mapa-conceptual` (+ rubrica.json
gradada). Verificat amb el parser real: l'exemple Novak amb verbs dona 1 root + 3 prop + 5
concept; el de categories, 1 root + 2 prop + 3 concept — tots dos correctes. Test de regressió
afegit a `tests/test_diagrames_parse.js` (al CI d'ATNE).

Quan decidiu, canonitzeu-ho a la SKILL i ATNE ho consumirà a tots els camins (producció +
fallback), sense divergència.
