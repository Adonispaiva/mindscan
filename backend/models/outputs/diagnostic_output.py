# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\outputs\diagnostic_output.py
# Última atualização: 2025-12-11T09:59:21.026903

from __future__ import_annotations

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class DiagnosticOutput(BaseModel):
    """
    Resultado integrado do diagnóstico MindScan.

    Este é o pacote final antes da geração do PDF,
    agregando outputs de todos os módulos:
    - Big Five
    - TEIQue
    - DASS
    - Esquemas
    - Bússola
    - Cognitivo
    - Performance
    - Cultura / OCAI
    - MI
    """

    candidate_id: str = Field(..., description="ID único do candidato.")
    session_id: Optional[str] = Field(default=None)

    modules: Dict[str, Any] = Field(
        default_factory=dict,
        description="Pacote consolidado com resultados finais por módulo."
    )

    summary: Optional[str] = Field(
        default=None,
        description="Resumo executivo integrado do diagnóstico."
    )

    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadados gerais, versão do modelo, runtime, etc."
    )

    def to_report_payload(self) -> Dict[str, Any]:
        return self.dict()
