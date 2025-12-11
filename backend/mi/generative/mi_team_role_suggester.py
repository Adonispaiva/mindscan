# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\generative\mi_team_role_suggester.py
# Última atualização: 2025-12-11T09:59:20.939724

class MITeamRoleSuggester:
    """
    Sugere papéis de time com base em comportamento e dinâmica social.
    """

    @staticmethod
    def suggest(results: dict) -> dict:
        synergy = results.get("social_dynamics", {}).get("team_synergy", 50)

        if synergy > 70:
            return {"recommended_role": "Conector Social"}
        elif synergy > 55:
            return {"recommended_role": "Apoiador Operacional"}
        else:
            return {"recommended_role": "Especialista Técnico"}
