# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\conclusao.py
# Última atualização: 2025-12-11T09:59:21.168743

# D:\mindscan\backend\services\pdf\conclusao.py
# ------------------------------------------------
# Conclusão — MindScan
# Autor: Leo Vinci — Inovexa Software
#
# Esta página apresenta:
# - Mensagem final do relatório
# - Encerramento institucional
# - Assinatura da SynMind (marca do MindScan)
# - Observações finais e disclaimers executivos
#
# Usado por:
# - Premium Renderer
# - Executive Renderer

from reportlab.platypus import Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import colors


class ConclusaoPDF:
    """
    Constrói a página de conclusão do relatório MindScan.
    Uma finalização elegante, padronizada e institucional.
    """

    def __init__(self, assets_path: str = None):
        self.assets_path = assets_path
        self.styles = getSampleStyleSheet()
        self.title_style = self._style_title()
        self.text_style = self._style_text()
        self.disclaimer_style = self._style_disclaimer()

    # --------------------------------------------------------------
    # ESTILOS
    # --------------------------------------------------------------

    def _style_title(self):
        style = self.styles["Heading1"]
        style.fontSize = 18
        style.leading = 24
        style.textColor = colors.HexColor("#003366")
        style.spaceAfter = 14
        return style

    def _style_text(self):
        style = self.styles["BodyText"]
        style.fontSize = 11
        style.leading = 17
        style.textColor = colors.black
        style.spaceAfter = 14
        return style

    def _style_disclaimer(self):
        style = self.styles["Italic"]
        style.fontSize = 9
        style.leading = 12
        style.textColor = colors.HexColor("#555555")
        style.spaceAfter = 10
        return style

    # --------------------------------------------------------------
    # CONSTRUÇÃO DA PÁGINA
    # --------------------------------------------------------------

    def build(self, conclusion_data: dict, story: list):

        story.append(Paragraph("Conclusão", self.title_style))
        story.append(Spacer(0, 0.5 * cm))

        # ------------------------------------------------------------------
        # Mensagem final (customizável)
        # ------------------------------------------------------------------

        mensagem = conclusion_data.get(
            "mensagem",
            "Este relatório representa uma visão integrada do funcionamento psicológico, "
            "emocional, cognitivo e comportamental do indivíduo, traduzida em linguagem "
            "executiva para aplicação profissional."
        )

        story.append(Paragraph(mensagem, self.text_style))
        story.append(Spacer(0, 0.7 * cm))

        # ------------------------------------------------------------------
        # Assinatura / Marca corporativa
        # ------------------------------------------------------------------

        if self.assets_path:
            logo_path = f\"{self.assets_path}/logos/synmind_logo.png\"
            try:
                logo = Image(logo_path, width=4*cm, height=4*cm)
                story.append(logo)
                story.append(Spacer(0, 0.6 * cm))
            except Exception:
                story.append(Paragraph("<b>SynMind — Inovexa Software</b>", self.text_style))
                story.append(Spacer(0, 0.5 * cm))
        else:
            story.append(Paragraph("<b>SynMind — Inovexa Software</b>", self.text_style))
            story.append(Spacer(0, 0.5 * cm))

        # ------------------------------------------------------------------
        # Disclaimers finais
        # ------------------------------------------------------------------

        disclaimer_default = (
            "O MindScan é uma ferramenta avançada de análise psicodinâmica aplicada, "
            "não substituindo acompanhamento clínico ou psicológico quando necessário. "
            "Sua finalidade é apoiar decisões estratégicas, de desenvolvimento e gestão."
        )

        disclaimer = conclusion_data.get("disclaimer", disclaimer_default)

        story.append(Paragraph(disclaimer, self.disclaimer_style))
        story.append(Spacer(0, 1 * cm))

        return story
