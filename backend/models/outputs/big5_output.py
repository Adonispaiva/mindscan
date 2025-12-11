# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\outputs\big5_output.py
# Última atualização: 2025-12-11T09:59:21.011277

from __future__ import annotations

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class Big5Output(BaseModel):
    """
    Representa o resultado final do módulo Big Five no MindScan.
    Inclui scores fatoriais normalizados, interpretações automáticas
    e eventuais observações relevantes para o relatório.
    """

    candidate_id: str = Field(..., description="ID único do candidato.")
    session_id: Optional[str] = Field(default=None)

    # Fatores centrais O, C, E, A, N
    scores: Dict[str, float] = Field(
        default_factory=dict,
        description="Mapa dos cinco fatores principais."
    )

    # Interpretações geradas após engines e cruzamentos
    interpretations: Dict[str, str] = Field(
        default_factory=dict,
        description="Interpretações individuais de cada fator."
    )

    # Observações resumidas para o relatório
    summary: Optional[str] = Field(
        default=None,
        description="Resumo textual da personalidade Big Five."
    )

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_report_payload(self) -> Dict[str, Any]:
        return self.dict()
