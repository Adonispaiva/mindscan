import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.spider import SpiderChart

class BaseRenderer:
    """
    Classe base robusta para todos os renderizadores MindScan.
    Contém a identidade visual e componentes gráficos da SynMind.
    """

    def __init__(self, test_id, results, candidate_name="Candidato"):
        self.test_id = test_id
        self.results = results
        self.candidate_name = candidate_name
        self.styles = getSampleStyleSheet()
        self.story = []
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Define a identidade visual SynMind (Cores e Fontes)"""
        # CORREÇÃO: colors.HexColor com 'H' maiúsculo
        self.styles.add(ParagraphStyle(
            name='SynMindTitle',
            parent=self.styles['Title'],
            fontSize=22,
            textColor=colors.HexColor("#1A3A5A"),
            spaceAfter=20
        ))

    def add_logo(self, logo_path="assets/logos/synmind_logo.png"):
        """Adiciona o logo se existir"""
        if os.path.exists(logo_path):
            img = Image(logo_path, width=4*cm, height=1.5*cm)
            img.hAlign = 'RIGHT'
            self.story.append(img)
            self.story.append(Spacer(1, 1*cm))

    def draw_radar_chart(self, data_dict, title="Perfil Psicométrico"):
        """
        Gera um gráfico de radar (aranha) para o BIG5 ou TEIQue.
        """
        labels = list(data_dict.keys())
        values = [list(data_dict.values())]

        drawing = Drawing(400, 250)
        sc = SpiderChart()
        sc.x = 100
        sc.y = 25
        sc.width = 200
        sc.height = 200
        sc.data = values
        sc.labels = labels
        sc.strandLabels.format = '%d'
        # CORREÇÃO: colors.HexColor
        sc.fillColor = colors.HexColor("#E6F2FF")
        sc.strokeColor = colors.HexColor("#1A3A5A")
        
        drawing.add(sc)
        self.story.append(drawing)
        self.story.append(Paragraph(f"<center>{title}</center>", self.styles["Italic"]))
        self.story.append(Spacer(1, 1*cm))

    def add_score_table(self, data_rows, title="Detalhamento"):
        """Tabela estilizada para DASS-21 ou Competências"""
        self.heading(title)
        t = Table(data_rows, colWidths=[8*cm, 4*cm, 4*cm])
        t.setStyle(TableStyle([
            # CORREÇÃO: colors.HexColor
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1A3A5A")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ]))
        self.story.append(t)
        self.story.append(Spacer(1, 0.5*cm))

    def title(self, text):
        self.story.append(Paragraph(text, self.styles["SynMindTitle"]))

    def heading(self, text):
        self.story.append(Paragraph(f"<b>{text}</b>", self.styles["Heading2"]))
        self.story.append(Spacer(1, 0.3 * cm))

    def paragraph(self, text):
        self.story.append(Paragraph(text, self.styles["BodyText"]))
        self.story.append(Spacer(1, 0.25 * cm))

    def page_break(self):
        self.story.append(PageBreak())