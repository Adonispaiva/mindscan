# D:\projetos-inovexa\mindscan\backend\README.md

# 📦 MindScan - Backend

API backend do projeto **MindScan** usando **FastAPI**, **PostgreSQL**, **SQLAlchemy async** e **Docker**.

---

## 🚀 Executar com Docker
```bash
cd D:\projetos-inovexa\mindscan\backend
docker-compose up --build
```

Acesse: [http://localhost:8000](http://localhost:8000)

---

## 🔍 Estrutura de Pastas
```
backend/
├── models/               # ORM (SQLAlchemy)
├── routers/              # Rotas (FastAPI)
├── main.py               # Entrypoint da API
├── requirements.txt      # Dependências
├── Dockerfile            # Imagem backend
├── docker-compose*.yml   # Orquestração
├── .env / .env.example   # Variáveis de ambiente
└── tests/                # Testes com pytest
```

---

## 🧪 Testes com Pytest
```bash
pip install -r requirements.txt
pytest tests/
```

---

## ⚙️ Variáveis de Ambiente (`.env`)
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mindscan_db
DB_USER=mindscan_user
DB_PASSWORD=mindscan_pass
ALLOWED_ORIGINS=http://localhost:3000
```

---

## 🔧 Endpoints principais
| Método | Rota     | Descrição                     |
|--------|----------|-------------------------------|
| GET    | `/`      | Verifica saúde da API         |
| GET    | `/user`  | Endpoint de exemplo de usuário|

> Rotas reais dependerão das implementações em `routers/`

---

## 👨‍💻 Manutenção
- Utilize `.env` para configurações locais
- Logs configurados com `logging`
- Docker usa volumes para dev com hot reload

---

## 📬 Contato
Projeto mantido por Inovexa Software · Engenharia: Leo + GPT Inovexa
