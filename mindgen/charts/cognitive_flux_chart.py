# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\mindgen\charts\cognitive_flux_chart.py
# Última atualização: 2025-12-11T09:59:27.699099

class CognitiveFluxChart:
    """
    Mostra oscilações de fluxo cognitivo (velocidade + profundidade).
    """

    @staticmethod
    def render(values: list):
        return {
            "type": "flux",
            "points": values
        }
