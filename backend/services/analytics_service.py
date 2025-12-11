# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\analytics_service.py
# Última atualização: 2025-12-11T09:59:21.089476

# -*- coding: utf-8 -*-
"""
analytics_service.py
--------------------

Camada analítica do MindScan.
Responsável por consolidar indicadores globais, médias,
percentis e métricas de interpretação estendida.

Base para:
- dashboards futuros
- relatórios avançados
- comparações normativas
"""

from typing import Dict, Any


class AnalyticsService:

    def __init__(self, payload: Dict[str, Any]):
        self.payload = payload
        self.results = payload.get("results", {})
        self.traits = self.results.get("traits", {})
        self.performance = self.results.get("performance", {})

    def build_global_indicator(self) -> int:
        """
        Índice geral de adaptabilidade/produtividade,
        usado como resumo matemático do perfil.
        """
        openness = self.traits.get("openness", 50)
        conscientious = self.traits.get("conscientiousness", 50)
        focus = self.performance.get("focus", 50)

        return int((openness * 0.3) + (conscientious * 0.4) + (focus * 0.3))

    def build_dimension_summary(self) -> Dict[str, int]:
        """
        Retorna somas simplificadas para leitura rápida.
        """
        return {
            "criatividade": self.traits.get("openness", 50),
            "organizacao": self.traits.get("conscientiousness", 50),
            "energia": self.traits.get("extraversion", 50),
            "estabilidade": self.traits.get("emotional_stability", 50),
        }

    def build(self) -> Dict[str, Any]:
        return {
            "indice_global": self.build_global_indicator(),
            "dimensoes_resumo": self.build_dimension_summary(),
        }
