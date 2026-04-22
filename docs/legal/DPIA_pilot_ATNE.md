# DPIA — Avaluacio d'Impacte en Proteccio de Dades

## Pilot ATNE (Adaptador de Textos a Necessitats Educatives)

**Versio del document**: 1.0 — esborrany inicial per revisio del DPO FJE
**Data de redaccio**: 2026-04-22
**Ambit**: pilot controlat amb 16 docents de Jesuites Educacio (20 d'abril — 8 de maig de 2026)
**Autor tecnic**: Miquel Amor (responsable del projecte ATNE, FJE)
**Estat**: pendent de revisio i aprovacio per part del DPO institucional de la FJE

---

## 1. Identificacio del responsable del tractament

**Responsable del tractament**:
Fundacio Jesuites Educacio (FJE) — titular de la xarxa escolar Jesuites Educacio.

**Delegat de Proteccio de Dades (DPO)**:
Pendent — cal confirmar amb el DPO institucional de la FJE.
*Contacte provisional fins a confirmacio:* miquel.amor@fje.edu.

**Encarregats del tractament (subencarregats tecnologics)**:

| Encarregat | Funcio | Ubicacio de les dades |
|---|---|---|
| Supabase (PostgreSQL gestionat) | Autenticacio i persistencia (perfils, historial, events) | UE |
| Google Cloud Run | Hosting del backend FastAPI (servei ATNE) | UE (europe-west1 o equivalent) |
| Google LLC (Gemini / Gemma API) | Crides sincrones al model LLM per a l'adaptacio de text | Segons regio de l'API; tractament transitori |
| OpenAI (GPT-4o, GPT-4.1-mini) | Crides sincrones al model LLM (rotacio) | Tractament transitori segons politica OpenAI API |
| LanguageTool API | Correccio ortografica determinista del text de sortida | UE |

Totes les crides a encarregats es fan des del backend FJE amb claus API institucionals. No hi ha acces directe del navegador del docent als LLMs de tercers.

---

## 2. Descripcio del tractament

ATNE es un assistent d'IA generativa que ajuda docents de la FJE a adaptar textos educatius (lectures, enunciats, consignes) a les necessitats d'aprenentatge de l'alumnat divers: nouvinguts, alumnat amb NESE (TDAH, dislexia, DEA, TEA), altes capacitats i configuracions multinivell DUA.

**Flux de dades tipic del pilot**:

1. El docent entra a ATNE via navegador i s'autentica amb Google OAuth restringit al domini `@fje.edu` (Supabase Auth + JWT).
2. **Pas 1** — tria o crea un perfil d'alumne o grup (curs, MECR, condicions).
3. **Pas 2** — enganxa, puja o genera un text base + configura materia, genere discursiu i complements.
4. **Pas 3** — el backend envia un prompt estructurat a un LLM (rotacio Gemma 4 31B / GPT-4o / GPT-4.1-mini / Gemma 3 27B) i retorna l'adaptacio via SSE (Server-Sent Events).
5. El docent valora el resultat (rubrica), pot refinar, exportar PDF, desar al seu historial (`atne_drafts`).
6. Paral.lelament es registra un event analitic (`pilot_events`) per a analisi d'us agregada.

**Tecnologies principals**:
- Backend: Python 3.12 + FastAPI + uvicorn (Cloud Run).
- Frontend: HTML + JavaScript vanilla + CSS (zero frameworks).
- Base de dades: Supabase (PostgreSQL gestionat).
- Autenticacio: Supabase Auth + Google OAuth (restringit a `@fje.edu`).
- LLMs: rotacio entre Gemma 4 31B (API free tier), GPT-4o, GPT-4.1-mini, Gemma 3 27B.

**Finalitats del tractament**:
- (a) Prestacio del servei d'adaptacio pedagogica.
- (b) Millora del sistema ATNE a partir de l'analisi d'us real.
- (c) Publicacio de resultats agregats i/o anonimitzats en comunicacions internes FJE i, si escau, en publicacions academiques derivades del pilot.

---

## 3. Categories de dades recollides

### 3.1 Dades identificatives

- Nom i cognoms del docent (via Google OAuth).
- Adreca de correu electronic `@fje.edu`.
- Identificador intern Supabase (`user_id` UUID).

### 3.2 Dades professionals

- Escola d'adscripcio.
- Curs(os) i materia(es) que imparteix.
- Etapa educativa.
- Rol dins del pilot (participant, coordinador).

### 3.3 Comportament d'us

- Events UX: clics, tries de model, durada de sessio, temps per tasca.
- Model LLM utilitzat en cada adaptacio.
- Versio del prompt / capa de configuracio activa.
- Nombre d'adaptacions, refinaments, exports.

### 3.4 Contingut generat

- Text original enganxat o pujat pel docent.
- Text adaptat retornat pel LLM.
- Complements generats (preguntes de comprensio, bastides, glossari).
- Configuracions de perfil d'alumnat (pseudonim/etiqueta, MECR, condicions, anotacions contextuals).

### 3.5 Judici pedagogic

- Valoracions numeriques (rubrica) sobre la qualitat de l'adaptacio.
- Comentaris lliures del docent.
- Feedback d'incidencies.

**No es recullen**:
- Categories especials de dades (art. 9 RGPD) directament. Pero el text lliure que el docent pot escriure a descripcions de perfil pot incloure informacio sensible (diagnostic, conducta) — veure mitigacions a §9.
- Dades de localitzacio precisa.
- Dades financeres.

---

## 4. Categories d'interessats

**Interessats directes**: 16 docents participants del pilot (adscrits a centres de la FJE).

**Interessats indirectes**: no es recullen dades directes de l'alumnat. Pero els docents poden, en descriure un perfil, incloure referencies contextuals a alumnes concrets. El disseny de l'eina ho desincentiva (veure §9 — mitigacions):

- Les etiquetes de perfil proposades son pseudonims genericos (p. ex. "Alumne A — 2n ESO B").
- La interficie recomana explicitament no incloure-hi noms reals.
- El consentiment informat (veure `ui/atne/consent.html`) alerta el docent.

---

## 5. Base juridica del tractament

- **Art. 6.1.a RGPD** — Consentiment informat exprés del docent, recollit abans del primer us efectiu de l'aplicacio mitjançant pantalla dedicada (`/ui/atne/consent.html`). El consentiment es granular: el docent pot usar l'eina sense participar al component de recerca.
- **Art. 6.1.f RGPD** — Interes legitim del responsable per a la millora del servei i l'avaluacio del sistema, amb ponderacio favorable pel baix risc (dades professionals, no sensibles directes) i amb mesures de mitigacio (pseudonimitzacio, minimitzacio).
- **LOPDGDD (LO 3/2018)** — garanties addicionals al tractament de dades en l'ambit educatiu.

No s'invoquen art. 6.1.b (execucio de contracte) ni 6.1.e (mission de servei public) en aquesta fase de pilot voluntari.

---

## 6. Finalitats i usos previstos

| # | Finalitat | Base juridica | Retencio |
|---|---|---|---|
| F1 | Prestacio del servei d'adaptacio | Consentiment | 2 anys, despres anonimitzacio irreversible |
| F2 | Millora del sistema (A/B, ajust de prompts, qualitat LLM) | Interes legitim | 2 anys sobre dades pseudonimitzades |
| F3 | Publicacio de resultats agregats en comunicacions FJE | Consentiment | Indefinit (dades anonimitzades o agregades) |
| F4 | Possible publicacio academica (congrès, revista) | Consentiment | Indefinit (dades anonimitzades) |

Els usos de F3 i F4 nomes utilitzaran dades agregades (estadistiques) o textos anonimitzats de forma irreversible (eliminacio de qualsevol element identificatiu directe o indirecte).

---

## 7. Avaluacio de necessitat i proporcionalitat

La recollida de dades es valora com a **minima necessaria** per a cada finalitat:

- **Identificatives**: imprescindibles per autenticacio (@fje.edu) i per oferir historial personal de treballs al docent.
- **Professionals**: necessaries per a adequar les adaptacions al context pedagogic i per analisi agregada per etapa/materia.
- **Comportament d'us**: necessaries per diagnosticar problemes d'usabilitat i triar el millor model LLM per cada tipus de cas.
- **Contingut generat**: necessari per a la finalitat central (prestacio del servei) i per a la millora mitjançant revisio qualitativa del rendiment del sistema.
- **Judici pedagogic**: imprescindible per a la finalitat de millora; constitueix el senyal de qualitat.

No s'ha identificat cap finalitat que requereixi dades addicionals. S'ha descartat recollir: IP, user-agent detallat, geolocalitzacio, historial de navegacio fora de l'app, dades de dispositius.

---

## 8. Riscos identificats

| Risc | Descripcio | Probabilitat | Impacte |
|---|---|---|---|
| R1 — Perfilat professional | Que les dades d'us es puguin utilitzar per avaluar individualment el rendiment del docent | Baixa | Mitja |
| R2 — Identificacio indirecta d'alumnes | Que el contingut de descripcions lliures inclogui dades personals d'alumnes concrets | Mitjana | Alt |
| R3 — Biaix algorismic | Que les adaptacions reforcin estereotips sobre condicions (dislexia, TDAH, etc.) | Mitjana | Mitja |
| R4 — Dependencia tecnologica | Vincle amb encarregats no-UE (OpenAI, Google LLC) per al processament del text | Alta | Baix-mitja |
| R5 — Fuites de contingut pedagogic | Acces no autoritzat a borradors o textos pujats | Baixa | Mitja |
| R6 — Conservacio excessiva | Mantenir dades identificatives mes enlla del necessari | Mitjana | Mitja |
| R7 — Transparencia insuficient | Docent no entén el tractament o l'abast | Mitjana | Alt (erosio de confiança) |

---

## 9. Mesures de mitigacio

### 9.1 Pseudonimitzacio

- Identificador primari per a analisi: `docent_hash = SHA256(email + salt institucional)`. L'email en clar queda a la taula d'autenticacio (amb acces restringit), pero els events, drafts i historial utilitzen nomes el hash.
- Els perfils d'alumne utilitzen etiquetes generiques, no noms reals. La UI desaconsella explicitament l'us de noms.

### 9.2 Anonimitzacio irreversible per a publicacio

- Abans de qualsevol us publicatiu (F3, F4) s'aplica un procediment d'anonimitzacio irreversible:
  - Eliminacio de `docent_hash`, email, escola especifica (substituida per etapa).
  - Revisio manual de textos lliures per eliminar noms d'alumnes, topónims, date concretes.
  - Agregacio a nivell d'etapa o materia quan el N ho permet.

### 9.3 Retencio

- **2 anys** des de la data de recollida per a dades identificatives + comportament + contingut.
- Passat aquest periode, s'aplica anonimitzacio irreversible o eliminacio segons la utilitat residual.
- El docent pot sol.licitar eliminacio anticipada en qualsevol moment (art. 17 RGPD).

### 9.4 Control d'acces

- Acces a dades identificades (taula `auth.users`, `atne_docents`): nomes Miquel Amor (responsable tecnic) i DPO FJE.
- La interficie `/admin` esta protegida per token HMAC i restringida a usuaris amb rol explicit.
- Cap desenvolupador/colaborador extern te acces a dades identificatives.
- Auditoria: totes les consultes administratives queden registrades.

### 9.5 Xifratge

- En transit: TLS 1.2+ (HTTPS obligatori, Cloud Run + Supabase).
- En reposa: xifratge nativo de Supabase (AES-256).
- Les claus d'API es gestionen via variables d'entorn i no s'exposen al client.

### 9.6 Drets ARCOPOL

Procediment per exercir drets:
- Contacte: `dpo@fje.edu` (placeholder — pendent confirmacio).
- Resposta en un maxim d'un mes (prorrogable segons art. 12.3 RGPD).
- Canal alternatiu: mail a responsable tecnic (`miquel.amor@fje.edu`).

Drets reconeguts:
- Acces (art. 15)
- Rectificacio (art. 16)
- Supressio / dret a l'oblit (art. 17)
- Limitacio (art. 18)
- Oposicio (art. 21)
- Portabilitat (art. 20)
- No ser objecte de decisions automatitzades (art. 22) — ATNE no pren decisions automatitzades amb efectes juridics sobre el docent.

### 9.7 Minimitzacio i transparencia

- No es registren prompts complets amb contingut identificable d'alumnes en logs operatius (nomes metadades).
- La pantalla de consentiment explica en llenguatge clar (no juridic) que es recull i que no es fa.
- El docent pot retirar el consentiment en qualsevol moment sense penalitzacio ni afectacio de l'us de l'eina.

### 9.8 Transferencies internacionals

Crides als LLMs d'OpenAI i Google LLC poden suposar transferencia puntual a tercers paisos. Mitigacions:
- S'utilitzen les APIs empresarials amb compromis de no-entrenament del model amb el contingut del client.
- Es prioritza, quan possible, el model Gemma 4 31B servit des d'infraestructura UE.
- Cap fitxer amb dades del pilot es carrega a serveis de tercers fora del flux sincron d'adaptacio.

---

## 10. Classificacio segons l'AI Act (Reglament (UE) 2024/1689)

ATNE es un **sistema d'IA generativa** integrat en un producte educatiu. La classificacio dins l'Annex III de l'AI Act:

- **No entra automaticament** a la categoria "alt risc" perque:
  - No avalua automaticament aprenentatges ni atorga titulacions.
  - No decideix sobre acces, admissio o expulsio d'estudiants.
  - El docent conserva el control editorial complet sobre el text generat.
- **Pero s'hi acosta** (zona gris "alt risc adjacent") perque:
  - Opera en el sector educatiu (Annex III §3).
  - Pot influir en les decisions pedagogiques del docent.
  - Tracta informacio sobre alumnat vulnerable.

**Compromis assumit pel projecte** (aplicacio voluntaria de requisits d'alt risc):

1. **Transparencia** (art. 13): la pantalla de consentiment i la interficie identifiquen clarament els continguts generats per IA.
2. **Supervisio humana** (art. 14): el docent revisa i accepta/modifica cada adaptacio abans del seu us amb l'alumnat. No hi ha auto-publicacio.
3. **Documentacio tecnica** (art. 11): es mantenen registres de configuracio, versions de prompt, models utilitzats.
4. **Qualitat de les dades** (art. 10): el corpus pedagogic de referencia (corpusFJE) es auditat internament.
5. **Robustesa i ciberseguretat** (art. 15): control d'acces, autenticacio forta, logs d'auditoria.

En el moment d'escalar mes enlla del pilot (cap als 1000+ docents de la FJE) s'hauria de fer una reavaluacio formal de la classificacio.

---

## 11. Consulta amb el DPO i aprovacio

- **Estat actual**: esborrany redactat pel responsable tecnic.
- **Accio pendent**: revisio i aprovacio del DPO institucional de la FJE abans de l'inici del pilot (20 d'abril de 2026). Si l'inici ja ha tingut lloc, aquesta DPIA s'incorpora com a documentacio contemporánia amb compromis de revisio en la primera setmana de pilot.
- **Observacions del DPO**: _[espai reservat per a anotacions del DPO]_.

---

## 12. Revisio

Aquesta DPIA es revisara:

- **Obligatoriament** abans d'escalar mes enlla del pilot (pas de 16 a 1000+ docents de la FJE).
- **Obligatoriament** si es produeix un canvi significatiu en:
  - Categories de dades tractades.
  - Models LLM utilitzats o localitzacio dels encarregats.
  - Finalitats del tractament.
- **Anualment** com a minim mentre el servei estigui en produccio.

---

## Annex A — Taules Supabase afectades

| Taula | Contingut | Dades identificatives directes? |
|---|---|---|
| `auth.users` | Credencials Google OAuth | SI (email, nom) |
| `atne_docents` | Perfil del docent FJE | SI (email, escola) |
| `atne_custom_profiles` | Perfils d'alumnat creats pel docent | Indirecte (descripcions lliures) |
| `atne_drafts` | Esborranys desats | Indirecte (contingut de textos) |
| `history` | Historial d'adaptacions | Pseudonimitzat via docent_hash |
| `pilot_events` | Events analitics del pilot | Pseudonimitzat via docent_hash |
| `system_config` | Configuracio del servei | No |
| `rag_fje`, `kg_nodes`, `kg_edges` | Corpus pedagogic (desactivat al pilot) | No |

## Annex B — Documents relacionats

- Pantalla de consentiment informat: `ui/atne/consent.html`.
- Politica de privacitat de la FJE: pendent d'enllaç institucional.
- Contractes amb encarregats del tractament (DPA): Supabase, Google Cloud, OpenAI — responsabilitat de l'area juridica FJE.

---

**Fi del document — v1.0**
