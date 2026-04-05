# Oportunitats de col.laboracio BSC i ajuts per ATNE

**Data**: 4 abril 2026
**Per a**: Direccio FJE — explorar vies de finançament i aliances

---

## 1. El BSC i per que ens interessa

El Barcelona Supercomputing Center (BSC) te dos projectes directament relacionats amb ATNE:

### 1.1 Projecte AINA (catala)
- **Que es**: Iniciativa de la Generalitat per garantir la supervivencia del catala en l'era digital
- **Model**: Salamandra (2B, 7B, 40B parametres) — entrenat amb catala sobremostrejat (2x)
- **Llicencia**: Apache 2.0 (totalment lliure)
- **Rellevancia ATNE**: Es l'unic LLM del mon **entrenat especificament per al catala** per una institucio publica

### 1.2 Projecte ALIA (espanyol i cooficials)
- **Que es**: Extensio d'AINA a castella, gallec, basc
- **Model**: ALIA-40B (disponible a HuggingFace)
- **Rellevancia ATNE**: Si escalem a 15.000 docents de tot Espanya, necessitem un model que funcioni be en totes les llengues cooficials

### 1.3 AI Factory Barcelona
- MareNostrum 5 s'amplia el 2026 amb GPU per entrenar LLMs
- Barcelona es una de les 7 AI Factories de la UE
- Telefonica + Fujitsu instal.len particions especifiques per LLMs

---

## 2. Proposta de col.laboracio BSC — Projecte win-win

### Que oferim nosaltres (FJE/ATNE)
1. **Cas d'us real i mesurable**: 1.000 docents, 15.000 alumnes, dades reals d'us
2. **Corpus pedagogic etiquetat**: 1.443 chunks vectoritzats + Knowledge Graph (952 nodes, 2.294 arestes)
3. **Rubrica d'avaluacio fonamentada**: 8 criteris, 6 marcs teorics, 3.000+ avaluacions
4. **Diversitat de perfils**: nouvinguts (arab, amazic, ucrates, xines), NESE, altes capacitats, 2e
5. **Experiencia en DUA**: Disseny Universal per a l'Aprenentatge aplicat a IA

### Que ofereix el BSC
1. **Infraestructura GPU** per entrenar/fine-tunar Salamandra per a educacio
2. **Expertise en NLP catala** (el millor equip del mon en tecnologia linguistica catalana)
3. **Prestigi academic** per a publicacions i congressos
4. **Connexio amb la Generalitat** (AINA es projecte governamental)

### Linies de recerca conjunta

| Linia | Descripcio | Impacte |
|-------|-----------|---------|
| **Fine-tuning Salamandra per educacio** | Adaptar Salamandra 40B amb el nostre corpus pedagogic per a simplificacio/adaptacio de textos educatius en catala | Model especific per educacio inclusiva |
| **Benchmark d'adaptacio textual en catala** | Publicar el nostre dataset de 1.800 adaptacions + 6.000 avaluacions com a benchmark academic | Referencia per a la comunitat investigadora |
| **Avaluacio automatica de textos adaptats** | Validar la nostra rubrica v2 com a metrica automatica (correlacio amb avaluacio humana) | Standard per avaluar simplificacio textual |
| **Sobirania linguistica en IA educativa** | Demostrar que models oberts entrenats localment competeixen amb GPT/Gemini per a catala educatiu | Argument politic i academic fort |

### Format del projecte
- **Tipus**: Conveni de col.laboracio BSC-FJE (no cal ser universitat)
- **Duracio**: 2-3 anys
- **Equip BSC**: Language Technologies Unit (LT) — el grup que fa Salamandra
- **Contacte**: projecteaina@bsc.es / lt@bsc.es
- **Precedent**: AINA ja col.labora amb entitats no universitaries (Omnium, VilaWeb, ACN, Nacio Digital)

---

## 3. Ajuts i finançament disponibles

### 3.1 Espanya — Convocatories actives o properes

| Ajut | Organisme | Import | Termini | Encaix ATNE |
|------|-----------|--------|---------|-------------|
| **Misiones I+D en IA** | Ministerio Ciencia | Fins 2M€ per projecte | Anual | Alt — IA per educacio inclusiva |
| **Proyectos en IA 2025/2026** | AEI (Agencia Estatal Investigacion) | Variable | 2026 | Alt — investigacio aplicada |
| **Ticket Innova 2026** | CDTI | Fins 7.000€ per PYME | Obert tot l'any | Baix (massa petit) |
| **CDTI Innovacio** | CDTI | Fins 250.000€ prestec bla | Continu | Mig — cal ser empresa |
| **Ajuts integracio IA en cadenes de valor** | Espana Digital 2026 | Variable | Periodica | Mig — mes orientat a industria |

### 3.2 Catalunya

