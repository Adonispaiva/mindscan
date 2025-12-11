# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\report_templates\technical_renderer.py
# Última atualização: 2025-12-11T09:59:21.292589

# ============================================================
# MindScan — Technical Renderer
# ============================================================
# Gera Relatório Técnico Completo:
# - 39 dimensões
# - Metadados
# - Scores híbridos
# ============================================================

from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from .base_renderer import BaseRenderer


class TechnicalRenderer(BaseRenderer):

    def build(self, story):
        styles = getSampleStyleSheet()
        title = Paragraph("<b>Relatório Técnico MindScan</b>", styles["Title"])
        story.append(title)
        story.append(Spacer(1, 12))

        # Normalized blocks (Big Five, TEIQue, etc.)
        normalized = self.results.get("normalized", {})

        for block, values in normalized.items():
            story.append(Paragraph(f"<b>{block.upper()}</b>", styles["Heading2"]))

            if isinstance(values, dict):
                for k, v in values.items():
                    if isinstance(v, dict) and "score" in v:
                        score = v["score"]
                        story.append(Paragraph(f"{k}: {score}", styles["BodyText"]))

            story.append(Spacer(1, 10))

        # Metadata
        metadata = self.results.get("metadata", {})
        story.append(Paragraph("<b>Metadados</b>", styles["Heading2"]))

        for k, v in metadata.items():
            story.append(Paragraph(f"{k}: {v}", styles["BodyText"]))

        return story
