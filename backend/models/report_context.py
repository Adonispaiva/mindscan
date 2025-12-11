# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\report_context.py
# Última atualização: 2025-12-11T09:59:20.980027

# D:\backend\models\report_context.py
# Estrutura definitiva do contexto de relatório no MindScan — versão Inovexa Ultra

from typing import Any, Dict, Optional, List
from pydantic import BaseModel, Field, validator


class ReportContext(BaseModel):
    """
    O Contexto do Relatório é uma estrutura essencial para o MindScan:
    
    Ele agrega informações de topo e metadados globais usados pelos
    renderizadores para:
      - contextualizar o diagnóstico
      - carregar dados do usuário avaliado
      - referenciar scores, perfis e sínteses
      - adaptar narrativa
      - parametrizar estilos e blocos
    
    O contexto acompanha cada renderer durante a execução.
    """

    test_id: str = Field(..., description="Identificador único do teste do usuário.")
    user_name: Optional[str] = Field(
        None,
        description="Nome da pessoa avaliada (se permitido pelo cliente)."
    )
    user_metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Dados contextuais não sensíveis sobre o usuário."
    )
    global_scores: Dict[str, Any] = Field(
        default_factory=dict,
        description="Mapa consolidado de pontuações globais dos módulos MindScan."
    )
    global_insights: Dict[str, Any] = Field(
        default_factory=dict,
        description="Insights agregados de todos os módulos (BIG5, TEIQue, etc)."
    )
    risk_profile: Dict[str, Any] = Field(
        default_factory=dict,
        description="Mapa de riscos consolidados (todos os algoritmos)."
    )
    strength_profile: Dict[str, Any] = Field(
        default_factory=dict,
        description="Mapa de forças consolidadas."
    )
    culture_profile: Optional[Dict[str, Any]] = Field(
        None,
        description="Perfil cultural OCAI, se disponível."
    )
    performance_profile: Optional[Dict[str, Any]] = Field(
        None,
        description="Perfil de performance agregada."
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadados globais do relatório, incluindo flags internas."
    )
    style: Dict[str, Any] = Field(
        default_factory=dict,
        description="Estilos globais aplicáveis aos renderizadores."
    )

    @validator("test_id")
    def validate_test_id(cls, value):
        if not value or not isinstance(value, str):
            raise ValueError("O campo test_id é obrigatório e deve ser string.")
        if " " in value:
            raise ValueError("O campo test_id não pode conter espaços.")
        return value

    def to_dict(self) -> Dict[str, Any]:
        """
        Converte todo o contexto para um dict serializável,
        compatível com todos os renderers (technical, executive, etc).
        """
        return {
            "test_id": self.test_id,
            "user_name": self.user_name,
            "user_metadata": self.user_metadata,
            "global_scores": self.global_scores,
            "global_insights": self.global_insights,
            "risk_profile": self.risk_profile,
            "strength_profile": self.strength_profile,
            "culture_profile": self.culture_profile,
            "performance_profile": self.performance_profile,
            "metadata": self.metadata,
            "style": self.style,
        }
