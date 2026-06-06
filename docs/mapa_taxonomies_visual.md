# Mapa visual de les taxonomies d'ATNE

## Diagrama 0 — SÍNTESI: com s'integra tot i com adaptem (flux teòric complet)

> El diagrama-resum. Mostra el procés sencer d'una adaptació ATNE de principi a fi,
> amb els marcs teòrics que fonamenten cada decisió. La resta de diagrames (1-7) en
> despleguen les peces. Renderitzat a `mapa_teoric_adaptacio.png`.

```mermaid
flowchart TB
    TEXT["📄 TEXT ORIGINAL<br/>(currículum, nivell estàndard)"]
    PERFIL["👤 PERFIL DE L'ALUMNE<br/>condició + MECR + L1 + fase lectora"]

    TEXT --> MOTOR
    PERFIL --> MOTOR
    MOTOR{"⚙️ MOTOR D'ADAPTACIÓ ATNE<br/>regla mestra: adaptar el COM,<br/>MAI rebaixar el QUÈ"}

    MOTOR --> VIA1
    MOTOR --> VIA2

    subgraph VIA1["✏️ VIA 1 · TRANSFORMAR EL TEXT (3 tipus)"]
        direction TB
        T1["Lingüístiques<br/><i>lèxic·sintaxi·cohesió·registre</i>"]
        T2["Estructurals<br/><i>segmentar·titular·ordenar</i>"]
        T3["Contingut curricular<br/><i>terminologia·rigor·exemples</i>"]
    end

    subgraph VIA2["🧰 VIA 2 · AFEGIR COMPLEMENTS (6 categories MALL)"]
        direction TB
        C1["Suports DUA · Bastides"]
        C2["Autoregulació · Extensió"]
        C3["(Ajuts i Crossa = humans,<br/>ATNE no els genera)"]
    end

    subgraph TEORIA["📚 MARCS TEÒRICS — ☂️ MALL FJE els integra (no és un marc més)"]
        direction LR
        CUM["Cummins<br/>BICS/CALP<br/><b>fil transversal</b>"]
        VYG["Vygotsky/Bruner<br/>ZDP · scaffolding"]
        HAL["Halliday · Bajtín/Adam<br/>text i gèneres"]
        SOL["Solé · Sanmartí · Mercer<br/>lectura · regulació · diàleg"]
        DUA["DUA (CAST)<br/>representació/implicació"]
    end

    TEORIA -.fonamenta.-> VIA1
    TEORIA -.fonamenta.-> VIA2

    VIA1 --> ORAL
    VIA2 --> ORAL
    ORAL["🗣️ EIX ORAL/ESCRIT (transversal)<br/>a pre-A1/A1: text = guió per a lectura mediada"]

    ORAL --> SORTIDA
    SORTIDA["📘 TEXT ADAPTAT + COMPLEMENTS<br/>regla: «menys és més» (principi MALL)"]

    SORTIDA --> DOCENT
    DOCENT["👩‍🏫 PER AL DOCENT (9 categories A–I)<br/>la factura: QUÈ s'ha transformat + QUÈ s'ha afegit + per què"]

    style TEXT fill:#e8e8e8,stroke:#555
    style PERFIL fill:#e8e8e8,stroke:#555
    style MOTOR fill:#fff3cd,stroke:#b8860b,stroke-width:2px
    style VIA1 fill:#eef6ff,stroke:#1565c0
    style VIA2 fill:#eafaea,stroke:#2e7d32
    style TEORIA fill:#faf0fb,stroke:#6a1b9a
    style CUM fill:#ffe0b2,stroke:#e65100,stroke-width:2px
    style ORAL fill:#e0f7fa,stroke:#00838f
    style SORTIDA fill:#fff8e1,stroke:#b8860b
    style DOCENT fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
```

---

## Diagrama 1 — Les dues coses que fem quan adaptem

```mermaid
flowchart TD
    TEXT["📄 Text original"]
    TEXT --> ADAPT["✏️ 1. ADAPTACIÓ DEL TEXT<br/>(reescriu el text EN SI)<br/>= 'transformacions'"]
    TEXT --> INSTR["🧰 2. INSTRUMENTS DE MEDIACIÓ<br/>(materials NOUS al voltant)<br/>= 'complements' a la UI"]

    ADAPT --> RESULT["📘 Text adaptat + complements"]
    INSTR --> RESULT

    RESULT --> DOCENT["👩‍🏫 'PER AL DOCENT'<br/>explica les DUES coses<br/>(categories A–I)"]

    style TEXT fill:#e8e8e8,stroke:#555
    style ADAPT fill:#cfe8ff,stroke:#1565c0
    style INSTR fill:#d6f5d6,stroke:#2e7d32
    style RESULT fill:#fff3cd,stroke:#b8860b
    style DOCENT fill:#f3e5f5,stroke:#6a1b9a
```

