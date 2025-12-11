# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\pipelines\esquemas_pipeline.py
# Última atualização: 2025-12-11T09:59:21.058152

"""
esquemas_pipeline.py — ULTRA SUPERIOR
Pipeline de análise de Esquemas Mentais (Schema Processing Layer).

Objetivos:
- Identificar padrões estruturais de pensamento
- Detectar esquemas nucleares e subesquemas ativados
- Mapear distorções cognitivas e pontos de ruptura
- Emitir relatório de alta densidade com riscos e recomendações
"""

from engine.validation_engine import ValidationEngine
from engine.normalization_engine import NormalizerEngine
from engine.integration_engine import IntegrationEngine
from engine.summary_engine import SummaryEngine
from engine.scoring_engine import ScoringEngine


class EsquemasPipeline:
    def __init__(self):
        self.validator = ValidationEngine()
        self.normalizer = NormalizerEngine()
        self.integrator = IntegrationEngine()
        self.scorer = ScoringEngine()
        self.summarizer = SummaryEngine()

    def run(self, payload: dict) -> dict:
        self.validator.validate_input(payload)

        normalized = self.normalizer.normalize(payload)

        estruturas = self.integrator.integrate_structures(normalized)

        score = self.scorer.compute_score(
            estruturas,
            mode="schemas"
        )

        summary = self.summarizer.generate_summary(
            estruturas,
            model="esquemas",
            density="ultra",
            include_risks=True,
            include_schema_links=True,
            include_meta_patterns=True
        )

        return {
            "normalized": normalized,
            "structures": estruturas,
            "score": score,
            "summary": summary
        }
