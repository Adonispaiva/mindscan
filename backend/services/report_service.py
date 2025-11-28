# Caminho: D:\backend\services\report_service.py
# MindScan — ReportService v2.0 (com Renderers Integrados)
# Diretor Técnico: Leo Vinci — Inovexa Software

from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import A4
from datetime import datetime
import os

from .report_templates.technical_renderer import TechnicalRenderer
from .report_templates.executive_renderer import ExecutiveRenderer
from .report_templates.psychodynamic_renderer import PsychodynamicRenderer
from .report_templates.premium_renderer import PremiumRenderer

RENDERER_MAP = {
    "technical": TechnicalRenderer,
    "executive": ExecutiveRenderer,
    "psychodynamic": PsychodynamicRenderer,
    "premium": PremiumRenderer,
}

class ReportService:
    @staticmethod
    def generate_pdf(test_id: str, results: list, report_type: str = "technical"):
        if report_type not in RENDERER_MAP:
            raise ValueError(f"Tipo de relatório inválido: {report_type}")

        RendererClass = RENDERER_MAP[report_type]
        renderer = RendererClass(test_id, results)

        output_dir = "D:/backend/reports"
        os.makedirs(output_dir, exist_ok=True)

        filename = f"mindscan_report_{test_id}_{report_type}.pdf"
        filepath = os.path.join(output_dir, filename)

        doc = SimpleDocTemplate(filepath, pagesize=A4)
        story = []

        renderer.build(story)
        doc.build(story)

        metadata = {
            "test_id": test_id,
            "report_type": report_type,
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "path": filepath
        }

        return filepath, metadata