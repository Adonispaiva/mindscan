# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\engine\pipeline.py
# Última atualização: 2025-12-11T09:59:20.821001

"""
MindScan Engine — Pipeline Principal
Autor: Inovexa Software
Versão: 1.0.0

A pipeline é o núcleo unificado que coordena:
- carregamento de dados
- normalização
- scoring
- geração de insights
- geração de diagnósticos
- sumarização final
"""

from .scoring_engine import ScoringEngine
from .summarization_engine import SummarizationEngine


class MindScanPipeline:
    """
    Orquestrador geral do fluxo MindScan.
    """

    def __init__(self):
        self.scoring = ScoringEngine()
        self.summarizer = SummarizationEngine()

    def run(self, user_data: dict) -> dict:
        """
        Executa TODA a pipeline do MindScan.

        :param user_data: dados brutos já pré-validados
        :return: dicionário contendo resultados completos
        """

        # 1. Scoring psicométrico
        scores = self.scoring.compute_scores(user_data)

        # 2. Sumarização inteligente (insights gerais)
        summary = self.summarizer.generate_summary(scores)

        return {
            "scores": scores,
            "summary": summary
        }
