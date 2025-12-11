# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\estrutura_motivacional.py
# Última atualização: 2025-12-11T09:59:21.168743

# D:\mindscan\backend\services\pdf\estrutura_motivacional.py
# -----------------------------------------------------------
# Página de Estrutura Motivacional do Relatório MindScan
# Autor: Leo Vinci — Inovexa Software
#
# Esta página apresenta:
# - Drivers motivacionais primários
# - Fontes de energia psicológica
# - Padrões de engajamento
# - Tensões motivacionais
# - Integrações com aspectos emocionais e cognitivos
#
# Usada por:
# - Premium Renderer
# - Executive Renderer
# - Psychodynamic Renderer

from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import colors


class EstruturaMotivacionalPDF:
    """
    Constrói a seção motivacional do relatório MindScan,
    traduzindo impulsos, energia e drivers para linguagem executiva.
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
        story.append(Paragraph("Estrutura Motivacional", self.title_style))
        story.append(Spacer(0, 0.5 * cm))

        # ----------------------------------------------------------
        # DRIVERS MOTIVACIONAIS PRINCIPAIS
        # ----------------------------------------------------------

        story.append(Paragraph("Drivers Motivacionais", self.section_style))
        drivers = psych_extract(psychdynamic, "motivational_drivers")
        story.append(Paragraph(self._bullet_list(drivers), self.text_style))
        story.append(Spacer(0, 0.4 * cm))

        # ----------------------------------------------------------
        # FONTES DE ENERGIA PSICOLÓGICA
        # ----------------------------------------------------------

        story.append(Paragraph("Fontes de Energia Psicológica", self.section_style))
        energia = psych_extract(psychdynamic, "energy_sources")
        story.append(Paragraph(self._bullet_list(energia), self.text_style))
        story.append(Spacer(0, 0.4 * cm))

        # ----------------------------------------------------------
        # PADRÕES DE ENGAJAMENTO
        # ----------------------------------------------------------

        story.append(Paragraph("Padrões de Engajamento", self.section_style))
        engajamento = psych_extract(psychdynamic, "engagement_patterns")
        story.append(Paragraph(self._bullet_list(engajamento), self.text_style))
        story.append(Spacer(0, 0.4 * cm))

        # ----------------------------------------------------------
        # TENSÕES MOTIVACIONAIS
        # ----------------------------------------------------------

        story.append(Paragraph("Tensões Motivacionais", self.section_style))
        tensoes = psych_extract(psychdynamic, "motivational_tensions")
        story.append(Paragraph(self._bullet_list(tensoes), self.text_style))
        story.append(Spacer(0, 1 * cm))

        return story


# ----------------------------------------------------------------------
# FUNÇÃO AUXILIAR — EXTRATOR PSICODINÂMICO
# ----------------------------------------------------------------------

def psych_extract(psych_data: dict, key: str):
    """
    Extrai listas de conteúdo motivacional, aceitando:
    - listas diretas
    - dicionários (valores textuais)
    - fallback seguro
    """
    block = psych_data.get(key, {})
    if isinstance(block, list):
        return block
    if isinstance(block, dict):
        return list(block.values())
    return ["Dados não fornecidos."]
