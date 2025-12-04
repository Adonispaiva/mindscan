# MindScan Post-Diagnostic Engine — Ultra Superior
# Responsável por criar interpretações pós-diagnósticas a partir
# de scores consolidados e matrizes de risco/força.

from backend.engine.validator import Validator
from backend.engine.summary_aggregator import SummaryAggregator
from backend.engine.report_generator import ReportGenerator

class PostDiagnosticEngine:

    def __init__(self):
        self.validator = Validator()
        self.summarizer = SummaryAggregator()
        self.report = ReportGenerator()

    def evaluate(self, dataset):
        """
        dataset: {
            "traits": {...},
            "risks": {...},
            "strengths": {...}
        }
        """

        self.validator.ensure_keyset(dataset, ["traits", "risks", "strengths"])

        summary = self.summarizer.aggregate(dataset)

        interpretation = {
            "risk_level": summary["risk_global_level"],
            "strength_level": summary["strength_global_level"],
            "trait_vectors": summary["traits_vectorized"],
            "recommendations": summary["recommendations"],
        }

        return self.report.wrap("POST_DIAGNOSTIC_ENGINE", interpretation)
