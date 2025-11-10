from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from analytics.diagnostic_engine import interpretar_dass21
from analytics.report_generator import gerar_relatorio_mi

router = APIRouter()

# -----------------------------
# 📥 MODELO DE ENTRADA
# -----------------------------
class DassInput(BaseModel):
    nome: str
    scores: dict  # Ex: {"DEPRESSAO": 6, "ANSIEDADE": 4, "ESTRESSE": 8}


# -----------------------------
# 🚀 ENDPOINT /diagnostic
# -----------------------------
@router.post("/diagnostic")
def gerar_diagnostico(payload: DassInput):
    try:
        resultado = interpretar_dass21(payload.scores)
        relatorio = gerar_relatorio_mi(resultado, nome=payload.nome)
        return {
            "nome": payload.nome,
            "resultado": resultado,
            "relatorio": relatorio
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
