# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\engine\trait_engine.py
# Última atualização: 2025-12-11T09:59:20.841083

# MindScan Trait Engine — Ultra Superior v1.0
# Atua na consolidação e interpretação de traços psicoprofissionais.

from backend.engine.normalizer import Normalizer
from backend.engine.validator import Validator
from backend.engine.report_generator import ReportGenerator

class TraitEngine:
    """
    TraitEngine
    -----------
    Processa indicadores de traços, normaliza, categoriza e classifica perfis.
    """

    def __init__(self):
        self.normalizer = Normalizer()
        self.validator = Validator()
        self.report = ReportGenerator()

    def analyze(self, traits):
        self.validator.ensure_numeric_map(traits)

        normalized = self.normalizer.zscore(traits)

        categories = {}
        for k, v in normalized.items():
            if v > 1.0:
                categories[k] = "Muito Alto"
            elif v > 0.3:
                categories[k] = "Alto"
            elif v > -0.3:
                categories[k] = "Moderado"
            elif v > -1.0:
                categories[k] = "Baixo"
            else:
                categories[k] = "Muito Baixo"

        result = {
            "normalized": normalized,
            "categories": categories
        }

        return self.report.wrap("TRAIT_ENGINE", result)
