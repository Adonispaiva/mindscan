# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\narrativa.py
# Última atualização: 2025-12-11T09:59:21.184463

# D:\mindscan\backend\services\pdf\narrativa.py
# ------------------------------------------------
# Página de Narrativa Psicodinâmica do Relatório MindScan
# Autor: Leo Vinci — Inovexa Software
#
# Esta página integra a leitura psicodinâmica gerada pelo PsychCoreService:
# - Esquemas
# - Big Five
# - TEIQue
# - DASS-21
# - Ligações cruzadas (Crosslinks)
#
# Utilizada pelos templates:
# - Psychodynamic Renderer
# - Premium Renderer

from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import colors


class NarrativaPDF:
    """
    Página dedicada à narrativa psicodinâmica.
    Constrói blocos de texto executivos, ordenados e visualmente agradáveis
    para relatórios PDF.
    """

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title_style = self._build_title_style()
        self.section_style = self._build_section_style()
        self.text_style = self._build_text_style()

    # ----------------------------------------------------------------------
    # ESTILOS
    # ----------------------------------------------------------------------

    def _build_title_style(self):
        style = self.styles["Heading1"]
        style.fontSize = 20
        style.leading = 26
        style.textColor = colors.HexColor("#003366")
        style.spaceAfter = 16
        return style

    def _build_section_style(self):
        style = self.styles["Heading2"]
        style.fontSize = 14
        style.leading = 18
        style.textColor = colors.HexColor("#003366")
        style.spaceAfter = 12
        return style

    def _build_text_style(self):
        style = self.styles["BodyText"]
        style.fontSize = 11
        style.leading = 16
        style.textColor = colors.HexColor("#000000")
        style.spaceAfter = 10
        return style

    # ----------------------------------------------------------------------
    # PARSER DE NARRATIVAS
    # ----------------------------------------------------------------------

    def _format_bullet_list(self, items):
        if not items:
            return "Dados não fornecidos."
        return "<br/>".join([f"• {item}" for item in items])

    # ----------------------------------------------------------------------
    # CONSTRUÇÃO GERAL
    # ----------------------------------------------------------------------

    def build(self, psychodynamic: dict, story: list):
        """
        Constrói a página narrativa completa.
        """

        # Título da página
        story.append(Paragraph("Narrativa Psicodinâmica", self.title_style))
        story.append(Spacer(0, 0.4 * cm))

        # --------------------------------------------------------------
        # Bloco: Esquemas
        # --------------------------------------------------------------

        story.append(Paragraph("Esquemas Predominantes", self.section_style))
        esquemas_text = self._format_bullet_list(psychdynamic_list(psychodynamic, "esquemas"))
        story.append(Paragraph(esquemas_text, self.text_style))
        story.append(Spacer(0, 0.3 * cm))

        # --------------------------------------------------------------
        # Bloco: Big Five
        # --------------------------------------------------------------

        story.append(Paragraph("Traços de Personalidade (Big Five)", self.section_style))
        big5_text = self._format_bullet_list(psychdynamic_list(psychodynamic, "big5"))
        story.append(Paragraph(big5_text, self.text_style))
        story.append(Spacer(0, 0.3 * cm))

        # --------------------------------------------------------------
        # Bloco: TEIQue
        # --------------------------------------------------------------

        story.append(Paragraph("Inteligência Emocional (TEIQue)", self.section_style))
        teique_text = self._format_bullet_list(psychdynamic_list(psychodynamic, "teique"))
        story.append(Paragraph(teique_text, self.text_style))
        story.append(Spacer(0, 0.3 * cm))

        # --------------------------------------------------------------
        # Bloco: DASS-21
        # --------------------------------------------------------------

        story.append(Paragraph("Indicadores DASS-21", self.section_style))
        dass_text = self._format_bullet_list(psychdynamic_list(psychodynamic, "dass"))
        story.append(Paragraph(dass_text, self.text_style))
        story.append(Spacer(0, 0.3 * cm))

        # --------------------------------------------------------------
        # Bloco: Ligações Cruzadas
        # --------------------------------------------------------------

        story.append(Paragraph("Integrações Psicodinâmicas (Crosslinks)", self.section_style))
        cross_text = self._format_bullet_list(psychdynamic_list(psychodynamic, "crosslinks"))
        story.append(Paragraph(cross_text, self.text_style))
        story.append(Spacer(0, 0.5 * cm))

        return story


# ----------------------------------------------------------------------
# FUNÇÃO AUXILIAR
# ----------------------------------------------------------------------

def psychdynamic_list(psych: dict, key: str):
    """
    Recupera uma lista do bloco psicodinâmico com fallback seguro.
    """
    block = psych.get(key, {})
    if isinstance(block, list):
        return block
    if isinstance(block, dict):
        return list(block.values())
    return ["Dados não fornecidos"]
