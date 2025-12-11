# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\diagnostic_request.py
# Última atualização: 2025-12-11T09:59:20.948776

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class AnswerItem(BaseModel):
    question_id: str = Field(..., description="ID da pergunta psicométrica")
    value: Any = Field(..., description="Valor bruto da resposta")

class InstrumentSection(BaseModel):
    instrument: str = Field(..., description="Instrumento psicométrico: BIG5, TEIQue, OCAI, DASS21, etc.")
    answers: List[AnswerItem] = Field(..., description="Lista de respostas do instrumento")

class CandidateInfo(BaseModel):
    name: str
    email: Optional[str]
    age: Optional[int]
    gender: Optional[str]
    notes: Optional[str]

class DiagnosticRequest(BaseModel):
    candidate: CandidateInfo = Field(..., description="Dados pessoais do candidato")
    instruments: List[InstrumentSection] = Field(..., description="Lista de instrumentos preenchidos")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Metadados adicionais do diagnóstico")
