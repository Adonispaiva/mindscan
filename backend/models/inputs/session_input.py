# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\inputs\session_input.py
# Última atualização: 2025-12-11T09:59:21.011277

from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class SessionInput(BaseModel):
    """
    Entrada de sessão utilizada em qualquer execução MindScan.
    """

    session_id: str = Field(..., description="ID único da sessão.")
    candidate_id: str = Field(..., description="ID do candidato.")
    timestamp: Optional[str] = Field(None, description="Horário ISO da sessão.")
    metadata: Optional[Dict[str, Any]] = Field(default=None)
