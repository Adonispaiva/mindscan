# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\pipelines\mindscan_pipeline.py
# Última atualização: 2025-12-11T09:59:21.058152

"""
mindscan_pipeline.py — NÚCLEO ULTRA SUPERIOR DO MINDSCAN
Pipeline oficial que controla:

- Normalização total
- Integração cognitiva
- Extração de insights centrais
- Mapeamento emocional
- Scoring estrutural
- Riscos
- Resumo executivo final
"""

from engine.validation_engine import ValidationEngine
from engine.normalizer_engine import NormalizerEngine
from engine.integration_engine import IntegrationEngine
from engine.insight_engine import InsightEngine
from engine.risk_engine import RiskEngine
from engine.scoring_engine import ScoringEngine
from engine.summary_engine import SummaryEngine


class MindScanPipeline:
    def __init__(self):
        self.validator = ValidationEngine()
        self.normalizer = NormalizerEngine()
        self.integrator = IntegrationEngine()
        self.insight = InsightEngine()
        self.risk = RiskEngine()
        self.scorer = ScoringEngine()
        self.summarizer = SummaryEngine()

    def run(self, payload: dict) -> dict:
        self.validator.validate_input(payload)

        normalized = self.normalizer.normalize(payload)
        integrated = self.integrator.integrate(normalized)
        insights = self.insight.extract_insights(integrated)
        risks = self.risk.evaluate(integrated)
        scores = self.scorer.compute_score(integrated)

        summary = self.summarizer.generate_summary(
            integrated,
            model="mindscan",
            density="ultra",
            include_insights=True,
            include_risks=True,
            include_behavior_predictions=True
        )

        return {
            "normalized": normalized,
            "integrated": integrated,
            "insights": insights,
            "risks": risks,
            "scores": scores,
            "summary": summary
        }
