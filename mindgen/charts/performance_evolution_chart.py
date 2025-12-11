# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\mindgen\charts\performance_evolution_chart.py
# Última atualização: 2025-12-11T09:59:27.699099

class PerformanceEvolutionChart:
    """
    Linha de evolução de performance.
    """

    @staticmethod
    def render(values: list):
        return {
            "type": "line",
            "points": values
        }
