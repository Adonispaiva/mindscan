# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\pipelines\big5_pipeline.py
# Última atualização: 2025-12-11T09:59:21.042587

"""
big5_pipeline.py — MindScan ULTRA SUPERIOR
Pipeline de processamento completo baseado nos traços Big Five,
com arquitetura expandida, validações profundas, camadas de síntese e
preparação para insights avançados.

Este módulo:
- processa entradas brutas,
- aplica normalização,
- analisa padrões comportamentais,
- gera perfil estruturado,
- emite scoring Big Five,
- envia resumo e insights de alta densidade analítica.
"""

from engine.normalizer_engine import NormalizerEngine
from engine.trait_engine import TraitEngine
from engine.scoring_engine import ScoringEngine
from engine.summary_engine import SummaryEngine
from engine.validation_engine import ValidationEngine


class Big5Pipeline:
    """Pipeline completo e robusto para avaliação Big Five."""

    def __init__(self):
        self.normalizer = NormalizerEngine()
        self.trait_engine = TraitEngine()
        self.scorer = ScoringEngine()
        self.summarizer = SummaryEngine()
        self.validator = ValidationEngine()

    def run(self, input_payload: dict) -> dict:
        """
        Executa o pipeline completo Big Five.
        """
        self.validator.validate_input(input_payload)

        normalized = self.normalizer.normalize(input_payload)

        trait_profile = self.trait_engine.extract_traits(normalized)

        score = self.scorer.compute_score(trait_profile)

        summary = self.summarizer.generate_summary(
            score,
            model="big5",
            density="high",
            include_behaviors=True,
            include_risks=True
        )

        return {
            "status": "success",
            "normalized": normalized,
            "traits": trait_profile,
            "score": score,
            "summary": summary
        }
