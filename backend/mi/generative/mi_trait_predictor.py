# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\generative\mi_trait_predictor.py
# Última atualização: 2025-12-11T09:59:20.941724

class MITraitPredictor:
    """
    Prevê evolução de traços com base em padrões atuais.
    """

    @staticmethod
    def predict(results: dict) -> dict:
        big5 = results.get("big5", {})
        predictions = {}

        for trait, value in big5.items():
            trend = value + 5 if value < 60 else value - 3
            predictions[trait] = round(trend, 2)

        return predictions
