# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\report\renderers\technical_renderer.py
# Última atualização: 2025-12-11T09:59:21.292589

from backend.services.report.renderers.base_renderer import BaseRenderer

class TechnicalRenderer(BaseRenderer):

    template_name = "technical_template"

    def build(self, test_id: str, results: dict) -> dict:

        payload = {
            "header": self.render_header(test_id, results),
            "scores": results,
            "footer": self.render_footer()
        }

        return payload
