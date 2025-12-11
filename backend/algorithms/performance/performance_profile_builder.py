# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\performance\performance_profile_builder.py
# Última atualização: 2025-12-11T09:59:20.714601

"""
Performance Profile Builder
Constrói o perfil profissional consolidado a partir das dimensões de performance.
"""

from typing import Dict, Any

from .performance_crosslinks import PerformanceCrosslinks
from .performance_strengths import PerformanceStrengths
from .performance_risk_map import PerformanceRiskMap
from .performance_insights import PerformanceInsights


class PerformanceProfileBuilder:
    def __init__(self):
        self.version = "1.0"

        self.cross = PerformanceCrosslinks()
        self.strengths_engine = PerformanceStrengths()
        self.risks_engine = PerformanceRiskMap()
        self.insights_engine = PerformanceInsights()

    def build(self, dims: Dict[str, float]) -> Dict[str, Any]:
        strengths = self.strengths_engine.extract(dims)
        risks = self.risks_engine.map(dims)
        insights = self.insights_engine.generate(dims)
        crosslinks = self.cross.generate(dims)

        top = max(dims, key=dims.get) if dims else None

        return {
            "module": "Performance",
            "version": self.version,
            "dimensions": dims,
            "strengths": strengths,
            "risks": risks,
            "insights": insights,
            "crosslinks": crosslinks["crosslinks"],
            "top_dimension": top,
        }
