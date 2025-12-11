# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\generative\mi_anomaly_explainer.py
# Última atualização: 2025-12-11T09:59:20.887954

class MIAnomalyExplainer:
    """
    Explica anomalias detectadas na análise estatística.
    """

    @staticmethod
    def explain(results: dict) -> dict:
        outliers = results.get("outliers", {})
        explanation = {}

        for block, values in outliers.items():
            if values:
                explanation[block] = f"Detectados desvios atípicos em {len(values)} parâmetros."

        return explanation
