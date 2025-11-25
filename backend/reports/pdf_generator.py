# ============================================================
# MindScan — PDF Generator
# ============================================================
# Converte o relatório textual do ReportEngine em um PDF
# profissional, com formatação padronizada.
#
# Este módulo usa a biblioteca "reportlab" como backend padrão.
# ============================================================

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from typing import Dict, Any
import datetime


class PDFGenerator:
    """
    Gera PDFs do relatório MindScan.
    """

    def __init__(self):
        self.styles = getSampleStyleSheet()

    # ------------------------------------------------------------
    # SALVAR EM PDF
    # ------------------------------------------------------------
    def generate_pdf(self, output_path: str, report_text: str, subject_name: str):
        """
        Gera o PDF final do relatório.
        """

        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            title=f"Relatório MindScan — {subject_name}",
            author="Inovexa Software",
            leftMargin=2 * cm,
            rightMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm
        )

        elements = []

        # Cabeçalho
        header_style = self.styles["Title"]
        elements.append(Paragraph("Relatório MindScan", header_style))
        elements.append(Spacer(1, 0.5 * cm))

        metadata_style = self.styles["Normal"]
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

        elements.append(Paragraph(f"Sujeito: {subject_name}", metadata_style))
        elements.append(Paragraph(f"Gerado em: {timestamp}", metadata_style))
        elements.append(Spacer(1, 1 * cm))

        # Corpo do relatório
        body_style = self.styles["BodyText"]

        for line in report_text.split("\n"):
            if line.strip():
                elements.append(Paragraph(line, body_style))
                elements.append(Spacer(1, 0.3 * cm))

        doc.build(elements)

        return output_path


# Instância pública
pdf_generator = PDFGenerator()
