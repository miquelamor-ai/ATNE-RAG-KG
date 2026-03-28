---
modul: M3
titol: "Gèneres discursius — Instruccions d'adaptació per gènere"
tipus: estrategia
descripcio: "Regles d'adaptació textual específiques per gènere discursiu (explicació, narració, instrucció, argumentació). Basades en la Lingüística Sistèmica Funcional de Halliday."
review_status: esborrany
generat_at: 2026-03-28T20:00:00
---

# Gèneres discursius — Adaptació textual per a l'LLM

## Context teòric

La Lingüística Sistèmica Funcional (LSF) de Halliday estableix que cada gènere discursiu té una estructura pròpia i unes convencions que afecten com s'ha d'adaptar el text. No es pot adaptar igual una narració que una explicació científica: les regles canvien.

FJE utilitza el terme **gèneres discursius** (no "textuals") perquè inclou gèneres orals, escrits i multimodals.

## Gèneres principals

### 1. Explicació

**Finalitat**: Fer entendre un fenomen, procés o concepte.

**Estructura canònica**: què és → com funciona → per què importa

**Instruccions per a l'LLM**:
```
GÈNERE DISCURSIU: Explicació
- Progressió del simple al complex
- Causa → efecte explícita (connector "perquè", "per tant")
- Desnominalitza processos ("l'oxidació" → "quan s'oxida")
- Estructura: què és → com funciona → per què importa
```

**Exemple adaptat (A2, ciències):**
> **Què és la fotosíntesi?**
> Les plantes fan el seu propi menjar. Usen la llum del sol.
> **Com funciona?**
> La planta agafa llum, aigua i diòxid de carboni. Per tant, fabrica glucosa.
> **Per què és important?**
> Sense fotosíntesi, no hi hauria oxigen. Les plantes ens donen l'aire que respirem.

### 2. Narració

**Finalitat**: Explicar fets o històries amb personatges, acció i desenllaç.

**Estructura canònica**: qui → què passa → per què → com acaba

**Instruccions per a l'LLM**:
```
GÈNERE DISCURSIU: Narració
- Mantén personatges principals, simplifica secundaris
- Explicita motivacions i emocions dels personatges
- Cronologia lineal (evitar flashbacks)
- Estructura: qui → què passa → per què → com acaba
```

**Exemple adaptat (A2, socials):**
> **Qui?** En Colom era un navegant.
> **Què va passar?** Va travessar l'oceà Atlàntic amb tres vaixells.
> **Per què?** Volia trobar un camí nou cap a l'Àsia per mar.
> **Com va acabar?** Va arribar a Amèrica el 1492. No sabia que era un continent nou.

### 3. Instrucció

**Finalitat**: Guiar l'execució d'una tasca, procés o procediment.

**Estructura canònica**: què necessites → passos → resultat esperat

**Instruccions per a l'LLM**:
```
GÈNERE DISCURSIU: Instrucció
- Numera els passos
- Un verb d'acció per pas, subjecte "tu" explícit
- Ordre cronològic estricte
- Estructura: què necessites → passos → resultat esperat
```

**Exemple adaptat (A2, ciències):**
> **Què necessites?** Un got, aigua, sal i una cullera.
> **Passos:**
> 1. Posa aigua al got.
> 2. Afegeix una cullerada de sal.
> 3. Remena amb la cullera fins que la sal desaparegui.
> **Resultat:** Has fet una dissolució. La sal s'ha dissolt a l'aigua.

### 4. Argumentació

**Finalitat**: Defensar una posició amb raons i evidències.

**Estructura canònica**: què defensa → arguments → conclusió

**Instruccions per a l'LLM**:
```
GÈNERE DISCURSIU: Argumentació
- Tesi al primer paràgraf
- Cada argument numerat amb evidència
- Conclusió explícita
- Estructura: què defensa → arguments → conclusió
```

**Exemple adaptat (B1, socials):**
> **Tesi:** El reciclatge és important per al medi ambient.
> **Argument 1:** El reciclatge redueix els residus als abocadors. Cada any, una persona genera 450 kg de brossa. Si reciclem, en guardem una part.
> **Argument 2:** Reciclar estalvia energia. Fer una llauna nova gasta 20 vegades més energia que reciclar-ne una de vella.
> **Conclusió:** Per tant, reciclar és una acció senzilla que ajuda a protegir el planeta.

## Detecció automàtica de gènere

El gènere es pot detectar per:
- **Paraules clau**: "per què" → explicació, "primer... després" → instrucció, "opino que" → argumentació
- **Estructura**: llistes numerades → instrucció, paràgrafs narratius → narració
- **Matèria**: ciències → explicació/instrucció, literatura → narració, ètica → argumentació

Aquesta detecció es pot implementar al codi Python per seleccionar automàticament el bloc de gènere adequat.
