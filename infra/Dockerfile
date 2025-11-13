# Etapa 1: Build do frontend
FROM node:20 AS frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Etapa 2: Backend (FastAPI)
FROM python:3.11 AS backend
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

# Copia backend e frontend compilado
COPY backend/ ./backend/
COPY --from=frontend /app/frontend/dist ./frontend/dist

# Porta e comando de inicialização
EXPOSE 8000
CMD ["python", "backend/start.py"]
