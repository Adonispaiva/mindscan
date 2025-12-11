# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\mindgen\widgets\executive_summary_widget.py
# Última atualização: 2025-12-11T09:59:27.745995

class ExecutiveSummaryWidget:
    """
    Widget que mostra resumo executivo do comportamento avaliado.
    """

    @staticmethod
    def render(summary: dict):
        return {
            "title": "Executive Summary",
            "summary": summary
        }
