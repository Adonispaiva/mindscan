# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\report\renderers\psychodynamic_renderer.py
# Última atualização: 2025-12-11T09:59:21.292589

from backend.services.report.renderers.base_renderer import BaseRenderer
from backend.mi.mi_risk_detector import MIRiskDetector

class PsychodynamicRenderer(BaseRenderer):

    template_name = "psychodynamic_template"

    def build(self, test_id: str, results: dict) -> dict:

        risks = MIRiskDetector.detect(results)

        payload = {
            "header": self.render_header(test_id, results),
            "risks": risks,
            "deep_factors": results.get("deep_factors", {}),
            "footer": self.render_footer()
        }

        return payload
