# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\arquetipos_dominancia.py
# Última atualização: 2025-12-11T09:59:21.168743

# Arquétipos de Dominância — MindScan Psicodinâmico
# Autor: Leo Vinci — Inovexa Software

from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import colors


class ArquetiposDominanciaPDF:

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title = self._title()
        self.text = self._text()

    def _title(self):
        st = self.styles["Heading1"]
        st.fontSize = 20
        st.textColor = colors.HexColor("#0B3D2E")
        st.spaceAfter = 14
        return st

    def _text(self):
        st = self.styles["BodyText"]
        st.fontSize = 11
        st.leading = 16
        return st

    def build(self, data: dict, story: list):

        story.append(Paragraph("Arquétipos de Dominância", self.title))
        story.append(Spacer(0, 0.4 * cm))

        if not data:
            story.append(Paragraph("Nenhum arquétipo informado.", self.text))
            return story

        rows = [["Arquétipo", "Padrão de dominância"]]

        for key, value in data.items():
            rows.append([key, value])

        table = Table(rows, colWidths=[6 * cm, 12 * cm])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DCEFE9")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#0B3D2E")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#0B3D2E")),
            ("VALIGN", (0, 1), (-1, -1), "TOP")
        ]))

        story.append(table)
        story.append(Spacer(0, 1 * cm))

        return story
