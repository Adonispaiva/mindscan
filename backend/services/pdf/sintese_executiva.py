# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\sintese_executiva.py
# Última atualização: 2025-12-11T09:59:21.200087

# D:\mindscan\backend\services\pdf\sintese_executiva.py
# -------------------------------------------------------
# Síntese Executiva — MindScan
# Autor: Leo Vinci — Inovexa Software
#
# Esta página apresenta:
# - Resumo executivo dos principais achados do MindScan
# - Forças críticas
# - Riscos prioritários
# - Indicadores-chave de personalidade, emoção, cognição e comportamento
# - Conclusões estratégicas para tomada de decisão
#
# Usado em:
# - Premium Renderer
# - Executive Renderer
# - Corporate Summary Packs

from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import colors


class SinteseExecutivaPDF:
    """
    Constrói a síntese executiva do relatório MindScan,
    consolidando os achados essenciais de todas as demais seções.
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
        style.spaceAfter = 8
        return style

    # --------------------------------------------------------------
    # AUXILIAR
    # --------------------------------------------------------------

    def _bullet_list(self, items):
        if not items:
            return "Nenhum dado fornecido."
        return "<br/>".join([f"• {item}" for item in items])

    # --------------------------------------------------------------
    # CONSTRUÇÃO DA PÁGINA
    # --------------------------------------------------------------

    def build(self, summary_data: dict, story: list):

        story.append(Paragraph("Síntese Executiva", self.title_style))
        story.append(Spacer(0, 0.6 * cm))

        if not summary_data:
            story.append(Paragraph("Sem dados executivos para exibir.", self.text_style))
            return story

        # ----------------------------------------------------------
        # Tabela principal de achados executivos
        # ----------------------------------------------------------

        story.append(Paragraph("Achados Centrais", self.section_style))

        rows = [["Dimensão", "Resumo Executivo"]]

        for key, value in summary_data.items():
            if key == "insights":
                continue
            rows.append([key, value])

        table = Table(rows, colWidths=[6 * cm, 12 * cm])
        table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DCE6F2")),
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
        # Insights estratégicos
        # ----------------------------------------------------------

        if "insights" in summary_data:
            story.append(Paragraph("Insights Estratégicos", self.section_style))
            story.append(
                Paragraph(self._bullet_list(summary_data["insights"]), self.text_style)
            )
            story.append(Spacer(0, 1 * cm))

        return story
