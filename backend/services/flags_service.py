# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\flags_service.py
# Última atualização: 2025-12-11T09:59:21.105108

# -*- coding: utf-8 -*-
"""
flags_service.py
----------------

Serviço responsável por identificar "flags" psicológicas e comportamentais:
- sinais de risco
- padrões de atenção
- indicadores positivos

Essas flags são usadas por:
- resumo estratégico
- renderers executivos
- módulos de risco
"""

from typing import Dict, Any, List


class FlagsService:

    def __init__(self, payload: Dict[str, Any]):
        self.payload = payload
        self.results = payload.get("results", {})

    def detect_positive_flags(self) -> List[str]:
        flags = []
        traits = self.results.get("traits", {})
        performance = self.results.get("performance", {})

        if traits.get("conscientiousness", 50) > 65:
            flags.append("Alta organização e confiabilidade.")
        if performance.get("learning_speed", 50) > 60:
            flags.append("Aprendiz rápido e adaptável.")
        if traits.get("agreeableness", 50) > 60:
            flags.append("Boa capacidade de colaboração.")

        return flags

    def detect_risk_flags(self) -> List[str]:
        flags = []
        emotional = self.results.get("emotional", {})
        risks = self.results.get("risks", {})

        if emotional.get("anxiety_level", 40) > 60:
            flags.append("Atenção: sinais elevados de ansiedade.")
        if risks.get("burnout_risk", 20) > 50:
            flags.append("Indicativo de risco de burnout.")
        if risks.get("conflict_risk", 20) > 50:
            flags.append("Propensão a conflitos em ambientes de pressão.")

        return flags

    def build(self) -> Dict[str, Any]:
        return {
            "flags_positivas": self.detect_positive_flags(),
            "flags_risco": self.detect_risk_flags()
        }
