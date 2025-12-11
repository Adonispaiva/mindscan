# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\mindgen\panels\performance_overview_panel.py
# Última atualização: 2025-12-11T09:59:27.723166

class PerformanceOverviewPanel:
    """
    Painel resumo de performance agregada e preditiva.
    """

    @staticmethod
    def render(perf: dict):
        return {
            "title": "Performance Overview",
            "performance": perf
        }
