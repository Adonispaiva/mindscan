# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\coaching_v4\ranking\coaching_priority_ranker_v4.py
# Última atualização: 2025-12-11T09:59:27.558489

class CoachingPriorityRankerV4:
    """
    Classifica ações de coaching por prioridade.
    """

    @staticmethod
    def rank(actions: list):
        return sorted(actions, key=lambda x: x.get("priority", 0), reverse=True)
