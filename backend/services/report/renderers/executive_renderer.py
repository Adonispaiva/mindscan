# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\report\renderers\executive_renderer.py
# Última atualização: 2025-12-11T09:59:21.292589

from backend.services.report.renderers.base_renderer import BaseRenderer
from backend.mi.mi_executive_summary_engine import MIExecutiveSummaryEngine
from backend.mi.mi_semantic_mapper import MISemanticMapper
from backend.mi.mi_cross_section_engine import MICrossSectionEngine

class ExecutiveRenderer(BaseRenderer):

    template_name = "executive_template"

    def build(self, test_id: str, results: dict) -> dict:

        semantic = MISemanticMapper.build_map(results)
        cross = MICrossSectionEngine.cross(results)

        executive_summary = MIExecutiveSummaryEngine.generate(
            results=results,
            semantic_map=semantic,
            cross=cross
        )

        payload = {
            "header": self.render_header(test_id, results),
            "executive_summary": executive_summary,
            "semantic_map": semantic,
            "cross_section": cross,
            "footer": self.render_footer()
        }

        return payload
