# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\identidade_emocional.py
# Última atualização: 2025-12-11T09:59:21.168743

# D:\mindscan\backend\services\pdf\identidade_emocional.py
# ---------------------------------------------------------
# Página de Identidade Emocional do Relatório MindScan
# Autor: Leo Vinci — Inovexa Software
#
# Esta seção apresenta:
# - Estrutura emocional (TEIQue)
# - Níveis de regulação e expressão emocional
# - Sensibilidade a estresse (DASS-21)
# - Padrões afetivos derivados do PsychCoreService
#
# Utilizada pelos templates:
# - Premium Renderer
# - Psychodynamic Renderer
# - Executive Renderer (quando habilitado)

from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import colors


class IdentidadeEmocionalPDF:
    """
    Constrói a página de Identidade Emocional do relatório,
    traduzindo padrões emocionais em linguagem executiva e clara.
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

    def build(self, psychodynamic: dict, story: list):

        story.append(Paragraph("Identidade Emocional", self.title_style))
        story.append(Spacer(0, 0.5 * cm))

        # --------------------------------------------------------------
        # TEIQue
        # --------------------------------------------------------------
        story.append(Paragraph("Padrões de Inteligência Emocional (TEIQue)", self.section_style))

        teique_block = psychdynamic_extract(psychdynamic, "teique")
        teique_text = self._bullet_list(teique_block)

        story.append(Paragraph(teique_text, self.text_style))
        story.append(Spacer(0, 0.4 * cm))

        # --------------------------------------------------------------
        # DASS-21
        # --------------------------------------------------------------
        story.append(Paragraph("Sensibilidade ao Estresse (DASS-21)", self.section_style))

        dass_block = psychdynamic_extract(psychdynamic, "dass")
        dass_text = self._bullet_list(dass_block)

        story.append(Paragraph(dass_text, self.text_style))
        story.append(Spacer(0, 0.4 * cm))

        # --------------------------------------------------------------
        # CROSSLINKS EMOCIONAIS
        # --------------------------------------------------------------
        story.append(Paragraph("Integrações Emocionais (Crosslinks)", self.section_style))

        cross_block = psychdynamic_extract(psychdynamic, "crosslinks")
        cross_text = self._bullet_list(cross_block)

        story.append(Paragraph(cross_text, self.text_style))
        story.append(Spacer(0, 1 * cm))

        return story


# ----------------------------------------------------------------------
# FUNÇÃO AUXILIAR — EXTRATOR DE LISTAS PSICODINÂMICAS
# ----------------------------------------------------------------------

def psychdynamic_extract(psych_data: dict, key: str):
    """
    Extrai listas de conteúdo psicodinâmico, aceitando:
    - listas diretas
    - dicionários com valores textuais
    - fallback seguro
    """
    block = psych_data.get(key, {})
    if isinstance(block, list):
        return block
    if isinstance(block, dict):
        return list(block.values())
    return ["Dados não fornecidos."]
