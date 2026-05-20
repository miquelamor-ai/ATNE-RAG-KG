# Validació MALL crítica V1 (productiu corpusFJE) — informe consolidat 2026-05-20

**Mètode**: NotebookLM "Model d'Aprenentatge de Llengües: Principis i Pràctica" (38 fonts MALL canòniques) com a crític rigorós. Prompt: identificar errors, simplificacions, principis absents.

**Cobertura**: 35/35 SKILL.md V1 productius analitzats en 3 rondes (12+12+11).

---

## ⚠️ VEREDICTE GLOBAL DE NotebookLM

**V1 NO és apta per a una producció que pretengui ser fidel al MALL FJE.** Es recomana **substitució urgent**.

> *"La versió V1 és un model d'execució productivista que genera textos i bastides en el buit, ignorant el cicle 'del text al text', l'eix plurilingüe transversal i el paper mediador imprescindible del docent."*

V1 < V3 pedagògicament (per què: V1 no té autoavaluació en gèneres, V3 sí).

---

## 1. DEFECTES SISTÈMICS V1 (els mateixos 6 que V3, + 1 extra)

### D1 — Plurilingüisme/TIL residual o absent
Mateix que V3. El TIL només apareix com "variant" a TOLC i com a "opcional" a activitats-aprofundiment. El MALL el vol eix vertebrador transversal.

### D2 — Fase de Mediació / Text Model absent
**Confirmat**: cap SKILL V1 força el cicle "del text al text". Les bastides es generen en el buit, sense anàlisi del Text Model previ. Crític a bastides-produccio.

### D3 — "No s'aplica pre-A1" antipedagògic
Tot i que bastides-lectura V1 i activitats-aprofundiment V1 incorporen el pre-A1 amb dictat a l'adult i accions físiques, **els 10 gèneres de producció V1 ignoren aquesta etapa**.

### D4 — Oralitat com a motor INVISIBLE
**Greu**: cap SKILL V1 té rastre de "parlar per escriure" / conversa exploratòria prèvia a la textualització.

### D5 — Simplificació en lloc de bastida
Confirmat: V1 escurça paraules ("≤10-12 per lead", "4-6 passos", etc.) en lloc d'oferir bastides lingüístiques.

### D6 — BICS/CALP confosos
write-resum V1: "reformular amb vocabulari accessible" pot fomentar BICS i impedir CALP. write-informe i write-manual: "evitar tecnicismes" antipedagògic — el lèxic acadèmic s'aprèn amb el concepte (Lemke 1993).

### D7 — AUTOAVALUACIÓ EN PRIMERA PERSONA ABSENT als gèneres
**Defecte EXCLUSIU de V1** (V3 sí ho té sistemàticament):
- V1 NO inclou cap pas d'autoavaluació en cap dels 22 SKILL.md de gèneres
- V1 NOMÉS la inclou a `generate-rubriques` i `generate-bastides-produccio` (Bloc C)
- És el major punt feble de V1 davant V3

---

## 2. ERRORS PUNTUALS GREUS V1

### Gèneres
- **write-assaig**: HCL Argumentar a A1 contradiu MALL (B2-C1) — **mateix error que V3**
- **write-opinio**: argumentar a A1-A2 — només cal "interpretar/valorar" a A1
- **write-reglament**: prioritza "veu imperativa" sobre HCL Justificar — "model dependent-tradicional"
- **write-informe**: omet hipòtesi/discussió a A1-A2 ("mutilar el gènere" — cal mantenir patró temàtic i posar bastides)
- **write-manual**: "evitar tecnicismes" antipedagògic
- **write-diari**: barreja en un sac diari personal (reflexiu) + diari laboratori (justificatiu) — HCL radicalment diferents
- **write-fabula**: no grada la complexitat de la moral (literalitat → interpretació profunda)
- **write-ressenya**: demanar "recomanació concreta" a A1 prematur
- **write-divulgatiu**: títol "captador" pot induir error sobre objectivitat científica

