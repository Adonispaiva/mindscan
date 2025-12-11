# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\mindgen\charts\competency_spider_chart.py
# Última atualização: 2025-12-11T09:59:27.699099

class CompetencySpiderChart:
    """
    Exibe competências em um gráfico spider de 6 eixos.
    """

    @staticmethod
    def render(competencies: dict):
        return {
            "type": "spider",
            "axes": competencies
        }
