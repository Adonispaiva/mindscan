# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\roadmap_service.py
# Última atualização: 2025-12-11T09:59:21.120711

# -*- coding: utf-8 -*-
"""
roadmap_service.py
------------------

Gera o roadmap de desenvolvimento baseado nos insights, desempenho
e riscos identificados no MindScan.

O roadmap alimenta:
- PDI
- seções PDF
- relatórios premium
- módulos de desenvolvimento corporativo
"""

from typing import Dict, Any, List


class RoadmapService:

    def __init__(self, payload: Dict[str, Any]):
        self.payload = payload
        self.insights: List[str] = payload.get("insights", [])
        self.performance = payload.get("results", {}).get("performance", {})

    def build_action_items(self) -> List[str]:
        actions = []

        if self.performance.get("focus", 50) < 45:
            actions.append("Desenvolver técnicas de foco prolongado e gestão de atenção.")

        if any("ansiedade" in i.lower() for i in self.insights):
            actions.append("Implementar estratégias de regulação emocional e redução de ansiedade.")

        if any("conflito" in i.lower() for i in self.insights):
            actions.append("Praticar habilidades de comunicação assertiva para redução de conflitos.")

        if not actions:
            actions.append("Manter plano atual de desenvolvimento, com acompanhamento trimestral.")

        return actions

    def build(self) -> Dict[str, Any]:
        return {
            "roadmap": self.build_action_items(),
            "nivel_recomendado": "Moderado",
            "frequencia_revisao": "Trimestral",
        }