### Mediació
- **generate-tolc V1**: **MILLOR/PITJOR que V3?** → PITJOR. Reduït a "taula de traducció bilingüe". Ignora dimensió intercultural i conceptualització translingüística
- **generate-cartes-conversacionals V1**: exclou pre-A1/A1 (mateix error que V3)
- **generate-resum-graduat V1**: "tirania del buit" — gradació basada només en mida del forat, no en macroregles
- **generate-pictogrames V1**: risc "alfabet logogràfic perpetu" que retardi la descodificació fonològica
- **generate-mapa-conceptual V1**: "mapa de contrast" reservat a C1 — massa conservador (pot començar B1/B2)

---

## 3. ✅ ÚNIC SKILL V1 FIDEL AL MALL

**generate-bastides-lectura V1** és **l'únic** SKILL canònicament fidel:
- Respecta els 3 moments (Abans/Durant/Després) i els 3 plànols (Literal/Inferencial/Crític)
- És l'únic que integra el Pre-A1 de forma funcional
- **Però** comparteix el buit de la "mediació dialogada": dissenyat com a lliurable unidireccional, no com a guió per a conversa literària/metacognitiva del docent

---

## 4. ✅ Punts on V1 = V3 (fidels al MALL)

- **generate-glossari V1**: sí integra L1 per a nouvinguts (variant bilingüe). Limitació: gradació CALP insuficient a nivells alts
- **generate-preguntes-comprensio V1**: cobreix bé els 3 plànols i 3 moments
- **generate-bastides-produccio V1**: Bloc C amb autoavaluació en 1a persona — canònic
- **generate-rubriques V1**: 1a persona + escala FJE (amb matís: AE com a salt qualitatiu, no quantitatiu)

---

## 5. COMPARATIVA V1 vs V3

| Dimensió | V1 (productiu) | V3 (esborrany) |
|---|---|---|
| Autoavaluació 1a persona | ❌ als gèneres (sí a rubriques + bastides-produccio Bloc C) | ✅ a tots (35/35) |
| TIL plurilingüisme | Variant/opcional | `translanguaging: false` a frontmatter |
| Mediació / Text Model | Absent | Absent |
| Pre-A1 | Incorporat a bastides-lectura, mediació, però gèneres no | Marcat "no s'aplica" a molts |
| Bastides-lectura | ✅ Únic SKILL fidel MALL | També bo (V3 hereta el patró) |
| TOLC | **Pitjor** (taula traducció) | Pitjor també, però amb els 3 moments |
| Cartes-conversacionals | Exclou pre-A1/A1 | Exclou pre-A1/A1 |
| Rúbriques | Canònic 1a persona | Canònic 1a persona |
| Gradació MECR explícita | Implícita al text | Explícita en taula 6 nivells |
| Riscos | "Model escolaritzat tradicional" | "Llista de control de producte" |

**Resultat global**: V3 lleugerament MILLOR que V1 (per autoavaluació + gradació explícita + intent d'introduir mediació amb plantilles/bastides). Però **ambdós tenen els mateixos 6 defectes sistèmics estructurals** del marc conceptual ATNE des de l'origen.

---

## 6. IMPLICACIONS PER A LA DECISIÓ V2+JSON DE FASE 0

La conclusió de Fase 0 era "V1≈V2≈V3 (empat tècnic) → V2+JSON com a SKILL productiu". 

**NotebookLM critic contradiu això**: V3 és pedagògicament millor que V1 (autoavaluació + gradació explícita). Però ambdós tenen els mateixos defectes sistèmics. **El problema no és el format (V1 vs V2 vs V3), és el contingut conceptual del marc ATNE**.

**Recomanació NotebookLM**: substitució urgent de V1, no només migració de format.

---

## 7. FITXERS DE PROVES (3 rondes V1)

- Ronda 1 (12 V1 gèneres A-F): `mcp-notebooklm-notebook_query-1779253103969.txt`
- Ronda 2 (12 V1 gèneres E-R + 2 mediació): `mcp-notebooklm-notebook_query-1779253347310.txt`
- Ronda 3 (11 V1 mediació): `mcp-notebooklm-notebook_query-1779253777555.txt`

Total: 3 queries, 72 sources_used acumulat, 181 citations al corpus MALL.
