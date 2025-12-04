"""
Performance — Núcleo de Avaliação de Performance Profissional
Integra normas, dimensões, alertas, riscos, forças, insights e previsão.
"""

from typing import Dict, Any

from .performance_norms import PerformanceNorms
from .performance_dimensions import PerformanceDimensions
from .performance_insights import PerformanceInsights
from .performance_alerts import PerformanceAlerts
from .performance_risk_map import PerformanceRiskMap
from .performance_strengths import PerformanceStrengths
from .performance_predictor import PerformancePredictor
from .performance_output_formatter import PerformanceOutputFormatter
from .performance_summary import PerformanceSummary
from .performance_validation import PerformanceValidation


class Performance:
    def __init__(self):
        self.norms = PerformanceNorms()
        self.dimensions = PerformanceDimensions()
        self.insights = PerformanceInsights()
        self.alerts = PerformanceAlerts()
        self.risks = PerformanceRiskMap()
        self.strengths = PerformanceStrengths()
        self.predictor = PerformancePredictor()
        self.formatter = PerformanceOutputFormatter()
        self.summary_engine = PerformanceSummary()
        self.validation = PerformanceValidation()

    def run(self, raw_scores: Dict[str, float]) -> Dict[str, Any]:
        if not self.validation.validate_raw(raw_scores):
            return {"error": "Invalid performance raw scores"}

        normalized = self.norms.normalize(raw_scores)

        dims = self.dimensions.compute(normalized)

        insights = self.insights.generate(dims)
        alerts = self.alerts.generate(dims)
        risks = self.risks.map(dims)
        strengths = self.strengths.extract(dims)
        prediction = self.predictor.predict(dims)
        summary = self.summary_engine.summarize(dims)

        formatted = self.formatter.format(
            dims=dims,
            insights=insights,
            alerts=alerts,
            risks=risks,
            strengths=strengths,
            prediction=prediction,
        )

        formatted["summary"] = summary

        return formatted
