# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\performance_service.py
# Última atualização: 2025-12-11T09:59:21.105108

# -*- coding: utf-8 -*-
"""
performance_service.py
----------------------

Serviço responsável por interpretar fatores de performance cognitiva
e comportamental do MindScan.

Gera indicadores usados por:
- RoadmapService
- PDIService
- Renderers técnicos
"""

from typing import Dict, Any

class PerformanceService:

    def __init__(self, payload: Dict[str, Any]):
        self.payload = payload
        self.results = payload.get("results", {})
        self.performance = self.results.get("performance", {})

    def compute_productivity_index(self) -> int:
        """
        Índice simplificado de produtividade.
        """
        focus = self.performance.get("focus", 50)
        learning = self.performance.get("learning_speed", 50)
        resilience = self.performance.get("resilience", 50)

        return int((focus * 0.4) + (learning * 0.3) + (resilience * 0.3))

    def compute_stress_index(self) -> int:
        stress = self.performance.get("stress", 50)
        stability = self.performance.get("emotional_stability", 50)
        return int((stress * 0.6) + (100 - stability) * 0.4)

    def build(self) -> Dict[str, Any]:
        return {
            "productivity_index": self.compute_productivity_index(),
            "stress_index": self.compute_stress_index(),
        }
