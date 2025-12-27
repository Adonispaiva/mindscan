import os
import sys
from pydantic import BaseModel
from typing import List
from openai import OpenAI
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração de Path para garantir reconhecimento dos módulos locais
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
sys.path.insert(0, ROOT_DIR)

import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from db.session import SessionLocal
from models.models import Usuario

# CLIENTE OPENAI - Carregamento via Variável de Ambiente
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

app = FastAPI(title="MindScan V4 - AI Powered")

app.mount("/static", StaticFiles(directory=os.path.join(ROOT_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Schemas para validação de dados (Pydantic)
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

def processar_ia_mindscan(nome: str, big5: List[int], dass: List[int]) -> str:
    """
    Motor de processamento que transforma números em laudo psicoprofissional.
    """
    if not api_key:
        return "<p>Erro: OPENAI_API_KEY não configurada no arquivo .env.</p>"

    system_prompt = (
        "Você é um Especialista em Psicometria e Analista de RH da Inovexa Software. "
        "Sua tarefa é analisar dados brutos e gerar um relatório executivo de alto nível."
    )
    
    user_content = f"""
    Candidato: {nome}
    Dados Big Five (50 itens): {big5}
    Dados DASS-21 (21 itens): {dass}

    Gere um relatório estruturado em HTML (use apenas tags <h4>, <p>, <ul> e <li>):
    1. Resumo do Perfil Comportamental.
    2. Principais Competências Identificadas.
    3. Alerta de Riscos (Baseado no DASS-21).
    4. Conclusão de Fit Cultural.
    """

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.7
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"<p>Erro no processamento da IA: {str(e)}</p>"

@app.get("/", response_class=HTMLResponse)
async def menu_inicial(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/form", response_class=HTMLResponse)
async def exibir_formulario(request: Request):
    return templates.TemplateResponse("form_mindscan.html", {"request": request})

@app.post("/api/v1/submit-assessment")
async def handle_submit(data: AssessmentData, db: Session = Depends(get_db)):
    try:
        # Geração do Laudo via Inteligência Artificial
        laudo_gerado = processar_ia_mindscan(data.name, data.big5_responses, data.dass21_responses)

        # Persistência no PostgreSQL
        novo_usuario = Usuario(
            nome=data.name, 
            email=data.user_id, 
            relatorio=laudo_gerado
        )
        db.add(novo_usuario)
        db.commit()
        
        return JSONResponse(content={"status": "success", "message": "Avaliação processada com IA"}, status_code=200)
    except Exception as e:
        db.rollback()
        return JSONResponse(content={"detail": str(e)}, status_code=500)

@app.get("/admin", response_class=HTMLResponse)
async def painel_admin(request: Request, db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return templates.TemplateResponse("dashboard_milena.html", {
        "request": request,
        "avaliacoes": usuarios
    })

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)