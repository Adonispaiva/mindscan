# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\fluxo_psicodinamico_integrado.py
# Última atualização: 2025-12-11T09:59:21.168743

# Fluxo Psicodinâmico Integrado — MindScan Estendido
# Autor: Leo Vinci — Inovexa Software

from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import colors


class FluxoPsicodinamicoIntegradoPDF:

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title = self._title()
        self.text = self._text()

    def _title(self):
        st = self.styles["Heading1"]
        st.fontSize = 20
        st.textColor = colors.HexColor("#002F2F")
        st.spaceAfter = 14
        return st

    def _text(self):
        st = self.styles["BodyText"]
        st.fontSize = 11
        st.leading = 16
        return st

    def build(self, data: dict, story: list):

        story.append(Paragraph("Fluxo Psicodinâmico Integrado", self.title))
        story.append(Spacer(0, 0.4 * cm))

        if not data:
            story.append(Paragraph("Fluxo psicodinâmico não fornecido.", self.text))
            return story

        # Trata o texto como narrativa integrada
        narrative = data.get("narrative", "Nenhuma narrativa integrada informada.")

        story.append(Paragraph(narrative, self.text))
        story.append(Spacer(0, 1 * cm))

        return story
