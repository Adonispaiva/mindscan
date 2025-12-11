# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\report_templates\base_renderer.py
# Última atualização: 2025-12-11T09:59:21.292589

from reportlab.platypus import Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

class BaseRenderer:
    """
    Classe base para todos os renderizadores MindScan.
    Cada template herda desta classe e implementa o método build(story).
    """

    def __init__(self, test_id, results):
        self.test_id = test_id
        self.results = results
        self.styles = getSampleStyleSheet()
        self.story = []

    # --------------------------
    # Helpers universais
    # --------------------------
    def title(self, text):
        self.story.append(Paragraph(f"<b>{text}</b>", self.styles["Title"]))
        self.story.append(Spacer(1, 0.5 * cm))

    def heading(self, text):
        self.story.append(Paragraph(f"<b>{text}</b>", self.styles["Heading2"]))
        self.story.append(Spacer(1, 0.3 * cm))

    def paragraph(self, text):
        self.story.append(Paragraph(text, self.styles["BodyText"]))
        self.story.append(Spacer(1, 0.25 * cm))

    def page_break(self):
        self.story.append(PageBreak())

    # --------------------------
    # Método obrigatório
    # --------------------------
    def build(self):
        """
        Deve ser implementado nos renderers específicos.
        Retorna uma lista `story` compatível com reportlab.platypus.SimpleDocTemplate.
        """
        raise NotImplementedError("O renderer específico deve implementar .build().")
