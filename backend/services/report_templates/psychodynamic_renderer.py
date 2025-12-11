# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\report_templates\psychodynamic_renderer.py
# Última atualização: 2025-12-11T09:59:21.292589

# ============================================================
# MindScan — Psychodynamic Renderer
# ============================================================
# Gera Relatório Narrativo Psicodinâmico:
# - Narrativa híbrida completa
# - Interpretação emocional
# - Interpretação cognitiva
# - Conexões entre módulos
# ============================================================

from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from .base_renderer import BaseRenderer


class PsychodynamicRenderer(BaseRenderer):

    def build(self, story):
        styles = getSampleStyleSheet()

        story.append(Paragraph("<b>Relatório Psicodinâmico MindScan</b>", styles["Title"]))
        story.append(Spacer(1, 12))

        narrative = self.results.get("narrative", [])

        for block in narrative:
            story.append(Paragraph(block, styles["BodyText"]))
            story.append(Spacer(1, 6))

        return story
