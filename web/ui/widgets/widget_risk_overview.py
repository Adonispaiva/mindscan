# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\ui\widgets\widget_risk_overview.py
# Última atualização: 2025-12-11T09:59:27.886588

class WidgetRiskOverview:
    """
    Widget para exibir visão geral de riscos comportamentais.
    """

    @staticmethod
    def render(data: dict):
        return {
            "title": "Risk Overview",
            "risk_index": data.get("risk_index", 0),
            "high_risk_count": data.get("high_risk_count", 0)
        }
