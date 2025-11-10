# Dockerfile para o backend MindScan (FastAPI)
FROM python:3.11-slim

# Criação de diretório de trabalho
WORKDIR /app

# Copia arquivos de dependência primeiro (cache)
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia a aplicação
COPY ./app ./app

# Comando de execução
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
