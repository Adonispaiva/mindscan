from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict

class CandidateInput(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    role: str = "Candidato"
    # Respostas cruas (1-5 ou 0-3)
    big5_responses: List[int] = Field(..., min_items=20, max_items=50) 
    dass21_responses: List[int] = Field(..., min_items=21, max_items=21)
    
class DiagnosticResult(BaseModel):
    user_id: str
    timestamp: str
    big5: Dict[str, float]       # Scores percentuais
    dass21: Dict[str, Any]       # Scores e Classificações
    bussula: Dict[str, str]      # Quadrante
    match_score: float           # 0 a 100% (MindMatch)
    competencias: Dict[str, float] # Competências derivadas
    metadata: Dict[str, Any]