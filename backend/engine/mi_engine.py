# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\engine\mi_engine.py
# Última atualização: 2025-12-11T09:59:20.813004

# MindScan MI Engine — Ultra Superior v1.0
# Módulo responsável por consolidar indicadores MI (Mind Integrity)
# Operação: entrada → normalização → cálculo → geração de estrutura MI

from backend.engine.normalizer import Normalizer
from backend.engine.validator import Validator
from backend.engine.report_generator import ReportGenerator

class MIEngine:
    """
    MIEngine
    --------
    Executa pipeline de inteligência MI:
    - Validação estrutural e semântica
    - Normalização vetorial
    - Cálculo de integridade cognitiva
    """

    def __init__(self):
        self.normalizer = Normalizer()
        self.validator = Validator()
        self.report = ReportGenerator()

    def compute_mi(self, data):
        """Executa pipeline MI completo."""
        self.validator.ensure_non_empty(data)
        self.validator.ensure_numeric_map(data)

        normalized = self.normalizer.scale_range(data, 0, 1)

        mi_score = sum(normalized.values()) / len(normalized)

        result = {
            "normalized": normalized,
            "mi_score": round(mi_score, 4),
            "status": "ok",
        }

        return self.report.wrap("MI_ENGINE", result)
