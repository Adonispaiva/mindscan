# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\recomendacoes.py
# Última atualização: 2025-12-11T09:59:21.200087

# D:\mindscan\backend\services\pdf\recomendacoes.py
# ---------------------------------------------------
# Recomendações — MindScan
# Autor: Leo Vinci — Inovexa Software
#
# Esta página apresenta:
# - Recomendações práticas
# - Ações de desenvolvimento
# - Sugestões estratégicas de alinhamento
# - Boas práticas derivadas de toda a psicodinâmica MindScan
#
# Usado por:
# - Premium Renderer
# - Executive Renderer

from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import colors


class RecomendacoesPDF:
    """
    Constrói a página de recomendações práticas do relatório MindScan.
    A partir de insights psicodinâmicos, gera direções claras e aplicáveis.
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
        style.leading = 28
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
            return "Nenhuma recomendação disponível."
        return "<br/>".join([f"• {item}" for item in items])

    # --------------------------------------------------------------
    # CONSTRUÇÃO
    # --------------------------------------------------------------

    def build(self, recommendations: dict, story: list):
        """
        Espera um dict do tipo:
        {
            "Desenvolvimento Pessoal": [...],
            "Performance": [...],
            "Relacionamento": [...],
            "Tomada de Decisão": [...],
            "Liderança": [...],
            "Gatilhos de Atenção": [...],
            "Recomendações Gerais": [...]
        }
        """

        story.append(Paragraph("Recomendações", self.title_style))
        story.append(Spacer(0, 0.5 * cm))

        if not recommendations:
            story.append(Paragraph("Sem recomendações fornecidas.", self.text_style))
            return story

        # ----------------------------------------------------------
        # GERAR SEÇÃO POR SEÇÃO
        # ----------------------------------------------------------

        for section, items in recommendations.items():
            story.append(Paragraph(section, self.section_style))
            story.append(Paragraph(self._bullet_list(items), self.text_style))
            story.append(Spacer(0, 0.6 * cm))

        return story
