# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\identidade_cognitiva.py
# Última atualização: 2025-12-11T09:59:21.168743

# D:\mindscan\backend\services\pdf\identidade_cognitiva.py
# ---------------------------------------------------------
# Página de Identidade Cognitiva do Relatório MindScan
# Autor: Leo Vinci — Inovexa Software
#
# Esta seção apresenta:
# - Funcionamento cognitivo predominante
# - Estratégias de tomada de decisão
# - Filtros de processamento
# - Padrões mentais derivados do PsychCoreService
#
# Usado por:
# - Premium Renderer
# - Executive Renderer
# - Psychodynamic Renderer (versão estendida)

from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import colors


class IdentidadeCognitivaPDF:
    """
    Constrói a página de Identidade Cognitiva do relatório MindScan,
    traduzindo padrões cognitivos e decisórios em linguagem clara.
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

        # Título
        story.append(Paragraph("Identidade Cognitiva", self.title_style))
        story.append(Spacer(0, 0.5 * cm))

        # ----------------------------------------------------------
        # PROCESSAMENTO COGNITIVO
        # ----------------------------------------------------------

        story.append(Paragraph("Padrões de Processamento Cognitivo", self.section_style))
        cognitive_block = psych_extract(psychodynamic, "cognitive")
        story.append(Paragraph(self._bullet_list(cognitive_block), self.text_style))
        story.append(Spacer(0, 0.4 * cm))

        # ----------------------------------------------------------
        # TOMADA DE DECISÃO
        # ----------------------------------------------------------

        story.append(Paragraph("Estilo de Tomada de Decisão", self.section_style))
        decision_block = psych_extract(psychdynamic, "decision_style")
        story.append(Paragraph(self._bullet_list(decision_block), self.text_style))
        story.append(Spacer(0, 0.4 * cm))

        # ----------------------------------------------------------
        # CROSSLINKS COGNITIVOS
        # ----------------------------------------------------------

        story.append(Paragraph("Integrações Cognitivas (Crosslinks)", self.section_style))
        cross_block = psych_extract(psychdynamic, "crosslinks_cognitive")
        story.append(Paragraph(self._bullet_list(cross_block), self.text_style))
        story.append(Spacer(0, 1 * cm))

        return story


# ----------------------------------------------------------------------
# FUNÇÃO AUXILIAR
# ----------------------------------------------------------------------

def psych_extract(psych_data: dict, key: str):
    """
    Extrai listas de blocos cognitivos, aceitando:
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
