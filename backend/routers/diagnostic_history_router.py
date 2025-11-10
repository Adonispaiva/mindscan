from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from datetime import datetime

router = APIRouter()

# ----------------------------
# 🧾 MODELO DE HISTÓRICO
# ----------------------------
class DiagnosticRecord(BaseModel):
    nome: str
    score_depressao: int
    score_ansiedade: int
    score_estresse: int
    data: datetime
    relatorio: str

# 🔒 MOCK DEPENDÊNCIA DE USUÁRIO (ex: login)
def get_current_user():
    return "milena@clinica.com"

# 📦 MOCK DATABASE TEMPORÁRIA
db_diagnostics = []

# ----------------------------
# 📤 POST: Salvar diagnóstico
# ----------------------------
@router.post("/diagnostic/save")
def salvar_diagnostico(registro: DiagnosticRecord, user: str = Depends(get_current_user)):
    db_diagnostics.append(registro)
    return {"status": "salvo"}

# ----------------------------
# 📥 GET: Histórico completo
# ----------------------------
@router.get("/diagnostic/history", response_model=List[DiagnosticRecord])
def listar_diagnosticos(user: str = Depends(get_current_user)):
    return db_diagnostics
