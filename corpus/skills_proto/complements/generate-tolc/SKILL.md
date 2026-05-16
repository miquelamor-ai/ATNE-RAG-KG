---
name: generate-tolc
description: >
  Use when the teacher has activated the "tolc" complement. Generates a
  Transllenguatge/TOLC block: a bilingual anchor section that uses the student's
  L1 as a cognitive bridge to Catalan. Includes vocabulary comparison, structural
  parallel, and a transfer prompt. Also integrates PBCS (Pedagogically-Based Code
  Switching) cues when appropriate. Only meaningful when newcomer profile is active
  with a known L1. At Emergent/pre-A1: oral recast prompts only — no written production.
author: FJE — Fundació Jesuïtes Educació
version: 1.0.0-proto
complement_key: tolc
agent_role: complements
tools_required: []
triggers:
  - path: params.complements.tolc
    equals: true
  - path: params.nouvingut.actiu
    equals: true
---

# Generar Transllenguatge / TOLC

## Quan activar aquesta skill

Activar quan el docent ha marcat el complement **"Transllenguatge / TOLC"** al Pas 2.

**Condició necessària**: `nouvingut.actiu = true` i `nouvingut.L1` definida.
Si la L1 no és coneguda, generar només el bloc PBCS genèric (sense traducció).

Aplica principalment a:
- **Nouvingut L2** (perfil principal): usar el repertori lingüístic com a recurs
- **NESE (TDAH, dislèxia, TEA)**: ancorar el concepte en L1 allibera càrrega cognitiva
- **AACC**: tasques de mediació complexa, contrast metalingüístic

## Dos instruments que genera

### TOLC (Translation for Other Learning Contexts)
Usa la **traducció** com a eina pedagògica. No és un glossari: és una comparació activa que fa visible com les dues llengües codifiquen el mateix concepte.

### PBCS (Pedagogically-Based Code Switching)
**Alternança estratègica de codis** dissenyada: el docent (o el material) indica explícitament quan canviar de llengua i per a quina funció. No és espontani. Objectiu: fer visible la diferència entre sistemes lingüístics.

Diferència clau: TOLC **tradueix i compara**; PBCS **alterna per consciència metalingüística**.

## Estructura del bloc generat

El bloc TOLC conté tres moments:

**1. Activació** — ancorar el concepte clau en L1 (pregunta comparativa)
**2. Acarament** — requadre de contrast L1↔català (estructura visible)
**3. Transferència** — consigna de producció (oral o escrita, segons MECR)

## Gradació per nivell MALL

| Nivell | TOLC | PBCS | Producció |
|---|---|---|---|
| **Emergent (pre-A1)** | Oral: "Com es diu X en la teva llengua?" — **cap escriptura** | Recast del docent en veu alta | ❌ Zero escriptura autònoma |
| **Inicial (A1)** | Taula 2 columnes: paraula L1 / paraula català (3-5 termes) | Consigna oral + pictograma | Dictat a l'adult o assenyalar |
| **Funcional (A2)** | Taula + frase de contrast estructural (p.ex. ordre subjecte-verb) | Requadre destacat de contrast | Frase curta en L1 → traduir al català |
| **Estratègic (B1)** | Contrast de connectors i construccions causals | Mediació epistèmica: resumir en una llengua un text de l'altra | Paràgraf breu |
| **Acadèmic+ (B2/C1)** | Contrast de gèneres entre L1 i català | Contrasta intenció comunicativa entre llengues | Mediació complexa (text complet) |

## Format de sortida

### Format A1-A2 (escrit, L1 coneguda)

```markdown
## Connexió amb la teva llengua

**Activació** — Com es diu «[concepte clau]» en la teva llengua?

| En [L1] | En català |
|---|---|
| [paraula L1 en alfabet original] | **[paraula catalana]** |
| [paraula L1] | **[paraula catalana]** |
| [paraula L1] | **[paraula catalana]** |

**Fixa't**: [observació sobre semblances o diferències estructurals entre les dues llengües — màx. 1 frase senzilla]

**Ara tu**: [consigna de transferència concreta i accionable]
```

### Format B1+ (mediació epistèmica)

```markdown
## Connexió amb la teva llengua

**Activació**: «[concepte del text]» en [L1] s'expressa com ___.
En català usem la construcció «[construcció]». Fixa't en la diferència: [observació].

**Mediació**: [consigna: resumir en L1 una part del text, o traduir una conclusió]

**Transferència**: [consigna de producció en català usant el pont de L1]
```

### Format Emergent (pre-A1, oral)

```markdown
## Connexió amb la teva llengua

🗣️ **Pregunta per al docent** (oral, no cal escriure):
«Com es diu [paraula clau del text] en la teva llengua? Dibuixa o assenyala la imatge mentre ho dius.»
```

## Regles estrictes de sortida

- **Pre-A1**: ZERO escriptura autònoma. El bloc és una indicació per al docent (italic o [entre claudàtors]).
- Usa sempre l'**alfabet original** de la L1: àrab الكتاب, xinès 书, urdú کتاب, ciríl·lic книга, armeni գիրք.
- Si la L1 no té equivalència exacta: usar la més propera + "(semblant)" entre parèntesis.
- **NO** exposis l'alumne: la consigna és sempre voluntària ("si vols", "si pots").
- Màxim **3-5 parells** de paraules a la taula. No sobrecarregar.
- L'observació estructural ha de ser **positiva** (semblances primer, diferències com a curiositat).
- Comença **sempre** amb la línia `## Connexió amb la teva llengua`.
- **NO** generar aquest complement si `nouvingut.actiu = false` — retorna un missatge d'advertència al docent.

## Exemple (A2, àrab, Ciències — volcans)

```markdown
## Connexió amb la teva llengua

**Activació** — Com es diu «volcà» en àrab?

| En àrab | En català |
|---|---|
| بركان (burkān) | **volcà** |
| حمم (humam) | **magma** |
| ثوران (thawrān) | **erupció** |

**Fixa't**: tant en àrab com en català, el nom del volcà va davant del verb quan descrivim
una erupció. Les dues llengües organitzen la frase de manera semblant.

**Ara tu**: Escriu una frase en àrab sobre els volcans i després intenta traduir-la al
català usant els connectors que hem vist (*perquè*, *quan*, *llavors*).
```
