# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\generative\mi_role_recommendation_engine.py
# Última atualização: 2025-12-11T09:59:20.932427

class MIRoleRecommendationEngine:
    """
    Recomenda cargos ou funções baseadas no perfil psicométrico.
    """

    ROLES = {
        "liderança": ["extroversao", "consciencia", "autocontrole"],
        "analítico": ["consciencia", "amabilidade"],
        "comercial": ["extroversao", "empatia"],
        "criativo": ["abertura"]
    }

    @staticmethod
    def recommend(results: dict) -> dict:
        big5 = results.get("big5", {})
        tei = results.get("teique", {})

        recommendations = []

        for role, traits in MIRoleRecommendationEngine.ROLES.items():
            score = 0
            for trait in traits:
                score += big5.get(trait, 0) + tei.get(trait, 0)
            recommendations.append((role, score))

        recommendations.sort(key=lambda x: x[1], reverse=True)

        return {
            "top_role": recommendations[0][0] if recommendations else None,
            "ranking": recommendations
        }
