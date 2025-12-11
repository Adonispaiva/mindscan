# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\ui\widgets\widget_team_map.py
# Última atualização: 2025-12-11T09:59:27.886588

class WidgetTeamMap:
    """
    Widget que exibe mapa comportamental de equipes.
    """

    @staticmethod
    def render(team_data: list):
        return {
            "title": "Team Behavioral Map",
            "members": team_data
        }
