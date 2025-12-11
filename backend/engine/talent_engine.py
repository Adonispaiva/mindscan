# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\engine\talent_engine.py
# Última atualização: 2025-12-11T09:59:20.841083

# MindScan Talent Engine — Ultra Superior v1.0
# Identifica talentos dominantes, potenciais, lacunas e zonas de excelência.

from backend.engine.validator import Validator
from backend.engine.normalizer import Normalizer
from backend.engine.report_generator import ReportGenerator

class TalentEngine:
    """
    TalentEngine
    ------------
    Consolida indicadores comportamentais e cognitivos para extrair:
    - Talentos principais
    - Potenciais latentes
    - Gaps críticos
    """

    def __init__(self):
        self.validator = Validator()
        self.normalizer = Normalizer()
        self.report = ReportGenerator()

    def evaluate(self, traits, strengths):
        self.validator.ensure_numeric_map(traits)
        self.validator.ensure_numeric_map(strengths)

        traits_norm = self.normalizer.scale_range(traits, 0, 100)
        strengths_norm = self.normalizer.scale_range(strengths, 0, 100)

        combined = {k: (traits_norm.get(k, 0) + strengths_norm.get(k, 0)) / 2 for k in traits_norm}

        sorted_talents = sorted(combined.items(), key=lambda x: x[1], reverse=True)

        response = {
            "talent_ranking": sorted_talents,
            "top_3": sorted_talents[:3],
            "normalized_traits": traits_norm,
            "normalized_strengths": strengths_norm
        }

        return self.report.wrap("TALENT_ENGINE", response)
