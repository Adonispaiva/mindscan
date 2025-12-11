# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\pipelines\bussola_pipeline.py
# Última atualização: 2025-12-11T09:59:21.058152

"""
bussola_pipeline.py — MindScan Bussola Cognitiva
Pipeline avançado para orientação psicológica, comportamental e estratégica.
Gera mapa cognitivo, perfil direcional e interpretações profundas de intenção,
foco, prioridade e energia mental.

Pilares:
- Arquitetura íntegra e expandida
- Zero regressão
- Padrão Inovexa de completude
"""

from engine.normalizer_engine import NormalizerEngine
from engine.meta_engine import MetaEngine
from engine.summary_engine import SummaryEngine
from engine.validation_engine import ValidationEngine


class BussolaPipeline:
    """Pipeline da Bússola Cognitiva — Arquitetura Ultra Superior."""

    def __init__(self):
        self.normalizer = NormalizerEngine()
        self.meta_engine = MetaEngine()
        self.summarizer = SummaryEngine()
        self.validator = ValidationEngine()

    def run(self, payload: dict) -> dict:
        self.validator.validate_input(payload)

        normalized = self.normalizer.normalize(payload)

        meta = self.meta_engine.generate_meta_profile(normalized)

        summary = self.summarizer.generate_summary(
            meta,
            density="ultra",
            model="bussola",
            include_orientation=True,
            include_dynamics=True
        )

        return {
            "normalized": normalized,
            "meta_profile": meta,
            "summary": summary
        }
