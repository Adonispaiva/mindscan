# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\ui\team\team_profile_renderer.py
# Última atualização: 2025-12-11T09:59:27.886588

class TeamProfileRenderer:
    """
    Renderiza perfis completos de times.
    """

    @staticmethod
    def render(profile: dict):
        return {
            "team": profile.get("team_name", "N/A"),
            "members": profile.get("members", []),
            "average": profile.get("average", 0)
        }
