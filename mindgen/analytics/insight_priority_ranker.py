# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\mindgen\analytics\insight_priority_ranker.py
# Última atualização: 2025-12-11T09:59:27.699099

class InsightPriorityRanker:
    """
    Classifica insights por prioridade e impacto potencial.
    """

    @staticmethod
    def rank(insights: list):
        return sorted(insights, key=lambda x: x.get("priority", 0), reverse=True)
