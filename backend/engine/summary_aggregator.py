# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\engine\summary_aggregator.py
# Última atualização: 2025-12-11T09:59:20.837001

# MindScan Summarization Aggregator — Ultra Superior
# Une múltiplos resumos setoriais e cria uma síntese final unificada.

from backend.engine.validator import Validator

class SummarizationAggregator:

    def __init__(self):
        self.validator = Validator()

    def aggregate(self, summaries):
        """Recebe lista de resumos e consolida em um só texto coerente."""
        self.validator.ensure_list(summaries)

        cleaned = [s["text"].strip() for s in summaries if "text" in s]

        combined = " ".join(cleaned)

        return {
            "merged_count": len(cleaned),
            "final_summary": combined,
        }
