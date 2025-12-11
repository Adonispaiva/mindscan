# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\dass\dass_factor_map.py
# Última atualização: 2025-12-11T09:59:20.652172

"""
DASS – FACTOR MAP (Versão ULTRA SUPERIOR)
Mapeamento técnico dos fatores do DASS clássico (stress, anxiety, depression)
com pesos, itens e vínculos para motores compostos e análises híbridas.
"""

from typing import Dict, List


class DASSFactorMap:
    """
    Oferece estrutura de fatores e pesos do DASS (LEGADO).
    Totalmente compatível com DASS21, sem substituí-lo.
    """

    FACTOR_STRUCTURE: Dict[str, Dict] = {
        "stress": {
            "weight": 1.20,
            "items": [
                "difficulty_relaxing",
                "nervous_arousal",
                "irritability_frustration",
                "easily_agitated"
            ],
            "description": "Reflete tensão fisiológica e hiperativação do sistema de stress."
        },
        "anxiety": {
            "weight": 1.15,
            "items": [
                "fear_sensation",
                "panic_indicators",
                "anticipatory_tension",
                "somatic_activation"
            ],
            "description": "Reflete inclinação a respostas de ansiedade e hipervigilância."
        },
        "depression": {
            "weight": 1.25,
            "items": [
                "low_positive_affect",
                "hopelessness",
                "self_criticism",
                "anhedonia"
            ],
            "description": "Representa padrões de humor deprimido e perda de interesse."
        }
    }

    def get_factor_map(self) -> Dict[str, Dict]:
        """
        Retorna o mapa completo de fatores e seus metadados.
        """
        return self.FACTOR_STRUCTURE

    def weighted_scores(self, raw_scores: Dict[str, float]) -> Dict[str, float]:
        """
        Aplica pesos técnicos aos scores brutos.
        """
        result = {}
        for factor, data in self.FACTOR_STRUCTURE.items():
            weight = data["weight"]
            value = raw_scores.get(factor, 0)
            result[factor] = round(value * weight, 2)
        return result
