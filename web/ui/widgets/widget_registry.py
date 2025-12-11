# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\ui\widgets\widget_registry.py
# Última atualização: 2025-12-11T09:59:27.886588

class WidgetRegistry:
    """
    Registro de widgets do Dashboard.
    """

    widgets = {
        "global_stats": {"title": "Global Stats"},
        "risk_overview": {"title": "Risk Overview"}
    }

    @staticmethod
    def list_widgets():
        return list(WidgetRegistry.widgets.keys())
