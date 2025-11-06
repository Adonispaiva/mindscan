# Imagem base
FROM python:3.10

# Define o diretório de trabalho como /app/backend
WORKDIR /app/backend

# Copia todos os arquivos do projeto
COPY . /app

# Instala as dependências
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Comando padrão para rodar o app
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=10000"]
