# Dockerfile - MindScan Backend
FROM python:3.10-slim

# Diretório de trabalho
WORKDIR /app

# Instalação de dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Cópia do restante da aplicação
COPY . .

# Variáveis de ambiente (podem ser substituídas no docker-compose ou CI)
ENV PYTHONUNBUFFERED=1

# Comando de execução padrão
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
