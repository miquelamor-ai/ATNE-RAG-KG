FROM python:3.12-slim

# Fonts per a generació de PDF (Liberation Sans = equivalent mètric d'Arial)
RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Cloud Run estableix PORT automàticament
ENV PORT=8080

CMD exec uvicorn server:app --host 0.0.0.0 --port $PORT
