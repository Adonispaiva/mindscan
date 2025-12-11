# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\reports\web_report_template_manager.py
# Última atualização: 2025-12-11T09:59:27.839711

class WebReportTemplateManager:
    """
    Gerencia templates visuais de relatórios em ambiente Web.
    """

    TEMPLATES = {
        "default": "<h1>MindScan Report</h1>",
        "corporate": "<h1>Corporate Behavioral Report</h1>"
    }

    @staticmethod
    def get(template: str):
        return WebReportTemplateManager.TEMPLATES.get(template, WebReportTemplateManager.TEMPLATES["default"])
