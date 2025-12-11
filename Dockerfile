# ============================================================
# MindScan — Dockerfile (API Web + MI Híbrido)
# ============================================================

FROM python:3.11-slim

# Evitar bytecode e buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Criar diretório da aplicação
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt /app/

# Instalar libs Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código do MindScan
COPY . /app/

# Expor porta da API
EXPOSE 8000

# Comando final: iniciar FastAPI via Uvicorn
CMD ["uvicorn", "mindscan_web_api:app", "--host", "0.0.0.0", "--port", "8000"]
