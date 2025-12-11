# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\generative\mi_adaptative_narrative_engine.py
# Última atualização: 2025-12-11T09:59:20.887954

from backend.mi.mi_narrative_polisher import MINarrativePolisher

class MIAdaptiveNarrativeEngine:
    """
    Combina insights, riscos, semântica e performance
    em uma narrativa adaptativa e personalizada.
    """

    @staticmethod
    def build(results: dict, insights: dict) -> str:
        text = []

        text.append(f"Resultado global: {results.get('global_score', 50)}.")
        text.append(f"Performance preditiva: {results.get('performance_estimate', 50)}.")

        if insights.get("count", 0) > 0:
            text.append("Principais insights comportamentais:")
            for ins in insights["insights"]:
                text.append(f"- {ins}")

        polished = MINarrativePolisher.polish(" ".join(text))
        return polished
