# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\report\builders\psychodynamic_builder.py
# Última atualização: 2025-12-11T09:59:21.276887

from backend.mi.mi_risk_detector import MIRiskDetector
from backend.mi.mi_narrative_polisher import MINarrativePolisher

class PsychodynamicBuilder:
    """
    Complementa relatórios psicodinâmicos com análise profunda.
    """

    @staticmethod
    def build(results: dict) -> dict:
        risks = MIRiskDetector.detect(results)
        narrative = f"Fatores psicodinâmicos detectados: {risks}"

        return {
            "deep_analysis": risks,
            "narrative": MINarrativePolisher.polish(narrative)
        }
