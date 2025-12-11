# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\report\assembler\report_assembler.py
# Última atualização: 2025-12-11T09:59:21.276887

from backend.services.report.enhancers.report_enhancer import ReportEnhancer
from backend.services.report.pdf.pdf_pipeline import PDFPipeline
from backend.services.report.renderers.executive_renderer import ExecutiveRenderer
from backend.services.report.renderers.premium_renderer import PremiumRenderer

class ReportAssembler:
    """
    Une renderer + enhancers + pipeline PDF para gerar
    o relatório final independente do tipo.
    """

    RENDERERS = {
        "executive": ExecutiveRenderer(),
        "premium": PremiumRenderer()
    }

    @staticmethod
    def assemble(report_type: str, test_id: str, results: dict) -> dict:
        renderer = ReportAssembler.RENDERERS.get(report_type)
        if not renderer:
            raise ValueError("Tipo de relatório não suportado.")

        base = renderer.build(test_id, results)
        enhanced = ReportEnhancer.enhance(base, results)
        doc = PDFPipeline.prepare_document(enhanced)
        export_info = PDFPipeline.export(doc)

        return export_info
