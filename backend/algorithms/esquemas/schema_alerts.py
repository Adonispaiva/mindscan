"""
Schema Alerts
Versão complementar de alertas, operando em nível de itens/dimensões.
"""

from typing import Dict, List


class SchemaAlerts:
    """
    Detecta alertas com base em itens individuais do questionário,
    complementando as bandeiras de risco dos esquemas finalizados.
    """

    def __init__(self):
        self.version = "1.0"
        self.threshold_item = 80  # valor já normalizado (0–100)

    def detect(self, normalized_items: Dict[str, float]) -> List[str]:
        alerts = []

        for item, value in normalized_items.items():
            if value >= self.threshold_item:
                alerts.append(
                    f"Alerta: item '{item}' apresenta intensidade elevada ({value})."
                )

        return alerts
