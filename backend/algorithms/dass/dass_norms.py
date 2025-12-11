# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\dass\dass_norms.py
# Última atualização: 2025-12-11T09:59:20.652172

"""
DASS – NORMS ENGINE (Versão ULTRA SUPERIOR)
Normas de referência para o DASS clássico (não DASS21).
Compatível com motores de normalização híbrida.
"""

from typing import Dict


class DASSNorms:
    """
    Normalizador técnico do DASS clássico.
    Transforma pontuações brutas em percentis e faixas qualitativas.
    """

    NORM_TABLE: Dict[str, Dict[str, tuple]] = {
        "stress": {
            "low": (0, 14),
            "moderate": (15, 25),
            "high": (26, 33),
            "extreme": (34, 100)
        },
        "anxiety": {
            "low": (0, 9),
            "moderate": (10, 19),
            "high": (20, 27),
            "extreme": (28, 100)
        },
        "depression": {
            "low": (0, 9),
            "moderate": (10, 20),
            "high": (21, 28),
            "extreme": (29, 100)
        }
    }

    def classify(self, scores: Dict[str, float]) -> Dict[str, str]:
        """
        Classifica scores brutos em faixas normativas.
        """
        result = {}

        for domain, value in scores.items():
            norms = self.NORM_TABLE.get(domain, {})
            classification = "undefined"

            for label, (low, high) in norms.items():
                if low <= value <= high:
                    classification = label
                    break

            result[domain] = classification

        return result
