# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\pipelines\ocai_pipeline.py
# Última atualização: 2025-12-11T09:59:21.058152

"""
ocai_pipeline.py — OCAI Organizational Culture Assessment
Análise completa do perfil cultural organizacional.

Camadas incluídas:
- Estrutura de valores
- Arquétipos culturais
- Conflitos de cultura
- Tendências de maturidade
- Riscos organizacionais
"""

from engine.validation_engine import ValidationEngine
from engine.normalizer_engine import NormalizerEngine
from engine.integration_engine import IntegrationEngine
from engine.summary_engine import SummaryEngine
from engine.scoring_engine import ScoringEngine


class OCAIPipeline:
    def __init__(self):
        self.validator = ValidationEngine()
        self.normalizer = NormalizerEngine()
        self.integrator = IntegrationEngine()
        self.scorer = ScoringEngine()
        self.summarizer = SummaryEngine()

    def run(self, payload: dict) -> dict:
        self.validator.validate_input(payload)
        normalized = self.normalizer.normalize(payload)
        integrated = self.integrator.integrate(normalized)

        score = self.scorer.compute_score(
            integrated,
            mode="ocai"
        )

        summary = self.summarizer.generate_summary(
            integrated,
            model="ocai",
            density="ultra",
            include_cultural_archetypes=True,
            include_organizational_risks=True
        )

        return {
            "normalized": normalized,
            "integrated": integrated,
            "score": score,
            "summary": summary
        }
