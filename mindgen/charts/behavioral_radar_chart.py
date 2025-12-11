# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\mindgen\charts\behavioral_radar_chart.py
# Última atualização: 2025-12-11T09:59:27.699099

class BehavioralRadarChart:
    """
    Gera gráfico radar com Big5 + TeiQue + Performance.
    """

    @staticmethod
    def render(traits: dict):
        return {
            "type": "radar",
            "data": traits
        }
