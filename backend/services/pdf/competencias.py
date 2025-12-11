# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\competencias.py
# Última atualização: 2025-12-11T09:59:21.168743

# D:\mindscan\backend\services\pdf\competencias.py
# --------------------------------------------------
# Página de Competências Corporativas do Relatório MindScan
# Autor: Leo Vinci — Inovexa Software
#
# Esta página apresenta:
# - Competências derivadas de personalidade, emoção e cognição
# - Indicadores profissionais
# - Forças corporativas baseadas em dados psicodinâmicos
#
# Usado pelo:
# - Executive Renderer
# - Premium Renderer

from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import colors


class CompetenciasPDF:
    """
    Constrói a página de competências corporativas do relatório,
    traduzindo scores psicodinâmicos em indicadores profissionais claros.
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
        style.fontSize = 20
        style.leading = 26
        style.textColor = colors.HexColor("#003366")
        style.spaceAfter = 16
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
    # CONSTRUÇÃO DA PÁGINA
    # --------------------------------------------------------------

    def build(self, competencies: dict, story: list):
        """
        Recebe um dict de competências estruturadas:
        {
            "Liderança": "Capacidade de influenciar...",
            "Comunicação": "Clareza, assertividade...",
            "Tomada de Decisão": "...",
            ...
        }
        """

        story.append(Paragraph("Competências Profissionais", self.title_style))
        story.append(Spacer(0, 0.5 * cm))

        if not competencies:
            story.append(Paragraph("Nenhuma competência fornecida.", self.text_style))
            return story

        # Montar tabela
        rows = [["Competência", "Descrição"]]

        for key, value in competencies.items():
            rows.append([key, value])

        table = Table(rows, colWidths=[6 * cm, 12 * cm])
        table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6EEF7")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#003366")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 12),
                ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#003366")),
                ("VALIGN", (0, 1), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ])
        )

        story.append(table)
        story.append(Spacer(0, 1 * cm))

        return story
