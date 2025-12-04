"""
Performance Validation
Validação dos dados brutos e normalizados para o módulo Performance.
"""

from typing import Dict, Any


class PerformanceValidation:
    def __init__(self):
        self.version = "1.0"
        self.raw_min = 0
        self.raw_max = 10

    def validate_raw(self, raw_scores: Dict[str, Any]) -> bool:
        if not isinstance(raw_scores, dict):
            return False

        for k, v in raw_scores.items():
            if not isinstance(v, (int, float)):
                return False
            if not (self.raw_min <= v <= self.raw_max):
                return False

        return True

    def validate_normalized(self, normalized: Dict[str, float]) -> bool:
        for v in normalized.values():
            if not 0 <= v <= 100:
                return False

        return True
