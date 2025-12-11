# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\engine\mi_engine_advanced.py
# Última atualização: 2025-12-11T09:59:20.814002

# MindScan Advanced MI Engine — Ultra Superior v1.0
# Versão avançada: correção de outliers, ponderação adaptativa,
# clusterização cognitiva e score multinível.

from backend.engine.normalizer import Normalizer
from backend.engine.validator import Validator
from backend.engine.profile_aggregator import ProfileAggregator
from backend.engine.report_generator import ReportGenerator

class MIEngineAdvanced:

    def __init__(self):
        self.normalizer = Normalizer()
        self.validator = Validator()
        self.aggregator = ProfileAggregator()
        self.report = ReportGenerator()

    def compute(self, data, weights=None):
        """Executa MI avançado com pesos adaptativos."""

        self.validator.ensure_non_empty(data)
        self.validator.ensure_numeric_map(data)

        base = self.normalizer.remove_outliers(data)
        scaled = self.normalizer.zscore(base)

        weights = weights or {k: 1 for k in scaled}
        total_weight = sum(weights.values())

        score = sum(scaled[k] * weights[k] for k in scaled) / total_weight

        profile = self.aggregator.generate_profile(scaled)

        response = {
            "scaled": scaled,
            "profile": profile,
            "mi_advanced_score": round(score, 4),
        }

        return self.report.wrap("MI_ENGINE_ADVANCED", response)
