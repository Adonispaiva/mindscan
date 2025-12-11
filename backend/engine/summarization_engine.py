# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\engine\summarization_engine.py
# Última atualização: 2025-12-11T09:59:20.835003

# MindScan Summarization Engine — Ultra Superior
# Responsável por sintetizar vários blocos informacionais em texto formal.

from backend.engine.validator import Validator
from backend.engine.report_generator import ReportGenerator

class SummarizationEngine:

    def __init__(self):
        self.validator = Validator()
        self.report = ReportGenerator()

    def synthesize(self, blocks):
        """Recebe múltiplos blocos de texto e cria resumo estruturado."""

        self.validator.ensure_list(blocks)
        self.validator.ensure_non_empty(blocks)

        cleaned = [b.strip() for b in blocks]
        summary = " ".join(cleaned)

        final = {
            "summary_length": len(summary),
            "sections_merged": len(blocks),
            "text": summary,
        }

        return self.report.wrap("SUMMARIZATION_ENGINE", final)
