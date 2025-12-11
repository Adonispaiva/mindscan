# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\carga_cognitiva.py
# Última atualização: 2025-12-11T09:59:21.168743

# Carga Cognitiva — MindScan Psicodinâmico
# Autor: Leo Vinci — Inovexa Software

from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import colors


class CargaCognitivaPDF:

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title = self._title()
        self.text = self._text()

    def _title(self):
        st = self.styles["Heading1"]
        st.fontSize = 20
        st.textColor = colors.HexColor("#00334E")
        st.spaceAfter = 14
        return st

    def _text(self):
        st = self.styles["BodyText"]
        st.fontSize = 11
        st.leading = 16
        return st

    def build(self, data: dict, story: list):

        story.append(Paragraph("Carga Cognitiva", self.title))
        story.append(Spacer(0, 0.4 * cm))

        if not data:
            story.append(Paragraph("Nenhuma informação de carga cognitiva disponível.", self.text))
            return story

        rows = [["Fator Cognitivo", "Impacto na Função"]]

        for key, value in data.items():
            rows.append([key, value])

        table = Table(rows, colWidths=[6 * cm, 12 * cm])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E2F0F7")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#00334E")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#00334E")),
            ("VALIGN", (0, 1), (-1, -1), "TOP")
        ]))

        story.append(table)
        story.append(Spacer(0, 1 * cm))

        return story