---

## Diagrama 2 — Les tres taxonomies i com es creuen

```mermaid
flowchart TB
    subgraph T1["TAXONOMIA 1 · INSTRUMENTS DE MEDIACIÓ (marc teòric MALL)"]
        direction TB
        BAST["BASTIDES"]
        DUA["SUPORTS DUA"]
        AUTO["AUTOREGULACIÓ"]
        EXT["EXTENSIÓ CURRICULAR"]
        AJUT["AJUTS (docent en directe — ATNE no genera)"]
        CROS["CROSSA (alumne — ATNE no genera)"]
    end

    subgraph T2["TAXONOMIA 2 · CATÀLEG DE BASTIDES (zoom dins BASTIDES)"]
        direction TB
        LEX["lingüístiques lèxiques"]
        SINT["lingüístiques sintàctiques"]
        DISC["lingüístiques discursives"]
        VIS["visuals i multimodals"]
        COG["cognitives"]
        META["metacognitives i lectura"]
        PROD["de producció"]
    end

    BAST -.zoom.-> T2

    style T1 fill:#eef6ff,stroke:#1565c0
    style T2 fill:#eafaea,stroke:#2e7d32
    style BAST fill:#cfe8ff,stroke:#1565c0,stroke-width:3px
```

---

## Diagrama 3 — Una eina viu a les TRES taxonomies alhora (el creuament)

```mermaid
flowchart TB
    GLOS["🔤 GLOSSARI<br/>(una eina concreta)"]

    GLOS --> Q1["Tax.1 — Què ÉS?<br/>→ SUPORT DUA"]
    GLOS --> Q2["Tax.2 — Quina família?<br/>→ Bastida lingüística lèxica"]
    GLOS --> Q3["Tax.3 — Què justifica al docent?<br/>→ Categoria A (+G si bilingüe)"]

    style GLOS fill:#fff3cd,stroke:#b8860b,stroke-width:2px
    style Q1 fill:#eef6ff,stroke:#1565c0
    style Q2 fill:#eafaea,stroke:#2e7d32
    style Q3 fill:#f3e5f5,stroke:#6a1b9a
```

---

## Diagrama 4 — "Per al docent" (A–I): què és transformació i què és complement

```mermaid
flowchart LR
    subgraph DOC["👩‍🏫 PER AL DOCENT (9 categories A–I)"]
        direction TB
        A["A · Adaptació lingüística"]
        B["B · Estructura i organització"]
        E["E · Contingut curricular"]
        C["C · Suport cognitiu"]
        D["D · Multimodalitat"]
        F["F · Avaluació i comprensió"]
        G["G · Personalització lingüística"]
        H["H · Adaptacions per perfil"]
        I["I · Meta-regles transversals"]
    end

    A --- TRANS["✏️ TRANSFORMACIÓ<br/>del text"]
    B --- TRANS
    E --- TRANS

    C --- COMPL["🧰 COMPLEMENT<br/>(instrument)"]
    D --- COMPL
    F --- COMPL

    G --- BOTH["🟣 LES DUES"]
    H --- BOTH

    I --- META["⚪ Transversal"]

    style TRANS fill:#cfe8ff,stroke:#1565c0
    style COMPL fill:#d6f5d6,stroke:#2e7d32
    style BOTH fill:#f3e5f5,stroke:#6a1b9a
    style META fill:#e8e8e8,stroke:#555
    style DOC fill:#faf5ff,stroke:#6a1b9a
```

---

## Diagrama 5 — L'origen teòric de les 3 transformacions

> Cap transformació "pertany" a un sol marc: cada una INTEGRA diversos marcs.
> Cummins (BICS/CALP) travessa les tres. MALL (FJE) és el paraigua que ho embolcalla tot.

```mermaid
flowchart TB
    CUMMINS["🧠 CUMMINS · BICS / CALP<br/>(el fil que travessa les TRES)"]

    subgraph LING["🔵 1. LINGÜÍSTIQUES"]
        L1["Cummins BICS/CALP → quin vocabulari"]
        L2["MECR → gradació (connectors per nivell)"]
        L3["Lectura Fàcil UNE 153101 → frases ≤20p"]
        L4["Plain language → simplificar amb dignitat"]
    end

    subgraph ESTR["🟢 2. ESTRUCTURALS"]
        E1["DUA Principi 1 (Representació) → múltiples vies"]
        E2["Sweller* → reduir càrrega extrínseca (segmentar)"]
        E3["Vygotsky ZDP → mantenir dins la zona"]
        E4["Gèneres: Bajtín + J.M. Adam → estructura canònica"]
    end

    subgraph CONT["🟡 3. CONTINGUT CURRICULAR"]
        C1["MALL doble eix → adaptar COM, mai el QUÈ"]
        C2["TILC/CLIL → contingut a través de la llengua"]
        C3["DUA Principi 3 (Implicació) → repte i interès"]
        C4["Translanguaging → L1 com a pont cognitiu"]
    end

    CUMMINS --> LING
    CUMMINS --> ESTR
    CUMMINS --> CONT

    MALL["☂️ MALL (FJE) · el paraigua que integra<br/>Cummins + DUA + Vygotsky/Bruner + Halliday + Bajtín/Adam + Solé"]
    LING --> MALL
    ESTR --> MALL
    CONT --> MALL

    style CUMMINS fill:#ffe0b2,stroke:#e65100,stroke-width:3px
    style LING fill:#eef6ff,stroke:#1565c0
    style ESTR fill:#eafaea,stroke:#2e7d32
    style CONT fill:#fff8e1,stroke:#b8860b
    style MALL fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
```

