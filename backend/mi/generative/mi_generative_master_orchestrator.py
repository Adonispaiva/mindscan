# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\generative\mi_generative_master_orchestrator.py
# Última atualização: 2025-12-11T09:59:20.903579

from backend.mi.generative.mi_generative_summary_engine import MIGenerativeSummaryEngine
from backend.mi.generative.mi_multioutput_merger import MIMultiOutputMerger

class MIGenerativeMasterOrchestrator:
    """
    Orquestrador final da MI Generativa.
    Integra:
    - emocional
    - cognitivo
    - social
    - risco
    - performance
    - previsões
    - oportunidades
    - persona
    E produz um bloco unificado para o MindScan 4.0.
    """

    @staticmethod
    def orchestrate(generative_outputs: dict) -> dict:
        merged = MIMultiOutputMerger.merge(generative_outputs)
        summary = MIGenerativeSummaryEngine.summarize(generative_outputs)

        return {
            "merged": merged,
            "summary": summary,
            "status": "MI Generativa concluída"
        }
