---
name: generar-resum-graduat
description: Instrument per generar una bastida de resum graduada per MECR. Distinció MALL recapitular (pre-A1/A1) vs. resumir (A2+). Marc parcialment complert amb forats calibrats al nivell. No és una tasca oberta. Correccions MALL 2026-05-17 aplicades.
type: instrument
categoria_principal: mediacio
categories_secundaries: []
mecr_range: [pre-A1, A1, A2, B1, B2, C1]
agent_roles: [adapter, generator]
translanguaging: false
multimodal: true
skill_meta: generate-resum-graduat@corpusFJE/skills/mediacio/generate-resum-graduat
version: 2.0.0-bootstrap
---

# Generar resum graduat — V2 Descriptiu

## Descripció

El resum graduat és una **bastida cognitiva**, no una tasca oberta. No es demana a l'alumne "fes un resum" — se li dona una estructura parcialment complerta que li permet construir el resum pas a pas.

**Tipologia MALL**: Mediació cognitiva (comprensió + producció)
**HCL principal**: Resumir — condensar la informació essencial en un text coherent propi
**Distinció fonamental MALL**: **recapitular** (pas previ, oral/visual: ordenar i seleccionar sense produir text autònom) vs. **resumir** (producció escrita coherent). A pre-A1 i A1, s'entrena el recapitular. El resumir escrit és la fita final d'un procés progressiu.
**Principi rector**: la gradació no és de complexitat del text, sinó de la **mida del forat** — a nivells baixos el marc és molt donat; a nivells alts, és mínim i l'alumne construeix lliurement.

## Estructura canònica

La bastida de resum té **3 variants** segons el nivell:

1. **Recapitular** (pre-A1/A1): ordenar imatges, dictat a l'adult, respondre qui/on/quan.
2. **Marc amb forats** (A2-B1): frases marc parcialment completes, forats completables en 1-3 paraules.
3. **Criteris de qualitat** (B2-C1): llista de criteris que l'alumne aplica per produir lliurement.

## Modulació per nivell MECR

### Pre-A1 — Emergent

**Cap escriptura autònoma.** El "resum" és una activitat oral i visual: ordenar seqüències d'imatges, respondre "De qui parla?" i "Qué fa?", dictat a l'adult que transcriu. Objectiu: demostrar comprensió global sense produir text.

### A1 — Inicial

Frase marc amb 1-2 forats i opcions tancades. L'alumne tria la paraula correcta d'una llista de 2-3 opcions. Les opcions han de tenir una resposta clarament correcta i distractors plausibles. Frases molt simples (màxim 10 paraules). El marc reflecteix l'estructura del text: narratiu (personatge/acció/desenllaç) o informatiu (tema/dada principal).

### A2 — Funcional

Marc de 2-3 frases amb 3-4 forats clau. L'alumne omple els forats sense opcions (resposta oberta però curta: 1-3 paraules). Per a text narratiu: personatge / acció / desenllaç. Per a text informatiu: tema / punts clau / conclusió. No cal copiar frases literals del text.

### B1 — Estratègic

Marc de 3 blocs (Tema / Punts clau / Conclusió) amb espais oberts. L'alumne omple amb paraules pròpies, no copia el text. Pot usar lèxic de la matèria. 3-4 frases pròpies en total. L'estructura fa visible la jerarquia informativa del text.

### B2 — Acadèmic

Criteris de qualitat del resum (3-5 ítems en format checklist). L'alumne produeix el resum complet i s'autoavalua contra els criteris. Els criteris han de ser específics del text (no genèrics): "Has identificat la causa principal de [fet concret]?". El resum ha de poder-se entendre sense llegir el text original.

### C1 — Crític

Rúbrica de metacognició: l'alumne produeix el resum i reflexiona sobre les tries que ha fet (per qué ha seleccionat unes idees i n'ha descartat d'altres). Pot incloure comparació amb un resum model o d'un company per detectar diferències de criteri.

## Regles crítiques

**FER:**
- Comença sempre amb `## Resum`.
- El marc ha de reflectir l'estructura del **text concret**, no un marc genèric.
- Pre-A1: proposta oral, adult transcriu.
- A1-A2: forats completables en 1-3 paraules màxim.
- A1: opcions tancades amb una resposta clarament correcta.
- B2+: criteris específics del text, no genèrics.

**NO FER:**
- ❌ "Fes un resum del text" com a única instrucció (tasca oberta sense bastida, fins a B2).
- ❌ Generar un resum model: l'alumne ha de construir el seu.
- ❌ Forats de frases senceres a A1-A2 (la mida del forat és clau).
- ❌ Marc genèric ("introducció, desenvolupament, conclusió") sense infusió del text real.

