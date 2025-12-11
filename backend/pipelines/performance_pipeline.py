# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\pipelines\performance_pipeline.py
# Última atualização: 2025-12-11T09:59:21.058152

"""
performance_pipeline.py — Performance Cognitiva e Operacional
Avaliação profunda do desempenho humano em contextos:

- Produtividade
- Tomada de decisão
- Foco e consistência
- Velocidade cognitiva
- Estabilidade emocional sob carga
"""

from engine.validation_engine import ValidationEngine
from engine.normalizer_engine import NormalizerEngine
from engine.scoring_engine import ScoringEngine
from engine.insight_engine import InsightEngine
from engine.summary_engine import SummaryEngine


class PerformancePipeline:
    def __init__(self):
        self.validator = ValidationEngine()
        self.normalizer = NormalizerEngine()
        self.scorer = ScoringEngine()
        self.insight = InsightEngine()
        self.summarizer = SummaryEngine()

    def run(self, payload: dict) -> dict:
        self.validator.validate_input(payload)

        normalized = self.normalizer.normalize(payload)
        performance_scores = self.scorer.compute_score(normalized, mode="performance")
        insights = self.insight.extract_insights(normalized)

        summary = self.summarizer.generate_summary(
            performance_scores,
            model="performance",
            density="ultra",
            include_insights=True,
            include_efficiency=True,
            include_resilience_index=True
        )

        return {
            "normalized": normalized,
            "scores": performance_scores,
            "insights": insights,
            "summary": summary
        }
