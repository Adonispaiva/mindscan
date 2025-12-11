# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\report_service.py
# Última atualização: 2025-12-11T09:59:21.120711

# ============================================================
# MindScan — Report Service (Final Hybrid Integration)
# ============================================================
# Responsável por:
#   - Executar MI Híbrido
#   - Montar payload final
#   - Escolher renderer adequado
#   - Gerar PDF final
# ============================================================

from typing import Dict, Any
from reportlab.platypus import SimpleDocTemplate

from backend.engine.mi_hybrid_orchestrator import MIHybridOrchestrator
from backend.services.report_templates.technical_renderer import TechnicalRenderer
from backend.services.report_templates.executive_renderer import ExecutiveRenderer
from backend.services.report_templates.psychodynamic_renderer import PsychodynamicRenderer
from backend.services.report_templates.premium_renderer import PremiumRenderer


RENDERER_MAP = {
    "technical": TechnicalRenderer,
    "executive": ExecutiveRenderer,
    "psychodynamic": PsychodynamicRenderer,
    "premium": PremiumRenderer,
}


class ReportService:

    def __init__(self):
        self.orchestrator = MIHybridOrchestrator()

    # ------------------------------------------------------------
    # GERAÇÃO DO RELATÓRIO FINAL (PDF)
    # ------------------------------------------------------------
    def generate_pdf(self, payload: Dict[str, Any], report_type: str = "technical") -> str:

        report_type = report_type.lower().strip()
        if report_type not in RENDERER_MAP:
            raise ValueError(f"Tipo de relatório inválido: {report_type}")

        # 1. Executar pipeline MI Híbrido completo
        final_payload = self.orchestrator.run(payload, mode="hybrid_auto")

        # 2. Instanciar renderer
        RendererClass = RENDERER_MAP[report_type]
        renderer = RendererClass(test_id="AUTO", results=final_payload)

        # 3. Montar PDF
        pdf_path = f"mindscan_report_{report_type}.pdf"
        doc = SimpleDocTemplate(pdf_path)

        story = []
        renderer.build(story)

        doc.build(story)

        return pdf_path
