"""
Bússola Alerts — Versão Ultra Superior
--------------------------------------------------------

Gera alertas comportamentais baseados nos vetores da Bússola:
- Excesso de foco
- Excessiva dispersão
- Orientação polarizada
- Fragilidade em eixos críticos
"""

from typing import Dict, List


class BussolaAlerts:
    def __init__(self):
        self.version = "2.0-ultra"

    def generate(self, vectors: Dict[str, float]) -> List[str]:
        alerts = []

        north = vectors.get("norte", 0)
        south = vectors.get("sul", 0)
        east = vectors.get("leste", 0)
        west = vectors.get("oeste", 0)

        # Polarização Norte-Sul
        if abs(north - south) >= 40:
            alerts.append("Polarização significativa no eixo Norte–Sul.")

        # Polarização Leste-Oeste
        if abs(east - west) >= 40:
            alerts.append("Polarização significativa no eixo Leste–Oeste.")

        # Excesso de direção dominante
        dominant = max(vectors.values())
        if dominant >= 80:
            alerts.append("Uma direção está excessivamente dominante no perfil.")

        # Fragilidade
        if min(vectors.values()) <= 20:
            alerts.append("Uma direção apresenta fragilidade crítica.")

        return alerts
