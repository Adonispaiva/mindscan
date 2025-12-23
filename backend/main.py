import os
import sys
from pydantic import BaseModel
from typing import List

# --- AJUSTE DE CAMINHOS PARA EVITAR ERROS DE MÓDULO ---
atual = os.path.dirname(os.path.abspath(__file__))
raiz = os.path.dirname(atual)
sys.path.insert(0, raiz)
sys.path.insert(0, atual)

import uvicorn
from fastapi import FastAPI, Request, Depends, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

# Importações seguras do Banco de Dados
try:
    from db.session import SessionLocal
except ImportError:
    from backend.db.session import SessionLocal

try:
    from models import Usuario
except ImportError:
    try:
        from models.models import Usuario
    except ImportError:
        from backend.models.models import Usuario

app = FastAPI(title="MindScan V4")

# Montagem de arquivos estáticos (Logo) e Templates
app.mount("/static", StaticFiles(directory=os.path.join(raiz, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(atual, "templates"))

# Modelo de dados para o questionário
class AssessmentData(BaseModel):
    user_id: str
    name: str
    big5_responses: List[int]
    dass21_responses: List[int]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ROTA 1: Home (Portal)
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ROTA 2: Formulário (Questionário)
@app.get("/form", response_class=HTMLResponse)
async def form(request: Request):
    return templates.TemplateResponse("form_mindscan.html", {"request": request})

# ROTA 3: Receber Dados do Questionário (API)
@app.post("/api/v1/submit-assessment")
async def handle_submit(data: AssessmentData, db: Session = Depends(get_db)):
    try:
        novo = Usuario(nome=data.name, email=data.user_id)
        db.add(novo)
        db.commit()
        return JSONResponse(content={"status": "success"}, status_code=200)
    except Exception as e:
        print(f"Erro ao salvar no banco: {e}")
        return JSONResponse(content={"detail": str(e)}, status_code=500)

# ROTA 4: Painel Admin
@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request, db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return templates.TemplateResponse("dashboard_milena.html", {"request": request, "avaliacoes": usuarios})

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)