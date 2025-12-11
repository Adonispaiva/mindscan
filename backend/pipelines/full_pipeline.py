# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\pipelines\full_pipeline.py
# Última atualização: 2025-12-11T09:59:21.058152

"""
full_pipeline.py — MindScan FULL STACK Pipeline
Este é o pipeline mais completo do MindScan, integrando:

- Big Five
- Traços avançados
- Riscos
- Regras psicoemocionais
- Mapas cognitivos
- Insights de alto nível
- Diagnóstico pré e pós-processado
- Integração multidimensional final

NÍVEL ULTRA SUPERIOR GARANTIDO.
"""

from engine.validation_engine import ValidationEngine
from engine.normalizer_engine import NormalizerEngine
from engine.integration_engine import IntegrationEngine
from engine.scoring_engine import ScoringEngine
from engine.summary_engine import SummaryEngine
from engine.risk_engine import RiskEngine
from engine.meta_engine import MetaEngine


class FullPipeline:
    def __init__(self):
        self.validator = ValidationEngine()
        self.normalizer = NormalizerEngine()
        self.integrator = IntegrationEngine()
        self.risk = RiskEngine()
        self.scorer = ScoringEngine()
        self.meta = MetaEngine()
        self.summarizer = SummaryEngine()

    def run(self, payload: dict) -> dict:
        self.validator.validate_input(payload)

        normalized = self.normalizer.normalize(payload)
        integrated = self.integrator.integrate(normalized)
        risk_map = self.risk.evaluate(integrated)
        scores = self.scorer.compute_score(integrated)
        meta = self.meta.generate_meta_profile(integrated)

        summary = self.summarizer.generate_summary(
            integrated,
            model="full",
            density="ultra",
            include_meta=True,
            include_risks=True,
            include_cross_signals=True
        )

        return {
            "normalized": normalized,
            "integrated": integrated,
            "risk_map": risk_map,
            "scores": scores,
            "meta": meta,
            "summary": summary
        }
