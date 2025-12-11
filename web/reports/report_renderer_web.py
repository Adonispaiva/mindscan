# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\reports\report_renderer_web.py
# Última atualização: 2025-12-11T09:59:27.839711

from .web_report_template_manager import WebReportTemplateManager

class ReportRendererWeb:
    """
    Renderiza relatórios combinando templates + dados analíticos.
    """

    @staticmethod
    def render(template: str, data: dict):
        base = WebReportTemplateManager.get(template)
        return base + f"<p>{data}</p>"
