import os
import sys
import logging

# =================================================================
# ORION: CONFIGURAÇÃO DE RAIZ E RESOLUÇÃO DE NAMESPACE
# =================================================================
backend_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(backend_dir)

if project_root not in sys.path:
    sys.path.insert(0, project_root)

if backend_dir in sys.path:
    sys.path.remove(backend_dir)

try:
    from backend.database import engine, Base, get_db
    from backend.models.user import User
    
    # Sincroniza tabelas com o PostgreSQL
    Base.metadata.create_all(bind=engine, checkfirst=True)
    print("✅ MindScan: Arquitetura Validada. Conexão PostgreSQL Ativa.")
except Exception as e:
    print(f"❌ Erro de Inicialização Orion: {e}")
    sys.exit(1)

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime

# Importação dos novos routers
from backend.routers import sessions

app = FastAPI(
    title="MindScan API Gateway", 
    version="4.0.0",
    description="Portal de diagnósticos e processos de seleção Inovexa"
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusão de rotas do sistema
app.include_router(sessions.router)

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    return {
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "database": "PostgreSQL Connected"
    }

@app.get("/test-db")
def test_database_persistence(db: Session = Depends(get_db)):
    """Cria um registro temporário para validar a escrita no banco."""
    try:
        new_user = User(name="Teste Orion", email=f"teste_{datetime.now().timestamp()}@inovexa.com")
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "Sucesso! Usuário persistido", "user": new_user.name, "id": new_user.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na persistência: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Execução via módulo para preservar o namespace no Windows
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)