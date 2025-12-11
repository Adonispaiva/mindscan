# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\engine\summary_engine.py
# Última atualização: 2025-12-11T09:59:20.838001

# MindScan Summary Engine — Ultra Superior v1.0
# Responsável por gerar resumos estruturados de múltiplas dimensões cognitivas,
# incluindo combinações MI, traços, riscos, forças e insights.

from backend.engine.validator import Validator
from backend.engine.report_generator import ReportGenerator

class SummaryEngine:
    """
    SummaryEngine
    -------------
    Consolida blocos analíticos em resumos padronizados MindScan.
    """

    def __init__(self):
        self.validator = Validator()
        self.report = ReportGenerator()

    def generate(self, blocks):
        """Recebe dict com eixos e blocos textuais e sintetiza resumo formal."""

        self.validator.ensure_dict(blocks)
        self.validator.ensure_non_empty(blocks)

        sections = []
        for key, text in blocks.items():
            if not isinstance(text, str):
                continue
            cleaned = text.strip()
            section = f"[{key.upper()}] {cleaned}"
            sections.append(section)

        final_summary = "\n\n".join(sections)

        response = {
            "sections_processed": len(sections),
            "summary": final_summary
        }

        return self.report.wrap("SUMMARY_ENGINE", response)