| Ajut | Organisme | Import | Encaix ATNE |
|------|-----------|--------|-------------|
| **Estrategia Catalunya IA 2030** | Generalitat (Politiques Digitals) | Pendent convocatories | Alt — IA + catala + educacio |
| **Projectes catala digital** | Generalitat | 56 projectes finançats (2025) | Molt alt — ATNE en catala per alumnat divers |
| **AI Skills Lab** | Dept. Educacio + URV | Integrat en centres | Alt — mateixa linia (IA a l'aula) |
| **Subvencions robotica/computacional** | ACCIO + Codi Escola 4.0 | Variable | Mig — mes orientat a STEM |

### 3.3 Europa — Horizon Europe 2026-2027

| Convocatoria | Pressupost | Termini | Encaix ATNE |
|-------------|-----------|---------|-------------|
| **HORIZON-CL2-2027-01-TRANSFO-05**: IA en entorns d'aprenentatge pre-primaria i primaria | 3 projectes finançats | 2027 | **MOLT ALT** — es exactament el que fem |
| **HORIZON-RAISE-2026-01**: IA responsable | 90M€ | 2026 | Alt — IA inclusiva i etica |
| **Cluster 2: Cultura, creativitat i societat inclusiva** | Variable | 2026-2027 | Alt — inclusio educativa |

**IMPORTANT**: La convocatoria Horizon CL2-2027-TRANSFO-05 ("IA en entorns d'aprenentatge") es **exactament ATNE**. Caldria un consorci europeu (FJE + BSC + universitat + partner europeu).

---

## 4. Visio ampliada: Ecosistema ATNE

L'ATNE actual (adaptador de textos) es nomes el primer modul d'un ecosistema mes ampli:

### Moduls futurs

| Modul | Descripcio | Base tecnologica |
|-------|-----------|-----------------|
| **M1. Adaptador de textos** (ATNE actual) | Adapta textos educatius per perfil alumne | RAG + LLM + rubrica v2 |
| **M2. Creador de materials** | Genera textos educatius nous a partir de descriptors curriculars | LLM + curriculum vectoritzat |
| **M3. Adaptador d'activitats** | Transforma activitats (exercicis, problemes) per nivell i perfil | LLM + banco d'activitats |
| **M4. Creador de dinamiques** | Dissenya dinamiques d'aula (debats, jocs, cooperatiu) | LLM + metodologies FJE |
| **M5. Sequenciador** | Crea sequencies didactiques i situacions d'aprenentatge | LLM + programacions + LOMLOE |
| **M6. Programador trimestral/anual** | Genera programacions per materia, etapa, grup | LLM + normativa + calendari |
| **M7. Avaluador** | Crea rubriques, proves, instruments d'avaluacio formativa | LLM + marc avaluacio FJE |
| **M8. Diagnostic** | Perfila alumnes a partir d'observacio docent (conversacional) | LLM + taxonomia 200+ variables |

### Arquitectura comuna

Tots els moduls compartirien:
- **Corpus FJE vectoritzat** (RAG + KG) — ja tenim la infraestructura
- **Perfils d'alumnat** (memoria triadica) — ja dissenyat
- **Motor LLM** (Gemma 4 / Salamandra / Gemini) — ja connectat
- **Sistema d'avaluacio** (rubrica adaptada per modul) — ja implementat per M1
- **UI docent** (parametres, no xat obert) — ja dissenyat

### Calendari possible

```
2026 S1: M1 (ATNE) validat + pilot FJE
2026 S2: M3 (activitats) + M7 (avaluacio) — reaprofiten 80% del codi
2027 S1: M2 (materials) + M5 (sequencies) — requereixen corpus curricular
2027 S2: M6 (programacions) + M8 (diagnostic)
2028:    Ecosistema complet + escalat
```

---

## 5. Proposta de projecte per a convocatoria

### Titol
**"IA Inclusiva per a l'Educacio: Adaptacio Automatica de Materials Educatius amb Models de Llenguatge Oberts i Sobirania Linguistica"**

### Consorci proposat
| Partner | Rol | Pais |
|---------|-----|------|
| **FJE (Jesuites Educacio)** | Lider pedagogic, pilot amb 1.000 docents, corpus | ES |
| **BSC** | Infraestructura GPU, models Salamandra/AINA, NLP catala | ES |
| **Universitat (UAB/UB/URV)** | Recerca academica, publicacions, avaluacio | ES |
| **Partner europeu (p.ex. universitat finlandesa/estoniana)** | Replicacio multilingue, comparativa | EU |

### Pressupost estimat
| Partida | Import |
|---------|--------|
| Personal investigador (3 anys) | 400.000€ |
| Infraestructura GPU (BSC in-kind) | 200.000€ |
| Pilot a centres educatius | 100.000€ |
| Disseminacio i publicacions | 50.000€ |
| Coordinacio i gestio | 50.000€ |
| **Total** | **~800.000€** |

### Impacte esperat
- Benchmark public d'adaptacio textual en catala i castella
- Model Salamandra fine-tunat per educacio (open-source)
- Ecosistema de 4-5 moduls per a 15.000 docents
- 3-5 publicacions academiques
- Replicable a altres llengues minoritaries europees

---

## 6. Proxims passos concrets

1. **Contactar BSC** (projecteaina@bsc.es) — presentar ATNE i proposar reunio exploratoria
2. **Contactar Dept. Educacio** — vincular amb AI Skills Lab i estrategia IA 2030
3. **Identificar universitat partner** — UAB (Dept. Traduccio) o URV (AI Skills Lab)
4. **Preparar dossier** — resultats avaluacio + demo funcional + visio ecosistema
5. **Monitoritzar convocatoria Horizon CL2-2027-TRANSFO-05** — termini probablement primavera 2027
6. **Sol.licitar reunio amb Catalonia.AI** — la nova oficina de la Generalitat per IA
