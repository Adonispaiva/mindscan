# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\inputs\user_profile.py
# Última atualização: 2025-12-11T09:59:21.011277

from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class UserProfileInput(BaseModel):
    """
    Dados opcionais de perfil que enriquecem o processamento MindScan.
    """

    candidate_id: str = Field(..., description="ID do candidato.")
    name: Optional[str] = Field(None)
    role: Optional[str] = Field(None)
    seniority: Optional[str] = Field(None)
    additional_data: Optional[Dict[str, Any]] = Field(default=None)
