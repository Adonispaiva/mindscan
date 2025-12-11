# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\services\insight_feed_service.py
# Última atualização: 2025-12-11T09:59:27.855343

class InsightFeedService:
    """
    Alimenta o dashboard com insights em tempo real.
    """

    @staticmethod
    def fetch_feed():
        return [
            {"type": "performance", "msg": "A performance média aumentou 3%"},
            {"type": "risk", "msg": "Riscos emocionais diminuíram este mês"}
        ]
