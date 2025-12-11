# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\leadership_service.py
# Última atualização: 2025-12-11T09:59:21.105108

# -*- coding: utf-8 -*-
"""
leadership_service.py
---------------------

Avalia potencial de liderança com base em:

- estabilidade emocional
- tomada de decisão
- visão estratégica
- impacto social
- autoconsciência

Usado em relatórios executivos e premium.
"""

from typing import Dict, Any


class LeadershipService:

    def __init__(self, payload: Dict[str, Any]):
        self.payload = payload
        self.results = payload.get("results", {})
        self.traits = self.results.get("traits", {})
        self.emotional = self.results.get("emotional", {})
        self.performance = self.results.get("performance", {})

    def compute_scores(self) -> Dict[str, int]:
        return {
            "visao_estrategica": int((self.traits.get("openness", 50) * 0.6)
                                     + (self.performance.get("learning_speed", 50) * 0.4)),
            "estabilidade_emocional": self.emotional.get("emotional_stability", 50),
            "impacto_social": self.traits.get("extraversion", 50),
            "confiabilidade": self.traits.get("conscientiousness", 50),
        }

    def classify_level(self, score: int) -> str:
        if score >= 70:
            return "Alto potencial"
        if score >= 50:
            return "Potencial moderado"
        return "Potencial reduzido"

    def build(self) -> Dict[str, Any]:
        scores = self.compute_scores()
        avg = int(sum(scores.values()) / len(scores))
        return {
            "scores_lideranca": scores,
            "nivel_geral": self.classify_level(avg),
        }
