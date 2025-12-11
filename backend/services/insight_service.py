# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\insight_service.py
# Última atualização: 2025-12-11T09:59:21.105108

# -*- coding: utf-8 -*-
"""
insight_service.py
------------------

Serviço central de geração de insights.
Integra outputs das diversas engines do MindScan
(Big Five, TEIQue, DASS, Esquemas, Bussola, Performance, etc.)
e produz insights estruturados para consumo do pipeline corporativo.

Este serviço é um dos pilares do sistema.
"""

from typing import Dict, Any, List


class InsightService:

    def __init__(self, payload: Dict[str, Any]):
        self.payload = payload
        self.results = payload.get("results", {})

    # --------------------------------------------------------------
    # 1. INSIGHTS DE PERSONALIDADE
    # --------------------------------------------------------------
    def build_personality_insights(self) -> List[str]:
        bf = self.results.get("big_five", {})
        insights = []

        if bf.get("neuroticism_score", 50) < 40:
            insights.append("Tende a manter estabilidade emocional mesmo sob pressão.")
        if bf.get("extraversion_score", 50) > 60:
            insights.append("Demonstra energia social elevada e facilidade em interações humanas.")
        if bf.get("openness_score", 50) > 55:
            insights.append("Apresenta boa capacidade criativa e abertura a novas ideias.")
        if bf.get("agreeableness_score", 50) > 65:
            insights.append("Tende a cooperar e manter relacionamentos harmoniosos.")
        if bf.get("conscientiousness_score", 50) > 65:
            insights.append("Possui disciplina e comprometimento com padrões elevados de entrega.")

        return insights

    # --------------------------------------------------------------
    # 2. INSIGHTS EMOCIONAIS (TEIQue, DASS)
    # --------------------------------------------------------------
    def build_emotional_insights(self) -> List[str]:
        emotional = self.results.get("emotional", {})
        insights = []

        if emotional.get("stress_tolerance", 50) > 60:
            insights.append("Demonstra boa tolerância ao estresse e manejo emocional equilibrado.")
        if emotional.get("impulse_control", 50) > 60:
            insights.append("Capacidade de controle de impulsos acima da média.")
        if emotional.get("anxiety_level", 50) > 60:
            insights.append("Atenção: nível de ansiedade elevado pode exigir suporte contínuo.")

        return insights

    # --------------------------------------------------------------
    # 3. INSIGHTS DE RISCO
    # --------------------------------------------------------------
    def build_risk_insights(self) -> List[str]:
        risks = self.results.get("risks", {})
        insights = []

        if risks.get("burnout_risk", 20) > 50:
            insights.append("Indício de risco aumentado para burnout em longo prazo.")
        if risks.get("conflict_risk", 20) > 50:
            insights.append("Possível tendência a conflitos interpessoais em ambientes tensos.")

        return insights

    # --------------------------------------------------------------
    # 4. INSIGHTS DE PERFORMANCE
    # --------------------------------------------------------------
    def build_performance_insights(self) -> List[str]:
        perf = self.results.get("performance", {})
        insights = []

        if perf.get("focus", 50) > 65:
            insights.append("Alta capacidade de foco e atenção prolongada.")
        if perf.get("learning_speed", 50) > 60:
            insights.append("Aprendizagem acelerada e boa retenção de novos conteúdos.")

        return insights

    # --------------------------------------------------------------
    # 5. AGREGADOR FINAL
    # --------------------------------------------------------------
    def build(self) -> List[str]:
        return (
            self.build_personality_insights()
            + self.build_emotional_insights()
            + self.build_risk_insights()
            + self.build_performance_insights()
        )
