# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\outputs\mi_output.py
# Última atualização: 2025-12-11T09:59:21.026903

from __future__ import annotations

from typing import Dict, Optional, Any
from pydantic import BaseModel, Field


class MIOutput(BaseModel):
    """
    Resultado final do módulo MI (Mente Interpretativa).

    A MI integra:
    - Big Five
    - TEIQue
    - DASS
    - Esquemas
    - Performance
    - Bússola
    - Cognitivo
    - Cultura / OCAI
    - Comportamento
    - Contexto
    """

    candidate_id: str = Field(..., description="ID do candidato.")
    session_id: Optional[str] = Field(default=None)

    persona: Optional[str] = Field(
        default=None,
        description="Arquetipo/tema interpretativo definido pela MI."
    )

    themes: Dict[str, str] = Field(
        default_factory=dict,
        description="Mapeamento de temas interpretativos centrais."
    )

    alerts: Dict[str, Any] = Field(
        default_factory=dict,
        description="Sinais críticos identificados pela MI."
    )

    summary: Optional[str] = Field(
        default=None,
        description="Resumo interpretativo principal."
    )

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_report_payload(self) -> Dict[str, Any]:
        return self.dict()
