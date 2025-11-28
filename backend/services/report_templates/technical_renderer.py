# Caminho: D:\backend\services\report_templates\technical_renderer.py
# MindScan — Technical Renderer v2.0
# Autor: Leo Vinci — Diretor de Tecnologia e Produção (Inovexa)
# Template técnico (dados completos, sem narrativa, sem gráficos)

from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

class TechnicalRenderer:
    def __init__(self, test_id, results):
        self.test_id = test_id
        self.results = results
        self.styles = getSampleStyleSheet()

    def build(self, story):
        # Cabeçalho
        title = f"MindScan — Relatório Técnico Completo ({self.test_id})"
        story.append(Paragraph(title, self.styles["Title"]))
        story.append(Spacer(1, 18))

        timestamp = datetime.utcnow().isoformat() + "Z"
        story.append(Paragraph(f"Gerado em: {timestamp}", self.styles["Normal"]))
        story.append(Spacer(1, 12))

        story.append(Paragraph("Resultados Psicometricos (Completo):", self.styles["Heading2"]))
        story.append(Spacer(1, 12))

        # Blocos técnicos
        for block in self.results:
            dim = block.get("dimension", "N/A")
            score = block.get("score", 0)
            desc = block.get("descriptor", "")
            metadata = block.get("metadata", {})
            model = metadata.get("model", "?")

            story.append(Paragraph(f"<b>{dim}</b> ({model})", self.styles["Heading3"]))
            story.append(Paragraph(f"Score: {score}", self.styles["Normal"]))
            story.append(Paragraph(f"Descrição: {desc}", self.styles["Normal"]))
            story.append(Spacer(1, 12))
