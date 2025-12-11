# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\dass\dass_alerts.py
# Última atualização: 2025-12-11T09:59:20.652172

"""
DASS – ALERT ENGINE (Versão ULTRA SUPERIOR)
Gera alertas estruturados a partir das combinações de sintomas,
escores brutos e padrões de risco detectados pelo módulo DASS.
"""

from typing import Dict, List


class DASSAlerts:
    """
    Sistema avançado de alertas do DASS (legado).
    Totalmente compatível com DASS21 e motores híbridos.
    """

    ALERT_RULES = {
        "stress_high": {
            "threshold": 75,
            "message": "Níveis muito elevados de estresse detectados.",
            "recommendations": [
                "Aplicar protocolos de regulação autonômica.",
                "Avaliar gatilhos recentes.",
                "Considerar plano de intervenção orientado."
            ]
        },
        "anxiety_high": {
            "threshold": 70,
            "message": "Marcadores de ansiedade acima do esperado.",
            "recommendations": [
                "Monitorar padrões de antecipação negativa.",
                "Aplicar técnicas de respiração diafragmática.",
            ]
        },
        "depression_high": {
            "threshold": 65,
            "message": "Indicadores sugestivos de humor deprimido significativo.",
            "recommendations": [
                "Verificar perda de interesse / anedonia.",
                "Aplicar protocolo de ativação comportamental.",
            ]
        }
    }

    def generate(self, scores: Dict[str, float]) -> List[Dict]:
        """
        Produz alertas baseados nos escores do DASS (legado).
        :param scores: dict com scores {'stress': X, 'anxiety': Y, 'depression': Z}
        """
        results = []

        for key, rule in self.ALERT_RULES.items():
            domain = key.split("_")[0]
            score = scores.get(domain, 0)

            if score >= rule["threshold"]:
                results.append({
                    "domain": domain,
                    "score": score,
                    "alert": rule["message"],
                    "recommendations": rule["recommendations"]
                })

        return results
