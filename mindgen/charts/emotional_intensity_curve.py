# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\mindgen\charts\emotional_intensity_curve.py
# Última atualização: 2025-12-11T09:59:27.699099

class EmotionalIntensityCurve:
    """
    Curva de intensidade emocional ao longo do tempo.
    """

    @staticmethod
    def render(values: list):
        return {
            "type": "curve",
            "points": values
        }
