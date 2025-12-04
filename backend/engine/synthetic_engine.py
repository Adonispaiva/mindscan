# MindScan Synthetic Engine — Ultra Superior
# Cria representação sintética de perfis cognitivos,
# combinando múltiplos níveis: MI, traços, riscos e forças.

from backend.engine.validator import Validator
from backend.engine.report_generator import ReportGenerator

class SyntheticEngine:

    def __init__(self):
        self.validator = Validator()
        self.report = ReportGenerator()

    def synthesize(self, block):
        """Gera síntese única a partir de blocos cognitivos."""
        self.validator.ensure_keyset(block, ["mi", "traits", "risks", "strengths"])

        combined = {
            "mi": block["mi"],
            "traits_major": block["traits"],
            "risk_factor": block["risks"],
            "strength_factor": block["strengths"],
            "synthetic_index": round(
                (block["mi"] + block["strengths"] - block["risks"]) / 3, 4
            ),
        }

        return self.report.wrap("SYNTHETIC_ENGINE", combined)
