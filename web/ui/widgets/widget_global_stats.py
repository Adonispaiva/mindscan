# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\ui\widgets\widget_global_stats.py
# Última atualização: 2025-12-11T09:59:27.886588

class WidgetGlobalStats:
    """
    Widget que exibe estatísticas globais do MindScan.
    """

    @staticmethod
    def render(data: dict):
        return {
            "title": "Global Stats",
            "content": {
                "tests": data.get("total_tests", 0),
                "avg_score": data.get("avg_global_score", 0),
                "risks": data.get("risks_detected", 0)
            }
        }
