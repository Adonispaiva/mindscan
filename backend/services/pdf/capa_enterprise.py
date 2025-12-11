# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\capa_enterprise.py
# Última atualização: 2025-12-11T09:59:21.168743

# D:\mindscan\backend\services\pdf\capa_enterprise.py
# ----------------------------------------------------
# Capa Enterprise do Relatório MindScan — SynMind
# Autor: Leo Vinci — Inovexa Software
#
# Esta capa é utilizada pelos templates:
# - Executive Renderer
# - Premium Renderer
#
# Ela segue o padrão visual corporativo:
# - Logo SynMind
# - Título padronizado
# - Gradiente ou fundo institucional
# - Metadados básicos do relatório

from reportlab.platypus import Paragraph, Spacer, Image, Frame
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import colors


class CapaEnterprise:
    """
    Classe responsável por construir a capa corporativa do PDF.
    Pode ser chamada diretamente pelos renderers Premium/Executive.
    """

    def __init__(self, assets_path: str):
        self.assets_path = assets_path
        self.styles = getSampleStyleSheet()
        self.title_style = self._build_title_style()

    # ----------------------------------------------------------------------
    # ESTILO
    # ----------------------------------------------------------------------

    def _build_title_style(self):
        style = self.styles["Title"]
        style.fontSize = 28
        style.leading = 32
        style.textColor = colors.HexColor("#003366")
        style.spaceAfter = 20
        return style

    # ----------------------------------------------------------------------
    # CONSTRUÇÃO DA CAPA
    # ----------------------------------------------------------------------

    def build(self, test_id: str, story: list):
        """
        Constrói a capa em cima de um story Platypus.
        """

        # Marca corporativa
        logo_path = f"{self.assets_path}/logos/synmind_logo.png"

        try:
            logo = Image(logo_path, width=6*cm, height=6*cm)
        except Exception:
            # fallback se logo não existir (ambientes de dev)
            logo = Paragraph("<b>SynMind</b>", self.styles["Heading1"])

        title = Paragraph("Relatório MindScan — Corporate Edition", self.title_style)

        meta = Paragraph(
            f"<font size=12>Test ID: {test_id}<br/>"
            f"Geração: automática — MindScan Engine</font>",
            self.styles["Normal"]
        )

        story.append(Spacer(0, 2*cm))
        story.append(logo)
        story.append(Spacer(0, 1*cm))
        story.append(title)
        story.append(Spacer(0, 0.5*cm))
        story.append(meta)
        story.append(Spacer(0, 4*cm))

        return story
