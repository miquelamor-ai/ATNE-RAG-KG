# M3 · Transliteració — estàndards canon per L1 (proposta ATNE per a corpusFJE)

> **Mòdul**: M3 — Llengua · **Marc rector**: MALL + TIL + reconeixement simbòlic Cummins
> **Estat**: PROPOSTA ATNE 2026-05-31 — pendent ingesta canònica per mineriaRAG al corpusFJE
> **Origen**: document esborrany `mineriaRAG/docs/transliteracio_standards_l1_2026-05-31.md` + cross-check ignasià NotebookLM (notebook "L'aula d'acollida a l'aula ordinària", perfil `fje`) + actes d'acollida FJE 26.02.2025
> **Versió**: 0.9 (esborrany per a ingesta canon)

---

## 1. Per què cal una taula canon de transliteració

La transliteració del terme de l'L1 a alfabet llatí és un instrument de **mediació pedagògica** que serveix simultàniament a tres agents:

1. **El docent català**: pot llegir i pronunciar el terme aproximadament, fent de model de llengua per a l'alumne.
2. **L'alumne**: ancora la pronunciació amb el seu sistema fonològic d'origen.
3. **La família**: reconeix el terme escrit en una forma que ja usa al dia a dia.

El **reconeixement simbòlic de la L1** al material escolar és canon FJE (Cummins 2002, MALL, TILC) i fonamenta la inclusió de la transliteració com a columna del glossari quan la L1 té alfabet no llatí.

---

## 2. Principi de selecció dels estàndards

Tres criteris, en aquest ordre de prioritat:

1. **Llegibilitat per a un docent català sense entrenament** — minimitzar diacrítics complicats (ḥ, ʿ, ṣ, ž, etc.).
2. **Reconeixement per part de l'alumne i la família** — preferir estàndards que els parlants ja utilitzen al dia a dia (Pinyin per al xinès, Roman Urdu informal per a l'urdú, Hepburn per al japonès).
3. **Compatibilitat amb el motor LLM** — preferir estàndards molt presents als corpus d'entrenament (ALA-LC, Pinyin, Hepburn, BGN/PCGN) perquè el motor els reprodueixi de forma fiable.

S'eviten estàndards estrictament acadèmics amb molts diacrítics (DIN 31635 àrab, McCune-Reischauer coreà, ALA-LC complet amb tots els signes): el docent català no els pot llegir i el motor no els reprodueix consistentment.

---

## 3. Taula canon d'estàndards per L1

| L1 | Codi ISO | Alfabet original | Estàndard adoptat | Exemple |
|---|---|---|---|---|
| Àrab (modern estàndard + dialectes magribí i llevantí) | `ar` | Àrab | **ALA-LC simplificat** (sense diacrítics) | كتاب → `kitab` |
| Xinès mandarí | `zh` | Han | **Pinyin amb tons** | 学校 → `xuéxiào` |
| Urdú | `ur` | Nasta'liq (variant àrab) | **Roman Urdu** (transliteració fonètica que els parlants ja usen) | کتاب → `kitaab` |
| Pendjabi | `pa` | Gurmukhi | **ALA-LC simplificat** | ਕਿਤਾਬ → `kitab` |
| Hindi | `hi` | Devanagari | **ALA-LC simplificat** | किताब → `kitab` |
| Bengalí | `bn` | Bengali | **ALA-LC simplificat** | বই → `boi` |
| Rus | `ru` | Ciríl·lic | **BGN/PCGN** (sense diacrítics) | школа → `shkola` |
| Ucraïnès | `uk` | Ciríl·lic | **BGN/PCGN 2019** | школа → `shkola` |
| Búlgar | `bg` | Ciríl·lic | **BGN/PCGN** | книга → `kniga` |
| Japonès | `ja` | Kanji + Hiragana + Katakana | **Hepburn** | 学校 → `gakkō` |
| Coreà | `ko` | Hangul | **Revised Romanization (RR, 2000)** | 학교 → `hakgyo` |
| Hebreu | `he` | Hebreu | **Fonètica simplificada** | ספר → `sefer` |
| Tai | `th` | Tai | **RTGS** (Royal Thai General System) | หนังสือ → `nangsue` |
| Amhàric | `am` | Ge'ez | **BGN/PCGN** | መጽሐፍ → `mäṣḥaf` |
| Armeni | `hy` | Armeni | **ALA-LC** | գիրք → `girk'` |
| Georgià | `ka` | Mkhedruli | **National 2002** | წიგნი → `ts'igni` |

