# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\ui\widgets\performance_heatmap_widget.py
# Última atualização: 2025-12-11T09:59:27.886588

class PerformanceHeatmapWidget:
    """
    Widget de heatmap de performance geral.
    """

    @staticmethod
    def render(data: dict):
        return {
            "title": "Performance Heatmap",
            "matrix": data.get("matrix", [])
        }
