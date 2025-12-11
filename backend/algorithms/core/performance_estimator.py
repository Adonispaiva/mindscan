# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\core\performance_estimator.py
# Última atualização: 2025-12-11T09:59:20.620871

class PerformanceEstimator:
    """
    Estimador que combina múltiplos fatores psicométricos
    para gerar um score de performance preditiva.
    """

    @staticmethod
    def estimate(results: dict) -> float:
        score = 0
        weight_sum = 0

        weights = {
            "extroversao": 1.1,
            "amabilidade": 1.0,
            "consciencia": 1.3,
            "autocontrole": 1.2,
            "estresse": -1.1
        }

        # Big Five
        if "big5" in results:
            big5 = results["big5"]
            for trait, weight in weights.items():
                if trait in big5:
                    score += big5[trait] * weight
                    weight_sum += abs(weight)

        # TEIQue
        if "teique" in results:
            tei = results["teique"]
            if "autocontrole" in tei:
                score += tei["autocontrole"] * 1.4
                weight_sum += 1.4

        return round(score / weight_sum, 2) if weight_sum else 0