### 3.1. L1s amb alfabet llatí (no necessiten translit)

Romanès (`ro`), holandès (`nl`), polonès (`pl`), portuguès (`pt`), francès (`fr`), italià (`it`), wòlof (`wo`), fulani (`ff`), mandinga (`mnk`), soninké (`snk`), albanès (`sq`), vietnamita (`vi`), etc. **La columna translit del glossari NO s'activa per a aquestes L1s** — el reconeixement simbòlic de la L1 es manté via la columna L1 sola.

### 3.2. GAPS de cobertura confirmats (cross-check NotebookLM ignasià)

Les actes d'acollida FJE 26.02.2025 (centres Poble Sec, Sagrat Cor-Vic, Casp, Educar-me Primària) confirmen L1s rellevants als FJE que **cal afegir a la taula canon**:

- **Amazic / Tamazight** (`zgh`) — alfabet variable: Tifinagh requereix translit (estàndard a definir); variant pan-amaziga és alfabet llatí (no translit). Pedagogicament és **error tractar les famílies marroquines com a parlants d'àrab estàndard** — moltes tenen Tamazight com a L1.
- **Mandinga** (`mnk`) — alfabet llatí, no translit. Cal entrada com a L1 reconeguda al perfil per al reconeixement simbòlic.
- **Fula / Fulani** (`ff`) — alfabet llatí, no translit. Idem.
- **Soninké / Sarahule** (`snk`) — alfabet llatí, no translit. Idem.
- **Persa / Farsi** (`fa`) — alfabet àrab modificat. Estàndard pendent (probable ALA-LC simplificat per coherència amb àrab).
- **Darija marroquí** — NO entrada separada; **variant** dialectal d'àrab (`ar-MA`). La translit segueix l'estàndard àrab.

### 3.3. Política open-list

Si arriba alumne amb L1 NO present a la taula:
- ATNE marca el cas com `unknown_L1`.
- El motor transliteri amb el **sistema "més proper"** per a la família lingüística més pròxima.
- Cada entrada es marca `verified:false` amb **prioritat alta** per a revisió docent.
- mineriaRAG **afegeix la L1 a la taula canon** quan se'n detecten **≥3 casos reals** a la BD ATNE.

Aquesta política garanteix que la taula creix per **evidència real**, no per teoria, i no bloqueja l'atenció a alumnes amb L1 rares.

---

## 4. Argumentació pedagògica per cada decisió (cross-check ignasià-FJE)

### 4.1. Àrab → ALA-LC simplificat (no Arabizi)

**Decisió**: ALA-LC simplificat sense diacrítics. **Alternativa descartada**: Arabizi (alfabet de xat amb números: `3` per ʿayn, `7` per ḥ, etc.).

**Raonament**: l'objectiu canon és que el docent català pugui fer de **model de llengua** i establir un **vincle afectiu** pronunciant correctament el nom o paraules de l'alumne (cura personalis ignasiana). Arabizi seria críptic per al docent; ALA-LC simplificat manté caràcter acadèmic adequat per al context escolar i el motor el reprodueix consistentment.

### 4.2. Xinès mandarí → Pinyin AMB tons (no sense)

**Decisió**: `xuéxiào` (amb tons), no `xuexiao`.

**Raonament**: les famílies xineses sovint fan anar els fills a **escoles de xinès els dissabtes** (5 hores, confirmat a actes FJE). Els tons són **essencials** per al significat — sense tons el glossari pot induir errors de pronunciació que invalidarien el reconeixement simbòlic de la L1. El docent català no ha de pronunciar els tons, només **reconèixer el terme**. Cura personalis = no desvirtuar la realitat lingüística de l'alumne.

### 4.3. Urdú → Roman Urdu informal (no ALA-LC acadèmic)

**Decisió**: `kitaab` (Roman Urdu de WhatsApp/SMS), no `kitāb` (ALA-LC).

**Raonament**: única decisió on triem informal sobre acadèmic. La **relació amb la família** és central al Pla d'Acollida FJE. Les famílies pakistaneses usen Roman Urdu en SMS, WhatsApp i xarxes socials — és **pont real de comunicació**, no estàndard acadèmic aliè. Prioritzar funcionalitat comunicativa sobre estàndard acadèmic redueix barreres de participació de les famílies (criteri FJE).

### 4.4. Hebreu → fonètica simplificada (no Academy of the Hebrew Language)

**Decisió**: fonètica simplificada `sefer`, no estàndard de l'Academy amb diacrítics.

