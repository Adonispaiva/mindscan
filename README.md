# MindScan — Backend API

API assíncrona construída com FastAPI para o projeto MindScan (Inovexa).

---

## 🚀 Execução Local

### Requisitos
- Python 3.11.6
- Virtualenv (opcional)

### Passos
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

pip install -r requirements.deploy.txt
uvicorn main:app --reload
