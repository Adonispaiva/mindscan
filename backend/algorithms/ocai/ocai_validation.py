# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\ocai\ocai_validation.py
# Última atualização: 2025-12-11T09:59:20.698978

"""
OCAI Validation
Valida entradas brutas e normalizadas do instrumento OCAI.
"""

from typing import Dict, Any


class OCAIValidation:
    """
    Regras simples de validação para garantir consistência
    antes da normalização e do cálculo das dimensões.
    """

    def __init__(self):
        self.version = "1.0"
        self.allowed_range = (0, 10)

    def validate_raw(self, raw_scores: Dict[str, Any]) -> bool:
        if not isinstance(raw_scores, dict):
            return False

        for key, value in raw_scores.items():
            if not isinstance(value, (int, float)):
                return False

            if not (self.allowed_range[0] <= value <= self.allowed_range[1]):
                return False

        return True

    def validate_normalized(self, normalized: Dict[str, float]) -> bool:
        for value in normalized.values():
            if not 0 <= value <= 100:
                return False
        return True
