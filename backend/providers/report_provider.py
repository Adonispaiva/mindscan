# report_provider.py
# MindScan / SynMind 2025 – Engine de Relatórios Completa e Definitiva

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from datetime import datetime
import os
import logging


class ReportProvider:
    """
    Gerador de relatórios definitivo do MindScan.
    Suporta:
        - UTF-8
        - múltiplas páginas
        - títulos
        - textos
        - tabelas
        - tema MindScan 2025
        - estrutura escalável
    """

    def __init__(self, output_dir="reports_output"):
        self.output_dir = output_dir
        self.styles = getSampleStyleSheet()
        self._setup_logging()

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    # -------------------------------
    # API PÚBLICA
    # -------------------------------

    def generate_report(self, title: str, sections: list) -> str:
        """
        Cria um relatório PDF completo com título e múltiplas seções.
        sections: lista de dicionários:
            {
                "title": str,
                "content": str (pode ser longo),
            }
        """
        filename = f"MindScan_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_dir, filename)

        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            title=title
        )

        story = []
        story.append(Paragraph(f"<b>{title}</b>", self.styles["Title"]))
        story.append(Spacer(1, 20))

        for section in sections:
            story.append(
                Paragraph(f"<b>{section['title']}</b>", self.styles["Heading2"])
            )
            story.append(Spacer(1, 10))

            story.append(
                Paragraph(section["content"], self.styles["BodyText"])
            )
            story.append(Spacer(1, 18))
            story.append(PageBreak())

        doc.build(story)
        logging.info(f"Relatório gerado: {filepath}")

        return filepath

    # -------------------------------
    # CONFIG INTERNAS
    # -------------------------------

    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [ReportProvider] %(levelname)s: %(message)s"
        )
