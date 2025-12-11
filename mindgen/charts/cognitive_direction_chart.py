# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\mindgen\charts\cognitive_direction_chart.py
# Última atualização: 2025-12-11T09:59:27.699099

class CognitiveDirectionChart:
    """
    Mostra direção cognitiva: expansão, retração, estabilidade.
    """

    @staticmethod
    def render(direction: dict):
        return {
            "type": "direction",
            "direction_model": direction
        }
