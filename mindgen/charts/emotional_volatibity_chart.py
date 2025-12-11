# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\mindgen\charts\emotional_volatibity_chart.py
# Última atualização: 2025-12-11T09:59:27.699099

class EmotionalVolatilityChart:
    """
    Mostra volatilidade emocional ao longo de ciclos.
    """

    @staticmethod
    def render(values: list):
        return {
            "type": "volatility",
            "series": values
        }
