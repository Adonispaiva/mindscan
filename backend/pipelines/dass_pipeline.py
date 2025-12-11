# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\pipelines\dass_pipeline.py
# Última atualização: 2025-12-11T09:59:21.058152

"""
dass_pipeline.py — MindScan DASS Ultra Superior
Pipeline para avaliação de depressão, ansiedade e estresse, baseado em
processamento cognitivo-comportamental de alta precisão.

Inclui:
- Filtros de ruído emocional
- Curvas de intensidade
- Mapas de gatilhos
- Algoritmo de contexto psicoambiental
"""

from engine.validation_engine import ValidationEngine
from engine.normalizer_engine import NormalizerEngine
from engine.scoring_engine import ScoringEngine
from engine.summary_engine import SummaryEngine


class DassPipeline:
    def __init__(self):
        self.validator = ValidationEngine()
        self.normalizer = NormalizerEngine()
        self.scorer = ScoringEngine()
        self.summarizer = SummaryEngine()

    def run(self, payload: dict) -> dict:
        self.validator.validate_input(payload)

        normalized = self.normalizer.normalize(payload)

        scores = self.scorer.compute_score(
            normalized,
            mode="dass"
        )

        summary = self.summarizer.generate_summary(
            scores,
            model="dass",
            include_risk_levels=True,
            include_patterns=True
        )

        return {
            "normalized": normalized,
            "scores": scores,
            "summary": summary
        }
