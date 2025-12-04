"""
OCAI Alerts
Detecta riscos culturais predominantes na organização.
"""

from typing import Dict, List


class OCAIAlerts:
    """
    Bandeiras de alerta para cada eixo cultural.
    """

    def __init__(self):
        self.version = "1.0"
        self.threshold = 75

    def detect(self, profile: Dict[str, float]) -> List[str]:
        alerts = []

        for dim, val in profile.items():
            if val >= self.threshold:
                alerts.append(
                    f"Risco cultural elevado em '{dim}' (valor {val})."
                )

        return alerts
