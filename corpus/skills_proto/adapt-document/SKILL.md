---
name: adapt-document
description: >
  Use when adapting a structured document (PDF, PPTX) segment by segment.
  Each segment is an independent text block (title, paragraph, exercise,
  question, instruction) extracted from the original layout. The LLM must
  treat each segment in isolation while maintaining consistent register and
  adaptation level across the whole document. The layout (columns, tables,
  blank lines, exercise numbers) is managed by the backend — the LLM only
  handles text content.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
agent_role: adapter
tools_required: []
triggers:
  - path: params.document_mode
    equals: true
---

# Adaptar document estructurat per segments

## Quan activar aquesta skill
Activa quan el text a adaptar prové d'un document estructurat (PDF o PPTX)
i s'envia com a llista de segments JSON. Cada segment és un bloc autònom
extret del document original: un títol, un paràgraf, un enunciat d'exercici,
una instrucció, una pregunta.

## Diferència respecte a l'adaptació de text continu
En l'adaptació estàndard, l'LLM rep un text complet i el reescriu com un tot.
En l'adaptació de documents, cada segment arriba independent i ha de tornar
independent. **El backend s'encarrega del layout** (columnes, taules,
espais per omplir, imatges): el LLM NO ha de reconstruir-lo.

## Instruccions crítiques

```
MODE DOCUMENT — REGLES ABSOLUTES:
- Adapta CADA segment de forma independent al perfil i nivell MECR indicats
- Retorna EXACTAMENT el mateix nombre de segments rebuts, amb els mateixos id
- NO afegeixis preguntes, seccions, complements ni text extra per compte propi
- NO fusiones segments ni parteixis un en dos
- Preserva la FUNCIÓ ESTRUCTURAL de cada segment:
    · Títol → segueix sent títol (més curt/simple, però títol)
    · Pregunta → segueix sent pregunta (mateixa estructura interrogativa)
    · Número d'exercici → preserva el número (1. / 2. / a) / b))
    · Instrucció → segueix sent instrucció (mantén el mode imperatiu)
    · Etiqueta curta (Nom:, Data:, Curs:) → adapta mínim o deixa igual
- Mantén un TO i REGISTRE consistents entre tots els segments del document
- Si un segment és massa curt per adaptar (< 4 paraules, nom propi, número
  sol), retorna'l sense canvis
```

## Mapa de tipus de segment → estratègia

| Tipus de segment | Estratègia d'adaptació |
|---|---|
| **Títol / encapçalament** | Simplifica vocabulari; no canviïs l'estructura nominal |
| **Paràgraf explicatiu** | Aplica totes les instruccions MECR/DUA/perfil actives |
| **Enunciat d'exercici** | Simplifica la pregunta; preserva el número i la forma interrogativa |
| **Instrucció d'activitat** | Simplifica; mantén l'imperatiu (Escriu, Ordena, Relaciona) |
| **Opció de resposta** (a/b/c) | Simplifica vocabulari; no canviïs l'ordre ni els marcadors |
| **Etiqueta de camp** (Nom:, Data:) | No adaptar — retorna igual |
| **Text de taula** | Adapta el contingut; preserva l'estructura paral·lela de les cel·les |
| **Peu de pàgina / referència** | No adaptar o adaptació mínima |

## Consistència entre segments
Quan adaptes, tens en compte que tots els segments pertanyen al mateix document:
- Si al segment 1 has usat "nutrients" per traduir "substàncies nutritives",
  usa "nutrients" en tots els segments següents on aparegui el concepte.
- El nivell de complexitat ha de ser uniforme: no simplifiquis molt un segment
  i poc el següent.
- El to (formal/informal, proper/distant) ha de ser el mateix a tot el document.

## Exemple

**Input (segment id=p0_b3):**
```
"Les plantes realitzen el procés de fotosíntesi absorbint la llum solar
 mitjançant la clorofil·la present als cloroplasts."
```

**Output esperat (perfil: nouvingut A2, DUA Core):**
```
"Les plantes fan fotosíntesi. Usen la llum del sol. La clorofil·la
 és la part verda de la fulla que capta la llum."
```

**Input (segment id=p0_b4, etiqueta curta):**
```
"Activitats:"
```

**Output esperat:**
```
"Activitats:"
```
(no s'adapta — és una etiqueta estructural de menys de 3 paraules)
