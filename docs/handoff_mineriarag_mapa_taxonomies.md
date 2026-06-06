# HANDOFF mineriaRAG — Mapa de taxonomies ATNE (transformacions + complements → marcs teòrics)

**Data:** 2026-06-06
**De:** ATNE (Miquel Amor)
**Per a:** mineriaRAG
**Regla aplicada:** ATNE = CONSUMIDOR del canon, mai ORIGEN. Aquest mapeig és
coneixement IMPLÍCIT reconstruït a ATNE. Es lliura a mineriaRAG perquè el
**canonitzi als M*.md** del corpusFJE. ATNE NO escriu aquest coneixement al
corpus directament; un cop canonitzat + derivat a JSON, ATNE el consumirà.

---

## 1. Què és aquest handoff

Durant una sessió d'aclariment conceptual amb Miquel s'ha reconstruït un **mapa
de relacions** entre les taxonomies pedagògiques d'ATNE i els seus orígens
teòrics. El mapa NO existeix de forma explícita i consolidada a cap M*.md: està
implícit i dispers en cites de M1/M2/M3. Es demana a mineriaRAG que decideixi si
val la pena canonitzar-lo i, si és el cas, on (quin M*.md) i amb quina forma.

**Validació prèvia:** tot el mapeig s'ha validat amb NotebookLM (notebook MALL,
28 fonts, sessió 2026-06-06). Veredicte: "pedagògicament sòlid" / "excel·lent".
Les 6 correccions de NotebookLM JA estan incorporades a les taules d'aquest doc.

---

## 2. L'estructura conceptual (3 taxonomies)

Quan ATNE adapta un text fa DUES coses:
1. **TRANSFORMA el text** (el reescriu) → "transformacions" (3 tipus)
2. **AFEGEIX materials al voltant** → "complements" = instruments de mediació (MALL)

I després, **"Per al docent"** (9 categories A-I) explica les dues coses al docent.

Relació jeràrquica:
- Inclusió neta ÚNICA: **Instruments de mediació ⊃ Bastides**.
- Les 3 taxonomies NO es contenen entre elles: es **creuen** (una mateixa eina
  viu a les tres amb un rol diferent — ex. glossari = Suport DUA + bastida lèxica
  + categoria docent A).

---

## 3. TAULA A — Transformacions del text → marcs teòrics (VALIDADA)

| Transformació | Marc dominant | Marcs que aporten | Notes de validació NotebookLM |
|---|---|---|---|
| Lingüístiques (lèxic/sintaxi/cohesió/registre) | Cummins (BICS/CALP) | MECR, Lectura Fàcil (UNE 153101)*, plain language, Halliday (LSF) | UNE no citada nominalment al MALL; concepte present |
| Estructurals (segmentació/jerarquia/ordre/senyalització) | DUA-1 (Representació) + Sweller* | Vygotsky ZDP, gèneres (Bajtín + J.M. Adam), Camps/Zayas | **Gèneres = Bajtín/Adam, NO Gibbons** (correcció). Sweller no citat nominalment |
| Contingut curricular (terminologia/rigor/exemples/context) | "doble eix" MALL/Cummins | TILC/CLIL, DUA-3 (Implicació), translanguaging, 5 HCL (Jorba/Sanmartí) | "adaptar el COM sense rebaixar el QUÈ" |

**Confirmat per NotebookLM (no tocar):**
- Cummins (BICS/CALP) = fil transversal de les 3 transformacions.
- MALL = paraigua integrador ("síntesi integradora de marcs consolidats"), no marc paral·lel.

**MARC ABSENT detectat per NotebookLM (decisió pedagògica per a mineriaRAG):**
- 🔴 **Pilar de l'ORALITAT.** El MALL considera l'oralitat el fonament de tot
  aprenentatge lingüístic. Possible 4a transformació: **text → guió oral**
  (lectura mediada) per a pre-A1/A1. ATNE NO ho implementa. ¿Canonitzar com a
  transformació futura?

---

## 4. TAULA B — Complements (instruments de mediació) → categoria MALL + teòric (VALIDADA)

