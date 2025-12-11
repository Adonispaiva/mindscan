# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\ui\widgets\widget_kpi_board.py
# Última atualização: 2025-12-11T09:59:27.886588

class WidgetKPIBoard:
    """
    Widget que exibe KPIs de liderança, engajamento e retenção.
    """

    @staticmethod
    def render(kpis: dict):
        return {
            "title": "Organizational KPIs",
            "kpis": kpis
        }
