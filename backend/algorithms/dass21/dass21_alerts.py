# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\dass21\dass21_alerts.py
# Última atualização: 2025-12-11T09:59:20.652172

"""
DASS21 Alerts — Versão ULTRA SUPERIOR
-------------------------------------------------------------

Gera alertas clínicos a partir das pontuações:

- Depressão
- Ansiedade
- Estresse

O foco deste módulo é:
- identificar riscos emocionais imediatos
- fornecer alertas combinados
- sugerir hipóteses interpretativas
"""

from typing import Dict, List


class DASS21Alerts:
    def __init__(self):
        self.version = "2.0-ultra"

    def generate(self, scores: Dict[str, float]) -> List[str]:
        alerts = []

        dep = scores.get("depressao", 0)
        ans = scores.get("ansiedade", 0)
        st = scores.get("stress", 0)

        # Depressão crítica
        if dep >= 70:
            alerts.append("Depressão em nível crítico — risco de retraimento profundo.")

        # Ansiedade alta + estresse alto
        if ans >= 60 and st >= 60:
            alerts.append("Ansiedade e estresse simultaneamente elevados — risco de colapso emocional.")

        # Ansiedade com baixa regulação (inferida)
        if ans >= 55:
            alerts.append("Níveis elevados de ansiedade podem prejudicar o foco e a clareza.")

        # Estresse significativo
        if st >= 60:
            alerts.append("Estresse elevado podendo comprometer a capacidade de decisão.")

        return alerts
