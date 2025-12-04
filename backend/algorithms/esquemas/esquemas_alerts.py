"""
Esquemas Alerts
Aponta esquemas disfuncionais elevados com base em thresholds padronizados.
"""

from typing import Dict, List


class EsquemasAlerts:
    """
    Gera bandeiras de risco segundo a literatura de Esquemas de Young.
    """

    def __init__(self):
        self.version = "1.0"
        self.threshold = 70

    def detect(self, classified: Dict[str, float]) -> List[str]:
        alerts = []
        for schema, value in classified.items():
            if value >= self.threshold:
                alerts.append(
                    f"Risco elevado no esquema '{schema}' (valor {value})."
                )
        return alerts