## Connexions MALL

- **Recapitular vs. resumir**: distinció MALL fonamental. El resum graduat evita el salt directe a producció escrita que fracassa a nivells baixos.
- **Textos amb llacunes (cloze)**: eina validada per MALL per a A1-A2. L'alumne processa activament sense la càrrega de producció complerta.
- **Multimodalitat**: a pre-A1, les imatges substitueixen el text escrit. A A1, suport visual opcional als forats per a termes concrets.

## Detecció

**Senyals docent** (quan activar resum graduat):
- Cal demostrar comprensió global del text (no detalls puntuals — per a detalls, usar preguntes de comprensió).
- L'alumnat confon idea principal amb detalls: copia frases literals en lloc de resumir.
- La unitat requereix un resum com a activitat de síntesi final.
- Text TILC llarg (>200 paraules) on cal guiar la identificació del nucli informatiu.

**Senyals alumne** (que indica que necessita bastida):
- Escriu el resum copiant frases literals del text, sense reformular.
- El "resum" té la mateixa llargada que el text original.
- Inclou tots els detalls sense jerarquitzar: no distingueix idea central de exemples.
- Quan li preguntes "Qué és el més important?", respon "Tot".
- Nouvingut A1-A2: pot rellegir el text però no pot dir de qué tracta amb paraules pròpies.

**Context favorable**:
- Matèria TILC on la comprensió global és prerequisit per a activitats posteriors.
- Text literari on cal identificar el tema i el missatge (no la trama detallada).
- Alumnat que va bé en lectura literal però falla en la síntesi i la jerarquització.

**Anti-senyals** (quan NO activar):
- Text molt curt (<100 paraules): la comprensió és immediata, millor discussió oral.
- L'objectiu és comprensió detallada → preguntes de comprensió lectora.
- Temps limitat: millor un resum oral col·lectiu guiat pel docent.

## Heurístiques docent

**H1 — La prova de la jerarquia**
Demano a l'alumne: "Si haguessis de dir a un company de qué tracta el text en 1 frase, qué diries?" Si respon amb un detall ("Un nen que perd el gat"), li dic: "Molt bé, però qué aprèn sobre [tema del text]?" Aquesta escala de dos preguntes, de detall a abstracció, és la bastida mínima de qualsevol resum.

**H2 — El resum que es llegeix sol**
Llegeixo el resum de l'alumne sense el text original i li pregunto: "Podria entendre de qué tracta el text llegint només el teu resum?" Si la resposta és "no", el criteri de qualitat és clar: el resum ha de ser autosuficient. A B2+, l'alumne es fa aquesta pregunta ell sol (checklist).

**H3 — El mapa del forat**
Per decidir on posar els forats a A1-A2, llegeixo el text i marco les 3-4 paraules o sintagmes més importants: aquelles que no podria substituir per "cosa" sense perdre el sentit. Aquelles paraules van als forats. Funciona especialment bé amb textos informatius on el vocabulari curricular és el nucli.

**H4 — Recapitular primer, resumir després**
Per a grups on el resum falla, introdueixo primer el recapitular oral: "Qui / Qué / On / Quan / Com". Un cop l'alumne pot respondre aquestes preguntes de memòria, la bastida escrita (marc amb forats) és molt menys intimidant perquè ja sap el contingut.

**H5 — El resum col·laboratiu com a diagnòstic**
Proposo que 3 alumnes es posin d'acord en un sol resum de 3 frases. La negociació verbal entre ells em dona informació diagnòstica: si discuteixen sobre un detall que tots pensen que és central, el text és massa complex per al nivell o necessita preguntes prèvies de comprensió.

## Autoavaluació (descriptors en primera persona)

- *Pre-A1*: "He dit de qui parla el text i qué fa." (oral)
- *A1*: "He triat la paraula correcta per completar el resum."
- *A2*: "He omplert els forats del resum amb les idees principals."
- *B1*: "He escrit el tema, els punts clau i la conclusió amb paraules meves."
- *B2*: "He escrit un resum que es pot entendre sense llegir el text original."
- *C1*: "He escrit el resum i he explicat per qué he triat unes idees i n'he deixat d'altres."

## Fonts principals

- MALL (Model d'Aprenentatge de Llengües i Literacitat): distinció recapitular/resumir, marc graduat.
- Solé (1992): estratègies de comprensió lectora — identificació d'idees principals.
- Cummins (2000): CALP — el resum com a activitat de llengua acadèmica.
- Kintsch & van Dijk (1978): macroestructura textual — jerarquia d'informació.
- Decret 175/2022 (currículum Catalunya): competència lectora i expressió escrita.
