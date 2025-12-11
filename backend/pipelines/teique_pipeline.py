# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\pipelines\teique_pipeline.py
# Última atualização: 2025-12-11T09:59:21.058152

"""
teique_pipeline.py — Trait Emotional Intelligence Pipeline (TEIQue)
Versão ULTRA SUPERIOR — Engenharia Inovexa

Objetivos:
- Avaliar Competência Emocional (Trait Emotional Intelligence)
- Mapear:
    • Autoconsciência emocional
    • Autocontrole
    • Expressividade emocional
    • Gestão de estresse
    • Facilidade social
- Emitir perfil completo com insights correlacionais e riscos emocionais
"""

from engine.validation_engine import ValidationEngine
from engine.normalizer_engine import NormalizerEngine
from engine.integration_engine import IntegrationEngine
from engine.insight_engine import InsightEngine
from engine.risk_engine import RiskEngine
from engine.scoring_engine import ScoringEngine
from engine.summary_engine import SummaryEngine


class TEIQuePipeline:
    def __init__(self):
        self.validator = ValidationEngine()
        self.normalizer = NormalizerEngine()
        self.integrator = IntegrationEngine()
        self.insight = InsightEngine()
        self.risk = RiskEngine()
        self.scorer = ScoringEngine()
        self.summarizer = SummaryEngine()

    def run(self, payload: dict) -> dict:
        # Validação
        self.validator.validate_input(payload)

        # Normalização
        normalized = self.normalizer.normalize(payload)

        # Integração emocional
        integrated = self.integrator.integrate(normalized)

        # Insights emocionais
        insights = self.insight.extract_insights(
            integrated,
            mode="emotional",
            high_resolution=True
        )

        # Avaliação de risco emocional
        risk_map = self.risk.evaluate(
            integrated,
            dimension="emotional_stability"
        )

        # Scoring TEIQue
        scores = self.scorer.compute_score(
            integrated,
            mode="teique"
        )

        # Resumo ULTRA
        summary = self.summarizer.generate_summary(
            integrated,
            model="teique",
            density="ultra",
            include_emotional_axes=True,
            include_risks=True,
            include_regulation_markers=True
        )

        return {
            "normalized": normalized,
            "integrated": integrated,
            "insights": insights,
            "risk_map": risk_map,
            "scores": scores,
            "summary": summary
        }
