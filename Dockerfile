FROM python:3.11-slim

WORKDIR /app

# Previene la scrittura dei file .pyc e forza l'output dei log immediato
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Installa le dipendenze di sistema minime
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia e installa i requisiti Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia l'intero progetto
COPY . .

# Crea le cartelle dati se non esistono
RUN mkdir -p data logs exports

# Espone la porta della Dashboard FastAPI
EXPOSE 8000

# Avvia il server web FastAPI
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]