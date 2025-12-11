# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\services\charts_service.py
# Última atualização: 2025-12-11T09:59:27.855343

class ChartsService:
    """
    Provê dados formatados para gráficos do Dashboard.
    """

    @staticmethod
    def build_line_chart(values: list):
        return {
            "type": "line",
            "points": values
        }
