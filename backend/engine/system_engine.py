# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\engine\system_engine.py
# Última atualização: 2025-12-11T09:59:20.841083

# MindScan System Engine — Ultra Superior v1.0
# Motor sistêmico que integra módulos, gera estado consolidado
# e valida coerência interna de outputs múltiplos.

from backend.engine.validator import Validator
from backend.engine.report_generator import ReportGenerator

class SystemEngine:
    """
    SystemEngine
    ------------
    Valida coerência entre múltiplos engines MindScan e consolida
    resultado sistêmico único.
    """

    def __init__(self):
        self.validator = Validator()
        self.report = ReportGenerator()

    def integrate(self, components):
        """
        components esperado:
        {
            "mi": {...},
            "traits": {...},
            "risks": {...},
            "strengths": {...},
            "synthetic": {...}
        }
        """

        required = ["mi", "traits", "risks", "strengths", "synthetic"]
        self.validator.ensure_keyset(components, required)

        # Coerência estrutural
        coherence = {
            "traits_vs_risks": len(components["traits"]) == len(components["risks"]),
            "traits_vs_strengths": len(components["traits"]) == len(components["strengths"]),
            "synthetic_valid": "synthetic_index" in components["synthetic"]
        }

        # Estado final sistêmico
        unified_state = {
            "coherence": coherence,
            "synthetic_index": components["synthetic"]["synthetic_index"],
            "dimensions": {
                "mi": components["mi"],
                "traits": components["traits"],
                "risks": components["risks"],
                "strengths": components["strengths"]
            }
        }

        return self.report.wrap("SYSTEM_ENGINE", unified_state)
