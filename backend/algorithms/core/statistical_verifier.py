# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\core\statistical_verifier.py
# Última atualização: 2025-12-11T09:59:20.620871

class StatisticalVerifier:
    """
    Executa verificações estatísticas simples para garantir a integridade dos resultados.
    """

    @staticmethod
    def detect_outliers(data: dict, threshold: float = 2.0) -> dict:
        outliers = {}
        values = list(data.values())

        if not values:
            return {}

        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        std = variance ** 0.5

        for k, v in data.items():
            if abs(v - mean) > threshold * std:
                outliers[k] = v

        return outliers

    @staticmethod
    def validate_range(data: dict, min_val=0, max_val=100):
        invalid = {k: v for k, v in data.items() if not (min_val <= v <= max_val)}
        return invalid
