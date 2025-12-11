# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\generative\mi_social_dynamics_engine.py
# Última atualização: 2025-12-11T09:59:20.933428

class MISocialDynamicsEngine:
    """
    Analisa impacto social e relacional do indivíduo na equipe.
    """

    @staticmethod
    def analyze(results: dict) -> dict:
        impact = {}

        amabilidade = results.get("big5", {}).get("amabilidade", 50)
        extroversao = results.get("big5", {}).get("extroversao", 50)

        impact["team_synergy"] = round((amabilidade + extroversao) / 2, 2)
        impact["conflict_risk"] = round(100 - impact["team_synergy"], 2)

        return impact
