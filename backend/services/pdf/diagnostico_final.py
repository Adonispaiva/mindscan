# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\diagnostico_final.py
# Última atualização: 2025-12-11T09:59:21.168743

# D:\mindscan\backend\services\pdf\diagnostico_final.py
# ------------------------------------------------------
# Diagnóstico Final — MindScan
# Autor: Leo Vinci — Inovexa Software
#
# Esta página apresenta:
# - Sumário técnico da análise psicodinâmica
# - Consolidação final emocional, cognitiva, motivacional e comportamental
# - Síntese analítica destinada a especialistas e consultores
#
# Usado por:
# - Premium Renderer
# - Executive Renderer
# - Psychodynamic Renderer (fechamento técnico)

from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import colors


class DiagnosticoFinalPDF:
    """
    Constrói a página de diagnóstico final do relatório MindScan.
    Esta é a visão técnica consolidada antes da montagem final do PDF.
    """

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title_style = self._style_title()
        self.section_style = self._style_section()
        self.text_style = self._style_text()

    # --------------------------------------------------------------
    # ESTILOS
    # --------------------------------------------------------------

    def _style_title(self):
        style = self.styles["Heading1"]
        style.fontSize = 22
        style.leading = 28
        style.textColor = colors.HexColor("#002B55")
        style.spaceAfter = 18
        return style

    def _style_section(self):
        style = self.styles["Heading2"]
        style.fontSize = 14
        style.leading = 18
        style.textColor = colors.HexColor("#003366")
        style.spaceAfter = 12
        return style

    def _style_text(self):
        style = self.styles["BodyText"]
        style.fontSize = 11
        style.leading = 16
        style.textColor = colors.black
        style.spaceAfter = 10
        return style

    # --------------------------------------------------------------
    # AUXILIAR
    # --------------------------------------------------------------

    def _bullet_list(self, items):
        if not items:
            return "Nenhum dado disponível."
        return "<br/>".join([f"• {item}" for item in items])

    # --------------------------------------------------------------
    # CONSTRUÇÃO DA PÁGINA
    # --------------------------------------------------------------

    def build(self, diagnostic_summary: dict, story: list):

        story.append(Paragraph("Diagnóstico Final", self.title_style))
        story.append(Spacer(0, 0.6 * cm))

        if not diagnostic_summary:
            story.append(Paragraph("Sem dados técnicos para diagnóstico final.", self.text_style))
            return story

        # ----------------------------------------------------------
        # TABELA DE CONSOLIDAÇÃO TÉCNICA
        # ----------------------------------------------------------

        story.append(Paragraph("Consolidação Psicodinâmica", self.section_style))

        rows = [["Dimensão Técnica", "Resumo Analítico"]]

        for key, value in diagnostic_summary.items():
            if key == "insights":
                continue
            rows.append([key, value])

        table = Table(rows, colWidths=[6 * cm, 12 * cm])
        table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E4ECF7")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#002B55")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#002B55")),
                ("VALIGN", (0, 1), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ])
        )

        story.append(table)
        story.append(Spacer(0, 1 * cm))

        # ----------------------------------------------------------
        # INSIGHTS TÉCNICOS FINAIS
        # ----------------------------------------------------------

        if "insights" in diagnostic_summary:
            story.append(Paragraph("Insights Técnicos Finais", self.section_style))
            story.append(
                Paragraph(self._bullet_list(diagnostic_summary["insights"]), self.text_style)
            )
            story.append(Spacer(0, 1 * cm))

        return story
