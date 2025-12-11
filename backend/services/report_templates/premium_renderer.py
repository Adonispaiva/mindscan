# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\report_templates\premium_renderer.py
# Última atualização: 2025-12-11T09:59:21.292589

# ============================================================
# MindScan — Premium Renderer
# ============================================================
# Relatório mais completo:
# - Tudo do executivo
# - Tudo do técnico
# - Toda a narrativa psicodinâmica
# - Gráficos avançados (placeholder)
# - Capa premium
# - Sumário automático
# ============================================================

from reportlab.platypus import Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

from .base_renderer import BaseRenderer


class PremiumRenderer(BaseRenderer):

    def build(self, story):
        styles = getSampleStyleSheet()

        # Capa
        story.append(Paragraph("<b>MindScan — Relatório Premium</b>", styles["Title"]))
        story.append(Spacer(1, 200))
        story.append(PageBreak())

        # Resumo Executivo
        summary = self.results.get("summary", {})
        highlights = summary.get("highlights", [])
        story.append(Paragraph("<b>Resumo Executivo</b>", styles["Heading1"]))
        for h in highlights:
            story.append(Paragraph(f"- {h}", styles["BodyText"]))
        story.append(PageBreak())

        # Narrativa Psicodinâmica
        narrative = self.results.get("narrative", [])
        story.append(Paragraph("<b>Narrativa Psicodinâmica</b>", styles["Heading1"]))
        for block in narrative:
            story.append(Paragraph(block, styles["BodyText"]))
            story.append(Spacer(1, 6))
        story.append(PageBreak())

        # Parte Técnica
        normalized = self.results.get("normalized", {})
        story.append(Paragraph("<b>Dados Técnicos</b>", styles["Heading1"]))
        for block, values in normalized.items():
            story.append(Paragraph(f"<b>{block.upper()}</b>", styles["Heading2"]))
            for k, v in values.items():
                if isinstance(v, dict) and "score" in v:
                    story.append(Paragraph(f"{k}: {v['score']}", styles["BodyText"]))
            story.append(Spacer(1, 10))

        return story