| Complement | Categoria MALL | Teòric pare | Estat ATNE | Validació NotebookLM |
|---|---|---|---|---|
| Glossari | Suport DUA | Cummins (CALP) + Ausubel* | ✅ | correcte (Ausubel no citat nominalment) |
| Pictogrames | Suport DUA | DUA-1 + Sweller* | ✅ | molt coherent |
| Il·lustracions | Suport DUA | DUA-1 + Mayer* | ✅ beta | molt coherent |
| TOLC/Transllenguatge | Suport DUA | Cummins + González-Davies + Corcoll | 🔲 parcial | **exacta** |
| Bastides lingüístiques | Bastida | Vygotsky/Bruner + Jorba/Gómez/Prat | ✅ | **exacta** |
| Esquema visual | Bastida cognitiva | Sweller* + Mayer* | ✅ | coherent |
| Mapa conceptual | Bastida cognitiva | Novak* (extern) | ✅ | ⚠️ MALL NO anomena Novak |
| Mapa mental | Bastida cognitiva | Buzan* (extern) | ✅ | ⚠️ MALL NO anomena Buzan |
| Preguntes comprensió | Bastida metacognitiva | **Isabel Solé** + Sanmartí | ✅ | ⚠️ faltava Solé (referent lectura 3 moments) |
| Pauta d'interrogació | Autoregulació | Sanmartí | ✅ | **confirmat** |
| Rúbriques | Autoregulació | Sanmartí + Black & Wiliam + DUA-3 | 🔲 | coherent |
| Activitats aprofundiment | Extensió curricular | Bloom + Vygotsky | ✅ | coherent |
| Plantilles de gènere | Bastida discursiva | Bajtín + J.M. Adam + TILC | 🔲 | gèneres = Bajtín/Adam |
| Resum graduat | Bastida cognitiva | Sweller* (complexitat progressiva) | 🔲 | — |
| Cartes conversacionals | Bastida de producció | MALL + Vygotsky | 🔲 | — |

\* No citats nominalment al corpus MALL (Sweller, Ausubel, Mayer, Novak, Buzan):
concepte present, autor no. Atribucions externes legítimes però marcades.

**Confirmat per NotebookLM:**
- Les 6 categories MALL ben classificades (cap complement mal posat).
- Regla "menys és més" sòlidament fonamentada (Sweller + Vygotsky). Font MALL
  literal: "6-10 preguntes totals. Mai més." Matriu proposa 2-3 complements/condició.

---

## 5. Incoherència interna del corpus a resoldre (per a mineriaRAG)

**M2_instruments-mediacio-pedagogica.md té DUES representacions de les bastides:**
- Arbre (línies 44-50): **3 famílies** (lingüístiques / cognitives / metacognitives).
- Catàleg (línies 423-499): **7-8 famílies** (lèxiques / sintàctiques / discursives /
  visuals-multimodals / cognitives / metacognitives-lectura / producció / procedimentals).

¿Quina és la canònica? Proposta ATNE: arbre = nivell estructural (3 mares amb
subtipus), catàleg = desplegament operatiu. Caldria fer-ho explícit al M2 perquè
no generi confusió.

---

## 6. Teòrics que el MALL SÍ cita i NO estaven al mapeig inicial (afegir)

NotebookLM recomana integrar aquests autors que el corpus MALL cita explícitament:
- **M.A.K. Halliday** — Lingüística Sistèmica Funcional (text com a unitat semàntica).
- **Anna Camps / Felipe Zayas** — Seqüència Didàctica + activitat metalingüística.
- **Mikhail Bajtín** — Gèneres discursius (esferes d'activitat social).
- **J.M. Adam** — Seqüències textuals.
- **Isabel Solé** — Estratègies de comprensió lectora (3 moments).

---

## 7. Demanda concreta a mineriaRAG

1. ¿Val la pena canonitzar aquest mapa (transformacions + complements → teòrics)
   a un M*.md? Si sí, ¿a quin? (candidats: M2_instruments, un M0/M3 nou de
   "marc teòric integrat").
2. Decidir sobre el **pilar de l'oralitat** com a transformació futura.
3. Resoldre la **incoherència 3 vs 7-8 famílies** de bastides al M2.
4. Confirmar la incorporació dels 5 teòrics absents (§6).
5. Un cop canonitzat + derivat a JSON, ATNE el consumirà (p.ex. perquè el "Per al
   docent" pugui citar l'origen teòric de cada decisió).

**Artefactes adjunts (a ATNE/docs/):**
- `mapa_taxonomies.md` — explicació conceptual completa.
- `mapa_taxonomies_visual.md` — 7 diagrames Mermaid + taules validades.
- `mapa_diagrama_1..7.png` — diagrames renderitzats.
