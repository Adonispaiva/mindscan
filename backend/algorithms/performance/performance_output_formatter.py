"""
Performance Output Formatter
Gera o payload final da avaliação de performance profissional.
"""

from typing import Dict, Any


class PerformanceOutputFormatter:
    def __init__(self):
        self.version = "1.0"

    def format(self,
               dims: Dict[str, float],
               insights: Dict[str, str],
               alerts: Dict[str, str],
               risks: Dict[str, str],
               strengths: Dict[str, str],
               prediction: Dict[str, Any]) -> Dict[str, Any]:

        return {
            "module": "Performance",
            "version": self.version,
            "dimensions": dims,
            "insights": insights,
            "alerts": alerts,
            "risks": risks,
            "strengths": strengths,
            "prediction": prediction,
        }
