# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\report\assets\charts\chart_generator.py
# Última atualização: 2025-12-11T09:59:21.276887

class ChartGenerator:
    """
    Gera payloads de gráficos para relatórios.
    (A geração de imagens é feita externamente.)
    """

    @staticmethod
    def build_bar_chart(data: dict, title: str):
        return {
            "type": "bar",
            "title": title,
            "data": [{"label": k, "value": v} for k, v in data.items()]
        }

    @staticmethod
    def build_radar_chart(data: dict, title: str):
        return {
            "type": "radar",
            "title": title,
            "data": [{"axis": k, "value": v} for k, v in data.items()]
        }
