# Usa imagem base leve do Python 3.10.12
FROM python:3.10.12-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia apenas o requirements.txt para instalar dependências
COPY requirements.txt requirements.txt

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os arquivos do projeto para o container
COPY . .

# Comando para iniciar o servidor (ajuste se o nome do arquivo for outro)
CMD ["python", "start_mindscan.py"]
