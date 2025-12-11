# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\pipelines\cross_pipeline.py
# Última atualização: 2025-12-11T09:59:21.058152

"""
cross_pipeline.py — MindScan Cross-Analysis
Pipeline de integração multidimensional que cruza traços, riscos, padrões,
sentenças, mapas cognitivos e variáveis contextuais.

Produce:
- Correlações profundas
- Sinais ocultos
- Padrões de convergência/divergência
- Insights acionáveis

Padrão ULTRA: máxima densidade de análise.
"""

from engine.integration_engine import IntegrationEngine
from engine.scoring_engine import ScoringEngine
from engine.summary_engine import SummaryEngine
from engine.validation_engine import ValidationEngine


class CrossPipeline:
    def __init__(self):
        self.integration = IntegrationEngine()
        self.scorer = ScoringEngine()
        self.summarizer = SummaryEngine()
        self.validator = ValidationEngine()

    def run(self, payload: dict) -> dict:
        self.validator.validate_input(payload)

        integrated = self.integration.integrate(payload)

        scores = self.scorer.compute_score(integrated)

        summary = self.summarizer.generate_summary(
            integrated,
            model="cross",
            density="ultra",
            include_cross_signals=True
        )

        return {
            "integrated": integrated,
            "scores": scores,
            "summary": summary
        }
