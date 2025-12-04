"""
DASS – RISK FLAGS (Versão ULTRA SUPERIOR)
Gera bandeiras de risco escalonadas (verde → amarelo → vermelho)
para motores preditivos.
"""

from typing import Dict


class DASSRiskFlags:

    RISK_LEVELS = {
        "green": (0, 39),
        "yellow": (40, 59),
        "orange": (60, 74),
        "red": (75, 100)
    }

    def classify(self, scores: Dict[str, float]) -> Dict[str, str]:
        """
        Classifica risco em cada domínio.
        :return dict ex: {"stress": "red", "anxiety": "yellow"}
        """
        result = {}

        for domain, value in scores.items():
            flag = "green"

            for label, (low, high) in self.RISK_LEVELS.items():
                if low <= value <= high:
                    flag = label
                    break

            result[domain] = flag

        return result
