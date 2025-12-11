# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\services\providers\risk_data_provider.py
# Última atualização: 2025-12-11T09:59:27.870966

class RiskDataProvider:
    """
    Fornece dados agregados de riscos detectados.
    """

    @staticmethod
    def fetch():
        return {
            "risk_index": 42,
            "high_risk_count": 128
        }
