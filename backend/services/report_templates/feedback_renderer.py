import os
from reportlab.lib.units import cm
from reportlab.platypus import Spacer, Paragraph, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

from .base_renderer import BaseRenderer
from .styles import SynMindTheme

class FeedbackRenderer(BaseRenderer):
    """
    Renderizador 'High-End' para o Candidato.
    Foco: Autoconhecimento, Acolhimento e Design Editorial.
    """
    
    def _setup_custom_styles(self):
        super()._setup_custom_styles()
        # Estilo de Título Editorial
        self.styles.add(ParagraphStyle(
            name='EditorialTitle',
            parent=self.styles['Heading1'],
            fontName=SynMindTheme.FONT_TITLE,
            fontSize=24,
            textColor=SynMindTheme.PRIMARY_BLUE,
            alignment=TA_CENTER,
            spaceAfter=20
        ))
        # Estilo de Texto Corrido (Justificado)
        self.styles.add(ParagraphStyle(
            name='EditorialBody',
            parent=self.styles['Normal'],
            fontName=SynMindTheme.FONT_BODY,
            fontSize=11,
            leading=14,
            textColor=SynMindTheme.TEXT_DARK,
            alignment=TA_JUSTIFY
        ))

    def build(self):
        # 1. Capa Imersiva
        self._build_cover()
        
        # 2. Introdução Acolhedora (Narrativa MI)
        self.page_break()
        self._build_intro()
        
        # 3. Gráficos de Personalidade
        self.page_break()
        self.heading("Sua Identidade Profissional")
        # Usa o gráfico de radar da Base, mas poderíamos customizar cores aqui
        big5 = self.results.get("big5", {})
        self.draw_radar_chart(big5, title="Mapa de Potências (BIG5)")
        
        # 4. Texto de Feedback (MI)
        mi_content = self.results.get("narrative", {}) # Vindo do MI Service
        if mi_content:
            self.story.append(Spacer(1, 1*cm))
            self.paragraph(f"<b>Resumo:</b> {mi_content.get('executive_summary', '')}", style="EditorialBody")
        
        return self.story

    def _build_cover(self):
        # Tenta carregar logo
        base_path = os.path.dirname(os.path.abspath(__file__))
        logo = os.path.join(base_path, "assets", "logos", "synmind_logo.png")
        
        if os.path.exists(logo):
            img = Image(logo, width=6*cm, height=2*cm)
            img.hAlign = 'CENTER'
            self.story.append(img)
            self.story.append(Spacer(1, 4*cm))
            
        self.story.append(Paragraph("RELATÓRIO DE<br/>FEEDBACK & DESENVOLVIMENTO", self.styles["EditorialTitle"]))
        self.story.append(Spacer(1, 1*cm))
        self.story.append(Paragraph(f"Preparado para: <b>{self.candidate_name}</b>", self.styles["BodyText"]))
        self.story.append(Spacer(1, 0.5*cm))
        self.story.append(Paragraph("<i>\"Conexão Viva. Transformação Real.\"</i>", self.styles["Italic"]))
        self.story.append(PageBreak())

    def _build_intro(self):
        self.heading("Sua Jornada Começa Aqui")
        texto = """
        Este relatório não é um rótulo, mas um mapa. Ele foi desenhado para revelar suas 
        potencialidades invisíveis e oferecer caminhos práticos para o seu desenvolvimento.
        Ao ler as próximas páginas, mantenha a mente aberta e curiosa sobre si mesmo.
        """
        self.story.append(Paragraph(texto, self.styles["EditorialBody"]))