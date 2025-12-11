# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\report_templates\executive_renderer.py
# Última atualização: 2025-12-11T09:59:21.292589

# ============================================================
# MindScan — Executive Renderer
# ============================================================
# Gera Relatório Executivo:
# - Resumo executivo
# - Forças
# - Riscos
# - Gráficos principais (placeholder)
# - Conteúdo técnico simplificado
# ============================================================

from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from .base_renderer import BaseRenderer


class ExecutiveRenderer(BaseRenderer):

    def build(self, story):
        styles = getSampleStyleSheet()

        story.append(Paragraph("<b>MindScan — Relatório Executivo</b>", styles["Title"]))
        story.append(Spacer(1, 12))

        summary = self.results.get("summary", {})
        highlights = summary.get("highlights", [])

        story.append(Paragraph("<b>Destaques Principais</b>", styles["Heading2"]))
        for h in highlights:
            story.append(Paragraph(f"- {h}", styles["BodyText"]))
        story.append(Spacer(1, 10))

        # Riscos (a partir de insights)
        insights = self.results.get("insights", {})
        story.append(Paragraph("<b>Riscos e Pontos de Atenção</b>", styles["Heading2"]))
        for k, v in insights.items():
            if "tensão" in v.lower() or "instabilidade" in v.lower():
                story.append(Paragraph(f"- {v}", styles["BodyText"]))

        story.append(Spacer(1, 10))

        story.append(Paragraph("<b>Resumo Técnico</b>", styles["Heading2"]))
        norm = self.results.get("normalized", {})
        story.append(Paragraph(f"Dimensões processadas: {len(norm.keys())}", styles["BodyText"]))

        return story
