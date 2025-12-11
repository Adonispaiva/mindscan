# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\report\renderers\premium_renderer.py
# Última atualização: 2025-12-11T09:59:21.292589

from backend.services.report.renderers.base_renderer import BaseRenderer
from backend.services.report.renderers.executive_renderer import ExecutiveRenderer
from backend.mi.mi_narrative_polisher import MINarrativePolisher
from backend.mi.mi_risk_detector import MIRiskDetector

class PremiumRenderer(BaseRenderer):

    template_name = "premium_template"

    def build(self, test_id: str, results: dict) -> dict:

        executive_renderer = ExecutiveRenderer()
        exec_section = executive_renderer.build(test_id, results)

        enriched_narrative = MINarrativePolisher.polish(
            results.get("narrative", "Sem narrativa disponível.")
        )

        risks = MIRiskDetector.detect(results)

        payload = {
            "header": self.render_header(test_id, results),
            "executive_section": exec_section,
            "premium_narrative": enriched_narrative,
            "risks": risks,
            "footer": self.render_footer()
        }

        return payload
