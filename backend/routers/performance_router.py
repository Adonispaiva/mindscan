# ===============================================================
#  ROTEADOR: PERFORMANCE ROUTER
#  Projeto: MindScan — SynMind MI v2.0
#  Autor: Leo Vinci (GPT Inovexa)
#  Data: 07/11/2025
#  Função: Endpoint REST para cálculo de performance e quadrante
# ===============================================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from backend.modules.performance_matcher import calcular_matcher, gerar_analise_performance

router = APIRouter(prefix="/performance", tags=["Performance Matcher"])

# ---------------------------------------------------------------
# Modelo de entrada
# ---------------------------------------------------------------
class PerformanceRequest(BaseModel):
    excelencia: float = Field(..., ge=0, le=100, description="Nível de excelência pessoal (0–100)")
    faturamento: float = Field(..., ge=0, le=100, description="Nível de entrega/resultados (0–100)")
    scores: dict = Field(..., description="Pontuações DASS-21 (DEPRESSAO, ANSIEDADE, ESTRESSE)")

# ---------------------------------------------------------------
# Endpoint principal: POST /performance/analyze
# ---------------------------------------------------------------
@router.post("/analyze")
async def analyze_performance(payload: PerformanceRequest):
    """
    Analisa indicadores de excelência, faturamento e fatores emocionais
    para determinar o quadrante da Bússola SynMind.
    """
    try:
        resultados = calcular_matcher(payload.dict())
        analise = gerar_analise_performance(resultados)

        return {
            "status": "success",
            "quadrante": resultados["quadrante"],
            "score_performance": resultados["score_performance"],
            "comentario": resultados["comentario"],
            "analise_textual": analise
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na análise de performance: {str(e)}")
