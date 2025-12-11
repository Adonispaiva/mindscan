# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\performance\performance_alerts.py
# Última atualização: 2025-12-11T09:59:20.698978

"""
Performance Alerts
Gera alertas com base em padrões críticos nas dimensões de performance.
"""

from typing import Dict, List


class PerformanceAlerts:
    """
    Detecta sinais de risco em produtividade, execução, autonomia e consistência.
    """

    def __init__(self):
        self.version = "1.0"
        self.threshold = 75  # valores normalizados (0–100)

    def generate(self, dims: Dict[str, float]) -> List[str]:
        alerts = []

        for k, v in dims.items():
            if v >= self.threshold:
                alerts.append(f"Risco alto detectado na dimensão '{k}' (valor {v}).")

        return alerts