---

## Taula resum — Transformació × Marc teòric

| Transformació | Marc DOMINANT | Marcs que hi aporten |
|---|---|---|
| 🔵 **Lingüístiques** | Cummins (BICS/CALP) | MECR · Lectura Fàcil (UNE 153101)* · Plain language · Halliday (LSF) · MALL P3+P5 |
| 🟢 **Estructurals** | DUA-1 + Sweller* | Vygotsky ZDP · Bruner scaffolding · gèneres discursius (Bajtín + J.M. Adam) · Camps/Zayas (seqüència didàctica) |
| 🟡 **Contingut curricular** | MALL "doble eix" / Cummins | TILC/CLIL · DUA-3 · Translanguaging · 5 HCL (Jorba/Sanmartí) |

> \* **Nota de validació NotebookLM (corpus MALL):** Sweller, Ausubel i la norma UNE 153101
> NO són citats nominalment al corpus MALL — el CONCEPTE hi és (càrrega cognitiva,
> organitzador previ, accessibilitat) però l'autor/norma no. Atribucions externes legítimes,
> però marcades com a tals.

**Claus de lectura:**
- **Cummins (BICS/CALP)** és el fil transversal: a la lingüística tria el vocabulari, a l'estructural sosté l'scaffolding, al contingut és el "doble eix" (mai rebaixar el QUÈ). ✅ *confirmat NotebookLM*
- **MALL** NO és un marc paral·lel: és el **paraigua institucional FJE** que integra tots els altres. ✅ *confirmat NotebookLM: "síntesi integradora de marcs consolidats"*
- **DUA** apareix a dues transformacions amb principis diferents: P1 (Representació) a l'estructural, P3 (Implicació) al contingut.
- ⚠️ **Gèneres = Bajtín (esferes d'activitat) + J.M. Adam (seqüències textuals)**, NO Gibbons (correcció NotebookLM).
- 🔴 **MARC ABSENT (pendent): el PILAR DE L'ORALITAT.** El MALL considera l'oralitat el fonament de tot aprenentatge lingüístic. Falta una 4a transformació possible: **text → guió oral** (lectura mediada) per a pre-A1/A1. Candidat a futur.

---

## Diagrama 6 — Els 12 complements per categoria MALL

> A diferència de les transformacions (origen difús), cada complement té un teòric "pare" nítid.

```mermaid
flowchart TB
    subgraph DUA["🟦 SUPORTS DUA (accés, poden ser permanents)"]
        GL["Glossari → Cummins (CALP) + Ausubel"]
        PI["Pictogrames → DUA-1 + Sweller"]
        IL["Il·lustracions → DUA-1 + Mayer"]
        TO["TOLC/Transllenguatge → Cummins + González-Davies"]
    end

    subgraph BAST["🟧 BASTIDES (temporals, es retiren)"]
        BL["Bastides lingüístiques → Vygotsky/Bruner + Jorba/Gómez/Prat"]
        EV["Esquema visual → Sweller* + Mayer*"]
        MC["Mapa conceptual → Novak* (extern)"]
        MM["Mapa mental → Buzan* (extern)"]
        PC["Preguntes comprensió → Isabel Solé + Sanmartí"]
    end

    subgraph AUTO["🟩 AUTOREGULACIÓ (apoderament alumne)"]
        PA["Pauta interrogació → Sanmartí"]
        RU["Rúbriques → Sanmartí + Black&Wiliam"]
    end

    subgraph EXT["🟪 EXTENSIÓ CURRICULAR (repte)"]
        AP["Activitats aprofundiment → Bloom + Vygotsky"]
    end

    style DUA fill:#eef6ff,stroke:#1565c0
    style BAST fill:#fff4e6,stroke:#e65100
    style AUTO fill:#eafaea,stroke:#2e7d32
    style EXT fill:#f3e5f5,stroke:#6a1b9a
```

---

## Diagrama 7 — La simetria: transformacions vs complements

```mermaid
flowchart LR
    TEXT["📄 Text original"]

    subgraph TR["✏️ TRANSFORMACIONS (3) — toquen el text"]
        T1["Lingüístiques"]
        T2["Estructurals"]
        T3["Contingut curricular"]
    end

    subgraph CO["🧰 COMPLEMENTS (12) — s'afegeixen al costat"]
        C1["Suports DUA (4)"]
        C2["Bastides (5)"]
        C3["Autoregulació (2)"]
        C4["Extensió curricular (1)"]
    end

    TEXT --> TR
    TEXT --> CO

    TR -.- RG1["Regla: MAI rebaixar el QUÈ<br/>(doble eix Cummins)"]
    CO -.- RG2["Regla: MENYS ÉS MÉS<br/>(no sobre-mediar — Sweller)"]

    style TEXT fill:#e8e8e8,stroke:#555
    style TR fill:#cfe8ff,stroke:#1565c0
    style CO fill:#d6f5d6,stroke:#2e7d32
    style RG1 fill:#fff3cd,stroke:#b8860b
    style RG2 fill:#fff3cd,stroke:#b8860b
```

---

## Taula resum — Complement × Categoria MALL × Teòric pare

| Complement | Categoria MALL | Teòric pare | Estat | Validació NotebookLM |
|---|---|---|---|---|
| Glossari | Suport DUA | Cummins (CALP) + Ausubel* | ✅ | ✅ correcte (Ausubel no citat nominalment) |
| Pictogrames | Suport DUA | DUA-1 + Sweller* | ✅ | ✅ molt coherent |
| Il·lustracions | Suport DUA | DUA-1 + Mayer* | ✅ (beta) | ✅ molt coherent |
| TOLC/Transllenguatge | Suport DUA | Cummins + González-Davies + Corcoll | 🔲 parcial | ✅ **exacta** |
| Bastides lingüístiques | Bastida | Vygotsky/Bruner + Jorba/Gómez/Prat | ✅ | ✅ **exacta** |
| Esquema visual | Bastida cognitiva | Sweller* + Mayer* | ✅ | ✅ coherent |
| Mapa conceptual | Bastida cognitiva | Novak* (extern) | ✅ | ⚠️ MALL NO anomena Novak |
| Mapa mental | Bastida cognitiva | Buzan* (extern) | ✅ | ⚠️ MALL NO anomena Buzan |
| Preguntes comprensió | Bastida metacognitiva | **Isabel Solé** + Sanmartí | ✅ | ⚠️ faltava Solé (referent lectura) |
| Pauta d'interrogació | Autoregulació | Sanmartí | ✅ (checklist) | ✅ **confirmat** |
| Rúbriques | Autoregulació | Sanmartí + Black & Wiliam + DUA-3 | 🔲 | ✅ coherent |
| Activitats aprofundiment | Extensió curricular | Bloom + Vygotsky | ✅ | ✅ coherent |
| Plantilles de gènere | Bastida discursiva | Bajtín + J.M. Adam + TILC | 🔲 | (gèneres = Bajtín/Adam) |
| Resum graduat | Bastida cognitiva | Sweller* (complexitat progressiva) | 🔲 | — |
| Cartes conversacionals | Bastida de producció | MALL + Vygotsky | 🔲 | — |

> \* **No citats nominalment al corpus MALL** (Sweller, Ausubel, Mayer, Novak, Buzan): el CONCEPTE
> hi és, l'autor no. Atribucions externes legítimes però marcades. Veredicte NotebookLM: mapeig
> **"excel·lent, especialment en Suports DUA i Autoregulació"**.

**Claus de lectura:**
- **DUA + Sweller** són el fil transversal dels complements (com Cummins ho era de les transformacions).
- Cada complement té un teòric pare clar, PERÒ atenció: **Novak (mapa conceptual) i Buzan (mapa mental) NO són citats pel MALL** — són atribucions externes nostres (la disciplina els reconeix, però el corpus FJE no els nomena).
- **Preguntes de comprensió: el referent principal de la LECTURA és Isabel Solé** (3 moments), reforçada per Sanmartí (regulació). Correcció NotebookLM.
- La regla mestra dels complements és **"menys és més"**: la matriu proposa 2-3 per condició, no tots. ✅ *Principi PROPI del MALL (font: "6-10 preguntes totals. Mai més."). Convergeix amb la càrrega cognitiva de Sweller, però el MALL no el cita — convergència externa, no fonament (canonitzat a M2_marc-teoric-mediacio.md).*
- 🔴 **Teòrics que el MALL SÍ cita i caldria integrar:** Halliday (LSF), Camps/Zayas (seqüència didàctica), Bajtín (gèneres).
