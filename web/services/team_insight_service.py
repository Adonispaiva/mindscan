# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\services\team_insight_service.py
# Última atualização: 2025-12-11T09:59:27.855343

class TeamInsightService:
    """
    Gera insights agregados sobre times.
    """

    @staticmethod
    def evaluate_team(members: list):
        avg_score = sum(m.get("score", 50) for m in members) / max(1, len(members))
        return {
            "team_avg_score": round(avg_score, 2),
            "team_size": len(members)
        }
