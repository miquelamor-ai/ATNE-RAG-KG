# ATNE-RAG-KG — Resum de sessió (2026-03-25)

## Repo
- **Local**: `C:\Users\miquel.amor\Documents\GitHub\ATNE\`
- **Remote origin**: `https://github.com/miquelamor-ai/ATNE-RAG-KG.git`
- **Branca**: `main`
- **Deploy**: Google Cloud Run → `https://atne-1050342211642.europe-west1.run.app`
- **Projecte GCP**: `dreseraios-drive`

## Stack
Python 3.12 + FastAPI + Gemini 2.5-flash + Supabase (RAG-KG) + Cloud Run

## Canvis fets avui

### 1. Reorganització de repos
- L'antic repo `miquelamor-ai/ATNE` es va traspassar a `FundacioJesuitesEducacio/ATNE`
- Es va crear un nou repo personal `miquelamor-ai/ATNE-RAG-KG` per mantenir la versió Python
- El remote `origin` d'aquesta carpeta ara apunta a `ATNE-RAG-KG`
- Es va treure el remote `fje` (ja no cal, el repo institucional té la seva carpeta)

### 2. Cursos i àmbits dinàmics per etapa
- Quan es selecciona **FP**, el menú Curs mostra: 1r CGM, 2n CGM, 1r CGS, 2n CGS
- El menú Àmbit canvia a "Família professional" amb 25 famílies de CF
- Cada etapa té cursos propis: Infantil (P3-P5), Primària (1r-6è), ESO (1r-4t), Batxillerat (1r-2n)
- Fitxer modificat: `ui/app.js` (constants `CURSOS_PER_ETAPA`, `AMBITS_PER_ETAPA`, funció `updateEtapaSelects`)

### 3. Deploy a Cloud Run
- Desplegada revisió `atne-00008-jdj` amb els canvis de cursos/àmbits
- URL: `https://atne-1050342211642.europe-west1.run.app`

## Qüestions pendents

### Per fer
- [ ] Renombrar carpeta local `ATNE` → `ATNE-RAG-KG` (cal tancar VSCode primer, botó dret → Rename)

### Notes
- El Cloud Run actual (`atne`) és la versió Python/RAG-KG amb Gemini i Supabase
- No cal re-deploy tret que es modifiqui codi a `server.py` o `ui/`
- Les credencials (`.env`) tenen Gemini API key + Supabase URL/key

## Estructura de carpetes

```
Documents/GitHub/
├── ATNE/              ← AQUEST PROJECTE (Python + RAG-KG) — renombrar a ATNE-RAG-KG
│   origin: miquelamor-ai/ATNE-RAG-KG.git
│   Deploy: Cloud Run (atne) — https://atne-1050342211642.europe-west1.run.app
│
└── ATNE-FJE/          ← Versió institucional (PHP + OpenAI)
    origin: FundacioJesuitesEducacio/ATNE.git
    Deploy: Cloud Run (atne-fje) — https://atne-fje-1050342211642.europe-west1.run.app
```
