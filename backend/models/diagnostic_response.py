from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class DiagnosticResponse(BaseModel):
    status: str = Field(..., description="Status da operação (ex: 'ok').")
    report_url: str = Field(..., description="URL ou caminho do PDF gerado.")
    
    # Resultados centrais
    insights: Optional[Dict[str, Any]] = Field(
        None, description="Insights gerados pelo motor MindScan."
    )
    profile: Optional[Dict[str, Any]] = Field(
        None, description="Perfil psicométrico consolidado."
    )
    scores: Optional[Dict[str, Any]] = Field(
        None, description="Pontuações brutas e normalizadas para cada instrumento."
    )
