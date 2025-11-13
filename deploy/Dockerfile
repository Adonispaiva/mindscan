# 🧠 MindScan / SynMind – Dockerfile de Deploy (Backend FastAPI)

# Imagem base enxuta
FROM python:3.11-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Variáveis de ambiente básicas
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Dependências de sistema mínimas (se precisar de mais, incluir aqui)
RUN apt-get update && apt-get install -y \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# Copia arquivos principais do projeto para dentro do container
# (backend + requirements da raiz)
COPY backend/ ./backend/
COPY requirements.txt ./requirements.txt

# Instala dependências Python
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Porta interna padrão da aplicação
EXPOSE 10000

# Comando de inicialização:
# - Usa backend.main:app como ponto de entrada FastAPI
# - Porta lida da variável PORT (Render/Heroku) com fallback 10000
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-10000}"]
