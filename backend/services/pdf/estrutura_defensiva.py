# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\estrutura_defensiva.py
# Última atualização: 2025-12-11T09:59:21.168743

# Estrutura Defensiva — MindScan Psicodinâmico
# Autor: Leo Vinci — Inovexa Software

from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import colors


class EstruturaDefensivaPDF:

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title = self._title()
        self.section = self._section()
        self.text = self._text()

    def _title(self):
        st = self.styles["Heading1"]
        st.fontSize = 20
        st.textColor = colors.HexColor("#381870")
        st.spaceAfter = 14
        return st

    def _section(self):
        st = self.styles["Heading2"]
        st.fontSize = 14
        st.textColor = colors.HexColor("#4F2789")
        st.spaceAfter = 10
        return st

    def _text(self):
        st = self.styles["BodyText"]
        st.fontSize = 11
        st.leading = 16
        st.textColor = colors.black
        return st

    def build(self, data: dict, story: list):

        story.append(Paragraph("Estrutura Defensiva", self.title))
        story.append(Spacer(0, 0.4 * cm))

        if not data:
            story.append(Paragraph("Nenhum dado defensivo informado.", self.text))
            return story

        rows = [["Mecanismo", "Descrição"]]

        for key, value in data.items():
            rows.append([key, value])

        table = Table(rows, colWidths=[6 * cm, 12 * cm])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EDE4F8")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#381870")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#381870")),
            ("VALIGN", (0, 1), (-1, -1), "TOP")
        ]))

        story.append(table)
        story.append(Spacer(0, 1 * cm))

        return story
