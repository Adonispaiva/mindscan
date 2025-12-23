from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

from backend.algorithms.mindscan_engine import MindScanEngine
from backend.algorithms.matcher import MindMatcher
from backend.services.mi_service import MasterInsightService

router = APIRouter()

# Instâncias globais para performance
engine = MindScanEngine()
matcher = MindMatcher()
mi_service = MasterInsightService()

class DiagnosticRequest(BaseModel):
    user_id: str
    name: str
    big5_responses: List[int]
    dass21_responses: List[int]

@router.post("/process")
async def process_diagnostic(request: DiagnosticRequest):
    """
    Endpoint principal: Recebe respostas -> Calcula -> Retorna JSON completo.
    """
    try:
        # 1. Engine Psicométrica
        raw_results = engine.process_full_diagnostic(request.dict())
        
        # 2. Matcher
        match_score = matcher.calculate_match_score(raw_results['big5'])
        raw_results['scores_consolidated'] = {"performance": match_score}
        
        # 3. MI (Narrativa)
        narrative = mi_service.generate_narrative(raw_results)
        raw_results['narrative'] = narrative
        
        return {
            "status": "success",
            "data": raw_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))