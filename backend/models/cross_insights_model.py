# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\cross_insights_model.py
# Última atualização: 2025-12-11T09:59:20.948776

# cross_insights_model.py
# MindScan Rebuild – Modelo de Insights Cruzados
# Versão Definitiva • Estrutura Avançada Pydantic-Style
# Autor: Leo Vinci — IA Supervisora Inovexa
# -------------------------------------------------------------------------
# Este arquivo padroniza a estrutura dos insights gerados pelo módulo
# cross_insights.py, garantindo:
#   - tipagem forte
#   - validação completa
#   - representação determinística
#   - compatibilidade total com mindscan_result.py
#   - utilização direta pelo Diagnostic Engine
# -------------------------------------------------------------------------

from dataclasses import dataclass, field
from typing import List, Dict, Any
import datetime


class ValidationError(Exception):
    pass


def require(condition: bool, message: str):
    if not condition:
        raise ValidationError(message)


@dataclass
class CrossInsight:
    """Representa um insight individual."""

    message: str
    tags: List[str] = field(default_factory=list)
    weight: float = 1.0  # futuro uso no Kernel

    def __post_init__(self):
        require(isinstance(self.message, str) and len(self.message) > 0,
                "Insight precisa ter uma mensagem válida.")
        require(isinstance(self.tags, list),
                "tags deve ser uma lista.")
        require(isinstance(self.weight, (int, float)),
                "weight deve ser numérico.")


@dataclass
class CrossInsightsModel:
    """
    Modelo final que encapsula o conjunto de insights cruzados
    gerados pelo módulo cross_insights.py
    """

    insights: List[CrossInsight]
    count: int
    generated_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

    def __post_init__(self):
        require(isinstance(self.insights, list),
                "insights deve ser uma lista de CrossInsight.")
        require(all(isinstance(i, CrossInsight) for i in self.insights),
                "todos os itens em insights devem ser CrossInsight.")
        require(isinstance(self.count, int) and self.count >= 0,
                "count deve ser inteiro >= 0.")
        require(isinstance(self.generated_at, str) and len(self.generated_at) > 0,
                "generated_at inválido.")

    # ---------------------------------------------------------------
    # Conversão para dict — formato final utilizado pelo sistema
    # ---------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        return {
            "insights": [
                {"message": i.message, "tags": i.tags, "weight": i.weight}
                for i in self.insights
            ],
            "count": self.count,
            "generated_at": self.generated_at
        }

    def summary(self) -> Dict[str, Any]:
        return {
            "count": self.count,
            "preview": [i.message for i in self.insights[:3]]
        }
