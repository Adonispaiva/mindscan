# ================================================
# Inovexa Monitoring v8.0.5 - Monitor Agent Dockerfile
# ================================================
# Codificação: UTF-8 (sem BOM)
# Base leve com Python 3.12
# -----------------------------------------------

FROM python:3.12-slim AS base

LABEL maintainer="Inovexa Software <labs@inovexa.ai>"
LABEL version="8.0.5"
LABEL description="Inovexa Mindscan - Monitor Agent for Prometheus & Grafana"

# Evita prompts interativos
ENV DEBIAN_FRONTEND=noninteractive

# Diretório de trabalho
WORKDIR /app

# Copia apenas os arquivos essenciais
COPY grafana_provision_omni.py /app/
COPY requirements.txt /app/

# Atualiza sistema e instala dependências mínimas
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta do monitor-agent
EXPOSE 8000

# Define o ponto de entrada
CMD ["python", "grafana_provision_omni.py"]
