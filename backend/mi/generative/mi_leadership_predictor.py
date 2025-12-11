# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\generative\mi_leadership_predictor.py
# Última atualização: 2025-12-11T09:59:20.903579

class MILeadershipPredictor:
    """
    Prediz potencial de liderança e evolução de estilo.
    """

    @staticmethod
    def predict(results: dict) -> dict:
        big5 = results.get("big5", {})
        tei = results.get("teique", {})

        leadership = (
            big5.get("extroversao", 50) * 0.4 +
            big5.get("consciencia", 50) * 0.3 +
            tei.get("autocontrole", 50) * 0.3
        )

        return {
            "leadership_potential": round(leadership, 2),
            "style": "visionário" if leadership > 70 else "operacional"
        }
