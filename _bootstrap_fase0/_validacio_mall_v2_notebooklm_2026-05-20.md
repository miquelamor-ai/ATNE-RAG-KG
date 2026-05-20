# Validació MALL crítica V2 (mostra) — informe 2026-05-20

**Mètode**: NotebookLM crític sobre 6 V2 representatius (notícia, assaig, poema, tolc, bastides, rubriques) com a mostra dels 34 V2.

**Cobertura**: 6/34 (17%) — mostra escollida per cobrir variats (gèneres expositiu/argumentatiu/literari + mediació plurilingüe/nuclear/avaluativa).

---

## VEREDICTE FINAL DE NotebookLM

### Ranking de fidelitat al MALL (els 3 formats)

| Lloc | Format | Justificació |
|---|---|---|
| 🥇 **1r** | **V2 descriptiu prosa** | Incorpora heurístiques docents + autoavaluació 1a persona + intenta plurilingüisme. Únic format que s'apropa a la ZDP. |
| 🥈 **2n** | **V3 rúbrica taula** | Sòlid en gradació MECR però rígid i cec a mediació. |
| 🥉 **3r** | **V1 productiu actual** | Regressiu, productivista, monolingüe. **Inapte** per a ATNE. |

### Recomanació clau

> *"L'arquitectura **V2+JSON** és la correcta, però el JSON ha de 'segrestar' la rigidesa del MECR que tenia la V3 per evitar que l'LLM ignori les restriccions de nivell en la seva resposta en prosa."*

→ **Valida la decisió de Fase 0 (V2+JSON com a productiu)** amb la condició que el JSON capturi la gradació explícita que V2 perd.

---

## Per què V2 > V3 per NotebookLM

- **V3 era una llista de control** (taula)
- **V2 ensenya a l'LLM a actuar com un mestre que "pensa en veu alta"** — això és modelatge MALL
- V2 té secció "Heurístiques docents" (H1, H2, H3...) que V3 va eliminar per estalvi de tokens
- V2 mantè l'autoavaluació 1a persona (igual que V3)

## Per què V2 perd respecte V3

- **Risc de dilució MECR**: en prosa, la gradació es difumina. L'LLM pot "barrejar" descriptors B1 en text A2
- **Pèrdua de visió de "contínuum"**: V2 sembla col·lecció d'estancs, V3 forçava veure com creix la complexitat de cada pas

→ **JSON resol això** capturant la gradació estructurada (passos × nivells) que V2 perd al prosa.

---

## Defectes sistèmics V2 (estat dels 6 de V3/V1)

1. **Plurilingüisme/TIL**: **PARCIALMENT RESOLT**. V2-tolc i V2-noticia/assaig marquen `translanguaging: true`. Però V2-poema i V2-rubriques marquen `false`. Incoherent.
2. **Fase Mediació / Text Model**: **PERSISTEIX**. Cap dels 6 V2 obliga a anàlisi prèvia del Text Model. Continua "del text del no res".
3. **Buit pre-A1**: **RESOLT EN GÈNERES**. V2-noticia i V2-poema inclouen pre-A1. **Persisteix a V2-assaig** (que el manté exclòs, antipedagògic).
4. **Errors HCL**: **PERSISTEIX**. V2-assaig encara activa Argumentar a A1 (MALL: només Interpretar/Valorar a A1).
5. **Simplificació vs Bastida**: **RESOLT PARCIALMENT**. Les heurístiques son bastides autèntiques. Però encara apareix "≤12 paraules/frase" com a simplificació mecànica.
6. **Oralitat**: **PERSISTEIX**. S'esmenta l'eix oral/escrit com a "connexió", però no s'integra com a conversa exploratòria obligatòria prèvia.

---

## Errors NOUS detectats a V2

- **V2-bastides Base d'orientació**: Bloc A és "procedimental", no "disciplinar". El MALL exigeix base d'orientació disciplinar (GPS de la matèria + gènere, no només del gènere).
- **V2-tolc falsa dualitat TOLC/PBCS**: V2 intenta separar-los com a "instruments integrats" quan el MALL els defineix com a estratègies que conflueixen en la **conceptualització translingüística**.

---

## 1 risc principal per instrument (6)

1. **V2-noticia**: piràmide invertida esdevingui regla sintàctica (curtedat) en lloc de regla informativa (rellevància)
2. **V2-assaig**: bloqueig cognitiu total demanant argumentació formal a A1 (mateix que V3 i V1)
3. **V2-poema**: metàfora concreta tan simple que perd la funció poètica
4. **V2-tolc**: reduït a taula traducció BICS, perd transferència CALP
5. **V2-bastides**: base d'orientació tan rígida que no es retira mai → alumnes dependents
6. **V2-rubriques**: descriptor AE interpretat com "fer-ho tot" en lloc de salt qualitatiu

---

## IMPLICACIÓ PER A LA DECISIÓ V2+JSON DE FASE 0

**NotebookLM VALIDA la decisió** amb 2 matisos crítics:

1. ✅ **V2 com a SKILL.md productiu**: confirmat com a millor format per fidelitat MALL
2. ⚠️ **JSON ha de capturar la gradació MECR explícita** que V2 perd al prosa — sense JSON, V2 sol té risc de dilució de nivells
3. 🔴 **Encara queden 2 defectes sistèmics SENSE RESOLDRE** que afecten V2 igual que V3 i V1:
   - **Text Model** absent (cap M*.md força anàlisi prèvia)
   - **Oralitat com a conversa exploratòria** invisible

→ Aquests 2 defectes son **estructurals al projecte ATNE**, no resolubles canviant de V1 a V2. Cal **decisió arquitectònica nova** per integrar-los abans del pilot real.

## FITXER DE PROVES

Resposta sencera dins de la conversa NotebookLM (conversation_id `3b48c074-155d-4bf2-83b9-7c80a6486bf2`). 6 sources usades (els 6 V2) + 7 sources MALL canòniques.
