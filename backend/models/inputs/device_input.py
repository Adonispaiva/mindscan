# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\inputs\device_input.py
# Última atualização: 2025-12-11T09:59:20.995650

from __future__ import annotations

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class DeviceInput(BaseModel):
    """
    Informações do dispositivo e contexto técnico da aplicação
    (opcional, mas útil para auditoria e análises de confiabilidade).

    Não participa diretamente dos algoritmos psicométricos,
    mas permite rastrear problemas de coleta e padronizar avaliações.
    """

    candidate_id: str = Field(..., description="ID único do candidato.")
    session_id: Optional[str] = Field(default=None)

    device_type: Optional[str] = Field(
        default=None,
        description="Tipo de dispositivo: desktop, mobile, tablet, etc."
    )
    os: Optional[str] = Field(default=None, description="Sistema operacional.")
    browser: Optional[str] = Field(default=None, description="Navegador utilizado.")
    screen_resolution: Optional[str] = Field(
        default=None, description="Resolução da tela no momento da aplicação."
    )
    network_quality: Optional[str] = Field(
        default=None,
        description="Qualidade estimada da conexão (opcional)."
    )

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_algorithm_payload(self) -> Dict[str, Any]:
        """
        Usado por engines de auditoria e estimadores de confiabilidade
        no backend (ex.: device_sanity_engine.py).
        """
        return self.dict()
