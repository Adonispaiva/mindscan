# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\planejamento.py
# Última atualização: 2025-12-11T09:59:21.184463

# D:\mindscan\backend\services\pdf\planejamento.py
# --------------------------------------------------
# Página de Planejamento Estratégico — MindScan
# Autor: Leo Vinci — Inovexa Software
#
# Esta página apresenta:
# - Estilo de planejamento
# - Coerência entre intenção → execução
# - Capacidade de priorização e organização
# - Indicadores de visão estratégica
# - Padrões de ação derivados da psicodinâmica MindScan
#
# Usado por:
# - Executive Renderer
# - Premium Renderer

from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import colors


class PlanejamentoPDF:
    """
    Constrói a página de planejamento estratégico do relatório MindScan,
    traduzindo padrões cognitivos, emocionais e motivacionais em ação prática.
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
    # AUXILIAR
    # --------------------------------------------------------------

    def _bullet_list(self, items):
        if not items:
            return "Dados não fornecidos."
        return "<br/>".join([f"• {item}" for item in items])

    # --------------------------------------------------------------
    # CONSTRUÇÃO DA PÁGINA
    # --------------------------------------------------------------

    def build(self, planning_data: dict, story: list):

        # Título
        story.append(Paragraph("Planejamento Estratégico Individual", self.title_style))
        story.append(Spacer(0, 0.5 * cm))

        if not planning_data:
            story.append(Paragraph("Sem dados de planejamento disponíveis.", self.text_style))
            return story

        # ----------------------------------------------------------
        # ESTRUTURA TABELADA
        # ----------------------------------------------------------

        story.append(Paragraph("Indicadores de Planejamento", self.section_style))

        rows = [["Indicador", "Descrição"]]

        for key, value in planning_data.items():
            rows.append([key, value])

        table = Table(rows, colWidths=[7 * cm, 11 * cm])
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

        # ----------------------------------------------------------
        # BLOCO NARRATIVO OPCIONAL
        # ----------------------------------------------------------

        insights = planning_data.get("insights", None)
        if insights:
            story.append(Paragraph("Análise Narrativa", self.section_style))
            story.append(Paragraph(self._bullet_list(insights), self.text_style))
            story.append(Spacer(0, 1 * cm))

        return story
