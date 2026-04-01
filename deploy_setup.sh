#!/bin/bash
# Script de configuració inicial per al deploy a Cloud Run
# Executa'l una sola vegada des del terminal (amb gcloud autenticat)
#
# Requisit: gcloud auth login (ja fet)
# Projecte: dreseraios-drive

PROJECT_ID="dreseraios-drive"
REGION="europe-west1"

echo "=== ATNE — Setup Cloud Run + GitHub ==="
echo "Projecte: $PROJECT_ID"
echo ""

# 1. Activar APIs necessàries
echo "[1/5] Activant APIs..."
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  secretmanager.googleapis.com \
  containerregistry.googleapis.com \
  --project=$PROJECT_ID

# 2. Crear secrets (et demanarà els valors)
echo ""
echo "[2/5] Creant secrets a Secret Manager..."
echo "  Introdueix el valor de GEMINI_API_KEY:"
read -s GEMINI_KEY
echo "$GEMINI_KEY" | gcloud secrets create GEMINI_API_KEY \
  --data-file=- --project=$PROJECT_ID 2>/dev/null || \
  echo "$GEMINI_KEY" | gcloud secrets versions add GEMINI_API_KEY \
  --data-file=- --project=$PROJECT_ID

echo "  Introdueix el valor de SUPABASE_URL:"
read -s SUPABASE_URL_VAL
echo "$SUPABASE_URL_VAL" | gcloud secrets create SUPABASE_URL \
  --data-file=- --project=$PROJECT_ID 2>/dev/null || \
  echo "$SUPABASE_URL_VAL" | gcloud secrets versions add SUPABASE_URL \
  --data-file=- --project=$PROJECT_ID

echo "  Introdueix el valor de SUPABASE_ANON_KEY:"
read -s SUPABASE_KEY
echo "$SUPABASE_KEY" | gcloud secrets create SUPABASE_ANON_KEY \
  --data-file=- --project=$PROJECT_ID 2>/dev/null || \
  echo "$SUPABASE_KEY" | gcloud secrets versions add SUPABASE_ANON_KEY \
  --data-file=- --project=$PROJECT_ID

# 3. Donar permisos al compte de servei de Cloud Build
echo ""
echo "[3/5] Configurant permisos Cloud Build..."
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')
CB_SA="${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${CB_SA}" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${CB_SA}" \
  --role="roles/iam.serviceAccountUser"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${CB_SA}" \
  --role="roles/secretmanager.secretAccessor"

# 4. Instruccions per connectar GitHub
echo ""
echo "[4/5] Connecta GitHub al Cloud Build:"
echo "  https://console.cloud.google.com/cloud-build/triggers/connect?project=$PROJECT_ID"
echo "  - Selecciona GitHub"
echo "  - Autoritza accés a miquelamor-ai/ATNE-RAG-KG"
echo "  - Crea trigger: branca 'main', fitxer 'cloudbuild.yaml'"
echo ""

echo "[5/5] Fet! Cada 'git push' a main desplegarà automàticament."
echo "URL del servei: https://atne-<hash>-ew.a.run.app"
echo "(disponible a: https://console.cloud.google.com/run?project=$PROJECT_ID)"
