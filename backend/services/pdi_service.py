# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdi_service.py
# Última atualização: 2025-12-11T09:59:21.105108

# -*- coding: utf-8 -*-
"""
pdi_service.py
--------------

Serviço responsável por gerar o PDI (Plano de Desenvolvimento Individual)
com base nos insights, roadmap, competências e perfil geral do MindScan.

Integra:
- insights emocionais
- riscos
- pontos fortes
- roadmap_service
- performance
"""

from typing import Dict, Any, List

class PDIService:

    def __init__(self, payload: Dict[str, Any]):
        self.payload = payload
        self.insights: List[str] = payload.get("insights", [])
        self.roadmap: Dict[str, Any] = payload.get("roadmap", {})
        self.performance = payload.get("results", {}).get("performance", {})

    def build_focus_areas(self) -> List[str]:
        areas = []

        if any("ansiedade" in i.lower() for i in self.insights):
            areas.append("Regulação emocional e manejo de ansiedade.")

        if self.performance.get("focus", 50) < 50:
            areas.append("Aprimorar foco e gestão da atenção.")

        if any("conflito" in i.lower() for i in self.insights):
            areas.append("Desenvolver comunicação assertiva e escuta ativa.")

        if not areas:
            areas.append("Manter plano atual, com foco em consolidação de pontos fortes.")

        return areas

    def build_actions(self) -> List[str]:
        """
        Ações práticas de desenvolvimento.
        """
        actions = []

        if any("estresse" in i.lower() for i in self.insights):
            actions.append("Praticar técnicas de respiração e mindfulness diariamente.")

        if self.performance.get("learning_speed", 50) > 60:
            actions.append("Aproveitar ritmo acelerado de aprendizado para cursos intensivos.")

        if not actions:
            actions.append("Participar de workshops trimestrais de atualização profissional.")

        return actions

    def build(self) -> Dict[str, Any]:
        return {
            "areas_foco": self.build_focus_areas(),
            "acoes_desenvolvimento": self.build_actions(),
            "periodo_recomendado": "90 dias",
        }
