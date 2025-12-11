# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\services\dashboard_data_aggregator.py
# Última atualização: 2025-12-11T09:59:27.855343

from .analytics_service import AnalyticsService
from .insight_feed_service import InsightFeedService
from .org_kpi_service import OrgKPIService

class DashboardDataAggregator:
    """
    Agrega múltiplas fontes de dados para compor o dashboard final.
    """

    @staticmethod
    def aggregate():
        return {
            "trends": AnalyticsService.compute_trends(),
            "kpis": OrgKPIService.get_kpis(),
            "feed": InsightFeedService.fetch_feed()
        }