**Raonament**: l'**oralitat** és prioritat al Pla d'Acollida; el docent ha de poder llegir el terme amb fluïdesa. Diacrítics acadèmics dificulten la lectura. Hebreu té poc volum a FJE → pragmatisme primer.

---

## 5. Format al rubrica.json del glossari

```json
"transliteracio": {
  "tipus_excepcio": "no_derivable_del_M3",
  "verified_default": false,
  "estandards_per_L1": {
    "ar": { "nom_estandard": "ALA-LC simplificat", "exemple": "كتاب → kitab", "diacritics": false },
    "zh": { "nom_estandard": "Pinyin amb tons", "exemple": "学校 → xuéxiào", "diacritics": true },
    "ur": { "nom_estandard": "Roman Urdu", "exemple": "کتاب → kitaab", "diacritics": false }
    /* ... resta de L1s ... */
  },
  "fallback": "Si L1 no és a la llista: usar ALA-LC genèric per a la família lingüística més propera. Marcar verified:false amb prioritat alta per a revisió docent.",
  "cache_validades": "Quan docent corregeix translit al Pas 3 → marca verified:true → entry cachejada (terme + L1 + standard → translit validada) per reutilitzar sense crida LLM futur. Ubicació: BD Supabase (taula atne_translits)."
}
```

---

## 6. Vàlvula docent (verified:false → verified:true)

La transliteració és **l'única excepció pactada** a la regla d'extracció determinista d'ATNE: els estàndards són canon, però la transliteració concreta de cada terme la fa el motor i pot equivocar-se.

**Flux operatiu**:
1. El motor genera la transliteració segons l'estàndard canon per a la L1 → entrada `verified:false`.
2. Indicador visual discret al Pas 3 indica les entrades no verificades.
3. El docent edita inline la translit si cal corregir-la.
4. En guardar, la translit queda `verified:true` i s'envia al cache (taula `atne_translits` a Supabase).
5. Futurs glossaris amb el mateix `(terme, L1)` consulten el cache primer i, si troben una `verified:true`, l'usen **sense cridar el motor**.

**Filosofia de coneixement acumulatiu cross-docent**: la validació d'un docent FJE serveix a tots els altres. La cobertura millora per **ús real**, no per teoria.

---

## 7. Termes científics moderns sense equivalent L1

Cas: termes com "fotosíntesi", "algorisme", "ADN" sovint no tenen calc directe a moltes L1s.

**Política canon**: deixar el **terme català** + nota "(sense equivalent directe)" com a default. El docent pot sobreescriure amb una perífrasi a la L1 si vol.

**Raonament**: és **honestedat lingüística**. Transliterar pseudo-fonèticament un terme científic en una L1 que no el té és confús i inútil. Si la perífrasi és necessària, el docent (que coneix l'alumne) decideix. La translit serveix per a termes que **sí existeixen** a la L1.

---

## 8. Casos vora documentats

- **L1 amb múltiples variants** (àrab dialectal vs estàndard, xinès mandarí vs cantonès): el motor usa la variant estàndard. Si la família parla un dialecte fort (darija marroquí), la translit pot no coincidir 1:1. La **vàlvula docent** ho resol.
- **L1 declarada però alumne ja literat en català** (segona generació): la columna translit aporta poc. El **toggle del Pas 3** ho resol (el docent l'amaga).
- **L1 amb alfabet variable** (amazic Tifinagh vs llatí): la decisió de translit es fa segons la variant declarada al perfil. Default: variant llatina si no s'especifica.

---

## 9. Referències i font

- mineriaRAG `docs/transliteracio_standards_l1_2026-05-31.md` (esborrany original)
- NotebookLM perfil `fje`, notebook "L'aula d'acollida a l'aula ordinària: transició" (12 fonts FJE, query 31/05)
- Actes d'acollida FJE 26.02.2025 (Poble Sec, Sagrat Cor-Vic, Casp, Educar-me Primària)
- Cummins, J. (2002). *Llengua, poder i pedagogia* — Hipòtesi d'Interdependència Lingüística
- Marc MALL/TILC (M2_PBCS, M2_LIT, M3_TIL al corpusFJE)
- Pedagogia ignasiana: cura personalis, acompanyament personalitzat, respecte a la identitat

---

## 10. Estat de la proposta

- **Esborrany 2026-05-31**: pendent ingesta canon per mineriaRAG.
- **Versió 1.0** congelada: quan mineriaRAG accepti la taula i resolgui els GAPS (§3.2 amazic/mandinga/fula/soninké/persa/darija).
- **Versió 1.x** evolutiva: la taula creix per evidència real (política open-list §3.3).
