FROM python:3.11-slim

WORKDIR /app

COPY . .

# Instalar dependências específicas da pasta backend
RUN pip install --no-cache-dir -r backend/requirements.txt

# Comando de inicialização correto
CMD ["uvicorn", "backend.main:app", "--host=0.0.0.0", "--port=10000"]
